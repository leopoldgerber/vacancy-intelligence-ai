from app.db.models.quality_issue import QualityIssue
from app.db.models.quality_run import QualityRun


def create_quality_run(
    quality_run_data: dict[str, str | int],
) -> QualityRun:
    """Create quality run model instance.
    Args:
        quality_run_data (dict[str, str | int]): Quality run payload."""
    quality_run = QualityRun(**quality_run_data)
    return quality_run


def create_quality_issue(
    quality_run_id: int,
    quality_issue_data: dict[str, int],
) -> QualityIssue:
    """Create quality issue model instance.
    Args:
        quality_run_id (int): Quality run identifier.
        quality_issue_data (dict[str, int]): Quality issue payload."""
    quality_issue = QualityIssue(
        quality_run_id=quality_run_id,
        **quality_issue_data,
    )
    return quality_issue
