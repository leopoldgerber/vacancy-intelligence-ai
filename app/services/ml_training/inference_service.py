from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from app.services.ml_training.inference_builders import build_inference_dataset
from app.services.ml_training.inference_builders import build_inference_rows
from app.services.ml_training.inference_builders import (
    predict_inference_dataset)
from app.services.ml_training.model_loaders import load_catboost_model


@dataclass
class MlInferenceResult:
    """ML inference result."""

    model_path: str
    row_count: int
    prediction_row_count: int
    predictions: list[float]
    prediction_rows: list[dict[str, Any]]


def build_inference_result(
    model_path: str | Path,
    row_count: int,
    prediction_rows: list[dict[str, Any]],
) -> MlInferenceResult:
    """Build ML inference result.
    Args:
        model_path (str | Path): Model artifact path.
        row_count (int): Source row count.
        prediction_rows (list[dict[str, Any]]): Built prediction rows."""
    predictions = [
        float(prediction_row['predicted_value'])
        for prediction_row in prediction_rows
    ]

    return MlInferenceResult(
        model_path=str(model_path),
        row_count=row_count,
        prediction_row_count=len(prediction_rows),
        predictions=predictions,
        prediction_rows=prediction_rows,
    )


def run_ml_inference(
    model_path: str | Path,
    data: pd.DataFrame,
) -> MlInferenceResult:
    """Run ML inference flow.
    Args:
        model_path (str | Path): Model artifact path.
        data (pd.DataFrame): Source inference dataframe."""
    model = load_catboost_model(model_path=model_path)
    dataset = build_inference_dataset(data=data)
    predictions = predict_inference_dataset(
        model=model,
        dataset=dataset,
    )
    prediction_rows = build_inference_rows(
        source_data=dataset.source_data,
        predictions=predictions,
    )

    return build_inference_result(
        model_path=model_path,
        row_count=dataset.row_count,
        prediction_rows=prediction_rows,
    )
