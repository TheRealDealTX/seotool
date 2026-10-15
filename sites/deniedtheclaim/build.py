#!/usr/bin/env python3
"""Static site generator for deniedtheclaim.com (stdlib only).

Every page body is a file in src/pages/*.html whose first line is a JSON
header inside an HTML comment, e.g.

    <!--{"path": "/denial-letter-explained/", "title": "...", "description": "...",
         "crumb": "Denial letter explained", "article": true}-->

build.py wraps each body in the shared "legal notebook" layout, builds the
JSON-LD graph (WebSite, LegalService, WebPage, BreadcrumbList, Article and a
FAQPage generated from the page's <details class="faq"> blocks) and writes the
finished site to public/ together with everything in src/static/.

    python3 build.py            # writes ./public
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

# Pages are indexable. Set to True on a test domain to noindex everything.
STAGING = False

SITE = {
    "name": "Denied the Claim",
    "origin": "https://deniedtheclaim.com",
    "tagline": "A Florida homeowner's guide to what to do when the property insurer denied the claim",
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
    ("The 9 steps", "/#steps"),
    ("Denial letters", "/denial-letter-explained/"),
    ("Appeal options", "/how-to-appeal-a-denied-homeowners-insurance-claim-florida/"),
    ("Hurricane", "/denied-hurricane-claim/"),
    ("Water", "/denied-water-damage-claim/"),
    ("The firm", "/about-the-firm/"),
]

REVIEWED = "October 2026"
PUBLISHED = "2026-10-15"
TODAY = date.today().isoformat()


def esc(text):
    return html.escape(str(text), quote=True)


def asset_version(rel):
    with open(os.path.join(SRC, "static", rel), "rb") as fh:
        return hashlib.sha1(fh.read()).hexdigest()[:10]


def strip_tags(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


FAQ_RE = re.compile(r'<details class="faq"[^>]*>\s*<summary>(.*?)</summary>(.*?)</details>', re.S)


def faq_schema(body, canonical):
    items = FAQ_RE.findall(body)
    if not items:
        return None
    return {
        "@type": "FAQPage",
        "@id": canonical + "#faq",
        "mainEntity": [
            {"@type": "Question", "name": strip_tags(q),
             "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
            for q, a in items
        ],
    }


def firm_node():
    def addr(o):
        return {"@type": "PostalAddress", "streetAddress": o["street"], "addressLocality": o["city"],
                "addressRegion": o["region"], "postalCode": o["zip"], "addressCountry": "US"}
    return {
        "@type": "LegalService",
        "@id": SITE["origin"] + "/#firm",
        "name": FIRM["legal_name"],
        "url": FIRM["site"],
        "telephone": FIRM["phone_href"],
        "image": SITE["origin"] + "/assets/img/lawgical-logo.png",
        "address": addr(FIRM),
        "location": [{"@type": "Place", "name": "Orlando office (principal)", "address": addr(FIRM)}] +
                    [{"@type": "Place", "name": o["label"].replace(" office", "") + " office", "address": addr(o)} for o in FIRM["offices"]],
        "areaServed": {"@type": "State", "name": "Florida"},
        "knowsAbout": ["Denied property insurance claims", "Homeowners insurance claim disputes",
                       "Hurricane and windstorm claims", "Water damage claims", "Florida property insurance law"],
    }


def head(page, body):
    canonical = SITE["origin"] + page["path"]
    robots = "noindex, nofollow" if STAGING else page.get("robots", "index, follow, max-image-preview:large")
    graph = [
        {"@type": "WebSite", "@id": SITE["origin"] + "/#website", "url": SITE["origin"] + "/",
         "name": SITE["name"], "description": SITE["tagline"], "inLanguage": "en-US",
         "publisher": {"@id": SITE["origin"] + "/#firm"}},
        firm_node(),
        {"@type": "WebPage", "@id": canonical + "#webpage", "url": canonical, "name": page["title"],
         "description": page["description"], "isPartOf": {"@id": SITE["origin"] + "/#website"},
         "inLanguage": "en-US", "dateModified": page.get("modified", PUBLISHED),
         "about": {"@type": "Thing", "name": "Denied property insurance claims in Florida"}},
    ]
    if page["path"] != "/" and not page["path"].endswith(".html"):
        graph.append({"@type": "BreadcrumbList", "@id": canonical + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE["origin"] + "/"},
            {"@type": "ListItem", "position": 2, "name": page["crumb"], "item": canonical},
        ]})
    if page.get("article"):
        graph.append({
            "@type": "Article", "@id": canonical + "#article", "headline": page["h1"][:110],
            "description": page["description"], "mainEntityOfPage": {"@id": canonical + "#webpage"},
            "datePublished": PUBLISHED, "dateModified": page.get("modified", PUBLISHED),
            "author": {"@id": SITE["origin"] + "/#firm"}, "publisher": {"@id": SITE["origin"] + "/#firm"},
            "inLanguage": "en-US",
        })
    faq = faq_schema(body, canonical)
    if faq:
        graph.append(faq)
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
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
<meta name="theme-color" content="#f6f2e9">
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,650;0,9..144,800;1,9..144,500&amp;family=Public+Sans:ital,wght@0,400;0,600;0,700;1,400&amp;family=IBM+Plex+Mono:wght@500&amp;display=swap">
<link rel="stylesheet" href="/assets/css/notebook.css?v={asset_version('assets/css/notebook.css')}">
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
<a class="skip" href="#main">Skip to the guide</a>
"""


