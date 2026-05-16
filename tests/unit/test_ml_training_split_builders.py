import pandas as pd

from app.services.ml_training.dataset_builders import build_dataset
from app.services.ml_training.feature_schema import get_training_columns
from app.services.ml_training.split_builders import build_random_split
from app.services.ml_training.split_builders import build_time_split
from app.services.ml_training.split_builders import build_training_split
from app.services.ml_training.split_builders import has_enough_dates


def build_split_dataframe(
    row_count: int = 20,
    unique_dates: int = 5,
) -> pd.DataFrame:
    """Build dataframe for split tests.
    Args:
        row_count (int): Number of rows.
        unique_dates (int): Number of unique dates."""
    rows = []
    base_date = pd.Timestamp('2025-08-01')

    for index in range(row_count):
        row = {
            'client_id': 1,
            'company_id': index % 3 + 1,
            'vacancy_id': 1000 + index,
            'date_day': base_date + pd.Timedelta(days=index % unique_dates),
            'callbacks': index + 1,
            'salary_mid': 1000 + index,
            'salary_is_specified': True,
            'salary_ratio_to_market_by_city': 1.0,
            'salary_ratio_to_market_by_profile': 0.95,
            'salary_ratio_to_market_by_city_profile': 1.05,
            'publication_activity_level': index % 4,
            'days_since_last_publication_activity': index % 5,
            'title_length': 20 + index,
            'description_length': 100 + index,
            'title_word_count': 2,
            'description_word_count': 15,
            'has_description': True,
            'description_is_empty': False,
            'has_salary_mention': index % 2 == 0,
            'has_schedule_mention': True,
            'has_requirements_mention': True,
            'has_benefits_mention': index % 2 == 1,
            'has_call_to_action': True,
            'publication_hour': 9,
            'publication_day_of_week': 1,
            'publication_month': 8,
            'publication_week': 31,
            'is_weekend': False,
            'vacancy_age_days': index,
            'city': 'Berlin',
            'region': 'Berlin',
            'profile': 'Filialleiter',
            'employment_type': 'Full-time',
            'work_experience': '1 year',
            'work_schedule': 'Full-time',
        }
        rows.append(row)

    return pd.DataFrame(
        rows,
        columns=get_training_columns(),
    )


def test_has_enough_dates_true() -> None:
    """Test date availability check with enough dates.
    Args:
        """
    data = build_split_dataframe(unique_dates=3)

    result = has_enough_dates(data=data)

    assert result is True


def test_has_enough_dates_false() -> None:
    """Test date availability check with one date.
    Args:
        """
    data = build_split_dataframe(unique_dates=1)

    result = has_enough_dates(data=data)

    assert result is False


def test_has_enough_dates_missing_column() -> None:
    """Test date availability check without date_day column.
    Args:
        """
    data = build_split_dataframe().drop(columns=['date_day'])

    result = has_enough_dates(data=data)

    assert result is False


def test_build_random_split() -> None:
    """Test deterministic random split.
    Args:
        """
    data = build_split_dataframe(row_count=20, unique_dates=1)
    dataset = build_dataset(data=data)

    result = build_random_split(dataset=dataset)

    assert result.split_strategy == 'random_fallback'
    assert result.train_row_count == 16
    assert result.test_row_count == 4
    assert len(result.train_features) == 16
    assert len(result.test_features) == 4
    assert len(result.train_target) == 16
    assert len(result.test_target) == 4


def test_build_time_split() -> None:
    """Test time-based split.
    Args:
        """
    data = build_split_dataframe(row_count=20, unique_dates=5)
    dataset = build_dataset(data=data)

    result = build_time_split(
        source_data=data,
        dataset=dataset,
    )

    assert result.split_strategy == 'time_based'
    assert result.train_row_count == 16
    assert result.test_row_count == 4
    assert len(result.train_features) == 16
    assert len(result.test_features) == 4
    assert len(result.train_target) == 16
    assert len(result.test_target) == 4


def test_build_training_split_uses_time_based() -> None:
    """Test training split uses time-based strategy.
    Args:
        """
    data = build_split_dataframe(row_count=20, unique_dates=5)
    dataset = build_dataset(data=data)

    result = build_training_split(
        source_data=data,
        dataset=dataset,
    )

    assert result.split_strategy == 'time_based'
    assert result.train_row_count == 16
    assert result.test_row_count == 4


def test_build_training_split_uses_random_fallback() -> None:
    """Test training split uses random fallback strategy.
    Args:
        """
    data = build_split_dataframe(row_count=20, unique_dates=1)
    dataset = build_dataset(data=data)

    result = build_training_split(
        source_data=data,
        dataset=dataset,
    )

    assert result.split_strategy == 'random_fallback'
    assert result.train_row_count == 16
    assert result.test_row_count == 4
