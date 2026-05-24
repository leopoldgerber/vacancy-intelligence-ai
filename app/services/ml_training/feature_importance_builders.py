from catboost import CatBoostRegressor

from app.services.ml_training.dataset_builders import TrainingDataset


def build_feature_importance_json(
    model: CatBoostRegressor,
    dataset: TrainingDataset,
) -> dict[str, float]:
    """Build feature importance json.
    Args:
        model (CatBoostRegressor): Trained CatBoost model.
        dataset (TrainingDataset): Prepared training dataset.
    """
    importance_values = model.get_feature_importance()

    feature_importance = {
        feature_name: float(importance_value)
        for feature_name, importance_value in zip(
            dataset.feature_columns,
            importance_values,
            strict=True,
        )
    }

    return dict(
        sorted(
            feature_importance.items(),
            key=lambda item: item[1],
            reverse=True,
        ),
    )
