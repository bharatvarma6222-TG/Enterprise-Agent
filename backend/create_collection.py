from qdrant_client.models import VectorParams
from qdrant_client.models import Distance

from app.retrieval.qdrant_client import client

if client.collection_exists("documents"):
    client.delete_collection(
        "documents"
    )

client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)

print("fresh collection created")
