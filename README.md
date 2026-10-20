# notesearch-lab (skeleton)

Offline mini search engine for my own notes: BM25 from scratch vs. embedding rerank / dense / hybrid, with a proper evaluation.

> Status: skeleton. Every function is a stub (`raise NotImplementedError`). Start with `PLAN.md`.

## Start
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 -m pytest -q          # all red now; green = done
```

## Where things are
- `PLAN.md`: the 3-day plan with checklists and checkpoints
- `ARCHITECTURE.md` + `docs/architecture.svg`: how the pieces fit
- `notesearch/`: the search engine (stubs)
- `evalkit/`: metrics, statistics, label pooling, eval runner (stubs)
- `tests/`: the spec for each module
- `LABELING.md`: labeling rules (edit on Day 1)
- `queries.example.jsonl`: the query file format

## Write-up sections (fill on Day 3)
Question and setup · Methods · Query set and labeling · Results (with CIs) · Error analysis · Limitations · What I'd do next · AI assistance
