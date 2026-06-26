from fastapi import FastAPI
from .core import settings, lifespan
from .v1 import api_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

app.include_router(
    api_router,
    prefix="/api/v1"
)