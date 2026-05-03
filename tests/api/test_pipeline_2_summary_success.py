from datetime import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.analytics_run import AnalyticsRun
from app.db.models.client import Client
from app.db.models.client_summary import ClientSummary
from app.db.models.company import Company
from app.db.models.competitor_summary import CompetitorSummary
from app.db.models.market_summary import MarketSummary
from app.db.models.vacancy import Vacancy
from app.db.models.vacancy_snapshot import VacancySnapshot


async def create_summary_test_data(
    db_session: AsyncSession,
) -> None:
    """Create test data for Pipeline 2 summary.
    Args:
        db_session (AsyncSession): Async database session.
    """
    test_client = Client(
        id=1,
        name='target_client',
        is_active=True,
    )
    target_company = Company(
        id=10,
        client_id=1,
        name='target_client',
    )
    competitor_company = Company(
        id=20,
        client_id=1,
        name='competitor_company',
    )

    db_session.add_all(
        [
            test_client,
            target_company,
            competitor_company,
        ],
    )
    await db_session.flush()

    vacancies = [
        Vacancy(
            vacancy_id=100,
            client_id=1,
            company_id=10,
            vacancy_title='Target vacancy one',
            vacancy_description='Target vacancy description.',
            employment_type='Full-time',
            profile='Verkäufer',
            publication_date=datetime(2025, 8, 4, 10, 0, 0),
            region='Berlin',
            city='Berlin',
            salary_from=1000,
            salary_to=2000,
            tariff='Standard',
            work_experience='1 year',
            work_schedule='Full-time',
            standard=1,
            standard_plus=0,
            premium=0,
        ),
        Vacancy(
            vacancy_id=101,
            client_id=1,
            company_id=10,
            vacancy_title='Target vacancy two',
            vacancy_description='Second target vacancy description.',
            employment_type='Full-time',
            profile='Verkäufer',
            publication_date=datetime(2025, 8, 5, 10, 0, 0),
            region='Berlin',
            city='Berlin',
            salary_from=1200,
            salary_to=2200,
            tariff='Standard',
            work_experience='1 year',
            work_schedule='Full-time',
            standard=1,
            standard_plus=0,
            premium=0,
        ),
        Vacancy(
            vacancy_id=200,
            client_id=1,
            company_id=20,
            vacancy_title='Competitor vacancy',
            vacancy_description='Competitor vacancy description.',
            employment_type='Part-time',
            profile='Verkäufer',
            publication_date=datetime(2025, 8, 6, 10, 0, 0),
            region='Berlin',
            city='Berlin',
            salary_from=1400,
            salary_to=2400,
            tariff='Premium',
            work_experience='3 years',
            work_schedule='Shift',
            standard=0,
            standard_plus=0,
            premium=1,
        ),
    ]
    db_session.add_all(vacancies)
    await db_session.flush()

    snapshots = [
        VacancySnapshot(
            client_id=1,
            company_id=10,
            vacancy_id=100,
            date_day=datetime(2025, 8, 4, 0, 0, 0),
            publication_date=datetime(2025, 8, 4, 10, 0, 0),
            vacancy_title='Target vacancy one',
            vacancy_description='Target vacancy description.',
            employment_type='Full-time',
            profile='Verkäufer',
            region='Berlin',
            city='Berlin',
            salary_from=1000,
            salary_to=2000,
            tariff='Standard',
            work_experience='1 year',
            work_schedule='Full-time',
            standard=1,
            standard_plus=0,
            premium=0,
            callbacks=10,
        ),
        VacancySnapshot(
            client_id=1,
            company_id=10,
            vacancy_id=101,
            date_day=datetime(2025, 8, 5, 0, 0, 0),
            publication_date=datetime(2025, 8, 5, 10, 0, 0),
            vacancy_title='Target vacancy two',
            vacancy_description='Second target vacancy description.',
            employment_type='Full-time',
            profile='Verkäufer',
            region='Berlin',
            city='Berlin',
            salary_from=1200,
            salary_to=2200,
            tariff='Standard',
            work_experience='1 year',
            work_schedule='Full-time',
            standard=1,
            standard_plus=0,
            premium=0,
            callbacks=15,
        ),
        VacancySnapshot(
            client_id=1,
            company_id=20,
            vacancy_id=200,
            date_day=datetime(2025, 8, 6, 0, 0, 0),
            publication_date=datetime(2025, 8, 6, 10, 0, 0),
            vacancy_title='Competitor vacancy',
            vacancy_description='Competitor vacancy description.',
            employment_type='Part-time',
            profile='Verkäufer',
            region='Berlin',
            city='Berlin',
            salary_from=1400,
            salary_to=2400,
            tariff='Premium',
            work_experience='3 years',
            work_schedule='Shift',
            standard=0,
            standard_plus=0,
            premium=1,
            callbacks=20,
        ),
    ]
    db_session.add_all(snapshots)

    await db_session.commit()


@pytest.mark.asyncio
async def test_run_pipeline_2_summary_success(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """Test successful Pipeline 2 summary execution.
    Args:
        client (AsyncClient): Async API client.
        db_session (AsyncSession): Async database session.
    """
    await create_summary_test_data(db_session=db_session)

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
    assert response_json['status'] == 'success'
    assert response_json['is_success'] is True
    assert response_json['snapshot_count'] == 3
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
    assert market_summary is not None
    assert client_summary is not None
    assert competitor_summary is not None

    assert market_summary.total_snapshot_count == 3
    assert market_summary.total_company_count == 2
    assert market_summary.total_vacancy_count == 3
    assert market_summary.total_callbacks == 45

    assert client_summary.client_company_name == 'target_client'
    assert client_summary.client_snapshot_count == 2
    assert client_summary.client_vacancy_count == 2
    assert client_summary.client_total_callbacks == 25

    assert competitor_summary.competitor_company_count == 1
    assert competitor_summary.competitor_snapshot_count == 1
    assert competitor_summary.competitor_vacancy_count == 1
    assert competitor_summary.competitor_total_callbacks == 20
