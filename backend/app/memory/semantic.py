from uuid import uuid4

from app.retrieval.qdrant_client import get_qdrant_client
from app.retrieval.embeddings import embeddings

client = get_qdrant_client()

COLLECTION = "semantic_memory"


def store_memory(memory_text: str):

    vector = embeddings.embed_query(
        memory_text
    )

    client.upsert(
        collection_name=COLLECTION,
        points=[
            {
                "id": str(uuid4()),
                "vector": vector,
                "payload": {
                    "memory": memory_text
                }
            }
        ]
    )


def recall_memory(query: str):

    query_vector = embeddings.embed_query(
        query
    )

    results = client.query_points(
        collection_name=COLLECTION,
        query=query_vector,
        limit=3
    )

    return results
