from sqlalchemy.ext.asyncio import AsyncSession

from app.services.ml_training.artifact_savers import save_catboost_model
from app.services.ml_training.constants import MIN_TRAINING_ROW_COUNT
from app.services.ml_training.constants import ML_MODEL_TYPE_CATBOOST_REGRESSOR
from app.services.ml_training.constants import ML_TARGET_CALLBACKS
from app.services.ml_training.constants import ML_TRAINING_STATUS_FAILED
from app.services.ml_training.constants import ML_TRAINING_STATUS_NO_DATA
from app.services.ml_training.constants import ML_TRAINING_STATUS_SUCCESS
from app.services.ml_training.data_loaders import load_ml_training_dataframe
from app.services.ml_training.data_loaders import resolve_ml_dataset_run
from app.services.ml_training.dataset_builders import build_dataset
from app.services.ml_training.model_builders import train_and_evaluate_catboost
from app.services.ml_training.name_builders import (
    build_ml_training_report_name)
from app.services.ml_training.name_builders import build_ml_training_run_name
from app.services.ml_training.persistence import save_ml_training_run
from app.services.ml_training.split_builders import build_training_split


def build_training_result(
    ml_training_run_id: int,
    training_run_name: str,
    status: str,
    is_success: bool,
    model_type: str,
    target_name: str,
    train_row_count: int,
    test_row_count: int,
    metric_mae: float | None,
    metric_rmse: float | None,
    metric_r2: float | None,
    model_path: str | None,
    report_name: str | None,
) -> dict[str, int | str | bool | float | None]:
    """Build ML training result response.
    Args:
        ml_training_run_id (int): ML training run identifier.
        training_run_name (str): ML training run name.
        status (str): Training status.
        is_success (bool): Whether training was successful.
        model_type (str): Model type.
        target_name (str): Target name.
        train_row_count (int): Number of train rows.
        test_row_count (int): Number of test rows.
        metric_mae (float | None): MAE metric.
        metric_rmse (float | None): RMSE metric.
        metric_r2 (float | None): R2 metric.
        model_path (str | None): Saved model path.
        report_name (str | None): Training report name.
    """
    return {
        'ml_training_run_id': ml_training_run_id,
        'training_run_name': training_run_name,
        'status': status,
        'is_success': is_success,
        'model_type': model_type,
        'target_name': target_name,
        'train_row_count': train_row_count,
        'test_row_count': test_row_count,
        'metric_mae': metric_mae,
        'metric_rmse': metric_rmse,
        'metric_r2': metric_r2,
        'model_path': model_path,
        'report_name': report_name,
    }


async def save_no_data_training_run(
    session: AsyncSession,
    training_run_name: str,
    ml_dataset_run_id: int | None,
    client_id: int,
    report_name: str,
) -> dict[str, int | str | bool | float | None]:
    """Save no-data ML training run.
    Args:
        session (AsyncSession): Database session.
        training_run_name (str): ML training run name.
        ml_dataset_run_id (int | None): ML dataset run identifier.
        client_id (int): Client identifier.
        report_name (str): Training report name.
    """
    ml_training_run = await save_ml_training_run(
        session=session,
        training_run_name=training_run_name,
        ml_dataset_run_id=ml_dataset_run_id,
        client_id=client_id,
        model_type=ML_MODEL_TYPE_CATBOOST_REGRESSOR,
        target_name=ML_TARGET_CALLBACKS,
        status=ML_TRAINING_STATUS_NO_DATA,
        is_success=False,
        train_row_count=0,
        test_row_count=0,
        metric_mae=None,
        metric_rmse=None,
        metric_r2=None,
        model_path=None,
        report_name=report_name,
    )

    return build_training_result(
        ml_training_run_id=ml_training_run.id,
        training_run_name=ml_training_run.training_run_name,
        status=ml_training_run.status,
        is_success=ml_training_run.is_success,
        model_type=ml_training_run.model_type,
        target_name=ml_training_run.target_name,
        train_row_count=ml_training_run.train_row_count,
        test_row_count=ml_training_run.test_row_count,
        metric_mae=ml_training_run.metric_mae,
        metric_rmse=ml_training_run.metric_rmse,
        metric_r2=ml_training_run.metric_r2,
        model_path=ml_training_run.model_path,
        report_name=ml_training_run.report_name,
    )


