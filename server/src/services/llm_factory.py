from langchain_groq import ChatGroq


class LLMFactory:

    @staticmethod
    def create_groq(api_key: str):

        return ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=api_key,
            temperature=0,
            max_tokens=120,
            max_retries=0,
        )
