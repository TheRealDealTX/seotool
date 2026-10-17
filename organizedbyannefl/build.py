#!/usr/bin/env python3
"""Static generator for organizedbyannefl.com.

Writes every page as an HTML file under pages/ (served by index.php at clean,
slash-less URLs that match the original Wix site: /about, /services, /contact),
plus sitemap.xml and robots.txt. Run: python3 build.py && python3 validate.py
"""

import html
import json
import os
import re
import sys
from datetime import date

from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "content"))

import blog_a  # noqa: E402
import blog_b  # noqa: E402
import services as services_mod  # noqa: E402
import pages_content as PC  # noqa: E402

BIZ = {
    "name": "Organized by Anne",
    "email": "info@organizedbyannefl.com",
    "origin": "https://organizedbyannefl.com",
    "city": "Fort Lauderdale",
    "state": "FL",
    "region": "Broward County",
    "lat": "26.1224",
    "lng": "-80.1373",
}
AREAS = ["Fort Lauderdale", "Las Olas", "Victoria Park", "Coral Ridge", "Rio Vista", "Harbor Beach",
         "Wilton Manors", "Oakland Park", "Lauderdale-by-the-Sea", "Plantation", "Davie", "Weston",
         "Coral Springs", "Hollywood", "Pompano Beach", "Dania Beach"]
TODAY = date.today().isoformat()
FONTS = ("https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;"
         "1,9..144,400;1,9..144,500&family=Manrope:wght@400;500;600;700;800&display=swap")

SERVICES = services_mod.SERVICES
POSTS = sorted(blog_a.POSTS + blog_b.POSTS, key=lambda p: p["date"], reverse=True)

SVC_IMG = {
    "home-organizing": ("home-organizing", "Bright, styled living room with neutral sofa, plants and woven accents"),
    "closet-organization": ("closet-rail", "Neatly hung clothing on matching wooden hangers along an open rail"),
    "kitchen-pantry-organization": ("kitchen-open-shelves", "Organized kitchen with open wood shelves and tidy countertops"),
    "decluttering-downsizing": ("minimal-living", "Clutter-free living room with a dresser, plant and floor lamp"),
    "move-in-unpacking": ("bright-empty-living", "Bright, freshly unpacked living room with clean lines"),
    "home-office-organization": ("green-home-office", "Calm home office with a desk, sage green wall and plants"),
    "laundry-bathroom-organization": ("laundry-baskets", "Laundry nook with woven baskets on open cube shelving"),
    "virtual-organizing": ("planning-checklist", "Hand writing an organizing checklist in a notebook"),
}
POST_IMG = {
    "junk-drawer-organization-tips": ("open-shelving", "Tall open shelving unit with neatly stacked towels and supplies"),
    "under-bed-storage-ideas": ("calm-bedroom", "Calm bedroom with an upholstered bed and bench at the foot"),
    "homeschool-organization-small-spaces": ("homeschool-table", "Children working on lessons together at a shared table"),
    "organizing-mistakes-that-backfire": ("floating-shelves", "Floating wall shelves styled with a few decor pieces"),
    "when-to-replace-household-items": ("ceramic-cups", "Simple ceramic cups and planters on a white shelf"),
    "refresh-your-space-for-under-10": ("boho-living", "Light-filled living room with a leather sofa and plants"),
    "hurricane-season-home-organization-florida": ("tropical-pool", "Palm trees around a tropical pool on a sunny day"),
    "closet-organization-humid-climate": ("neutral-wardrobe", "Neutral knitwear hanging on a rail beside dried pampas grass"),
    "pantry-organization-ideas": ("kitchen-rail", "Kitchen wall rail holding pans and utensils above the counter"),
    "room-by-room-decluttering-checklist": ("cozy-living", "Tidy living room with a blue sofa and framed print"),
    "small-bathroom-organization-ideas": ("white-bathroom", "Clean white bathroom with a glass shower and floating vanity"),
    "how-to-organize-a-home-office": ("studio-office", "Bright shared workspace with desks, lamps and storage cubbies"),
    "how-much-does-a-professional-organizer-cost": ("planner-board", "Planning board with schedules and sticky notes"),
    "seasonal-home-organization-snowbirds": ("palm-beach", "Palm-lined beachfront with high-rise condos in South Florida"),
}

# ----------------------------------------------------------------- helpers

def esc(s):
    return html.escape(html.unescape(str(s)), quote=True)


def slugify(s):
    s = re.sub(r"<[^>]+>", "", html.unescape(s)).lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:60]


_ICONS = {}


def icon(name, cls="icon"):
    name = {"home": "house"}.get(name, name)
    if name not in _ICONS:
        raw = open(os.path.join(ROOT, "icons", name + ".svg")).read()
        raw = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
        inner = re.search(r"<svg[^>]*>(.*)</svg>", raw, re.S).group(1)
        inner = re.sub(r"\s+", " ", inner).strip()
        _ICONS[name] = inner
    return ('<svg class="%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>') % (cls, _ICONS[name])


_DIMS = {}


def img_dims(name):
    if name not in _DIMS:
        with Image.open(os.path.join(ROOT, "assets/img", name + ".webp")) as im:
            _DIMS[name] = im.size
    return _DIMS[name]


def ensure_small(name):
    """640px-wide variant used in srcset for cards and mobile."""
    src = os.path.join(ROOT, "assets/img", name + ".webp")
    dst = os.path.join(ROOT, "assets/img", name + "-sm.webp")
    if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
        with Image.open(src) as im:
            w, h = im.size
            im.resize((640, round(h * 640 / w)), Image.LANCZOS).save(dst, "WEBP", quality=74, method=6)


