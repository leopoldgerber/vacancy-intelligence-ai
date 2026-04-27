import pandas as pd

from app.services.data_validation.field_checks import (
    check_reference_exists_in_clients,
    check_value_is_integer,
    check_value_matches_datetime_format,
    check_value_not_empty,
)


def test_check_value_not_empty_success() -> None:
    """Test not empty check success.
    Args:
        """
    data = pd.DataFrame(
        {
            'company_name': ['company_1', 'company_2'],
        }
    )

    result = check_value_not_empty(
        data=data,
        column_name='company_name',
    )

    assert result['field_name'] == 'company_name'
    assert result['rule_name'] == 'value_not_empty'
    assert result['is_valid'] is True
    assert result['issue_count'] == 0
    assert result['message'] == (
        'Column company_name does not contain empty values.'
    )


def test_check_value_not_empty_failure() -> None:
    """Test not empty check failure.
    Args:
        """
    data = pd.DataFrame(
        {
            'company_name': ['company_1', '', None, '   '],
        }
    )

    result = check_value_not_empty(
        data=data,
        column_name='company_name',
    )

    assert result['field_name'] == 'company_name'
    assert result['rule_name'] == 'value_not_empty'
    assert result['is_valid'] is False
    assert result['issue_count'] == 3
    assert result['message'] == 'Column company_name contains empty values.'


def test_check_value_is_integer_success() -> None:
    """Test integer check success.
    Args:
        """
    data = pd.DataFrame(
        {
            'client_id': [1, 2, 3],
        }
    )

    result = check_value_is_integer(
        data=data,
        column_name='client_id',
    )

    assert result['field_name'] == 'client_id'
    assert result['rule_name'] == 'value_is_integer'
    assert result['is_valid'] is True
    assert result['issue_count'] == 0
    assert result['message'] == (
        'Column client_id contains valid integer values.'
    )


def test_check_value_is_integer_failure() -> None:
    """Test integer check failure.
    Args:
        """
    data = pd.DataFrame(
        {
            'client_id': [1, 'bad_value', 2.5, None],
        }
    )

    result = check_value_is_integer(
        data=data,
        column_name='client_id',
    )

    assert result['field_name'] == 'client_id'
    assert result['rule_name'] == 'value_is_integer'
    assert result['is_valid'] is False
    assert result['issue_count'] == 2
    assert result['message'] == 'Column client_id contains non-integer values.'


def test_check_value_matches_datetime_format_success() -> None:
    """Test datetime format check success.
    Args:
        """
    data = pd.DataFrame(
        {
            'date_day': [
                '2025-08-04 00:00:00',
                '2025-08-05 11:30:00',
            ],
        }
    )

    result = check_value_matches_datetime_format(
        data=data,
        column_name='date_day',
        datetime_format='%Y-%m-%d %H:%M:%S',
    )

    assert result['field_name'] == 'date_day'
    assert result['rule_name'] == 'value_matches_datetime_format'
    assert result['is_valid'] is True
    assert result['issue_count'] == 0
    assert result['message'] == (
        'Column date_day matches datetime format %Y-%m-%d %H:%M:%S.'
    )


def test_check_value_matches_datetime_format_failure() -> None:
    """Test datetime format check failure.
    Args:
        """
    data = pd.DataFrame(
        {
            'date_day': [
                '2025-08-04 00:00:00',
                '04-08-2025 11:30:00',
                None,
            ],
        }
    )

    result = check_value_matches_datetime_format(
        data=data,
        column_name='date_day',
        datetime_format='%Y-%m-%d %H:%M:%S',
    )

    assert result['field_name'] == 'date_day'
    assert result['rule_name'] == 'value_matches_datetime_format'
    assert result['is_valid'] is False
    assert result['issue_count'] == 1
    assert result['message'] == (
        'Column date_day contains invalid datetime values.'
    )


def test_check_reference_exists_in_clients_success() -> None:
    """Test client reference check success.
    Args:
        """
    data = pd.DataFrame(
        {
            'client_id': [1, 2],
        }
    )

    result = check_reference_exists_in_clients(
        data=data,
        client_ids=[1, 2, 3],
        column_name='client_id',
    )

    assert result['field_name'] == 'client_id'
    assert result['rule_name'] == 'reference_exists_in_clients'
    assert result['is_valid'] is True
    assert result['issue_count'] == 0
    assert result['message'] == (
        'Column client_id contains valid client references.'
    )


def test_check_reference_exists_in_clients_failure() -> None:
    """Test client reference check failure.
    Args:
        """
    data = pd.DataFrame(
        {
            'client_id': [1, 99, None, 'bad_value'],
        }
    )

    result = check_reference_exists_in_clients(
        data=data,
        client_ids=[1, 2, 3],
        column_name='client_id',
    )

    assert result['field_name'] == 'client_id'
    assert result['rule_name'] == 'reference_exists_in_clients'
    assert result['is_valid'] is False
    assert result['issue_count'] == 1
    assert result['message'] == (
        'Column client_id contains unknown client references.'
    )
