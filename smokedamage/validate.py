#!/usr/bin/env python3
"""Pre-publish checks for the SmokeDamage.com build (run after build.py).

Exits non-zero on any error. Warnings are printed but don't fail the build.
Also used by the weekly automation before it publishes a new article/event.
"""
import glob
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(ROOT, "public")
sys.path.insert(0, ROOT)
from siteconfig import SITE  # noqa: E402

errors, warnings = [], []
err = lambda f, m: errors.append(f"{os.path.relpath(f, PUB)}: {m}")
warn = lambda f, m: warnings.append(f"{os.path.relpath(f, PUB)}: {m}")

FORBIDDEN = [
    r"fight the insurance compan", r"every penny", r"insurance companies always", r"we guarantee",
    r"guaranteed (?:settlement|payment|result|outcome|payout)", r"maximi[sz]e your (?:settlement|claim|payout)",
    r"get (?:you )?(?:more|the most) money", r"bad[- ]faith insurers", r"insurers? (?:are|is) dishonest",
    r"in today's world", r"navigating the complexities", r"\bdelve\b", r"rest assured", r"peace of mind",
    r"lorem ipsum", r"\bTODO\b", r"\{\{", r"^\s*:::",
]
# Things we must never claim to do (we are not a restoration contractor).
CONTRACTOR = [r"\bwe (?:clean|remediate|restore|rebuild|repair|demolish|remove soot)\b", r"\bour (?:restoration|cleaning|remediation) (?:crew|team|services)\b"]

pages = sorted(glob.glob(os.path.join(PUB, "**", "*.html"), recursive=True))
titles, descs = {}, {}
for f in pages:
    rel = "/" + os.path.relpath(f, PUB)
    s = open(f, encoding="utf-8").read()
    noindex = 'content="noindex' in s
    text = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S)))

    h1 = re.findall(r"<h1[\s>]", s)
    if len(h1) != 1:
        err(f, f"{len(h1)} <h1> tags")
    t = re.search(r"<title>(.*?)</title>", s, re.S)
    d = re.search(r'<meta name="description" content="([^"]*)"', s)
    if not t or not t.group(1).strip():
        err(f, "missing <title>")
    if not d or not d.group(1).strip():
        err(f, "missing meta description")
    if t and not noindex:
        tt = html.unescape(t.group(1))
        if tt in titles:
            err(f, f"duplicate title with {titles[tt]}")
        titles[tt] = rel
        if len(tt) > 70:
            warn(f, f"title {len(tt)} chars")
    if d and not noindex:
        dd = html.unescape(d.group(1))
        if dd in descs:
            err(f, f"duplicate description with {descs[dd]}")
        descs[dd] = rel
        if len(dd) > 150:
            (err if "/blog/" in rel else warn)(f, f"meta description {len(dd)} chars (max 150)")
    if not noindex and '<link rel="canonical"' not in s and not rel.endswith("404.html"):
        err(f, "missing canonical")
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            data = json.loads(m.group(1))
            types = [g.get("@type") for g in data.get("@graph", [])]
            if "FAQPage" in types and "<details class=\"faq-item\"" not in s:
                err(f, "FAQPage schema without visible FAQ")
            if any(x in ("Review", "AggregateRating") for x in types) or '"aggregateRating"' in m.group(1):
                err(f, "review/rating schema is not allowed")
        except Exception as e:
            err(f, f"invalid JSON-LD: {e}")
    for m in re.finditer(r"<img\b[^>]*>", s):
        if "alt=" not in m.group(0):
            err(f, "img without alt")
        elif re.search(r'alt=""', m.group(0)):
            warn(f, "empty alt on img")
    # internal links + assets
    for m in re.finditer(r'(?:href|src)="(/[^"#?]*)', s):
        u = m.group(1)
        if u.startswith(("/api/", "/admin/")):
            continue
        target = os.path.join(PUB, u.lstrip("/"))
        ok = os.path.isfile(target) or os.path.isfile(os.path.join(target, "index.html")) or (u == "/" and os.path.isfile(os.path.join(PUB, "home.html")))
        if not ok:
            err(f, f"broken link {u}")
    for m in re.finditer(r'srcset="([^"]+)"', s):
        for part in m.group(1).split(","):
            u = part.strip().split(" ")[0]
            if u.startswith("/") and not os.path.isfile(os.path.join(PUB, u.lstrip("/"))):
                err(f, f"missing srcset asset {u}")
    for pat in FORBIDDEN:
        if re.search(pat, text, re.I | re.M):
            err(f, f"forbidden phrase /{pat}/")
    for pat in CONTRACTOR:
        mm = re.search(pat, text, re.I)
        if mm:
            ctx = text[max(0, mm.start() - 60): mm.end() + 60].replace("\n", " ")
            if not re.search(r"\b(?:not|never|don't|do not|doesn't)\b", ctx, re.I):
                err(f, f"possible contractor claim: …{ctx.strip()}…")
    # advertising disclosure (Tex. Ins. Code 4102.113): name, address, license number on every page
    if rel not in ("/admin/index.html",):
        for needle in (SITE["company"], SITE["license_number"]) + ((SITE["licensed_address"],) if SITE["licensed_address"] else ()):
            if html.escape(needle) not in s and needle not in s:
                err(f, f"missing required disclosure: {needle}")
    if "tel:+18445371427" not in s:
        err(f, "no clickable phone link")
    if "/blog/" in rel and rel.count("/") > 3 and not noindex:
        for need, label in (('"author"', "author schema"), ("article:published_time", "published date"), ('og:image', "image"), ("/contact/", "CTA")):
            if need not in s:
                err(f, f"blog post missing {label}")

# Homepage keyword usage
home = open(os.path.join(PUB, "home.html"), encoding="utf-8").read()
body = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style|head)[^>]*>.*?</\1>", " ", home, flags=re.S)))
body = re.sub(r"\s+", " ", body)
n1 = len(re.findall(r"Smoke Damage Public Adjuster", body))
n2 = len(re.findall(r"Texas Smoke Damage Public Adjuster", body))
print(f"homepage: 'Smoke Damage Public Adjuster' x{n1}, 'Texas Smoke Damage Public Adjuster' x{n2}")
if not 10 <= n1 <= 16:
    warnings.append(f"home.html: exact phrase count {n1} (target ~10-14)")
if not 3 <= n2 <= 5:
    warnings.append(f"home.html: Texas phrase count {n2} (target 3-5)")

# sitemap entries resolve
sm = open(os.path.join(PUB, "sitemap.xml")).read()
for loc in re.findall(r"<loc>https://smokedamage\.com(/[^<]*)</loc>", sm):
    t = os.path.join(PUB, loc.lstrip("/"))
    if not (loc == "/" or os.path.isfile(os.path.join(t, "index.html"))):
        errors.append(f"sitemap.xml: {loc} does not exist")

for w in warnings:
    print("WARN ", w)
for e in errors:
    print("ERROR", e)
print(f"{len(pages)} pages checked, {len(errors)} errors, {len(warnings)} warnings")
sys.exit(1 if errors else 0)
