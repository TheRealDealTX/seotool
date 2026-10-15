#!/usr/bin/env python3
"""Build claimhurricanetoday.com into ./public (Python 3 standard library only).

Source pages live in src/pages/*.html. The first line of each file is an HTML
comment holding a JSON object, for example:

    <!--{"path": "/hurricane-claim-checklist/", "kind": "guide", "title": "...",
         "description": "...", "h1": "...", "lede": "...", "crumb": "Checklist"}-->

kind = "home"  -> body is used as-is inside the shell (it carries its own H1)
kind = "guide" -> build adds the navy page head (breadcrumbs, H1, lede,
                  "Last reviewed"), a two-column layout with a sticky sidebar,
                  and Article + FAQPage schema (FAQ read from <details> blocks)
kind = "page"  -> like guide but without Article schema / review stamp

Shortcodes inside bodies: {{LEAD_FORM}}, {{CALC}}, {{PHONE}}, {{TEL}},
{{FIRM_SITE}}, {{SITEMAP}}.

    python3 build.py && python3 validate.py
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

STAGING = False          # True => noindex everywhere + robots.txt Disallow: /
ORIGIN = "https://claimhurricanetoday.com"
SITE_NAME = "Claim Hurricane Today"
REVIEWED = "October 2026"
MODIFIED = "2026-10-15"

FIRM = {
    "legal": "The Lawgical Firm, P.A.",
    "short": "The Lawgical Firm",
    "site": "https://thelawgicalfirm.com/",
    "practice": "https://thelawgicalfirm.com/residential-property-insurance-claims/hurricane-windstorm/",
    "phone": "(407) 433-4131",
    "tel": "+14074334131",
    "offices": [
        {"label": "Principal office", "street": "3191 Maguire Blvd, Ste 160", "city": "Orlando", "zip": "32803"},
        {"label": "Destin office", "street": "34990 Emerald Coast Pkwy, Ste 359", "city": "Destin", "zip": "32541"},
    ],
}

# Short labels on purpose: the exact-match phrase is counted on the homepage and
# should come from the body copy, not from repeated navigation labels.
NAV = [
    ("How to File", "/how-to-file-a-hurricane-claim/"),
    ("Deadlines", "/hurricane-claim-deadline-florida/"),
    ("Checklist", "/hurricane-claim-checklist/"),
    ("Delayed", "/hurricane-claim-delayed/"),
    ("Underpaid", "/hurricane-claim-underpaid/"),
    ("Denied", "/hurricane-claim-denied/"),
]
GUIDES = [
    ("How to file, step by step", "/how-to-file-a-hurricane-claim/"),
    ("Notice deadline calculator", "/hurricane-claim-deadline-florida/"),
    ("Printable claim checklist", "/hurricane-claim-checklist/"),
    ("When the insurer is slow", "/hurricane-claim-delayed/"),
    ("When the payment is too low", "/hurricane-claim-underpaid/"),
    ("When coverage is denied", "/hurricane-claim-denied/"),
    ("Hurricane deductible rules", "/hurricane-deductible-florida/"),
    ("Living expenses while displaced", "/additional-living-expenses-hurricane-claim/"),
]

CLAIM_TYPES = [
    "Hurricane wind damage to my home",
    "Roof damage or roof leak after the storm",
    "Water intrusion / interior damage",
    "My claim is delayed",
    "My claim was underpaid",
    "My claim was denied",
    "Additional living expenses dispute",
    "Commercial property hurricane claim",
    "Something else",
]


def esc(s):
    return html.escape(str(s), quote=True)


def ver(rel):
    with open(os.path.join(SRC, "static", rel), "rb") as fh:
        return hashlib.sha1(fh.read()).hexdigest()[:10]


def strip_tags(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def faq_items(body):
    out = []
    for q, a in re.findall(r"<details>\s*<summary>(.*?)</summary>\s*<div>(.*?)</div>\s*</details>", body, re.S):
        out.append({"@type": "Question", "name": strip_tags(q),
                    "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}})
    return out


def schema(p):
    url = ORIGIN + p["path"]
    firm_id = ORIGIN + "/#firm"
    graph = [
        {"@type": "WebSite", "@id": ORIGIN + "/#website", "url": ORIGIN + "/", "name": SITE_NAME,
         "inLanguage": "en-US", "publisher": {"@id": firm_id}},
        {"@type": "LegalService", "@id": firm_id, "name": FIRM["legal"], "url": FIRM["site"],
         "telephone": FIRM["tel"], "logo": ORIGIN + "/assets/img/lawgical-logo.png",
         "address": [{"@type": "PostalAddress", "streetAddress": o["street"], "addressLocality": o["city"],
                      "addressRegion": "FL", "postalCode": o["zip"], "addressCountry": "US"} for o in FIRM["offices"]],
         "areaServed": {"@type": "State", "name": "Florida"},
         "knowsAbout": ["Hurricane insurance claims", "Windstorm damage claims",
                        "Delayed, underpaid and denied property insurance claims"]},
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": p["title"],
         "description": p["description"], "isPartOf": {"@id": ORIGIN + "/#website"},
         "inLanguage": "en-US", "dateModified": MODIFIED},
    ]
    crumbs = [{"@type": "ListItem", "position": 1, "name": "Home", "item": ORIGIN + "/"}]
    if p["path"] != "/":
        crumbs.append({"@type": "ListItem", "position": 2, "name": p.get("crumb", p["h1"]), "item": url})
    graph.append({"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": crumbs})
    if p.get("kind") == "guide":
        graph.append({"@type": "Article", "@id": url + "#article", "headline": p["h1"],
                      "description": p["description"], "mainEntityOfPage": {"@id": url + "#webpage"},
                      "author": {"@id": firm_id}, "publisher": {"@id": firm_id},
                      "datePublished": MODIFIED, "dateModified": MODIFIED, "inLanguage": "en-US"})
    faqs = faq_items(p["body"])
    if faqs:
        graph.append({"@type": "FAQPage", "@id": url + "#faq", "mainEntity": faqs})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)


def head(p):
    url = ORIGIN + p["path"]
    robots = "noindex, nofollow" if (STAGING or p.get("noindex")) else "index, follow, max-image-preview:large"
    canonical = f'<link rel="canonical" href="{url}">'
    return f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(p['title'])}</title>
<meta name="description" content="{esc(p['description'])}">
{canonical}
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#0a1a33">
<meta property="og:type" content="{'article' if p.get('kind') == 'guide' else 'website'}">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{esc(p['title'])}">
<meta property="og:description" content="{esc(p['description'])}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,700..900&amp;family=Public+Sans:wght@400;600;700&amp;display=swap">
<link rel="stylesheet" href="/assets/css/main.css?v={ver('assets/css/main.css')}">
<script type="application/ld+json">
{schema(p)}
</script>
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
"""


