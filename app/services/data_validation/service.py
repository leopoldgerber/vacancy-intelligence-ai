from sqlalchemy.ext.asyncio import AsyncSession

import pandas as pd

from app.services.data_validation.run_validation_pipeline import (
    run_validation_pipeline,
)


async def validate_data(
    session: AsyncSession,
    data: pd.DataFrame,
    validation_name: str,
    source_name: str,
    report_name: str,
    required_columns: list[str],
    datetime_format: str = '%Y-%m-%d %H:%M:%S',
) -> dict[str, object]:
    """Run validation service and return final result.
    Args:
        session (AsyncSession): Async database session.
        data (pd.DataFrame): Input dataset.
        validation_name (str): Validation run name.
        source_name (str): Source dataset name.
        report_name (str): Markdown report name.
        required_columns (list[str]): Required dataset columns.
        datetime_format (str): Datetime format for validation."""
    validation_run, validation_issue, saved_report_path = (
        await run_validation_pipeline(
            session=session,
            data=data,
            validation_name=validation_name,
            source_name=source_name,
            report_name=report_name,
            required_columns=required_columns,
            datetime_format=datetime_format,
        )
    )

    validation_result = {
        'status': validation_run.status,
        'is_valid': validation_run.is_valid,
        'validation_run': validation_run,
        'validation_issue': validation_issue,
        'report_path': saved_report_path,
    }
    return validation_result
