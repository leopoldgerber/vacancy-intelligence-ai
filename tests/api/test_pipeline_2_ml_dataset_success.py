from datetime import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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


async def create_ml_dataset_test_data(
    db_session: AsyncSession,
) -> None:
    """Create test data for ML dataset pipeline.
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
        vacancy_title='Filialleiter Vollzeit',
        vacancy_description='Wir bieten Gehalt. Bewirb dich jetzt.',
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
    )

    test_snapshot = VacancySnapshot(
        client_id=1,
        company_id=10,
        vacancy_id=100,
        date_day=datetime(2025, 8, 4, 0, 0, 0),
        publication_date=datetime(2025, 8, 1, 10, 30, 0),
        vacancy_title='Filialleiter Vollzeit',
        vacancy_description='Wir bieten Gehalt. Bewirb dich jetzt.',
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
    )

    db_session.add_all(
        [
            test_vacancy,
            test_snapshot,
        ],
    )
    await db_session.flush()

    salary_run = FeatureRun(
        feature_run_name='salary_features_2025-08-21_10-00-00',
        client_id=1,
        date_from=datetime(2025, 8, 1),
        date_to=datetime(2025, 8, 21),
        status='success',
        is_success=True,
        snapshot_count=1,
        feature_count=1,
        report_name='salary_features_2025-08-21_10-00-00.md',
    )
    publication_activity_run = FeatureRun(
        feature_run_name=(
            'publication_activity_features_2025-08-21_10-00-00'
        ),
        client_id=1,
        date_from=datetime(2025, 8, 1),
        date_to=datetime(2025, 8, 21),
        status='success',
        is_success=True,
        snapshot_count=1,
        feature_count=1,
        report_name=(
            'publication_activity_features_2025-08-21_10-00-00.md'
        ),
    )
    text_run = FeatureRun(
        feature_run_name='text_features_2025-08-21_10-00-00',
        client_id=1,
        date_from=datetime(2025, 8, 1),
        date_to=datetime(2025, 8, 21),
        status='success',
        is_success=True,
        snapshot_count=1,
        feature_count=1,
        report_name='text_features_2025-08-21_10-00-00.md',
    )
    time_run = FeatureRun(
        feature_run_name='time_features_2025-08-21_10-00-00',
        client_id=1,
        date_from=datetime(2025, 8, 1),
        date_to=datetime(2025, 8, 21),
        status='success',
        is_success=True,
        snapshot_count=1,
        feature_count=1,
        report_name='time_features_2025-08-21_10-00-00.md',
    )
    categorical_run = FeatureRun(
        feature_run_name='categorical_features_2025-08-21_10-00-00',
        client_id=1,
        date_from=datetime(2025, 8, 1),
        date_to=datetime(2025, 8, 21),
        status='success',
        is_success=True,
        snapshot_count=1,
        feature_count=1,
        report_name='categorical_features_2025-08-21_10-00-00.md',
    )

    db_session.add_all(
        [
            salary_run,
            publication_activity_run,
            text_run,
            time_run,
            categorical_run,
        ],
    )
    await db_session.flush()

    salary_feature = SalaryFeature(
        feature_run_id=salary_run.id,
        client_id=1,
        company_id=10,
        vacancy_id=100,
        date_day=datetime(2025, 8, 4, 0, 0, 0),
        salary_mid=1500.0,
        salary_is_specified=True,
        company_salary_median_by_city=1500.0,
        market_salary_median_excl_company_by_city=2000.0,
        salary_ratio_to_market_by_city=0.75,
        company_salary_median_by_profile=1500.0,
        market_salary_median_excl_company_by_profile=1800.0,
        salary_ratio_to_market_by_profile=0.8333333333,
        company_salary_median_by_city_profile=1500.0,
        market_salary_median_excl_company_by_city_profile=1750.0,
        salary_ratio_to_market_by_city_profile=0.8571428571,
    )
    publication_activity_feature = PublicationActivityFeature(
        feature_run_id=publication_activity_run.id,
        client_id=1,
        company_id=10,
        vacancy_id=100,
        date_day=datetime(2025, 8, 4, 0, 0, 0),
        publication_activity_level=2,
        days_since_last_publication_activity=0,
    )
    text_feature = TextFeature(
        feature_run_id=text_run.id,
        client_id=1,
        company_id=10,
        vacancy_id=100,
        date_day=datetime(2025, 8, 4, 0, 0, 0),
        title_length=21,
        description_length=39,
        title_word_count=2,
        description_word_count=6,
        has_description=True,
        description_is_empty=False,
        has_salary_mention=True,
        has_schedule_mention=False,
        has_requirements_mention=False,
        has_benefits_mention=True,
        has_call_to_action=True,
    )
    time_feature = TimeFeature(
        feature_run_id=time_run.id,
        client_id=1,
        company_id=10,
        vacancy_id=100,
        date_day=datetime(2025, 8, 4, 0, 0, 0),
        publication_hour=10,
        publication_day_of_week=4,
        publication_month=8,
        publication_week=31,
        is_weekend=False,
        vacancy_age_days=3,
    )
    categorical_feature = CategoricalFeature(
        feature_run_id=categorical_run.id,
        client_id=1,
        company_id=10,
        vacancy_id=100,
        date_day=datetime(2025, 8, 4, 0, 0, 0),
        city='Berlin',
        region='Berlin',
        profile='Filialleiter',
        employment_type='Full-time',
        work_experience='1 year',
        work_schedule='Full-time',
    )

    db_session.add_all(
        [
            salary_feature,
            publication_activity_feature,
            text_feature,
            time_feature,
            categorical_feature,
        ],
    )

    await db_session.commit()


@pytest.mark.asyncio
async def test_run_pipeline_2_ml_dataset_success(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """Test successful Pipeline 2 ML dataset execution.
    Args:
        client (AsyncClient): Async API client.
        db_session (AsyncSession): Async database session.
    """
    await create_ml_dataset_test_data(db_session=db_session)

    response = await client.post(
        '/pipeline-2/ml-dataset/run',
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
    assert response_json['row_count'] == 1
    assert response_json['report_name'].endswith('.md')
    assert response_json['ml_dataset_run_id'] > 0

    ml_dataset_run_id = response_json['ml_dataset_run_id']

    ml_dataset_run = await db_session.scalar(
        select(MlDatasetRun).where(
            MlDatasetRun.id == ml_dataset_run_id,
        ),
    )
    ml_feature_rows = (
        await db_session.scalars(
            select(MlFeatureRow).where(
                MlFeatureRow.ml_dataset_run_id == ml_dataset_run_id,
            ),
        )
    ).all()

    assert ml_dataset_run is not None
    assert ml_dataset_run.status == 'success'
    assert ml_dataset_run.is_success is True
    assert ml_dataset_run.row_count == 1

    assert ml_dataset_run.salary_feature_run_id is not None
    assert ml_dataset_run.publication_activity_feature_run_id is not None
    assert ml_dataset_run.text_feature_run_id is not None
    assert ml_dataset_run.time_feature_run_id is not None
    assert ml_dataset_run.categorical_feature_run_id is not None

    assert len(ml_feature_rows) == 1

    row = ml_feature_rows[0]

    assert row.client_id == 1
    assert row.company_id == 10
    assert row.vacancy_id == 100
    assert row.callbacks == 12

    assert row.salary_mid == 1500.0
    assert row.salary_is_specified is True
    assert row.salary_ratio_to_market_by_city == 0.75
    assert row.salary_ratio_to_market_by_profile == pytest.approx(
        0.8333333333,
    )
    assert row.salary_ratio_to_market_by_city_profile == pytest.approx(
        0.8571428571,
    )

    assert row.publication_activity_level == 2
    assert row.days_since_last_publication_activity == 0

    assert row.title_length == 21
    assert row.description_length == 39
    assert row.title_word_count == 2
    assert row.description_word_count == 6
    assert row.has_description is True
    assert row.description_is_empty is False
    assert row.has_salary_mention is True
    assert row.has_schedule_mention is False
    assert row.has_requirements_mention is False
    assert row.has_benefits_mention is True
    assert row.has_call_to_action is True

    assert row.publication_hour == 10
    assert row.publication_day_of_week == 4
    assert row.publication_month == 8
    assert row.publication_week == 31
    assert row.is_weekend is False
    assert row.vacancy_age_days == 3

    assert row.city == 'Berlin'
    assert row.region == 'Berlin'
    assert row.profile == 'Filialleiter'
    assert row.employment_type == 'Full-time'
    assert row.work_experience == '1 year'
    assert row.work_schedule == 'Full-time'
