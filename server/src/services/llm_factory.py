import os
from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv(Path(__file__).resolve().parents[3] / ".env")



class LLMFactory:

    @staticmethod
    def create_gemini(api_key: str, model: str | None = None):

        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0,
            max_tokens=1024,
        )