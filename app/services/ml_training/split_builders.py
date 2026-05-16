from dataclasses import dataclass

import pandas as pd
from sklearn.model_selection import train_test_split

from app.services.ml_training.constants import RANDOM_SEED
from app.services.ml_training.constants import TEST_SIZE
from app.services.ml_training.dataset_builders import TrainingDataset


@dataclass
class TrainingSplit:
    """Prepared train/test split."""

    train_features: pd.DataFrame
    test_features: pd.DataFrame
    train_target: pd.Series
    test_target: pd.Series
    split_strategy: str
    train_row_count: int
    test_row_count: int


def has_enough_dates(data: pd.DataFrame) -> bool:
    """Check whether data has enough unique dates for time split.
    Args:
        data (pd.DataFrame): Source training dataframe."""
    if 'date_day' not in data.columns:
        return False

    return data['date_day'].nunique() >= 2


def build_time_split(
    source_data: pd.DataFrame,
    dataset: TrainingDataset,
) -> TrainingSplit:
    """Build time-based train/test split.
    Args:
        source_data (pd.DataFrame): Source training dataframe with date_day.
        dataset (TrainingDataset): Prepared training dataset."""
    sorted_data = source_data.copy()
    sorted_data['date_day'] = pd.to_datetime(sorted_data['date_day'])
    sorted_data = sorted_data.sort_values('date_day').reset_index(drop=True)

    unique_dates = sorted_data['date_day'].drop_duplicates().sort_values()
    test_date_count = max(1, int(len(unique_dates) * TEST_SIZE))
    test_dates = set(unique_dates.iloc[-test_date_count:])

    train_mask = ~sorted_data['date_day'].isin(test_dates)
    test_mask = sorted_data['date_day'].isin(test_dates)

    if train_mask.sum() == 0 or test_mask.sum() == 0:
        return build_random_split(dataset=dataset)

    train_indices = sorted_data.index[train_mask].tolist()
    test_indices = sorted_data.index[test_mask].tolist()

    normalized_features = dataset.features.reset_index(drop=True)
    normalized_target = dataset.target.reset_index(drop=True)

    return TrainingSplit(
        train_features=normalized_features.iloc[train_indices].reset_index(
            drop=True,
        ),
        test_features=normalized_features.iloc[test_indices].reset_index(
            drop=True,
        ),
        train_target=normalized_target.iloc[train_indices].reset_index(
            drop=True,
        ),
        test_target=normalized_target.iloc[test_indices].reset_index(
            drop=True,
        ),
        split_strategy='time_based',
        train_row_count=len(train_indices),
        test_row_count=len(test_indices),
    )


def build_random_split(dataset: TrainingDataset) -> TrainingSplit:
    """Build deterministic random train/test split.

    Args:
        dataset (TrainingDataset): Prepared training dataset.
    """
    (
        train_features,
        test_features,
        train_target,
        test_target,
    ) = train_test_split(
        dataset.features,
        dataset.target,
        test_size=TEST_SIZE,
        random_state=RANDOM_SEED,
        shuffle=True,
    )

    return TrainingSplit(
        train_features=train_features.reset_index(drop=True),
        test_features=test_features.reset_index(drop=True),
        train_target=train_target.reset_index(drop=True),
        test_target=test_target.reset_index(drop=True),
        split_strategy='random_fallback',
        train_row_count=len(train_features),
        test_row_count=len(test_features),
    )


def build_training_split(
    source_data: pd.DataFrame,
    dataset: TrainingDataset,
) -> TrainingSplit:
    """Build train/test split for ML training.
    Args:
        source_data (pd.DataFrame): Source training dataframe.
        dataset (TrainingDataset): Prepared training dataset."""
    if has_enough_dates(data=source_data):
        return build_time_split(
            source_data=source_data,
            dataset=dataset,
        )

    return build_random_split(dataset=dataset)
