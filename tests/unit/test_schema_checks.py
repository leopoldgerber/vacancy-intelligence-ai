import pandas as pd

from app.services.data_validation.schema_checks import (
    check_column_name_unique,
    check_dataset_not_empty,
    check_required_columns,
    run_schema_checks,
)


def build_valid_dataframe() -> pd.DataFrame:
    """Build valid dataframe for schema checks.
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


def test_check_dataset_not_empty_success() -> None:
    """Test non-empty dataset check.
    Args:
        """
    data = build_valid_dataframe()

    result = check_dataset_not_empty(data=data)

    assert result['rule_name'] == 'dataset_not_empty'
    assert result['is_valid'] is True
    assert result['issue_count'] == 0
    assert result['message'] == 'Dataset is not empty.'


def test_check_dataset_not_empty_failure() -> None:
    """Test empty dataset check.
    Args:
        """
    data = pd.DataFrame()

    result = check_dataset_not_empty(data=data)

    assert result['rule_name'] == 'dataset_not_empty'
    assert result['is_valid'] is False
    assert result['issue_count'] == 1
    assert result['message'] == 'Dataset is empty.'


def test_check_column_name_unique_success() -> None:
    """Test unique column names check.
    Args:
        """
    data = build_valid_dataframe()

    result = check_column_name_unique(data=data)

    assert result['rule_name'] == 'column_name_unique'
    assert result['is_valid'] is True
    assert result['issue_count'] == 0
    assert result['message'] == 'Column names are unique.'


def test_check_required_columns_success() -> None:
    """Test required columns check success.
    Args:
        """
    data = build_valid_dataframe()
    required_columns = ['client_id', 'company_name', 'vacancy_id']

    result = check_required_columns(
        data=data,
        required_columns=required_columns,
    )

    assert result['rule_name'] == 'required_column_exists'
    assert result['is_valid'] is True
    assert result['issue_count'] == 0
    assert result['missing_columns'] == []
    assert result['message'] == 'All required columns exist.'


def test_check_required_columns_failure() -> None:
    """Test required columns check failure.
    Args:
        """
    data = build_valid_dataframe()
    required_columns = [
        'client_id',
        'company_name',
        'vacancy_id',
        'date_day',
    ]

    result = check_required_columns(
        data=data,
        required_columns=required_columns,
    )

    assert result['rule_name'] == 'required_column_exists'
    assert result['is_valid'] is False
    assert result['issue_count'] == 1
    assert result['missing_columns'] == ['date_day']
    assert result['message'] == 'Missing required columns: date_day.'


def test_run_schema_checks() -> None:
    """Test full schema checks execution.
    Args:
        """
    data = build_valid_dataframe()
    required_columns = ['client_id', 'company_name', 'vacancy_id']

    result = run_schema_checks(
        data=data,
        required_columns=required_columns,
    )

    assert 'dataset_not_empty' in result
    assert 'column_name_unique' in result
    assert 'required_columns' in result

    assert result['dataset_not_empty']['is_valid'] is True
    assert result['column_name_unique']['is_valid'] is True
    assert result['required_columns']['is_valid'] is True
