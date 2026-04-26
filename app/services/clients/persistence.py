from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.client import Client


async def create_client(
    session: AsyncSession,
    client_id: int,
    name: str,
    is_active: bool = True,
) -> Client:
    """Create client record.
    Args:
        session (AsyncSession): Async database session.
        client_id (int): Client identifier.
        name (str): Client name.
        is_active (bool): Client active flag."""
    client = Client(
        id=client_id,
        name=name,
        is_active=is_active,
    )
    session.add(client)
    await session.commit()
    await session.refresh(client)

    return client


async def get_client_by_id(
    session: AsyncSession,
    client_id: int,
) -> Client | None:
    """Get client by identifier.
    Args:
        session (AsyncSession): Async database session.
        client_id (int): Client identifier."""
    statement = select(Client).where(Client.id == client_id)
    result = await session.execute(statement)
    client = result.scalar_one_or_none()

    return client


async def create_client_if_missing(
    session: AsyncSession,
    client_id: int,
    name: str,
    is_active: bool = True,
) -> Client:
    """Create client if it does not exist.
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

    client = await create_client(
        session=session,
        client_id=client_id,
        name=name,
        is_active=is_active,
    )
    return client
