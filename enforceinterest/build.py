#!/usr/bin/env python3
"""Build enforceinterest.com into ./public.

    python3 build.py && python3 validate.py

Needs Python 3 and Pillow (only for the generated share/feature images, which
are cached in assets/img/gen/ and rebuilt only when their text changes).
Page copy lives in content/; shared constants and components in lib.py.
"""
import hashlib
import json
import os
import re
import shutil
import sys
from xml.sax.saxutils import escape as xesc

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")      # -> public_html
PAGES = os.path.join(OUT, "_pages")     # HTML pages, served only through index.php
sys.path.insert(0, ROOT)

import lib  # noqa: E402
from lib import SITE, NAME, EMAIL, FIRM, LICENSE, ASSET_V, BUILD_DATE, esc, icon, MARK_SVG  # noqa: E402
from content import home, pages, tools, posts, seo  # noqa: E402

# ------------------------------------------------------------------ navigation
NAV = [
    ("Texas law", "dd", [
        ("/texas-prompt-payment-act/", "Texas Prompt Payment Act", "Chapter 542 deadlines, section by section"),
        ("/blog/18-standard-rate-explained/", "The 18% standard rate", "§542.060(a) interest on non-weather claims"),
        ("/blog/act-of-god-floating-rate/", "Act of God floating rate", f"§542.060(c) — currently {lib.FLOAT_RATE_S}"),
        ("/texas-judgment-interest-rate/", "Judgment interest rate", "OCCC §304.003 rate history"),
        ("/texas-prejudgment-interest/", "Prejudgment interest", "How Texas courts add it, with calculator"),
        ("/blog/texas-insurance-claim-deadlines/", "Every claim deadline", "Ch. 542, 542A, TWIA and limitations"),
        ("/faq/", "FAQ", "Straight answers to common questions"),
    ]),
    ("Claims", "dd", [
        ("/hail-wind-claims/", "Hail &amp; wind claims", "Roof and storm losses under Ch. 542A"),
        ("/hurricane-claims/", "Hurricane claims", "Gulf Coast, TWIA and named-storm deductibles"),
        ("/fire-smoke-damage/", "Fire &amp; smoke damage", "Full 18% rate, smoke scope disputes"),
        ("/water-plumbing-damage/", "Water &amp; plumbing damage", "Sudden discharge, mold and freeze"),
        ("/post-appraisal-interest-recovery/", "Post-appraisal interest", "Hinojos: the award doesn&rsquo;t end it"),
        ("/long-term-claim-supplements/", "Claim supplements", "Late supplement payments and interest"),
        ("/does-my-claim-qualify/", "Does my claim qualify?", "Two-minute eligibility check"),
    ]),
    ("Tools", "wide", [(t["path"], t["short"], t["blurb"]) for t in tools.TOOL_LIST]),
    ("Blog", "/blog/", None),
    ("About", "/about-us/", None),
]


def header(path):
    desk, mob = [], []
    for label, kind, items in NAV:
        if items is None:
            cur = ' aria-current="page"' if path == kind or (kind != "/" and path.startswith(kind)) else ""
            desk.append(f'<a href="{kind}"{cur}>{label}</a>')
            mob.append(f'<a href="{kind}">{label}</a>')
            continue
        links = "".join(f'<a href="{h}"><b>{t}</b><span>{d}</span></a>' for h, t, d in items)
        cls = "dropdown wide" if kind == "wide" else "dropdown"
        desk.append(f'<div class="nav-item"><button type="button" aria-expanded="false">{label}{icon("chev")}</button>'
                    f'<div class="{cls}">{links}</div></div>')
        mob.append(f'<h4>{label}</h4>' + "".join(f'<a href="{h}">{t}</a>' for h, t, d in items))
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="scroll-progress" aria-hidden="true"><span></span></div>
<header class="site-header">
  <div class="wrap hdr-in">
    <a class="logo" href="/" aria-label="{NAME} home">{MARK_SVG}<span>Enforce <em>Interest</em></span></a>
    <nav class="nav-desktop" aria-label="Main">{"".join(desk)}<a class="btn btn-primary btn-sm nav-cta" href="/contact/">Free claim review</a></nav>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="mobile-nav" aria-label="Open menu"><span></span><span></span><span></span></button>
  </div>
  <nav class="nav-mobile" id="mobile-nav" aria-label="Mobile">
    <a href="/">Home</a>{"".join(mob)}<a href="/contact/">Contact</a>
    <a class="btn btn-primary" href="/contact/">Free claim review</a>
  </nav>
