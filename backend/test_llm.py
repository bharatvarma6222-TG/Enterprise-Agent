from app.core.llm import llm

response = llm.invoke(
    "Explain LangGraph in one sentence."
)

print(response.content)
