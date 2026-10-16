def chunk_pages(
    pages: list[dict],
    chunk_size: int = 1000,
    overlap: int = 150,
) -> list[dict]:
    """
    Split extracted PDF pages into overlapping text chunks.

    Each chunk retains its source filename and page number.
    Chunk sizes and overlap are measured in characters.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be non-negative and smaller than chunk_size.")

    chunks = []
    chunk_id = 0

    for page in pages:
        text = page.get("text", "").strip()

        if not text:
            continue

        start = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    {
                        "chunk_id": chunk_id,
                        "source": page["source"],
                        "page_number": page["page_number"],
                        "text": chunk_text,
                    }
                )
                chunk_id += 1

            if end == len(text):
                break

            start = end - overlap

    return chunks
