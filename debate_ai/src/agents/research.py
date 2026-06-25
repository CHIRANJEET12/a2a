from services import llm 
from models import DebateMessage
from tools import web_search
from langchain.agents import create_agent

research_react_agent = create_agent(
    model=llm,
    tools=[
        web_search,
        # wikipedia_search,
    ]
)

def research_agent(state):

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