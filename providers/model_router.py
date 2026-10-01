from __future__ import annotations

from providers.groq_provider import GroqProvider
from providers.gemini_provider import GeminiProvider
from config.settings import Settings
from config.models import ModelResult


class ModelRouter:
    """
    Provider router with bidirectional fallback.

    Preferred order:
        Gemini -> Groq
    or:
        Groq -> Gemini

    This prevents one provider/network restriction from breaking
    the entire investigation pipeline.
    """

    def __init__(self, settings: Settings):
        self.settings = settings

        self.groq = GroqProvider(
            settings.groq_api_key,
            settings.groq_model,
        )

        self.gemini = GeminiProvider(
            settings.gemini_api_key,
            settings.gemini_models,
        )

    def groq_complete(
        self,
        prompt: str,
        system: str = "",
        temperature: float = 0.2,
    ) -> ModelResult:
        return self.groq.complete(
            prompt,
            system,
            temperature,
        )

    def gemini_complete(
        self,
        prompt: str,
        system: str = "",
        temperature: float = 0.2,
    ) -> ModelResult:
        return self.gemini.complete(
            prompt,
            system,
            temperature,
        )

    def best_available(
        self,
        prompt: str,
        system: str = "",
        prefer_gemini: bool = False,
    ) -> ModelResult:

        attempts = []

        if prefer_gemini:
            providers = [
                ("gemini", self.gemini_complete),
                ("groq", self.groq_complete),
            ]
        else:
            providers = [
                ("groq", self.groq_complete),
                ("gemini", self.gemini_complete),
            ]

        for provider_name, provider_call in providers:
            try:
                result = provider_call(prompt, system)

                if result and result.text and result.text.strip():
                    if attempts:
                        result.fallback_used = True

                    return result

                attempts.append(
                    f"{provider_name}: empty response"
                )

            except Exception as exc:
                error = str(exc).strip()

                attempts.append(
                    f"{provider_name}: {error}"
                )

                continue

        details = " | ".join(attempts)

        raise RuntimeError(
            "All AI providers failed. "
            f"Attempts: {details}"
        )
