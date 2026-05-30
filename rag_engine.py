"""
rag_engine.py
=============
Phase 2 of the LLM-powered SAST tool: the Retrieval-Augmented Generation (RAG)
engine.

Responsibilities
----------------
1. Load the OWASP knowledge-base Markdown files from ``knowledge_base/``.
2. Split them into overlapping chunks (LangChain, Markdown-aware).
3. Embed the chunks with a Sentence-Transformers model.
4. Build an in-memory FAISS index (the "ephemeral vector DB").
5. Retrieve the most relevant rule chunks for a piece of source code.

Design notes
------------
* We use ``sentence-transformers`` + ``faiss`` *directly* rather than wrapping
  everything in LangChain's vector-store abstraction. This keeps the FAISS
  index inspectable (important for the PNDC report and viva) and lets us
  control batching / parallel encoding ourselves.
* Embeddings are L2-normalised and we use an inner-product index
  (``IndexFlatIP``), so inner product == cosine similarity.
* ``encode_chunks()`` exposes a ``parallel`` switch and the build step is timed,
  giving you a ready-made sequential-vs-parallel benchmark for the
  Parallel & Distributed Computing deliverable.
"""

from __future__ import annotations

import glob
import os
import time
from dataclasses import dataclass, field
from typing import List, Tuple

import faiss
import numpy as np
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
KNOWLEDGE_BASE_DIR = os.path.join(os.path.dirname(__file__), "knowledge_base")

# all-MiniLM-L6-v2: 384-dim, ~80 MB, fast on CPU. A good fit for the limited
# resources of Streamlit Community Cloud.
EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

CHUNK_SIZE = 600        # characters per chunk
CHUNK_OVERLAP = 100     # characters of overlap between chunks
DEFAULT_TOP_K = 4       # how many rule chunks to retrieve per query


# --------------------------------------------------------------------------- #
# Data structures
# --------------------------------------------------------------------------- #
@dataclass
class Chunk:
    """A single retrievable unit of knowledge."""
    text: str
    source: str          # e.g. "a03_injection.md"


@dataclass
class RetrievalResult:
    chunk: Chunk
    score: float         # cosine similarity in [-1, 1]; higher is closer


@dataclass
class RagEngine:
    """In-memory RAG engine over the OWASP knowledge base."""

    model_name: str = EMBED_MODEL_NAME
    chunks: List[Chunk] = field(default_factory=list)
    _model: SentenceTransformer | None = field(default=None, repr=False)
    _index: faiss.Index | None = field(default=None, repr=False)
    build_seconds: float = 0.0

    # ----------------------------- loading -------------------------------- #
    def load_knowledge_base(self, kb_dir: str = KNOWLEDGE_BASE_DIR) -> List[Chunk]:
        """Read every .md file and split it into Markdown-aware chunks."""
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            # Prefer to break on Markdown structure first, then sentences.
            separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " ", ""],
        )

        chunks: List[Chunk] = []
        md_paths = sorted(glob.glob(os.path.join(kb_dir, "*.md")))
        if not md_paths:
            raise FileNotFoundError(f"No .md files found in {kb_dir!r}")

        for path in md_paths:
            with open(path, "r", encoding="utf-8") as fh:
                content = fh.read()
            source = os.path.basename(path)
            for piece in splitter.split_text(content):
                piece = piece.strip()
                if piece:
                    chunks.append(Chunk(text=piece, source=source))

        self.chunks = chunks
        return chunks

    # ----------------------------- embedding ------------------------------ #
    def _get_model(self) -> SentenceTransformer:
        if self._model is None:
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def encode_chunks(self, parallel: bool = False, batch_size: int = 32) -> np.ndarray:
        """
        Embed all loaded chunks and return a normalised (n, dim) float32 matrix.

        Parameters
        ----------
        parallel:
            If True, use Sentence-Transformers' multi-process pool to spread
            encoding across CPU cores (true data-parallelism). If False, encode
            in a single process. Toggling this is the basis of your PNDC speedup
            benchmark.
        """
        model = self._get_model()
        texts = [c.text for c in self.chunks]

        if parallel:
            pool = model.start_multi_process_pool()
            try:
                embeddings = model.encode_multi_process(
                    texts, pool, batch_size=batch_size, normalize_embeddings=True
                )
            finally:
                model.stop_multi_process_pool(pool)
        else:
            embeddings = model.encode(
                texts,
                batch_size=batch_size,
                normalize_embeddings=True,
                show_progress_bar=False,
            )

        return np.asarray(embeddings, dtype="float32")

    # ----------------------------- index build --------------------------- #
    def build(self, parallel: bool = False) -> "RagEngine":
        """Load KB (if needed), embed, and build the FAISS index. Timed."""
        start = time.perf_counter()

        if not self.chunks:
            self.load_knowledge_base()

        embeddings = self.encode_chunks(parallel=parallel)
        dim = embeddings.shape[1]

        # IndexFlatIP = exact inner-product search. With normalised vectors this
        # is cosine similarity. FAISS runs the search multi-threaded (OpenMP)
        # internally -- one of the parallelism points for the PNDC write-up.
        index = faiss.IndexFlatIP(dim)
        index.add(embeddings)
        self._index = index

        self.build_seconds = time.perf_counter() - start
        return self

    # ----------------------------- retrieval ----------------------------- #
    def search(self, query: str, top_k: int = DEFAULT_TOP_K) -> List[RetrievalResult]:
        """Return the top_k most relevant rule chunks for a query string."""
        if self._index is None:
            raise RuntimeError("Index not built. Call build() first.")

        model = self._get_model()
        q_vec = model.encode(
            [query], normalize_embeddings=True, show_progress_bar=False
        ).astype("float32")

        scores, indices = self._index.search(q_vec, top_k)

        results: List[RetrievalResult] = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:  # FAISS returns -1 when fewer than top_k exist
                continue
            results.append(RetrievalResult(chunk=self.chunks[idx], score=float(score)))
        return results

    # ----------------------------- stats --------------------------------- #
    def stats(self) -> dict:
        return {
            "documents": len({c.source for c in self.chunks}),
            "chunks": len(self.chunks),
            "embedding_model": self.model_name,
            "vector_dim": self._index.d if self._index else None,
            "build_seconds": round(self.build_seconds, 3),
        }


# --------------------------------------------------------------------------- #
# Convenience factory
# --------------------------------------------------------------------------- #
def build_engine(parallel: bool = False) -> RagEngine:
    """Build and return a ready-to-query engine."""
    return RagEngine().build(parallel=parallel)


# --------------------------------------------------------------------------- #
# CLI smoke test:  python rag_engine.py
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    print("Building RAG engine (sequential)...")
    engine = build_engine(parallel=False)
    print("Stats:", engine.stats())

    # A snippet that should retrieve the SQL-injection rule.
    sample = (
        'cursor.execute("SELECT * FROM users WHERE name = \'" + username + "\'")'
    )
    print("\nQuery snippet:\n  ", sample)
    print("\nTop matches:")
    for r in engine.search(sample, top_k=3):
        first_line = r.chunk.text.splitlines()[0]
        print(f"  [{r.score:.3f}] {r.chunk.source:32s} | {first_line}")
