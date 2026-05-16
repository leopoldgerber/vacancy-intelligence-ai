IDENTIFIER_COLUMNS = [
    'client_id',
    'company_id',
    'vacancy_id',
    'date_day',
]

TARGET_COLUMN = 'callbacks'

NUMERICAL_FEATURE_COLUMNS = [
    'salary_mid',
    'salary_is_specified',
    'salary_ratio_to_market_by_city',
    'salary_ratio_to_market_by_profile',
    'salary_ratio_to_market_by_city_profile',
    'publication_activity_level',
    'days_since_last_publication_activity',
    'title_length',
    'description_length',
    'title_word_count',
    'description_word_count',
    'has_description',
    'description_is_empty',
    'has_salary_mention',
    'has_schedule_mention',
    'has_requirements_mention',
    'has_benefits_mention',
    'has_call_to_action',
    'publication_hour',
    'publication_day_of_week',
    'publication_month',
    'publication_week',
    'is_weekend',
    'vacancy_age_days',
]

CATEGORICAL_FEATURE_COLUMNS = [
    'city',
    'region',
    'profile',
    'employment_type',
    'work_experience',
    'work_schedule',
]


def get_feature_columns() -> list[str]:
    """Get model feature columns.
    Args:
        """
    return NUMERICAL_FEATURE_COLUMNS + CATEGORICAL_FEATURE_COLUMNS


def get_training_columns() -> list[str]:
    """Get all columns needed for model training.
    Args:
        """
    return IDENTIFIER_COLUMNS + get_feature_columns() + [TARGET_COLUMN]


def get_missing_columns(columns: list[str]) -> list[str]:
    """Get missing training columns.
    Args:
        columns (list[str]): Existing dataframe columns."""
    required_columns = get_training_columns()

    return [
        column
        for column in required_columns
        if column not in columns
    ]


def get_categorical_feature_indices() -> list[int]:
    """Get categorical feature indices for CatBoost.
    Args:
        """
    feature_columns = get_feature_columns()

    return [
        feature_columns.index(column)
        for column in CATEGORICAL_FEATURE_COLUMNS
    ]
