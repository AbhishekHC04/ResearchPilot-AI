
from unittest.mock import patch

from src.researchpilot.answer_generator import AnswerGenerator


def test_returns_sources_when_no_passages():
    generator = AnswerGenerator()

    result = generator.generate_answer(
        "What is machine learning?",
        [],
    )

    assert result["sources"] == []
    assert "couldn't find relevant information" in result["answer"]


@patch("src.researchpilot.answer_generator.urlopen")
def test_generates_answer_and_returns_citations(mock_urlopen):
    mock_response = mock_urlopen.return_value.__enter__.return_value
    mock_response.read.return_value = (
        b'{"response": "Machine learning learns patterns from data."}'
    )

    generator = AnswerGenerator()

    passages = [
        {
            "source": "research.pdf",
            "page_number": 3,
            "text": "Machine learning algorithms learn patterns from data.",
        }
    ]

    result = generator.generate_answer(
        "What is machine learning?",
        passages,
    )

    assert result["answer"] == "Machine learning learns patterns from data."
    assert result["sources"] == [
        {"source": "research.pdf", "page_number": 3}
    ]
    mock_urlopen.assert_called_once()

