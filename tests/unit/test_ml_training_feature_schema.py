from app.services.ml_training.feature_schema import (
    CATEGORICAL_FEATURE_COLUMNS,
)
from app.services.ml_training.feature_schema import IDENTIFIER_COLUMNS
from app.services.ml_training.feature_schema import NUMERICAL_FEATURE_COLUMNS
from app.services.ml_training.feature_schema import TARGET_COLUMN
from app.services.ml_training.feature_schema import (
    get_categorical_feature_indices)
from app.services.ml_training.feature_schema import get_feature_columns
from app.services.ml_training.feature_schema import get_missing_columns
from app.services.ml_training.feature_schema import get_training_columns


def test_get_feature_columns() -> None:
    """Test model feature columns.
    Args:
        """
    result = get_feature_columns()

    assert result == NUMERICAL_FEATURE_COLUMNS + CATEGORICAL_FEATURE_COLUMNS
    assert TARGET_COLUMN not in result
    assert 'client_id' not in result
    assert 'company_id' not in result
    assert 'vacancy_id' not in result
    assert 'date_day' not in result


def test_get_training_columns() -> None:
    """Test training columns.
    Args:
        """
    result = get_training_columns()

    assert result == (
        IDENTIFIER_COLUMNS
        + NUMERICAL_FEATURE_COLUMNS
        + CATEGORICAL_FEATURE_COLUMNS
        + [TARGET_COLUMN]
    )
    assert result.count(TARGET_COLUMN) == 1


def test_get_missing_columns() -> None:
    """Test missing training column detection.
    Args:
        """
    columns = get_training_columns()
    columns.remove('salary_mid')
    columns.remove('city')

    result = get_missing_columns(columns=columns)

    assert result == ['salary_mid', 'city']


def test_get_missing_columns_empty_result() -> None:
    """Test missing training column detection without missing columns.
    Args:
        """
    result = get_missing_columns(columns=get_training_columns())

    assert result == []


def test_get_categorical_feature_indices() -> None:
    """Test categorical feature indices.
    Args:
        """
    feature_columns = get_feature_columns()

    result = get_categorical_feature_indices()

    assert result == [
        feature_columns.index(column)
        for column in CATEGORICAL_FEATURE_COLUMNS
    ]
    assert len(result) == len(CATEGORICAL_FEATURE_COLUMNS)
