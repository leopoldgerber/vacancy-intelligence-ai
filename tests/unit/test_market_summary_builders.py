import pandas as pd

from app.services.analytics.market_summary_builders import (
    build_market_summary_data,
)
from app.services.analytics.market_summary_builders import (
    calculate_salary_share,
)
from app.services.analytics.market_summary_builders import get_series_mode


def build_market_dataframe() -> pd.DataFrame:
    """Build market summary test dataframe.
    Args:
        """
    return pd.DataFrame(
        {
            'client_id': [1, 1, 1, 1],
            'company_id': [10, 10, 20, 30],
            'vacancy_id': [100, 101, 200, 300],
            'callbacks': [10, 20, 30, 40],
            'city': ['Berlin', 'Berlin', 'Munich', 'Berlin'],
            'region': ['Berlin', 'Berlin', 'Bavaria', 'Berlin'],
            'profile': [
                'Filialleiter',
                'Filialleiter',
                'Manager',
                'Filialleiter',
            ],
            'tariff': ['Standard', 'Standard', 'Premium', None],
            'work_schedule': ['Full-time', 'Full-time', 'Shift', 'Full-time'],
            'work_experience': ['1 year', '1 year', '3 years', '1 year'],
            'employment_type': ['Full-time', 'Full-time', 'Part-time', ''],
            'salary_from': [1000.0, 1200.0, None, None],
            'salary_to': [2000.0, 2200.0, None, None],
        },
    )


def test_get_series_mode() -> None:
    """Test most frequent series value.
    Args:
        """
    data = build_market_dataframe()

    result = get_series_mode(series=data['city'])

    assert result == 'Berlin'


def test_get_series_mode_empty_values() -> None:
    """Test mode with empty values.
    Args:
        """
    data = pd.Series([None, '', '   '])

    result = get_series_mode(series=data)

    assert result is None


def test_calculate_salary_share() -> None:
    """Test salary share calculation.
    Args:
        """
    data = build_market_dataframe()

    result = calculate_salary_share(data=data)

    assert result['salary_specified_share'] == 0.5
    assert result['salary_missing_share'] == 0.5


def test_calculate_salary_share_empty_data() -> None:
    """Test salary share calculation with empty data.
    Args:
        """
    data = pd.DataFrame(
        {
            'salary_from': [],
            'salary_to': [],
        },
    )

    result = calculate_salary_share(data=data)

    assert result['salary_specified_share'] == 0.0
    assert result['salary_missing_share'] == 0.0


def test_build_market_summary_data() -> None:
    """Test market summary data builder.
    Args:
        """
    data = build_market_dataframe()

    result = build_market_summary_data(
        data=data,
        analytics_run_id=1,
        client_id=1,
    )

    assert result['analytics_run_id'] == 1
    assert result['client_id'] == 1
    assert result['total_snapshot_count'] == 4
    assert result['total_company_count'] == 3
    assert result['total_vacancy_count'] == 4
    assert result['total_callbacks'] == 100
    assert result['avg_callbacks'] == 25.0
    assert result['median_callbacks'] == 25.0
    assert result['mode_city'] == 'Berlin'
    assert result['mode_region'] == 'Berlin'
    assert result['mode_profile'] == 'Filialleiter'
    assert result['mode_tariff'] == 'Standard'
    assert result['mode_work_schedule'] == 'Full-time'
    assert result['mode_work_experience'] == '1 year'
    assert result['mode_employment_type'] == 'Full-time'
    assert result['median_salary_from'] == 1100.0
    assert result['median_salary_to'] == 2100.0
    assert result['salary_specified_share'] == 0.5
    assert result['salary_missing_share'] == 0.5
