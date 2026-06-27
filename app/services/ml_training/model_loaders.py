from pathlib import Path

from catboost import CatBoostRegressor

from app.services.ml_training.artifact_savers import CATBOOST_MODEL_EXTENSION


def validate_model_path(model_path: str | Path) -> Path:
    """Validate CatBoost model artifact path.
    Args:
        model_path (str | Path): Model artifact path."""
    resolved_path = Path(model_path)

    if not resolved_path.exists():
        raise FileNotFoundError(
            f'CatBoost model artifact was not found: {resolved_path}',
        )

    if not resolved_path.is_file():
        raise ValueError(
            f'CatBoost model artifact path is not a file: {resolved_path}',
        )

    if resolved_path.suffix != CATBOOST_MODEL_EXTENSION:
        raise ValueError(
            'CatBoost model artifact must have '
            f'{CATBOOST_MODEL_EXTENSION} extension: {resolved_path}',
        )

    return resolved_path


def load_catboost_model(model_path: str | Path) -> CatBoostRegressor:
    """Load CatBoost model artifact.
    Args:
        model_path (str | Path): Model artifact path."""
    resolved_path = validate_model_path(model_path=model_path)
    model = CatBoostRegressor()
    model.load_model(str(resolved_path))

    return model
