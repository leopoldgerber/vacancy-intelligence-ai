from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine)

from app.db.config import get_database_config


database_config = get_database_config()

engine = create_async_engine(database_config.async_url, future=True)
SessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield async database session.
    Args:
        """
    async with SessionLocal() as session:
        yield session
