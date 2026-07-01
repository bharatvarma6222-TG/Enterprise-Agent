from app.memory.semantic_store import search_memory


def memory_search(query):

    memories = search_memory(query)

    return "\n".join(memories)