</header>'''


def footer():
    tl = "".join(f'<li><a href="{t["path"]}">{t["short"]}</a></li>' for t in tools.TOOL_LIST[:7])
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="logo" href="/">{MARK_SVG}<span>Enforce <em>Interest</em></span></a>
        <p style="margin-top:16px">A {FIRM} service. Texas-licensed public adjusting focused on prompt-payment
        statutory interest under Texas Insurance Code Chapter 542, for homeowners and commercial policyholders statewide.</p>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a><br>{lib.CITY}, Texas &middot; Serving all of Texas</p>
      </div>
      <div><h4>The rule</h4><ul>
        <li><a href="/texas-prompt-payment-act/">Texas Prompt Payment Act</a></li>
        <li><a href="/blog/18-standard-rate-explained/">18% standard rate</a></li>
        <li><a href="/blog/act-of-god-floating-rate/">Act of God floating rate</a></li>
        <li><a href="/texas-judgment-interest-rate/">Judgment interest rate</a></li>
        <li><a href="/texas-prejudgment-interest/">Prejudgment interest</a></li>
        <li><a href="/does-my-claim-qualify/">Does my claim qualify?</a></li>
      </ul></div>
      <div><h4>Claim types</h4><ul>
        <li><a href="/hail-wind-claims/">Hail &amp; wind claims</a></li>
        <li><a href="/hurricane-claims/">Hurricane claims</a></li>
        <li><a href="/fire-smoke-damage/">Fire &amp; smoke damage</a></li>
        <li><a href="/water-plumbing-damage/">Water &amp; plumbing damage</a></li>
        <li><a href="/post-appraisal-interest-recovery/">Post-appraisal interest</a></li>
        <li><a href="/long-term-claim-supplements/">Claim supplements</a></li>
      </ul></div>
      <div><h4>Free tools</h4><ul>{tl}<li><a href="/tools/">All tools &rarr;</a></li></ul></div>
      <div><h4>Company</h4><ul>
        <li><a href="/about-us/">About us</a></li>
        <li><a href="/contact/">Free claim review</a></li>
        <li><a href="/blog/">Blog</a></li>
        <li><a href="/faq/">FAQ</a></li>
        <li><a href="/privacy-policy/">Privacy policy</a></li>
        <li><a href="/terms-of-use/">Terms of use</a></li>
        <li><a href="/disclaimer/">Disclaimer</a></li>
        <li><a href="/sitemap/">Sitemap</a></li>
      </ul>
      <h4 style="margin-top:22px">Authorities</h4><ul>
        <li><a href="https://statutes.capitol.texas.gov/Docs/IN/htm/IN.542.htm" rel="noopener" target="_blank">Tex. Ins. Code ch. 542</a></li>
        <li><a href="https://www.tdi.texas.gov/" rel="noopener" target="_blank">Texas Dept. of Insurance</a></li>
        <li><a href="https://occc.texas.gov/publications/interest-rates/" rel="noopener" target="_blank">OCCC judgment rates</a></li>
      </ul></div>
    </div>
    <div class="foot-legal">{NAME} is a service of {FIRM}, a public adjusting firm licensed by the Texas Department of
    Insurance (license #{LICENSE}). We are not a law firm and do not provide legal advice; nothing on this site creates an
    attorney&ndash;client relationship. Information here is general and educational: outcomes depend on the facts of each
    claim, the policy language and the carrier&rsquo;s conduct, and past results do not guarantee future recoveries.
    Under Tex. Ins. Code §4102.158, a public adjuster may not solicit employment for an attorney; we do not refer claims
    to attorneys for a fee. Public adjuster compensation in Texas is capped at 10% of the insurance settlement on the
    claim (§4102.104). Service area: Texas only.</div>
    <div class="foot-bottom"><span>&copy; {lib.YEAR} {FIRM} &middot; All rights reserved</span><span>enforceinterest.com &middot; {lib.CITY} &middot; Texas</span></div>
  </div>
</footer>
<button class="to-top" type="button" aria-label="Back to top">&uarr;</button>'''


