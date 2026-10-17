#!/usr/bin/env python3
"""Generate the evergrey-photography.com static site into public/.

Pages are written to public/_pages/<route>.html and served at clean,
slash-less URLs (the original Wix paths: /about, /post/<slug>) by
public/index.php. Run: python3 build.py && python3 validate.py
"""
import datetime as dt
import html
import json
import os
import re
import shutil
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import siteconfig as C  # noqa: E402

FONTS = "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&amp;family=Manrope:wght@400;500;600&amp;display=swap"

GTAG = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-BTLDQSK5EM"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-BTLDQSK5EM');
</script>"""
from content import posts_a, posts_b, posts_c  # noqa: E402

ROOT = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(ROOT, "public")
PAGES = os.path.join(PUB, "_pages")
IMG = os.path.join(PUB, "assets", "img")
VER = dt.date.today().strftime("%Y%m%d")
TODAY = dt.date.today().isoformat()

POSTS = sorted(posts_a.POSTS + posts_b.POSTS + posts_c.POSTS, key=lambda p: p["date"], reverse=True)
POST_BY_SLUG = {p["slug"]: p for p in POSTS}
SITEMAP = []

esc = html.escape


def og(key):
    """1200x630 JPEG share image (Facebook/LinkedIn don't reliably read WebP)."""
    d = os.path.join(IMG, "og")
    os.makedirs(d, exist_ok=True)
    out = os.path.join(d, key + ".jpg")
    if not os.path.exists(out):
        with Image.open(os.path.join(IMG, key + ".webp")) as im:
            im = im.convert("RGB")
            r = max(1200 / im.width, 630 / im.height)
            im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
            x, y = (im.width - 1200) // 2, (im.height - 630) // 2
            im.crop((x, y, x + 1200, y + 630)).save(out, "JPEG", quality=82, optimize=True, progressive=True)
    return key


def url(route):
    return C.SITE + ("/" if route == "" else "/" + route)


# ---------------------------------------------------------------- images
_dims = {}


def dims(key, sm=False):
    f = os.path.join(IMG, key + ("-sm" if sm else "") + ".webp")
    if f not in _dims:
        with Image.open(f) as im:
            _dims[f] = im.size
    return _dims[f]


def img(key, alt, sizes="100vw", cls="", eager=False, attrs=""):
    w, h = dims(key)
    sw, _ = dims(key, True)
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img src="/assets/img/{key}-sm.webp" srcset="/assets/img/{key}-sm.webp {sw}w, /assets/img/{key}.webp {w}w" '
            f'sizes="{sizes}" width="{w}" height="{h}" alt="{esc(alt)}" {load}{c}{attrs}>')


def figure_tokens(body):
    def rep(m):
        parts = m.group(1).split("|")
        key, alt = parts[0].strip(), parts[1].strip() if len(parts) > 1 else ""
        cap = parts[2].strip() if len(parts) > 2 else ""
        figcap = f"<figcaption>{cap}</figcaption>" if cap else ""
        return f'<figure><div class="img-reveal">{img(key, alt, "(max-width: 1020px) 100vw, 760px")}</div>{figcap}</figure>'
    return re.sub(r"\{\{img:([^}]+)\}\}", rep, body)


# ---------------------------------------------------------------- icons
ICON = {
    "camera": '<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>',
    "leaf": '<path d="M5 19c0-8 6-14 15-14 0 9-6 15-14 15"/><path d="M5 19l8-8"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "heart": '<path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.5-7 10-7 10z"/>',
    "map": '<path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2z"/><path d="M9 4v14M15 6v14"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "compass": '<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2 5-5 2 2-5z"/>',
    "image": '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="m21 16-5-5-9 9"/>',
}


def icon(name):
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[name]}</svg>')


LOGO = ('<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="19" fill="none" stroke="currentColor" stroke-width="1.2"/>'
        '<path d="M20 7 12.5 19h4L11 27.5h7V33h4v-5.5h7L23.5 19h4z" fill="currentColor"/></svg>')

ARROW = '<span class="arr" aria-hidden="true">→</span>'


# ---------------------------------------------------------------- layout
def header(active, over_hero):
    links = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if active == h else ""}>{t}</a>' for h, t in C.NAV)
    mlinks = "".join(
        f'<li><a class="m-link" href="{h}">{t}<small>0{i + 1}</small></a></li>' for i, (h, t) in enumerate(C.NAV))
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header{" over-hero" if over_hero else ""}">
  <div class="wrap">
    <a class="logo" href="/" aria-label="{C.NAME} home">{LOGO}<span class="logo-text">Evergrey<small>Photography</small></span></a>
    <nav class="main-nav" aria-label="Main">{links}<a class="nav-cta" href="/contact">Inquire</a></nav>
    <button class="nav-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-nav"><span></span><span></span><span></span></button>
  </div>
</header>
<div class="mobile-nav" id="mobile-nav" aria-hidden="true">
  <nav aria-label="Mobile"><ul>{mlinks}<li><a class="m-link" href="/contact">Inquire<small>09</small></a></li></ul></nav>
  <div class="m-foot"><p>Victoria, BC · Vancouver Island<br><a href="mailto:{C.EMAIL}">{C.EMAIL}</a></p></div>
</div>'''


def footer():
    svc = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in [
        ("/weddings", "Victoria weddings"), ("/elopements", "Vancouver Island elopements"),
        ("/engagements", "Engagements & couples"), ("/portfolio", "Portfolio"), ("/pricing", "Pricing")])
    tools = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in [
        ("/tools/golden-hour-calculator", "Golden hour calculator"), ("/tools/wedding-timeline-planner", "Wedding timeline planner"),
        ("/tools/elopement-location-finder", "Elopement location finder"), ("/blog", "The Journal")])
    studio = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in [
        ("/about", "About"), ("/contact", "Contact"), ("/post/kasha-justin", "Kasha + Justin"),
        ("/post/sarina-riley", "Sarina + Riley"), ("/post/florence-kyle", "Florence + Kyle"), ("/privacy-policy", "Privacy")])
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="logo" href="/">{LOGO}<span class="logo-text">Evergrey<small>Photography</small></span></a>
        <p style="margin-top:22px;max-width:34ch">Wedding, elopement and couples photography in Victoria, BC — and anywhere the Vancouver Island coast takes you.</p>
        <p><a href="mailto:{C.EMAIL}">{C.EMAIL}</a></p>
      </div>
      <div><h4>Photography</h4><ul>{svc}</ul></div>
      <div><h4>Plan</h4><ul>{tools}</ul></div>
      <div><h4>Studio</h4><ul>{studio}</ul></div>
    </div>
    <p class="foot-big"><a href="/contact">Let’s make something honest.</a></p>
    <div class="foot-bottom"><span>© <span data-year>{dt.date.today().year}</span> {C.NAME} · Victoria, British Columbia</span><span>Serving Victoria, Sooke, the Saanich Peninsula, Cowichan Valley &amp; all of Vancouver Island</span></div>
  </div>
</footer>
<button class="to-top" type="button" aria-label="Back to top">↑</button>'''


def org_schema():
    return {
        "@type": ["LocalBusiness", "ProfessionalService"],
        "@id": C.SITE + "/#business",
        "name": C.NAME,
        "url": C.SITE + "/",
        "email": C.EMAIL,
        "image": C.SITE + "/assets/img/hero-bouquet-golden-light.webp",
        "logo": C.SITE + "/assets/img/logo.png",
        "description": "Wedding, elopement and engagement photographer based in Victoria, BC, serving all of Vancouver Island.",
        "priceRange": "$$",
        "address": {"@type": "PostalAddress", "addressLocality": C.CITY, "addressRegion": C.REGION, "addressCountry": "CA"},
        "geo": {"@type": "GeoCoordinates", "latitude": C.GEO[0], "longitude": C.GEO[1]},
        "areaServed": [{"@type": "Place", "name": a} for a in C.AREAS],
        "knowsAbout": ["Wedding photography", "Elopement photography", "Engagement photography", "Couples photography"],
    }


def breadcrumbs(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": url(r)} for i, (n, r) in enumerate(trail)]}


def crumbs_html(trail):
    parts = []
    for i, (n, r) in enumerate(trail):
        if i == len(trail) - 1:
            parts.append(f"<span aria-current=\"page\" style=\"margin:0;opacity:1\">{esc(n)}</span>")
        else:
            parts.append(f'<a href="{"/" + r if r else "/"}">{esc(n)}</a><span>/</span>')
    return f'<nav class="crumbs" aria-label="Breadcrumb">{"".join(parts)}</nav>'


def faq_schema(faq):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in faq]}


def faq_html(faq, title="Questions couples ask"):
    items = "".join(f"<details><summary>{esc(q)}</summary><div><p>{a}</p></div></details>" for q, a in faq)
    return f'<div class="faq">{f"<h2 data-reveal>{title}</h2>" if title else ""}{items}</div>'


