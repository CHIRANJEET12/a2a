from services import structured_llm_evidence

def final_staging_agent(state):

    history = "\n\n".join(
        [
            f"{msg.agent}: {msg.message}"
            for msg in state["conversation_history"]
        ]
    )


    prompt = f"""
You are an evidence extraction agent.

Topic:
{state['topic']}

Debate Transcript:
{history}

Your task:

- Identify the strongest overall argument from the debate.
- Extract the most important pieces of evidence.
- Remove duplicate evidence.
- Ignore rhetorical statements.
- Focus on verifiable facts.

Return:
- argument
- evidence
- confidence

The confidence score should represent how well-supported the argument is by the evidence provided.
"""

    response = structured_llm_evidence.invoke(prompt)

    return {
        "supporting_evidence": {
            "argument": response.argument,
            "evidence": response.evidence,
            "confidence": response.confidence,
        }
    }