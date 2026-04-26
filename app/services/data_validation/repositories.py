from app.db.models.validation_issue import ValidationIssue
from app.db.models.validation_run import ValidationRun


def create_validation_run(
    validation_run_data: dict[str, str | int | bool],
) -> ValidationRun:
    """Create validation run model instance.
    Args:
        validation_run_data (dict[str, str | int | bool]): Validation run
            payload."""
    validation_run = ValidationRun(**validation_run_data)
    return validation_run


def create_validation_issue(
    validation_run_id: int,
    validation_issue_data: dict[str, int],
) -> ValidationIssue:
    """Create validation issue model instance.
    Args:
        validation_run_id (int): Validation run identifier.
        validation_issue_data (dict[str, int]): Validation issue payload."""
    validation_issue = ValidationIssue(
        validation_run_id=validation_run_id,
        **validation_issue_data,
    )
    return validation_issue
