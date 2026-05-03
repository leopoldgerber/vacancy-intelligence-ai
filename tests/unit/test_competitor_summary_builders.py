import pandas as pd
import pytest

from app.services.analytics.competitor_summary_builders import (
    build_competitor_summary_data,
)
from app.services.analytics.competitor_summary_builders import (
    build_empty_competitor_summary_data,
)


def build_competitor_dataframe() -> pd.DataFrame:
    """Build competitor summary test dataframe.
    Args:
        """
    return pd.DataFrame(
        {
            'client_id': [1, 1, 1, 1],
            'company_id': [20, 20, 30, 30],
            'vacancy_id': [200, 201, 300, 301],
            'callbacks': [15, 25, 35, 45],
            'city': ['Berlin', 'Berlin', 'Munich', 'Berlin'],
            'region': ['Berlin', 'Berlin', 'Bavaria', 'Berlin'],
            'profile': [
                'Filialleiter',
                'Filialleiter',
                'Manager',
                'Filialleiter',
            ],
            'tariff': ['Standard', 'Premium', 'Premium', 'Standard'],
            'work_schedule': ['Full-time', 'Shift', 'Shift', 'Full-time'],
            'work_experience': ['1 year', '3 years', '3 years', '1 year'],
            'employment_type': [
                'Full-time',
                'Part-time',
                'Part-time',
                'Full-time',
            ],
            'salary_from': [1000.0, None, 1400.0, None],
            'salary_to': [2000.0, None, 2400.0, None],
        },
    )


def test_build_empty_competitor_summary_data() -> None:
    """Test empty competitor summary data builder.
    Args:
        """
    result = build_empty_competitor_summary_data(
        analytics_run_id=1,
        client_id=1,
    )

    assert result['analytics_run_id'] == 1
    assert result['client_id'] == 1
    assert result['competitor_company_count'] == 0
    assert result['competitor_snapshot_count'] == 0
    assert result['competitor_vacancy_count'] == 0
    assert result['competitor_total_callbacks'] == 0
    assert result['competitor_avg_callbacks'] == 0.0
    assert result['competitor_median_callbacks'] == 0.0
    assert result['competitor_mode_city'] is None
    assert result['competitor_mode_region'] is None
    assert result['competitor_mode_profile'] is None
    assert result['competitor_mode_tariff'] is None
    assert result['competitor_mode_work_schedule'] is None
    assert result['competitor_mode_work_experience'] is None
    assert result['competitor_mode_employment_type'] is None
    assert result['competitor_median_salary_from'] is None
    assert result['competitor_median_salary_to'] is None
    assert result['competitor_salary_specified_share'] == 0.0
    assert result['competitor_salary_missing_share'] == 0.0


def test_build_competitor_summary_data() -> None:
    """Test competitor summary data builder.
    Args:
        """
    data = build_competitor_dataframe()

    result = build_competitor_summary_data(
        data=data,
        analytics_run_id=1,
        client_id=1,
    )

    assert result['analytics_run_id'] == 1
    assert result['client_id'] == 1
    assert result['competitor_company_count'] == 2
    assert result['competitor_snapshot_count'] == 4
    assert result['competitor_vacancy_count'] == 4
    assert result['competitor_total_callbacks'] == 120
    assert result['competitor_avg_callbacks'] == 30.0
    assert result['competitor_median_callbacks'] == 30.0
    assert result['competitor_mode_city'] == 'Berlin'
    assert result['competitor_mode_region'] == 'Berlin'
    assert result['competitor_mode_profile'] == 'Filialleiter'
    assert result['competitor_mode_tariff'] == 'Premium'
    assert result['competitor_mode_work_schedule'] == 'Full-time'
    assert result['competitor_mode_work_experience'] == '1 year'
    assert result['competitor_mode_employment_type'] == 'Full-time'
    assert result['competitor_median_salary_from'] == 1200.0
    assert result['competitor_median_salary_to'] == 2200.0
    assert result['competitor_salary_specified_share'] == pytest.approx(0.5)
    assert result['competitor_salary_missing_share'] == pytest.approx(0.5)


def test_build_competitor_summary_data_empty_dataframe() -> None:
    """Test competitor summary builder with empty dataframe.
    Args:
        """
    data = pd.DataFrame()

    result = build_competitor_summary_data(
        data=data,
        analytics_run_id=1,
        client_id=1,
    )

    assert result['analytics_run_id'] == 1
    assert result['client_id'] == 1
    assert result['competitor_company_count'] == 0
    assert result['competitor_snapshot_count'] == 0
    assert result['competitor_vacancy_count'] == 0
    assert result['competitor_total_callbacks'] == 0
    assert result['competitor_avg_callbacks'] == 0.0
    assert result['competitor_median_callbacks'] == 0.0
