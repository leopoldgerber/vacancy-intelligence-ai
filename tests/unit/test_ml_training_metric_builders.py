import numpy as np
import pandas as pd
import pytest

from app.services.ml_training.metric_builders import (
    calculate_baseline_predictions)
from app.services.ml_training.metric_builders import calculate_mae
from app.services.ml_training.metric_builders import calculate_r2
from app.services.ml_training.metric_builders import calculate_rmse
from app.services.ml_training.metric_builders import calculate_training_metrics


def test_calculate_mae() -> None:
    """Test MAE calculation.
    Args:
        """
    actual = pd.Series([10, 20, 30])
    predicted = np.array([12, 18, 33])

    result = calculate_mae(
        actual=actual,
        predicted=predicted,
    )

    assert result == pytest.approx(7 / 3)


def test_calculate_rmse() -> None:
    """Test RMSE calculation.
    Args:
        """
    actual = pd.Series([10, 20, 30])
    predicted = np.array([12, 18, 33])

    result = calculate_rmse(
        actual=actual,
        predicted=predicted,
    )

    expected = np.sqrt((4 + 4 + 9) / 3)

    assert result == pytest.approx(expected)


def test_calculate_r2() -> None:
    """Test R2 calculation.
    Args:
        """
    actual = pd.Series([10, 20, 30])
    predicted = np.array([10, 20, 30])

    result = calculate_r2(
        actual=actual,
        predicted=predicted,
    )

    assert result == pytest.approx(1.0)


def test_calculate_baseline_predictions() -> None:
    """Test baseline predictions calculation.
    Args:
        """
    train_target = pd.Series([10, 20, 30])

    result = calculate_baseline_predictions(
        train_target=train_target,
        test_row_count=4,
    )

    assert result.tolist() == [20.0, 20.0, 20.0, 20.0]


def test_calculate_training_metrics() -> None:
    """Test training metric calculation.
    Args:
        """
    train_target = pd.Series([10, 20, 30])
    test_target = pd.Series([12, 22, 32])
    predictions = np.array([11, 24, 30])

    result = calculate_training_metrics(
        train_target=train_target,
        test_target=test_target,
        predictions=predictions,
    )

    assert result['metric_mae'] == pytest.approx((1 + 2 + 2) / 3)
    assert result['metric_rmse'] == pytest.approx(np.sqrt((1 + 4 + 4) / 3))
    assert isinstance(result['metric_r2'], float)
    assert result['baseline_mae'] == pytest.approx((8 + 2 + 12) / 3)
    assert result['mean_target'] == pytest.approx(20.0)
