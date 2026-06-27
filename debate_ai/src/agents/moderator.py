from ..models import DebateMessage
from .utils import invoke_with_retry

def moderator_agent(state, config):
    llm = config["configurable"]["llm"]
    topic = state["topic"]

    prompt = f"""Moderate this debate topic.

Topic: {topic}

Briefly cover:
- Scope of the debate
- Key rules (2-3 bullet points)
"""

    response = invoke_with_retry(llm, prompt)

    history = state['conversation_history'].copy()
    history.append(DebateMessage(agent="moderator", message=response.content))

    return {"conversation_history": history}