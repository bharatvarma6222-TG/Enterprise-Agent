from pathlib import Path


def format_retrieval_context(results):

    formatted = []
    seen = set()

    for doc in results:

        source = Path(
            doc.get("source", "Unknown")
        ).as_posix()

        chunk = doc.get(
            "chunk_id",
            "Unknown"
        )

        key = (
            source,
            chunk
        )

        if key in seen:
            continue

        seen.add(key)

        formatted.append(
            f"""
SOURCE: {source}
CHUNK: {chunk}

CONTENT:
{doc["text"]}
"""
        )

    return "\n\n".join(formatted)
