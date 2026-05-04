from datetime import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.client import Client
from app.db.models.company import Company
from app.db.models.feature_run import FeatureRun
from app.db.models.salary_feature import SalaryFeature
from app.db.models.vacancy import Vacancy
from app.db.models.vacancy_snapshot import VacancySnapshot


async def create_salary_feature_test_data(
    db_session: AsyncSession,
) -> None:
    """Create test data for salary feature pipeline.
    Args:
        db_session (AsyncSession): Async database session.
    """
    test_client = Client(
        id=1,
        name='target_client',
        is_active=True,
    )
    company_one = Company(
        id=10,
        client_id=1,
        name='target_client',
    )
    company_two = Company(
        id=20,
        client_id=1,
        name='competitor_one',
    )
    company_three = Company(
        id=30,
        client_id=1,
        name='competitor_two',
    )

    db_session.add_all(
        [
            test_client,
            company_one,
            company_two,
            company_three,
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
            profile='Filialleiter',
            publication_date=datetime(2025, 8, 1, 10, 0, 0),
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
            vacancy_description='Target vacancy description.',
            employment_type='Full-time',
            profile='Filialleiter',
            publication_date=datetime(2025, 8, 1, 11, 0, 0),
            region='Berlin',
            city='Berlin',
            salary_from=1200,
            salary_to=2400,
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
            vacancy_title='Competitor vacancy one',
            vacancy_description='Competitor description.',
            employment_type='Full-time',
            profile='Filialleiter',
            publication_date=datetime(2025, 8, 1, 12, 0, 0),
            region='Berlin',
            city='Berlin',
            salary_from=2000,
            salary_to=4000,
            tariff='Premium',
            work_experience='3 years',
            work_schedule='Shift',
            standard=0,
            standard_plus=0,
            premium=1,
        ),
        Vacancy(
            vacancy_id=201,
            client_id=1,
            company_id=20,
            vacancy_title='Competitor vacancy two',
            vacancy_description='Competitor description.',
            employment_type='Full-time',
            profile='Filialleiter',
            publication_date=datetime(2025, 8, 1, 13, 0, 0),
            region='Berlin',
            city='Berlin',
            salary_from=2200,
            salary_to=4400,
            tariff='Premium',
            work_experience='3 years',
            work_schedule='Shift',
            standard=0,
            standard_plus=0,
            premium=1,
        ),
        Vacancy(
            vacancy_id=300,
            client_id=1,
            company_id=30,
            vacancy_title='Competitor vacancy three',
            vacancy_description='Competitor description.',
            employment_type='Full-time',
            profile='Filialleiter',
            publication_date=datetime(2025, 8, 1, 14, 0, 0),
            region='Berlin',
            city='Berlin',
            salary_from=3000,
            salary_to=None,
            tariff='Premium',
            work_experience='3 years',
            work_schedule='Shift',
            standard=0,
            standard_plus=0,
            premium=1,
        ),
        Vacancy(
            vacancy_id=301,
            client_id=1,
            company_id=30,
            vacancy_title='Competitor vacancy four',
            vacancy_description='Competitor description.',
            employment_type='Full-time',
            profile='Filialleiter',
            publication_date=datetime(2025, 8, 1, 15, 0, 0),
            region='Berlin',
            city='Berlin',
            salary_from=None,
            salary_to=3600,
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
            date_day=datetime(2025, 8, 1, 0, 0, 0),
            publication_date=datetime(2025, 8, 1, 10, 0, 0),
            vacancy_title='Target vacancy one',
            vacancy_description='Target vacancy description.',
            employment_type='Full-time',
            profile='Filialleiter',
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
            date_day=datetime(2025, 8, 1, 0, 0, 0),
            publication_date=datetime(2025, 8, 1, 11, 0, 0),
            vacancy_title='Target vacancy two',
            vacancy_description='Target vacancy description.',
            employment_type='Full-time',
            profile='Filialleiter',
            region='Berlin',
            city='Berlin',
            salary_from=1200,
            salary_to=2400,
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
            date_day=datetime(2025, 8, 1, 0, 0, 0),
            publication_date=datetime(2025, 8, 1, 12, 0, 0),
            vacancy_title='Competitor vacancy one',
            vacancy_description='Competitor description.',
            employment_type='Full-time',
            profile='Filialleiter',
            region='Berlin',
            city='Berlin',
            salary_from=2000,
            salary_to=4000,
            tariff='Premium',
            work_experience='3 years',
            work_schedule='Shift',
            standard=0,
            standard_plus=0,
            premium=1,
            callbacks=20,
        ),
        VacancySnapshot(
            client_id=1,
            company_id=20,
            vacancy_id=201,
            date_day=datetime(2025, 8, 1, 0, 0, 0),
            publication_date=datetime(2025, 8, 1, 13, 0, 0),
            vacancy_title='Competitor vacancy two',
            vacancy_description='Competitor description.',
            employment_type='Full-time',
            profile='Filialleiter',
            region='Berlin',
            city='Berlin',
            salary_from=2200,
            salary_to=4400,
            tariff='Premium',
            work_experience='3 years',
            work_schedule='Shift',
            standard=0,
            standard_plus=0,
            premium=1,
            callbacks=25,
        ),
        VacancySnapshot(
            client_id=1,
            company_id=30,
            vacancy_id=300,
            date_day=datetime(2025, 8, 1, 0, 0, 0),
            publication_date=datetime(2025, 8, 1, 14, 0, 0),
            vacancy_title='Competitor vacancy three',
            vacancy_description='Competitor description.',
            employment_type='Full-time',
            profile='Filialleiter',
            region='Berlin',
            city='Berlin',
            salary_from=3000,
            salary_to=None,
            tariff='Premium',
            work_experience='3 years',
            work_schedule='Shift',
            standard=0,
            standard_plus=0,
            premium=1,
            callbacks=30,
        ),
        VacancySnapshot(
            client_id=1,
            company_id=30,
            vacancy_id=301,
            date_day=datetime(2025, 8, 1, 0, 0, 0),
            publication_date=datetime(2025, 8, 1, 15, 0, 0),
            vacancy_title='Competitor vacancy four',
            vacancy_description='Competitor description.',
            employment_type='Full-time',
            profile='Filialleiter',
            region='Berlin',
            city='Berlin',
            salary_from=None,
            salary_to=3600,
            tariff='Premium',
            work_experience='3 years',
            work_schedule='Shift',
            standard=0,
            standard_plus=0,
            premium=1,
            callbacks=35,
        ),
    ]

    db_session.add_all(snapshots)
    await db_session.commit()


