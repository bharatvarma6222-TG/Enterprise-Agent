from fastapi import APIRouter

from app.memory.chat_history import (
    get_session,
    get_all_sessions,
    clear_session
)

router = APIRouter(
    prefix="/session",
    tags=["Session"]
)


@router.get("/list")
def list_sessions():
    return get_all_sessions()


@router.get("/{session_id}")
def session(session_id: str):
    return get_session(session_id)


@router.delete("/{session_id}")
def delete_session(session_id: str):
    clear_session(session_id)

    return {
        "status": "deleted"
    }
