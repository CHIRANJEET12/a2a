from typing import Any, TypedDict
from typing import List
from pydantic import HttpUrl

from pydantic import BaseModel

class EvidenceItem(BaseModel):
    text: str
    url: HttpUrl | None = None

class JudgeResponse(BaseModel):
    winner: str
    reasoning: str
    pro_score: float
    against_score: float

class DebateResponse(BaseModel):
    argument: str
    evidence: list[EvidenceItem]
    confidence: float

class DebateMessage(BaseModel):
    agent: str
    message: str

class SearchResult(BaseModel):
    title: str
    url: str
    content: str

class DebateState(TypedDict):
    topic: str
    research: str

    conversation_history: List[DebateMessage]
    research_sources: List[str]

    verdict: dict

    supporting_evidence: dict[str, Any]


