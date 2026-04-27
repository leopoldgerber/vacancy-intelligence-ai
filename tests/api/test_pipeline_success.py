import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.client import Client
from tests.api.pipeline_helpers import build_test_dataframe
from tests.api.pipeline_helpers import build_xlsx_bytes


@pytest.mark.asyncio
async def test_run_pipeline_success(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """Test successful pipeline execution.
    Args:
        client (AsyncClient): Async API client.
        db_session (AsyncSession): Async database session."""
    test_client = Client(
        id=1,
        name='target_client',
        is_active=True,
    )
    db_session.add(test_client)
    await db_session.commit()

    data = build_test_dataframe()
    xlsx_bytes = build_xlsx_bytes(data=data)

    response = await client.post(
        '/pipeline/run',
        files={
            'file': (
                'test_input.xlsx',
                xlsx_bytes,
                'application/vnd.openxmlformats-'
                'officedocument.spreadsheetml.sheet',
            ),
        },
    )

    response_json = response.json()

    assert response.status_code == 200
    assert response_json['status'] == 'ok'
    assert response_json['message'] == 'Pipeline 1 completed successfully.'
    assert response_json['should_ingest'] is True
    assert response_json['company_count'] == 2
    assert response_json['vacancy_count'] == 2
    assert response_json['snapshot_count'] == 2


@pytest.mark.asyncio
async def test_run_pipeline_repeat_upload(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """Test repeated pipeline execution with the same file.
    Args:
        client (AsyncClient): Async API client.
        db_session (AsyncSession): Async database session."""
    test_client = Client(
        id=1,
        name='target_client',
        is_active=True,
    )
    db_session.add(test_client)
    await db_session.commit()

    data = build_test_dataframe()
    first_xlsx_bytes = build_xlsx_bytes(data=data)

    first_response = await client.post(
        '/pipeline/run',
        files={
            'file': (
                'test_input.xlsx',
                first_xlsx_bytes,
                'application/vnd.openxmlformats-'
                'officedocument.spreadsheetml.sheet',
            ),
        },
    )

    first_response_json = first_response.json()

    assert first_response.status_code == 200
    assert first_response_json['status'] == 'ok'
    assert first_response_json['message'] == (
        'Pipeline 1 completed successfully.'
    )
    assert first_response_json['should_ingest'] is True
    assert first_response_json['company_count'] == 2
    assert first_response_json['vacancy_count'] == 2
    assert first_response_json['snapshot_count'] == 2

    second_xlsx_bytes = build_xlsx_bytes(data=data)

    second_response = await client.post(
        '/pipeline/run',
        files={
            'file': (
                'test_input.xlsx',
                second_xlsx_bytes,
                'application/vnd.openxmlformats-'
                'officedocument.spreadsheetml.sheet',
            ),
        },
    )

    second_response_json = second_response.json()

    assert second_response.status_code == 200
    assert second_response_json['status'] == 'ok'
    assert second_response_json['message'] == (
        'Pipeline 1 completed successfully.'
    )
    assert second_response_json['should_ingest'] is True
    assert second_response_json['company_count'] == 2
    assert second_response_json['vacancy_count'] == 2
    assert second_response_json['snapshot_count'] == 0
