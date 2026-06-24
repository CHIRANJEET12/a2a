from typing import TypedDict
from typing import List

from pydantic import BaseModel

class DebateMessage(BaseModel):
    agent: str
    message: str

class DebateState(TypedDict):
    topic: str
    research: str

    conversation_history: List[DebateMessage]


    verdict: str
