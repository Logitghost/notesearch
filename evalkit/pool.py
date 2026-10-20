"""Build the label pool: union of every system's top-k per query, shuffled and system-blind.

Pooling from a single system biases the eval toward it. Pool from ALL systems, shuffle so you
cannot tell which system returned what, then label.

    python -m evalkit.pool --index idx_paragraph --queries queries.jsonl --k 10 --out label_pool.tsv

Output columns (TSV): query_id, doc_id, grade (empty, YOU fill), query_text, snippet
TODO(day2): implement main(). The finished, filled-in file doubles as qrels.tsv.
"""

from __future__ import annotations


def main(argv=None):
    raise NotImplementedError


if __name__ == "__main__":
    main()
