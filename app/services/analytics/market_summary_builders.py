import pandas as pd


def get_series_mode(series: pd.Series) -> str | None:
    """Get most frequent non-empty series value.
    Args:
        series (pd.Series): Input pandas series.
    """
    clean_series = series.dropna()

    if clean_series.empty:
        return None

    clean_series = clean_series.astype(str).str.strip()
    clean_series = clean_series[clean_series.ne('')]

    if clean_series.empty:
        return None

    return str(clean_series.mode().iloc[0])


def calculate_salary_share(data: pd.DataFrame) -> dict[str, float]:
    """Calculate salary specified and missing shares.
    Args:
        data (pd.DataFrame): Snapshot dataframe.
    """
    salary_mask = (
        data['salary_from'].notna()
        | data['salary_to'].notna()
    )
    total_count = len(data)

    if total_count == 0:
        return {
            'salary_specified_share': 0.0,
            'salary_missing_share': 0.0,
        }

    salary_specified_share = float(salary_mask.sum() / total_count)
    salary_missing_share = float(1 - salary_specified_share)

    return {
        'salary_specified_share': salary_specified_share,
        'salary_missing_share': salary_missing_share,
    }


def build_market_summary_data(
    data: pd.DataFrame,
    analytics_run_id: int,
    client_id: int,
) -> dict[str, int | float | str | None]:
    """Build market summary data.
    Args:
        data (pd.DataFrame): Snapshot dataframe.
        analytics_run_id (int): Analytics run identifier.
        client_id (int): Client identifier.
    """
    salary_share = calculate_salary_share(data=data)

    return {
        'analytics_run_id': analytics_run_id,
        'client_id': client_id,
        'total_snapshot_count': int(len(data)),
        'total_company_count': int(data['company_id'].nunique()),
        'total_vacancy_count': int(data['vacancy_id'].nunique()),
        'total_callbacks': int(data['callbacks'].sum()),
        'avg_callbacks': float(data['callbacks'].mean()),
        'median_callbacks': float(data['callbacks'].median()),
        'mode_city': get_series_mode(series=data['city']),
        'mode_region': get_series_mode(series=data['region']),
        'mode_profile': get_series_mode(series=data['profile']),
        'mode_tariff': get_series_mode(series=data['tariff']),
        'mode_work_schedule': get_series_mode(
            series=data['work_schedule'],
        ),
        'mode_work_experience': get_series_mode(
            series=data['work_experience'],
        ),
        'mode_employment_type': get_series_mode(
            series=data['employment_type'],
        ),
        'median_salary_from': float(data['salary_from'].median())
        if data['salary_from'].notna().any()
        else None,
        'median_salary_to': float(data['salary_to'].median())
        if data['salary_to'].notna().any()
        else None,
        'salary_specified_share': salary_share[
            'salary_specified_share'
        ],
        'salary_missing_share': salary_share[
            'salary_missing_share'
        ],
    }
