from pathlib import Path

import pandas as pd
import pytest
from catboost import CatBoostRegressor

from app.services.ml_training.feature_schema import CATEGORICAL_FEATURE_COLUMNS
from app.services.ml_training.feature_schema import NUMERICAL_FEATURE_COLUMNS
from app.services.ml_training.inference_builders import build_inference_dataset
from app.services.ml_training.inference_service import MlInferenceResult
from app.services.ml_training.inference_service import build_inference_result
from app.services.ml_training.inference_service import run_ml_inference


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
    """Build fitted CatBoost model for inference service tests.
    Args:
        data (pd.DataFrame): Source inference dataframe."""
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


def save_test_model(
    tmp_path: Path,
    data: pd.DataFrame,
) -> Path:
    """Save fitted CatBoost model for inference service tests.
    Args:
        tmp_path (Path): Temporary pytest path.
        data (pd.DataFrame): Source inference dataframe."""
    model = build_fitted_model(data=data)
    model_path = tmp_path / 'model.cbm'
    model.save_model(str(model_path))

    return model_path


def test_build_inference_result(tmp_path: Path) -> None:
    """Test ML inference result building.
    Args:
        tmp_path (Path): Temporary pytest path."""
    model_path = tmp_path / 'model.cbm'
    prediction_rows = [
        {
            'source_row_index': 0,
            'predicted_value': 1.5,
        },
        {
            'source_row_index': 1,
            'predicted_value': 2.5,
        },
    ]

    result = build_inference_result(
        model_path=model_path,
        row_count=2,
        prediction_rows=prediction_rows,
    )

    assert result == MlInferenceResult(
        model_path=str(model_path),
        row_count=2,
        prediction_row_count=2,
        predictions=[1.5, 2.5],
        prediction_rows=prediction_rows,
    )


def test_run_ml_inference(tmp_path: Path) -> None:
    """Test full ML inference flow.
    Args:
        tmp_path (Path): Temporary pytest path."""
    data = build_feature_data()
    model_path = save_test_model(
        tmp_path=tmp_path,
        data=data,
    )

    result = run_ml_inference(
        model_path=model_path,
        data=data,
    )

    assert result.model_path == str(model_path)
    assert result.row_count == 6
    assert result.prediction_row_count == 6
    assert len(result.predictions) == 6
    assert len(result.prediction_rows) == 6
    assert result.prediction_rows[0]['client_id'] == 1
    assert result.prediction_rows[0]['company_id'] == 10
    assert result.prediction_rows[0]['vacancy_id'] == 100


def test_run_ml_inference_empty_data(tmp_path: Path) -> None:
    """Test full ML inference flow with empty data.
    Args:
        tmp_path (Path): Temporary pytest path."""
    data = build_feature_data()
    model_path = save_test_model(
        tmp_path=tmp_path,
        data=data,
    )

    with pytest.raises(ValueError):
        run_ml_inference(
            model_path=model_path,
            data=pd.DataFrame(),
        )
