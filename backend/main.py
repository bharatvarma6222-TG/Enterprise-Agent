from fastapi import FastAPI

from app.api.chat import router

app = FastAPI(
    title="Enterprise Agent Gateway"
)

app.include_router(router)