# ------------------------------------------------------------------ images
IMG = {}   # name -> (w, h) for every image in assets/img (filled by scan_images)


def scan_images():
    from PIL import Image
    d = os.path.join(ROOT, "assets", "img")
    for dirpath, _, files in os.walk(d):
        for f in files:
            if f.endswith(".jpg") or f.endswith(".png"):
                rel = os.path.relpath(os.path.join(dirpath, f), d)
                with Image.open(os.path.join(dirpath, f)) as im:
                    IMG[rel.rsplit(".", 1)[0]] = im.size


def make_card(name, kicker, title, size=(1200, 630), motif="ring"):
    """Typographic share/feature card. Cached by a hash of its inputs."""
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    gen = os.path.join(ROOT, "assets", "img", "gen")
    os.makedirs(gen, exist_ok=True)
    key = hashlib.md5(json.dumps([kicker, title, size, motif, 4]).encode()).hexdigest()[:10]
    stamp = os.path.join(gen, name + ".key")
    jpg, webp = os.path.join(gen, name + ".jpg"), os.path.join(gen, name + ".webp")
    if os.path.exists(stamp) and open(stamp).read() == key and os.path.exists(jpg):
        return "gen/" + name
    W, H = size
    s = 2
    im = Image.new("RGB", (W * s, H * s), (23, 13, 12))
    glow = Image.new("RGB", (W * s, H * s), (23, 13, 12))
    g = ImageDraw.Draw(glow)
    g.ellipse((int(W * s * .45), -int(H * s * .6), int(W * s * 1.4), int(H * s * .7)), fill=(120, 26, 24))
    g.ellipse((-int(W * s * .4), int(H * s * .55), int(W * s * .45), int(H * s * 1.6)), fill=(70, 50, 20))
    glow = glow.filter(ImageFilter.GaussianBlur(160 * s))
    im = Image.blend(im, glow, .85)
    d = ImageDraw.Draw(im)
    for x in range(0, W * s, 56 * s):
        d.line([(x, 0), (x, H * s)], fill=(40, 26, 24), width=1)
    for y in range(0, H * s, 56 * s):
        d.line([(0, y), (W * s, y)], fill=(40, 26, 24), width=1)
    F = os.path.join(ROOT, "tools", "fonts")
    serif = os.path.join(F, "Fraunces-SemiBold.ttf")
    ital = os.path.join(F, "Fraunces-Italic.ttf")
    mono = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Medium.ttf"
    if not os.path.exists(mono):
        mono = serif
    sect = ImageFont.truetype(ital, int(H * 1.25 * s))
    d.text((int(W * .70 * s), int(-H * .22 * s)), "§", font=sect, fill=(52, 30, 27))
    # motif: a 60-day progress ring
    cx, cy, r = int(W * .83 * s), int(H * .50 * s), int(min(W, H) * .26 * s)
    if motif == "ring":
        d.arc((cx - r, cy - r, cx + r, cy + r), 0, 360, fill=(60, 40, 36), width=14 * s)
        d.arc((cx - r, cy - r, cx + r, cy + r), -90, 200, fill=(201, 162, 79), width=14 * s)
        d.arc((cx - r, cy - r, cx + r, cy + r), 200, 260, fill=(255, 106, 77), width=14 * s)
    elif motif == "bars":
        for i, hgt in enumerate([.35, .5, .42, .62, .58, .78, .9]):
            x0 = int(W * .66 * s) + i * 44 * s
            d.rounded_rectangle((x0, int(H * (.82 - hgt * .6) * s), x0 + 26 * s, int(H * .82 * s)), 6 * s,
                                fill=(201, 162, 79) if i < 6 else (255, 106, 77))
    pad = 72 * s
    kf = ImageFont.truetype(mono, 24 * s)
    d.text((pad, pad), kicker.upper(), font=kf, fill=(201, 162, 79))
    maxw = int(W * (.62 if motif else .86) * s)
    fs = 66 if len(title) < 60 else 56 if len(title) < 90 else 48
    while True:
        tf = ImageFont.truetype(serif, fs * s)
        words, lines, cur = title.split(), [], ""
        for w_ in words:
            t = (cur + " " + w_).strip()
            if d.textlength(t, font=tf) <= maxw:
                cur = t
            else:
                lines.append(cur)
                cur = w_
        lines.append(cur)
        if len(lines) * fs * 1.16 < H * .58 or fs < 36:
            break
        fs -= 4
    y = pad + 60 * s
    for ln in lines:
        d.text((pad, y), ln, font=tf, fill=(255, 253, 248))
        y += int(fs * 1.16 * s)
    bf = ImageFont.truetype(serif, 34 * s)
    bi = ImageFont.truetype(ital, 34 * s)
    by = H * s - pad - 34 * s
    d.ellipse((pad, by - 6 * s, pad + 46 * s, by + 40 * s), fill=(111, 24, 24))
    d.text((pad + 9 * s, by + 1 * s), "EI", font=ImageFont.truetype(ital, 24 * s), fill=(255, 253, 248))
    d.text((pad + 62 * s, by - 2 * s), "Enforce", font=bf, fill=(255, 253, 248))
    d.text((pad + 62 * s + d.textlength("Enforce ", font=bf), by - 2 * s), "Interest", font=bi, fill=(201, 162, 79))
    uf = ImageFont.truetype(mono, 20 * s)
    u = "enforceinterest.com"
    d.text((W * s - pad - d.textlength(u, font=uf), by + 8 * s), u, font=uf, fill=(170, 150, 140))
    im = im.resize((W, H), Image.LANCZOS)
    im.save(jpg, quality=84, optimize=True, progressive=True)
    im.save(webp, quality=80, method=6)
    open(stamp, "w").write(key)
    return "gen/" + name


