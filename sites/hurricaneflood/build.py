#!/usr/bin/env python3
"""Static builder for hurricaneflood.com (stdlib only).

Every file in src/pages/ is an HTML body whose first line is a JSON comment:

    <!--{"path": "/wind-vs-flood-damage/", "title": "...", "description": "...", "kind": "guide"}-->

The builder wraps each body in the shared shell (head, masthead, footer),
expands a few {{SHORTCODES}}, derives FAQPage schema from the page's
<details class="qa"> blocks, and writes public/ with sitemap.xml and robots.txt.
Everything in src/static/ (CSS, JS, PHP front controller, lead API) is copied
as-is.

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

STAGING = False   # True = noindex every page and disallow crawling

SITE = {
    "name": "HurricaneFlood.com",
    "origin": "https://hurricaneflood.com",
    "tagline": "Florida hurricane flood, storm surge and wind-damage claim information",
}

FIRM = {
    "name": "The Lawgical Firm",
    "legal": "The Lawgical Firm, P.A.",
    "site": "https://thelawgicalfirm.com/",
    "practice": "https://thelawgicalfirm.com/residential-property-insurance-claims/hurricane-windstorm/",
    "phone": "(407) 433-4131",
    "tel": "+14074334131",
    "offices": [
        {"label": "Principal office", "street": "3191 Maguire Blvd, Ste 160", "city": "Orlando", "zip": "32803"},
        {"label": "Destin office", "street": "34990 Emerald Coast Pkwy, Ste 359", "city": "Destin", "zip": "32541"},
    ],
}

NAV = [
    ("Storm Surge", "/storm-surge-damage-claim/"),
    ("Wind vs Flood", "/wind-vs-flood-damage/"),
    ("Wind-Driven Rain", "/wind-driven-rain-claim/"),
    ("Flood Claims", "/hurricane-flood-insurance-claim-florida/"),
    ("Deductibles", "/hurricane-deductible-florida/"),
    ("Deadlines", "/hurricane-claim-deadlines-florida/"),
]

GUIDES = [
    ("/storm-surge-damage-claim/", "Storm surge damage claims", "Who pays when the Gulf or the Atlantic comes ashore."),
    ("/wind-vs-flood-damage/", "Wind vs flood damage", "How insurers split a mixed loss, and anti-concurrent causation clauses."),
    ("/wind-driven-rain-claim/", "Wind-driven rain claims", "The opening rule that decides interior rain coverage."),
    ("/hurricane-flood-insurance-claim-florida/", "Flood insurance claims in Florida", "NFIP and private flood: proof of loss, appeals and suit limits."),
    ("/hurricane-deductible-florida/", "Hurricane deductibles", "How s. 627.701 deductibles work, with a quick calculator."),
    ("/documenting-hurricane-flood-damage/", "Documenting the damage", "Water lines, wind signatures and the evidence file."),
    ("/hurricane-claim-deadlines-florida/", "Claim deadlines", "Both policy types side by side, from notice to lawsuit."),
    ("/claim-denied-as-flood/", "Claim denied as flood?", "What to do when wind damage is blamed on water."),
]

TODAY = date.today().isoformat()
REVIEWED = "October 2026"


def esc(s):
    return html.escape(str(s), quote=True)


def ver(rel):
    with open(os.path.join(SRC, "static", rel), "rb") as fh:
        return hashlib.sha1(fh.read()).hexdigest()[:10]


def strip_tags(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def faq_schema(body):
    qas = re.findall(r'(?s)<details class="qa"[^>]*>\s*<summary>(.*?)</summary>(.*?)</details>', body)
    if not qas:
        return None
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip_tags(q),
         "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in qas]}


def short_title(page):
    return page.get("crumb") or page["title"].split(" | ")[0]


def schema(page):
    url = SITE["origin"] + page["path"]
    graph = [
        {"@type": "WebSite", "@id": SITE["origin"] + "/#site", "url": SITE["origin"] + "/",
         "name": SITE["name"], "description": SITE["tagline"], "inLanguage": "en-US",
         "publisher": {"@id": SITE["origin"] + "/#firm"}},
        {"@type": "LegalService", "@id": SITE["origin"] + "/#firm", "name": FIRM["legal"],
         "url": FIRM["site"], "telephone": FIRM["tel"],
         "logo": SITE["origin"] + "/assets/img/lawgical-logo.png",
         "address": {"@type": "PostalAddress", "streetAddress": FIRM["offices"][0]["street"],
                     "addressLocality": "Orlando", "addressRegion": "FL", "postalCode": "32803", "addressCountry": "US"},
         "location": [{"@type": "Place", "name": f"{FIRM['legal']} - {o['label']}",
                       "address": {"@type": "PostalAddress", "streetAddress": o["street"], "addressLocality": o["city"],
                                   "addressRegion": "FL", "postalCode": o["zip"], "addressCountry": "US"}}
                      for o in FIRM["offices"]],
         "areaServed": {"@type": "State", "name": "Florida"},
         "knowsAbout": ["Hurricane and windstorm insurance claims", "Wind versus flood causation disputes",
                        "Water damage insurance claims", "Denied and underpaid property insurance claims"]},
        {"@type": "WebPage", "@id": url + "#page", "url": url, "name": page["title"],
         "description": page["description"], "isPartOf": {"@id": SITE["origin"] + "/#site"},
         "inLanguage": "en-US", "dateModified": page.get("modified", TODAY)},
    ]
    if page["path"] != "/":
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE["origin"] + "/"},
            {"@type": "ListItem", "position": 2, "name": short_title(page), "item": url}]})
    if page.get("kind") == "guide":
        graph.append({"@type": "Article", "@id": url + "#article", "headline": page["h1"] if "h1" in page else short_title(page),
                      "description": page["description"], "mainEntityOfPage": {"@id": url + "#page"},
                      "datePublished": page.get("published", "2026-10-15"), "dateModified": page.get("modified", TODAY),
                      "author": {"@id": SITE["origin"] + "/#firm"}, "publisher": {"@id": SITE["origin"] + "/#firm"},
                      "inLanguage": "en-US"})
    fs = faq_schema(page["body"])
    if fs:
        graph.append(fs)
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)


def head(page):
    url = SITE["origin"] + page["path"]
    robots = "noindex, nofollow" if STAGING else page.get("robots", "index, follow, max-image-preview:large")
    return f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(page['title'])}</title>
<meta name="description" content="{esc(page['description'])}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#0b121a">
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&amp;family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&amp;display=swap">
<link rel="stylesheet" href="/assets/css/storm.css?v={ver('assets/css/storm.css')}">
<script type="application/ld+json">
{schema(page)}
</script>
</head>
<body class="pg-{page.get('kind', 'page')}">
<a class="skip" href="#main">Skip to main content</a>
"""


