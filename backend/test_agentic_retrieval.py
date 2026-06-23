from app.graph.workflow import graph

result = graph.invoke(
    {
        "query": "Compare sekiro and god of war",
        "session_id": "bharat"
    }
)

print(result["answer"])