def masthead(active):
    links = "".join(
        f'<li><a href="{href}"{" aria-current=\"page\"" if href == active else ""}>{label}</a></li>' for label, href in NAV
    )
    return f"""<div class="adbar"><div class="wrap adbar-in"><span>Attorney advertising &middot; {FIRM['legal_name']}</span><a href="tel:{FIRM['phone_href']}">Free review: {FIRM['phone_display']}</a></div></div>
<header class="mast">
<div class="wrap mast-in">
<a class="wordmark" href="/" aria-label="{SITE['name']} home"><span class="wm-mark" aria-hidden="true">&times;</span><span class="wm-text">Denied <em>the</em> Claim</span><span class="wm-sub">A Florida homeowner&rsquo;s notebook</span></a>
<button class="menu" type="button" aria-expanded="false" aria-controls="nav" data-menu>Menu</button>
<nav id="nav" class="nav" aria-label="Primary"><ul>{links}</ul><a class="nav-cta" href="/free-case-review/">Free case review</a></nav>
</div>
</header>
<main id="main">
"""


def closing_cta():
    return f"""<section class="closing" aria-labelledby="closing-h">
<div class="wrap closing-in">
<div>
<p class="tag">Next page in your notebook</p>
<h2 id="closing-h">Have a lawyer read the denial with you</h2>
<p>{FIRM['legal_name']} handles Florida residential and commercial property insurance claims that were denied, delayed or underpaid. Send the letter, the policy and your photos; the review is free and there are no upfront fees.</p>
</div>
<div class="closing-act">
<a class="btn btn-red" href="/free-case-review/">Start a free case review</a>
<a class="btn btn-line" href="tel:{FIRM['phone_href']}">Call {FIRM['phone_display']}</a>
</div>
</div>
</section>
"""


