import time
import json
import logging
from ..models import DebateMessage
from ..tools import web_search
from .utils import invoke_with_retry

logger = logging.getLogger(__name__)


def _run_search(topic: str) -> tuple[str, list]:
    """Call web_search directly — no agent loop, no tool-call schema issues."""
    try:
        results = web_search.invoke({"query": topic})

        sources = []
        snippets = []

        if isinstance(results, list):
            for r in results[:5]:
                if isinstance(r, dict):
                    url     = r.get("url") or r.get("link") or r.get("href") or ""
                    title   = r.get("title", "")
                    snippet = r.get("content") or r.get("snippet") or r.get("body") or ""
                    if url:
                        sources.append({"title": title, "url": url})
                    if snippet:
                        snippets.append(f"- {title}: {snippet[:300]}")
        elif isinstance(results, str):
            snippets.append(results[:1500])

        raw_text = "\n\n".join(snippets) if snippets else f"No results found for: {topic}"
        return raw_text, sources

    except Exception as e:
        logger.warning(f"web_search failed: {e}")
        return f"No search results available for: {topic}", []


def research_agent(state, config):
    llm   = config["configurable"]["llm"]
    topic = state["topic"]

    time.sleep(1)  # small buffer for TPM

    raw_text, sources = _run_search(topic)

    # Summarise with plain LLM call — zero tool use
    prompt = f"""You are a research assistant preparing a debate briefing.

Topic: {topic}

Search results:
{raw_text[:1500]}

Write a concise research summary (max 200 words) with:
- One strong supporting point (cite source URL if available)
- One opposing point (cite source URL if available)
- One neutral fact

Be factual and concise."""

    response = invoke_with_retry(llm, prompt)
    final_research = response.content

    history = state["conversation_history"].copy()
    history.append(DebateMessage(agent="researcher", message=final_research))

    return {
        "research": final_research,
        "research_sources": sources,
        "conversation_history": history,
    }