from app.core.config import settings
from app.llm.config import LLMConfig
from app.llm.factory import LLMFactory
from app.config.settings_manager import load_settings


class LLMManager:

    def __init__(self):

        self.config = LLMConfig(
            provider="groq",
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            max_tokens=4000,
            api_key=settings.GROQ_API_KEY,
        )

        self.provider = LLMFactory.create(self.config)

    def invoke(self, prompt):
        return self.provider.invoke(prompt)

    def stream(self, prompt):
        return self.provider.stream(prompt)

    def set_provider(self, config: LLMConfig):

        # Preserve existing API key if frontend doesn't send one
        if not config.api_key:
            config.api_key = self.config.api_key

        self.config = config
        self.provider = LLMFactory.create(config)

    def current_config(self):

        return {
            "provider": self.config.provider,
            "model": self.config.model,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "stream": self.config.stream,
        }

    def current_settings(self):
        return load_settings()

    def available_models(self, provider):

        provider = provider.lower()

        if provider == "groq":
            return self.groq.available_models()

        if provider == "openai":
            return self.openai.available_models()

        if provider == "gemini":
            return self.gemini.available_models()

        if provider == "ollama":
            return self.ollama.available_models()

        return []


llm = LLMManager()
