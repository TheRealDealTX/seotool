#!/usr/bin/env python3
"""Static site generator for deniedfloodclaim.com (stdlib only).

Every page body lives in src/pages/*.html and begins with a one-line JSON
header inside an HTML comment, for example:

    <!--{"path": "/nfip-claim-denied/", "title": "...", "description": "...",
         "crumb": "NFIP Claim Denied", "article": true, "group": "Guides"}-->

The body is wrapped in the shared shell below and written to public/.
Everything under src/static/ (CSS, JS, PHP, favicon, .htaccess) is copied as is.
FAQ blocks written as <details class="faq-item"><summary>Q</summary><div>A</div></details>
are turned into FAQPage structured data automatically.

    python3 build.py
"""

import hashlib
import html
import json
import os
import re
import shutil
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "public")

# Production: pages are indexable. Set True on a temporary/test domain.
STAGING = False

SITE = {
    "name": "DeniedFloodClaim.com",
    "origin": "https://deniedfloodclaim.com",
    "tagline": "Florida flood insurance claim information: NFIP denials, FEMA appeals, proof of loss and wind-vs-water disputes",
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
    ("NFIP Denials", "/nfip-claim-denied/"),
    ("FEMA Appeal", "/flood-insurance-appeal-fema/"),
    ("Deadlines", "/flood-proof-of-loss-deadline/"),
    ("Wind vs. Flood", "/wind-vs-flood-damage-claim/"),
    ("Private Flood", "/private-flood-insurance-claim-denied-florida/"),
    ("Underpaid", "/flood-claim-underpaid/"),
]

TODAY = date.today().isoformat()
REVIEWED = "October 2026"


def esc(text):
    return html.escape(str(text), quote=True)


def asset_version(rel):
    with open(os.path.join(SRC, "static", rel), "rb") as fh:
        return hashlib.sha1(fh.read()).hexdigest()[:10]


def strip_tags(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


FAQ_RE = re.compile(r'<details class="faq-item"[^>]*>\s*<summary>(.*?)</summary>\s*<div[^>]*>(.*?)</div>\s*</details>', re.S)


def schema_graph(page):
    canonical = SITE["origin"] + page["path"]
    firm_addresses = [{"@type": "PostalAddress", "streetAddress": o["street"], "addressLocality": o["city"],
                       "addressRegion": o["region"], "postalCode": o["zip"], "addressCountry": "US"}
                      for o in [FIRM] + FIRM["offices"]]
    graph = [
        {"@type": "WebSite", "@id": SITE["origin"] + "/#website", "url": SITE["origin"] + "/",
         "name": SITE["name"], "description": SITE["tagline"], "inLanguage": "en-US",
         "publisher": {"@id": SITE["origin"] + "/#firm"}},
        {"@type": "LegalService", "@id": SITE["origin"] + "/#firm", "name": FIRM["legal_name"],
         "url": FIRM["site"], "telephone": FIRM["phone_href"], "address": firm_addresses,
         "logo": SITE["origin"] + "/assets/img/lawgical-logo.png",
         "areaServed": {"@type": "State", "name": "Florida"},
         "knowsAbout": ["Florida property insurance claims", "Hurricane and windstorm insurance claims",
                        "Water damage insurance claims", "Denied and underpaid property insurance claims"]},
        {"@type": "WebPage", "@id": canonical + "#webpage", "url": canonical, "name": page["title"],
         "description": page["description"], "isPartOf": {"@id": SITE["origin"] + "/#website"},
         "inLanguage": "en-US", "dateModified": page.get("modified", TODAY)},
    ]
    if page["path"] != "/" and not page["path"].endswith(".html"):
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE["origin"] + "/"},
            {"@type": "ListItem", "position": 2, "name": page.get("crumb", page["title"].split(" | ")[0]), "item": canonical},
        ]})
    if page.get("article"):
        graph.append({"@type": "Article", "@id": canonical + "#article", "headline": page["h1"],
                      "description": page["description"], "mainEntityOfPage": {"@id": canonical + "#webpage"},
                      "datePublished": page.get("published", "2026-10-15"), "dateModified": page.get("modified", TODAY),
                      "author": {"@id": SITE["origin"] + "/#firm"}, "publisher": {"@id": SITE["origin"] + "/#firm"},
                      "inLanguage": "en-US"})
    faqs = FAQ_RE.findall(page["body"])
    if faqs:
        graph.append({"@type": "FAQPage", "@id": canonical + "#faq", "mainEntity": [
            {"@type": "Question", "name": strip_tags(q), "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
            for q, a in faqs]})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)


