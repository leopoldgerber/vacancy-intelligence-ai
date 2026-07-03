from typing import Any

import pytest

import app.api.routes.ml_inference as ml_inference_route
from app.api.schemas.ml_inference import MlInferenceRunRequest
from app.services.ml_training.run_ml_inference_pipeline import (
    MlInferencePipelineResult,
)


def build_pipeline_result() -> MlInferencePipelineResult:
    """Build ML inference pipeline result for API tests.
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

    return MlInferencePipelineResult(
        ml_training_run_id=1,
        training_run_name='ml_training_2026-06-21_21-23-44',
        ml_dataset_run_id=10,
        client_id=1,
        model_path='artifacts/models/pipeline_3/model.cbm',
        row_count=2,
        prediction_row_count=2,
        predictions=[1.5, 2.5],
        prediction_rows=prediction_rows,
        report_name='ml_inference_2026-06-21_21-23-44.md',
        report_path=(
            'artifacts/reports/pipeline_3/inference/'
            'ml_inference_2026-06-21_21-23-44.md'
        ),
    )


@pytest.mark.asyncio
async def test_run_pipeline_3_inference(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test Pipeline 3 inference API route.
    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest monkeypatch fixture."""
    pipeline_result = build_pipeline_result()

    async def fake_run_inference(
        client_id: int,
        ml_training_run_id: int | None = None,
    ) -> MlInferencePipelineResult:
        """Run fake ML inference service.
        Args:
            client_id (int): Client identifier.
            ml_training_run_id (int | None):
                Optional ML training run identifier."""
        assert client_id == 1
        assert ml_training_run_id == 1

        return pipeline_result

    monkeypatch.setattr(
        ml_inference_route,
        'run_ml_inference',
        fake_run_inference,
    )

    request = MlInferenceRunRequest(
        client_id=1,
        ml_training_run_id=1,
    )

    result = await ml_inference_route.run_pipeline_3_inference(
        request=request,
    )

    assert result.ml_training_run_id == 1
    assert result.training_run_name == 'ml_training_2026-06-21_21-23-44'
    assert result.ml_dataset_run_id == 10
    assert result.client_id == 1
    assert result.model_path == 'artifacts/models/pipeline_3/model.cbm'
    assert result.row_count == 2
    assert result.prediction_row_count == 2
    assert result.predictions == [1.5, 2.5]
    assert len(result.prediction_rows) == 2
    assert result.report_name == 'ml_inference_2026-06-21_21-23-44.md'
    assert result.report_path is not None


def test_inference_response_schema() -> None:
    """Test ML inference response schema.
    Args:
        """
    pipeline_result = build_pipeline_result()

    response_data: dict[str, Any] = {
        'ml_training_run_id': pipeline_result.ml_training_run_id,
        'training_run_name': pipeline_result.training_run_name,
        'ml_dataset_run_id': pipeline_result.ml_dataset_run_id,
        'client_id': pipeline_result.client_id,
        'model_path': pipeline_result.model_path,
        'row_count': pipeline_result.row_count,
        'prediction_row_count': pipeline_result.prediction_row_count,
        'predictions': pipeline_result.predictions,
        'prediction_rows': pipeline_result.prediction_rows,
        'report_name': pipeline_result.report_name,
        'report_path': pipeline_result.report_path,
    }

    result = ml_inference_route.MlInferenceRunResponse(**response_data)

    assert result.ml_training_run_id == 1
    assert result.prediction_row_count == 2
    assert result.predictions == [1.5, 2.5]
    assert result.report_name == 'ml_inference_2026-06-21_21-23-44.md'
    assert result.report_path is not None