def make_brand_images():
    """Logo PNG for schema and the default share image."""
    from PIL import Image
    d = os.path.join(ROOT, "assets", "img")
    src = os.path.join(ROOT, "backup", "wordpress-2026-11-03", "media", "Enforce-Interest-Logo.webp")
    out = os.path.join(d, "enforce-interest-logo.png")
    if os.path.exists(src) and not os.path.exists(out):
        Image.open(src).save(out, optimize=True)
    make_card("og-default", "Texas Insurance Code §542.060",
              "Paid late? Texas law may owe you statutory interest.", motif="ring")
    shutil.copy(os.path.join(d, "gen", "og-default.jpg"), os.path.join(d, "og-default.jpg"))


def pic(name, alt, w=None, h=None, eager=False, cls=""):
    w0, h0 = IMG[name]
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    webp = f'<source type="image/webp" srcset="/assets/img/{name}.webp">' if os.path.exists(
        os.path.join(ROOT, "assets", "img", name + ".webp")) else ""
    return (f'<picture>{webp}<img src="/assets/img/{name}.jpg" alt="{esc(alt)}" width="{w or w0}" '
            f'height="{h or h0}" {load}{c}></picture>')


# ------------------------------------------------------------------ page shell
def render(p):
    url = SITE + p["path"]
    og = p.get("og") or "og-default"
    ow, oh = IMG[og]
    schemas = [lib.org_schema()] + p.get("schema", [])
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    robots = "noindex, follow" if p.get("noindex") else "index, follow, max-image-preview:large, max-snippet:-1"
    canon = "" if p.get("noindex") else f'<link rel="canonical" href="{url}">\n'
    art = ""
    if p.get("type") == "article":
        art = (f'<meta property="article:published_time" content="{p["published"]}T09:00:00-05:00">\n'
               f'<meta property="article:modified_time" content="{p.get("modified", p["published"])}T09:00:00-06:00">\n'
               f'<meta property="article:section" content="{esc(p.get("section", "Texas insurance law"))}">\n')
    extra_js = "".join(f'<script src="/assets/js/{j}?v={ASSET_V}" defer></script>\n' for j in p.get("js", []))
    return f'''<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(p["title"])}</title>
<meta name="description" content="{esc(p["desc"])}">
<meta name="robots" content="{robots}">
{canon}<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="{NAME}">
<meta property="og:type" content="{"article" if p.get("type") == "article" else "website"}">
<meta property="og:title" content="{esc(p.get("og_title", p["title"]))}">
<meta property="og:description" content="{esc(p["desc"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/{og}.jpg">
<meta property="og:image:width" content="{ow}">
<meta property="og:image:height" content="{oh}">
<meta property="og:image:alt" content="{esc(p.get("og_title", p["title"]))}">
{art}<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(p.get("og_title", p["title"]))}">
<meta name="twitter:description" content="{esc(p["desc"])}">
<meta name="twitter:image" content="{SITE}/assets/img/{og}.jpg">
<meta name="theme-color" content="#170d0c">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="alternate" type="application/rss+xml" title="{NAME} blog" href="{SITE}/feed/">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;1,9..144,500&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={ASSET_V}">
<script>document.documentElement.className+=" js"</script>
{ld}
</head>
<body class="{p.get("body_class", "")}">
{header(p["path"])}
<main id="main">
{p["body"]}
</main>
{footer()}
<script src="/assets/js/site.js?v={ASSET_V}" defer></script>
{extra_js}</body>
</html>
'''


