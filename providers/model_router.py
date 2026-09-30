from __future__ import annotations
from providers.groq_provider import GroqProvider
from providers.gemini_provider import GeminiProvider
from config.settings import Settings
from config.models import ModelResult

class ModelRouter:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.groq = GroqProvider(settings.groq_api_key, settings.groq_model)
        self.gemini = GeminiProvider(settings.gemini_api_key, settings.gemini_models)

    def groq_complete(self, prompt: str, system: str = "", temperature: float = 0.2) -> ModelResult:
        return self.groq.complete(prompt, system, temperature)

    def gemini_complete(self, prompt: str, system: str = "", temperature: float = 0.2) -> ModelResult:
        return self.gemini.complete(prompt, system, temperature)

    def best_available(self, prompt: str, system: str = "", prefer_gemini: bool = False) -> ModelResult:
        if prefer_gemini and self.settings.gemini_api_key:
            try:
                return self.gemini_complete(prompt, system)
            except Exception:
                pass
        return self.groq_complete(prompt, system)
