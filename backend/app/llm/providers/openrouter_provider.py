from langchain_openai import ChatOpenAI

from app.llm.langchain_provider import LangChainProvider


class OpenRouterProvider(LangChainProvider):

    def __init__(self, config):

        super().__init__(

            ChatOpenAI(

                base_url="https://openrouter.ai/api/v1",

                api_key=config.api_key,

                model=config.model,

                temperature=config.temperature,
            )

        )
