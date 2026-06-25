from services import structured_llm_judge

def judge_agent(state):

    history = "\n\n".join(
        [
            f"{msg.agent}: {msg.message}"
            for msg in state["conversation_history"]
        ]
    )


    prompt = f"""

    You are an impartial debate judge.

    Evaluate both sides based on:

    1. Strength of evidence (40%)
    2. Logical reasoning (30%)
    3. Rebuttal quality (20%)
    4. Clarity and persuasion (10%)


    Topic:
    {state['topic']}

    Debate Transcript:
    {history}

    Evaluate:

    1. Evidence Quality
    2. Logical Consistency
    3. Persuasiveness
    4. Rebuttal Strength

    Give:

    - Pro Score (/10)
    - Against Score (/10)
    - Winner
    - Reasoning
    """

    response = structured_llm_judge.invoke(prompt)

    return {
        "verdict": {
            "winner": response.winner,
            "reasoning": response.reasoning,
            "pro_score": response.pro_score,
            "against_score": response.against_score,
        }
    }