def page(route, title, desc, body, *, active="", over_hero=True, schema=None, og_image="hero-bouquet-golden-light",
         og_type="website", scripts="", head_extra="", sitemap=True, priority="0.7", lastmod=None, full_title=False):
    canonical = url(route)
    t = title if full_title or len(title) + len(C.NAME) + 3 > 66 else f"{title} | {C.NAME}"
    graph = [org_schema(), {"@type": "WebSite", "@id": C.SITE + "/#website", "url": C.SITE + "/", "name": C.NAME}]
    graph += schema or []
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    doc = f'''<!doctype html>
<html lang="en-CA">
<head>
{GTAG}
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(t)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#1b2420">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{C.NAME}">
<meta property="og:title" content="{esc(t)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{C.SITE}/assets/img/og/{og(og_image)}.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:alt" content="{esc(t)}">
<meta property="og:locale" content="en_CA">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(t)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{C.SITE}/assets/img/og/{og_image}.jpg">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png" type="image/png" sizes="96x96">
<link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">
<link rel="manifest" href="/site.webmanifest">
<link rel="alternate" type="application/rss+xml" title="The Evergrey Journal" href="/feed.xml">
<meta name="apple-mobile-web-app-title" content="Evergrey">
<meta name="author" content="{C.NAME}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="{FONTS}" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="{FONTS}"></noscript>
<link rel="stylesheet" href="/assets/css/site.css?v={VER}">
{head_extra}<script type="application/ld+json">{ld}</script>
</head>
<body>
{header(active, over_hero)}
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/js/site.js?v={VER}" defer></script>
{scripts}</body>
</html>
'''
    out = os.path.join(PAGES, (route or "index") + ".html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(doc)
    if sitemap:
        imgs = []
        for k in re.findall(r"/assets/img/([a-z0-9-]+?)(?:-sm)?\.webp", body):
            if k not in imgs:
                imgs.append(k)
        SITEMAP.append((canonical, lastmod or TODAY, priority, imgs[:20]))


def page_hero(h1, lead, image, alt, trail, cls="", eyebrow=""):
    eb = f'<span class="eyebrow light">{eyebrow}</span>' if eyebrow else ""
    return f'''<section class="page-hero grain {cls}">
  <div class="bg" data-parallax="0.12">{img(image, alt, eager=True)}</div>
  <div class="wrap">{crumbs_html(trail)}{eb}<h1>{h1}</h1><p class="lead">{lead}</p></div>
</section>'''


def cta(title="Tell us about your <em>day</em>", lead="Share your date, your place and what matters most. We reply to every inquiry within two business days.", image="ocean-sunset-rocks"):
    return f'''<section class="section cta grain">
  <div class="bg" data-parallax="0.15">{img(image, "", sizes="100vw")}</div>
  <div class="wrap"><span class="eyebrow light">Now booking 2027 &amp; 2028</span><h2 data-reveal>{title}</h2><p class="lead" data-reveal>{lead}</p>
  <div class="btn-row" data-reveal><a class="btn light" href="/contact">Check your date {ARROW}</a><a class="btn ghost-light" href="/pricing">See pricing</a></div></div>
</section>'''


def post_card(p, big=False, i=0):
    d = dt.date.fromisoformat(p["date"]).strftime("%b %Y")
    return f'''<a class="post-card{" big" if big else ""}" href="/post/{p["slug"]}" data-cat="{p["category"].lower().replace(" ", "-")}" data-reveal data-delay="{(i % 3) * 120}">
  <div class="thumb">{img(p["image"], p["image_alt"], "(max-width: 680px) 100vw, (max-width: 1020px) 50vw, 420px")}</div>
  <span class="meta">{p["category"]} · {d}</span><h3>{esc(p["h1"])}</h3><p>{esc(p["excerpt"])}</p>
</a>'''


def service_schema(name, desc, route, offers_from=None):
    s = {"@type": "Service", "name": name, "description": desc, "serviceType": name, "url": url(route),
         "provider": {"@id": C.SITE + "/#business"}, "areaServed": {"@type": "Place", "name": "Vancouver Island, BC"}}
    if offers_from:
        s["offers"] = {"@type": "Offer", "priceCurrency": "CAD", "price": str(offers_from), "url": url("pricing")}
    return s


def split(media, text, flip=False, cls=""):
    return f'<div class="split {"flip " if flip else ""}{cls}"><div class="media">{media}</div><div>{text}</div></div>'


def two_img(main, main_alt, small, small_alt, stamp=False):
    st = ('<svg class="stamp" viewBox="0 0 120 120" aria-hidden="true"><defs><path id="c" d="M60,60 m-46,0 a46,46 0 1,1 92,0 a46,46 0 1,1 -92,0"/></defs>'
          '<circle cx="60" cy="60" r="58" fill="#f6f4ef"/><text><textPath href="#c">Victoria · Vancouver Island ·</textPath></text>'
          '<path d="M60 40 53 52h4l-6 9h7v6h4v-6h7l-6-9h4z" fill="currentColor"/></svg>') if stamp else ""
    return (f'{st}<div class="img-reveal" style="border-radius:var(--radius)">{img(main, main_alt, "(max-width: 1020px) 100vw, 600px")}</div>'
            f'<div class="float" data-reveal="zoom" data-delay="300">{img(small, small_alt, "300px")}</div>')


# ---------------------------------------------------------------- pages
def build_home():
    slides = [("hero-bouquet-golden-light", "Bride holding a wildflower bouquet in warm evening light"),
              ("couple-walking-hills", "Couple walking hand in hand across golden hills"),
              ("couple-black-sand-beach", "Couple kissing on a moody West Coast beach"),
              ("bride-beach-forest-edge", "Bride in a lace gown on a beach at the forest edge")]
    figs = ""
    for i, (k, a) in enumerate(slides):
        w, h = dims(k)
        if i == 0:
            figs += f'<figure class="active">{img(k, a, eager=True)}</figure>'
        else:
            figs += (f'<figure><img data-src="/assets/img/{k}.webp" src="data:image/gif;base64,R0lGODlhAQABAAAAACw=" '
                     f'width="{w}" height="{h}" alt="{esc(a)}"></figure>')
    dots = "".join(f'<button type="button" aria-label="Show photo {i + 1}"{" class=\"active\"" if i == 0 else ""}></button>' for i in range(len(slides)))
    marquee_words = ["Victoria weddings", "Vancouver Island elopements", "Engagements", "Golden hour", "Forest & sea", "Honest moments"]
    mq = "".join(f"<span>{w}</span>" for w in marquee_words) * 2

    services = [
        ("01", "Weddings", "/weddings", "recessional-petals", "Guests throwing petals as newlyweds walk down the aisle",
         "Full-day storytelling for celebrations across Victoria — from getting ready to the last song."),
        ("02", "Elopements", "/elopements", "bride-pebble-beach-veil", "Bride with a long veil on a pebble beach",
         "Just the two of you (and maybe a few favourites) on a cliff, a beach or deep in the cedars."),
        ("03", "Engagements", "/engagements", "sunset-silhouette", "Couple silhouetted against a sunset",
         "Relaxed couples sessions — coastline walks, castle gardens or cozy at home."),
    ]
    svc_cards = "".join(f'''<a class="svc-card" href="{h}" data-reveal data-delay="{i * 140}">{img(k, a, "(max-width: 680px) 100vw, 400px")}
  <div class="in-card"><span class="num">{n}</span><h3>{t}</h3><p>{d}</p><span class="go">Explore</span></div></a>''' for i, (n, t, h, k, a, d) in enumerate(services))

    strip_imgs = ["confetti-kiss", "bw-veil-kiss", "hands-rings-florals", "veil-embrace-field", "couple-autumn-lake",
                  "peach-bouquet", "long-table-florals", "bikes-sunset", "holding-hands-shadow", "garden-gazebo"]
    alts = {"confetti-kiss": "Newlyweds kissing under confetti", "bw-veil-kiss": "Black and white portrait of a couple kissing under a veil",
            "hands-rings-florals": "Close-up of hands with wedding rings and florals", "veil-embrace-field": "Couple embracing under a veil in a field",
            "couple-autumn-lake": "Couple by a lake in autumn colour", "peach-bouquet": "Bride holding a peach rose bouquet",
            "long-table-florals": "Long reception table with candles and flowers", "bikes-sunset": "Couple on bicycles at sunset",
            "holding-hands-shadow": "Couple holding hands with shadows on the grass", "garden-gazebo": "Garden ceremony gazebo with white chairs"}
    strip = "".join(f'<figure>{img(k, alts[k], "(max-width: 680px) 80vw, 420px")}</figure>' for k in strip_imgs)

    latest = [p for p in POSTS if p["kind"] == "guide"][:2] + [POST_BY_SLUG["kasha-justin"]]
    cards = "".join(post_card(p, i=i) for i, p in enumerate(latest))

    faq = [
        ("Where are you based and where do you travel?", "We're based in Victoria, BC and photograph weddings and elopements across Greater Victoria, Sooke, the Saanich Peninsula, the Cowichan Valley, Nanaimo and Tofino. Ferry trips to the Gulf Islands and Vancouver are easy to arrange, and travel further afield is always welcome."),
        ("How much does wedding photography cost?", "Elopements start at $1,650 and full wedding coverage starts at $2,700 (CAD, plus GST). Our <a href=\"/pricing\">interactive estimator</a> builds a quote from your hours, add-ons and location in about thirty seconds."),
        ("How far ahead should we book?", "Most couples book 9–14 months out for summer Saturdays. Weekday elopements and shoulder-season dates (April, May, October) often have openings on shorter notice — just ask."),
        ("When will we see our photos?", "You'll get a sneak peek within a week and the full, hand-edited online gallery within six to eight weeks, with print rights and a private download link."),
        ("What happens if it rains?", "On the West Coast we plan for it. Clear umbrellas, forest canopies and covered heritage spots make for some of our favourite images — read our <a href=\"/post/rainy-day-wedding-photo-tips\">rainy day wedding photo tips</a>."),
    ]

    body = f'''<section class="hero grain">
  <div class="hero-slides">{figs}</div>
  <div class="wrap">
    <span class="eyebrow light">Victoria, BC · Wedding &amp; Elopement Photographer</span>
    <h1><span class="line"><span>Victoria <em>wedding</em></span></span> <span class="line"><span>photography for</span></span> <span class="line"><span>wild hearts.</span></span></h1>
    <div class="hero-meta">
      <div><p class="lead">Evergrey Photography is a Victoria wedding photographer for couples who would rather feel their day than pose through it — weddings, elopements and engagements across Vancouver Island.</p>
      <div class="btn-row"><a class="btn light" href="/contact">Check your date {ARROW}</a><a class="btn ghost-light" href="/portfolio">View portfolio</a></div></div>
      <div class="hero-dots">{dots}</div>
    </div>
  </div>
  <span class="scroll-cue">Scroll</span>
</section>

<div class="marquee" aria-hidden="true"><div class="marquee-track">{mq}</div></div>

<section class="section">
  <div class="wrap">
    {split(two_img("hands-bouquet-watch", "Groom's hand resting on the bride's hand and bouquet", "gold-rings", "Two gold wedding bands", stamp=True),
           '''<span class="eyebrow" data-reveal>Victoria wedding photography</span>
    <h2 data-reveal>Photographs that feel like <em>being there</em> again</h2>
    <p class="lead" data-reveal>Fog rolling off the Strait of Juan de Fuca. Rain-dark cedars in Goldstream. That last orange sliver of sun over Dallas Road. Vancouver Island weddings have a mood all of their own, and we love leaning into it.</p>
    <p data-reveal>Our approach to Victoria wedding photography is mostly documentary: we watch for the glances, the belly laughs and the quiet hands-held moments, then step in with gentle direction when the light is too good to waste. The result is a gallery that looks like your day, not a template.</p>
    <p data-reveal>When couples search for the best wedding photographers in Victoria, BC, they're usually looking for three things — someone calm, someone who knows the local light, and someone whose pricing is clear from the start. That's exactly how we work.</p>
    <div class="btn-row" data-reveal><a class="btn" href="/about">Meet the studio <span class="arr" aria-hidden="true">→</span></a></div>''')}
  </div>
</section>

<section class="section bg-mist">
  <div class="wrap">
    <div class="strip-head"><div><span class="eyebrow" data-reveal>What we photograph</span><h2 data-reveal style="margin:0">Weddings, elopements <em>&amp;</em> love stories</h2></div>
    <a class="text-link" href="/pricing" data-reveal>Pricing &amp; packages</a></div>
    <div class="grid-3">{svc_cards}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="center" style="margin-bottom:60px"><span class="eyebrow" data-reveal>How we work</span><h2 data-reveal>Calm, unhurried, <em>light-obsessed</em></h2></div>
    <div class="features">
      <div class="feature" data-reveal><div class="ico">{icon("heart")}</div><h3>Documentary first</h3><p>Most of your gallery happens without a single instruction. We blend in, read the room and catch what's real.</p></div>
      <div class="feature" data-reveal data-delay="120"><div class="ico">{icon("sun")}</div><h3>Planned around the sun</h3><p>We build your timeline around golden hour and the tide tables, so portraits happen in the best light of the day.</p></div>
      <div class="feature" data-reveal data-delay="240"><div class="ico">{icon("leaf")}</div><h3>True-to-life colour</h3><p>Soft, filmic edits that keep skin tones honest and greens deep — photos that won't feel dated in ten years.</p></div>
    </div>
  </div>
</section>

<section class="band grain">
  <div class="bg" data-parallax="0.18">{img("misty-forest", "Mist drifting through a West Coast forest")}</div>
  <div class="wrap"><blockquote data-reveal>“Nothing fancy, just love.”<cite>Kasha, on her rainy <a href="/post/kasha-justin" style="color:inherit">Aylard Farm elopement</a></cite></blockquote></div>
</section>

<section class="section" style="padding-bottom:60px">
  <div class="wrap"><div class="strip-head"><div><span class="eyebrow" data-reveal>Recent frames</span><h2 data-reveal style="margin:0">Drag to wander <em>through</em></h2></div><a class="text-link" href="/portfolio" data-reveal>Full portfolio</a></div></div>
  <div class="strip" aria-label="Recent wedding photographs">{strip}</div>
</section>

<section class="section bg-mist">
  <div class="wrap">
    {split('''<div class="compare" data-reveal="zoom" style="--pos:50%">''' + img("couple-dried-bouquet", "Couple laughing with a dried flower bouquet — our final edit", "(max-width: 1020px) 100vw, 640px") +
           img("couple-dried-bouquet", "The same photograph straight out of camera", "(max-width: 1020px) 100vw, 640px", cls="raw") +
           '''<span class="handle"></span><span class="lbl l">Straight from camera</span><span class="lbl r">Evergrey edit</span>
      <input type="range" min="0" max="100" value="50" aria-label="Compare unedited and edited photo"></div>''',
           f'''<span class="eyebrow" data-reveal>Our edit</span><h2 data-reveal>Every image, <em>hand-finished</em></h2>
    <p class="lead" data-reveal>Slide across to see what happens between the camera and your gallery.</p>
    <p data-reveal>We don't batch-apply a trendy preset and call it done. Each photograph is colour-balanced by hand for warm, natural skin, rich West Coast greens and soft highlights — so a rainy forest and a sunny garden still look like they belong in the same story.</p>
    <ul data-reveal style="padding-left:1.2em"><li>Sneak peek within 7 days</li><li>Full gallery in 6–8 weeks</li><li>Private online gallery with print release</li></ul>''', flip=True)}
  </div>
</section>

<section class="section bg-ink on-dark grain">
  <div class="wrap">
    <div style="margin-bottom:60px"><span class="eyebrow" data-reveal>The experience</span><h2 data-reveal>From first hello to <em>heirloom</em></h2></div>
    <div class="steps">
      <div class="step" data-reveal><h3>Say hello</h3><p>Tell us your date, place and plans. We'll reply within two business days with availability and ideas.</p></div>
      <div class="step" data-reveal data-delay="120"><h3>Plan together</h3><p>A video call, a timeline built around the light, location scouting and a shot list for family photos.</p></div>
      <div class="step" data-reveal data-delay="240"><h3>Celebrate</h3><p>We show up early, stay calm and quietly handle the logistics so you can be present.</p></div>
      <div class="step" data-reveal data-delay="360"><h3>Relive it</h3><p>Your hand-edited gallery arrives in six to eight weeks, ready to share, print and keep forever.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="strip-head"><div><span class="eyebrow" data-reveal>Free planning tools</span><h2 data-reveal style="margin:0">Plan around the <em>light</em></h2></div><a class="text-link" href="/tools" data-reveal>All tools</a></div>
    <div class="grid-3">
      <a class="price-card" href="/tools/golden-hour-calculator" style="text-decoration:none" data-reveal><div class="ico" style="width:46px;height:46px;border-radius:50%;display:grid;place-items:center;background:var(--sand-2)">{icon("sun")}</div><h3 style="margin-top:20px">Golden hour calculator</h3><p>Exact sunrise, sunset, golden and blue hour for Victoria-area locations on any date.</p><span class="text-link" style="margin-top:auto">Open tool</span></a>
      <a class="price-card featured" href="/tools/wedding-timeline-planner" style="text-decoration:none" data-reveal data-delay="120"><div class="ico" style="width:46px;height:46px;border-radius:50%;display:grid;place-items:center;background:rgba(255,255,255,.12)">{icon("clock")}</div><h3 style="margin-top:20px">Wedding timeline planner</h3><p>Enter your ceremony time and get a photo-friendly schedule that lands portraits in golden hour.</p><span class="text-link" style="margin-top:auto">Open tool</span></a>
      <a class="price-card" href="/tools/elopement-location-finder" style="text-decoration:none" data-reveal data-delay="240"><div class="ico" style="width:46px;height:46px;border-radius:50%;display:grid;place-items:center;background:var(--sand-2)">{icon("compass")}</div><h3 style="margin-top:20px">Elopement location finder</h3><p>Four quick questions to match you with Vancouver Island elopement spots that fit your style.</p><span class="text-link" style="margin-top:auto">Take the quiz</span></a>
    </div>
  </div>
</section>

<section class="section bg-mist">
  <div class="wrap">
    <div class="strip-head"><div><span class="eyebrow" data-reveal>The Journal</span><h2 data-reveal style="margin:0">Stories &amp; <em>planning guides</em></h2></div><a class="text-link" href="/blog" data-reveal>Read the journal</a></div>
    <div class="post-grid">{cards}</div>
  </div>
</section>

<section class="section">
  <div class="wrap narrow">{faq_html(faq)}</div>
</section>
{cta()}'''
    page("", "Victoria Wedding Photography | Evergrey Photography — Victoria, BC",
         "Evergrey Photography: Victoria wedding photography, Vancouver Island elopements and engagement sessions with natural, light-filled storytelling. Check your date.",
         body, full_title=True, priority="1.0", schema=[faq_schema(faq), {"@type": "WebPage", "@id": url("") + "#webpage", "url": url(""), "name": "Victoria Wedding Photography", "about": {"@id": C.SITE + "/#business"}}])


def build_about():
    vals = [
        ("Presence over perfection", "We'd rather catch your dad wiping his eyes than spend twenty minutes perfecting a pose."),
        ("Clear, kind communication", "Fast replies, written timelines, no surprises in the contract or the final invoice."),
        ("Leave it better", "We follow Leave No Trace on every beach and trail, and we always ask about permits before we shoot."),
        ("Small on purpose", "We take a limited number of weddings each year so every gallery gets our full attention."),
    ]
    v = "".join(f'<div class="feature" data-reveal data-delay="{i * 100}"><div class="ico">{icon(["heart", "clock", "leaf", "camera"][i])}</div><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(vals))
    body = page_hero("About Evergrey Photography", "A small Victoria, BC photography studio for couples who love wild coastlines, moody skies and honest, unposed moments.",
                     "photographer-city", "Photographer holding a camera at dusk", [("Home", ""), ("About", "about")]) + f'''
<section class="section">
  <div class="wrap">
    {split(two_img("camera-flatlay", "Camera and lenses on a dark table", "airy-hands", "Delicate hands holding florals", stamp=True),
           '''<span class="eyebrow" data-reveal>Our story</span><h2 data-reveal>Why <em>Evergrey?</em></h2>
    <p class="lead" data-reveal>Because on Vancouver Island the forests stay ever-green and the skies are often grey — and both are beautiful.</p>
    <p data-reveal>Evergrey Photography began with a simple idea: West Coast weddings don't need to look like a sunny California magazine spread. The soft overcast light, the fog that hangs in the Douglas-firs, the cold green ocean — that's the real backdrop of a Victoria wedding, and it's flattering, cinematic and completely yours.</p>
    <p data-reveal>So we photograph what's actually there. We plan around the sun and the tides, we pack the clear umbrellas, and we let the day unfold in front of the camera instead of directing it from behind. Couples tell us their galleries feel like stepping back into the day, and that's the whole point.</p>''')}
  </div>
</section>
<section class="section bg-mist">
  <div class="wrap">
    <div class="center" style="margin-bottom:56px"><span class="eyebrow" data-reveal>What we believe</span><h2 data-reveal>Four promises to <em>every couple</em></h2></div>
    <div class="features" style="grid-template-columns:repeat(2,1fr)">{v}</div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    {split(f'<div class="img-reveal" style="border-radius:var(--radius)">{img("bride-pebble-beach-veil", "Bride with a cathedral veil blowing on a pebble beach", "(max-width: 1020px) 100vw, 600px")}</div>',
           '''<span class="eyebrow" data-reveal>Where we work</span><h2 data-reveal>Home base: <em>Victoria, BC</em></h2>
    <p data-reveal>We photograph weddings in Victoria, Oak Bay, Saanich, Esquimalt and the West Shore, elopements along the Juan de Fuca coast from East Sooke to Botanical Beach, vineyard celebrations in the Cowichan Valley, and surf-town weekends in Tofino and Ucluelet. Ferries to the Gulf Islands and the mainland are part of the adventure.</p>
    <p data-reveal>Some favourite places we keep coming back to: the meadow and coves at <a href="/post/aylard-farm-east-sooke-wedding-photos">Aylard Farm in East Sooke</a>, the gardens of <a href="/post/hatley-castle-engagement-photos">Hatley Castle</a>, and the driftwood beaches along Dallas Road.</p>
    <div class="btn-row" data-reveal><a class="btn" href="/portfolio">See the work <span class="arr" aria-hidden="true">→</span></a><a class="btn ghost" href="/contact">Say hello</a></div>''', flip=True)}
  </div>
</section>
<section class="band grain">
  <div class="bg" data-parallax="0.18">{img("foggy-evergreens", "Evergreen forest disappearing into fog")}</div>
  <div class="wrap"><blockquote data-reveal>Ever-green forests. Ever-grey skies. <em>Always</em> worth photographing.</blockquote></div>
</section>
{cta()}'''
    page("about", "About Evergrey Photography — Victoria, BC Wedding Photographer",
         "Meet Evergrey Photography, a Victoria, BC wedding and elopement photographer who loves West Coast light, misty forests and honest, unposed moments.",
         body, active="/about", full_title=True, og_image="photographer-city",
         schema=[breadcrumbs([("Home", ""), ("About", "about")]), {"@type": "AboutPage", "url": url("about"), "name": "About Evergrey Photography"}])


def service_page(route, h1, title, desc, hero, hero_alt, lead, intro_h2, intro, incl, gallery, faq, extra="", from_price=None, eyebrow=""):
    inc = "".join(f'<li>{x}</li>' for x in incl)
    gal = "".join(f'<figure>{img(k, a, "(max-width: 680px) 80vw, 420px")}</figure>' for k, a in gallery)
    body = page_hero(h1, lead, hero, hero_alt, [("Home", ""), (h1.replace("<em>", "").replace("</em>", ""), route)], eyebrow=eyebrow) + f'''
<section class="section">
  <div class="wrap">
    {split(two_img(gallery[0][0], gallery[0][1], gallery[1][0], gallery[1][1], stamp=True), f'<span class="eyebrow" data-reveal>{eyebrow or "Overview"}</span><h2 data-reveal>{intro_h2}</h2>{intro}')}
  </div>
</section>
<section class="section bg-ink on-dark grain">
  <div class="wrap">
    <div class="split"><div><span class="eyebrow" data-reveal>What's included</span><h2 data-reveal>Everything you need, <em>nothing</em> you don't</h2>
    <p data-reveal style="color:rgba(233,236,230,.78)">{"Coverage starts from $" + format(from_price, ",") + " CAD. " if from_price else ""}Build an exact estimate with our pricing tool — hours, add-ons, travel and GST included.</p>
    <div class="btn-row" data-reveal><a class="btn light" href="/pricing">Estimate your price {ARROW}</a></div></div>
    <ul class="price-card featured" style="margin:0;background:transparent;border-color:var(--line-light)" data-reveal>{inc}</ul></div>
  </div>
</section>
{extra}
<section class="section" style="padding-bottom:60px">
  <div class="wrap"><div class="strip-head"><div><span class="eyebrow" data-reveal>From the archive</span><h2 data-reveal style="margin:0">A few <em>favourites</em></h2></div><a class="text-link" href="/portfolio" data-reveal>Full portfolio</a></div></div>
  <div class="strip">{gal}</div>
</section>
<section class="section bg-mist"><div class="wrap narrow">{faq_html(faq)}</div></section>
{cta()}'''
    plain_h1 = re.sub("<[^>]+>", "", h1)
    page(route, title, desc, body, active="/" + route, full_title=True, og_image=hero, priority="0.9",
         schema=[breadcrumbs([("Home", ""), (plain_h1, route)]), service_schema(plain_h1, desc, route, from_price), faq_schema(faq)])


def build_services():
    service_page(
        "weddings", "Wedding Photographer in <em>Victoria, BC</em>", "Wedding Photographer Victoria BC — Full-Day Coverage | Evergrey",
        "Wedding photographer in Victoria, BC with a calm, documentary approach. Full-day coverage across Greater Victoria and Vancouver Island from $2,700 CAD.",
        "recessional-petals", "Guests throwing petals as a newly married couple walks back up the aisle",
        "Full-day, story-driven coverage for weddings across Greater Victoria and Vancouver Island — from the first buttonhole to the last dance.",
        "A Victoria wedding photographer who <em>knows the light</em>",
        '''<p class="lead" data-reveal>Your wedding day moves fast. Our job is to slow it down in the photographs.</p>
<p data-reveal>Victoria wedding photography comes with its own beautiful challenges: bright marine overcast that turns harsh at noon, sunsets past 9 p.m. in June, and garden venues that glow for exactly twenty minutes before the sun dips behind the Sooke Hills. We plan for all of it. Before your day we build a photo-friendly timeline, scout your venue's light, and write a family photo list so formals take minutes, not an hour.</p>
<p data-reveal>On the day, expect us to blend in: no shouting poses across the lawn, no flash in your officiant's face. We'll quietly gather the details, document the ceremony from discreet angles, and steal you away for portraits when the light turns golden. Whether you're celebrating at a castle in Colwood, a vineyard in the Cowichan Valley or a backyard in Oak Bay, the gallery will feel like your day.</p>
<p data-reveal>Still choosing a place? Our guide to <a href="/post/best-wedding-venues-victoria-bc">the best wedding venues in Victoria, BC</a> covers our favourites and how each one photographs.</p>''',
        ["4 to 12 hours of continuous coverage", "Pre-wedding planning call &amp; custom photo timeline", "Family formals shot list and coordination",
         "Hand-edited, high-resolution gallery (typically 70–100 images per hour)", "Sneak peek within 7 days", "Private online gallery with print release",
         "Optional second photographer, engagement session &amp; heirloom album"],
        [("confetti-kiss", "Newlyweds kissing as guests throw confetti"), ("long-table-florals", "Reception table with florals and candles"),
         ("ceremony-aisle", "Outdoor ceremony aisle lined with florals"), ("hands-rings-florals", "Hands with wedding rings resting on a bouquet"),
         ("garden-reception-table", "Garden reception table with blue linens"), ("bw-veil-kiss", "Black and white veil kiss"),
         ("garden-gazebo", "Garden gazebo set for a ceremony"), ("mr-mrs-sign", "Wooden Mr and Mrs sign in the trees")],
        [("How many hours of wedding photography do we need?", "Most full weddings in Victoria are best covered with 8 hours: getting ready, ceremony, portraits, and the first part of the reception. Smaller celebrations often need 5–6. Try our <a href=\"/tools/wedding-timeline-planner\">wedding timeline planner</a> to see what your day needs."),
         ("Do you offer a second photographer?", "Yes — a second photographer is $95 per hour and is most helpful for weddings over 100 guests, or when both partners are getting ready in different places."),
         ("Can you recommend vendors and venues?", "Absolutely. After years of Vancouver Island weddings we're happy to point you to planners, florists and venues that suit your style and budget."),
         ("Is a deposit required?", "A 30% retainer and signed agreement reserve your date. The balance is due a month before the wedding."),
         ("Do you photograph same-sex and non-traditional weddings?", "Always, and joyfully. Every couple and every kind of celebration is welcome here.")],
        from_price=2700, eyebrow="Weddings")
    service_page(
        "elopements", "Vancouver Island <em>Elopement</em> Photography", "Vancouver Island Elopement Photographer | Evergrey Photography",
        "Vancouver Island elopement photography from Victoria to Tofino. Help with locations, permits and timing for intimate, adventurous ceremonies. From $1,650.",
        "couple-black-sand-beach", "Couple embracing on a dark-sand beach below sea stacks",
        "Intimate ceremonies on cliffs, beaches and forest trails — with help on locations, permits, timing and the marriage licence.",
        "Elope somewhere that <em>takes your breath away</em>",
        '''<p class="lead" data-reveal>An elopement isn't a smaller wedding. It's a different kind of day — built entirely around the two of you.</p>
<p data-reveal>Vancouver Island is made for eloping. Within an hour of Victoria you can say your vows in a meadow above the ocean at <a href="/post/aylard-farm-east-sooke-wedding-photos">Aylard Farm</a>, under old-growth cedars at Goldstream, or on a pebble beach along the Juan de Fuca coast. Head up-island and there's Cathedral Grove, the Cowichan vineyards and the wide surf beaches of Tofino.</p>
<p data-reveal>We help plan the whole thing: shortlisting locations with our <a href="/tools/elopement-location-finder">elopement location finder</a>, timing your ceremony to the tide and the light with the <a href="/tools/golden-hour-calculator">golden hour calculator</a>, checking park permit requirements, and walking you through the BC marriage licence. Our <a href="/post/vancouver-island-elopement-guide">Vancouver Island elopement guide</a> covers it step by step.</p>
<p data-reveal>Rain isn't a deal-breaker — just ask <a href="/post/kasha-justin">Kasha and Justin</a>, whose clouds parted the moment their ceremony began.</p>''',
        ["2-hour, 4-hour and micro-wedding options", "Location scouting and a custom route for the day", "Help with permits and the BC marriage licence process",
         "Officiant and vendor recommendations", "Can act as one of your two witnesses", "Hand-edited online gallery with print release", "Sneak peek within 7 days"],
        [("bride-pebble-beach-veil", "Bride with a cathedral-length veil on a beach"), ("couple-walking-hills", "Couple walking through golden grassland"),
         ("bride-beach-forest-edge", "Bride on the sand at the edge of a forest"), ("veil-embrace-field", "Couple wrapped in a veil in a field"),
         ("forest-path", "Sunlit forest trail"), ("ocean-sunset-rocks", "Rocky shoreline at sunset"), ("couple-black-sand-beach", "Couple kissing on a beach")],
        [("Is eloping legal anywhere in BC?", "You need a valid BC marriage licence, a licensed marriage commissioner or religious representative, and two witnesses. The ceremony can happen almost anywhere you have permission to be — check park rules before you choose."),
         ("Do we need a permit to elope in a park?", "It depends on the park and the size of your group. CRD Regional Parks, BC Parks and Parks Canada each have their own rules for ceremonies and commercial photography, so we confirm requirements for your spot as part of planning."),
         ("What's the best time of year to elope on Vancouver Island?", "Late spring through early autumn has the most reliable weather, but October and winter storm-watching season bring incredible moody light and far fewer people."),
         ("Can we bring guests?", "Of course. Our micro-wedding option covers up to 30 guests; many couples invite just immediate family or a couple of close friends.")],
        from_price=1650, eyebrow="Elopements")
    service_page(
        "engagements", "Engagement &amp; <em>Couples</em> Photography", "Engagement Photographer Victoria BC | Evergrey Photography",
        "Relaxed engagement and couples photography in Victoria, BC — beaches, castle gardens, forests or cozy in-home sessions. Sessions from $450 CAD.",
        "sunset-silhouette", "Couple silhouetted against an orange sunset sky",
        "Relaxed sessions for engaged couples, anniversaries and just-because — on the coast, in the forest, or cozy at home.",
        "A session that feels like <em>a date</em>, not a photoshoot",
        '''<p class="lead" data-reveal>Most couples tell us they're “awkward in photos.” Give us ten minutes.</p>
<p data-reveal>An engagement session is the easiest way to get comfortable in front of the camera before your wedding — and to come away with photos you'll actually want on the wall. We'll walk, talk, play a few silly prompts and chase the good light. You won't be asked to hold a stiff pose for long.</p>
<p data-reveal>Favourite spots include the driftwood along Dallas Road, the gardens of <a href="/post/hatley-castle-engagement-photos">Hatley Castle</a>, and the ferns of Goldstream — see our list of the <a href="/post/best-engagement-photo-locations-victoria-bc">best engagement photo locations in Victoria, BC</a>. Prefer something intimate? An <a href="/post/in-home-couple-session">in-home couple session</a> with coffee, records and your dog on the sofa is one of our very favourite things to photograph.</p>
<p data-reveal>Not sure what to wear? Our <a href="/post/what-to-wear-for-engagement-photos">engagement outfit guide</a> has palettes for forest, beach and city settings.</p>''',
        ["60–90 minute session at one or two nearby locations", "Location and outfit guidance", "Golden-hour scheduling",
         "50+ hand-edited images in a private online gallery", "Print release", "$450 when added to a wedding package, $550 on its own"],
        [("couple-autumn-lake", "Couple by a lake surrounded by autumn colour"), ("sunset-silhouette", "Couple silhouetted at sunset"),
         ("couple-dried-bouquet", "Couple laughing together with dried flowers"), ("bikes-sunset", "Couple on bikes at sunset"),
         ("city-lights-candles", "Couple sitting among candles above city lights"), ("holding-hands-shadow", "Couple holding hands on grass"), ("heart-bokeh", "Heart-shaped bokeh lights")],
        [("When should we book our engagement session?", "Anywhere from a year to two months before the wedding. If you want the photos for save-the-dates, plan a session at least four months out."),
         ("What if it rains?", "We'll reschedule if you'd like, or lean in with umbrellas and a forest location. Some of our favourite sessions happened in drizzle."),
         ("Can we bring our dog?", "Yes please. Bring a helper to take them home partway through if you'd like a few photos of just the two of you."),
         ("Do you photograph anniversaries and proposals?", "Yes — the same session works beautifully for anniversaries, and we're happy to help plan a surprise proposal.")],
        from_price=450, eyebrow="Engagements")


GALLERY = [
    ("confetti-kiss", "weddings", "Confetti kiss after the ceremony"), ("bride-pebble-beach-veil", "elopements", "Veil caught by the sea breeze"),
    ("couple-autumn-lake", "couples", "Autumn by the lake"), ("hands-rings-florals", "details", "Rings and florals"),
    ("veil-embrace-field", "elopements", "Wrapped in the veil"), ("recessional-petals", "weddings", "Petal recessional"),
    ("sunset-silhouette", "couples", "Sunset silhouette"), ("peach-bouquet", "details", "Peach garden roses"),
    ("couple-black-sand-beach", "elopements", "Storm-watching vows"), ("bw-veil-kiss", "weddings", "Black and white kiss"),
    ("city-lights-candles", "couples", "Candles above the city"), ("rings-on-peonies", "details", "Rings on peonies"),
    ("couple-walking-hills", "elopements", "Into the hills"), ("long-table-florals", "weddings", "Long-table dinner"),
    ("couple-dried-bouquet", "couples", "Laughter and dried florals"), ("arch-florals", "details", "Ceremony arch"),
    ("bride-beach-forest-edge", "elopements", "Where the forest meets the sand"), ("garden-gazebo", "weddings", "Garden ceremony"),
    ("bikes-sunset", "couples", "Riding into golden hour"), ("gold-rings", "details", "Gold bands"),
    ("hero-bouquet-golden-light", "weddings", "Bouquet in the last light"), ("holding-hands-shadow", "couples", "Long shadows"),
    ("bouquet-brick-wall", "details", "Bouquet against brick"), ("ceremony-aisle", "weddings", "The aisle"),
]


def build_portfolio():
    chips = "".join(f'<button class="chip{" active" if f == "all" else ""}" type="button" data-filter="{f}" aria-pressed="{"true" if f == "all" else "false"}">{t}</button>'
                    for f, t in [("all", "All"), ("weddings", "Weddings"), ("elopements", "Elopements"), ("couples", "Couples"), ("details", "Details")])
    items = "".join(f'<button type="button" class="g-item" data-cat="{c}" data-cap="{esc(cap)}" data-full="/assets/img/{k}.webp" data-reveal data-delay="{(i % 3) * 80}">{img(k, cap, "(max-width: 680px) 50vw, 400px")}</button>'
                    for i, (k, c, cap) in enumerate(GALLERY))
    body = page_hero("Wedding &amp; Elopement <em>Portfolio</em>", "A collection of weddings, elopements, couples sessions and the small details in between — photographed across Victoria and Vancouver Island.",
                     "veil-embrace-field", "Couple embracing beneath a flowing veil", [("Home", ""), ("Portfolio", "portfolio")], cls="short") + f'''
<section class="section">
  <div class="wrap">
    <div class="chips" data-filter-group="#masonry" role="group" aria-label="Filter portfolio">{chips}</div>
    <div class="masonry" id="masonry">{items}</div>
  </div>
</section>
<div class="lightbox" role="dialog" aria-modal="true" aria-label="Photo viewer" aria-hidden="true">
  <button class="lb-close" type="button" aria-label="Close">✕</button><button class="lb-prev" type="button" aria-label="Previous photo">←</button><button class="lb-next" type="button" aria-label="Next photo">→</button>
  <figure style="margin:0"><img src="data:image/gif;base64,R0lGODlhAQABAAAAACw=" alt=""><figcaption></figcaption></figure>
</div>
{cta("Picture <em>yourselves</em> here?")}'''
    page("portfolio", "Wedding Photography Portfolio — Victoria & Vancouver Island", "Browse the Evergrey Photography portfolio: Victoria weddings, Vancouver Island elopements, engagement sessions and wedding details. Filter by style and tap to view.",
         body, active="/portfolio", og_image="veil-embrace-field",
         schema=[breadcrumbs([("Home", ""), ("Portfolio", "portfolio")]),
                 {"@type": "ImageGallery", "name": "Evergrey Photography portfolio", "url": url("portfolio"),
                  "image": [C.SITE + f"/assets/img/{k}.webp" for k, _, _ in GALLERY[:12]]}])


def build_pricing():
    P = C.PRICING
    eopts = "".join(f'<label class="toggle"><span class="t-l"><b>{v["label"]}</b></span><span class="t-p">${v["price"]:,}</span><input type="radio" name="elope" value="{k}"{" checked" if i == 0 else ""}></label>'
                    for i, (k, v) in enumerate(P["elopement"].items()))
    addons = "".join(f'<label class="toggle"{" data-only=\"wedding\"" if k == "rehearsal" else ""}><span class="t-l"><b>{v["label"]}</b><small>{"$" + str(v["price"]) + " per hour of coverage" if v.get("perHour") else ""}</small></span><span class="t-p">{"" if v.get("perHour") else "$" + format(v["price"], ",")}</span><input type="checkbox" data-addon="{k}"></label>'
                     for k, v in P["addons"].items())
    travel = "".join(f'<option value="{k}">{v["label"]}{" — +$" + str(v["price"]) if v["price"] else " — included"}</option>' for k, v in P["travel"].items())
    faq = [
        ("Are you an affordable photographer in Victoria, BC?", "We aim to be clear rather than cheap: elopements from $1,650 and weddings from $2,700, with no hidden fees. Weekday and off-season dates, shorter coverage and skipping the album are all easy ways to bring the total down. Our guide to <a href=\"/post/wedding-photographer-cost-victoria-bc\">wedding photographer cost in Victoria, BC</a> explains what drives pricing."),
        ("Do your prices include GST?", "Listed prices are in Canadian dollars before 5% GST. The estimator adds GST so you can see the full number."),
        ("Do you offer payment plans?", "Yes. After the 30% retainer, you can split the balance into monthly payments, as long as it's paid off a month before your date."),
        ("Is travel included?", "Travel anywhere in Greater Victoria, the Saanich Peninsula and the West Shore is included. Further afield we add a flat travel fee, shown in the estimator."),
        ("Can we customise a package?", "Every package can be adjusted. Use the estimator as a starting point and tell us what you have in mind."),
    ]
    data = json.dumps(P)
    body = page_hero("Wedding Photography <em>Pricing</em>", "Clear, all-in pricing for Victoria weddings, Vancouver Island elopements and couples sessions — plus an instant estimator.",
                     "gold-rings", "Two gold wedding rings", [("Home", ""), ("Pricing", "pricing")], cls="short") + f'''
<section class="section">
  <div class="wrap">
    <div class="center" style="margin-bottom:56px"><span class="eyebrow" data-reveal>Collections</span><h2 data-reveal>Honest pricing, <em>no guesswork</em></h2>
    <p class="lead" data-reveal>Looking for an affordable photographer in Victoria, BC who doesn't cut corners? Every collection includes planning help, a hand-edited gallery and a print release. Prices in CAD, before GST.</p></div>
    <div class="price-cards">
      <div class="price-card" data-reveal><span class="tag">Elopements</span><div class="amt">$1,650 <small>from</small></div><p>Two to five hours for intimate ceremonies anywhere on the island.</p>
        <ul><li>2-hour, 4-hour or micro-wedding</li><li>Location &amp; permit guidance</li><li>Sneak peek in 7 days</li><li>Online gallery &amp; print release</li></ul><a class="btn ghost" href="/elopements">Elopements {ARROW}</a></div>
      <div class="price-card featured" data-reveal data-delay="120"><span class="tag">Most chosen · Weddings</span><div class="amt">$3,700 <small>8 hours</small></div><p>Full-day storytelling from getting ready to the dance floor. From $2,700 for 4 hours.</p>
        <ul><li>Planning call &amp; custom timeline</li><li>Family formals coordination</li><li>Golden-hour portraits</li><li>Full gallery in 6–8 weeks</li></ul><a class="btn light" href="/weddings">Weddings {ARROW}</a></div>
      <div class="price-card" data-reveal data-delay="240"><span class="tag">Engagements &amp; couples</span><div class="amt">$550 <small>session</small></div><p>60–90 minutes on the coast, in the forest or at home. $450 with a wedding collection.</p>
        <ul><li>One or two locations</li><li>Outfit &amp; location guide</li><li>50+ edited images</li><li>Print release</li></ul><a class="btn ghost" href="/engagements">Couples {ARROW}</a></div>
    </div>
  </div>
</section>
<section class="section bg-mist" id="estimate">
  <div class="wrap">
    <div style="margin-bottom:44px"><span class="eyebrow" data-reveal>Instant estimate</span><h2 data-reveal>Build your <em>collection</em></h2><p class="lead" data-reveal>Pick your coverage, add what you love, choose a location. The total updates as you go.</p></div>
    <div class="calc-layout" id="estimator">
      <div class="panel">
        <div class="field"><span class="lab">Type of day</span><div class="seg" role="group" aria-label="Type of day"><button type="button" class="active" data-mode="wedding" aria-pressed="true">Wedding</button><button type="button" data-mode="elopement" aria-pressed="false">Elopement</button></div></div>
        <div class="field" id="est-wedding"><label for="est-hours">Hours of coverage</label><div class="range-row"><input type="range" id="est-hours" min="4" max="12" step="1" value="8"><span class="range-val" id="est-hours-val">8 h</span></div></div>
        <div class="field" id="est-elope" hidden><span class="lab">Elopement collection</span><div class="toggles">{eopts}</div></div>
        <div class="field"><span class="lab">Add-ons</span><div class="toggles">{addons}</div></div>
        <div class="field"><label for="est-travel">Location</label><select id="est-travel">{travel}</select></div>
      </div>
      <aside class="total-box grain" aria-live="polite"><span class="eyebrow light">Your estimate</span><div class="big" id="est-total">$0</div><small>CAD, including 5% GST</small>
        <ul class="lines" id="est-lines"></ul><a class="btn light" id="est-cta" href="/contact">Send this to us {ARROW}</a>
        <p style="margin:18px 0 0;font-size:.82rem;color:var(--sage)">An estimate, not a quote — we'll confirm the details with you.</p></aside>
    </div>
  </div>
</section>
<section class="section"><div class="wrap narrow">{faq_html(faq, "Pricing questions")}</div></section>
{cta()}'''
    page("pricing", "Wedding Photography Pricing — Affordable Photographer Victoria BC",
         "Transparent wedding and elopement photography pricing in Victoria, BC. Elopements from $1,650, weddings from $2,700. Use the instant estimator to price your day.",
         body, active="/pricing", og_image="gold-rings", full_title=False,
         scripts=f'<script>window.EG_PRICING={data};</script>\n<script src="/assets/js/tools.js?v={VER}" defer></script>\n',
         schema=[breadcrumbs([("Home", ""), ("Pricing", "pricing")]), faq_schema(faq),
                 {"@type": "OfferCatalog", "name": "Photography collections", "itemListElement": [
                     {"@type": "Offer", "name": "Elopement photography", "price": "1650", "priceCurrency": "CAD"},
                     {"@type": "Offer", "name": "Wedding photography (4 hours)", "price": "2700", "priceCurrency": "CAD"},
                     {"@type": "Offer", "name": "Wedding photography (8 hours)", "price": "3700", "priceCurrency": "CAD"},
                     {"@type": "Offer", "name": "Engagement session", "price": "550", "priceCurrency": "CAD"}]}])


def build_contact():
    body = page_hero("Check your <em>date</em>", "Tell us about your plans — big wedding, tiny elopement or somewhere in between. We reply within two business days.",
                     "lake-dock", "Wooden dock on a calm lake at dawn", [("Home", ""), ("Contact", "contact")], cls="short") + f'''
<section class="section">
  <div class="wrap">
    <div class="calc-layout">
      <form class="panel" id="inquiry-form" action="/contact.php" method="post" novalidate>
        <div class="form-grid">
          <div class="field"><label for="f-name">Your name *</label><input id="f-name" name="name" required autocomplete="name"></div>
          <div class="field"><label for="f-partner">Partner's name</label><input id="f-partner" name="partner" autocomplete="off"></div>
          <div class="field"><label for="f-email">Email *</label><input id="f-email" name="email" type="email" required autocomplete="email"></div>
          <div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
          <div class="field"><label for="f-type">What are you planning?</label><select id="f-type" name="type"><option value="wedding">Wedding</option><option value="elopement">Elopement</option><option value="micro-wedding">Micro-wedding</option><option value="engagement">Engagement / couples session</option><option value="other">Something else</option></select></div>
          <div class="field"><label for="f-date">Date (or season)</label><input id="f-date" name="date" placeholder="e.g. 2027-06-12 or “fall 2027”"></div>
          <div class="field full"><label for="f-loc">Venue or location</label><input id="f-loc" name="location" placeholder="e.g. Hatley Castle, East Sooke, still deciding"></div>
          <div class="field full"><label for="f-msg">Tell us about your day *</label><textarea id="f-msg" name="message" required placeholder="Guest count, what matters most, the kind of photos you love…"></textarea></div>
          <div class="field full"><label for="f-heard">How did you find us?</label><input id="f-heard" name="heard"></div>
        </div>
        <div class="hp" aria-hidden="true"><label>Website <input name="website" tabindex="-1" autocomplete="off"></label></div>
        <input type="hidden" name="ts" value="">
        <button class="btn" type="submit">Send inquiry {ARROW}</button>
        <p class="form-status" role="status" aria-live="polite"></p>
      </form>
      <aside class="aside" style="position:static">
        <div class="box dark grain" style="position:relative"><h4>Prefer email?</h4><p>Write to us any time at<br><a href="mailto:{C.EMAIL}" style="color:var(--sand-2)">{C.EMAIL}</a></p><p style="margin:0;color:var(--sage);font-size:.9rem">Based in Victoria, BC · photographing all of Vancouver Island</p></div>
        <div class="box"><h4>What happens next</h4><ol style="padding-left:1.2em;margin:0;font-size:.95rem"><li>We check your date and reply within two business days.</li><li>We set up a relaxed video call to hear your plans.</li><li>If it feels right, a simple agreement and retainer reserve your date.</li></ol></div>
        <div class="box"><h4>Plan ahead</h4><ul class="toc"><li><a href="/pricing">Estimate your price</a></li><li><a href="/tools/wedding-timeline-planner">Build a wedding timeline</a></li><li><a href="/tools/golden-hour-calculator">Find golden hour</a></li></ul></div>
      </aside>
    </div>
  </div>
</section>'''
    page("contact", "Contact Evergrey Photography — Check Your Wedding Date",
         "Contact Evergrey Photography to check availability for your Victoria wedding, Vancouver Island elopement or engagement session. Email info@evergrey-photography.com.",
         body, full_title=True, og_image="lake-dock",
         schema=[breadcrumbs([("Home", ""), ("Contact", "contact")]), {"@type": "ContactPage", "url": url("contact"), "name": "Contact Evergrey Photography"}])


def build_blog():
    cats = sorted({p["category"] for p in POSTS})
    chips = '<button class="chip active" type="button" data-filter="all" aria-pressed="true">All</button>' + "".join(
        f'<button class="chip" type="button" data-filter="{c.lower().replace(" ", "-")}" aria-pressed="false">{c}</button>' for c in cats)
    cards = "".join(post_card(p, big=(i == 0), i=i) for i, p in enumerate(POSTS))
    body = page_hero("The <em>Journal</em>", "Real weddings, Vancouver Island location guides and honest planning advice from a Victoria, BC wedding photographer.",
                     "vintage-camera-prints", "Vintage camera with printed photographs on a map", [("Home", ""), ("Journal", "blog")], cls="short") + f'''
<section class="section">
  <div class="wrap">
    <div class="chips" data-filter-group="#posts" role="group" aria-label="Filter posts">{chips}</div>
    <div class="post-grid" id="posts">{cards}</div>
  </div>
</section>
{cta()}'''
    page("blog", "Wedding Photography Blog — Victoria & Vancouver Island Journal",
         "Real weddings, elopement and engagement guides, venue picks and planning tips for couples marrying in Victoria, BC and across Vancouver Island.",
         body, active="/blog", og_image="vintage-camera-prints", priority="0.8",
         schema=[breadcrumbs([("Home", ""), ("Journal", "blog")]),
                 {"@type": "Blog", "name": "The Evergrey Journal", "url": url("blog"),
                  "blogPost": [{"@type": "BlogPosting", "headline": p["h1"], "url": url("post/" + p["slug"]), "datePublished": p["date"]} for p in POSTS]}])


def build_posts():
    for p in POSTS:
        body_html = figure_tokens(p["body"])
        # wrap tables for horizontal scroll on phones
        body_html = re.sub(r'(<table class="table">.*?</table>)', r'<div class="table-scroll">\1</div>', body_html, flags=re.S)
        heads = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body_html)
        toc = "".join(f'<li><a href="#{i}">{re.sub("<[^>]+>", "", t)}</a></li>' for i, t in heads)
        words = len(re.sub("<[^>]+>", " ", p["body"]).split())
        mins = max(3, round(words / 220))
        date_h = dt.date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        related = [q for q in POSTS if q["slug"] != p["slug"] and q["category"] == p["category"]][:3]
        if len(related) < 3:
            related += [q for q in POSTS if q["slug"] != p["slug"] and q not in related][:3 - len(related)]
        rel = "".join(post_card(q, i=i) for i, q in enumerate(related))
        faq = faq_html(p["faq"], "Frequently asked questions") if p["faq"] else ""
        trail = [("Home", ""), ("Journal", "blog"), (p["h1"], "post/" + p["slug"])]
        hero = f'''<section class="page-hero grain">
  <div class="bg" data-parallax="0.12">{img(p["image"], p["image_alt"], eager=True)}</div>
  <div class="wrap">{crumbs_html(trail)}<span class="eyebrow light">{p["category"]}</span><h1 style="max-width:20ch">{esc(p["h1"])}</h1>
  <div class="post-meta"><span>{date_h}</span><span>{mins} min read</span><span>By {C.NAME}</span></div></div>
</section>'''
        side_tool = ('<a class="btn light" href="/tools/elopement-location-finder">Find your spot</a>' if p["category"] in ("Elopements", "Locations")
                     else '<a class="btn light" href="/tools/golden-hour-calculator">Golden hour</a>')
        body = hero + f'''<div class="progress" aria-hidden="true"></div>
<section class="section tight">
  <div class="wrap">
    <div class="article">
      <article class="prose">{body_html}{faq}</article>
      <aside class="aside">
        {"<div class=\"box\"><h4>In this post</h4><ul class=\"toc\">" + toc + "</ul></div>" if toc else ""}
        <div class="box dark grain" style="position:relative"><h4>Planning something?</h4><p style="font-size:.95rem">We photograph weddings and elopements across Victoria and Vancouver Island.</p><div class="btn-row" style="margin-top:10px"><a class="btn light" href="/contact">Check your date</a></div></div>
        <div class="box"><h4>Free tools</h4><p style="font-size:.92rem">Plan your timeline around the best light of the day.</p>{side_tool}</div>
      </aside>
    </div>
  </div>
</section>
<section class="section bg-mist"><div class="wrap"><div class="strip-head"><div><span class="eyebrow">Keep reading</span><h2 style="margin:0">More from the <em>Journal</em></h2></div><a class="text-link" href="/blog">All posts</a></div><div class="post-grid">{rel}</div></div></section>
{cta()}'''
        schema = [breadcrumbs(trail), {
            "@type": "BlogPosting", "headline": p["h1"], "description": p["description"], "datePublished": p["date"], "dateModified": max(p["date"], "2026-10-17") if p["kind"] == "guide" else p["date"],
            "image": C.SITE + f"/assets/img/{p['image']}.webp", "url": url("post/" + p["slug"]), "mainEntityOfPage": url("post/" + p["slug"]),
            "author": {"@type": "Organization", "name": C.NAME, "url": C.SITE + "/"}, "publisher": {"@id": C.SITE + "/#business"},
            "keywords": p["keyword"], "articleSection": p["category"], "wordCount": words}]
        if p["faq"]:
            schema.append(faq_schema(p["faq"]))
        page("post/" + p["slug"], p["title"], p["description"], body, active="/blog", og_image=p["image"], og_type="article",
             schema=schema, lastmod=p["date"], priority="0.8" if p["kind"] == "story" else "0.7",
             head_extra=f'<meta property="article:published_time" content="{p["date"]}">\n')


def tool_page(route, h1, title, desc, lead, hero, hero_alt, inner, about, faq, extra_js=""):
    trail = [("Home", ""), ("Tools", "tools"), (re.sub("<[^>]+>", "", h1), route)]
    body = page_hero(h1, lead, hero, hero_alt, trail, cls="short", eyebrow="Free planning tool") + f'''
<section class="section tight"><div class="wrap">{inner}</div></section>
<section class="section bg-mist"><div class="wrap narrow"><div class="prose">{about}</div>{faq_html(faq, "Questions")}</div></section>
{cta()}'''
    locs = json.dumps([dict(key=k, name=n, lat=la, lng=ln) for k, n, la, ln in C.LOCATIONS])
    page(route, title, desc, body, active="/tools", og_image=hero,
         scripts=f'<script>window.EG_LOCATIONS={locs};{extra_js}</script>\n<script src="/assets/js/tools.js?v={VER}" defer></script>\n',
         schema=[breadcrumbs(trail), faq_schema(faq),
                 {"@type": "WebApplication", "name": re.sub("<[^>]+>", "", h1), "url": url(route), "applicationCategory": "LifestyleApplication",
                  "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "CAD"}, "provider": {"@id": C.SITE + "/#business"}}])


def build_tools():
    # golden hour
    gh = f'''<div id="golden-hour-tool" class="panel">
  <div class="form-grid">
    <div class="field"><label for="gh-loc">Location</label><select id="gh-loc"></select></div>
    <div class="field"><label for="gh-date">Date</label><input type="date" id="gh-date"></div>
  </div>
  <div class="chips" style="margin:0 0 10px"><button class="chip" type="button" data-jump="today">Today</button><button class="chip" type="button" data-jump="06-21">Summer solstice</button><button class="chip" type="button" data-jump="09-22">Autumn equinox</button><button class="chip" type="button" data-jump="12-21">Winter solstice</button></div>
  <p style="font:500 1.5rem var(--serif);margin:20px 0 0" id="gh-place"></p>
  <div class="sun-arc"><svg viewBox="0 0 1000 200" preserveAspectRatio="none" role="img" aria-label="Sun elevation through the day"></svg></div>
  <div class="daybar" role="img" aria-label="Night, blue hour, golden hour and daylight across 24 hours"></div>
  <div class="daybar-axis"><span>12 a.m.</span><span>6 a.m.</span><span>Noon</span><span>6 p.m.</span><span>12 a.m.</span></div>
  <div class="sun-results" style="margin-top:28px">
    <div class="sun-stat hl"><div class="k">Best portrait window</div><div class="v" id="gh-best"></div></div>
    <div class="sun-stat"><div class="k"><i style="background:#e0a85a"></i>Evening golden hour</div><div class="v" id="gh-evening"></div></div>
    <div class="sun-stat"><div class="k"><i style="background:#4c6a8c"></i>Evening blue hour</div><div class="v" id="gh-blue"></div></div>
    <div class="sun-stat"><div class="k">Sunrise</div><div class="v" id="gh-sunrise"></div></div>
    <div class="sun-stat"><div class="k">Sunset</div><div class="v" id="gh-sunset"></div></div>
    <div class="sun-stat"><div class="k"><i style="background:#e0a85a"></i>Morning golden hour</div><div class="v" id="gh-morning"></div></div>
  </div>
  <p style="margin:14px 0 0;font-size:.9rem;color:var(--moss)">Day length: <strong id="gh-length"></strong>. Times are Pacific time and accurate to about a minute; hills and tall trees can hide the sun earlier.</p>
  <h3 style="margin-top:40px">The next seven days</h3>
  <div class="table-scroll"><table class="week-table" id="gh-week"><thead><tr><th>Date</th><th>Sunrise</th><th>Golden hour</th><th>Sunset</th><th>Blue hour ends</th></tr></thead><tbody></tbody></table></div>
  <div class="btn-row"><a class="btn" id="gh-inquire" href="/contact">Ask about this date {ARROW}</a><a class="btn ghost" href="/tools/wedding-timeline-planner">Build a timeline</a></div>
</div>'''
    tool_page("tools/golden-hour-calculator", "Golden Hour <em>Calculator</em>", "Golden Hour Calculator for Victoria, BC & Vancouver Island",
              "Free golden hour calculator for Victoria, BC and Vancouver Island. Find sunrise, sunset, golden hour and blue hour for any date and plan your wedding photos.",
              "Sunrise, sunset, golden hour and blue hour for Victoria and Vancouver Island locations — on any date.",
              "ocean-sunset-rocks", "Waves washing over rocks under a pastel sunset", gh,
              '''<h2 id="what-is-golden-hour">What is golden hour?</h2>
<p>Golden hour is the stretch of time when the sun sits low — roughly between 6° above the horizon and sunset. Light travels through more atmosphere, turning warm and soft, and shadows stretch long and flattering. For wedding portraits it's the most forgiving light of the day.</p>
<p>Blue hour follows sunset, while the sun is between about 4° and 6° below the horizon: cool, even light that is perfect for city-light portraits around the Inner Harbour.</p>
<h2 id="how-to-use">How to use this for your wedding</h2>
<p>Pick your venue or the closest location, choose your date, and note the best portrait window. Then schedule 15–20 minutes of couple portraits inside it — our <a href="/tools/wedding-timeline-planner">wedding timeline planner</a> does this automatically. On Vancouver Island, summer golden hour arrives late (after 8 p.m. in June), while in December the sun sets before 4:30 p.m., so ceremony times shift a lot by season. Read more in our <a href="/post/wedding-day-timeline-victoria-bc">wedding day timeline guide</a>.</p>''',
              [("How accurate are these times?", "The calculator uses standard solar-position formulas and should be within a minute or two of published sunrise and sunset times. Local terrain — hills, tall trees, buildings — can block the sun earlier than the calculated sunset."),
               ("Does it handle daylight saving time?", "Yes. All times are shown in Pacific time and switch automatically between PST and PDT."),
               ("Is golden hour the same everywhere on Vancouver Island?", "No. Tofino sets several minutes later than Victoria, and further north the days are longer in summer and shorter in winter. Choose the location closest to yours."),
               ("What if it's cloudy?", "Overcast skies soften light all day, which is beautiful for portraits. Golden hour still brings a subtle warmth — and sometimes a dramatic break in the clouds.")])

    # timeline planner
    tp = f'''<div id="timeline-tool" class="calc-layout">
  <form class="panel no-print">
    <div class="form-grid">
      <div class="field"><label for="tl-date">Wedding date</label><input type="date" id="tl-date" name="date"></div>
      <div class="field"><label for="tl-loc">Nearest location</label><select id="tl-loc" name="loc"></select></div>
      <div class="field"><label for="tl-c">Ceremony start</label><input type="time" id="tl-c" name="ceremony" value="17:00" step="900"></div>
      <div class="field"><label for="tl-clen">Ceremony length</label><select id="tl-clen" name="clen"><option value="20">20 minutes</option><option value="30" selected>30 minutes</option><option value="45">45 minutes</option><option value="60">60 minutes</option></select></div>
      <div class="field"><label for="tl-groups">Family photo groupings</label><select id="tl-groups" name="groups"><option>4</option><option>6</option><option selected>8</option><option>10</option><option>12</option><option>15</option></select></div>
      <div class="field"><label for="tl-cock">Cocktail hour</label><select id="tl-cock" name="cocktail"><option value="45">45 minutes</option><option value="60" selected>60 minutes</option><option value="90">90 minutes</option></select></div>
      <div class="field"><label for="tl-travel">Travel to reception</label><select id="tl-travel" name="travel"><option value="0" selected>Same venue</option><option value="15">15 minutes</option><option value="30">30 minutes</option><option value="45">45 minutes</option></select></div>
      <div class="field"><label for="tl-party">Dance-floor coverage</label><select id="tl-party" name="party"><option value="0">None</option><option value="1" selected>1 hour</option><option value="2">2 hours</option></select></div>
    </div>
    <div class="toggles">
      <label class="toggle"><span class="t-l"><b>First look</b><small>See each other before the ceremony</small></span><input type="checkbox" name="firstlook" checked></label>
      <label class="toggle"><span class="t-l"><b>Getting-ready coverage</b><small>Details, dressing and quiet moments</small></span><input type="checkbox" name="prep" checked></label>
    </div>
  </form>
  <div class="panel">
    <span class="eyebrow">Your photo timeline</span>
    <p id="tl-summary" style="font-size:.98rem"></p>
    <div id="tl-out"></div>
    <div class="btn-row no-print"><button class="btn" type="button" id="tl-print">Print / save PDF</button><a class="btn ghost" id="tl-pricing" href="/pricing">Price this coverage</a></div>
  </div>
</div>'''
    tool_page("tools/wedding-timeline-planner", "Wedding Timeline <em>Planner</em>", "Wedding Day Timeline Planner — Free Photo Schedule Tool",
              "Build a photo-friendly wedding day timeline in seconds. Enter your ceremony time and date and we'll schedule portraits around golden hour.",
              "Enter your ceremony details and get a photo-friendly schedule that lands your portraits in golden hour.",
              "ceremony-aisle", "Outdoor wedding ceremony aisle lined with flowers", tp,
              '''<h2 id="how-it-works">How the planner works</h2>
<p>The planner works backwards and forwards from your ceremony time using the same blocks we use with our own couples: time for details and getting ready, a first look (or not), realistic family-photo timing based on the number of groupings, a cocktail-hour portrait session, and the key reception moments.</p>
<p>It then calculates the sunset for your date and location and slots a 15–20 minute golden-hour portrait session just before it. If sunset lands too early or too late for your schedule, the summary tells you — that's usually a sign to shift the ceremony by thirty minutes or add an hour of coverage.</p>
<h2 id="tips">Timeline tips from a Victoria wedding photographer</h2>
<ul><li>Add a 10–15 minute buffer anywhere hair, makeup or travel is involved.</li><li>Write a named family-photo list and assign a helper who knows everyone.</li><li>In summer, sunset can be after 9 p.m. — plan to slip out between dinner and dancing.</li><li>Ferry or highway travel on the Malahat? Add extra margin.</li></ul>
<p>Want the full explanation? Read our <a href="/post/wedding-day-timeline-victoria-bc">wedding day timeline guide</a>.</p>''',
              [("Is a first look necessary?", "Not at all. A first look frees up time for portraits before the ceremony; without one we simply do more portraits during cocktail hour. Toggle it to compare."),
               ("How long do family photos take?", "Plan about three minutes per grouping plus a few minutes to gather people. Eight groupings is roughly half an hour."),
               ("How many hours of coverage do we need?", "The summary suggests coverage based on your inputs. Most full weddings land between seven and nine hours."),
               ("Can I save my timeline?", "Use the print button to save a PDF, or copy it into your planning document. The settings stay as long as the page is open.")])

    # elopement finder
    qs = [
        ("scene", "Which backdrop makes your heart race?", [("forest", "Old-growth forest", "Moss, ferns, giant cedars"), ("ocean", "Wild coastline", "Beaches, tide pools, crashing waves"),
                                                            ("garden", "Gardens &amp; castles", "Manicured, romantic, historic"), ("view", "Big viewpoint", "Summits and panoramas"),
                                                            ("city", "Harbour &amp; city", "Heritage brick and city lights"), ("any", "Surprise us", "We love it all")]),
        ("walk", "How far are you happy to walk in your outfits?", [("easy", "A few steps", "Paved paths or right by the car"), ("moderate", "Up to 20 minutes", "A gentle trail is fine"),
                                                                     ("hike", "Let's hike", "45+ minutes, proper shoes on")]),
        ("privacy", "How much privacy do you want?", [("low", "Don't mind people", "Passers-by cheering is fun"), ("med", "Fairly quiet", "Some solitude would be nice"),
                                                      ("high", "Totally secluded", "Just us and the view")]),
        ("drive", "How far will you travel from Victoria?", [("near", "Under 30 minutes", "Keep it close"), ("hour", "Up to about an hour", "A scenic drive is fine"),
                                                             ("trip", "Road trip!", "Make a weekend of it")]),
    ]
    qhtml = ""
    for i, (k, q, opts) in enumerate(qs):
        o = "".join(f'<button type="button" class="quiz-opt" data-q="{k}" data-v="{v}"><b>{t}</b><small>{s}</small></button>' for v, t, s in opts)
        qhtml += f'<div class="quiz-q"><span class="eyebrow">Question {i + 1} of {len(qs)}</span><h2 style="font-size:clamp(1.8rem,3.4vw,2.6rem)">{q}</h2><div class="quiz-opts">{o}</div></div>'
    lf = f'''<div id="finder-tool" class="panel" style="max-width:900px;margin:0 auto">
  <div class="quiz-progress"><span></span></div>
  {qhtml}
  <div id="finder-results" hidden><span class="eyebrow">Your matches</span><h2 style="font-size:clamp(1.8rem,3.4vw,2.6rem)">Spots made for <em>you two</em></h2><div id="finder-list"></div>
    <p style="font-size:.88rem;color:var(--moss);margin-top:20px">Always check current access, park rules and permit requirements before you book — we'll help with this when we plan together.</p>
    <div class="btn-row"><a class="btn" href="/contact?type=elopement">Plan our elopement {ARROW}</a><button class="btn ghost" type="button" id="quiz-restart">Start over</button></div></div>
  <div class="btn-row" style="margin-top:20px"><button class="text-link" type="button" id="quiz-back" style="background:none;border:0;border-bottom:1px solid var(--sand);cursor:pointer" hidden>← Back</button></div>
</div>'''
    spots = json.dumps(C.SPOTS)
    tool_page("tools/elopement-location-finder", "Elopement <em>Location Finder</em>", "Vancouver Island Elopement Location Finder — Free Quiz",
              "Find your perfect Vancouver Island elopement location. Answer four quick questions and get matched with beaches, forests and viewpoints near Victoria, BC.",
              "Four quick questions, then your best-matched elopement spots around Victoria and Vancouver Island.",
              "forest-path", "Sunlit trail winding through an evergreen forest", lf,
              '''<h2 id="choosing">Choosing an elopement location on Vancouver Island</h2>
<p>The island packs a remarkable range of scenery into a short drive: old-growth rainforest, cobble and sand beaches, rocky headlands, Garry oak meadows, vineyards and mountain summits. The right spot depends on how you want the day to feel — and on practical things like walking distance, privacy and the season.</p>
<p>Once you have a shortlist, check the light with our <a href="/tools/golden-hour-calculator">golden hour calculator</a> and read the <a href="/post/vancouver-island-elopement-guide">Vancouver Island elopement guide</a> for licences, permits and a sample timeline. Rain on the forecast? Forest canopies are your friend — see how <a href="/post/kasha-justin">Kasha and Justin</a> made the most of it at <a href="/post/aylard-farm-east-sooke-wedding-photos">Aylard Farm</a>.</p>''',
              [("Do we need a permit to elope at these locations?", "Many regional, provincial and national parks require a permit for ceremonies or commercial photography, and the rules change. We confirm the current requirements for your chosen spot during planning."),
               ("What's the best season for a beach elopement?", "Summer brings the warmest, driest weather, but late spring and early autumn offer softer light and quieter beaches. Winter storms are dramatic if you dress for them."),
               ("Can our families come?", "Yes. Easy-access spots like French Beach, Dallas Road or Hatley Park suit guests with limited mobility; choose 'A few steps' in the quiz."),
               ("Are the drive times exact?", "They're rough estimates from downtown Victoria without traffic or ferries. Always allow extra time on the Malahat and Highway 14.")],
              extra_js=f"window.EG_SPOTS={spots};")

    # tools hub
    hub = f'''<div class="grid-3">
  <a class="price-card" href="/tools/golden-hour-calculator" style="text-decoration:none" data-reveal><div class="ico" style="width:46px;height:46px;border-radius:50%;display:grid;place-items:center;background:var(--sand-2)">{icon("sun")}</div><h3 style="margin-top:20px">Golden hour calculator</h3><p>Sunrise, sunset, golden and blue hour for 13 Vancouver Island locations, with a seven-day outlook.</p><span class="text-link" style="margin-top:auto">Open tool</span></a>
  <a class="price-card featured" href="/tools/wedding-timeline-planner" style="text-decoration:none" data-reveal data-delay="120"><div class="ico" style="width:46px;height:46px;border-radius:50%;display:grid;place-items:center;background:rgba(255,255,255,.12)">{icon("clock")}</div><h3 style="margin-top:20px">Wedding timeline planner</h3><p>A printable photo schedule built around your ceremony time, family photos and sunset.</p><span class="text-link" style="margin-top:auto">Open tool</span></a>
  <a class="price-card" href="/tools/elopement-location-finder" style="text-decoration:none" data-reveal data-delay="240"><div class="ico" style="width:46px;height:46px;border-radius:50%;display:grid;place-items:center;background:var(--sand-2)">{icon("compass")}</div><h3 style="margin-top:20px">Elopement location finder</h3><p>Match your style, fitness and travel range to beaches, forests and viewpoints.</p><span class="text-link" style="margin-top:auto">Take the quiz</span></a>
  <a class="price-card" href="/pricing#estimate" style="text-decoration:none" data-reveal><div class="ico" style="width:46px;height:46px;border-radius:50%;display:grid;place-items:center;background:var(--sand-2)">{icon("camera")}</div><h3 style="margin-top:20px">Photography price estimator</h3><p>Choose hours, add-ons and location to see an instant estimate including GST.</p><span class="text-link" style="margin-top:auto">Estimate</span></a>
</div>'''
    body = page_hero("Wedding Planning <em>Tools</em>", "Free, interactive tools for planning a wedding or elopement around Vancouver Island's light, places and budget.",
                     "camera-lenses-dark", "Camera body and lens on a dark surface", [("Home", ""), ("Tools", "tools")], cls="short") + f'''
<section class="section"><div class="wrap">{hub}</div></section>{cta()}'''
    page("tools", "Free Wedding Planning Tools for Vancouver Island Couples",
         "Free wedding planning tools from Evergrey Photography: golden hour calculator, wedding timeline planner, elopement location finder and price estimator.",
         body, active="/tools", og_image="camera-lenses-dark", schema=[breadcrumbs([("Home", ""), ("Tools", "tools")])])


def build_legal():
    body = page_hero("Privacy <em>Policy</em>", "How we handle the information you share with us.", "lake-dock", "Calm lake at dawn",
                     [("Home", ""), ("Privacy Policy", "privacy-policy")], cls="short") + f'''
<section class="section"><div class="wrap narrow prose">
<p>Evergrey Photography (“we”, “us”) respects your privacy. This policy explains what we collect through evergrey-photography.com and how we use it.</p>
<h2 id="what-we-collect">What we collect</h2>
<p>When you send an inquiry we receive the details you enter — such as your name, email, phone number, event date, location and message. Our web host records standard server logs (IP address, browser and pages requested) for security and performance. The interactive tools run entirely in your browser; the dates and options you enter are not sent to us.</p>
<h2 id="how-we-use-it">How we use it</h2>
<p>We use inquiry details only to respond to you, prepare a proposal and, if you book, deliver our services. We never sell or rent your information.</p>
<h2 id="photographs">Photographs</h2>
<p>If you book with us, how your photographs may be shared (for example in our portfolio or journal) is set out in your photography agreement, and we always respect requests to keep a gallery private.</p>
<h2 id="third-parties">Third parties</h2>
<p>We use Google Fonts to display typefaces, which means your browser connects to Google's servers. We do not use advertising trackers.</p>
<h2 id="your-rights">Your rights</h2>
<p>You can ask to see, correct or delete the personal information we hold about you at any time by emailing <a href="mailto:{C.EMAIL}">{C.EMAIL}</a>. We handle personal information in line with Canadian privacy law, including PIPEDA and BC's Personal Information Protection Act.</p>
<p><em>Last updated {dt.date.today().strftime("%B %-d, %Y")}.</em></p>
</div></section>'''
    page("privacy-policy", "Privacy Policy", "Privacy policy for Evergrey Photography, a Victoria, BC wedding and elopement photographer: what we collect, how we use it and your rights.",
         body, priority="0.3", schema=[breadcrumbs([("Home", ""), ("Privacy Policy", "privacy-policy")])])


def build_404():
    body = f'''<section class="page-hero grain" style="min-height:100vh;min-height:100svh">
  <div class="bg">{img("foggy-evergreens", "Evergreen trees fading into fog", eager=True)}</div>
  <div class="wrap"><span class="eyebrow light">Error 404</span><h1>Lost in the <em>fog</em></h1><p class="lead">The page you were looking for has wandered off the trail. Let's get you back.</p>
  <div class="btn-row"><a class="btn light" href="/">Home {ARROW}</a><a class="btn ghost-light" href="/blog">The Journal</a><a class="btn ghost-light" href="/contact">Contact</a></div></div>
</section>'''
    page("404", "Page Not Found", "This page could not be found.", body, sitemap=False)
    f = os.path.join(PAGES, "404.html")
    s = open(f, encoding="utf-8").read().replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">')
    s = re.sub(r'<link rel="canonical"[^>]+>\n', "", s)
    open(f, "w", encoding="utf-8").write(s)


def write_static():
    with open(os.path.join(PUB, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
                 'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n')
        for loc, lm, pr, imgs in sorted(SITEMAP, key=lambda x: (-float(x[2]), x[0])):
            im = "".join(f"<image:image><image:loc>{C.SITE}/assets/img/{k}.webp</image:loc></image:image>" for k in imgs)
            fh.write(f"  <url><loc>{loc}</loc><lastmod>{lm}</lastmod><priority>{pr}</priority>{im}</url>\n")
        fh.write("</urlset>\n")
    items = "".join(
        f"<item><title>{esc(p['h1'])}</title><link>{url('post/' + p['slug'])}</link><guid>{url('post/' + p['slug'])}</guid>"
        f"<pubDate>{dt.datetime.fromisoformat(p['date']).strftime('%a, %d %b %Y 12:00:00 -0800')}</pubDate>"
        f"<category>{esc(p['category'])}</category><description>{esc(p['excerpt'])}</description></item>\n" for p in POSTS)
    with open(os.path.join(PUB, "feed.xml"), "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>'
                 f'<title>The Evergrey Journal</title><link>{url("blog")}</link><description>Real weddings, Vancouver Island location guides and planning advice from {C.NAME}.</description>'
                 f'<language>en-ca</language><atom:link href="{C.SITE}/feed.xml" rel="self" type="application/rss+xml"/>\n{items}</channel></rss>\n')
    with open(os.path.join(PUB, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write(f"User-agent: *\nAllow: /\nDisallow: /_pages/\nDisallow: /contact.php\n\nSitemap: {C.SITE}/sitemap.xml\n")


def favicons():
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="9" fill="#1b2420"/>'
           '<path d="M20 7 12.5 19h4L11 27.5h7V33h4v-5.5h7L23.5 19h4z" fill="#c4a275"/></svg>')
    open(os.path.join(PUB, "favicon.svg"), "w").write(svg)
    from PIL import ImageDraw
    pts = [(20, 7), (12.5, 19), (16.5, 19), (11, 27.5), (18, 27.5), (18, 33), (22, 33), (22, 27.5), (29, 27.5), (23.5, 19), (27.5, 19)]

    def icon_png(size, radius=.22, pad=0.0):
        big = size * 4  # supersample for smooth edges
        im = Image.new("RGBA", (big, big), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, big - 1, big - 1], radius=int(big * radius), fill="#1b2420")
        s, off = big * (1 - 2 * pad) / 40, big * pad
        d.polygon([(off + x * s, off + y * s) for x, y in pts], fill="#c4a275")
        return im.resize((size, size), Image.LANCZOS)

    icon_png(96).save(os.path.join(PUB, "favicon-96x96.png"))
    icon_png(180, radius=0).save(os.path.join(PUB, "apple-touch-icon.png"))
    icon_png(192, radius=0, pad=.1).save(os.path.join(PUB, "web-app-manifest-192x192.png"))
    icon_png(512, radius=0, pad=.1).save(os.path.join(PUB, "web-app-manifest-512x512.png"))
    icon_png(512).save(os.path.join(IMG, "logo.png"))
    icon_png(256).save(os.path.join(PUB, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    for stale in ("favicon.png",):
        f = os.path.join(PUB, stale)
        if os.path.exists(f):
            os.remove(f)
    manifest = {
        "name": C.NAME, "short_name": "Evergrey", "start_url": "/", "display": "standalone",
        "background_color": "#f6f4ef", "theme_color": "#1b2420",
        "icons": [
            {"src": "/web-app-manifest-192x192.png", "sizes": "192x192", "type": "image/png", "purpose": "maskable"},
            {"src": "/web-app-manifest-512x512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
            {"src": "/favicon-96x96.png", "sizes": "96x96", "type": "image/png"},
        ],
    }
    with open(os.path.join(PUB, "site.webmanifest"), "w") as fh:
        json.dump(manifest, fh, indent=2)
    # Google Search Console HTML-file verification
    with open(os.path.join(PUB, "googlecccfbf2f7e9e5ae4.html"), "w") as fh:
        fh.write("google-site-verification: googlecccfbf2f7e9e5ae4.html")


def main():
    if os.path.isdir(PAGES):
        shutil.rmtree(PAGES)
    os.makedirs(PAGES)
    build_home()
    build_about()
    build_services()
    build_portfolio()
    build_pricing()
    build_contact()
    build_blog()
    build_posts()
    build_tools()
    build_legal()
    build_404()
    write_static()
    favicons()
    print(f"built {len(SITEMAP)} indexable pages + 404 into {PAGES}")


if __name__ == "__main__":
    main()
