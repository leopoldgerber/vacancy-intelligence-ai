from pathlib import Path

from app.db.models.validation_issue import ValidationIssue
from app.db.models.validation_run import ValidationRun


def build_validation_report(
    validation_run: ValidationRun,
    validation_issue: ValidationIssue,
) -> str:
    """Build markdown validation report.
    Args:
        validation_run (ValidationRun): Validation run model instance.
        validation_issue (ValidationIssue): Validation issue model instance."""
    report_text = f"""# Validation Report

## Validation Run

- validation_name: {validation_run.validation_name}
- source_name: {validation_run.source_name}
- status: {validation_run.status}
- is_valid: {validation_run.is_valid}
- error_count: {validation_run.error_count}
- warning_count: {validation_run.warning_count}
- row_count: {validation_run.row_count}
- column_count: {validation_run.column_count}
- report_name: {validation_run.report_name}
- created_at: {validation_run.created_at}

## Validation Issues

- missing_required_columns_count: {
    validation_issue.missing_required_columns_count
}
- empty_blocking_values_count: {
    validation_issue.empty_blocking_values_count
}
- invalid_type_values_count: {
    validation_issue.invalid_type_values_count
}
- invalid_datetime_values_count: {
    validation_issue.invalid_datetime_values_count
}
- invalid_reference_values_count: {
    validation_issue.invalid_reference_values_count
}
- created_at: {
    validation_issue.created_at
}
"""
    return report_text


def save_validation_report(
    report_text: str,
    report_name: str,
    reports_dir: str = 'artifacts/reports/validation',
) -> str:
    """Save markdown validation report.
    Args:
        report_text (str): Markdown report content.
        report_name (str): Markdown report file name.
        reports_dir (str): Directory for validation reports."""
    reports_path = Path(reports_dir)
    reports_path.mkdir(parents=True, exist_ok=True)

    report_path = reports_path / report_name
    report_path.write_text(report_text, encoding='utf-8')

    return str(report_path)
