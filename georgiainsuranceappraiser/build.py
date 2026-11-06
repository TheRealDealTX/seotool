#!/usr/bin/env python3
"""Static site generator for georgiainsuranceappraiser.com.

python3 build.py   -> writes the complete site into ./public
No dependencies beyond the Python 3 standard library.
"""
import html
import json
import os
import shutil
import sys
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "src"))

from services import SERVICES  # noqa: E402
from locations import LOCATIONS  # noqa: E402
from learn import PROCESS_BODY, FAQ, GLOSSARY, POSTS  # noqa: E402
from tools import TOOLS, GAP_MINI  # noqa: E402

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")

BRAND = "Georgia Insurance Appraiser"
DOMAIN = "https://georgiainsuranceappraiser.com"
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@georgiainsuranceappraiser.com"
TODAY = date.today().isoformat()
VER = "20261106b"

SVC_BASE = "/appraisal-services/"
LOC_BASE = "/locations/"
TOOL_BASE = "/claim-tools/"
POST_BASE = "/insights/"

e = html.escape
pages = []  # (path, priority) for sitemap


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}-ga/"


def loc_label(l):
    return f"{l['city']}, GA"


LOC_BY = {l["slug"]: l for l in LOCATIONS}

MARK = ('<svg viewBox="0 0 48 48" aria-hidden="true"><rect x="1.5" y="1.5" width="45" height="45" fill="#1d4636" stroke="#12211b" stroke-width="3"/>'
        '<circle cx="24" cy="21" r="11" fill="#f0956b"/><path d="M24 10c3 -4 7 -5 10 -4c-2 3 -5 5 -10 4z" fill="#6f8f5f"/>'
        '<rect x="8" y="33" width="32" height="3" fill="#f6f1e6"/><rect x="8" y="39" width="20" height="3" fill="#f7c3a6"/>'
        '<path d="M19 21l4 4 7-8" fill="none" stroke="#12211b" stroke-width="3" stroke-linecap="square"/></svg>')


# ---------------------------------------------------------------- schema
def org_schema():
    return {
        "@type": "ProfessionalService",
        "@id": DOMAIN + "/#business",
        "name": BRAND,
        "url": DOMAIN + "/",
        "telephone": PHONE_INTL,
        "email": EMAIL,
        "logo": DOMAIN + "/assets/img/mark.svg",
        "image": DOMAIN + "/assets/img/og-image.png",
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims throughout Georgia.",
        "areaServed": [{"@type": "State", "name": "Georgia"}] + [{"@type": "City", "name": l["city"].split(" &")[0]} for l in LOCATIONS],
        "priceRange": "$$",
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Property claim valuation", "Xactimate estimating", "Hail damage", "Hurricane claims"],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "18:00"}],
    }


def site_schema():
    return {"@type": "WebSite", "@id": DOMAIN + "/#website", "url": DOMAIN + "/", "name": BRAND, "publisher": {"@id": DOMAIN + "/#business"}, "inLanguage": "en-US"}


def crumbs_schema(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": DOMAIN + p} for i, (n, p) in enumerate(trail)]}


def faq_schema(faqs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


# ---------------------------------------------------------------- layout
def nav():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES)
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS)
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<nav class="nav" id="nav" aria-label="Main">
<ul>
<li><button type="button" data-drop aria-expanded="false">Services<span class="chev">▼</span></button><ul class="drop cols">{svc}<li><a class="all" href="{SVC_BASE}">All appraisal services →</a></li></ul></li>
<li><button type="button" data-drop aria-expanded="false">Locations<span class="chev">▼</span></button><ul class="drop cols">{loc}<li><a class="all" href="{LOC_BASE}">Statewide coverage →</a></li></ul></li>
<li><button type="button" data-drop aria-expanded="false">Claim Tools<span class="chev">▼</span></button><ul class="drop">{tl}<li><a class="all" href="{TOOL_BASE}">All free tools →</a></li></ul></li>
<li><button type="button" data-drop aria-expanded="false">Learn<span class="chev">▼</span></button><ul class="drop"><li><a href="/how-appraisal-works/">How appraisal works</a></li><li><a href="/appraisal-faq/">Appraisal FAQ</a></li><li><a href="/claim-glossary/">Claim glossary</a></li><li><a href="{POST_BASE}">Insights &amp; guides</a></li></ul></li>
<li><a href="/about/">About</a></li>
<li><a href="/contact/">Contact</a></li>
</ul>
<a class="btn peach head-cta-m" href="tel:{TEL}">Call {PHONE}</a>
</nav>"""


def header():
    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="strip"><div class="wrap"><span><i class="dot"></i>Independent property claim appraisal · All 159 Georgia counties</span>
<div class="strip-r"><a class="hide-s" href="mailto:{EMAIL}">{EMAIL}</a><a href="tel:{TEL}">{PHONE_INTL}</a></div></div></div>
<header class="head"><div class="wrap">
<a class="brand" href="/" aria-label="{BRAND} home">{MARK}<span><b>{BRAND}</b><small>Claim valuation · Appraisal · Umpire</small></span></a>
{nav()}
<a class="btn head-cta" href="tel:{TEL}">Talk to an appraiser</a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="nav" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:6])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS[:8])
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="foot"><div class="wrap">
<div class="foot-top">
<div><a class="brand" href="/">{MARK}<span><b>{BRAND}</b><small>Claim valuation · Appraisal · Umpire</small></span></a>
<p>Independent appraisal and estimating support for property owners with disputed insurance claims, from the North Georgia mountains to the Golden Isles.</p>
<div class="foot-contact"><a href="tel:{TEL}">{PHONE_INTL}</a><a href="mailto:{EMAIL}">{EMAIL}</a><span>Mon–Fri 8am–6pm ET · Statewide</span></div></div>
<div><h4>Services</h4><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h4>Locations</h4><ul>{loc}<li><a href="{LOC_BASE}">All Georgia</a></li></ul></div>
<div><h4>Free tools</h4><ul>{tl}</ul></div>
<div><h4>Company</h4><ul><li><a href="/about/">About</a></li><li><a href="/how-appraisal-works/">How appraisal works</a></li><li><a href="/appraisal-faq/">FAQ</a></li><li><a href="/claim-glossary/">Glossary</a></li><li><a href="{POST_BASE}">Insights</a></li><li><a href="/contact/">Contact</a></li></ul></div>
</div>
<div class="foot-bottom"><span>© <span data-year>{date.today().year}</span> {BRAND}. All rights reserved.</span>
<ul><li><a href="/privacy-policy/">Privacy</a></li><li><a href="/terms-of-use/">Terms</a></li><li><a href="/disclaimer/">Disclaimer</a></li><li><a href="/site-map/">Site map</a></li></ul></div>
<p class="foot-disc">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not provide legal advice and are not acting as a public adjuster. Information on this site is general and educational; policy terms vary. Results depend on the facts of each claim and are never guaranteed.</p>
</div></footer>
<div class="mobile-call"><a href="tel:{TEL}">Call now</a><a href="/contact/">Send claim details</a></div>"""


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow"):
    canonical = DOMAIN + path
    graph = [org_schema(), site_schema()] + (schema or [])
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    return f"""<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{DOMAIN}/assets/img/og-image.png">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1d4636">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32x32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,500&family=Instrument+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600;700&display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v={VER}">
<script type="application/ld+json">{ld}</script>
</head>
<body>
{header()}
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/js/app.js?v={VER}" defer></script>
</body>
</html>
"""


