from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.core.config import settings

client = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY
)

client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(
        size=1536,
        distance=Distance.COSINE
    )
)

print("Collection Created")
