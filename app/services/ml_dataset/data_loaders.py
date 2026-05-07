from datetime import datetime

import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.categorical_feature import CategoricalFeature
from app.db.models.feature_run import FeatureRun
from app.db.models.publication_activity_feature import (
    PublicationActivityFeature,
)
from app.db.models.salary_feature import SalaryFeature
from app.db.models.text_feature import TextFeature
from app.db.models.time_feature import TimeFeature
from app.db.models.vacancy_snapshot import VacancySnapshot


async def load_latest_successful_feature_run(
    session: AsyncSession,
    client_id: int,
    date_from: datetime,
    date_to: datetime,
    feature_name_prefix: str,
) -> FeatureRun | None:
    """Load latest successful feature run by name prefix.
    Args:
        session (AsyncSession): Database session.
        client_id (int): Client identifier.
        date_from (datetime): Feature period start.
        date_to (datetime): Feature period end.
        feature_name_prefix (str): Feature run name prefix.
    """
    statement = (
        select(FeatureRun)
        .where(FeatureRun.client_id == client_id)
        .where(FeatureRun.date_from == date_from)
        .where(FeatureRun.date_to == date_to)
        .where(FeatureRun.status == 'success')
        .where(FeatureRun.feature_run_name.like(f'{feature_name_prefix}%'))
        .order_by(FeatureRun.created_at.desc())
        .limit(1)
    )

    result = await session.execute(statement)

    return result.scalar_one_or_none()


async def load_target_snapshot_data(
    session: AsyncSession,
    client_id: int,
    date_from: datetime,
    date_to: datetime,
) -> pd.DataFrame:
    """Load target values from vacancy snapshots.
    Args:
        session (AsyncSession): Database session.
        client_id (int): Client identifier.
        date_from (datetime): Dataset period start.
        date_to (datetime): Dataset period end.
    """
    statement = (
        select(VacancySnapshot)
        .where(VacancySnapshot.client_id == client_id)
        .where(VacancySnapshot.date_day >= date_from)
        .where(VacancySnapshot.date_day <= date_to)
    )

    result = await session.execute(statement)
    snapshots = result.scalars().all()

    rows = [
        {
            'client_id': snapshot.client_id,
            'company_id': snapshot.company_id,
            'vacancy_id': snapshot.vacancy_id,
            'date_day': snapshot.date_day,
            'callbacks': snapshot.callbacks or 0,
        }
        for snapshot in snapshots
    ]

    return pd.DataFrame(rows)


async def load_salary_feature_data(
    session: AsyncSession,
    feature_run_id: int,
) -> pd.DataFrame:
    """Load salary feature data.
    Args:
        session (AsyncSession): Database session.
        feature_run_id (int): Feature run identifier.
    """
    statement = select(SalaryFeature).where(
        SalaryFeature.feature_run_id == feature_run_id,
    )

    result = await session.execute(statement)
    features = result.scalars().all()

    rows = [
        {
            'client_id': feature.client_id,
            'company_id': feature.company_id,
            'vacancy_id': feature.vacancy_id,
            'date_day': feature.date_day,
            'salary_mid': feature.salary_mid,
            'salary_is_specified': feature.salary_is_specified,
            'salary_ratio_to_market_by_city': (
                feature.salary_ratio_to_market_by_city
            ),
            'salary_ratio_to_market_by_profile': (
                feature.salary_ratio_to_market_by_profile
            ),
            'salary_ratio_to_market_by_city_profile': (
                feature.salary_ratio_to_market_by_city_profile
            ),
        }
        for feature in features
    ]

    return pd.DataFrame(rows)


async def load_publication_activity_feature_data(
    session: AsyncSession,
    feature_run_id: int,
) -> pd.DataFrame:
    """Load publication activity feature data.
    Args:
        session (AsyncSession): Database session.
        feature_run_id (int): Feature run identifier.
    """
    statement = select(PublicationActivityFeature).where(
        PublicationActivityFeature.feature_run_id == feature_run_id,
    )

    result = await session.execute(statement)
    features = result.scalars().all()

    rows = [
        {
            'client_id': feature.client_id,
            'company_id': feature.company_id,
            'vacancy_id': feature.vacancy_id,
            'date_day': feature.date_day,
            'publication_activity_level': (
                feature.publication_activity_level
            ),
            'days_since_last_publication_activity': (
                feature.days_since_last_publication_activity
            ),
        }
        for feature in features
    ]

    return pd.DataFrame(rows)


async def load_text_feature_data(
    session: AsyncSession,
    feature_run_id: int,
) -> pd.DataFrame:
    """Load text feature data.
    Args:
        session (AsyncSession): Database session.
        feature_run_id (int): Feature run identifier.
    """
    statement = select(TextFeature).where(
        TextFeature.feature_run_id == feature_run_id,
    )

    result = await session.execute(statement)
    features = result.scalars().all()

    rows = [
        {
            'client_id': feature.client_id,
            'company_id': feature.company_id,
            'vacancy_id': feature.vacancy_id,
            'date_day': feature.date_day,
            'title_length': feature.title_length,
            'description_length': feature.description_length,
            'title_word_count': feature.title_word_count,
            'description_word_count': feature.description_word_count,
            'has_description': feature.has_description,
            'description_is_empty': feature.description_is_empty,
            'has_salary_mention': feature.has_salary_mention,
            'has_schedule_mention': feature.has_schedule_mention,
            'has_requirements_mention': feature.has_requirements_mention,
            'has_benefits_mention': feature.has_benefits_mention,
            'has_call_to_action': feature.has_call_to_action,
        }
        for feature in features
    ]

    return pd.DataFrame(rows)


async def load_time_feature_data(
    session: AsyncSession,
    feature_run_id: int,
) -> pd.DataFrame:
    """Load time feature data.
    Args:
        session (AsyncSession): Database session.
        feature_run_id (int): Feature run identifier.
    """
    statement = select(TimeFeature).where(
        TimeFeature.feature_run_id == feature_run_id,
    )

    result = await session.execute(statement)
    features = result.scalars().all()

    rows = [
        {
            'client_id': feature.client_id,
            'company_id': feature.company_id,
            'vacancy_id': feature.vacancy_id,
            'date_day': feature.date_day,
            'publication_hour': feature.publication_hour,
            'publication_day_of_week': feature.publication_day_of_week,
            'publication_month': feature.publication_month,
            'publication_week': feature.publication_week,
            'is_weekend': feature.is_weekend,
            'vacancy_age_days': feature.vacancy_age_days,
        }
        for feature in features
    ]

    return pd.DataFrame(rows)


async def load_categorical_feature_data(
    session: AsyncSession,
    feature_run_id: int,
) -> pd.DataFrame:
    """Load categorical feature data.
    Args:
        session (AsyncSession): Database session.
        feature_run_id (int): Feature run identifier.
    """
    statement = select(CategoricalFeature).where(
        CategoricalFeature.feature_run_id == feature_run_id,
    )

    result = await session.execute(statement)
    features = result.scalars().all()

    rows = [
        {
            'client_id': feature.client_id,
            'company_id': feature.company_id,
            'vacancy_id': feature.vacancy_id,
            'date_day': feature.date_day,
            'city': feature.city,
            'region': feature.region,
            'profile': feature.profile,
            'employment_type': feature.employment_type,
            'work_experience': feature.work_experience,
            'work_schedule': feature.work_schedule,
        }
        for feature in features
    ]

    return pd.DataFrame(rows)
