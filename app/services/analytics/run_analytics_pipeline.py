from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.analytics.client_summary_builders import (
    build_client_summary_data,
)
from app.services.analytics.constants import ANALYTICS_STATUS_NO_DATA
from app.services.analytics.constants import ANALYTICS_STATUS_SUCCESS
from app.services.analytics.data_loaders import load_client_snapshot_data
from app.services.analytics.data_loaders import load_snapshot_data
from app.services.analytics.market_summary_builders import (
    build_market_summary_data,
)
from app.services.analytics.name_builders import build_analytics_name
from app.services.analytics.name_builders import build_analytics_report_name
from app.services.analytics.persistence import save_analytics_run
from app.services.analytics.persistence import save_client_summary
from app.services.analytics.persistence import save_market_summary
from app.services.analytics.report_builders import build_analytics_report
from app.services.analytics.report_writers import save_analytics_report
from app.services.analytics.repositories import get_client_name


async def run_analytics_pipeline(
    session: AsyncSession,
    client_id: int,
    date_from: datetime,
    date_to: datetime,
    city: str | None,
    profile: str | None,
) -> dict[str, int | str | bool]:
    """Run analytics pipeline.
    Args:
        session (AsyncSession): Database session.
        client_id (int): Client identifier.
        date_from (datetime): Analytics period start.
        date_to (datetime): Analytics period end.
        city (str | None): City filter.
        profile (str | None): Profile filter.
    """
    analytics_name = build_analytics_name()
    report_name = build_analytics_report_name(
        analytics_name=analytics_name,
    )
    client_company_name = await get_client_name(
        session=session,
        client_id=client_id,
    )

    if client_company_name is None:
        client_company_name = 'unknown'

    snapshot_data = await load_snapshot_data(
        session=session,
        client_id=client_id,
        date_from=date_from,
        date_to=date_to,
        city=city,
        profile=profile,
    )
    snapshot_count = len(snapshot_data)

    if snapshot_data.empty:
        analytics_run = await save_analytics_run(
            session=session,
            analytics_name=analytics_name,
            client_id=client_id,
            date_from=date_from,
            date_to=date_to,
            status=ANALYTICS_STATUS_NO_DATA,
            is_success=False,
            snapshot_count=snapshot_count,
            report_name=report_name,
        )
        report_content = build_analytics_report(
            analytics_run=analytics_run,
            market_summary=None,
            client_summary=None,
            city=city,
            profile=profile,
        )
        save_analytics_report(
            report_name=analytics_run.report_name,
            report_content=report_content,
        )

        return {
            'analytics_run_id': analytics_run.id,
            'analytics_name': analytics_run.analytics_name,
            'status': analytics_run.status,
            'is_success': analytics_run.is_success,
            'snapshot_count': analytics_run.snapshot_count,
            'report_name': analytics_run.report_name,
        }

    analytics_run = await save_analytics_run(
        session=session,
        analytics_name=analytics_name,
        client_id=client_id,
        date_from=date_from,
        date_to=date_to,
        status=ANALYTICS_STATUS_SUCCESS,
        is_success=True,
        snapshot_count=snapshot_count,
        report_name=report_name,
    )

    market_summary_data = build_market_summary_data(
        data=snapshot_data,
        analytics_run_id=analytics_run.id,
        client_id=client_id,
    )
    market_summary = await save_market_summary(
        session=session,
        market_summary_data=market_summary_data,
    )

    client_snapshot_data = await load_client_snapshot_data(
        session=session,
        client_id=client_id,
        date_from=date_from,
        date_to=date_to,
        city=city,
        profile=profile,
    )
    client_summary_data = build_client_summary_data(
        data=client_snapshot_data,
        analytics_run_id=analytics_run.id,
        client_id=client_id,
        client_company_name=client_company_name,
    )
    client_summary = await save_client_summary(
        session=session,
        client_summary_data=client_summary_data,
    )

    report_content = build_analytics_report(
        analytics_run=analytics_run,
        market_summary=market_summary,
        client_summary=client_summary,
        city=city,
        profile=profile,
    )
    save_analytics_report(
        report_name=analytics_run.report_name,
        report_content=report_content,
    )

    return {
        'analytics_run_id': analytics_run.id,
        'analytics_name': analytics_run.analytics_name,
        'status': analytics_run.status,
        'is_success': analytics_run.is_success,
        'snapshot_count': analytics_run.snapshot_count,
        'report_name': analytics_run.report_name,
    }
