from app.ingestion.ingest_pipeline import ingest_pdf

count = ingest_pdf(
    "sample.pdf"
)

print(
    f"{count} chunks indexed"
)
