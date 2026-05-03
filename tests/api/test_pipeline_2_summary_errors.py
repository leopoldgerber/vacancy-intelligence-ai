import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.analytics_run import AnalyticsRun
from app.db.models.client import Client
from app.db.models.client_summary import ClientSummary
from app.db.models.competitor_summary import CompetitorSummary
from app.db.models.market_summary import MarketSummary


async def create_client_only(
    db_session: AsyncSession,
) -> None:
    """Create client without snapshots.
    Args:
        db_session (AsyncSession): Async database session.
    """
    test_client = Client(
        id=1,
        name='target_client',
        is_active=True,
    )

    db_session.add(test_client)
    await db_session.commit()


@pytest.mark.asyncio
async def test_run_pipeline_2_summary_no_data(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """Test Pipeline 2 summary execution without data.
    Args:
        client (AsyncClient): Async API client.
        db_session (AsyncSession): Async database session.
    """
    await create_client_only(db_session=db_session)

    response = await client.post(
        '/pipeline-2/analytics/summary/run',
        data={
            'client_id': '1',
            'date_from': '2025-08-01',
            'date_to': '2025-08-21',
            'city': '',
            'profile': '',
        },
    )

    response_json = response.json()

    assert response.status_code == 200
    assert response_json['status'] == 'no_data'
    assert response_json['is_success'] is False
    assert response_json['snapshot_count'] == 0
    assert response_json['report_name'].endswith('.md')
    assert response_json['analytics_run_id'] > 0

    analytics_run_id = response_json['analytics_run_id']

    analytics_run = await db_session.scalar(
        select(AnalyticsRun).where(AnalyticsRun.id == analytics_run_id),
    )
    market_summary = await db_session.scalar(
        select(MarketSummary).where(
            MarketSummary.analytics_run_id == analytics_run_id,
        ),
    )
    client_summary = await db_session.scalar(
        select(ClientSummary).where(
            ClientSummary.analytics_run_id == analytics_run_id,
        ),
    )
    competitor_summary = await db_session.scalar(
        select(CompetitorSummary).where(
            CompetitorSummary.analytics_run_id == analytics_run_id,
        ),
    )

    assert analytics_run is not None
    assert analytics_run.status == 'no_data'
    assert analytics_run.is_success is False
    assert analytics_run.snapshot_count == 0

    assert market_summary is None
    assert client_summary is None
    assert competitor_summary is None
