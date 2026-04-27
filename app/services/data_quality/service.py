import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.data_quality.run_quality_pipeline import (
    run_quality_pipeline,
)


async def check_data_quality(
    session: AsyncSession,
    data: pd.DataFrame,
    quality_name: str,
    source_name: str,
    report_name: str,
) -> dict[str, object]:
    """Run quality service and return final result.
    Args:
        session (AsyncSession): Async database session.
        data (pd.DataFrame): Input dataset.
        quality_name (str): Quality run name.
        source_name (str): Source dataset name.
        report_name (str): Markdown report name."""
    quality_run, quality_issue, saved_report_path = (
        await run_quality_pipeline(
            session=session,
            data=data,
            quality_name=quality_name,
            source_name=source_name,
            report_name=report_name,
        )
    )

    quality_result = {
        'warning_count': quality_run.warning_count,
        'quality_run': quality_run,
        'quality_issue': quality_issue,
        'report_path': saved_report_path,
    }
    return quality_result
