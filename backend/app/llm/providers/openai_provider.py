from langchain_openai import ChatOpenAI

from app.llm.langchain_provider import LangChainProvider


class OpenAIProvider(LangChainProvider):

    def __init__(self, config):

        super().__init__(

            ChatOpenAI(

                model=config.model,

                temperature=config.temperature,

                max_tokens=config.max_tokens,

                api_key=config.api_key,
            )

        )