async def save_failed_training_run(
    session: AsyncSession,
    training_run_name: str,
    ml_dataset_run_id: int | None,
    client_id: int,
    report_name: str,
) -> dict[str, int | str | bool | float | None]:
    """Save failed ML training run.
    Args:
        session (AsyncSession): Database session.
        training_run_name (str): ML training run name.
        ml_dataset_run_id (int | None): ML dataset run identifier.
        client_id (int): Client identifier.
        report_name (str): Training report name.
    """
    ml_training_run = await save_ml_training_run(
        session=session,
        training_run_name=training_run_name,
        ml_dataset_run_id=ml_dataset_run_id,
        client_id=client_id,
        model_type=ML_MODEL_TYPE_CATBOOST_REGRESSOR,
        target_name=ML_TARGET_CALLBACKS,
        status=ML_TRAINING_STATUS_FAILED,
        is_success=False,
        train_row_count=0,
        test_row_count=0,
        metric_mae=None,
        metric_rmse=None,
        metric_r2=None,
        model_path=None,
        report_name=report_name,
    )

    return build_training_result(
        ml_training_run_id=ml_training_run.id,
        training_run_name=ml_training_run.training_run_name,
        status=ml_training_run.status,
        is_success=ml_training_run.is_success,
        model_type=ml_training_run.model_type,
        target_name=ml_training_run.target_name,
        train_row_count=ml_training_run.train_row_count,
        test_row_count=ml_training_run.test_row_count,
        metric_mae=ml_training_run.metric_mae,
        metric_rmse=ml_training_run.metric_rmse,
        metric_r2=ml_training_run.metric_r2,
        model_path=ml_training_run.model_path,
        report_name=ml_training_run.report_name,
    )


async def run_ml_training_pipeline(
    session: AsyncSession,
    client_id: int,
    ml_dataset_run_id: int | None = None,
) -> dict[str, int | str | bool | float | None]:
    """Run ML training pipeline.
    Args:
        session (AsyncSession): Database session.
        client_id (int): Client identifier.
        ml_dataset_run_id (int | None): Optional ML dataset run identifier.
    """
    training_run_name = build_ml_training_run_name()
    report_name = build_ml_training_report_name(
        training_run_name=training_run_name,
    )

    ml_dataset_run = await resolve_ml_dataset_run(
        session=session,
        client_id=client_id,
        ml_dataset_run_id=ml_dataset_run_id,
    )

    if ml_dataset_run is None:
        return await save_no_data_training_run(
            session=session,
            training_run_name=training_run_name,
            ml_dataset_run_id=None,
            client_id=client_id,
            report_name=report_name,
        )

    training_dataframe = await load_ml_training_dataframe(
        session=session,
        ml_dataset_run_id=ml_dataset_run.id,
    )

    if training_dataframe.empty:
        return await save_no_data_training_run(
            session=session,
            training_run_name=training_run_name,
            ml_dataset_run_id=ml_dataset_run.id,
            client_id=client_id,
            report_name=report_name,
        )

    if len(training_dataframe) < MIN_TRAINING_ROW_COUNT:
        return await save_no_data_training_run(
            session=session,
            training_run_name=training_run_name,
            ml_dataset_run_id=ml_dataset_run.id,
            client_id=client_id,
            report_name=report_name,
        )

    try:
        dataset = build_dataset(data=training_dataframe)
        split = build_training_split(
            source_data=training_dataframe,
            dataset=dataset,
        )
        training_result = train_and_evaluate_catboost(
            dataset=dataset,
            split=split,
        )
        metrics = training_result['metrics']
        model_path = save_catboost_model(
            model=training_result['model'],
            training_run_name=training_run_name,
        )
    except ValueError:
        return await save_failed_training_run(
            session=session,
            training_run_name=training_run_name,
            ml_dataset_run_id=ml_dataset_run.id,
            client_id=client_id,
            report_name=report_name,
        )

    ml_training_run = await save_ml_training_run(
        session=session,
        training_run_name=training_run_name,
        ml_dataset_run_id=ml_dataset_run.id,
        client_id=client_id,
        model_type=ML_MODEL_TYPE_CATBOOST_REGRESSOR,
        target_name=ML_TARGET_CALLBACKS,
        status=ML_TRAINING_STATUS_SUCCESS,
        is_success=True,
        train_row_count=split.train_row_count,
        test_row_count=split.test_row_count,
        metric_mae=metrics['metric_mae'],
        metric_rmse=metrics['metric_rmse'],
        metric_r2=metrics['metric_r2'],
        model_path=model_path,
        report_name=report_name,
    )

    return build_training_result(
        ml_training_run_id=ml_training_run.id,
        training_run_name=ml_training_run.training_run_name,
        status=ml_training_run.status,
        is_success=ml_training_run.is_success,
        model_type=ml_training_run.model_type,
        target_name=ml_training_run.target_name,
        train_row_count=ml_training_run.train_row_count,
        test_row_count=ml_training_run.test_row_count,
        metric_mae=ml_training_run.metric_mae,
        metric_rmse=ml_training_run.metric_rmse,
        metric_r2=ml_training_run.metric_r2,
        model_path=ml_training_run.model_path,
        report_name=ml_training_run.report_name,
    )
