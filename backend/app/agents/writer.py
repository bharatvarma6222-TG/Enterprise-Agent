from app.llm.manager import llm


def write_report(query, research, critique):

    prompt = f"""
You are a senior AI research writer.

Use ONLY the provided sources.

Whenever making a factual claim,
append:

[SOURCE: source_name | chunk_id]

If the Research says exactly 'I couldn't find relevant information in the uploaded documents.', output ONLY that exact message. Do not generate an Executive Summary, Detailed Findings, or Sources. Stop generating immediately.

Knowledge:

{research}

Question:

{query}
"""

    response = llm.invoke(prompt)

    return response.content
