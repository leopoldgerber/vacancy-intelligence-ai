import pandas as pd

from app.services.ml_training.dataset_builders import build_dataset
from app.services.ml_training.feature_importance_builders import (
    build_feature_importance_json,
)
from app.services.ml_training.feature_schema import get_feature_columns
from app.services.ml_training.feature_schema import get_training_columns
from app.services.ml_training.model_builders import build_catboost_model
from app.services.ml_training.model_builders import train_catboost_model
from app.services.ml_training.split_builders import build_training_split


def build_feature_importance_dataframe(row_count: int = 40) -> pd.DataFrame:
    """Build dataframe for feature importance tests.
    Args:
        row_count (int): Number of rows.
    """
    rows = []
    base_date = pd.Timestamp('2025-08-01')

    for index in range(row_count):
        city = 'Berlin' if index % 2 == 0 else 'Hamburg'
        profile = 'Filialleiter' if index % 3 == 0 else 'Verkäufer'

        row = {
            'client_id': 1,
            'company_id': index % 3 + 1,
            'vacancy_id': 1000 + index,
            'date_day': base_date + pd.Timedelta(days=index % 8),
            'callbacks': float((index % 10) + 5),
            'salary_mid': 1000 + index * 10,
            'salary_is_specified': index % 2 == 0,
            'salary_ratio_to_market_by_city': 1.0 + (index % 3) * 0.05,
            'salary_ratio_to_market_by_profile': 0.95 + (index % 4) * 0.03,
            'salary_ratio_to_market_by_city_profile': (
                1.05 + (index % 5) * 0.02
            ),
            'publication_activity_level': index % 4,
            'days_since_last_publication_activity': index % 5,
            'title_length': 20 + index,
            'description_length': 100 + index * 2,
            'title_word_count': 2 + index % 4,
            'description_word_count': 15 + index % 8,
            'has_description': True,
            'description_is_empty': False,
            'has_salary_mention': index % 2 == 0,
            'has_schedule_mention': True,
            'has_requirements_mention': index % 3 == 0,
            'has_benefits_mention': index % 2 == 1,
            'has_call_to_action': True,
            'publication_hour': 8 + index % 10,
            'publication_day_of_week': index % 7,
            'publication_month': 8,
            'publication_week': 31 + index % 2,
            'is_weekend': index % 7 in [5, 6],
            'vacancy_age_days': index,
            'city': city,
            'region': city,
            'profile': profile,
            'employment_type': 'Full-time',
            'work_experience': '1 year',
            'work_schedule': 'Full-time',
        }
        rows.append(row)

    return pd.DataFrame(
        rows,
        columns=get_training_columns(),
    )


def test_build_feature_importance_json() -> None:
    """Test feature importance json builder.
    Args:
        """
    data = build_feature_importance_dataframe()
    dataset = build_dataset(data=data)
    split = build_training_split(
        source_data=data,
        dataset=dataset,
    )
    model = build_catboost_model()
    trained_model = train_catboost_model(
        model=model,
        dataset=dataset,
        split=split,
    )

    result = build_feature_importance_json(
        model=trained_model,
        dataset=dataset,
    )

    assert isinstance(result, dict)
    assert list(result.keys()) == sorted(
        result,
        key=result.get,
        reverse=True,
    )
    assert set(result.keys()) == set(get_feature_columns())

    for value in result.values():
        assert isinstance(value, float)
        assert value >= 0
