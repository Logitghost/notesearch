"""Index building/loading and the four retrieval systems. See ARCHITECTURE.md for the data flow.

Systems (all rank CHUNKS, then collapse to documents by best chunk):
  bm25    lexical only
  dense   cosine similarity of query vs ALL chunk embeddings (brute force is fine at this scale)
  rerank  take BM25 top-`depth` chunks, re-order them by embedding similarity
          (cannot recover anything BM25 missed: that ceiling is a finding, measure it)
  hybrid  reciprocal rank fusion: score(c) = sum over rankings of 1 / (rrf_k + rank_of_c), rrf_k = 60

On-disk index layout (one folder per chunking config, e.g. idx_paragraph/):
  meta.json  chunks.jsonl  bm25.json  embeddings.npy
"""

from __future__ import annotations

MODES = ("bm25", "dense", "rerank", "hybrid")


class Engine:
    def __init__(self, chunks, tokenizer, bm25, emb, model, meta, index_dir=None):
        self.chunks = chunks
        self.tokenizer = tokenizer
        self.bm25 = bm25
        self.emb = emb          # (n_chunks, dim) float32 or None for BM25-only indexes
        self.model = model
        self.meta = meta
        self.index_dir = index_dir

    @classmethod
    def build(cls, folder: str, out_dir: str, chunking: str = "paragraph", model: str | None = None,
              tokenizer=None, k1: float = 1.5, b: float = 0.75, **chunk_kwargs) -> "Engine":
        """TODO(day1 for bm25 part, day2 for embeddings): load_notes -> chunk_docs -> tokenize -> BM25Index.build
        -> (optional) Embedder.encode -> write meta.json, chunks.jsonl, bm25.json, embeddings.npy to out_dir."""
        raise NotImplementedError

    @classmethod
    def load(cls, index_dir: str) -> "Engine":
        """TODO(day1): read the files written by build()."""
        raise NotImplementedError

    def chunk_ranking(self, query: str, mode: str, depth: int = 50, rrf_k: int = 60) -> list[tuple[int, float]]:
        """TODO(day1: bm25, day2: dense/rerank/hybrid): [(chunk_idx, score)] best first."""
        raise NotImplementedError

    def search(self, query: str, mode: str = "bm25", k: int = 10, depth: int = 50,
               rrf_k: int = 60, level: str = "doc") -> list[dict]:
        """TODO(day1): wrap chunk_ranking. level='doc' keeps only each note's best chunk.
        Each hit: {"rank", "doc_id", "chunk_id", "score", "text"}."""
        raise NotImplementedError
