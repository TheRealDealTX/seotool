#!/usr/bin/env python3
"""Builds claimroofleak.com into ./public (stdlib only).

Every file in src/pages/ is an HTML body whose first line is a JSON comment:

    <!--{"path": "/x/", "title": "...", "description": "...", "crumb": "...", "kind": "guide"}-->

kind "guide" pages get an "On this page" list built from their <h2 id> headings,
Article schema and a "Last reviewed" line. Any <details class="qa"> blocks on a
page become FAQPage schema automatically. src/static/ is copied as-is.

    python3 build.py
"""

import hashlib
import html
import json
import os
import re
import shutil
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")
OUT = os.path.join(HERE, "public")

STAGING = False                       # True = noindex everything + block robots
ORIGIN = "https://claimroofleak.com"
SITE_NAME = "Claim Roof Leak"
REVIEWED = "October 2026"
TODAY = date.today().isoformat()

FIRM = {
    "name": "The Lawgical Firm",
    "legal": "The Lawgical Firm, P.A.",
    "site": "https://thelawgicalfirm.com/",
    "roof_page": "https://thelawgicalfirm.com/residential-property-insurance-claims/roof-leak-insurance-claims-in-orlando-fl/",
    "phone": "(407) 433-4131",
    "tel": "+14074334131",
    "offices": [
        {"label": "Principal office", "street": "3191 Maguire Blvd, Ste 160", "city": "Orlando", "zip": "32803"},
        {"label": "Destin office", "street": "34990 Emerald Coast Pkwy, Ste 359", "city": "Destin", "zip": "32541"},
    ],
}

MENU = [
    ("Is it covered?", "/is-a-roof-leak-covered-by-homeowners-insurance-florida/"),
    ("Filing in Florida", "/roof-leak-insurance-claim-florida/"),
    ("Claim denied", "/roof-leak-claim-denied/"),
    ("25% roof rule", "/florida-25-percent-roof-rule/"),
    ("About the firm", "/about-the-firm/"),
]

CLAIM_TYPES = ["Claim denied", "Claim underpaid / low offer", "Claim delayed or no answer",
               "Haven't filed yet", "Water damage or mold from a roof leak", "Something else"]


def esc(s):
    return html.escape(str(s), quote=True)


def ver(rel):
    with open(os.path.join(SRC, "static", rel), "rb") as fh:
        return hashlib.sha1(fh.read()).hexdigest()[:8]


def strip_tags(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


# ---------------------------------------------------------------- schema
def schema(page):
    url = ORIGIN + page["path"]
    graph = [
        {"@type": "WebSite", "@id": ORIGIN + "/#site", "url": ORIGIN + "/", "name": SITE_NAME,
         "inLanguage": "en-US", "publisher": {"@id": ORIGIN + "/#lawfirm"}},
        {"@type": "LegalService", "@id": ORIGIN + "/#lawfirm", "name": FIRM["legal"], "url": FIRM["site"],
         "telephone": FIRM["tel"], "areaServed": {"@type": "State", "name": "Florida"},
         "address": [{"@type": "PostalAddress", "streetAddress": o["street"], "addressLocality": o["city"],
                      "addressRegion": "FL", "postalCode": o["zip"], "addressCountry": "US"} for o in FIRM["offices"]],
         "knowsAbout": ["Roof leak insurance claims", "Roof damage insurance claims", "Denied property insurance claims",
                        "Water damage claims", "Mold claims"]},
        {"@type": "WebPage", "@id": url + "#page", "url": url, "name": page["title"],
         "description": page["description"], "isPartOf": {"@id": ORIGIN + "/#site"},
         "inLanguage": "en-US", "dateModified": TODAY},
    ]
    if page["path"] != "/":
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": ORIGIN + "/"},
            {"@type": "ListItem", "position": 2, "name": page.get("crumb", page["title"]), "item": url}]})
    if page.get("kind") == "guide":
        graph.append({"@type": "Article", "headline": page["h1"], "description": page["description"],
                      "mainEntityOfPage": {"@id": url + "#page"}, "dateModified": TODAY,
                      "datePublished": page.get("published", "2026-10-15"),
                      "author": {"@id": ORIGIN + "/#lawfirm"}, "publisher": {"@id": ORIGIN + "/#lawfirm"}})
    qas = re.findall(r'<details class="qa"[^>]*>\s*<summary>(.*?)</summary>(.*?)</details>', page["body"], re.S)
    if qas:
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": strip_tags(q),
             "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in qas]})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)


