import pandas as pd


def calculate_salary_mid(
    salary_from: float | None,
    salary_to: float | None,
) -> float:
    """Calculate salary midpoint.
    Args:
        salary_from (float | None): Lower salary bound.
        salary_to (float | None): Upper salary bound.
    """
    has_salary_from = pd.notna(salary_from)
    has_salary_to = pd.notna(salary_to)

    if has_salary_from and has_salary_to:
        return float((salary_from + salary_to) / 2)

    if has_salary_from:
        return float(salary_from)

    if has_salary_to:
        return float(salary_to)

    return 0.0


def calculate_salary_ratio(
    company_salary_median: float,
    market_salary_median: float,
) -> float:
    """Calculate salary ratio to market.
    Args:
        company_salary_median (float): Company salary median.
        market_salary_median (float): Market salary median without company.
    """
    if market_salary_median == 0:
        return 0.0

    return float(company_salary_median / market_salary_median)


def add_salary_mid_features(data: pd.DataFrame) -> pd.DataFrame:
    """Add row-level salary midpoint features.
    Args:
        data (pd.DataFrame): Input snapshot dataframe.
    """
    feature_data = data.copy()

    feature_data['salary_mid'] = feature_data.apply(
        lambda row: calculate_salary_mid(
            salary_from=row['salary_from'],
            salary_to=row['salary_to'],
        ),
        axis=1,
    )
    feature_data['salary_is_specified'] = (
        feature_data['salary_from'].notna()
        | feature_data['salary_to'].notna()
    )

    return feature_data


def get_group_median(
    data: pd.DataFrame,
    company_id: int,
    group_columns: list[str],
    row: pd.Series,
) -> float:
    """Get company salary median for row group.
    Args:
        data (pd.DataFrame): Salary feature dataframe.
        company_id (int): Company identifier.
        group_columns (list[str]): Group columns.
        row (pd.Series): Current dataframe row.
    """
    group_mask = data['company_id'] == company_id

    for column in group_columns:
        group_mask = group_mask & (data[column] == row[column])

    group_data = data.loc[group_mask, 'salary_mid']

    if group_data.empty:
        return 0.0

    return float(group_data.median())


def get_market_median_excl_company(
    data: pd.DataFrame,
    company_id: int,
    group_columns: list[str],
    row: pd.Series,
) -> float:
    """Get market salary median excluding current company.
    Args:
        data (pd.DataFrame): Salary feature dataframe.
        company_id (int): Company identifier.
        group_columns (list[str]): Group columns.
        row (pd.Series): Current dataframe row.
    """
    group_mask = data['company_id'] != company_id

    for column in group_columns:
        group_mask = group_mask & (data[column] == row[column])

    group_data = data.loc[group_mask, 'salary_mid']

    if group_data.empty:
        return 0.0

    return float(group_data.median())


def add_salary_group_features(
    data: pd.DataFrame,
    group_columns: list[str],
    company_median_column: str,
    market_median_column: str,
    ratio_column: str,
) -> pd.DataFrame:
    """Add grouped salary benchmark features.
    Args:
        data (pd.DataFrame): Salary feature dataframe.
        group_columns (list[str]): Group columns.
        company_median_column (str): Company median output column.
        market_median_column (str): Market median output column.
        ratio_column (str): Salary ratio output column.
    """
    feature_data = data.copy()

    company_medians = []
    market_medians = []
    ratios = []

    for _, row in feature_data.iterrows():
        company_id = int(row['company_id'])
        company_median = get_group_median(
            data=feature_data,
            company_id=company_id,
            group_columns=group_columns,
            row=row,
        )
        market_median = get_market_median_excl_company(
            data=feature_data,
            company_id=company_id,
            group_columns=group_columns,
            row=row,
        )
        ratio = calculate_salary_ratio(
            company_salary_median=company_median,
            market_salary_median=market_median,
        )

        company_medians.append(company_median)
        market_medians.append(market_median)
        ratios.append(ratio)

    feature_data[company_median_column] = company_medians
    feature_data[market_median_column] = market_medians
    feature_data[ratio_column] = ratios

    return feature_data


def build_salary_feature_dataframe(data: pd.DataFrame) -> pd.DataFrame:
    """Build salary feature dataframe.
    Args:
        data (pd.DataFrame): Input snapshot dataframe.
    """
    if data.empty:
        return pd.DataFrame()

    feature_data = add_salary_mid_features(data=data)

    feature_data = add_salary_group_features(
        data=feature_data,
        group_columns=['city'],
        company_median_column='company_salary_median_by_city',
        market_median_column='market_salary_median_excl_company_by_city',
        ratio_column='salary_ratio_to_market_by_city',
    )
    feature_data = add_salary_group_features(
        data=feature_data,
        group_columns=['profile'],
        company_median_column='company_salary_median_by_profile',
        market_median_column='market_salary_median_excl_company_by_profile',
        ratio_column='salary_ratio_to_market_by_profile',
    )
    feature_data = add_salary_group_features(
        data=feature_data,
        group_columns=['city', 'profile'],
        company_median_column='company_salary_median_by_city_profile',
        market_median_column=(
            'market_salary_median_excl_company_by_city_profile'
        ),
        ratio_column='salary_ratio_to_market_by_city_profile',
    )

    return feature_data


def build_salary_feature_rows(
    data: pd.DataFrame,
    feature_run_id: int,
) -> list[dict[str, int | float | bool | pd.Timestamp]]:
    """Build salary feature rows for persistence.
    Args:
        data (pd.DataFrame): Input snapshot dataframe.
        feature_run_id (int): Feature run identifier.
    """
    feature_data = build_salary_feature_dataframe(data=data)

    if feature_data.empty:
        return []

    rows = []

    for _, row in feature_data.iterrows():
        rows.append(
            {
                'feature_run_id': feature_run_id,
                'client_id': int(row['client_id']),
                'company_id': int(row['company_id']),
                'vacancy_id': int(row['vacancy_id']),
                'date_day': row['date_day'],
                'salary_mid': float(row['salary_mid']),
                'salary_is_specified': bool(row['salary_is_specified']),
                'company_salary_median_by_city': float(
                    row['company_salary_median_by_city'],
                ),
                'market_salary_median_excl_company_by_city': float(
                    row['market_salary_median_excl_company_by_city'],
                ),
                'salary_ratio_to_market_by_city': float(
                    row['salary_ratio_to_market_by_city'],
                ),
                'company_salary_median_by_profile': float(
                    row['company_salary_median_by_profile'],
                ),
                'market_salary_median_excl_company_by_profile': float(
                    row['market_salary_median_excl_company_by_profile'],
                ),
                'salary_ratio_to_market_by_profile': float(
                    row['salary_ratio_to_market_by_profile'],
                ),
                'company_salary_median_by_city_profile': float(
                    row['company_salary_median_by_city_profile'],
                ),
                'market_salary_median_excl_company_by_city_profile': float(
                    row[
                        'market_salary_median_excl_company_by_city_profile'
                    ],
                ),
                'salary_ratio_to_market_by_city_profile': float(
                    row['salary_ratio_to_market_by_city_profile'],
                ),
            },
        )

    return rows
