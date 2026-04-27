import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.quality_issue import QualityIssue
from app.db.models.quality_run import QualityRun
from app.services.data_quality.checks import run_quality_checks
from app.services.data_quality.persistence import save_quality_result
from app.services.data_quality.report_builders import (
    build_quality_report,
    save_quality_report,
)
from app.services.data_quality.result_builders import build_quality_result


async def run_quality_pipeline(
    session: AsyncSession,
    data: pd.DataFrame,
    quality_name: str,
    source_name: str,
    report_name: str,
) -> tuple[QualityRun, QualityIssue, str]:
    """Run quality pipeline and save report.
    Args:
        session (AsyncSession): Async database session.
        data (pd.DataFrame): Input dataset.
        quality_name (str): Quality run name.
        source_name (str): Source dataset name.
        report_name (str): Markdown report name."""
    quality_results = run_quality_checks(data=data)

    quality_result = build_quality_result(
        data=data,
        quality_name=quality_name,
        source_name=source_name,
        report_name=report_name,
        quality_results=quality_results,
    )

    quality_run, quality_issue = await save_quality_result(
        session=session,
        quality_result=quality_result,
    )

    report_text = build_quality_report(
        quality_run=quality_run,
        quality_issue=quality_issue,
    )

    saved_report_path = save_quality_report(
        report_text=report_text,
        report_name=quality_run.report_name,
    )

    return quality_run, quality_issue, saved_report_path
