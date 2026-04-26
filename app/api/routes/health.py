from fastapi import APIRouter


router = APIRouter(prefix='/health', tags=['health'])


@router.get('')
async def health_check() -> dict[str, str]:
    """Return application health status.
    Args:
        """
    health_status = {
        'status': 'ok',
    }
    return health_status
