from uuid import uuid4

from app.retrieval.qdrant_client import get_qdrant_client
from app.retrieval.embeddings import embeddings

client = get_qdrant_client()


def add_document(text: str):

    vector = embeddings.embed_query(text)

    client.upsert(
        collection_name="documents",
        points=[
            {
                "id": str(uuid4()),
                "vector": vector,
                "payload": {
                    "text": text
                }
            }
        ]
    )
