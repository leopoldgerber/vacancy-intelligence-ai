from collections.abc import AsyncGenerator
from pathlib import Path
import sys

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.api.main import app  # noqa
from app.db.models.client import Client  # noqa
from app.db.models.company import Company  # noqa
from app.db.models.quality_issue import QualityIssue  # noqa
from app.db.models.quality_run import QualityRun  # noqa
from app.db.models.validation_issue import ValidationIssue  # noqa
from app.db.models.validation_run import ValidationRun  # noqa
from app.db.models.vacancy import Vacancy  # noqa
from app.db.models.vacancy_snapshot import VacancySnapshot  # noqa
from app.db.session import SessionLocal, engine, get_session  # noqa


async def clear_tables(session: AsyncSession) -> None:
    """Clear database tables used in pipeline 1 tests.
    Args:
        session (AsyncSession): Async database session."""
    delete_statements = [
        delete(VacancySnapshot),
        delete(Vacancy),
        delete(Company),
        delete(QualityIssue),
        delete(QualityRun),
        delete(ValidationIssue),
        delete(ValidationRun),
        delete(Client),
    ]

    for statement in delete_statements:
        await session.execute(statement)

    await session.commit()


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide clean async database session for tests.
    Args:
        """
    async with SessionLocal() as session:
        await clear_tables(session=session)
        yield session
        await clear_tables(session=session)

    await engine.dispose()


@pytest_asyncio.fixture
async def client(
    db_session: AsyncSession,
) -> AsyncGenerator[AsyncClient, None]:
    """Provide async API client for tests.
    Args:
        db_session (AsyncSession): Async database session."""
    async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        """Override application database session.
        Args:
            """
        yield db_session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url='http://testserver',
    ) as async_client:
        yield async_client

    app.dependency_overrides.clear()
