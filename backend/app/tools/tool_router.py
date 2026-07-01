from app.llm.manager import llm


def select_tool(query):

    prompt = f"""
You are a router.

Choose ONE word only.

calculator
memory
pdf
search

Question:
{query}

Return ONLY one word.
"""

    response = llm.invoke(prompt)

    print("="*60)
    print("RAW TOOL OUTPUT")
    print(repr(response.content))
    print("="*60)

    return response.content.strip().lower()
