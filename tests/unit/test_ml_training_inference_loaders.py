from datetime import datetime
from typing import Any

import pytest

from app.db.models.ml_feature_row import MlFeatureRow
from app.db.models.ml_training_run import MlTrainingRun
from app.services.ml_training.constants import ML_MODEL_TYPE_CATBOOST_REGRESSOR
from app.services.ml_training.constants import ML_TARGET_CALLBACKS
from app.services.ml_training.constants import ML_TRAINING_STATUS_SUCCESS
from app.services.ml_training.feature_schema import IDENTIFIER_COLUMNS
from app.services.ml_training.feature_schema import get_feature_columns
from app.services.ml_training.inference_loaders import build_feature_record
from app.services.ml_training.inference_loaders import get_inference_columns
from app.services.ml_training.inference_loaders import load_inference_dataframe
from app.services.ml_training.inference_loaders import resolve_training_run
from app.services.ml_training.inference_loaders import validate_training_run


class FakeResult:
    """Fake SQLAlchemy execute result."""

    def __init__(self, value: Any = None, rows: list[Any] | None = None):
        """Initialize fake result.
        Args:
            value (Any): Scalar result value.
            rows (list[Any] | None): Scalar rows."""
        self.value = value
        self.rows = rows or []

    def scalar_one_or_none(self) -> Any:
        """Return scalar value.
        Args:
            """
        return self.value

    def scalars(self) -> 'FakeResult':
        """Return fake scalar result.
        Args:
            """
        return self

    def all(self) -> list[Any]:
        """Return fake scalar rows.
        Args:
            """
        return self.rows


class FakeSession:
    """Fake async database session."""

    def __init__(self, result: FakeResult):
        """Initialize fake session.
        Args:
            result (FakeResult): Fake execute result."""
        self.result = result
        self.statement = None

    async def execute(self, statement: Any) -> FakeResult:
        """Execute fake statement.
        Args:
            statement (Any): SQLAlchemy statement."""
        self.statement = statement

        return self.result


def build_training_run(
    ml_dataset_run_id: int | None = 10,
    model_path: str | None = 'artifacts/models/pipeline_3/model.cbm',
) -> MlTrainingRun:
    """Build ML training run for loader tests.
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


def build_feature_row() -> MlFeatureRow:
    """Build ML feature row for loader tests.
    Args:
        """
    return MlFeatureRow(
        id=1,
        ml_dataset_run_id=10,
        client_id=1,
        company_id=2,
        vacancy_id=100,
        date_day=datetime(2025, 9, 1),
        callbacks=5,
        salary_mid=1500.0,
        salary_is_specified=True,
        salary_ratio_to_market_by_city=1.0,
        salary_ratio_to_market_by_profile=0.95,
        salary_ratio_to_market_by_city_profile=1.05,
        publication_activity_level=2,
        days_since_last_publication_activity=0,
        title_length=25,
        description_length=120,
        title_word_count=3,
        description_word_count=20,
        has_description=True,
        description_is_empty=False,
        has_salary_mention=True,
        has_schedule_mention=True,
        has_requirements_mention=True,
        has_benefits_mention=False,
        has_call_to_action=True,
        publication_hour=9,
        publication_day_of_week=1,
        publication_month=9,
        publication_week=36,
        is_weekend=False,
        vacancy_age_days=4,
        city='Berlin',
        region='Berlin',
        profile='Courier',
        employment_type='Full-time',
        work_experience='1 year',
        work_schedule='Day shift',
        created_at=datetime(2025, 9, 1, 10, 0, 0),
    )


def test_get_inference_columns() -> None:
    """Test inference column list.
    Args:
        """
    result = get_inference_columns()

    assert result == IDENTIFIER_COLUMNS + get_feature_columns()
    assert 'callbacks' not in result


def test_validate_training_run() -> None:
    """Test ML training run validation.
    Args:
        """
    ml_training_run = build_training_run()

    result = validate_training_run(ml_training_run=ml_training_run)

    assert result == ml_training_run


def test_validate_missing_training() -> None:
    """Test missing ML training run validation.
    Args:
        """
    with pytest.raises(ValueError, match='was not found'):
        validate_training_run(ml_training_run=None)


def test_validate_missing_dataset() -> None:
    """Test ML training run without dataset identifier.
    Args:
        """
    ml_training_run = build_training_run(ml_dataset_run_id=None)

    with pytest.raises(ValueError, match='no ML dataset run identifier'):
        validate_training_run(ml_training_run=ml_training_run)


def test_validate_missing_model() -> None:
    """Test ML training run without model artifact path.
    Args:
        """
    ml_training_run = build_training_run(model_path=None)

    with pytest.raises(ValueError, match='no model artifact path'):
        validate_training_run(ml_training_run=ml_training_run)


def test_build_feature_record() -> None:
    """Test feature record building from database row.
    Args:
        """
    feature_row = build_feature_row()

    result = build_feature_record(feature_row=feature_row)

    assert result['client_id'] == 1
    assert result['company_id'] == 2
    assert result['vacancy_id'] == 100
    assert result['salary_mid'] == 1500.0
    assert result['city'] == 'Berlin'
    assert 'callbacks' not in result


@pytest.mark.asyncio
async def test_resolve_training_run() -> None:
    """Test ML training run resolving.
    Args:
        """
    ml_training_run = build_training_run()
    session = FakeSession(result=FakeResult(value=ml_training_run))

    result = await resolve_training_run(
        session=session,
        client_id=1,
        ml_training_run_id=1,
    )

    assert result == ml_training_run
    assert session.statement is not None


@pytest.mark.asyncio
async def test_load_inference_dataframe() -> None:
    """Test inference dataframe loading.
    Args:
        """
    feature_row = build_feature_row()
    session = FakeSession(result=FakeResult(rows=[feature_row]))

    result = await load_inference_dataframe(
        session=session,
        ml_dataset_run_id=10,
    )

    assert list(result.columns) == get_inference_columns()
    assert len(result) == 1
    assert result.loc[0, 'client_id'] == 1
    assert result.loc[0, 'vacancy_id'] == 100
    assert result.loc[0, 'city'] == 'Berlin'
    assert 'callbacks' not in result.columns


@pytest.mark.asyncio
async def test_load_empty_dataframe() -> None:
    """Test empty inference dataframe loading.
    Args:
        """
    session = FakeSession(result=FakeResult(rows=[]))

    result = await load_inference_dataframe(
        session=session,
        ml_dataset_run_id=10,
    )

    assert list(result.columns) == get_inference_columns()
    assert result.empty
