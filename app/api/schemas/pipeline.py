from pydantic import BaseModel


class PipelineUploadResponse(BaseModel):
    """Store pipeline upload response payload.
    Args:
        """
    status: str
    message: str
    should_ingest: bool
    company_count: int | None
    vacancy_count: int | None
    snapshot_count: int | None
