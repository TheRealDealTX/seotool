#!/usr/bin/env python3
"""Static site generator for floridahomelaw.com (Florida Home Law).

Every page body lives in src/pages/*.html and begins with a one-line JSON
header inside an HTML comment, e.g.

    <!--{"path": "/property-insurance-mediation/", "title": "...", "description": "...",
          "crumb": "Mediation & Appraisal", "article": true}-->

build.py wraps each body in the shared layout and writes public/ (plus
sitemap.xml and robots.txt). Everything in src/static/ is copied verbatim.
FAQ blocks written as <details class="qa"><summary>Q</summary><div class="qa-a">A</div></details>
are turned into FAQPage structured data automatically.

    python3 build.py
"""

import hashlib
import html as htmllib
import json
import os
import re
import shutil
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "public")

# Live domain. True = noindex everything and block crawlers (test domains only).
STAGING = False

SITE = {
    "name": "Florida Home Law",
    "origin": "https://floridahomelaw.com",
    "tagline": "Plain-English Florida home law for homeowners protecting their homes through property insurance",
}

FIRM = {
    "name": "The Lawgical Firm",
    "legal_name": "The Lawgical Firm, P.A.",
    "site": "https://thelawgicalfirm.com/",
    "phone_display": "(407) 433-4131",
    "phone_href": "+14074334131",
    "street": "3191 Maguire Blvd, Ste 160",
    "city": "Orlando",
    "region": "FL",
    "zip": "32803",
    "offices": [
        {"label": "Destin office", "street": "34990 Emerald Coast Pkwy, Ste 359", "city": "Destin", "region": "FL", "zip": "32541"},
    ],
}

NAV = [
    ("Bill of Rights", "/homeowner-claims-bill-of-rights/"),
    ("Claim Process", "/homeowners-insurance-claim-process/"),
    ("2023 Law Changes", "/florida-insurance-law-changes-2023/"),
    ("Citizens", "/citizens-property-insurance-claim/"),
    ("Roof &amp; Hurricane", "/roof-and-hurricane-insurance-rules/"),
    ("Mediation", "/property-insurance-mediation/"),
    ("Lawyer Help", "/homeowner-insurance-lawyer/"),
]

TODAY = date.today().isoformat()
REVIEWED = "October 2026"


def ver(rel):
    with open(os.path.join(SRC, "static", rel), "rb") as fh:
        return hashlib.sha1(fh.read()).hexdigest()[:10]


def esc(text):
    return (str(text).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def strip_tags(s):
    return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


QA_RE = re.compile(r'<details class="qa"[^>]*>\s*<summary>(.*?)</summary>\s*<div class="qa-a">(.*?)</div>\s*</details>', re.S)


def schema_graph(page):
    origin = SITE["origin"]
    canonical = origin + page["path"]
    offices = [FIRM] + FIRM["offices"]
    graph = [
        {"@type": "WebSite", "@id": origin + "/#website", "url": origin + "/", "name": SITE["name"],
         "description": SITE["tagline"], "inLanguage": "en-US", "publisher": {"@id": origin + "/#firm"}},
        {"@type": "LegalService", "@id": origin + "/#firm", "name": FIRM["legal_name"], "url": FIRM["site"],
         "telephone": FIRM["phone_href"], "logo": origin + "/assets/img/lawgical-logo.png",
         "address": [{"@type": "PostalAddress", "streetAddress": o["street"], "addressLocality": o["city"],
                      "addressRegion": o["region"], "postalCode": o["zip"], "addressCountry": "US"} for o in offices],
         "areaServed": {"@type": "State", "name": "Florida"},
         "knowsAbout": ["Florida property insurance claims", "Homeowners insurance claim disputes",
                        "Hurricane and windstorm claims", "Roof damage claims", "Water damage claims"]},
        {"@type": "WebPage", "@id": canonical + "#webpage", "url": canonical, "name": page["title"],
         "description": page["description"], "isPartOf": {"@id": origin + "/#website"},
         "inLanguage": "en-US", "dateModified": page.get("modified", TODAY)},
    ]
    if page["path"] != "/" and not page["path"].endswith(".html"):
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": origin + "/"},
            {"@type": "ListItem", "position": 2, "name": page.get("crumb", page["title"].split(" | ")[0]), "item": canonical},
        ]})
    if page.get("article"):
        graph.append({"@type": "Article", "@id": canonical + "#article", "headline": page.get("h1", page["title"].split(" | ")[0]),
                      "description": page["description"], "mainEntityOfPage": {"@id": canonical + "#webpage"},
                      "author": {"@type": "Organization", "name": SITE["name"], "url": origin + "/"},
                      "publisher": {"@id": origin + "/#firm"},
                      "datePublished": page.get("published", "2026-10-15"), "dateModified": page.get("modified", TODAY),
                      "inLanguage": "en-US"})
    qas = QA_RE.findall(page["body"])
    if qas:
        graph.append({"@type": "FAQPage", "@id": canonical + "#faq", "mainEntity": [
            {"@type": "Question", "name": strip_tags(q), "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
            for q, a in qas]})
    return graph


def head(page):
    canonical = SITE["origin"] + page["path"]
    robots = "noindex, nofollow" if STAGING else page.get("robots", "index, follow, max-image-preview:large")
    ld = json.dumps({"@context": "https://schema.org", "@graph": schema_graph(page)}, ensure_ascii=False, indent=1)
    og_type = "article" if page.get("article") else "website"
    return f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(page['title'])}</title>
