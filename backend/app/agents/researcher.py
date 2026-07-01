from app.llm.manager import llm


def research(query, context):

    prompt = f"""
You are a research agent.

Question:
{query}

Retrieved Information:
{context}

Extract the most useful facts.
If the retrieved context does not contain sufficient information or is '[]', respond EXACTLY with: 'I couldn't find relevant information in the uploaded documents.' Do not use prior knowledge. Do not guess.
"""

    response = llm.invoke(prompt)

    return response.content