def img(name, alt, sizes="100vw", lazy=True, cls="", extra=""):
    ensure_small(name)
    w, h = img_dims(name)
    return ('<img src="/assets/img/{n}.webp" srcset="/assets/img/{n}-sm.webp 640w, /assets/img/{n}.webp {w}w" '
            'sizes="{s}" width="{w}" height="{h}" alt="{a}"{l}{c}{x}>').format(
        n=name, w=w, h=h, s=sizes, a=esc(alt), l=' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"',
        c=' class="%s"' % cls if cls else "", x=extra)


def words(htm):
    return len(re.sub(r"<[^>]+>", " ", htm).split())


BRAND_MARK = ('<svg class="brand-mark" viewBox="0 0 48 48" aria-hidden="true"><rect x="1" y="1" width="46" height="46" rx="15" '
              'fill="#4d614f"/><path d="M14.5 34 24 13.5 33.5 34" fill="none" stroke="#fbf7f2" stroke-width="2.6" '
              'stroke-linecap="round" stroke-linejoin="round"/><path d="M18.6 26.2h10.8" stroke="#e7a98d" stroke-width="2.6" '
              'stroke-linecap="round"/><circle cx="36.5" cy="12" r="2.4" fill="#e7a98d"/></svg>')


def brand():
    return ('<a class="brand" href="/" aria-label="Organized by Anne home">%s<span><span class="brand-name">'
            'Organized <em>by</em> Anne</span><span class="brand-sub">Fort Lauderdale · Home Organizing</span></span></a>') % BRAND_MARK

# ----------------------------------------------------------------- schema

def org_schema():
    return {
        "@type": "ProfessionalService",
        "@id": BIZ["origin"] + "/#business",
        "name": BIZ["name"],
        "url": BIZ["origin"] + "/",
        "email": BIZ["email"],
        "image": BIZ["origin"] + "/assets/img/hero-living-room.webp",
        "logo": BIZ["origin"] + "/favicon.svg",
        "slogan": "Organizing with a touch of design",
        "description": "Professional home organizing with a touch of design in Fort Lauderdale and Broward County, Florida.",
        "address": {"@type": "PostalAddress", "addressLocality": BIZ["city"], "addressRegion": BIZ["state"],
                    "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": BIZ["lat"], "longitude": BIZ["lng"]},
        "areaServed": [{"@type": "City", "name": a} for a in
                       ["Fort Lauderdale", "Wilton Manors", "Oakland Park", "Lauderdale-by-the-Sea", "Plantation",
                        "Davie", "Weston", "Coral Springs", "Hollywood", "Pompano Beach"]],
        "knowsAbout": ["Home organizing", "Closet organization", "Pantry organization", "Decluttering",
                       "Unpacking services", "Home office organization"],
    }


def website_schema():
    return {"@type": "WebSite", "@id": BIZ["origin"] + "/#website", "url": BIZ["origin"] + "/", "name": BIZ["name"],
            "publisher": {"@id": BIZ["origin"] + "/#business"}}


def crumbs_schema(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": html.unescape(n), "item": BIZ["origin"] + (u if u != "/" else "/")}
        for i, (n, u) in enumerate(trail)]}


def faq_schema(faqs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": html.unescape(q), "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a)}}
        for q, a in faqs]}

# ----------------------------------------------------------------- layout

NAV = [("About", "/about"), ("Blog", "/blog"), ("Free Tools", "/tools"), ("Service Area", "/service-area"),
       ("Contact", "/contact")]


def header(path):
    def cur(u):
        return ' aria-current="page"' if path == u or (u != "/" and path.startswith(u + "/")) else ""
    drop = "".join(
        '<a href="/services/{s}"><span class="di">{i}</span><span><strong>{n}</strong><small>{b}</small></span></a>'.format(
            s=s["slug"], i=icon(s["icon"]), n=esc(s["name"]), b=esc(" ".join(s["short"].split()[:9]) + "…"))
        for s in SERVICES)
    nav = ('<div class="nav-drop"><button type="button" aria-haspopup="true">Services %s</button>'
           '<div class="drop-panel">%s<a class="drop-all" href="/services">View all services %s</a></div></div>') % (
        icon("chevron-down"), drop, icon("arrow-right"))
    nav += "".join('<a href="%s"%s>%s</a>' % (u, cur(u), n) for n, u in NAV)
    msub = "".join('<li><a href="/services/%s">%s%s</a></li>' % (s["slug"], icon(s["icon"]), esc(s["name"])) for s in SERVICES)
    mlinks = ('<li><button type="button" class="m-sub-toggle" aria-expanded="false" aria-controls="m-services">Services %s</button>'
              '<ul class="m-sub" id="m-services"><li><a href="/services">%sAll services</a></li>%s</ul></li>') % (
        icon("chevron-down"), icon("layers"), msub)
    mlinks += '<li><a href="/">Home</a></li>' + "".join('<li><a href="%s">%s</a></li>' % (u, n) for n, u in NAV)
    return """<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap header-inner">
    {brand}
    <nav class="main-nav" aria-label="Main">{nav}</nav>
    <div class="header-cta">
      <a class="btn btn-terra btn-sm" href="/contact">Book a consultation {arrow}</a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="mobile-nav" aria-label="Open menu"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="mobile-nav" id="mobile-nav" aria-hidden="true" inert>
  <nav aria-label="Mobile"><ul class="m-links">{mlinks}</ul></nav>
  <div class="m-foot">
    <a class="btn btn-terra" href="/contact">Book a consultation {arrow}</a>
    <a class="m-mail" href="mailto:{email}">{mail} {email}</a>
  </div>
</div>""".format(brand=brand(), nav=nav, arrow=icon("arrow-right"), mlinks=mlinks, email=BIZ["email"], mail=icon("mail"))


