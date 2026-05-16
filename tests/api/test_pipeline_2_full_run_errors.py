import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.analytics_run import AnalyticsRun
from app.db.models.categorical_feature import CategoricalFeature
from app.db.models.client import Client
from app.db.models.feature_run import FeatureRun
from app.db.models.ml_dataset_run import MlDatasetRun
from app.db.models.ml_feature_row import MlFeatureRow
from app.db.models.publication_activity_feature import (
    PublicationActivityFeature,
)
from app.db.models.salary_feature import SalaryFeature
from app.db.models.text_feature import TextFeature
from app.db.models.time_feature import TimeFeature


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
async def test_run_pipeline_2_full_run_no_data(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """Test Pipeline 2 full run without snapshot data.
    Args:
        client (AsyncClient): Async API client.
        db_session (AsyncSession): Async database session.
    """
    await create_client_only(db_session=db_session)

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
    assert response_json['status'] == 'partial_or_no_data'
    assert response_json['is_success'] is False

    assert response_json['summary']['status'] == 'no_data'
    assert response_json['summary']['is_success'] is False
    assert response_json['summary']['snapshot_count'] == 0

    assert response_json['salary_features']['status'] == 'no_data'
    assert response_json['salary_features']['is_success'] is False
    assert response_json['salary_features']['snapshot_count'] == 0
    assert response_json['salary_features']['feature_count'] == 0

    assert (
        response_json['publication_activity_features']['status']
        == 'no_data'
    )
    assert (
        response_json['publication_activity_features']['is_success']
        is False
    )
    assert (
        response_json['publication_activity_features']['snapshot_count']
        == 0
    )
    assert (
        response_json['publication_activity_features']['feature_count']
        == 0
    )

    assert response_json['text_features']['status'] == 'no_data'
    assert response_json['text_features']['is_success'] is False
    assert response_json['text_features']['snapshot_count'] == 0
    assert response_json['text_features']['feature_count'] == 0

    assert response_json['time_features']['status'] == 'no_data'
    assert response_json['time_features']['is_success'] is False
    assert response_json['time_features']['snapshot_count'] == 0
    assert response_json['time_features']['feature_count'] == 0

    assert response_json['categorical_features']['status'] == 'no_data'
    assert response_json['categorical_features']['is_success'] is False
    assert response_json['categorical_features']['snapshot_count'] == 0
    assert response_json['categorical_features']['feature_count'] == 0

    assert response_json['ml_dataset']['status'] == 'no_data'
    assert response_json['ml_dataset']['is_success'] is False
    assert response_json['ml_dataset']['row_count'] == 0

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
    assert len(salary_features) == 0
    assert len(publication_activity_features) == 0
    assert len(text_features) == 0
    assert len(time_features) == 0
    assert len(categorical_features) == 0
    assert len(ml_dataset_runs) == 1
    assert len(ml_feature_rows) == 0
