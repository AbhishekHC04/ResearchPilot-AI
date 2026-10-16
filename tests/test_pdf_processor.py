import pymupdf
import pytest

from src.researchpilot.pdf_processor import extract_pdf_pages


def test_extract_pdf_pages_preserves_page_numbers(tmp_path):
    pdf_path = tmp_path / "sample.pdf"

    with pymupdf.open() as document:
        first_page = document.new_page()
        first_page.insert_text((72, 72), "ResearchPilot AI first page")

        second_page = document.new_page()
        second_page.insert_text((72, 72), "ResearchPilot AI second page")

        document.save(pdf_path)

    pages = extract_pdf_pages(pdf_path)

    assert len(pages) == 2
    assert pages[0]["page_number"] == 1
    assert "first page" in pages[0]["text"]
    assert pages[1]["page_number"] == 2
    assert "second page" in pages[1]["text"]


def test_missing_pdf_raises_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        extract_pdf_pages(tmp_path / "missing.pdf")


def test_non_pdf_file_is_rejected(tmp_path):
    text_path = tmp_path / "notes.txt"
    text_path.write_text("Not a PDF", encoding="utf-8")

    with pytest.raises(ValueError, match="must be a PDF"):
        extract_pdf_pages(text_path)
