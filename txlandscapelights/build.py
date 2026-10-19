#!/usr/bin/env python3
"""Build txlandscapelights.com into public/. Run: python3 build.py && python3 validate.py"""
import html
import json
import re
import shutil
from datetime import date
from pathlib import Path

import photos
import svgart
from siteconf import (ASSET_V, BASE, CATEGORIES, CITIES, EMAIL, NAME, PHONE, PHONE_E164, SERVICES, TEL, TOOLS, icon)

ROOT = Path(__file__).parent
OUT = ROOT / "public"
CONTENT = ROOT / "content"
TODAY = date(2026, 10, 19).isoformat()
esc = lambda s: html.escape(str(s), quote=True)
PAGES = []  # (path, lastmod, priority) for sitemap


# ---------- content loading ----------

def load(group, slug):
    raw = (CONTENT / group / f"{slug}.html").read_text()
    m = re.match(r"<!--meta (\{.*?\}) -->\s*", raw, re.S)
    meta = json.loads(m.group(1))
    body = raw[m.end():]
    hero = hero_photo(group, slug)
    used = {hero}
    def art(a):
        theme = a.group(1)
        pool = photos.THEME.get(theme, photos.THEME["facade"])
        start = __import__("zlib").crc32(slug.encode()) % len(pool)
        key = next((pool[(start + i) % len(pool)] for i in range(len(pool)) if pool[(start + i) % len(pool)] not in used), pool[start])
        used.add(key)
        return f'<figure class="art">{photos.img(key)}</figure>'
    body = re.sub(r'<div class="art" data-art="(\w+)"></div>', art, body)
    meta["photo"] = hero
    meta["body"] = body
    meta["slug"] = slug
    return meta


def hero_photo(group, slug):
    if group == "services":
        return photos.SERVICE.get(slug, "facade-estate")
    if group == "areas":
        return photos.CITY.get(slug) or photos.pick("city", slug)
    if group == "blog":
        return photos.POST.get(slug, "house-night")
    return photos.PAGE.get(slug, "house-night")


def words(h):
    return len(re.sub(r"<[^>]+>", " ", h).split())


def add_ids(body):
    """Give prose h2s ids and return (body, toc)."""
    toc, seen = [], set()
    def rep(m):
        text = re.sub(r"<[^>]+>", "", m.group(2))
        sid = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60]
        while sid in seen:
            sid += "-2"
        seen.add(sid)
        toc.append((sid, text))
        return f'<h2{m.group(1)} id="{sid}">{m.group(2)}</h2>'
    return re.sub(r"<h2([^>]*)>(.*?)</h2>", rep, body), toc


# ---------- shared fragments ----------

def nav_items():
    svc = "".join(f'<li><a href="/services/{s["slug"]}/">{esc(s["name"])}</a></li>' for s in SERVICES)
    ar = "".join(f'<li><a href="/service-areas/{c["slug"]}/">{esc(c["name"])}</a></li>' for c in CITIES)
    tl = "".join(f'<li><a href="/tools/{t["slug"]}/">{esc(t["name"])}</a></li>' for t in TOOLS)
    return [("Services", "/services/", f'<ul class="sub">{svc}<li><a href="/services/">All services →</a></li></ul>'),
            ("Service Areas", "/service-areas/", f'<ul class="sub sub--cols">{ar}<li><a href="/service-areas/">All of Texas →</a></li></ul>'),
            ("Tools", "/tools/", f'<ul class="sub">{tl}</ul>'),
            ("Ideas", "/inspiration/", None), ("Blog", "/blog/", None), ("About", "/about-us/", None), ("Contact", "/contact/", None)]


def header(cur):
    items = []
    for label, href, sub in nav_items():
        on = ' aria-current="page"' if cur.startswith(href) else ""
        items.append(f'<li class="{"has-sub" if sub else ""}"><a href="{href}"{on}>{label}</a>{sub or ""}</li>')
    drawer = []
    for label, href, sub in nav_items():
        if sub:
            drawer.append(f'<details><summary>{label}</summary><div><a href="{href}">{label} overview</a>{re.sub(r"</?(ul|li)[^>]*>", "", sub)}</div></details>')
        else:
            drawer.append(f'<a href="{href}">{label}</a>')
    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="ubar"><div class="wrap"><div class="ubar__l"><span class="ubar__star">{icon("star")} Landscape lighting for homes across Texas</span><a href="mailto:{EMAIL}">{icon("mail")} {EMAIL}</a></div><div class="ubar__r"><a href="/tools/">{icon("wand")} Free planning tools</a><a href="{TEL}">{icon("phone")} {PHONE}</a></div></div></div>
