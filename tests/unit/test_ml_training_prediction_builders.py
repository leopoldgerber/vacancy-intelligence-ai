from datetime import date
from types import SimpleNamespace

import numpy as np
import pandas as pd

from app.services.ml_training.constants import ML_TARGET_CALLBACKS
from app.services.ml_training.prediction_builders import SPLIT_NAME_TEST
from app.services.ml_training.prediction_builders import build_prediction_rows
from app.services.ml_training.prediction_builders import normalize_date_day


def build_source_data() -> pd.DataFrame:
    """Build source data for prediction row tests.
    Args:
        """
    return pd.DataFrame(
        [
            {
                'client_id': 1,
                'company_id': 57,
                'vacancy_id': 17,
                'date_day': pd.Timestamp('2025-08-20'),
            },
            {
                'client_id': 1,
                'company_id': 58,
                'vacancy_id': 18,
                'date_day': pd.Timestamp('2025-09-03'),
            },
            {
                'client_id': 1,
                'company_id': 59,
                'vacancy_id': 19,
                'date_day': pd.Timestamp('2025-09-10'),
            },
        ],
    )


def build_test_split() -> SimpleNamespace:
    """Build test split for prediction row tests.
    Args:
        """
    return SimpleNamespace(
        test_target=pd.Series(
            [3.0, 7.0],
            index=[0, 2],
        ),
    )


def test_normalize_date_day_timestamp() -> None:
    """Test date day normalization for pandas timestamp.
    Args:
        """
    result = normalize_date_day(pd.Timestamp('2025-08-20'))

    assert result == date(2025, 8, 20)


def test_normalize_date_day_date() -> None:
    """Test date day normalization for date.
    Args:
        """
    raw_date = date(2025, 9, 3)

    result = normalize_date_day(raw_date)

    assert result == raw_date


def test_normalize_date_day_none() -> None:
    """Test date day normalization for none.
    Args:
        """
    result = normalize_date_day(None)

    assert result is None


def test_build_prediction_rows() -> None:
    """Test prediction rows builder.
    Args:
        """
    source_data = build_source_data()
    split = build_test_split()
    predictions = np.array([4.5, 5.0])

    result = build_prediction_rows(
        ml_training_run_id=6,
        source_data=source_data,
        split=split,
        predictions=predictions,
    )

    assert len(result) == 2

    first_row = result[0]

    assert first_row == {
        'ml_training_run_id': 6,
        'source_row_index': 0,
        'client_id': 1,
        'company_id': 57,
        'vacancy_id': 17,
        'date_day': date(2025, 8, 20),
        'split_name': SPLIT_NAME_TEST,
        'target_name': ML_TARGET_CALLBACKS,
        'actual_value': 3.0,
        'predicted_value': 4.5,
        'prediction_error': 1.5,
        'absolute_error': 1.5,
        'squared_error': 2.25,
    }

    second_row = result[1]

    assert second_row == {
        'ml_training_run_id': 6,
        'source_row_index': 2,
        'client_id': 1,
        'company_id': 59,
        'vacancy_id': 19,
        'date_day': date(2025, 9, 10),
        'split_name': SPLIT_NAME_TEST,
        'target_name': ML_TARGET_CALLBACKS,
        'actual_value': 7.0,
        'predicted_value': 5.0,
        'prediction_error': -2.0,
        'absolute_error': 2.0,
        'squared_error': 4.0,
    }
