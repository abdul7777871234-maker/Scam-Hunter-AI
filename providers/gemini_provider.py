from __future__ import annotations
from config.models import ModelResult

class GeminiProvider:
    def __init__(self, api_key: str, models: tuple[str, ...]):
        self.api_key = api_key
        self.models = models
        self.client = None
        if api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=api_key)
            except Exception:
                self.client = None

    def complete(self, prompt: str, system: str = "", temperature: float = 0.2) -> ModelResult:
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured.")
        if not self.client:
            raise RuntimeError("Gemini SDK could not be initialized.")
        full_prompt = f"{system}\n\n{prompt}" if system else prompt
        last_error = None
        for i, model in enumerate(self.models):
            try:
                response = self.client.models.generate_content(
                    model=model,
                    contents=full_prompt,
                    config={"temperature": temperature},
                )
                text = getattr(response, "text", None) or ""
                if not text.strip():
                    raise RuntimeError("Gemini returned an empty response.")
                return ModelResult(text, "gemini", model, fallback_used=(i > 0))
            except Exception as exc:
                last_error = exc
                continue
        raise RuntimeError(f"All Gemini fallback models failed: {last_error}")
