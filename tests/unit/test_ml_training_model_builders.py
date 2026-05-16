import numpy as np
import pandas as pd
from catboost import CatBoostRegressor

from app.services.ml_training.dataset_builders import build_dataset
from app.services.ml_training.feature_schema import get_training_columns
from app.services.ml_training.model_builders import build_catboost_model
from app.services.ml_training.model_builders import predict_model
from app.services.ml_training.model_builders import train_and_evaluate_catboost
from app.services.ml_training.model_builders import train_catboost_model
from app.services.ml_training.split_builders import build_training_split


def build_model_training_dataframe(row_count: int = 40) -> pd.DataFrame:
    """Build dataframe for model training tests.
    Args:
        row_count (int): Number of rows."""
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


def test_build_catboost_model() -> None:
    """Test CatBoost model builder.
    Args:
        """
    model = build_catboost_model()

    assert isinstance(model, CatBoostRegressor)


def test_train_catboost_model() -> None:
    """Test CatBoost model training.
    Args:
        """
    data = build_model_training_dataframe()
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

    assert isinstance(trained_model, CatBoostRegressor)
    assert trained_model.is_fitted()


def test_predict_model() -> None:
    """Test CatBoost model prediction.
    Args:
        """
    data = build_model_training_dataframe()
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

    predictions = predict_model(
        model=trained_model,
        split=split,
    )

    assert isinstance(predictions, np.ndarray)
    assert len(predictions) == split.test_row_count


def test_train_and_evaluate_catboost() -> None:
    """Test CatBoost training and evaluation.
    Args:
        """
    data = build_model_training_dataframe()
    dataset = build_dataset(data=data)
    split = build_training_split(
        source_data=data,
        dataset=dataset,
    )

    result = train_and_evaluate_catboost(
        dataset=dataset,
        split=split,
    )

    assert isinstance(result['model'], CatBoostRegressor)
    assert isinstance(result['predictions'], np.ndarray)
    assert isinstance(result['metrics'], dict)

    metrics = result['metrics']

    assert 'metric_mae' in metrics
    assert 'metric_rmse' in metrics
    assert 'metric_r2' in metrics
    assert 'baseline_mae' in metrics
    assert 'mean_target' in metrics
    assert isinstance(metrics['metric_mae'], float)
    assert isinstance(metrics['metric_rmse'], float)
    assert isinstance(metrics['metric_r2'], float)
    assert isinstance(metrics['baseline_mae'], float)
    assert isinstance(metrics['mean_target'], float)
