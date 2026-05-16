from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.ml_training_run import MlTrainingRun


async def save_ml_training_run(
    session: AsyncSession,
    training_run_name: str,
    ml_dataset_run_id: int | None,
    client_id: int,
    model_type: str,
    target_name: str,
    status: str,
    is_success: bool,
    train_row_count: int,
    test_row_count: int,
    metric_mae: float | None,
    metric_rmse: float | None,
    metric_r2: float | None,
    model_path: str | None,
    report_name: str | None,
) -> MlTrainingRun:
    """Save ML training run.
    Args:
        session (AsyncSession): Database session.
        training_run_name (str): ML training run name.
        ml_dataset_run_id (int | None): ML dataset run identifier.
        client_id (int): Client identifier.
        model_type (str): Model type.
        target_name (str): Target name.
        status (str): Training run status.
        is_success (bool): Whether training run is successful.
        train_row_count (int): Number of train rows.
        test_row_count (int): Number of test rows.
        metric_mae (float | None): MAE metric.
        metric_rmse (float | None): RMSE metric.
        metric_r2 (float | None): R2 metric.
        model_path (str | None): Saved model path.
        report_name (str | None): Training report name.
    """
    ml_training_run = MlTrainingRun(
        training_run_name=training_run_name,
        ml_dataset_run_id=ml_dataset_run_id,
        client_id=client_id,
        model_type=model_type,
        target_name=target_name,
        status=status,
        is_success=is_success,
        train_row_count=train_row_count,
        test_row_count=test_row_count,
        metric_mae=metric_mae,
        metric_rmse=metric_rmse,
        metric_r2=metric_r2,
        model_path=model_path,
        report_name=report_name,
    )

    session.add(ml_training_run)
    await session.flush()

    return ml_training_run
