from fastapi import APIRouter

from app.api.schemas.ml_inference import MlInferenceRunRequest
from app.api.schemas.ml_inference import MlInferenceRunResponse
from app.services.ml_training.inference_api_service import run_ml_inference


router = APIRouter(tags=['pipeline-3'])


@router.post(
    '/pipeline-3/inference/run',
    response_model=MlInferenceRunResponse,
)
async def run_pipeline_3_inference(
    request: MlInferenceRunRequest,
) -> MlInferenceRunResponse:
    """Run Pipeline 3 ML inference.
    Args:
        request (MlInferenceRunRequest): ML inference request."""
    result = await run_ml_inference(
        client_id=request.client_id,
        ml_training_run_id=request.ml_training_run_id,
    )

    return MlInferenceRunResponse(
        ml_training_run_id=result.ml_training_run_id,
        training_run_name=result.training_run_name,
        ml_dataset_run_id=result.ml_dataset_run_id,
        client_id=result.client_id,
        model_path=result.model_path,
        row_count=result.row_count,
        prediction_row_count=result.prediction_row_count,
        predictions=result.predictions,
        prediction_rows=result.prediction_rows,
    )
