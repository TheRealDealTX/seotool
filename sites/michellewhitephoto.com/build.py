#!/usr/bin/env python3
"""Static site generator for michellewhitephoto.com.

    python3 build.py      # writes the deployable site into ./public

Standard library only. Page copy lives in content.py; this file holds the
shared layout, components and the page list.
"""
import json
import os
import re
import shutil
from html import escape

from PIL import Image

import content as C

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "public")
ORIGIN = C.SITE["origin"]
V = "6"

GTAG_ID = "G-FTGZF9WD7R"
GTAG = f"""<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GTAG_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', '{GTAG_ID}');
</script>"""

_SIZES = {}


def img_size(name):
    """Pixel size of the full (1600w) WebP, so every <img> gets width/height and doesn't shift layout."""
    if name not in _SIZES:
        with Image.open(os.path.join(SRC, "img", name + ".webp")) as im:
            _SIZES[name] = im.size
    return _SIZES[name]


OG_USED = set()  # asset cache-buster

NAV = [
    ("Home", "/"),
    ("About", "/about/"),
    ("Weddings", "/weddings/"),
    ("Interiors", "/interiors/"),
    ("Journal", "/blog/"),
    ("Contact", "/contact/"),
]


# ---------------------------------------------------------------- helpers
def img(name, alt, cls="", eager=False, sizes="(max-width: 960px) 100vw, 50vw", attrs=""):
    """Responsive <img> for an image in src/img (name without extension)."""
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    w, h = img_size(name)
    return (f'<img{c} src="/assets/img/{name}.webp" srcset="/assets/img/{name}-sm.webp 800w, '
            f'/assets/img/{name}.webp 1600w" sizes="{sizes}" width="{w}" height="{h}" alt="{escape(alt)}" '
            f'{loading} decoding="async"{attrs}>')


def url(path):
    return ORIGIN + path


def expand_images(html):
    """Replace [[name|alt]] placeholders in post bodies with responsive images."""
    import re
    return re.sub(r"\[\[([\w-]+)\|([^\]]+)\]\]", lambda m: img(m.group(1), m.group(2), sizes="(max-width: 960px) 100vw, 60vw"), html)


def post_url(slug):
    # The host 301s /blog/<slug> to /blog/<slug>/ before PHP runs, so the slash form is canonical.
    return f"/blog/{slug}/"


def crumbs(items):
    out = []
    for i, (label, href) in enumerate(items):
        if href and i < len(items) - 1:
            out.append(f'<a href="{href}">{escape(label)}</a>')
        else:
            out.append(f'<span aria-current="page" style="margin:0;opacity:1">{escape(label)}</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span aria-hidden="true">/</span>'.join(out) + "</nav>"


def breadcrumb_ld(items):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": label, "item": url(href)}
            for i, (label, href) in enumerate(items)
        ],
    }


BUSINESS_LD = {
    "@type": ["ProfessionalService", "LocalBusiness"],
    "@id": ORIGIN + "/#business",
    "name": C.SITE["name"],
    "alternateName": ["Michelle White Photography", "Michelle White"],
    "url": ORIGIN + "/",
    "email": C.SITE["email"],
    "image": ORIGIN + "/assets/og/hero-couple-field.jpg",
    "logo": {"@type": "ImageObject", "url": ORIGIN + "/web-app-manifest-512x512.png", "width": 512, "height": 512},
    "description": C.SITE["description"],
    "priceRange": "$$$",
    "address": {"@type": "PostalAddress", "addressLocality": "Salt Lake City", "addressRegion": "UT", "addressCountry": "US"},
    "areaServed": [{"@type": "State", "name": "Utah"}, {"@type": "City", "name": "Salt Lake City"},
                   {"@type": "City", "name": "Park City"}, {"@type": "Place", "name": "Destination weddings worldwide"}],
    "knowsAbout": ["Wedding photography", "Elopement photography", "Interior photography", "Architectural photography"],
}
WEBSITE_LD = {"@type": "WebSite", "@id": ORIGIN + "/#website", "url": ORIGIN + "/", "name": C.SITE["name"],
              "publisher": {"@id": ORIGIN + "/#business"}}


# ---------------------------------------------------------------- layout
def header(active):
    links = "".join(
        f'<li><a href="{href}"{" aria-current=\"page\"" if href == active else ""}>{label}</a></li>'
        for label, href in NAV
    )
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Michelle White Photo — home"><b>Michelle White</b><small>Photography</small></a>
    <nav class="nav" id="site-nav" aria-label="Main">
      <ul>{links}</ul>
      <div class="nav-cta"><a href="mailto:{C.SITE['email']}">{C.SITE['email']}</a><p>Weddings, elopements &amp; interiors — Salt Lake City, Utah &amp; beyond.</p></div>
    </nav>
    <a class="btn header-cta" href="/contact/">Inquire <span class="arr">&rarr;</span></a>
    <button class="nav-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="site-nav"><span></span><span></span><span></span></button>
  </div>
