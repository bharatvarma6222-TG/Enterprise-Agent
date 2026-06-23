from app.retrieval.qdrant_client import get_qdrant_client
from app.retrieval.embeddings import embeddings

client = get_qdrant_client()


def vector_search(query):

    query_vector = embeddings.embed_query(query)

    results = client.query_points(
        collection_name="documents",
        query=query_vector,
        limit=5
    )

    return results
