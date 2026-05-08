from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.ml_dataset_run import MlDatasetRun
from app.db.models.ml_feature_row import MlFeatureRow


async def save_ml_dataset_run(
    session: AsyncSession,
    dataset_run_name: str,
    client_id: int,
    date_from: datetime,
    date_to: datetime,
    salary_feature_run_id: int | None,
    publication_activity_feature_run_id: int | None,
    text_feature_run_id: int | None,
    time_feature_run_id: int | None,
    categorical_feature_run_id: int | None,
    status: str,
    is_success: bool,
    row_count: int,
    report_name: str,
) -> MlDatasetRun:
    """Save ML dataset run.
    Args:
        session (AsyncSession): Database session.
        dataset_run_name (str): ML dataset run name.
        client_id (int): Client identifier.
        date_from (datetime): Dataset period start.
        date_to (datetime): Dataset period end.
        salary_feature_run_id (int | None): Salary feature run identifier.
        publication_activity_feature_run_id (int | None):
            Publication activity feature run identifier.
        text_feature_run_id (int | None): Text feature run identifier.
        time_feature_run_id (int | None): Time feature run identifier.
        categorical_feature_run_id (int | None):
            Categorical feature run identifier.
        status (str): Dataset run status.
        is_success (bool): Whether dataset run is successful.
        row_count (int): Number of dataset rows.
        report_name (str): Dataset report name.
    """
    ml_dataset_run = MlDatasetRun(
        dataset_run_name=dataset_run_name,
        client_id=client_id,
        date_from=date_from,
        date_to=date_to,
        salary_feature_run_id=salary_feature_run_id,
        publication_activity_feature_run_id=(
            publication_activity_feature_run_id
        ),
        text_feature_run_id=text_feature_run_id,
        time_feature_run_id=time_feature_run_id,
        categorical_feature_run_id=categorical_feature_run_id,
        status=status,
        is_success=is_success,
        row_count=row_count,
        report_name=report_name,
    )

    session.add(ml_dataset_run)
    await session.flush()

    return ml_dataset_run


async def save_ml_feature_rows(
    session: AsyncSession,
    ml_feature_rows: list[dict[str, int | float | bool | str | datetime]],
) -> list[MlFeatureRow]:
    """Save materialized ML feature rows.
    Args:
        session (AsyncSession): Database session.
        ml_feature_rows (list[dict[str, int | float | bool | str | datetime]]):
            Materialized ML feature rows.
    """
    feature_rows = [
        MlFeatureRow(**ml_feature_row)
        for ml_feature_row in ml_feature_rows
    ]

    session.add_all(feature_rows)
    await session.flush()

    return feature_rows
