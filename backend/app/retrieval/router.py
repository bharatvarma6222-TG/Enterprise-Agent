from app.retrieval.search import vector_search
from app.tools.tavily_tool import search_web


def retrieve(query: str):

    local_results = vector_search(query)

    local_context = []

    for point in local_results.points:
        local_context.append(
            point.payload["text"]
        )

    web_results = search_web(query)

    return {
        "local": local_context,
        "web": web_results
    }