def head(page):
    canonical = SITE["origin"] + page["path"]
    robots = "noindex, nofollow" if STAGING else page.get("robots", "index, follow, max-image-preview:large")
    return f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(page['title'])}</title>
<meta name="description" content="{esc(page['description'])}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#0b2a35">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="{'article' if page.get('article') else 'website'}">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:title" content="{esc(page['title'])}">
<meta property="og:description" content="{esc(page['description'])}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700;800&amp;family=Public+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&amp;display=swap">
<link rel="stylesheet" href="/assets/css/flood.css?v={asset_version('assets/css/flood.css')}">
<script type="application/ld+json">
{schema_graph(page)}
</script>
</head>
<body class="{page.get('body_class', 'pg')}">
<a class="skip" href="#main">Skip to main content</a>
"""


def masthead(active):
    links = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{l}</a></li>' for l, h in NAV)
    return f"""<header class="mast">
<div class="wrap mast-row">
<a class="logo" href="/" aria-label="{SITE['name']} home">
<svg viewBox="0 0 40 40" width="34" height="34" aria-hidden="true"><rect width="40" height="40" rx="10" fill="#0e4f5c"/><path d="M20 7c5 7 9 11.5 9 16.5A9 9 0 0 1 11 23.5C11 18.5 15 14 20 7z" fill="#35e0d0"/><path d="M8 30c3-2 6-2 9 0s6 2 9 0 6-2 9 0" stroke="#f5a524" stroke-width="2.4" fill="none" stroke-linecap="round"/></svg>
<span class="logo-txt">DeniedFloodClaim<span>.com</span></span>
</a>
<nav class="topnav" id="topnav" aria-label="Main">
<ul>{links}</ul>
<a class="tn-review" href="/free-case-review/">Free case review</a>
</nav>
<div class="mast-act">
<a class="mast-tel" href="tel:{FIRM['phone_href']}"><svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z" fill="currentColor"/></svg>{FIRM['phone_display']}</a>
<button class="burger" type="button" aria-expanded="false" aria-controls="topnav" data-burger><span class="sr">Menu</span><i></i><i></i><i></i></button>
</div>
</div>
</header>
<main id="main">
"""


def crumbs(page):
    if page["path"] == "/" or page["path"].endswith(".html"):
        return ""
    name = page.get("crumb", page["title"].split(" | ")[0])
    return f'<nav class="crumbs wrap" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li><li aria-current="page">{esc(name)}</li></ol></nav>\n'


def review_band():
    return f"""<section class="band" aria-labelledby="band-h">
