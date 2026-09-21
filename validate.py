#!/usr/bin/env python3
"""Post-build checks: JSON-LD validity, internal links, SEO basics, no WP leftovers."""

import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.abspath(__file__))
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}
errors, warnings = [], []


class Checker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.bad = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.bad.append(f"stray </{tag}>")
        elif self.stack[-1] == tag:
            self.stack.pop()
        elif tag in self.stack:
            while self.stack and self.stack[-1] != tag:
                self.bad.append(f"unclosed <{self.stack.pop()}> before </{tag}>")
            if self.stack:
                self.stack.pop()
        else:
            self.bad.append(f"stray </{tag}>")


def pages():
    for dirpath, _dirs, files in os.walk(ROOT):
        if any(part in dirpath for part in (".git", "assets", "__pycache__", "templates", "backup", "dist")):
            continue
        for f in files:
            if f.endswith(".html"):
                yield os.path.join(dirpath, f)


def site_path(fs_path):
    rel = os.path.relpath(fs_path, ROOT)
    if rel.endswith("index.html"):
        p = "/" + rel[: -len("index.html")]
        return p if p != "/" else "/"
    return "/" + rel


all_paths = set()
for f in pages():
    all_paths.add(site_path(f))
all_paths |= {"/sitemap.xml", "/robots.txt", "/favicon.ico", "/favicon-96x96.png",
              "/apple-touch-icon.png", "/favicon.svg", "/site.webmanifest",
              "/web-app-manifest-192x192.png", "/web-app-manifest-512x512.png"}
for dirpath, _d, files in os.walk(os.path.join(ROOT, "assets")):
    for f in files:
        all_paths.add("/" + os.path.relpath(os.path.join(dirpath, f), ROOT))

titles, descs = {}, {}

for fs in sorted(pages()):
    sp = site_path(fs)
    html = open(fs, encoding="utf-8").read()

    # --- well-formedness ---
    c = Checker()
    c.feed(html)
    if c.bad:
        errors.append(f"{sp}: unbalanced tags -> {c.bad[:5]}")
    if c.stack:
        errors.append(f"{sp}: never closed -> {c.stack[:5]}")

    # --- JSON-LD ---
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            json.loads(m.group(1))
        except Exception as e:
            errors.append(f"{sp}: invalid JSON-LD: {e}")

    # --- single H1 ---
    h1s = re.findall(r"<h1\b", html)
    if len(h1s) != 1:
        errors.append(f"{sp}: {len(h1s)} <h1> tags (want 1)")

    # --- title / description ---
    t = re.search(r"<title>(.*?)</title>", html, re.S)
    d = re.search(r'<meta name="description" content="(.*?)">', html, re.S)
    if not t:
        errors.append(f"{sp}: no <title>")
    else:
        titles.setdefault(t.group(1), []).append(sp)
        if len(t.group(1)) > 65:
            warnings.append(f"{sp}: title {len(t.group(1))} chars")
    if not d:
        errors.append(f"{sp}: no meta description")
    else:
        descs.setdefault(d.group(1), []).append(sp)
        if len(d.group(1)) > 165:
            warnings.append(f"{sp}: description {len(d.group(1))} chars")

    # --- canonical ---
    if not re.search(r'<link rel="canonical"', html):
        errors.append(f"{sp}: no canonical")

    # --- no WordPress / source-site leftovers (brief §7) ---
    # Source cities, their counties and zip codes, plus WP fingerprints.
    for bad in ["wp-content", "wp-includes", "elementor", "litespeed", "wp-json",
                "templeroofs", "kyleroofs", "copperascoveroofs",
                "Temple", "Belton", "Kyle", "Copperas Cove", "Harker Heights",
                "Killeen", "Buda", "San Marcos",
                "Bell County", "Coryell County", "Hays County",
                "76501", "76502", "76504", "76508", "76513", "76522", "76548", "78640"]:
        if bad.lower() in html.lower():
            errors.append(f"{sp}: contains '{bad}'")
    # Only Hutto Roofers' own number may appear, in any formatting.
    for num in set(re.findall(r"\+?1?[\s.-]?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}", html)):
        if re.sub(r"\D", "", num)[-10:] != "5122977580":
            errors.append(f"{sp}: unexpected phone number {num!r}")
    # And only Hutto's zip.
    for z in set(re.findall(r"\b7[5-9]\d{3}\b", re.sub(r"<script.*?</script>", "", html, flags=re.S))):
        if z != "78634":
            errors.append(f"{sp}: unexpected zip code {z}")

    # --- internal links resolve ---
    for href in re.findall(r'href="(/[^"#?]*)', html):
        if href not in all_paths:
            errors.append(f"{sp}: broken internal link -> {href}")

    # --- images resolve ---
    for src in re.findall(r'src="(/[^"]+)"', html):
        if src not in all_paths:
            errors.append(f"{sp}: missing asset -> {src}")

    # --- every img has alt ---
    for tag in re.findall(r"<img\b[^>]*>", html):
        if "alt=" not in tag:
            errors.append(f"{sp}: <img> without alt")

    # --- footer service-area line present ---
    if "Serving Hutto, Round Rock, Pflugerville, Taylor, Georgetown &amp; Manor" not in html:
        errors.append(f"{sp}: footer serving line missing")

