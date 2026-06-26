#//v1/debate.py

from fastapi import APIRouter, Depends, status

from schemas import DebateRequest, DebateResponse
from services import DebateService

router = APIRouter(
    prefix="/debate",
    tags=["Debate"]
)

def get_debate_service() -> DebateService:
    """
    Dependency that returns a DebateService instance.
    Later this can inject databases, caches, etc.
    """
    return DebateService()

@router.post("", response_model=DebateResponse, status_code=status.HTTP_200_OK, summary="Run an AI debate")
async def run_debate(request: DebateRequest, service: DebateService = Depends(get_debate_service),):
    """
    Run a complete debate on the supplied topic.
    """

    result = await service.run(topic=request.topic, groq_api_key=request.groq_api_key)

    return result