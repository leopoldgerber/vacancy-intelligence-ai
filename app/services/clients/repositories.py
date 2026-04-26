from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.client import Client


async def get_active_client_ids(session: AsyncSession) -> list[int]:
    """Get active client identifiers.
    Args:
        session (AsyncSession): Async database session."""
    statement = select(Client.id).where(Client.is_active.is_(True))
    result = await session.execute(statement)
    client_ids = list(result.scalars().all())
    return client_ids
