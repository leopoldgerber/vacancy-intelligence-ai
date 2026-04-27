import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_client_duplicate_id(
    client: AsyncClient,
) -> None:
    """Test client creation with duplicate identifier.
    Args:
        client (AsyncClient): Async API client."""
    first_response = await client.post(
        '/clients',
        json={
            'client_id': 1,
            'name': 'target_client',
            'is_active': True,
        },
    )

    assert first_response.status_code == 200

    second_response = await client.post(
        '/clients',
        json={
            'client_id': 1,
            'name': 'target_client_duplicate',
            'is_active': True,
        },
    )

    response_json = second_response.json()

    assert second_response.status_code == 409
    assert response_json['detail'] == 'Client with this id already exists.'
