from src.researchpilot.answer_generator import validate_citations


def test_keeps_citation_mentioned_in_answer():
    answer = "Source: researchpilot_ai_ml_basics.pdf, Page: 2"
    sources = [
        {"source": "researchpilot_ai_ml_basics.pdf", "page_number": 2}
    ]

    assert validate_citations(answer, sources) == [
        "[Source: researchpilot_ai_ml_basics.pdf, Page: 2]"
    ]


def test_excludes_unmentioned_retrieved_sources():
    answer = "Source: researchpilot_ai_ml_basics.pdf, Page: 2"
    sources = [
        {"source": "researchpilot_ai_ml_basics.pdf", "page_number": 2},
        {"source": "researchpilot_ai_rag_safety.pdf", "page_number": 1},
    ]

    assert validate_citations(answer, sources) == [
        "[Source: researchpilot_ai_ml_basics.pdf, Page: 2]"
    ]


def test_returns_empty_list_when_answer_has_no_citation():
    answer = "The documents do not provide enough information."
    sources = [
        {"source": "researchpilot_ai_ml_basics.pdf", "page_number": 2}
    ]

    assert validate_citations(answer, sources) == []