<meta name="description" content="{esc(page['description'])}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#1d5c4d">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:title" content="{esc(page['title'])}">
<meta property="og:description" content="{esc(page['description'])}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,500;0,600;0,700;1,500&amp;family=Source+Sans+3:wght@400;600;700&amp;display=swap">
<link rel="stylesheet" href="/assets/css/home-law.css?v={ver('assets/css/home-law.css')}">
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
"""


BRAND_SVG = ('<svg class="mark" viewBox="0 0 44 44" aria-hidden="true" focusable="false">'
             '<rect width="44" height="44" rx="12" fill="#1d5c4d"/>'
             '<path d="M10 23 22 13l12 10v11a1 1 0 0 1-1 1h-7v-7h-8v7h-7a1 1 0 0 1-1-1z" fill="#f6efe2"/>'
             '<path d="M31 8c-3 0-5 1.6-6 3.6 2-.9 4-.8 5.6.2-2.4.2-4.3 1.5-5 3.2 2.1-1 4.5-.7 6 .7V20h1.6v-4.3c1.5-1.4 3.9-1.7 6-.7-.7-1.7-2.6-3-5-3.2 1.6-1 3.6-1.1 5.6-.2-1-2-3-3.6-6-3.6z" fill="#ef7a5f"/>'
             '</svg>')


def header(active):
    links = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if href == active else ""}>{label}</a>' for label, href in NAV)
    return f"""<header class="masthead">
<div class="wrap masthead-row">
<a class="brand" href="/">{BRAND_SVG}<span><b>Florida Home Law</b><small>Homeowner insurance rights, explained</small></span></a>
<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" data-nav-toggle><span class="bars" aria-hidden="true"></span>Topics</button>
<nav id="site-nav" class="site-nav" aria-label="Main topics">{links}</nav>
<a class="phone-pill" href="tel:{FIRM['phone_href']}"><span>Free case review</span>{FIRM['phone_display']}</a>
</div>
</header>
<main id="main">
"""


def help_strip():
    return f"""<aside class="help-strip" aria-labelledby="help-strip-h">
