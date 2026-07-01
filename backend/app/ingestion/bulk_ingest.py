from pathlib import Path

from app.ingestion.ingest_pipeline import (
    ingest_pdf
)


def ingest_folder(folder):

    pdfs = Path(folder).glob(
        "*.pdf"
    )

    total = 0

    for pdf in pdfs:

        print(
            f"Ingesting {pdf.name}"
        )

        count = ingest_pdf(
            str(pdf)
        )

        total += count

    print(
        f"\nTotal Chunks Indexed: {total}"
    )

    return total
