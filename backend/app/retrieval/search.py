from qdrant_client.http import models

from app.retrieval.qdrant_client import get_qdrant_client
from app.retrieval.embeddings import embeddings

client = get_qdrant_client()


def vector_search(
    query,
    session_id=None,
    score_threshold=0.75
):

    query_vector = embeddings.embed_query(query)

    query_filter = None

    if session_id:

        query_filter = models.Filter(

            must=[

                models.FieldCondition(
                    key="session_id",
                    match=models.MatchValue(
                        value=session_id
                    )
                )

            ]

        )

    results = client.query_points(

        collection_name="documents",

        query=query_vector,

        query_filter=query_filter,

        score_threshold=score_threshold,

        limit=5,

        with_payload=True

    )

    docs = []

    for point in results.points:

        print(
            point.score,
            point.payload.get("source")
        )

        docs.append(

            {
                "text": point.payload["text"],
                "source": point.payload.get("source"),
                "chunk_id": point.payload.get("chunk_id"),
                "score": point.score,
            }

        )

    return docs


def search_by_filename(
    filename,
    session_id=None
):

    must_conditions = [

        models.FieldCondition(

            key="source",

            match=models.MatchText(
                text=f"uploads/{filename}"
            )

        )

    ]

    if session_id:

        must_conditions.append(

            models.FieldCondition(

                key="session_id",

                match=models.MatchValue(
                    value=session_id
                )

            )

        )

    results, _ = client.scroll(

        collection_name="documents",

        scroll_filter=models.Filter(
            must=must_conditions
        ),

        limit=100,

        with_payload=True

    )

    docs = []

    for point in results:

        docs.append(

            {
                "text": point.payload["text"],
                "source": point.payload.get("source"),
                "chunk_id": point.payload.get("chunk_id"),
                "score": 1.0,
            }

        )

    print(
        f"Filename search found {len(docs)} chunks."
    )

    return docs
