import uuid
from datetime import datetime

from qdrant_client.models import (
    PointStruct,
    PointIdsList,
    VectorParams,
    Distance,
)

from app.retrieval.qdrant_client import client
from app.retrieval.embeddings import embeddings

from qdrant_client.http.exceptions import UnexpectedResponse


def ensure_memory_collection():
    try:
        client.get_collection("semantic_memory")
    except Exception:
        print("Creating semantic_memory collection...")

        client.create_collection(
            collection_name="semantic_memory",
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )
# -----------------------------
# Save Memory
# -----------------------------


def save_fact(fact: str, session_id: str = "global"):
    ensure_memory_collection()

    vector = embeddings.embed_query(fact)

    client.upsert(
        collection_name="semantic_memory",
        points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "text": fact,
                    "session_id": session_id,
                    "timestamp": str(datetime.now())
                }
            )
        ]
    )


# -----------------------------
# Semantic Search
# -----------------------------
def search_memory(query: str):
    ensure_memory_collection()

    query_vector = embeddings.embed_query(query)

    results = client.query_points(
        collection_name="semantic_memory",
        query=query_vector,
        limit=5
    )

    memories = []

    for point in results.points:

        memories.append(
            point.payload.get("text", "")
        )

    return memories


# -----------------------------
# List Memories
# -----------------------------
def get_all_memories():
    ensure_memory_collection()

    points, _ = client.scroll(
        collection_name="semantic_memory",
        limit=100
    )

    memories = []

    for point in points:

        payload = point.payload or {}

        memories.append(
            {
                "id": str(point.id),
                "text": payload.get("text", ""),
                "timestamp": payload.get("timestamp", "")
            }
        )

    return memories


# -----------------------------
# Delete One Memory
# -----------------------------
def delete_memory(memory_id: str):

    client.delete(
        collection_name="semantic_memory",
        points_selector=PointIdsList(
            points=[memory_id]
        )
    )


# -----------------------------
# Delete All Memories
# -----------------------------
def delete_all_memories():

    try:
        client.delete_collection(
            collection_name="semantic_memory"
        )
    except Exception:
        pass

    client.create_collection(
        collection_name="semantic_memory",
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )
