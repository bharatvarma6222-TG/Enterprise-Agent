from app.graph.workflow import graph

result = graph.invoke(
    {
        "query": "What is LangGraph?",
        "session_id": "bharat"
    }
)

print(result["answer"])
