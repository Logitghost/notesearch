"""Uncertainty over per-query scores. With ~40 queries, small differences are noise: quantify that.

Look at the CI of the PAIRED difference, not at whether two separate CIs overlap.
"""

from __future__ import annotations


def bootstrap_ci(values, n_boot: int = 10_000, alpha: float = 0.05, seed: int = 0):
    """TODO(day2): percentile bootstrap CI of the mean. Resample queries with replacement.
    Return (mean, lo, hi). Use numpy's default_rng(seed) so results are reproducible."""
    raise NotImplementedError


def paired_bootstrap(a, b, n_boot: int = 10_000, alpha: float = 0.05, seed: int = 0) -> dict:
    """TODO(day2): bootstrap the mean of per-query differences (a - b).
    Return {"diff", "lo", "hi", "p"}; p = two-sided bootstrap p-value for H0: diff == 0."""
    raise NotImplementedError


def win_loss_tie(a, b, eps: float = 1e-9) -> tuple[int, int, int]:
    """TODO(day2): per-query counts where a > b, a < b, |a - b| <= eps."""
    raise NotImplementedError
