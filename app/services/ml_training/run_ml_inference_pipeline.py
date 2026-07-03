from dataclasses import dataclass
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.ml_training_run import MlTrainingRun
from app.services.ml_training.inference_artifact_savers import (
    build_report_name,
    save_inference_report,
)
from app.services.ml_training.inference_loaders import load_inference_dataframe
from app.services.ml_training.inference_loaders import resolve_training_run
from app.services.ml_training.inference_loaders import validate_training_run
from app.services.ml_training.inference_service import MlInferenceResult
from app.services.ml_training.inference_service import run_ml_inference


@dataclass
class MlInferencePipelineResult:
    """ML inference pipeline result."""

    ml_training_run_id: int
    training_run_name: str
    ml_dataset_run_id: int
    client_id: int
    model_path: str
    row_count: int
    prediction_row_count: int
    predictions: list[float]
    prediction_rows: list[dict[str, Any]]
    report_name: str | None = None
    report_path: str | None = None


def build_pipeline_result(
    ml_training_run: MlTrainingRun,
    inference_result: MlInferenceResult,
) -> MlInferencePipelineResult:
    """Build ML inference pipeline result.
    Args:
        ml_training_run (MlTrainingRun): ML training run used for inference.
        inference_result (MlInferenceResult): ML inference result."""
    ml_dataset_run_id = ml_training_run.ml_dataset_run_id
    model_path = ml_training_run.model_path

    if ml_dataset_run_id is None:
        raise ValueError('ML training run has no ML dataset run identifier.')

    if not model_path:
        raise ValueError('ML training run has no model artifact path.')

    return MlInferencePipelineResult(
        ml_training_run_id=ml_training_run.id,
        training_run_name=ml_training_run.training_run_name,
        ml_dataset_run_id=ml_dataset_run_id,
        client_id=ml_training_run.client_id,
        model_path=model_path,
        row_count=inference_result.row_count,
        prediction_row_count=inference_result.prediction_row_count,
        predictions=inference_result.predictions,
        prediction_rows=inference_result.prediction_rows,
    )


def save_pipeline_report(
    result: MlInferencePipelineResult,
) -> MlInferencePipelineResult:
    """Save ML inference pipeline report.
    Args:
        result (MlInferencePipelineResult): ML inference pipeline result."""
    report_name = build_report_name(
        training_run_name=result.training_run_name,
    )
    report_path = save_inference_report(result=result)
    result.report_name = report_name
    result.report_path = report_path

    return result


async def run_inference_pipeline(
    session: AsyncSession,
    client_id: int,
    ml_training_run_id: int | None = None,
) -> MlInferencePipelineResult:
    """Run DB-backed ML inference pipeline.
    Args:
        session (AsyncSession): Database session.
        client_id (int): Client identifier.
        ml_training_run_id (int | None):
            Optional ML training run identifier."""
    ml_training_run = await resolve_training_run(
        session=session,
        client_id=client_id,
        ml_training_run_id=ml_training_run_id,
    )
    validated_training_run = validate_training_run(
        ml_training_run=ml_training_run,
    )

    ml_dataset_run_id = validated_training_run.ml_dataset_run_id
    model_path = validated_training_run.model_path

    if ml_dataset_run_id is None:
        raise ValueError('ML training run has no ML dataset run identifier.')

    if not model_path:
        raise ValueError('ML training run has no model artifact path.')

    inference_dataframe = await load_inference_dataframe(
        session=session,
        ml_dataset_run_id=ml_dataset_run_id,
    )
    inference_result = run_ml_inference(
        model_path=model_path,
        data=inference_dataframe,
    )
    pipeline_result = build_pipeline_result(
        ml_training_run=validated_training_run,
        inference_result=inference_result,
    )

    return save_pipeline_report(result=pipeline_result)
