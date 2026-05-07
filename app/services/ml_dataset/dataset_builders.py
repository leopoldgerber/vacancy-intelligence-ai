from datetime import datetime

import pandas as pd


JOIN_KEYS = [
    'client_id',
    'company_id',
    'vacancy_id',
    'date_day',
]


def join_feature_dataframes(
    target_data: pd.DataFrame,
    salary_data: pd.DataFrame,
    publication_activity_data: pd.DataFrame,
    text_data: pd.DataFrame,
    time_data: pd.DataFrame,
    categorical_data: pd.DataFrame,
) -> pd.DataFrame:
    """Join all feature dataframes into final ML dataset dataframe.
    Args:
        target_data (pd.DataFrame): Target dataframe with callbacks.
        salary_data (pd.DataFrame): Salary feature dataframe.
        publication_activity_data (pd.DataFrame):
            Publication activity dataframe.
        text_data (pd.DataFrame): Text feature dataframe.
        time_data (pd.DataFrame): Time feature dataframe.
        categorical_data (pd.DataFrame): Categorical feature dataframe.
    """
    if target_data.empty:
        return pd.DataFrame()

    dataset = target_data.copy()

    feature_dataframes = [
        salary_data,
        publication_activity_data,
        text_data,
        time_data,
        categorical_data,
    ]

    for feature_dataframe in feature_dataframes:
        if feature_dataframe.empty:
            return pd.DataFrame()

        dataset = dataset.merge(
            feature_dataframe,
            on=JOIN_KEYS,
            how='inner',
        )

    return dataset


def build_ml_feature_rows(
    dataset: pd.DataFrame,
    ml_dataset_run_id: int,
) -> list[dict[str, int | float | bool | str | datetime]]:
    """Build ML feature rows for persistence.
    Args:
        dataset (pd.DataFrame): Joined ML dataset dataframe.
        ml_dataset_run_id (int): ML dataset run identifier.
    """
    if dataset.empty:
        return []

    rows = []

    for _, row in dataset.iterrows():
        rows.append(
            {
                'ml_dataset_run_id': ml_dataset_run_id,
                'client_id': int(row['client_id']),
                'company_id': int(row['company_id']),
                'vacancy_id': int(row['vacancy_id']),
                'date_day': row['date_day'],
                'callbacks': int(row['callbacks']),
                'salary_mid': float(row['salary_mid']),
                'salary_is_specified': bool(row['salary_is_specified']),
                'salary_ratio_to_market_by_city': float(
                    row['salary_ratio_to_market_by_city'],
                ),
                'salary_ratio_to_market_by_profile': float(
                    row['salary_ratio_to_market_by_profile'],
                ),
                'salary_ratio_to_market_by_city_profile': float(
                    row['salary_ratio_to_market_by_city_profile'],
                ),
                'publication_activity_level': int(
                    row['publication_activity_level'],
                ),
                'days_since_last_publication_activity': int(
                    row['days_since_last_publication_activity'],
                ),
                'title_length': int(row['title_length']),
                'description_length': int(row['description_length']),
                'title_word_count': int(row['title_word_count']),
                'description_word_count': int(
                    row['description_word_count'],
                ),
                'has_description': bool(row['has_description']),
                'description_is_empty': bool(row['description_is_empty']),
                'has_salary_mention': bool(row['has_salary_mention']),
                'has_schedule_mention': bool(row['has_schedule_mention']),
                'has_requirements_mention': bool(
                    row['has_requirements_mention'],
                ),
                'has_benefits_mention': bool(
                    row['has_benefits_mention'],
                ),
                'has_call_to_action': bool(row['has_call_to_action']),
                'publication_hour': int(row['publication_hour']),
                'publication_day_of_week': int(
                    row['publication_day_of_week'],
                ),
                'publication_month': int(row['publication_month']),
                'publication_week': int(row['publication_week']),
                'is_weekend': bool(row['is_weekend']),
                'vacancy_age_days': int(row['vacancy_age_days']),
                'city': str(row['city']),
                'region': str(row['region']),
                'profile': str(row['profile']),
                'employment_type': str(row['employment_type']),
                'work_experience': str(row['work_experience']),
                'work_schedule': str(row['work_schedule']),
            },
        )

    return rows
