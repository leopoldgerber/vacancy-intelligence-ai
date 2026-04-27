import pandas as pd


def build_quality_run_data(
    data: pd.DataFrame,
    quality_name: str,
    source_name: str,
    report_name: str,
    warning_count: int,
) -> dict[str, str | int]:
    """Build data for quality_runs table.
    Args:
        data (pd.DataFrame): Input dataset.
        quality_name (str): Quality run name.
        source_name (str): Source dataset name.
        report_name (str): Markdown report name.
        warning_count (int): Total warning count."""
    quality_run_data = {
        'quality_name': quality_name,
        'source_name': source_name,
        'warning_count': warning_count,
        'report_name': report_name,
    }
    return quality_run_data


def build_quality_issue_data(
    quality_results: dict[str, dict[str, int | str]],
) -> dict[str, int]:
    """Build aggregated data for quality_issues table.
    Args:
        quality_results (dict[str, dict[str, int | str]]): Quality check
            results."""
    quality_issue_data = {
        'missing_values_count': int(
            quality_results['missing_values']['issue_count']
        ),
        'duplicate_row_count': int(
            quality_results['duplicate_rows']['issue_count']
        ),
        'empty_text_values_count': int(
            quality_results['empty_text_values']['issue_count']
        ),
        'whitespace_text_values_count': int(
            quality_results['whitespace_text_values']['issue_count']
        ),
    }
    return quality_issue_data


def build_warning_count(
    quality_results: dict[str, dict[str, int | str]],
) -> int:
    """Build total warning count for quality checks.
    Args:
        quality_results (dict[str, dict[str, int | str]]): Quality check
            results."""
    warning_count = int(
        quality_results['missing_values']['issue_count']
        + quality_results['duplicate_rows']['issue_count']
        + quality_results['empty_text_values']['issue_count']
        + quality_results['whitespace_text_values']['issue_count']
    )
    return warning_count


def build_quality_result(
    data: pd.DataFrame,
    quality_name: str,
    source_name: str,
    report_name: str,
    quality_results: dict[str, dict[str, int | str]],
) -> dict[str, dict[str, str | int]]:
    """Build final quality result.
    Args:
        data (pd.DataFrame): Input dataset.
        quality_name (str): Quality run name.
        source_name (str): Source dataset name.
        report_name (str): Markdown report name.
        quality_results (dict[str, dict[str, int | str]]): Quality check
            results."""
    warning_count = build_warning_count(
        quality_results=quality_results,
    )

    quality_run_data = build_quality_run_data(
        data=data,
        quality_name=quality_name,
        source_name=source_name,
        report_name=report_name,
        warning_count=warning_count,
    )

    quality_issue_data = build_quality_issue_data(
        quality_results=quality_results,
    )

    quality_result = {
        'quality_run': quality_run_data,
        'quality_issue': quality_issue_data,
    }
    return quality_result
