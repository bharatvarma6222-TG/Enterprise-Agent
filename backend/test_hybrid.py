from app.retrieval.ingest import add_document
from app.retrieval.search import vector_search

add_document(
    "LangGraph is an orchestration framework for AI agents."
)

results = vector_search(
    "What is LangGraph?"
)

print(results)
