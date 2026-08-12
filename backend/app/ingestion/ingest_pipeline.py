import uuid

from qdrant_client.models import PointStruct

from app.retrieval.qdrant_client import client
from app.retrieval.embeddings import embeddings

from app.ingestion.pdf_loader import load_pdf
from app.ingestion.chunker import chunk_documents


def ingest_pdf(path: str, session_id: str):

    print("=" * 80)
    print("INGEST START")
    print(path)
    print("=" * 80)

    docs = load_pdf(path)

    print(f"Loaded pages: {len(docs)}")

    chunks = chunk_documents(docs)

    print(f"Generated chunks: {len(chunks)}")

    if len(chunks) == 0:
        print("❌ No chunks generated!")
        return 0

    points = []

    for i, chunk in enumerate(chunks):

        text = chunk.page_content

        vector = embeddings.embed_query(text)

        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "text": text,
                    "source": path,
                    "chunk_id": i,
                    "session_id": session_id,
                },
            )
        )

    print(f"Prepared {len(points)} vectors")

    try:

        print("Calling Qdrant upsert...")

        result = client.upsert(
            collection_name="documents_v2",
            points=points,
            wait=True,
        )

        print("UPSERT RESULT")
        print(result)

    except Exception as e:

        print("=" * 80)
        print("UPSERT FAILED")
        print(type(e).__name__)
        print(e)
        print("=" * 80)
        raise

    count = client.count(
        collection_name="documents_v2"
    )

    print("=" * 60)
    print("TOTAL VECTORS:", count.count)
    print("=" * 60)

    records, _ = client.scroll(
        collection_name="documents_v2",
        limit=5,
        with_payload=True,
    )

    print("=" * 60)
    print(f"FIRST {len(records)} STORED RECORDS")
    print("=" * 60)

    for r in records:
        print(r.payload)
        print("-" * 60)

    return len(points)