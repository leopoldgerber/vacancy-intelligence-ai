from datetime import datetime

import pandas as pd

from app.services.features.time_feature_builders import (
    build_time_feature_dataframe,
)
from app.services.features.time_feature_builders import (
    build_time_feature_rows,
)
from app.services.features.time_feature_builders import (
    calculate_is_weekend,
)
from app.services.features.time_feature_builders import (
    calculate_publication_day_of_week,
)
from app.services.features.time_feature_builders import (
    calculate_publication_hour,
)
from app.services.features.time_feature_builders import (
    calculate_publication_month,
)
from app.services.features.time_feature_builders import (
    calculate_publication_week,
)
from app.services.features.time_feature_builders import (
    calculate_vacancy_age_days,
)


def build_time_feature_test_dataframe() -> pd.DataFrame:
    """Build time feature test dataframe.
    Args:
        """
    return pd.DataFrame(
        {
            'client_id': [1, 1, 1],
            'company_id': [10, 10, 20],
            'vacancy_id': [100, 101, 200],
            'date_day': pd.to_datetime(
                [
                    '2025-08-04',
                    '2025-08-05',
                    '2025-08-03',
                ],
            ),
            'publication_date': pd.to_datetime(
                [
                    '2025-08-01 10:30:00',
                    '2025-08-05 15:00:00',
                    '2025-08-04 09:00:00',
                ],
            ),
        },
    )


def test_calculate_publication_hour() -> None:
    """Test publication hour calculation.
    Args:
        """
    result = calculate_publication_hour(
        publication_date=datetime(2025, 8, 1, 10, 30, 0),
    )

    assert result == 10


def test_calculate_publication_hour_missing() -> None:
    """Test publication hour with missing publication date.
    Args:
        """
    result = calculate_publication_hour(publication_date=None)

    assert result == -1


def test_calculate_publication_day_of_week() -> None:
    """Test publication day of week calculation.
    Args:
        """
    result = calculate_publication_day_of_week(
        publication_date=datetime(2025, 8, 1, 10, 30, 0),
    )

    assert result == 4


def test_calculate_publication_month() -> None:
    """Test publication month calculation.
    Args:
        """
    result = calculate_publication_month(
        publication_date=datetime(2025, 8, 1, 10, 30, 0),
    )

    assert result == 8


def test_calculate_publication_week() -> None:
    """Test publication ISO week calculation.
    Args:
        """
    result = calculate_publication_week(
        publication_date=datetime(2025, 8, 1, 10, 30, 0),
    )

    assert result == 31


def test_calculate_is_weekend_false() -> None:
    """Test weekend flag for weekday.
    Args:
        """
    result = calculate_is_weekend(
        publication_date=datetime(2025, 8, 1, 10, 30, 0),
    )

    assert result is False


def test_calculate_is_weekend_true() -> None:
    """Test weekend flag for weekend.
    Args:
        """
    result = calculate_is_weekend(
        publication_date=datetime(2025, 8, 2, 10, 30, 0),
    )

    assert result is True


def test_calculate_vacancy_age_days() -> None:
    """Test vacancy age in days calculation.
    Args:
        """
    result = calculate_vacancy_age_days(
        date_day=datetime(2025, 8, 4, 0, 0, 0),
        publication_date=datetime(2025, 8, 1, 10, 30, 0),
    )

    assert result == 3


def test_calculate_vacancy_age_days_negative() -> None:
    """Test negative vacancy age protection.
    Args:
        """
    result = calculate_vacancy_age_days(
        date_day=datetime(2025, 8, 3, 0, 0, 0),
        publication_date=datetime(2025, 8, 4, 10, 30, 0),
    )

    assert result == 0


def test_calculate_vacancy_age_days_missing() -> None:
    """Test vacancy age with missing dates.
    Args:
        """
    result = calculate_vacancy_age_days(
        date_day=None,
        publication_date=datetime(2025, 8, 4, 10, 30, 0),
    )

    assert result == -1


def test_build_time_feature_dataframe() -> None:
    """Test time feature dataframe builder.
    Args:
        """
    data = build_time_feature_test_dataframe()

    result = build_time_feature_dataframe(data=data)

    assert len(result) == 3

    first_row = result.iloc[0]
    second_row = result.iloc[1]
    third_row = result.iloc[2]

    assert first_row['publication_hour'] == 10
    assert first_row['publication_day_of_week'] == 4
    assert first_row['publication_month'] == 8
    assert first_row['publication_week'] == 31
    assert bool(first_row['is_weekend']) is False
    assert first_row['vacancy_age_days'] == 3

    assert second_row['publication_hour'] == 15
    assert second_row['publication_day_of_week'] == 1
    assert second_row['vacancy_age_days'] == 0

    assert third_row['vacancy_age_days'] == 0


def test_build_time_feature_dataframe_empty_data() -> None:
    """Test time feature dataframe builder with empty data.
    Args:
        """
    data = pd.DataFrame()

    result = build_time_feature_dataframe(data=data)

    assert result.empty


def test_build_time_feature_rows() -> None:
    """Test time feature rows builder.
    Args:
        """
    data = build_time_feature_test_dataframe()

    result = build_time_feature_rows(
        data=data,
        feature_run_id=1,
    )

    assert len(result) == 3

    first_row = result[0]

    assert first_row['feature_run_id'] == 1
    assert first_row['client_id'] == 1
    assert first_row['company_id'] == 10
    assert first_row['vacancy_id'] == 100
    assert first_row['date_day'] is not None
    assert first_row['publication_hour'] == 10
    assert first_row['publication_day_of_week'] == 4
    assert first_row['publication_month'] == 8
    assert first_row['publication_week'] == 31
    assert first_row['is_weekend'] is False
    assert first_row['vacancy_age_days'] == 3


def test_build_time_feature_rows_empty_data() -> None:
    """Test time feature rows builder with empty data.
    Args:
        """
    data = pd.DataFrame()

    result = build_time_feature_rows(
        data=data,
        feature_run_id=1,
    )

    assert result == []
