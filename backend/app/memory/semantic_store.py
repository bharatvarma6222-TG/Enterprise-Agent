import uuid

from app.retrieval.embeddings import embeddings
from app.retrieval.qdrant_client import client

MEMORY_COLLECTION = "semantic_memory"


def save_fact(fact: str):

    vector = embeddings.embed_query(
        fact
    )

    client.upsert(
        collection_name=MEMORY_COLLECTION,
        points=[
            {
                "id": str(uuid.uuid4()),
                "vector": vector,
                "payload": {
                    "memory": fact
                }
            }
        ]
    )
