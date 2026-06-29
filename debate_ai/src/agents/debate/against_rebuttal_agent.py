from ...models import DebateMessage, DebateResponse

def against_rebuttal_agent(state, config):
    llm = config["configurable"]["llm"]
    structured_llm = llm.with_structured_output(DebateResponse)

    last_msg = DebateMessage.model_validate(
        state["conversation_history"][-1]
    )
    opponent_message = last_msg.message[:600]

    sources = state["research_sources"]

    prompt = f"""Topic: {state['topic']}

Opponent's rebuttal: {opponent_message}
Research Sources: {state["research_sources"]}

Every factual claim must cite one of the supplied URLs.


Instead attach the link of the urls like this:

According to Oracle:
https://...



As the AGAINST side, write a focused counter-rebuttal (3-5 sentences):
- Challenge the weakest point
- Reinforce your strongest evidence
"""

    response = structured_llm.invoke(prompt)

    history = state["conversation_history"].copy()
    history.append(DebateMessage(agent="against", message=response.argument))
    evidence = state.get("supporting_evidence", {}).copy()
    evidence["against"] = [*evidence.get("against", []), *response.evidence]

    return {
        "research_sources": sources,
        "conversation_history": history,
        "supporting_evidence": evidence,
    }
