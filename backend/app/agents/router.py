from app.llm.manager import llm


def route_query(query):

    prompt = f"""
Classify query.

Routes:

calculator
memory
research

Return ONLY route name.

Query:
{query}
"""

    response = llm.invoke(prompt)

    return response.content.strip().lower()
