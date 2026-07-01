from app.llm.manager import llm


def evaluate_answer(
    question,
    retrieval_context,
    answer,
):
    prompt = f"""
You are an AI evaluator.

Question:
{question}

Knowledge:
{retrieval_context}

Answer:
{answer}

Evaluate ONLY using the supplied knowledge.

Score from 0-10:

1. Groundedness
2. Completeness
3. Hallucination Risk (Low/Medium/High)
4. Confidence (0-100)

Return ONLY JSON.

Example:

{{
"groundedness":9,
"completeness":8,
"hallucination":"Low",
"confidence":94
}}
"""

    response = llm.invoke(prompt)

    return response.content
