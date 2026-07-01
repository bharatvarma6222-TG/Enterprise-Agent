from app.retrieval.search import vector_search

results = vector_search(
    "What is this document about?"
)

print(results)
