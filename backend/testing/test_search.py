# test_search.py

from app.retrieval.search import vector_search

results = vector_search(
    "What is LangGraph?"
)

print(results)
