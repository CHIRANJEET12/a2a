from ...models import DebateMessage
from ..utils import truncate_research, invoke_with_retry

def against_opening_agent(state, config):
    llm = config["configurable"]["llm"]

    last_msg = DebateMessage.model_validate(
        state["conversation_history"][-1]
    )
    pro_message = last_msg.message
    research = truncate_research(state["research"])

    prompt = f"""You are a professional debater taking the AGAINST position.

Topic: {state['topic']}

Research (summary): {research}

Opponent's opening: {pro_message[:500]}

Write a concise opening argument:
- Main counter-argument (2-3 sentences)
- Key evidence (2 points)
- Conclusion (1-2 sentences)
"""

    response = invoke_with_retry(llm, prompt)

    history = state['conversation_history'].copy()
    history.append(DebateMessage(agent="against", message=response.content))

    return {"conversation_history": history}