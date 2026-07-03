from qdrant_client.models import (
    Distance,
    VectorParams
)

from app.retrieval.qdrant_client import (
    get_qdrant_client
)

client = get_qdrant_client()

client.create_collection(
    collection_name="semantic_memory",
    vectors_config=VectorParams(
        size=1536,
        distance=Distance.COSINE
    )
)

print("Semantic collection created.")
