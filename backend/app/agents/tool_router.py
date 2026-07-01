from app.llm.manager import llm


VALID_TOOLS = {
    "calculator",
    "memory",
    "pdf",
    "search",
}


def select_tool(query: str):

    prompt = f"""
You are an AI router.

Choose EXACTLY ONE tool.

Available tools:

calculator
memory
pdf
search

Rules:

- calculator -> arithmetic, equations, percentages, maths
- memory -> questions about previous conversation
- pdf -> uploaded document questions
- search -> facts, knowledge, research

Return ONLY ONE WORD.

Question:

{query}
"""

    response = llm.invoke(prompt)

    tool = response.content.strip().lower()

    tool = tool.replace(".", "").replace('"', "")

    if tool not in VALID_TOOLS:
        tool = "search"

    return tool