MARK = ('<svg class="mark" viewBox="0 0 40 40" aria-hidden="true" focusable="false">'
        '<rect width="40" height="40" rx="6" fill="#13263f"/>'
        '<path d="M20 6a14 14 0 0 1 12 7c-4-2-9-2-12 1 4-1 8 1 9 5 1 5-3 9-9 9" fill="none" stroke="#19d3f0" stroke-width="3" stroke-linecap="round"/>'
        '<path d="M4 30c4-3 8-3 12 0s8 3 12 0 6-3 8-1" fill="none" stroke="#d42a25" stroke-width="3" stroke-linecap="round"/></svg>')


def masthead(active):
    links = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a></li>' for t, h in NAV)
    return f"""<div class="warnbar"><div class="wrap warnbar-in"><span class="warnbar-tag">Storm claim line</span>
<span class="warnbar-msg">Insurer blaming flood for wind damage? <a href="/claim-denied-as-flood/">Read this first</a></span>
<a class="warnbar-tel" href="tel:{FIRM['tel']}">{FIRM['phone']}</a></div></div>
<header class="mast">
<div class="wrap mast-in">
<a class="logo" href="/" aria-label="HurricaneFlood.com home">{MARK}<span class="logo-txt"><b>HurricaneFlood</b><i>.com</i></span></a>
<nav class="topnav" id="topnav" aria-label="Main">
<ul>{links}</ul>
<a class="btn btn-red topnav-cta" href="/free-case-review/">Free review</a>
</nav>
<button class="navtoggle" type="button" aria-expanded="false" aria-controls="topnav" data-navtoggle><span class="bars" aria-hidden="true"></span><span class="navtoggle-l">Menu</span></button>
</div>
</header>
<main id="main">
"""


def crumbs(page):
    if page["path"] == "/" or page.get("kind") == "error":
        return ""
    return (f'<nav class="crumbs wrap" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li>'
            f'<li aria-current="page">{esc(short_title(page))}</li></ol></nav>\n')


def offices_html():
    return "".join(f'<p><span class="lbl">{o["label"]}</span>{o["street"]}<br>{o["city"]}, FL {o["zip"]}</p>' for o in FIRM["offices"])


