import time
import logging
from ..models import DebateMessage
from ..tools import web_search
from langchain.agents import create_agent

logger = logging.getLogger(__name__)


def get_research_agent(llm):
    research_react_agent = create_agent(
        model=llm,
        tools=[web_search],
    )
    return research_react_agent


def research_agent(state, config):
    llm = config["configurable"]["llm"]
    research_react_agent = get_research_agent(llm)
    topic = state["topic"]

    # Small delay before the research call to avoid bursting the TPM limit
    time.sleep(3)

    response = research_react_agent.invoke(
        {
            "messages": [
                (
                    "system",
                    "You are a research assistant. Use only the web_search tool. "
                    "Be concise — limit your final summary to 300 words."
                ),
                (
                    "user",
                    f"Research this debate topic briefly:\n\n{topic}\n\n"
                    "Collect one supporting point, one opposing point, and one neutral fact."
                ),
            ]
        }
    )

    history = state['conversation_history'].copy()
    final_research = response["messages"][-1].content

    msg = response["messages"]

    sources = []

    for r in msg:
        if r.type == "tool":
            sources.append(r.content)

    history.append(
        DebateMessage(agent="researcher", message=final_research)
    )

    return {
        "research": final_research,
        "research_sources": sources,
        "conversation_history": history,
    }
