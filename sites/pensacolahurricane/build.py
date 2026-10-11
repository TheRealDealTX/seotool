#!/usr/bin/env python3
"""Static site generator for pensacolahurricane.com.

Each page body lives in src/pages/*.html and starts with a one-line JSON
header in an HTML comment:

    <!--{"path": "/weather/", "title": "...", "description": "...", "nav": "/weather/"}-->

build.py wraps every body in the shared layout and writes the finished site
to public/, together with everything under src/static/ (CSS, JS, PHP APIs).

    python3 build.py            # writes ./public
"""

import json
import os
import re
import shutil
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "public")

# Live on destinhurricane.com (2026-10-11). Set STAGING back to True to make
# every page noindex and block crawlers in robots.txt (e.g. on a test domain).
STAGING = False

SITE = {
    "name": "Pensacola Hurricane",
    "origin": "https://destinhurricane.com",
    "tagline": "Hurricane tracking, preparedness and recovery for Pensacola, Florida",
    "lat": 30.4213,
    "lon": -87.2169,
}

# The law firm this site advertises. Florida Bar Rule 4-7.12 requires every
# advertisement to name the responsible firm and the city of an office; those
# disclosures render in the footer, the CTA band and the lead form from here.
FIRM = {
    "name": "The Lawgical Firm",
    "legal_name": "The Lawgical Firm, P.A.",
    "site": "https://thelawgicalfirm.com/",
    "url": "https://thelawgicalfirm.com/residential-property-insurance-claims/hurricane-windstorm/",
    "phone_display": "(407) 433-4131",
    "phone_href": "+14074334131",
    "street": "3191 Maguire Blvd, Ste 160",
    "city": "Orlando",
    "region": "FL",
    "zip": "32803",
}

NAV = [
    ("Denied Claims", "/denied-hurricane-claim/"),
    ("Underpaid Claims", "/underpaid-hurricane-claim/"),
    ("Delayed Claims", "/delayed-hurricane-claim/"),
    ("Claim Help", "/insurance-claims/"),
    ("Hurricane Isaias", "/hurricane-isaias-claims/"),
    ("Our Attorneys", "/the-lawgical-firm/"),
    ("Storm Center", "/hurricane-tracker/"),
]

TODAY = date.today().isoformat()


def asset_version(rel):
    """Short content hash so a changed CSS/JS file gets a new URL (CDN and browser caches)."""
    import hashlib
    with open(os.path.join(SRC, "static", rel), "rb") as fh:
        return hashlib.sha1(fh.read()).hexdigest()[:10]


