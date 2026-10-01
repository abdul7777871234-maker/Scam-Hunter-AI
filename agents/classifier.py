from __future__ import annotations


class ClassifierAgent:
    """Classifies an investigation request and decides which evidence sources are needed."""

    def __init__(self, router):
        self.router = router

    def run(self, user_text: str) -> dict:
        prompt = f"""
You are the classification agent for ScamHunter AI.

Analyze the user's request and return ONLY valid JSON with these keys:

{{
  "category": "one of: phishing, investment, job, romance, payment, shopping, identity_theft, giveaway, technical_support, crypto, other",
  "requires_rag": true,
  "requires_web": false,
  "risk_level": "low, medium, high, or unknown",
  "reason": "short explanation"
}}

Rules:
- Use the internal knowledge base when the request concerns scam patterns, investigation guidance, or known scam behavior.
- Set requires_web to true when current, external, source-level, domain-level, organization-level, link-level, or sender-level information would materially help investigate the request.
- For a suspicious message, link, offer, payment request, account warning, sender claim, organization claim, or other externally verifiable scam claim, prefer web research when practical.
- Do not decide that something is a scam solely from the user's wording.
- Do not invent facts.

USER REQUEST:
{user_text}
"""

        try:
            result = self.router.best_available(
                prompt,
                system="You are a precise scam-investigation classification agent. Return JSON only.",
                prefer_gemini=True,
            )

            data = self._parse(result.text)

        except Exception:
            data = {
                "category": "other",
                "requires_rag": True,
                "requires_web": False,
                "risk_level": "unknown",
                "reason": "Classification could not be completed reliably.",
            }

        # Deterministic safety net: external evidence discovery must not depend
        # entirely on the model classifier choosing requires_web=true.
        if self._web_signal(user_text):
            data["requires_web"] = True

        return data

    @staticmethod
    def _web_signal(text: str) -> bool:
        import re

        value = (text or "").lower()

        if re.search(
            r"https?://|www\.|\b[a-z0-9-]+\.(?:com|net|org|co|io|sa|pk|uk|gov|edu)\b",
            value,
        ):
            return True

        if re.search(r"\b(?:\+?\d[\d\s().-]{7,}\d)\b", value):
            return True

        web_terms = (
            "is this a scam",
            "is this legit",
            "is this legitimate",
            "verify this",
            "check this link",
            "investigate this link",
            "check this website",
            "check this domain",
            "who sent this",
            "bank",
            "payment",
            "account",
            "otp",
            "verification",
            "refund",
            "prize",
            "investment",
            "job offer",
            "delivery",
            "package",
            "whatsapp",
            "telegram",
            "crypto",
            "wallet",
        )

        return any(term in value for term in web_terms)

    @staticmethod
    def _parse(text: str) -> dict:
        import json

        cleaned = text.strip()
        fence = chr(96) * 3

        if cleaned.startswith(fence):
            cleaned = cleaned.replace(fence + "json", "", 1)
            cleaned = cleaned.replace(fence, "")
            cleaned = cleaned.strip()

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            return {
                "category": "other",
                "requires_rag": True,
                "requires_web": False,
                "risk_level": "unknown",
                "reason": "The classifier returned an invalid JSON response.",
            }

        return {
            "category": str(data.get("category", "other")),
            "requires_rag": bool(data.get("requires_rag", True)),
            "requires_web": bool(data.get("requires_web", False)),
            "risk_level": str(data.get("risk_level", "unknown")),
            "reason": str(data.get("reason", "")),
        }