# ---------------------------------------------------------------- layout
def head(page):
    url = ORIGIN + page["path"]
    robots = "noindex, nofollow" if (STAGING or page.get("noindex")) else "index, follow"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(page['title'])}</title>
<meta name="description" content="{esc(page['description'])}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#a5482a">
<meta property="og:type" content="{'article' if page.get('kind') == 'guide' else 'website'}">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{esc(page['title'])}">
<meta property="og:description" content="{esc(page['description'])}">
<meta property="og:url" content="{url}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&amp;family=Plus+Jakarta+Sans:wght@400;500;600;700&amp;display=swap">
<link rel="stylesheet" href="/assets/roof.css?v={ver('assets/roof.css')}">
<script type="application/ld+json">{schema(page)}</script>
</head>
<body class="{page.get('kind', 'page')}">
<a class="skip" href="#main">Skip to main content</a>
"""


LOGO = ('<svg class="mark" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="11" fill="#a5482a"/>'
        '<path d="M6 21 20 9l14 12" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M11 19v12h18V19" fill="none" stroke="#fde9dc" stroke-width="2.6" stroke-linejoin="round"/>'
        '<path d="M20 20c-2.2 3-3.3 4.8-3.3 6.2a3.3 3.3 0 0 0 6.6 0c0-1.4-1.1-3.2-3.3-6.2z" fill="#7cc4ee"/></svg>')


def topbar(active):
    links = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a></li>' for t, h in MENU)
    return f"""<header class="top">
<div class="wrap top-row">
<a class="logo" href="/">{LOGO}<span><b>Claim Roof Leak</b><small>Florida roof claim guide</small></span></a>
<nav class="menu" id="menu" aria-label="Main menu"><ul>{links}</ul>
<a class="menu-cta" href="/free-case-review/">Free case review</a></nav>
<a class="top-call" href="tel:{FIRM['tel']}"><span>Talk to a lawyer</span>{FIRM['phone']}</a>
<button class="burger" type="button" aria-controls="menu" aria-expanded="false" data-burger><span class="sr">Open menu</span><i></i><i></i><i></i></button>
</div>
</header>
"""


def crumbs(page):
    if page["path"] == "/":
        return ""
    return (f'<nav class="crumbs wrap" aria-label="Breadcrumb"><a href="/">Home</a>'
            f'<span aria-hidden="true">&rsaquo;</span><span aria-current="page">{esc(page.get("crumb", ""))}</span></nav>\n')


def toc_and_ids(body):
    """Give every <h2> inside the article an id and return (body, toc html)."""
    items = []

    def fix(m):
        attrs, text = m.group(1), m.group(2)
        idm = re.search(r'id="([^"]+)"', attrs)
        hid = idm.group(1) if idm else re.sub(r"[^a-z0-9]+", "-", strip_tags(text).lower()).strip("-")[:60]
        items.append((hid, strip_tags(text)))
        return f'<h2{attrs if idm else attrs + f" id=\"{hid}\""}>{text}</h2>'

    body = re.sub(r"<h2([^>]*)>(.*?)</h2>", fix, body, flags=re.S)
    toc = "".join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in items)
    return body, toc


def guide_shell(page, body):
    body, toc = toc_and_ids(body)
    head_html = page.get("lede", "")
    return f"""<div class="guide-hero"><div class="wrap">
<p class="kicker">{esc(page.get('kicker', 'Florida roof claim guide'))}</p>
<h1>{page['h1']}</h1>
{head_html}
<p class="reviewed">Last reviewed: {REVIEWED} &middot; General Florida information, not legal advice. Deadlines depend on your policy and date of loss.</p>
</div><svg class="eave" viewBox="0 0 1200 40" preserveAspectRatio="none" aria-hidden="true"><path d="M0 40V22l40-12 40 12 40-12 40 12 40-12 40 12 40-12 40 12 40-12 40 12 40-12 40 12 40-12 40 12 40-12 40 12 40-12 40 12 40-12 40 12 40-12 40 12 40-12 40 12 40-12 40 12 40-12 40 12 40-12 40 12 40-12 40 12 40-12 40 12V40z"/></svg></div>
<div class="wrap guide-grid">
<aside class="side">
<details class="toc" open><summary>On this page</summary><ol>{toc}</ol></details>
<div class="side-card"><p class="side-title">Roof leak claim problem?</p>
<p>Free review of your denial letter or estimate. No upfront fees.</p>
<a class="btn btn-clay" href="/free-case-review/">Start a free review</a>
<a class="side-tel" href="tel:{FIRM['tel']}">or call {FIRM['phone']}</a></div>
</aside>
<article class="prose">
{body}
</article>
</div>
"""


def help_strip():
    return f"""<section class="help-strip">
