from datetime import datetime

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.data_validation.constants import DEFAULT_DATETIME_FORMAT
from app.services.data_validation.constants import REQUIRED_COLUMNS
from app.services.pre_ingestion.run_pre_ingestion_pipeline import (
    run_pre_ingestion_pipeline,
)


def build_operation_name(operation_name: str) -> str:
    """Build operation name with current timestamp.
    Args:
        operation_name (str): Operation name prefix."""
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    operation_value = f'{operation_name}_{timestamp}'
    return operation_value


async def prepare_data_for_ingestion(
    session: AsyncSession,
    data: pd.DataFrame,
    source_name: str,
) -> dict[str, object]:
    """Prepare data for ingestion.
    Args:
        session (AsyncSession): Async database session.
        data (pd.DataFrame): Input dataset.
        source_name (str): Source dataset name."""
    validation_name = build_operation_name(operation_name='validation')
    validation_report_name = f'{validation_name}.md'

    quality_name = build_operation_name(operation_name='quality')
    quality_report_name = f'{quality_name}.md'

    pre_ingestion_result = await run_pre_ingestion_pipeline(
        session=session,
        data=data,
        source_name=source_name,
        validation_name=validation_name,
        validation_report_name=validation_report_name,
        quality_name=quality_name,
        quality_report_name=quality_report_name,
        required_columns=REQUIRED_COLUMNS,
        datetime_format=DEFAULT_DATETIME_FORMAT,
    )
    return pre_ingestion_result