LOGO_SVG = ('<svg class="logo-mark" viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="12" fill="#0a1a33"/>'
            '<path d="M32 12c-9 0-16 4-19 11 6-4 13-5 19-4-7 3-11 8-11 14 0 7 6 12 13 12 9 0 16-4 19-11-6 4-13 5-19 4 7-3 11-8 11-14 0-7-6-12-13-12z" fill="#ea580c"/>'
            '<circle cx="32" cy="32" r="4.5" fill="#fff"/></svg>')


def masthead(active):
    nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{l}</a>' for l, h in NAV)
    drawer = "".join(f'<li><a href="{h}">{l}</a></li>' for l, h in GUIDES)
    return f"""<div class="topline"><div class="wrap">
<span><span class="pulse" aria-hidden="true"></span><strong>Florida hurricane claims:</strong> notice deadlines are short. Check yours.</span>
<a href="/hurricane-claim-deadline-florida/">Deadline calculator</a>
</div></div>
<header class="masthead">
<div class="wrap">
<a class="logo" href="/">{LOGO_SVG}<span class="logo-word">Claim <span>Hurricane</span> Today<small>Florida claim guide &middot; {FIRM['short']}</small></span></a>
<nav class="mainnav" aria-label="Main">{nav}</nav>
<a class="btn btn-go btn-sm callbtn" href="tel:{FIRM['tel']}">Call {FIRM['phone']}</a>
<button class="navtoggle" type="button" data-navtoggle aria-expanded="false" aria-controls="drawer">Menu</button>
</div>
<nav class="drawer" id="drawer" aria-label="Guides"><ul>{drawer}<li><a href="/free-case-review/">Free case review</a></li><li><a href="/about-the-firm/">About the firm</a></li></ul></nav>
</header>
<div class="hazard" aria-hidden="true"></div>
<main id="main">
"""


def ctastrip():
    return f"""<section class="ctastrip" aria-label="Free case review">
<div class="wrap">
<div><h2>Insurer stalling, short-paying or saying no?</h2>
<p>Have the claim reviewed at no cost by {FIRM['legal']}. No upfront fees.</p></div>
<div class="acts"><a class="btn btn-navy" href="/free-case-review/">Start free review</a><a class="btn btn-light" href="tel:{FIRM['tel']}">{FIRM['phone']}</a></div>
</div>
</section>
"""


