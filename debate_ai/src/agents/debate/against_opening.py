from ...models import DebateMessage

def against_opening_agent(state,config):

    llm = config["configurable"]["llm"]
    
    last_msg = DebateMessage.model_validate(
        state["conversation_history"][-1]
    )
    pro_message = last_msg.message

    prompt = f"""
    Topic:
    {state['topic']}

    Research:
    {state['research']}

    Opponent Argument:
    {pro_message}

    Take the AGAINST position.

    Create:
    - Main argument
    - Supporting evidence
    - Conclusion

    Be persuasive.
    """

    response = llm.invoke(prompt)

    history = state['conversation_history'].copy()

    history.append(DebateMessage(agent="against", message=response.content))

    return {
        "conversation_history": history
    }