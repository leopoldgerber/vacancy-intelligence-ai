from datetime import datetime

import pandas as pd


UNKNOWN_CATEGORY_VALUE = 'unknown'


def normalize_category_value(value: str | None) -> str:
    """Normalize categorical value.
    Args:
        value (str | None): Raw category value.
    """
    if value is None:
        return UNKNOWN_CATEGORY_VALUE

    normalized_value = str(value).strip()

    if not normalized_value:
        return UNKNOWN_CATEGORY_VALUE

    return normalized_value


def build_categorical_feature_dataframe(data: pd.DataFrame) -> pd.DataFrame:
    """Build categorical feature dataframe.
    Args:
        data (pd.DataFrame): Input snapshot dataframe.
    """
    if data.empty:
        return pd.DataFrame()

    feature_data = data.copy()

    categorical_columns = [
        'city',
        'region',
        'profile',
        'employment_type',
        'work_experience',
        'work_schedule',
    ]

    for column in categorical_columns:
        feature_data[column] = feature_data[column].apply(
            normalize_category_value,
        )

    return feature_data


def build_categorical_feature_rows(
    data: pd.DataFrame,
    feature_run_id: int,
) -> list[dict[str, int | str | datetime]]:
    """Build categorical feature rows for persistence.
    Args:
        data (pd.DataFrame): Input snapshot dataframe.
        feature_run_id (int): Feature run identifier.
    """
    feature_data = build_categorical_feature_dataframe(data=data)

    if feature_data.empty:
        return []

    rows = []

    for _, row in feature_data.iterrows():
        rows.append(
            {
                'feature_run_id': feature_run_id,
                'client_id': int(row['client_id']),
                'company_id': int(row['company_id']),
                'vacancy_id': int(row['vacancy_id']),
                'date_day': row['date_day'],
                'city': str(row['city']),
                'region': str(row['region']),
                'profile': str(row['profile']),
                'employment_type': str(row['employment_type']),
                'work_experience': str(row['work_experience']),
                'work_schedule': str(row['work_schedule']),
            },
        )

    return rows
