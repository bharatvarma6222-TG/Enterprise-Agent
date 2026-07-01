from app.llm.manager import llm
import ast


def create_plan(query: str):

    prompt = f"""
You are a planning agent.

If the request is SIMPLE
(greeting, math, memory question, single fact)

Return

["single_task"]

ONLY.

If it requires research or multiple steps,
break it into multiple tasks.

Return ONLY a Python list.

User:

{query}
"""

    response = llm.invoke(prompt)

    try:
        return ast.literal_eval(response.content)

    except Exception:

        return ["single_task"]
