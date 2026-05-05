from datetime import datetime

from fastapi import APIRouter
from fastapi import Form

from app.api.schemas.features import FeatureRunResponse
from app.services.features.service import run_publication_activity_features
from app.services.features.service import run_salary_features
from app.services.features.service import run_text_features


router = APIRouter(
    prefix='/pipeline-2/features',
    tags=['pipeline'],
)


@router.post('/salary/run', response_model=FeatureRunResponse)
async def run_pipeline_2_salary_features(
    client_id: int = Form(1),
    date_from: datetime = Form('2025-08-01'),
    date_to: datetime = Form('2025-08-21'),
) -> FeatureRunResponse:
    """Run Pipeline 2 salary feature engineering.
    Args:
        client_id (int): Client identifier.
        date_from (datetime): Feature period start.
        date_to (datetime): Feature period end.
    """
    feature_result = await run_salary_features(
        client_id=client_id,
        date_from=date_from,
        date_to=date_to,
    )

    return FeatureRunResponse(**feature_result)


@router.post(
    '/publication-activity/run',
    response_model=FeatureRunResponse,
)
async def run_pipeline_2_publication_activity_features(
    client_id: int = Form(1),
    date_from: datetime = Form('2025-08-01'),
    date_to: datetime = Form('2025-08-21'),
) -> FeatureRunResponse:
    """Run Pipeline 2 publication activity feature engineering.
    Args:
        client_id (int): Client identifier.
        date_from (datetime): Feature period start.
        date_to (datetime): Feature period end.
    """
    feature_result = await run_publication_activity_features(
        client_id=client_id,
        date_from=date_from,
        date_to=date_to,
    )

    return FeatureRunResponse(**feature_result)


@router.post('/text/run', response_model=FeatureRunResponse)
async def run_pipeline_2_text_features(
    client_id: int = Form(1),
    date_from: datetime = Form('2025-08-01'),
    date_to: datetime = Form('2025-08-21'),
) -> FeatureRunResponse:
    """Run Pipeline 2 text feature engineering.
    Args:
        client_id (int): Client identifier.
        date_from (datetime): Feature period start.
        date_to (datetime): Feature period end.
    """
    feature_result = await run_text_features(
        client_id=client_id,
        date_from=date_from,
        date_to=date_to,
    )

    return FeatureRunResponse(**feature_result)
