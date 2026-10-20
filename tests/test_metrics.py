import math

import pytest

from evalkit.metrics import ndcg_at_k, precision_at_k, recall_at_k, reciprocal_rank
from evalkit.stats import bootstrap_ci, paired_bootstrap, win_loss_tie


def test_reciprocal_rank():
    assert reciprocal_rank(["a", "b", "c"], {"c": 2}) == pytest.approx(1 / 3)
    assert reciprocal_rank(["a", "b", "c"], {"a": 1}) == 1.0
    assert reciprocal_rank(["a", "b", "c"], {"c": 2}, k=2) == 0.0  # beyond cutoff
    assert reciprocal_rank(["a", "b"], {"b": 0}) == 0.0  # grade 0 is not relevant
    assert reciprocal_rank(["a"], {}) == 0.0


def test_ndcg_hand_computed_linear():
    ranked, rels = ["a", "b", "c"], {"a": 1, "b": 0, "c": 2}
    dcg = 1 / math.log2(2) + 0 + 2 / math.log2(4)  # = 2.0
    ideal = 2 / math.log2(2) + 1 / math.log2(3)  # [2, 1]
    assert ndcg_at_k(ranked, rels, 10, "linear") == pytest.approx(dcg / ideal)


def test_ndcg_hand_computed_exponential_gain():
    ranked, rels = ["a", "b", "c"], {"a": 1, "b": 0, "c": 2}
    dcg = 1 / math.log2(2) + 0 + 3 / math.log2(4)
    ideal = 3 / math.log2(2) + 1 / math.log2(3)
    assert ndcg_at_k(ranked, rels, 10, "exp") == pytest.approx(dcg / ideal)


def test_ndcg_perfect_and_empty_and_cutoff():
    rels = {"a": 2, "b": 1}
    assert ndcg_at_k(["a", "b", "x"], rels) == pytest.approx(1.0)
    assert ndcg_at_k(["b", "a"], rels) < 1.0
    assert ndcg_at_k(["a", "b"], {}) == 0.0
    assert ndcg_at_k(["x", "a"], {"a": 2}, k=1) == 0.0


def test_ndcg_unjudged_docs_count_as_irrelevant():
    assert ndcg_at_k(["unjudged", "a"], {"a": 2}) < ndcg_at_k(["a", "unjudged"], {"a": 2})


def test_recall_and_precision():
    rels = {"a": 2, "b": 1, "c": 0, "d": 2}
    ranked = ["a", "x", "b", "y"]
    assert recall_at_k(ranked, rels, 3) == pytest.approx(2 / 3)
    assert recall_at_k(ranked, rels, 1) == pytest.approx(1 / 3)
    assert recall_at_k(ranked, rels, 3, min_grade=2) == pytest.approx(1 / 2)
    assert precision_at_k(ranked, rels, 4) == pytest.approx(2 / 4)
    assert recall_at_k(ranked, {}, 3) == 0.0


def test_bootstrap_ci_brackets_mean_and_is_deterministic():
    vals = [0.0, 1.0, 0.5, 0.25, 0.75, 1.0, 0.0, 0.5]
    m, lo, hi = bootstrap_ci(vals, n_boot=2000, seed=1)
    assert lo <= m <= hi
    assert (m, lo, hi) == bootstrap_ci(vals, n_boot=2000, seed=1)


def test_paired_bootstrap_identical_systems():
    x = [0.2, 0.4, 0.6, 0.8]
    r = paired_bootstrap(x, x, n_boot=1000)
    assert r["diff"] == 0 and r["lo"] == 0 and r["hi"] == 0 and r["p"] == 1.0


def test_paired_bootstrap_detects_consistent_improvement():
    a = [0.5 + 0.1 * (i % 3) + 0.2 for i in range(30)]
    b = [0.5 + 0.1 * (i % 3) for i in range(30)]
    r = paired_bootstrap(a, b, n_boot=2000)
    assert r["diff"] == pytest.approx(0.2) and r["lo"] > 0 and r["p"] < 0.01


def test_win_loss_tie():
    assert win_loss_tie([1, 0.5, 0.3, 0.9], [0.5, 0.5, 0.4, 0.1]) == (2, 1, 1)
