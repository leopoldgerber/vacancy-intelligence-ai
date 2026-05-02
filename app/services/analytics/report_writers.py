from pathlib import Path


ANALYTICS_REPORTS_DIR = Path(
    'artifacts/reports/pipeline_2/analytics',
)


def save_analytics_report(
    report_name: str,
    report_content: str,
) -> Path:
    """Save analytics report.
    Args:
        report_name (str): Report file name.
        report_content (str): Report content.
    """
    ANALYTICS_REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    report_path = ANALYTICS_REPORTS_DIR / report_name
    report_path.write_text(
        report_content,
        encoding='utf-8',
    )

    return report_path