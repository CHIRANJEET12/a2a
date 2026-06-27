from ..models import JudgeResponse
from .utils import truncate_history

def judge_agent(state, config):
    llm = config["configurable"]["llm"]
    structured_llm = llm.with_structured_output(JudgeResponse)

    history = truncate_history(state["conversation_history"], max_chars=2000)

    prompt = f"""You are an impartial debate judge.

Topic: {state['topic']}

Transcript:
{history}

Score each side (0-10) on:
- Evidence quality (40%)
- Logic (30%)
- Rebuttal (20%)
- Clarity (10%)

Return: pro_score, against_score, winner, reasoning (2-3 sentences).
"""

    response = structured_llm.invoke(prompt)

    return {
        "verdict": {
            "winner": response.winner,
            "reasoning": response.reasoning,
            "pro_score": response.pro_score,
            "against_score": response.against_score,
        }
    }