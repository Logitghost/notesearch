"""BM25 from scratch: inverted index + Okapi BM25 scoring. No search libraries.

Recap of the formula (look up the derivation yourself, that is part of the exercise):
    score(q, d) = sum over unique query terms t of  idf(t) * tf * (k1 + 1) / (tf + k1 * (1 - b + b * |d| / avgdl))
Decide on an IDF form and WHY. The classic log((N - df + 0.5) / (df + 0.5)) goes negative for terms in
more than half the docs; the "+1 inside the log" variant does not. Tests expect the non-negative one.

Store raw term frequencies and doc lengths in the index so k1 and b can be changed at QUERY time
(that makes the k1/b grid search on Day 3 cheap: no rebuild).
"""

from __future__ import annotations


class BM25Index:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.postings: dict[str, list[tuple[int, int]]] = {}  # term -> [(doc_idx, tf), ...]
        self.doc_len: list[int] = []
        self.avgdl: float = 0.0
        self.n_docs: int = 0

    def build(self, doc_tokens: list[list[str]]) -> "BM25Index":
        """TODO(day1): fill postings, doc_len, avgdl, n_docs. Return self."""
        raise NotImplementedError

    def idf(self, term: str) -> float:
        """TODO(day1): non-negative IDF; unknown terms (df = 0) must not crash."""
        raise NotImplementedError

    def score_all(self, query_tokens: list[str]) -> dict[int, float]:
        """TODO(day1): {doc_idx: score} for docs containing >= 1 query term (term-at-a-time).
        Each UNIQUE query term counts once."""
        raise NotImplementedError

    def search(self, query_tokens: list[str], k: int = 10) -> list[tuple[int, float]]:
        """TODO(day1): top-k (doc_idx, score), best first. Ties: lower doc_idx first (deterministic)."""
        raise NotImplementedError

    def explain(self, query_tokens: list[str], doc_idx: int) -> dict[str, float]:
        """TODO(optional): per-term contribution to one doc's score. Great for error analysis."""
        raise NotImplementedError

    def save(self, path: str) -> None:
        """TODO(day1): persist (JSON is fine). Must round-trip k1, b, doc_len, postings."""
        raise NotImplementedError

    @classmethod
    def load(cls, path: str) -> "BM25Index":
        """TODO(day1): inverse of save(); recompute n_docs and avgdl."""
        raise NotImplementedError
