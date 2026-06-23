# backend/check_collection.py

from app.retrieval.qdrant_client import get_qdrant_client

client = get_qdrant_client()

info = client.get_collection("documents")

print(info)
