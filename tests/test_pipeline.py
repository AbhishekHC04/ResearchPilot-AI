from unittest.mock import MagicMock, patch

import pytest

from src.researchpilot.pipeline import ResearchPipeline


def test_ingest_pdf_extracts_chunks_and_builds_index():
    pipeline = ResearchPipeline()

    fake_pages = [
        {
            "source": "sample.pdf",
            "page_number": 1,
            "text": "Machine learning helps computers learn from data.",
        }
    ]

    fake_chunks = [
        {
            "chunk_id": 0,
            "source": "sample.pdf",
            "page_number": 1,
            "text": "Machine learning helps computers learn from data.",
        }
    ]

    with (
        patch("src.researchpilot.pipeline.extract_pdf_pages", return_value=fake_pages),
        patch("src.researchpilot.pipeline.chunk_pages", return_value=fake_chunks),
    ):
        pipeline.search_engine = MagicMock()
        count = pipeline.ingest_pdf("sample.pdf")

    assert count == 1
    assert pipeline.chunks == fake_chunks
    pipeline.search_engine.build_index.assert_called_once_with(fake_chunks)


def test_search_delegates_to_search_engine():
    pipeline = ResearchPipeline()
    expected = [{"source": "sample.pdf", "page_number": 1}]

    pipeline.search_engine = MagicMock()
    pipeline.search_engine.search.return_value = expected

    result = pipeline.search("What is machine learning?", top_k=2)

    assert result == expected
    pipeline.search_engine.search.assert_called_once_with(
        "What is machine learning?",
        top_k=2,
    )
