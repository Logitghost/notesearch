# 3-day plan: BM25 vs. embeddings on your own notes

**Goal:** a finished, honest comparison of BM25, dense, rerank and hybrid retrieval on your notes, with confidence intervals and failure analysis. The eval is the project; the search code serves it.

**How the skeleton works:** every function is a stub with a `TODO(dayN)` tag. `pytest` is your progress bar: tests in `tests/` are the spec, and they all fail right now. Make them go green one file at a time.

Times are estimates for focused work (about 8 hours per day). Each day ends with a **checkpoint**; if you miss it, use the **cut list** at the bottom instead of working late.

---

## Day 1: corpus, queries, BM25

### Block 1: setup (30 min)
- [ ] `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
  (start the `sentence-transformers` install now, it is a big download)
- [ ] `git init`, first commit of the skeleton
- [ ] Read `ARCHITECTURE.md` and look at `docs/architecture.svg` once, so every stub has a place in your head

### Block 2: corpus (1 hour)
- [ ] Copy 300 to 800 `.md` / `.txt` notes into `data/` (Notion/Obsidian/Docs export; add saved articles if short)
- [ ] Remove secrets and private info
- [ ] Freeze it: do not edit `data/` for the rest of the project
- [ ] Note down for the README: how many notes, rough total words, what kinds (meeting notes, code snippets, articles...)

### Block 3: write queries BEFORE building anything (2 hours)
This must come before you see any search result, so results cannot shape your queries.
- [ ] Copy `queries.example.jsonl` to `queries.jsonl` and write **40 queries**: 8 each of `keyword`, `question`, `vague`, `exact`, `paraphrase`
- [ ] Method: pick a note you remember, close it, and write the query you would actually type. Never copy phrases from the note.
- [ ] Mark **25 as `dev`, 15 as `test`**, balanced across types. Do not look at test results until Day 3.
- [ ] For each query, jot the note(s) you expect to be right (in a scratch file, not committed). This helps later, when labels disagree with expectations.
- [ ] Write `LABELING.md` (template is included): 3 grades, rules, tie-break rule.
- [ ] Commit `queries.jsonl` and `LABELING.md`.

### Block 4: tokenizer + chunking (1.5 hours)
- [ ] `tokenizer.py`: `Tokenizer.__call__`, `to_config`, `from_config`. Run `pytest tests/test_tokenizer.py`.
- [ ] `chunking.py`: `load_notes`, `chunk_docs` (whole, paragraph, window). Run `pytest tests/test_chunking.py`.
- [ ] Look at 10 real chunks by eye. Are headings glued to their text? Are any chunks tiny or huge?

### Block 5: BM25 from scratch (2 hours)
Implement in this order, running `pytest tests/test_bm25.py` as you go:
1. [ ] `build` (postings, doc lengths, avgdl)
2. [ ] `idf` (non-negative form)
3. [ ] `score_all` then `search`
4. [ ] `save` / `load`
5. [ ] `explain` (optional but useful tomorrow)

The reference function in the test file is a naive version of the formula: if yours disagrees, yours is the bug.

### Block 6: engine (bm25 only) + CLI (1 hour)
- [ ] `Engine.build` / `Engine.load` / `search` for `mode="bm25"` (skip embeddings for now)
- [ ] `cli.py`: `index --no-embed` and `search --mode bm25`
- [ ] Run 8 to 10 of your real queries. Do the results look sensible? Write down 3 surprises.
- [ ] Commit.

### Day 1 checkpoint
- `pytest tests/test_bm25.py tests/test_tokenizer.py tests/test_chunking.py` all green
- 40 queries written and split, `LABELING.md` written
- `search --mode bm25` works on your real notes

---

## Day 2: embeddings, all four systems, labels, metrics

### Block 1: embeddings (1 hour)
- [ ] `embed.py`: `Embedder.__init__` and `encode` (prefixes for bge/e5, normalization, batching)
- [ ] Quick sanity check in a REPL: embed "cat" and "kitten", "cat" and "tax law"; the first pair should be closer
- [ ] `Engine.build`: encode all chunks, save `embeddings.npy` (time it, you will report this)

### Block 2: dense, rerank, hybrid (1.5 hours)
- [ ] `dense`: query vector · all chunk vectors, argsort
- [ ] `rerank`: BM25 top-`depth`, reorder by cosine
- [ ] `hybrid`: reciprocal rank fusion with `rrf_k=60`
- [ ] Doc-level collapse (best chunk per note) in `search`
- [ ] CLI: all four `--mode`s. Eyeball 10 queries: where do the modes disagree?
- [ ] Build **two index folders**: `idx_paragraph` and `idx_whole`

### Block 3: eval IO + pooling (1 hour)
- [ ] `evalkit/io.py`: `load_queries`, `load_qrels`
- [ ] `evalkit/pool.py`: union of every system's top-10 per query, shuffled, system-blind, output TSV
- [ ] Generate `label_pool.tsv` and check the size (expect 15 to 25 unique notes per query, so about 600 to 1,000 rows)

### Block 4: label (2.5 hours, do not rush)
- [ ] Re-read `LABELING.md`, then fill the `grade` column for **every** row
- [ ] Do the labeling in two sittings with a break, to keep judgments consistent
- [ ] Save as `qrels.tsv`
- [ ] Spot check: re-label 20 random rows without looking at your first answers. Count disagreements; this is your label-noise estimate for the write-up.

### Block 5: metrics + stats (1.5 hours)
- [ ] `metrics.py`: `reciprocal_rank`, `dcg`, `ndcg_at_k`, `recall_at_k`. Run `pytest tests/test_metrics.py`.
- [ ] `stats.py`: `bootstrap_ci`, `paired_bootstrap`, `win_loss_tie`
- [ ] `run_eval.py`: main table (mean [95% CI] for MRR@10, NDCG@10, Recall@10, Recall@50), skipping and reporting queries with no relevant label, saving per-query scores with `--out`
- [ ] Run on `--split dev`. First real results table. Commit it in `runs/` or paste it in your notes.

### Day 2 checkpoint
- All tests green
- `qrels.tsv` complete for all 40 queries
- A dev results table for the four systems, with CIs

---

## Day 3: ablations, held-out run, error analysis, write-up

### Block 1: extend `run_eval.py` (1 hour)
- [ ] By-query-type NDCG@10 table
- [ ] Paired comparisons vs. BM25: diff, CI, p, wins/losses/ties
- [ ] Flags: `--stem`, `--stopwords`, `--k1`, `--b`, `--depths`, `--grid`
- [ ] `--split test` prints a "run once" warning

### Block 2: ablations on **dev only** (1.5 hours)
Fill this table as you go; each row is one run.

| question | runs |
|---|---|
| Does stemming help BM25? | `--stem` vs. default |
| Do stopwords matter? | `--stopwords` vs. default |
| Best `k1`, `b`? | `--grid` (pick on dev only) |
| Does chunking matter? | `idx_whole` vs. `idx_paragraph` |
| How deep must rerank go? | `--depths 20 50 100` (watch Recall@50 vs. depth) |

- [ ] Write one sentence per row saying what you found, even if "no difference".
- [ ] Freeze the final config for each system **now**, and write it down.

### Block 3: held-out run (30 min)
- [ ] Run each system's frozen config on `--split test`, **once**
- [ ] Save as `runs/test.json`. With only about 15 queries, treat it as indicative, and say so.

### Block 4: error analysis (1.5 hours)
- [ ] For each system, list its 5 worst dev queries (write a small script over `runs/dev.json`, or sort the per-query scores)
- [ ] For each failure, open the query, the expected note, and what was returned. Write one line on why:
  vocabulary mismatch, chunk boundary split the answer, embedding confused by jargon, short ambiguous query, label noise, stemming, etc.
- [ ] Find 2 queries where hybrid beat both, and 2 where it hurt
- [ ] Use `BM25Index.explain` on at least one BM25 failure to see which terms drove the score

### Block 5: write-up (2 hours)
Fill `README.md` with these sections:
1. **Question and setup:** corpus size and type, models, hardware, index time and size
2. **Methods:** the 4 systems, tokenizer choices, chunking, dev/test split
3. **Query set and labeling protocol:** types, counts, `LABELING.md`, pooling, your label-noise estimate
4. **Results:** main dev table with CIs, then the test table; the by-type table; ablation table; rerank-depth plot (optional)
5. **Error analysis:** the failure cases and what they teach
6. **Limitations:** one annotator, small query set, personal corpus, pooling bias, unjudged = irrelevant
7. **What I'd do next**
8. **AI assistance:** say which parts of the starter skeleton were provided and what you wrote yourself

### Block 6: polish (1 hour)
- [ ] Add a `repro.sh` that runs: tests → build both indexes → dev eval → test eval
- [ ] Pin versions in `requirements.txt`; record the model name and a random seed
- [ ] Decide what is safe to publish. Never commit your real notes; consider a small sample corpus
- [ ] Final commit and push

### Day 3 checkpoint
- Dev and test results tables, with CIs
- An error analysis with real examples
- A README another person could follow

---

## What a good conclusion looks like
Not "embeddings win". Something like: "On my 25 dev queries, hybrid beat BM25 on NDCG@10 by 0.06 (CI [−0.01, +0.13], not significant), driven by paraphrase queries (+0.20) while BM25 stayed ahead on exact-match queries; reranking was capped by BM25's recall at depth 20." Specific, hedged, backed by per-type numbers.

## Cut list (when behind, cut in this order)
1. Chunking ablation (keep paragraph only)
2. `k1` / `b` grid (keep defaults)
3. Rerank-depth sweep (use depth 50)
4. `window` chunking and `explain`
5. Never cut: labeling, bootstrap CIs, error analysis, dev/test discipline

## Common traps
- Writing queries after seeing results (bias). Write them first.
- Copying phrases from the target note into the query (BM25 wins trivially).
- Tuning on the test split. Look at it once.
- Labeling only one system's results (pooling bias). Label the shuffled union.
- Reporting a 0.02 difference as a win with 25 queries. Look at the paired CI.
- Forgetting the BGE query prefix, then concluding dense retrieval is bad.
- Letting the notes folder change mid-project, which breaks old labels.
