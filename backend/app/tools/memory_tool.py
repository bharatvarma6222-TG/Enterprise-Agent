from app.memory.semantic_store import search_memory


def memory_search(query):

    try:
        results = search_memory(query)
    except Exception as e:
        print("Memory search failed:", e)
        return ""

    return str(results)
