import uuid

from qdrant_client.models import PointStruct

from app.retrieval.qdrant_client import client
from app.retrieval.embeddings import embeddings

from app.ingestion.pdf_loader import load_pdf
from app.ingestion.chunker import chunk_documents


def ingest_pdf(path: str, session_id: str):

    docs = load_pdf(path)

    chunks = chunk_documents(docs)

    points = []

    for i, chunk in enumerate(chunks):

        text = chunk.page_content

        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embeddings.embed_query(text),
                payload={
                    "text": text,
                    "source": path,
                    "chunk_id": i,
                    "session_id": session_id
                }
            )
        )

    client.upsert(
        collection_name="documents",
        points=points
    )

    return len(points)
