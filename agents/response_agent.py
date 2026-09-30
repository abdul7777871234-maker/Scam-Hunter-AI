from __future__ import annotations


class ResponseAgent:
    """Produces the final user-facing investigation response."""

    def __init__(self, router):
        self.router = router

    def run(
        self,
        user_text: str,
        pattern_analysis: str,
        contradiction_analysis: str,
        judge_assessment: str,
        evidence: list,
    ) -> str:
        evidence_text = self._format_evidence(evidence)

        prompt = f"""
You are the response agent for ScamHunter AI.

Answer the user's investigation request using ONLY the supplied analysis
and evidence.

Your response must:

1. Start with a clear, concise assessment.
2. Explain the main indicators or evidence.
3. Clearly distinguish verified information from claims or uncertainty.
4. Never invent facts, sources, URLs, organizations, names, dates, or statistics.
5. Never claim certainty when the evidence does not establish certainty.
6. Give practical verification and safety steps.
7. Tell the user what additional information would help if evidence is insufficient.
8. Keep the language understandable for a general user.

When referencing evidence, use labels such as:
- Knowledge Base Evidence
- Web Evidence
- User-provided information

Do not fabricate citations.

USER REQUEST:
{user_text}

SCAM-PATTERN ANALYSIS:
{pattern_analysis}

CONTRADICTION CHECK:
{contradiction_analysis}

EVIDENCE REVIEW:
{judge_assessment}

AVAILABLE EVIDENCE:
{evidence_text}
"""

        try:
            result = self.router.best_available(
                prompt,
                system=(
                    "You are ScamHunter AI's final response writer. "
                    "Be factual, cautious, concise, and useful."
                ),
                prefer_gemini=False,
            )
            return result.text.strip()

        except Exception as exc:
            return (
                "I could not generate the investigation response reliably. "
                f"Reason: {exc}"
            )

    @staticmethod
    def _format_evidence(evidence: list) -> str:
        if not evidence:
            return "No evidence available."

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
