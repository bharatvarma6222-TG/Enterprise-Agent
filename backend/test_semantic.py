from app.memory.semantic import (
    store_memory,
    recall_memory
)

store_memory(
    "User prefers Groq over OpenAI"
)

results = recall_memory(
    "Which LLM provider does the user prefer?"
)

print(results)
