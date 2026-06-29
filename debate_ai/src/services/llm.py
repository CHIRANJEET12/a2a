# from langchain_groq import ChatGroq
# from config import settings
# from models import DebateResponse, JudgeResponse

# llm = ChatGroq(
#     model="llama-3.1-8b-instant",
#     api_key=settings.GROQ_API_KEY,
#     temperature=0,
#     max_retries=0,
# )

# structured_llm_judge = llm.with_structured_output(JudgeResponse)

# structured_llm_evidence = llm.with_structured_output(DebateResponse)