#!/usr/bin/env python3
"""Fetch one Creative Commons hero image per page from Openverse.

Reads content/pages/*.json (image_queries) plus EXTRA below, downloads the
first suitable CC0 / CC BY / public-domain result not already used, and writes
public/assets/img/<slug>.webp (1600w) and <slug>-sm.webp (800w). Licence and
attribution go to content/credits.json, which build.py prints on each page.

Re-running skips slugs already in credits.json; delete an entry (and its
images) to re-pick it, or add its URL to content/image-blocklist.txt.
"""
import io, json, sys, time, urllib.parse, urllib.request
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "public/assets/img"
CREDITS = ROOT / "content/credits.json"
BLOCK = ROOT / "content/image-blocklist.txt"
API = "https://api.openverse.org/v1/images/"
UA = {"User-Agent": "asmith-photography-build/1.0"}

# Pages that are not article JSON files.
EXTRA = {
    "home-hero": ["city night street", "night city"],
    "home-skate": ["skateboarding", "skateboarder"],
    "home-editorial": ["fashion model", "portrait woman"],
    "home-sport": ["cycling", "athlete running"],
    "home-footwear": ["shoes sneakers", "leather shoes"],
    "about": ["vintage camera", "film camera"],
    "contact": ["camera lens", "photographer"],
    "journal": ["film roll", "darkroom"],
}


def get(url, timeout=60):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _query(params):
    data = json.loads(get(API + "?" + urllib.parse.urlencode(params)))
    time.sleep(1.5)
    return data.get("results", [])


def search(q):
    """StockSnap (curated CC0 photography) first, then the wider CC pool."""
    words = q.split()
    out = []
    for n in range(len(words), 0, -1):
        out += _query({"q": " ".join(words[:n]), "source": "stocksnap", "page_size": 12})
        if len(out) >= 6:
            break
    out += _query({"q": q, "license": "cc0,by,pdm", "page_size": 12,
                   "aspect_ratio": "wide", "size": "large", "mature": "false"})
    return [r for r in out if (r.get("width") or 0) >= (r.get("height") or 1)]


def save(slug, raw):
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    if im.width < 900:
        raise ValueError("too small")
    for suffix, w in (("", 1600), ("-sm", 800)):
        c = im.copy()
        if c.width > w:
            c = c.resize((w, round(c.height * w / c.width)), Image.LANCZOS)
        c.save(OUT / f"{slug}{suffix}.webp", "WEBP", quality=78, method=6)
    return im.width, im.height


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    credits = json.loads(CREDITS.read_text()) if CREDITS.exists() else {}
    blocked = set(BLOCK.read_text().split()) if BLOCK.exists() else set()
    used = {c["source"] for c in credits.values()}
    jobs = dict(EXTRA)
    for f in sorted((ROOT / "content/pages").glob("*.json")):
        p = json.loads(f.read_text())
        jobs[p["slug"]] = p.get("image_queries") or [p["h1"]]
    picks = json.loads((ROOT / "content/image-picks.json").read_text()) \
        if (ROOT / "content/image-picks.json").exists() else {}
    only = set(sys.argv[1:])
    for slug, queries in jobs.items():
        if (only and slug not in only) or (slug in credits and not only):
            continue
        done = False
        if slug in picks:
            queries = [picks[slug]["q"]] + list(queries)
        for q in queries:
            try:
                results = search(q)
            except Exception as e:
                print("search fail", slug, q, e); time.sleep(10); continue
            time.sleep(2)
            if slug in picks and q == picks[slug]["q"]:
                results = results[picks[slug]["i"]:] + results[:picks[slug]["i"]]
            for r in results:
                src = r["url"]
                if src in used or src in blocked or r.get("mature"):
                    continue
                try:
                    w, h = save(slug, get(src))
                except Exception:
                    continue
                credits[slug] = {
                    "title": r.get("title") or "Untitled", "creator": r.get("creator") or "Unknown",
                    "creator_url": r.get("creator_url"), "landing": r.get("foreign_landing_url"),
                    "license": r["license"], "license_version": r.get("license_version"),
                    "license_url": r.get("license_url"), "source": src, "query": q,
                }
                used.add(src); done = True
                print("ok", slug, "<-", q, "|", r.get("title"))
                break
            if done:
                break
        if not done:
            print("MISSING", slug)
        CREDITS.write_text(json.dumps(credits, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
