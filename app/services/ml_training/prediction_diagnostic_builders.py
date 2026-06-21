from typing import Any

import numpy as np
import pandas as pd


DIAGNOSTIC_GROUP_COLUMNS = [
    'profile',
    'city',
    'company_id',
]

TOP_WORST_PREDICTION_COUNT = 10


def normalize_json_value(value: Any) -> Any:
    """Normalize value for JSON serialization.
    Args:
        value (Any): Raw value.
    """
    if value is None:
        return None

    if pd.isna(value):
        return None

    if isinstance(value, np.integer):
        return int(value)

    if isinstance(value, np.floating):
        return float(value)

    if isinstance(value, pd.Timestamp):
        return value.isoformat()

    if hasattr(value, 'isoformat'):
        return value.isoformat()

    return value


def enrich_prediction_data(
    prediction_rows: list[dict[str, Any]],
    source_data: pd.DataFrame,
) -> pd.DataFrame:
    """Enrich prediction rows with source data.
    Args:
        prediction_rows (list[dict[str, Any]]): Prediction rows.
        source_data (pd.DataFrame): Source training dataframe.
    """
    prediction_data = pd.DataFrame(prediction_rows)

    if prediction_data.empty:
        return prediction_data

    source_columns = [
        column
        for column in DIAGNOSTIC_GROUP_COLUMNS
        if column in source_data.columns
    ]

    if not source_columns:
        return prediction_data

    source_metadata = source_data[source_columns].copy()
    source_metadata['source_row_index'] = source_metadata.index

    return prediction_data.merge(
        source_metadata,
        how='left',
        on='source_row_index',
        suffixes=('', '_source'),
    )


def build_group_errors(
    prediction_data: pd.DataFrame,
    group_column: str,
) -> dict[str, float]:
    """Build mean absolute error by group.
    Args:
        prediction_data (pd.DataFrame): Enriched prediction data.
        group_column (str): Group column name.
    """
    if prediction_data.empty:
        return {}

    if group_column not in prediction_data.columns:
        return {}

    grouped_errors = (
        prediction_data
        .dropna(subset=[group_column])
        .groupby(group_column)['absolute_error']
        .mean()
        .sort_values(ascending=False)
    )

    return {
        str(group_name): float(error_value)
        for group_name, error_value in grouped_errors.items()
    }


def build_worst_predictions(
    prediction_data: pd.DataFrame,
    top_row_count: int = TOP_WORST_PREDICTION_COUNT,
) -> list[dict[str, Any]]:
    """Build worst prediction rows by absolute error.
    Args:
        prediction_data (pd.DataFrame): Enriched prediction data.
        top_row_count (int): Number of worst rows.
    """
    if prediction_data.empty:
        return []

    available_columns = [
        column
        for column in [
            'source_row_index',
            'client_id',
            'company_id',
            'vacancy_id',
            'date_day',
            'profile',
            'city',
            'actual_value',
            'predicted_value',
            'prediction_error',
            'absolute_error',
            'squared_error',
        ]
        if column in prediction_data.columns
    ]

    worst_rows = (
        prediction_data
        .sort_values('absolute_error', ascending=False)
        .head(top_row_count)
    )

    result = []

    for row in worst_rows[available_columns].to_dict(orient='records'):
        result.append(
            {
                key: normalize_json_value(value)
                for key, value in row.items()
            },
        )

    return result


def build_prediction_diagnostics(
    prediction_rows: list[dict[str, Any]],
    source_data: pd.DataFrame,
) -> dict[str, Any]:
    """Build prediction diagnostics.
    Args:
        prediction_rows (list[dict[str, Any]]): Prediction rows.
        source_data (pd.DataFrame): Source training dataframe.
    """
    prediction_data = enrich_prediction_data(
        prediction_rows=prediction_rows,
        source_data=source_data,
    )

    if prediction_data.empty:
        return {
            'prediction_row_count': 0,
            'mean_prediction_error': None,
            'mean_absolute_error': None,
            'max_absolute_error': None,
            'mean_squared_error': None,
            'root_mean_squared_error': None,
            'over_prediction_count': 0,
            'under_prediction_count': 0,
            'mean_absolute_error_by_profile': {},
            'mean_absolute_error_by_city': {},
            'mean_absolute_error_by_company_id': {},
            'top_worst_predictions': [],
        }

    mean_squared_error = float(prediction_data['squared_error'].mean())

    return {
        'prediction_row_count': int(len(prediction_data)),
        'mean_prediction_error': float(
            prediction_data['prediction_error'].mean(),
        ),
        'mean_absolute_error': float(
            prediction_data['absolute_error'].mean(),
        ),
        'max_absolute_error': float(
            prediction_data['absolute_error'].max(),
        ),
        'mean_squared_error': mean_squared_error,
        'root_mean_squared_error': float(np.sqrt(mean_squared_error)),
        'over_prediction_count': int(
            (prediction_data['prediction_error'] > 0).sum(),
        ),
        'under_prediction_count': int(
            (prediction_data['prediction_error'] < 0).sum(),
        ),
        'mean_absolute_error_by_profile': build_group_errors(
            prediction_data=prediction_data,
            group_column='profile',
        ),
        'mean_absolute_error_by_city': build_group_errors(
            prediction_data=prediction_data,
            group_column='city',
        ),
        'mean_absolute_error_by_company_id': build_group_errors(
            prediction_data=prediction_data,
            group_column='company_id',
        ),
        'top_worst_predictions': build_worst_predictions(
            prediction_data=prediction_data,
        ),
    }
