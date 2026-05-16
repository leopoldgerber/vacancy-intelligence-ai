from pathlib import Path

from catboost import CatBoostRegressor


MODEL_ARTIFACT_DIR = Path('artifacts/models/pipeline_3')
CATBOOST_MODEL_EXTENSION = '.cbm'


def build_model_artifact_path(training_run_name: str) -> Path:
    """Build model artifact path.

    Args:
        training_run_name (str): Training run name.
    """
    model_filename = f'{training_run_name}{CATBOOST_MODEL_EXTENSION}'
    return MODEL_ARTIFACT_DIR / model_filename


def save_catboost_model(
    model: CatBoostRegressor,
    training_run_name: str,
) -> str:
    """Save CatBoost model artifact.
    Args:
        model (CatBoostRegressor): Trained CatBoost model.
        training_run_name (str): Training run name."""
    MODEL_ARTIFACT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    model_path = build_model_artifact_path(
        training_run_name=training_run_name,
    )

    model.save_model(str(model_path))

    return str(model_path)
