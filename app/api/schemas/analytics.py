from pydantic import BaseModel


class AnalyticsRunResponse(BaseModel):
    """Analytics run response schema."""

    analytics_run_id: int
    analytics_name: str
    status: str
    is_success: bool
    snapshot_count: int
    report_name: str