def cta_strip():
    return f"""<section class="band band-red cta-strip" aria-labelledby="cta-h">
<div class="wrap cta-strip-in">
<div><p class="kicker">No upfront fees &middot; no attorney fee unless there is a recovery</p>
<h2 id="cta-h">Wind damage blamed on water? Get the claim reviewed.</h2>
<p>{FIRM['legal']} handles Florida hurricane, windstorm and water-damage property insurance claims for homeowners and commercial property owners.</p></div>
<div class="cta-strip-btns"><a class="btn btn-white" href="/free-case-review/">Start a free case review</a><a class="btn btn-line-white" href="tel:{FIRM['tel']}">Call {FIRM['phone']}</a></div>
</div></section>
"""


def footer(page):
    guide_links = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t, _ in GUIDES)
    return f"""</main>
{cta_strip() if page.get('cta', True) else ''}<footer class="foot">
<div class="wrap foot-grid">
<div class="foot-brand">
<a class="logo logo-foot" href="/">{MARK}<span class="logo-txt"><b>HurricaneFlood</b><i>.com</i></span></a>
<p>Plain-language Florida information on storm surge, flood, wind and wind-driven rain claims, sponsored by {FIRM['legal']}</p>
<a href="{FIRM['site']}" rel="noopener" target="_blank"><img src="/assets/img/lawgical-logo-white.png" alt="{FIRM['name']}" width="150" height="56" loading="lazy"></a>
</div>
<div><h2 class="foot-h">Guides</h2><ul class="foot-list">{guide_links}</ul></div>
<div><h2 class="foot-h">The firm</h2><ul class="foot-list"><li><a href="/free-case-review/">Free case review</a></li><li><a href="/about-the-firm/">About the firm</a></li><li><a href="/sitemap/">Sitemap</a></li><li><a href="/disclaimer/">Disclaimer</a></li><li><a href="/privacy-policy/">Privacy policy</a></li></ul></div>
<div class="foot-contact"><h2 class="foot-h">{FIRM['legal']}</h2><p><a class="foot-tel" href="tel:{FIRM['tel']}">{FIRM['phone']}</a></p>{offices_html()}</div>
</div>
<div class="wrap foot-legal">
<p><strong>Attorney advertising.</strong> This website is sponsored by {FIRM['legal']}, which is responsible for its content. Principal office: Orlando, Florida. Additional office: Destin, Florida. Phone {FIRM['phone']}. See our <a href="/disclaimer/">disclaimer</a>.</p>
<p>The material on this site is information only, not legal advice. Reading it, calling, or submitting a form does not create an attorney-client relationship. Laws and policy terms change and deadlines depend on your policy and date of loss. The hiring of a lawyer is an important decision that should not be based solely on advertisements.</p>
<p>&copy; {date.today().year} {FIRM['legal']} &middot; <a href="/privacy-policy/">Privacy</a> &middot; <a href="/sitemap/">Sitemap</a></p>
</div>
</footer>
<div class="callbar"><a class="callbar-tel" href="tel:{FIRM['tel']}">Call {FIRM['phone']}</a><a class="callbar-form" href="/free-case-review/">Free review</a></div>
<script src="/assets/js/storm.js?v={ver('assets/js/storm.js')}" defer></script>
</body>
</html>
"""


CLAIM_TYPES = [
    "Hurricane wind damage denied or reduced as flood",
    "Mixed wind and storm surge damage",
    "Wind-driven rain / roof opening damage",
    "Underpaid hurricane claim",
    "Delayed hurricane claim / no decision",
    "Hurricane deductible dispute",
    "Commercial property hurricane claim",
    "Not sure / something else",
]


def lead_form(n):
    opts = "".join(f"<option>{esc(c)}</option>" for c in CLAIM_TYPES)
    p = f"lf{n}"
    return f"""<form class="lead" data-lead novalidate>
<div class="lead-grid">
<div class="fld"><label for="{p}-name">Full name</label><input id="{p}-name" name="name" type="text" autocomplete="name" required></div>
<div class="fld"><label for="{p}-phone">Phone</label><input id="{p}-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required></div>
<div class="fld"><label for="{p}-email">Email</label><input id="{p}-email" name="email" type="email" autocomplete="email" required></div>
<div class="fld"><label for="{p}-loc">Property city or ZIP</label><input id="{p}-loc" name="location" type="text" autocomplete="postal-code" required></div>
<div class="fld fld-full"><label for="{p}-type">Claim type</label><select id="{p}-type" name="claim_type" required><option value="">Choose one</option>{opts}</select></div>
<div class="fld fld-full"><label for="{p}-msg">What happened? <span class="opt">(short description)</span></label><textarea id="{p}-msg" name="message" rows="4" maxlength="3000" placeholder="Example: Water line 14 inches inside, but the roof also lost shingles and the ceilings are stained. Insurer denied everything as flood."></textarea></div>
<input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
<label class="consent fld-full"><input type="checkbox" name="consent" value="1" required> <span>I understand that submitting this form does not create an attorney-client relationship with {FIRM['legal']}, that I should not send confidential details until an attorney agrees to represent me, and I agree to be contacted about my inquiry by phone, text or email.</span></label>
</div>
<button class="btn btn-red btn-wide" type="submit">Request my free case review</button>
<p class="lead-note">Prefer to talk? Call <a href="tel:{FIRM['tel']}">{FIRM['phone']}</a>. Information only, not legal advice.</p>
<div class="lead-out" role="status" aria-live="polite" data-lead-out></div>
</form>"""


