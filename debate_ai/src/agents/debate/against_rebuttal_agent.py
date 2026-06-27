from ...models import DebateMessage
from ..utils import invoke_with_retry

def against_rebuttal_agent(state, config):
    llm = config["configurable"]["llm"]

    last_msg = DebateMessage.model_validate(
        state["conversation_history"][-1]
    )
    opponent_message = last_msg.message[:600]

    prompt = f"""Topic: {state['topic']}

Opponent's rebuttal: {opponent_message}

As the AGAINST side, write a focused counter-rebuttal (3-5 sentences):
- Challenge the weakest point
- Reinforce your strongest evidence
"""

    response = invoke_with_retry(llm, prompt)

    history = state["conversation_history"].copy()
    history.append(DebateMessage(agent="against", message=response.content))

    return {"conversation_history": history}