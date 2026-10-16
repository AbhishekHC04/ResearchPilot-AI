
from pathlib import Path

from src.researchpilot.pdf_processor import extract_pdf_pages
from src.researchpilot.text_chunker import chunk_pages
from src.researchpilot.semantic_search import SemanticSearch
from src.researchpilot.answer_generator import AnswerGenerator


class ResearchPipeline:
    """Index multiple PDFs and answer questions using their passages."""

    def __init__(self):
        self.search_engine = SemanticSearch()
        self.answer_generator = AnswerGenerator()
        self.chunks = []
        self.documents = []

    def ingest_pdf(self, pdf_path: str | Path) -> int:
        """Add one PDF to the shared index and return its new chunk count."""
        path = Path(pdf_path)
        pages = extract_pdf_pages(path)
        chunks = chunk_pages(pages)

        # Preserve the actual document filename in citations.
        for chunk in chunks:
            chunk["source"] = path.name

        if not chunks:
            raise ValueError(f"No text chunks could be extracted from {path.name}.")

        updated_chunks = self.chunks + chunks

        # Build the index before changing the current state.
        self.search_engine.build_index(updated_chunks)
        self.chunks = updated_chunks

        if path.name not in self.documents:
            self.documents.append(path.name)

        return len(chunks)

    def search(self, question: str, top_k: int = 3) -> list[dict]:
        """Retrieve relevant passages across all indexed PDFs."""
        return self.search_engine.search(question, top_k=top_k)

    
    def ask(
        self,
        question: str,
        top_k: int = 3,
        history: list[dict] | None = None,
    ) -> dict:
        """Generate a grounded answer using retrieved passages and conversation history."""
        passages = self.search(question, top_k=top_k)
        result = self.answer_generator.generate_answer(
            question,
            passages,
            history=history,
        )

        return {
            "question": question,
            "answer": result["answer"],
            "sources": result["sources"],
            "valid_citations": result.get("valid_citations", []),
            "retrieved_passages": passages,
        }