<svg class="band-wave" viewBox="0 0 1200 120" preserveAspectRatio="none" aria-hidden="true"><path d="M0 70 C200 20 400 120 600 70 S1000 20 1200 70 V120 H0z" fill="currentColor"/></svg>
<div class="wrap band-in">
<div>
<p class="kicker kicker-amber">Clock running on a flood or storm claim?</p>
<h2 id="band-h">Get a free review of the denial letter and your policy</h2>
<p>Send the letter, the estimate and the policy declarations. The attorneys at {FIRM['legal_name']} will tell you, at no cost, which deadlines apply and whether the claim is one the firm can take on. No upfront fees.</p>
</div>
<div class="band-act">
<a class="btn btn-amber" href="/free-case-review/">Start a free case review</a>
<a class="btn btn-line" href="tel:{FIRM['phone_href']}">Call {FIRM['phone_display']}</a>
</div>
</div>
</section>
"""


def footer(page):
    offices = "".join(f"<p><strong>{o['label']}</strong><br>{o['street']}<br>{o['city']}, {o['region']} {o['zip']}</p>" for o in FIRM["offices"])
    return f"""</main>
{review_band() if page.get('band', True) else ''}<footer class="foot">
<div class="wrap foot-grid">
<div class="foot-brand">
<p class="foot-logo">DeniedFloodClaim<span>.com</span></p>
<p>A Florida flood-claim information resource sponsored by {FIRM['legal_name']}, a Florida property insurance claims law firm.</p>
<a href="/about-the-firm/"><img src="/assets/img/lawgical-logo-white.png" alt="{FIRM['name']}" width="150" height="56" loading="lazy"></a>
</div>
<div>
<p class="foot-h">Flood claim guides</p>
<ul>
<li><a href="/nfip-claim-denied/">NFIP claim denied</a></li>
<li><a href="/flood-insurance-appeal-fema/">FEMA flood appeal</a></li>
<li><a href="/flood-proof-of-loss-deadline/">Proof of loss deadline</a></li>
<li><a href="/what-nfip-flood-insurance-covers/">What NFIP covers</a></li>
<li><a href="/wind-vs-flood-damage-claim/">Wind vs. flood damage</a></li>
<li><a href="/private-flood-insurance-claim-denied-florida/">Private flood policies</a></li>
<li><a href="/flood-claim-underpaid/">Underpaid flood claims</a></li>
</ul>
</div>
<div>
<p class="foot-h">Contact</p>
<p><a class="foot-tel" href="tel:{FIRM['phone_href']}">{FIRM['phone_display']}</a></p>
<p><strong>Principal office</strong><br>{FIRM['street']}<br>{FIRM['city']}, {FIRM['region']} {FIRM['zip']}</p>
{offices}
</div>
</div>
<div class="wrap foot-legal">
<p><strong>Attorney advertising.</strong> This website is sponsored by {FIRM['legal_name']}, which is responsible for its content. Principal office: {FIRM['city']}, Florida; additional office in Destin, Florida. Phone {FIRM['phone_display']}.
The content is general information only, not legal advice. Reading this site, submitting a form or calling does not create an attorney-client relationship. Deadlines depend on your policy, your insurer and your date of loss.
The hiring of a lawyer is an important decision that should not be based solely upon advertisements. See the full <a href="/disclaimer/">disclaimer</a>.</p>
<p class="foot-links"><span>&copy; {date.today().year} {FIRM['legal_name']}</span><a href="/about-the-firm/">About the firm</a><a href="/disclaimer/">Disclaimer</a><a href="/privacy-policy/">Privacy policy</a><a href="/sitemap/">Sitemap</a></p>
</div>
</footer>
<div class="dock" aria-label="Contact">
<a href="tel:{FIRM['phone_href']}">Call {FIRM['phone_display']}</a>
<a class="dock-b" href="/free-case-review/">Free review</a>
</div>
<script src="/assets/js/flood.js?v={asset_version('assets/js/flood.js')}" defer></script>
</body>
</html>
"""


CLAIM_TYPES = [
    "NFIP flood policy: claim denied",
    "NFIP flood policy: paid too little",
    "Private flood policy: denied or underpaid",
    "Homeowners claim denied as \"flood\" (wind vs. water)",
    "Hurricane / windstorm claim",
    "Other property insurance claim",
]


def lead_form(n):
    opts = "".join(f"<option>{esc(x)}</option>" for x in CLAIM_TYPES)
    p = f"lf{n}"
    return f"""<form class="intake" data-intake novalidate>
