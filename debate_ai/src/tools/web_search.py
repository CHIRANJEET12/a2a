from ..config import settings
from ..models import SearchResult
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
        search_depth="basic",
        max_results=3,
    )

    formatted = []

    for item in results["results"]:
        formatted.append(
            SearchResult(
            title=item["title"],
            url=item["url"],
            content=item["content"][:250]
            )
        )

    return "\n".join(
    f"{r.title}\n{r.content}\n{r.url}"
    for r in formatted
)