</header>"""


def footer():
    e = C.SITE["email"]
    return f"""<section class="marquee" aria-hidden="true"><div class="marquee-track">{"".join(
        f"<span>{w}</span><span>&#10022;</span>" for w in ["Weddings", "Elopements", "Interiors", "Utah", "Heirlooms", "Light"] * 2)}</div></section>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-top">
      <div>
        <a class="brand" href="/"><b>Michelle White</b><small>Photography</small></a>
        <p style="max-width:34ch">Natural, light-filled wedding and interior photography from Salt Lake City, Utah — made to feel the way the day felt.</p>
      </div>
      <div>
        <h2 class="foot-h">Explore</h2>
        <ul>{"".join(f'<li><a href="{h}">{l}</a></li>' for l, h in NAV[1:])}</ul>
      </div>
      <div>
        <h2 class="foot-h">Journal</h2>
        <ul>{"".join(f'<li><a href="{post_url(p["slug"])}">{escape(p["short"])}</a></li>' for p in C.POSTS[:5])}</ul>
      </div>
      <div>
        <h2 class="foot-h">Say hello</h2>
        <ul>
          <li><a href="mailto:{e}">{e}</a></li>
          <li>Salt Lake City, Utah</li>
          <li>Available for travel</li>
          <li style="margin-top:18px"><a href="/contact/">Check your date &rarr;</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-big" aria-hidden="true">Michelle White</div>
    <div class="footer-bottom">
      <span>&copy; <span data-year>2026</span> Michelle White Photo. All rights reserved.</span>
      <span><a href="/privacy-policy/">Privacy policy</a> &nbsp;·&nbsp; <a href="/sitemap.xml">Sitemap</a></span>
    </div>
  </div>
</footer>"""


def page(path, title, desc, body, active=None, ld=None, og_image="hero-couple-field", og_type="website",
         canonical=None, extra_head="", robots="index, follow", progress=False, og_alt=None):
    canonical = canonical if canonical is not None else url(path)
    canon_tag = f'<link rel="canonical" href="{canonical}">\n' if canonical else ""
    OG_USED.add(og_image)
    og_alt = og_alt or title
    # Preload the first high-priority (LCP) image.
    m = re.search(r'<img[^>]*srcset="([^"]+)" sizes="([^"]+)"[^>]*fetchpriority="high"', body)
    preload = (f'<link rel="preload" as="image" imagesrcset="{m.group(1)}" imagesizes="{m.group(2)}" fetchpriority="high">\n'
               if m else "")
    graph = [BUSINESS_LD, WEBSITE_LD] + (ld or [])
    ld_json = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=None)
    og_img = f"{ORIGIN}/assets/og/{og_image}.jpg"
    return f"""<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
{GTAG}
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<meta name="robots" content="{robots}">
{canon_tag}<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="{C.SITE['name']}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{canonical or url(path)}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{escape(og_alt)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(title)}">
<meta name="twitter:description" content="{escape(desc)}">
<meta name="twitter:image" content="{og_img}">
<meta name="theme-color" content="#1c1a18">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png" type="image/png" sizes="96x96">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
{preload}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Manrope:wght@400;600&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={V}">
{extra_head}<script type="application/ld+json">{ld_json}</script>
</head>
<body>
{'<div class="progress" aria-hidden="true"></div>' if progress else ''}{header(active)}
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/js/site.js?v={V}" defer></script>
</body>
</html>
"""


def page_hero(image, eyebrow, h1, sub, items, alt):
    return f"""<section class="page-hero">
  {img(image, alt, eager=True, sizes="100vw", attrs=' data-parallax="0.18"')}
  <div class="wrap">
    {crumbs(items)}
    <span class="eyebrow">{eyebrow}</span>
    <h1>{h1}</h1>
    {f'<p>{sub}</p>' if sub else ''}
  </div>
</section>"""


def cta_band(title="Let&rsquo;s make something <em>timeless</em>", text=None, image="mountains-sunset"):
    text = text or "Tell me about your day, your space or your story. I take a limited number of weddings and interior commissions each year so every one gets my full attention."
    return f"""<section class="cta-band">
  {img(image, "", sizes="100vw", attrs=' data-parallax="0.2" aria-hidden="true"')}
  <div class="wrap reveal">
    <span class="eyebrow" style="color:rgba(255,255,255,.85)">Now booking 2027 &amp; 2028</span>
    <h2>{title}</h2>
    <p>{text}</p>
    <a class="btn btn--light" href="/contact/">Start your inquiry <span class="arr">&rarr;</span></a>
  </div>
