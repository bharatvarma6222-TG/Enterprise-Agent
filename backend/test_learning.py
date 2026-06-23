from app.graph.workflow import graph

graph.invoke(
    {
        "query": "I prefer Groq over OpenAI",
        "session_id": "bharat"
    }
)

print("learning complete")
