"""SPEC for notesearch/bm25.py. Make these pass in order (top to bottom). The reference
implementation below is deliberately naive: use it to check your fast version."""
import math
from collections import Counter

from notesearch.bm25 import BM25Index

DOCS = [
    "the cat sat on the mat",
    "the dog chased the cat around the garden",
    "bm25 is a ranking function used by search engines",
    "cats and dogs and cats again",
    "the the the the the",
]


def reference_scores(docs_tokens, query_tokens, k1, b):
    """Naive, obviously-correct BM25 straight from the formula, to validate the index."""
    n = len(docs_tokens)
    avgdl = sum(len(d) for d in docs_tokens) / n
    out = {}
    for i, d in enumerate(docs_tokens):
        tf = Counter(d)
        s = 0.0
        for t in set(query_tokens):
            if tf[t] == 0:
                continue
            df = sum(1 for dd in docs_tokens if t in dd)
            idf = math.log(1 + (n - df + 0.5) / (df + 0.5))
            s += idf * tf[t] * (k1 + 1) / (tf[t] + k1 * (1 - b + b * len(d) / avgdl))
        if s > 0:
            out[i] = s
    return out


def test_matches_reference_for_several_queries_and_params():
    toks = [d.split() for d in DOCS]
    for k1, b in [(1.5, 0.75), (1.2, 0.3), (2.0, 0.9), (0.9, 0.0)]:
        idx = BM25Index(k1, b).build(toks)
        for q in ["cat", "the cat garden", "bm25 search ranking", "dog dog cats", "unknownterm cat"]:
            got = idx.score_all(q.split())
            want = reference_scores(toks, q.split(), k1, b)
            assert got.keys() == want.keys()
            for i in want:
                assert math.isclose(got[i], want[i], rel_tol=1e-9), (q, k1, b, i)


def test_idf_is_never_negative_even_for_ubiquitous_terms():
    toks = [["common", "x"], ["common", "y"], ["common", "z"]]
    idx = BM25Index().build(toks)
    assert idx.idf("common") > 0


def test_only_docs_with_query_terms_are_scored_and_order_is_sensible():
    toks = [d.split() for d in DOCS]
    idx = BM25Index().build(toks)
    res = idx.search(["bm25"], k=10)
    assert [d for d, _ in res] == [2]
    res = idx.search(["cat"], k=10)
    assert {d for d, _ in res} == {0, 1}  # doc 3 only has "cats": no stemming, so no match
    scores = [s for _, s in res]
    assert scores == sorted(scores, reverse=True)


def test_length_normalization_prefers_shorter_doc_for_equal_tf():
    toks = [["alpha", "beta"], ["alpha"] + ["filler"] * 50]
    idx = BM25Index(b=0.75).build(toks)
    res = dict(idx.search(["alpha"]))
    assert res[0] > res[1]
    idx.b = 0.0  # no length normalization -> tie
    res = dict(idx.search(["alpha"]))
    assert math.isclose(res[0], res[1])


def test_save_load_roundtrip(tmp_path):
    toks = [d.split() for d in DOCS]
    idx = BM25Index(1.3, 0.6).build(toks)
    p = tmp_path / "bm25.json"
    idx.save(str(p))
    loaded = BM25Index.load(str(p))
    assert loaded.k1 == 1.3 and loaded.b == 0.6
    assert loaded.search(["cat", "dog"]) == idx.search(["cat", "dog"])


def test_explain_sums_to_score():
    toks = [d.split() for d in DOCS]
    idx = BM25Index().build(toks)
    q = ["cat", "garden", "the"]
    score = idx.score_all(q)[1]
    assert math.isclose(sum(idx.explain(q, 1).values()), score)
