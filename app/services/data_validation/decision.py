def build_ingestion_decision(
    validation_result: dict[str, object],
) -> dict[str, object]:
    """Build ingestion decision from validation result.
    Args:
        validation_result (dict[str, object]): Final validation result."""
    is_valid = bool(validation_result['is_valid'])
    status = str(validation_result['status'])

    decision_result = {
        'should_continue': is_valid,
        'status': status,
        'message': (
            'Validation passed. Data can be loaded into the database.'
            if is_valid
            else 'Validation failed. Data loading must be stopped.'
        ),
    }
    return decision_result
