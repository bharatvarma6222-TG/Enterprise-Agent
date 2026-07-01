from fastapi import APIRouter, UploadFile, File
import shutil
import os

from app.ingestion.ingest_pipeline import ingest_pdf

router = APIRouter()

UPLOAD_DIR = "uploaded_docs"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    filepath = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(
        filepath,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    chunks = ingest_pdf(
        filepath
    )

    return {
        "uploaded": file.filename,
        "chunks_indexed": chunks
    }