<div class="wrap help-strip-row">
<div>
<p class="kicker">Claim denied, delayed or underpaid?</p>
<h2 id="help-strip-h">Ask a Florida property insurance attorney to look at it &mdash; free.</h2>
<p>{FIRM['legal_name']} reviews homeowners' policies, denial letters and estimates at no cost. No upfront fees: the firm does not get paid unless you get paid.</p>
</div>
<div class="help-strip-actions">
<a class="btn btn-coral" href="/free-case-review/">Request a free case review</a>
<a class="btn btn-line-light" href="tel:{FIRM['phone_href']}">Call {FIRM['phone_display']}</a>
</div>
</div>
</aside>
"""


def footer(show_help=True):
    offices = "".join(f"<p><b>{o['label']}</b><br>{o['street']}<br>{o['city']}, {o['region']} {o['zip']}</p>" for o in FIRM["offices"])
    return f"""</main>
{help_strip() if show_help else ""}<footer class="foot">
<div class="wrap foot-grid">
<div class="foot-col foot-about">
<p class="foot-brand">Florida Home Law</p>
<p>A plain-English library on Florida homeowner law as it applies to property insurance claims, sponsored by {FIRM['legal_name']}, a Florida property insurance claims law firm.</p>
<a href="/about-the-firm/"><img src="/assets/img/lawgical-logo-white.png" alt="{FIRM['name']}" width="150" height="56" loading="lazy"></a>
</div>
<div class="foot-col">
<p class="foot-h">Guides</p>
<a href="/homeowner-claims-bill-of-rights/">Homeowner Claims Bill of Rights</a>
<a href="/homeowners-insurance-claim-process/">Claim process &amp; deadlines</a>
<a href="/florida-insurance-law-changes-2023/">2022&ndash;2023 law changes</a>
<a href="/citizens-property-insurance-claim/">Citizens claims</a>
<a href="/roof-and-hurricane-insurance-rules/">Roof &amp; hurricane rules</a>
<a href="/property-insurance-mediation/">Mediation &amp; appraisal</a>
</div>
<div class="foot-col">
<p class="foot-h">Get help</p>
<a href="/free-case-review/">Free case review</a>
<a href="/homeowner-insurance-lawyer/">When to hire a lawyer</a>
<a href="/about-the-firm/">About the firm</a>
<a href="tel:{FIRM['phone_href']}">{FIRM['phone_display']}</a>
</div>
<div class="foot-col">
<p class="foot-h">Offices</p>
<p><b>Principal office</b><br>{FIRM['street']}<br>{FIRM['city']}, {FIRM['region']} {FIRM['zip']}</p>
{offices}
</div>
</div>
<div class="wrap foot-legal">
<p><strong>Attorney advertising.</strong> This website is sponsored by {FIRM['legal_name']}, which is responsible for its content. Principal office: Orlando, Florida; additional office in Destin, Florida. Phone {FIRM['phone_display']}.
The material on this site is general information only, not legal advice. Reading it or contacting us does not create an attorney-client relationship. Laws change and every policy is different, so deadlines and rights depend on your policy and your date of loss.
The hiring of a lawyer is an important decision that should not be based solely upon advertisements. See the <a href="/disclaimer/">full disclaimer</a>.</p>
<p class="foot-bottom"><span>&copy; {date.today().year} Florida Home Law &middot; {FIRM['legal_name']}</span>
<span><a href="/disclaimer/">Disclaimer</a> &middot; <a href="/privacy-policy/">Privacy policy</a> &middot; <a href="/sitemap/">Site map</a></span></p>
</div>
</footer>
<div class="dock" aria-label="Contact {FIRM['name']}">
<a class="dock-call" href="tel:{FIRM['phone_href']}">Call {FIRM['phone_display']}</a>
<a class="dock-form" href="/free-case-review/">Free review</a>
</div>
<script src="/assets/js/home-law.js?v={ver('assets/js/home-law.js')}" defer></script>
</body>
</html>
"""


CLAIM_TYPES = ["Hurricane or windstorm", "Roof damage or roof leak", "Water damage / plumbing leak", "Mold",
               "Fire or smoke", "Hail", "Sinkhole", "Theft or vandalism", "Other / not sure"]
STATUS = ["Denied", "Underpaid / low offer", "Delayed / no answer", "Not filed yet", "Other"]


def lead_form(n):
    opts = lambda xs: "".join(f"<option>{esc(x)}</option>" for x in xs)
    return f"""<form class="intake" data-intake novalidate>