<div class="in-grid">
<div class="fld"><label for="{p}-name">Full name</label><input id="{p}-name" name="name" type="text" autocomplete="name" required></div>
<div class="fld"><label for="{p}-phone">Phone</label><input id="{p}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="fld"><label for="{p}-email">Email</label><input id="{p}-email" name="email" type="email" autocomplete="email" required></div>
<div class="fld"><label for="{p}-loc">Property city or ZIP</label><input id="{p}-loc" name="location" type="text" autocomplete="postal-code" required></div>
<div class="fld fld-w"><label for="{p}-type">Claim type</label><select id="{p}-type" name="claim_type" required><option value="">Choose one</option>{opts}</select></div>
<div class="fld fld-w"><label for="{p}-msg">Briefly, what happened?</label><textarea id="{p}-msg" name="message" rows="4" maxlength="3000" placeholder="Date of loss, the storm, what the insurer said in its letter, and the date on that letter."></textarea></div>
<div class="hp" aria-hidden="true"><label for="{p}-web">Leave blank</label><input id="{p}-web" name="website" type="text" tabindex="-1" autocomplete="off"></div>
<div class="fld fld-w chk"><input id="{p}-ok" name="consent" type="checkbox" value="1" required><label for="{p}-ok">I understand that submitting this form does not create an attorney-client relationship, that I should not send confidential information until a lawyer agrees to represent me, and I agree that {FIRM['legal_name']} may contact me about my inquiry by phone, text or email.</label></div>
</div>
<button class="btn btn-amber btn-full" type="submit">Request my free case review</button>
<p class="in-note">Free and confidential. Prefer to talk? Call <a href="tel:{FIRM['phone_href']}">{FIRM['phone_display']}</a>.</p>
<div class="in-out" data-intake-out role="status" aria-live="polite"></div>
</form>"""


def expand(body):
    rep = {
        "{{PHONE}}": FIRM["phone_display"], "{{TEL}}": FIRM["phone_href"], "{{FIRM}}": FIRM["name"],
        "{{FIRM_LEGAL}}": FIRM["legal_name"], "{{FIRM_SITE}}": FIRM["site"], "{{REVIEWED}}": REVIEWED,
    }
    for k, v in rep.items():
        body = body.replace(k, v)
    body = body.replace("{{REVIEWED_LINE}}", f'<p class="reviewed"><svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><circle cx="8" cy="8" r="7" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M8 4v4l3 2" stroke="currentColor" stroke-width="1.6" fill="none"/></svg>Last reviewed: {REVIEWED}. General information, not legal advice.</p>')
    if "{{TOC}}" in body:
        items = []

        def add_id(m):
            text = strip_tags(m.group(1))
            slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60].strip("-")
            items.append((slug, text))
            return f'<h2 id="{slug}">{m.group(1)}</h2>'
        body = re.sub(r"<h2>(.*?)</h2>", add_id, body, flags=re.S)
        toc = "".join(f'<li><a href="#{s}">{esc(t)}</a></li>' for s, t in items)
        body = body.replace("{{TOC}}", f'<nav class="toc" aria-label="On this page"><p>On this page</p><ol>{toc}</ol>'
                                       f'<a class="toc-cta" href="/free-case-review/">Free case review &rarr;</a></nav>')
    n = 0
    while "{{LEAD_FORM}}" in body:
        n += 1
        body = body.replace("{{LEAD_FORM}}", lead_form(n), 1)
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
        meta["h1"] = strip_tags(h1.group(1)) if h1 else meta["title"]
        pages.append(meta)
    return pages


def out_file(path):
    if path == "/":
        return os.path.join(OUT, "home.html")
    if path.endswith(".html"):
        return os.path.join(OUT, path.lstrip("/"))
    return os.path.join(OUT, path.strip("/"), "index.html")


def sitemap_html(pages):
    groups = {}
    for p in pages:
        if p.get("sitemap") is False:
            continue
        groups.setdefault(p.get("group", "Site"), []).append(p)
    out = ""
    for g in ("Start here", "Guides", "Site"):
        if g in groups:
            items = "".join(f'<li><a href="{p["path"]}">{esc(p["h1"])}</a><span>{esc(p["description"])}</span></li>' for p in groups[g])
            out += f'<h2>{g}</h2><ul class="smap">{items}</ul>'
    return out


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(SRC, "static"), OUT)
    pages = load_pages()
    for p in pages:
        body = p["body"].replace("{{SITEMAP}}", sitemap_html(pages))
        p["body"] = body
        doc = head(p) + masthead(p.get("nav", p["path"])) + crumbs(p) + body + footer(p)
        f = out_file(p["path"])
        os.makedirs(os.path.dirname(f), exist_ok=True)
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(doc)
    urls = "".join(f"<url><loc>{SITE['origin']}{p['path']}</loc><lastmod>{p.get('modified', TODAY)}</lastmod></url>\n"
                   for p in pages if p.get("sitemap") is not False)
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as fh:
        if STAGING:
            fh.write("User-agent: *\nDisallow: /\n")
        else:
            fh.write(f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {SITE['origin']}/sitemap.xml\n")
    print(f"built {len(pages)} pages into public/ (staging={STAGING})")


if __name__ == "__main__":
    main()
