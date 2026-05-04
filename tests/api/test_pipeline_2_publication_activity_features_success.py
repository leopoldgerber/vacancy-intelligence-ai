from datetime import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.client import Client
from app.db.models.company import Company
from app.db.models.feature_run import FeatureRun
from app.db.models.publication_activity_feature import (
    PublicationActivityFeature,
)
from app.db.models.vacancy import Vacancy
from app.db.models.vacancy_snapshot import VacancySnapshot


async def create_publication_activity_test_data(
    db_session: AsyncSession,
) -> None:
    """Create test data for publication activity feature pipeline.
    Args:
        db_session (AsyncSession): Async database session.
    """
    test_client = Client(
        id=1,
        name='target_client',
        is_active=True,
    )
    test_company = Company(
        id=10,
        client_id=1,
        name='target_client',
    )

    db_session.add_all(
        [
            test_client,
            test_company,
        ],
    )
    await db_session.flush()

    test_vacancy = Vacancy(
        vacancy_id=100,
        client_id=1,
        company_id=10,
        vacancy_title='Target vacancy',
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
    )

    db_session.add(test_vacancy)
    await db_session.flush()

    snapshots = [
        VacancySnapshot(
            client_id=1,
            company_id=10,
            vacancy_id=100,
            date_day=datetime(2025, 8, 1, 0, 0, 0),
            publication_date=datetime(2025, 8, 1, 10, 0, 0),
            vacancy_title='Target vacancy',
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
            vacancy_id=100,
            date_day=datetime(2025, 8, 2, 0, 0, 0),
            publication_date=datetime(2025, 8, 1, 10, 0, 0),
            vacancy_title='Target vacancy',
            vacancy_description='Target vacancy description.',
            employment_type='Full-time',
            profile='Filialleiter',
            region='Berlin',
            city='Berlin',
            salary_from=1000,
            salary_to=2000,
            tariff=None,
            work_experience='1 year',
            work_schedule='Full-time',
            standard=0,
            standard_plus=0,
            premium=0,
            callbacks=7,
        ),
        VacancySnapshot(
            client_id=1,
            company_id=10,
            vacancy_id=100,
            date_day=datetime(2025, 8, 3, 0, 0, 0),
            publication_date=datetime(2025, 8, 1, 10, 0, 0),
            vacancy_title='Target vacancy',
            vacancy_description='Target vacancy description.',
            employment_type='Full-time',
            profile='Filialleiter',
            region='Berlin',
            city='Berlin',
            salary_from=1000,
            salary_to=2000,
            tariff=None,
            work_experience='1 year',
            work_schedule='Full-time',
            standard=0,
            standard_plus=0,
            premium=0,
            callbacks=6,
        ),
        VacancySnapshot(
            client_id=1,
            company_id=10,
            vacancy_id=100,
            date_day=datetime(2025, 8, 4, 0, 0, 0),
            publication_date=datetime(2025, 8, 1, 10, 0, 0),
            vacancy_title='Target vacancy',
            vacancy_description='Target vacancy description.',
            employment_type='Full-time',
            profile='Filialleiter',
            region='Berlin',
            city='Berlin',
            salary_from=1000,
            salary_to=2000,
            tariff='Standard Plus',
            work_experience='1 year',
            work_schedule='Full-time',
            standard=0,
            standard_plus=1,
            premium=0,
            callbacks=12,
        ),
        VacancySnapshot(
            client_id=1,
            company_id=10,
            vacancy_id=100,
            date_day=datetime(2025, 8, 5, 0, 0, 0),
            publication_date=datetime(2025, 8, 1, 10, 0, 0),
            vacancy_title='Target vacancy',
            vacancy_description='Target vacancy description.',
            employment_type='Full-time',
            profile='Filialleiter',
            region='Berlin',
            city='Berlin',
            salary_from=1000,
            salary_to=2000,
            tariff=None,
            work_experience='1 year',
            work_schedule='Full-time',
            standard=0,
            standard_plus=0,
            premium=0,
            callbacks=8,
        ),
    ]

    db_session.add_all(snapshots)
    await db_session.commit()


@pytest.mark.asyncio
async def test_run_pipeline_2_publication_activity_features_success(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """Test successful Pipeline 2 publication activity feature execution.
    Args:
        client (AsyncClient): Async API client.
        db_session (AsyncSession): Async database session.
    """
    await create_publication_activity_test_data(db_session=db_session)

    response = await client.post(
        '/pipeline-2/features/publication-activity/run',
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
    assert response_json['snapshot_count'] == 5
    assert response_json['feature_count'] == 5
    assert response_json['report_name'].endswith('.md')
    assert response_json['feature_run_id'] > 0

    feature_run_id = response_json['feature_run_id']

    feature_run = await db_session.scalar(
        select(FeatureRun).where(FeatureRun.id == feature_run_id),
    )
    publication_activity_features = (
        await db_session.scalars(
            select(PublicationActivityFeature)
            .where(
                PublicationActivityFeature.feature_run_id == feature_run_id,
            )
            .order_by(PublicationActivityFeature.date_day),
        )
    ).all()

    assert feature_run is not None
    assert feature_run.status == 'success'
    assert feature_run.is_success is True
    assert feature_run.snapshot_count == 5
    assert feature_run.feature_count == 5

    assert len(publication_activity_features) == 5

    assert [
        feature.publication_activity_level
        for feature in publication_activity_features
    ] == [1, 0, 0, 2, 0]

    assert [
        feature.days_since_last_publication_activity
        for feature in publication_activity_features
    ] == [0, 1, 2, 0, 1]
