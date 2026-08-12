from qdrant_client.http import models

from app.retrieval.qdrant_client import (
    get_qdrant_client,
    COLLECTION_NAME,
)
from app.retrieval.embeddings import embeddings

client = get_qdrant_client()


def vector_search(
    query,
    session_id=None,
    score_threshold=0.0,
):
    print("=" * 80)
    print("VECTOR SEARCH START")
    print("Query:", query)
    print("Session:", session_id)
    print("=" * 80)

    # -----------------------------
    # Embedding
    # -----------------------------
    print("Before embeddings...")

    query_vector = embeddings.embed_query(query)

    print("After embeddings.")

    # -----------------------------
    # Session Filter
    # -----------------------------
    query_filter = None

    if session_id:
        query_filter = models.Filter(
            must=[
                models.FieldCondition(
                    key="session_id",
                    match=models.MatchValue(
                        value=session_id,
                    ),
                )
            ]
        )

    print("=" * 80)
    print("USING COLLECTION:", COLLECTION_NAME)
    print("FILTER:", query_filter)
    print("=" * 80)

    # -----------------------------
    # DEBUG: Count collection
    # -----------------------------
    try:
        count = client.count(
            collection_name=COLLECTION_NAME
        )

        print("TOTAL VECTORS:", count.count)

    except Exception as e:
        print("COUNT ERROR:", e)

    # -----------------------------
    # DEBUG: Show first few payloads
    # -----------------------------
    try:

        points, _ = client.scroll(
            collection_name=COLLECTION_NAME,
            limit=3,
            with_payload=True,
        )

        print("=" * 80)
        print("FIRST STORED RECORDS")
        print("=" * 80)

        for p in points:
            print(p.payload)
            print("-" * 60)

    except Exception as e:
        print("SCROLL ERROR:", e)

    # -----------------------------
    # Qdrant Search
    # -----------------------------
    print("Before Qdrant query...")

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        query_filter=query_filter,
        score_threshold=score_threshold,
        limit=5,
        with_payload=True,
    )

    print("After Qdrant query.")

    print("=" * 80)
    print("FOUND POINTS:", len(results.points))
    print("=" * 80)

    docs = []

    for point in results.points:

        print(
            "Score:",
            point.score,
            "| Source:",
            point.payload.get("source"),
            "| Session:",
            point.payload.get("session_id"),
        )

        docs.append(
            {
                "text": point.payload.get("text", ""),
                "source": point.payload.get("source"),
                "chunk_id": point.payload.get("chunk_id"),
                "score": point.score,
            }
        )

    return docs


def search_by_filename(
    filename,
    session_id=None,
):
    print("=" * 80)
    print("FILENAME SEARCH")
    print("Filename:", filename)
    print("Session:", session_id)
    print("=" * 80)

    must_conditions = [
        models.FieldCondition(
            key="source",
            match=models.MatchText(
                text=f"uploads/{filename}"
            ),
        )
    ]

    if session_id:
        must_conditions.append(
            models.FieldCondition(
                key="session_id",
                match=models.MatchValue(
                    value=session_id,
                ),
            )
        )

    print("Before Qdrant scroll...")

    results, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        scroll_filter=models.Filter(
            must=must_conditions,
        ),
        limit=100,
        with_payload=True,
    )

    print("After Qdrant scroll.")

    docs = []

    for point in results:

        docs.append(
            {
                "text": point.payload.get("text", ""),
                "source": point.payload.get("source"),
                "chunk_id": point.payload.get("chunk_id"),
                "score": 1.0,
            }
        )

    print("=" * 80)
    print(f"Filename search found {len(docs)} chunks.")
    print("=" * 80)

    return docs