from src.researchpilot.semantic_search import SemanticSearch


def test_retrieves_relevant_research_passage():
    engine = SemanticSearch()

    chunks = [
        {
            "chunk_id": 0,
            "source": "climate.pdf",
            "page_number": 2,
            "text": (
                "Climate change increases average global temperatures "
                "and can intensify extreme weather events."
            ),
        },
        {
            "chunk_id": 1,
            "source": "machine_learning.pdf",
            "page_number": 5,
            "text": (
                "Machine learning algorithms learn patterns from data "
                "to make predictions on new examples."
            ),
        },
        {
            "chunk_id": 2,
            "source": "space.pdf",
            "page_number": 3,
            "text": (
                "Astronomers study distant galaxies, stars, and planets "
                "using telescopes and observations."
            ),
        },
    ]

    engine.build_index(chunks)
    results = engine.search(
        "How does climate change affect temperatures?",
        top_k=2,
    )

    assert len(results) == 2
    assert results[0]["source"] == "climate.pdf"
    assert results[0]["page_number"] == 2
    assert results[0]["similarity"] > 0
