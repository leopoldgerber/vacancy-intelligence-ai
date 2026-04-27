from pydantic import BaseModel


class ValidationUploadResponse(BaseModel):
    """Store validation upload response payload.
    Args:
        """
    status: str
    message: str
    validation_run_id: int
    report_path: str