def write(path, content, priority=0.6, sitemap=True):
    rel = "home.html" if path == "/" else path.strip("/") + "/index.html"
    if path.endswith(".html"):
        rel = path.strip("/")
    full = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    if sitemap:
        pages.append((path, priority))


# ---------------------------------------------------------------- shared blocks
def crumbs(trail):
    parts = []
    for i, (n, p) in enumerate(trail):
        parts.append(e(n) if i == len(trail) - 1 else f'<a href="{p}">{e(n)}</a>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + "<span>/</span>".join(parts) + "</nav>"


def page_hero(trail, tag, h1, lede, facts=None, cta=True):
    f = ""
    if facts:
        f = '<div class="facts">' + "".join(f"<div><small>{e(k)}</small><b>{e(v)}</b></div>" for k, v in facts) + "</div>"
    c = f'<div class="btn-row"><a class="btn" href="tel:{TEL}">Call {PHONE}</a><a class="btn ghost" href="/contact/">Send claim details</a></div>' if cta else ""
    return f"""<section class="page-hero"><div class="wrap">{crumbs(trail)}<span class="tag">{e(tag)}</span><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f"<details><summary>{e(q)}</summary><div class=\"a\"><p>{a}</p></div></details>" for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="box call"><h3>Talk through your claim</h3><p>Free initial conversation. We’ll tell you honestly whether appraisal fits.</p><a class="big" href="tel:{TEL}">{PHONE_INTL}</a><a class="btn peach on-dark" href="/contact/">Send claim details</a></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}</a></li>' for n, p in items)
    return f'<div class="box"><h3>{e(title)}</h3><ul>{li}</ul></div>'


def cta_band(h="Have a claim that doesn’t add up?", p="Send us the carrier’s estimate. We’ll review it and tell you what we see."):
    return f"""<section class="cta-band"><div class="wrap"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row"><a class="btn" href="tel:{TEL}">Call {PHONE}</a><a class="btn ghost" href="/contact/">Email the estimate</a></div></div></section>"""


def lead_form(heading="Send us your claim details", sub="Free review. No obligation. Usually a reply within one business day.", page="/"):
    losses = ["Hail", "Wind / tornado", "Hurricane / tropical storm", "Water / leak", "Fire / smoke", "Fallen tree", "Other"]
    roles = ["Homeowner", "Commercial owner", "Property manager / HOA", "Contractor", "Attorney", "Public adjuster", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in Georgia"]
    opt = lambda xs: "".join(f"<option>{e(x)}</option>" for x in xs)
    return f"""<form class="form" action="/api/contact.php" method="post" data-lead novalidate>
<h3>{e(heading)}</h3><p class="sub">{e(sub)}</p>
<div class="fgrid">
<div><label for="f-name">Full name *</label><input id="f-name" name="name" autocomplete="name" required></div>
<div><label for="f-phone">Phone *</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="f-email">Email *</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="f-role">I am a…</label><select id="f-role" name="role">{opt(roles)}</select></div>
<div><label for="f-loss">Type of loss</label><select id="f-loss" name="loss">{opt(losses)}</select></div>
<div><label for="f-city">Property location</label><select id="f-city" name="city">{opt(cities)}</select></div>
<div><label for="f-amt">Approx. amount in dispute</label><select id="f-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="f-car">Insurance company (optional)</label><input id="f-car" name="carrier"></div>
<div class="full"><label for="f-det">What happened, and where does the claim stand?</label><textarea id="f-det" name="details" placeholder="Date of loss, what the carrier has paid or offered, and what you think was missed."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Submitting this form doesn’t create a client relationship. See our <a href="/privacy-policy/">privacy policy</a>.</span></label></div>
<div class="full"><button class="btn peach" type="submit" style="width:100%">Send my claim details</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


# ---------------------------------------------------------------- home
REGIONS = [
    ("north", "North Georgia Mountains", "Dalton · Blue Ridge · Dahlonega", ["Ice & snow load", "Frozen pipes", "Wind on ridgelines", "Falling hardwoods"],
     "Elevation brings winter weather the rest of the state rarely sees. Ice-laden limbs, collapsed gutters and burst pipes in seasonal cabins are the claims we see most in Rabun, Union, Fannin, Gilmer and Whitfield counties.",
     "Rome, Dalton, Calhoun, Blue Ridge, Ellijay, Dahlonega"),
    ("metro", "Metro Atlanta", "Atlanta · Marietta · Alpharetta", ["Hail", "Severe storms", "Tornadoes", "Water losses"],
     "The busiest claim market in the Southeast. Spring hail tracks through Cobb, Cherokee, Gwinnett and North Fulton, while in-town neighborhoods add historic homes and high-rise condos to the mix.",
     "Atlanta, Marietta, Alpharetta, Sandy Springs, Roswell, Lawrenceville, Decatur"),
    ("piedmont", "Piedmont & Middle Georgia", "Athens · Macon · Columbus", ["Tornadoes", "Straight-line winds", "Tree damage", "Fire"],
     "Spring squall lines strengthen across the Piedmont. Mature oaks over historic homes in Macon and Athens mean tree impacts are as common as roof damage.",
     "Athens, Macon, Columbus, Warner Robins, Milledgeville, LaGrange"),
    ("south", "South & Southwest Georgia", "Albany · Valdosta · Tifton", ["Hurricanes", "Fallen pines", "Farm structures", "Tornadoes"],
     "Gulf hurricanes cross this region with surprising strength. Pine forests, pecan orchards and farm outbuildings create claims that blend residential, agricultural and commercial coverage.",
     "Albany, Valdosta, Tifton, Thomasville, Moultrie, Americus"),
    ("coast", "Coastal Georgia", "Savannah · Brunswick · St. Marys", ["Named storms", "Wind-driven rain", "Mold", "Condo losses"],
     "Named-storm deductibles, wind-versus-flood questions and historic buildings define coastal claims from Chatham County to Camden County.",
     "Savannah, Brunswick, St. Simons Island, Richmond Hill, Kingsland, St. Marys"),
]


def home():
    ticker_items = ["Hail · Marietta", "Tornado · Macon", "Hurricane · Savannah", "Fallen pine · Augusta", "Burst pipe · Athens", "Wind · Columbus", "Fire · Alpharetta", "Named storm · Brunswick", "Roof · Warner Robins", "Tree · Valdosta"]
    ticker = "".join(f"<span>{t}</span>" for t in ticker_items * 2)

    svc = "".join(f'<a href="{SVC_BASE}{s["slug"]}/"><span class="n">{i + 1:02d}</span><h3>{e(s["name"])}</h3><p>{e(s["short"])}</p><span class="go">→</span></a>' for i, s in enumerate(SERVICES))

    tabs = "".join(
        f'<button type="button" role="tab" id="tab-{k}" aria-controls="panel-{k}" aria-selected="{"true" if i == 1 else "false"}" tabindex="{0 if i == 1 else -1}">{e(n)}<small>{e(s)}</small></button>'
        for i, (k, n, s, _, _, _) in enumerate(REGIONS))
    panels = "".join(
        f'<div class="region-panel" role="tabpanel" id="panel-{k}" aria-labelledby="tab-{k}"{"" if i == 1 else " hidden"}><h3>{e(n)}</h3><ul class="peril-chips">{"".join(f"<li>{e(p)}</li>" for p in perils)}</ul><p>{e(t)}</p><p class="cities">Communities: {e(c)}</p></div>'
        for i, (k, n, _, perils, t, c) in enumerate(REGIONS))

    tiles = "".join(f'<a class="tile" href="{TOOL_BASE}{t["slug"]}/"><span class="kind">{t["kind"]}</span><span class="ico">{t["icon"]}</span><h3>{e(t["name"])}</h3><p>{e(t["short"])}</p><span class="more">Open tool</span></a>' for t in TOOLS)
    cities = "".join(f'<a href="{loc_path(l)}"><b>{e(l["city"])}</b><small>{e(l["county"])}</small></a>' for l in LOCATIONS)
    posts = "".join(f'<article class="post"><span class="meta">{p["read"]} read · Guide</span><h3><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h3><p>{e(p["summary"])}</p><a class="arrow-link" href="{POST_BASE}{p["slug"]}/">Read guide</a></article>' for p in POSTS[:3])

    home_faqs = [
        ("What does a Georgia Insurance Appraiser actually do?", "We value property damage when you and your insurer agree a loss is covered but disagree on the cost. As your appointed appraiser we inspect, build an independent line-item estimate, work with the carrier’s appraiser and, if needed, present unresolved items to a neutral umpire."),
        ("How is this different from a public adjuster?", "A public adjuster manages and negotiates the whole claim. An appraiser works inside the policy’s appraisal clause on one question: the amount of loss. We don’t negotiate claims outside appraisal and we don’t give legal advice."),
        ("When should I call a Georgia Insurance Appraiser?", "When coverage is accepted, you have the carrier’s estimate, and the gap between it and your contractor’s number is meaningful — generally more than about 10% or several thousand dollars."),
        ("Is the appraisal award binding?", "Yes, on the amount of loss, once any two of the three panel members sign. That’s why documentation matters so much before you invoke appraisal."),
        ("What does it cost?", "Each side pays its own appraiser and usually half of the umpire. We put our fee in writing before any work starts, and our first conversation is free."),
        ("Do you serve my part of Georgia?", "Yes. We work statewide across all 159 counties, with regular work in metro Atlanta, Savannah, Augusta, Columbus, Macon, Athens and South Georgia."),
    ]

    body = f"""
<section class="hero"><div class="wrap">
<div>
<span class="tag">Independent claim appraisal · Statewide</span>
<h1>Georgia Insurance Appraiser for <em>underpaid</em> property claims</h1>
<p class="lede">When your carrier accepts the claim but the check won’t cover the repair, Georgia Insurance Appraiser builds an independent, line-by-line valuation and takes it through the appraisal process written into your policy.</p>
<ul class="hero-points"><li>Your appointed appraiser under the policy’s appraisal clause</li><li>Xactimate estimates priced for your Georgia ZIP code</li><li>Homes, condos, HOAs, churches and commercial buildings</li></ul>
<div class="btn-row"><a class="btn peach" href="tel:{TEL}">Call {PHONE}</a><a class="btn ghost" href="#check">Check your claim gap</a></div>
</div>
<div class="sheet" aria-label="Example claim comparison">
<span class="stamp">Example file</span>
<div class="sheet-head"><span>Claim worksheet · Cobb Co.</span><i>Hail</i></div>
<div class="sheet-body">
<div class="sheet-row strike"><span>Carrier estimate (2 slopes)</span><b>$11,840</b></div>
<div class="sheet-row"><span>Full roof replacement · 34 sq</span><b>$19,720</b></div>
<div class="sheet-row"><span>Gutters, AC fins, window wraps</span><b>$3,460</b></div>
<div class="sheet-row"><span>Steep charge · permit · O&amp;P</span><b>$4,115</b></div>
</div>
<div class="sheet-bars">
<div><div class="bar-l"><span>Carrier</span><span>$11.8k</span></div><div class="bar"><span data-w="43%"></span></div></div>
<div><div class="bar-l"><span>Independent valuation</span><span>$27.3k</span></div><div class="bar alt"><span data-w="100%"></span></div></div>
</div>
<div class="sheet-foot"><span>Disputed amount</span><b>$15,455</b></div>
<p class="sheet-note">Illustrative figures for a typical scope dispute — not a client result.</p>
</div>
</div></section>

<div class="ticker" aria-hidden="true"><div class="ticker-track">{ticker}</div></div>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><span class="sec-num">§ 01</span><div><h2>Why property owners call a Georgia Insurance Appraiser</h2><p>Most underpaid claims aren’t denied — they’re just short. A missing roof slope, a mismatched floor, a code item nobody priced. Georgia Insurance Appraiser exists for that gap between “covered” and “paid in full.”</p></div></div>
<div class="trio rv">
<div><span class="k">What we do</span><h3>Value the loss independently</h3><p>We inspect, measure and price the damage from scratch instead of editing the carrier’s numbers, so every line can be defended in front of an umpire.</p></div>
<div><span class="k">When it fits</span><h3>Coverage accepted, cost disputed</h3><ul><li>Repair vs. replace disagreements</li><li>Matching and discontinued materials</li><li>Missing trades, code items and O&amp;P</li><li>Mitigation invoices cut back</li></ul></div>
<div><span class="k">When it doesn’t</span><h3>We’ll tell you honestly</h3><ul><li>Outright coverage denials</li><li>Bad-faith or legal claims</li><li>Gaps too small to justify fees</li><li>Deadlines that need an attorney first</li></ul></div>
</div>
</div></section>

<section class="sec alt"><div class="wrap">
<div class="sec-head rv"><span class="sec-num">§ 02</span><div><h2>What Georgia Insurance Appraiser does for your claim</h2><p>Eleven services built around one job: producing a valuation of your loss that holds up. Start with an estimate review, or bring us in once appraisal has been demanded.</p></div></div>
<div class="ledger rv">{svc}</div>
<p style="margin-top:28px"><a class="arrow-link" href="{SVC_BASE}">Compare all appraisal services</a></p>
</div></section>

<section class="sec" id="check"><div class="wrap split wide-l">
<div class="rv">{GAP_MINI}</div>
<div class="rv"><span class="tag">Quick gap check</span><h2>Is your gap worth an appraisal?</h2><p>Type in the two numbers you already have. If the difference is large, a conversation with a Georgia Insurance Appraiser makes sense. If it’s small, a documented supplement request may close it faster and cheaper.</p><p>The full <a href="{TOOL_BASE}appraisal-value-estimator/">appraisal value estimator</a> adds appraiser and umpire fees so you can see a realistic net figure.</p><a class="btn" href="{TOOL_BASE}">See all six free tools</a></div>
</div></section>

<section class="sec pine"><div class="wrap">
<div class="sec-head rv"><span class="sec-num">§ 03</span><div><h2>One state, five very different claim climates</h2><p>Ice in Blue Ridge, hail in Marietta, tornadoes in Macon, hurricanes in Valdosta and Brunswick. A Georgia Insurance Appraiser has to know how each region’s weather shows up on a roof — and in an estimate.</p></div></div>
<div class="regions rv" data-regions><div class="region-tabs" role="tablist" aria-label="Georgia regions">{tabs}</div>{panels}</div>
</div></section>

<section class="sec card-bg"><div class="wrap">
<div class="sec-head rv"><span class="sec-num">§ 04</span><div><h2>How appraisal moves a stuck claim</h2><p>The appraisal clause turns an open-ended argument into a defined process with a binding result. Here is how Georgia Insurance Appraiser takes a file from first call to signed award.</p></div></div>
<ol class="steps rv">
<li><h3>Free claim review</h3><p>We read your policy, the carrier’s estimate and your photos, then tell you whether appraisal fits.</p></li>
<li><h3>Independent valuation</h3><p>On-site inspection, measurements and a line-item estimate priced for your area.</p></li>
<li><h3>Written demand</h3><p>Appraisal is invoked in writing and we’re named as your appraiser within the policy’s deadline.</p></li>
<li><h3>Panel negotiation</h3><p>We work line by line with the carrier’s appraiser. Most disputes narrow sharply here.</p></li>
<li><h3>Award</h3><p>Unresolved items go to a neutral umpire. Two signatures set the amount of loss.</p></li>
</ol>
<p style="margin-top:28px"><a class="arrow-link" href="/how-appraisal-works/">Read the full appraisal process guide</a></p>
</div></section>

<section class="sec alt"><div class="wrap">
<div class="sec-head rv"><span class="sec-num">§ 05</span><div><h2>Free claim tools built by a Georgia Insurance Appraiser</h2><p>Run the numbers before you pick up the phone. Every tool works in your browser — nothing is stored or sent.</p></div></div>
<div class="tiles rv">{tiles}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><span class="sec-num">§ 06</span><div><h2>Georgia Insurance Appraiser locations</h2><p>We serve every county in the state. These are the communities where Georgia Insurance Appraiser handles claims most often, each with its own local page on storm patterns, housing stock and common disputes.</p></div></div>
<div class="cities-grid rv">{cities}</div>
<p style="margin-top:28px"><a class="arrow-link" href="{LOC_BASE}">See statewide coverage</a></p>
</div></section>

<section class="sec card-bg"><div class="wrap">
<div class="sec-head rv"><span class="sec-num">§ 07</span><div><h2>Appraiser, public adjuster or attorney?</h2><p>Each one solves a different problem. Picking the right help first saves time and fees — and Georgia Insurance Appraiser will point you elsewhere when appraisal isn’t the right tool.</p></div></div>
<div class="table-wrap rv"><table><thead><tr><th>Question</th><th>Georgia Insurance Appraiser</th><th>Public adjuster</th><th>Attorney</th></tr></thead><tbody>
<tr><th>Main job</th><td class="hl">Value the amount of loss</td><td>Manage &amp; negotiate the claim</td><td>Legal disputes &amp; litigation</td></tr>
<tr><th>Best stage</th><td class="hl">Coverage accepted, number disputed</td><td>Early, from first notice</td><td>Denials, bad faith, deadlines</td></tr>
<tr><th>Result</th><td class="hl">Binding award (2 of 3 signatures)</td><td>Negotiated settlement</td><td>Settlement or judgment</td></tr>
<tr><th>Decides coverage?</th><td class="hl">No</td><td>No</td><td>Argues it in court</td></tr>
</tbody></table></div>
</div></section>

<section class="sec dark"><div class="wrap split">
<div class="rv"><span class="sec-num">§ 08</span><h2 style="margin-top:20px">Questions people ask a Georgia Insurance Appraiser</h2><p>Straight answers about how appraisal works, what it costs and when it’s the wrong move.</p><div class="btn-row" style="margin-top:22px"><a class="btn peach on-dark" href="/appraisal-faq/">All FAQs</a><a class="btn ghost on-dark" href="/claim-glossary/">Claim glossary</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><span class="sec-num">§ 09</span><div><h2>Read before you invoke appraisal</h2><p>Practical guides from the Georgia Insurance Appraiser team on policy language, documentation and strategy.</p></div></div>
<div class="posts rv">{posts}</div>
</div></section>

<section class="sec dark" id="contact"><div class="wrap contact">
<div class="rv"><span class="tag light">Start with a conversation</span><h2>Talk to a Georgia Insurance Appraiser about your claim</h2><p>Tell us what happened and what the carrier offered. We’ll review it and give you a straight answer on whether appraisal is worth pursuing — no pressure, no obligation.</p>
<ul class="contact-lines"><li><span>Call / text</span><a href="tel:{TEL}">{PHONE_INTL}</a></li><li><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><span>Hours</span><b style="color:#fff">Mon–Fri, 8am–6pm ET</b></li><li><span>Coverage</span><b style="color:#fff">All 159 Georgia counties</b></li></ul></div>
<div class="rv">{lead_form(page="/")}</div>
</div></section>
"""
    schema = [faq_schema(home_faqs), {"@type": "WebPage", "@id": DOMAIN + "/#webpage", "url": DOMAIN + "/", "name": f"{BRAND} | Independent Property Claim Appraisal in Georgia", "about": {"@id": DOMAIN + "/#business"}, "isPartOf": {"@id": DOMAIN + "/#website"}}]
    write("/", document("/", f"{BRAND} | Independent Property Claim Appraiser",
                        "Georgia Insurance Appraiser provides independent appraisal, estimate review and umpire services for underpaid hail, wind, hurricane, water and fire claims statewide.",
                        body, schema), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for s in SERVICES:
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        rel = [x for x in SERVICES if x is not s][:3]
        related = "".join(f'<a href="{SVC_BASE}{r["slug"]}/"><small>Service</small>{e(r["name"])}</a>' for r in rel)
        locs = [(loc_label(l), loc_path(l)) for l in LOCATIONS[:6]]
        body = page_hero(trail, "Appraisal service", s["h1"], s["lede"], s["facts"]) + f"""
<div class="wrap layout"><article class="prose">{s["body"]}
<h2>Frequently asked questions</h2>{faq_block(s["faqs"])}
<h2>Related services</h2><div class="related">{related}</div>
</article>
<aside class="aside">{call_box()}{list_box("All services", items, path)}{list_box("Where we work", locs + [("All Georgia locations", LOC_BASE)])}</aside></div>
{cta_band()}"""
        schema = [crumbs_schema(trail), faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "State", "name": "Georgia"}, "url": DOMAIN + path}]
        write(path, document(path, s["title"], s["desc"], body, schema), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(f'<a class="index-card" href="{SVC_BASE}{s["slug"]}/"><span class="k">{i + 1:02d} · Service</span><h2>{e(s["name"])}</h2><p>{e(s["short"])}</p></a>' for i, s in enumerate(SERVICES))
    body = page_hero(trail, "What we do", "Insurance Appraisal Services for Georgia Property Claims",
                     "From a single estimate review to full panel representation and neutral umpire work, every Georgia Insurance Appraiser service is built around an accurate, defensible valuation of your loss.") + f"""
<section class="sec"><div class="wrap"><div class="index-list">{cards}</div></div></section>
<section class="sec alt"><div class="wrap split"><div><span class="tag">Not sure where to start?</span><h2>Most claims begin with an estimate review</h2><p>Before anyone invokes appraisal, it helps to know exactly where the carrier’s estimate falls short and what that gap is worth. A review gives you that answer in days, and many disputes close at that stage.</p><a class="btn" href="{SVC_BASE}insurance-estimate-review/">About estimate reviews</a></div><div>{faq_block([("Can I hire you for just one part of the process?", "Yes. Many clients start with an estimate review and decide later whether to invoke appraisal."), ("Do you work on both residential and commercial claims?", "Yes — houses, condos, multifamily, retail, office, industrial, churches and HOA properties."), ("Do you only work on hail claims?", "No. We handle wind, hurricane, water, fire, tree and other covered perils.")])}</div></div></section>
{cta_band()}"""
    schema = [crumbs_schema(trail), {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": DOMAIN + f'{SVC_BASE}{s["slug"]}/', "name": s["name"]} for i, s in enumerate(SERVICES)]}]
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in Georgia | Claim Valuation",
                             "Georgia insurance appraisal services: appraisal clause representation, estimate review, hail, wind, hurricane, water, fire and tree claims, plus neutral umpire work.",
                             body, schema), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        name = loc_label(l)
        trail = [("Home", "/"), ("Locations", LOC_BASE), (l["city"], path)]
        near = "".join(f'<a href="{loc_path(LOC_BY[n])}"><small>Nearby</small>{e(LOC_BY[n]["city"])}</a>' for n in l["near"])
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:6])
        body = page_hero(trail, l["region"], f"Insurance Appraiser in {name}", l["lede"],
                         [("County", l["county"]), ("Region", l["region"]), ("Coverage", "On-site inspections")]) + f"""
<div class="wrap layout"><article class="prose">
<div class="note"><b class="h">Local claim risks</b><ul class="peril-chips" style="margin:8px 0 0">{"".join(f'<li style="color:var(--ink);border-color:var(--ink)">{e(p)}</li>' for p in l["perils"])}</ul></div>
{l["body"]}
<h2>Services available in {e(l["city"])}</h2>
<p>Every {BRAND} service is available to property owners in {e(l["city"])} and the surrounding area, including:</p>
<ul>{svc_links}</ul>
<h2>Questions from {e(l["city"])} property owners</h2>{faq_block(l["faqs"])}
<h2>Nearby service areas</h2><div class="related">{near}</div>
</article>
<aside class="aside">{call_box()}{list_box("Georgia locations", items, path)}{list_box("Free claim tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])}</aside></div>
{cta_band(f"Disputed claim in {l['city']}?", "Send us the estimate and your photos. We’ll tell you what we see.")}"""
        city = l["city"].split(" &")[0]
        schema = [crumbs_schema(trail), faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {name}", "serviceType": "Insurance appraisal", "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "City", "name": city, "containedInPlace": {"@type": "State", "name": "Georgia"}}, "url": DOMAIN + path}]
        title = f"Insurance Appraiser {city} GA | Disputed Claim Appraisal" if len(city) < 14 else f"Insurance Appraiser {city}, GA | Claim Appraisal"
        desc = f"Independent insurance appraiser serving {l['city']} and {l['county']}. Appraisal and estimate review for underpaid storm, water and fire claims."
        write(path, document(path, title, desc, body, schema), 0.8)

    trail = [("Home", "/"), ("Locations", LOC_BASE)]
    cities = "".join(f'<a href="{loc_path(l)}"><b>{e(l["city"])}</b><small>{e(l["county"])}</small></a>' for l in LOCATIONS)
    reg = "".join(f'<div class="index-card"><span class="k">{e(s)}</span><h2>{e(n)}</h2><p>{e(t)}</p><p style="margin-top:10px;font-size:.88rem;color:var(--muted)">{e(c)}</p></div>' for k, n, s, _, t, c in REGIONS)
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal Across All 159 Georgia Counties",
                     "Georgia Insurance Appraiser works statewide — from the Tennessee line to the St. Marys River. These local pages cover the cities where we handle claims most often.") + f"""
<section class="sec"><div class="wrap"><div class="cities-grid">{cities}</div></div></section>
<section class="sec alt"><div class="wrap"><div class="sec-head"><span class="sec-num">Regions</span><div><h2>How claims differ across Georgia</h2><p>The same policy language plays out very differently in a mountain cabin, a Buckhead condo and a Golden Isles beach house.</p></div></div><div class="index-list">{reg}</div></div></section>
{cta_band("Don’t see your city?", "We cover every Georgia county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Georgia Insurance Appraiser Locations | Statewide Claim Appraisal",
                             "Insurance appraisal across Georgia: Atlanta, Savannah, Augusta, Columbus, Macon, Athens, Marietta, Alpharetta, Albany, Valdosta, Warner Robins and Brunswick.",
                             body, [crumbs_schema(trail)]), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for t in TOOLS:
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Claim tools", TOOL_BASE), (t["name"], path)]
        others = "".join(f'<a href="{TOOL_BASE}{o["slug"]}/"><small>{o["kind"]}</small>{e(o["name"])}</a>' for o in [x for x in TOOLS if x is not t][:3])
        body = page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], t["lede"], cta=False) + f"""
<section class="sec tight" style="border-bottom:0"><div class="wrap">{t["markup"]}
<p class="hint">For planning only. Results depend on the figures you enter and your policy’s terms, and aren’t a quote, appraisal or legal advice.</p></div></section>
<div class="wrap layout" style="padding-top:20px"><article class="prose">{t["explain"]}
<h2>Questions about this tool</h2>{faq_block(t["faqs"])}
<h2>More free tools</h2><div class="related">{others}</div></article>
<aside class="aside">{call_box()}{list_box("All claim tools", items, path)}</aside></div>
{cta_band("Want a professional to check the numbers?", "Send us your estimate and we’ll review it line by line.")}"""
        schema = [crumbs_schema(trail), faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema), 0.8)

    trail = [("Home", "/"), ("Claim tools", TOOL_BASE)]
    tiles = "".join(f'<a class="tile" href="{TOOL_BASE}{t["slug"]}/"><span class="kind">{t["kind"]}</span><span class="ico">{t["icon"]}</span><h2 style="font-size:1.2rem">{e(t["name"])}</h2><p>{e(t["short"])}</p><span class="more">Open tool</span></a>' for t in TOOLS)
    body = page_hero(trail, "Free & private", "Free Insurance Claim Tools for Georgia Property Owners",
                     "Six calculators and planners built from real appraisal work. Use them to understand your claim, check the carrier’s math and decide on next steps — no sign-up, nothing stored.", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="tiles">{tiles}</div></div></section>
<section class="sec alt"><div class="wrap split"><div><span class="tag">Suggested order</span><h2>Using the tools together</h2><ol><li>Start with the <a href="{TOOL_BASE}claim-deadline-planner/">deadline planner</a> so nothing lapses.</li><li>Check the roof math with the <a href="{TOOL_BASE}roof-squares-pitch-calculator/">squares &amp; pitch calculator</a>.</li><li>See what you’re actually owed with the <a href="{TOOL_BASE}wind-hail-deductible-calculator/">deductible</a> and <a href="{TOOL_BASE}depreciation-holdback-calculator/">depreciation</a> calculators.</li><li>Test the dispute with the <a href="{TOOL_BASE}appraisal-value-estimator/">appraisal value estimator</a>.</li><li>Finish with the <a href="{TOOL_BASE}appraisal-readiness-score/">readiness score</a>.</li></ol></div><div>{call_box()}</div></div></section>"""
    schema = [crumbs_schema(trail), {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": DOMAIN + f'{TOOL_BASE}{t["slug"]}/', "name": t["name"]} for i, t in enumerate(TOOLS)]}]
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Calculators & Tools for Georgia",
                              "Free property claim tools: appraisal value estimator, depreciation calculator, roof squares, wind/hail deductible, deadline planner and readiness score.",
                              body, schema), 0.9)


# ---------------------------------------------------------------- learn
def learn_pages():
    learn_items = [("How appraisal works", "/how-appraisal-works/"), ("Appraisal FAQ", "/appraisal-faq/"), ("Claim glossary", "/claim-glossary/"), ("Insights & guides", POST_BASE)]

    # process
    path = "/how-appraisal-works/"
    trail = [("Home", "/"), ("How appraisal works", path)]
    body = page_hero(trail, "Process guide", "How Insurance Appraisal Works in Georgia, Step by Step",
                     "Seven stages, from the first disagreement to a signed award — what happens, who does what, and where claims most often go wrong.",
                     [("Stages", "7"), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + f"""
<div class="wrap layout"><article class="prose">{PROCESS_BODY}</article>
<aside class="aside">{call_box()}{list_box("Learn", learn_items, path)}</aside></div>{cta_band()}"""
    howto = {"@type": "HowTo", "name": "How insurance appraisal works in Georgia", "step": [{"@type": "HowToStep", "position": i + 1, "name": n} for i, n in enumerate(["The disagreement", "The written demand", "Both sides name appraisers", "Choosing an umpire", "Negotiation between appraisers", "Umpire review", "The award"])]}
    write(path, document(path, "How Insurance Appraisal Works in Georgia | 7-Step Process Guide",
                         "Step-by-step guide to insurance appraisal in Georgia: the written demand, choosing appraisers and an umpire, negotiation, umpire review and the binding award.",
                         body, [crumbs_schema(trail), howto]), 0.8)

    # FAQ
    path = "/appraisal-faq/"
    trail = [("Home", "/"), ("Appraisal FAQ", path)]
    groups = "".join(f'<h2>{e(g)}</h2>{faq_block(qs)}' for g, qs in FAQ)
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers", "Insurance Appraisal FAQ for Georgia Property Owners",
                     "Plain answers to the questions we hear most — about the appraisal process, costs, timing and how Georgia rules fit in.") + f"""
<div class="wrap layout"><article class="prose">{groups}</article>
<aside class="aside">{call_box()}{list_box("Learn", learn_items, path)}</aside></div>{cta_band("Didn’t see your question?", "Call or email — we’re happy to talk it through.")}"""
    write(path, document(path, "Insurance Appraisal FAQ | Costs, Timing & Georgia Rules",
                         "Answers to common questions about insurance appraisal in Georgia: how it works, what it costs, how long it takes, binding awards and Georgia-specific rules.",
                         body, [crumbs_schema(trail), faq_schema(allq)]), 0.8)

    # glossary
    path = "/claim-glossary/"
    trail = [("Home", "/"), ("Claim glossary", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in GLOSSARY:
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f"<dt{anchor}>{e(term)}</dt><dd>{e(d)}</dd>"
    body = page_hero(trail, "Reference", "Property Insurance Claim Glossary",
                     f"{len(GLOSSARY)} terms you’ll see in policies, estimates and appraisal awards, defined in plain English.", cta=False) + f"""
<div class="wrap layout"><article class="prose"><div class="filter"><label for="gloss-filter">Filter terms</label><input id="gloss-filter" type="search" placeholder="Try “depreciation” or “umpire”"></div><div class="az">{az}</div><dl class="glossary">{dl}</dl></article>
<aside class="aside">{call_box()}{list_box("Learn", learn_items, path)}</aside></div>"""
    dts = {"@type": "DefinedTermSet", "name": "Property insurance claim glossary", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}
    write(path, document(path, "Insurance Claim Glossary | ACV, RCV, Umpire & More Defined",
                         "Plain-English definitions of property insurance claim terms: actual cash value, replacement cost, depreciation, appraisal award, umpire, O&P and more.",
                         body, [crumbs_schema(trail), dts]), 0.7)

    # posts
    for p in POSTS:
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Insights", POST_BASE), (p["title"], path)]
        others = "".join(f'<a href="{POST_BASE}{o["slug"]}/"><small>Guide</small>{e(o["title"])}</a>' for o in [x for x in POSTS if x is not p][:3])
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        body = page_hero(trail, f"Guide · {p['read']} read · {nice}", p["title"], e(p["summary"]), cta=False) + f"""
<div class="wrap layout"><article class="prose">{p["body"]}<h2>Keep reading</h2><div class="related">{others}</div></article>
<aside class="aside">{call_box()}{list_box("Learn", learn_items)}{list_box("Free tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]])}</aside></div>{cta_band()}"""
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "author": {"@type": "Organization", "name": BRAND}, "publisher": {"@id": DOMAIN + "/#business"}, "mainEntityOfPage": DOMAIN + path, "image": DOMAIN + "/assets/img/og-image.png"}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), art], og_type="article"), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Insights", path)]
    cards = "".join(f'<article class="post"><span class="meta">{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {p["read"]} read</span><h2 style="font-size:1.3rem;margin:10px 0"><a href="{POST_BASE}{p["slug"]}/" style="color:var(--ink);text-decoration:none">{e(p["title"])}</a></h2><p>{e(p["summary"])}</p><a class="arrow-link" href="{POST_BASE}{p["slug"]}/">Read guide</a></article>' for p in POSTS)
    body = page_hero(trail, "Insights & guides", "Insurance Appraisal Insights for Georgia Property Owners",
                     "Practical guides on policy language, documentation and claim strategy, written by people who work appraisal panels.", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="posts">{cards}</div></div></section>{cta_band()}"""
    write(path, document(path, "Insurance Appraisal Insights & Guides for Georgia",
                         "Guides for Georgia property owners on appraisal clauses, hail documentation, reading insurance estimates and choosing between appraisers, adjusters and attorneys.",
                         body, [crumbs_schema(trail)]), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    # about
    path = "/about/"
    trail = [("Home", "/"), ("About", path)]
    body = page_hero(trail, "About us", "About Georgia Insurance Appraiser",
                     "We’re estimators and appraisers who believe a property claim should be paid on what the damage actually costs — documented clearly enough that everyone at the table can see it.") + f"""
<div class="wrap layout"><article class="prose">
<h2>Why we focus only on appraisal</h2>
<p>Most property claim professionals do a little of everything. We chose to specialize. Georgia Insurance Appraiser works on one question — the amount of loss — and we’ve built our process, tools and documentation standards around answering it well. That focus lets us serve as your appointed appraiser, review estimates before a dispute escalates, or sit as a neutral umpire on panels where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Independent scope first.</strong> We inspect and measure before we look at anyone else’s numbers.</li>
<li><strong>Defensible over impressive.</strong> An inflated estimate might look good on day one, but it loses credibility with the umpire. We price what we can support.</li>
<li><strong>Plain-English reporting.</strong> You’ll understand every difference between our valuation and the carrier’s.</li>
<li><strong>Honest triage.</strong> If your claim needs an attorney or a public adjuster instead, we’ll say so.</li>
<li><strong>Fees in writing.</strong> Before any work starts, you know exactly what it costs.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, condo owners, landlords, HOA boards, property managers, churches, business owners, contractors, public adjusters and attorneys across Georgia. On any given claim, we serve in one role only, and we disclose any prior relationships with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We aren’t a law firm and don’t give legal advice. We don’t act as public adjusters or negotiate claims outside the appraisal process. We don’t guarantee outcomes — no honest appraiser can.</p>
<h2>Statewide, on purpose</h2>
<p>Georgia’s weather varies dramatically between the mountains, the Piedmont, the Coastal Plain and the coast. Working statewide means we see every kind of loss the state produces — ice in Blue Ridge, hail in Marietta, tornadoes in Macon, hurricanes in Brunswick — and price each one with local knowledge.</p>
</article><aside class="aside">{call_box()}{list_box("Explore", [("Our services", SVC_BASE), ("Locations", LOC_BASE), ("Free tools", TOOL_BASE), ("How appraisal works", "/how-appraisal-works/")])}</aside></div>{cta_band()}"""
    write(path, document(path, "About Georgia Insurance Appraiser | Independent Claim Valuation",
                         "Georgia Insurance Appraiser is an independent appraisal and estimating practice focused on one question: the amount of loss on disputed property insurance claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage", "url": DOMAIN + path, "about": {"@id": DOMAIN + "/#business"}}]), 0.7)

    # contact
    path = "/contact/"
    trail = [("Home", "/"), ("Contact", path)]
    body = page_hero(trail, "Get in touch", "Contact Georgia Insurance Appraiser",
                     "Call, text, email or send your claim details below. Our first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", cta=False) + f"""
<section class="sec dark"><div class="wrap contact">
<div><span class="tag light">Direct lines</span><h2>Reach us directly</h2>
<ul class="contact-lines"><li><span>Call / text</span><a href="tel:{TEL}">{PHONE_INTL}</a></li><li><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><span>Hours</span><b style="color:#fff">Mon–Fri, 8am–6pm ET</b></li><li><span>Service area</span><b style="color:#fff">Statewide — all 159 counties</b></li></ul>
<h3>Helpful to have ready</h3><ul><li>Declarations page</li><li>The carrier’s full estimate (PDF)</li><li>Letters or emails from the carrier</li><li>Photos and your contractor’s estimate</li></ul></div>
<div>{lead_form("Tell us about your claim", page=path)}</div></div></section>"""
    write(path, document(path, "Contact Georgia Insurance Appraiser | (844) 537-1427",
                         "Contact Georgia Insurance Appraiser for a free review of your disputed property claim. Call or text (844) 537-1427 or email info@georgiainsuranceappraiser.com.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage", "url": DOMAIN + path}]), 0.8)

    legal = {
        "/privacy-policy/": ("Privacy Policy", f"""
<p><em>Last updated: {date.today().strftime("%B %-d, %Y")}</em></p>
<h2>What we collect</h2><p>When you submit a form, call or email us, we collect the information you choose to provide — such as your name, phone number, email address, property location and details about your claim. Our web server also records standard technical data (IP address, browser type, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim.</li><li>To provide services you request.</li><li>To keep the site secure and working properly.</li></ul>
<p>We don’t sell your personal information. We share it only with people who need it to help with your claim (with your permission), with service providers who host our site and email, or when required by law.</p>
<h2>Claim tools</h2><p>Our calculators and checklists run in your browser. The numbers you enter aren’t sent to us or stored on our servers.</p>
<h2>Cookies</h2><p>This site doesn’t use advertising cookies. Fonts are loaded from Google Fonts, which may log standard request data under Google’s privacy policy.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>You can ask us to access, correct or delete the personal information you’ve given us by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>"""),
        "/terms-of-use/": ("Terms of Use", f"""
<p><em>Last updated: {date.today().strftime("%B %-d, %Y")}</em></p>
<h2>Use of this site</h2><p>By using this website you agree to these terms. The content is provided for general information about insurance appraisal and property claims in Georgia.</p>
<h2>No professional relationship</h2><p>Reading this site, using its tools or submitting a form doesn’t create an appraiser–client relationship. That relationship begins only when we both sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm. Nothing on this site is legal advice. Insurance policies differ, and laws and court decisions change. Consult a licensed Georgia attorney for legal questions.</p>
<h2>Tools and estimates</h2><p>Calculators provide planning estimates based on the information you enter. They are not appraisals, quotes or predictions of any claim outcome.</p>
<h2>Intellectual property</h2><p>Site content, design and tools belong to {BRAND}. You may share links and print pages for personal use.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent permitted by law, we aren’t liable for decisions made based on its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Georgia.</p>"""),
        "/disclaimer/": ("Disclaimer", f"""
<h2>General information only</h2><p>The content on this website is educational and general. It describes how insurance appraisal commonly works, but your policy’s language controls. Always read your own policy and its endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We are not attorneys, we don’t provide legal advice, and we don’t act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>No guarantee of results</h2><p>Every claim is different. Example figures on this site are illustrative and are not results for any specific client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Insurance policies contain deadlines, including for notice, proof of loss, depreciation recovery and lawsuits. Information on this site doesn’t extend or alter any deadline. If a deadline is approaching, consult a Georgia attorney promptly.</p>
<h2>Third-party references</h2><p>References to statutes, agencies or weather events are for context. Verify current law and facts with official sources such as the Georgia Office of Commissioner of Insurance and Safety Fire.</p>"""),
    }
    for path, (title, content) in legal.items():
        trail = [("Home", "/"), (title, path)]
        body = page_hero(trail, "Legal", title, f"How {BRAND} handles {title.lower().replace('policy', '').strip()} matters.", cta=False) + f'<div class="wrap layout"><article class="prose narrow">{content}</article><aside class="aside">{call_box()}</aside></div>'
        write(path, document(path, f"{title} | {BRAND}", f"{title} for {BRAND} (georgiainsuranceappraiser.com).", body, [crumbs_schema(trail)]), 0.3)


def sitemap_pages():
    path = "/site-map/"
    trail = [("Home", "/"), ("Site map", path)]
    groups = [
        ("Main", [("Home", "/"), ("About", "/about/"), ("Contact", "/contact/")]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Locations", [("All locations", LOC_BASE)] + [(loc_label(l), loc_path(l)) for l in LOCATIONS]),
        ("Claim tools", [("All tools", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Learn", [("How appraisal works", "/how-appraisal-works/"), ("Appraisal FAQ", "/appraisal-faq/"), ("Claim glossary", "/claim-glossary/"), ("Insights", POST_BASE)] + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Legal", [("Privacy policy", "/privacy-policy/"), ("Terms of use", "/terms-of-use/"), ("Disclaimer", "/disclaimer/")]),
    ]
    cols = "".join(f'<div class="index-card"><h2>{e(g)}</h2><ul style="padding-left:1.1em;margin:0">{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Site Map", f"Every page on {BRAND}.", cta=False) + f'<section class="sec"><div class="wrap"><div class="index-list">{cols}</div></div></section>'
    write(path, document(path, f"Site Map | {BRAND}", f"A complete list of every page on {BRAND}: services, Georgia locations, free claim tools and guides.", body, [crumbs_schema(trail)]), 0.3)

    # 404
    body = f"""<section class="page-hero"><div class="wrap"><span class="tag">Error 404</span><h1>This page isn’t in the file</h1><p class="lede">The page you’re looking for may have moved. Try one of these instead.</p><div class="btn-row"><a class="btn" href="/">Home</a><a class="btn ghost" href="{SVC_BASE}">Services</a><a class="btn ghost" href="{TOOL_BASE}">Free tools</a><a class="btn ghost" href="/contact/">Contact</a></div></div></section>"""
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}", "The requested page could not be found.", body, robots="noindex,follow"), sitemap=False)


def root_files():
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p, pr in pages:
        xml.append(f"  <url><loc>{DOMAIN}{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr:.1f}</priority></url>")
    xml.append("</urlset>")
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write("\n".join(xml) + "\n")
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /home.html\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    with open(os.path.join(OUT, "index.php"), "w") as f:
        f.write(INDEX_PHP)
    with open(os.path.join(OUT, ".htaccess"), "w") as f:
        f.write("DirectoryIndex index.html index.php\nErrorDocument 404 /404.html\nOptions -Indexes\n")


INDEX_PHP = r"""<?php
// Georgia Insurance Appraiser - front controller for the static build.
// The host serves real files directly and routes "/" and unknown paths here.
$path = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$home = 'https://georgiainsuranceappraiser.com';

// Canonical host/scheme - only once the real domain is connected.
if ($host === 'www.georgiainsuranceappraiser.com' ||
    ($host === 'georgiainsuranceappraiser.com' && ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http')) {
    header('Location: ' . $home . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// Keep temporary preview domains out of search results.
if ($host !== 'georgiainsuranceappraiser.com') {
    header('X-Robots-Tag: noindex, nofollow');
}

if ($path === '/' || $path === '/index.php') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path)) {
    header('Location: ' . $path . '/', true, 301);
    exit;
}
if (substr($path, -1) === '/' && is_file(__DIR__ . $path . 'index.html')) {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . $path . 'index.html');
    exit;
}
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
"""


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(STATIC, OUT)
    home()
    service_pages()
    location_pages()
    tool_pages()
    learn_pages()
    company_pages()
    sitemap_pages()
    root_files()
    print(f"built {len(pages)} sitemap pages into {OUT}")


if __name__ == "__main__":
    main()
