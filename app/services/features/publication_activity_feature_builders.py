from datetime import datetime

import pandas as pd


def calculate_publication_activity_level(
    standard: int | None,
    standard_plus: int | None,
    premium: int | None,
) -> int:
    """Calculate publication activity level.
    Args:
        standard (int | None): Standard publication flag.
        standard_plus (int | None): Standard Plus publication flag.
        premium (int | None): Premium publication flag.
    """
    if premium == 1:
        return 3

    if standard_plus == 1:
        return 2

    if standard == 1:
        return 1

    return 0


def add_publication_activity_level(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """Add publication activity level.
    Args:
        data (pd.DataFrame): Input snapshot dataframe.
    """
    feature_data = data.copy()

    feature_data['publication_activity_level'] = feature_data.apply(
        lambda row: calculate_publication_activity_level(
            standard=row['standard'],
            standard_plus=row['standard_plus'],
            premium=row['premium'],
        ),
        axis=1,
    )

    return feature_data


def add_days_since_last_publication_activity(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """Add days since last publication activity.
    Args:
        data (pd.DataFrame): Input dataframe with publication activity level.
    """
    feature_data = data.copy()
    feature_data = feature_data.sort_values(
        by=[
            'client_id',
            'company_id',
            'vacancy_id',
            'date_day',
        ],
    )

    feature_data['days_since_last_publication_activity'] = -1

    group_columns = [
        'client_id',
        'company_id',
        'vacancy_id',
    ]

    for _, group_index in feature_data.groupby(group_columns).groups.items():
        last_activity_date: datetime | None = None

        for row_index in group_index:
            row = feature_data.loc[row_index]
            current_date = row['date_day']
            activity_level = int(row['publication_activity_level'])

            if activity_level > 0:
                feature_data.loc[
                    row_index,
                    'days_since_last_publication_activity',
                ] = 0
                last_activity_date = current_date
                continue

            if last_activity_date is None:
                feature_data.loc[
                    row_index,
                    'days_since_last_publication_activity',
                ] = -1
                continue

            days_since = (current_date - last_activity_date).days
            feature_data.loc[
                row_index,
                'days_since_last_publication_activity',
            ] = int(days_since)

    return feature_data


def build_publication_activity_feature_dataframe(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """Build publication activity feature dataframe.
    Args:
        data (pd.DataFrame): Input snapshot dataframe.
    """
    if data.empty:
        return pd.DataFrame()

    feature_data = add_publication_activity_level(data=data)
    feature_data = add_days_since_last_publication_activity(
        data=feature_data,
    )

    return feature_data


def build_publication_activity_feature_rows(
    data: pd.DataFrame,
    feature_run_id: int,
) -> list[dict[str, int | datetime]]:
    """Build publication activity feature rows for persistence.
    Args:
        data (pd.DataFrame): Input snapshot dataframe.
        feature_run_id (int): Feature run identifier.
    """
    feature_data = build_publication_activity_feature_dataframe(data=data)

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
                'publication_activity_level': int(
                    row['publication_activity_level'],
                ),
                'days_since_last_publication_activity': int(
                    row['days_since_last_publication_activity'],
                ),
            },
        )

    return rows
