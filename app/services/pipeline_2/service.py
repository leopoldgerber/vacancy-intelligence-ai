from datetime import datetime

from app.services.analytics.service import run_analytics
from app.services.features.service import run_categorical_features
from app.services.features.service import run_publication_activity_features
from app.services.features.service import run_salary_features
from app.services.features.service import run_text_features
from app.services.features.service import run_time_features
from app.services.ml_dataset.service import run_ml_dataset


async def run_pipeline_2_full(
    client_id: int,
    date_from: datetime,
    date_to: datetime,
) -> dict:
    """Run full Pipeline 2 flow.
    Args:
        client_id (int): Client identifier.
        date_from (datetime): Pipeline period start.
        date_to (datetime): Pipeline period end.
    """
    summary_result = await run_analytics(
        client_id=client_id,
        date_from=date_from,
        date_to=date_to,
        city=None,
        profile=None,
    )

    salary_features_result = await run_salary_features(
        client_id=client_id,
        date_from=date_from,
        date_to=date_to,
    )

    publication_activity_features_result = (
        await run_publication_activity_features(
            client_id=client_id,
            date_from=date_from,
            date_to=date_to,
        )
    )

    text_features_result = await run_text_features(
        client_id=client_id,
        date_from=date_from,
        date_to=date_to,
    )

    time_features_result = await run_time_features(
        client_id=client_id,
        date_from=date_from,
        date_to=date_to,
    )

    categorical_features_result = await run_categorical_features(
        client_id=client_id,
        date_from=date_from,
        date_to=date_to,
    )

    ml_dataset_result = await run_ml_dataset(
        client_id=client_id,
        date_from=date_from,
        date_to=date_to,
    )

    is_success = all(
        [
            bool(summary_result['is_success']),
            bool(salary_features_result['is_success']),
            bool(publication_activity_features_result['is_success']),
            bool(text_features_result['is_success']),
            bool(time_features_result['is_success']),
            bool(categorical_features_result['is_success']),
            bool(ml_dataset_result['is_success']),
        ],
    )

    status = 'success' if is_success else 'partial_or_no_data'

    return {
        'status': status,
        'is_success': is_success,
        'summary': summary_result,
        'salary_features': salary_features_result,
        'publication_activity_features': (
            publication_activity_features_result
        ),
        'text_features': text_features_result,
        'time_features': time_features_result,
        'categorical_features': categorical_features_result,
        'ml_dataset': ml_dataset_result,
    }
