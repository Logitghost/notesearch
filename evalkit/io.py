"""Read the two eval files.

queries.jsonl  one JSON object per line:
    {"id": "q01", "text": "...", "type": "keyword|question|vague|exact|paraphrase", "split": "dev|test"}

qrels.tsv      query_id <TAB> doc_id <TAB> grade      (0 irrelevant, 1 partial, 2 highly relevant)
    - skip blank lines and lines starting with '#'
    - skip rows whose grade is empty (so an unfinished label_pool.tsv is not silently scored)
"""

from __future__ import annotations


def load_queries(path: str, split: str = "all") -> list[dict]:
    """TODO(day2): split in {'all', 'dev', 'test'}."""
    raise NotImplementedError


def load_qrels(path: str) -> dict[str, dict[str, int]]:
    """TODO(day2): {query_id: {doc_id: grade}}."""
    raise NotImplementedError
