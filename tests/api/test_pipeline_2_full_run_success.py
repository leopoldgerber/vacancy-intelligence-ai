from datetime import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.analytics_run import AnalyticsRun
from app.db.models.categorical_feature import CategoricalFeature
from app.db.models.client import Client
from app.db.models.company import Company
from app.db.models.feature_run import FeatureRun
from app.db.models.ml_dataset_run import MlDatasetRun
from app.db.models.ml_feature_row import MlFeatureRow
from app.db.models.publication_activity_feature import (
    PublicationActivityFeature,
)
from app.db.models.salary_feature import SalaryFeature
from app.db.models.text_feature import TextFeature
from app.db.models.time_feature import TimeFeature
from app.db.models.vacancy import Vacancy
from app.db.models.vacancy_snapshot import VacancySnapshot


async def create_pipeline_2_full_run_test_data(
    db_session: AsyncSession,
) -> None:
    """Create test data for Pipeline 2 full run.
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
        name='competitor',
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
            vacancy_title='Filialleiter Vollzeit',
            vacancy_description=(
                'Wir bieten Gehalt, Weiterbildung und flexible '
                'Arbeitszeit. Du bringst Erfahrung mit. '
                'Bewirb dich jetzt.'
            ),
            employment_type='Full-time',
            profile='Filialleiter',
            publication_date=datetime(2025, 8, 1, 10, 30, 0),
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
            vacancy_id=200,
            client_id=1,
            company_id=20,
            vacancy_title='Filialleiter Premium',
            vacancy_description=(
                'Wir bieten Benefits, Gehalt und Karriere. '
                'Jetzt bewerben.'
            ),
            employment_type='Full-time',
            profile='Filialleiter',
            publication_date=datetime(2025, 8, 1, 11, 0, 0),
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
    ]

    db_session.add_all(vacancies)
    await db_session.flush()

    snapshots = [
        VacancySnapshot(
            client_id=1,
            company_id=10,
            vacancy_id=100,
            date_day=datetime(2025, 8, 4, 0, 0, 0),
            publication_date=datetime(2025, 8, 1, 10, 30, 0),
            vacancy_title='Filialleiter Vollzeit',
            vacancy_description=(
                'Wir bieten Gehalt, Weiterbildung und flexible '
                'Arbeitszeit. Du bringst Erfahrung mit. '
                'Bewirb dich jetzt.'
            ),
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
            callbacks=12,
        ),
        VacancySnapshot(
            client_id=1,
            company_id=20,
            vacancy_id=200,
            date_day=datetime(2025, 8, 4, 0, 0, 0),
            publication_date=datetime(2025, 8, 1, 11, 0, 0),
            vacancy_title='Filialleiter Premium',
            vacancy_description=(
                'Wir bieten Benefits, Gehalt und Karriere. '
                'Jetzt bewerben.'
            ),
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
            callbacks=25,
        ),
    ]

    db_session.add_all(snapshots)
    await db_session.commit()


@pytest.mark.asyncio
async def test_run_pipeline_2_full_run_success(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """Test successful Pipeline 2 full run.
    Args:
        client (AsyncClient): Async API client.
        db_session (AsyncSession): Async database session.
    """
    await create_pipeline_2_full_run_test_data(db_session=db_session)

    response = await client.post(
        '/pipeline-2/run',
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

    assert response_json['summary']['status'] == 'success'
    assert response_json['summary']['is_success'] is True
    assert response_json['summary']['snapshot_count'] == 2

    assert response_json['salary_features']['status'] == 'success'
    assert response_json['salary_features']['feature_count'] == 2

    assert (
        response_json['publication_activity_features']['status']
        == 'success'
    )
    assert (
        response_json['publication_activity_features']['feature_count']
        == 2
    )

    assert response_json['text_features']['status'] == 'success'
    assert response_json['text_features']['feature_count'] == 2

    assert response_json['time_features']['status'] == 'success'
    assert response_json['time_features']['feature_count'] == 2

    assert response_json['categorical_features']['status'] == 'success'
    assert response_json['categorical_features']['feature_count'] == 2

    assert response_json['ml_dataset']['status'] == 'success'
    assert response_json['ml_dataset']['is_success'] is True
    assert response_json['ml_dataset']['row_count'] == 2

    analytics_runs = (
        await db_session.scalars(select(AnalyticsRun))
    ).all()
    feature_runs = (
        await db_session.scalars(select(FeatureRun))
    ).all()
    salary_features = (
        await db_session.scalars(select(SalaryFeature))
    ).all()
    publication_activity_features = (
        await db_session.scalars(select(PublicationActivityFeature))
    ).all()
    text_features = (
        await db_session.scalars(select(TextFeature))
    ).all()
    time_features = (
        await db_session.scalars(select(TimeFeature))
    ).all()
    categorical_features = (
        await db_session.scalars(select(CategoricalFeature))
    ).all()
    ml_dataset_runs = (
        await db_session.scalars(select(MlDatasetRun))
    ).all()
    ml_feature_rows = (
        await db_session.scalars(select(MlFeatureRow))
    ).all()

    assert len(analytics_runs) == 1
    assert len(feature_runs) == 5
    assert len(salary_features) == 2
    assert len(publication_activity_features) == 2
    assert len(text_features) == 2
    assert len(time_features) == 2
    assert len(categorical_features) == 2
    assert len(ml_dataset_runs) == 1
    assert len(ml_feature_rows) == 2

    ml_row = next(
        row for row in ml_feature_rows if row.vacancy_id == 100
    )

    assert ml_row.callbacks == 12
    assert ml_row.salary_mid == 1500.0
    assert ml_row.publication_activity_level == 1
    assert ml_row.title_word_count == 2
    assert ml_row.publication_hour == 10
    assert ml_row.city == 'Berlin'
    assert ml_row.profile == 'Filialleiter'
