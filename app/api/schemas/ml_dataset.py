from pydantic import BaseModel


class MlDatasetRunResponse(BaseModel):
    """ML dataset run response schema."""

    ml_dataset_run_id: int
    dataset_run_name: str
    status: str
    is_success: bool
    row_count: int
    report_name: str
