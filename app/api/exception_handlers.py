from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import AppError


async def app_error_handler(
    request: Request,
    exc: AppError,
) -> JSONResponse:
    """Handle application exceptions.
    Args:
        request (Request): Incoming request.
        exc (AppError): Application exception."""
    response = JSONResponse(
        status_code=exc.status_code,
        content={'detail': exc.detail},
    )
    return response


def register_exception_handlers(app: FastAPI) -> None:
    """Register application exception handlers.
    Args:
        app (FastAPI): FastAPI application."""
    app.add_exception_handler(AppError, app_error_handler)