</section>"""


def post_card(p, cls=""):
    return f"""<a class="post-card reveal {cls}" href="{post_url(p['slug'])}">
  <div class="thumb">{img(p['image'], p['image_alt'], sizes="(max-width: 640px) 100vw, 33vw")}</div>
  <span class="meta">{p['category']} · {p['date_display']}</span>
  <h3>{escape(p['title_card'])}</h3>
  <p>{escape(p['excerpt'])}</p>
</a>"""


def gallery(items, filters=False):
    figs = []
    for name, alt, cat in items:
        figs.append(f'<figure class="reveal" data-cat="{cat}">{img(name, alt, sizes="(max-width: 640px) 50vw, 33vw", attrs=f" data-full=\"/assets/img/{name}.webp\"")}'
                    f'<figcaption>{escape(alt)}</figcaption></figure>')
    f = ""
    if filters:
        cats = []
        for _, _, c in items:
            if c not in cats:
                cats.append(c)
        f = '<div class="filters" role="group" aria-label="Filter gallery"><button class="is-active" aria-pressed="true" data-filter="all">All</button>' + "".join(
            f'<button aria-pressed="false" data-filter="{c}">{c.title()}</button>' for c in cats) + "</div>"
    return f + '<div class="gallery">' + "".join(figs) + "</div>"


# ---------------------------------------------------------------- pages
def build_home():
    slides = [("hero-couple-field", "Bride and groom walking hand in hand across an open mountain meadow"),
              ("black-sand", "Couple embracing on a black sand beach beneath sea stacks"),
              ("interior-lounge", "Sunlit modern living room with warm wood and low lounge chairs"),
              ("veil-field", "Groom wrapping the bride in her veil in a golden field")]
    sl = "".join(
        f'<div class="hero-slide{" is-active" if i == 0 else ""}">{img(n, a, eager=(i == 0), sizes="100vw")}</div>'
        for i, (n, a) in enumerate(slides))
    dots = "".join(f'<button aria-label="Show slide {i + 1}"{" class=\"is-active\"" if i == 0 else ""}></button>' for i in range(len(slides)))
    posts = "".join(post_card(p) for p in C.POSTS[:3])
    body = f"""<section class="hero">
  <div class="hero-slides">{sl}</div>
  <div class="hero-dots">{dots}</div>
  <div class="wrap hero-inner">
    <span class="eyebrow">Michelle White Photography · Salt Lake City, Utah</span>
    <h1><span class="line"><span>Honest light,</span></span><span class="line"><span><em>quiet</em> moments,</span></span><span class="line"><span>lasting heirlooms.</span></span></h1>
    <div class="hero-sub">
      <p>Wedding, elopement and interior photography for people who care how a picture <em>feels</em> — natural, unhurried and full of light.</p>
      <a class="btn btn--light" href="/contact/">Check your date <span class="arr">&rarr;</span></a>
    </div>
  </div>
  <div class="scroll-cue" aria-hidden="true"></div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="split-media">
      <div class="frame reveal-img">{img("bouquet-brick", "Bride holding a loose garden bouquet of peach roses and greenery")}</div>
      <div class="float reveal-img d2">{img("golden-rings", "Two gold wedding bands resting on soft white florals", sizes="30vw")}</div>
      <div class="badge" aria-hidden="true"><svg viewBox="0 0 124 124"><defs><path id="c" d="M62,62 m-46,0 a46,46 0 1,1 92,0 a46,46 0 1,1 -92,0"/></defs><text><textPath href="#c">Weddings · Interiors · Utah ·</textPath></text></svg></div>
    </div>
    <div class="reveal">
      <span class="eyebrow">Welcome</span>
      <h2>Photographs that feel like <em>the day felt</em></h2>
      <p class="lede">Michelle White Photo is a Salt Lake City photography studio for weddings, elopements and interiors. The approach is simple: find the best light, stay out of the way, and notice the small, unrepeatable things.</p>
      <p>Whether it&rsquo;s a mountain ceremony above Park City, a garden reception in the Salt Lake valley or a freshly finished home that deserves to be shown at its best, the goal is the same — clean, timeless images with real colour and real emotion that still look right in thirty years.</p>
      <p class="signature">Michelle White</p>
      <a class="link-line" href="/about/">More about the studio</a>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head">
      <h2 class="reveal">What we <em>photograph</em></h2>
      <p class="reveal d1">Three kinds of work, one way of seeing: patient, natural and quietly editorial.</p>
    </div>
    <div class="cards">
      <a class="card reveal" href="/weddings/">{img("lake-couple", "Bride and groom by a mountain lake at golden hour", sizes="(max-width: 640px) 100vw, 33vw")}
        <div class="card-body"><span class="num">01</span><h3>Weddings</h3><p>Full-day storytelling from getting ready to the last dance, across Utah and wherever you&rsquo;re headed.</p></div></a>
      <a class="card reveal d1" href="/weddings/#elopements">{img("black-sand", "Couple eloping on a dramatic black sand beach", sizes="(max-width: 640px) 100vw, 33vw")}
        <div class="card-body"><span class="num">02</span><h3>Elopements</h3><p>Intimate ceremonies in the desert, the mountains or the city — planned around the light.</p></div></a>
      <a class="card reveal d2" href="/interiors/">{img("interior-open-plan", "Open-plan modern home with white sofa and timber feature wall", sizes="(max-width: 640px) 100vw, 33vw")}
        <div class="card-body"><span class="num">03</span><h3>Interiors</h3><p>Editorial interior and architectural photography for designers, builders and publications.</p></div></a>
    </div>
  </div>
