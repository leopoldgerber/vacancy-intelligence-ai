from typing import Any

from pydantic import BaseModel


class MlTrainingRunResponse(BaseModel):
    """ML training run response schema."""

    ml_training_run_id: int
    training_run_name: str
    status: str
    is_success: bool
    model_type: str
    target_name: str
    model_params_json: dict[str, Any] | None
    feature_importance_json: dict[str, Any] | None
    train_row_count: int
    test_row_count: int
    metric_mae: float | None
    metric_rmse: float | None
    metric_r2: float | None
    baseline_mae: float | None
    mean_target: float | None
    model_path: str | None
    report_name: str | None
