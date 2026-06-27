import time
import logging
from typing import List

from ..models import DebateMessage

logger = logging.getLogger(__name__)


def truncate_text(text: str, max_chars: int = 3000, from_end: bool = False) -> str:
    if len(text) <= max_chars:
        return text

    if from_end:
        return "... [truncated earlier content]\n" + text[-max_chars:]

    return text[:max_chars] + "\n\n... [truncated]"


def truncate_research(text: str, max_chars: int = 1200) -> str:
    """Reduced from 1800 to 1200 to stay within TPM limits."""
    return truncate_text(text, max_chars=max_chars)


def truncate_history(history: List[DebateMessage], max_chars: int = 2000) -> str:
    """Reduced from 3000 to 2000 to stay within TPM limits."""
    joined = "\n\n".join(
        f"{msg.agent}: {msg.message}" for msg in history
    )
    return truncate_text(joined, max_chars=max_chars, from_end=True)


def invoke_with_retry(llm, prompt: str, max_retries: int = 5, base_delay: float = 15.0):
    """
    Invoke LLM with exponential backoff on rate limit errors (HTTP 429).
    Groq free tier: 6000 TPM — wait and retry automatically.
    """
    for attempt in range(max_retries):
        try:
            return llm.invoke(prompt)
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "rate_limit_exceeded" in error_str:
                # Parse suggested wait time from error if present
                wait = base_delay * (2 ** attempt)
                try:
                    import re
                    match = re.search(r"try again in ([0-9.]+)s", error_str)
                    if match:
                        wait = float(match.group(1)) + 2.0  # add buffer
                except Exception:
                    pass
                logger.warning(
                    f"Rate limit hit (attempt {attempt + 1}/{max_retries}). "
                    f"Waiting {wait:.1f}s before retry..."
                )
                time.sleep(wait)
            else:
                raise  # Non-rate-limit errors bubble up immediately

    raise RuntimeError(
        f"LLM call failed after {max_retries} retries due to rate limiting."
    )