</section>

<section class="section section--tight" style="overflow:hidden">
  <div class="wrap strip">
    <figure>{img("bride-road", "Bride in a floral gown standing on an open desert road", sizes="33vw", attrs=' data-parallax="0.08"')}</figure>
    <figure>{img("floral-arch", "Wedding arch draped in linen and garden roses", sizes="40vw", attrs=' data-parallax="-0.06"')}</figure>
    <figure>{img("staircase", "Bright modern staircase with timber treads and gallery wall", sizes="33vw", attrs=' data-parallax="0.1"')}</figure>
  </div>
</section>

<section class="section section--dark statement">
  <div class="wrap reveal">
    <span class="eyebrow">The approach</span>
    <blockquote>&ldquo;The best photographs aren&rsquo;t posed. They&rsquo;re <em>noticed</em>.&rdquo;</blockquote>
    <cite>— Michelle White Photo</cite>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2 class="reveal">How it <em>works</em></h2>
      <p class="reveal d1">A calm, clear process from first email to finished gallery — no surprises.</p>
    </div>
    <div class="steps">
      <div class="step reveal"><h3>Inquire</h3><p>Share your date, location and what matters most. You&rsquo;ll get availability and a collection guide within two business days.</p></div>
      <div class="step reveal d1"><h3>Plan</h3><p>A planning call shapes a photography timeline around sunset, travel and the moments you can&rsquo;t miss.</p></div>
      <div class="step reveal d2"><h3>Create</h3><p>On the day, gentle direction when it helps and quiet observation when it doesn&rsquo;t. Nothing stiff, nothing forced.</p></div>
      <div class="step reveal d3"><h3>Treasure</h3><p>A sneak peek within a week and your full, hand-edited online gallery within six weeks, ready to print and share.</p></div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head">
      <h2 class="reveal">From the <em>journal</em></h2>
      <a class="link-line reveal d1" href="/blog/">All stories</a>
    </div>
    <div class="posts">{posts}</div>
  </div>
</section>

<section class="section">
  <div class="wrap narrow">
    <div class="reveal" style="text-align:center;margin-bottom:40px">
      <span class="eyebrow">Questions</span>
      <h2>Good to <em>know</em></h2>
    </div>
    <div class="faq reveal">{faq_html(C.HOME_FAQ)}</div>
  </div>
</section>

{cta_band()}"""
    ld = [faq_ld(C.HOME_FAQ),
          {"@type": "WebPage", "@id": ORIGIN + "/#webpage", "url": ORIGIN + "/", "name": C.HOME_TITLE,
           "about": {"@id": ORIGIN + "/#business"}, "isPartOf": {"@id": ORIGIN + "/#website"}}]
    return page("/", C.HOME_TITLE, C.HOME_DESC, body, active="/", ld=ld)


def faq_html(items):
    return "".join(f"<details><summary>{escape(q)}</summary><p>{a}</p></details>" for q, a in items)


def faq_ld(items):
    import re
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}}
        for q, a in items]}


def build_about():
    items = [("Home", "/"), ("About", "/about/")]
    body = page_hero("mountains-sunset", "About", "About Michelle White <em>Photography</em>",
                     "A Salt Lake City studio for weddings, elopements and interiors — built on natural light and an unhurried eye.",
                     items, "Snow-capped mountain peaks above a sea of clouds at sunset") + f"""
