from sqlalchemy import desc
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.analytics_run import AnalyticsRun


async def get_latest_analytics_run(
    session: AsyncSession,
    client_id: int,
) -> AnalyticsRun | None:
    """Get latest successful analytics run.
    Args:
        session (AsyncSession): Database session.
        client_id (int): Client identifier.
    """
    statement = (
        select(AnalyticsRun)
        .where(AnalyticsRun.client_id == client_id)
        .where(AnalyticsRun.is_success.is_(True))
        .order_by(desc(AnalyticsRun.created_at))
        .limit(1)
    )

    result = await session.execute(statement)

    return result.scalar_one_or_none()
