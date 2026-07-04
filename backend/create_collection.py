from qdrant_client.models import VectorParams, Distance
from app.retrieval.qdrant_client import client

if client.collection_exists("documents_v2"):
    client.delete_collection("documents_v2")

client.create_collection(
    collection_name="documents_v2",
    vectors_config=VectorParams(
        size=1024,
        distance=Distance.COSINE,
    )
)

print("Fresh collection created.")
