from ...models import DebateMessage, DebateResponse
from ..utils import truncate_research

def pro_opening_agent(state, config):
    llm = config["configurable"]["llm"]
    structured_llm = llm.with_structured_output(DebateResponse)
    research = truncate_research(state["research"])
    sources = state["research_sources"]

    prompt = f"""You are a professional debater taking the PRO position.

Topic: {state["topic"]}

Research (summary): {research}

Research Sources: {state["research_sources"]}

Every factual claim must cite one of the supplied URLs.

Instead write:

According to Oracle:
url


Write a concise opening argument:
- Main argument (2-3 sentences)
- Key evidence (2 points)
- Conclusion (1-2 sentences)
"""

    response = structured_llm.invoke(prompt)

    history = state['conversation_history'].copy()
    history.append(DebateMessage(agent="pro", message=response.argument))
    evidence = state.get("supporting_evidence", {}).copy()
    evidence["pro"] = [*evidence.get("pro", []), *response.evidence]

    return {
        "research_sources": sources,
        "conversation_history": history,
        "supporting_evidence": evidence,
    }
