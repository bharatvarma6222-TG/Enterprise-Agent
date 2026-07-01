from app.guardrails.policy import (
    PROMPT_INJECTION_PATTERNS,
    SAFETY_PATTERNS,
)

MAX_QUERY_LENGTH = 5000


def validate_query(query: str):

    q = query.lower().strip()

    if len(q) > MAX_QUERY_LENGTH:
        return False, "Query is too long."

    # Prompt injection
    for pattern in PROMPT_INJECTION_PATTERNS:

        if pattern in q:
            return (
                False,
                "Prompt injection attempt detected."
            )

    # Unsafe requests
    for pattern in SAFETY_PATTERNS:

        if pattern in q:
            return (
                False,
                "This request violates security policies."
            )

    return True, None
