"""Minimal CLI (argparse).

    python -m notesearch.cli index data --out idx_paragraph --chunking paragraph [--no-embed]
    python -m notesearch.cli search "your query" --index idx_paragraph --mode bm25 -k 10

TODO(day1): `index` and `search --mode bm25`.   TODO(day2): add the other modes.
Show for each hit: rank, score, doc_id, a ~140 char snippet.
"""

from __future__ import annotations


def main(argv=None):
    raise NotImplementedError


if __name__ == "__main__":
    main()
