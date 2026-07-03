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
        collection_name="documents_v2",
        points=points
    )

    count = client.count(
        collection_name="documents_v2"
    )

    print("=" * 60)
    print("TOTAL VECTORS:", count.count)
    print("=" * 60)

    points, _ = client.scroll(
        collection_name="documents_v2",
        limit=5,
        with_payload=True
    )

    print("=" * 60)
    print("FIRST STORED PAYLOADS")
    for p in points:
        print(p.payload)
        print("=" * 60)
        points, _ = client.scroll(
            collection_name="documents_v2",
            limit=5,
            with_payload=True
        )

    for p in points:
        print(p.payload)

    count = client.count(
        collection_name="documents_v2"
    )

    print("=" * 60)
    print("TOTAL VECTORS IN DOCUMENTS:", count.count)
    print("=" * 60)

    return len(points)
