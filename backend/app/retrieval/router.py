from app.retrieval.search import (
    vector_search,
    search_by_filename
)

from app.retrieval.filename_search import extract_filename

from app.tools.tavily_tool import search_web


def retrieve(
    query,
    session_id=None
):

    filename = extract_filename(query)

    if filename:

        print("=" * 60)
        print("FILE SEARCH:", filename)
        print("=" * 60)

        local_results = search_by_filename(
            filename,
            session_id=session_id
        )

    else:

        print("=" * 60)
        print("VECTOR SEARCH")
        print("=" * 60)

        local_results = vector_search(
            query,
            session_id=session_id
        )

    try:

        web_results = search_web(query)

    except Exception as e:

        print("Web search failed:", e)

        web_results = []

    return {

        "local": local_results,

        "web": web_results

    }
