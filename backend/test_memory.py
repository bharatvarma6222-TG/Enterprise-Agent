from app.memory.short_term import (
    add_message,
    get_messages
)

session_id = "demo"

add_message(
    session_id,
    "user",
    "My name is Bharat"
)

add_message(
    session_id,
    "assistant",
    "Nice to meet you Bharat"
)

print(
    get_messages(session_id)
)
