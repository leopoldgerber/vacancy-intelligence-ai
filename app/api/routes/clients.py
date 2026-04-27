from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.client import ClientCreateRequest, ClientResponse
from app.db.session import get_session
from app.services.clients.persistence import get_client_by_id
from app.services.clients.service import create_client_entry


router = APIRouter(prefix='/clients', tags=['clients'])


@router.post('', response_model=ClientResponse)
async def create_client(
    payload: ClientCreateRequest,
    session: AsyncSession = Depends(get_session),
) -> ClientResponse:
    """Create client record.
    Args:
        payload (ClientCreateRequest): Client create payload.
        session (AsyncSession): Async database session."""
    existing_client = await get_client_by_id(
        session=session,
        client_id=payload.client_id,
    )

    if existing_client is not None:
        raise HTTPException(
            status_code=409,
            detail='Client with this id already exists.',
        )

    client = await create_client_entry(
        session=session,
        client_id=payload.client_id,
        name=payload.name,
        is_active=payload.is_active,
    )

    client_response = ClientResponse.model_validate(client)
    return client_response
