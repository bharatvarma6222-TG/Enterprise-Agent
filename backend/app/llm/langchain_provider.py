from app.llm.base import BaseLLM


class LangChainProvider(BaseLLM):

    def __init__(self, llm):

        self.llm = llm

    def invoke(self, prompt):

        return self.llm.invoke(prompt)

    def stream(self, prompt):

        return self.llm.stream(prompt)
