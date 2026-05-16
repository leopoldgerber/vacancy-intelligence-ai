from app.db.session import SessionLocal
from app.services.ml_training.run_ml_training_pipeline import (
    run_ml_training_pipeline,
)


async def run_ml_training(
    client_id: int,
    ml_dataset_run_id: int | None = None,
) -> dict[str, int | str | bool | float | None]:
    """Run ML training service.
    Args:
        client_id (int): Client identifier.
        ml_dataset_run_id (int | None): Optional ML dataset run identifier.
    """
    async with SessionLocal() as session:
        async with session.begin():
            training_result = await run_ml_training_pipeline(
                session=session,
                client_id=client_id,
                ml_dataset_run_id=ml_dataset_run_id,
            )

    return training_result
