"""Run systems over a query set and print results with uncertainty.

    python -m evalkit.run_eval --index idx_paragraph --queries queries.jsonl --qrels qrels.tsv --split dev

TODO(day2) main table: per system, mean [95% CI] of MRR@10, NDCG@10, Recall@10, Recall@50.
TODO(day2) skip (and REPORT) queries with no relevant label instead of scoring them as 0.
TODO(day2) save per-query scores with --out runs/dev.json (needed for failure analysis).
TODO(day3) breakdown of NDCG@10 by query type.
TODO(day3) paired comparisons vs BM25: diff, CI, p, wins/losses/ties.
TODO(day3) flags: --stem, --stopwords, --k1/--b, --grid (k1 x b table), --depths 20 50 100,
              --split test must print a "run this once" warning.
"""

from __future__ import annotations


def main(argv=None):
    raise NotImplementedError


if __name__ == "__main__":
    main()
