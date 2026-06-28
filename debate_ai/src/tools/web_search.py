from ..config import settings
from ..models import SearchResult
from tavily import TavilyClient
from langchain.tools import tool


client = TavilyClient(api_key=settings.TRAVILY_API_KEY)


@tool
def web_search(query: str) -> list[dict]:
    """
    When citing evidence:

- Quote the supporting statement.
- Copy the corresponding URL EXACTLY as provided.
- Never invent URLs.
- If no source exists, return null.
    """

    results = client.search(
        query=query,
        search_depth="basic",
        max_results=2,
    )

    formatted = []

    for item in results["results"]:
        formatted.append(
            SearchResult(
            title=item["title"],
            url=item["url"],
            content=item["content"][:150]
            )
        )

    return [r.model_dump(mode="json") for r in formatted]

