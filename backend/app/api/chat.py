from fastapi import APIRouter

from app.graph.workflow import graph
from app.graph.workflow import ChatRequest

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("")
async def chat(request: ChatRequest):

    result = graph.invoke(
        {
            "query": request.query,
            "session_id": request.session_id
        }
    )

    return {
        "answer": result["answer"],
        "logs": result["logs"],
        "metrics": result.get("metrics", {})
    }
