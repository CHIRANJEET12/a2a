from services import llm

def moderator_agent(state):
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

    return {
        "debate_scope": response.content
    }