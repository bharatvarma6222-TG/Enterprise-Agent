from app.core.llm import llm


def critique_answer(
    question,
    context,
    answer
):

    prompt = f"""
Question:
{question}

Context:
{context}

Answer:
{answer}

Check if answer is grounded.

If incorrect explain why.

If correct return PASS.
"""

    response = llm.invoke(prompt)

    return response.content
