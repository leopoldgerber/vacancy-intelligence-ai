from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.company import Company


async def get_companies_by_client_ids(
    session: AsyncSession,
    client_ids: list[int],
) -> list[Company]:
    """Get companies by client identifiers.
    Args:
        session (AsyncSession): Async database session.
        client_ids (list[int]): Client identifiers."""
    statement = select(Company).where(Company.client_id.in_(client_ids))
    result = await session.execute(statement)
    companies = list(result.scalars().all())
    return companies
