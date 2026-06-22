from fastapi import APIRouter

from app.models.chat_models import ChatRequest
from app.graph.workflow import graph

router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest):

    result = graph.invoke(
        {
            "query": request.query,
            "web_results": "",
            "answer": ""
        }
    )

    return {
        "answer": result["answer"]
    }
