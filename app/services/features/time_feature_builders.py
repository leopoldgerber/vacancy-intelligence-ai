from datetime import datetime

import pandas as pd


def calculate_publication_hour(
    publication_date: datetime | None,
) -> int:
    """Calculate publication hour.
    Args:
        publication_date (datetime | None): Publication datetime.
    """
    if pd.isna(publication_date):
        return -1

    return int(publication_date.hour)


def calculate_publication_day_of_week(
    publication_date: datetime | None,
) -> int:
    """Calculate publication day of week.
    Args:
        publication_date (datetime | None): Publication datetime.
    """
    if pd.isna(publication_date):
        return -1

    return int(publication_date.weekday())


def calculate_publication_month(
    publication_date: datetime | None,
) -> int:
    """Calculate publication month.
    Args:
        publication_date (datetime | None): Publication datetime.
    """
    if pd.isna(publication_date):
        return -1

    return int(publication_date.month)


def calculate_publication_week(
    publication_date: datetime | None,
) -> int:
    """Calculate publication ISO week.
    Args:
        publication_date (datetime | None): Publication datetime.
    """
    if pd.isna(publication_date):
        return -1

    return int(publication_date.isocalendar().week)


def calculate_is_weekend(
    publication_date: datetime | None,
) -> bool:
    """Calculate weekend flag.
    Args:
        publication_date (datetime | None): Publication datetime.
    """
    if pd.isna(publication_date):
        return False

    return publication_date.weekday() in [5, 6]


def calculate_vacancy_age_days(
    date_day: datetime | None,
    publication_date: datetime | None,
) -> int:
    """Calculate vacancy age in days.
    Args:
        date_day (datetime | None): Snapshot date.
        publication_date (datetime | None): Publication datetime.
    """
    if pd.isna(date_day) or pd.isna(publication_date):
        return -1

    age_days = (date_day.date() - publication_date.date()).days

    if age_days < 0:
        return 0

    return int(age_days)


def build_time_feature_dataframe(data: pd.DataFrame) -> pd.DataFrame:
    """Build time feature dataframe.
    Args:
        data (pd.DataFrame): Input snapshot dataframe.
    """
    if data.empty:
        return pd.DataFrame()

    feature_data = data.copy()

    feature_data['publication_hour'] = feature_data[
        'publication_date'
    ].apply(calculate_publication_hour)
    feature_data['publication_day_of_week'] = feature_data[
        'publication_date'
    ].apply(calculate_publication_day_of_week)
    feature_data['publication_month'] = feature_data[
        'publication_date'
    ].apply(calculate_publication_month)
    feature_data['publication_week'] = feature_data[
        'publication_date'
    ].apply(calculate_publication_week)
    feature_data['is_weekend'] = feature_data[
        'publication_date'
    ].apply(calculate_is_weekend)

    feature_data['vacancy_age_days'] = feature_data.apply(
        lambda row: calculate_vacancy_age_days(
            date_day=row['date_day'],
            publication_date=row['publication_date'],
        ),
        axis=1,
    )

    return feature_data


def build_time_feature_rows(
    data: pd.DataFrame,
    feature_run_id: int,
) -> list[dict[str, int | bool | datetime]]:
    """Build time feature rows for persistence.
    Args:
        data (pd.DataFrame): Input snapshot dataframe.
        feature_run_id (int): Feature run identifier.
    """
    feature_data = build_time_feature_dataframe(data=data)

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
                'publication_hour': int(row['publication_hour']),
                'publication_day_of_week': int(
                    row['publication_day_of_week'],
                ),
                'publication_month': int(row['publication_month']),
                'publication_week': int(row['publication_week']),
                'is_weekend': bool(row['is_weekend']),
                'vacancy_age_days': int(row['vacancy_age_days']),
            },
        )

    return rows
