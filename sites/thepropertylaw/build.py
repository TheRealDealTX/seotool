#!/usr/bin/env python3
"""Build thepropertylaw.com into ./public (stdlib only).

Pages live in src/pages/*.html. Line one of each file is a JSON object in an
HTML comment that describes the page:

    <!--{"path": "/sinkhole-claim-florida/", "kind": "guide", "title": "...", "description": "...",
         "h1": "...", "lede": "...", "keyword": "sinkhole claim Florida", "crumb": "Sinkhole claims",
         "cites": ["627.706"], "related": ["/property-damage-claim/"]}-->

kind "guide" pages get a hero, breadcrumb, sticky table of contents (built from
each <h2 id>), Article + FAQPage schema (FAQs come from <details class="faq">
blocks) and a related-reading row. kind "page" bodies render as written.
Everything in src/static/ is copied verbatim (PHP front controller, .htaccess,
lead endpoint, CSS, JS, favicon).
"""

import hashlib
import html
import json
import os
import re
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "public")

STAGING = False          # True = noindex every page and disallow crawling
REVIEWED = "October 2026"
PUBLISHED = "2026-10-15"
MODIFIED = "2026-10-15"

SITE = {
    "name": "The Property Law",
    "origin": "https://thepropertylaw.com",
    "tagline": "A Florida property insurance law reference for homeowners and property owners",
}

FIRM = {
    "name": "The Lawgical Firm",
    "legal": "The Lawgical Firm, P.A.",
    "site": "https://thelawgicalfirm.com/",
    "phone": "(407) 433-4131",
    "tel": "+14074334131",
    "offices": [
        {"label": "Principal office", "street": "3191 Maguire Blvd, Ste 160", "city": "Orlando", "zip": "32803"},
        {"label": "Destin office", "street": "34990 Emerald Coast Pkwy, Ste 359", "city": "Destin", "zip": "32541"},
    ],
}

NAV = [
    ("Florida law", "/florida-property-insurance-law/"),
    ("Policy exclusions", "/insurance-policy-exclusions/"),
    ("Damage claims", "/property-damage-claim/"),
    ("Sinkhole", "/sinkhole-claim-florida/"),
    ("Fire", "/fire-damage-insurance-claim-florida/"),
    ("Commercial", "/commercial-property-insurance-claim/"),
    ("Lawyer", "/property-insurance-lawyer-florida/"),
]

CLAIM_TYPES = ["Hurricane or windstorm", "Roof damage or roof leak", "Water damage or plumbing leak", "Fire or smoke",
               "Sinkhole", "Mold", "Hail", "Theft or vandalism", "Other / not sure"]


def esc(s):
    return html.escape(str(s), quote=True)


