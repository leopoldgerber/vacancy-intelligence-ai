from datetime import datetime

import pandas as pd

from app.services.features.categorical_feature_builders import (
    UNKNOWN_CATEGORY_VALUE,
)
from app.services.features.categorical_feature_builders import (
    build_categorical_feature_dataframe,
)
from app.services.features.categorical_feature_builders import (
    build_categorical_feature_rows,
)
from app.services.features.categorical_feature_builders import (
    normalize_category_value,
)


def build_categorical_feature_test_dataframe() -> pd.DataFrame:
    """Build categorical feature test dataframe.
    Args:
        """
    return pd.DataFrame(
        {
            'client_id': [1, 1, 1],
            'company_id': [10, 10, 20],
            'vacancy_id': [100, 101, 200],
            'date_day': pd.to_datetime(
                [
                    '2025-08-01',
                    '2025-08-02',
                    '2025-08-03',
                ],
            ),
            'city': [
                ' Berlin ',
                '',
                None,
            ],
            'region': [
                'Berlin',
                '   ',
                None,
            ],
            'profile': [
                'Filialleiter',
                '',
                None,
            ],
            'employment_type': [
                'Full-time',
                '',
                None,
            ],
            'work_experience': [
                '1 year',
                '   ',
                None,
            ],
            'work_schedule': [
                'Full-time',
                '',
                None,
            ],
        },
    )


def test_normalize_category_value() -> None:
    """Test category normalization with regular value.
    Args:
        """
    result = normalize_category_value(value=' Berlin ')

    assert result == 'Berlin'


def test_normalize_category_value_none() -> None:
    """Test category normalization with None.
    Args:
        """
    result = normalize_category_value(value=None)

    assert result == UNKNOWN_CATEGORY_VALUE


def test_normalize_category_value_empty_string() -> None:
    """Test category normalization with empty string.
    Args:
        """
    result = normalize_category_value(value='')

    assert result == UNKNOWN_CATEGORY_VALUE


def test_normalize_category_value_whitespace() -> None:
    """Test category normalization with whitespace-only string.
    Args:
        """
    result = normalize_category_value(value='   ')

    assert result == UNKNOWN_CATEGORY_VALUE


def test_build_categorical_feature_dataframe() -> None:
    """Test categorical feature dataframe builder.
    Args:
        """
    data = build_categorical_feature_test_dataframe()

    result = build_categorical_feature_dataframe(data=data)

    assert len(result) == 3

    first_row = result.iloc[0]
    second_row = result.iloc[1]
    third_row = result.iloc[2]

    assert first_row['city'] == 'Berlin'
    assert first_row['region'] == 'Berlin'
    assert first_row['profile'] == 'Filialleiter'
    assert first_row['employment_type'] == 'Full-time'
    assert first_row['work_experience'] == '1 year'
    assert first_row['work_schedule'] == 'Full-time'

    assert second_row['city'] == UNKNOWN_CATEGORY_VALUE
    assert second_row['region'] == UNKNOWN_CATEGORY_VALUE
    assert second_row['profile'] == UNKNOWN_CATEGORY_VALUE
    assert second_row['employment_type'] == UNKNOWN_CATEGORY_VALUE
    assert second_row['work_experience'] == UNKNOWN_CATEGORY_VALUE
    assert second_row['work_schedule'] == UNKNOWN_CATEGORY_VALUE

    assert third_row['city'] == UNKNOWN_CATEGORY_VALUE
    assert third_row['region'] == UNKNOWN_CATEGORY_VALUE
    assert third_row['profile'] == UNKNOWN_CATEGORY_VALUE
    assert third_row['employment_type'] == UNKNOWN_CATEGORY_VALUE
    assert third_row['work_experience'] == UNKNOWN_CATEGORY_VALUE
    assert third_row['work_schedule'] == UNKNOWN_CATEGORY_VALUE


def test_build_categorical_feature_dataframe_empty_data() -> None:
    """Test categorical feature dataframe builder with empty data.
    Args:
        """
    data = pd.DataFrame()

    result = build_categorical_feature_dataframe(data=data)

    assert result.empty


def test_build_categorical_feature_rows() -> None:
    """Test categorical feature rows builder.
    Args:
        """
    data = build_categorical_feature_test_dataframe()

    result = build_categorical_feature_rows(
        data=data,
        feature_run_id=1,
    )

    assert len(result) == 3

    first_row = result[0]
    second_row = result[1]
    third_row = result[2]

    assert first_row['feature_run_id'] == 1
    assert first_row['client_id'] == 1
    assert first_row['company_id'] == 10
    assert first_row['vacancy_id'] == 100
    assert isinstance(first_row['date_day'], pd.Timestamp | datetime)
    assert first_row['city'] == 'Berlin'
    assert first_row['region'] == 'Berlin'
    assert first_row['profile'] == 'Filialleiter'
    assert first_row['employment_type'] == 'Full-time'
    assert first_row['work_experience'] == '1 year'
    assert first_row['work_schedule'] == 'Full-time'

    assert second_row['city'] == UNKNOWN_CATEGORY_VALUE
    assert second_row['region'] == UNKNOWN_CATEGORY_VALUE
    assert second_row['profile'] == UNKNOWN_CATEGORY_VALUE
    assert second_row['employment_type'] == UNKNOWN_CATEGORY_VALUE
    assert second_row['work_experience'] == UNKNOWN_CATEGORY_VALUE
    assert second_row['work_schedule'] == UNKNOWN_CATEGORY_VALUE

    assert third_row['city'] == UNKNOWN_CATEGORY_VALUE
    assert third_row['region'] == UNKNOWN_CATEGORY_VALUE
    assert third_row['profile'] == UNKNOWN_CATEGORY_VALUE
    assert third_row['employment_type'] == UNKNOWN_CATEGORY_VALUE
    assert third_row['work_experience'] == UNKNOWN_CATEGORY_VALUE
    assert third_row['work_schedule'] == UNKNOWN_CATEGORY_VALUE


def test_build_categorical_feature_rows_empty_data() -> None:
    """Test categorical feature rows builder with empty data.
    Args:
        """
    data = pd.DataFrame()

    result = build_categorical_feature_rows(
        data=data,
        feature_run_id=1,
    )

    assert result == []
