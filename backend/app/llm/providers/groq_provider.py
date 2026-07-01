from langchain_groq import ChatGroq

from app.llm.langchain_provider import LangChainProvider


class GroqProvider(LangChainProvider):

    def __init__(self, config):

        super().__init__(

            ChatGroq(

                model=config.model,

                temperature=config.temperature,

                max_tokens=config.max_tokens,

                api_key=config.api_key,
            )

        )
