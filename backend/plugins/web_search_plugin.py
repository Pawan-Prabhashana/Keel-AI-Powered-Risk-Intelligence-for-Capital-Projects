"""Web search plugin for the risk agents.

Gives the political, tariff, and logistics agents grounded web search using
Anthropic's built-in web search tool, returning text plus source citations.
"""

import os
import json
import anthropic
from semantic_kernel.functions.kernel_function_decorator import kernel_function

SEARCH_MODEL = os.getenv("ANTHROPIC_SEARCH_MODEL", "claude-sonnet-4-6")


class WebSearchPlugin:
    """Grounded web search backed by Anthropic's web_search tool."""

    def __init__(self, api_key: str = None, max_uses: int = 5):
        self.client = anthropic.Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
        self.max_uses = max_uses

    @kernel_function(description="Searches the web for current news and returns findings with source citations")
    def search_web(self, query: str) -> str:
        """Runs a grounded web search and returns findings + citations as JSON."""
        try:
            resp = self.client.messages.create(
                model=SEARCH_MODEL,
                max_tokens=2000,
                tools=[{
                    "type": "web_search_20250305",
                    "name": "web_search",
                    "max_uses": self.max_uses,
                }],
                messages=[{
                    "role": "user",
                    "content": (
                        f"Search the web and report current, dated findings for: {query}\n"
                        "List each finding with: title, publication name, URL, publication date, "
                        "and a one-sentence summary. Only reputable sources."
                    ),
                }],
            )

            text_parts, citations = [], []
            for block in resp.content:
                if getattr(block, "type", None) == "text":
                    text_parts.append(block.text)
                    for c in (getattr(block, "citations", None) or []):
                        citations.append({
                            "title": getattr(c, "title", None),
                            "url": getattr(c, "url", None),
                        })

            return json.dumps({
                "query": query,
                "findings": "\n".join(text_parts).strip(),
                "citations": citations,
            }, default=str)
        except Exception as e:
            return json.dumps({"query": query, "error": str(e), "findings": "", "citations": []})
