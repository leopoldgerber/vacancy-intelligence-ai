from datetime import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.client import Client
from app.db.models.company import Company
from app.db.models.feature_run import FeatureRun
from app.db.models.text_feature import TextFeature
from app.db.models.vacancy import Vacancy
from app.db.models.vacancy_snapshot import VacancySnapshot


async def create_text_feature_test_data(
    db_session: AsyncSession,
) -> None:
    """Create test data for text feature pipeline.
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
            vacancy_title='Filialleiter Vollzeit',
            vacancy_description=(
                'Wir bieten Gehalt, Weiterbildung und flexible '
                'Arbeitszeit. Du bringst Erfahrung mit. '
                'Bewirb dich jetzt.'
            ),
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
            vacancy_title='Aushilfe',
            vacancy_description='',
            employment_type='Part-time',
            profile='Aushilfe',
            publication_date=datetime(2025, 8, 2, 10, 0, 0),
            region='Berlin',
            city='Berlin',
            salary_from=None,
            salary_to=None,
            tariff=None,
            work_experience='No experience',
            work_schedule='Flexible',
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
            callbacks=10,
        ),
        VacancySnapshot(
            client_id=1,
            company_id=10,
            vacancy_id=101,
            date_day=datetime(2025, 8, 2, 0, 0, 0),
            publication_date=datetime(2025, 8, 2, 10, 0, 0),
            vacancy_title='Aushilfe',
            vacancy_description='',
            employment_type='Part-time',
            profile='Aushilfe',
            region='Berlin',
            city='Berlin',
            salary_from=None,
            salary_to=None,
            tariff=None,
            work_experience='No experience',
            work_schedule='Flexible',
            standard=0,
            standard_plus=0,
            premium=0,
            callbacks=3,
        ),
    ]

    db_session.add_all(snapshots)
    await db_session.commit()


@pytest.mark.asyncio
async def test_run_pipeline_2_text_features_success(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """Test successful Pipeline 2 text feature execution.
    Args:
        client (AsyncClient): Async API client.
        db_session (AsyncSession): Async database session.
    """
    await create_text_feature_test_data(db_session=db_session)

    response = await client.post(
        '/pipeline-2/features/text/run',
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
    text_features = (
        await db_session.scalars(
            select(TextFeature)
            .where(TextFeature.feature_run_id == feature_run_id)
            .order_by(TextFeature.vacancy_id),
        )
    ).all()

    assert feature_run is not None
    assert feature_run.status == 'success'
    assert feature_run.is_success is True
    assert feature_run.snapshot_count == 2
    assert feature_run.feature_count == 2

    assert len(text_features) == 2

    first_feature = text_features[0]
    second_feature = text_features[1]

    assert first_feature.vacancy_id == 100
    assert first_feature.title_length == len('Filialleiter Vollzeit')
    assert first_feature.description_length > 0
    assert first_feature.title_word_count == 2
    assert first_feature.description_word_count > 0
    assert first_feature.has_description is True
    assert first_feature.description_is_empty is False
    assert first_feature.has_salary_mention is True
    assert first_feature.has_schedule_mention is True
    assert first_feature.has_requirements_mention is True
    assert first_feature.has_benefits_mention is True
    assert first_feature.has_call_to_action is True

    assert second_feature.vacancy_id == 101
    assert second_feature.title_length == len('Aushilfe')
    assert second_feature.description_length == 0
    assert second_feature.title_word_count == 1
    assert second_feature.description_word_count == 0
    assert second_feature.has_description is False
    assert second_feature.description_is_empty is True
    assert second_feature.has_salary_mention is False
    assert second_feature.has_schedule_mention is False
    assert second_feature.has_requirements_mention is False
    assert second_feature.has_benefits_mention is False
    assert second_feature.has_call_to_action is False