def footer():
    svc = "".join('<li><a href="/services/%s">%s</a></li>' % (s["slug"], esc(s["name"])) for s in SERVICES)
    return """<footer class="site-footer">
  <div class="footer-big" aria-hidden="true">a sorted space is a work of art</div>
  <div class="wrap">
    <div class="footer-grid">
      <div>
        {brand}
        <p class="footer-blurb">Professional home organizing with a touch of design for Fort Lauderdale and Broward County homes, condos and home offices.</p>
        <a class="btn btn-light btn-sm" href="mailto:{email}">{mail} {email}</a>
      </div>
      <div><h4>Services</h4><ul>{svc}</ul></div>
      <div><h4>Explore</h4><ul>
        <li><a href="/about">About</a></li><li><a href="/services">All services</a></li><li><a href="/service-area">Service area</a></li>
        <li><a href="/blog">Organizing blog</a></li><li><a href="/contact">Contact</a></li></ul></div>
      <div><h4>Free tools</h4><ul>
        <li><a href="/tools/organizing-time-estimator">Time estimator</a></li>
        <li><a href="/tools/declutter-decision-helper">Keep or let go?</a></li>
        <li><a href="/tools/30-day-declutter-challenge">30-day challenge</a></li>
        <li><a href="/tools/closet-rod-calculator">Closet rod calculator</a></li></ul>
        <h4 style="margin-top:28px">Based in</h4><p style="margin:0;font-size:.94rem">Fort Lauderdale, FL<br>Serving Broward County</p></div>
    </div>
    <div class="footer-bottom">
      <span>&copy; {year} Organized by Anne. All rights reserved.</span>
      <nav aria-label="Legal"><a href="/privacy-policy">Privacy</a><a href="/terms">Terms</a><a href="/sitemap.xml">Sitemap</a></nav>
    </div>
  </div>
</footer>
<button class="to-top" type="button" aria-label="Back to top">{arrow}</button>""".format(
        brand=brand(), email=BIZ["email"], mail=icon("mail"), svc=svc, year=date.today().year, arrow=icon("arrow-right"))


