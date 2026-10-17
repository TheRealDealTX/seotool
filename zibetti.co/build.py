#!/usr/bin/env python3
"""Static site generator for zibetti.co (Zibetti Photo + Film).

Writes every page into ./site. Run:  python3 build.py && python3 validate.py
Hand-written assets (css, js, images) live in site/assets and are not touched.
"""

import html
import json
import os
import shutil
from datetime import date

from posts import POSTS

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
ORIGIN = "https://zibetti.co"
BRAND = "Zibetti Photo + Film"
EMAIL = "info@zibetti.co"
TODAY = date.today().isoformat()

NAV = [
    ("Portfolio", "/portfolio/"),
    ("About", "/about-us/"),
    ("Film", "/video/"),
    ("Pricing", "/pricing/"),
    ("Journal", "/blog/"),
    ("Tools", "/tools/"),
    ("FAQ", "/faq/"),
]

ICONS = {
    "sun": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "map": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2-6-2z"/><path d="M9 4v14M15 6v14"/></svg>',
    "calc": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 11h2M12 11h2M16 11h0M8 15h2M12 15h2M8 18h2M12 18h4"/></svg>',
    "play": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M6 4l14 8-14 8z"/></svg>',
    "up": '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg>',
}

TOOLS = [
    ("/tools/golden-hour-calculator/", "Golden Hour Calculator", "sun",
     "Find golden hour, blue hour and sunset for any date at Utah’s best elopement spots — or anywhere in the world."),
    ("/tools/wedding-day-timeline-builder/", "Wedding Day Timeline Builder", "clock",
     "Build a photographer-approved wedding or elopement timeline around your real sunset time."),
    ("/tools/utah-elopement-location-finder/", "Utah Elopement Location Finder", "map",
     "Filter 20 Utah locations by season, scenery, hiking and drive time to find your spot."),
]


def esc(s):
    return html.escape(s, quote=True)


def img(name, alt, cls="", sizes="100vw", lazy=True, w=1800, h=1200, extra=""):
    """Responsive <img> using the full and -sm webp variants."""
    attrs = [
        f'src="/assets/img/{name}.webp"',
        f'srcset="/assets/img/{name}-sm.webp 900w, /assets/img/{name}.webp 1800w"',
        f'sizes="{sizes}"',
        f'alt="{esc(alt)}"',
        f'width="{w}" height="{h}"',
    ]
    if cls:
        attrs.append(f'class="{cls}"')
    if lazy:
        attrs.append('loading="lazy" decoding="async"')
    else:
        attrs.append('fetchpriority="high"')
    if extra:
        attrs.append(extra)
    return "<img " + " ".join(attrs) + ">"


ORG = {
    "@type": ["ProfessionalService", "LocalBusiness"],
    "@id": ORIGIN + "/#business",
    "name": BRAND,
    "alternateName": ["Zibetti & Co", "Zibetti Photo and Film"],
    "url": ORIGIN + "/",
    "email": EMAIL,
    "image": ORIGIN + "/assets/img/mountain-elopement-couple.webp",
    "logo": ORIGIN + "/favicon.svg",
    "description": "Destination wedding and elopement photographers and filmmakers based in Provo, Utah.",
    "address": {"@type": "PostalAddress", "addressLocality": "Provo", "addressRegion": "UT", "addressCountry": "US"},
    "areaServed": ["Utah", "United States", "Worldwide"],
    "priceRange": "$$$",
    "knowsAbout": ["Wedding photography", "Elopement photography", "Wedding videography", "Engagement photography"],
}
WEBSITE = {"@type": "WebSite", "@id": ORIGIN + "/#website", "url": ORIGIN + "/", "name": BRAND, "publisher": {"@id": ORIGIN + "/#business"}}


def crumbs_schema(trail):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": ORIGIN + u} for i, (n, u) in enumerate(trail)
        ],
    }