def footer(show_cta=True):
    offices = "".join(f"<p><strong>{o['label']}</strong><br>{o['street']}<br>{o['city']}, {o['region']} {o['zip']}</p>" for o in FIRM["offices"])
    return f"""</main>
{closing_cta() if show_cta else ''}<footer class="foot">
<div class="wrap">
<div class="foot-grid">
<div>
<p class="foot-name">Denied <em>the</em> Claim</p>
<p>Plain-language notes for Florida homeowners whose property insurance company denied the claim. Published by {FIRM['legal_name']}.</p>
<img src="/assets/img/lawgical-logo.png" alt="{FIRM['name']}" width="141" height="50" loading="lazy">
</div>
<div>
<p class="foot-h">Guides</p>
<ul>
<li><a href="/insurance-denied-my-claim-florida/">Insurance denied my claim in Florida</a></li>
<li><a href="/denial-letter-explained/">Denial letter explained</a></li>
<li><a href="/wear-and-tear-denial/">Wear and tear denials</a></li>
<li><a href="/late-notice-claim-denial/">Late notice denials</a></li>
<li><a href="/how-to-appeal-a-denied-homeowners-insurance-claim-florida/">How to appeal a denied claim</a></li>
<li><a href="/denied-hurricane-claim/">Denied hurricane claims</a></li>
<li><a href="/denied-water-damage-claim/">Denied water damage claims</a></li>
</ul>
</div>
<div>
<p class="foot-h">{FIRM['legal_name']}</p>
<p><strong>Principal office</strong><br>{FIRM['street']}<br>{FIRM['city']}, {FIRM['region']} {FIRM['zip']}</p>
{offices}
<p><a href="tel:{FIRM['phone_href']}">{FIRM['phone_display']}</a></p>
</div>
</div>
<p class="legal">Attorney advertising. This website is published by {FIRM['legal_name']}, which is responsible for its content. Principal office: {FIRM['city']}, Florida; additional office in {', '.join(o['city'] for o in FIRM['offices'])}, Florida. Phone {FIRM['phone_display']}.
The material on this site is information only, not legal advice, and may not reflect the law that applies to your policy or date of loss. Reading it or contacting us does not create an attorney-client relationship.
No upfront fees: the firm is paid only if you recover; ask how case costs are handled under the written fee agreement. The hiring of a lawyer is an important decision that should not be based solely upon advertisements. See the full <a href="/disclaimer/">disclaimer</a>.</p>
<p class="foot-bottom"><span>&copy; {date.today().year} {FIRM['legal_name']}</span><span><a href="/about-the-firm/">About the firm</a> &middot; <a href="/disclaimer/">Disclaimer</a> &middot; <a href="/privacy-policy/">Privacy</a> &middot; <a href="/sitemap/">Sitemap</a></span></p>
</div>
</footer>
<div class="callbar"><a href="tel:{FIRM['phone_href']}">Call {FIRM['phone_display']}</a><a href="/free-case-review/" class="callbar-red">Free review</a></div>
<script src="/assets/js/notebook.js?v={asset_version('assets/js/notebook.js')}" defer></script>
</body>
</html>
"""


CLAIM_TYPES = ["Hurricane or windstorm", "Water damage / plumbing leak", "Roof damage or roof leak", "Fire",
               "Mold", "Hail", "Sinkhole", "Theft or vandalism", "Commercial property", "Other / not sure"]
STATUS = ["Fully denied", "Partly denied / paid less than repairs cost", "Denied as below my deductible",
          "Delayed / no decision yet", "Not filed yet"]


def lead_form(n):
    opts = lambda xs: "".join(f"<option>{esc(x)}</option>" for x in xs)
    return f"""<form class="form" data-lead novalidate>
<div class="form-grid">
<p class="field"><label for="f{n}-name">Full name</label><input id="f{n}-name" name="name" type="text" autocomplete="name" required></p>
<p class="field"><label for="f{n}-phone">Phone</label><input id="f{n}-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required></p>
<p class="field"><label for="f{n}-email">Email</label><input id="f{n}-email" name="email" type="email" autocomplete="email" required></p>
<p class="field"><label for="f{n}-loc">Property city or ZIP</label><input id="f{n}-loc" name="location" type="text" autocomplete="postal-code" required></p>
<p class="field"><label for="f{n}-type">Claim type</label><select id="f{n}-type" name="claim_type" required>{opts(CLAIM_TYPES)}</select></p>
<p class="field"><label for="f{n}-status">Where the claim stands</label><select id="f{n}-status" name="status">{opts(STATUS)}</select></p>
<p class="field wide"><label for="f{n}-msg">Briefly, what happened? <span class="opt">(optional)</span></label><textarea id="f{n}-msg" name="message" rows="3" maxlength="3000" placeholder="Date of loss, insurer, and the reason given in the denial letter"></textarea></p>
<p class="hp" aria-hidden="true"><label for="f{n}-web">Leave blank</label><input id="f{n}-web" type="text" name="website" tabindex="-1" autocomplete="off"></p>
<p class="field wide check"><input id="f{n}-ok" type="checkbox" name="consent" value="1" required><label for="f{n}-ok">I understand that sending this form does not create an attorney-client relationship, and that I should not send confidential details until a lawyer agrees to represent me. {FIRM['legal_name']} may contact me by phone, text or email about this request.</label></p>
</div>
<button class="btn btn-red btn-wide" type="submit">Request my free case review</button>
<p class="form-note">Free and confidential review by {FIRM['legal_name']}. Prefer to talk? Call <a href="tel:{FIRM['phone_href']}">{FIRM['phone_display']}</a>.</p>
<p class="form-out" data-out role="status" aria-live="polite"></p>
</form>"""


