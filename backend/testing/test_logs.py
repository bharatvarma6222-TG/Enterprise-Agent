from app.graph.workflow import graph

result = graph.invoke(
    {
        "query": "What is Sekiro posture system?",
        "session_id": "bharat"
    }
)

print("\nANSWER:\n")
print(result["answer"])

print("\nLOGS:\n")

for log in result["logs"]:
    print(log)
