"""Turn text into a list of terms. Used for BOTH documents and queries (must be identical).

Design questions to settle (and note your answers in the README):
  - lowercase? split on what? what about snake_case, v1.2.3, foo-bar, error codes like E1234?
  - keep the whole compound as an extra token, or only its parts?
  - stopwords and stemming are ABLATIONS, so each must be a switch, off by default.
"""

from __future__ import annotations


class Tokenizer:
    def __init__(self, stopwords: bool = False, stem: bool = False, keep_compounds: bool = True):
        self.stopwords = stopwords
        self.stem = stem
        self.keep_compounds = keep_compounds

    def __call__(self, text: str) -> list[str]:
        # TODO(day1): regex-based tokenization honoring the three switches.
        # Hint: re.findall on lowercase text; stemming via nltk SnowballStemmer (import lazily).
        raise NotImplementedError

    def to_config(self) -> dict:
        # TODO(day1): return the 3 switches as a dict (saved next to the index so queries are
        # tokenized the same way at search time).
        raise NotImplementedError

    @classmethod
    def from_config(cls, cfg: dict) -> "Tokenizer":
        # TODO(day1)
        raise NotImplementedError
