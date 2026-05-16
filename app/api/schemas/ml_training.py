from pydantic import BaseModel


class MlTrainingRunResponse(BaseModel):
    """ML training run response schema."""

    ml_training_run_id: int
    training_run_name: str
    status: str
    is_success: bool
    model_type: str
    target_name: str
    train_row_count: int
    test_row_count: int
    metric_mae: float | None
    metric_rmse: float | None
    metric_r2: float | None
    model_path: str | None
    report_name: str | None
