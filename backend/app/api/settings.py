from fastapi import APIRouter

from app.llm.manager import llm
from app.llm.config import LLMConfig

router = APIRouter()


@router.get("/llm")
def get_llm():

    return llm.current_config()


@router.post("/llm")
def update_llm(config: LLMConfig):

    llm.set_provider(config)

    return {
        "success": True,
        "provider": config.provider,
        "model": config.model,
    }
