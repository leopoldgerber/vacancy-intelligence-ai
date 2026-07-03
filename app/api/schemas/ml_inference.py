from typing import Any

from pydantic import BaseModel


class MlInferenceRunRequest(BaseModel):
    client_id: int
    ml_training_run_id: int | None = None


class MlInferenceRunResponse(BaseModel):
    ml_training_run_id: int
    training_run_name: str
    ml_dataset_run_id: int
    client_id: int
    model_path: str
    row_count: int
    prediction_row_count: int
    predictions: list[float]
    prediction_rows: list[dict[str, Any]]
