from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.ml_dataset.constants import ML_DATASET_STATUS_NO_DATA
from app.services.ml_dataset.constants import ML_DATASET_STATUS_SUCCESS
from app.services.ml_dataset.data_loaders import (
    load_categorical_feature_data,
)
from app.services.ml_dataset.data_loaders import (
    load_latest_successful_feature_run,
)
from app.services.ml_dataset.data_loaders import (
    load_publication_activity_feature_data,
)
from app.services.ml_dataset.data_loaders import load_salary_feature_data
from app.services.ml_dataset.data_loaders import load_target_snapshot_data
from app.services.ml_dataset.data_loaders import load_text_feature_data
from app.services.ml_dataset.data_loaders import load_time_feature_data
from app.services.ml_dataset.dataset_builders import build_ml_feature_rows
from app.services.ml_dataset.dataset_builders import join_feature_dataframes
from app.services.ml_dataset.name_builders import build_ml_dataset_report_name
from app.services.ml_dataset.name_builders import build_ml_dataset_run_name
from app.services.ml_dataset.persistence import save_ml_dataset_run
from app.services.ml_dataset.persistence import save_ml_feature_rows


async def run_ml_dataset_pipeline(
    session: AsyncSession,
    client_id: int,
    date_from: datetime,
    date_to: datetime,
) -> dict[str, int | str | bool]:
    """Run final ML dataset pipeline.
    Args:
        session (AsyncSession): Database session.
        client_id (int): Client identifier.
        date_from (datetime): Dataset period start.
        date_to (datetime): Dataset period end.
    """
    dataset_run_name = build_ml_dataset_run_name()
    report_name = build_ml_dataset_report_name(
        dataset_run_name=dataset_run_name,
    )

    salary_feature_run = await load_latest_successful_feature_run(
        session=session,
        client_id=client_id,
        date_from=date_from,
        date_to=date_to,
        feature_name_prefix='salary_features',
    )
    publication_activity_feature_run = (
        await load_latest_successful_feature_run(
            session=session,
            client_id=client_id,
            date_from=date_from,
            date_to=date_to,
            feature_name_prefix='publication_activity_features',
        )
    )
    text_feature_run = await load_latest_successful_feature_run(
        session=session,
        client_id=client_id,
        date_from=date_from,
        date_to=date_to,
        feature_name_prefix='text_features',
    )
    time_feature_run = await load_latest_successful_feature_run(
        session=session,
        client_id=client_id,
        date_from=date_from,
        date_to=date_to,
        feature_name_prefix='time_features',
    )
    categorical_feature_run = await load_latest_successful_feature_run(
        session=session,
        client_id=client_id,
        date_from=date_from,
        date_to=date_to,
        feature_name_prefix='categorical_features',
    )

    feature_runs = [
        salary_feature_run,
        publication_activity_feature_run,
        text_feature_run,
        time_feature_run,
        categorical_feature_run,
    ]

    if any(feature_run is None for feature_run in feature_runs):
        ml_dataset_run = await save_ml_dataset_run(
            session=session,
            dataset_run_name=dataset_run_name,
            client_id=client_id,
            date_from=date_from,
            date_to=date_to,
            salary_feature_run_id=(
                salary_feature_run.id if salary_feature_run else None
            ),
            publication_activity_feature_run_id=(
                publication_activity_feature_run.id
                if publication_activity_feature_run
                else None
            ),
            text_feature_run_id=(
                text_feature_run.id if text_feature_run else None
            ),
            time_feature_run_id=(
                time_feature_run.id if time_feature_run else None
            ),
            categorical_feature_run_id=(
                categorical_feature_run.id
                if categorical_feature_run
                else None
            ),
            status=ML_DATASET_STATUS_NO_DATA,
            is_success=False,
            row_count=0,
            report_name=report_name,
        )

        return {
            'ml_dataset_run_id': ml_dataset_run.id,
            'dataset_run_name': ml_dataset_run.dataset_run_name,
            'status': ml_dataset_run.status,
            'is_success': ml_dataset_run.is_success,
            'row_count': ml_dataset_run.row_count,
            'report_name': ml_dataset_run.report_name,
        }

    target_data = await load_target_snapshot_data(
        session=session,
        client_id=client_id,
        date_from=date_from,
        date_to=date_to,
    )
    salary_data = await load_salary_feature_data(
        session=session,
        feature_run_id=salary_feature_run.id,
    )
    publication_activity_data = await load_publication_activity_feature_data(
        session=session,
        feature_run_id=publication_activity_feature_run.id,
    )
    text_data = await load_text_feature_data(
        session=session,
        feature_run_id=text_feature_run.id,
    )
    time_data = await load_time_feature_data(
        session=session,
        feature_run_id=time_feature_run.id,
    )
    categorical_data = await load_categorical_feature_data(
        session=session,
        feature_run_id=categorical_feature_run.id,
    )

    dataset = join_feature_dataframes(
        target_data=target_data,
        salary_data=salary_data,
        publication_activity_data=publication_activity_data,
        text_data=text_data,
        time_data=time_data,
        categorical_data=categorical_data,
    )
    # row_count = len(dataset)

    if dataset.empty:
        ml_dataset_run = await save_ml_dataset_run(
            session=session,
            dataset_run_name=dataset_run_name,
            client_id=client_id,
            date_from=date_from,
            date_to=date_to,
            salary_feature_run_id=salary_feature_run.id,
            publication_activity_feature_run_id=(
                publication_activity_feature_run.id
            ),
            text_feature_run_id=text_feature_run.id,
            time_feature_run_id=time_feature_run.id,
            categorical_feature_run_id=categorical_feature_run.id,
            status=ML_DATASET_STATUS_NO_DATA,
            is_success=False,
            row_count=0,
            report_name=report_name,
        )

        return {
            'ml_dataset_run_id': ml_dataset_run.id,
            'dataset_run_name': ml_dataset_run.dataset_run_name,
            'status': ml_dataset_run.status,
            'is_success': ml_dataset_run.is_success,
            'row_count': ml_dataset_run.row_count,
            'report_name': ml_dataset_run.report_name,
        }

    ml_dataset_run = await save_ml_dataset_run(
        session=session,
        dataset_run_name=dataset_run_name,
        client_id=client_id,
        date_from=date_from,
        date_to=date_to,
        salary_feature_run_id=salary_feature_run.id,
        publication_activity_feature_run_id=(
            publication_activity_feature_run.id
        ),
        text_feature_run_id=text_feature_run.id,
        time_feature_run_id=time_feature_run.id,
        categorical_feature_run_id=categorical_feature_run.id,
        status=ML_DATASET_STATUS_SUCCESS,
        is_success=True,
        row_count=0,
        report_name=report_name,
    )

    ml_feature_rows = build_ml_feature_rows(
        dataset=dataset,
        ml_dataset_run_id=ml_dataset_run.id,
    )
    saved_rows = await save_ml_feature_rows(
        session=session,
        ml_feature_rows=ml_feature_rows,
    )

    ml_dataset_run.row_count = len(saved_rows)
    await session.flush()

    return {
        'ml_dataset_run_id': ml_dataset_run.id,
        'dataset_run_name': ml_dataset_run.dataset_run_name,
        'status': ml_dataset_run.status,
        'is_success': ml_dataset_run.is_success,
        'row_count': ml_dataset_run.row_count,
        'report_name': ml_dataset_run.report_name,
    }
