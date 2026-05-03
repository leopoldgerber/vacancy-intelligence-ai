from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.analytics_run import AnalyticsRun
from app.db.models.market_summary import MarketSummary


async def save_analytics_run(
    session: AsyncSession,
    analytics_name: str,
    client_id: int,
    date_from: datetime,
    date_to: datetime,
    status: str,
    is_success: bool,
    snapshot_count: int,
    report_name: str,
) -> AnalyticsRun:
    """Save analytics run.
    Args:
        session (AsyncSession): Database session.
        analytics_name (str): Analytics run name.
        client_id (int): Client identifier.
        date_from (datetime): Analytics period start.
        date_to (datetime): Analytics period end.
        status (str): Analytics run status.
        is_success (bool): Whether analytics run is successful.
        snapshot_count (int): Number of snapshots in analytics input.
        report_name (str): Analytics report name.
    """
    analytics_run = AnalyticsRun(
        analytics_name=analytics_name,
        client_id=client_id,
        date_from=date_from,
        date_to=date_to,
        status=status,
        is_success=is_success,
        snapshot_count=snapshot_count,
        report_name=report_name,
    )

    session.add(analytics_run)
    await session.flush()

    return analytics_run


async def save_market_summary(
    session: AsyncSession,
    market_summary_data: dict[str, int | float | str | None],
) -> MarketSummary:
    """Save market summary.
    Args:
        session (AsyncSession): Database session.
        market_summary_data (dict[str, int | float | str | None]):
            Summary data.
    """
    market_summary = MarketSummary(**market_summary_data)

    session.add(market_summary)
    await session.flush()

    return market_summary
