from datetime import datetime

import pandas as pd

from app.services.ml_dataset.dataset_builders import build_ml_feature_rows
from app.services.ml_dataset.dataset_builders import join_feature_dataframes


def build_target_dataframe() -> pd.DataFrame:
    """Build target dataframe.
    Args:
        """
    return pd.DataFrame(
        {
            'client_id': [1],
            'company_id': [10],
            'vacancy_id': [100],
            'date_day': pd.to_datetime(['2025-08-01']),
            'callbacks': [12],
        },
    )


def build_salary_dataframe() -> pd.DataFrame:
    """Build salary feature dataframe.
    Args:
        """
    return pd.DataFrame(
        {
            'client_id': [1],
            'company_id': [10],
            'vacancy_id': [100],
            'date_day': pd.to_datetime(['2025-08-01']),
            'salary_mid': [1500.0],
            'salary_is_specified': [True],
            'salary_ratio_to_market_by_city': [0.8],
            'salary_ratio_to_market_by_profile': [0.9],
            'salary_ratio_to_market_by_city_profile': [0.85],
        },
    )


def build_publication_activity_dataframe() -> pd.DataFrame:
    """Build publication activity feature dataframe.
    Args:
        """
    return pd.DataFrame(
        {
            'client_id': [1],
            'company_id': [10],
            'vacancy_id': [100],
            'date_day': pd.to_datetime(['2025-08-01']),
            'publication_activity_level': [2],
            'days_since_last_publication_activity': [0],
        },
    )


def build_text_dataframe() -> pd.DataFrame:
    """Build text feature dataframe.
    Args:
        """
    return pd.DataFrame(
        {
            'client_id': [1],
            'company_id': [10],
            'vacancy_id': [100],
            'date_day': pd.to_datetime(['2025-08-01']),
            'title_length': [20],
            'description_length': [120],
            'title_word_count': [2],
            'description_word_count': [18],
            'has_description': [True],
            'description_is_empty': [False],
            'has_salary_mention': [True],
            'has_schedule_mention': [True],
            'has_requirements_mention': [True],
            'has_benefits_mention': [True],
            'has_call_to_action': [True],
        },
    )


def build_time_dataframe() -> pd.DataFrame:
    """Build time feature dataframe.
    Args:
        """
    return pd.DataFrame(
        {
            'client_id': [1],
            'company_id': [10],
            'vacancy_id': [100],
            'date_day': pd.to_datetime(['2025-08-01']),
            'publication_hour': [10],
            'publication_day_of_week': [4],
            'publication_month': [8],
            'publication_week': [31],
            'is_weekend': [False],
            'vacancy_age_days': [3],
        },
    )


def build_categorical_dataframe() -> pd.DataFrame:
    """Build categorical feature dataframe.
    Args:
        """
    return pd.DataFrame(
        {
            'client_id': [1],
            'company_id': [10],
            'vacancy_id': [100],
            'date_day': pd.to_datetime(['2025-08-01']),
            'city': ['Berlin'],
            'region': ['Berlin'],
            'profile': ['Filialleiter'],
            'employment_type': ['Full-time'],
            'work_experience': ['1 year'],
            'work_schedule': ['Full-time'],
        },
    )


def test_join_feature_dataframes() -> None:
    """Test joining all feature dataframes.
    Args:
        """
    result = join_feature_dataframes(
        target_data=build_target_dataframe(),
        salary_data=build_salary_dataframe(),
        publication_activity_data=build_publication_activity_dataframe(),
        text_data=build_text_dataframe(),
        time_data=build_time_dataframe(),
        categorical_data=build_categorical_dataframe(),
    )

    assert len(result) == 1

    row = result.iloc[0]

    assert row['client_id'] == 1
    assert row['company_id'] == 10
    assert row['vacancy_id'] == 100
    assert row['callbacks'] == 12
    assert row['salary_mid'] == 1500.0
    assert row['publication_activity_level'] == 2
    assert row['title_length'] == 20
    assert row['publication_hour'] == 10
    assert row['city'] == 'Berlin'


def test_join_feature_dataframes_empty_target() -> None:
    """Test joining with empty target dataframe.
    Args:
        """
    result = join_feature_dataframes(
        target_data=pd.DataFrame(),
        salary_data=build_salary_dataframe(),
        publication_activity_data=build_publication_activity_dataframe(),
        text_data=build_text_dataframe(),
        time_data=build_time_dataframe(),
        categorical_data=build_categorical_dataframe(),
    )

    assert result.empty


def test_join_feature_dataframes_missing_feature_data() -> None:
    """Test joining with missing feature dataframe.
    Args:
        """
    result = join_feature_dataframes(
        target_data=build_target_dataframe(),
        salary_data=pd.DataFrame(),
        publication_activity_data=build_publication_activity_dataframe(),
        text_data=build_text_dataframe(),
        time_data=build_time_dataframe(),
        categorical_data=build_categorical_dataframe(),
    )

    assert result.empty


def test_build_ml_feature_rows() -> None:
    """Test ML feature rows builder.
    Args:
        """
    dataset = join_feature_dataframes(
        target_data=build_target_dataframe(),
        salary_data=build_salary_dataframe(),
        publication_activity_data=build_publication_activity_dataframe(),
        text_data=build_text_dataframe(),
        time_data=build_time_dataframe(),
        categorical_data=build_categorical_dataframe(),
    )

    result = build_ml_feature_rows(
        dataset=dataset,
        ml_dataset_run_id=1,
    )

    assert len(result) == 1

    first_row = result[0]

    assert first_row['ml_dataset_run_id'] == 1
    assert first_row['client_id'] == 1
    assert first_row['company_id'] == 10
    assert first_row['vacancy_id'] == 100
    assert isinstance(first_row['date_day'], pd.Timestamp | datetime)
    assert first_row['callbacks'] == 12

    assert first_row['salary_mid'] == 1500.0
    assert first_row['salary_is_specified'] is True
    assert first_row['salary_ratio_to_market_by_city'] == 0.8
    assert first_row['salary_ratio_to_market_by_profile'] == 0.9
    assert first_row['salary_ratio_to_market_by_city_profile'] == 0.85

    assert first_row['publication_activity_level'] == 2
    assert first_row['days_since_last_publication_activity'] == 0

    assert first_row['title_length'] == 20
    assert first_row['description_length'] == 120
    assert first_row['title_word_count'] == 2
    assert first_row['description_word_count'] == 18
    assert first_row['has_description'] is True
    assert first_row['description_is_empty'] is False
    assert first_row['has_salary_mention'] is True
    assert first_row['has_schedule_mention'] is True
    assert first_row['has_requirements_mention'] is True
    assert first_row['has_benefits_mention'] is True
    assert first_row['has_call_to_action'] is True

    assert first_row['publication_hour'] == 10
    assert first_row['publication_day_of_week'] == 4
    assert first_row['publication_month'] == 8
    assert first_row['publication_week'] == 31
    assert first_row['is_weekend'] is False
    assert first_row['vacancy_age_days'] == 3

    assert first_row['city'] == 'Berlin'
    assert first_row['region'] == 'Berlin'
    assert first_row['profile'] == 'Filialleiter'
    assert first_row['employment_type'] == 'Full-time'
    assert first_row['work_experience'] == '1 year'
    assert first_row['work_schedule'] == 'Full-time'


def test_build_ml_feature_rows_empty_dataset() -> None:
    """Test ML feature rows builder with empty dataset.
    Args:
        """
    result = build_ml_feature_rows(
        dataset=pd.DataFrame(),
        ml_dataset_run_id=1,
    )

    assert result == []