def footer(cta=True):
    guides = "".join(f'<li><a href="{h}">{l}</a></li>' for l, h in GUIDES)
    return f"""</main>
{ctastrip() if cta else ''}<footer class="foot">
<div class="wrap">
<div class="foot-grid">
<div>
<h2>{SITE_NAME}</h2>
<p>A plain-English, Florida-specific guide to reporting and pursuing a hurricane insurance claim, published by {FIRM['legal']}, a Florida property insurance claims law firm.</p>
<p><img src="/assets/img/lawgical-logo-white.png" alt="{FIRM['short']}" width="150" height="56" loading="lazy"></p>
</div>
<div>
<h2>Guides</h2>
<ul>{guides}</ul>
</div>
<div>
<h2>Contact</h2>
<ul>
<li><a href="tel:{FIRM['tel']}">{FIRM['phone']}</a></li>
<li><a href="/free-case-review/">Free case review</a></li>
<li><a href="/about-the-firm/">About the firm</a></li>
<li><a href="/disclaimer/">Disclaimer</a></li>
<li><a href="/privacy-policy/">Privacy policy</a></li>
<li><a href="/sitemap/">Site map</a></li>
</ul>
</div>
</div>
<div class="adv">
<p><strong>Attorney advertising.</strong> This website is an advertisement for {FIRM['legal']}. Principal office: {FIRM['offices'][0]['street']}, Orlando, FL {FIRM['offices'][0]['zip']}. Destin office: {FIRM['offices'][1]['street']}, Destin, FL {FIRM['offices'][1]['zip']}. Phone <a href="tel:{FIRM['tel']}">{FIRM['phone']}</a>. Firm website: <a href="{FIRM['site']}" rel="noopener">thelawgicalfirm.com</a>.</p>
<p>The information on this site is for general information only and is not legal advice. Contacting us does not create an attorney-client relationship. The hiring of a lawyer is an important decision that should not be based solely upon advertisements. Read the full <a href="/disclaimer/">disclaimer</a>.</p>
<p>&copy; 2026 {FIRM['legal']}</p>
</div>
</div>
</footer>
<div class="stickycall"><a class="c1" href="tel:{FIRM['tel']}">Call now</a><a class="c2" href="/free-case-review/">Free review</a></div>
<script src="/assets/js/main.js?v={ver('assets/js/main.js')}" defer></script>
</body>
</html>
"""


def lead_form(n):
    opts = '<option value="">Choose one</option>' + "".join(f"<option>{esc(t)}</option>" for t in CLAIM_TYPES)
    i = f"lf{n}"
    return f"""<form class="leadbox" data-lead novalidate>
<h2 id="{i}-h">Free hurricane claim review</h2>
<p class="note">Tell us what happened. A member of the {FIRM['short']} team will contact you.</p>
<div class="lf">
<div><label for="{i}-name">Full name</label><input id="{i}-name" name="name" type="text" autocomplete="name" required></div>
<div><label for="{i}-phone">Phone</label><input id="{i}-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required></div>
<div><label for="{i}-email">Email</label><input id="{i}-email" name="email" type="email" autocomplete="email"></div>
<div><label for="{i}-loc">Property city or ZIP</label><input id="{i}-loc" name="location" type="text" autocomplete="postal-code" required></div>
<div class="full"><label for="{i}-type">Claim type</label><select id="{i}-type" name="claim_type" required>{opts}</select></div>
<div class="full"><label for="{i}-det">Briefly, what happened? (storm, date of loss, insurer, where things stand)</label><textarea id="{i}-det" name="details" maxlength="3000"></textarea></div>
<div class="hp" aria-hidden="true"><label for="{i}-co">Company</label><input id="{i}-co" name="company" type="text" tabindex="-1" autocomplete="off"></div>
<label class="consent full"><input type="checkbox" name="consent" value="1" required><span>I agree to be contacted about my inquiry by phone, text or email. I understand that submitting this form does not create an attorney-client relationship and that I should not send confidential information until one exists.</span></label>
<div class="full"><button class="btn btn-go" type="submit">Request my free review</button></div>
<p class="lf-status full" data-lead-status role="status" aria-live="polite"></p>
</div>
<p class="formnote">Prefer the phone? Call <a href="tel:{FIRM['tel']}">{FIRM['phone']}</a>. {FIRM['legal']} &middot; Orlando and Destin, Florida.</p>
</form>"""


