import pandas as pd
import pytest

from app.services.analytics.client_summary_builders import (
    build_client_summary_data,
)
from app.services.analytics.client_summary_builders import (
    build_empty_client_summary_data,
)


def build_client_dataframe() -> pd.DataFrame:
    """Build client summary test dataframe.
    Args:
        """
    return pd.DataFrame(
        {
            'client_id': [1, 1, 1],
            'company_id': [10, 10, 10],
            'vacancy_id': [100, 101, 102],
            'callbacks': [10, 20, 30],
            'city': ['Berlin', 'Berlin', 'Munich'],
            'region': ['Berlin', 'Berlin', 'Bavaria'],
            'profile': [
                'Filialleiter',
                'Filialleiter',
                'Manager',
            ],
            'tariff': ['Standard', 'Standard', 'Premium'],
            'work_schedule': ['Full-time', 'Full-time', 'Shift'],
            'work_experience': ['1 year', '1 year', '3 years'],
            'employment_type': ['Full-time', 'Full-time', 'Part-time'],
            'salary_from': [1000.0, 1200.0, None],
            'salary_to': [2000.0, 2200.0, None],
        },
    )


def test_build_empty_client_summary_data() -> None:
    """Test empty client summary data builder.
    Args:
        """
    result = build_empty_client_summary_data(
        analytics_run_id=1,
        client_id=1,
        client_company_name='Lidl',
    )

    assert result['analytics_run_id'] == 1
    assert result['client_id'] == 1
    assert result['client_company_name'] == 'Lidl'
    assert result['client_snapshot_count'] == 0
    assert result['client_vacancy_count'] == 0
    assert result['client_total_callbacks'] == 0
    assert result['client_avg_callbacks'] == 0.0
    assert result['client_median_callbacks'] == 0.0
    assert result['client_mode_city'] is None
    assert result['client_mode_region'] is None
    assert result['client_mode_profile'] is None
    assert result['client_mode_tariff'] is None
    assert result['client_mode_work_schedule'] is None
    assert result['client_mode_work_experience'] is None
    assert result['client_mode_employment_type'] is None
    assert result['client_median_salary_from'] is None
    assert result['client_median_salary_to'] is None
    assert result['client_salary_specified_share'] == 0.0
    assert result['client_salary_missing_share'] == 0.0


def test_build_client_summary_data() -> None:
    """Test client summary data builder.
    Args:
        """
    data = build_client_dataframe()

    result = build_client_summary_data(
        data=data,
        analytics_run_id=1,
        client_id=1,
        client_company_name='Lidl',
    )

    assert result['analytics_run_id'] == 1
    assert result['client_id'] == 1
    assert result['client_company_name'] == 'Lidl'
    assert result['client_snapshot_count'] == 3
    assert result['client_vacancy_count'] == 3
    assert result['client_total_callbacks'] == 60
    assert result['client_avg_callbacks'] == 20.0
    assert result['client_median_callbacks'] == 20.0
    assert result['client_mode_city'] == 'Berlin'
    assert result['client_mode_region'] == 'Berlin'
    assert result['client_mode_profile'] == 'Filialleiter'
    assert result['client_mode_tariff'] == 'Standard'
    assert result['client_mode_work_schedule'] == 'Full-time'
    assert result['client_mode_work_experience'] == '1 year'
    assert result['client_mode_employment_type'] == 'Full-time'
    assert result['client_median_salary_from'] == 1100.0
    assert result['client_median_salary_to'] == 2100.0
    assert result['client_salary_specified_share'] == pytest.approx(2 / 3)
    assert result['client_salary_missing_share'] == pytest.approx(1 / 3)


def test_build_client_summary_data_empty_dataframe() -> None:
    """Test client summary builder with empty dataframe.
    Args:
        """
    data = pd.DataFrame()

    result = build_client_summary_data(
        data=data,
        analytics_run_id=1,
        client_id=1,
        client_company_name='Lidl',
    )

    assert result['analytics_run_id'] == 1
    assert result['client_id'] == 1
    assert result['client_company_name'] == 'Lidl'
    assert result['client_snapshot_count'] == 0
    assert result['client_vacancy_count'] == 0
    assert result['client_total_callbacks'] == 0
    assert result['client_avg_callbacks'] == 0.0
    assert result['client_median_callbacks'] == 0.0
