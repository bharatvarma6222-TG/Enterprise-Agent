from app.graph.workflow import graph

result = graph.invoke(
    {
        "query": "Who is Odin?",
        "session_id": "bharat",

        "citations": [],
        "logs": [],
        "metrics": {}
    }
)
print(result["answer"])