<header class="hdr"><div class="wrap">
<a class="logo" href="/" aria-label="{NAME} home">{svgart.logo_svg()}<span><b>Texas Landscape</b><small>Lights · Design · Install</small></span></a>
<nav aria-label="Main"><ul class="nav">{"".join(items)}</ul></nav>
<div class="hdr__cta"><a class="btn btn--ghost btn--sm" href="{TEL}">{icon("phone")} {PHONE}</a><a class="btn btn--sm" href="/quote/">{icon("sparkles")}<span>Free Quote</span></a>
<button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="drawer"><span></span><span></span><span></span></button></div>
</div></header>
<div class="scrim"></div>
<nav class="drawer" id="drawer" aria-hidden="true" aria-label="Mobile">
<div class="drawer__top"><a class="logo" href="/" aria-label="{NAME} home">{svgart.logo_svg()}<span><b>Texas Landscape</b><small>Lights · Design · Install</small></span></a>
<button class="drawer__x" type="button" aria-label="Close menu">{icon("x")}</button></div>
<div class="drawer__nav">{"".join(drawer)}</div>
<div class="drawer__cta"><a class="btn btn--block" href="/quote/">{icon("sparkles")} Get my free quote</a><a class="btn btn--ghost btn--block" href="{TEL}">{icon("phone")} Call {PHONE}</a>
<a class="drawer__mail" href="mailto:{EMAIL}">{icon("mail")} {EMAIL}</a></div>
</nav>"""


def footer():
    svc = "".join(f'<li><a href="/services/{s["slug"]}/">{esc(s["name"])}</a></li>' for s in SERVICES)
    ar = "".join(f'<li><a href="/service-areas/{c["slug"]}/">{esc(c["short"])}</a></li>' for c in CITIES[:9])
    return f"""<footer class="ftr"><div class="wrap">
<div class="ftr__g">
<div><a class="logo" href="/">{svgart.logo_svg()}<span><b>Texas Landscape</b><small>Lights · Design · Install</small></span></a>
<p>Custom low-voltage LED landscape lighting design, installation, repair and upgrades for homeowners across Texas, from the Gulf Coast to the Hill Country and DFW.</p>
<ul class="contact-list"><li><a href="{TEL}">{icon("phone")}<span><small>Call or text</small><b>{PHONE}</b></span></a></li><li><a href="mailto:{EMAIL}">{icon("mail")}<span><small>Email</small><b>{EMAIL}</b></span></a></li></ul></div>
<div><h4>Services</h4><ul>{svc}</ul></div>
<div><h4>Service areas</h4><ul>{ar}<li><a href="/service-areas/">All Texas areas →</a></li></ul></div>
<div><h4>Company</h4><ul><li><a href="/about-us/">About us</a></li><li><a href="/our-process/">Our process</a></li><li><a href="/inspiration/">Ideas &amp; inspiration</a></li><li><a href="/tools/">Planning tools</a></li><li><a href="/blog/">Blog</a></li><li><a href="/faq/">FAQ</a></li><li><a href="/contact/">Contact</a></li><li><a href="/quote/">Free quote</a></li></ul></div>
</div>
<div class="ftr__b"><span>© {date.today().year} {NAME}. All rights reserved.</span><nav><a href="/privacy-policy/">Privacy Policy</a><a href="/terms-of-service/">Terms of Service</a><a href="/photo-credits/">Photo Credits</a><a href="/sitemap.xml">Sitemap</a></nav></div>
</div></footer>
<a class="fcall" href="{TEL}" aria-label="Call {PHONE}">{icon("phone")}</a>
<button class="totop" aria-label="Back to top">{icon("up")}</button>"""


PROJECTS = [s["name"] for s in SERVICES] + ["Complete new lighting system", "Not sure yet"]


def qform(fid, source, compact=False):
    proj = "".join(f"<option>{esc(p)}</option>" for p in PROJECTS)
    extra = "" if compact else ('<label class="fld"><span>Best time to reach you</span><select name="time"><option>Any time</option><option>Morning</option><option>Afternoon</option><option>Evening</option></select></label>')
    return f"""<form class="qform" id="{fid}" method="post" action="/app/lead.php" data-qform novalidate>
<input type="hidden" name="source" value="{esc(source)}"><input type="hidden" name="form" value="{fid}"><input type="hidden" name="t" value="">
<div class="hp" aria-hidden="true"><label>Website <input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
<div class="qform__grid">
<label class="fld"><span>Full name *</span><input type="text" name="name" required autocomplete="name" placeholder="Jane Smith"></label>
<label class="fld"><span>Phone *</span><input type="tel" name="phone" required autocomplete="tel" placeholder="(281) 555-0123"></label>
<label class="fld"><span>Email *</span><input type="email" name="email" required autocomplete="email" placeholder="you@example.com"></label>
<label class="fld"><span>City</span><input type="text" name="city" autocomplete="address-level2" placeholder="e.g. Houston"></label>
<label class="fld{' fld--full' if compact else ''}"><span>Project type</span><select name="project"><option value="">Select a service</option>{proj}</select></label>
{extra}
<label class="fld fld--full"><span>Project details</span><textarea name="message" rows="{3 if compact else 4}" placeholder="What would you like to light? Facade, trees, walkway, patio, pool, repairs…"></textarea></label>
</div>
<button class="btn btn--block" type="submit">{icon("sparkles")}<span>{"Get My Free Lighting Plan" if compact else "Request My Free Consultation"}</span></button>
<p class="qform__status" role="status" aria-live="polite"></p>
<p class="qform__note">{icon("shield")} No obligation. We never share your details. Or call <a href="{TEL}">{PHONE}</a>.</p>
</form>"""


def popup():
    return f"""<div class="pop" id="pop" role="dialog" aria-modal="true" aria-labelledby="pop-t" aria-hidden="true">
