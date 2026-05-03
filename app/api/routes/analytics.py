from datetime import datetime

from fastapi import APIRouter
from fastapi import Form

from app.api.schemas.analytics import AnalyticsRunResponse
from app.services.analytics.service import run_analytics


router = APIRouter(
    prefix='/pipeline-2/analytics/summary',
    tags=['pipeline'],
)


@router.post('/run', response_model=AnalyticsRunResponse)
async def run_pipeline_2_summary(
    client_id: int = Form(1),
    date_from: datetime = Form('2025-08-01'),
    date_to: datetime = Form('2025-08-21'),
    city: str | None = Form(None, examples=['Berlin']),
    profile: str | None = Form(None, examples=['Filialleiter']),
) -> AnalyticsRunResponse:
    """Run Pipeline 2 summary analytics.
    Args:
        client_id (int): Client identifier.
        date_from (datetime): Analytics period start.
        date_to (datetime): Analytics period end.
        city (str | None): City filter.
        profile (str | None): Profile filter.
    """
    analytics_result = await run_analytics(
        client_id=client_id,
        date_from=date_from,
        date_to=date_to,
        city=city,
        profile=profile,
    )

    return AnalyticsRunResponse(**analytics_result)
