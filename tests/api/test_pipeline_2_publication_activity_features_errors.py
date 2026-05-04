import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.client import Client
from app.db.models.feature_run import FeatureRun
from app.db.models.publication_activity_feature import (
    PublicationActivityFeature,
)


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
async def test_run_pipeline_2_publication_activity_features_no_data(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """Test Pipeline 2 publication activity feature execution without data.
    Args:
        client (AsyncClient): Async API client.
        db_session (AsyncSession): Async database session.
    """
    await create_client_only(db_session=db_session)

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
    assert response_json['status'] == 'no_data'
    assert response_json['is_success'] is False
    assert response_json['snapshot_count'] == 0
    assert response_json['feature_count'] == 0
    assert response_json['report_name'].endswith('.md')
    assert response_json['feature_run_id'] > 0

    feature_run_id = response_json['feature_run_id']

    feature_run = await db_session.scalar(
        select(FeatureRun).where(FeatureRun.id == feature_run_id),
    )
    publication_activity_features = (
        await db_session.scalars(
            select(PublicationActivityFeature).where(
                PublicationActivityFeature.feature_run_id == feature_run_id,
            ),
        )
    ).all()

    assert feature_run is not None
    assert feature_run.status == 'no_data'
    assert feature_run.is_success is False
    assert feature_run.snapshot_count == 0
    assert feature_run.feature_count == 0

    assert publication_activity_features == []