<div class="intake-grid">
<p class="fld"><label for="f{n}-name">Full name</label><input id="f{n}-name" name="name" type="text" autocomplete="name" required></p>
<p class="fld"><label for="f{n}-phone">Phone</label><input id="f{n}-phone" name="phone" type="tel" autocomplete="tel" required></p>
<p class="fld"><label for="f{n}-email">Email</label><input id="f{n}-email" name="email" type="email" autocomplete="email" required></p>
<p class="fld"><label for="f{n}-loc">Property city or ZIP</label><input id="f{n}-loc" name="location" type="text" autocomplete="postal-code" required></p>
<p class="fld"><label for="f{n}-type">Type of claim</label><select id="f{n}-type" name="claim_type" required><option value="">Choose one&hellip;</option>{opts(CLAIM_TYPES)}</select></p>
<p class="fld"><label for="f{n}-status">Where things stand</label><select id="f{n}-status" name="status">{opts(STATUS)}</select></p>
<p class="fld wide"><label for="f{n}-msg">Briefly, what happened?</label><textarea id="f{n}-msg" name="message" rows="4" maxlength="3000" placeholder="Date of loss, insurer, and what the insurer has said or paid so far."></textarea></p>
<p class="hp" aria-hidden="true"><label for="f{n}-web">Leave blank</label><input id="f{n}-web" type="text" name="website" tabindex="-1" autocomplete="off"></p>
<p class="fld wide consent"><input id="f{n}-ok" type="checkbox" name="consent" value="1" required><label for="f{n}-ok">I understand that submitting this form does not create an attorney-client relationship, that I should not send confidential details until a lawyer agrees to represent me, and that {FIRM['legal_name']} may contact me by phone, text or email about my inquiry.</label></p>
</div>
<button class="btn btn-coral btn-wide" type="submit">Send for free review</button>
<p class="intake-note">Reviewed by {FIRM['legal_name']}. Prefer to talk? Call <a href="tel:{FIRM['phone_href']}">{FIRM['phone_display']}</a>.</p>
<div class="intake-out" data-intake-out role="status" aria-live="polite"></div>
</form>"""


def reviewed():
    return f'<p class="reviewed">Last reviewed: {REVIEWED}. General information about Florida law, not legal advice for your situation.</p>'


def expand(body):
    body = (body.replace("{{PHONE}}", FIRM["phone_display"]).replace("{{TEL}}", FIRM["phone_href"])
            .replace("{{FIRM}}", FIRM["name"]).replace("{{FIRM_LEGAL}}", FIRM["legal_name"])
            .replace("{{FIRM_SITE}}", FIRM["site"]).replace("{{REVIEWED}}", reviewed()))
    n = 0
    while "{{FORM}}" in body:
        n += 1
        body = body.replace("{{FORM}}", lead_form(n), 1)
    return body


HEADER_RE = re.compile(r"^\s*<!--(\{.*?\})-->\s*", re.S)


def load_pages():
    pages = []
    for name in sorted(os.listdir(os.path.join(SRC, "pages"))):
        if not name.endswith(".html"):
            continue
        raw = open(os.path.join(SRC, "pages", name), encoding="utf-8").read()
        m = HEADER_RE.match(raw)
        if not m:
            raise SystemExit(f"{name}: missing JSON header")
        meta = json.loads(m.group(1))
        meta["body"] = expand(raw[m.end():])
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", meta["body"], re.S)
        if h1:
            meta["h1"] = strip_tags(h1.group(1))
        pages.append(meta)
    return pages


def out_file(path):
    if path == "/":
        return os.path.join(OUT, "home.html")
    if path.endswith(".html"):
        return os.path.join(OUT, path.lstrip("/"))
    return os.path.join(OUT, path.strip("/"), "index.html")


def sitemap_list(pages):
    groups = {}
    for p in pages:
        if p.get("sitemap") is False:
            continue
        groups.setdefault(p.get("group", "Site information"), []).append(p)
    out = ""
    for g in ["Start here", "Guides", "Get help", "Site information"]:
        if g in groups:
            items = "".join(f'<li><a href="{p["path"]}">{esc(p.get("crumb", p["title"].split(" | ")[0]))}</a></li>' for p in groups[g])
            out += f'<section class="map-group"><h2>{g}</h2><ul>{items}</ul></section>'
    return out


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(SRC, "static"), OUT)
    pages = load_pages()
    for p in pages:
        p["body"] = p["body"].replace("{{SITEMAP}}", sitemap_list(pages))
        doc = head(p) + header(p.get("nav", p["path"])) + p["body"] + footer(p.get("help", True))
        f = out_file(p["path"])
        os.makedirs(os.path.dirname(f), exist_ok=True)
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(doc)
    urls = "".join(f"<url><loc>{SITE['origin']}{p['path']}</loc><lastmod>{p.get('modified', TODAY)}</lastmod></url>\n"
                   for p in pages if p.get("sitemap") is not False)
    with open(os.path.join(OUT, "sitemap.xml"), "w") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                 + urls + "</urlset>\n")
    with open(os.path.join(OUT, "robots.txt"), "w") as fh:
        if STAGING:
            fh.write("User-agent: *\nDisallow: /\n")
        else:
            fh.write(f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {SITE['origin']}/sitemap.xml\n")
    print(f"built {len(pages)} pages into public/ (staging={STAGING})")


if __name__ == "__main__":
    main()
