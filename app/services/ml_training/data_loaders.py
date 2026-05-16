import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.ml_dataset_run import MlDatasetRun
from app.db.models.ml_feature_row import MlFeatureRow
from app.services.ml_training.feature_schema import get_training_columns


async def load_latest_successful_ml_dataset_run(
    session: AsyncSession,
    client_id: int,
) -> MlDatasetRun | None:
    """Load latest successful ML dataset run.
    Args:
        session (AsyncSession): Database session.
        client_id (int): Client identifier.
    """
    statement = (
        select(MlDatasetRun)
        .where(MlDatasetRun.client_id == client_id)
        .where(MlDatasetRun.status == 'success')
        .where(MlDatasetRun.is_success.is_(True))
        .order_by(MlDatasetRun.created_at.desc())
        .limit(1)
    )

    result = await session.execute(statement)

    return result.scalar_one_or_none()


async def load_successful_ml_dataset_run_by_id(
    session: AsyncSession,
    client_id: int,
    ml_dataset_run_id: int,
) -> MlDatasetRun | None:
    """Load successful ML dataset run by identifier.
    Args:
        session (AsyncSession): Database session.
        client_id (int): Client identifier.
        ml_dataset_run_id (int): ML dataset run identifier.
    """
    statement = (
        select(MlDatasetRun)
        .where(MlDatasetRun.id == ml_dataset_run_id)
        .where(MlDatasetRun.client_id == client_id)
        .where(MlDatasetRun.status == 'success')
        .where(MlDatasetRun.is_success.is_(True))
        .limit(1)
    )

    result = await session.execute(statement)

    return result.scalar_one_or_none()


async def resolve_ml_dataset_run(
    session: AsyncSession,
    client_id: int,
    ml_dataset_run_id: int | None,
) -> MlDatasetRun | None:
    """Resolve ML dataset run for training.
    Args:
        session (AsyncSession): Database session.
        client_id (int): Client identifier.
        ml_dataset_run_id (int | None): Optional ML dataset run identifier.
    """
    if ml_dataset_run_id is not None:
        return await load_successful_ml_dataset_run_by_id(
            session=session,
            client_id=client_id,
            ml_dataset_run_id=ml_dataset_run_id,
        )

    return await load_latest_successful_ml_dataset_run(
        session=session,
        client_id=client_id,
    )


async def load_ml_training_dataframe(
    session: AsyncSession,
    ml_dataset_run_id: int,
) -> pd.DataFrame:
    """Load ML training dataframe from materialized feature rows.
    Args:
        session (AsyncSession): Database session.
        ml_dataset_run_id (int): ML dataset run identifier.
    """
    statement = select(MlFeatureRow).where(
        MlFeatureRow.ml_dataset_run_id == ml_dataset_run_id,
    )

    result = await session.execute(statement)
    feature_rows = result.scalars().all()

    rows = [
        {
            'client_id': feature_row.client_id,
            'company_id': feature_row.company_id,
            'vacancy_id': feature_row.vacancy_id,
            'date_day': feature_row.date_day,
            'callbacks': feature_row.callbacks,
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
            'publication_activity_level': (
                feature_row.publication_activity_level
            ),
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
        for feature_row in feature_rows
    ]

    if not rows:
        return pd.DataFrame(columns=get_training_columns())

    dataframe = pd.DataFrame(rows)

    return dataframe[get_training_columns()]