def strip_tags(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def version(rel):
    with open(os.path.join(SRC, "static", rel), "rb") as fh:
        return hashlib.sha1(fh.read()).hexdigest()[:10]


# --------------------------------------------------------------------- schema
def schema(page, faqs):
    url = SITE["origin"] + page["path"]
    graph = [
        {"@type": "WebSite", "@id": SITE["origin"] + "/#site", "url": SITE["origin"] + "/", "name": SITE["name"],
         "description": SITE["tagline"], "inLanguage": "en-US", "publisher": {"@id": SITE["origin"] + "/#firm"}},
        {"@type": "LegalService", "@id": SITE["origin"] + "/#firm", "name": FIRM["legal"], "url": FIRM["site"],
         "telephone": FIRM["tel"], "logo": SITE["origin"] + "/assets/img/lawgical-logo.png",
         "address": [{"@type": "PostalAddress", "streetAddress": o["street"], "addressLocality": o["city"],
                      "addressRegion": "FL", "postalCode": o["zip"], "addressCountry": "US"} for o in FIRM["offices"]],
         "areaServed": {"@type": "State", "name": "Florida"},
         "knowsAbout": ["Florida property insurance law", "Property damage claims", "Sinkhole claims",
                        "Fire damage claims", "Commercial property insurance claims", "Insurance appraisal"]},
        {"@type": "WebPage", "@id": url + "#page", "url": url, "name": page["title"], "description": page["description"],
         "isPartOf": {"@id": SITE["origin"] + "/#site"}, "inLanguage": "en-US", "dateModified": MODIFIED},
    ]
    if page["path"] != "/" and not page["path"].endswith(".html"):
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE["origin"] + "/"},
            {"@type": "ListItem", "position": 2, "name": page.get("crumb", page["h1"] if "h1" in page else page["title"]), "item": url}]})
    if page.get("kind") == "guide":
        graph.append({"@type": "Article", "@id": url + "#article", "headline": page["h1"], "description": page["description"],
                      "datePublished": PUBLISHED, "dateModified": MODIFIED, "mainEntityOfPage": {"@id": url + "#page"},
                      "author": {"@id": SITE["origin"] + "/#firm"}, "publisher": {"@id": SITE["origin"] + "/#firm"},
                      "about": page.get("keyword"), "inLanguage": "en-US"})
    if faqs:
        graph.append({"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)


# --------------------------------------------------------------------- chrome
def head(page, faqs):
    url = SITE["origin"] + page["path"]
    robots = "noindex, nofollow" if STAGING else page.get("robots", "index, follow, max-snippet:-1")
    return f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(page['title'])}</title>
<meta name="description" content="{esc(page['description'])}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#fafafb">
<meta property="og:type" content="{'article' if page.get('kind') == 'guide' else 'website'}">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:title" content="{esc(page['title'])}">
<meta property="og:description" content="{esc(page['description'])}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={version('assets/css/site.css')}">
<script type="application/ld+json">
{schema(page, faqs)}
</script>
</head>
<body data-kind="{page.get('kind', 'page')}">
<a class="skip" href="#main">Skip to content</a>
"""


def header(active):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a>' for t, h in NAV)
    return f"""<header class="top">
<div class="wrap top-in">
<a class="mark" href="/"><span class="mark-sym" aria-hidden="true">&sect;</span><span>The Property Law<small>Florida property insurance reference</small></span></a>
<nav class="nav" aria-label="Guides">{links}</nav>
<div class="top-act">
<a class="top-phone" href="tel:{FIRM['tel']}">{FIRM['phone']}</a>
<a class="btn btn-primary" href="/free-case-review/">Free case review</a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="drawer" data-menu><span aria-hidden="true"></span>Menu</button>
</div>
</div>
<div class="drawer" id="drawer" hidden><div class="wrap"><nav aria-label="Guides (mobile)">
<a href="/">Property law index</a>{links}
<a class="btn btn-primary" href="/free-case-review/">Free case review</a>
<a class="btn btn-line" href="tel:{FIRM['tel']}">Call {FIRM['phone']}</a>
</nav></div></div>
</header>
<main id="main">
"""


def lead_form(n):
    opts = "".join(f"<option>{esc(c)}</option>" for c in CLAIM_TYPES)
    return f"""<form class="form" data-lead novalidate>
<div class="form-grid">
<div class="field"><label for="f{n}-name">Full name</label><input id="f{n}-name" name="name" autocomplete="name" required></div>
<div class="field"><label for="f{n}-phone">Phone</label><input id="f{n}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="field"><label for="f{n}-email">Email <span class="opt">(optional)</span></label><input id="f{n}-email" name="email" type="email" autocomplete="email"></div>
<div class="field"><label for="f{n}-loc">Property city or ZIP</label><input id="f{n}-loc" name="location" autocomplete="postal-code" required></div>
<div class="field"><label for="f{n}-type">Claim type</label><select id="f{n}-type" name="claim_type" required>{opts}</select></div>
<div class="field"><label for="f{n}-prop">Property</label><select id="f{n}-prop" name="property"><option>Home / residential</option><option>Condo or HOA</option><option>Commercial property</option></select></div>
<div class="field full"><label for="f{n}-desc">Briefly, what happened? <span class="opt">(optional)</span></label><textarea id="f{n}-desc" name="description" rows="3" maxlength="3000"></textarea></div>
<input class="hp" type="text" name="company_url" tabindex="-1" autocomplete="off" aria-hidden="true">
<label class="consent full"><input type="checkbox" name="consent" value="1" required><span>I understand that sending this form does not create an attorney-client relationship, that I should not send confidential details until a lawyer agrees to represent me, and that {esc(FIRM['legal'])} may contact me by phone, text or email about my request.</span></label>
</div>
<button class="btn btn-primary btn-block btn-lg" type="submit">Request my free case review</button>
<p class="form-note">No upfront fees. Prefer to talk? Call <a href="tel:{FIRM['tel']}">{FIRM['phone']}</a>.</p>
<div class="form-out" data-out role="status" aria-live="polite"></div>
</form>"""


def consult(n):
    return f"""<section class="consult" aria-labelledby="consult-h{n}">
<div class="wrap consult-in">
<div>
<span class="label label-accent">Free case review</span>
<h2 id="consult-h{n}">Questions about a denied, delayed or underpaid property claim?</h2>
<p class="muted">The attorneys at {FIRM['legal']} handle Florida residential and commercial property insurance claims. Tell us what happened and we will look at your policy and the insurer's decision.</p>
<ul class="consult-points">
<li><b>No upfront fees.</b> We don't get paid unless you do; costs are explained in the written fee agreement.</li>
<li><b>Florida-wide.</b> Offices in Orlando and Destin.</li>
<li><b>Bring what you have:</b> the policy, the claim number and any letters or estimates from the insurer.</li>
</ul>
</div>
{lead_form(n)}
</div>
</section>
"""


def footer():
    offices = "".join(f"<li><address><strong>{o['label']}</strong><br>{o['street']}<br>{o['city']}, FL {o['zip']}</address></li>" for o in FIRM["offices"])
    return f"""</main>
<footer class="foot">
<div class="wrap">
<div class="foot-grid">
<div>
<a class="mark" href="/"><span class="mark-sym" aria-hidden="true">&sect;</span><span>The Property Law</span></a>
<p style="margin-top:14px">A plain-language reference to Florida property insurance law, sponsored by {FIRM['legal']}</p>
<p><a href="tel:{FIRM['tel']}"><strong>{FIRM['phone']}</strong></a></p>
</div>
<div><h2>Guides</h2><ul>
<li><a href="/florida-property-insurance-law/">Florida property insurance law</a></li>
<li><a href="/insurance-policy-exclusions/">Policy exclusions explained</a></li>
<li><a href="/property-damage-claim/">Property damage claims</a></li>
<li><a href="/sinkhole-claim-florida/">Sinkhole claims</a></li>
<li><a href="/fire-damage-insurance-claim-florida/">Fire damage claims</a></li>
<li><a href="/commercial-property-insurance-claim/">Commercial property claims</a></li>
</ul></div>
<div><h2>The firm</h2><ul>
<li><a href="/property-insurance-lawyer-florida/">What a property insurance lawyer does</a></li>
<li><a href="/about-the-firm/">About {FIRM['name']}</a></li>
<li><a href="/free-case-review/">Free case review</a></li>
<li><a href="/disclaimer/">Disclaimer</a></li>
<li><a href="/privacy-policy/">Privacy policy</a></li>
<li><a href="/sitemap/">Sitemap</a></li>
</ul></div>
<div><h2>Offices</h2><ul>{offices}</ul></div>
</div>
<p class="foot-legal"><strong>Attorney advertising.</strong> This website is sponsored by {FIRM['legal']}, which is responsible for its content. Principal office: Orlando, Florida; additional office in Destin, Florida. Phone {FIRM['phone']}.
The material on this site is general information only, not legal advice, and it may not reflect the law that applies to your policy or date of loss. Reading this site or contacting us does not create an attorney-client relationship.
The hiring of a lawyer is an important decision that should not be based solely on advertisements. See our <a href="/disclaimer/">disclaimer</a>.</p>
<div class="foot-bottom"><span>&copy; 2026 {FIRM['legal']}</span><span>Legal information last reviewed {REVIEWED}</span></div>
</div>
</footer>
<div class="callbar"><a class="c1" href="tel:{FIRM['tel']}">Call {FIRM['phone']}</a><a class="c2" href="/free-case-review/">Free case review</a></div>
<script src="/assets/js/site.js?v={version('assets/js/site.js')}" defer></script>
</body>
</html>
"""


# --------------------------------------------------------------------- pages
HEADER_RE = re.compile(r"^\s*<!--(\{.*?\})-->\s*", re.S)
FAQ_RE = re.compile(r'<details class="faq"><summary>(.*?)</summary>(.*?)</details>', re.S)
H2_RE = re.compile(r'<h2 id="([\w-]+)">(.*?)</h2>', re.S)


def expand(body, counter):
    for k, v in {"{{PHONE}}": FIRM["phone"], "{{TEL}}": FIRM["tel"], "{{FIRM}}": FIRM["name"],
                 "{{FIRM_LEGAL}}": FIRM["legal"], "{{FIRM_SITE}}": FIRM["site"], "{{REVIEWED}}": REVIEWED}.items():
        body = body.replace(k, v)
    while "{{FORM}}" in body:
        counter[0] += 1
        body = body.replace("{{FORM}}", lead_form(counter[0]), 1)
    return body


def load():
    pages = []
    for name in sorted(os.listdir(os.path.join(SRC, "pages"))):
        if name.endswith(".html"):
            raw = open(os.path.join(SRC, "pages", name), encoding="utf-8").read()
            m = HEADER_RE.match(raw)
            if not m:
                raise SystemExit(f"{name}: missing JSON header")
            meta = json.loads(m.group(1))
            meta["raw"] = raw[m.end():]
            pages.append(meta)
    return pages


def guide(page, body, by_path, n):
    toc = "".join(f'<li><a href="#{i}">{strip_tags(t)}</a></li>' for i, t in H2_RE.findall(body))
    cites = "".join(f'<span class="cite">&sect; {esc(c)}</span>' for c in page.get("cites", []))
    words = len(strip_tags(body).split())
    related = ""
    if page.get("related"):
        cards = "".join(f'<a href="{p}"><strong>{esc(by_path[p].get("crumb", by_path[p]["title"]))}</strong><span>{esc(by_path[p]["description"][:120].rsplit(" ", 1)[0])}&hellip;</span></a>'
                        for p in page["related"])
        related = f'<section class="related"><div class="wrap"><span class="label">Related reading</span><div class="related-grid" style="margin-top:14px">{cards}</div></div></section>'
    return f"""<section class="doc-hero gridbg"><div class="wrap doc-hero-in">
<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="/">Property law index</a></li><li aria-current="page">{esc(page['crumb'])}</li></ol></nav>
<span class="label label-accent">{esc(page.get('eyebrow', 'Guide'))}</span>
<h1>{page['h1']}</h1>
<p class="doc-lede">{page['lede']}</p>
<div class="doc-meta"><span>Last reviewed: {REVIEWED}</span><span>{max(1, round(words / 230))} min read</span><span>Statutes: {cites}</span></div>
</div></section>
<div class="wrap doc">
<aside class="toc" data-toc><div class="toc-inner"><div class="toc-box"><details><summary>On this page</summary><ol>{toc}</ol></details></div>
<div class="toc-cta"><strong>Talk it through</strong>Free case review with {FIRM['legal']}. No upfront fees.<a class="btn btn-primary" href="/free-case-review/">Start a review</a><a class="btn btn-line" style="margin-top:8px;width:100%" href="tel:{FIRM['tel']}">{FIRM['phone']}</a></div></div></aside>
<article class="prose">
{body}
<p class="reviewed">Last reviewed: {REVIEWED}. Statutes cited are from the 2026 Florida Statutes. Deadlines and rules depend on your policy language, when the policy was issued and your date of loss; this page is general information, not legal advice.</p>
</article>
</div>
{related}
{consult(n)}"""


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(SRC, "static"), OUT)
    pages = load()
    by_path = {p["path"]: p for p in pages}
    counter = [0]
    for p in pages:
        body = expand(p["raw"], counter)
        if "{{SITEMAP}}" in body:
            items = "".join(f'<li><a href="{q["path"]}">{esc(q.get("crumb", q["title"]))}</a><span>{esc(q["description"])}</span></li>'
                            for q in pages if q.get("sitemap", True))
            body = body.replace("{{SITEMAP}}", f'<ul class="sitemap-list">{items}</ul>')
        faqs = [(strip_tags(q), strip_tags(a)) for q, a in FAQ_RE.findall(body)]
        if p.get("kind") == "guide":
            counter[0] += 1
            main_html = guide(p, body, by_path, counter[0])
        else:
            if "{{CONSULT}}" in body:
                counter[0] += 1
                body = body.replace("{{CONSULT}}", consult(counter[0]))
            main_html = body
        doc = head(p, faqs) + header(p.get("nav", p["path"])) + main_html + footer()
        out = os.path.join(OUT, "home.html") if p["path"] == "/" else (
            os.path.join(OUT, p["path"].lstrip("/")) if p["path"].endswith(".html") else os.path.join(OUT, p["path"].strip("/"), "index.html"))
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(doc)
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for p in pages:
            if p.get("sitemap", True):
                fh.write(f"<url><loc>{SITE['origin']}{p['path']}</loc><lastmod>{MODIFIED}</lastmod></url>\n")
        fh.write("</urlset>\n")
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write("User-agent: *\nDisallow: /\n" if STAGING else
                 f"User-agent: *\nAllow: /\n\nSitemap: {SITE['origin']}/sitemap.xml\n")
    print(f"built {len(pages)} pages -> public/ (staging={STAGING})")


if __name__ == "__main__":
    main()
