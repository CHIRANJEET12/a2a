from fastapi import APIRouter
from .health import router as health_router
from .debate import router as debate_router
api_router = APIRouter()

api_router.include_router(
    health_router,
    tags=["Health"]
)

api_router.include_router(
    debate_router,
    tags=["Debate"]
)