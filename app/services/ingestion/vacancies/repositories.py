from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.vacancy import Vacancy


async def get_vacancies_by_ids(
    session: AsyncSession,
    vacancy_ids: list[int],
) -> list[Vacancy]:
    """Get vacancies by vacancy identifiers.
    Args:
        session (AsyncSession): Async database session.
        vacancy_ids (list[int]): Vacancy identifiers."""
    statement = select(Vacancy).where(Vacancy.vacancy_id.in_(vacancy_ids))
    result = await session.execute(statement)
    vacancies = list(result.scalars().all())
    return vacancies
