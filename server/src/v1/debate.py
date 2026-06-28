#//v1/debate.py

import asyncio

from fastapi import APIRouter, Depends, HTTPException, status


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

    try:
        result = await service.run(topic=request.topic, groq_api_key=request.groq_api_key)
    except asyncio.TimeoutError as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=(
                "The debate took too long. This is usually caused by provider latency, "
                "Tavily search delay, or Groq quota/rate-limit waiting. Please try again later "
                "or use a shorter topic."
            ),
        ) from exc
    except Exception as exc:
        error_text = str(exc)
        if "429" in error_text or "rate_limit_exceeded" in error_text or "rate limit" in error_text.lower():
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=(
                    "Groq rate limit or daily token quota was reached. Please retry after the "
                    "wait time shown by Groq, use a different key/org, or upgrade your Groq tier."
                ),
            ) from exc
        raise

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