for val, paths in titles.items():
    if len(paths) > 1:
        errors.append(f"duplicate title {val!r} on {paths}")
for val, paths in descs.items():
    if len(paths) > 1:
        errors.append(f"duplicate description on {paths}")

# --- keyword placement on the money pages ---
sys.path.insert(0, ROOT)
from content.services import SERVICES          # noqa: E402
from content.areas import AREAS                # noqa: E402

for item in SERVICES + AREAS:
    fs = os.path.join(ROOT, item["path"].strip("/"), "index.html")
    html = open(fs, encoding="utf-8").read().lower()
    kw = item["keyword"].lower()
    words = kw.split()
    title = re.search(r"<title>(.*?)</title>", html, re.S).group(1)
    desc = re.search(r'<meta name="description" content="(.*?)">', html, re.S).group(1)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S).group(1)
    h1 = re.sub(r"<[^>]+>", "", h1)
    body = re.sub(r"<[^>]+>", " ", html)
    for label, hay in [("title", title), ("meta", desc), ("h1", h1)]:
        if not all(w in hay for w in words):
            errors.append(f"{item['path']}: keyword {kw!r} missing from {label}: {hay[:90]!r}")
    if kw not in re.sub(r"\s+", " ", body):
        errors.append(f"{item['path']}: exact keyword {kw!r} not in body")

# --- homepage keywords ---
# The primary keyword must appear verbatim. The secondaries are allowed to
# appear as natural variants ("a roofer in Hutto, TX"), so those are matched as
# an in-order token sequence within a short window rather than as a literal.
home_text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", open(
    os.path.join(ROOT, "index.html"), encoding="utf-8").read().lower()))

if "roofing hutto tx" not in home_text:
    errors.append("/: primary keyword 'roofing hutto tx' not in homepage body")

def near_sequence(text, phrase, window=5):
    """True if the phrase's words appear in order with few words between them."""
    toks = re.findall(r"[a-z]+", text)
    want = re.findall(r"[a-z]+", phrase)
    for i in range(len(toks)):
        j, gap = 0, 0
        for t in toks[i:]:
            if t == want[j]:
                j += 1
                if j == len(want):
                    return True
            elif j:
                gap += 1
                if gap > window:
                    break
        # keep scanning from the next start position
    return False

for kw in ["hutto roofing company", "roofer hutto tx", "roofers in hutto texas",
           "hutto roofing contractor"]:
    if not near_sequence(home_text, kw):
        warnings.append(f"/: homepage secondary keyword {kw!r} not found")

# --- blog keywords: title, H1, meta and body ---
from content.blog import POSTS                 # noqa: E402
for post in POSTS:
    fs = os.path.join(ROOT, post["path"].strip("/"), "index.html")
    html = open(fs, encoding="utf-8").read().lower()
    kw = post["keyword"].lower()
    title = re.search(r"<title>(.*?)</title>", html, re.S).group(1)
    desc = re.search(r'<meta name="description" content="(.*?)">', html, re.S).group(1)
    h1 = re.sub(r"<[^>]+>", "", re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S).group(1))
    body = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))
    for label, hay in [("title", title), ("meta", desc), ("h1", h1), ("body", body)]:
        if not near_sequence(hay, kw, window=3):
            errors.append(f"{post['path']}: keyword {kw!r} missing from {label}")

print(f"{len(list(pages()))} HTML pages checked")
if warnings:
    print(f"\n{len(warnings)} warning(s):")
    for w in warnings:
        print("  ! " + w)
if errors:
    print(f"\n{len(errors)} ERROR(s):")
    for e in errors[:60]:
        print("  x " + e)
    sys.exit(1)
print("\nAll checks passed.")
