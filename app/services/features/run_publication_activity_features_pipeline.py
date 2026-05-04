from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.features.constants import FEATURE_STATUS_NO_DATA
from app.services.features.constants import FEATURE_STATUS_SUCCESS
from app.services.features.data_loaders import load_feature_snapshot_data
from app.services.features.name_builders import build_feature_report_name
from app.services.features.name_builders import build_feature_run_name
from app.services.features.persistence import save_feature_run
from app.services.features.persistence import (
    save_publication_activity_features,
)
from app.services.features.publication_activity_feature_builders import (
    build_publication_activity_feature_rows,
)


async def run_publication_activity_features_pipeline(
    session: AsyncSession,
    client_id: int,
    date_from: datetime,
    date_to: datetime,
) -> dict[str, int | str | bool]:
    """Run publication activity feature engineering pipeline.
    Args:
        session (AsyncSession): Database session.
        client_id (int): Client identifier.
        date_from (datetime): Feature period start.
        date_to (datetime): Feature period end.
    """
    feature_run_name = build_feature_run_name()
    report_name = build_feature_report_name(
        feature_run_name=feature_run_name,
    )
    snapshot_data = await load_feature_snapshot_data(
        session=session,
        client_id=client_id,
        date_from=date_from,
        date_to=date_to,
    )
    snapshot_count = len(snapshot_data)

    if snapshot_data.empty:
        feature_run = await save_feature_run(
            session=session,
            feature_run_name=feature_run_name,
            client_id=client_id,
            date_from=date_from,
            date_to=date_to,
            status=FEATURE_STATUS_NO_DATA,
            is_success=False,
            snapshot_count=snapshot_count,
            feature_count=0,
            report_name=report_name,
        )

        return {
            'feature_run_id': feature_run.id,
            'feature_run_name': feature_run.feature_run_name,
            'status': feature_run.status,
            'is_success': feature_run.is_success,
            'snapshot_count': feature_run.snapshot_count,
            'feature_count': feature_run.feature_count,
            'report_name': feature_run.report_name,
        }

    feature_run = await save_feature_run(
        session=session,
        feature_run_name=feature_run_name,
        client_id=client_id,
        date_from=date_from,
        date_to=date_to,
        status=FEATURE_STATUS_SUCCESS,
        is_success=True,
        snapshot_count=snapshot_count,
        feature_count=0,
        report_name=report_name,
    )

    publication_activity_feature_rows = (
        build_publication_activity_feature_rows(
            data=snapshot_data,
            feature_run_id=feature_run.id,
        )
    )
    publication_activity_features = (
        await save_publication_activity_features(
            session=session,
            publication_activity_feature_rows=(
                publication_activity_feature_rows
            ),
        )
    )

    feature_run.feature_count = len(publication_activity_features)
    await session.flush()

    return {
        'feature_run_id': feature_run.id,
        'feature_run_name': feature_run.feature_run_name,
        'status': feature_run.status,
        'is_success': feature_run.is_success,
        'snapshot_count': feature_run.snapshot_count,
        'feature_count': feature_run.feature_count,
        'report_name': feature_run.report_name,
    }