<div class="pop__bg" data-pop-close></div>
<div class="pop__box">
<button class="pop__x" type="button" aria-label="Close" data-pop-close>{icon("x")}</button>
<div class="pop__side">{photos.img("pool-string-lights", "pop__bg", alt="")}<div><span class="eyebrow">Free lighting plan</span><h2>See your home in a new light</h2><p>Tell us a little about your property and we will put together a custom night-lighting plan, free and with no obligation.</p></div>
<a class="pop__ph" href="{TEL}">{icon("phone")} {PHONE}</a>
</div>
<div class="pop__main"><h3 id="pop-t">Get your free quote</h3><p>Most requests get a reply within one business day.</p>{qform("popup-form", "popup", compact=True)}</div>
</div></div>"""


def quote_section(source, title="Request your free lighting plan", h="Tell us about your project", alt=False):
    return f"""<section class="sec{' sec--alt' if alt else ''}" id="quote"><div class="wrap qsec">
<div data-reveal><span class="eyebrow">{esc(title)}</span><h2>{esc(h)}</h2>
<p class="lead">Share a few details and we will reach out to schedule a free consultation. We will talk through your goals, look at the property and, where it helps, show you a night demo before you decide anything.</p>
<ul class="checks"><li>Custom design for your home, not a preset package</li><li>Written proposal with fixture locations and pricing</li><li>Warm, low-glare 12V LED systems built for Texas weather</li><li>Final aiming visit after dark</li></ul>
<ul class="contact-list"><li><a href="{TEL}">{icon("phone")}<span><small>Call or text</small><b>{PHONE}</b></span></a></li><li><a href="mailto:{EMAIL}">{icon("mail")}<span><small>Email</small><b>{EMAIL}</b></span></a></li></ul></div>
<div class="qcard" data-reveal><h3>Free consultation request</h3>{qform("quote-" + re.sub(r"[^a-z0-9]+", "-", source.strip("/") or "home"), source)}</div>
</div></section>"""


def cta_band(h="Ready to see your home in a new light?", p="Talk to Texas Landscape Lights about a custom lighting plan for your property, anywhere in Texas."):
    return f"""<section class="cta"><div class="wrap"><span class="eyebrow">Free consultation</span><h2>{h}</h2><p>{p}</p>
<div class="cta__b"><a class="btn" href="/quote/">{icon("sparkles")} Get my free quote</a><a class="btn btn--ghost" href="{TEL}">{icon("phone")} {PHONE}</a></div></div></section>"""


def faq_block(faqs, title="Common questions", light=False):
    if not faqs:
        return ""
    qa = "".join(f'<details class="qa"><summary>{esc(q)}</summary><div><p>{esc(a)}</p></div></details>' for q, a in faqs)
    return f'<section class="sec{" sec--light" if light else ""}" id="faq"><div class="wrap"><div class="head head--center"><span class="eyebrow">FAQ</span><h2>{esc(title)}</h2></div><div class="faq">{qa}</div></div></section>'


# ---------- schema ----------

BUSINESS_ID = f"{BASE}/#business"


def business_schema():
    return {
        "@type": ["LocalBusiness", "HomeAndConstructionBusiness"], "@id": BUSINESS_ID, "name": NAME, "url": f"{BASE}/",
        "telephone": PHONE_E164, "email": EMAIL, "logo": f"{BASE}/assets/img/logo-512.png", "image": f"{BASE}/assets/img/og-image.png",
        "description": "Custom low-voltage LED landscape lighting design, installation, repair and upgrades for homes and select commercial properties across Texas.",
        "areaServed": [{"@type": "State", "name": "Texas"}] + [{"@type": "City", "name": c["name"]} for c in CITIES],
        "knowsAbout": ["Landscape lighting", "Architectural lighting", "Low-voltage LED lighting", "Outdoor lighting design", "Tree uplighting"],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Landscape lighting services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f'{BASE}/services/{s["slug"]}/'}} for s in SERVICES]},
    }


def crumbs_schema(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u} for i, (n, u) in enumerate(trail)]}


def faq_schema(faqs):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


# ---------- page shell ----------

def page(path, title, desc, main, schema=(), og_type="website", robots="index, follow, max-image-preview:large, max-snippet:-1", priority="0.6", lastmod=TODAY, scripts=("site",), crumbs=None, sitemap=True, image=None):
    url = BASE + path
    graph = [business_schema() if path == "/" else {"@type": "LocalBusiness", "@id": BUSINESS_ID, "name": NAME, "telephone": PHONE_E164, "url": f"{BASE}/"},
             {"@type": "WebSite", "@id": f"{BASE}/#website", "url": f"{BASE}/", "name": NAME, "publisher": {"@id": BUSINESS_ID}, "inLanguage": "en-US"},
             {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc, "isPartOf": {"@id": f"{BASE}/#website"}, "about": {"@id": BUSINESS_ID}, "inLanguage": "en-US", "dateModified": lastmod}]
    if crumbs:
        graph.append(crumbs_schema(crumbs))
    graph += list(schema)
    js = "".join(f'<script src="/assets/js/{s}.js?v={ASSET_V}" defer></script>' for s in scripts)
    doc = f"""<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-CCJ95Y61X4"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', 'G-CCJ95Y61X4');
