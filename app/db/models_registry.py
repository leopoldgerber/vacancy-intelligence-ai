from importlib import import_module


def load_models() -> None:
    """Load SQLAlchemy models for metadata registration.
    Args:
        """
    model_modules = [
        'app.db.models.client',
        'app.db.models.validation_run',
        'app.db.models.validation_issue',
        'app.db.models.quality_run',
        'app.db.models.quality_issue',
    ]

    for module_path in model_modules:
        import_module(module_path)