def deadline_tool(n):
    return f"""<div class="tool" data-deadlines>
<p class="tool-h">Deadline worksheet</p>
<p class="field"><label for="dl{n}">Date of loss (for a hurricane, the landfall date)</label><input id="dl{n}" type="date" data-dol></p>
<ol class="tool-out" data-dl-out aria-live="polite"><li>Enter a date to see the general Florida timelines.</li></ol>
<p class="tool-fine">General statutory periods only (ss. 627.70132 and 95.11(2)(e), Fla. Stat.). Your policy, the date it was issued and the facts can change the answer &mdash; confirm with a lawyer.</p>
</div>"""


def aside(body):
    """Sticky sidebar for guide pages: a table of contents built from <h2 id=...> plus a call box."""
    heads = re.findall(r'<h2 id="([\w-]+)"[^>]*>(.*?)</h2>', body, re.S)
    toc = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in heads)
    return f"""<aside class="aside" aria-label="On this page"><div class="aside-in">
<nav class="toc" aria-label="Contents"><p>On this page</p><ol>{toc}</ol></nav>
<div class="mini-cta"><strong>Denied? Get a second set of eyes.</strong><p>{FIRM['legal_name']} reviews Florida property claim denials for free. No upfront fees.</p>
<a class="btn btn-red" href="/free-case-review/">Free case review</a><a class="btn btn-line" href="tel:{FIRM['phone_href']}">{FIRM['phone_display']}</a></div>
</div></aside>"""


def expand(body):
    if "{{ASIDE}}" in body:
        body = body.replace("{{ASIDE}}", aside(body))
    rep = {
        "{{PHONE}}": FIRM["phone_display"], "{{TEL}}": FIRM["phone_href"], "{{FIRM}}": FIRM["name"],
        "{{FIRM_LEGAL}}": FIRM["legal_name"], "{{FIRM_SITE}}": FIRM["site"], "{{REVIEWED}}": REVIEWED,
    }
    for k, v in rep.items():
        body = body.replace(k, v)
    n = 0
    while "{{LEAD_FORM}}" in body:
        n += 1
        body = body.replace("{{LEAD_FORM}}", lead_form(n), 1)
    n = 0
    while "{{DEADLINES}}" in body:
        n += 1
        body = body.replace("{{DEADLINES}}", deadline_tool(n), 1)
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
            raise SystemExit(f"{name}: missing JSON header comment")
        meta = json.loads(m.group(1))
        meta["body"] = expand(raw[m.end():])
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", meta["body"], re.S)
        meta["h1"] = strip_tags(h1.group(1)) if h1 else meta["title"]
        meta.setdefault("crumb", meta["h1"])
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
        groups.setdefault(p.get("group", "Site"), []).append(p)
    out = ""
    for g in ("Start here", "Guides", "Site"):
        if g in groups:
            items = "".join(f'<li><a href="{p["path"]}">{esc(p["crumb"] if p["path"] != "/" else "Home: what to do when the insurer denied the claim")}</a></li>' for p in groups[g])
            out += f"<h2>{g}</h2><ul class=\"maplist\">{items}</ul>"
    return out


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(SRC, "static"), OUT)
    pages = load_pages()
    for p in pages:
        body = p["body"].replace("{{SITEMAP}}", sitemap_list(pages))
        doc = head(p, body) + masthead(p.get("nav")) + body + footer(p.get("cta", True))
        f = out_file(p["path"])
        os.makedirs(os.path.dirname(f), exist_ok=True)
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(doc)
    urls = "".join(
        f"  <url><loc>{SITE['origin']}{p['path']}</loc><lastmod>{p.get('modified', PUBLISHED)}</lastmod></url>\n"
        for p in pages if p.get("sitemap") is not False
    )
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                 + urls + "</urlset>\n")
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as fh:
        if STAGING:
            fh.write("User-agent: *\nDisallow: /\n")
        else:
            fh.write(f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {SITE['origin']}/sitemap.xml\n")
    print(f"built {len(pages)} pages into public/ (staging={STAGING})")


if __name__ == "__main__":
    main()
