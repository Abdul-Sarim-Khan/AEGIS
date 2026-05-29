"""
rag_engine.py
=============
Optimized Phase 2 of the LLM-powered SAST tool (AEGIS).
Replaced LangChain text splitter with a pure-Python parser to completely fix MemoryError.
"""

from __future__ import annotations

import glob
import os
import time
import pickle
from dataclasses import dataclass, field
from typing import List

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
KNOWLEDGE_BASE_DIR = os.path.join(os.path.dirname(__file__), "knowledge_base")
CACHE_DIR = os.path.join(os.path.dirname(__file__), ".cache")
INDEX_PATH = os.path.join(CACHE_DIR, "faiss_owasp.index")
CHUNKS_PATH = os.path.join(CACHE_DIR, "chunks.pkl")

EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 600        
CHUNK_OVERLAP = 100     
DEFAULT_TOP_K = 4       

@dataclass
class Chunk:
    text: str
    source: str          

@dataclass
class RetrievalResult:
    chunk: Chunk
    score: float         

@dataclass
class RagEngine:
    model_name: str = EMBED_MODEL_NAME
    chunks: List[Chunk] = field(default_factory=list)
    _model: getattr('SentenceTransformer', None) = field(default=None, repr=False)
    _index: getattr('faiss.Index', None) = field(default=None, repr=False)
    build_seconds: float = 0.0

    def load_knowledge_base(self, kb_dir: str = KNOWLEDGE_BASE_DIR) -> List[Chunk]:
        """
        Pure-Python sliding window splitter that mimics LangChain's chunking logic.
        Eliminates the dependency on heavy libraries during file parsing.
        """
        chunks: List[Chunk] = []
        md_paths = sorted(glob.glob(os.path.join(kb_dir, "*.md")))
        if not md_paths:
            raise FileNotFoundError(f"No .md files found in {kb_dir!r}")

        for path in md_paths:
            with open(path, "r", encoding="utf-8") as fh:
                content = fh.read()
            source = os.path.basename(path)
            
            # Basic character-based sliding window layout
            start = 0
            while start < len(content):
                end = start + CHUNK_SIZE
                piece = content[start:end].strip()
                if piece:
                    chunks.append(Chunk(text=piece, source=source))
                start += (CHUNK_SIZE - CHUNK_OVERLAP)

        self.chunks = chunks
        return chunks

    def _get_model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def encode_chunks(self, parallel: bool = False, batch_size: int = 32):
        import numpy as np
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

    def build(self, parallel: bool = False, force_rebuild: bool = False) -> "RagEngine":
        start = time.perf_counter()
        
        # Check cache instantly without looking up any models
        if not force_rebuild and os.path.exists(INDEX_PATH) and os.path.exists(CHUNKS_PATH):
            try:
                import faiss
                self._index = faiss.read_index(INDEX_PATH)
                with open(CHUNKS_PATH, "rb") as f:
                    self.chunks = pickle.load(f)
                self.build_seconds = time.perf_counter() - start
                return self
            except Exception:
                pass 

        if not self.chunks:
            self.load_knowledge_base()

        import faiss
        embeddings = self.encode_chunks(parallel=parallel)
        dim = embeddings.shape[1]

        index = faiss.IndexFlatIP(dim)
        index.add(embeddings)
        self._index = index

        os.makedirs(CACHE_DIR, exist_ok=True)
        faiss.write_index(index, INDEX_PATH)
        with open(CHUNKS_PATH, "wb") as f:
            pickle.dump(self.chunks, f)

        self.build_seconds = time.perf_counter() - start
        return self

    def search(self, query: str, top_k: int = DEFAULT_TOP_K) -> List[RetrievalResult]:
        if self._index is None:
            raise RuntimeError("Index not built. Call build() first.")

        import numpy as np
        model = self._get_model()
        q_vec = model.encode(
            [query], normalize_embeddings=True, show_progress_bar=False
        ).astype("float32")

        scores, indices = self._index.search(q_vec, top_k)

        results: List[RetrievalResult] = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            results.append(RetrievalResult(chunk=self.chunks[idx], score=float(score)))
        return results

    def stats(self) -> dict:
        return {
            "documents": len({c.source for c in self.chunks}) if self.chunks else 0,
            "chunks": len(self.chunks),
            "embedding_model": self.model_name,
            "vector_dim": self._index.d if self._index else None,
            "build_seconds": round(self.build_seconds, 3),
        }

def build_engine(parallel: bool = False, force_rebuild: bool = False) -> RagEngine:
    return RagEngine().build(parallel=parallel, force_rebuild=force_rebuild)