@pytest.mark.asyncio
async def test_run_pipeline_2_salary_features_success(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """Test successful Pipeline 2 salary feature execution.
    Args:
        client (AsyncClient): Async API client.
        db_session (AsyncSession): Async database session.
    """
    await create_salary_feature_test_data(db_session=db_session)

    response = await client.post(
        '/pipeline-2/features/salary/run',
        data={
            'client_id': '1',
            'date_from': '2025-08-01',
            'date_to': '2025-08-21',
        },
    )

    response_json = response.json()

    assert response.status_code == 200
    assert response_json['status'] == 'success'
    assert response_json['is_success'] is True
    assert response_json['snapshot_count'] == 6
    assert response_json['feature_count'] == 6
    assert response_json['report_name'].endswith('.md')
    assert response_json['feature_run_id'] > 0

    feature_run_id = response_json['feature_run_id']

    feature_run = await db_session.scalar(
        select(FeatureRun).where(FeatureRun.id == feature_run_id),
    )
    salary_features = (
        await db_session.scalars(
            select(SalaryFeature).where(
                SalaryFeature.feature_run_id == feature_run_id,
            ),
        )
    ).all()

    assert feature_run is not None
    assert feature_run.status == 'success'
    assert feature_run.is_success is True
    assert feature_run.snapshot_count == 6
    assert feature_run.feature_count == 6

    assert len(salary_features) == 6

    target_feature = next(
        salary_feature
        for salary_feature in salary_features
        if salary_feature.company_id == 10
        and salary_feature.vacancy_id == 100
    )

    assert target_feature.salary_mid == 1500.0
    assert target_feature.salary_is_specified is True
    assert target_feature.company_salary_median_by_city == 1650.0
    assert (
        target_feature.market_salary_median_excl_company_by_city
        == 3150.0
    )
    assert target_feature.salary_ratio_to_market_by_city == pytest.approx(
        1650.0 / 3150.0,
    )
    assert target_feature.company_salary_median_by_profile == 1650.0
    assert target_feature.salary_ratio_to_market_by_profile == pytest.approx(
        1650.0 / 3150.0,
    )
    assert (
        target_feature.company_salary_median_by_city_profile
        == 1650.0
    )
    assert (
        target_feature.salary_ratio_to_market_by_city_profile
        == pytest.approx(1650.0 / 3150.0)
    )
