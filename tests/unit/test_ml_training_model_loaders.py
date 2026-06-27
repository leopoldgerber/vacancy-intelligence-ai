from pathlib import Path

import pandas as pd
import pytest
from catboost import CatBoostRegressor

from app.services.ml_training.model_loaders import load_catboost_model
from app.services.ml_training.model_loaders import validate_model_path


def build_test_model() -> CatBoostRegressor:
    """Build fitted CatBoost model for loader tests.
    Args:
        """
    train_features = pd.DataFrame(
        {
            'salary_mid': [1000, 1200, 1400, 1600, 1800, 2000],
            'publication_hour': [8, 9, 10, 11, 12, 13],
        },
    )
    train_target = [5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    model = CatBoostRegressor(
        iterations=2,
        learning_rate=0.1,
        depth=2,
        loss_function='RMSE',
        verbose=False,
        allow_writing_files=False,
    )
    model.fit(train_features, train_target)

    return model


def test_validate_model_path(tmp_path: Path) -> None:
    """Test CatBoost model path validation.
    Args:
        tmp_path (Path): Temporary pytest path."""
    model_path = tmp_path / 'model.cbm'
    model_path.write_text('model artifact placeholder')

    validated_path = validate_model_path(model_path=model_path)

    assert validated_path == model_path


def test_validate_missing_path(tmp_path: Path) -> None:
    """Test missing CatBoost model path validation.
    Args:
        tmp_path (Path): Temporary pytest path."""
    model_path = tmp_path / 'missing.cbm'

    with pytest.raises(FileNotFoundError):
        validate_model_path(model_path=model_path)


def test_validate_invalid_extension(tmp_path: Path) -> None:
    """Test invalid CatBoost model extension validation.
    Args:
        tmp_path (Path): Temporary pytest path."""
    model_path = tmp_path / 'model.txt'
    model_path.write_text('model artifact placeholder')

    with pytest.raises(ValueError):
        validate_model_path(model_path=model_path)


def test_load_catboost_model(tmp_path: Path) -> None:
    """Test CatBoost model artifact loading.
    Args:
        tmp_path (Path): Temporary pytest path."""
    source_model = build_test_model()
    model_path = tmp_path / 'model.cbm'
    source_model.save_model(str(model_path))

    loaded_model = load_catboost_model(model_path=model_path)

    assert isinstance(loaded_model, CatBoostRegressor)
    assert loaded_model.is_fitted()
