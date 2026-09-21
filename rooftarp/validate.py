#!/usr/bin/env python3
"""Post-build checks for rooftarp.com.

    python3 build.py && python3 validate.py

Standard SEO/quality checks, plus the one that matters most for this site:
a cross-page near-duplicate detector.

The WordPress site this replaces was demoted by Google's August 2026 spam
update because its 158 city pages were 96-98% identical to one another. That
failure is easy to reintroduce -- the next person who needs a Tyler page will
be tempted to copy the Waco one and swap the city name. NEAR_DUPLICATE_LIMIT
makes the build fail if they do.
"""

import difflib
import html
import json
import os
import re
import sys
from itertools import combinations

ROOT = os.path.dirname(os.path.abspath(__file__))

# Two pages' unique body copy may not exceed this word-level similarity.
# The old city pages scored 0.98. Genuinely distinct pages on the same topic
# land around 0.25-0.45.
NEAR_DUPLICATE_LIMIT = 0.60

# Fingerprints that must never appear in the output: the sister site this
# generator was adapted from, and WordPress/Elementor remnants.
FORBIDDEN = [
    "huttoroofs",
    "Hutto Roofers",
    "elementor",
    "wp-content",
    "wp-includes",
    "TODO",
]

# Unreplaced template placeholders, e.g. {{CITY}}. Checked with a pattern
# rather than a bare "{{" so JSON-LD's closing braces do not trip it.
PLACEHOLDER = re.compile(r"\{\{\s*[A-Z_][A-Z0-9_]*\s*\}\}")

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


# --------------------------------------------------------------------------

def html_files():
    for dirpath, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in {".git", "__pycache__", "templates", "content"}]
        for f in files:
            # The Search Console verification files are HTML by name only --
            # single-line tokens Google requires at the document root.
            if f.endswith(".html") and not f.startswith("google"):
                yield os.path.join(dirpath, f)


def rel_url(path):
    r = os.path.relpath(path, ROOT).replace(os.sep, "/")
    if r == "index.html":
        return "/"
    if r == "404.html":
        return "/404.html"
    return "/" + r[: -len("index.html")]


def text_of(fragment):
    fragment = re.sub(r"(?is)<(script|style).*?</\1>", " ", fragment)
    t = re.sub(r"<[^>]+>", " ", fragment)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def body_region(doc):
    """The page's own copy: everything inside <main>, minus shared chrome.

    Shared chrome (header, footer, breadcrumbs, CTA bands, sidebar) is
    identical by design, so including it would mask real duplication.
    """
    m = re.search(r"(?is)<main[^>]*>(.*?)</main>", doc)
    frag = m.group(1) if m else doc
    for pat in [
        r"(?is)<nav class=\"breadcrumbs\".*?</nav>",
        r"(?is)<aside class=\"sidebar\">.*?</aside>",
        r"(?is)<section class=\"cta-band\">.*?</section>",
        r"(?is)<div class=\"hero-actions\">.*?</div>",
    ]:
        frag = re.sub(pat, " ", frag)
    return text_of(frag)


# --------------------------------------------------------------------------

