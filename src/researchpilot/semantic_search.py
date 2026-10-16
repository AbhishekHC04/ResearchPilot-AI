import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


class SemanticSearch:
    """Build a local semantic index and retrieve relevant text chunks."""

    def __init__(self, model_name: str = DEFAULT_MODEL):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunks = []

    def build_index(self, chunks: list[dict]) -> None:
        if not chunks:
            raise ValueError("At least one text chunk is required.")

        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=True,
        )

        embeddings = np.asarray(embeddings, dtype=np.float32)
        self.index = faiss.IndexFlatIP(embeddings.shape[1])
        self.index.add(embeddings)
        self.chunks = list(chunks)

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        if self.index is None:
            raise RuntimeError("Build the index before searching.")

        if not query or not query.strip():
            raise ValueError("Query must not be empty.")

        if top_k < 1:
            raise ValueError("top_k must be at least 1.")

        query_embedding = self.model.encode(
            [query.strip()],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        query_embedding = np.asarray(query_embedding, dtype=np.float32)

        scores, indices = self.index.search(
            query_embedding,
            min(top_k, len(self.chunks)),
        )

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue

            result = dict(self.chunks[int(idx)])
            result["similarity"] = float(score)
            results.append(result)

        return results
