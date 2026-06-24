from services import llm 


def research_agent(state):
    topic = state["topic"]

    prompt = f"""
    Research the topic given by the Moderator.

    Topic:
    {topic}

    Give:
    - Key facts
    - Supporting evidence
    - Counter evidence
    """

    response = llm.invoke(prompt)

    return {
        "research": response.content
    }