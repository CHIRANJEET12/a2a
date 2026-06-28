from ..models import DebateResponse
from .utils import truncate_history

def final_staging_agent(state, config):
    llm = config["configurable"]["llm"]
    structured_llm = llm.with_structured_output(DebateResponse)

    history = truncate_history(state["conversation_history"], max_chars=2000)

    pro_evidence = state.get("supporting_evidence", {}).get("pro", [])
    against_evidence = state.get("supporting_evidence", {}).get("against", [])

    prompt = f"""
You are an evidence extraction agent.

Topic: {state['topic']}

Research Sources: {state["research_sources"]}

Pro evidence:
{pro_evidence}

Against evidence:
{against_evidence}

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
            "evidence": [item.model_dump(mode="json") for item in response.evidence],
            "confidence": response.confidence,
        }
    }
