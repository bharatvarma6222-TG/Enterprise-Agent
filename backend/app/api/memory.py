from fastapi import APIRouter

from app.memory.semantic_store import (
    get_all_memories,
    delete_memory,
    delete_all_memories,
)

router = APIRouter(
    prefix="/memory",
    tags=["Memory"],
)


@router.get("/list")
def list_memory():
    return get_all_memories()


@router.delete("/{memory_id}")
def remove_memory(memory_id: str):
    delete_memory(memory_id)

    return {
        "status": "deleted"
    }


@router.delete("/all")
def remove_all():
    delete_all_memories()

    return {
        "status": "all memories deleted"
    }
