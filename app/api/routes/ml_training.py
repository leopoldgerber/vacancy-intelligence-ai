from fastapi import APIRouter
from fastapi import Form

from app.api.schemas.ml_training import MlTrainingRunResponse
from app.services.ml_training.service import run_ml_training


router = APIRouter(
    prefix='/pipeline-3/training',
    tags=['pipeline'],
)


@router.post('/run', response_model=MlTrainingRunResponse)
async def run_pipeline_3_training(
    client_id: int = Form(1),
    ml_dataset_run_id: int | None = Form(None),
) -> MlTrainingRunResponse:
    """Run Pipeline 3 ML training.
    Args:
        client_id (int): Client identifier.
        ml_dataset_run_id (int | None): Optional ML dataset run identifier.
    """
    training_result = await run_ml_training(
        client_id=client_id,
        ml_dataset_run_id=ml_dataset_run_id,
    )

    return MlTrainingRunResponse(**training_result)
