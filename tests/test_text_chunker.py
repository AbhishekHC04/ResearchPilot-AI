import pytest

from src.researchpilot.text_chunker import chunk_pages


def test_chunk_pages_preserves_source_and_page_number():
    pages = [
        {
            "source": "research.pdf",
            "page_number": 3,
            "text": "A" * 2500,
        }
    ]

    chunks = chunk_pages(pages, chunk_size=1000, overlap=150)

    assert len(chunks) == 3
    assert chunks[0]["source"] == "research.pdf"
    assert chunks[0]["page_number"] == 3
    assert chunks[0]["chunk_id"] == 0
    assert len(chunks[0]["text"]) == 1000
    assert chunks[1]["chunk_id"] == 1
    assert chunks[1]["text"].startswith("A" * 150)


def test_empty_pages_produce_no_chunks():
    pages = [
        {"source": "empty.pdf", "page_number": 1, "text": ""},
        {"source": "empty.pdf", "page_number": 2, "text": "   "},
    ]

    assert chunk_pages(pages) == []


def test_invalid_chunk_size_is_rejected():
    with pytest.raises(ValueError, match="chunk_size"):
        chunk_pages([], chunk_size=0)


def test_invalid_overlap_is_rejected():
    with pytest.raises(ValueError, match="overlap"):
        chunk_pages([], chunk_size=100, overlap=100)
