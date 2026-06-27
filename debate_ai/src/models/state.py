from typing import TypedDict
from typing import List

from pydantic import BaseModel

class EvidenceItem(BaseModel):
    text: str
    url: str | None

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

class DebateState(TypedDict):
    topic: str
    research: str

    conversation_history: List[DebateMessage]


    verdict: dict

    supporting_evidence: dict


class SearchResult(BaseModel):
    title: str
    url: str
    content: str