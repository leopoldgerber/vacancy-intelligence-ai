from collections.abc import Sequence
import pandas as pd


def check_value_not_empty(
        data: pd.DataFrame,
        column_name: str
) -> dict[str, int | str | bool]:
    """Check that column values are not empty.
    Args:
        data (pd.DataFrame): Input dataset.
        column_name (str): Column name to validate."""
    column_series = data[column_name]

    def is_empty_value(value: object) -> bool:
        """Check whether value should be treated as empty.
        Args:
            value (object): Value to validate."""
        if pd.isna(value):
            return True

        if isinstance(value, str):
            return value.strip() == ''

        return False

    empty_mask = column_series.apply(is_empty_value)

    issue_count = int(empty_mask.sum())
    is_valid = issue_count == 0

    result = {
        'field_name': column_name,
        'rule_name': 'value_not_empty',
        'is_valid': is_valid,
        'issue_count': issue_count,
        'message': (
            f'Column {column_name} does not contain empty values.'
            if is_valid
            else f'Column {column_name} contains empty values.'
        ),
    }
    return result


def check_value_is_string(
        data: pd.DataFrame,
        column_name: str
) -> dict[str, int | str | bool]:
    """Check that non-empty column values are strings.
    Args:
        data (pd.DataFrame): Input dataset.
        column_name (str): Column name to validate."""
    column_series = data[column_name]
    non_empty_mask = ~column_series.isna()

    if non_empty_mask.any():
        invalid_mask = non_empty_mask & ~column_series.apply(
            lambda value: isinstance(value, str))
    else:
        invalid_mask = pd.Series(False, index=data.index)

    issue_count = int(invalid_mask.sum())
    is_valid = issue_count == 0

    result = {
        'field_name': column_name,
        'rule_name': 'value_is_string',
        'is_valid': is_valid,
        'issue_count': issue_count,
        'message': (
            f'Column {column_name} contains valid string values.'
            if is_valid
            else f'Column {column_name} contains non-string values.'
        ),
    }
    return result


def check_value_is_integer(
        data: pd.DataFrame,
        column_name: str
) -> dict[str, int | str | bool]:
    """Check that non-empty column values are integers.
    Args:
        data (pd.DataFrame): Input dataset.
        column_name (str): Column name to validate."""
    column_series = data[column_name]
    non_empty_mask = ~column_series.isna()

    if non_empty_mask.any():
        parsed_series = pd.to_numeric(
            column_series[non_empty_mask], errors='coerce')
        invalid_mask = pd.Series(False, index=data.index)
        invalid_mask.loc[non_empty_mask] = (
            parsed_series.isna()
            | (parsed_series % 1 != 0)
        )
    else:
        invalid_mask = pd.Series(False, index=data.index)

    issue_count = int(invalid_mask.sum())
    is_valid = issue_count == 0

    result = {
        'field_name': column_name,
        'rule_name': 'value_is_integer',
        'is_valid': is_valid,
        'issue_count': issue_count,
        'message': (
            f'Column {column_name} contains valid integer values.'
            if is_valid
            else f'Column {column_name} contains non-integer values.'
        ),
    }
    return result


def check_value_matches_datetime_format(
    data: pd.DataFrame,
    column_name: str,
    datetime_format: str,
) -> dict[str, int | str | bool]:
    """Check that non-empty column values match datetime format.
    Args:
        data (pd.DataFrame): Input dataset.
        column_name (str): Column name to validate.
        datetime_format (str): Datetime format string."""
    column_series = data[column_name]
    non_empty_mask = ~column_series.isna()

    if non_empty_mask.any():
        parsed_series = pd.to_datetime(
            column_series[non_empty_mask],
            format=datetime_format,
            errors='coerce',
        )
        invalid_mask = pd.Series(False, index=data.index)
        invalid_mask.loc[non_empty_mask] = parsed_series.isna()
    else:
        invalid_mask = pd.Series(False, index=data.index)

    issue_count = int(invalid_mask.sum())
    is_valid = issue_count == 0

    result = {
        'field_name': column_name,
        'rule_name': 'value_matches_datetime_format',
        'is_valid': is_valid,
        'issue_count': issue_count,
        'message': (
            f'Column {column_name} matches datetime format {datetime_format}.'
            if is_valid
            else f'Column {column_name} contains invalid datetime values.'
        ),
    }
    return result


def check_reference_exists_in_clients(
    data: pd.DataFrame,
    client_ids: Sequence[int],
    column_name: str = 'client_id',
) -> dict[str, int | str | bool]:
    """Check that client identifiers exist in clients reference.
    Args:
        data (pd.DataFrame): Input dataset.
        client_ids (Sequence[int]): Valid client identifiers.
        column_name (str): Column name to validate."""
    column_series = data[column_name]
    non_empty_mask = ~column_series.isna()

    if non_empty_mask.any():
        parsed_series = pd.to_numeric(
            column_series[non_empty_mask], errors='coerce')
        comparable_mask = parsed_series.notna() & (parsed_series % 1 == 0)
        invalid_mask = pd.Series(False, index=data.index)
        invalid_values_mask = (
            comparable_mask
            & ~parsed_series.astype(int).isin(client_ids)
        )
        invalid_mask.loc[parsed_series.index] = invalid_values_mask
    else:
        invalid_mask = pd.Series(False, index=data.index)

    issue_count = int(invalid_mask.sum())
    is_valid = issue_count == 0

    result = {
        'field_name': column_name,
        'rule_name': 'reference_exists_in_clients',
        'is_valid': is_valid,
        'issue_count': issue_count,
        'message': (
            f'Column {column_name} contains valid client references.'
            if is_valid
            else f'Column {column_name} contains unknown client references.'
        ),
    }
    return result


