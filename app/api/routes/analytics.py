from datetime import datetime

from fastapi import APIRouter
from fastapi import Form

from app.api.schemas.analytics import AnalyticsRunResponse
from app.services.analytics.service import run_analytics


router = APIRouter(
    prefix='/pipeline-2',
    tags=['pipeline'],
)


@router.post('/run', response_model=AnalyticsRunResponse)
async def run_pipeline_2(
    client_id: int = Form(1),
    date_from: datetime = Form('2025-08-01'),
    date_to: datetime = Form('2025-08-21'),
) -> AnalyticsRunResponse:
    """Run Pipeline 2 analytics.
    Args:
        client_id (int): Client identifier.
        date_from (datetime): Analytics period start.
        date_to (datetime): Analytics period end.
    """
    analytics_result = await run_analytics(
        client_id=client_id,
        date_from=date_from,
        date_to=date_to,
    )

    return AnalyticsRunResponse(**analytics_result)
