from ..models import DebateMessage
from ..tools import web_search
from langchain.agents import create_agent


def get_research_agent(llm):
    research_react_agent = create_agent(
        model=llm,
        tools=[
            web_search,
            # wikipedia_search,
        ]
    )

    return research_react_agent

def research_agent(state, config):

    llm = config["configurable"]["llm"]

    research_react_agent = get_research_agent(llm)

    topic = state["topic"]

    response = research_react_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    f"""
                    Research the following topic thoroughly:
                    You also can use tools for web_search and attach the links.


                    {topic}

                    Collect:
                    - Supporting evidence
                    - Opposing evidence
                    - Neutral facts
                    """
                )
            ]
        }
    )


    history = state['conversation_history'].copy()

    final_research = response["messages"][-1].content

    history.append(
        DebateMessage(
            agent="researcher",
            message=final_research
        )
    )

    return {
        "research": final_research,
        "conversation_history": history,
    }