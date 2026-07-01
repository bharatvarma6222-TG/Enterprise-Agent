from app.llm.providers.openai_provider import OpenAIProvider
from app.llm.providers.groq_provider import GroqProvider


class LLMFactory:

    @staticmethod
    def create(config):

        if config.provider == "openai":
            return OpenAIProvider(config)

        elif config.provider == "groq":
            return GroqProvider(config)

        raise ValueError(
            f"Unknown provider: {config.provider}"
        )
