"""Load notes from disk and split them into chunks.

doc_id   = note path relative to the notes folder (posix style). Labels refer to doc_ids.
chunk_id = f"{doc_id}#{i}"
Retrieval happens on chunks; the eval happens on documents (best chunk per doc).
"""

from __future__ import annotations

from dataclasses import dataclass

EXTENSIONS = {".md", ".txt"}


@dataclass
class Doc:
    doc_id: str
    text: str


@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    text: str


def load_notes(folder: str) -> list[Doc]:
    """TODO(day1): walk `folder`, read EXTENSIONS files (utf-8, errors='ignore'), strip YAML
    front matter, skip empty files, return Docs sorted by doc_id (deterministic order!)."""
    raise NotImplementedError


def chunk_docs(docs: list[Doc], strategy: str = "paragraph", min_words: int = 30,
               window: int = 200, overlap: int = 50) -> list[Chunk]:
    """TODO(day1): strategy is 'whole' | 'paragraph' | 'window'; raise ValueError otherwise.
      whole     : one chunk per note
      paragraph : split on blank lines; merge tiny paragraphs (headings!) until >= min_words
      window    : sliding window of `window` words with `overlap` words of overlap
    """
    raise NotImplementedError
