#!/usr/bin/env python3
"""Static site generator for connectedrenter.com.

python3 build.py   -> writes every page into this directory (home.html, */index.html, sitemap.xml, ...)
python3 validate.py -> checks the output
"""
import html
import json
import math
import os
import re
import sys
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from icons import icon, sprite  # noqa: E402
from tools import TOOLS, render as render_tool  # noqa: E402
from content.resources import RESOURCES  # noqa: E402
from content.blog import POSTS, CATS  # noqa: E402

ORIGIN = "https://connectedrenter.com"
SITE = "Connected Renter"
TAGLINE = "Connecting Made Easy"
PHONE = "210-903-9471"
PHONE_HREF = "+12109039471"
EMAIL = "iamjosephdittman@gmail.com"
ADDRESS = ("2140 E Southlake Blvd", "Southlake", "TX", "76092")
TODAY = date.today().isoformat()
VER = TODAY.replace("-", "")

esc = html.escape
PAGES = []  # (path, lastmod, priority) for the sitemap


def fill(body):
    body = re.sub(r"__ICON_([a-z-]+)__", lambda m: icon(m.group(1)), body)
    return re.sub(r"__TOOL_([a-z-]+)__", lambda m: render_tool(m.group(1), "-b"), body)


def words(s):
    return len(re.sub(r"<[^>]+>", " ", s).split())


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "</script>"


ORG = {
    "@type": "Organization", "@id": ORIGIN + "/#org", "name": SITE, "url": ORIGIN + "/",
    "slogan": TAGLINE, "logo": ORIGIN + "/assets/img/connected-renter-logo.png",
    "email": EMAIL, "telephone": "+1-" + PHONE,
    "address": {"@type": "PostalAddress", "streetAddress": ADDRESS[0], "addressLocality": ADDRESS[1], "addressRegion": ADDRESS[2], "postalCode": ADDRESS[3], "addressCountry": "US"},
}
WEBSITE = {"@type": "WebSite", "@id": ORIGIN + "/#website", "url": ORIGIN + "/", "name": SITE, "publisher": {"@id": ORIGIN + "/#org"}}


