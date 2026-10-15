#!/usr/bin/env python3
"""Static site generator for deniedclaimlaw.com (stdlib only).

Every page body lives in src/pages/*.html and starts with a one-line JSON
header in an HTML comment, e.g.

    <!--{"path": "/insurance-appraisal-florida/", "kind": "guide", "title": "...",
         "description": "...", "h1": "...", "dek": "...", "crumb": "Appraisal"}-->

kind = "home" | "guide" | "page".  Guide pages get the law-library layout:
a title block with a "Last reviewed" line, a sticky table of contents built
from the body's <h2 id="..."> headings, Article schema, and FAQPage schema
built from the body's <details class="faq"> blocks.

    python3 build.py        # writes ./public
"""

import hashlib
import html as htmlmod
import json
import os
import re
import shutil
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "public")

STAGING = False  # True = noindex every page and disallow crawling

SITE = {
    "name": "Denied Claim Law",
    "domain": "deniedclaimlaw.com",
    "origin": "https://deniedclaimlaw.com",
    "tagline": "The Florida law behind denied property insurance claims",
    "reviewed": "October 2026",
    "published": "2026-10-15",
}

# Florida Bar Rule 4-7.12: name the responsible firm and an office city.
FIRM = {
    "name": "The Lawgical Firm",
    "legal_name": "The Lawgical Firm, P.A.",
    "site": "https://thelawgicalfirm.com/",
    "phone_display": "(407) 433-4131",
    "phone_href": "+14074334131",
    "offices": [
        {"label": "Principal office", "street": "3191 Maguire Blvd, Ste 160", "city": "Orlando", "region": "FL", "zip": "32803"},
        {"label": "Destin office", "street": "34990 Emerald Coast Pkwy, Ste 359", "city": "Destin", "region": "FL", "zip": "32541"},
    ],
}

NAV = [
    ("Florida Lawyer", "/denied-claim-lawyer-florida/"),
    ("Claim Deadlines", "/florida-claim-deadlines/"),
    ("Pre-Suit Notice", "/pre-suit-notice-florida-property-insurance/"),
    ("Appraisal", "/insurance-appraisal-florida/"),
    ("Bad Faith", "/florida-insurance-bad-faith-law/"),
    ("Fees After HB 837", "/florida-insurance-attorney-fees/"),
    ("Do I Need a Lawyer?", "/do-i-need-a-lawyer-for-a-denied-insurance-claim/"),
]

CLAIM_TYPES = ["Roof damage or roof leak", "Hurricane / windstorm", "Hail damage", "Water damage / plumbing leak",
               "Fire or smoke", "Mold", "Sinkhole", "Theft or vandalism", "Commercial property", "Other / not sure"]
STATUS = ["Denied in full", "Partly denied / underpaid", "No decision yet (delayed)", "Insurer demanded appraisal or EUO",
          "Not filed yet"]

TODAY = date.today().isoformat()


def esc(t):
    return htmlmod.escape(str(t), quote=True)


def ver(rel):
    with open(os.path.join(SRC, "static", rel), "rb") as fh:
        return hashlib.sha1(fh.read()).hexdigest()[:10]


