"""Embedding backend: text -> L2-normalized float32 vectors.

Pick ONE small model for the 3-day version, e.g. BAAI/bge-small-en-v1.5 or all-MiniLM-L6-v2
(sentence-transformers, runs on CPU, offline after the first download).

Gotchas to handle:
  - bge expects an instruction prefix on QUERIES ("Represent this sentence for searching relevant
    passages: ") but not on passages; e5 expects "query: " / "passage: ".
  - normalize vectors so dot product == cosine similarity.
  - encode in batches; show a progress bar only for the big corpus encode.
"""

from __future__ import annotations

import numpy as np

DEFAULT_MODEL = "BAAI/bge-small-en-v1.5"


class Embedder:
    def __init__(self, model_name: str = DEFAULT_MODEL):
        # TODO(day2): lazily import sentence_transformers; load the model; set query/passage prefixes.
        raise NotImplementedError

    def encode(self, texts: list[str], is_query: bool = False, batch_size: int = 64) -> np.ndarray:
        """TODO(day2): return array of shape (len(texts), dim), float32, rows L2-normalized."""
        raise NotImplementedError