</script>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{"" if "noindex" in robots else f'<link rel="canonical" href="{url}">'}
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#1d1f22">
<meta property="og:locale" content="en_US"><meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}">
{og_image(image)}
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{BASE + (photos.src(image) if image else "/assets/img/og-image.png")}">
<meta name="geo.region" content="US-TX"><meta name="geo.placename" content="Texas">
<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="icon" type="image/png" sizes="96x96" href="/favicon-96x96.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Barlow:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={ASSET_V}">
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)}</script>
{js}
</head>
<body>
{header(path)}
<main id="main">
{main}
</main>
{footer()}
{popup()}
</body>
</html>
"""
    dest = OUT / "home.html" if path == "/" else OUT / path.strip("/") / ("index.html" if path.endswith("/") else "")
    if path == "/404.html":
        dest = OUT / "404.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(doc)
    if sitemap and "noindex" not in robots:
        PAGES.append((path, lastmod, priority, image))


def og_image(key):
    if not key:
        return f'<meta property="og:image" content="{BASE}/assets/img/og-image.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
    p = photos.PHOTOS[key]
    return (f'<meta property="og:image" content="{BASE}{photos.src(key)}"><meta property="og:image:width" content="{p["w"]}"><meta property="og:image:height" content="{p["h"]}">'
            f'<meta property="og:image:alt" content="{esc(p["alt"])}">')


def phero(eyebrow, h1, lede, trail, meta_line="", photo=None):
    cr = "".join(f'<li><a href="{u}">{esc(n)}</a></li>' if i < len(trail) - 1 else f'<li aria-current="page">{esc(n)}</li>' for i, (n, u) in enumerate(trail))
    bg = f'<div class="phero__img" aria-hidden="true">{photos.img(photo, "", eager=True, sizes="(max-width: 900px) 100vw, 60vw", alt="")}</div>' if photo else ""
    return f"""<section class="phero{' phero--photo' if photo else ''}">{bg}<div class="wrap"><nav aria-label="Breadcrumb"><ol class="crumbs">{cr}</ol></nav>
