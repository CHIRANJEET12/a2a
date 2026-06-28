from ...models import DebateMessage, DebateResponse
from ..utils import truncate_research

def against_opening_agent(state, config):
    llm = config["configurable"]["llm"]

    structured_llm = llm.with_structured_output(DebateResponse)

    last_msg = DebateMessage.model_validate(
        state["conversation_history"][-1]
    )
    pro_message = last_msg.message
    research = truncate_research(state["research"])
    sources = state["research_sources"]

    prompt = f"""You are a professional debater taking the AGAINST position.

Topic: {state['topic']}

Research (summary): {research}

Research Sources: {state["research_sources"]}

Opponent's opening: {pro_message[:500]}

Every factual claim must cite one of the supplied URLs.

Never say "studies show..."

Instead write:

According to Oracle:
https://...

or

According to Databricks:
https://...

Write a concise opening argument:
- Main counter-argument (2-3 sentences)
- Key evidence (2 points)
- Conclusion (1-2 sentences)
"""

    response = structured_llm.invoke(prompt)

    history = state['conversation_history'].copy()
    history.append(DebateMessage(agent="against", message=response.argument))
    evidence = state.get("supporting_evidence", {}).copy()
    evidence["against"] = [*evidence.get("against", []), *response.evidence]

    return {
        "research_sources": sources,
        "conversation_history": history,
        "supporting_evidence": evidence,
    }
