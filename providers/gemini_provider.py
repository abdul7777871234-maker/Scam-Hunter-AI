from __future__ import annotations

from config.models import ModelResult


class GeminiProvider:
    """
    Gemini provider with automatic model fallback.

    Models are tried in the order supplied by Settings.
    """

    def __init__(
        self,
        api_key: str,
        models: tuple[str, ...],
    ):
        self.api_key = api_key
        self.models = models
        self.client = None

        if api_key:
            try:
                from google import genai

                self.client = genai.Client(
                    api_key=api_key
                )

            except Exception:
                self.client = None

    def complete(
        self,
        prompt: str,
        system: str = "",
        temperature: float = 0.2,
    ) -> ModelResult:

        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured."
            )

        if not self.client:
            raise RuntimeError(
                "Gemini SDK could not be initialized."
            )

        full_prompt = (
            f"{system}\n\n{prompt}"
            if system
            else prompt
        )

        errors = []

        for index, model in enumerate(self.models):

            try:
                # Gemini 3.8 migration:
                # Do not send temperature/top_p/top_k.
                response = self.client.models.generate_content(
                    model=model,
                    contents=full_prompt,
                )

                text = getattr(
                    response,
                    "text",
                    None,
                ) or ""

                if not text.strip():
                    raise RuntimeError(
                        "Gemini returned an empty response."
                    )

                return ModelResult(
                    text=text.strip(),
                    provider="gemini",
                    model=model,
                    fallback_used=(index > 0),
                )

            except Exception as exc:
                errors.append(
                    f"{model}: {str(exc).strip()}"
                )
                continue

        raise RuntimeError(
            "All Gemini models failed. "
            + " | ".join(errors)
        )
