import pandas as pd

from app.services.analytics.market_summary_builders import (
    calculate_salary_share,
)
from app.services.analytics.market_summary_builders import get_series_mode


def build_empty_competitor_summary_data(
    analytics_run_id: int,
    client_id: int,
) -> dict[str, int | float | str | None]:
    """Build empty competitor summary data.
    Args:
        analytics_run_id (int): Analytics run identifier.
        client_id (int): Client identifier.
    """
    return {
        'analytics_run_id': analytics_run_id,
        'client_id': client_id,
        'competitor_company_count': 0,
        'competitor_snapshot_count': 0,
        'competitor_vacancy_count': 0,
        'competitor_total_callbacks': 0,
        'competitor_avg_callbacks': 0.0,
        'competitor_median_callbacks': 0.0,
        'competitor_mode_city': None,
        'competitor_mode_region': None,
        'competitor_mode_profile': None,
        'competitor_mode_tariff': None,
        'competitor_mode_work_schedule': None,
        'competitor_mode_work_experience': None,
        'competitor_mode_employment_type': None,
        'competitor_median_salary_from': None,
        'competitor_median_salary_to': None,
        'competitor_salary_specified_share': 0.0,
        'competitor_salary_missing_share': 0.0,
    }


def build_competitor_summary_data(
    data: pd.DataFrame,
    analytics_run_id: int,
    client_id: int,
) -> dict[str, int | float | str | None]:
    """Build competitor summary data.
    Args:
        data (pd.DataFrame): Competitor snapshot dataframe.
        analytics_run_id (int): Analytics run identifier.
        client_id (int): Client identifier.
    """
    if data.empty:
        return build_empty_competitor_summary_data(
            analytics_run_id=analytics_run_id,
            client_id=client_id,
        )

    salary_share = calculate_salary_share(data=data)

    return {
        'analytics_run_id': analytics_run_id,
        'client_id': client_id,
        'competitor_company_count': int(data['company_id'].nunique()),
        'competitor_snapshot_count': int(len(data)),
        'competitor_vacancy_count': int(data['vacancy_id'].nunique()),
        'competitor_total_callbacks': int(data['callbacks'].sum()),
        'competitor_avg_callbacks': float(data['callbacks'].mean()),
        'competitor_median_callbacks': float(data['callbacks'].median()),
        'competitor_mode_city': get_series_mode(series=data['city']),
        'competitor_mode_region': get_series_mode(series=data['region']),
        'competitor_mode_profile': get_series_mode(series=data['profile']),
        'competitor_mode_tariff': get_series_mode(series=data['tariff']),
        'competitor_mode_work_schedule': get_series_mode(
            series=data['work_schedule'],
        ),
        'competitor_mode_work_experience': get_series_mode(
            series=data['work_experience'],
        ),
        'competitor_mode_employment_type': get_series_mode(
            series=data['employment_type'],
        ),
        'competitor_median_salary_from': float(
            data['salary_from'].median(),
        )
        if data['salary_from'].notna().any()
        else None,
        'competitor_median_salary_to': float(data['salary_to'].median())
        if data['salary_to'].notna().any()
        else None,
        'competitor_salary_specified_share': salary_share[
            'salary_specified_share'
        ],
        'competitor_salary_missing_share': salary_share[
            'salary_missing_share'
        ],
    }
