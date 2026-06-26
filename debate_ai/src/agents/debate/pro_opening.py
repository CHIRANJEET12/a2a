from ...models import DebateMessage

def pro_opening_agent(state,config):

    llm = config["configurable"]["llm"]

    prompt = f"""
    You are a professional debater.

    Topic:
    {state["topic"]}

    Research:
    {state["research"]}

    Take the PRO position.

    Create:
    - Main argument
    - Supporting evidence
    - Conclusion

    Be persuasive.
    """

    response = llm.invoke(prompt)

    history = state['conversation_history'].copy()

    history.append(DebateMessage(agent="pro", message=response.content))

    return {
        "conversation_history": history
    }