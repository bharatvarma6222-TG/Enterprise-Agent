from langchain_openai import ChatOpenAI

from app.llm.langchain_provider import LangChainProvider


class LMStudioProvider(LangChainProvider):

    def __init__(self, config):

        super().__init__(

            ChatOpenAI(

                base_url=config.base_url,

                api_key="lm-studio",

                model=config.model,

                temperature=config.temperature,
            )

        )
