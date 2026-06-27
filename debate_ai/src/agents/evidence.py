from ..models import DebateResponse
from .utils import truncate_history

def final_staging_agent(state, config):
    llm = config["configurable"]["llm"]
    structured_llm = llm.with_structured_output(DebateResponse)

    history = truncate_history(state["conversation_history"], max_chars=2000)

    prompt = f"""
You are an evidence extraction agent.

Topic: {state['topic']}

Transcript:
{history}

Extract:
- Strongest argument
- 2–3 evidence points
- Each evidence MUST include:
  - text: factual claim
  - url: real source URL if available, otherwise null

Return structured output only.
"""

    response = structured_llm.invoke(prompt)

    return {
        "supporting_evidence": {
            "argument": response.argument,
            "evidence": [item.model_dump() for item in response.evidence],
            "confidence": response.confidence,
        }
    }