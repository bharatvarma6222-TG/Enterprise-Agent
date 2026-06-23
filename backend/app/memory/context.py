from app.memory.short_term import get_messages


def build_memory_context(
    session_id: str
):

    messages = get_messages(
        session_id
    )

    memory_text = ""

    for msg in messages:

        memory_text += (
            f"{msg['role']}: "
            f"{msg['content']}\n"
        )

    return memory_text
