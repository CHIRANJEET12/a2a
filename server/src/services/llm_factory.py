from langchain_groq import ChatGroq

class LLMFactory:

    @staticmethod
    def create_groq(api_key: str):

        return ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=api_key,
            temperature=0
        )