import pandas as pd


def check_dataset_not_empty(data: pd.DataFrame) -> dict[str, int | str]:
    """Check that dataset is not empty.
    Args:
        data (pd.DataFrame): Input dataset."""
    row_count = int(len(data))
    is_valid = row_count > 0

    result = {
        'rule_name': 'dataset_not_empty',
        'is_valid': is_valid,
        'issue_count': 0 if is_valid else 1,
        'message': (
            'Dataset is not empty.' if is_valid else 'Dataset is empty.'),
    }
    return result


def check_column_name_unique(data: pd.DataFrame) -> dict[str, int | str]:
    """Check that column names are unique.
    Args:
        data (pd.DataFrame): Input dataset."""
    duplicate_count = int(data.columns.duplicated().sum())
    is_valid = duplicate_count == 0

    result = {
        'rule_name': 'column_name_unique',
        'is_valid': is_valid,
        'issue_count': duplicate_count,
        'message': (
            'Column names are unique.'
            if is_valid
            else 'Duplicate column names were found.'
        ),
    }
    return result


def check_required_columns(
    data: pd.DataFrame,
    required_columns: list[str],
) -> dict[str, bool | int | list[str] | str]:
    """Check that all required columns exist.
    Args:
        data (pd.DataFrame): Input dataset.
        required_columns (list[str]): Required column names."""
    missing_columns = [
        column_name
        for column_name in required_columns
        if column_name not in data.columns
    ]
    is_valid = len(missing_columns) == 0

    result = {
        'rule_name': 'required_column_exists',
        'is_valid': is_valid,
        'issue_count': len(missing_columns),
        'missing_columns': missing_columns,
        'message': (
            'All required columns exist.'
            if is_valid
            else f'Missing required columns: {", ".join(missing_columns)}.'
        ),
    }
    return result


def run_schema_checks(
    data: pd.DataFrame,
    required_columns: list[str],
) -> dict[str, dict[str, bool | int | list[str] | str]]:
    """Run schema-level validation checks.
    Args:
        data (pd.DataFrame): Input dataset.
        required_columns (list[str]): Required column names."""
    dataset_not_empty_result = check_dataset_not_empty(data=data)
    column_name_unique_result = check_column_name_unique(data=data)
    required_columns_result = check_required_columns(
        data=data,
        required_columns=required_columns,
    )

    schema_results = {
        'dataset_not_empty': dataset_not_empty_result,
        'column_name_unique': column_name_unique_result,
        'required_columns': required_columns_result,
    }
    return schema_results
