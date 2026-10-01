from __future__ import annotations

from config.models import ModelResult
from config.settings import Settings
from providers.gemini_provider import GeminiProvider
from providers.groq_provider import GroqProvider


class ModelRouter:
    """
    Central model router.

    Text generation:
        Groq <-> Gemini fallback

    Image analysis:
        Gemini with automatic model fallback

    The router never exposes API keys in returned errors.
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

    # ---------------------------------------------------------
    # DIRECT PROVIDER CALLS
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # BEST AVAILABLE TEXT MODEL
    # ---------------------------------------------------------

    def best_available(
        self,
        prompt: str,
        system: str = "",
        prefer_gemini: bool = False,
        temperature: float = 0.2,
    ) -> ModelResult:

        attempts: list[str] = []

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
                result = provider_call(
                    prompt,
                    system,
                    temperature,
                )

                if result and result.text and result.text.strip():
                    if attempts:
                        result.fallback_used = True

                    return result

                attempts.append(
                    f"{provider_name}: empty response"
                )

            except Exception as exc:
                message = self._safe_error(exc)

                attempts.append(
                    f"{provider_name}: {message}"
                )

        details = " | ".join(attempts)

        raise RuntimeError(
            "All AI providers failed. "
            f"Attempts: {details}"
        )

    # ---------------------------------------------------------
    # IMAGE ANALYSIS
    # ---------------------------------------------------------

    def describe_image(
        self,
        image_bytes: bytes,
        mime_type: str,
        prompt: str,
    ) -> ModelResult:
        """
        Analyze an image with Gemini.

        Gemini is used directly because the Groq provider in this
        repository is configured for text completion.
        """

        if not image_bytes:
            raise ValueError(
                "The uploaded image is empty."
            )

        return self.gemini.describe_image(
            image_bytes=image_bytes,
            mime_type=mime_type,
            prompt=prompt,
        )

    # ---------------------------------------------------------
    # ERROR SANITIZATION
    # ---------------------------------------------------------

    @staticmethod
    def _safe_error(exc: Exception) -> str:
        """
        Keep provider errors useful without leaking secrets.
        """

        message = str(exc).strip()

        if not message:
            return exc.__class__.__name__

        # Never expose obvious API-key material.
        sensitive_markers = (
            "gsk_",
            "AIza",
            "sk-",
            "Bearer ",
        )

        for marker in sensitive_markers:
            if marker in message:
                return (
                    f"{exc.__class__.__name__}: "
                    "provider authentication/request error"
                )

        # Avoid huge SDK trace payloads in the UI.
        if len(message) > 500:
            message = message[:500] + "..."

        return message
