from qdrant_client.models import (
    VectorParams,
    Distance
)

from app.retrieval.qdrant_client import client

client.recreate_collection(
    collection_name="semantic_memory",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)

print("semantic memory ready")