def esc(text):
    return (str(text).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def head(page):
    canonical = SITE["origin"] + page["path"]
    robots = "noindex, nofollow" if STAGING else page.get("robots", "index, follow, max-image-preview:large")
    schema = page.get("schema")
    graph = [
        {
            "@type": "WebSite",
            "@id": SITE["origin"] + "/#website",
            "url": SITE["origin"] + "/",
            "name": SITE["name"],
            "description": SITE["tagline"],
            "inLanguage": "en-US",
            "publisher": {"@id": SITE["origin"] + "/#firm"},
        },
        {
            "@type": "LegalService",
            "@id": SITE["origin"] + "/#firm",
            "name": FIRM["legal_name"],
            "url": FIRM["site"],
            "telephone": FIRM["phone_href"],
            "address": {"@type": "PostalAddress", "streetAddress": FIRM["street"], "addressLocality": FIRM["city"],
                        "addressRegion": FIRM["region"], "postalCode": FIRM["zip"], "addressCountry": "US"},
            "areaServed": [{"@type": "City", "name": "Pensacola, FL"}, {"@type": "AdministrativeArea", "name": "Escambia County, FL"},
                           {"@type": "AdministrativeArea", "name": "Santa Rosa County, FL"}, {"@type": "State", "name": "Florida"}],
            "knowsAbout": ["Hurricane insurance claims", "Denied property insurance claims", "Underpaid insurance claims", "Windstorm damage claims"],
        },
        {
            "@type": "WebPage",
            "@id": canonical + "#webpage",
            "url": canonical,
            "name": page["title"],
            "description": page["description"],
            "isPartOf": {"@id": SITE["origin"] + "/#website"},
            "about": {"@type": "Place", "name": "Pensacola, Florida",
                      "geo": {"@type": "GeoCoordinates", "latitude": SITE["lat"], "longitude": SITE["lon"]}},
            "dateModified": page.get("modified", TODAY),
        },
    ]
    if page["path"] != "/" and not page["path"].endswith(".html"):
        crumbs = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE["origin"] + "/"}]
        parts = [p for p in page["path"].strip("/").split("/") if p]
        for i, _ in enumerate(parts):
            sub = "/" + "/".join(parts[: i + 1]) + "/"
            name = page["title"].split(" | ")[0] if i == len(parts) - 1 else page.get("parent_name", parts[i].replace("-", " ").title())
            crumbs.append({"@type": "ListItem", "position": i + 2, "name": name, "item": SITE["origin"] + sub})
        graph.append({"@type": "BreadcrumbList", "itemListElement": crumbs})
    if schema:
        graph.extend(schema)
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    og_type = page.get("og_type", "website")
    article = ""
    if page.get("published"):
        article = (f'<meta property="article:published_time" content="{page["published"]}">\n'
                   f'<meta property="article:modified_time" content="{page.get("modified", page["published"])}">\n')
    return f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(page['title'])}</title>
<meta name="description" content="{esc(page['description'])}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#000046">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:title" content="{esc(page['title'])}">
<meta property="og:description" content="{esc(page['description'])}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE['origin']}/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
{article}<meta name="geo.region" content="US-FL">
<meta name="geo.placename" content="Pensacola, Florida">
<meta name="geo.position" content="{SITE['lat']};{SITE['lon']}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800;900&amp;family=Inter:wght@400;500;600;700&amp;display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={asset_version("assets/css/site.css")}">
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
<a class="skip-link" href="#content">Skip to content</a>
"""


def header(active):
    links = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if href == active else ""}>{label}</a>'
        for label, href in NAV
    )
    return f"""<div class="alertbar" data-alertbar role="status" aria-live="polite">
<div class="container alertbar-inner">
<span class="alertbar-dot" aria-hidden="true"></span>
<span class="alertbar-text" data-alertbar-text>Checking National Weather Service alerts for Pensacola&hellip;</span>
<a class="alertbar-link" href="/free-case-review/">Storm damage? Free claim review &rarr;</a>
</div>
</div>
<header class="site-header">
<div class="container nav-wrap">
<a class="brand" href="/" aria-label="Pensacola Hurricane home">
<svg class="brand-mark" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="23" fill="#c58911"/><path d="M24 9c-6 0-11 3-13 8 4-3 9-4 13-3-5 2-8 6-8 10 0 5 4 9 9 9 6 0 11-3 13-8-4 3-9 4-13 3 5-2 8-6 8-10 0-5-4-9-9-9z" fill="#fff"/><circle cx="24" cy="24" r="3.2" fill="#01017c"/></svg>
<span class="brand-copy"><strong>Pensacola Hurricane</strong><span>Storm claim help &middot; {FIRM['name']}</span></span>
</a>
<a class="firm-badge" href="/the-lawgical-firm/" aria-label="Sponsored by {FIRM['legal_name']}"><span>Sponsored by</span><img src="/assets/img/lawgical-logo-white.png" alt="{FIRM['name']}" width="110" height="41"></a>
<div class="nav-actions">
<a class="nav-phone" href="tel:{FIRM['phone_href']}" aria-label="Call {FIRM['name']} at {FIRM['phone_display']}"><span class="nav-phone-label">Free review</span>{FIRM['phone_display']}</a>
<a class="btn btn-warn nav-cta" href="/free-case-review/">Free Case Review</a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="primary-nav" data-menu-btn>
<span class="menu-icon" aria-hidden="true"><span></span><span></span><span></span></span><span class="menu-label">Menu</span>
</button>
</div>
</div>
<div class="scroll-progress" aria-hidden="true"><span data-scroll-progress></span></div>
<nav class="nav-row" id="primary-nav" aria-label="Primary"><div class="container">
<div class="nav-links">{links}</div>
<div class="nav-drawer-cta">
<a class="btn btn-warn" href="/free-case-review/">Free Case Review</a>
<a class="btn btn-outline-light" href="tel:{FIRM['phone_href']}">Call {FIRM['phone_display']}</a>
<img class="drawer-logo" src="/assets/img/lawgical-logo-white.png" alt="{FIRM['name']}" width="132" height="49" loading="lazy">
<p>No upfront fees &middot; {FIRM['legal_name']}</p>
</div>
</div></nav>
</header>
<div class="nav-backdrop" data-nav-backdrop hidden></div>
<main id="content">
"""


def cta_band():
    return f"""<section class="claim-cta">
