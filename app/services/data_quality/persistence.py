from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.quality_issue import QualityIssue
from app.db.models.quality_run import QualityRun
from app.services.data_quality.repositories import (
    create_quality_issue,
    create_quality_run,
)


async def save_quality_result(
    session: AsyncSession,
    quality_result: dict[str, dict[str, str | int] | dict[str, int]],
) -> tuple[QualityRun, QualityIssue]:
    """Save quality result to database.
    Args:
        session (AsyncSession): Async database session.
        quality_result (dict[str, dict[str, str | int] | dict[str, int]]):
            Final quality result payload."""
    quality_run_data = quality_result['quality_run']
    quality_issue_data = quality_result['quality_issue']

    quality_run = create_quality_run(
        quality_run_data=quality_run_data,
    )
    session.add(quality_run)
    await session.flush()

    quality_issue = create_quality_issue(
        quality_run_id=quality_run.id,
        quality_issue_data=quality_issue_data,
    )
    session.add(quality_issue)

    await session.commit()
    await session.refresh(quality_run)
    await session.refresh(quality_issue)

    return quality_run, quality_issue
