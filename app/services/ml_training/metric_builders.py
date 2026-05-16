import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score


def calculate_mae(
    actual: pd.Series,
    predicted: np.ndarray,
) -> float:
    """Calculate mean absolute error.
    Args:
        actual (pd.Series): Actual target values.
        predicted (np.ndarray): Predicted target values."""
    return float(mean_absolute_error(actual, predicted))


def calculate_rmse(
    actual: pd.Series,
    predicted: np.ndarray,
) -> float:
    """Calculate root mean squared error.
    Args:
        actual (pd.Series): Actual target values.
        predicted (np.ndarray): Predicted target values."""
    mse = mean_squared_error(actual, predicted)

    return float(np.sqrt(mse))


def calculate_r2(
    actual: pd.Series,
    predicted: np.ndarray,
) -> float:
    """Calculate R2 score.
    Args:
        actual (pd.Series): Actual target values.
        predicted (np.ndarray): Predicted target values."""
    return float(r2_score(actual, predicted))


def calculate_baseline_predictions(
    train_target: pd.Series,
    test_row_count: int,
) -> np.ndarray:
    """Calculate baseline predictions from train target mean.
    Args:
        train_target (pd.Series): Train target values.
        test_row_count (int): Number of test rows."""
    baseline_value = float(train_target.mean())

    return np.full(
        shape=test_row_count,
        fill_value=baseline_value,
    )


def calculate_training_metrics(
    train_target: pd.Series,
    test_target: pd.Series,
    predictions: np.ndarray,
) -> dict[str, float]:
    """Calculate training metrics.
    Args:
        train_target (pd.Series): Train target values.
        test_target (pd.Series): Test target values.
        predictions (np.ndarray): Model predictions."""
    baseline_predictions = calculate_baseline_predictions(
        train_target=train_target,
        test_row_count=len(test_target),
    )

    return {
        'metric_mae': calculate_mae(
            actual=test_target,
            predicted=predictions,
        ),
        'metric_rmse': calculate_rmse(
            actual=test_target,
            predicted=predictions,
        ),
        'metric_r2': calculate_r2(
            actual=test_target,
            predicted=predictions,
        ),
        'baseline_mae': calculate_mae(
            actual=test_target,
            predicted=baseline_predictions,
        ),
        'mean_target': float(train_target.mean()),
    }
