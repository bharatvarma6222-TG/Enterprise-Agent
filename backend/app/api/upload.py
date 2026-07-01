from app.ingestion.ingest_pipeline import ingest_pdf
import uuid
import shutil
import os
from fastapi import (
    APIRouter,
    UploadFile,
    File
)
print("UPLOAD ROUTER LOADED")


router = APIRouter()


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    os.makedirs("uploads", exist_ok=True)

    session_id = str(uuid.uuid4())

    path = f"uploads/{file.filename}"

    with open(path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    chunks = ingest_pdf(
        path,
        session_id
    )

    print("=" * 60)
    print("UPLOAD SESSION:", session_id)
    print("=" * 60)

    return {
        "uploaded": file.filename,
        "chunks": chunks,
        "session_id": session_id
    }
