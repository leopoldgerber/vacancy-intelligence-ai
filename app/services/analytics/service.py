from datetime import datetime

from app.db.session import SessionLocal
from app.services.analytics.run_analytics_pipeline import (
    run_analytics_pipeline,
)


async def run_analytics(
    client_id: int,
    date_from: datetime,
    date_to: datetime,
    city: str | None,
    profile: str | None,
    company_name: str | None,
) -> dict[str, int | str | bool]:
    """Run analytics service.
    Args:
        client_id (int): Client identifier.
        date_from (datetime): Analytics period start.
        date_to (datetime): Analytics period end.
        city (str | None): City filter.
        profile (str | None): Profile filter.
        company_name (str | None): Company name filter.
    """
    async with SessionLocal() as session:
        async with session.begin():
            analytics_result = await run_analytics_pipeline(
                session=session,
                client_id=client_id,
                date_from=date_from,
                date_to=date_to,
                city=city,
                profile=profile,
                company_name=company_name,
            )

    return analytics_result
