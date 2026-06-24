from services import llm
from models import DebateMessage

def against_rebuttal_agent(state):

    last_msg = DebateMessage.model_validate(
        state["conversation_history"][-1]
    )
    opponent_message = last_msg.message
    prompt = f"""
    Topic:
    {state['topic']}

    Opponent Rebuttal:
    {opponent_message}

    Defend your position.
    """

    response = llm.invoke(prompt)

    history = state["conversation_history"].copy()

    history.append(
        DebateMessage(agent="against", message=response.content),
    )

    return {
        "conversation_history": history
    }