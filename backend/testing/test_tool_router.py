from app.graph.workflow import graph

result = graph.invoke(
    {
        "query": "What is Sekiro's posture system?",
        "session_id": "bharat"
    }
)

print(result["answer"])
