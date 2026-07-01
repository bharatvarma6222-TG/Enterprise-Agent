from app.graph.workflow import graph

result = graph.invoke({
    "query": "Compare LangGraph and CrewAI",
    "session_id": "bharat"
})

print(result["answer"])