<div class="wrap help-inner">
<svg class="help-roof" viewBox="0 0 120 70" aria-hidden="true"><path d="M8 40 60 8l52 32" fill="none" stroke="currentColor" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/><path d="M24 36v28h72V36" fill="none" stroke="currentColor" stroke-width="5" opacity=".5"/></svg>
<div>
<h2>Insurer said no &mdash; or not enough?</h2>
<p>{FIRM['name']} reviews Florida roof leak, roof damage and water damage claims at no cost. We don&rsquo;t get paid unless you get paid, and there are no upfront fees.</p>
</div>
<div class="help-actions">
<a class="btn btn-sky" href="/free-case-review/">Get a free case review</a>
<a class="btn btn-line" href="tel:{FIRM['tel']}">Call {FIRM['phone']}</a>
</div>
</div>
</section>
"""


def bottom(page):
    offices = "".join(f'<li><b>{o["label"]}</b><br>{o["street"]}<br>{o["city"]}, FL {o["zip"]}</li>' for o in FIRM["offices"])
    return f"""</main>
{help_strip() if page.get('strip', True) else ''}<footer class="foot">
<div class="wrap foot-grid">
<div class="foot-brand">
<a class="logo logo-foot" href="/">{LOGO}<span><b>Claim Roof Leak</b><small>Florida roof claim guide</small></span></a>
<p>Plain-language information for Florida homeowners dealing with a leaking roof, from the first drip to a denial letter. Sponsored by {FIRM['legal']}.</p>
<img src="/assets/img/lawgical-logo-white.png" alt="{FIRM['name']}" width="150" height="56" loading="lazy">
</div>
<div><p class="foot-h">Guides</p><ul class="foot-links">
<li><a href="/is-a-roof-leak-covered-by-homeowners-insurance-florida/">Is a roof leak covered?</a></li>
<li><a href="/roof-leak-insurance-claim-florida/">Filing in Florida, step by step</a></li>
<li><a href="/roof-damage-insurance-claim-florida/">Roof damage insurance claims</a></li>
<li><a href="/wear-and-tear-roof-denial/">Wear and tear roof denials</a></li>
<li><a href="/florida-25-percent-roof-rule/">Florida 25% roof rule</a></li>
<li><a href="/roof-leak-water-damage-mold-claim/">Water damage &amp; mold</a></li>
<li><a href="/roof-leak-claim-denied/">When the claim is denied</a></li>
</ul></div>
<div><p class="foot-h">The firm</p><ul class="foot-links foot-offices">
<li><a href="tel:{FIRM['tel']}">{FIRM['phone']}</a></li>{offices}
<li><a href="/free-case-review/">Free case review</a> &middot; <a href="/about-the-firm/">About</a></li>
</ul></div>
</div>
<div class="wrap legal">
<p><strong>Attorney advertising.</strong> This website is sponsored by {FIRM['legal']}, which is responsible for its content. Principal office: Orlando, Florida; additional office in Destin, Florida. Phone {FIRM['phone']}. The information here is general information only, not legal advice, and reading it or contacting us does not create an attorney-client relationship. The hiring of a lawyer is an important decision that should not be based solely upon advertisements. See the full <a href="/disclaimer/">disclaimer</a>.</p>
<p class="legal-row"><span>&copy; {date.today().year} {FIRM['legal']}</span><span><a href="/disclaimer/">Disclaimer</a> &middot; <a href="/privacy-policy/">Privacy policy</a> &middot; <a href="/sitemap/">Sitemap</a></span></p>
</div>
</footer>
<div class="dock"><a class="dock-call" href="tel:{FIRM['tel']}">Call {FIRM['phone']}</a><a class="dock-form" href="/free-case-review/">Free review</a></div>
<script src="/assets/roof.js?v={ver('assets/roof.js')}" defer></script>
</body>
</html>
"""


def lead_form(n):
    opts = "".join(f"<option>{esc(c)}</option>" for c in CLAIM_TYPES)
    p = f"f{n}"
    return f"""<form class="intake" data-intake novalidate>
