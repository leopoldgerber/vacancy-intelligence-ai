from datetime import datetime

import pandas as pd

from app.services.features.publication_activity_feature_builders import (
    build_publication_activity_feature_dataframe,
)
from app.services.features.publication_activity_feature_builders import (
    build_publication_activity_feature_rows,
)
from app.services.features.publication_activity_feature_builders import (
    calculate_publication_activity_level,
)


def build_publication_activity_dataframe() -> pd.DataFrame:
    """Build publication activity feature test dataframe.
    Args:
        """
    return pd.DataFrame(
        {
            'client_id': [1, 1, 1, 1, 1, 1],
            'company_id': [10, 10, 10, 10, 20, 20],
            'vacancy_id': [100, 100, 100, 100, 200, 200],
            'date_day': pd.to_datetime(
                [
                    '2025-08-01',
                    '2025-08-02',
                    '2025-08-03',
                    '2025-08-04',
                    '2025-08-01',
                    '2025-08-03',
                ],
            ),
            'standard': [1, 0, 0, 0, 0, 0],
            'standard_plus': [0, 0, 0, 2, 0, 0],
            'premium': [0, 0, 0, 0, 1, 0],
        },
    )


def test_calculate_publication_activity_level_premium() -> None:
    """Test premium publication activity level.
    Args:
        """
    result = calculate_publication_activity_level(
        standard=1,
        standard_plus=1,
        premium=1,
    )

    assert result == 3


def test_calculate_publication_activity_level_standard_plus() -> None:
    """Test standard plus publication activity level.
    Args:
        """
    result = calculate_publication_activity_level(
        standard=1,
        standard_plus=1,
        premium=0,
    )

    assert result == 2


def test_calculate_publication_activity_level_standard() -> None:
    """Test standard publication activity level.
    Args:
        """
    result = calculate_publication_activity_level(
        standard=1,
        standard_plus=0,
        premium=0,
    )

    assert result == 1


def test_calculate_publication_activity_level_no_activity() -> None:
    """Test no publication activity level.
    Args:
        """
    result = calculate_publication_activity_level(
        standard=0,
        standard_plus=0,
        premium=0,
    )

    assert result == 0


def test_build_publication_activity_feature_dataframe() -> None:
    """Test publication activity feature dataframe builder.
    Args:
        """
    data = build_publication_activity_dataframe()

    result = build_publication_activity_feature_dataframe(data=data)

    assert len(result) == 6

    vacancy_100_rows = result[
        result['vacancy_id'] == 100
    ].sort_values('date_day')
    vacancy_200_rows = result[
        result['vacancy_id'] == 200
    ].sort_values('date_day')

    assert vacancy_100_rows[
        'publication_activity_level'
    ].tolist() == [1, 0, 0, 0]

    assert vacancy_100_rows[
        'days_since_last_publication_activity'
    ].tolist() == [0, 1, 2, 3]

    assert vacancy_200_rows[
        'publication_activity_level'
    ].tolist() == [3, 0]

    assert vacancy_200_rows[
        'days_since_last_publication_activity'
    ].tolist() == [0, 2]


def test_build_publication_activity_feature_dataframe_no_prior_activity(
) -> None:
    """Test days since last publication when no prior activity exists.
    Args:
        """
    data = pd.DataFrame(
        {
            'client_id': [1, 1],
            'company_id': [10, 10],
            'vacancy_id': [100, 100],
            'date_day': pd.to_datetime(
                [
                    '2025-08-01',
                    '2025-08-02',
                ],
            ),
            'standard': [0, 0],
            'standard_plus': [0, 0],
            'premium': [0, 0],
        },
    )

    result = build_publication_activity_feature_dataframe(data=data)

    assert result[
        'publication_activity_level'
    ].tolist() == [0, 0]
    assert result[
        'days_since_last_publication_activity'
    ].tolist() == [-1, -1]


def test_build_publication_activity_feature_dataframe_empty_data() -> None:
    """Test publication activity feature dataframe builder with empty data.
    Args:
        """
    data = pd.DataFrame()

    result = build_publication_activity_feature_dataframe(data=data)

    assert result.empty


def test_build_publication_activity_feature_rows() -> None:
    """Test publication activity feature rows builder.
    Args:
        """
    data = build_publication_activity_dataframe()

    result = build_publication_activity_feature_rows(
        data=data,
        feature_run_id=1,
    )

    assert len(result) == 6

    first_row = result[0]

    assert first_row['feature_run_id'] == 1
    assert first_row['client_id'] == 1
    assert first_row['company_id'] == 10
    assert first_row['vacancy_id'] == 100
    assert isinstance(first_row['date_day'], pd.Timestamp | datetime)
    assert first_row['publication_activity_level'] == 1
    assert first_row['days_since_last_publication_activity'] == 0


def test_build_publication_activity_feature_rows_empty_data() -> None:
    """Test publication activity feature rows builder with empty data.
    Args:
        """
    data = pd.DataFrame()

    result = build_publication_activity_feature_rows(
        data=data,
        feature_run_id=1,
    )

    assert result == []
