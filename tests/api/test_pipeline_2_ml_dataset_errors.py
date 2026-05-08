import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.client import Client
from app.db.models.ml_dataset_run import MlDatasetRun
from app.db.models.ml_feature_row import MlFeatureRow


async def create_client_only(
    db_session: AsyncSession,
) -> None:
    """Create client without feature runs.
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
async def test_run_pipeline_2_ml_dataset_no_data_without_feature_runs(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """Test ML dataset execution without required feature runs.
    Args:
        client (AsyncClient): Async API client.
        db_session (AsyncSession): Async database session.
    """
    await create_client_only(db_session=db_session)

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
    assert response_json['status'] == 'no_data'
    assert response_json['is_success'] is False
    assert response_json['row_count'] == 0
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
    assert ml_dataset_run.status == 'no_data'
    assert ml_dataset_run.is_success is False
    assert ml_dataset_run.row_count == 0

    assert ml_dataset_run.salary_feature_run_id is None
    assert ml_dataset_run.publication_activity_feature_run_id is None
    assert ml_dataset_run.text_feature_run_id is None
    assert ml_dataset_run.time_feature_run_id is None
    assert ml_dataset_run.categorical_feature_run_id is None

    assert ml_feature_rows == []
