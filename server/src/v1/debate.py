#//v1/debate.py

from fastapi import APIRouter, Depends, status


from ..schemas import DebateRequest, DebateResult, APIResponse
from ..services import DebateService

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

@router.post("", response_model=APIResponse[DebateResult], status_code=status.HTTP_200_OK, summary="Run an AI debate")
async def run_debate(request: DebateRequest, service: DebateService = Depends(get_debate_service),):
    """
    Run a complete debate on the supplied topic.
    """

    result = await service.run(topic=request.topic, groq_api_key=request.groq_api_key)

    response = DebateResult(
        topic=result["topic"],
        transcript=result["conversation_history"],
        verdict=result["verdict"],
        supporting_evidence=result["supporting_evidence"],
    )

    return APIResponse(
        success=True,
        message="Debate completed successfully.",
        data=response,
    )