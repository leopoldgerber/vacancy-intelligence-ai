from datetime import datetime

from fastapi import APIRouter
from fastapi import Form

from app.api.schemas.ml_dataset import MlDatasetRunResponse
from app.services.ml_dataset.service import run_ml_dataset


router = APIRouter(
    prefix='/pipeline-2/ml-dataset',
    tags=['pipeline'],
)


@router.post('/run', response_model=MlDatasetRunResponse)
async def run_pipeline_2_ml_dataset(
    client_id: int = Form(1),
    date_from: datetime = Form('2025-08-01'),
    date_to: datetime = Form('2025-08-21'),
) -> MlDatasetRunResponse:
    """Run Pipeline 2 final ML dataset build.
    Args:
        client_id (int): Client identifier.
        date_from (datetime): Dataset period start.
        date_to (datetime): Dataset period end.
    """
    dataset_result = await run_ml_dataset(
        client_id=client_id,
        date_from=date_from,
        date_to=date_to,
    )

    return MlDatasetRunResponse(**dataset_result)
