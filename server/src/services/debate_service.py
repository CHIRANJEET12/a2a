from debate_ai import graph, DebateMessage
from .llm_factory import LLMFactory

class DebateService:

    def __init__(self):
        pass

    async def run(self, topic: str, groq_api_key: str):
        """
        Execute a debate.
        """

        llm = LLMFactory.create_groq(
            api_key=groq_api_key
        )



        init_stage = {
            "topic": topic,
            "research": "",
            "conversation_history": [
                DebateMessage(
                    agent="system",
                    message="Debate started."
                )
            ],
            "verdict": {},
            "supporting_evidence": {},
        }

        config = {"configurable": {
            "llm": llm,
            }
        }

        result = graph.invoke(
            init_stage,
            config=config
        )

        return result
    

