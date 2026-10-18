"""Download a corpus of Wikipedia articles (as .md files) into data/.

Uses only the Python standard library. Run it on YOUR computer (it needs internet).

Examples
--------
  python scripts/fetch_corpus.py --preset cs
  python scripts/fetch_corpus.py --categories "Category:Machine learning" "Category:Databases" --limit 400
  python scripts/fetch_corpus.py --preset cs --limit 50 --out data_small      # quick test first

Each article is saved as data/<Title>.md  ("# Title" + plain text). Re-running skips files that
already exist, so you can stop and resume. Wikimedia asks for a descriptive User-Agent and polite
request rates; this script sleeps between requests.
"""

from __future__ import annotations

import argparse
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://en.wikipedia.org/w/api.php"
UA = "notesearch-lab-student-project/0.1 (personal learning project; contact: set-your-email@example.com)"

PRESETS = {
    "cs": ["Category:Machine learning", "Category:Databases", "Category:Information retrieval",
           "Category:Web development", "Category:Computer security", "Category:Operating systems",
           "Category:Software engineering", "Category:Algorithms"],
    "science": ["Category:Physics", "Category:Chemistry", "Category:Biology", "Category:Astronomy",
                "Category:Mathematics", "Category:Earth sciences"],
    "history": ["Category:Ancient history", "Category:Medieval history", "Category:Modern history",
                "Category:Wars", "Category:History of science"],
    "mixed": ["Category:Machine learning", "Category:Databases", "Category:Physics", "Category:Economics",
              "Category:Psychology", "Category:Cooking", "Category:Music theory", "Category:Health"],
}


def call(params: dict, delay: float) -> dict:
    url = API + "?" + urllib.parse.urlencode({**params, "format": "json", "formatversion": "2"})
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.load(r)
            time.sleep(delay)
            return data
        except Exception as e:  # network hiccup: back off and retry
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))
            print(f"  retrying after error: {e}")
    raise RuntimeError("unreachable")


def category_members(cat: str, kind: str, delay: float, cap: int = 500) -> list[str]:
    out, cont = [], {}
    while len(out) < cap:
        d = call({"action": "query", "list": "categorymembers", "cmtitle": cat, "cmtype": kind,
                  "cmlimit": "500", **cont}, delay)
        out += [m["title"] for m in d.get("query", {}).get("categorymembers", [])]
        if "continue" not in d:
            break
        cont = {"cmcontinue": d["continue"]["cmcontinue"]}
    return out[:cap]


def article_text(title: str, delay: float) -> str:
    d = call({"action": "query", "prop": "extracts", "explaintext": "1", "exsectionformat": "plain",
              "redirects": "1", "titles": title}, delay)
    pages = d.get("query", {}).get("pages", [])
    return (pages[0].get("extract") or "") if pages else ""


def safe_name(title: str) -> str:
    return re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", title).strip(" .")[:120] or "untitled"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preset", choices=sorted(PRESETS), help="ready-made topic list")
    ap.add_argument("--categories", nargs="*", default=[], help='e.g. "Category:Databases"')
    ap.add_argument("--limit", type=int, default=400, help="max articles to save")
    ap.add_argument("--min-words", type=int, default=150, help="skip stubs shorter than this")
    ap.add_argument("--max-words", type=int, default=6000, help="truncate very long articles")
    ap.add_argument("--out", default="data")
    ap.add_argument("--delay", type=float, default=0.3, help="seconds between requests")
    a = ap.parse_args()

    cats = list(a.categories) + (PRESETS[a.preset] if a.preset else [])
    if not cats:
        ap.error("give --preset or --categories")
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    # Collect candidate titles: pages in each category, plus pages of its direct subcategories.
    titles: list[str] = []
    seen: set[str] = set()
    per_cat = max(10, (a.limit * 3) // max(1, len(cats)))   # over-collect, stubs get filtered later
    for cat in cats:
        found = category_members(cat, "page", a.delay, per_cat)
        for sub in category_members(cat, "subcat", a.delay, 15):
            if len(found) >= per_cat:
                break
            found += category_members(sub, "page", a.delay, 40)
        added = 0
        for t in found:
            if t not in seen and not t.startswith(("List of", "Index of", "Outline of")):
                seen.add(t); titles.append(t); added += 1
        print(f"{cat}: {added} candidate articles")

    saved = len(list(out.glob("*.md")))
    for title in titles:
        if saved >= a.limit:
            break
        path = out / f"{safe_name(title)}.md"
        if path.exists():
            continue
        try:
            text = article_text(title, a.delay)
        except Exception as e:
            print(f"  skip {title!r}: {e}")
            continue
        words = text.split()
        if len(words) < a.min_words:
            continue
        text = " ".join(words[: a.max_words]) if len(words) > a.max_words else text
        path.write_text(f"# {title}\n\n{text}\n", encoding="utf-8")
        saved += 1
        if saved % 25 == 0:
            print(f"  saved {saved}/{a.limit}")
    print(f"done: {saved} articles in {out}/")


if __name__ == "__main__":
    main()
