#!/usr/bin/env python3
"""Originality check: flags any 10-word run an article shares with its sources.

    python3 tools/overlap_check.py content/articles/2026-10-08.json [more.json ...]

Fetches every source URL in the given article files and prints shared
10-word sequences. Exit code 1 if any article shares a run of 12+ words
(i.e. 3+ overlapping 10-grams in a row) or more than 6 overlapping 10-grams
in total -- reword those passages in your own words and run again.
Short shared fragments (names, addresses, agency names) are normal.
"""
import concurrent.futures as cf
import html
import json
import re
import sys
import urllib.request

N = 10


def words(t):
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
    return re.findall(r"[a-z0-9']+", html.unescape(re.sub(r"<[^>]+>", " ", t)).lower())


def get(u):
    try:
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (RenterNews originality check)"})
        return urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")
    except Exception:  # noqa: BLE001
        return ""


arts = []
for f in sys.argv[1:]:
    d = json.load(open(f, encoding="utf-8"))
    arts += d if isinstance(d, list) else [d]
urls = {s["url"] for a in arts for s in a.get("sources", [])}
with cf.ThreadPoolExecutor(12) as ex:
    pages = dict(zip(urls, ex.map(get, urls)))

bad = False
for a in arts:
    aw = words(a["body_html"])
    grams = [tuple(aw[i:i + N]) for i in range(len(aw) - N + 1)]
    src = set()
    fetched = 0
    for s in a.get("sources", []):
        sw = words(pages.get(s["url"], ""))
        fetched += bool(sw)
        src |= {tuple(sw[i:i + N]) for i in range(len(sw) - N + 1)}
    hits = [i for i, g in enumerate(grams) if g in src]
    run = best = 0
    for i, h in enumerate(hits):
        run = run + 1 if i and h == hits[i - 1] + 1 else 1
        best = max(best, run)
    flag = best >= 3 or len(hits) > 6
    bad |= flag
    print(f"{'REWORD' if flag else 'ok    '} {a['slug']}: sources fetched {fetched}/{len(a.get('sources', []))}, "
          f"overlapping 10-grams {len(hits)}, longest run {best + N - 1 if best else 0} words")
    for i in hits[:8]:
        print("        ", " ".join(grams[i]))
sys.exit(1 if bad else 0)
