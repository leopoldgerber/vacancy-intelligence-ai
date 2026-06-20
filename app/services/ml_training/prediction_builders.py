from datetime import date
from typing import Any

import numpy as np
import pandas as pd

from app.services.ml_training.constants import ML_TARGET_CALLBACKS
from app.services.ml_training.split_builders import TrainingSplit


SPLIT_NAME_TEST = 'test'


def normalize_date_day(value: Any) -> date | None:
    """Normalize date day value.
    Args:
        value (Any): Raw date value.
    """
    if value is None:
        return None

    if pd.isna(value):
        return None

    if isinstance(value, pd.Timestamp):
        return value.date()

    if isinstance(value, date):
        return value

    return pd.to_datetime(value).date()


def build_prediction_rows(
    ml_training_run_id: int,
    source_data: pd.DataFrame,
    split: TrainingSplit,
    predictions: np.ndarray,
) -> list[dict[str, Any]]:
    """Build ML training prediction rows.
    Args:
        ml_training_run_id (int): ML training run identifier.
        source_data (pd.DataFrame): Source training dataframe.
        split (TrainingSplit): Prepared train/test split.
        predictions (np.ndarray): Test predictions.
    """
    test_indices = list(split.test_target.index)
    actual_values = split.test_target.to_numpy()

    prediction_rows = []

    for source_row_index, actual_value, predicted_value in zip(
        test_indices,
        actual_values,
        predictions,
        strict=True,
    ):
        source_row = source_data.loc[source_row_index]
        actual_float = float(actual_value)
        predicted_float = float(predicted_value)
        prediction_error = predicted_float - actual_float

        prediction_rows.append(
            {
                'ml_training_run_id': ml_training_run_id,
                'source_row_index': int(source_row_index),
                'client_id': int(source_row['client_id']),
                'company_id': int(source_row['company_id']),
                'vacancy_id': int(source_row['vacancy_id']),
                'date_day': normalize_date_day(source_row.get('date_day')),
                'split_name': SPLIT_NAME_TEST,
                'target_name': ML_TARGET_CALLBACKS,
                'actual_value': actual_float,
                'predicted_value': predicted_float,
                'prediction_error': prediction_error,
                'absolute_error': abs(prediction_error),
                'squared_error': prediction_error**2,
            },
        )

    return prediction_rows