<span class="eyebrow">{esc(eyebrow)}</span><h1>{esc(h1)}</h1><p class="lead">{esc(lede)}</p>{meta_line}</div></section>"""


def aside(kind, slug, toc=None):
    cards = []
    if toc and len(toc) > 2:
        cards.append('<div class="aside__card toc"><h4>On this page</h4><ul>' + "".join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in toc) + "</ul></div>")
    cards.append(f'<div class="aside__card aside__card--hot"><h4>Free lighting plan</h4><p>Custom design, written proposal and a final aiming visit after dark.</p><a class="btn btn--block" href="/quote/">{icon("sparkles")} Get my free quote</a><p style="margin:12px 0 0;text-align:center"><a href="{TEL}">{PHONE}</a></p></div>')
    if kind == "services":
        cards.append('<div class="aside__card"><h4>Other services</h4><ul>' + "".join(f'<li><a href="/services/{s["slug"]}/">{esc(s["name"])}</a></li>' for s in SERVICES if s["slug"] != slug) + "</ul></div>")
    elif kind == "areas":
        cards.append('<div class="aside__card"><h4>More Texas areas</h4><ul>' + "".join(f'<li><a href="/service-areas/{c["slug"]}/">{esc(c["name"])}</a></li>' for c in CITIES if c["slug"] != slug) + "</ul></div>")
    else:
        cards.append('<div class="aside__card"><h4>Planning tools</h4><ul>' + "".join(f'<li><a href="/tools/{t["slug"]}/">{esc(t["name"])}</a></li>' for t in TOOLS) + "</ul></div>")
    return '<aside class="aside">' + "".join(cards) + "</aside>"


def related_links(items):
    return '<div class="related">' + "".join(f'<a href="{u}"><small>{esc(k)}</small>{esc(n)}</a>' for k, n, u in items) + "</div>"


# ---------- page builders ----------

def build_content_page(group, slug, path, trail, kind, priority="0.7", extra_schema=(), related=None, faq_title="Questions & answers", full=False):
    m = load(group, slug)
    body, toc = add_ids(m["body"])
    faqs = m.get("faqs") or []
    sch = list(extra_schema)
    if faqs:
        sch.append(faq_schema(faqs))
    if slug == "faq":
        pairs = re.findall(r'<details class="qa"><summary>(.*?)</summary><div>(.*?)</div></details>', body, re.S)
        sch.append(faq_schema([(re.sub("<[^>]+>", "", q).strip(), re.sub(r"\s+", " ", re.sub("<[^>]+>", "", a)).strip()) for q, a in pairs]))
    rel = f'<div class="prose"><h2>Keep exploring</h2></div>{related_links(related)}' if related else ""
    layout = "layout layout--full" if full else "layout"
    side = "" if full else aside(kind, slug, toc)
    main = (phero(m["eyebrow"], m["h1"], m["lede"], trail, photo=m["photo"])
            + f'<section class="sec"><div class="wrap {layout}"><div class="body">{body}{rel}</div>{side}</div></section>'
            + faq_block(faqs, faq_title, light=True)
            + (quote_section(path) if slug not in ("privacy-policy", "terms-of-service") else "")
            + cta_band())
    page(path, m["title"], m["description"], main, schema=sch, priority=priority, crumbs=trail, image=m["photo"])
    return m


def build_services():
    home = ("Home", "/")
    for s in SERVICES:
        path = f'/services/{s["slug"]}/'
        rel = [("Service area", c["name"], f'/service-areas/{c["slug"]}/') for c in CITIES[:4]]
        m = load("services", s["slug"])
        svc_schema = {"@type": "Service", "name": s["name"], "serviceType": m.get("keyword", s["name"]), "url": BASE + path, "provider": {"@id": BUSINESS_ID}, "areaServed": {"@type": "State", "name": "Texas"}, "description": m["description"]}
        build_content_page("services", s["slug"], path, [home, ("Services", "/services/"), (s["name"], path)], "services", "0.8", [svc_schema], rel)
    cards = "".join(service_card(s, i) for i, s in enumerate(SERVICES))
    main = (phero("What we do", "Landscape Lighting Services in Texas", "Design, installation, repair and upgrades for every part of a Texas property, from the front elevation to the back fence.", [home, ("Services", "/services/")], photo=photos.PAGE["services"])
            + f'<section class="sec"><div class="wrap"><div class="hub">{cards}</div></div></section>'
            + process_rail() + quote_section("/services/") + cta_band())
    page("/services/", "Landscape Lighting Services in Texas | Texas Landscape Lights", "Architectural, pathway, tree, patio, pool and commercial landscape lighting plus smart controls, repairs and LED upgrades for Texas homes. Free quote.", main, priority="0.9", crumbs=[home, ("Services", "/services/")], image=photos.PAGE["services"])


def service_card(s, i, cls=""):
    return (f'<a class="svc {cls}" href="/services/{s["slug"]}/"><div class="svc__art">{photos.img(photos.SERVICE[s["slug"]], sizes="(max-width: 640px) 100vw, 40vw")}</div>'
            f'<span class="svc__n">{i + 1:02d}</span><h3>{esc(s["name"])}</h3><p>{esc(s["short"])}</p><span class="svc__go">Explore {icon("arrow")}</span></a>')


def process_rail():
    steps = [("Consultation", "A quick call about your goals, budget and how you use the yard after dark."),
             ("Night walkthrough", "We study the property and, where it helps, show a live demo after sunset."),
             ("Custom plan", "Fixture locations, beam spreads, color temperature, zones and controls."),
             ("Clear proposal", "A written scope and price for the planned system. No surprises."),
             ("Clean install", "Concealed wire, protected beds and roots, tidy site, tested connections."),
             ("Final aiming", "We return after dark to fine-tune every fixture until it is right.")]
    li = "".join(f"<li><h3>{a}</h3><p>{b}</p></li>" for a, b in steps)
    return f'<section class="sec sec--alt" id="process"><div class="wrap"><div class="head head--row"><div><span class="eyebrow">How it works</span><h2>Six steps from first call to first night</h2></div><a class="btn btn--ghost" href="/our-process/">Our full process {icon("arrow")}</a></div><ol class="rail" data-reveal>{li}</ol></div></section>'


def build_areas():
    home = ("Home", "/")
    for i, c in enumerate(CITIES):
        path = f'/service-areas/{c["slug"]}/'
        near = sorted((x for x in CITIES if x is not c), key=lambda x: (x["lat"] - c["lat"]) ** 2 + (x["lon"] - c["lon"]) ** 2)[:3]
        rel = [("Nearby", x["name"], f'/service-areas/{x["slug"]}/') for x in near] + [("Tool", "Sunset & Timer Planner", "/tools/sunset-timer-planner/")]
        m = load("areas", c["slug"])
        svc = {"@type": "Service", "name": f'Landscape lighting in {c["name"]}', "serviceType": "Landscape lighting", "provider": {"@id": BUSINESS_ID}, "areaServed": {"@type": "City", "name": c["name"]}, "url": BASE + path}
        build_content_page("areas", c["slug"], path, [home, ("Service Areas", "/service-areas/"), (c["name"], path)], "areas", "0.8", [svc], rel, faq_title=f'Landscape lighting in {c["short"]}: FAQ')
    main = (phero("Where we work", "Landscape Lighting Across Texas", "From Houston and the Gulf Coast to Dallas–Fort Worth, Austin, San Antonio and the Hill Country, we design and install lighting that suits each region's homes, trees and weather.", [home, ("Service Areas", "/service-areas/")], photo=photos.PAGE["service-areas"])
            + f'<section class="sec"><div class="wrap">{map_block(False)}</div></section>'
            + '<section class="sec sec--alt"><div class="wrap"><div class="head"><span class="eyebrow">City guides</span><h2>Choose your area</h2></div><div class="areas-hub">'
            + "".join(f'<a class="area" href="/service-areas/{c["slug"]}/"><small>{esc(c["county"])}</small><b>{esc(c["short"])}</b><p>{esc(c["blurb"])}</p></a>' for c in CITIES)
            + '</div><div class="prose" style="margin-top:34px"><p>Not on the list? We serve homeowners throughout Texas. Call <a href="' + TEL + '">' + PHONE + '</a> or <a href="/quote/">send us your project</a> and we will let you know how we can help in your city.</p></div></div></section>'
            + quote_section("/service-areas/") + cta_band())
    page("/service-areas/", "Texas Service Areas | Texas Landscape Lights", "Landscape lighting in Houston, Dallas, Austin, San Antonio, Fort Worth, Plano, Frisco, Katy, Sugar Land, The Woodlands and across Texas. Free quote.", main, priority="0.9", crumbs=[home, ("Service Areas", "/service-areas/")], image=photos.PAGE["service-areas"])


def map_block(home=True):
    lst = "".join(f'<li><a href="/service-areas/{c["slug"]}/" data-city="{c["slug"]}">{esc(c["short"])} <small>{esc(c["region"])}</small></a></li>' for c in CITIES)
    txt = ('<span class="eyebrow">Statewide service</span><h2>Texas landscape lights, from the coast to the Hill Country</h2>'
           '<p class="lead">Texas Landscape Lights designs for the way each part of the state looks and weathers. Pick a city to see local neighborhoods, home styles, trees and the lighting approach that suits them.</p>') if home else (
           '<span class="eyebrow">Interactive map</span><h2>Find your city</h2><p class="lead">Hover a city on the map or the list, then click through for a local guide.</p>')
    return f'<div class="map" data-map><div class="txmap" data-reveal>{svgart.texas_map(CITIES, __import__("siteconf").MAP_SIDE)}</div><div>{txt}<ul class="arealist">{lst}</ul><a class="btn btn--ghost" href="/service-areas/">All service areas {icon("arrow")}</a></div></div>'


def post_card(m):
    return (f'<a class="post" href="/blog/{m["slug"]}/"><div class="post__art">{photos.img(photos.POST.get(m["slug"], "house-night"), sizes="(max-width: 640px) 100vw, 33vw")}</div>'
            f'<div class="post__b"><span class="post__m">{CATEGORIES[m["category"]][0]} · {read_time(m)} min read</span><h3>{esc(m["h1"])}</h3><p>{esc(m["excerpt"])}</p></div></a>')


def read_time(m):
    return max(3, round(words(m["body"]) / 230))


def fmt_date(iso):
    d = date.fromisoformat(iso)
    return d.strftime("%B ") + str(d.day) + d.strftime(", %Y")


def build_blog():
    home = ("Home", "/")
    posts = sorted((load("blog", p.stem) for p in (CONTENT / "blog").glob("*.html")), key=lambda m: m["date"], reverse=True)
    for m in posts:
        path = f'/blog/{m["slug"]}/'
        body, toc = add_ids(m["body"])
        cat = CATEGORIES[m["category"]][0]
        trail = [home, ("Blog", "/blog/"), (cat, f'/blog/category/{m["category"]}/'), (m["h1"], path)]
        meta_line = (f'<div class="phero__meta"><span>{icon("cal")} {fmt_date(m["date"])}</span><span>{icon("clock")} {read_time(m)} min read</span>'
                     f'<span>{icon("book")} <a href="/blog/category/{m["category"]}/">{cat}</a></span></div>')
        others = [p for p in posts if p is not m]
        more = sorted(others, key=lambda p: (p["category"] != m["category"], p["date"]))[:3]
        art_ = {"@type": "BlogPosting", "headline": m["h1"], "description": m["description"], "datePublished": m["date"], "dateModified": m["date"],
                "author": {"@type": "Organization", "name": NAME, "url": f"{BASE}/"}, "publisher": {"@id": BUSINESS_ID}, "mainEntityOfPage": BASE + path,
                "image": BASE + photos.src(m["photo"]), "articleSection": cat, "keywords": m.get("keyword", ""), "wordCount": words(body)}
        share = f'<div class="share"><span>Share this guide:</span><button type="button" data-copy>Copy link</button></div>'
        cover = f'<figure class="cover">{photos.img(m["photo"], eager=False, sizes="(max-width: 1100px) 100vw, 800px")}</figure>'
        main = (phero(m["eyebrow"], m["h1"], m["lede"], trail, meta_line, photo=m["photo"])
                + f'<section class="sec"><div class="wrap layout"><article class="body">{cover}{body}{share}</article>{aside("blog", m["slug"], toc)}</div></section>'
                + faq_block(m.get("faqs"), "Questions about this topic", light=True)
                + f'<section class="sec"><div class="wrap"><div class="head"><span class="eyebrow">Keep reading</span><h2>More from the blog</h2></div><div class="posts">{"".join(post_card(p) for p in more)}</div></div></section>'
                + cta_band())
        page(path, m["title"], m["description"], main, schema=[art_, faq_schema(m["faqs"])] if m.get("faqs") else [art_], og_type="article", priority="0.6", lastmod=m["date"], crumbs=trail, image=m["photo"])
    def listing(path, h1, lede, items, trail, title, desc):
        chips = '<div class="presets" style="margin-bottom:28px"><a class="chip" href="/blog/">All posts</a>' + "".join(f'<a class="chip{" is-on" if path.endswith(k + "/") else ""}" href="/blog/category/{k}/">{v[0]}</a>' for k, v in CATEGORIES.items()) + "</div>"
        main = (phero("Lighting journal", h1, lede, trail, photo=photos.PAGE["blog"])
                + f'<section class="sec"><div class="wrap">{chips}<div class="posts">{"".join(post_card(p) for p in items)}</div></div></section>' + cta_band())
        page(path, title, desc, main, priority="0.7" if path == "/blog/" else "0.4", crumbs=trail, image=photos.PAGE["blog"])
    listing("/blog/", "Texas Landscape Lighting Blog", "Honest cost advice, design ideas and maintenance guides for lighting a Texas home.", posts, [home, ("Blog", "/blog/")],
            "Landscape Lighting Blog | Texas Landscape Lights", "Landscape lighting cost guides, design ideas, transformer sizing, LED upgrades and Texas storm and maintenance advice from Texas Landscape Lights.")
    for k, (n, d) in CATEGORIES.items():
        listing(f"/blog/category/{k}/", f"{n}: Landscape Lighting {n}", d, [p for p in posts if p["category"] == k], [home, ("Blog", "/blog/"), (n, f"/blog/category/{k}/")],
                f"{n} | Texas Landscape Lighting Blog", f"{d} Read the {n.lower()} from Texas Landscape Lights.")
    return posts


def build_static_pages():
    home = ("Home", "/")
    simple = [("about-us", "About Us", "0.6", False), ("our-process", "Our Process", "0.6", False), ("faq", "FAQ", "0.6", False), ("inspiration", "Ideas & Inspiration", "0.6", False),
              ("privacy-policy", "Privacy Policy", "0.2", True), ("terms-of-service", "Terms of Service", "0.2", True)]
    for slug, label, pr, full in simple:
        path = f"/{slug}/"
        build_content_page("pages", slug, path, [home, (label, path)], "pages", pr, full=full)
    for slug, label in (("contact", "Contact"), ("quote", "Free Quote")):
        m = load("pages", slug)
        path = f"/{slug}/"
        trail = [home, (label, path)]
        form = f'<div class="qcard"><h3>{"Send us a message" if slug == "contact" else "Free consultation request"}</h3>{qform(slug + "-form", path)}</div>'
        cl = f'<ul class="contact-list"><li><a href="{TEL}">{icon("phone")}<span><small>Call or text</small><b>{PHONE}</b></span></a></li><li><a href="mailto:{EMAIL}">{icon("mail")}<span><small>Email</small><b>{EMAIL}</b></span></a></li><li><span>{icon("pin")}<span><small>Service area</small><b>Homeowners across Texas</b></span></span></li></ul>'
        main = (phero(m["eyebrow"], m["h1"], m["lede"], trail, photo=m["photo"])
                + f'<section class="sec"><div class="wrap qsec"><div class="body">{m["body"]}{cl}</div>{form}</div></section>'
                + faq_block(m.get("faqs"), "Before you reach out", light=True) + cta_band())
        page(path, m["title"], m["description"], main, schema=[faq_schema(m["faqs"])] if m.get("faqs") else [], priority="0.8", crumbs=trail, image=m["photo"])
    # photo credits (required by CC BY / BY-SA)
    lic_url = {"by": "https://creativecommons.org/licenses/by/{v}/", "by-sa": "https://creativecommons.org/licenses/by-sa/{v}/",
               "cc0": "https://creativecommons.org/publicdomain/zero/1.0/", "pdm": "https://creativecommons.org/publicdomain/mark/1.0/"}
    lic_name = {"by": "CC BY {v}", "by-sa": "CC BY-SA {v}", "cc0": "CC0 1.0", "pdm": "Public Domain Mark 1.0"}
    rows = "".join(
        f'<tr><td><img src="{photos.src(k, True)}" width="120" height="{round(120 * p["h"] / p["w"])}" alt="{esc(p["alt"])}" loading="lazy"></td>'
        f'<td><a href="{esc(p["src"])}" rel="nofollow noopener" target="_blank">{esc(p["title"])}</a></td><td>{esc(p["creator"])}</td>'
        f'<td><a href="{lic_url[p["license"]].format(v=p["lv"])}" rel="nofollow noopener" target="_blank">{lic_name[p["license"]].format(v=p["lv"])}</a></td></tr>'
        for k, p in photos.PHOTOS.items())
    body = (f'<div class="prose"><p>The photographs on this site are royalty-free images published under Creative Commons or public-domain terms. '
            f'They illustrate lighting styles and Texas cities and are not photos of Texas Landscape Lights projects unless stated. Images were resized and converted for the web; no other changes were made. '
            f'Thank you to the photographers below.</p></div>'
            f'<div class="table-wrap"><table><thead><tr><th>Photo</th><th>Title &amp; source</th><th>Photographer</th><th>License</th></tr></thead><tbody>{rows}</tbody></table></div>')
    page("/photo-credits/", "Photo Credits | Texas Landscape Lights", "Credits and licenses for the royalty-free Creative Commons and public-domain photographs used on the Texas Landscape Lights website.",
         phero("Credits", "Photo Credits", "The photographers and licenses behind the images on this site.", [home, ("Photo Credits", "/photo-credits/")])
         + f'<section class="sec"><div class="wrap">{body}</div></section>', priority="0.2", crumbs=[home, ("Photo Credits", "/photo-credits/")])
    # thank you + 404
    page("/thank-you/", "Thank You | Texas Landscape Lights", "Thanks for contacting Texas Landscape Lights.",
         phero("Request received", "Thank you!", "Your request is in. We will be in touch shortly to talk through your project.", [home, ("Thank you", "/thank-you/")])
         + f'<section class="sec"><div class="wrap"><div class="prose"><p>Need us sooner? Call <a href="{TEL}">{PHONE}</a>. In the meantime, try our <a href="/tools/">free planning tools</a> or browse <a href="/inspiration/">lighting ideas</a>.</p></div></div></section>',
         robots="noindex, follow", sitemap=False)
    page("/404.html", "Page Not Found | Texas Landscape Lights", "The page you are looking for could not be found.",
         f'<section class="notfound"><div class="wrap"><b>404</b><h1>This page is in the dark</h1><p class="lead">The page you were looking for has moved or never existed.</p><div class="cta__b"><a class="btn" href="/">Back to home</a><a class="btn btn--ghost" href="/services/">Our services</a></div></div></section>',
         robots="noindex, follow", sitemap=False)


def write_extras():
    def img_tag(key):
        return f"<image:image><image:loc>{BASE}{photos.src(key)}</image:loc></image:image>" if key else ""
    urls = "".join(f"<url><loc>{BASE}{p}</loc><lastmod>{lm}</lastmod><priority>{pr}</priority>{img_tag(im)}</url>\n" for p, lm, pr, im in PAGES)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n{urls}</urlset>\n')
    (OUT / "robots.txt").write_text(f"User-agent: *\nDisallow: /app/\n\nSitemap: {BASE}/sitemap.xml\n")
    (OUT / "site.webmanifest").write_text(json.dumps({"name": NAME, "short_name": "TX Lights", "icons": [
        {"src": "/assets/img/logo-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/assets/img/logo-512.png", "sizes": "512x512", "type": "image/png"}],
        "theme_color": "#1d1f22", "background_color": "#1d1f22", "display": "standalone"}, indent=1))
    (OUT / "favicon.svg").write_text(svgart.logo_svg().replace('class=""', 'xmlns:xlink="http://www.w3.org/1999/xlink"'))


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "src", OUT)
    import home
    import tools
    PAGES.clear()
    posts = build_blog()
    home.build(posts)
    build_services()
    build_areas()
    tools.build()
    build_static_pages()
    write_extras()
    PAGES.sort(key=lambda p: (p[0] != "/", -float(p[2]), p[0]))
    write_extras()
    print(f"built {len(PAGES)} indexable pages into {OUT}")


if __name__ == "__main__":
    import build as _b  # run through the importable module so home.py/tools.py share its state
    _b.main()
