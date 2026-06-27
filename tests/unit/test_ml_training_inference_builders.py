from datetime import date

import numpy as np
import pandas as pd
import pytest
from catboost import CatBoostRegressor

from app.services.ml_training.feature_schema import CATEGORICAL_FEATURE_COLUMNS
from app.services.ml_training.feature_schema import NUMERICAL_FEATURE_COLUMNS
from app.services.ml_training.inference_builders import build_inference_dataset
from app.services.ml_training.inference_builders import build_inference_rows
from app.services.ml_training.inference_builders import get_missing_features
from app.services.ml_training.inference_builders import (
    normalize_inference_features)
from app.services.ml_training.inference_builders import (
    predict_inference_dataset)
from app.services.ml_training.inference_builders import validate_inference_data


def build_feature_data() -> pd.DataFrame:
    """Build inference feature dataframe for tests.
    Args:
        """
    rows = []

    for index in range(6):
        row = {
            'client_id': 1,
            'company_id': 10 + index,
            'vacancy_id': 100 + index,
            'date_day': pd.Timestamp('2025-09-01') + pd.Timedelta(days=index),
        }

        for column in NUMERICAL_FEATURE_COLUMNS:
            row[column] = float(index + 1)

        for column in CATEGORICAL_FEATURE_COLUMNS:
            row[column] = f'{column}_{index}'

        rows.append(row)

    return pd.DataFrame(rows)


def build_fitted_model(data: pd.DataFrame) -> CatBoostRegressor:
    """Build fitted CatBoost model for inference tests.
    Args:
        data (pd.DataFrame): Source inference dataframe.
    """
    dataset = build_inference_dataset(data=data)
    target = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    model = CatBoostRegressor(
        iterations=2,
        learning_rate=0.1,
        depth=2,
        loss_function='RMSE',
        verbose=False,
        allow_writing_files=False,
    )
    model.fit(
        dataset.features,
        target,
        cat_features=list(range(
            len(NUMERICAL_FEATURE_COLUMNS),
            len(NUMERICAL_FEATURE_COLUMNS) + len(CATEGORICAL_FEATURE_COLUMNS),
        )),
    )

    return model


def test_get_missing_features() -> None:
    """Test missing inference feature detection.
    Args:
        """
    data = build_feature_data()
    data = data.drop(columns=['salary_mid'])

    result = get_missing_features(columns=list(data.columns))

    assert result == ['salary_mid']


def test_validate_empty_data() -> None:
    """Test empty inference dataframe validation.
    Args:
        """
    data = pd.DataFrame()

    with pytest.raises(ValueError):
        validate_inference_data(data=data)


def test_validate_inference_data() -> None:
    """Test inference dataframe validation.
    Args:
        """
    data = build_feature_data()

    result = validate_inference_data(data=data)

    assert result.equals(data)


def test_normalize_inference_features() -> None:
    """Test inference feature normalization.
    Args:
        """
    data = build_feature_data()
    data['salary_mid'] = data['salary_mid'].astype(object)
    data.loc[0, 'salary_mid'] = 'invalid'
    data.loc[1, 'city'] = '  '
    data.loc[2, 'region'] = None

    result = normalize_inference_features(data=data)

    assert result.loc[0, 'salary_mid'] == 0
    assert result.loc[1, 'city'] == 'unknown'
    assert result.loc[2, 'region'] == 'unknown'


def test_build_inference_dataset() -> None:
    """Test inference dataset building.
    Args:
        """
    data = build_feature_data()

    result = build_inference_dataset(data=data)

    assert result.row_count == 6
    assert result.features.shape == (6, 30)
    assert result.feature_columns == (
        NUMERICAL_FEATURE_COLUMNS + CATEGORICAL_FEATURE_COLUMNS)


def test_predict_inference_dataset() -> None:
    """Test inference dataset prediction.
    Args:
        """
    data = build_feature_data()
    model = build_fitted_model(data=data)
    dataset = build_inference_dataset(data=data)

    result = predict_inference_dataset(
        model=model,
        dataset=dataset,
    )

    assert isinstance(result, np.ndarray)
    assert len(result) == 6


def test_build_inference_rows() -> None:
    """Test inference prediction row building.
    Args:
        """
    data = build_feature_data()
    predictions = np.array([1.5, 2.5, 3.5, 4.5, 5.5, 6.5])

    result = build_inference_rows(
        source_data=data,
        predictions=predictions,
    )

    assert len(result) == 6
    assert result[0] == {
        'source_row_index': 0,
        'predicted_value': 1.5,
        'client_id': 1,
        'company_id': 10,
        'vacancy_id': 100,
        'date_day': date(2025, 9, 1),
    }


def test_build_inference_rows_length_mismatch() -> None:
    """Test inference prediction row length validation.
    Args:
        """
    data = build_feature_data()
    predictions = np.array([1.5, 2.5])

    with pytest.raises(ValueError):
        build_inference_rows(
            source_data=data,
            predictions=predictions,
        )
