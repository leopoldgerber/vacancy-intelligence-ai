from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.vacancy_snapshot import VacancySnapshot


async def get_existing_snapshot_keys(
    session: AsyncSession,
    client_ids: list[int],
    company_ids: list[int],
    vacancy_ids: list[int],
) -> set[tuple[int, int, int, object]]:
    """Get existing vacancy snapshot keys.
    Args:
        session (AsyncSession): Async database session.
        client_ids (list[int]): Client identifiers.
        company_ids (list[int]): Company identifiers.
        vacancy_ids (list[int]): Vacancy identifiers."""
    statement = select(
        VacancySnapshot.client_id,
        VacancySnapshot.company_id,
        VacancySnapshot.vacancy_id,
        VacancySnapshot.date_day,
    ).where(
        VacancySnapshot.client_id.in_(client_ids),
        VacancySnapshot.company_id.in_(company_ids),
        VacancySnapshot.vacancy_id.in_(vacancy_ids),
    )

    result = await session.execute(statement)
    rows = result.all()

    snapshot_keys = {
        (
            int(row.client_id),
            int(row.company_id),
            int(row.vacancy_id),
            row.date_day,
        )
        for row in rows
    }
    return snapshot_keys