<div class="container claim-cta-inner">
<div>
<div class="eyebrow" style="color:#f3c35a">Free case review &middot; No upfront fees</div>
<h2>Hurricane claim denied, delayed or underpaid?</h2>
<p>Talk to the attorneys at {FIRM['name']} about your Pensacola-area hurricane claim. We review your policy and the insurer's estimate at no cost, and you pay no attorney fee unless there is a recovery.</p>
</div>
<div class="claim-cta-actions">
<a class="btn btn-warn btn-lg" href="/free-case-review/">Start my free case review</a>
<a class="btn btn-ghost btn-lg" href="tel:{FIRM['phone_href']}">Call {FIRM['phone_display']}</a>
</div>
</div>
</section>
"""


def footer(show_cta=True):
    return f"""</main>
{cta_band() if show_cta else ""}<footer class="site-footer">
<div class="container">
<div class="footer-grid">
<div class="footer-about">
<a class="brand brand-footer" href="/"><strong>Pensacola Hurricane</strong></a>
<p>Hurricane claim help for Pensacola, Pensacola Beach, Perdido Key, Gulf Breeze, Warrington, Milton, Pace,
Navarre and all of Escambia and Santa Rosa counties, sponsored by <a href="{FIRM['site']}" target="_blank" rel="noopener">{FIRM['legal_name']}</a>,
a Florida property insurance claims law firm.</p>
<a class="footer-logo" href="/the-lawgical-firm/"><img src="/assets/img/lawgical-logo-white.png" alt="{FIRM['name']}" width="165" height="62" loading="lazy"></a>
<p class="footer-firm"><strong>{FIRM['legal_name']}</strong><br>{FIRM['street']}<br>{FIRM['city']}, {FIRM['region']} {FIRM['zip']}<br>
<a href="tel:{FIRM['phone_href']}">{FIRM['phone_display']}</a><br><span class="small">Representing property owners throughout Florida, including the Pensacola area.</span></p>
</div>
<div>
<div class="footer-title">Claim Help</div>
<div class="footer-links">
<a href="/free-case-review/">Free Case Review</a>
<a href="/denied-hurricane-claim/">Denied Hurricane Claims</a>
<a href="/underpaid-hurricane-claim/">Underpaid Hurricane Claims</a>
<a href="/delayed-hurricane-claim/">Delayed Hurricane Claims</a>
<a href="/insurance-claims/">Roof, Water &amp; Wind Claims</a>
<a href="/hurricane-isaias-claims/">Hurricane Isaias Claims</a>
<a href="/the-lawgical-firm/">Our Attorneys</a>
</div>
</div>
<div>
<div class="footer-title">Storm Resources</div>
<div class="footer-links">
<a href="/hurricane-tracker/">Live Hurricane Tracker</a>
<a href="/weather/">Pensacola Weather</a>
<a href="/evacuation-zones/">Evacuation Zone Checker</a>
<a href="/tools/">Deductible &amp; Damage Tools</a>
<a href="/recovery/">Recovery Resources</a>
<a href="/hurricane-history/">Hurricane History</a>
<a href="/news/">Hurricane News</a>
</div>
</div>
<div>
<div class="footer-title">Communities</div>
<div class="footer-links">
<a href="/communities/pensacola-beach/">Pensacola Beach</a>
<a href="/communities/perdido-key/">Perdido Key</a>
<a href="/communities/gulf-breeze/">Gulf Breeze</a>
<a href="/communities/warrington/">Warrington</a>
<a href="/communities/milton/">Milton</a>
<a href="/communities/navarre/">Navarre</a>
<a href="/communities/pace/">Pace</a>
<a href="/communities/downtown-pensacola/">Downtown Pensacola</a>
</div>
</div>
</div>
<p class="footer-legal">Attorney advertising. This website is sponsored by {FIRM['legal_name']}, which is responsible for its content; principal office: {FIRM['city']}, Florida.
The information on this site is general information, not legal advice, and reading it or contacting us does not create an attorney-client relationship.
Fees: no attorney fee unless there is a recovery; ask how case costs are handled under the written fee agreement. Past results do not guarantee a similar outcome. The hiring of a lawyer is an important decision that should not be based solely on advertisements.
In a life-threatening emergency, call 911 and follow instructions from Escambia County and Santa Rosa County officials.</p>
<div class="footer-bottom">
<span>&copy; {date.today().year} Pensacola Hurricane &middot; {FIRM['legal_name']}</span>
<span><a href="/about/">About</a> &middot; <a href="/disclaimer/">Disclaimer</a> &middot; <a href="/privacy-policy/">Privacy</a> &middot; <a href="/sitemap/">Sitemap</a></span>
</div>
</div>
</footer>
<a class="to-top" href="#content" aria-label="Back to top" data-to-top>&uarr;</a>
<div class="call-bar" aria-label="Contact {FIRM['name']}">
<a href="tel:{FIRM['phone_href']}">Call {FIRM['phone_display']}</a>
<a href="/free-case-review/" class="call-bar-cta">Free Case Review</a>
</div>
<script src="/assets/js/site.js?v={asset_version("assets/js/site.js")}" defer></script>
</body>
</html>
"""


ISSUES = ["My claim was denied", "My claim was underpaid / offer is too low", "My claim is delayed / no response",
          "I haven't filed yet", "Partial denial (e.g. roof or flood)", "Something else"]
STORMS = ["Hurricane Isaias (2026)", "Hurricane Sally (2020)", "Another storm / not sure"]


def lead_form(n, compact=False):
    """Free case review form; posts to /api/lead.php. n keeps element ids unique per page."""
    opts = lambda xs: "".join(f"<option>{esc(x)}</option>" for x in xs)
    msg = "" if compact else (f'<div class="field full"><label for="lf{n}-msg">What happened? (optional)</label>'
                              f'<textarea id="lf{n}-msg" name="message" rows="3" placeholder="Roof damage from Isaias; insurer offered $3,200 but the roofer estimate is $21,000&hellip;"></textarea></div>'
                              f'<div class="field"><label for="lf{n}-ins">Insurance company (optional)</label><input id="lf{n}-ins" name="insurer" type="text"></div>')
    return f"""<form class="lead-form" data-lead-form>
