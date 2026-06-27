import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.ml_feature_row import MlFeatureRow
from app.db.models.ml_training_run import MlTrainingRun
from app.services.ml_training.constants import ML_MODEL_TYPE_CATBOOST_REGRESSOR
from app.services.ml_training.constants import ML_TARGET_CALLBACKS
from app.services.ml_training.constants import ML_TRAINING_STATUS_SUCCESS
from app.services.ml_training.feature_schema import IDENTIFIER_COLUMNS
from app.services.ml_training.feature_schema import get_feature_columns


def get_inference_columns() -> list[str]:
    """Get columns needed for model inference.
    Args:
        """
    return IDENTIFIER_COLUMNS + get_feature_columns()


async def load_latest_training(
    session: AsyncSession,
    client_id: int,
) -> MlTrainingRun | None:
    """Load latest successful ML training run for inference.
    Args:
        session (AsyncSession): Database session.
        client_id (int): Client identifier."""
    statement = (
        select(MlTrainingRun)
        .where(MlTrainingRun.client_id == client_id)
        .where(MlTrainingRun.status == ML_TRAINING_STATUS_SUCCESS)
        .where(MlTrainingRun.is_success.is_(True))
        .where(MlTrainingRun.model_type == ML_MODEL_TYPE_CATBOOST_REGRESSOR)
        .where(MlTrainingRun.target_name == ML_TARGET_CALLBACKS)
        .where(MlTrainingRun.ml_dataset_run_id.is_not(None))
        .where(MlTrainingRun.model_path.is_not(None))
        .order_by(MlTrainingRun.created_at.desc())
        .limit(1)
    )

    result = await session.execute(statement)

    return result.scalar_one_or_none()


async def load_training_by_id(
    session: AsyncSession,
    client_id: int,
    ml_training_run_id: int,
) -> MlTrainingRun | None:
    """Load successful ML training run by identifier.
    Args:
        session (AsyncSession): Database session.
        client_id (int): Client identifier.
        ml_training_run_id (int): ML training run identifier."""
    statement = (
        select(MlTrainingRun)
        .where(MlTrainingRun.id == ml_training_run_id)
        .where(MlTrainingRun.client_id == client_id)
        .where(MlTrainingRun.status == ML_TRAINING_STATUS_SUCCESS)
        .where(MlTrainingRun.is_success.is_(True))
        .where(MlTrainingRun.model_type == ML_MODEL_TYPE_CATBOOST_REGRESSOR)
        .where(MlTrainingRun.target_name == ML_TARGET_CALLBACKS)
        .where(MlTrainingRun.ml_dataset_run_id.is_not(None))
        .where(MlTrainingRun.model_path.is_not(None))
        .limit(1)
    )

    result = await session.execute(statement)

    return result.scalar_one_or_none()


async def resolve_training_run(
    session: AsyncSession,
    client_id: int,
    ml_training_run_id: int | None,
) -> MlTrainingRun | None:
    """Resolve ML training run for inference.
    Args:
        session (AsyncSession): Database session.
        client_id (int): Client identifier.
        ml_training_run_id (int | None):
            Optional ML training run identifier."""
    if ml_training_run_id is not None:
        return await load_training_by_id(
            session=session,
            client_id=client_id,
            ml_training_run_id=ml_training_run_id,
        )

    return await load_latest_training(
        session=session,
        client_id=client_id,
    )


def validate_training_run(
    ml_training_run: MlTrainingRun | None,
) -> MlTrainingRun:
    """Validate ML training run for inference.
    Args:
        ml_training_run (MlTrainingRun | None): ML training run."""
    if ml_training_run is None:
        raise ValueError('Successful ML training run was not found.')

    if ml_training_run.ml_dataset_run_id is None:
        raise ValueError('ML training run has no ML dataset run identifier.')

    if not ml_training_run.model_path:
        raise ValueError('ML training run has no model artifact path.')

    return ml_training_run


def build_feature_record(feature_row: MlFeatureRow) -> dict[str, object]:
    """Build inference feature record from database row.
    Args:
        feature_row (MlFeatureRow): Materialized ML feature row."""
    return {
        'client_id': feature_row.client_id,
        'company_id': feature_row.company_id,
        'vacancy_id': feature_row.vacancy_id,
        'date_day': feature_row.date_day,
        'salary_mid': feature_row.salary_mid,
        'salary_is_specified': feature_row.salary_is_specified,
        'salary_ratio_to_market_by_city': (
            feature_row.salary_ratio_to_market_by_city
        ),
        'salary_ratio_to_market_by_profile': (
            feature_row.salary_ratio_to_market_by_profile
        ),
        'salary_ratio_to_market_by_city_profile': (
            feature_row.salary_ratio_to_market_by_city_profile
        ),
        'publication_activity_level': feature_row.publication_activity_level,
        'days_since_last_publication_activity': (
            feature_row.days_since_last_publication_activity
        ),
        'title_length': feature_row.title_length,
        'description_length': feature_row.description_length,
        'title_word_count': feature_row.title_word_count,
        'description_word_count': feature_row.description_word_count,
        'has_description': feature_row.has_description,
        'description_is_empty': feature_row.description_is_empty,
        'has_salary_mention': feature_row.has_salary_mention,
        'has_schedule_mention': feature_row.has_schedule_mention,
        'has_requirements_mention': feature_row.has_requirements_mention,
        'has_benefits_mention': feature_row.has_benefits_mention,
        'has_call_to_action': feature_row.has_call_to_action,
        'publication_hour': feature_row.publication_hour,
        'publication_day_of_week': feature_row.publication_day_of_week,
        'publication_month': feature_row.publication_month,
        'publication_week': feature_row.publication_week,
        'is_weekend': feature_row.is_weekend,
        'vacancy_age_days': feature_row.vacancy_age_days,
        'city': feature_row.city,
        'region': feature_row.region,
        'profile': feature_row.profile,
        'employment_type': feature_row.employment_type,
        'work_experience': feature_row.work_experience,
        'work_schedule': feature_row.work_schedule,
    }


async def load_inference_dataframe(
    session: AsyncSession,
    ml_dataset_run_id: int,
) -> pd.DataFrame:
    """Load ML inference dataframe from materialized feature rows.
    Args:
        session (AsyncSession): Database session.
        ml_dataset_run_id (int): ML dataset run identifier."""
    statement = (
        select(MlFeatureRow)
        .where(MlFeatureRow.ml_dataset_run_id == ml_dataset_run_id)
        .order_by(MlFeatureRow.date_day.asc(), MlFeatureRow.id.asc())
    )

    result = await session.execute(statement)
    feature_rows = result.scalars().all()
    rows = [
        build_feature_record(feature_row=feature_row)
        for feature_row in feature_rows
    ]

    if not rows:
        return pd.DataFrame(columns=get_inference_columns())

    dataframe = pd.DataFrame(rows)

    return dataframe[get_inference_columns()]
