from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.validation import router as validation_router


app = FastAPI(title='vacancy-intelligence-ai')

app.include_router(health_router)
app.include_router(validation_router)