def main():
    files = sorted(html_files())
    if not files:
        err("no HTML found — run build.py first")
        report()

    pages = {}
    for fp in files:
        doc = open(fp, encoding="utf-8").read()
        pages[rel_url(fp)] = {"file": fp, "doc": doc, "body": body_region(doc)}

    print(f"Checking {len(pages)} pages\n")

    titles, descs = {}, {}

    for url, p in sorted(pages.items()):
        doc = p["doc"]

        # ---- title / description ----------------------------------------
        m = re.search(r"(?is)<title>(.*?)</title>", doc)
        if not m:
            err(f"{url}: no <title>")
        else:
            t = html.unescape(m.group(1)).strip()
            p["title"] = t
            if len(t) > 65:
                warn(f"{url}: title is {len(t)} chars (over 65)")
            if t in titles:
                err(f"{url}: duplicate title, same as {titles[t]}")
            titles[t] = url

        m = re.search(r'(?is)<meta name="description" content="(.*?)"', doc)
        if not m:
            err(f"{url}: no meta description")
        else:
            d = html.unescape(m.group(1)).strip()
            if not (50 <= len(d) <= 170):
                warn(f"{url}: meta description is {len(d)} chars (want 50-170)")
            if d in descs:
                err(f"{url}: duplicate meta description, same as {descs[d]}")
            descs[d] = url

        # ---- one H1 ------------------------------------------------------
        h1s = re.findall(r"(?is)<h1[^>]*>(.*?)</h1>", doc)
        if len(h1s) != 1:
            err(f"{url}: found {len(h1s)} <h1> elements (want exactly 1)")

        # ---- canonical ---------------------------------------------------
        m = re.search(r'(?is)<link rel="canonical" href="([^"]+)"', doc)
        if not m:
            err(f"{url}: no canonical")
        elif url != "/404.html" and not m.group(1).endswith(url):
            err(f"{url}: canonical points to {m.group(1)}")

        # ---- JSON-LD parses ----------------------------------------------
        blocks = re.findall(
            r'(?is)<script type="application/ld\+json">(.*?)</script>', doc
        )
        if not blocks:
            err(f"{url}: no JSON-LD")
        for b in blocks:
            try:
                json.loads(b)
            except json.JSONDecodeError as e:
                err(f"{url}: invalid JSON-LD — {e}")

        # ---- forbidden fingerprints --------------------------------------
        low = doc.lower()
        for bad in FORBIDDEN:
            if bad.lower() in low:
                err(f"{url}: contains forbidden string {bad!r}")
        for ph in set(PLACEHOLDER.findall(doc)):
            err(f"{url}: unreplaced template placeholder {ph}")

        # ---- body has real content ---------------------------------------
        words = len(p["body"].split())
        p["words"] = words
        if url not in ("/404.html", "/sitemap/") and words < 250:
            warn(f"{url}: only {words} words of unique body copy")

    # ---- internal links resolve -------------------------------------------
    known = set(pages)
    for url, p in sorted(pages.items()):
        for href in set(re.findall(r'href="(/[^"#?]*)"', p["doc"])):
            if href.startswith(("/assets/", "/favicon")):
                target = os.path.join(ROOT, href.lstrip("/"))
                if not os.path.exists(target):
                    err(f"{url}: missing asset {href}")
            elif href in ("/sitemap.xml", "/robots.txt"):
                if not os.path.exists(os.path.join(ROOT, href.lstrip("/"))):
                    err(f"{url}: missing file {href}")
            elif href not in known:
                err(f"{url}: broken internal link {href}")

    # ---- keyword presence --------------------------------------------------
    sys.path.insert(0, ROOT)
    from content.services import SERVICES
    from content.areas import AREAS

    for s in SERVICES:
        u = f"/services/{s['slug']}/"
        p = pages.get(u)
        if not p:
            err(f"missing service page {u}")
            continue
        kw = s["keyword"].lower()
        if kw not in p.get("title", "").lower():
            warn(f"{u}: keyword {kw!r} not in title")
        if kw.replace("/", "") not in p["body"].lower().replace("/", ""):
            err(f"{u}: keyword {kw!r} not in body copy")

    for a in AREAS:
        u = f"/service-areas/{a['slug']}/"
        p = pages.get(u)
        if not p:
            err(f"missing area page {u}")
            continue
        if a["city"].lower() not in p["body"].lower():
            err(f"{u}: city {a['city']!r} not in body copy")
        if a["county"].lower() not in p["body"].lower():
            warn(f"{u}: county {a['county']!r} not in body copy")

    # ---- sitemap coverage --------------------------------------------------
    sm = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(sm):
        err("sitemap.xml missing")
    else:
        locs = re.findall(r"<loc>https://rooftarp\.com(/[^<]*)</loc>", open(sm).read())
        for u in locs:
            if u not in known:
                err(f"sitemap.xml lists {u} but no such page was built")
        indexable = {
            u
            for u, p in pages.items()
            if 'name="robots" content="noindex' not in p["doc"] and u != "/404.html"
        }
        for u in sorted(indexable - set(locs)):
            warn(f"{u} is indexable but not in sitemap.xml")

    # ---- THE duplicate-content guard ---------------------------------------
    print("Near-duplicate scan (limit "
          f"{NEAR_DUPLICATE_LIMIT:.2f})...")
    scored = []
    checkable = {
        u: p["body"].lower().split()
        for u, p in pages.items()
        if p.get("words", 0) >= 250
    }
    for (u1, w1), (u2, w2) in combinations(sorted(checkable.items()), 2):
        # Cheap length prefilter — very different lengths cannot be near-dupes.
        lo, hi = sorted((len(w1), len(w2)))
        if hi == 0 or lo / hi < NEAR_DUPLICATE_LIMIT:
            continue
        ratio = difflib.SequenceMatcher(None, w1, w2).ratio()
        scored.append((ratio, u1, u2))
        if ratio >= NEAR_DUPLICATE_LIMIT:
            err(f"NEAR-DUPLICATE: {u1} and {u2} are {ratio*100:.1f}% identical")

    if scored:
        scored.sort(reverse=True)
        print("  highest similarity pairs:")
        for ratio, u1, u2 in scored[:5]:
            print(f"    {ratio*100:5.1f}%  {u1}  vs  {u2}")
        worst = scored[0][0]
        print(f"  worst: {worst*100:.1f}%  (limit {NEAR_DUPLICATE_LIMIT*100:.0f}%)\n")

    report(pages)


def report(pages=None):
    for w in warnings:
        print(f"  WARN  {w}")
    if warnings:
        print()
    for e in errors:
        print(f"  FAIL  {e}")
    if errors:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
        sys.exit(1)
    if pages:
        total = sum(p.get("words", 0) for p in pages.values())
        print(f"OK — {len(pages)} pages, {total:,} words of unique body copy, "
              f"{len(warnings)} warning(s)")
    sys.exit(0)


if __name__ == "__main__":
    main()
