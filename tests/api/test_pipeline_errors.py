import pytest
from httpx import AsyncClient

from tests.api.pipeline_helpers import build_test_dataframe
from tests.api.pipeline_helpers import build_xlsx_bytes


@pytest.mark.asyncio
async def test_run_pipeline_invalid_file_extension(
    client: AsyncClient,
) -> None:
    """Test pipeline request with invalid file extension.
    Args:
        client (AsyncClient): Async API client."""
    response = await client.post(
        '/pipeline-1/run',
        files={
            'file': (
                'test_input.csv',
                b'col1,col2\n1,2',
                'text/csv',
            ),
        },
    )

    response_json = response.json()

    assert response.status_code == 400
    assert response_json['detail'] == 'Only .xlsx files are allowed.'


@pytest.mark.asyncio
async def test_run_pipeline_missing_client_reference(
    client: AsyncClient,
) -> None:
    """Test pipeline execution without client reference in database.
    Args:
        client (AsyncClient): Async API client."""
    data = build_test_dataframe()
    xlsx_bytes = build_xlsx_bytes(data=data)

    response = await client.post(
        '/pipeline-1/run',
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
    assert response_json['status'] == 'failed'
    assert response_json['message'] == (
        'Pipeline 1 failed on pre-ingestion checks.'
    )
    assert response_json['should_ingest'] is False
    assert response_json['company_count'] is None
    assert response_json['vacancy_count'] is None
    assert response_json['snapshot_count'] is None
