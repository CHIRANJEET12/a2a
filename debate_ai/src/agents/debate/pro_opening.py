from ...models import DebateMessage
from ..utils import truncate_research, invoke_with_retry

def pro_opening_agent(state, config):
    llm = config["configurable"]["llm"]
    research = truncate_research(state["research"])

    prompt = f"""You are a professional debater taking the PRO position.

Topic: {state["topic"]}

Research (summary): {research}

Write a concise opening argument:
- Main argument (2-3 sentences)
- Key evidence (2 points)
- Conclusion (1-2 sentences)
"""

    response = invoke_with_retry(llm, prompt)

    history = state['conversation_history'].copy()
    history.append(DebateMessage(agent="pro", message=response.content))

    return {"conversation_history": history}