import pandas as pd


def build_text_columns(data: pd.DataFrame) -> list[str]:
    """Build text column list for quality checks.
    Args:
        data (pd.DataFrame): Input dataset."""
    text_columns = [
        'city',
        'company_name',
        'employment_type',
        'profile',
        'region',
        'tariff',
        'vacancy_description',
        'vacancy_title',
        'work_experience',
        'work_schedule',
    ]
    quality_text_columns = [
        column_name
        for column_name in text_columns
        if column_name in data.columns
    ]
    return quality_text_columns


def check_sample_size(data: pd.DataFrame) -> dict[str, int]:
    """Check dataset sample size.
    Args:
        data (pd.DataFrame): Input dataset."""
    sample_result = {
        'row_count': int(len(data)),
        'column_count': int(data.shape[1]),
    }
    return sample_result


def check_missing_values(data: pd.DataFrame) -> dict[str, int | str]:
    """Check missing values in dataset.
    Args:
        data (pd.DataFrame): Input dataset."""
    missing_values_count = int(data.isna().sum().sum())

    result = {
        'rule_name': 'missing_values_check',
        'issue_count': missing_values_count,
        'message': (
            'Dataset does not contain missing values.'
            if missing_values_count == 0
            else 'Dataset contains missing values.'
        ),
    }
    return result


def check_duplicate_rows(data: pd.DataFrame) -> dict[str, int | str]:
    """Check duplicate rows in dataset.
    Args:
        data (pd.DataFrame): Input dataset."""
    duplicate_row_count = int(data.duplicated().sum())

    result = {
        'rule_name': 'duplicate_rows_check',
        'issue_count': duplicate_row_count,
        'message': (
            'Dataset does not contain duplicate rows.'
            if duplicate_row_count == 0
            else 'Dataset contains duplicate rows.'
        ),
    }
    return result


def check_empty_text_values(
    data: pd.DataFrame,
    text_columns: list[str],
) -> dict[str, int | str]:
    """Check empty text values in text columns.
    Args:
        data (pd.DataFrame): Input dataset.
        text_columns (list[str]): Text column names."""
    empty_text_values_count = 0

    for column_name in text_columns:
        column_series = data[column_name]

        def is_empty_value(value: object) -> bool:
            """Check whether text value is empty.
            Args:
                value (object): Value to validate."""
            if pd.isna(value):
                return True

            if isinstance(value, str):
                return value == ''

            return False

        empty_mask = column_series.apply(is_empty_value)
        empty_text_values_count += int(empty_mask.sum())

    result = {
        'rule_name': 'empty_text_values_check',
        'issue_count': empty_text_values_count,
        'message': (
            'Text columns do not contain empty values.'
            if empty_text_values_count == 0
            else 'Text columns contain empty values.'
        ),
    }
    return result


def check_whitespace_text_values(
    data: pd.DataFrame,
    text_columns: list[str],
) -> dict[str, int | str]:
    """Check whitespace-only text values in text columns.
    Args:
        data (pd.DataFrame): Input dataset.
        text_columns (list[str]): Text column names."""
    whitespace_text_values_count = 0

    for column_name in text_columns:
        column_series = data[column_name]

        def is_whitespace_value(value: object) -> bool:
            """Check whether text value contains only whitespace.
            Args:
                value (object): Value to validate."""
            if not isinstance(value, str):
                return False

            return value != '' and value.strip() == ''

        whitespace_mask = column_series.apply(is_whitespace_value)
        whitespace_text_values_count += int(whitespace_mask.sum())

    result = {
        'rule_name': 'whitespace_text_values_check',
        'issue_count': whitespace_text_values_count,
        'message': (
            'Text columns do not contain whitespace-only values.'
            if whitespace_text_values_count == 0
            else 'Text columns contain whitespace-only values.'
        ),
    }
    return result


def run_quality_checks(
    data: pd.DataFrame,
) -> dict[str, dict[str, int | str]]:
    """Run data quality checks.
    Args:
        data (pd.DataFrame): Input dataset."""
    text_columns = build_text_columns(data=data)

    sample_result = check_sample_size(data=data)
    missing_values_result = check_missing_values(data=data)
    duplicate_rows_result = check_duplicate_rows(data=data)
    empty_text_values_result = check_empty_text_values(
        data=data,
        text_columns=text_columns,
    )
    whitespace_text_values_result = check_whitespace_text_values(
        data=data,
        text_columns=text_columns,
    )

    quality_results = {
        'sample': sample_result,
        'missing_values': missing_values_result,
        'duplicate_rows': duplicate_rows_result,
        'empty_text_values': empty_text_values_result,
        'whitespace_text_values': whitespace_text_values_result,
    }
    return quality_results
