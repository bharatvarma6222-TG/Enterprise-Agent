from app.retrieval.embeddings import embeddings

vector = embeddings.embed_query(
    "hello world"
)

print(len(vector))
