from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.validation_issue import ValidationIssue
from app.db.models.validation_run import ValidationRun
from app.services.data_validation.repositories import (
    create_validation_issue,
    create_validation_run,
)


async def save_validation_result(
    session: AsyncSession,
    validation_result: dict[str, dict[str, str | int | bool] | dict[str, int]],
) -> tuple[ValidationRun, ValidationIssue]:
    """Save validation result to database.
    Args:
        session (AsyncSession): Async database session.
        validation_result (dict[str, dict[str, str | int | bool] |
            dict[str, int]]): Final validation result payload."""
    validation_run_data = validation_result['validation_run']
    validation_issue_data = validation_result['validation_issue']

    validation_run = create_validation_run(
        validation_run_data=validation_run_data,
    )
    session.add(validation_run)
    await session.flush()

    validation_issue = create_validation_issue(
        validation_run_id=validation_run.id,
        validation_issue_data=validation_issue_data,
    )
    session.add(validation_issue)

    await session.commit()
    await session.refresh(validation_run)
    await session.refresh(validation_issue)

    return validation_run, validation_issue