def calc(n):
    return f"""<form class="calc" data-calc aria-labelledby="calc{n}-h">
<h2 id="calc{n}-h">Hurricane claim deadline countdown</h2>
<p>Enter the landfall date. We count the Florida notice windows in s. 627.70132 for you.</p>
<label for="calc{n}-dol">Date of loss (hurricane landfall)</label>
<input id="calc{n}-dol" name="dol" type="date" required>
<label for="calc{n}-rep">Date you reported the claim (optional)</label>
<input id="calc{n}-rep" name="reported" type="date">
<button class="btn btn-go" type="submit">Show my deadlines</button>
<div class="calc-out" data-calc-out role="status" aria-live="polite" hidden></div>
<p class="calc-fine">Estimate only, not legal advice. Deadlines depend on your policy, your date of loss and the law in effect for that loss; insurer timelines can be tolled or extended. Do not wait for the last day. <a href="/hurricane-claim-deadline-florida/">How these dates are counted</a>.</p>
</form>"""


def sidebar(p):
    links = "".join(f'<li><a href="{h}">{l}</a></li>' for l, h in GUIDES if h != p["path"])
    return f"""<aside class="sidebar" aria-label="Related">
<div class="sidecard sidecard-cta">
<h2>Talk to a claims lawyer</h2>
<p>Free review of your hurricane claim, policy and the insurer's estimate. No upfront fees.</p>
<a class="btn btn-go" href="tel:{FIRM['tel']}">Call {FIRM['phone']}</a>
<a class="btn btn-line" href="/free-case-review/">Online review form</a>
</div>
<div class="sidecard">
<h2>More claim guides</h2>
<ul>{links}</ul>
</div>
</aside>"""


def wrap_guide(p):
    reviewed = f'<span class="reviewed">Last reviewed: {REVIEWED}</span>' if p.get("kind") == "guide" else ""
    lede = f'<p class="lede">{p["lede"]}</p>' if p.get("lede") else ""
    side = sidebar(p) if p.get("sidebar", True) else ""
    layout_cls = "layout" if side else "layout layout-full"
    return f"""<div class="pagehead"><div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <span aria-current="page">{esc(p.get('crumb', p['h1']))}</span></nav>
<h1>{p['h1']}</h1>
{lede}
{reviewed}
</div></div>
<div class="wrap {layout_cls}">
<article class="prose">
{p['body']}
</article>
{side}
</div>
"""


def expand(body, pages):
    n = {"lead": 0, "calc": 0}

    def lead(_):
        n["lead"] += 1
        return lead_form(n["lead"])

    def cal(_):
        n["calc"] += 1
        return calc(n["calc"])

    body = re.sub(r"\{\{LEAD_FORM\}\}", lead, body)
    body = re.sub(r"\{\{CALC\}\}", cal, body)
    body = body.replace("{{PHONE}}", FIRM["phone"]).replace("{{TEL}}", FIRM["tel"])
    body = body.replace("{{FIRM_SITE}}", FIRM["site"]).replace("{{FIRM_PRACTICE}}", FIRM["practice"])
    if "{{SITEMAP}}" in body:
        items = "".join(f'<li><a href="{q["path"]}">{esc(q.get("crumb", q.get("h1", q["title"])))}</a></li>'
                        for q in pages if q.get("sitemap", True))
        body = body.replace("{{SITEMAP}}", f'<ul class="sitemap-cols">{items}</ul>')
    return body


HEADER = re.compile(r"\A\s*<!--(\{.*?\})-->\s*", re.S)


def load():
    pages = []
    for name in sorted(os.listdir(os.path.join(SRC, "pages"))):
        if not name.endswith(".html"):
            continue
        raw = open(os.path.join(SRC, "pages", name), encoding="utf-8").read()
        m = HEADER.match(raw)
        if not m:
            raise SystemExit(f"{name}: first line must be a JSON header comment")
        meta = json.loads(m.group(1))
        meta["body"] = raw[m.end():]
        meta["file"] = name
        pages.append(meta)
    return pages


def target(path):
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
        p["body"] = expand(p["body"], pages)
        main_html = p["body"] if p.get("kind") == "home" else wrap_guide(p)
        doc = head(p) + masthead(p.get("nav", p["path"])) + main_html + footer(cta=p.get("cta", True))
        f = target(p["path"])
        os.makedirs(os.path.dirname(f), exist_ok=True)
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(doc)
    indexable = [p for p in pages if p.get("sitemap", True)]
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for p in indexable:
            fh.write(f"<url><loc>{ORIGIN}{p['path']}</loc><lastmod>{MODIFIED}</lastmod></url>\n")
        fh.write("</urlset>\n")
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as fh:
        if STAGING:
            fh.write("User-agent: *\nDisallow: /\n")
        else:
            fh.write(f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {ORIGIN}/sitemap.xml\n")
    print(f"built {len(pages)} pages -> public/ (staging={STAGING})")


if __name__ == "__main__":
    main()
