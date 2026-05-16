from dataclasses import dataclass

import pandas as pd

from app.services.ml_training.constants import MIN_TRAINING_ROW_COUNT
from app.services.ml_training.feature_schema import CATEGORICAL_FEATURE_COLUMNS
from app.services.ml_training.feature_schema import NUMERICAL_FEATURE_COLUMNS
from app.services.ml_training.feature_schema import TARGET_COLUMN
from app.services.ml_training.feature_schema import (
    get_categorical_feature_indices)
from app.services.ml_training.feature_schema import get_feature_columns
from app.services.ml_training.feature_schema import get_missing_columns


@dataclass
class TrainingDataset:
    """Prepared training dataset."""

    features: pd.DataFrame
    target: pd.Series
    feature_columns: list[str]
    categorical_feature_columns: list[str]
    categorical_feature_indices: list[int]
    row_count: int


def validate_columns(data: pd.DataFrame) -> None:
    """Validate required training columns.
    Args:
        data (pd.DataFrame): Source training dataframe."""
    missing_columns = get_missing_columns(columns=list(data.columns))

    if missing_columns:
        raise ValueError(
            f'Missing required ML training columns: {missing_columns}',
        )


def validate_rows(data: pd.DataFrame) -> None:
    """Validate training row count.
    Args:
        data (pd.DataFrame): Source training dataframe."""
    if data.empty:
        raise ValueError('ML training dataframe is empty.')

    if len(data) < MIN_TRAINING_ROW_COUNT:
        raise ValueError(
            'ML training dataframe has insufficient rows: '
            f'{len(data)}. Minimum required: {MIN_TRAINING_ROW_COUNT}.',
        )


def validate_target(data: pd.DataFrame) -> None:
    """Validate target column.
    Args:
        data (pd.DataFrame): Source training dataframe."""
    if data[TARGET_COLUMN].isna().any():
        raise ValueError('ML training target contains missing values.')


def normalize_features(data: pd.DataFrame) -> pd.DataFrame:
    """Normalize feature values for training.
    Args:
        data (pd.DataFrame): Source training dataframe."""
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


def build_dataset(data: pd.DataFrame) -> TrainingDataset:
    """Build prepared training dataset.
    Args:
        data (pd.DataFrame): Source training dataframe."""
    validate_columns(data=data)
    validate_rows(data=data)
    validate_target(data=data)

    normalized_data = normalize_features(data=data)
    feature_columns = get_feature_columns()

    features = normalized_data[feature_columns].copy()
    target = pd.to_numeric(
        normalized_data[TARGET_COLUMN],
        errors='coerce',
    )

    if target.isna().any():
        raise ValueError('ML training target contains invalid numeric values.')

    return TrainingDataset(
        features=features,
        target=target,
        feature_columns=feature_columns,
        categorical_feature_columns=CATEGORICAL_FEATURE_COLUMNS,
        categorical_feature_indices=get_categorical_feature_indices(),
        row_count=len(normalized_data),
    )
