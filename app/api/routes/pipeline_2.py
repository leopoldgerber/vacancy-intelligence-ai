from datetime import datetime

from fastapi import APIRouter
from fastapi import Form

from app.api.schemas.pipeline_2 import Pipeline2FullRunResponse
from app.services.pipeline_2.service import run_pipeline_2_full


router = APIRouter(
    prefix='/pipeline-2',
    tags=['pipeline'],
)


@router.post('/run', response_model=Pipeline2FullRunResponse)
async def run_pipeline_2(
    client_id: int = Form(1),
    date_from: datetime = Form('2025-08-01'),
    date_to: datetime = Form('2025-08-21'),
) -> Pipeline2FullRunResponse:
    """Run full Pipeline 2.
    Args:
        client_id (int): Client identifier.
        date_from (datetime): Pipeline period start.
        date_to (datetime): Pipeline period end.
    """
    pipeline_result = await run_pipeline_2_full(
        client_id=client_id,
        date_from=date_from,
        date_to=date_to,
    )

    return Pipeline2FullRunResponse(**pipeline_result)
