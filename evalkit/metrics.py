"""Ranking metrics from scratch.

`ranked` = list of doc_ids, best first.  `rels` = {doc_id: grade} for ONE query.
Anything missing from `rels` counts as grade 0 (unjudged == irrelevant: say so in your write-up).
"""

from __future__ import annotations


def reciprocal_rank(ranked: list[str], rels: dict[str, int], k: int = 10, min_grade: int = 1) -> float:
    """TODO(day2): 1/rank of the first doc with grade >= min_grade within top-k, else 0."""
    raise NotImplementedError


def dcg(grades: list[int], gain: str = "linear") -> float:
    """TODO(day2): sum_i gain(g_i) / log2(i + 2), i from 0. gain 'linear' -> g, 'exp' -> 2**g - 1."""
    raise NotImplementedError


def ndcg_at_k(ranked: list[str], rels: dict[str, int], k: int = 10, gain: str = "linear") -> float:
    """TODO(day2): DCG of the ranking / DCG of the ideal ranking (all judged grades, sorted desc).
    Return 0.0 if the ideal DCG is 0."""
    raise NotImplementedError


def recall_at_k(ranked: list[str], rels: dict[str, int], k: int, min_grade: int = 1) -> float:
    """TODO(day2): fraction of relevant docs (grade >= min_grade) found in top-k. 0.0 if none exist."""
    raise NotImplementedError


def precision_at_k(ranked: list[str], rels: dict[str, int], k: int, min_grade: int = 1) -> float:
    """TODO(optional)"""
    raise NotImplementedError
