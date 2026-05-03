from importlib import import_module


def load_models() -> None:
    """Load SQLAlchemy models for metadata registration.
    Args:
        """
    model_modules = [
        'app.db.models.client',
        'app.db.models.company',
        'app.db.models.vacancy',
        'app.db.models.vacancy_snapshot',
        'app.db.models.validation_run',
        'app.db.models.validation_issue',
        'app.db.models.quality_run',
        'app.db.models.quality_issue',
        'app.db.models.analytics_run',
        'app.db.models.market_summary',
        'app.db.models.client_summary',
        'app.db.models.competitor_summary',
    ]

    for module_path in model_modules:
        import_module(module_path)
