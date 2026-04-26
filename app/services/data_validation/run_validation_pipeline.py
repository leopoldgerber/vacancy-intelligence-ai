# from collections.abc import Sequence

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.validation_issue import ValidationIssue
from app.db.models.validation_run import ValidationRun
from app.services.clients.repositories import get_active_client_ids
from app.services.data_validation.persistence import (
    save_validation_result,
)
from app.services.data_validation.report_builders import (
    build_validation_report,
    save_validation_report,
)
from app.services.data_validation.run_validation import run_validation


async def run_validation_pipeline(
    session: AsyncSession,
    data: pd.DataFrame,
    validation_name: str,
    source_name: str,
    report_name: str,
    required_columns: list[str],
    datetime_format: str = '%Y-%m-%d %H:%M:%S',
) -> tuple[ValidationRun, ValidationIssue, str]:
    """Run validation pipeline and save report.
    Args:
        session (AsyncSession): Async database session.
        data (pd.DataFrame): Input dataset.
        validation_name (str): Validation run name.
        source_name (str): Source dataset name.
        report_name (str): Markdown report name.
        required_columns (list[str]): Required dataset columns.
        datetime_format (str): Datetime format for validation."""
    client_ids = await get_active_client_ids(session=session)

    validation_result = run_validation(
        data=data,
        validation_name=validation_name,
        source_name=source_name,
        report_name=report_name,
        required_columns=required_columns,
        client_ids=client_ids,
        datetime_format=datetime_format,
    )

    validation_run, validation_issue = await save_validation_result(
        session=session,
        validation_result=validation_result,
    )

    report_text = build_validation_report(
        validation_run=validation_run,
        validation_issue=validation_issue,
    )

    saved_report_path = save_validation_report(
        report_text=report_text,
        report_name=validation_run.report_name,
    )

    return validation_run, validation_issue, saved_report_path
