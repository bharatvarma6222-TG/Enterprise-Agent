from collections import defaultdict

# In-memory conversation storage
chat_db = defaultdict(list)


def add_message(session_id: str, role: str, content: str):
    """
    Store a chat message.
    """
    chat_db[session_id].append(
        {
            "role": role,
            "content": content
        }
    )


def get_session(session_id: str):
    """
    Get all messages for one session.
    """
    return chat_db.get(session_id, [])


def get_all_sessions():
    """
    Return all session IDs.
    """
    return list(chat_db.keys())


def clear_session(session_id: str):
    """
    Delete one conversation.
    """
    if session_id in chat_db:
        del chat_db[session_id]