<div class="intake-grid">
<p class="fld"><label for="{p}n">Your name</label><input id="{p}n" name="name" autocomplete="name" required></p>
<p class="fld"><label for="{p}p">Phone</label><input id="{p}p" name="phone" type="tel" autocomplete="tel" required></p>
<p class="fld"><label for="{p}e">Email</label><input id="{p}e" name="email" type="email" autocomplete="email" required></p>
<p class="fld"><label for="{p}c">Property city or ZIP</label><input id="{p}c" name="location" autocomplete="postal-code" required></p>
<p class="fld wide"><label for="{p}t">Claim type</label><select id="{p}t" name="claim_type" required><option value="">Choose one&hellip;</option>{opts}</select></p>
<p class="fld wide"><label for="{p}d">What happened? <span class="opt">(a few sentences)</span></label><textarea id="{p}d" name="message" rows="4" maxlength="3000" placeholder="When the leak started, what the insurer said, and any dates you know."></textarea></p>
<p class="hp" aria-hidden="true"><label for="{p}w">Leave blank</label><input id="{p}w" name="website" tabindex="-1" autocomplete="off"></p>
<p class="consent wide"><input id="{p}k" name="consent" type="checkbox" value="1" required><label for="{p}k">I agree that {FIRM['legal']} may contact me about my claim by phone, text or email. I understand that submitting this form does not create an attorney-client relationship and that I should not send confidential information until I have spoken with the firm.</label></p>
</div>
<button class="btn btn-clay btn-full" type="submit">Request my free case review</button>
<p class="intake-note">Free and confidential review &middot; No upfront fees &middot; Prefer the phone? <a href="tel:{FIRM['tel']}">{FIRM['phone']}</a></p>
<p class="intake-out" data-out role="status" aria-live="polite"></p>
</form>"""


def fill(body):
    for k, v in {"{{PHONE}}": FIRM["phone"], "{{TEL}}": FIRM["tel"], "{{FIRM}}": FIRM["name"],
                 "{{LEGAL}}": FIRM["legal"], "{{FIRM_SITE}}": FIRM["site"], "{{FIRM_ROOF}}": FIRM["roof_page"],
                 "{{REVIEWED}}": REVIEWED}.items():
        body = body.replace(k, v)
    n = 0
    while "{{FORM}}" in body:
        n += 1
        body = body.replace("{{FORM}}", lead_form(n), 1)
    return body


HDR = re.compile(r"^\s*<!--(\{.*?\})-->\s*", re.S)


def load():
    pages = []
    for fn in sorted(os.listdir(os.path.join(SRC, "pages"))):
        if fn.endswith(".html"):
            raw = open(os.path.join(SRC, "pages", fn), encoding="utf-8").read()
            m = HDR.match(raw)
            if not m:
                raise SystemExit(f"{fn}: missing JSON header")
            meta = json.loads(m.group(1))
            meta["body"] = fill(raw[m.end():])
            for k in ("lede",):
                if k in meta:
                    meta[k] = fill(meta[k])
            pages.append(meta)
    return pages


def target(path):
    if path == "/":
        return os.path.join(OUT, "home.html")
    if path.endswith(".html"):
        return os.path.join(OUT, path.lstrip("/"))
    return os.path.join(OUT, path.strip("/"), "index.html")


def sitemap_list(pages):
    groups = {}
    for p in pages:
        if p.get("in_sitemap", True):
            groups.setdefault(p.get("group", "Site"), []).append(p)
    out = ""
    for g in ("Guides", "Help", "Site"):
        if g in groups:
            li = "".join(f'<li><a href="{p["path"]}">{esc(p.get("crumb") or "Home")}</a> &ndash; {esc(p["description"][:110].rsplit(" ", 1)[0])}&hellip;</li>' for p in groups[g])
            out += f'<h2>{g}</h2><ul class="map-list">{li}</ul>'
    return out


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(SRC, "static"), OUT)
    pages = load()
    for p in pages:
        body = p["body"].replace("{{SITEMAP}}", sitemap_list(pages))
        main_html = guide_shell(p, body) if p.get("kind") == "guide" else body
        doc = head(p) + topbar(p.get("nav", p["path"])) + '<main id="main">\n' + crumbs(p) + main_html + bottom(p)
        f = target(p["path"])
        os.makedirs(os.path.dirname(f), exist_ok=True)
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(doc)
    listed = [p for p in pages if p.get("in_sitemap", True)]
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for p in listed:
            fh.write(f"  <url><loc>{ORIGIN}{p['path']}</loc><lastmod>{TODAY}</lastmod></url>\n")
        fh.write("</urlset>\n")
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write("User-agent: *\nDisallow: /\n" if STAGING else f"User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n")
    print(f"built {len(pages)} pages -> public/ (staging={STAGING})")


if __name__ == "__main__":
    main()
