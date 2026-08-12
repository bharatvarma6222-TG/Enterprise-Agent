from qdrant_client import QdrantClient
from qdrant_client.http import models

from app.core.config import settings

COLLECTION_NAME = "documents_v2"

client = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY
)

print("=" * 80)
print("QDRANT_URL =", repr(settings.QDRANT_URL))
print("QDRANT_API_KEY =", settings.QDRANT_API_KEY[:10] + "...")
print("=" * 80)


def create_indexes():

    try:

        collections = [
            c.name
            for c in client.get_collections().collections
        ]

        if COLLECTION_NAME not in collections:

            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=models.VectorParams(
                    size=1024,
                    distance=models.Distance.COSINE,
                )
            )

        client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name="source",
            field_schema=models.PayloadSchemaType.KEYWORD,
        )

        client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name="session_id",
            field_schema=models.PayloadSchemaType.KEYWORD,
        )

    except Exception as e:

        print("Qdrant setup:", e)


create_indexes()


def get_qdrant_client():
    return client
