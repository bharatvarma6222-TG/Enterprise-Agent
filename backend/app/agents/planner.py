from app.core.llm import llm
import ast


def create_plan(query: str):

    prompt = f"""
You are a research planning agent.

Break the user's request into smaller research tasks.

Return ONLY a Python list.

Example:
[
    "Research LangGraph features",
    "Research CrewAI features",
    "Compare LangGraph and CrewAI architectures"
]

User Request:
{query}
"""

    response = llm.invoke(prompt)

    try:
        return ast.literal_eval(
            response.content
        )
    except Exception:
        return [
            response.content
        ]
