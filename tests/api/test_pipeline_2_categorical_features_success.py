from datetime import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.categorical_feature import CategoricalFeature
from app.db.models.client import Client
from app.db.models.company import Company
from app.db.models.feature_run import FeatureRun
from app.db.models.vacancy import Vacancy
from app.db.models.vacancy_snapshot import VacancySnapshot


async def create_categorical_feature_test_data(
    db_session: AsyncSession,
) -> None:
    """Create test data for categorical feature pipeline.
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
            employment_type='',
            profile='',
            publication_date=datetime(2025, 8, 2, 10, 0, 0),
            region='   ',
            city='',
            salary_from=None,
            salary_to=None,
            tariff=None,
            work_experience='   ',
            work_schedule='',
            standard=0,
            standard_plus=0,
            premium=0,
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
            date_day=datetime(2025, 8, 2, 0, 0, 0),
            publication_date=datetime(2025, 8, 2, 10, 0, 0),
            vacancy_title='Target vacancy two',
            vacancy_description='Target vacancy description.',
            employment_type='',
            profile='',
            region='   ',
            city='',
            salary_from=None,
            salary_to=None,
            tariff=None,
            work_experience='   ',
            work_schedule='',
            standard=0,
            standard_plus=0,
            premium=0,
            callbacks=3,
        ),
    ]

    db_session.add_all(snapshots)
    await db_session.commit()


@pytest.mark.asyncio
async def test_run_pipeline_2_categorical_features_success(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """Test successful Pipeline 2 categorical feature execution.
    Args:
        client (AsyncClient): Async API client.
        db_session (AsyncSession): Async database session.
    """
    await create_categorical_feature_test_data(db_session=db_session)

    response = await client.post(
        '/pipeline-2/features/categorical/run',
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
    assert response_json['snapshot_count'] == 2
    assert response_json['feature_count'] == 2
    assert response_json['report_name'].endswith('.md')
    assert response_json['feature_run_id'] > 0

    feature_run_id = response_json['feature_run_id']

    feature_run = await db_session.scalar(
        select(FeatureRun).where(FeatureRun.id == feature_run_id),
    )
    categorical_features = (
        await db_session.scalars(
            select(CategoricalFeature)
            .where(CategoricalFeature.feature_run_id == feature_run_id)
            .order_by(CategoricalFeature.vacancy_id),
        )
    ).all()

    assert feature_run is not None
    assert feature_run.status == 'success'
    assert feature_run.is_success is True
    assert feature_run.snapshot_count == 2
    assert feature_run.feature_count == 2

    assert len(categorical_features) == 2

    first_feature = categorical_features[0]
    second_feature = categorical_features[1]

    assert first_feature.vacancy_id == 100
    assert first_feature.city == 'Berlin'
    assert first_feature.region == 'Berlin'
    assert first_feature.profile == 'Filialleiter'
    assert first_feature.employment_type == 'Full-time'
    assert first_feature.work_experience == '1 year'
    assert first_feature.work_schedule == 'Full-time'

    assert second_feature.vacancy_id == 101
    assert second_feature.city == 'unknown'
    assert second_feature.region == 'unknown'
    assert second_feature.profile == 'unknown'
    assert second_feature.employment_type == 'unknown'
    assert second_feature.work_experience == 'unknown'
    assert second_feature.work_schedule == 'unknown'
