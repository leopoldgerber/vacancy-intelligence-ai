from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.feature_run import FeatureRun
from app.db.models.publication_activity_feature import (
    PublicationActivityFeature,
)
from app.db.models.salary_feature import SalaryFeature
from app.db.models.text_feature import TextFeature
from app.db.models.time_feature import TimeFeature


async def save_feature_run(
    session: AsyncSession,
    feature_run_name: str,
    client_id: int,
    date_from: datetime,
    date_to: datetime,
    status: str,
    is_success: bool,
    snapshot_count: int,
    feature_count: int,
    report_name: str,
) -> FeatureRun:
    """Save feature engineering run.
    Args:
        session (AsyncSession): Database session.
        feature_run_name (str): Feature run name.
        client_id (int): Client identifier.
        date_from (datetime): Feature period start.
        date_to (datetime): Feature period end.
        status (str): Feature run status.
        is_success (bool): Whether feature run is successful.
        snapshot_count (int): Number of snapshots in input.
        feature_count (int): Number of feature rows created.
        report_name (str): Feature report name.
    """
    feature_run = FeatureRun(
        feature_run_name=feature_run_name,
        client_id=client_id,
        date_from=date_from,
        date_to=date_to,
        status=status,
        is_success=is_success,
        snapshot_count=snapshot_count,
        feature_count=feature_count,
        report_name=report_name,
    )

    session.add(feature_run)
    await session.flush()

    return feature_run


async def save_salary_features(
    session: AsyncSession,
    salary_feature_rows: list[dict[str, int | float | bool | datetime]],
) -> list[SalaryFeature]:
    """Save salary feature rows.
    Args:
        session (AsyncSession): Database session.
        salary_feature_rows (list[dict[str, int | float | bool | datetime]]):
            Salary feature rows.
    """
    salary_features = [
        SalaryFeature(**salary_feature_row)
        for salary_feature_row in salary_feature_rows
    ]

    session.add_all(salary_features)
    await session.flush()

    return salary_features


async def save_publication_activity_features(
    session: AsyncSession,
    publication_activity_feature_rows: list[dict[str, int | datetime]],
) -> list[PublicationActivityFeature]:
    """Save publication activity feature rows.
    Args:
        session (AsyncSession): Database session.
        publication_activity_feature_rows (list[dict[str, int | datetime]]):
            Publication activity feature rows.
    """
    publication_activity_features = [
        PublicationActivityFeature(**publication_activity_feature_row)
        for publication_activity_feature_row in (
            publication_activity_feature_rows
        )
    ]

    session.add_all(publication_activity_features)
    await session.flush()

    return publication_activity_features


async def save_text_features(
    session: AsyncSession,
    text_feature_rows: list[dict[str, int | bool | datetime]],
) -> list[TextFeature]:
    """Save text feature rows.
    Args:
        session (AsyncSession): Database session.
        text_feature_rows (list[dict[str, int | bool | datetime]]):
            Text feature rows.
    """
    text_features = [
        TextFeature(**text_feature_row)
        for text_feature_row in text_feature_rows
    ]

    session.add_all(text_features)
    await session.flush()

    return text_features


async def save_time_features(
    session: AsyncSession,
    time_feature_rows: list[dict[str, int | bool | datetime]],
) -> list[TimeFeature]:
    """Save time feature rows.
    Args:
        session (AsyncSession): Database session.
        time_feature_rows (list[dict[str, int | bool | datetime]]):
            Time feature rows.
    """
    time_features = [
        TimeFeature(**time_feature_row)
        for time_feature_row in time_feature_rows
    ]

    session.add_all(time_features)
    await session.flush()

    return time_features