def layout(path, title, desc, body, schema=(), og_image="hero-living-room", og_type="website", extra_js="", head_extra=""):
    url = BIZ["origin"] + (path if path != "/" else "/")
    graph = {"@context": "https://schema.org", "@graph": [org_schema(), website_schema()] + list(schema)}
    full_title = title if "Organized by Anne" in title else title + " | Organized by Anne"
    return """<!doctype html>
<html lang="en-US" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<link rel="canonical" href="{u}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="{ot}">
<meta property="og:site_name" content="Organized by Anne">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{u}">
<meta property="og:image" content="{o}/assets/img/{img}.webp">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{o}/assets/img/{img}.webp">
<meta name="theme-color" content="#fbf7f2">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{fonts}">
<link rel="stylesheet" href="/assets/css/site.css?v={v}">
{he}<script type="application/ld+json">{ld}</script>
</head>
<body>
{header}
<main id="main">
{body}
</main>
{footer}
<script src="/assets/js/site.js?v={v}" defer></script>{xj}
</body>
</html>
""".format(t=esc(full_title), d=esc(desc), u=url, ot=og_type, o=BIZ["origin"], img=og_image, fonts=FONTS, v=VERSION,
           ld=json.dumps(graph, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/"), header=header(path), body=body,
           footer=footer(), xj=extra_js, he=head_extra)


def breadcrumbs(trail):
    items = []
    for i, (n, u) in enumerate(trail):
        if i == len(trail) - 1:
            items.append('<li aria-current="page">%s</li>' % n)
        else:
            items.append('<li><a href="%s">%s</a></li>' % (u, n))
    return '<ol class="crumbs">%s</ol>' % "".join(items)


def page_hero(trail, eyebrow, h1, lead, image=None, alt=""):
    if image:
        return """<section class="page-hero">
  <div class="blob blob-1" aria-hidden="true"></div>
  <div class="wrap page-hero-split">
    <div class="reveal">
      <nav aria-label="Breadcrumb">{c}</nav>
      <span class="eyebrow">{e}</span>
      <h1>{h}</h1>
      <p class="lead">{l}</p>
      <div class="hero-actions"><a class="btn btn-terra" href="/contact">Book a consultation {a}</a><a class="btn btn-ghost" href="/tools/organizing-time-estimator">Estimate your project</a></div>
    </div>
    <div class="hero-media reveal-img">{i}</div>
  </div>
</section>""".format(c=breadcrumbs(trail), e=eyebrow, h=h1, l=lead, a=icon("arrow-right"),
                     i=img(image, alt, "(max-width: 900px) 100vw, 45vw", lazy=False))
    return """<section class="page-hero">
  <div class="blob blob-1" aria-hidden="true"></div><div class="blob blob-2" aria-hidden="true"></div>
  <div class="wrap reveal">
    <nav aria-label="Breadcrumb">{c}</nav>
    <span class="eyebrow">{e}</span>
    <h1>{h}</h1>
    <p class="lead">{l}</p>
  </div>
</section>""".format(c=breadcrumbs(trail), e=eyebrow, h=h1, l=lead)


def faq_block(faqs, heading="Frequently asked questions"):
    items = "".join('<details><summary>%s</summary><p>%s</p></details>' % (esc(q), esc(a)) for q, a in faqs)
    return '<h2 id="faq">%s</h2><div class="faq">%s</div>' % (heading, items)


def cta_band(title="Ready for a calmer home?", text="Tell us about the space that's stressing you out. We'll reply within one business day with next steps for an in-home or virtual consultation."):
    return """<section class="section-tight"><div class="wrap">
  <div class="cta-band reveal">
    <div class="blob blob-1" aria-hidden="true"></div>
    <div style="position:relative"><h2>{t}</h2><p>{x}</p></div>
    <div class="actions"><a class="btn btn-light" href="/contact">Book a consultation {a}</a><a class="btn btn-ghost" style="--fg:#fff;border-color:rgba(255,255,255,.35)" href="mailto:{e}">{m} Email us</a></div>
  </div>
</div></section>""".format(t=title, x=text, a=icon("arrow-right"), e=BIZ["email"], m=icon("mail"))


def svc_card(s, i=0):
    im, alt = SVC_IMG[s["slug"]]
    return """<a class="svc-card reveal" style="--d:{d}s" href="/services/{slug}" data-tilt>
  <div class="ph">{img}<span class="ic">{ic}</span></div>
  <div class="body"><h3>{n}</h3><p>{b}</p><span class="more">Explore {n2} {a}</span></div>
</a>""".format(d=(i % 4) * 0.08, slug=s["slug"], img=img(im, alt, "(max-width: 600px) 100vw, 300px"), ic=icon(s["icon"]),
               n=esc(s["name"]), n2=esc(s["name"].lower()), b=esc(s["short"]), a=icon("arrow-right"))


def post_card(p, i=0):
    im, alt = POST_IMG[p["slug"]]
    return """<a class="post-card reveal" style="--d:{d}s" href="/blog/{slug}" data-cat="{cs}">
  <div class="ph">{img}</div>
  <div class="post-meta"><span class="cat">{c}</span><span>{date}</span><span>{m} min read</span></div>
  <h3>{t}</h3><p>{e}</p>
</a>""".format(d=(i % 3) * 0.08, slug=p["slug"], img=img(im, alt, "(max-width: 600px) 100vw, 380px"), c=esc(p["category"]),
               cs=slugify(p["category"]), date=nice_date(p["date"]), m=max(3, round(words(p["body_html"]) / 230)),
               t=esc(p["h1"]), e=esc(p["excerpt"]))


def nice_date(iso):
    y, m, d = map(int, iso.split("-"))
    return date(y, m, d).strftime("%b %-d, %Y")


def tool_cards():
    out = []
    for i, (slug, ic, t, d) in enumerate(PC.TOOLS):
        out.append('<a class="tool-card reveal" style="--d:%ss" href="/tools/%s"><span class="ti">%s</span><h3>%s</h3><p>%s</p>'
                   '<span class="more">Try it free %s</span></a>' % (i * 0.08, slug, icon(ic), t, d, icon("arrow-right")))
    return "".join(out)


def process_steps():
    steps = "".join('<div class="step" style="--d:%ss"><span class="num">%s</span><div><h3>%s</h3><p>%s</p></div></div>' % (
        0.3 + i * 0.3, icon(ic), t, d) for i, (ic, t, d) in enumerate(PC.PROCESS))
    return '<div class="process" data-reveal><span class="bar"></span>%s</div>' % steps


def link_body(htm):
    """Add ids to h2s and wrap tables so they scroll on phones."""
    toc = []

    def h2(m):
        text = m.group(1)
        hid = slugify(text)
        toc.append((hid, re.sub(r"<[^>]+>", "", text)))
        return '<h2 id="%s">%s</h2>' % (hid, text)
    htm = re.sub(r"<h2>(.*?)</h2>", h2, htm, flags=re.S)
    htm = re.sub(r"(<table class=\"table\">.*?</table>)", r'<div class="table-wrap">\1</div>', htm, flags=re.S)
    return htm, toc

# ----------------------------------------------------------------- pages

OUT = {}


def write(path, content):
    OUT[path] = content


def build_home():
    calm = []
    for i, (ic, color, mx, my, mr) in enumerate(PC.CALM_ITEMS):
        tx = 10 + (i % 4) * 21
        ty = 7 + (i // 4) * 25
        calm.append('<span class="calm-item" style="--mx:%s%%;--my:%s%%;--mr:%sdeg;--tx:%s%%;--ty:%s%%;--dl:%ss;background:%s">%s</span>' % (
            mx, my, mr, tx, ty, round(i * 0.05, 2), color, icon(ic)))
    picker_data = {k: dict(v, img="/assets/img/%s.webp" % v["img"]) for k, v in PC.PICKER.items()}
    first = next(iter(PC.PICKER))
    fp = PC.PICKER[first]
    chips = "".join('<button type="button" class="chip" data-key="%s" aria-pressed="%s">%s</button>' % (
        k, "true" if k == first else "false", v["label"]) for k, v in PC.PICKER.items())
    rot = "".join('<span%s>%s</span>' % (' class="is-active"' if i == 0 else "", w) for i, w in enumerate(PC.ROTATE))
    marquee = "".join("<span>%s</span>" % w for w in PC.MARQUEE * 2)
    svc_cards = "".join(svc_card(s, i) for i, s in enumerate(SERVICES))
    posts = "".join(post_card(p, i) for i, p in enumerate(POSTS[:3]))
    tags = "".join("<span>%s</span>" % a for a in AREAS[:12])
    faqs = PC.HOME_FAQS
    body = PC.HOME_TEMPLATE.format(
        arrow=icon("arrow-right"), check=icon("circle-check"), sparkles=icon("sparkles"), rot=rot,
        hero_img=img("hero-living-room", "Serene, organized living room styled with neutral textiles and plants", "(max-width: 900px) 100vw, 46vw", lazy=False),
        fc1=img("closet-rail", "Organized clothing rail with matching hangers", "200px"),
        fc2=img("laundry-baskets", "Laundry shelves with labeled woven baskets", "200px"),
        marquee=marquee, calm="".join(calm),
        svc_cards=svc_cards,
        about_a=img("styled-sideboard", "Styled sideboard with plants, a mirror and an accent chair", "(max-width: 900px) 100vw, 40vw"),
        about_b=img("neutral-wardrobe", "Neutral sweaters hanging neatly beside dried pampas grass", "240px"),
        leaf=icon("leaf"), palette=icon("palette"), heart=icon("hand-heart"),
        process=process_steps(),
        chips=chips, picker_json=json.dumps(picker_data).replace("</", "<\\/"),
        p_img=img(fp["img"], fp["alt"], "(max-width: 600px) 100vw, 300px"), p_title=fp["title"], p_tip=fp["tip"],
        p_href=fp["href"], p_cta=fp["cta"],
        tools=tool_cards(),
        area_img=img("palm-beach", "Palm trees and high-rise condos along a South Florida beach", "100vw", extra=' data-parallax'),
        tags=tags, posts=posts,
        faq=faq_block(faqs, "Questions, answered"),
        email=BIZ["email"], mail=icon("mail"), send=icon("send"),
    )
    schema = [faq_schema(faqs), {"@type": "WebPage", "@id": BIZ["origin"] + "/#webpage", "url": BIZ["origin"] + "/",
                                 "name": PC.HOME_TITLE, "about": {"@id": BIZ["origin"] + "/#business"}}]
    write("/", layout("/", PC.HOME_TITLE, PC.HOME_DESC, body, schema))


def build_about():
    trail = [("Home", "/"), ("About", "/about")]
    body = page_hero(trail, "About Organized by Anne", "Organizing with a touch of design, rooted in Fort Lauderdale",
                     "We believe your home should support the life you're living right now — and that a sorted space can be a work of art.",
                     "styled-sideboard", "Styled sideboard with plants, a mirror and an accent chair")
    body += PC.ABOUT_BODY.format(
        a=img("neutral-wardrobe", "Neutral wardrobe on a rail beside pampas grass", "(max-width: 900px) 100vw, 40vw"),
        b=img("plant-desk", "Bright room with plants, shelves and a reading chair", "240px"),
        leaf=icon("leaf"), palette=icon("palette"), heart=icon("hand-heart"), arrow=icon("arrow-right"),
        process=process_steps(), svc_cards="".join(svc_card(s, i) for i, s in enumerate(SERVICES[:4])),
        faq=faq_block(PC.ABOUT_FAQS))
    body += cta_band()
    schema = [crumbs_schema(trail), faq_schema(PC.ABOUT_FAQS),
              {"@type": "AboutPage", "url": BIZ["origin"] + "/about", "name": "About Organized by Anne",
               "about": {"@id": BIZ["origin"] + "/#business"}}]
    write("/about", layout("/about", "About Organized by Anne | Fort Lauderdale Home Organizer",
                           "Meet Organized by Anne, a Fort Lauderdale home organizing studio that pairs practical systems with a touch of design for homes, condos and offices.",
                           body, schema, og_image="styled-sideboard"))


def build_services():
    trail = [("Home", "/"), ("Services", "/services")]
    body = page_hero(trail, "Services", "Home organizing services in Fort Lauderdale",
                     "From a single overflowing closet to a whole-home reset after a move, every project starts with a consultation and ends with a system that fits the way you live — finished with a touch of design.")
    body += '<section class="section-tight"><div class="wrap"><div class="card-grid">%s</div></div></section>' % "".join(
        svc_card(s, i) for i, s in enumerate(SERVICES))
    body += PC.SERVICES_BODY.format(process=process_steps(), arrow=icon("arrow-right"), check=icon("circle-check"),
                                    faq=faq_block(PC.SERVICES_FAQS))
    body += cta_band()
    schema = [crumbs_schema(trail), faq_schema(PC.SERVICES_FAQS),
              {"@type": "ItemList", "itemListElement": [
                  {"@type": "ListItem", "position": i + 1, "url": BIZ["origin"] + "/services/" + s["slug"], "name": html.unescape(s["name"])}
                  for i, s in enumerate(SERVICES)]}]
    write("/services", layout("/services", "Home Organizing Services in Fort Lauderdale",
                              "Home organizing services in Fort Lauderdale: closets, kitchens and pantries, decluttering, unpacking, home offices and virtual consultations.",
                              body, schema, og_image="home-organizing"))
    for s in SERVICES:
        build_service(s)


def build_service(s):
    path = "/services/" + s["slug"]
    trail = [("Home", "/"), ("Services", "/services"), (esc(s["name"]), path)]
    im, alt = SVC_IMG[s["slug"]]
    body = page_hero(trail, esc(s["name"]), esc(s["h1"]), esc(s["short"]), im, alt)
    prose, _ = link_body(s["body_html"])
    includes = "".join("<li>%s<span>%s</span></li>" % (icon("circle-check"), esc(x)) for x in s["includes"])
    others = "".join('<li><a href="/services/%s"%s>%s %s</a></li>' % (
        o["slug"], ' aria-current="page"' if o is s else "", esc(o["name"]), icon("arrow-right")) for o in SERVICES)
    related = [p for p in POSTS if ("/services/" + s["slug"]) in p["body_html"]][:3] or POSTS[:3]
    if len(related) < 3:
        related += [p for p in POSTS if p not in related][:3 - len(related)]
    body += """<section class="section-tight"><div class="wrap content-grid">
  <article class="prose reveal">{prose}{faq}</article>
  <aside class="sidebar">
    <div class="side-card"><h3>What's included</h3><ul class="includes">{inc}</ul></div>
    <div class="side-card dark"><h3>Start with a consultation</h3><p>Tell us about your space and we'll suggest the right plan — in person in Broward County, or by video anywhere.</p>
      <a class="btn btn-terra" href="/contact">Book a consultation {arrow}</a></div>
    <div class="side-card"><h3>All services</h3><ul class="side-links">{others}</ul></div>
  </aside>
</div></section>
<section class="section section-sand"><div class="wrap">
  <div class="section-head"><span class="eyebrow">From the blog</span><h2>Ideas you can use today</h2></div>
  <div class="card-grid posts">{posts}</div>
</div></section>""".format(prose=prose, faq=faq_block(s["faqs"]), inc=includes, arrow=icon("arrow-right"), others=others,
                           posts="".join(post_card(p, i) for i, p in enumerate(related)))
    body += cta_band()
    schema = [crumbs_schema([(html.unescape(n), u) for n, u in trail]), faq_schema(s["faqs"]),
              {"@type": "Service", "name": html.unescape(s["name"]), "serviceType": html.unescape(s["keyword"]),
               "description": html.unescape(s["description"]), "url": BIZ["origin"] + path,
               "provider": {"@id": BIZ["origin"] + "/#business"},
               "areaServed": {"@type": "AdministrativeArea", "name": "Broward County, Florida"},
               "image": BIZ["origin"] + "/assets/img/%s.webp" % im}]
    write(path, layout(path, s["title"], s["description"], body, schema, og_image=im))


def build_blog():
    trail = [("Home", "/"), ("Blog", "/blog")]
    cats = []
    for p in POSTS:
        if p["category"] not in cats:
            cats.append(p["category"])
    chips = '<button type="button" class="chip" data-cat="all" aria-pressed="true">All posts</button>' + "".join(
        '<button type="button" class="chip" data-cat="%s" aria-pressed="false">%s</button>' % (slugify(c), esc(c)) for c in cats)
    body = page_hero(trail, "The Organized Home Journal", "Home organizing tips &amp; ideas",
                     "Practical, design-minded advice for calmer closets, kitchens and everyday routines — with a few Florida-specific lessons on humidity, hurricane season and seasonal living.")
    body += '<section class="section-tight"><div class="wrap"><div class="blog-filter" role="group" aria-label="Filter posts by topic">%s</div><div class="card-grid posts">%s</div></div></section>' % (
        chips, "".join(post_card(p, i) for i, p in enumerate(POSTS)))
    body += cta_band("Want a pro to do it with you?")
    schema = [crumbs_schema(trail), {"@type": "Blog", "url": BIZ["origin"] + "/blog", "name": "Organized by Anne Blog",
                                     "blogPost": [{"@type": "BlogPosting", "headline": html.unescape(p["h1"]), "url": BIZ["origin"] + "/blog/" + p["slug"],
                                                   "datePublished": p["date"]} for p in POSTS]}]
    write("/blog", layout("/blog", "Home Organizing Tips & Ideas Blog",
                          "Home organizing tips and ideas from Organized by Anne: decluttering, closets, pantries, small spaces, home offices and Florida living.",
                          body, schema, og_image="boho-living"))
    for p in POSTS:
        build_post(p)


def build_post(p):
    path = "/blog/" + p["slug"]
    trail = [("Home", "/"), ("Blog", "/blog"), (esc(p["h1"]), path)]
    im, alt = POST_IMG[p["slug"]]
    prose, toc = link_body(p["body_html"])
    mins = max(3, round(words(p["body_html"]) / 230))
    toc_html = "".join('<li><a href="#%s">%s</a></li>' % (h, esc(t)) for h, t in toc)
    related = [x for x in POSTS if x["category"] == p["category"] and x is not p]
    related += [x for x in POSTS if x not in related and x is not p]
    svc = next((s for s in SERVICES if ("/services/" + s["slug"]) in p["body_html"]), SERVICES[0])
    body = """<div class="progress" aria-hidden="true"></div>
<section class="page-hero article-head">
  <div class="blob blob-1" aria-hidden="true"></div>
  <div class="narrow reveal">
    <nav aria-label="Breadcrumb">{crumbs}</nav>
    <div class="post-meta"><span class="cat">{cat}</span><span>{date}</span><span>{mins} min read</span></div>
    <h1>{h1}</h1>
    <p class="lead">{ex}</p>
  </div>
  <div class="wrap"><div class="hero-media reveal-img">{img}</div></div>
</section>
<section class="section-tight"><div class="wrap content-grid">
  <article class="prose" data-article>{prose}{faq}
    <div class="share-row"><strong>Found this useful?</strong>
      <a class="btn btn-ghost btn-sm" href="mailto:?subject={qt}&amp;body={qu}">{mail} Email it to a friend</a>
      <a class="btn btn-ghost btn-sm" href="/blog">More articles {arrow}</a></div>
  </article>
  <aside class="sidebar">
    <div class="side-card"><h3>In this article</h3><ol class="toc">{toc}</ol></div>
    <div class="side-card dark"><h3>{sname}</h3><p>{sshort}</p><a class="btn btn-terra" href="/services/{sslug}">See the service {arrow}</a></div>
    <div class="side-card"><h3>Free tools</h3><ul class="side-links">{tools}</ul></div>
  </aside>
</div></section>
<section class="section section-sand"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Keep reading</span><h2>Related articles</h2></div>
  <div class="card-grid posts">{rel}</div>
</div></section>""".format(
        crumbs=breadcrumbs(trail), cat=esc(p["category"]), date=nice_date(p["date"]), mins=mins, h1=esc(p["h1"]),
        ex=esc(p["excerpt"]), img=img(im, alt, "100vw", lazy=False), prose=prose, faq=faq_block(p["faqs"]),
        qt=esc(html.unescape(p["h1"]).replace(" ", "%20")), qu=esc(BIZ["origin"] + path), mail=icon("mail"), arrow=icon("arrow-right"),
        toc=toc_html, sname=esc(svc["name"]), sshort=esc(svc["short"]), sslug=svc["slug"],
        tools="".join('<li><a href="/tools/%s">%s %s</a></li>' % (s, t, icon("arrow-right")) for s, _, t, _ in PC.TOOLS),
        rel="".join(post_card(x, i) for i, x in enumerate(related[:3])))
    body += cta_band()
    schema = [crumbs_schema([(html.unescape(n), u) for n, u in trail]), faq_schema(p["faqs"]),
              {"@type": "BlogPosting", "headline": html.unescape(p["h1"]), "description": html.unescape(p["description"]),
               "datePublished": p["date"], "dateModified": p["date"], "url": BIZ["origin"] + path,
               "mainEntityOfPage": BIZ["origin"] + path, "image": BIZ["origin"] + "/assets/img/%s.webp" % im,
               "wordCount": words(p["body_html"]), "articleSection": html.unescape(p["category"]),
               "author": {"@type": "Organization", "name": BIZ["name"], "url": BIZ["origin"] + "/about"},
               "publisher": {"@id": BIZ["origin"] + "/#business"}}]
    head = '<meta property="article:published_time" content="%sT09:00:00-04:00">\n' % p["date"]
    write(path, layout(path, p["title"], p["description"], body, schema, og_image=im, og_type="article", head_extra=head))


def build_contact():
    trail = [("Home", "/"), ("Contact", "/contact")]
    spaces = "".join('<label><input type="checkbox" name="spaces[]" value="%s"><span class="chip">%s</span></label>' % (esc(x), esc(x))
                     for x in ["Closet", "Kitchen / pantry", "Whole home", "Decluttering", "Move / unpacking", "Home office",
                               "Bathroom / laundry", "Garage", "Kids' rooms", "Virtual consult"])
    body = page_hero(trail, "Let's connect", "Contact Organized by Anne",
                     "Tell us a little about your space and what's not working. We'll reply within one business day to set up your consultation — in person in Broward County, or by video from anywhere.")
    body += PC.CONTACT_BODY.format(email=BIZ["email"], mail=icon("mail"), pin=icon("map-pin"), clock=icon("clock"),
                                   video=icon("video"), spaces=spaces, send=icon("send"),
                                   img=img("cozy-living", "Tidy living room with a blue sofa and framed print", "(max-width: 900px) 100vw, 40vw"),
                                   faq=faq_block(PC.CONTACT_FAQS))
    schema = [crumbs_schema(trail), faq_schema(PC.CONTACT_FAQS),
              {"@type": "ContactPage", "url": BIZ["origin"] + "/contact", "name": "Contact Organized by Anne"}]
    write("/contact", layout("/contact", "Contact a Fort Lauderdale Professional Organizer",
                             "Contact Organized by Anne to book an in-home organizing consultation in Fort Lauderdale and Broward County, or a virtual session from anywhere.",
                             body, schema, og_image="cozy-living"))


def build_area():
    trail = [("Home", "/"), ("Service Area", "/service-area")]
    body = page_hero(trail, "Service area", "Professional organizing across Fort Lauderdale &amp; Broward County",
                     "We're based in Fort Lauderdale and work in homes, condos and high-rises throughout Broward County. Outside the area? Our virtual consultations work anywhere.",
                     "palm-beach", "Palm trees and high-rise condos along a South Florida beach")
    tags = "".join("<span class='chip'>%s %s</span>" % (icon("map-pin"), a) for a in AREAS)
    body += PC.AREA_BODY.format(tags=tags, arrow=icon("arrow-right"), check=icon("circle-check"),
                                img=img("tropical-pool", "Palm trees around a tropical pool", "(max-width: 900px) 100vw, 45vw"),
                                faq=faq_block(PC.AREA_FAQS))
    body += cta_band()
    schema = [crumbs_schema(trail), faq_schema(PC.AREA_FAQS)]
    write("/service-area", layout("/service-area", "Fort Lauderdale & Broward County Service Area",
                                  "Organized by Anne serves Fort Lauderdale, Wilton Manors, Plantation, Weston, Coral Springs, Hollywood, Pompano Beach and nearby Broward County cities.",
                                  body, schema, og_image="palm-beach"))


TOOL_ICONS = ["rotate-ccw", "refresh-cw", "heart", "house", "box", "hand-heart", "tag", "gift", "recycle", "trash-2"]


def icon_templates():
    return "".join('<template id="i-%s">%s</template>' % (n, icon(n)) for n in TOOL_ICONS)


def build_tools():
    trail = [("Home", "/"), ("Free Tools", "/tools")]
    body = page_hero(trail, "Free organizing tools", "Free home organizing tools &amp; calculators",
                     "Interactive helpers to plan your project, make faster keep-or-let-go decisions, build a daily decluttering habit and size your closet — no sign-up needed.")
    body += '<section class="section-tight"><div class="wrap"><div class="card-grid">%s</div></div></section>' % tool_cards()
    body += cta_band("Prefer a pro to plan it with you?")
    write("/tools", layout("/tools", "Free Home Organizing Tools & Calculators",
                           "Free home organizing tools: an organizing time estimator, a keep-or-let-go decision helper, a 30-day declutter challenge and a closet rod calculator.",
                           body, [crumbs_schema(trail)], og_image="planner-board"))
    for t in PC.TOOL_PAGES:
        path = "/tools/" + t["slug"]
        tr = [("Home", "/"), ("Free Tools", "/tools"), (t["name"], path)]
        body = page_hero(tr, "Free tool", t["h1"], t["lead"])
        widget = t["widget"].format(arrow=icon("arrow-right"), check=icon("circle-check"), refresh=icon("refresh-cw"),
                                    rotate=icon("rotate-ccw"), calendar=icon("calendar"), json=json.dumps(PC.DECISION).replace("</", "<\\/"),
                                    rooms=PC.estimator_rooms(icon), days=PC.challenge_days(), ruler=icon("ruler"))
        body += '<section class="section-tight"><div class="wrap">%s</div></section>' % widget
        body += '<section class="section-tight"><div class="narrow prose reveal">%s%s</div></section>' % (t["body"], faq_block(t["faqs"]))
        body += cta_band()
        schema = [crumbs_schema(tr), faq_schema(t["faqs"]),
                  {"@type": "WebApplication", "name": t["name"], "url": BIZ["origin"] + path, "applicationCategory": "LifestyleApplication",
                   "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
                   "provider": {"@id": BIZ["origin"] + "/#business"}}]
        write(path, layout(path, t["title"], t["description"], body + icon_templates(), schema, og_image=t["img"],
                           extra_js='\n<script src="/assets/js/tools.js?v=%s" defer></script>' % VERSION))


def build_legal():
    for slug, title, desc, content in PC.LEGAL:
        path = "/" + slug
        trail = [("Home", "/"), (title, path)]
        body = page_hero(trail, "Legal", title, "Last updated %s." % nice_date(TODAY))
        body += '<section class="section-tight"><div class="narrow prose">%s</div></section>' % content.format(email=BIZ["email"])
        write(path, layout(path, title, desc, body, [crumbs_schema(trail)]))


def build_404():
    body = """<section class="err-hero"><div class="wrap">
  <div class="code">404</div><h1>This page has been decluttered</h1>
  <p class="lead">We couldn't find what you were looking for — but everything else is right where it belongs.</p>
  <div class="hero-actions" style="justify-content:center"><a class="btn btn-terra" href="/">Back to home {a}</a><a class="btn btn-ghost" href="/services">Our services</a><a class="btn btn-ghost" href="/blog">Read the blog</a></div>
</div></section>""".format(a=icon("arrow-right"))
    page = layout("/404", "Page not found", "The page you were looking for could not be found.", body)
    page = page.replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">')
    page = re.sub(r'<link rel="canonical"[^>]*>\n', "", page)
    write("/404", page)


def sitemap():
    urls = []
    for path in OUT:
        if path == "/404":
            continue
        pr = "1.0" if path == "/" else "0.8" if path.count("/") == 1 else "0.6"
        lastmod = TODAY
        if path.startswith("/blog/"):
            lastmod = next(p["date"] for p in POSTS if "/blog/" + p["slug"] == path)
        urls.append("<url><loc>%s%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>" % (
            BIZ["origin"], path if path != "/" else "/", lastmod, pr))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s\n</urlset>\n'
            % "\n".join(urls))


def out_file(path):
    return os.path.join(ROOT, "pages", "home.html" if path == "/" else path.strip("/") + ".html")


VERSION = TODAY.replace("-", "")


def main():
    build_home()
    build_about()
    build_services()
    build_blog()
    build_contact()
    build_area()
    build_tools()
    build_legal()
    build_404()
    pages_dir = os.path.join(ROOT, "pages")
    keep = set()
    for path, content in OUT.items():
        f = out_file(path)
        os.makedirs(os.path.dirname(f), exist_ok=True)
        with open(f, "w") as fh:
            fh.write(content)
        keep.add(f)
    for d, _, files in os.walk(pages_dir):
        for name in files:
            f = os.path.join(d, name)
            if f not in keep:
                os.remove(f)
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as fh:
        fh.write(sitemap())
    with open(os.path.join(ROOT, "routes.json"), "w") as fh:
        json.dump(sorted(OUT), fh, indent=0)
    print("built %d pages, %d services, %d posts" % (len(OUT), len(SERVICES), len(POSTS)))


if __name__ == "__main__":
    main()
