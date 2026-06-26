from ..models import DebateMessage

def moderator_agent(state,config):
    llm = config["configurable"]["llm"]

    topic = state["topic"]

    prompt = f"""
    Act as a moderator for the topic.

    Topic:
    {topic}

    Give:
    - Understand the topic.
    - Define debate scope.
    - Generate debate rules.
    """

    response = llm.invoke(prompt)

    history = state['conversation_history'].copy()

    history.append(DebateMessage(agent="moderator", message=response.content))

    return {
        "conversation_history": history
    }