def crumbs_html(trail):
    parts = []
    for i, (n, u) in enumerate(trail):
        if i == len(trail) - 1:
            parts.append(f"<span aria-current=\"page\">{esc(n)}</span>")
        else:
            parts.append(f'<a href="{u}">{esc(n)}</a><span>/</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + "".join(parts) + "</nav>"


def header(path, on_hero):
    items = []
    for n, u in NAV:
        cur = ' aria-current="page"' if (path == u or (u != "/" and path.startswith(u))) else ""
        items.append(f'<li><a href="{u}"{cur}>{n}</a></li>')
    items.append('<li><a class="nav-cta" href="/contact-us/">Inquire</a></li>')
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-header{' on-hero' if on_hero else ''}">
  <div class="wrap bar">
    <a class="logo" href="/" aria-label="{BRAND} home"><b>Zibetti</b><small>Photo + Film</small></a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="main-nav" aria-label="Open menu"><span></span><span></span><span></span></button>
    <nav class="main-nav" id="main-nav" aria-label="Main">
      <ul>{''.join(items)}</ul>
      <p class="nav-foot">Destination weddings &amp; elopements · Provo, Utah<br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </nav>
  </div>
</header>"""


def footer():
    tools = "".join(f'<li><a href="{u}">{n}</a></li>' for u, n, _, _ in TOOLS)
    recent = "".join(f'<li><a href="/blog/{p["slug"]}/">{esc(p["short"])}</a></li>' for p in POSTS[:5])
    return f"""<footer class="site-footer">
  <div class="wrap">
    <p class="footer-big reveal">Let’s make something<br><em><a href="/contact-us/">timeless →</a></em></p>
    <div class="footer-grid">
      <div>
        <a class="logo" href="/"><b>Zibetti</b><small>Photo + Film</small></a>
        <p style="margin-top:18px;max-width:34ch">Destination wedding and elopement photographers and filmmakers based in Provo, Utah — traveling anywhere love takes you.</p>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
      <div><h4>Studio</h4><ul>
        <li><a href="/portfolio/">Portfolio</a></li><li><a href="/about-us/">About us</a></li><li><a href="/video/">Wedding film</a></li>
        <li><a href="/pricing/">Pricing</a></li><li><a href="/faq/">FAQ</a></li><li><a href="/contact-us/">Contact</a></li></ul></div>
      <div><h4>Planning tools</h4><ul>{tools}<li><a href="/pricing/#estimator">Pricing estimator</a></li></ul></div>
      <div><h4>From the journal</h4><ul>{recent}</ul></div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>{date.today().year}</span> {BRAND}. All rights reserved.</span>
      <span><a href="/privacy-policy/">Privacy</a> · <a href="/sitemap.xml">Sitemap</a></span>
    </div>
  </div>
</footer>
<button class="to-top" type="button" aria-label="Back to top">{ICONS['up']}</button>"""


def page(path, title, desc, body, *, schema=None, og_image="mountain-elopement-couple", on_hero=True,
         og_type="website", tools_js=False, extra_head="", noindex=False):
    canonical = ORIGIN + path
    graph = [ORG, WEBSITE] + (schema or [])
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    robots = '<meta name="robots" content="noindex,follow">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'
    scripts = '<script src="/assets/js/site.js" defer></script>'
    if tools_js:
        scripts += '\n<script src="/assets/js/tools.js" defer></script>'
    return f"""<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{ORIGIN}/assets/img/{og_image}.webp">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#15120f">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Manrope:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/assets/css/site.css">
{extra_head}<script type="application/ld+json">{ld}</script>
</head>
<body>
{header(path, on_hero)}
<main id="main">
{body}
</main>
{footer()}
{scripts}
</body>
</html>
"""


def page_hero(trail, eyebrow, h1, lead, image, alt, short=False):
    return f"""<section class="page-hero grain{' page-hero--short' if short else ''}">
  {img(image, alt, lazy=False, extra='data-parallax="0.18"')}
  <div class="wrap">
    {crumbs_html(trail)}
    <span class="eyebrow">{eyebrow}</span>
    <h1>{h1}</h1>
    {f'<p class="lead">{lead}</p>' if lead else ''}
  </div>
</section>"""


def cta(title="Tell us about your day", text="Share your date, your dream location and the feeling you want to remember. We reply to every inquiry within two business days.", image="alpenglow-mountain-peak"):
    return f"""<section class="section--tight"><div class="wrap">
  <div class="cta reveal">
    {img(image, "Mountain peaks glowing at sunset", sizes="(max-width: 1240px) 100vw, 1240px")}
    <span class="eyebrow" style="color:#f2c9a8">Now booking {date.today().year + 1}–{date.today().year + 2}</span>
    <h2>{title}</h2>
    <p>{text}</p>
    <div class="hero-actions"><a class="btn btn--light" href="/contact-us/">Start your inquiry <span class="arrow">→</span></a>
    <a class="btn btn--ghost" href="/pricing/">See pricing</a></div>
  </div>
</div></section>"""


def post_cards(posts, feature=False):
    cards = []
    for i, p in enumerate(posts):
        cards.append(f"""<a class="post-card reveal" data-delay="{i % 3}" href="/blog/{p['slug']}/">
  <div class="thumb">{img(p['image'], p['image_alt'], sizes='(max-width: 760px) 100vw, 33vw')}</div>
  <span class="meta">{p['category']} · {p['minutes']} min read</span>
  <h3>{esc(p['title'])}</h3>
  <p>{esc(p['excerpt'])}</p>
</a>""")
    return f'<div class="posts{" posts--feature" if feature else ""}">' + "".join(cards) + "</div>"


def tool_tiles():
    out = []
    for i, (u, n, ico, d) in enumerate(TOOLS):
        out.append(f'<a class="tool-tile reveal" data-delay="{i}" href="{u}"><span class="ico">{ICONS[ico]}</span><h3>{n}</h3><p>{d}</p><span class="link-arrow" style="align-self:flex-start">Open the tool →</span></a>')
    return '<div class="tool-grid">' + "".join(out) + "</div>"


STAMP = """<svg class="stamp" viewBox="0 0 120 120" aria-hidden="true"><defs><path id="c" d="M60,60 m-46,0 a46,46 0 1,1 92,0 a46,46 0 1,1 -92,0"/></defs>
<text><textPath href="#c">photo · film · utah · worldwide · photo · film ·</textPath></text>
<circle cx="60" cy="60" r="4" fill="currentColor"/></svg>"""

# ----------------------------------------------------------------------------------------------
# Pages
# ----------------------------------------------------------------------------------------------

PAGES = {}


def add(path, html_text):
    PAGES[path] = html_text


def build_home():
    slides = [
        ("mountain-elopement-couple", "Couple walking hand in hand through a golden mountain meadow"),
        ("black-sand-beach-elopement", "Bride and groom embracing on a black sand beach"),
        ("fall-lake-wedding-portrait", "Newlyweds smiling beside an autumn lake"),
    ]
    figs = "".join(
        f'<figure class="{"active" if i == 0 else ""}">{img(n, a, lazy=i != 0)}</figure>' for i, (n, a) in enumerate(slides)
    )
    dots = "".join(f'<button type="button" aria-label="Show photo {i + 1}" class="{"active" if i == 0 else ""}"></button>' for i in range(len(slides)))
    places = ["Moab", "Zion", "the Uinta Mountains", "Big Sur", "Iceland", "the Salt Flats", "Lake Como", "Bryce Canyon", "Tulum", "the Tetons", "Sundance"]
    marquee = "".join(f"<span>{p}</span>" for p in places) * 2
    strip_imgs = [
        ("bride-in-meadow", "Bride holding her bouquet in a meadow", "Fall bridals", 1202, 1800),
        ("black-white-wedding-kiss", "Black and white photo of a wedding kiss", "Timeless", 1800, 1050),
        ("beach-wedding-veil", "Bride and groom with a long veil on the beach", "Coastal vows", 1200, 1800),
        ("wedding-ring-hands", "Close-up of hands showing wedding rings", "The details", 1800, 1202),
        ("confetti-wedding-exit", "Newlyweds walking through a confetti toss", "Confetti exit", 1200, 1800),
        ("black-white-first-dance", "Black and white photo of a first dance", "First dance", 1800, 1200),
        ("bride-with-bouquet", "Bride holding a pastel bouquet", "Bridal", 1200, 1800),
        ("reception-couple-celebration", "Couple celebrating at an outdoor reception", "Celebration", 1800, 1202),
    ]
    strip = "".join(
        f'<figure>{img(n, a, sizes="(max-width: 760px) 80vw, 40vw", w=w, h=h)}<figcaption>{c}</figcaption></figure>' for n, a, c, w, h in strip_imgs
    )
    services = [
        ("01", "Elopements", "Just the two of you (or a handful of favorite people) somewhere wild. Hiking, permits, timing and locations — we plan it all with you.", "mountain-elopement-couple", "/blog/how-to-elope-in-utah/"),
        ("02", "Weddings", "Full-day coverage that tells the whole story: the nerves, the vows, the toasts and the dance-floor chaos.", "bride-groom-bouquet", "/pricing/"),
        ("03", "Wedding film", "Cinematic films with real sound — your vows, your toasts, your laughter — edited like a short movie.", "black-white-first-dance", "/video/"),
    ]
    cards = "".join(
        f'<a class="card reveal" data-delay="{i}" href="{u}">{img(im, t + " by Zibetti Photo + Film", sizes="(max-width: 760px) 100vw, 33vw")}<div class="card-body"><span class="num">{n}</span><h3>{t}</h3><p>{d}</p></div></a>'
        for i, (n, t, d, im, u) in enumerate(services)
    )
    body = f"""
<section class="hero grain" aria-label="Introduction">
  <div class="hero-slides">{figs}</div>
  <div class="wrap hero-content">
    <span class="eyebrow fade-up">Zibetti Photo + Film · Provo, Utah</span>
    <h1><span class="split-line"><span>Love stories,</span></span><span class="split-line"><span>told <em>wild</em> &amp;</span></span><span class="split-line"><span>beautifully.</span></span></h1>
    <p class="lead fade-up">Hello! We are the Zibetti team — destination wedding and elopement photographers and filmmakers capturing the big, special moments and all the tiny details you’ll want to remember forever.</p>
    <div class="hero-meta fade-up">
      <div class="hero-actions"><a class="btn btn--light" href="/contact-us/">Check your date <span class="arrow">→</span></a><a class="btn btn--ghost" href="/portfolio/">View portfolio</a></div>
      <div style="display:flex;gap:30px;align-items:end"><div class="slide-dots">{dots}</div><a class="scroll-cue" href="#intro">Scroll<i></i></a></div>
    </div>
  </div>
</section>

<div class="marquee" aria-hidden="true"><div class="marquee-track">{marquee}</div></div>

<section class="section" id="intro">
  <div class="wrap intro-grid">
    <div class="stack reveal">
      {img("photographer-on-cliff", "Photographer capturing a mountain view above the clouds", sizes="(max-width: 760px) 90vw, 45vw")}
      {img("camera-and-lenses", "Camera body and lenses on a dark table", sizes="(max-width: 760px) 50vw, 25vw", w=1439, h=1800)}
      {STAMP}
    </div>
    <div class="reveal" data-delay="1">
      <span class="eyebrow">Hello, we’re Zibetti</span>
      <h2>Photo + film for couples who’d rather be <em>outside</em>.</h2>
      <p class="lead">We’re a small photo-and-film studio based in Provo, Utah. We love traveling, and we love couples who want their wedding to feel like them — not like a template.</p>
      <p>Since we offer both photography and film, you get one calm, coordinated crew on your wedding day instead of two vendors working around each other. We guide you through every pose that doesn’t look like a pose, plan around the best light, and edit every image by hand.</p>
      <p class="signature">— the Zibetti crew</p>
      <a class="link-arrow" href="/about-us/">Learn more about us →</a>
      <div class="stats">
        <div class="stat"><b data-count="500" data-suffix="+">0</b><span>Images per full day</span></div>
        <div class="stat"><b data-count="300" data-suffix="+">0</b><span>Even for small weddings</span></div>
        <div class="stat"><b data-count="10">0</b><span>Weeks, max, to delivery</span></div>
        <div class="stat"><b data-count="2">0</b><span>Crafts: photo + film</span></div>
      </div>
    </div>
  </div>
</section>

<section class="section section--sand">
  <div class="wrap">
    <div class="section-head">
      <div><span class="eyebrow">What we do</span><h2>Three ways to remember it all.</h2></div>
      <p class="muted">From a sunrise elopement on a red-rock rim to a 200-guest celebration under the Wasatch, every collection is built around your day — not the other way around.</p>
    </div>
    <div class="cards">{cards}</div>
  </div>
</section>

<section class="section" aria-label="Recent work">
  <div class="wrap section-head">
    <div><span class="eyebrow">Recent frames</span><h2>A little film strip of feelings.</h2></div>
    <p class="muted">Drag, swipe or scroll sideways. <a class="link-arrow" href="/portfolio/">See the full portfolio →</a></p>
  </div>
  <div class="strip" tabindex="0" aria-label="Scrollable gallery">{strip}</div>
</section>

<section class="quote-band grain">
  {img("alpine-lake-boat", "Turquoise alpine lake surrounded by mountains", extra='data-parallax="0.22"')}
  <blockquote class="reveal">“Don’t even worry. We’ll guide you through the whole thing — by the end you’ll realize there was never anything to worry about.”<cite>Our promise to every camera-shy couple</cite></blockquote>
</section>

<section class="section section--dark">
  <div class="wrap">
    <div class="section-head">
      <div><span class="eyebrow" style="color:var(--accent-2)">How it works</span><h2>From “just engaged” to heirloom album.</h2></div>
      <p>Four simple steps, and you’re never left wondering what happens next.</p>
    </div>
    <div class="steps">
      <div class="step"><h3>Say hello</h3><p class="muted">Tell us your date, location and vibe. We’ll send our full guide and set up a video call.</p></div>
      <div class="step"><h3>Book your date</h3><p class="muted">A signed contract and 50% retainer locks you in. The rest is due a month before.</p></div>
      <div class="step"><h3>Plan together</h3><p class="muted">Timelines, locations, permits and golden-hour timing — we handle the logistics with you.</p></div>
      <div class="step"><h3>Relive it</h3><p class="muted">Sneak peeks within days, your full gallery and film in 8–10 weeks, prints any time.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <div><span class="eyebrow">Free planning tools</span><h2>Plan smarter, stress less.</h2></div>
      <p class="muted">The same calculators we use when we plan a shoot — free for every couple, booked with us or not.</p>
    </div>
    {tool_tiles()}
  </div>
</section>

<section class="section section--sand">
  <div class="wrap">
    <div class="section-head">
      <div><span class="eyebrow">The journal</span><h2>Guides, stories &amp; real advice.</h2></div>
      <a class="link-arrow" href="/blog/">Read the journal →</a>
    </div>
    {post_cards(POSTS[:3])}
  </div>
</section>

{cta()}
"""
    schema = [{"@type": "WebPage", "@id": ORIGIN + "/#webpage", "url": ORIGIN + "/", "name": "Zibetti Photo + Film", "isPartOf": {"@id": ORIGIN + "/#website"}, "about": {"@id": ORIGIN + "/#business"}}]
    add("/", page("/", "Zibetti Photo + Film | Utah Destination Wedding & Elopement Photographers",
                  "Zibetti Photo + Film are destination wedding and elopement photographers and videographers based in Provo, Utah. Photo + film for adventurous couples, anywhere.",
                  body, schema=schema))


def build_about():
    body = page_hero([("Home", "/"), ("About us", "/about-us/")], "About us", "The people behind <em>the cameras</em>.",
                     "A small photo + film studio from Provo, Utah, chasing light and love stories.",
                     "photographer-on-cliff", "Photographer standing on a cliff above the clouds") + f"""
<section class="section">
  <div class="wrap intro-grid">
    <div class="reveal">
      <span class="eyebrow">Our story</span>
      <h2>One team. Two crafts. Zero stiff poses.</h2>
      <p class="lead">Zibetti Photo + Film is a small photography and filmmaking studio based in Provo, Utah, built for couples who want their wedding to feel like them — not like a template.</p>
      <p>We started with a simple idea: couples shouldn’t have to juggle two strangers with cameras on the most important day of their lives. So we built a studio where photo and film are planned together, shot together and delivered together. One timeline, one crew, every angle covered.</p>
      <p>Home base is the Wasatch Front, which means red-rock deserts, alpine lakes and salt flats are all a day trip away. But we pack light and travel often — across the United States and abroad — anywhere love takes you.</p>
    </div>
    <div class="stack reveal" data-delay="1">
      {img("vintage-camera-map", "Vintage camera resting on a travel map", sizes="(max-width: 760px) 90vw, 45vw", w=1800, h=1350)}
      {img("travel-planning-map", "Travel planning flat lay with a camera and backpack", sizes="(max-width: 760px) 50vw, 25vw", w=1800, h=1422)}
      {STAMP}
    </div>
  </div>
</section>

<section class="section section--sand">
  <div class="wrap">
    <div class="section-head"><div><span class="eyebrow">What we believe</span><h2>The way we work.</h2></div></div>
    <div class="price-grid">
      <div class="price reveal"><span class="tag">01</span><h3>Direction, not posing</h3><p>Almost every couple tells us they’re awkward on camera. We give lots of gentle direction and prompts, so your photos feel candid and natural — never stiff.</p></div>
      <div class="price reveal" data-delay="1"><span class="tag">02</span><h3>Light is everything</h3><p>We plan your timeline around the sun. Golden hour, blue hour, canyon shadows — we check it all before your day so the light works for you.</p></div>
      <div class="price reveal" data-delay="2"><span class="tag">03</span><h3>Every image, by hand</h3><p>No bulk presets. We edit and deliver all the good, non-duplicate images, so you usually end up with more than the guaranteed count.</p></div>
    </div>
  </div>
</section>

<section class="quote-band grain">
  {img("campfire-gathering", "Friends gathered around a campfire at dusk", extra='data-parallax="0.2"')}
  <blockquote class="reveal">We’re here to help capture your big, special moments and all the tiny details for you to remember forever.<cite>Why we do this</cite></blockquote>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><div><span class="eyebrow">Where we work</span><h2>Utah first. Anywhere next.</h2></div>
    <p class="muted">Collections are priced by where you are, with travel already built in.</p></div>
    <div class="tool-grid">
      <a class="tool-tile reveal" href="/blog/best-places-to-elope-in-utah/"><h3>Utah</h3><p>Arches, Zion, Bryce, the Uintas, Sundance and the Salt Flats — our backyard, and we know its light and permits well.</p><span class="link-arrow" style="align-self:flex-start">Best places to elope in Utah →</span></a>
      <a class="tool-tile reveal" data-delay="1" href="/pricing/"><h3>Across the U.S.</h3><p>California coastlines, Teton meadows, Arizona deserts. Stateside destination collections include travel and lodging.</p><span class="link-arrow" style="align-self:flex-start">Destination pricing →</span></a>
      <a class="tool-tile reveal" data-delay="2" href="/blog/how-to-travel-with-a-wedding-dress/"><h3>Abroad</h3><p>Iceland, Italy, Mexico and beyond. We’ll help with logistics — down to how to fly with your dress.</p><span class="link-arrow" style="align-self:flex-start">Travel with your dress →</span></a>
    </div>
  </div>
</section>
{cta("Let’s do this thing, together.")}
"""
    schema = [crumbs_schema([("Home", "/"), ("About us", "/about-us/")]), {"@type": "AboutPage", "url": ORIGIN + "/about-us/", "name": "About Zibetti Photo + Film"}]
    add("/about-us/", page("/about-us/", "About Us | Zibetti Photo + Film, Provo Utah Wedding Photographers",
                           "Meet Zibetti Photo + Film — a Provo, Utah photo and film studio for destination weddings and elopements. Our story, our approach and where we work.",
                           body, schema=schema, og_image="photographer-on-cliff"))


def build_pricing():
    tiers = [
        ("Sessions", "Engagements, anniversaries &amp; couples", 750, ["Up to 2 hours of coverage", "1–2 nearby locations", "Outfit change welcome", "60+ edited images", "Online gallery with print store"], False),
        ("Elopements", "Utah elopements", 2400, ["Up to 4 hours of coverage", "Location scouting + permit guidance", "Golden-hour timeline planning", "250+ edited images", "Sneak peeks within a week"], False),
        ("Most booked", "Utah weddings", 3600, ["8 hours of coverage", "Planning call + custom timeline", "500+ edited images", "Engagement session discount", "Online gallery + print store"], True),
        ("Travel", "Stateside destination", 5200, ["8 hours of coverage", "Travel &amp; lodging included in the U.S.", "Location scouting the day before", "500+ edited images", "Optional welcome-party coverage"], False),
        ("Abroad", "International destination", 6500, ["10 hours of coverage", "International travel included", "Multi-day adventure options", "600+ edited images", "Heirloom album credit"], False),
        ("Film", "Video packages", 3200, ["Cinematic highlight film (4–6 min)", "Full ceremony &amp; toasts edit", "Clean, professional audio", "Drone footage where permitted", "Add to any photo package for $2,000"], False),
    ]
    cards = "".join(
        f"""<div class="price reveal{' featured' if feat else ''}" data-delay="{i % 3}"><span class="tag">{tag}</span><h3>{name}</h3>
<div class="from"><small>from</small>${p:,}</div><ul>{''.join(f'<li>{x}</li>' for x in feats)}</ul>
<a class="btn" href="/contact-us/">Inquire <span class="arrow">→</span></a></div>"""
        for i, (tag, name, p, feats, feat) in enumerate(tiers)
    )
    types = [("session", "Session"), ("elope", "Utah elopement"), ("utah", "Utah wedding"), ("stateside", "Stateside travel"), ("intl", "International")]
    type_chips = "".join(f'<label class="chip"><input type="radio" name="est-type" value="{v}"{" checked" if v == "utah" else ""}><span>{n}</span></label>' for v, n in types)
    svc = [("photo", "Photo"), ("both", "Photo + film"), ("film", "Film only")]
    svc_chips = "".join(f'<label class="chip"><input type="radio" name="est-service" value="{v}"{" checked" if v == "photo" else ""}><span>{n}</span></label>' for v, n in svc)
    body = page_hero([("Home", "/"), ("Pricing", "/pricing/")], "Investment", "Pricing &amp; <em>collections</em>.",
                     "Clear starting prices for sessions, elopements, weddings and film — plus an estimator to build your own collection.",
                     "gold-wedding-rings", "Two gold wedding rings resting on white fabric") + f"""
<section class="section">
  <div class="wrap">
    <div class="section-head"><div><span class="eyebrow">Collections</span><h2>Where every story starts.</h2></div>
    <p class="muted">Every collection includes a planning call, a hand-edited online gallery with print ordering, and sneak peeks. Our full price guide is packed with detail — <a class="link-arrow" href="/contact-us/">ask for it here</a>.</p></div>
    <div class="price-grid">{cards}</div>
  </div>
</section>

<section class="section section--sand" id="estimator-section">
  <div class="wrap">
    <div class="section-head"><div><span class="eyebrow">Interactive</span><h2>Build your collection.</h2></div>
    <p class="muted">Pick your day, add what you want and see a ballpark instantly. Final quotes depend on date, travel and season.</p></div>
    <div class="tool" id="estimator">
      <div class="tool-cols tool-cols--est">
        <div>
          <div class="field"><span class="label">What are we capturing?</span><div class="chips">{type_chips}</div></div>
          <div class="field"><span class="label">Photo, film or both?</span><div class="chips">{svc_chips}</div></div>
          <div class="field"><label for="est-hours">Extra coverage</label><input type="range" id="est-hours" min="0" max="6" step="1" value="0"><small id="est-hours-val">None</small></div>
          <div class="field"><span class="label">Add-ons</span>
            <label class="check"><input type="checkbox" id="est-second"> Second photographer (+$600)</label>
            <label class="check"><input type="checkbox" id="est-engage"> Engagement session (+$500)</label>
            <label class="check"><input type="checkbox" id="est-album"> Heirloom linen album (+$650)</label>
            <label class="check"><input type="checkbox" id="est-raw"> Unedited files on a hard drive (+$150)</label>
          </div>
        </div>
        <aside class="estimate" aria-live="polite">
          <span class="eyebrow" style="color:var(--accent-2)">Your estimate</span>
          <div class="total" id="est-total">$0</div>
          <ul id="est-lines"></ul>
          <p style="font-size:.9rem">Retainer to book: <b id="est-deposit">$0</b> <small>50% holds your date; the balance is due one month before.</small></p>
          <a class="btn btn--light" href="/contact-us/">Check availability <span class="arrow">→</span></a>
        </aside>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="narrow prose">
    <span class="eyebrow">Good to know</span>
    <h2>What’s always included</h2>
    <ul>
      <li><strong>Guaranteed image counts.</strong> Smaller weddings (4–6 hours) receive at least 300 edited images; full days (7+ hours) at least 500.</li>
      <li><strong>Turnaround.</strong> Sessions are delivered within a week or two. Weddings take 8–10 weeks, with sneak peeks much sooner.</li>
      <li><strong>Overtime.</strong> Running 15–30 minutes late is no big deal. Beyond an hour, additional time is $200/hour.</li>
      <li><strong>Booking.</strong> A 50% non-refundable retainer holds your date; the remainder is due one month before your wedding.</li>
    </ul>
    <p>Wondering how we compare? Read <a href="/blog/how-much-does-a-destination-wedding-photographer-cost/">how much a destination wedding photographer costs</a> or our guide to <a href="/blog/photo-and-video-should-you-hire-both/">hiring photo and video together</a>.</p>
  </div>
</section>
{cta("Want the full price guide?", "Email us your date and location and we’ll send the complete guide with every collection, add-on and travel detail.")}
"""
    offers = [{"@type": "Offer", "name": n.replace("&amp;", "&"), "price": str(p), "priceCurrency": "USD", "description": "Starting price"} for _, n, p, _, _ in tiers]
    schema = [crumbs_schema([("Home", "/"), ("Pricing", "/pricing/")]),
              {"@type": "Service", "name": "Wedding and elopement photography and film", "provider": {"@id": ORIGIN + "/#business"}, "areaServed": "Worldwide",
               "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Collections", "itemListElement": offers}}]
    add("/pricing/", page("/pricing/", "Pricing | Wedding & Elopement Photography Collections | Zibetti",
                          "Starting prices for Utah elopements, Utah weddings, destination weddings, engagement sessions and wedding films — plus an interactive pricing estimator.",
                          body, schema=schema, og_image="gold-wedding-rings", tools_js=True))


def build_video():
    body = page_hero([("Home", "/"), ("Film", "/video/")], "Wedding film", "Your day, in <em>motion</em>.",
                     "Cinematic wedding and elopement films with real sound — the vows, the toasts, the laughter.",
                     "film-clapperboard", "Hand holding a film clapperboard in the desert") + f"""
<section class="section">
  <div class="wrap">
    <a class="video-feature reveal" href="/contact-us/" aria-label="Request our sample wedding films">
      {img("black-white-first-dance", "Black and white first dance at a wedding reception", sizes="(max-width: 1240px) 100vw, 1240px")}
      <span class="reel-bars"></span><span class="reel-bars b"></span>
      <span class="play">{ICONS['play']}</span>
      <span class="label">Request our full-length sample films</span>
    </a>
  </div>
</section>
<section class="section section--tight">
  <div class="wrap intro-grid">
    <div class="reveal">
      <span class="eyebrow">Why film</span>
      <h2>Photos show how it looked. Film shows how it <em>felt</em>.</h2>
      <p class="lead">The shake in a voice during vows. Your dad’s laugh. The song that played as you walked in. Those are things only film can keep.</p>
      <p>Because we’re a photo + film team, adding film doesn’t mean adding a stranger to your day. We plan one timeline, move as one crew and never step into each other’s shots. Film can be added to any photo collection for $2,000, and it covers the same hours as your photography.</p>
      <a class="btn" href="/pricing/#estimator">Estimate photo + film <span class="arrow">→</span></a>
    </div>
    <div class="stack reveal" data-delay="1">
      {img("reception-couple-celebration", "Couple celebrating at an outdoor reception", sizes="(max-width: 760px) 90vw, 45vw")}
      {img("confetti-wedding-exit", "Newlyweds walking through a confetti toss", sizes="(max-width: 760px) 50vw, 25vw", w=1200, h=1800)}
    </div>
  </div>
</section>
<section class="section section--sand">
  <div class="wrap">
    <div class="section-head"><div><span class="eyebrow">What you get</span><h2>Every film includes.</h2></div></div>
    <div class="price-grid">
      <div class="price reveal"><span class="tag">Highlight film</span><h3>4–6 minutes</h3><p>A story-driven edit set to licensed music, built around your vows, letters and toasts.</p></div>
      <div class="price reveal" data-delay="1"><span class="tag">Documentary edits</span><h3>Ceremony + toasts</h3><p>Your full ceremony and speeches, multi-camera and color-graded, so nothing is lost.</p></div>
      <div class="price reveal" data-delay="2"><span class="tag">Sound</span><h3>Clean audio</h3><p>Discreet lav mics and recorders on the officiant, the couple and the toast mic.</p></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap compare">
    <div class="reveal"><h3>Photo only</h3><p class="muted">Perfect for intimate elopements and couples who want timeless stills and printed albums.</p><a class="link-arrow" href="/pricing/">Photo collections →</a></div>
    <div class="reveal" data-delay="1"><h3>Photo + film</h3><p class="muted">One team, one plan, every angle. The most popular choice for full weddings.</p><a class="link-arrow" href="/blog/photo-and-video-should-you-hire-both/">Should you hire both? →</a></div>
  </div>
</section>
{cta("Let’s make you a movie.")}
"""
    schema = [crumbs_schema([("Home", "/"), ("Film", "/video/")]),
              {"@type": "Service", "name": "Wedding videography", "serviceType": "Wedding film", "provider": {"@id": ORIGIN + "/#business"},
               "offers": {"@type": "Offer", "price": "3200", "priceCurrency": "USD", "description": "Video packages starting at"}}]
    add("/video/", page("/video/", "Wedding Videography | Cinematic Wedding & Elopement Films | Zibetti",
                        "Cinematic wedding and elopement films from Zibetti Photo + Film in Utah. Highlight films, full ceremony edits and clean audio — add film to any photo package.",
                        body, schema=schema, og_image="film-clapperboard"))


FAQS = [
    ("Do you travel for weddings?", "Yes! We love traveling for weddings and have photographed them all over the United States and abroad. We have special collections built just for destination weddings — travel and lodging are already included. <a href=\"/contact-us/\">Contact us</a> with your location for details."),
    ("Do you offer both photo and video?", "Yes. Because we work as a photo + film team, we can cover both on your wedding day. Adding a wedding film to a photo collection is a $2,000 add-on and covers the same hours as your photography. Photo-only and film-only collections are available too, but hiring one coordinated team for both is just so convenient. Read more in <a href=\"/blog/photo-and-video-should-you-hire-both/\">Photo and video: should you hire both?</a>"),
    ("How many images will we receive? Do you deliver RAW files?", "It depends on the length of your day. For smaller weddings (4–6 hours) we guarantee 300 edited images; for longer weddings (7+ hours) at least 500. That isn’t a cap — we deliver every good, non-duplicate image, so most couples get more. Unedited files are available on a hard drive for a small fee; we ask that you don’t edit or post them, since they don’t represent our finished style."),
    ("What if our wedding runs late?", "No problem. Running 15–30 minutes over usually isn’t a big deal. If your day goes over by more than an hour, additional time is billed at $200/hour."),
    ("How long until we get our photos?", "Engagement and bridal sessions are usually delivered within a week — sooner if you need them for announcements. Wedding galleries take 8–10 weeks depending on the season. We send sneak peeks as soon as possible, but we never rush the edit."),
    ("Do we need a second shooter?", "It depends. Smaller weddings rarely need one. For larger weddings, or if you book photo + film and want an extra photographer, a second shooter is a $600 add-on."),
    ("How do we book our date?", "A signed contract and a 50% non-refundable retainer hold your date. The remaining balance is due one month before your wedding."),
    ("What happens if you get sick?", "Only an extreme illness, a death in the family or a true emergency would keep us from your wedding — and we’ve worked through plenty of colds. In the rare case something happens, we have a list of trusted photographers and filmmakers we can call on."),
    ("Can we combine our wedding with a second location or day?", "Yes. Many couples add a day-after adventure session, a welcome party or a second location. We’ll build it into your collection and timeline."),
    ("How will our photos be delivered?", "Through a beautiful online gallery you can share with family. You can download everything in high resolution and order prints and albums directly from the gallery."),
    ("Can we see your full price list?", "Our price guide is packed with information, so it’s easiest to <a href=\"mailto:info@zibetti.co\">email us</a> and we’ll send the complete version. You can also get a ballpark instantly with our <a href=\"/pricing/#estimator\">pricing estimator</a>."),
    ("We’re awkward in front of the camera. Help?", "This is the thing we’re proudest of. Almost every couple says they’re nervous on camera, and our answer is always: don’t worry. We give lots of direction (not stiff posing) so your photos feel candid and natural, and we take time to get to know you. By the end of the shoot you’ll realize there was never anything to worry about."),
    ("Do you use shot lists?", "Honestly, we don’t love them — we’d rather you trust us to document your day the way we know how, and we won’t miss a big moment. Just give us a heads-up about anything non-traditional, plus a list of the family group photos you want after the ceremony."),
    ("Do you help with permits and locations for elopements?", "Absolutely. We help you choose a location, understand the permit you’ll need and plan around the light. Try our <a href=\"/tools/utah-elopement-location-finder/\">Utah elopement location finder</a> and read <a href=\"/blog/how-to-elope-in-utah/\">how to elope in Utah</a>."),
]


def build_faq():
    items = "".join(f'<details class="reveal"><summary>{q}</summary><div class="answer"><p>{a}</p></div></details>' for q, a in FAQS)
    body = page_hero([("Home", "/"), ("FAQ", "/faq/")], "Frequently asked questions", "Good <em>questions</em>.",
                     "Everything couples usually ask us — delivery, travel, film, booking and what to do if you’re camera-shy.",
                     "ceremony-chairs-lawn", "Two decorated wedding chairs on a lawn by the water", short=True) + f"""
<section class="section"><div class="narrow"><div class="faq-list">{items}</div>
<p style="margin-top:40px" class="muted">Still curious? <a class="link-arrow" href="/contact-us/">Ask us anything →</a></p></div></section>
{cta()}
"""
    import re
    faq_schema = {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in FAQS]}
    add("/faq/", page("/faq/", "FAQ | Wedding Photography & Film Questions | Zibetti Photo + Film",
                      "Answers about image counts, delivery times, travel, photo + video, second shooters, booking and permits from Zibetti Photo + Film.",
                      body, schema=[crumbs_schema([("Home", "/"), ("FAQ", "/faq/")]), faq_schema], og_image="ceremony-chairs-lawn"))


def build_contact():
    body = page_hero([("Home", "/"), ("Contact us", "/contact-us/")], "Contact", "Let’s do this thing, <em>together</em>.",
                     "Tell us about your plans. We reply to every inquiry within two business days.",
                     "couple-holding-hands", "Bride and groom holding hands", short=True) + f"""
<section class="section">
  <div class="wrap contact-grid">
    <div class="reveal">
      <span class="eyebrow">Say hello</span>
      <h2>We’d love to hear your story.</h2>
      <p class="lead">Whether it’s a sunrise elopement in Arches or a full wedding weekend in Italy, we’re here to help capture your big, special moments and all the tiny details.</p>
      <ul class="info-list">
        <li><b>Email</b><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><b>Based in</b>Provo, Utah — available worldwide</li>
        <li><b>Response time</b>Within two business days</li>
        <li><b>Planning early?</b>Try our <a href="/tools/wedding-day-timeline-builder/">timeline builder</a> and <a href="/tools/golden-hour-calculator/">golden hour calculator</a>.</li>
      </ul>
    </div>
    <div class="form-card reveal" data-delay="1">
      <p class="notice" data-form-status hidden role="status"></p>
      <form action="/contact.php" method="post">
        <div class="row2">
          <div class="field"><label for="f-name">Your names</label><input id="f-name" name="name" autocomplete="name" required></div>
          <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
        </div>
        <div class="row2">
          <div class="field"><label for="f-date">Date (or season)</label><input id="f-date" name="date" placeholder="e.g. Oct 2027"></div>
          <div class="field"><label for="f-loc">Location</label><input id="f-loc" name="location" placeholder="e.g. Moab, UT"></div>
        </div>
        <div class="field"><label for="f-type">What are you planning?</label>
          <select id="f-type" name="type"><option>Elopement</option><option>Wedding</option><option>Engagement / couples session</option><option>Something else</option></select></div>
        <div class="field"><span class="label">Interested in</span><div class="chips">
          <label class="chip"><input type="checkbox" name="services[]" value="Photo" checked><span>Photo</span></label>
          <label class="chip"><input type="checkbox" name="services[]" value="Film"><span>Film</span></label>
          <label class="chip"><input type="checkbox" name="services[]" value="Album"><span>Album</span></label></div></div>
        <div class="field"><label for="f-msg">Tell us everything</label><textarea id="f-msg" name="message" required placeholder="Your story, your vibe, your guest count, the songs you can't stop playing..."></textarea></div>
        <div class="hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
        <button class="btn" type="submit">Send inquiry <span class="arrow">→</span></button>
      </form>
    </div>
  </div>
</section>
"""
    add("/contact-us/", page("/contact-us/", "Contact Us | Book Zibetti Photo + Film",
                             "Contact Zibetti Photo + Film for wedding, elopement and engagement photography and film. Email info@zibetti.co or send an inquiry.",
                             body, schema=[crumbs_schema([("Home", "/"), ("Contact us", "/contact-us/")]), {"@type": "ContactPage", "url": ORIGIN + "/contact-us/"}],
                             og_image="couple-holding-hands"))


def build_portfolio():
    items = [
        ("mountain-elopement-couple", "Couple walking through a mountain meadow", "Mountain elopement", "elopement", 1800, 1200),
        ("bride-in-meadow", "Bride holding her bouquet in a meadow", "Fall bridals", "wedding", 1202, 1800),
        ("black-sand-beach-elopement", "Couple embracing on a black sand beach", "Iceland-style coastline", "elopement destination", 1800, 1200),
        ("gold-wedding-rings", "Gold wedding rings", "Ring details", "details", 1800, 1200),
        ("fall-lake-wedding-portrait", "Couple by an autumn lake", "Autumn lake portraits", "wedding", 1800, 1200),
        ("beach-wedding-veil", "Bride and groom with a flowing veil on the beach", "Coastal vows", "destination wedding", 1200, 1800),
        ("bridal-bouquet-moody", "Bride holding a dark, moody bouquet", "Moody florals", "details", 1800, 1200),
        ("confetti-wedding-exit", "Couple walking through confetti", "Confetti exit", "wedding", 1200, 1800),
        ("black-white-wedding-kiss", "Black and white wedding kiss", "Timeless", "wedding", 1800, 1050),
        ("bride-with-bouquet", "Bride holding a pastel bouquet", "Bridal portrait", "wedding", 1200, 1800),
        ("wedding-ring-hands", "Couple's hands with rings and bouquet", "Just married", "details", 1800, 1202),
        ("reception-couple-celebration", "Couple celebrating at an outdoor reception", "Reception", "wedding", 1800, 1202),
        ("ceremony-chairs-lawn", "Decorated ceremony chairs on a lawn", "Ceremony details", "details", 1800, 1200),
        ("black-white-first-dance", "Black and white first dance", "First dance", "wedding", 1800, 1200),
        ("couple-holding-hands", "Couple holding hands", "Hand in hand", "elopement", 1800, 1200),
        ("rings-on-flowers", "Wedding rings resting on flowers", "Rings + roses", "details", 1800, 1200),
        ("newlywed-hands-bouquet", "Newlyweds holding hands over a bouquet", "Newlyweds", "wedding", 1800, 1200),
        ("bride-groom-bouquet", "Bride and groom holding a bouquet", "Garden wedding", "wedding", 1800, 1202),
        ("reception-table-setting", "Reception table with florals", "Tablescape", "details", 1800, 1200),
        ("red-rock-desert-road", "Road through red rock desert", "On the road to Moab", "destination elopement", 1200, 1800),
    ]
    figs = "".join(
        f'<figure data-cat="{c}">{img(n, a, sizes="(max-width: 760px) 100vw, 33vw", w=w, h=h, extra=f"data-full=\"/assets/img/{n}.webp\"")}<figcaption>{cap}</figcaption></figure>'
        for n, a, cap, c, w, h in items
    )
    filt = "".join(f'<button type="button" data-filter="{v}" aria-pressed="{"true" if v == "all" else "false"}">{n}</button>' for v, n in [("all", "All"), ("elopement", "Elopements"), ("wedding", "Weddings"), ("destination", "Destination"), ("details", "Details")])
    body = page_hero([("Home", "/"), ("Portfolio", "/portfolio/")], "Portfolio", "Moments worth <em>keeping</em>.",
                     "Elopements, weddings and the tiny details — tap any image to view it full screen.",
                     "black-sand-beach-elopement", "Couple embracing on a black sand beach", short=True) + f"""
<section class="section"><div class="wrap">
  <div class="filters" role="group" aria-label="Filter portfolio">{filt}</div>
  <div class="masonry">{figs}</div>
</div></section>
<div class="lightbox" role="dialog" aria-modal="true" aria-label="Image viewer">
  <button class="lb-close" type="button" aria-label="Close">×</button>
  <button class="lb-prev" type="button" aria-label="Previous image">‹</button>
  <div><img src="data:image/gif;base64,R0lGODlhAQABAAAAACw=" alt=""><p></p></div>
  <button class="lb-next" type="button" aria-label="Next image">›</button>
</div>
{cta()}
"""
    add("/portfolio/", page("/portfolio/", "Portfolio | Wedding & Elopement Photography | Zibetti Photo + Film",
                            "Browse wedding, elopement and destination photography by Zibetti Photo + Film — mountains, deserts, coastlines and the details in between.",
                            body, schema=[crumbs_schema([("Home", "/"), ("Portfolio", "/portfolio/")]), {"@type": "CollectionPage", "url": ORIGIN + "/portfolio/", "name": "Portfolio"}],
                            og_image="black-sand-beach-elopement"))


def build_tools():
    body = page_hero([("Home", "/"), ("Tools", "/tools/")], "Free planning tools", "Plan around the <em>light</em>.",
                     "Free calculators for couples planning a wedding, elopement or engagement session.",
                     "mountains-above-clouds", "Mountains rising above a sea of clouds at sunset", short=True) + f"""
<section class="section"><div class="wrap">{tool_tiles()}
<div class="tool-grid" style="margin-top:22px"><a class="tool-tile reveal" href="/pricing/#estimator"><span class="ico">{ICONS['calc']}</span><h3>Pricing Estimator</h3><p>Build a photo, film or photo + film collection and see a ballpark instantly.</p><span class="link-arrow" style="align-self:flex-start">Open the estimator →</span></a></div>
</div></section>
{cta()}"""
    add("/tools/", page("/tools/", "Free Wedding Planning Tools | Golden Hour, Timeline & Location Finder",
                        "Free wedding and elopement planning tools: golden hour calculator, wedding day timeline builder, Utah elopement location finder and pricing estimator.",
                        body, schema=[crumbs_schema([("Home", "/"), ("Tools", "/tools/")])], og_image="mountains-above-clouds"))

    # Golden hour calculator
    trail = [("Home", "/"), ("Tools", "/tools/"), ("Golden hour calculator", "/tools/golden-hour-calculator/")]
    body = page_hero(trail, "Free tool", "Golden hour <em>calculator</em>.",
                     "See golden hour, blue hour, sunrise and sunset for any date — preloaded with Utah’s favorite elopement spots and dream destinations.",
                     "sunset-sky", "Fiery red sunset over the horizon", short=True) + f"""
<section class="section"><div class="wrap">
  <div class="tool" id="golden-hour-tool">
    <div class="tool-cols">
      <div>
        <div class="field"><label for="gh-place">Location</label><select id="gh-place"></select></div>
        <div id="gh-custom" hidden>
          <div class="row2"><div class="field"><label for="gh-lat">Latitude</label><input id="gh-lat" inputmode="decimal" placeholder="40.2338"></div>
          <div class="field"><label for="gh-lng">Longitude</label><input id="gh-lng" inputmode="decimal" placeholder="-111.6585"></div></div>
        </div>
        <button class="btn btn--ghost" type="button" id="gh-geo" style="margin-bottom:18px">Use my location</button>
        <div class="field"><label for="gh-date">Date</label><input type="date" id="gh-date"></div>
        <p class="muted" style="font-size:.88rem">Golden hour = sun between 6° above and 4° below the horizon. Blue hour = 4° to 6° below.</p>
      </div>
      <div aria-live="polite">
        <svg class="sun-arc" id="gh-arc" viewBox="0 0 600 200" role="img" aria-label="Chart of the sun's height through the day"></svg>
        <div id="gh-out"></div>
      </div>
    </div>
  </div>
</div></section>
<section class="section section--sand"><div class="narrow prose">
  <h2>Why golden hour matters for wedding photos</h2>
  <p>Golden hour is the stretch of time just after sunrise and just before sunset when the sun sits low in the sky. Its light travels through more atmosphere, so it turns warm, soft and directional — it wraps around faces instead of carving harsh shadows under eyes. Blue hour follows sunset: the sky goes cool and even, perfect for moody portraits and sparkler exits.</p>
  <p>In Utah, the landscape changes the math. Deep canyons like Zion lose direct light long before official sunset, while open overlooks like Dead Horse Point keep it until the last minute. Mountain ridges to the west of the Wasatch Front can steal 20–30 minutes from the evening. That’s why we always pair this calculator with a scouting visit or satellite map.</p>
  <p>Ready to turn the numbers into a plan? Try the <a href="/tools/wedding-day-timeline-builder/">wedding day timeline builder</a>, or read <a href="/blog/golden-hour-wedding-photos/">how to plan your wedding around golden hour</a>.</p>
</div></section>
{cta()}"""
    add("/tools/golden-hour-calculator/", page("/tools/golden-hour-calculator/", "Golden Hour Calculator for Wedding & Elopement Photos | Zibetti",
                                                "Free golden hour calculator: find golden hour, blue hour, sunrise and sunset times for any date in Utah or anywhere in the world, built for wedding planning.",
                                                body, schema=[crumbs_schema(trail), {"@type": "WebApplication", "name": "Golden Hour Calculator", "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "url": ORIGIN + "/tools/golden-hour-calculator/"}],
                                                og_image="sunset-sky", tools_js=True))

    # Timeline builder
    trail = [("Home", "/"), ("Tools", "/tools/"), ("Wedding day timeline builder", "/tools/wedding-day-timeline-builder/")]
    body = page_hero(trail, "Free tool", "Wedding day <em>timeline</em> builder.",
                     "Answer a few questions and get a photographer-approved schedule built around your actual sunset.",
                     "reception-table-setting", "Reception table set with flowers and candles", short=True) + """
<section class="section"><div class="wrap">
  <div class="tool" id="timeline-tool">
    <div class="tool-cols">
      <div>
        <div class="field"><span class="label">Type of day</span><div class="chips">
          <label class="chip"><input type="radio" name="tl-type" value="wedding" checked><span>Wedding</span></label>
          <label class="chip"><input type="radio" name="tl-type" value="elopement"><span>Elopement</span></label></div></div>
        <div class="field"><label for="tl-place">Location</label><select id="tl-place"></select></div>
        <div class="field"><label for="tl-date">Date</label><input type="date" id="tl-date"><small>Sunset that day: <b id="tl-sunset">—</b></small></div>
        <label class="check"><input type="checkbox" id="tl-auto" checked> Pick the best ceremony time for me</label>
        <div class="field"><label for="tl-ceremony">Ceremony time</label><input type="time" id="tl-ceremony" value="16:00" step="900"></div>
        <div class="field"><label for="tl-hours">Photo coverage</label><input type="range" id="tl-hours" min="3" max="12" step="1" value="8"><small id="tl-hours-val">8 hours</small></div>
        <label class="check"><input type="checkbox" id="tl-firstlook" checked> We’re doing a first look</label>
        <label class="check"><input type="checkbox" id="tl-ready" checked> Include getting-ready coverage</label>
        <div class="field" style="margin-top:12px"><label for="tl-family">Family photos</label>
          <select id="tl-family"><option value="20">Small family (about 20 min)</option><option value="30" selected>Medium family (about 30 min)</option><option value="45">Big family (about 45 min)</option></select></div>
      </div>
      <div>
        <div id="tl-out" aria-live="polite"></div>
        <div class="tool-actions no-print"><button class="btn" type="button" id="tl-print">Print / save PDF</button><button class="btn btn--ghost" type="button" id="tl-copy">Copy timeline</button></div>
      </div>
    </div>
  </div>
</div></section>
<section class="section section--sand"><div class="narrow prose">
  <h2>How this timeline is built</h2>
  <p>We work backwards from the two things that can’t move: your ceremony and the sunset. Couple portraits land in golden hour whenever possible, family formals happen right after the ceremony while everyone is still together, and we build in a buffer before guests arrive so you’re never rushed.</p>
  <ul>
    <li><strong>First look or not?</strong> A first look moves most portraits before the ceremony, so you get to enjoy cocktail hour.</li>
    <li><strong>Family formals.</strong> Plan roughly two minutes per grouping and hand us a written list.</li>
    <li><strong>Sunset portraits.</strong> Even 15 minutes away from the reception gives you the best photos of the day.</li>
  </ul>
  <p>Want the full playbook? Read our <a href="/blog/wedding-day-timeline-for-photos/">wedding day timeline guide</a>.</p>
</div></section>
""" + cta()
    add("/tools/wedding-day-timeline-builder/", page("/tools/wedding-day-timeline-builder/", "Wedding Day Timeline Builder (Free) | Plan Around Sunset | Zibetti",
                                                      "Free wedding day timeline builder: enter your date, location and ceremony time to get a photo-friendly wedding or elopement schedule built around sunset.",
                                                      body, schema=[crumbs_schema(trail), {"@type": "WebApplication", "name": "Wedding Day Timeline Builder", "applicationCategory": "LifestyleApplication", "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "url": ORIGIN + "/tools/wedding-day-timeline-builder/"}],
                                                      og_image="reception-table-setting", tools_js=True))

    # Location finder
    trail = [("Home", "/"), ("Tools", "/tools/"), ("Utah elopement location finder", "/tools/utah-elopement-location-finder/")]
    lands = [("redrock", "Red rock"), ("canyon", "Canyons"), ("desert", "Desert"), ("alpine", "Alpine"), ("lake", "Lakes"), ("forest", "Forest"), ("river", "Rivers &amp; falls"), ("saltflats", "Salt flats"), ("snow", "Snow")]
    land_chips = "".join(f'<label class="chip"><input type="checkbox" name="lf-land" value="{v}"><span>{n}</span></label>' for v, n in lands)
    body = page_hero(trail, "Free tool", "Utah elopement <em>location</em> finder.",
                     "Filter 20 of Utah’s most beautiful places to say “I do” by season, scenery, hiking and drive time from Provo.",
                     "red-rock-desert-road", "Highway leading into red rock desert", short=True) + f"""
<section class="section"><div class="wrap">
  <div class="tool" id="location-tool">
    <div class="tool-cols">
      <div>
        <div class="field"><label for="lf-season">Season</label><select id="lf-season"><option value="any">Any season</option><option value="spring">Spring (Mar–May)</option><option value="summer">Summer (Jun–Aug)</option><option value="fall" selected>Fall (Sep–Nov)</option><option value="winter">Winter (Dec–Feb)</option></select></div>
        <div class="field"><span class="label">Scenery you love</span><div class="chips">{land_chips}</div></div>
        <div class="field"><label for="lf-hike">How much hiking?</label><select id="lf-hike"><option value="0">Walk-up only</option><option value="1" selected>A short hike is fine</option><option value="2">We love a real hike</option></select></div>
        <div class="field"><label for="lf-drive">Drive time from Provo</label><input type="range" id="lf-drive" min="0.5" max="6" step="0.5" value="6"><small id="lf-drive-val">Any distance</small></div>
        <div class="field"><label for="lf-guests">Guests (including you two)</label><input type="number" id="lf-guests" min="2" max="200" value="2"></div>
      </div>
      <div>
        <p class="muted" style="margin-bottom:12px"><b id="lf-count"></b> · sorted by best fit</p>
        <div class="loc-results" id="lf-out" aria-live="polite"></div>
      </div>
    </div>
  </div>
  <p class="muted" style="font-size:.88rem;margin-top:18px">Permit rules, group limits and road access change. Always confirm with the managing agency before you book — we help every couple we work with do exactly that.</p>
</div></section>
<section class="section section--sand"><div class="narrow prose">
  <h2>Choosing your Utah elopement location</h2>
  <p>Utah packs five national parks, dozens of state parks, alpine lakes, salt flats and slot canyons into one state. The right spot depends on three things: the season, how far you want to walk in your wedding clothes, and how many people you’re bringing. National parks cap group sizes and require a special use permit, state parks have their own process, and national forest and BLM land can be more flexible.</p>
  <p>For a deeper dive, read <a href="/blog/best-places-to-elope-in-utah/">the best places to elope in Utah</a> and our step-by-step guide on <a href="/blog/how-to-elope-in-utah/">how to elope in Utah</a>.</p>
</div></section>
{cta()}"""
    add("/tools/utah-elopement-location-finder/", page("/tools/utah-elopement-location-finder/", "Utah Elopement Location Finder | 20 Spots by Season & Scenery",
                                                        "Find the perfect Utah elopement location. Filter 20 spots — Arches, Zion, Bryce, the Uintas, the Salt Flats and more — by season, scenery, hiking and drive time.",
                                                        body, schema=[crumbs_schema(trail), {"@type": "WebApplication", "name": "Utah Elopement Location Finder", "applicationCategory": "TravelApplication", "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "url": ORIGIN + "/tools/utah-elopement-location-finder/"}],
                                                        og_image="red-rock-desert-road", tools_js=True))


def build_blog():
    body = page_hero([("Home", "/"), ("Journal", "/blog/")], "The journal", "Stories, guides &amp; <em>good advice</em>.",
                     "Planning guides for elopements and destination weddings, written by the people behind the camera.",
                     "mountain-valley-pines", "Mountain valley framed by pine trees", short=True) + f"""
<section class="section"><div class="wrap">{post_cards(POSTS, feature=True)}</div></section>
{cta()}"""
    schema = [crumbs_schema([("Home", "/"), ("Journal", "/blog/")]),
              {"@type": "Blog", "url": ORIGIN + "/blog/", "name": "The Zibetti Journal",
               "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": f"{ORIGIN}/blog/{p['slug']}/", "datePublished": p["date"]} for p in POSTS]}]
    add("/blog/", page("/blog/", "Journal | Elopement & Destination Wedding Planning Guides | Zibetti",
                       "Elopement and destination wedding planning guides from Zibetti Photo + Film: Utah locations, timelines, golden hour, travel tips and what to wear.",
                       body, schema=schema, og_image="mountain-valley-pines"))

    for i, p in enumerate(POSTS):
        url = f"/blog/{p['slug']}/"
        trail = [("Home", "/"), ("Journal", "/blog/"), (p["short"], url)]
        toc = "".join(f'<li><a href="#{hid}">{esc(t)}</a></li>' for hid, t in p["toc"])
        related = [q for q in POSTS if q["slug"] != p["slug"]]
        related = sorted(related, key=lambda q: (q["category"] != p["category"]))[:3]
        hero = f"""<section class="page-hero grain">
  {img(p['image'], p['image_alt'], lazy=False, extra='data-parallax="0.18"')}
  <div class="wrap">
    {crumbs_html(trail)}
    <span class="eyebrow">{p['category']}</span>
    <h1>{esc(p['title'])}</h1>
    <div class="article-meta"><span>{date.fromisoformat(p['date']).strftime('%B %-d, %Y')}</span><span>{p['minutes']} min read</span><span>By the Zibetti team</span></div>
  </div>
</section>"""
        body = f"""<div class="progress" aria-hidden="true"></div>
{hero}
<section class="section section--tight"><div class="wrap article-layout">
  <article class="prose" data-article>
    {p['body']}
  </article>
  <aside class="toc">
    <div class="toc-box"><h4>In this guide</h4><ol>{toc}</ol></div>
    <div class="toc-box"><h4>Plan it</h4><ul style="list-style:none;padding:0;margin:0;font-size:.92rem">
      {''.join(f'<li style="margin-bottom:.6em"><a href="{u}">{n} →</a></li>' for u, n, _, _ in TOOLS)}</ul></div>
    <a class="btn" href="/contact-us/" style="width:100%;justify-content:center">Inquire about your date</a>
  </aside>
</div></section>
<section class="section section--sand"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow">Keep reading</span><h2>More from the journal.</h2></div></div>
  {post_cards(related)}
</div></section>
{cta()}"""
        schema = [crumbs_schema(trail), {
            "@type": "BlogPosting", "headline": p["title"], "description": p["description"], "datePublished": p["date"], "dateModified": p.get("updated", p["date"]),
            "image": f"{ORIGIN}/assets/img/{p['image']}.webp", "mainEntityOfPage": ORIGIN + url,
            "author": {"@type": "Organization", "name": BRAND, "url": ORIGIN + "/"}, "publisher": {"@id": ORIGIN + "/#business"}}]
        if p.get("faq"):
            schema.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]})
        add(url, page(url, p["seo_title"], p["description"], body, schema=schema, og_image=p["image"], og_type="article",
                      tools_js=bool(p.get("tools_js")),
                      extra_head=f'<meta property="article:published_time" content="{p["date"]}">\n'))


def build_legal():
    trail = [("Home", "/"), ("Privacy policy", "/privacy-policy/")]
    body = page_hero(trail, "Legal", "Privacy policy", "", "mountain-river-forest", "Mountain river running through a forest", short=True) + f"""
<section class="section"><div class="narrow prose">
<p><em>Last updated {date.today().strftime('%B %-d, %Y')}</em></p>
<p>{BRAND} (“we”, “us”) respects your privacy. This policy explains what we collect through zibetti.co and how we use it.</p>
<h2>What we collect</h2>
<p>When you send an inquiry, we receive the details you choose to share — typically your names, email address, event date, location and message. Our planning tools (golden hour calculator, timeline builder, location finder and pricing estimator) run entirely in your browser; the information you enter into them is not sent to us. If you use “Use my location”, your coordinates stay on your device.</p>
<h2>How we use it</h2>
<p>We use inquiry details only to reply to you, prepare a proposal and, if you book, deliver our services. We never sell your information.</p>
<h2>Cookies and analytics</h2>
<p>This site does not set advertising cookies. Fonts are loaded from Google Fonts, which may log standard request data such as your IP address.</p>
<h2>Your photos</h2>
<p>We may share images from your session or wedding in our portfolio or on social media. If you’d prefer we don’t, just tell us — we’ll respect that.</p>
<h2>Contact</h2>
<p>Questions or deletion requests: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</div></section>"""
    add("/privacy-policy/", page("/privacy-policy/", "Privacy Policy | Zibetti Photo + Film", "How Zibetti Photo + Film collects, uses and protects the information you share through zibetti.co.",
                                 body, schema=[crumbs_schema(trail)], og_image="mountain-river-forest"))

    body = f"""<section class="page-hero grain" style="min-height:100svh">
  {img("mountains-above-clouds", "Mountains above the clouds", lazy=False)}
  <div class="wrap"><span class="eyebrow">404</span><h1>Lost in the <em>clouds</em>.</h1>
  <p class="lead">The page you’re looking for has wandered off the trail. Let’s get you back.</p>
  <div class="hero-actions"><a class="btn btn--light" href="/">Back home <span class="arrow">→</span></a><a class="btn btn--ghost" href="/blog/">Read the journal</a></div></div>
</section>"""
    add("/404.html", page("/404.html", "Page not found | Zibetti Photo + Film", "This page could not be found.", body, noindex=True))


# ----------------------------------------------------------------------------------------------

def write_out():
    # wipe generated html (keep assets and hand-written root files)
    keep = {"assets", "favicon.svg", "robots.txt", "index.php", "contact.php", ".htaccess"}
    for name in os.listdir(OUT):
        if name in keep:
            continue
        p = os.path.join(OUT, name)
        if os.path.isdir(p):
            shutil.rmtree(p)
        else:
            os.remove(p)
    for path, text in PAGES.items():
        if path == "/":
            target = os.path.join(OUT, "home.html")
        elif path.endswith(".html"):
            target = os.path.join(OUT, path.lstrip("/"))
        else:
            target = os.path.join(OUT, path.strip("/"), "index.html")
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            f.write(text)
    urls = [p for p in PAGES if not p.endswith(".html")]
    prio = lambda u: "1.0" if u == "/" else ("0.9" if u.count("/") == 2 else "0.7")
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"  <url><loc>{ORIGIN}{u}</loc><lastmod>{TODAY}</lastmod><priority>{prio(u)}</priority></url>")
    sm.append("</urlset>")
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write("\n".join(sm) + "\n")
    print(f"built {len(PAGES)} pages -> {OUT}")


if __name__ == "__main__":
    build_home()
    build_about()
    build_pricing()
    build_video()
    build_faq()
    build_contact()
    build_portfolio()
    build_tools()
    build_blog()
    build_legal()
    write_out()
