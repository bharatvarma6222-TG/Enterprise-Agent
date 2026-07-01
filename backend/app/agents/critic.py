from app.llm.manager import llm


def critique(research):

    prompt = f"""
You are a critic agent.

Review this research.

Identify:
- missing information
- weak evidence
- contradictions

Research:
{research}
"""

    response = llm.invoke(prompt)

    return response.content
