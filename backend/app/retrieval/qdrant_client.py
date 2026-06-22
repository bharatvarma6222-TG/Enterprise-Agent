from qdrant_client import QdrantClient
from app.core.config import settings

client = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY
)


def get_qdrant_client():
    return client
