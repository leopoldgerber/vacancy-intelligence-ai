from app.services.ml_training.constants import RANDOM_SEED


CATBOOST_BASELINE_PARAMS = {
    'iterations': 100,
    'learning_rate': 0.05,
    'depth': 6,
    'loss_function': 'RMSE',
    'random_seed': RANDOM_SEED,
    'verbose': False,
    'allow_writing_files': False,
}


def get_catboost_baseline_params() -> dict[str, int | float | str | bool]:
    """Get CatBoost baseline model parameters.
    Args:
        """
    return CATBOOST_BASELINE_PARAMS.copy()
