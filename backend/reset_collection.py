# backend/reset_collection.py

from qdrant_client.models import VectorParams
from qdrant_client.models import Distance

from app.retrieval.qdrant_client import get_qdrant_client

client = get_qdrant_client()

client.delete_collection(
    collection_name="documents"
)

client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)

print("Collection recreated.")
