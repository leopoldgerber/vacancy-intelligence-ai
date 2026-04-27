from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.client import Client
from app.services.clients.persistence import create_client_if_missing
from app.services.clients.persistence import get_client_by_id


async def create_client_entry(
    session: AsyncSession,
    client_id: int,
    name: str,
    is_active: bool = True,
) -> Client:
    """Create client entry.
    Args:
        session (AsyncSession): Async database session.
        client_id (int): Client identifier.
        name (str): Client name.
        is_active (bool): Client active flag."""
    existing_client = await get_client_by_id(
        session=session,
        client_id=client_id,
    )

    if existing_client is not None:
        return existing_client

    client = await create_client_if_missing(
        session=session,
        client_id=client_id,
        name=name,
        is_active=is_active,
    )
    return client
