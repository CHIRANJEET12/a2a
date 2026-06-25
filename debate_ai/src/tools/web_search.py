from config import settings
from tavily import TavilyClient
from pydantic import BaseModel
from langchain.tools import tool
from typing import List
import os


client = TavilyClient(api_key=settings.TRAVILY_API_KEY)

class SearchResult(BaseModel):
    title: str
    url: str
    content: str

@tool
def web_search(query: str) -> str:
    """
    Search the web using Tavily.
    """

    results = client.search(
        query=query,
        search_depth="advanced",
        max_results=5,
    )

    return str(results)