# ------------------------------------------------------------------ outputs
def write(rel, text):
    path = os.path.join(PAGES, rel.strip("/"), "index.html") if not rel.endswith((".html", ".xml")) else os.path.join(PAGES, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def sitemap(all_pages):
    urls = []
    for p in all_pages:
        if p.get("noindex"):
            continue
        img = ""
        if p.get("og") and p["og"] != "og-default":
            img = (f'<image:image><image:loc>{SITE}/assets/img/{p["og"]}.jpg</image:loc></image:image>')
        urls.append(f'<url><loc>{SITE}{p["path"]}</loc><lastmod>{p.get("modified") or p.get("published") or BUILD_DATE}</lastmod>'
                    f'<changefreq>{p.get("freq", "monthly")}</changefreq><priority>{p.get("priority", "0.6")}</priority>{img}</url>')
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' + "\n".join(urls) + "\n</urlset>\n")


def feed(post_pages):
    items = []
    for p in sorted(post_pages, key=lambda x: x["published"], reverse=True):
        from email.utils import format_datetime
        from datetime import datetime, timezone
        dt = format_datetime(datetime.fromisoformat(p["published"] + "T09:00:00").replace(tzinfo=timezone.utc))
        items.append(f'<item><title>{xesc(p["h1_plain"])}</title><link>{SITE}{p["path"]}</link>'
                     f'<guid isPermaLink="true">{SITE}{p["path"]}</guid><pubDate>{dt}</pubDate>'
                     f'<description>{xesc(p["desc"])}</description></item>')
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>'
            f'<title>{NAME} blog</title><link>{SITE}/blog/</link><description>Texas prompt-payment interest, claim '
            f'deadlines and appraisal law for policyholders.</description><language>en-us</language>'
            f'<atom:link href="{SITE}/feed/" rel="self" type="application/rss+xml"/>{"".join(items)}</channel></rss>\n')


