import pandas as pd
import pytest

from app.services.ml_training.constants import MIN_TRAINING_ROW_COUNT
from app.services.ml_training.dataset_builders import build_dataset
from app.services.ml_training.dataset_builders import normalize_features
from app.services.ml_training.dataset_builders import validate_columns
from app.services.ml_training.dataset_builders import validate_rows
from app.services.ml_training.dataset_builders import validate_target
from app.services.ml_training.feature_schema import CATEGORICAL_FEATURE_COLUMNS
from app.services.ml_training.feature_schema import NUMERICAL_FEATURE_COLUMNS
from app.services.ml_training.feature_schema import TARGET_COLUMN
from app.services.ml_training.feature_schema import get_feature_columns
from app.services.ml_training.feature_schema import get_training_columns


def build_training_dataframe(row_count: int = 12) -> pd.DataFrame:
    """Build training dataframe for tests.
    Args:
        row_count (int): Number of rows."""
    rows = []

    for index in range(row_count):
        row = {
            'client_id': 1,
            'company_id': index % 3 + 1,
            'vacancy_id': 1000 + index,
            'date_day': pd.Timestamp('2025-08-01'),
            'callbacks': index + 1,
            'salary_mid': 1000 + index,
            'salary_is_specified': True,
            'salary_ratio_to_market_by_city': 1.0,
            'salary_ratio_to_market_by_profile': 0.95,
            'salary_ratio_to_market_by_city_profile': 1.05,
            'publication_activity_level': index % 4,
            'days_since_last_publication_activity': index % 5,
            'title_length': 20 + index,
            'description_length': 100 + index,
            'title_word_count': 2,
            'description_word_count': 15,
            'has_description': True,
            'description_is_empty': False,
            'has_salary_mention': index % 2 == 0,
            'has_schedule_mention': True,
            'has_requirements_mention': True,
            'has_benefits_mention': index % 2 == 1,
            'has_call_to_action': True,
            'publication_hour': 9,
            'publication_day_of_week': 1,
            'publication_month': 8,
            'publication_week': 31,
            'is_weekend': False,
            'vacancy_age_days': index,
            'city': 'Berlin',
            'region': 'Berlin',
            'profile': 'Filialleiter',
            'employment_type': 'Full-time',
            'work_experience': '1 year',
            'work_schedule': 'Full-time',
        }
        rows.append(row)

    return pd.DataFrame(
        rows,
        columns=get_training_columns(),
    )


def test_validate_columns_success() -> None:
    """Test required columns validation success.
    Args:
        """
    data = build_training_dataframe()

    validate_columns(data=data)


def test_validate_columns_error() -> None:
    """Test required columns validation error.
    Args:
        """
    data = build_training_dataframe()
    data = data.drop(columns=['salary_mid'])

    with pytest.raises(
        ValueError,
        match='Missing required ML training columns'
    ):
        validate_columns(data=data)


def test_validate_rows_success() -> None:
    """Test row count validation success.
    Args:
        """
    data = build_training_dataframe(row_count=MIN_TRAINING_ROW_COUNT)

    validate_rows(data=data)


def test_validate_rows_empty_error() -> None:
    """Test empty row count validation error.
    Args:
        """
    data = build_training_dataframe(row_count=0)

    with pytest.raises(ValueError, match='ML training dataframe is empty'):
        validate_rows(data=data)


def test_validate_rows_insufficient_error() -> None:
    """Test insufficient row count validation error.
    Args:
        """
    data = build_training_dataframe(row_count=MIN_TRAINING_ROW_COUNT - 1)

    with pytest.raises(ValueError, match='insufficient rows'):
        validate_rows(data=data)


def test_validate_target_success() -> None:
    """Test target validation success.
    Args:
        """
    data = build_training_dataframe()

    validate_target(data=data)


def test_validate_target_missing_error() -> None:
    """Test target validation with missing values.
    Args:
        """
    data = build_training_dataframe()
    data.loc[0, TARGET_COLUMN] = None

    with pytest.raises(ValueError, match='target contains missing values'):
        validate_target(data=data)


def test_normalize_features() -> None:
    """Test feature normalization.
    Args:
        """
    data = build_training_dataframe()
    data.loc[0, 'salary_mid'] = None
    data.loc[0, 'city'] = None
    data.loc[1, 'profile'] = '   '
    data.loc[2, 'employment_type'] = ''

    result = normalize_features(data=data)

    assert result.loc[0, 'salary_mid'] == 0
    assert result.loc[0, 'city'] == 'unknown'
    assert result.loc[1, 'profile'] == 'unknown'
    assert result.loc[2, 'employment_type'] == 'unknown'


def test_build_dataset() -> None:
    """Test prepared training dataset builder.
    Args:
        """
    data = build_training_dataframe()

    result = build_dataset(data=data)

    assert result.row_count == len(data)
    assert list(result.features.columns) == get_feature_columns()
    assert len(result.features) == len(data)
    assert len(result.target) == len(data)
    assert result.feature_columns == get_feature_columns()
    assert result.categorical_feature_columns == CATEGORICAL_FEATURE_COLUMNS
    assert len(result.categorical_feature_indices) == len(
        CATEGORICAL_FEATURE_COLUMNS,
    )
    assert TARGET_COLUMN not in result.features.columns

    for column in NUMERICAL_FEATURE_COLUMNS:
        assert column in result.features.columns

    for column in CATEGORICAL_FEATURE_COLUMNS:
        assert column in result.features.columns


def test_build_dataset_invalid_target_error() -> None:
    """Test prepared training dataset builder with invalid target.
    Args:
        """
    data = build_training_dataframe()
    data[TARGET_COLUMN] = data[TARGET_COLUMN].astype(object)
    data.loc[0, TARGET_COLUMN] = 'invalid'

    with pytest.raises(ValueError, match='invalid numeric values'):
        build_dataset(data=data)
