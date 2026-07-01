from langchain_anthropic import ChatAnthropic

from app.llm.langchain_provider import LangChainProvider


class AnthropicProvider(LangChainProvider):

    def __init__(self, config):

        super().__init__(

            ChatAnthropic(

                model=config.model,

                api_key=config.api_key,

                temperature=config.temperature,

                max_tokens=config.max_tokens,
            )

        )
