import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.data_quality.service import check_data_quality
from app.services.data_validation.service import validate_data


async def run_pre_ingestion_pipeline(
    session: AsyncSession,
    data: pd.DataFrame,
    source_name: str,
    validation_name: str,
    validation_report_name: str,
    quality_name: str,
    quality_report_name: str,
    required_columns: list[str],
    datetime_format: str = '%Y-%m-%d %H:%M:%S',
) -> dict[str, object]:
    """Run pre-ingestion pipeline.
    Args:
        session (AsyncSession): Async database session.
        data (pd.DataFrame): Input dataset.
        source_name (str): Source dataset name.
        validation_name (str): Validation run name.
        validation_report_name (str): Validation report name.
        quality_name (str): Quality run name.
        quality_report_name (str): Quality report name.
        required_columns (list[str]): Required dataset columns.
        datetime_format (str): Datetime format for validation."""
    validation_result = await validate_data(
        session=session,
        data=data,
        validation_name=validation_name,
        source_name=source_name,
        report_name=validation_report_name,
        required_columns=required_columns,
        datetime_format=datetime_format,
    )

    if not validation_result['is_valid']:
        pre_ingestion_result = {
            'status': 'failed',
            'should_ingest': False,
            'validation_result': validation_result,
            'quality_result': None,
        }
        return pre_ingestion_result

    quality_result = await check_data_quality(
        session=session,
        data=data,
        quality_name=quality_name,
        source_name=source_name,
        report_name=quality_report_name,
    )

    pre_ingestion_result = {
        'status': 'ready_for_ingestion',
        'should_ingest': True,
        'validation_result': validation_result,
        'quality_result': quality_result,
    }
    return pre_ingestion_result
