from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from catboost import CatBoostRegressor

from app.services.ml_training.feature_schema import CATEGORICAL_FEATURE_COLUMNS
from app.services.ml_training.feature_schema import IDENTIFIER_COLUMNS
from app.services.ml_training.feature_schema import NUMERICAL_FEATURE_COLUMNS
from app.services.ml_training.feature_schema import get_feature_columns
from app.services.ml_training.prediction_builders import normalize_date_day


@dataclass
class InferenceDataset:
    """Prepared inference dataset."""

    source_data: pd.DataFrame
    features: pd.DataFrame
    feature_columns: list[str]
    row_count: int


def get_missing_features(columns: list[str]) -> list[str]:
    """Get missing inference feature columns.
    Args:
        columns (list[str]): Existing dataframe columns.
    """
    feature_columns = get_feature_columns()

    return [
        column
        for column in feature_columns
        if column not in columns
    ]


def validate_inference_data(data: pd.DataFrame) -> pd.DataFrame:
    """Validate inference dataframe.
    Args:
        data (pd.DataFrame): Source inference dataframe.
    """
    if data.empty:
        raise ValueError('ML inference dataframe is empty.')

    missing_features = get_missing_features(columns=list(data.columns))

    if missing_features:
        raise ValueError(
            f'Missing required ML inference features: {missing_features}',
        )

    return data


def normalize_inference_features(data: pd.DataFrame) -> pd.DataFrame:
    """Normalize feature values for inference.
    Args:
        data (pd.DataFrame): Source inference dataframe.
    """
    normalized_data = data.copy()

    for column in NUMERICAL_FEATURE_COLUMNS:
        normalized_data[column] = pd.to_numeric(
            normalized_data[column],
            errors='coerce',
        ).fillna(0)

    for column in CATEGORICAL_FEATURE_COLUMNS:
        normalized_data[column] = (
            normalized_data[column]
            .fillna('unknown')
            .astype(str)
            .str.strip()
            .replace('', 'unknown')
        )

    return normalized_data


def build_inference_dataset(data: pd.DataFrame) -> InferenceDataset:
    """Build prepared inference dataset.
    Args:
        data (pd.DataFrame): Source inference dataframe.
    """
    validated_data = validate_inference_data(data=data)
    normalized_data = normalize_inference_features(data=validated_data)
    feature_columns = get_feature_columns()

    features = normalized_data[feature_columns].copy()

    return InferenceDataset(
        source_data=normalized_data,
        features=features,
        feature_columns=feature_columns,
        row_count=len(normalized_data),
    )


def predict_inference_dataset(
    model: CatBoostRegressor,
    dataset: InferenceDataset,
) -> np.ndarray:
    """Predict values for inference dataset.
    Args:
        model (CatBoostRegressor): Loaded CatBoost model.
        dataset (InferenceDataset): Prepared inference dataset.
    """
    predictions = model.predict(dataset.features)

    return np.asarray(predictions)


def build_inference_rows(
    source_data: pd.DataFrame,
    predictions: np.ndarray,
) -> list[dict[str, Any]]:
    """Build inference prediction rows.
    Args:
        source_data (pd.DataFrame): Source inference dataframe.
        predictions (np.ndarray): Inference predictions.
    """
    if len(source_data) != len(predictions):
        raise ValueError(
            'Inference source rows and predictions have different lengths: '
            f'{len(source_data)} != {len(predictions)}.',
        )

    inference_rows = []

    for source_row_index, predicted_value in zip(
        list(source_data.index),
        predictions,
        strict=True,
    ):
        source_row = source_data.loc[source_row_index]
        inference_row = {
            'source_row_index': int(source_row_index),
            'predicted_value': float(predicted_value),
        }

        for column in IDENTIFIER_COLUMNS:
            if column not in source_data.columns:
                continue

            column_value = source_row[column]

            if column == 'date_day':
                inference_row[column] = normalize_date_day(column_value)
                continue

            if pd.isna(column_value):
                inference_row[column] = None
                continue

            inference_row[column] = int(column_value)

        inference_rows.append(inference_row)

    return inference_rows
