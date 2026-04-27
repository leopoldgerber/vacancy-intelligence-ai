from pathlib import Path

from app.db.models.quality_issue import QualityIssue
from app.db.models.quality_run import QualityRun


def build_quality_report(
    quality_run: QualityRun,
    quality_issue: QualityIssue,
) -> str:
    """Build markdown quality report.
    Args:
        quality_run (QualityRun): Quality run model instance.
        quality_issue (QualityIssue): Quality issue model instance."""
    report_text = f"""# Quality Report

## Quality Run

- quality_name: {quality_run.quality_name}
- source_name: {quality_run.source_name}
- warning_count: {quality_run.warning_count}
- report_name: {quality_run.report_name}
- created_at: {quality_run.created_at}

## Quality Issues

- missing_values_count: {quality_issue.missing_values_count}
- duplicate_row_count: {quality_issue.duplicate_row_count}
- empty_text_values_count: {quality_issue.empty_text_values_count}
- whitespace_text_values_count: {quality_issue.whitespace_text_values_count}
- created_at: {quality_issue.created_at}
"""
    return report_text


def save_quality_report(
    report_text: str,
    report_name: str,
    reports_dir: str = 'artifacts/reports/quality',
) -> str:
    """Save markdown quality report.
    Args:
        report_text (str): Markdown report content.
        report_name (str): Markdown report file name.
        reports_dir (str): Directory for quality reports."""
    reports_path = Path(reports_dir)
    reports_path.mkdir(parents=True, exist_ok=True)

    report_path = reports_path / report_name
    report_path.write_text(report_text, encoding='utf-8')

    return str(report_path)
