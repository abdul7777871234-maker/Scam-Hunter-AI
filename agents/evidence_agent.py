from __future__ import annotations


class EvidenceAgent:
    """Analyzes retrieved evidence without treating unverified claims as facts."""

    def __init__(self, router):
        self.router = router

    def run(self, user_text: str, rag: dict, web: dict) -> dict:
        rag_items = rag.get("evidence", [])
        web_items = web.get("items", [])

        evidence = []

        for item in rag_items:
            evidence.append({
                "source_type": "knowledge_base",
                "source": item,
            })

        for item in web_items:
            evidence.append({
                "source_type": "web",
                "source": item,
            })

        evidence_text = self._format_evidence(evidence)

        prompt = f"""
You are the evidence analysis agent for ScamHunter AI.

Analyze the user's suspicious content against the supplied evidence.

Do not invent facts.
Do not treat a source's claim as automatically verified.
Clearly distinguish:
- observed information
- supporting evidence
- unverified claims
- missing information

Return a concise evidence analysis followed by a structured evidence list.

USER CONTENT:
{user_text}

AVAILABLE EVIDENCE:
{evidence_text}
"""

        try:
            result = self.router.best_available(
                prompt,
                system=(
                    "You are an evidence-first investigation analyst. "
                    "Be precise, cautious, and explicit about uncertainty."
                ),
                prefer_gemini=True,
            )

            analysis = result.text.strip()

        except Exception as exc:
            analysis = (
                "Evidence analysis could not be completed reliably. "
                f"Reason: {exc}"
            )

        return {
            "analysis": analysis,
            "evidence": evidence,
        }

    @staticmethod
    def _format_evidence(evidence: list) -> str:
        if not evidence:
            return "No evidence was retrieved."

        lines = []

        for index, item in enumerate(evidence, start=1):
            source_type = item.get("source_type", "unknown")
            source = item.get("source", {})

            if isinstance(source, dict):
                title = source.get("title", "")
                content = (
                    source.get("content")
                    or source.get("text")
                    or source.get("snippet")
                    or str(source)
                )
                url = source.get("url", "")
            else:
                title = ""
                content = str(source)
                url = ""

            lines.append(
                f"[Evidence {index} | {source_type}]\n"
                f"Title: {title}\n"
                f"URL: {url}\n"
                f"Content: {content}"
            )

        return "\n\n".join(lines)
