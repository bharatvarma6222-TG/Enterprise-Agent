from langchain_ollama import ChatOllama

from app.llm.langchain_provider import LangChainProvider


class OllamaProvider(LangChainProvider):

    def __init__(self, config):

        super().__init__(

            ChatOllama(

                model=config.model,

                base_url=config.base_url,

                temperature=config.temperature,
            )

        )