def llms(all_pages):
    lines = [f"# {NAME}", "",
             f"> {NAME} is a {FIRM} service (Texas public adjuster license #{LICENSE}) that documents late-paid Texas "
             "property insurance claims and calculates statutory interest under Texas Insurance Code §542.060: "
             f"18% a year for most claims, or the §304.003 judgment rate plus 5% (currently {lib.FLOAT_RATE_S}, "
             f"{lib.RATE_MONTH}) for weather claims made on or after September 1, 2017.", "",
             "Not a law firm; information is educational.", ""]
    groups = {"Guides": [], "Tools": [], "Blog": [], "Pages": []}
    for p in all_pages:
        if p.get("noindex") or p["path"] in ("/sitemap/",):
            continue
        g = "Tools" if p.get("is_tool") else "Blog" if p.get("type") == "article" else "Guides" if p.get("guide") else "Pages"
        groups[g].append(f"- [{p.get('h1_plain') or p['title']}]({SITE}{p['path']}): {p['desc']}")
    for g, items in groups.items():
        lines += [f"## {g}", ""] + items + [""]
    return "\n".join(lines)


def html_sitemap(all_pages):
    groups = {}
    for p in all_pages:
        if p.get("noindex") or p["path"] == "/sitemap/":
            continue
        g = "Free tools" if p.get("is_tool") else "Blog" if p.get("type") == "article" else "Guides &amp; claim types" if p.get("guide") else "Site"
        groups.setdefault(g, []).append(p)
    cols = "".join(f'<div class="card"><h3>{g}</h3><ul>' + "".join(
        f'<li><a href="{p["path"]}">{esc(p.get("h1_plain") or p["title"])}</a></li>' for p in ps) + '</ul></div>'
        for g, ps in groups.items())
    return cols


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(PAGES)
    make_brand_images()
    ctx = {"make_card": make_card, "pic": pic, "IMG": IMG, "scan": scan_images}
    # Content modules generate their cards first, then we scan sizes.
    post_pages = posts.build(ctx)
    tool_pages = tools.build(ctx)
    core_pages = pages.build(ctx, post_pages)
    home_page = home.build(ctx, post_pages)
    scan_images()
    for p in post_pages + tool_pages + core_pages + [home_page]:
        if callable(p["body"]):
            p["body"] = p["body"]()
    all_pages = [home_page] + core_pages + tool_pages + post_pages
    for p in all_pages:
        p["desc"] = seo.DESC.get(p["path"], p["desc"])
        p["title"] = seo.TITLES.get(p["path"], p["title"])
    smap = next(p for p in all_pages if p["path"] == "/sitemap/")
    smap["body"] = smap["body"].replace("<!--SITEMAP-->", html_sitemap(all_pages))
    seen = set()
    for p in all_pages:
        assert p["path"] not in seen, p["path"]
        seen.add(p["path"])
        write("" if p["path"] == "/" else p["path"], render(p))
    nf = pages.not_found()
    with open(os.path.join(PAGES, "404.html"), "w", encoding="utf-8") as f:
        f.write(render(nf))
    with open(os.path.join(PAGES, "feed.xml"), "w", encoding="utf-8") as f:
        f.write(feed(post_pages))
    # assets + root files
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"),
                    ignore=shutil.ignore_patterns("*.key"))
    with open(os.path.join(OUT, "assets", "js", "rates.js"), "w") as f:
        f.write(lib.rates_js())
    for fn in os.listdir(os.path.join(ROOT, "static")):
        src = os.path.join(ROOT, "static", fn)
        if os.path.isfile(src):
            shutil.copy(src, os.path.join(OUT, fn))
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write(sitemap(all_pages))
    with open(os.path.join(OUT, "llms.txt"), "w") as f:
        f.write(llms(all_pages))
    print(f"built {len(all_pages)} pages -> {os.path.relpath(OUT, ROOT)}/")


if __name__ == "__main__":
    main()
