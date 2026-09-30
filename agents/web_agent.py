from __future__ import annotations


class WebResearchAgent:
    """Performs external web research when current evidence is required."""

    def __init__(self, web_search):
        self.web_search = web_search

    def run(self, query: str) -> dict:
        try:
            items, cached = self.web_search.search(query)

            return {
                "items": items or [],
                "cached": cached,
            }

        except Exception as exc:
            return {
                "items": [],
                "cached": False,
                "error": str(exc),
            }
