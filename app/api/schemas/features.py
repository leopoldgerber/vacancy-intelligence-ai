from pydantic import BaseModel


class FeatureRunResponse(BaseModel):
    """Feature engineering run response schema."""

    feature_run_id: int
    feature_run_name: str
    status: str
    is_success: bool
    snapshot_count: int
    feature_count: int
    report_name: str
