import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv(Path(__file__).resolve().parents[3] / ".env")

DEFAULT_GROQ_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"


class LLMFactory:

    @staticmethod
    def create_groq(api_key: str, model: str | None = None):
        model_name = model or os.getenv("GROQ_MODEL", DEFAULT_GROQ_MODEL)

        return ChatGroq(
            model=model_name,
            api_key=api_key,
            temperature=0,
            max_tokens=384,
            max_retries=2,
        )
