from fastapi import FastAPI

from app.api.exception_handlers import register_exception_handlers
from app.api.routes.clients import router as clients_router
from app.api.routes.health import router as health_router
from app.api.routes.pipeline_1 import router as pipeline_router
from app.api.routes.validation import router as validation_router
from app.api.routes.analytics import router as analytics_router


app = FastAPI(title='vacancy-intelligence-ai')

register_exception_handlers(app)

app.include_router(health_router)
app.include_router(clients_router)
app.include_router(validation_router)
app.include_router(pipeline_router)
app.include_router(analytics_router)