def check_value_is_numeric_if_present(
    data: pd.DataFrame,
    column_name: str,
) -> dict[str, int | str | bool]:
    """Check that non-empty column values are numeric.
    Args:
        data (pd.DataFrame): Input dataset.
        column_name (str): Column name to validate."""
    column_series = data[column_name]
    non_empty_mask = ~column_series.isna()

    if non_empty_mask.any():
        parsed_series = pd.to_numeric(
            column_series[non_empty_mask], errors='coerce')
        invalid_mask = pd.Series(False, index=data.index)
        invalid_mask.loc[non_empty_mask] = parsed_series.isna()
    else:
        invalid_mask = pd.Series(False, index=data.index)

    issue_count = int(invalid_mask.sum())
    is_valid = issue_count == 0

    result = {
        'field_name': column_name,
        'rule_name': 'value_is_numeric_if_present',
        'is_valid': is_valid,
        'issue_count': issue_count,
        'message': (
            f'Column {column_name} contains valid numeric values when present.'
            if is_valid
            else f'Column {column_name} contains invalid numeric values.'
        ),
    }
    return result


def run_blocking_field_checks(
    data: pd.DataFrame,
    client_ids: Sequence[int],
    datetime_format: str = '%Y-%m-%d %H:%M:%S',
) -> list[dict[str, int | str | bool]]:
    """Run blocking field validation checks.
    Args:
        data (pd.DataFrame): Input dataset.
        client_ids (Sequence[int]): Valid client identifiers.
        datetime_format (str): Datetime format string."""
    check_results = [
        check_value_not_empty(data=data, column_name='client_id'),
        check_value_is_integer(data=data, column_name='client_id'),
        check_reference_exists_in_clients(
            data=data,
            client_ids=client_ids,
            column_name='client_id'
        ),
        check_value_not_empty(data=data, column_name='company_name'),
        check_value_is_string(data=data, column_name='company_name'),
        check_value_not_empty(data=data, column_name='date_day'),
        check_value_matches_datetime_format(
            data=data,
            column_name='date_day',
            datetime_format=datetime_format,
        ),
        check_value_not_empty(data=data, column_name='publication_date'),
        check_value_matches_datetime_format(
            data=data,
            column_name='publication_date',
            datetime_format=datetime_format,
        ),
        check_value_not_empty(data=data, column_name='vacancy_id'),
        check_value_is_integer(data=data, column_name='vacancy_id'),
        check_value_not_empty(data=data, column_name='vacancy_title'),
        check_value_is_string(data=data, column_name='vacancy_title'),
        check_value_not_empty(data=data, column_name='callbacks'),
        check_value_is_integer(data=data, column_name='callbacks'),
        check_value_not_empty(data=data, column_name='city'),
        check_value_is_string(data=data, column_name='city'),
        check_value_not_empty(data=data, column_name='profile'),
        check_value_is_string(data=data, column_name='profile'),
        check_value_not_empty(data=data, column_name='region'),
        check_value_is_string(data=data, column_name='region'),
        check_value_not_empty(data=data, column_name='standard'),
        check_value_is_integer(data=data, column_name='standard'),
        check_value_not_empty(data=data, column_name='standard_plus'),
        check_value_is_integer(data=data, column_name='standard_plus'),
        check_value_not_empty(data=data, column_name='premium'),
        check_value_is_integer(data=data, column_name='premium'),
    ]
    return check_results


def run_warning_field_checks(
        data: pd.DataFrame
) -> list[dict[str, int | str | bool]]:
    """Run warning-level field validation checks.
    Args:
        data (pd.DataFrame): Input dataset."""
    check_results = [
        check_value_not_empty(data=data, column_name='employment_type'),
        check_value_is_string(data=data, column_name='employment_type'),
        check_value_is_numeric_if_present(
            data=data,
            column_name='salary_from'
        ),
        check_value_is_numeric_if_present(data=data, column_name='salary_to'),
        check_value_not_empty(data=data, column_name='tariff'),
        check_value_is_string(data=data, column_name='tariff'),
        check_value_not_empty(data=data, column_name='vacancy_description'),
        check_value_is_string(data=data, column_name='vacancy_description'),
        check_value_not_empty(data=data, column_name='work_experience'),
        check_value_is_string(data=data, column_name='work_experience'),
        check_value_not_empty(data=data, column_name='work_schedule'),
        check_value_is_string(data=data, column_name='work_schedule'),
    ]
    return check_results


if __name__ == '__main__':
    import pandas as pd

    data = pd.read_excel('data/input_sample.xlsx')
    client_ids = [1]

    blocking_results = run_blocking_field_checks(
        data=data,
        client_ids=client_ids,
    )

    warning_results = run_warning_field_checks(data=data)
    print(warning_results)
