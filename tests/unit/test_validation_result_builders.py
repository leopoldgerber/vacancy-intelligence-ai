import pandas as pd

from app.services.data_validation.result_builders import (
    build_error_count,
    build_validation_issue_data,
    build_validation_result,
    build_validation_run_data,
    build_validation_status,
    build_warning_count,
)


def build_test_dataframe() -> pd.DataFrame:
    """Build dataframe for validation result builder tests.
    Args:
        """
    data = pd.DataFrame(
        {
            'client_id': [1, 1],
            'company_name': ['company_1', 'company_2'],
            'vacancy_id': [101, 102],
        }
    )
    return data


def build_schema_results() -> dict[str, dict[str, object]]:
    """Build schema check results.
    Args:
        """
    schema_results = {
        'dataset_not_empty': {
            'rule_name': 'dataset_not_empty',
            'is_valid': True,
            'issue_count': 0,
        },
        'column_name_unique': {
            'rule_name': 'column_name_unique',
            'is_valid': True,
            'issue_count': 0,
        },
        'required_columns': {
            'rule_name': 'required_column_exists',
            'is_valid': False,
            'issue_count': 1,
            'missing_columns': ['date_day'],
        },
    }
    return schema_results


def build_blocking_results() -> list[dict[str, object]]:
    """Build blocking check results.
    Args:
        """
    blocking_results = [
        {
            'field_name': 'client_id',
            'rule_name': 'value_not_empty',
            'is_valid': True,
            'issue_count': 0,
        },
        {
            'field_name': 'vacancy_id',
            'rule_name': 'value_is_integer',
            'is_valid': False,
            'issue_count': 2,
        },
        {
            'field_name': 'date_day',
            'rule_name': 'value_matches_datetime_format',
            'is_valid': False,
            'issue_count': 3,
        },
        {
            'field_name': 'client_id',
            'rule_name': 'reference_exists_in_clients',
            'is_valid': False,
            'issue_count': 4,
        },
    ]
    return blocking_results


def build_warning_results() -> list[dict[str, object]]:
    """Build warning check results.
    Args:
        """
    warning_results = [
        {
            'field_name': 'tariff',
            'rule_name': 'value_not_empty',
            'is_valid': False,
            'issue_count': 5,
        },
        {
            'field_name': 'salary_from',
            'rule_name': 'value_is_numeric_if_present',
            'is_valid': True,
            'issue_count': 0,
        },
    ]
    return warning_results


def test_build_validation_status_failed() -> None:
    """Test failed validation status.
    Args:
        """
    result = build_validation_status(
        error_count=1,
        warning_count=0,
    )

    assert result == 'failed'


def test_build_validation_status_passed_with_warnings() -> None:
    """Test passed with warnings validation status.
    Args:
        """
    result = build_validation_status(
        error_count=0,
        warning_count=2,
    )

    assert result == 'passed_with_warnings'


def test_build_validation_status_passed() -> None:
    """Test passed validation status.
    Args:
        """
    result = build_validation_status(
        error_count=0,
        warning_count=0,
    )

    assert result == 'passed'


def test_build_error_count() -> None:
    """Test error count builder.
    Args:
        """
    schema_results = build_schema_results()
    blocking_results = build_blocking_results()

    result = build_error_count(
        schema_results=schema_results,
        blocking_results=blocking_results,
    )

    assert result == 10


def test_build_warning_count() -> None:
    """Test warning count builder.
    Args:
        """
    warning_results = build_warning_results()

    result = build_warning_count(warning_results=warning_results)

    assert result == 5


def test_build_validation_issue_data() -> None:
    """Test validation issue data builder.
    Args:
        """
    schema_results = build_schema_results()
    blocking_results = build_blocking_results()

    result = build_validation_issue_data(
        schema_results=schema_results,
        blocking_results=blocking_results,
    )

    assert result == {
        'missing_required_columns_count': 1,
        'empty_blocking_values_count': 0,
        'invalid_type_values_count': 2,
        'invalid_datetime_values_count': 3,
        'invalid_reference_values_count': 4,
    }


def test_build_validation_run_data() -> None:
    """Test validation run data builder.
    Args:
        """
    data = build_test_dataframe()

    result = build_validation_run_data(
        data=data,
        validation_name='validation_2026-04-27_10-39-15',
        source_name='input.xlsx',
        report_name='validation_2026-04-27_10-39-15.md',
        error_count=0,
        warning_count=2,
    )

    assert result == {
        'validation_name': 'validation_2026-04-27_10-39-15',
        'source_name': 'input.xlsx',
        'status': 'passed_with_warnings',
        'is_valid': True,
        'error_count': 0,
        'warning_count': 2,
        'row_count': 2,
        'column_count': 3,
        'report_name': 'validation_2026-04-27_10-39-15.md',
    }


def test_build_validation_result() -> None:
    """Test final validation result builder.
    Args:
        """
    data = build_test_dataframe()
    schema_results = build_schema_results()
    blocking_results = build_blocking_results()
    warning_results = build_warning_results()

    result = build_validation_result(
        data=data,
        validation_name='validation_test',
        source_name='input.xlsx',
        report_name='validation_test.md',
        schema_results=schema_results,
        blocking_results=blocking_results,
        warning_results=warning_results,
    )

    assert result['validation_run']['validation_name'] == 'validation_test'
    assert result['validation_run']['source_name'] == 'input.xlsx'
    assert result['validation_run']['status'] == 'failed'
    assert result['validation_run']['is_valid'] is False
    assert result['validation_run']['error_count'] == 10
    assert result['validation_run']['warning_count'] == 5
    assert result['validation_issue']['missing_required_columns_count'] == 1
    assert result['validation_issue']['invalid_type_values_count'] == 2
    assert result['validation_issue']['invalid_datetime_values_count'] == 3
    assert result['validation_issue']['invalid_reference_values_count'] == 4