def reviewed():
    return f'<p class="reviewed">Last reviewed: {REVIEWED}. Florida statutes cited are from the 2026 Florida Statutes; NFIP terms from 44 CFR Part 61, Appendix A.</p>'


def related(current):
    cards = "".join(f'<li><a href="{h}"><b>{t}</b><span>{d}</span></a></li>' for h, t, d in GUIDES if h != current)
    return f'<section class="band band-ink related" aria-labelledby="rel-h"><div class="wrap"><h2 id="rel-h">Keep reading</h2><ul class="relgrid">{cards}</ul></div></section>'


def sitemap_html(pages):
    groups = {"Guides": [], "Firm": [], "Legal": []}
    for p in pages:
        if p.get("sitemap") is False:
            continue
        groups[p.get("group", "Guides")].append(p)
    out = ""
    for g, items in groups.items():
        lis = "".join(f'<li><a href="{p["path"]}">{esc(short_title(p))}</a> <span>{esc(p["description"])}</span></li>' for p in items)
        out += f'<h2>{g}</h2><ul class="smap">{lis}</ul>'
    return out


HEADER_RE = re.compile(r"^\s*<!--(\{.*?\})-->\s*", re.S)


def load():
    pages = []
    for name in sorted(os.listdir(os.path.join(SRC, "pages"))):
        if not name.endswith(".html"):
            continue
        raw = open(os.path.join(SRC, "pages", name), encoding="utf-8").read()
        m = HEADER_RE.match(raw)
        if not m:
            raise SystemExit(f"{name}: missing JSON header")
        meta = json.loads(m.group(1))
        meta["body"] = raw[m.end():]
        meta["src"] = name
        pages.append(meta)
    return pages


def expand(page, pages):
    b = page["body"]
    rep = {
        "{{PHONE}}": FIRM["phone"], "{{TEL}}": FIRM["tel"], "{{FIRM}}": FIRM["name"], "{{FIRM_LEGAL}}": FIRM["legal"],
        "{{FIRM_SITE}}": FIRM["site"], "{{FIRM_PRACTICE}}": FIRM["practice"], "{{REVIEWED}}": reviewed(),
        "{{RELATED}}": related(page["path"]), "{{OFFICES}}": offices_html(),
    }
    for k, v in rep.items():
        b = b.replace(k, v)
    if "{{SITEMAP}}" in b:
        b = b.replace("{{SITEMAP}}", sitemap_html(pages))
    n = 0
    while "{{LEAD_FORM}}" in b:
        n += 1
        b = b.replace("{{LEAD_FORM}}", lead_form(n), 1)
    return b


def out_path(path):
    if path == "/":
        return os.path.join(OUT, "home.html")
    if path.endswith(".html"):
        return os.path.join(OUT, path.lstrip("/"))
    return os.path.join(OUT, path.strip("/"), "index.html")


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(SRC, "static"), OUT)
    pages = load()
    for p in pages:
        p["body"] = expand(p, pages)
    for p in pages:
        doc = head(p) + masthead(p.get("nav", p["path"])) + crumbs(p) + p["body"] + footer(p)
        f = out_path(p["path"])
        os.makedirs(os.path.dirname(f), exist_ok=True)
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(doc)
    urls = "".join(f"<url><loc>{SITE['origin']}{p['path']}</loc><lastmod>{p.get('modified', TODAY)}</lastmod></url>\n"
                   for p in pages if p.get("sitemap") is not False)
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                 + urls + "</urlset>\n")
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as fh:
        if STAGING:
            fh.write("User-agent: *\nDisallow: /\n")
        else:
            fh.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE['origin']}/sitemap.xml\n")
    print(f"built {len(pages)} pages -> {os.path.relpath(OUT, ROOT)}/ (staging={STAGING})")


if __name__ == "__main__":
    main()
