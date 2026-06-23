from app.core.llm import llm


def extract_fact(text: str):

    prompt = f"""
Extract ONLY a user preference, fact, skill, tool preference,
or persistent information.

If nothing important exists return:

NONE

Text:
{text}
"""

    response = llm.invoke(prompt)

    fact = response.content.strip()

    return fact