<div class="form-grid">
<div class="field"><label for="lf{n}-name">Name</label><input id="lf{n}-name" name="name" type="text" autocomplete="name" required></div>
<div class="field"><label for="lf{n}-phone">Phone</label><input id="lf{n}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="field{" full" if compact else ""}"><label for="lf{n}-email">Email</label><input id="lf{n}-email" name="email" type="email" autocomplete="email"></div>
<div class="field{" full" if compact else ""}"><label for="lf{n}-zip">Property ZIP or city</label><input id="lf{n}-zip" name="location" type="text" autocomplete="postal-code" placeholder="32561 / Pensacola Beach" required></div>
<div class="field full"><label for="lf{n}-issue">What's going on with your claim?</label><select id="lf{n}-issue" name="issue" required>{opts(ISSUES)}</select></div>
<div class="field{" full" if compact else ""}"><label for="lf{n}-storm">Storm</label><select id="lf{n}-storm" name="storm">{opts(STORMS)}</select></div>
{msg}
<input type="text" name="website" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true">
<label class="check full small"><input type="checkbox" name="sms_consent" value="1"> I agree to receive text messages from {FIRM['legal_name']} about my inquiry. Msg &amp; data rates may apply; reply STOP to opt out.</label>
</div>
<button class="btn btn-warn btn-block" type="submit">Get my free case review</button>
<div class="lead-firm"><img src="/assets/img/lawgical-logo.png" alt="{FIRM['name']}" width="118" height="42" loading="lazy"><span>Your review is handled by the attorneys at {FIRM['legal_name']}</span></div>
<p class="form-note">Free and confidential. Submitting this form does not create an attorney-client relationship. Prefer to talk? Call <a href="tel:{FIRM['phone_href']}">{FIRM['phone_display']}</a>.</p>
<div class="lead-out" data-lead-out role="status" aria-live="polite"></div>
</form>"""


def expand(body):
    """Small shortcodes so pages stay readable."""
    body = body.replace("{{FIRM_URL}}", FIRM["url"])
    body = body.replace("{{FIRM_NAME}}", FIRM["name"])
    body = body.replace("{{FIRM_PHONE}}", FIRM["phone_display"])
    body = body.replace("{{FIRM_TEL}}", FIRM["phone_href"])
    body = body.replace("{{TODAY}}", TODAY)
    body = body.replace("{{FIRM_LEGAL}}", FIRM["legal_name"])
    body = body.replace("{{FIRM_SITE}}", FIRM["site"])
    n = 0
    while "{{LEAD_FORM" in body:
        n += 1
        compact = body.find("{{LEAD_FORM_COMPACT}}")
        full = body.find("{{LEAD_FORM}}")
        if compact != -1 and (full == -1 or compact < full):
            body = body.replace("{{LEAD_FORM_COMPACT}}", lead_form(n, compact=True), 1)
        else:
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
            raise SystemExit(f"{name}: missing JSON header comment")
        meta = json.loads(m.group(1))
        meta["body"] = expand(raw[m.end():])
        meta["source"] = name
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
        groups.setdefault(p.get("group", "Pages"), []).append(p)
    order = ["Main", "Tools", "Communities", "News", "Pages"]
    html = ""
    for g in order:
        if g not in groups:
            continue
        items = "".join(f'<li><a href="{p["path"]}">{esc(p["title"].split(" | ")[0])}</a></li>'
                        for p in sorted(groups[g], key=lambda x: x["path"]))
        html += f"<h2>{g}</h2><ul class=\"sitemap-list\">{items}</ul>"
    return html


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(SRC, "static"), OUT)
    pages = load_pages()
    for p in pages:
        body = p["body"].replace("{{SITEMAP}}", sitemap_html(pages))
        html = head(p) + header(p.get("nav")) + body + footer(show_cta=p.get("cta", True))
        f = out_file(p["path"])
        os.makedirs(os.path.dirname(f), exist_ok=True)
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(html)
    urls = "".join(
        f"<url><loc>{SITE['origin']}{p['path']}</loc><lastmod>{p.get('modified', TODAY)}</lastmod></url>\n"
        for p in pages if p.get("sitemap") is not False
    )
    with open(os.path.join(OUT, "sitemap.xml"), "w") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    with open(os.path.join(OUT, "robots.txt"), "w") as fh:
        if STAGING:
            fh.write("# Staging (temporary domain) - do not index\nUser-agent: *\nDisallow: /\n")
        else:
            fh.write(f"User-agent: *\nDisallow: /api/\n\nSitemap: {SITE['origin']}/sitemap.xml\n")
    print(f"built {len(pages)} pages into {os.path.relpath(OUT, ROOT)}/ (staging={STAGING})")


if __name__ == "__main__":
    main()
