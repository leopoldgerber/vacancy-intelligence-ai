import numpy as np
from catboost import CatBoostRegressor

from app.services.ml_training.constants import RANDOM_SEED
from app.services.ml_training.dataset_builders import TrainingDataset
from app.services.ml_training.metric_builders import calculate_training_metrics
from app.services.ml_training.split_builders import TrainingSplit


def build_catboost_model() -> CatBoostRegressor:
    """Build CatBoost regressor model.
    Args:
        """
    return CatBoostRegressor(
        iterations=100,
        learning_rate=0.05,
        depth=6,
        loss_function='RMSE',
        random_seed=RANDOM_SEED,
        verbose=False,
        allow_writing_files=False,
    )


def train_catboost_model(
    model: CatBoostRegressor,
    dataset: TrainingDataset,
    split: TrainingSplit,
) -> CatBoostRegressor:
    """Train CatBoost regressor model.
    Args:
        model (CatBoostRegressor): CatBoost model instance.
        dataset (TrainingDataset): Prepared training dataset.
        split (TrainingSplit): Prepared train/test split."""
    model.fit(
        split.train_features,
        split.train_target,
        cat_features=dataset.categorical_feature_indices,
    )

    return model


def predict_model(
    model: CatBoostRegressor,
    split: TrainingSplit,
) -> np.ndarray:
    """Predict target values with trained model.
    Args:
        model (CatBoostRegressor): Trained CatBoost model.
        split (TrainingSplit): Prepared train/test split."""
    predictions = model.predict(split.test_features)

    return np.asarray(predictions)


def train_and_evaluate_catboost(
    dataset: TrainingDataset,
    split: TrainingSplit,
) -> dict[str, object]:
    """Train and evaluate CatBoost regressor.
    Args:
        dataset (TrainingDataset): Prepared training dataset.
        split (TrainingSplit): Prepared train/test split."""
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
    metrics = calculate_training_metrics(
        train_target=split.train_target,
        test_target=split.test_target,
        predictions=predictions,
    )

    return {
        'model': trained_model,
        'predictions': predictions,
        'metrics': metrics,
    }
