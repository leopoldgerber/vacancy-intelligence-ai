from datetime import datetime
from typing import Any

import pandas as pd
import pytest

import app.services.ml_training.run_ml_inference_pipeline as inference_pipeline
from app.db.models.ml_training_run import MlTrainingRun
from app.services.ml_training.constants import ML_MODEL_TYPE_CATBOOST_REGRESSOR
from app.services.ml_training.constants import ML_TARGET_CALLBACKS
from app.services.ml_training.constants import ML_TRAINING_STATUS_SUCCESS
from app.services.ml_training.inference_service import MlInferenceResult
from app.services.ml_training.run_ml_inference_pipeline import (
    MlInferencePipelineResult,
    build_pipeline_result,
    run_inference_pipeline,
)


class FakeSession:
    """Fake async database session."""


def build_training_run(
    ml_dataset_run_id: int | None = 10,
    model_path: str | None = 'artifacts/models/pipeline_3/model.cbm',
) -> MlTrainingRun:
    """Build ML training run for inference pipeline tests.
    Args:
        ml_dataset_run_id (int | None): ML dataset run identifier.
        model_path (str | None): Model artifact path."""
    return MlTrainingRun(
        id=1,
        training_run_name='ml_training_2026-06-21_21-23-44',
        ml_dataset_run_id=ml_dataset_run_id,
        client_id=1,
        model_type=ML_MODEL_TYPE_CATBOOST_REGRESSOR,
        target_name=ML_TARGET_CALLBACKS,
        model_params_json=None,
        feature_importance_json=None,
        prediction_diagnostics_json=None,
        status=ML_TRAINING_STATUS_SUCCESS,
        is_success=True,
        train_row_count=80,
        test_row_count=20,
        prediction_row_count=20,
        metric_mae=0.31,
        metric_rmse=0.86,
        metric_r2=0.09,
        baseline_mae=0.33,
        mean_target=0.21,
        model_path=model_path,
        report_name='ml_training_2026-06-21_21-23-44.md',
        created_at=datetime(2026, 6, 21, 21, 23, 44),
    )


def build_inference_result() -> MlInferenceResult:
    """Build ML inference result for pipeline tests.
    Args:
        """
    prediction_rows = [
        {
            'source_row_index': 0,
            'predicted_value': 1.5,
            'client_id': 1,
            'company_id': 10,
            'vacancy_id': 100,
        },
        {
            'source_row_index': 1,
            'predicted_value': 2.5,
            'client_id': 1,
            'company_id': 11,
            'vacancy_id': 101,
        },
    ]

    return MlInferenceResult(
        model_path='artifacts/models/pipeline_3/model.cbm',
        row_count=2,
        prediction_row_count=2,
        predictions=[1.5, 2.5],
        prediction_rows=prediction_rows,
    )


def test_build_pipeline_result() -> None:
    """Test ML inference pipeline result building.
    Args:
        """
    ml_training_run = build_training_run()
    inference_result = build_inference_result()

    result = build_pipeline_result(
        ml_training_run=ml_training_run,
        inference_result=inference_result,
    )

    assert result == MlInferencePipelineResult(
        ml_training_run_id=1,
        training_run_name='ml_training_2026-06-21_21-23-44',
        ml_dataset_run_id=10,
        client_id=1,
        model_path='artifacts/models/pipeline_3/model.cbm',
        row_count=2,
        prediction_row_count=2,
        predictions=[1.5, 2.5],
        prediction_rows=inference_result.prediction_rows,
    )


def test_build_result_missing_dataset() -> None:
    """Test ML inference pipeline result without dataset identifier.
    Args:
        """
    ml_training_run = build_training_run(ml_dataset_run_id=None)
    inference_result = build_inference_result()

    with pytest.raises(ValueError, match='no ML dataset run identifier'):
        build_pipeline_result(
            ml_training_run=ml_training_run,
            inference_result=inference_result,
        )


def test_build_result_missing_model() -> None:
    """Test ML inference pipeline result without model artifact path.
    Args:
        """
    ml_training_run = build_training_run(model_path=None)
    inference_result = build_inference_result()

    with pytest.raises(ValueError, match='no model artifact path'):
        build_pipeline_result(
            ml_training_run=ml_training_run,
            inference_result=inference_result,
        )


@pytest.mark.asyncio
async def test_run_inference_pipeline(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test DB-backed ML inference pipeline orchestration.
    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest monkeypatch fixture."""
    session = FakeSession()
    ml_training_run = build_training_run()
    inference_dataframe = pd.DataFrame(
        {
            'client_id': [1, 1],
            'company_id': [10, 11],
            'vacancy_id': [100, 101],
        },
    )
    inference_result = build_inference_result()

    async def fake_resolve_training(
        session: Any,
        client_id: int,
        ml_training_run_id: int | None,
    ) -> MlTrainingRun | None:
        """Resolve fake ML training run.
        Args:
            session (Any): Fake database session.
            client_id (int): Client identifier.
            ml_training_run_id (int | None):
                Optional training run identifier."""
        assert client_id == 1
        assert ml_training_run_id == 1

        return ml_training_run

    async def fake_load_dataframe(
        session: Any,
        ml_dataset_run_id: int,
    ) -> pd.DataFrame:
        """Load fake inference dataframe.
        Args:
            session (Any): Fake database session.
            ml_dataset_run_id (int): ML dataset run identifier."""
        assert ml_dataset_run_id == 10

        return inference_dataframe

    def fake_run_inference(
        model_path: str,
        data: pd.DataFrame,
    ) -> MlInferenceResult:
        """Run fake ML inference.
        Args:
            model_path (str): Model artifact path.
            data (pd.DataFrame): Source inference dataframe."""
        assert model_path == 'artifacts/models/pipeline_3/model.cbm'
        assert data.equals(inference_dataframe)

        return inference_result

    monkeypatch.setattr(
        inference_pipeline,
        'resolve_training_run',
        fake_resolve_training,
    )
    monkeypatch.setattr(
        inference_pipeline,
        'load_inference_dataframe',
        fake_load_dataframe,
    )
    monkeypatch.setattr(
        inference_pipeline,
        'run_ml_inference',
        fake_run_inference,
    )

    result = await run_inference_pipeline(
        session=session,
        client_id=1,
        ml_training_run_id=1,
    )

    assert result.ml_training_run_id == 1
    assert result.training_run_name == 'ml_training_2026-06-21_21-23-44'
    assert result.ml_dataset_run_id == 10
    assert result.client_id == 1
    assert result.row_count == 2
    assert result.prediction_row_count == 2
    assert result.predictions == [1.5, 2.5]


@pytest.mark.asyncio
async def test_run_inference_missing_training(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test DB-backed ML inference pipeline without training run.
    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest monkeypatch fixture."""
    session = FakeSession()

    async def fake_resolve_training(
        session: Any,
        client_id: int,
        ml_training_run_id: int | None,
    ) -> MlTrainingRun | None:
        """Resolve missing ML training run.
        Args:
            session (Any): Fake database session.
            client_id (int): Client identifier.
            ml_training_run_id (int | None):
                Optional training run identifier."""
        return None

    monkeypatch.setattr(
        inference_pipeline,
        'resolve_training_run',
        fake_resolve_training,
    )

    with pytest.raises(ValueError, match='was not found'):
        await run_inference_pipeline(
            session=session,
            client_id=1,
            ml_training_run_id=None,
        )
