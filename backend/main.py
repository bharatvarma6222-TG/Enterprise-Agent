from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.api.stream import router as stream_router
from app.api.upload import router as upload_router
from app.api.files import router as files_router
from app.api.memory import router as memory_router
from app.api.session import router as session_router
from app.api.settings import router as settings_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Enterprise Agent Gateway"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat_router)
app.include_router(stream_router)
app.include_router(upload_router)
app.include_router(files_router)
app.include_router(memory_router)
app.include_router(session_router)

app.include_router(
    settings_router,
    prefix="/settings",
    tags=["Settings"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