<section class="section">
  <div class="wrap split">
    <div class="split-media">
      <div class="frame reveal-img">{img("photographer-flowers", "Photographer framing a shot through blooming pink flowers")}</div>
      <div class="float reveal-img d2">{img("camera", "Mirrorless camera body and lenses on a dark surface", sizes="30vw")}</div>
    </div>
    <div class="reveal">
      <span class="eyebrow">The studio</span>
      <h2>Light first. <em>People always.</em></h2>
      {C.ABOUT_INTRO}
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head"><h2 class="reveal">What guides the <em>work</em></h2></div>
    <div class="steps">
      {"".join(f'<div class="step reveal d{i % 4}"><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(C.VALUES))}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split split--rev">
    <div class="split-media">
      <div class="frame reveal-img">{img("interior-gallery-wall", "Light-filled living room with a grid of framed photographs")}</div>
    </div>
    <div class="reveal">
      <span class="eyebrow">Two disciplines, one eye</span>
      <h2>Weddings <em>&amp;</em> interiors</h2>
      {C.ABOUT_TWO}
      <div style="display:flex;flex-wrap:wrap;gap:14px;margin-top:10px">
        <a class="btn" href="/weddings/">Weddings <span class="arr">&rarr;</span></a>
        <a class="btn" href="/interiors/">Interiors <span class="arr">&rarr;</span></a>
      </div>
    </div>
  </div>
</section>

<section class="section section--dark">
  <div class="wrap">
    <div class="section-head"><h2 class="reveal">What&rsquo;s <em>included</em></h2><p class="reveal d1">Every wedding collection is built around the same essentials.</p></div>
    <div class="steps">
      {"".join(f'<div class="step reveal d{i % 4}"><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(C.INCLUDED))}
    </div>
  </div>
</section>

{cta_band("Tell me your <em>story</em>", image="hands-held")}"""
    ld = [breadcrumb_ld(items), {"@type": "AboutPage", "url": url("/about/"), "name": C.ABOUT_TITLE,
                                 "about": {"@id": ORIGIN + "/#business"}}]
    return page("/about/", C.ABOUT_TITLE, C.ABOUT_DESC, body, active="/about/", ld=ld, og_image="mountains-sunset")


def build_weddings():
    items = [("Home", "/"), ("Weddings", "/weddings/")]
    body = page_hero("veil-field", "Weddings &amp; elopements", "Utah wedding <em>photography</em>",
                     "Natural, editorial wedding and elopement photography in Salt Lake City, Park City and across the American West.",
                     items, "Groom wrapping his bride in her veil in a golden meadow") + f"""
<section class="section">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Your day, as it was</span>
      <h2>Unposed, unhurried, <em>unforgettable</em></h2>
      {C.WEDDINGS_INTRO}
    </div>
    <div class="split-media">
      <div class="frame reveal-img">{img("beach-veil", "Bride and groom on a pebble beach with a cathedral-length veil")}</div>
      <div class="float reveal-img d2">{img("ring-hands", "Couple's hands with wedding rings and a small bouquet", sizes="30vw")}</div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head"><h2 class="reveal">The <em>portfolio</em></h2><p class="reveal d1">Tap any image to view it full screen.</p></div>
    {gallery(C.WEDDING_GALLERY, filters=True)}
  </div>
</section>

<section class="section" id="elopements">
  <div class="wrap split split--rev">
    <div class="split-media">
      <div class="frame reveal-img">{img("black-sand", "Couple dancing on a black sand beach during their elopement")}</div>
    </div>
    <div class="reveal">
      <span class="eyebrow">Elopements</span>
      <h2>Small ceremony, <em>big</em> landscape</h2>
      {C.ELOPEMENT_INTRO}
    </div>
  </div>
</section>

<section class="section section--dark">
  <div class="wrap">
    <div class="section-head"><h2 class="reveal">Collections</h2><p class="reveal d1">Every collection can be tailored. Full pricing is shared with your availability.</p></div>
    <div class="steps">
      {"".join(f'<div class="step reveal d{i % 4}"><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(C.COLLECTIONS))}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap narrow">
    <div class="reveal" style="text-align:center;margin-bottom:40px"><span class="eyebrow">Wedding FAQ</span><h2>Planning <em>questions</em></h2></div>
    <div class="faq reveal">{faq_html(C.WEDDING_FAQ)}</div>
  </div>
</section>

{cta_band("Is your date still <em>open?</em>", image="confetti-exit")}"""
    ld = [breadcrumb_ld(items), faq_ld(C.WEDDING_FAQ),
          {"@type": "Service", "name": "Wedding & elopement photography", "serviceType": "Wedding photography",
           "provider": {"@id": ORIGIN + "/#business"}, "areaServed": "Utah", "url": url("/weddings/")}]
    return page("/weddings/", C.WEDDINGS_TITLE, C.WEDDINGS_DESC, body, active="/weddings/", ld=ld, og_image="veil-field")


def build_interiors():
    items = [("Home", "/"), ("Interiors", "/interiors/")]
    body = page_hero("interior-lounge", "Interiors &amp; architecture", "Interior <em>photography</em>",
                     "Editorial interior and architectural photography for designers, architects, builders and publications in Salt Lake City and beyond.",
                     items, "Sunlit modern living room with warm timber and lounge chairs") + f"""
<section class="section">
  <div class="wrap split">
    <div class="split-media">
      <div class="frame reveal-img">{img("interior-yellow-chair", "Minimal living room with a mustard armchair and black-and-white art")}</div>
      <div class="float reveal-img d2">{img("staircase", "Floating timber staircase in a bright modern home", sizes="30vw")}</div>
    </div>
    <div class="reveal">
      <span class="eyebrow">Spaces with a story</span>
      <h2>Rooms that <em>breathe</em></h2>
      {C.INTERIORS_INTRO}
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head"><h2 class="reveal">Selected <em>spaces</em></h2></div>
    {gallery(C.INTERIOR_GALLERY)}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2 class="reveal">Who it&rsquo;s <em>for</em></h2></div>
    <div class="steps">
      {"".join(f'<div class="step reveal d{i % 4}"><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(C.INTERIOR_CLIENTS))}
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap narrow">
    <div class="reveal" style="text-align:center;margin-bottom:40px"><span class="eyebrow">Interiors FAQ</span><h2>Before the <em>shoot</em></h2></div>
    <div class="faq reveal">{faq_html(C.INTERIOR_FAQ)}</div>
  </div>
</section>

{cta_band("Show your space at its <em>best</em>", "Booking interior and architectural shoots for designers, builders and editorial clients. Tell me about the project and your timeline.", image="home-exterior-dusk")}"""
    ld = [breadcrumb_ld(items), faq_ld(C.INTERIOR_FAQ),
          {"@type": "Service", "name": "Interior & architectural photography", "serviceType": "Interior photography",
           "provider": {"@id": ORIGIN + "/#business"}, "areaServed": "Utah", "url": url("/interiors/")}]
    return page("/interiors/", C.INTERIORS_TITLE, C.INTERIORS_DESC, body, active="/interiors/", ld=ld, og_image="interior-lounge")


def build_blog_index():
    items = [("Home", "/"), ("Journal", "/blog/")]
    cards = "".join(post_card(p) for p in C.POSTS)
    body = page_hero("bw-kiss", "The journal", "Stories, guides <em>&amp;</em> inspiration",
                     "Wedding stories, styling ideas and practical planning advice from the Michelle White Photo studio.",
                     items, "Black-and-white photograph of a bride and groom kissing in the wind") + f"""
<section class="section">
  <div class="wrap">
    <div class="posts posts--featured">{cards}</div>
  </div>
</section>
{cta_band()}"""
    ld = [breadcrumb_ld(items), {"@type": "Blog", "url": url("/blog/"), "name": "Michelle White Photo Journal",
                                 "blogPost": [{"@type": "BlogPosting", "headline": p["h1_plain"], "url": url(post_url(p["slug"]))} for p in C.POSTS]}]
    return page("/blog/", C.BLOG_TITLE, C.BLOG_DESC, body, active="/blog/", ld=ld, og_image="bw-kiss")


def build_post(p):
    path = post_url(p["slug"])
    items = [("Home", "/"), ("Journal", "/blog/"), (p["short"], path)]
    others = [o for o in C.POSTS if o["slug"] != p["slug"]]
    hero = f"""<section class="page-hero">
  {img(p['image'], p['image_alt'], eager=True, sizes="100vw", attrs=' data-parallax="0.18"')}
  <div class="wrap">
    {crumbs(items)}
    <span class="eyebrow">{p['category']}</span>
    <h1>{p['h1']}</h1>
    <div class="post-meta"><span>{p['date_display']}</span><span>{p['read']} min read</span><span>Michelle White Photo</span></div>
  </div>
</section>"""
    body = hero + f"""
<section class="section">
  <div class="wrap article-wrap">
    <article class="prose">
      {expand_images(p['body'])}
      <p style="margin-top:2.4em"><a class="btn btn--solid" href="/contact/">Plan your photography <span class="arr">&rarr;</span></a></p>
    </article>
    <aside class="aside">
      <div class="aside-box">
        <h3>Planning a wedding?</h3>
        <p>Natural, light-led wedding and elopement photography in Salt Lake City, Utah and beyond.</p>
        <a class="link-line" href="/contact/">Check your date</a>
      </div>
      <div class="aside-box">
        <h3>More stories</h3>
        <ul>{"".join(f'<li><a href="{post_url(o["slug"])}">{escape(o["short"])}</a></li>' for o in others)}</ul>
      </div>
    </aside>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head"><h2 class="reveal">Keep <em>reading</em></h2><a class="link-line reveal" href="/blog/">All stories</a></div>
    <div class="posts">{"".join(post_card(o) for o in others[:3])}</div>
  </div>
</section>"""
    ld = [breadcrumb_ld(items), {
        "@type": "BlogPosting", "headline": p["h1_plain"], "description": p["desc"], "url": url(path),
        "mainEntityOfPage": url(path), "datePublished": p["date"], "dateModified": C.MODIFIED,
        "image": f"{ORIGIN}/assets/og/{p['image']}.jpg",
        "author": {"@type": "Organization", "name": C.SITE["name"], "url": ORIGIN + "/"},
        "publisher": {"@id": ORIGIN + "/#business"}}]
    extra = f'<meta property="article:published_time" content="{p["date"]}">\n'
    return page(path, p["title"], p["desc"], body, active="/blog/", ld=ld, og_image=p["image"],
                og_type="article", extra_head=extra, progress=True, og_alt=p["image_alt"])


def build_contact():
    items = [("Home", "/"), ("Contact", "/contact/")]
    e = C.SITE["email"]
    body = page_hero("ceremony-aisle", "Inquire", "Let&rsquo;s <em>talk</em>",
                     "Share a few details and you&rsquo;ll hear back within two business days with availability and a collection guide.",
                     items, "Outdoor ceremony aisle lined with chairs and pastel floral arrangements") + f"""
<section class="section">
  <div class="wrap contact-grid">
    <div class="contact-info reveal">
      <span class="eyebrow">Get in touch</span>
      <h2>Check your <em>date</em></h2>
      <p>Weddings, elopements, interiors and editorial commissions. If your date is close, email is the quickest way to reach the studio.</p>
      <dl>
        <dt>Email</dt><dd><a href="mailto:{e}">{e}</a></dd>
        <dt>Studio</dt><dd>Salt Lake City, Utah</dd>
        <dt>Travel</dt><dd>Park City, Moab, the Wasatch &amp; worldwide</dd>
        <dt>Reply time</dt><dd>Within two business days</dd>
      </dl>
    </div>
    <div class="reveal d1">
      <div id="form-status" role="status" aria-live="polite"></div>
      <form class="form" action="/contact.php" method="post">
        <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" required autocomplete="name"></div>
        <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" required autocomplete="email"></div>
        <div class="field"><label for="f-type">I&rsquo;m inquiring about</label>
          <select id="f-type" name="type"><option>Wedding</option><option>Elopement</option><option>Engagement session</option><option>Interior / architecture</option><option>Something else</option></select></div>
        <div class="field"><label for="f-date">Date (if known)</label><input id="f-date" name="date" type="text" placeholder="e.g. June 12, 2027"></div>
        <div class="field full"><label for="f-loc">Location / venue</label><input id="f-loc" name="location"></div>
        <div class="field full"><label for="f-msg">Tell me about it</label><textarea id="f-msg" name="message" required></textarea></div>
        <div class="hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
        <div class="full" style="display:flex;flex-wrap:wrap;align-items:center;gap:20px">
          <button class="btn btn--solid" type="submit">Send inquiry <span class="arr">&rarr;</span></button>
          <p class="form-note">Prefer email? Write to <a href="mailto:{e}">{e}</a></p>
        </div>
      </form>
    </div>
  </div>
</section>
<script>
(function(){{var s=new URLSearchParams(location.search).get('sent'),el=document.getElementById('form-status');
if(s==='1')el.innerHTML='<div class="notice notice--ok">Thank you — your inquiry is on its way. You&rsquo;ll hear back within two business days.</div>';
if(s==='0')el.innerHTML='<div class="notice notice--err">Sorry, that didn&rsquo;t send. Please check the form or email {e} directly.</div>';}})();
</script>"""
    ld = [breadcrumb_ld(items), {"@type": "ContactPage", "url": url("/contact/"), "name": C.CONTACT_TITLE}]
    return page("/contact/", C.CONTACT_TITLE, C.CONTACT_DESC, body, active="/contact/", ld=ld, og_image="ceremony-aisle")


def build_privacy():
    items = [("Home", "/"), ("Privacy policy", "/privacy-policy/")]
    body = page_hero("chairs-lawn", "Legal", "Privacy policy", None, items, "Two decorated chairs on a lawn") + f"""
<section class="section"><div class="wrap narrow prose">{C.PRIVACY}</div></section>"""
    return page("/privacy-policy/", "Privacy Policy | Michelle White Photo", "How Michelle White Photo collects, uses and protects the information you share through this website.",
                body, ld=[breadcrumb_ld(items)], og_image="chairs-lawn")


def build_404():
    body = f"""<section class="page-hero" style="min-height:100vh">
  {img("mountains-sunset", "Mountain peaks above the clouds", eager=True, sizes="100vw")}
  <div class="wrap">
    <span class="eyebrow">Error 404</span>
    <h1>This page has <em>wandered off</em></h1>
    <p>The page you&rsquo;re looking for may have moved. Try the journal, the portfolio or head back home.</p>
    <div style="display:flex;flex-wrap:wrap;gap:14px;margin-top:30px">
      <a class="btn btn--light" href="/">Home <span class="arr">&rarr;</span></a>
      <a class="btn btn--light" href="/blog/">Journal <span class="arr">&rarr;</span></a>
      <a class="btn btn--light" href="/contact/">Contact <span class="arr">&rarr;</span></a>
    </div>
  </div>
</section>"""
    return page("/404.html", "Page not found | Michelle White Photo", "The page you were looking for could not be found.",
                body, robots="noindex, follow", canonical="")


# ---------------------------------------------------------------- write
PAGES = {}


def write(rel, html):
    PAGES[rel] = html
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(SRC, "img"), os.path.join(OUT, "assets/img"))
    os.makedirs(os.path.join(OUT, "assets/css"))
    os.makedirs(os.path.join(OUT, "assets/js"))
    shutil.copy(os.path.join(SRC, "site.css"), os.path.join(OUT, "assets/css/site.css"))
    shutil.copy(os.path.join(SRC, "site.js"), os.path.join(OUT, "assets/js/site.js"))
    for f in ("index.php", "contact.php", ".htaccess", "robots.txt", "googlecccfbf2f7e9e5ae4.html"):
        shutil.copy(os.path.join(SRC, f), os.path.join(OUT, f))
    build_icons()

    # Homepage is home.html served by index.php (see README "Hosting note").
    write("home.html", build_home())
    write("about/index.html", build_about())
    write("weddings/index.html", build_weddings())
    write("interiors/index.html", build_interiors())
    write("blog/index.html", build_blog_index())
    for p in C.POSTS:
        write(f"blog/{p['slug']}/index.html", build_post(p))
    write("contact/index.html", build_contact())
    write("privacy-policy/index.html", build_privacy())
    write("404.html", build_404())

    build_og()

    urls = [("/", "home.html", "1.0"), ("/about/", "about/index.html", "0.8"), ("/weddings/", "weddings/index.html", "0.9"),
            ("/interiors/", "interiors/index.html", "0.9"), ("/blog/", "blog/index.html", "0.7"),
            ("/contact/", "contact/index.html", "0.6"), ("/privacy-policy/", "privacy-policy/index.html", "0.2")] + [
        (post_url(p["slug"]), f"blog/{p['slug']}/index.html", "0.6") for p in C.POSTS]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for u, rel, pr in urls:
        # Images in <main> only (the footer repeats nothing image-wise, but keep it scoped anyway).
        main = PAGES[rel].split('<main id="main">', 1)[1].split("</main>", 1)[0]
        imgs = list(dict.fromkeys(re.findall(r'src="(/assets/img/[\w-]+\.webp)"', main)))
        im = "".join(f"<image:image><image:loc>{ORIGIN}{i}</image:loc></image:image>" for i in imgs)
        sm.append(f"  <url><loc>{url(u)}</loc><lastmod>{C.MODIFIED}</lastmod><priority>{pr}</priority>{im}</url>")
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm) + "\n")
    print(f"built {len(urls) + 1} pages into {OUT}")


def build_icons():
    """Favicon set from src/icon-master.png (1024px)."""
    import base64
    import io
    master = Image.open(os.path.join(SRC, "icon-master.png")).convert("RGBA")

    def sized(n):
        return master.resize((n, n), Image.LANCZOS)
    sized(48).save(os.path.join(OUT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    sized(96).save(os.path.join(OUT, "favicon-96x96.png"), optimize=True)
    # Apple ignores transparency, so give the touch icon a solid square background.
    apple = Image.new("RGBA", (180, 180), (28, 26, 24, 255))
    apple.alpha_composite(sized(180))
    apple.convert("RGB").save(os.path.join(OUT, "apple-touch-icon.png"), optimize=True)
    for n in (192, 512):
        sized(n).save(os.path.join(OUT, f"web-app-manifest-{n}x{n}.png"), optimize=True)
    buf = io.BytesIO()
    sized(128).save(buf, "PNG", optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    with open(os.path.join(OUT, "favicon.svg"), "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 128 128">'
                f'<image width="128" height="128" xlink:href="data:image/png;base64,{b64}"/></svg>')
    manifest = {
        "name": C.SITE["name"], "short_name": "M. White Photo", "start_url": "/", "display": "standalone",
        "background_color": "#f7f2eb", "theme_color": "#1c1a18",
        "icons": [{"src": f"/web-app-manifest-{n}x{n}.png", "sizes": f"{n}x{n}", "type": "image/png", "purpose": "any"}
                  for n in (192, 512)],
    }
    with open(os.path.join(OUT, "site.webmanifest"), "w") as f:
        json.dump(manifest, f, indent=2)


def build_og():
    """1200x630 JPEG share images (social platforms handle JPEG more reliably than WebP)."""
    os.makedirs(os.path.join(OUT, "assets/og"), exist_ok=True)
    for name in sorted(OG_USED):
        with Image.open(os.path.join(SRC, "img", name + ".webp")) as im:
            im = im.convert("RGB")
            tw, th = 1200, 630
            scale = max(tw / im.width, th / im.height)
            im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
            left, top = (im.width - tw) // 2, max(0, (im.height - th) // 3)
            im.crop((left, top, left + tw, top + th)).save(os.path.join(OUT, f"assets/og/{name}.jpg"), quality=82, optimize=True, progressive=True)


if __name__ == "__main__":
    main()
