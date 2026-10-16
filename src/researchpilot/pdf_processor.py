from pathlib import Path

import pymupdf


def extract_pdf_pages(pdf_path: str | Path) -> list[dict]:
    """Extract text from a PDF while preserving page numbers."""
    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("The provided file must be a PDF.")

    pages = []

    with pymupdf.open(path) as document:
        if document.is_encrypted:
            raise ValueError("Encrypted PDFs are not supported.")

        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text").strip()

            if text:
                pages.append(
                    {
                        "page_number": page_number,
                        "text": text,
                        "source": path.name,
                    }
                )

    if not pages:
        raise ValueError(
            "No extractable text found. The PDF may be scanned "
            "and require OCR."
        )

    return pages