def strip_tags(s):
    return re.sub(r"\s+", " ", htmlmod.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


# ---------------------------------------------------------------- schema
def firm_node():
    return {
        "@type": "LegalService",
        "@id": SITE["origin"] + "/#firm",
        "name": FIRM["legal_name"],
        "url": FIRM["site"],
        "telephone": FIRM["phone_href"],
        "logo": SITE["origin"] + "/assets/img/lawgical-logo.png",
        "address": [{"@type": "PostalAddress", "streetAddress": o["street"], "addressLocality": o["city"],
                     "addressRegion": o["region"], "postalCode": o["zip"], "addressCountry": "US"} for o in FIRM["offices"]],
        "areaServed": {"@type": "State", "name": "Florida"},
        "knowsAbout": ["Denied property insurance claims", "Florida property insurance law", "Insurance appraisal",
                       "Civil Remedy Notices", "Pre-suit notice under s. 627.70152, Florida Statutes"],
    }


def schema(page, canonical):
    graph = [
        {"@type": "WebSite", "@id": SITE["origin"] + "/#website", "url": SITE["origin"] + "/", "name": SITE["name"],
         "description": SITE["tagline"], "inLanguage": "en-US", "publisher": {"@id": SITE["origin"] + "/#firm"}},
        firm_node(),
        {"@type": "WebPage", "@id": canonical + "#webpage", "url": canonical, "name": page["title"],
         "description": page["description"], "isPartOf": {"@id": SITE["origin"] + "/#website"},
         "inLanguage": "en-US", "dateModified": TODAY},
    ]
    if page["path"] != "/" and not page["path"].endswith(".html"):
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE["origin"] + "/"},
            {"@type": "ListItem", "position": 2, "name": page.get("crumb", page["title"]), "item": canonical}]})
    if page.get("kind") == "guide":
        graph.append({"@type": "Article", "@id": canonical + "#article", "headline": page["h1"][:110],
                      "description": page["description"], "mainEntityOfPage": {"@id": canonical + "#webpage"},
                      "datePublished": SITE["published"], "dateModified": TODAY,
                      "author": {"@id": SITE["origin"] + "/#firm"}, "publisher": {"@id": SITE["origin"] + "/#firm"},
                      "about": page.get("keyword", "")})
    faqs = re.findall(r'<details class="faq"><summary>(.*?)</summary>(.*?)</details>', page["body"], re.S)
    if faqs:
        graph.append({"@type": "FAQPage", "@id": canonical + "#faq", "mainEntity": [
            {"@type": "Question", "name": strip_tags(q),
             "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in faqs]})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)


# ---------------------------------------------------------------- chrome
def head(page):
    canonical = SITE["origin"] + page["path"]
    robots = "noindex, nofollow" if STAGING else page.get("robots", "index, follow, max-image-preview:large")
    og_type = "article" if page.get("kind") == "guide" else "website"
    return f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(page['title'])}</title>
<meta name="description" content="{esc(page['description'])}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#173326">
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&amp;family=Source+Sans+3:wght@400;600;700&amp;display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={ver('assets/css/site.css')}">
<script type="application/ld+json">
{schema(page, canonical)}
</script>
</head>
<body class="k-{page.get('kind', 'page')}">
<a class="skip" href="#main">Skip to content</a>
"""


SEAL = ('<svg class="seal" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="30" fill="none" stroke="currentColor" stroke-width="2"/>'
        '<circle cx="32" cy="32" r="25" fill="none" stroke="currentColor" stroke-width="1"/>'
        '<text x="32" y="43" text-anchor="middle" font-family="Libre Baskerville, Georgia, serif" font-size="30" fill="currentColor">&#167;</text></svg>')


def masthead(active):
    links = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{l}</a></li>' for l, h in NAV)
    return f"""<div class="topline"><div class="wrap topline-in">
<span>Florida property insurance &middot; statutes, deadlines &amp; remedies</span>
<a href="tel:{FIRM['phone_href']}">Talk to a lawyer: <strong>{FIRM['phone_display']}</strong></a>
</div></div>
<header class="mast">
<div class="wrap mast-in">
<a class="mark" href="/">{SEAL}<span class="mark-txt"><span class="mark-name">Denied Claim Law</span><span class="mark-sub">A Florida reference &middot; {FIRM['legal_name']}</span></span></a>
<div class="mast-act">
<a class="btn btn-brass" href="/free-case-review/">Free case review</a>
<button class="navtoggle" type="button" aria-expanded="false" aria-controls="volnav" data-navtoggle>Index</button>
</div>
</div>
<nav class="volnav" id="volnav" aria-label="Guides"><div class="wrap"><ol>{links}</ol></div></nav>
</header>
<main id="main">
"""


def counsel_band():
    return f"""<section class="counsel">
<div class="wrap counsel-in">
<div>
<p class="kicker">Free case review &middot; No upfront fees</p>
<h2>Read the denial letter with a lawyer</h2>
<p>{FIRM['legal_name']} reviews denied, underpaid and delayed Florida property claims at no cost. The firm is paid only if you recover.</p>
</div>
<div class="counsel-act">
<a class="btn btn-brass btn-lg" href="/free-case-review/">Request a review</a>
<a class="btn btn-line btn-lg" href="tel:{FIRM['phone_href']}">Call {FIRM['phone_display']}</a>
</div>
</div>
</section>
"""


def footer(show_band=True):
    offices = "".join(f"<p><span class='lbl'>{o['label']}</span>{o['street']}<br>{o['city']}, {o['region']} {o['zip']}</p>" for o in FIRM["offices"])
    guides = "".join(f'<li><a href="{h}">{l}</a></li>' for l, h in NAV)
    return f"""</main>
{counsel_band() if show_band else ''}<footer class="foot">
<div class="wrap foot-grid">
<div>
<p class="foot-name">Denied Claim Law</p>
<p>A plain-English reference to Florida property insurance law, published by {FIRM['legal_name']}, a Florida property insurance claims law firm.</p>
<a href="/about-the-firm/"><img src="/assets/img/lawgical-logo-white.png" alt="{FIRM['name']}" width="150" height="56" loading="lazy"></a>
</div>
<div>
<p class="foot-h">Guides</p>
<ul>{guides}</ul>
</div>
<div>
<p class="foot-h">The firm</p>
<p><a class="foot-tel" href="tel:{FIRM['phone_href']}">{FIRM['phone_display']}</a></p>
{offices}
<ul><li><a href="/free-case-review/">Free case review</a></li><li><a href="/about-the-firm/">About the firm</a></li></ul>
</div>
</div>
<div class="wrap">
<p class="foot-legal"><strong>Attorney advertising.</strong> This website is sponsored by {FIRM['legal_name']}, which is responsible for its content. Principal office: Orlando, Florida; additional office in Destin, Florida. Phone {FIRM['phone_display']}.
The material on this site is information only, not legal advice, and reading it or contacting us does not create an attorney-client relationship. Statutes change and every policy is different; deadlines depend on your policy and your date of loss.
No upfront fees; the firm is paid only if you recover, under a written fee agreement that also explains how case costs are handled. The hiring of a lawyer is an important decision that should not be based solely on advertisements. See the full <a href="/disclaimer/">disclaimer</a>.</p>
<p class="foot-bottom"><span>&copy; {date.today().year} {FIRM['legal_name']} &middot; deniedclaimlaw.com</span>
<span><a href="/disclaimer/">Disclaimer</a> &middot; <a href="/privacy-policy/">Privacy</a> &middot; <a href="/sitemap/">Site index</a></span></p>
</div>
</footer>
<div class="callbar"><a href="tel:{FIRM['phone_href']}">Call {FIRM['phone_display']}</a><a href="/free-case-review/" class="callbar-cta">Free review</a></div>
<script src="/assets/js/site.js?v={ver('assets/js/site.js')}" defer></script>
</body>
</html>
"""


# ---------------------------------------------------------------- form
def lead_form(n):
    opts = lambda xs: "".join(f"<option>{esc(x)}</option>" for x in xs)
    return f"""<form class="brief-form" data-lead-form novalidate>
<div class="fgrid">
<div class="fld"><label for="f{n}-name">Full name</label><input id="f{n}-name" name="name" type="text" autocomplete="name" required></div>
<div class="fld"><label for="f{n}-phone">Phone</label><input id="f{n}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="fld"><label for="f{n}-email">Email</label><input id="f{n}-email" name="email" type="email" autocomplete="email"></div>
<div class="fld"><label for="f{n}-loc">Property city or ZIP</label><input id="f{n}-loc" name="location" type="text" autocomplete="postal-code" required></div>
<div class="fld"><label for="f{n}-type">Type of claim</label><select id="f{n}-type" name="claim_type" required>{opts(CLAIM_TYPES)}</select></div>
<div class="fld"><label for="f{n}-status">Where the claim stands</label><select id="f{n}-status" name="status">{opts(STATUS)}</select></div>
<div class="fld wide"><label for="f{n}-msg">Briefly, what happened?</label><textarea id="f{n}-msg" name="message" rows="4" maxlength="3000"></textarea></div>
<input type="text" name="website" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true">
<label class="consent wide"><input type="checkbox" name="consent" value="1" required> I agree that {FIRM['legal_name']} may contact me about this request by phone, text or email. I understand that submitting this form does not create an attorney-client relationship and that I should not send confidential details until the firm agrees to represent me.</label>
</div>
<button class="btn btn-brass btn-block" type="submit">Send for free review</button>
<p class="fnote">Prefer to talk? Call <a href="tel:{FIRM['phone_href']}">{FIRM['phone_display']}</a>. Information only; not legal advice.</p>
<div class="fout" data-lead-out role="status" aria-live="polite"></div>
</form>"""


def statute_url(chapter, section):
    """{{S:627.70131}} -> official Online Sunshine URL for that section of the Florida Statutes."""
    ch = int(chapter)
    lo = ch // 100 * 100
    return ("http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&amp;URL="
            f"{lo:04d}-{lo + 99:04d}/{ch:04d}/Sections/{ch:04d}.{section}.html")


def expand(body):
    for k, v in {"{{PHONE}}": FIRM["phone_display"], "{{TEL}}": FIRM["phone_href"], "{{FIRM}}": FIRM["name"],
                 "{{FIRM_LEGAL}}": FIRM["legal_name"], "{{FIRM_SITE}}": FIRM["site"], "{{REVIEWED}}": SITE["reviewed"]}.items():
        body = body.replace(k, v)
    body = re.sub(r"\{\{S:(\d+)\.(\w+)\}\}", lambda m: statute_url(m.group(1), m.group(2)), body)
    n = 0
    while "{{LEAD_FORM}}" in body:
        n += 1
        body = body.replace("{{LEAD_FORM}}", lead_form(n), 1)
    return body


def guide_wrap(page):
    body = page["body"]
    heads = re.findall(r'<h2 id="([\w-]+)">(.*?)</h2>', body)
    toc = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in heads)
    return f"""<div class="title-block">
<div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> <span aria-hidden="true">&rsaquo;</span> <span>{esc(page.get('crumb', ''))}</span></nav>
<p class="kicker">{esc(page.get('kicker', 'Florida property insurance law'))}</p>
<h1>{page['h1']}</h1>
<p class="dek">{page['dek']}</p>
<p class="reviewed">Last reviewed: {SITE['reviewed']} &middot; Florida Statutes cited to current text at leg.state.fl.us &middot; Information only, not legal advice</p>
</div>
</div>
<div class="wrap guide-grid">
<aside class="toc" aria-label="Contents">
<details class="toc-box" open data-toc><summary>Contents</summary><ol>{toc}</ol></details>
<div class="toc-cta"><p>Denied claim?</p><a href="tel:{FIRM['phone_href']}">{FIRM['phone_display']}</a><a href="/free-case-review/">Free case review &rarr;</a></div>
</aside>
<article class="prose">
{body}
</article>
</div>
"""


# ---------------------------------------------------------------- build
HDR = re.compile(r"^\s*<!--(\{.*?\})-->\s*", re.S)


def load_pages():
    pages = []
    for name in sorted(os.listdir(os.path.join(SRC, "pages"))):
        if not name.endswith(".html"):
            continue
        raw = open(os.path.join(SRC, "pages", name), encoding="utf-8").read()
        m = HDR.match(raw)
        if not m:
            raise SystemExit(f"{name}: missing JSON header")
        meta = json.loads(m.group(1))
        meta["body"] = expand(raw[m.end():])
        pages.append(meta)
    return pages


def out_file(path):
    if path == "/":
        return os.path.join(OUT, "home.html")
    if path.endswith(".html"):
        return os.path.join(OUT, path.lstrip("/"))
    return os.path.join(OUT, path.strip("/"), "index.html")


def site_index(pages):
    groups = {}
    for p in pages:
        if p.get("sitemap") is False:
            continue
        groups.setdefault(p.get("group", "Firm & policies"), []).append(p)
    out = ""
    for g in ["Reference", "Guides", "Firm & policies"]:
        if g in groups:
            items = "".join(f'<li><a href="{p["path"]}">{esc(p.get("crumb") or p["title"].split(" | ")[0])}</a> <span>{esc(p["description"])}</span></li>'
                            for p in groups[g])
            out += f'<h2 id="{g.split()[0].lower()}">{g}</h2><ul class="index-list">{items}</ul>'
    return out


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(SRC, "static"), OUT)
    pages = load_pages()
    for p in pages:
        p["body"] = p["body"].replace("{{SITE_INDEX}}", site_index(pages))
        main_html = guide_wrap(p) if p.get("kind") == "guide" else p["body"]
        doc = head(p) + masthead(p["path"]) + main_html + footer(p.get("band", True))
        f = out_file(p["path"])
        os.makedirs(os.path.dirname(f), exist_ok=True)
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(doc)
    urls = "".join(f"<url><loc>{SITE['origin']}{p['path']}</loc><lastmod>{TODAY}</lastmod></url>\n"
                   for p in pages if p.get("sitemap") is not False)
    with open(os.path.join(OUT, "sitemap.xml"), "w") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                 + urls + "</urlset>\n")
    with open(os.path.join(OUT, "robots.txt"), "w") as fh:
        fh.write("User-agent: *\nDisallow: /\n" if STAGING else
                 f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {SITE['origin']}/sitemap.xml\n")
    print(f"built {len(pages)} pages into public/ (staging={STAGING})")


if __name__ == "__main__":
    main()
