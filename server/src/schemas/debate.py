from pydantic import BaseModel, Field

class DebateRequest(BaseModel):

    topic: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="Topic to debate."
    )

    groq_api_key: str = Field(
        ...,
        description="Customer's Groq API Key."
    )


class DebateResponse(BaseModel):
    topic: str
    transcript: list

    verdict: dict

    supporting_evidence: dict