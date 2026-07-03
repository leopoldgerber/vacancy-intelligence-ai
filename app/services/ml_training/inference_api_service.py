from app.db.session import SessionLocal
from app.services.ml_training.run_ml_inference_pipeline import (
    MlInferencePipelineResult,
    run_inference_pipeline,
)


async def run_ml_inference(
    client_id: int,
    ml_training_run_id: int | None = None,
) -> MlInferencePipelineResult:
    """Run ML inference from API layer.
    Args:
        client_id (int): Client identifier.
        ml_training_run_id (int | None):
            Optional ML training run identifier."""
    async with SessionLocal() as session:
        return await run_inference_pipeline(
            session=session,
            client_id=client_id,
            ml_training_run_id=ml_training_run_id,
        )
