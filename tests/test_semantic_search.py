from unittest.mock import MagicMock

import numpy as np
import pytest

from src.researchpilot.semantic_search import SemanticSearch


@pytest.fixture
def search_engine():
    engine = SemanticSearch.__new__(SemanticSearch)
    engine.model = MagicMock()
    engine.index = None
    engine.chunks = []
    return engine


def test_build_index_rejects_empty_chunks(search_engine):
    with pytest.raises(ValueError, match="At least one"):
        search_engine.build_index([])


def test_search_requires_index(search_engine):
    with pytest.raises(RuntimeError, match="Build the index"):
        search_engine.search("What is machine learning?")


def test_search_rejects_empty_query(search_engine):
    search_engine.index = MagicMock()

    with pytest.raises(ValueError, match="must not be empty"):
        search_engine.search("   ")


def test_search_rejects_invalid_top_k(search_engine):
    search_engine.index = MagicMock()

    with pytest.raises(ValueError, match="at least 1"):
        search_engine.search("What is machine learning?", top_k=0)