def crumbs_ld(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": ORIGIN + u} for i, (n, u) in enumerate(trail)]}


def faq_ld(faqs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


# ------------------------------------------------------------------ layout

def nav(current):
    def cur(p):
        return ' aria-current="page"' if current == p else ""
    res = "".join(
        f'<li><a href="/moving-resources/{r["slug"]}/"><span class="mi">{icon(r["icon"])}</span><span><strong>{r["name"]}</strong><small>{esc(r["short"])}</small></span></a></li>'
        for r in RESOURCES)
    res += f'<li><a href="/landing/"><span class="mi">{icon("compass")}</span><span><strong>Renter Roadmap</strong><small>Start here: every step from search to settled.</small></span></a></li>'
    res += f'<li class="menu-all"><a class="menu-all" href="/moving-resources/">All moving resources {icon("arrow")}</a></li>'
    tl = "".join(f'<li><a href="/tools/{t[0]}/"><span class="mi">{icon(t[3])}</span><span><strong>{t[2]}</strong></span></a></li>' for t in TOOLS)
    tl += f'<li><a class="menu-all" href="/tools/">All free tools {icon("arrow")}</a></li>'
    return f"""<ul class="nav" id="nav">
<li class="has-menu"><button class="nav-link" aria-expanded="false" aria-controls="m-res">Moving Resources {icon("chev", "icon chev")}</button><ul class="menu mega" id="m-res">{res}</ul></li>
<li class="has-menu"><button class="nav-link" aria-expanded="false" aria-controls="m-tools">Tools {icon("chev", "icon chev")}</button><ul class="menu" id="m-tools">{tl}</ul></li>
<li><a class="nav-link" href="/courses/"{cur("/courses/")}>Courses</a></li>
<li><a class="nav-link" href="/blog/"{cur("/blog/")}>Blog</a></li>
<li><a class="nav-link" href="/shop/"{cur("/shop/")}>Shop</a></li>
<li><a class="nav-link" href="/contact-us/"{cur("/contact-us/")}>Contact</a></li>
<li class="nav-cta"><a class="btn sm" href="/tools/">{icon("calculator")} Free Tools</a></li>
</ul>"""


def header(current):
    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
<div class="topbar">Moving Made Easy courses — just $20 each. <a href="/courses/">Check out our courses →</a></div>
<header class="site-header"><div class="wrap nav-row">
<a class="brand" href="/" aria-label="{SITE} home"><img src="/assets/img/connected-renter-logo.png" alt="{SITE} — {TAGLINE}" width="524" height="139"></a>
{nav(current)}
<button class="search-btn" type="button" data-open-search aria-label="Search the site">{icon("search")}<span class="lbl">Search</span><kbd>Ctrl K</kbd></button>
<button class="menu-btn" type="button" aria-label="Menu" aria-expanded="false" aria-controls="nav">{icon("menu")}</button>
</div></header>"""


def footer():
    res = "".join(f'<li><a href="/moving-resources/{r["slug"]}/">{r["name"]}</a></li>' for r in RESOURCES)
    tl = "".join(f'<li><a href="/tools/{t[0]}/">{t[2]}</a></li>' for t in TOOLS)
    return f"""<footer class="site-footer">
<div class="wrap foot-grid">
<div class="foot-brand"><img src="/assets/img/connected-renter-logo-white.png" alt="{SITE}" width="524" height="139" loading="lazy">
<p>The free resource hub for renters — finding a place, moving, utilities, insurance, credit and everything in between.</p>
<form class="newsletter" data-mailto="{EMAIL}" data-subject="Subscribe me to Connected Renter updates"><label class="sr-only" for="nl-email">Email address</label><input id="nl-email" type="email" name="email" placeholder="Your email" required><button class="btn gold sm" type="submit">Subscribe</button><div class="form-msg">Thanks! Your email app should open to confirm.</div></form>
</div>
<div><h4>Moving Resources</h4><ul>{res}<li><a href="/landing/">Renter Roadmap</a></li></ul></div>
<div><h4>Free Tools</h4><ul>{tl}</ul></div>
<div><h4>Get in Touch</h4><ul class="foot-contact">
<li>{icon("phone")}<a href="tel:{PHONE_HREF}">{PHONE}</a></li>
<li>{icon("mail")}<a href="mailto:{EMAIL}">{EMAIL}</a></li>
<li>{icon("map-pin")}<span>{ADDRESS[0]}, {ADDRESS[1]}, {ADDRESS[2]} {ADDRESS[3]}, USA</span></li>
</ul>
<h4 style="margin-top:24px">Company</h4><ul><li><a href="/about-us/">About</a></li><li><a href="/courses/">Courses</a></li><li><a href="/blog/">Blog</a></li><li><a href="/shop/">Shop</a></li><li><a href="/contact-us/">Contact</a></li></ul></div>
</div>
<div class="wrap foot-word" aria-hidden="true">Connected Renter</div>
<div class="wrap foot-bottom"><span>Copyright © <span data-year>{date.today().year}</span> {SITE}. All Rights Reserved.</span>
<nav aria-label="Legal"><a href="/privacy-policy/">Privacy Policy</a><a href="/terms-of-use/">Terms of Use</a><a href="/sitemap.xml">Sitemap</a></nav></div>
</footer>
<button class="to-top" type="button" aria-label="Back to top">{icon("arrow-up")}</button>
<div class="palette" role="dialog" aria-modal="true" aria-label="Search Connected Renter"><div class="palette-box">
<div class="palette-in">{icon("search")}<input type="search" placeholder="Search resources, tools and guides…" aria-label="Search"><kbd class="note">Esc</kbd></div>
<div class="palette-list"></div></div></div>"""


def page(path, title, desc, main, current=None, schema=None, og_type="website", og_image=None, tools=False, extra_head=""):
    canon = ORIGIN + path
    graph = [ORG, WEBSITE] + (schema or [])
    img = ORIGIN + (og_image or "/assets/img/og-default.png")
    tools_js = f'<script src="/assets/js/tools.js?v={VER}" defer></script>' if tools else ""
    doc = f"""<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:site_name" content="{SITE}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{img}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{img}">
<meta name="theme-color" content="#680404">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="/favicon-48.png" sizes="48x48">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&family=Sora:wght@600;700;800&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={VER}">
{extra_head}{ld({"@context": "https://schema.org", "@graph": graph})}
</head>
<body>
{sprite()}
{header(current)}
<main id="main">
{main}
</main>
{footer()}
<script src="/assets/js/search-index.js?v={VER}" defer></script>
<script src="/assets/js/site.js?v={VER}" defer></script>
{tools_js}
</body>
</html>
"""
    out = os.path.join(ROOT, "home.html" if path == "/" else path.strip("/") + "/index.html") if not path.endswith(".html") else os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    return doc


def blobs():
    return '<div class="fx" aria-hidden="true"><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div><div class="grid-bg"></div></div>'


def page_hero(trail, h1, lead, ic=None, meta=""):
    cr = " / ".join(f'<a href="{u}">{esc(n)}</a>' for n, u in trail[:-1]) + f" / <span>{esc(trail[-1][0])}</span>"
    ico = f'<div class="hero-ico glass float" aria-hidden="true">{icon(ic)}</div>' if ic else ""
    return f"""<section class="page-hero">{blobs()}<div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb">{cr}</nav>
<h1>{h1}</h1><p class="lead">{lead}</p>{meta}</div>{ico}</section>"""


def faq_html(faqs, title="Frequently asked questions"):
    items = "".join(f'<details><summary>{esc(q)}</summary><div class="ans"><p>{esc(a)}</p></div></details>' for q, a in faqs)
    return f'<h2 id="faq">{title}</h2><div class="faq">{items}</div>'


def toc(body, extra=()):
    hs = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body)
    hs += list(extra)
    links = "".join(f'<li><a href="#{i}">{re.sub("<[^>]+>", "", t)}</a></li>' for i, t in hs)
    return f'<div class="side-box toc"><h3>On this page</h3><ul>{links}</ul></div>'


def cta_band(title="Make your next move the easy one.", text="Free tools and step-by-step guides for every part of renting — all in one place.", primary=("Explore free tools", "/tools/"), secondary=("Browse resources", "/moving-resources/")):
    return f"""<section class="section tight"><div class="wrap"><div class="cta-band reveal">{blobs()}
<div><span class="eyebrow dark">{icon("rocket")} Connected Renter</span><h2>{title}</h2><p>{text}</p></div>
<div class="actions"><a class="btn gold" href="{primary[1]}">{primary[0]} {icon("arrow", "icon arrow")}</a><a class="btn light" href="{secondary[1]}">{secondary[0]}</a></div>
</div></div></section>"""


def resource_card(r, i=0):
    return f"""<a class="card link-card reveal d{i % 4}" href="/moving-resources/{r['slug']}/"><span class="ico">{icon(r['icon'])}</span><h3>{r['name']}</h3><p>{esc(r['short'])}</p><span class="more">Read more {icon('arrow')}</span></a>"""


def tool_card(t, i=0, dark=False):
    return f"""<a class="card link-card{' dark' if dark else ''} reveal d{i % 4}" href="/tools/{t[0]}/"><span class="tag">Free</span><span class="ico">{icon(t[3])}</span><h3>{t[2]}</h3><p>{esc(t[4])}</p><span class="more">Open tool {icon('arrow')}</span></a>"""


def fmt_date(d):
    return date.fromisoformat(d).strftime("%b %-d, %Y")


def post_card(p, i=0):
    thumb = (f'<div class="thumb"><img src="/assets/img/{p["img"]}" alt="{esc(p["title"])}" width="500" height="330" loading="lazy"></div>' if p.get("img")
             else f'<div class="thumb art">{icon(p["icon"])}</div>')
    return f"""<article class="card post-card reveal d{i % 4}" data-cat="{p['cat']}">{thumb}<div class="body">
<div class="date"><span>{fmt_date(p['date'])}</span><span>{CATS[p['cat']]}</span></div>
<h3><a href="{p['path']}">{esc(p['title'])}</a></h3><p>{esc(p['excerpt'])}</p><span class="more">Read article {icon('arrow')}</span></div></article>"""


def sorted_posts():
    return sorted(POSTS, key=lambda p: p["date"], reverse=True)


# ------------------------------------------------------------------ home

def build_home():
    res_cards = "".join(resource_card(r, i) for i, r in enumerate(RESOURCES))
    marquee_items = "".join(f'<a href="/moving-resources/{r["slug"]}/"><span class="dot"></span>{r["name"]}</a>' for r in RESOURCES)
    journey = [
        ("Find", "Find the right place", "Know your budget, search smarter and apply with confidence.", ["Set a realistic budget with the 30% and 3× income rules", "Use a free apartment locator to surface specials", "Tour with a checklist and read the whole lease"], [("Apartment Locator", "/moving-resources/apartment-locator/"), ("Affordability calculator", "/tools/rent-affordability-calculator/"), ("5 steps to your perfect apartment", "/5-easy-steps-to-find-your-perfect-apartment/")]),
        ("Plan", "Plan the move", "Pick the right way to move and put every task on a calendar.", ["Compare DIY, movers and containers", "Get a dated checklist for the next eight weeks", "Order the right number of boxes"], [("Moving checklist", "/tools/moving-checklist/"), ("Moving cost calculator", "/tools/moving-cost-calculator/"), ("Packing calculator", "/tools/packing-calculator/")]),
        ("Move", "Move day, done right", "Book the help you need and protect your stuff on the road.", ["Vet movers and avoid moving scams", "Pick the right truck size and drive it safely", "Book move-out cleaning to protect your deposit"], [("Movers", "/moving-resources/movers/"), ("Moving Truck Rentals", "/moving-resources/moving-truck-rentals/"), ("Maid Services", "/moving-resources/maid-services/")]),
        ("Connect", "Connect your home", "Lights, water and Wi-Fi on before you arrive, furniture that fits.", ["Schedule utilities two to three weeks out", "Compare electricity plans and estimate the bill", "Furnish on any budget"], [("Utility Connections", "/moving-resources/utility-connections/"), ("Electricity", "/moving-resources/electricity/"), ("Furniture", "/moving-resources/furniture/")]),
        ("Protect", "Protect & build", "Insure what you own, know your rights and turn rent into credit.", ["Get the right renters insurance coverage", "Understand ESA letters and fair housing rights", "Report rent and repair your credit"], [("Rental Insurance", "/moving-resources/rental-insurance/"), ("Credit Rent Boost", "/moving-resources/credit-rent-boost/"), ("Credit Repair", "/moving-resources/credit-repair/")]),
    ]
    tabs = "".join(f'<button class="tab" role="tab" id="tab-{i}" aria-controls="panel-{i}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}"><span class="num">{i + 1}</span>{k}</button>' for i, (k, *_r) in enumerate(journey))
    panels = ""
    for i, (k, t, d, pts, links) in enumerate(journey):
        lis = "".join(f"<li>{icon('check-circle')}<span>{p}</span></li>" for p in pts)
        ls = "".join(f'<a class="btn sm {"" if j == 0 else "ghost"}" href="{u}">{n}</a>' for j, (n, u) in enumerate(links))
        panels += f'<div class="panel" role="tabpanel" id="panel-{i}" aria-labelledby="tab-{i}"{"" if i == 0 else " hidden"}><span class="eyebrow">Step {i + 1} · {k}</span><h3 style="font-size:1.6rem">{t}</h3><p class="lead">{d}</p><ul>{lis}</ul><div class="panel-links">{ls}</div></div>'
    other_tools = "".join(tool_card(t, i, dark=True) for i, t in enumerate(TOOLS) if t[1] != "affordability")
    posts = "".join(post_card(p, i) for i, p in enumerate(sorted_posts()[:3]))
    faqs = [
        ("What is Connected Renter?", "Connected Renter is a free resource hub for renters. We bring together guides, checklists and calculators for every stage of renting — finding an apartment, moving, setting up utilities, insurance, credit and more."),
        ("Is Connected Renter free to use?", "Yes. Every Connected Renter guide and tool is free, with no sign-up. Our Moving Made Easy courses are optional and cost $20 each."),
        ("Who is Connected Renter for?", "Anyone who rents: first-time renters, families relocating, students, roommates and anyone rebuilding credit or planning a move."),
        ("Does Connected Renter sell my information?", "No. The tools run in your browser and checklists save only on your device. See our privacy policy for details."),
    ]
    main = f"""
<section class="hero">{blobs()}
<div class="wrap hero-grid">
<div>
<span class="eyebrow dark">{icon("sparkles")} Connected Renter · {TAGLINE}</span>
<h1 class="hero-title">Moving Made <span class="big grad-text">EASY.</span></h1>
<p class="lead">Connected Renter is the free, all-in-one resource for renters. Find an apartment, plan the move, connect utilities, protect your stuff and build credit — every guide and tool a renter needs, connected in one place.</p>
<div class="finder"><label for="finder-q">What do you need help with?</label>
<div class="finder-box">{icon("search")}<input id="finder-q" type="text" placeholder="Try “movers”, “renters insurance” or “credit”" autocomplete="off"><a class="btn sm gold" href="/moving-resources/">Browse all</a></div>
<div class="finder-results" role="listbox"></div></div>
<div class="chips"><a class="chip" href="/moving-resources/apartment-locator/">Find an apartment</a><a class="chip" href="/tools/moving-cost-calculator/">Moving costs</a><a class="chip" href="/moving-resources/rental-insurance/">Renters insurance</a><a class="chip" href="/moving-resources/esa-letters/">ESA letters</a><a class="chip" href="/moving-resources/credit-rent-boost/">Build credit</a></div>
</div>
<div class="hero-visual" aria-hidden="true">
<div class="glass hv-main float"><h3>{icon("clipboard")} Move checklist · 4 weeks out</h3>
<div class="hv-row"><span class="tick">{icon("check")}</span>Book movers<span>Done</span></div>
<div class="hv-row"><span class="tick">{icon("check")}</span>Renters insurance<span>Done</span></div>
<div class="hv-row"><span class="tick">{icon("check")}</span>Order boxes<span>Done</span></div>
<div class="hv-row"><span class="tick off"></span>Schedule internet install<span>Due Fri</span></div>
<div class="hv-row"><span class="tick off"></span>Set up electricity<span>2 wks</span></div>
<div class="hv-bar"><i></i></div></div>
<div class="glass hv-chip c1 float d2"><span class="ico">{icon("calculator")}</span><div><small>You can afford</small><b>$1,450/mo</b></div></div>
<div class="glass hv-chip c2 float d3"><span class="ico">{icon("trending-up")}</span><div><small>Rent reported</small><b>+12 months</b></div></div>
</div>
</div>
<svg class="wave" viewBox="0 0 1440 70" preserveAspectRatio="none" aria-hidden="true"><path d="M0 40c240 30 480 30 720 0s480-30 720 0v30H0z" fill="#fffaf1"/></svg>
</section>

<div class="wrap"><div class="stats">
<div class="stat reveal"><b data-count="{len(RESOURCES)}">{len(RESOURCES)}</b><span>renter resource guides</span></div>
<div class="stat reveal d1"><b data-count="{len(TOOLS)}">{len(TOOLS)}</b><span>free interactive tools</span></div>
<div class="stat reveal d2"><b data-count="{len(POSTS)}">{len(POSTS)}</b><span>in-depth articles</span></div>
<div class="stat reveal d3"><b data-count="0" data-prefix="$">$0</b><span>to use — no sign-up</span></div>
</div></div>

<section class="section" id="resources"><div class="wrap">
<div class="sec-head center reveal"><span class="eyebrow">{icon("box")} Moving Support</span>
<h2>Everything a renter needs, <span class="grad-text">connected</span></h2>
<p class="lead">Moving can be stressful, especially if you have to do it alone. Connected Renter brings every moving support service into one place — so you spend less time searching and more time settling in.</p></div>
<div class="grid g4">{res_cards}
<a class="card link-card reveal d3" href="/landing/" style="background:var(--grad-deep);color:#f4dcd6;border:0"><span class="ico" style="background:rgba(255,255,255,.12);border-color:rgba(255,255,255,.25);color:#fff">{icon("compass")}</span><h3 style="color:#fff">Renter Roadmap</h3><p style="color:#efd2cb">New here? Start with the step-by-step path from search to settled.</p><span class="more" style="color:var(--gold-2)">Start here {icon('arrow')}</span></a>
</div></div></section>

<div class="marquee" aria-label="Moving resources"><div class="marquee-track">{marquee_items}{marquee_items.replace('<a ', '<a tabindex="-1" aria-hidden="true" ')}</div></div>

<section class="section alt"><div class="wrap">
<div class="sec-head reveal"><span class="eyebrow">{icon("compass")} The Connected Renter roadmap</span>
<h2>Five steps from “just looking” to “home sweet home”</h2>
<p class="lead">Pick where you are in your rental journey and the Connected Renter roadmap shows you exactly what to do next.</p></div>
<div class="journey reveal"><div class="tabs" role="tablist" aria-label="Renter journey">{tabs}</div><div>{panels}</div></div>
</div></section>

<section class="section"><div class="wrap split">
<div class="reveal"><span class="eyebrow">{icon("calculator")} Try it now</span>
<h2>How much rent can you <span class="grad-text">really</span> afford?</h2>
<p class="lead">Slide the rent and watch the verdict change. This is one of nine free Connected Renter tools — no sign-up, no email required, and nothing leaves your browser.</p>
<ul class="checklist"><li>{icon("check")}<span>Checks the 30% rule, 40× rule and your debt-to-income</span></li><li>{icon("check")}<span>Tells you if you'll pass the landlord's 3× income test</span></li><li>{icon("check")}<span>Works on your phone, right at the leasing office</span></li></ul>
<a class="btn" href="/tools/">See all free tools {icon("arrow", "icon arrow")}</a></div>
<div class="reveal d1">{render_tool("affordability", "-home")}</div>
</div></section>

<section class="section dark" style="overflow:hidden">{blobs()}<div class="wrap">
<div class="sec-head reveal"><span class="eyebrow dark">{icon("sparkles")} Free renter tools</span>
<h2>Calculators and checklists that do the math for you</h2>
<p class="lead">From truck sizes to rent splits, every Connected Renter tool turns a stressful decision into a two-minute answer.</p></div>
<div class="grid g4">{other_tools}</div></div></section>

<section class="section"><div class="wrap">
<div class="sec-head center reveal"><span class="eyebrow">{icon("cap")} Moving Made Easy courses</span>
<h2>Learn it once. Move like a pro forever.</h2>
<p class="lead">Short, practical video courses from Connected Renter — just $20 each.</p></div>
<div class="grid g3">{courses_cards(short=True)}</div>
<div class="center" style="margin-top:32px"><a class="btn ghost" href="/courses/">View all courses {icon("arrow", "icon arrow")}</a></div>
</div></section>

<section class="section alt"><div class="wrap split rev">
<div class="reveal"><div class="product-img" style="max-width:440px;margin:auto"><img src="/assets/img/connected-renter-tshirt.webp" alt="Connected Renter short sleeve t-shirt in black" width="300" height="300" loading="lazy"></div></div>
<div class="reveal d1"><span class="eyebrow">{icon("tshirt")} Check out our merch</span>
<h2>Rep the Connected Renter crew</h2>
<p class="lead">Our soft, fitted short sleeve tee — perfect for moving day (it hides the dust). From $18.00.</p>
<a class="btn" href="/shop/">Visit shop {icon("arrow", "icon arrow")}</a></div>
</div></section>

<section class="section"><div class="wrap">
<div class="sec-head reveal" style="display:flex;justify-content:space-between;align-items:flex-end;gap:20px;flex-wrap:wrap;max-width:none"><div><span class="eyebrow">{icon("news")} Latest</span><h2>News &amp; Trends</h2><p class="lead">Get the latest renter guides and moving tips from the Connected Renter blog.</p></div><a class="btn ghost" href="/blog/">Read more blogs {icon("arrow", "icon arrow")}</a></div>
<div class="grid g3">{posts}</div></div></section>

<section class="section alt"><div class="wrap split">
<div class="reveal"><span class="eyebrow">{icon("heart")} Why Connected Renter</span>
<h2>Built for renters, not landlords</h2>
<p class="lead">Renting comes with a hundred small decisions and nobody hands you a manual. Connected Renter is that manual — written in plain English and kept up to date.</p>
<ul class="checklist">
<li>{icon("check")}<span><strong>Everything in one place.</strong> Eleven moving resources, nine tools and a growing library of guides.</span></li>
<li>{icon("check")}<span><strong>Honest and independent.</strong> We explain your options and the red flags, including the free ones.</span></li>
<li>{icon("check")}<span><strong>Private by design.</strong> Our tools run in your browser — your numbers stay with you.</span></li>
<li>{icon("check")}<span><strong>Texas roots, nationwide help.</strong> Connected Renter started in Southlake, TX and serves renters everywhere.</span></li>
</ul></div>
<div class="reveal d1">{faq_html(faqs, "Connected Renter FAQ")}</div>
</div></section>

{cta_band("Ready for your easiest move yet?", "Join the renters who use Connected Renter to find, move, connect and protect — for free.")}
"""
    page("/", "Connected Renter | Moving Made Easy — Every Renter Resource in One Place",
         "Connected Renter is the free hub for renters: apartment locating, movers, truck rentals, utilities, renters insurance, ESA letters, credit help and 9 free tools.",
         main, current="/", tools=True, schema=[faq_ld(faqs)])
    PAGES.append(("/", TODAY, "1.0"))


# ------------------------------------------------------------------ resources

def build_resources():
    cards = "".join(resource_card(r, i) for i, r in enumerate(RESOURCES))
    main = page_hero([("Home", "/"), ("Moving Resources", "/moving-resources/")], "Moving Resources for Renters",
                     "Eleven in-depth guides covering every service you'll need when you rent and move — from finding the apartment to building credit with your rent.", "box")
    main += f"""<section class="section"><div class="wrap"><div class="grid g3">{cards}
<a class="card link-card reveal" href="/landing/"><span class="ico">{icon("compass")}</span><h3>Renter Roadmap</h3><p>See how every resource fits together, step by step.</p><span class="more">Start here {icon("arrow")}</span></a></div></div></section>
<section class="section alt"><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">{icon("calculator")} Pair them with</span><h2>Free renter tools</h2></div>
<div class="grid g3">{"".join(tool_card(t, i) for i, t in enumerate(TOOLS[:6]))}</div></div></section>{cta_band()}"""
    page("/moving-resources/", "Moving Resources for Renters | Connected Renter",
         "Guides to apartment locators, cleaners, movers, truck rentals, rent reporting, furniture, electricity, credit repair, renters insurance, ESA letters and utilities.",
         main, schema=[crumbs_ld([("Home", "/"), ("Moving Resources", "/moving-resources/")]),
                       {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{ORIGIN}/moving-resources/{r['slug']}/", "name": r["name"]} for i, r in enumerate(RESOURCES)]}])
    PAGES.append(("/moving-resources/", TODAY, "0.9"))

    for r in RESOURCES:
        path = f"/moving-resources/{r['slug']}/"
        body = fill(r["body"])
        tool_html = ""
        extra_toc = []
        if r["tool"]:
            t = next(x for x in TOOLS if x[1] == r["tool"])
            tool_html = f'<h2 id="tool">Free tool: {t[2]}</h2><p>{t[7]}</p>{render_tool(r["tool"])}'
            extra_toc.append(("tool", f"Free tool: {t[2]}"))
        extra_toc.append(("faq", "FAQ"))
        mins = max(3, math.ceil(words(body) / 220))
        side_links = "".join(f'<li><a href="/moving-resources/{x["slug"]}/"{" aria-current=page" if x is r else ""}>{icon(x["icon"])}{x["name"]}</a></li>' for x in RESOURCES)
        tool_link = f'/tools/{next(x[0] for x in TOOLS if x[1] == r["tool"])}/' if r["tool"] else "/tools/"
        others = [x for x in RESOURCES if x is not r]
        idx = RESOURCES.index(r)
        rel = [others[(idx + k) % len(others)] for k in range(3)]
        meta = f'<div class="meta-row"><span>{icon("clock")} {mins} min read</span><span>{icon("calendar")} Updated {date.fromisoformat(TODAY).strftime("%B %Y")}</span><span>{icon("check-circle")} Free resource</span></div>'
        main = page_hero([("Home", "/"), ("Moving Resources", "/moving-resources/"), (r["name"], path)], r["h1"], r["lead"], r["icon"], meta)
        main += f"""<section class="section"><div class="wrap content-grid">
<article class="prose">{body}{tool_html}{faq_html(r["faqs"])}</article>
<aside class="sidebar">{toc(body, extra_toc)}
<div class="side-box"><h3>Moving resources</h3><ul>{side_links}</ul></div>
<div class="side-box cta"><h3>Run the numbers</h3><p>Free calculators for rent, moving costs, insurance and more.</p><a class="btn gold sm" href="{tool_link}">Open the tool {icon("arrow", "icon arrow")}</a></div>
</aside></div></section>
<section class="section alt tight"><div class="wrap"><h2 class="reveal">Related resources</h2><div class="grid g3">{"".join(resource_card(x, i) for i, x in enumerate(rel))}</div></div></section>
{cta_band()}"""
        schema = [crumbs_ld([("Home", "/"), ("Moving Resources", "/moving-resources/"), (r["name"], path)]), faq_ld(r["faqs"]),
                  {"@type": "Article", "headline": r["h1"], "description": r["desc"], "dateModified": TODAY, "datePublished": "2023-07-02",
                   "author": {"@id": ORIGIN + "/#org"}, "publisher": {"@id": ORIGIN + "/#org"}, "mainEntityOfPage": ORIGIN + path, "image": ORIGIN + "/assets/img/og-default.png"}]
        page(path, r["seo_title"] + " | Connected Renter", r["desc"], main, schema=schema, og_type="article", tools=bool(r["tool"]))
        PAGES.append((path, TODAY, "0.8"))


# ------------------------------------------------------------------ tools

def build_tools():
    main = page_hero([("Home", "/"), ("Tools", "/tools/")], "Free Tools for Renters",
                     "Calculators, planners and checklists that answer the big renting questions in minutes. No sign-up, and everything runs privately in your browser.", "calculator")
    main += f"""<section class="section"><div class="wrap"><div class="grid g3">{"".join(tool_card(t, i) for i, t in enumerate(TOOLS))}</div></div></section>
<section class="section alt"><div class="wrap split"><div class="reveal"><span class="eyebrow">{icon("calculator")} Featured</span><h2>Start with your budget</h2><p class="lead">Every good rental decision starts with knowing what you can comfortably pay. Try the calculator right here.</p></div><div class="reveal d1">{render_tool("affordability")}</div></div></section>{cta_band("Need the full picture?", "Pair each tool with an in-depth Connected Renter guide.", ("Browse resources", "/moving-resources/"), ("Read the blog", "/blog/"))}"""
    page("/tools/", "Free Renter Tools & Calculators | Connected Renter",
         "Free renter tools: rent affordability, moving cost, truck size, packing, rent split, insurance and electricity calculators, plus moving and inspection checklists.",
         main, tools=True, schema=[crumbs_ld([("Home", "/"), ("Tools", "/tools/")])])
    PAGES.append(("/tools/", TODAY, "0.9"))

    for slug, key, name, ic, short, seo, desc, intro, how, faqs in TOOLS:
        path = f"/tools/{slug}/"
        others = [t for t in TOOLS if t[0] != slug][:3]
        main = page_hero([("Home", "/"), ("Tools", "/tools/"), (name, path)], name, intro, ic)
        main += f"""<section class="section tight"><div class="wrap">{render_tool(key)}</div></section>
<section class="section tight"><div class="wrap content-grid"><article class="prose"><h2 id="how">How this tool works</h2>{how}{faq_html(faqs)}</article>
<aside class="sidebar"><div class="side-box"><h3>More free tools</h3><ul>{"".join(f'<li><a href="/tools/{t[0]}/">{icon(t[3])}{t[2]}</a></li>' for t in TOOLS if t[0] != slug)}</ul></div></aside></div></section>
<section class="section alt tight"><div class="wrap"><h2 class="reveal">Try another tool</h2><div class="grid g3">{"".join(tool_card(t, i) for i, t in enumerate(others))}</div></div></section>"""
        schema = [crumbs_ld([("Home", "/"), ("Tools", "/tools/"), (name, path)]), faq_ld(faqs),
                  {"@type": "WebApplication", "name": name, "url": ORIGIN + path, "description": desc, "applicationCategory": "FinanceApplication",
                   "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "publisher": {"@id": ORIGIN + "/#org"}}]
        page(path, seo + " | Connected Renter", desc, main, tools=True, schema=schema)
        PAGES.append((path, TODAY, "0.8"))


# ------------------------------------------------------------------ blog

def build_blog():
    ps = sorted_posts()
    filters = '<div class="filters" role="group" aria-label="Filter by category"><button type="button" data-filter="all" aria-pressed="true">All</button>' + "".join(
        f'<button type="button" data-filter="{k}" aria-pressed="false">{v}</button>' for k, v in CATS.items()) + "</div>"
    main = page_hero([("Home", "/"), ("Blog", "/blog/")], "The Connected Renter Blog", "Get the latest news, trends and how-to guides about renting and moving.", "news")
    main += f'<section class="section"><div class="wrap">{filters}<div class="grid g3">{"".join(post_card(p, i) for i, p in enumerate(ps))}</div></div></section>{cta_band()}'
    page("/blog/", "Renter Blog: Moving Tips, Guides & Trends | Connected Renter",
         "Renter guides and moving tips from Connected Renter: DIY moves, finding an apartment, budgeting, credit, security deposits, tenant rights and more.",
         main, current="/blog/", schema=[crumbs_ld([("Home", "/"), ("Blog", "/blog/")]),
                                         {"@type": "Blog", "name": "Connected Renter Blog", "url": ORIGIN + "/blog/", "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": ORIGIN + p["path"], "datePublished": p["date"]} for p in ps]}])
    PAGES.append(("/blog/", TODAY, "0.8"))

    for p in POSTS:
        body = fill(p["body"])
        mins = max(3, math.ceil(words(body) / 220))
        lede = f'<img class="lede-img" src="/assets/img/{p["img"]}" alt="{esc(p["title"])}" width="500" height="330">' if p.get("img") else ""
        upd = p.get("updated")
        upd_html = f'<span>{icon("refresh")} Updated {fmt_date(upd)}</span>' if upd else ""
        meta = f'<div class="meta-row"><span>{icon("calendar")} {fmt_date(p["date"])}</span>{upd_html}<span>{icon("clock")} {mins} min read</span><span>{icon("book")} {CATS[p["cat"]]}</span></div>'
        rel = [x for x in sorted_posts() if x is not p and x["cat"] == p["cat"]][:3]
        rel += [x for x in sorted_posts() if x is not p and x not in rel][:3 - len(rel)]
        main = page_hero([("Home", "/"), ("Blog", "/blog/"), (p["title"], p["path"])], esc(p["title"]), esc(p["excerpt"]), p["icon"], meta)
        main += f"""<section class="section"><div class="wrap content-grid">
<article class="prose">{lede}{body}<p class="note" style="margin-top:2em">By the Connected Renter team. General information only — not legal or financial advice.</p></article>
<aside class="sidebar">{toc(body)}
<div class="side-box"><h3>Popular tools</h3><ul>{"".join(f'<li><a href="/tools/{t[0]}/">{icon(t[3])}{t[2]}</a></li>' for t in TOOLS[:5])}</ul></div>
<div class="side-box cta"><h3>New to renting?</h3><p>Follow the Renter Roadmap from search to settled.</p><a class="btn gold sm" href="/landing/">Start here {icon("arrow", "icon arrow")}</a></div>
</aside></div></section>
<section class="section alt tight"><div class="wrap"><h2 class="reveal">Keep reading</h2><div class="grid g3">{"".join(post_card(x, i) for i, x in enumerate(rel))}</div></div></section>"""
        img = "/assets/img/" + p["img"] if p.get("img") else "/assets/img/og-default.png"
        schema = [crumbs_ld([("Home", "/"), ("Blog", "/blog/"), (p["title"], p["path"])]),
                  {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": upd or p["date"],
                   "author": {"@type": "Organization", "name": SITE, "url": ORIGIN + "/"}, "publisher": {"@id": ORIGIN + "/#org"},
                   "image": ORIGIN + img, "mainEntityOfPage": ORIGIN + p["path"], "articleSection": CATS[p["cat"]]}]
        has_tool = "__TOOL_" in p["body"]
        page(p["path"], p["seo_title"] + " | Connected Renter", p["desc"], main, og_type="article", og_image=img, schema=schema, tools=has_tool,
             extra_head=f'<meta property="article:published_time" content="{p["date"]}">\n')
        PAGES.append((p["path"], upd or p["date"], "0.7"))


# ------------------------------------------------------------------ courses / shop

COURSES = [
    ("moving-made-easy-diy-move", "Moving Made Easy: The DIY Move Masterclass", "truck", "Beginner", "8 lessons · ~90 min",
     "Plan, pack, load and drive your own move — and save hundreds compared with full-service movers.",
     ["Budgeting a DIY move and choosing the right truck", "Packing systems: labels, box sizes and the 'open first' box", "Loading a truck so nothing shifts or breaks", "Driving a box truck safely", "Unloading and settling in fast"]),
    ("first-apartment-bootcamp", "First Apartment Bootcamp", "key", "Beginner", "7 lessons · ~75 min",
     "Everything first-time renters wish they knew: budgets, applications, leases and move-in day.",
     ["Setting a realistic rent budget", "Touring like a pro and spotting red flags", "Applications, credit checks and guarantors", "Reading your lease line by line", "Move-in inspections that protect your deposit"]),
    ("credit-and-rent", "Credit & Rent: Build Your Score While You Rent", "trending-up", "All levels", "6 lessons · ~60 min",
     "Turn your biggest monthly bill into credit history and get approved for better places.",
     ["How credit scores and tenant screening work", "Rent reporting: options, costs and results", "Disputing credit report errors yourself", "Secured cards and credit-builder loans", "A 90-day credit action plan"]),
]


def courses_cards(short=False):
    out = ""
    for i, (slug, title, ic, lvl, dur, desc, mods) in enumerate(COURSES):
        mods_html = "" if short else "<ul>" + "".join(f"<li>{icon('check')}<span>{m}</span></li>" for m in mods) + "</ul>"
        btn = (f'<a class="btn{"" if i == 0 else " ghost"}" href="/courses/#{slug}">View course {icon("arrow", "icon arrow")}</a>' if short else
               f'<a class="btn{"" if i == 0 else " ghost"}" href="mailto:{EMAIL}?subject={esc("Enroll me: " + title)}">Reserve my spot {icon("arrow", "icon arrow")}</a>')
        out += f"""<div class="card course-card reveal d{i}{" featured" if i == 0 else ""}" id="{slug}">{'<span class="tag">Most popular</span>' if i == 0 else ''}<span class="ico">{icon(ic)}</span>
<p class="note" style="margin:0 0 6px">Course #{i + 1}</p><h3>{title}</h3><div class="lvl"><span>{icon("cap")} {lvl}</span><span>{icon("clock")} {dur}</span></div>
<p>{desc}</p>{mods_html}<div class="price">$20 <small>one-time</small></div><div style="margin-top:14px">{btn}</div></div>"""
    return out


def build_courses():
    main = page_hero([("Home", "/"), ("Courses", "/courses/")], "Moving Made Easy Courses",
                     "A variety of short, practical courses that take the stress out of renting and moving — just $20 each.", "cap")
    main += f"""<section class="section"><div class="wrap"><div class="grid g3">{courses_cards()}</div>
<div class="callout" style="margin-top:40px">{icon("info")}<div><p><strong>How enrollment works:</strong> tap “Reserve my spot” to email us, and we'll reply with access details and payment options. Questions? <a href="/contact-us/">Contact us</a>.</p></div></div></div></section>
<section class="section alt"><div class="wrap split"><div class="reveal"><span class="eyebrow">{icon("star")} Why take a course?</span><h2>Free guides tell you what. Courses show you how.</h2>
<ul class="checklist"><li>{icon("check")}<span>Step-by-step video lessons you can watch on your phone</span></li><li>{icon("check")}<span>Printable checklists and templates with every course</span></li><li>{icon("check")}<span>Lifetime access, including future updates</span></li></ul></div>
<div class="reveal d1">{faq_html([("How much do the courses cost?", "Each Moving Made Easy course is $20, one time."), ("Do I need any experience?", "No. The courses are designed for first-time renters and movers."), ("Is there a refund policy?", "If a course isn't helpful, contact us within 14 days of purchase for a refund.")], "Course FAQ")}</div></div></section>"""
    schema = [crumbs_ld([("Home", "/"), ("Courses", "/courses/")])] + [
        {"@type": "Course", "name": t, "description": d, "url": f"{ORIGIN}/courses/#{s}", "provider": {"@id": ORIGIN + "/#org"},
         "offers": {"@type": "Offer", "price": "20.00", "priceCurrency": "USD", "category": "Paid"}} for s, t, _i, _l, _d, d, _m in COURSES]
    page("/courses/", "Moving Made Easy Courses ($20) | Connected Renter",
         "Short, practical Moving Made Easy courses for renters — DIY moves, first apartments and building credit while you rent. $20 each.", main, current="/courses/", schema=schema)
    PAGES.append(("/courses/", TODAY, "0.7"))


def build_shop():
    sizes = ["S", "M", "L", "XL", "2XL", "3XL"]
    opts = "".join(f'<option>{s}</option>' for s in sizes)
    main = page_hero([("Home", "/"), ("Shop", "/shop/")], "Connected Renter Shop", "Looking for a cool shirt to rock? Check out our merch.", "bag")
    main += f"""<section class="section"><div class="wrap product">
<div class="product-img reveal"><img src="/assets/img/connected-renter-tshirt.webp" alt="Connected Renter men's fitted short sleeve t-shirt, black, front" width="300" height="300"></div>
<div class="reveal d1"><span class="eyebrow">Apparel</span><h2>Short Sleeve T-shirt</h2>
<div class="price">$18.00 – $22.50</div>
<p class="lead">A soft, fitted short sleeve tee with the Connected Renter logo. Lightweight, breathable and built for moving day.</p>
<ul class="checklist"><li>{icon("check")}<span>Fitted cut, crew neck</span></li><li>{icon("check")}<span>Black · sizes S–3XL (2XL and 3XL priced higher)</span></li><li>{icon("check")}<span>Printed on demand and shipped to you</span></li></ul>
<form class="form-grid" data-mailto="{EMAIL}" data-subject="Order: Connected Renter Short Sleeve T-shirt" style="margin-top:20px">
<div class="field"><label for="sz">Size</label><select id="sz" name="size" required>{opts}</select></div>
<div class="field"><label for="qty">Quantity</label><input id="qty" type="number" name="quantity" min="1" value="1" required></div>
<div class="field full"><label for="sname">Your name</label><input id="sname" type="text" name="name" required></div>
<div class="full"><button class="btn" type="submit">{icon("bag")} Order by email</button><div class="form-msg">Your email app should open with the order details. We'll reply with payment and shipping info.</div></div>
</form></div></div></section>{cta_band()}"""
    schema = [crumbs_ld([("Home", "/"), ("Shop", "/shop/")]),
              {"@type": "Product", "name": "Connected Renter Short Sleeve T-shirt", "image": ORIGIN + "/assets/img/connected-renter-tshirt.webp",
               "description": "Fitted short sleeve t-shirt with the Connected Renter logo.", "brand": {"@type": "Brand", "name": SITE},
               "offers": {"@type": "AggregateOffer", "lowPrice": "18.00", "highPrice": "22.50", "priceCurrency": "USD", "offerCount": len(sizes)}}]
    page("/shop/", "Shop Connected Renter Merch | Short Sleeve T-shirt", "Shop Connected Renter merch: our fitted short sleeve t-shirt in black, sizes S–3XL, from $18.00.", main, current="/shop/", schema=schema)
    PAGES.append(("/shop/", TODAY, "0.5"))


# ------------------------------------------------------------------ contact / about / landing / legal

def build_contact():
    main = page_hero([("Home", "/"), ("Contact", "/contact-us/")], "Get in Touch With Us", "Questions about a resource, a course or a merch order? Suggestions for a new tool? We'd love to hear from you.", "mail")
    main += f"""<section class="section"><div class="wrap contact-grid">
<div class="reveal"><h2>Contact Connected Renter</h2><p class="lead">We usually reply within one to two business days.</p>
<div class="contact-item"><span class="ico">{icon("phone")}</span><div><strong>Phone</strong><br><a href="tel:{PHONE_HREF}">{PHONE}</a></div></div>
<div class="contact-item"><span class="ico">{icon("mail")}</span><div><strong>Email</strong><br><a href="mailto:{EMAIL}">{EMAIL}</a></div></div>
<div class="contact-item"><span class="ico">{icon("map-pin")}</span><div><strong>Mailing address</strong><br>{ADDRESS[0]}<br>{ADDRESS[1]}, {ADDRESS[2]} {ADDRESS[3]}, USA</div></div>
</div>
<div class="card reveal d1"><h3>Send us a message</h3>
<form class="form-grid" data-mailto="{EMAIL}" data-subject="Connected Renter website enquiry">
<div class="field"><label for="cn">Name</label><input id="cn" type="text" name="name" autocomplete="name" required></div>
<div class="field"><label for="ce">Email</label><input id="ce" type="email" name="email" autocomplete="email" required></div>
<div class="field full"><label for="ct">Topic</label><select id="ct" name="subject"><option value="">General question</option><option>Moving resources</option><option>Courses</option><option>Shop order</option><option>Partnership / listing</option><option>Report a problem</option></select></div>
<div class="field full"><label for="cm">Message</label><textarea id="cm" name="message" required></textarea></div>
<div class="full"><button class="btn" type="submit">{icon("send")} Send message</button><div class="form-msg">Your email app should open with your message ready to send.</div></div>
</form></div></div></section>"""
    page("/contact-us/", "Contact Us | Connected Renter", "Contact Connected Renter by phone, email or our contact form with questions about renter resources, courses or merch orders.",
         main, current="/contact-us/", schema=[crumbs_ld([("Home", "/"), ("Contact", "/contact-us/")]), {"@type": "ContactPage", "url": ORIGIN + "/contact-us/", "about": {"@id": ORIGIN + "/#org"}}])
    PAGES.append(("/contact-us/", TODAY, "0.6"))


def build_about():
    main = page_hero([("Home", "/"), ("About", "/about-us/")], "About Connected Renter", "Connecting made easy — for every renter, at every step.", "heart")
    main += f"""<section class="section"><div class="wrap content-grid"><article class="prose">
<h2 id="story">Our story</h2>
<p>Connected Renter started in Southlake, Texas with a simple observation: renting involves dozens of services — locators, movers, truck rentals, cleaners, utilities, insurance, credit — and nobody connects them. Renters end up with twenty browser tabs, conflicting advice and surprise fees.</p>
<p>So we built the hub we wished we'd had. Every resource is written in plain English, every tool is free, and everything is organized around the way a move actually happens.</p>
<h2 id="believe">What we believe</h2>
<ul><li><strong>Renters deserve straight answers.</strong> We explain the options, the costs and the red flags.</li><li><strong>Free should mean free.</strong> No sign-up walls on our guides or tools.</li><li><strong>Your data is yours.</strong> Our calculators run in your browser.</li></ul>
<h2 id="editorial">How we create content</h2>
<p>Our guides are researched from official sources — such as HUD, the CFPB, the FMCSA and state agencies — and reviewed regularly. Figures like moving costs and insurance premiums are planning ranges; always confirm with providers. Our content is general information, not legal or financial advice.</p>
</article><aside class="sidebar"><div class="side-box cta"><h3>Get in touch</h3><p>Ideas for a guide or tool? We'd love to hear them.</p><a class="btn gold sm" href="/contact-us/">Contact us</a></div></aside></div></section>{cta_band()}"""
    page("/about-us/", "About Us | Connected Renter", "Connected Renter is a free resource hub for renters, founded in Southlake, Texas, connecting every guide and tool renters need in one place.",
         main, schema=[crumbs_ld([("Home", "/"), ("About", "/about-us/")]), {"@type": "AboutPage", "url": ORIGIN + "/about-us/", "about": {"@id": ORIGIN + "/#org"}}])
    PAGES.append(("/about-us/", TODAY, "0.5"))


def build_landing():
    steps = [
        ("Know your budget", "calculator", "Use the 30% rule and 3× income test to set a number you can live with.", [("Rent affordability calculator", "/tools/rent-affordability-calculator/"), ("How much rent can I afford?", "/blog/how-much-rent-can-i-afford/")]),
        ("Check & build your credit", "trending-up", "Pull your free reports, fix errors and add rent payments to your file.", [("Credit Repair", "/moving-resources/credit-repair/"), ("Credit Rent Boost", "/moving-resources/credit-rent-boost/")]),
        ("Find the right place", "map-pin", "Let a free locator find specials and tour with a checklist.", [("Apartment Locator", "/moving-resources/apartment-locator/"), ("5 steps to your perfect apartment", "/5-easy-steps-to-find-your-perfect-apartment/")]),
        ("Plan the move", "clipboard", "Get a dated checklist, compare moving options and order supplies.", [("Moving checklist", "/tools/moving-checklist/"), ("Moving cost calculator", "/tools/moving-cost-calculator/")]),
        ("Book help", "truck", "Movers, truck rentals and cleaners — vetted the right way.", [("Movers", "/moving-resources/movers/"), ("Moving Truck Rentals", "/moving-resources/moving-truck-rentals/"), ("Maid Services", "/moving-resources/maid-services/")]),
        ("Connect utilities", "plug", "Electricity, internet, water and gas on before you arrive.", [("Utility Connections", "/moving-resources/utility-connections/"), ("Electricity", "/moving-resources/electricity/")]),
        ("Protect yourself", "shield", "Renters insurance, an inspection report and knowing your rights.", [("Rental Insurance", "/moving-resources/rental-insurance/"), ("Inspection checklist", "/tools/move-in-inspection-checklist/"), ("ESA Letters", "/moving-resources/esa-letters/")]),
        ("Make it home", "sofa", "Furnish on any budget and settle in.", [("Furniture", "/moving-resources/furniture/"), ("First apartment checklist", "/blog/first-apartment-checklist/")]),
    ]
    items = ""
    for i, (t, ic, d, links) in enumerate(steps):
        ls = " ".join(f'<a href="{u}">{n}</a>' for n, u in links)
        items += f'<li class="reveal"><h3 style="margin:0 0 4px">{icon(ic)} {t}</h3><p style="margin:0 0 6px;color:var(--muted)">{d}</p><p style="margin:0" class="pill-list">{ls}</p></li>'
    main = page_hero([("Home", "/"), ("Renter Roadmap", "/landing/")], "The Renter Roadmap: Start Here",
                     "New to renting or planning a move? Follow these eight steps in order — each one links to the guide or tool you need.", "compass")
    main += f"""<section class="section"><div class="wrap" style="max-width:860px"><ol class="steps prose" style="max-width:none">{items}</ol></div></section>
<section class="section alt"><div class="wrap"><div class="sec-head reveal"><h2>Plan it all in one place</h2><p class="lead">Set your moving date and get every step on a calendar.</p></div>{render_tool("checklist")}</div></section>{cta_band()}"""
    page("/landing/", "Renter Roadmap: Your Step-by-Step Guide to Renting & Moving | Connected Renter",
         "Start here: an eight-step renter roadmap from budget and credit to finding a place, moving, utilities, insurance and settling in.",
         main, tools=True, schema=[crumbs_ld([("Home", "/"), ("Renter Roadmap", "/landing/")]),
                                   {"@type": "HowTo", "name": "How to rent and move into a new home", "step": [{"@type": "HowToStep", "position": i + 1, "name": s[0], "text": s[2]} for i, s in enumerate(steps)]}])
    PAGES.append(("/landing/", TODAY, "0.7"))


def build_legal():
    upd = date.fromisoformat(TODAY).strftime("%B %-d, %Y")
    privacy = f"""<p><em>Last updated {upd}</em></p>
<h2 id="overview">Overview</h2><p>This policy explains how {SITE} ("we", "us") handles information when you use connectedrenter.com.</p>
<h2 id="collect">Information we collect</h2><ul><li><strong>Information you send us.</strong> When you email us, use the contact form, order merch or reserve a course, your email app sends us your message and contact details.</li><li><strong>Tool data.</strong> Our calculators and checklists run in your browser. Checklist progress is stored in your browser's local storage on your device; we do not receive it.</li><li><strong>Technical data.</strong> Our hosting provider may log standard server information such as IP address, browser type and pages requested for security and performance.</li></ul>
<h2 id="use">How we use information</h2><p>We use what you send us to reply to you, fulfil orders and course enrollments, and improve the site. We do not sell your personal information.</p>
<h2 id="third">Third parties</h2><p>We load fonts from Google Fonts. Pages may link to third-party websites, which have their own privacy policies.</p>
<h2 id="choices">Your choices</h2><p>You can clear saved checklist data by clearing your browser's site data. To ask about or delete information you've sent us, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2 id="children">Children</h2><p>This site is not directed to children under 13.</p>
<h2 id="changes">Changes</h2><p>We may update this policy and will change the date above when we do.</p>"""
    terms = f"""<p><em>Last updated {upd}</em></p>
<h2 id="acceptance">Acceptance</h2><p>By using connectedrenter.com you agree to these terms.</p>
<h2 id="info">Information only</h2><p>Content and tools on {SITE} are for general information and planning. They are not legal, financial, insurance or tax advice. Cost figures and estimates are approximations; confirm details with providers and a qualified professional.</p>
<h2 id="third">Third-party services</h2><p>We may mention or link to third-party businesses. We don't control them and aren't responsible for their products, services or terms. We may receive compensation from some partners; this never changes what we tell renters about their options.</p>
<h2 id="purchases">Courses and merch</h2><p>Course and merchandise orders are confirmed by email with payment and delivery details. Course refunds are available within 14 days of purchase on request.</p>
<h2 id="ip">Intellectual property</h2><p>The {SITE} name, logo and content are ours. You may share links and quote short excerpts with attribution.</p>
<h2 id="liability">Limitation of liability</h2><p>To the extent permitted by law, {SITE} is not liable for losses arising from use of the site or reliance on its content.</p>
<h2 id="law">Governing law</h2><p>These terms are governed by the laws of the State of Texas.</p>
<h2 id="contact">Contact</h2><p>Questions? Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>"""
    for path, title, lead, body in [("/privacy-policy/", "Privacy Policy", "How Connected Renter handles your information.", privacy), ("/terms-of-use/", "Terms of Use", "The rules for using connectedrenter.com.", terms)]:
        main = page_hero([("Home", "/"), (title, path)], title, lead) + f'<section class="section"><div class="wrap"><article class="prose">{body}</article></div></section>'
        page(path, f"{title} | Connected Renter", f"{title} for connectedrenter.com. {lead}", main, schema=[crumbs_ld([("Home", "/"), (title, path)])])
        PAGES.append((path, TODAY, "0.2"))


def build_404():
    main = f"""<section class="hero" style="padding:110px 0">{blobs()}<div class="wrap center">
<div class="err-num grad-text">404</div><h1 style="font-size:clamp(1.8rem,4vw,2.8rem)">Looks like this page moved out.</h1>
<p class="lead" style="margin-inline:auto">It didn't leave a forwarding address. Try searching, or head to one of these:</p>
<div class="hero-actions" style="justify-content:center"><a class="btn gold" href="/">Home</a><a class="btn light" href="/moving-resources/">Moving resources</a><a class="btn light" href="/tools/">Free tools</a><button class="btn light" type="button" data-open-search>{icon("search")} Search</button></div></div></section>"""
    doc = page("/404.html", "Page Not Found | Connected Renter", "The page you were looking for could not be found.", main)
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as f:
        f.write(doc.replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">').replace(f'<link rel="canonical" href="{ORIGIN}/404.html">\n', ""))


# ------------------------------------------------------------------ support files

def build_support():
    idx = []
    for r in RESOURCES:
        idx.append({"t": r["name"], "u": f"/moving-resources/{r['slug']}/", "d": r["short"], "k": r["seo_title"] + " " + r["desc"], "kind": "Resource", "i": r["icon"], "f": 1})
    for t in TOOLS:
        idx.append({"t": t[2], "u": f"/tools/{t[0]}/", "d": t[4], "k": t[5] + " calculator tool", "kind": "Tool", "i": t[3], "f": 1})
    for p in POSTS:
        idx.append({"t": p["title"], "u": p["path"], "d": p["excerpt"][:110], "k": p["desc"], "kind": "Article", "i": p["icon"]})
    for t, u, d, i in [("Renter Roadmap", "/landing/", "Start here: step-by-step from search to settled.", "compass"), ("Moving Made Easy Courses", "/courses/", "Practical $20 courses for renters.", "cap"),
                       ("Shop", "/shop/", "Connected Renter merch.", "bag"), ("Contact", "/contact-us/", "Phone, email and contact form.", "mail"), ("About", "/about-us/", "Our story.", "heart")]:
        idx.append({"t": t, "u": u, "d": d, "k": "", "kind": "Page", "i": i})
    with open(os.path.join(ROOT, "assets/js/search-index.js"), "w", encoding="utf-8") as f:
        f.write("window.CR_INDEX=" + json.dumps(idx, ensure_ascii=False, separators=(",", ":")) + ";\n")

    urls = "".join(f"<url><loc>{ORIGIN}{p}</loc><lastmod>{m}</lastmod><priority>{pr}</priority></url>\n" for p, m, pr in PAGES)
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    with open(os.path.join(ROOT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nDisallow: /home.html\n\nSitemap: {ORIGIN}/sitemap.xml\n")
    with open(os.path.join(ROOT, "site.webmanifest"), "w") as f:
        json.dump({"name": SITE, "short_name": SITE, "start_url": "/", "display": "standalone", "background_color": "#fffaf1", "theme_color": "#680404",
                   "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, f, indent=1)


def build_og():
    out = os.path.join(ROOT, "assets/img/og-default.png")
    if os.path.exists(out):
        return
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), "#1a0e0d")
    px = im.load()
    for y in range(H):
        for x in range(W):
            t = (x / W * 0.6 + y / H * 0.4)
            px[x, y] = (int(42 + (104 - 42) * t + 50 * max(0, t - .7)), int(6 + 4 * t), int(6 + 4 * t))
    dr = ImageDraw.Draw(im)
    logo = Image.open(os.path.join(ROOT, "assets/img/connected-renter-logo-white.png")).convert("RGBA")
    logo = logo.resize((680, int(680 * logo.height / logo.width)))
    im.paste(logo, (80, 150), logo)
    try:
        f1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 46)
    except OSError:
        f1 = ImageFont.load_default()
    dr.text((86, 400), "Every renter resource, connected.", fill="#f3c54f", font=f1)
    dr.rectangle([0, H - 14, W, H], fill="#DBA622")
    im.save(out, optimize=True)


def main():
    build_og()
    build_home()
    build_resources()
    build_tools()
    build_blog()
    build_courses()
    build_shop()
    build_contact()
    build_about()
    build_landing()
    build_legal()
    build_404()
    build_support()
    print(f"built {len(PAGES)} pages + 404")


if __name__ == "__main__":
    main()
