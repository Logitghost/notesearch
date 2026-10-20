"""SPEC for notesearch/chunking.py"""
import pytest

from notesearch.chunking import Doc, chunk_docs, load_notes


def test_chunking_strategies():
    text = "\n\n".join(f"para {i} " + "word " * 40 for i in range(4))
    docs = [Doc("a.md", text)]
    assert len(chunk_docs(docs, "whole")) == 1
    assert len(chunk_docs(docs, "paragraph", min_words=30)) == 4
    w = chunk_docs(docs, "window", window=50, overlap=10)
    assert len(w) > 1 and all(c.doc_id == "a.md" for c in w)
    assert [c.chunk_id for c in chunk_docs(docs, "paragraph")][:2] == ["a.md#0", "a.md#1"]
    with pytest.raises(ValueError):
        chunk_docs(docs, "nope")


def test_tiny_paragraphs_are_merged_not_dropped():
    docs = [Doc("a.md", "# Heading\n\n" + "word " * 40)]
    chunks = chunk_docs(docs, "paragraph", min_words=30)
    assert len(chunks) == 1 and "Heading" in chunks[0].text


def test_load_notes_sorted_and_strips_front_matter(tmp_path):
    (tmp_path / "b.md").write_text("---\ntitle: x\n---\nhello b")
    (tmp_path / "a.txt").write_text("hello a")
    (tmp_path / "ignore.png").write_text("nope")
    (tmp_path / "empty.md").write_text("   ")
    docs = load_notes(str(tmp_path))
    assert [d.doc_id for d in docs] == ["a.txt", "b.md"]
    assert docs[1].text == "hello b"
