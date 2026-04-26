import pandas as pd


def build_validation_status(
    error_count: int,
    warning_count: int,
) -> str:
    """Build validation status.
    Args:
        error_count (int): Total blocking error count.
        warning_count (int): Total warning count."""
    if error_count > 0:
        return 'failed'

    if warning_count > 0:
        return 'passed_with_warnings'

    return 'passed'


def build_validation_run_data(
    data: pd.DataFrame,
    validation_name: str,
    source_name: str,
    report_name: str,
    error_count: int,
    warning_count: int,
) -> dict[str, str | int | bool]:
    """Build data for validation_runs table.
    Args:
        data (pd.DataFrame): Input dataset.
        validation_name (str): Validation run name.
        source_name (str): Source dataset name.
        report_name (str): Markdown report name.
        error_count (int): Total blocking error count.
        warning_count (int): Total warning count."""
    status = build_validation_status(
        error_count=error_count,
        warning_count=warning_count,
    )

    validation_run_data = {
        'validation_name': validation_name,
        'source_name': source_name,
        'status': status,
        'is_valid': error_count == 0,
        'error_count': error_count,
        'warning_count': warning_count,
        'row_count': int(len(data)),
        'column_count': int(data.shape[1]),
        'report_name': report_name,
    }
    return validation_run_data


def build_validation_issue_data(
    schema_results: dict[str, dict[str, object]],
    blocking_results: list[dict[str, object]],
) -> dict[str, int]:
    """Build aggregated data for validation_issues table.
    Args:
        schema_results (dict[str, dict[str, object]]): Schema check results.
        blocking_results (list[dict[str, object]]): Blocking field check
            results."""
    missing_required_columns_count = int(
        schema_results['required_columns']['issue_count']
    )

    empty_blocking_values_count = int(
        sum(
            result['issue_count']
            for result in blocking_results
            if result['rule_name'] == 'value_not_empty'
        )
    )

    invalid_type_values_count = int(
        sum(
            result['issue_count']
            for result in blocking_results
            if result['rule_name'] in (
                'value_is_integer',
                'value_is_string',
            )
        )
    )

    invalid_datetime_values_count = int(
        sum(
            result['issue_count']
            for result in blocking_results
            if result['rule_name'] == 'value_matches_datetime_format'
        )
    )

    invalid_reference_values_count = int(
        sum(
            result['issue_count']
            for result in blocking_results
            if result['rule_name'] == 'reference_exists_in_clients'
        )
    )

    validation_issue_data = {
        'missing_required_columns_count': missing_required_columns_count,
        'empty_blocking_values_count': empty_blocking_values_count,
        'invalid_type_values_count': invalid_type_values_count,
        'invalid_datetime_values_count': invalid_datetime_values_count,
        'invalid_reference_values_count': invalid_reference_values_count,
    }
    return validation_issue_data


def build_error_count(
    schema_results: dict[str, dict[str, object]],
    blocking_results: list[dict[str, object]],
) -> int:
    """Build total blocking error count.
    Args:
        schema_results (dict[str, dict[str, object]]): Schema check results.
        blocking_results (list[dict[str, object]]): Blocking field check
            results."""
    schema_error_count = int(
        sum(
            result['issue_count']
            for result in schema_results.values()
            if not result['is_valid']
        )
    )

    blocking_error_count = int(
        sum(
            result['issue_count']
            for result in blocking_results
            if not result['is_valid']
        )
    )

    error_count = schema_error_count + blocking_error_count
    return error_count


def build_warning_count(
    warning_results: list[dict[str, object]],
) -> int:
    """Build total warning count.
    Args:
        warning_results (list[dict[str, object]]): Warning-level field check
            results."""
    warning_count = int(
        sum(
            result['issue_count']
            for result in warning_results
            if not result['is_valid']
        )
    )
    return warning_count


def build_validation_result(
    data: pd.DataFrame,
    validation_name: str,
    source_name: str,
    report_name: str,
    schema_results: dict[str, dict[str, object]],
    blocking_results: list[dict[str, object]],
    warning_results: list[dict[str, object]],
) -> dict[str, dict[str, str | int | bool]]:
    """Build final validation result.
    Args:
        data (pd.DataFrame): Input dataset.
        validation_name (str): Validation run name.
        source_name (str): Source dataset name.
        report_name (str): Markdown report name.
        schema_results (dict[str, dict[str, object]]): Schema check results.
        blocking_results (list[dict[str, object]]): Blocking field check
            results.
        warning_results (list[dict[str, object]]): Warning-level field check
            results."""
    error_count = build_error_count(
        schema_results=schema_results,
        blocking_results=blocking_results,
    )
    warning_count = build_warning_count(
        warning_results=warning_results,
    )

    validation_run_data = build_validation_run_data(
        data=data,
        validation_name=validation_name,
        source_name=source_name,
        report_name=report_name,
        error_count=error_count,
        warning_count=warning_count,
    )

    validation_issue_data = build_validation_issue_data(
        schema_results=schema_results,
        blocking_results=blocking_results,
    )

    validation_result = {
        'validation_run': validation_run_data,
        'validation_issue': validation_issue_data,
    }
    return validation_result
