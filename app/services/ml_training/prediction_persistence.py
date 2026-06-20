from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.ml_training_prediction import MlTrainingPrediction


async def save_ml_training_predictions(
    session: AsyncSession,
    prediction_rows: list[dict[str, Any]],
) -> list[MlTrainingPrediction]:
    """Save ML training prediction rows.
    Args:
        session (AsyncSession): Database session.
        prediction_rows (list[dict[str, Any]]): Prediction rows.
    """
    ml_training_predictions = [
        MlTrainingPrediction(
            ml_training_run_id=row['ml_training_run_id'],
            source_row_index=row['source_row_index'],
            client_id=row['client_id'],
            company_id=row.get('company_id'),
            vacancy_id=row.get('vacancy_id'),
            date_day=row.get('date_day'),
            split_name=row['split_name'],
            target_name=row['target_name'],
            actual_value=row['actual_value'],
            predicted_value=row['predicted_value'],
            prediction_error=row['prediction_error'],
            absolute_error=row['absolute_error'],
            squared_error=row['squared_error'],
        )
        for row in prediction_rows
    ]

    session.add_all(ml_training_predictions)
    await session.flush()

    return ml_training_predictions
