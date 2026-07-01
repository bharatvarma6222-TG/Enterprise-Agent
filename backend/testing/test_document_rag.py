from app.retrieval.search import vector_search

results = vector_search(
    "What does the document talk about?"
)

print(results)
