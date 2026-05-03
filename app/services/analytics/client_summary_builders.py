import pandas as pd

from app.services.analytics.market_summary_builders import (
    calculate_salary_share,
)
from app.services.analytics.market_summary_builders import get_series_mode


def build_empty_client_summary_data(
    analytics_run_id: int,
    client_id: int,
    client_company_name: str,
) -> dict[str, int | float | str | None]:
    """Build empty client summary data.
    Args:
        analytics_run_id (int): Analytics run identifier.
        client_id (int): Client identifier.
        client_company_name (str): Target client company name.
    """
    return {
        'analytics_run_id': analytics_run_id,
        'client_id': client_id,
        'client_company_name': client_company_name,
        'client_snapshot_count': 0,
        'client_vacancy_count': 0,
        'client_total_callbacks': 0,
        'client_avg_callbacks': 0.0,
        'client_median_callbacks': 0.0,
        'client_mode_city': None,
        'client_mode_region': None,
        'client_mode_profile': None,
        'client_mode_tariff': None,
        'client_mode_work_schedule': None,
        'client_mode_work_experience': None,
        'client_mode_employment_type': None,
        'client_median_salary_from': None,
        'client_median_salary_to': None,
        'client_salary_specified_share': 0.0,
        'client_salary_missing_share': 0.0,
    }


def build_client_summary_data(
    data: pd.DataFrame,
    analytics_run_id: int,
    client_id: int,
    client_company_name: str,
) -> dict[str, int | float | str | None]:
    """Build client summary data.
    Args:
        data (pd.DataFrame): Target client snapshot dataframe.
        analytics_run_id (int): Analytics run identifier.
        client_id (int): Client identifier.
        client_company_name (str): Target client company name.
    """
    if data.empty:
        return build_empty_client_summary_data(
            analytics_run_id=analytics_run_id,
            client_id=client_id,
            client_company_name=client_company_name,
        )

    salary_share = calculate_salary_share(data=data)

    return {
        'analytics_run_id': analytics_run_id,
        'client_id': client_id,
        'client_company_name': client_company_name,
        'client_snapshot_count': int(len(data)),
        'client_vacancy_count': int(data['vacancy_id'].nunique()),
        'client_total_callbacks': int(data['callbacks'].sum()),
        'client_avg_callbacks': float(data['callbacks'].mean()),
        'client_median_callbacks': float(data['callbacks'].median()),
        'client_mode_city': get_series_mode(series=data['city']),
        'client_mode_region': get_series_mode(series=data['region']),
        'client_mode_profile': get_series_mode(series=data['profile']),
        'client_mode_tariff': get_series_mode(series=data['tariff']),
        'client_mode_work_schedule': get_series_mode(
            series=data['work_schedule'],
        ),
        'client_mode_work_experience': get_series_mode(
            series=data['work_experience'],
        ),
        'client_mode_employment_type': get_series_mode(
            series=data['employment_type'],
        ),
        'client_median_salary_from': float(data['salary_from'].median())
        if data['salary_from'].notna().any()
        else None,
        'client_median_salary_to': float(data['salary_to'].median())
        if data['salary_to'].notna().any()
        else None,
        'client_salary_specified_share': salary_share[
            'salary_specified_share'
        ],
        'client_salary_missing_share': salary_share[
            'salary_missing_share'
        ],
    }
