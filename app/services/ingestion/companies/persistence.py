from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.company import Company


def create_company(
    client_id: int,
    name: str,
) -> Company:
    """Create company model instance.
    Args:
        client_id (int): Client identifier.
        name (str): Company name."""
    company = Company(
        client_id=client_id,
        name=name,
    )
    return company


async def save_companies(
    session: AsyncSession,
    companies: list[Company],
) -> list[Company]:
    """Save company model instances.
    Args:
        session (AsyncSession): Async database session.
        companies (list[Company]): Company model instances."""
    if not companies:
        return companies

    session.add_all(companies)
    await session.flush()

    return companies
