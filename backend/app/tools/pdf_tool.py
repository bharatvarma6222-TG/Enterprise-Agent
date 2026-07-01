from app.retrieval.search import vector_search


def pdf_search(query, session_id=None):

    return vector_search(query, session_id=session_id)
