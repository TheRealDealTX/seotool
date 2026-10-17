#!/usr/bin/env python3
"""Static site generator for dukoraidea.com.

Writes every page as `_pages/<url path>.html` (the homepage is `_pages/home.html`)
plus `sitemap.xml` and `robots.txt`. `index.php` maps clean, Shopify-style URLs
(no trailing slash) onto those files. Standard library only.
"""

import html
import json
import re
import shutil
from datetime import date
from pathlib import Path

from content import posts_a, posts_b, posts_c, products as products_mod

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "_pages"

SITE = {
    "name": "Dukora Idea",
    "short": "Dukora",
    "origin": "https://dukoraidea.com",
    "email": "info@dukoraidea.com",
    "tagline": "DIY lighting ideas, light guides and tools for cozy, glowing spaces.",
}
TODAY = date.today().isoformat()
IMG = json.loads((ROOT / "assets/img/sizes.json").read_text())

POSTS = posts_a.POSTS + posts_b.POSTS + posts_c.POSTS
POSTS.sort(key=lambda p: p["published"], reverse=True)
POST_BY = {p["slug"]: p for p in POSTS}
PRODUCTS = products_mod.PRODUCTS
PROD_BY = {p["slug"]: p for p in PRODUCTS}

COLLECTIONS = {
    "fairy-lights": dict(
        title="Fairy Lights & String Lights",
        h1="Fairy Lights, String Lights & Garlands",
        meta_title="Fairy Lights & String Lights Guides",
        description="Every Dukora fairy light guide in one place: battery operated, outdoor, waterproof, firefly and garland lights, plus fake ivy to style them with.",
        lead="Battery packs, copper wire, timers, waterproof ratings and the styling tricks that make a string of tiny lights look magical.",
        image="hands-holding-fairy-lights",
        members=("fairy-lights", "decor"),
    ),
    "smart-lights": dict(
        title="Smart Lights",
        h1="Smart Lights: LED Strips, Bulbs & Controllers",
        meta_title="Smart Lights: LED Strip, Bulb & Controller Guides",
        description="Smart LED strip lights, color-changing smart bulbs and Wi-Fi LED controllers explained: setup, Alexa and Google Home, power supplies and best uses.",
        lead="App-controlled LED strips, color bulbs and the controllers that run them, explained without the jargon.",
        image="smart-home-bulbs",
        members=("smart-lights",),
    ),
    "all": dict(
        title="All Light Guides",
        h1="All Dukora Light Guides",
        meta_title="All Light Guides: Fairy, String & Smart Lights",
        description="Browse every Dukora light guide: fairy lights, outdoor string lights, battery garlands, smart LED strip lights, smart bulbs, LED controllers and more.",
        lead="Eleven in-depth guides to the lights we love most, from micro fairy lights to Wi-Fi LED strips.",
        image="globe-string-lights",
        members=("fairy-lights", "smart-lights", "decor"),
    ),
}

NAV = [
    ("Fairy Lights", "/collections/fairy-lights"),
    ("Smart Lights", "/collections/smart-lights"),
    ("Ideas & Blog", "/blogs/blog"),
    ("Light Tools", "/pages/light-tools"),
    ("About", "/pages/about-us"),
]

CATEGORIES = ["DIY Projects", "Decor Ideas", "Smart Lighting", "Guides", "Events & Holidays"]

E = html.escape

# Google Analytics 4 tag, emitted at the top of <head> on every page (including the 404).
GTAG = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-ZPW2DBNKW1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-ZPW2DBNKW1');
</script>"""


def url(path):
    return SITE["origin"] + path


def fmt_date(d):
    y, m, dd = d.split("-")
    months = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
    return f"{months[int(m) - 1]} {int(dd)}, {y}"


def words(htm):
    return len(re.sub(r"<[^>]+>", " ", htm).split())


# ---------------------------------------------------------------- images
def img(name, alt, cls="", sizes="(max-width: 900px) 100vw, 50vw", eager=False, small=False):
    w, h = IMG[name]
    src = f"/assets/img/{name}{'-800' if small else ''}.webp"
    sw = round(w * 800 / max(w, h))
    srcset = f"/assets/img/{name}-800.webp {sw}w, /assets/img/{name}.webp {w}w"
    if small:
        r = 800 / max(w, h)
        w, h = round(w * r), round(h * r)
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img src="{src}" srcset="{srcset}" sizes="{sizes}" width="{w}" height="{h}" '
            f'alt="{E(alt)}"{c} {load}>')


def figure(name, alt, caption):
    return (f'<figure class="reveal">{img(name, alt, sizes="(max-width: 1080px) 100vw, 760px")}'
            f"<figcaption>{E(caption)}</figcaption></figure>")


# ---------------------------------------------------------------- icons
ICONS = {
    "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "up": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5M6 11l6-6 6 6"/></svg>',
    "battery": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="7" width="17" height="10" rx="2"/><path d="M22 11v2M6 10v4M10 10v4"/></svg>',
    "strip": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 9h18v6H3z"/><path d="M7 12h.01M12 12h.01M17 12h.01"/></svg>',
    "color": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
    "patio": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 5c5 4 15 4 20 0"/><path d="M6 7.5v2M12 8.6v2M18 7.5v2"/><path d="M4 21V12M20 21V12"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
}


def logo_svg(uid):
    return (f'<svg viewBox="0 0 40 40" aria-hidden="true"><defs><radialGradient id="lg{uid}" cx="50%" cy="38%" r="60%">'
            '<stop offset="0" stop-color="#fff8e4"/><stop offset=".5" stop-color="#ffc56b"/><stop offset="1" stop-color="#ff8a5b"/>'
            '</radialGradient></defs>'
            f'<path d="M20 3.5c-6.6 0-11.2 4.9-11.2 10.8 0 4 2.1 6.6 4.1 8.7 1.4 1.4 2 2.8 2 4.5h10.2c0-1.7.6-3.1 2-4.5 2-2.1 4.1-4.7 4.1-8.7C31.2 8.4 26.6 3.5 20 3.5z" fill="url(#lg{uid})"/>'
            '<path d="M16.5 21.5c1.2-3 2.3-4.6 3.5-4.6s2.3 1.6 3.5 4.6" fill="none" stroke="#a24d10" stroke-width="1.6" stroke-linecap="round"/>'
            '<rect x="14.8" y="29" width="10.4" height="3.2" rx="1.6" fill="#d9ddf2"/><rect x="16.3" y="33.2" width="7.4" height="2.8" rx="1.4" fill="#a3a9cc"/></svg>')


# ---------------------------------------------------------------- tools
def tool_html(kind, level="h3", tid=""):
    h = level
    if kind == "battery":
        return f'''<div class="tool reveal" data-tool="battery" id="{tid or 'battery-calculator'}">
<{h}>Fairy light battery life calculator</{h}>
<p class="tool-intro">Estimate how long a battery-operated string will glow. Move the sliders and watch the lights.</p>
<div class="tool-grid"><div>
<div class="field"><label for="cell-{tid}">Battery type</label><select id="cell-{tid}" name="cell">
<option value="2500" selected>AA alkaline (about 2,500 mAh)</option><option value="2000">AA rechargeable NiMH (about 2,000 mAh)</option>
<option value="1100">AAA alkaline (about 1,100 mAh)</option><option value="800">AAA rechargeable NiMH (about 800 mAh)</option>
<option value="220">CR2032 coin cell (about 220 mAh)</option><option value="3000">USB power bank, 5,000 mAh (about 3,000 usable at 5 V)</option>
</select></div>
<div class="field"><label for="leds-{tid}">Number of LEDs <output data-out="leds"></output></label><input id="leds-{tid}" type="range" name="leds" min="10" max="300" step="10" value="100"></div>
<div class="field"><span class="label">Light mode</span><div class="seg" role="group" aria-label="Light mode"><button type="button" data-v="1" aria-pressed="true">Steady</button><button type="button" data-v="0.6" aria-pressed="false">Twinkle</button><button type="button" data-v="0.5" aria-pressed="false">Slow fade</button></div></div>
<div class="field"><label for="bright-{tid}">Brightness <output data-out="bright"></output></label><input id="bright-{tid}" type="range" name="bright" min="10" max="100" step="5" value="100"></div>
<div class="field"><label for="hours-{tid}">Hours on per night (timer) <output data-out="hours"></output></label><input id="hours-{tid}" type="range" name="hours" min="1" max="12" step="1" value="6"></div>
</div><div class="result" aria-live="polite">
<div class="result-big" data-out="runtime"></div>
<div class="led-row" aria-hidden="true"></div>
<div class="result-row"><span>Estimated draw</span><b data-out="draw"></b></div>
<div class="result-row"><span>Lasts about</span><b data-out="nights"></b></div>
<div class="result-row"><span>Per 30 days you'll use</span><b data-out="month"></b></div>
<div class="battery-bar" aria-hidden="true"><span></span></div>
<p class="result-note">Estimate based on about 0.75 mA per micro LED at full brightness and 85% usable capacity. Cold weather and cheap cells shorten runtime.</p>
</div></div></div>'''
    if kind == "strip":
        sw = "".join(f'<button type="button" data-c="{c}" aria-pressed="{"true" if i == 0 else "false"}" style="background:{c}" aria-label="{n}"></button>'
                     for i, (c, n) in enumerate([("#ffc56b", "Warm white"), ("#ff4f8b", "Pink"), ("#8b6cff", "Purple"), ("#3fb6ff", "Blue"), ("#5ee6c9", "Mint"), ("#ff5a3c", "Red")]))
        return f'''<div class="tool reveal" data-tool="strip" id="{tid or 'strip-calculator'}">
<{h}>LED strip length and power supply calculator</{h}>
<p class="tool-intro">Size the power supply, find the cut interval and see whether a long run needs power injection.</p>
<div class="tool-grid"><div>
<div class="field"><span class="label">Units</span><div class="seg" data-k="unit" role="group" aria-label="Units"><button type="button" data-v="ft" aria-pressed="true">Feet</button><button type="button" data-v="m" aria-pressed="false">Meters</button></div></div>
<div class="field"><label for="len-{tid}">Strip length <output data-out="len"></output></label><input id="len-{tid}" type="range" name="len" min="1" max="100" step="1" value="16"></div>
<div class="field"><label for="dens-{tid}">LED type and density</label><select id="dens-{tid}" name="dens">
<option value="30" data-w="7.2">5050 RGB, 30 LEDs/m (about 7.2 W/m)</option><option value="60" data-w="14.4" selected>5050 RGB, 60 LEDs/m (about 14.4 W/m)</option>
<option value="120" data-w="9.6">2835 white, 120 LEDs/m (about 9.6 W/m)</option><option value="cob" data-w="10">COB dotless strip (about 10 W/m)</option></select></div>
<div class="field"><label for="wpm-{tid}">Watts per meter (from the label)</label><input id="wpm-{tid}" type="number" name="wpm" min="1" max="40" step="0.1" value="14.4"></div>
<div class="field"><span class="label">Voltage</span><div class="seg" data-k="volts" role="group" aria-label="Voltage"><button type="button" data-v="5" aria-pressed="false">5 V (USB)</button><button type="button" data-v="12" aria-pressed="true">12 V</button><button type="button" data-v="24" aria-pressed="false">24 V</button></div></div>
<div class="field"><span class="label">Preview color</span><div class="swatch-row">{sw}</div></div>
</div><div class="result" aria-live="polite">
<div class="result-big" data-out="watts"></div>
<div class="strip-vis" aria-hidden="true"></div>
<div class="result-row"><span>Current draw</span><b data-out="amps"></b></div>
<div class="result-row"><span>Power supply (20% headroom)</span><b data-out="psu"></b></div>
<div class="result-row"><span>LEDs on the run</span><b data-out="leds"></b></div>
<div class="result-row"><span>Cut marks</span><b data-out="cut"></b></div>
<div class="result-row"><span>Power injection</span><b data-out="inject"></b></div>
<p class="result-note">Each block in the preview is one powered section. Always check the watts-per-meter on your strip's label; it varies by brand.</p>
</div></div></div>'''
    if kind == "color":
        moods = "".join(f'<button type="button" data-mood="{k}" aria-pressed="false">{n}</button>'
                        for k, n in [("sleep", "Sleep"), ("relax", "Relax"), ("read", "Read"), ("focus", "Focus"), ("movie", "Movie"), ("party", "Party")])
        return f'''<div class="tool reveal" data-tool="color" id="{tid or 'color-picker'}">
<{h}>Color temperature and mood picker</{h}>
<p class="tool-intro">Slide through warm to cool white, or pick a mood, and preview how the room will feel.</p>
<div class="tool-grid"><div>
<div class="room-preview" aria-hidden="true"><div class="rp-wall"></div><div class="rp-floor"></div><div class="rp-lamp"></div><div class="rp-bulb"></div><div class="rp-sofa"></div><div class="rp-plant"></div><span class="rp-label"></span></div>
</div><div>
<div class="field"><span class="label">Pick a mood</span><div class="seg" role="group" aria-label="Mood">{moods}</div></div>
<div class="field"><label for="k-{tid}">White temperature <output data-out="kelvin"></output></label><input id="k-{tid}" type="range" name="kelvin" min="1800" max="6500" step="100" value="2700"><div class="kelvin-track" aria-hidden="true"></div></div>
<div class="field"><label for="hue-{tid}">Or a color (RGB mode) <output data-out="hue"></output></label><input id="hue-{tid}" type="range" name="hue" min="0" max="360" step="1" value="285" style="accent-color:#9d8cff"></div>
<div class="field"><label for="cb-{tid}">Brightness <output data-out="bright"></output></label><input id="cb-{tid}" type="range" name="cbright" min="10" max="100" step="5" value="70"></div>
<div class="result" aria-live="polite"><div class="result-row" style="border:0;padding-top:0"><span>Feel</span><b data-out="name"></b></div><div class="result-row"><span>Hex</span><b data-out="hex"></b></div><p class="result-note" data-out="use" style="color:#e9e9f2;font-size:.95rem"></p></div>
</div></div></div>'''
    if kind == "patio":
        return f'''<div class="tool reveal" data-tool="patio" id="{tid or 'patio-planner'}">
<{h}>Patio string light planner</{h}>
<p class="tool-intro">Enter your space, choose a hanging pattern and get the strand count, bulbs and anchor points, with a plan drawing.</p>
<div class="tool-grid"><div>
<div class="field"><label for="pw-{tid}">Width <output data-out="pw"></output></label><input id="pw-{tid}" type="range" name="pw" min="8" max="60" step="1" value="16"></div>
<div class="field"><label for="pl-{tid}">Length <output data-out="pl"></output></label><input id="pl-{tid}" type="range" name="pl" min="8" max="60" step="1" value="20"></div>
<div class="field"><span class="label">Pattern</span><div class="seg" role="group" aria-label="Pattern"><button type="button" data-v="perimeter" aria-pressed="true">Perimeter</button><button type="button" data-v="zigzag" aria-pressed="false">Zigzag</button><button type="button" data-v="parallel" aria-pressed="false">Parallel</button><button type="button" data-v="canopy" aria-pressed="false">Canopy</button></div></div>
<div class="field"><label for="st-{tid}">Strand length</label><select id="st-{tid}" name="strand"><option value="24">24 ft strands</option><option value="48" selected>48 ft strands</option><option value="100">100 ft strands</option></select></div>
<div class="field"><label for="sp-{tid}">Bulb spacing</label><select id="sp-{tid}" name="spacing"><option value="1">Every 1 ft (fairy and micro)</option><option value="2" selected>Every 2 ft (festoon)</option><option value="3">Every 3 ft (large globes)</option></select></div>
</div><div>
<svg class="patio-svg" viewBox="0 0 400 280" role="img" aria-label="Plan drawing of the string light layout"></svg>
<div class="result" aria-live="polite" style="margin-top:14px">
<div class="result-big" data-out="total"></div>
<div class="result-row"><span>You'll need</span><b data-out="strands"></b></div>
<div class="result-row"><span>Bulbs</span><b data-out="bulbs"></b></div>
<div class="result-row"><span>Hooks or posts</span><b data-out="anchors"></b></div>
<div class="result-row"><span>Steel guide wire</span><b data-out="wire"></b></div>
<p class="result-note">Includes about 10% for a gentle drape and 6 ft to reach the outlet. Check the maximum number of strands your lights can link end to end.</p>
</div></div></div></div>'''
    raise ValueError(kind)


TOOLS = [
    ("battery", "Battery life calculator", "How many nights will your battery fairy lights last?"),
    ("strip", "LED strip calculator", "Watts, amps, power supply and cut marks for any strip."),
    ("color", "Color & mood picker", "Preview warm-to-cool white and RGB moods in a room."),
    ("patio", "Patio light planner", "Strands, bulbs and anchor points for your outdoor space."),
]
TOOL_ANCHOR = {"battery": "battery-calculator", "strip": "strip-calculator", "color": "color-picker", "patio": "patio-planner"}


# ---------------------------------------------------------------- body rendering
def slugify(s):
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s).lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:60]


def render_body(body):
    """Expand {{fig}} / {{tool}} tokens, id the h2s; return (html, toc)."""
    def fig(m):
        name, alt, cap = (m.group(1).split("|") + ["", ""])[:3]
        name = name.strip()
        if name not in IMG:
            raise SystemExit(f"unknown image {name!r}")
        return figure(name, alt.strip(), cap.strip())

    body = re.sub(r"(?:<p>\s*)?\{\{fig:([^}]+)\}\}(?:\s*</p>)?", fig, body)
    body = re.sub(r"(?:<p>\s*)?\{\{tool:(\w+)\}\}(?:\s*</p>)?", lambda m: tool_html(m.group(1)), body)
    toc, seen = [], set()

    def h2(m):
        text = m.group(2)
        sid = slugify(text) or "section"
        while sid in seen:
            sid += "-2"
        seen.add(sid)
        toc.append((sid, re.sub(r"<[^>]+>", "", text)))
        return f'<h2 id="{sid}"{m.group(1)}>{text}</h2>'

    body = re.sub(r"<h2([^>]*)>(.*?)</h2>", h2, body, flags=re.S)
    if "{{" in body:
        raise SystemExit("unexpanded token: " + body[body.index("{{"):][:60])
    return body, toc


def toc_html(toc):
    if not toc:
        return ""
    items = "".join(f'<li><a href="#{i}">{E(t)}</a></li>' for i, t in toc)
    return f'<nav class="toc" aria-label="On this page"><h2>On this page</h2><ol>{items}</ol></nav>'


def faq_html(faq, heading="Frequently asked questions"):
    if not faq:
        return ""
    items = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in faq)
    return (f'<section class="section section--cream" id="faq"><div class="wrap"><div class="section-head center reveal">'
            f'<span class="eyebrow">Questions</span><h2>{heading}</h2></div><div class="faq reveal">{items}</div></div></section>')


# ---------------------------------------------------------------- schema
ORG = {
    "@type": "Organization", "@id": SITE["origin"] + "/#org", "name": SITE["name"], "url": SITE["origin"] + "/",
    "logo": {"@type": "ImageObject", "url": SITE["origin"] + "/assets/img/logo-512.png", "width": 512, "height": 512},
    "email": SITE["email"],
    "contactPoint": {"@type": "ContactPoint", "email": SITE["email"], "contactType": "customer support"},
}
WEBSITE = {"@type": "WebSite", "@id": SITE["origin"] + "/#website", "url": SITE["origin"] + "/", "name": SITE["name"],
           "publisher": {"@id": SITE["origin"] + "/#org"}, "inLanguage": "en-US"}


def crumbs_schema(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": url(p)} for i, (n, p) in enumerate(trail)]}


def faq_schema(faq):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}


def crumbs_html(trail):
    lis = []
    for i, (n, p) in enumerate(trail):
        if i == len(trail) - 1:
            lis.append(f'<li aria-current="page">{E(n)}</li>')
        else:
            lis.append(f'<li><a href="{p}">{E(n)}</a></li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(lis)}</ol></nav>'


# ---------------------------------------------------------------- layout
def full_title(t):
    suffix = " | Dukora Idea"
    return t + suffix if len(t + suffix) <= 65 else t


def layout(*, path, title, description, body, image="mason-jar-fairy-lights", schema=(), og_type="website",
           extra_head="", solid_header=False, progress=False, noindex=False, raw_title=False, image_alt=None, preload=None):
    canonical = url(path)
    t = title if raw_title else full_title(title)
    graph = [ORG, WEBSITE] + [s for s in schema if s]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    ld = ld.replace("</", "<\\/")
    nav = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if (path == h or (h != "/" and path.startswith(h + "/"))) else ""}>{n}</a></li>'
        for n, h in NAV)
    w, h = IMG[image]
    robots = '<meta name="robots" content="noindex, follow">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
{GTAG}
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(t)}</title>
<meta name="description" content="{E(description)}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE['origin']}/assets/img/{image}.webp">
<meta property="og:image:width" content="{w}">
<meta property="og:image:height" content="{h}">
<meta property="og:image:type" content="image/webp">
<meta property="og:image:alt" content="{E(image_alt or title)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(title)}">
<meta name="twitter:description" content="{E(description)}">
<meta name="twitter:image" content="{SITE['origin']}/assets/img/{image}.webp">
<meta name="twitter:image:alt" content="{E(image_alt or title)}">
<meta name="theme-color" content="#0a0d1c">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-96.png" sizes="96x96" type="image/png">
<link rel="icon" href="/favicon-48.png" sizes="48x48" type="image/png">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="alternate" type="application/atom+xml" title="Dukora Idea blog" href="{SITE['origin']}/blogs/blog.atom">
<link rel="sitemap" type="application/xml" href="{SITE['origin']}/sitemap.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;1,9..144,500;1,9..144,600&family=Manrope:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={ASSET_V}">
{f'<link rel="preload" as="image" href="/assets/img/{preload}.webp" fetchpriority="high">' if preload else ''}
{extra_head}<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
{'<div class="reading-progress" aria-hidden="true"></div>' if progress else ''}
<header class="site-header{' is-solid' if solid_header else ''}">
<div class="wrap">
<a class="logo" href="/" aria-label="Dukora Idea home">{logo_svg('h')}<span>Dukora<small>Idea</small></span></a>
<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="main-nav" aria-label="Open menu"><span></span><span></span><span></span></button>
<nav class="main-nav" id="main-nav" aria-label="Main">
<ul>{nav}<li class="nav-cta"><a href="/pages/contact">Say hello</a></li></ul>
<div class="nav-drawer-extra"><p>Lighting project questions? <a href="mailto:{SITE['email']}">{SITE['email']}</a></p></div>
</nav>
</div>
</header>
<main id="main">
{body}
</main>
{footer()}
<button class="to-top" type="button" aria-label="Back to top">{ICONS['up']}</button>
<script src="/assets/js/site.js?v={ASSET_V}" defer></script>
</body>
</html>
'''


def footer():
    fairy = "".join(f'<li><a href="/products/{p["slug"]}">{E(p["name"])}</a></li>' for p in PRODUCTS if p["collection"] != "smart-lights")
    smart = "".join(f'<li><a href="/products/{p["slug"]}">{E(p["name"])}</a></li>' for p in PRODUCTS if p["collection"] == "smart-lights")
    return f'''<footer class="site-footer">
<div class="wrap">
<div class="footer-grid">
<div class="about">
<a class="logo" href="/" aria-label="Dukora Idea home">{logo_svg('f')}<span>Dukora<small>Idea</small></span></a>
<p style="margin-top:18px">{SITE['tagline']} Fairy lights, LED strips, smart bulbs and the little projects that make a room glow.</p>
<p><a href="mailto:{SITE['email']}">{SITE['email']}</a></p>
</div>
<div><h3>Fairy &amp; String Lights</h3><ul>{fairy}</ul></div>
<div><h3>Smart Lights</h3><ul>{smart}<li><a href="/collections/all">All light guides</a></li></ul>
<h3 style="margin-top:28px">Light Tools</h3><ul>{''.join(f'<li><a href="/pages/light-tools#{TOOL_ANCHOR[k]}">{n}</a></li>' for k, n, _ in TOOLS)}</ul></div>
<div><h3>Explore</h3><ul><li><a href="/blogs/blog">Ideas &amp; Blog</a></li><li><a href="/blogs/blog/create-your-mason-jar-fairy-lights-in-5-minutes">Mason jar fairy lights</a></li><li><a href="/pages/about-us">About Dukora</a></li><li><a href="/pages/contact">Contact</a></li><li><a href="/policies/privacy-policy">Privacy policy</a></li><li><a href="/policies/terms-of-service">Terms of service</a></li><li><a href="/sitemap.xml">Sitemap</a></li></ul></div>
</div>
<div class="footer-bottom"><span>&copy; <span data-year>{date.today().year}</span> Dukora Idea. Made for night owls and fairy-light hoarders.</span><span>Ideas and guides only: we don't sell lights.</span></div>
</div>
</footer>'''


# ---------------------------------------------------------------- cards
def post_card(p, small=True):
    return f'''<a class="card reveal" href="/blogs/blog/{p['slug']}" data-cat="{slugify(p['category'])}">
<div class="card-media">{img(p['image'], p['image_alt'], sizes="(max-width: 620px) 100vw, (max-width: 900px) 50vw, 380px", small=small)}</div>
<div class="card-body"><div class="card-meta"><span class="chip">{E(p['category'])}</span><span>{max(3, round(words(p['body']) / 220))} min read</span></div>
<h3>{E(p['title'])}</h3><p>{E(p['excerpt'])}</p><span class="more">Read the idea &rarr;</span></div></a>'''


def guide_card(p):
    return f'''<a class="card card--guide reveal" href="/products/{p['slug']}">
<div class="card-media">{img(p['image'], p['image_alt'], sizes="(max-width: 620px) 100vw, (max-width: 1080px) 50vw, 290px", small=True)}</div>
<div class="card-body"><span class="tagline">{E(COLLECTIONS.get(p['collection'], {'title': 'Decor'})['title'] if p['collection'] != 'decor' else 'Decor')}</span>
<h3>{E(p['name'])}</h3><p>{E(p['tagline'])}</p><span class="more">Open the guide &rarr;</span></div></a>'''


def firefly_canvas():
    return '<canvas class="fireflies" aria-hidden="true"></canvas>'


def light_string_svg():
    bulbs = []
    colors = ["#ffc56b", "#ff8a5b", "#9d8cff", "#5ee6c9", "#ffd590"]
    n = 22
    for i in range(1, n):
        x = i * 1000 / n
        y = 10 + 50 * (1 - ((x - 500) / 500) ** 2) if True else 0
        y = 10 + 42 * (1 - ((x % 500 - 250) / 250) ** 2)
        c = colors[i % len(colors)]
        bulbs.append(f'<g class="bulb" style="animation-delay:{(i * 0.37) % 3:.2f}s"><line x1="{x:.0f}" y1="{y:.0f}" x2="{x:.0f}" y2="{y + 8:.0f}" stroke="rgba(255,255,255,.25)"/>'
                     f'<ellipse cx="{x:.0f}" cy="{y + 14:.0f}" rx="4.5" ry="6.5" fill="{c}" style="filter:drop-shadow(0 0 6px {c})"/></g>')
    return ('<div class="light-string" aria-hidden="true"><svg viewBox="0 0 1000 90" preserveAspectRatio="none">'
            '<path class="wire" d="M0 10 Q250 94 500 10 Q750 94 1000 10"/>' + "".join(bulbs) + "</svg></div>")


# ---------------------------------------------------------------- pages
PAGES = {}  # path -> (html, lastmod, priority)


def emit(path, doc, lastmod=TODAY, priority="0.6", sitemap=True, images=()):
    PAGES[path] = (doc, lastmod, priority, sitemap, list(images))


def figs_in(body):
    """(image, alt) pairs for every {{fig:...}} token in a content body (for the image sitemap)."""
    out = []
    for m in re.finditer(r"\{\{fig:([^}|]+)\|([^}|]*)", body):
        out.append((m.group(1).strip(), m.group(2).strip()))
    return out


def page_hero(title, lead, image, trail, eyebrow=None, extra=""):
    return f'''<section class="page-hero">
<div class="bg">{img(image, "", sizes="100vw", eager=True)}</div>{firefly_canvas()}
<div class="wrap">{crumbs_html(trail)}{f'<span class="eyebrow">{E(eyebrow)}</span>' if eyebrow else ''}
<h1>{title}</h1>{f'<p class="lead">{lead}</p>' if lead else ''}{extra}</div></section>'''


def build_home():
    top = POST_BY["create-your-mason-jar-fairy-lights-in-5-minutes"]
    latest = [p for p in POSTS if p["slug"] != top["slug"]][:6]
    featured_guides = [PROD_BY[s] for s in ("outdoor-fairy-lights", "wifi-smart-led-strip-lights", "battery-operated-fairy-lights", "smart-led-light-bulbs")]
    fairy_n = sum(1 for p in PRODUCTS if p["collection"] != "smart-lights")
    smart_n = sum(1 for p in PRODUCTS if p["collection"] == "smart-lights")
    rooms = [
        ("bedroom", "Bedroom", "warm-bedroom-lighting", "A softly lit bedroom with warm lamp light",
         [("Headboard halo", "drape 10 to 20 ft of warm white copper-wire lights behind a sheer curtain."),
          ("Bedside jar", "a mason jar of micro lights on a 6-hour timer makes a gentle night light."),
          ("Under-bed glow", "an LED strip at 2,200K on 20% brightness for midnight trips without glare.")]),
        ("living", "Living room", "fairy-light-photo-wall", "Photos clipped to fairy lights on a wall",
         [("Photo wall", "clip prints to fairy lights in loose swags; it's renter friendly with removable hooks."),
          ("TV bias light", "a USB LED strip behind the screen cuts eye strain during movie nights."),
          ("Sofa glow", "a strip tucked under the couch frame makes the whole room feel bigger.")]),
        ("patio", "Patio & garden", "garden-string-lights-night", "A garden patio lit by string lights through trees",
         [("Festoon canopy", "run strands from a center pole to the edges for a café-style ceiling."),
          ("Tree wraps", "spiral waterproof fairy lights up trunks, about 6 inches apart."),
          ("Solar jars", "line a path with jars of solar fairy lights; no cables to trip on.")]),
        ("party", "Parties & weddings", "wedding-reception-lights", "Guests at an outdoor reception under string lights",
         [("Overhead swags", "zigzag festoon strands 8 to 9 ft above the dance floor."),
          ("Table runners", "battery micro lights woven through greenery down the table."),
          ("Glowing backdrop", "a curtain of fairy lights behind sheer fabric for photos.")]),
    ]
    tabs = "".join(f'<button class="tab-btn" type="button" role="tab" id="tab-{k}" aria-controls="panel-{k}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{n}</button>' for i, (k, n, *_r) in enumerate(rooms))
    panels = ""
    for i, (k, n, im, alt, ideas) in enumerate(rooms):
        lis = "".join(f"<li><b>{E(a)}:</b> {E(b)}</li>" for a, b in ideas)
        panels += (f'<div class="tab-panel" role="tabpanel" id="panel-{k}" aria-labelledby="tab-{k}"{"" if i == 0 else " hidden"}>'
                   f'{img(im, alt, sizes="(max-width: 900px) 100vw, 640px", small=True)}<div><h3>{n} glow ideas</h3><ul>{lis}</ul>'
                   f'<a class="btn" href="/blogs/blog">More ideas {ICONS["arrow"]}</a></div></div>')
    faq = [
        ("What is Dukora Idea?", "Dukora Idea is a home for DIY lighting ideas: step-by-step projects, in-depth light guides and free calculators for fairy lights, string lights, LED strips and smart bulbs."),
        ("Do you sell lights?", "No. Dukora is an ideas and guides site. Our light guides explain what to look for so you can choose well wherever you shop."),
        ("What's the easiest fairy light project for beginners?", "A mason jar of battery-operated copper-wire fairy lights. It takes about five minutes, needs no tools, and works as a night light, centerpiece or gift."),
        ("Are warm white or cool white fairy lights better?", "For cozy rooms, warm white (about 2,700K or lower) almost always looks better. Cool white suits icy holiday themes and task areas. Try our color and mood picker to compare."),
        ("How long do battery fairy lights last?", "A typical 100-LED string on 3×AA alkaline batteries runs very roughly 25 to 40 hours steady. Timers and twinkle modes stretch that across many nights; our battery calculator gives an estimate for your setup."),
    ]
    tool_cards = "".join(f'<a class="tool-card reveal" style="--rd:{i * .08}s" href="/pages/light-tools#{TOOL_ANCHOR[k]}"><span class="ico">{ICONS[k]}</span><h3>{n}</h3><p>{d}</p></a>' for i, (k, n, d) in enumerate(TOOLS))
    marquee_words = ["Mason jar lights", "Fairy light walls", "Smart LED strips", "Patio canopies", "Starlight bottles", "Wedding glow", "Battery garlands", "Color moods", "Under-sofa light"]
    mq = "".join(f"<span>{w}</span>" for w in marquee_words * 2)
    body = f'''<section class="hero dark">
{firefly_canvas()}<div class="spotlight" aria-hidden="true"></div>{light_string_svg()}
<div class="wrap hero-grid">
<div class="reveal">
<span class="eyebrow">DIY lighting ideas &amp; light guides</span>
<h1>Light up the <span class="glow-text">little things</span>.</h1>
<p class="lead">Dukora Idea is your workshop for fairy lights, string lights and smart LEDs: five-minute projects, honest light guides and interactive tools that help every corner of your home glow.</p>
<div class="hero-actions"><a class="btn" href="/blogs/blog">Explore ideas {ICONS['arrow']}</a><a class="btn btn--ghost" href="/pages/light-tools">Try the light tools</a></div>
<div class="hero-stats"><div><strong>{len(POSTS)}</strong><span>DIY ideas &amp; guides</span></div><div><strong>{len(PRODUCTS)}</strong><span>in-depth light guides</span></div><div><strong>4</strong><span>free interactive tools</span></div></div>
</div>
<div class="collage reveal" style="--rd:.15s">
<figure class="c1">{img('mason-jar-fairy-lights', 'Mason jar filled with glowing fairy lights at night', sizes="(max-width: 900px) 60vw, 340px", eager=True, small=True)}</figure>
<figure class="c2">{img('garden-string-lights-night', 'Garden patio lit with string lights', sizes="(max-width: 900px) 50vw, 300px", eager=True, small=True)}</figure>
<figure class="c3">{img('smart-home-bulbs', 'Smart color bulbs glowing pink next to a smartphone', sizes="(max-width: 900px) 50vw, 290px", small=True)}</figure>
<div class="badge"><b>5 min</b> mason jar fairy lights &rarr;</div>
</div>
</div>
</section>
<div class="marquee" aria-hidden="true"><div class="marquee-track">{mq}</div></div>

<section class="section">
<div class="wrap">
<div class="section-head reveal"><span class="eyebrow">Start with a glow</span><h2>Pick your kind of light</h2><p>Whether it's a jar of tiny copper-wire lights or a Wi-Fi LED strip that changes with your playlist, start with the guide that fits your project.</p></div>
<div class="tiles">
<a class="tile reveal" href="/collections/fairy-lights">{img('hands-holding-fairy-lights', 'Hands holding a bundle of warm fairy lights', sizes="(max-width: 900px) 100vw, 400px", small=True)}<span class="count">{fairy_n} guides</span><div class="tile-body"><h3>Fairy &amp; string lights</h3><p>Battery packs, copper wire, timers, garlands and waterproof strings.</p></div></a>
<a class="tile reveal" style="--rd:.1s" href="/collections/smart-lights">{img('gaming-rgb-setup', 'Desk setup glowing with RGB LED lighting', sizes="(max-width: 900px) 100vw, 400px", small=True)}<span class="count">{smart_n} guides</span><div class="tile-body"><h3>Smart LED lights</h3><p>LED strip lights, color bulbs and Wi-Fi controllers for Alexa and Google Home.</p></div></a>
<a class="tile reveal" style="--rd:.2s" href="/blogs/blog/most-significant-wedding-celebration-motif-patterns">{img('wedding-table-garden', 'Wedding table on a lawn under string lights', sizes="(max-width: 900px) 100vw, 400px", small=True)}<span class="count">Ideas</span><div class="tile-body"><h3>Events &amp; outdoors</h3><p>Patio canopies, wedding motifs and party lighting that photographs beautifully.</p></div></a>
</div>
</div>
</section>

<section class="section section--cream">
<div class="wrap split">
<div class="reveal">
<span class="eyebrow">Most-loved project</span>
<h2>Mason jar fairy lights in five minutes</h2>
<p>Our most popular idea for years, and still the fastest way to fall in love with fairy lights. One jar, one string of micro LEDs, zero tools.</p>
<ol class="mini-steps">
<li><div><strong>Pick a clear jar</strong><span>Wide-mouth jars make it easy to feed the lights in.</span></div></li>
<li><div><strong>Feed the lights in loosely</strong><span>Start with the tip, then let the wire coil on its own for a natural sparkle.</span></div></li>
<li><div><strong>Hide the battery pack</strong><span>Tuck it under the lid, inside a burlap wrap or in a hollow cork.</span></div></li>
</ol>
<a class="btn btn--dark" href="/blogs/blog/{top['slug']}">See the full project {ICONS['arrow']}</a>
</div>
<div class="split-media reveal" style="--rd:.1s"><div class="glow-ring" aria-hidden="true"></div>{img('jar-fairy-lights-twilight', 'Glass jar of fairy lights glowing at twilight', sizes="(max-width: 900px) 100vw, 560px", small=True)}</div>
</div>
</section>

<section class="section">
<div class="wrap">
<div class="section-head section-head--row reveal"><div><span class="eyebrow">Light guides</span><h2>Know your lights before you buy</h2><p>Plain-English guides to what matters: power, wire, waterproofing, timers, apps and where each light looks its best.</p></div><a class="link-arrow" href="/collections/all">All {len(PRODUCTS)} guides {ICONS['arrow']}</a></div>
<div class="grid grid-4">{''.join(guide_card(p) for p in featured_guides)}</div>
</div>
</section>

<section class="section dark" style="overflow:hidden">
<div class="wrap">
<div class="section-head center reveal"><span class="eyebrow">Interactive</span><h2>Play with light before you buy a single bulb</h2><p>Four free tools to plan battery life, LED strip power, color temperature and patio layouts.</p></div>
<div class="reveal">{tool_html('color', tid='home-color')}</div><div class="tool-cards" style="margin-top:28px">{tool_cards}</div>
</div>
</section>

<section class="section">
<div class="wrap">
<div class="section-head section-head--row reveal"><div><span class="eyebrow">Fresh ideas</span><h2>Latest from the blog</h2></div><a class="link-arrow" href="/blogs/blog">All ideas {ICONS['arrow']}</a></div>
<div class="grid grid-3">{''.join(post_card(p) for p in latest)}</div>
</div>
</section>

<section class="section dark">
<div class="wrap" data-tabs>
<div class="section-head reveal"><span class="eyebrow">Room by room</span><h2>Glow ideas for every space</h2></div>
<div class="tabs reveal" role="tablist" aria-label="Rooms">{tabs}</div>
<div class="reveal">{panels}</div>
</div>
</section>

{faq_html(faq, "Good to know")}

<section class="section">
<div class="wrap"><div class="cta-band reveal">
<span class="eyebrow">Got a lighting project?</span>
<h2>Tell us what you're making and we'll help you light it.</h2>
<p>Stuck on a power supply, a battery pack that won't hide or a patio that needs a plan? Send us a note and we'll point you to the right guide.</p>
<div class="cta-actions"><a class="btn" href="/pages/contact">{ICONS['mail']} Contact Dukora</a><a class="btn btn--ghost" href="mailto:{SITE['email']}">{SITE['email']}</a></div>
</div></div>
</section>'''
    doc = layout(path="/", title="Dukora Idea: DIY Fairy Light & Smart LED Lighting Ideas", raw_title=True,
                 description="DIY lighting ideas, fairy light projects and smart LED guides. Make mason jar fairy lights, plan patio string lights and size LED strips with free tools.",
                 body=body, image="mason-jar-fairy-lights",
                 schema=[faq_schema(faq), {"@type": "WebPage", "@id": url("/") + "#webpage", "url": url("/"), "name": "Dukora Idea", "isPartOf": {"@id": SITE["origin"] + "/#website"}}])
    emit("/", doc, priority="1.0", images=[("mason-jar-fairy-lights", "Mason jar filled with glowing fairy lights at night"),
                                           ("garden-string-lights-night", "Garden patio lit with string lights"),
                                           ("jar-fairy-lights-twilight", "Glass jar of fairy lights glowing at twilight")])


def build_post(p):
    body, toc = render_body(p["body"])
    path = f"/blogs/blog/{p['slug']}"
    trail = [("Home", "/"), ("Blog", "/blogs/blog"), (p["title"], path)]
    mins = max(3, round(words(p["body"]) / 220))
    meta = (f'<div class="post-meta"><span class="chip">{E(p["category"])}</span><span>Published {fmt_date(p["published"])}</span>'
            f'<span>Updated {fmt_date(p["updated"])}</span><span>{mins} min read</span></div>')
    related = [POST_BY[s] for s in p.get("related", []) if s in POST_BY][:3]
    prods = [PROD_BY[s] for s in p.get("products", []) if s in PROD_BY][:3]
    tool_kinds = re.findall(r'data-tool="(\w+)"', body)
    side_tool = next((t for t in TOOLS if t[0] not in tool_kinds), TOOLS[0])
    hero_fig = figure(p["image"], p["image_alt"], "")
    hero_fig = hero_fig.replace("<figcaption></figcaption>", "")
    html_body = page_hero(E(p["title"]), "", p["image"], trail, extra=meta) + f'''
<section class="section"><div class="wrap article-layout">
<article class="prose">{body}</article>
<aside class="sidebar">{toc_html(toc)}
<div class="side-card"><h3>{side_tool[1]}</h3><p>{side_tool[2]}</p><a class="btn" href="/pages/light-tools#{TOOL_ANCHOR[side_tool[0]]}">Open the tool {ICONS['arrow']}</a></div>
</aside></div></section>
{faq_html(p.get('faq'))}
{f'<section class="section"><div class="wrap"><div class="section-head reveal"><span class="eyebrow">Light guides</span><h2>Lights for this idea</h2></div><div class="grid grid-3">{"".join(guide_card(x) for x in prods)}</div></div></section>' if prods else ''}
<section class="section section--cream"><div class="wrap"><div class="section-head section-head--row reveal"><div><span class="eyebrow">Keep glowing</span><h2>More ideas you'll like</h2></div><a class="link-arrow" href="/blogs/blog">All ideas {ICONS['arrow']}</a></div>
<div class="grid grid-3">{''.join(post_card(x) for x in related)}</div></div></section>'''
    w, h = IMG[p["image"]]
    schema = [
        {"@type": "BlogPosting", "@id": url(path) + "#article", "headline": p["title"], "description": p["description"],
         "image": {"@type": "ImageObject", "url": f"{SITE['origin']}/assets/img/{p['image']}.webp", "width": w, "height": h},
         "datePublished": p["published"], "dateModified": p["updated"], "author": {"@type": "Organization", "name": SITE["name"], "url": SITE["origin"] + "/"},
         "publisher": {"@id": SITE["origin"] + "/#org"}, "mainEntityOfPage": url(path), "articleSection": p["category"],
         "keywords": p["keyword"], "wordCount": words(p["body"]), "inLanguage": "en-US"},
        crumbs_schema(trail),
        faq_schema(p["faq"]) if p.get("faq") else None,
    ]
    doc = layout(path=path, title=p["meta_title"], description=p["description"], body=html_body, image=p["image"],
                 schema=schema, og_type="article", progress=True, image_alt=p["image_alt"],
                 extra_head=(f'<meta property="article:published_time" content="{p["published"]}">\n'
                             f'<meta property="article:modified_time" content="{p["updated"]}">\n'
                             f'<meta property="article:section" content="{E(p["category"])}">\n'
                             f'<meta property="article:tag" content="{E(p["keyword"])}">\n'))
    emit(path, doc, lastmod=p["updated"], priority="0.9" if p["slug"].startswith("create-your-mason") else "0.7",
         images=[(p["image"], p["image_alt"])] + figs_in(p["body"]))


def build_product(p):
    body, toc = render_body(p["body"])
    path = f"/products/{p['slug']}"
    coll = "smart-lights" if p["collection"] == "smart-lights" else "fairy-lights"
    trail = [("Home", "/"), (COLLECTIONS[coll]["title"], f"/collections/{coll}"), (p["name"], path)]
    pics = [p["image"]] + [g for g in p.get("gallery", []) if g in IMG][:3]
    thumbs = "".join(
        f'<button type="button" aria-pressed="{"true" if i == 0 else "false"}" data-src="/assets/img/{g}.webp" data-alt="{E(p["image_alt"] if i == 0 else p["name"] + " idea")}" aria-label="Show photo {i + 1}">'
        f'<img src="/assets/img/{g}-800.webp" alt="" width="84" height="84" loading="lazy"></button>' for i, g in enumerate(pics))
    hl = "".join(f"<li>{E(h)}</li>" for h in p["highlights"])
    specs = "".join(f"<div><dt>{E(a)}</dt><dd>{E(b)}</dd></div>" for a, b in p["specs"])
    tool_kinds = re.findall(r'data-tool="(\w+)"', body)
    jump_tool = f'<a class="btn btn--ghost" href="#{TOOL_ANCHOR[tool_kinds[0]]}">Try the calculator</a>' if tool_kinds else ""
    rel_p = [PROD_BY[s] for s in p.get("related_products", []) if s in PROD_BY][:3]
    rel_b = [POST_BY[s] for s in p.get("related_posts", []) if s in POST_BY][:3]
    side_tool = next((t for t in TOOLS if t[0] not in tool_kinds), TOOLS[0])
    html_body = f'''<section class="guide-hero dark">{firefly_canvas()}
<div class="wrap guide-grid">
<div data-gallery class="reveal"><div class="gallery-main">{img(p['image'], p['image_alt'], sizes="(max-width: 900px) 100vw, 560px", eager=True)}</div>
<div class="gallery-thumbs">{thumbs}</div></div>
<div class="reveal" style="--rd:.1s">{crumbs_html(trail)}<span class="eyebrow">Dukora light guide</span>
<h1>{E(p['title'])}</h1><p class="tagline">{E(p['tagline'])}</p>
<ul class="highlights">{hl}</ul>
<div class="jump"><a class="btn" href="#guide">Read the guide {ICONS['arrow']}</a>{jump_tool}<a class="btn btn--ghost" href="#specs">What to look for</a></div>
</div></div></section>
<section id="specs" style="scroll-margin-top:90px"><div class="wrap"><div class="specs-card reveal"><span class="eyebrow">Checklist</span><h2 style="font-size:clamp(1.5rem,2.6vw,2rem)">What to look for in {E(p['name'].lower())}</h2><dl class="specs">{specs}</dl></div></div></section>
<section class="section" id="guide" style="scroll-margin-top:60px"><div class="wrap article-layout">
<article class="prose">{body}</article>
<aside class="sidebar">{toc_html(toc)}
<div class="side-card"><h3>Questions about {E(p['name'].lower())}?</h3><p>Tell us about your space and we'll point you to the right setup.</p><a class="btn" href="/pages/contact">Ask Dukora {ICONS['arrow']}</a></div>
<div class="side-card"><h3>{side_tool[1]}</h3><p>{side_tool[2]}</p><a class="btn" href="/pages/light-tools#{TOOL_ANCHOR[side_tool[0]]}">Open the tool {ICONS['arrow']}</a></div>
</aside></div></section>
{faq_html(p.get('faq'))}
<section class="section"><div class="wrap"><div class="section-head section-head--row reveal"><div><span class="eyebrow">Related light guides</span><h2>Pairs well with</h2></div><a class="link-arrow" href="/collections/all">All guides {ICONS['arrow']}</a></div>
<div class="grid grid-3">{''.join(guide_card(x) for x in rel_p)}</div></div></section>
<section class="section section--cream"><div class="wrap"><div class="section-head reveal"><span class="eyebrow">Projects</span><h2>Ideas using {E(p['name'].lower())}</h2></div>
<div class="grid grid-3">{''.join(post_card(x) for x in rel_b)}</div></div></section>'''
    w, h = IMG[p["image"]]
    schema = [
        {"@type": "Article", "@id": url(path) + "#guide", "headline": p["title"], "description": p["description"],
         "image": {"@type": "ImageObject", "url": f"{SITE['origin']}/assets/img/{p['image']}.webp", "width": w, "height": h},
         "dateModified": p.get("updated", TODAY), "datePublished": "2021-09-01", "author": {"@type": "Organization", "name": SITE["name"]},
         "publisher": {"@id": SITE["origin"] + "/#org"}, "mainEntityOfPage": url(path), "about": p["keyword"], "inLanguage": "en-US"},
        crumbs_schema(trail),
        faq_schema(p["faq"]) if p.get("faq") else None,
    ]
    doc = layout(path=path, title=p["meta_title"], description=p["description"], body=html_body, image=p["image"], schema=schema,
                 og_type="article", image_alt=p["image_alt"],
                 extra_head=f'<meta property="article:modified_time" content="{p.get("updated", TODAY)}">\n')
    emit(path, doc, lastmod=p.get("updated", TODAY), priority="0.9" if p["slug"] in ("outdoor-fairy-lights", "wifi-smart-led-strip-lights") else "0.8",
         images=[(p["image"], p["image_alt"])] + [(g, p["name"]) for g in p.get("gallery", []) if g in IMG] + figs_in(p["body"]))


def build_collection(key):
    c = COLLECTIONS[key]
    path = f"/collections/{key}"
    items = [p for p in PRODUCTS if p["collection"] in c["members"]]
    trail = [("Home", "/"), (c["title"], path)]
    if key == "smart-lights":
        posts = [p for p in POSTS if p["category"] == "Smart Lighting"][:6]
    elif key == "fairy-lights":
        posts = [p for p in POSTS if p["category"] in ("DIY Projects", "Decor Ideas")][:6]
    else:
        posts = POSTS[:6]
    others = "".join(f'<a class="btn btn--ghost" href="/collections/{k}">{E(v["title"])}</a>' for k, v in COLLECTIONS.items() if k != key)
    body = page_hero(E(c["h1"]), E(c["lead"]), c["image"], trail, eyebrow=f"{len(items)} light guides",
                     extra=f'<div class="hero-actions">{others}</div>') + f'''
<section class="section"><div class="wrap"><div class="grid grid-3">{''.join(guide_card(p) for p in items)}</div></div></section>
<section class="section dark"><div class="wrap"><div class="section-head center reveal"><span class="eyebrow">Plan it first</span><h2>Free light tools</h2><p>Check battery life, LED strip power, color moods and patio layouts before you hang a single strand.</p></div>
<div class="tool-cards">{''.join(f'<a class="tool-card reveal" href="/pages/light-tools#{TOOL_ANCHOR[k]}"><span class="ico">{ICONS[k]}</span><h3>{n}</h3><p>{d}</p></a>' for k, n, d in TOOLS)}</div></div></section>
<section class="section section--cream"><div class="wrap"><div class="section-head section-head--row reveal"><div><span class="eyebrow">Ideas</span><h2>Projects to try</h2></div><a class="link-arrow" href="/blogs/blog">All ideas {ICONS['arrow']}</a></div>
<div class="grid grid-3">{''.join(post_card(p) for p in posts)}</div></div></section>'''
    schema = [{"@type": "CollectionPage", "@id": url(path) + "#page", "url": url(path), "name": c["h1"], "description": c["description"],
               "mainEntity": {"@type": "ItemList", "itemListElement": [
                   {"@type": "ListItem", "position": i + 1, "url": url(f"/products/{p['slug']}"), "name": p["name"]} for i, p in enumerate(items)]}},
              crumbs_schema(trail)]
    emit(path, layout(path=path, title=c["meta_title"], description=c["description"], body=body, image=c["image"], schema=schema), priority="0.8")


def build_blog_index():
    path = "/blogs/blog"
    trail = [("Home", "/"), ("Blog", path)]
    feat = POST_BY["create-your-mason-jar-fairy-lights-in-5-minutes"]
    rest = [p for p in POSTS if p is not feat]
    cats = [c for c in CATEGORIES if any(p["category"] == c for p in rest)]
    filters = '<button class="filter-btn" type="button" data-cat="all" aria-pressed="true">All ideas</button>' + "".join(
        f'<button class="filter-btn" type="button" data-cat="{slugify(c)}" aria-pressed="false">{E(c)}</button>' for c in cats)
    body = page_hero('Ideas &amp; <span class="glow-text">DIY lighting</span> blog',
                     "Projects, decor ideas and smart lighting how-tos. Everything we've learned from years of untangling fairy lights.",
                     "fairy-light-photo-wall", trail, eyebrow=f"{len(POSTS)} ideas and counting") + f'''
<section class="section"><div class="wrap">
<a class="feature-post reveal" href="/blogs/blog/{feat['slug']}"><div class="media">{img(feat['image'], feat['image_alt'], sizes="(max-width: 900px) 100vw, 660px", small=True)}</div>
<div class="body"><span class="eyebrow">Reader favorite</span><h2>{E(feat['title'])}</h2><p>{E(feat['excerpt'])}</p><span class="btn" style="align-self:start">Start the project {ICONS['arrow']}</span></div></a>
<div class="filters reveal" data-filters="post-grid" role="group" aria-label="Filter by category">{filters}</div>
<div class="grid grid-3" id="post-grid">{''.join(post_card(p) for p in rest)}</div>
</div></section>'''
    schema = [{"@type": "Blog", "@id": url(path) + "#blog", "url": url(path), "name": "Dukora Idea Blog", "publisher": {"@id": SITE["origin"] + "/#org"},
               "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": url(f"/blogs/blog/{p['slug']}"), "datePublished": p["published"]} for p in POSTS]},
              crumbs_schema(trail)]
    emit(path, layout(path=path, title="DIY Lighting Ideas & Fairy Light Blog", description="DIY fairy light projects, decor ideas and smart LED how-tos: mason jar lights, starlight bottles, patio string lights, LED strips, smart bulbs and more.",
                      body=body, image="fairy-light-photo-wall", schema=schema), priority="0.8")


def build_tools():
    path = "/pages/light-tools"
    trail = [("Home", "/"), ("Light Tools", path)]
    intro = {
        "battery": ("Battery life", "How long will battery fairy lights last?", "Pick your battery, LED count, mode and timer. The estimate updates as you go. Twinkle and fade modes use less power than steady-on, and rechargeable NiMH cells hold slightly less charge than alkaline but save money over a season.", ["/products/battery-operated-fairy-lights", "battery-operated fairy lights"], ["/blogs/blog/how-long-do-battery-fairy-lights-last", "fairy light battery guide"]),
        "strip": ("LED strips", "How big a power supply does my LED strip need?", "Enter the length and the watts per meter printed on the reel. We add 20% headroom (power supplies run cooler and last longer that way), round up to a common size and flag runs long enough to need power injection.", ["/products/wifi-smart-led-strip-lights", "smart LED strip lights"], ["/blogs/blog/how-to-cut-and-connect-led-strip-lights", "how to cut and connect strips"]),
        "color": ("Color & mood", "Which light color fits the mood?", "Color temperature is measured in kelvin: lower numbers are warm and candle-like, higher numbers are cool and daylight-like. Slide through the range or tap a mood to see how a room changes.", ["/products/smart-led-light-bulbs", "smart LED light bulbs"], ["/blogs/blog/led-strip-light-colors-meaning", "LED colors and moods"]),
        "patio": ("Outdoor", "How many string lights do I need for my patio?", "Set the size of your patio or deck and choose a pattern. The planner adds drape and the run to your outlet, then counts strands, bulbs and the hooks or posts you'll need.", ["/products/outdoor-string-lights", "waterproof string lights"], ["/blogs/blog/how-to-hang-outdoor-string-lights", "how to hang outdoor string lights"]),
    }
    secs = ""
    for i, (k, n, d) in enumerate(TOOLS):
        eb, h2, p, g, b = intro[k]
        secs += f'''<section class="section{' section--cream' if i % 2 else ''}" style="padding-block:70px"><div class="wrap">
<div class="section-head reveal"><span class="eyebrow">{eb}</span><h2>{h2}</h2><p>{p} Related: <a href="{g[0]}">{g[1]}</a> and <a href="{b[0]}">{b[1]}</a>.</p></div>
{tool_html(k, tid=TOOL_ANCHOR[k])}</div></section>'''
    jump = "".join(f'<a class="btn btn--ghost" href="#{TOOL_ANCHOR[k]}">{n}</a>' for k, n, _ in TOOLS)
    body = page_hero('Free <span class="glow-text">light tools</span>', "Four interactive calculators to plan battery life, LED strip power, color moods and patio string-light layouts. No sign-up, no downloads.",
                     "globe-string-lights", trail, eyebrow="Interactive", extra=f'<div class="hero-actions">{jump}</div>') + secs
    schema = [{"@type": "WebApplication", "name": n, "url": url(path) + "#" + TOOL_ANCHOR[k], "applicationCategory": "UtilitiesApplication",
               "operatingSystem": "Any", "description": d, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}} for k, n, d in TOOLS] + [crumbs_schema(trail)]
    emit(path, layout(path=path, title="Free Lighting Calculators & Planners", description="Free lighting tools: fairy light battery life calculator, LED strip power supply calculator, color temperature mood picker and patio string light planner.",
                      body=body, image="globe-string-lights", schema=schema), priority="0.8")


def build_about():
    path = "/pages/about-us"
    trail = [("Home", "/"), ("About", path)]
    body = page_hero('About <span class="glow-text">Dukora Idea</span>', "A small corner of the internet for people who can't walk past a string of fairy lights.", "cozy-fairy-lights", trail, eyebrow="Our story") + f'''
<section class="section"><div class="wrap split">
<div class="prose reveal">
<h2>Ideas that glow</h2>
<p>Dukora Idea started with fairy lights, LED strips and smart bulbs, and the readers who wanted to know what to do with them. The questions were always the same: how do I hide the battery pack? Why does my strip go pink at the end? How many strands do I need for the patio?</p>
<p>So that's what this site is for. We write step-by-step DIY projects, honest light guides that explain what actually matters (power, wire, waterproofing, timers, apps) and free tools that do the math for you.</p>
<h2>What you'll find here</h2>
<ul class="checklist"><li>Five-minute projects like <a href="/blogs/blog/create-your-mason-jar-fairy-lights-in-5-minutes">mason jar fairy lights</a></li><li>In-depth <a href="/collections/all">light guides</a> for every kind of light</li><li><a href="/pages/light-tools">Interactive calculators</a> for battery life, strips and patios</li><li>Room, party and <a href="/blogs/blog/most-significant-wedding-celebration-motif-patterns">wedding lighting ideas</a></li></ul>
<h2>How we write</h2>
<p>We don't sell lights, and nobody pays to appear in our guides. Numbers like battery life and power draw are typical ranges, not lab results, and we say so. If something here is wrong or out of date, <a href="/pages/contact">tell us</a> and we'll fix it.</p>
</div>
<div class="split-media reveal"><div class="glow-ring" aria-hidden="true"></div>{img('glowing-jar-hands', 'Hands holding a glowing jar of fairy lights', sizes="(max-width: 900px) 100vw, 560px", small=True)}</div>
</div></section>
<section class="section"><div class="wrap"><div class="cta-band reveal"><span class="eyebrow">Say hello</span><h2>Have an idea we should try?</h2><p>We love reader projects, questions and corrections.</p><div class="cta-actions"><a class="btn" href="/pages/contact">Contact us {ICONS['arrow']}</a></div></div></div></section>'''
    schema = [{"@type": "AboutPage", "url": url(path), "name": "About Dukora Idea", "about": {"@id": SITE["origin"] + "/#org"}}, crumbs_schema(trail)]
    emit(path, layout(path=path, title="About Dukora Idea", description="Dukora Idea shares DIY lighting ideas, honest fairy light and smart LED guides, and free calculators to help you light every corner of your home.",
                      body=body, image="cozy-fairy-lights", schema=schema), priority="0.5")


def build_contact():
    path = "/pages/contact"
    trail = [("Home", "/"), ("Contact", path)]
    topics = "".join(f"<option>{t}</option>" for t in ["A DIY lighting project", "Fairy lights", "LED strips & controllers", "Smart bulbs", "Outdoor & patio lights", "A correction", "Something else"])
    body = page_hero('Let\'s talk <span class="glow-text">light</span>', "Questions, project photos, corrections or ideas you'd like us to try. We read everything.", "hands-holding-fairy-lights", trail, eyebrow="Contact") + f'''
<section class="section"><div class="wrap split" style="align-items:start">
<div class="reveal">
<h2>Write to us</h2>
<p>The fastest way to reach Dukora is email:</p>
<p><a class="btn btn--dark" href="mailto:{SITE['email']}">{ICONS['mail']} {SITE['email']}</a></p>
<p style="margin-top:28px">Before you write, these might already have your answer:</p>
<ul class="checklist"><li><a href="/pages/light-tools#battery-calculator">Battery life calculator</a></li><li><a href="/pages/light-tools#strip-calculator">LED strip power calculator</a></li><li><a href="/blogs/blog/how-to-connect-alexa-to-led-strip-lights">Connecting Alexa to LED strips</a></li><li><a href="/blogs/blog/how-to-hang-outdoor-string-lights">Hanging outdoor string lights</a></li></ul>
<p style="margin-top:20px;color:var(--ink-2)">Please note: we're an ideas and guides site, so we can't help with orders, returns or warranties for lights bought elsewhere.</p>
</div>
<form class="form-card reveal" method="post" action="/contact" style="position:relative">
<div class="notice notice--ok" data-notice="sent" hidden>Thanks! Your message is on its way. We'll reply by email.</div>
<div class="notice notice--err" data-notice="error" hidden>Sorry, that didn't send. Please check the fields or email us directly at {SITE['email']}.</div>
<label for="cf-name">Your name</label><input id="cf-name" name="name" autocomplete="name" required maxlength="100">
<label for="cf-email">Email</label><input id="cf-email" name="email" type="email" autocomplete="email" required maxlength="150">
<label for="cf-topic">What's it about?</label><select id="cf-topic" name="topic">{topics}</select>
<label for="cf-msg">Message</label><textarea id="cf-msg" name="message" rows="6" required maxlength="5000"></textarea>
<div class="hp" aria-hidden="true"><label for="cf-web">Website</label><input id="cf-web" name="website" tabindex="-1" autocomplete="off"></div>
<button class="btn" type="submit">Send message {ICONS['arrow']}</button>
</form>
</div></section>
<script>(function(){{var s=new URLSearchParams(location.search).get("status");if(s){{var n=document.querySelector('[data-notice="'+s+'"]');if(n)n.hidden=false;}}}})();</script>'''
    schema = [{"@type": "ContactPage", "url": url(path), "name": "Contact Dukora Idea"}, crumbs_schema(trail)]
    emit(path, layout(path=path, title="Contact Dukora Idea", description="Contact Dukora Idea with lighting questions, DIY project photos or corrections. Email info@dukoraidea.com or use the form and we'll reply by email.",
                      body=body, image="hands-holding-fairy-lights", schema=schema), priority="0.4")


LEGAL = {
    "privacy-policy": ("Privacy Policy", "How Dukora Idea handles information: what we collect when you browse or contact us, cookies, third-party services and how to reach us about privacy.", [
        ("Who we are", f"Dukora Idea (dukoraidea.com) publishes DIY lighting ideas, light guides and free calculators. You can contact us at <a href=\"mailto:{SITE['email']}\">{SITE['email']}</a>."),
        ("Information we collect", "We don't run accounts, shops or comment sections, so we collect very little. If you use the contact form or email us, we receive your name, email address and message. Our web host keeps standard server logs (IP address, browser, pages requested, time) for security and troubleshooting."),
        ("How we use it", "We use your message only to reply to you. We don't sell, rent or share your information for marketing. Server logs are used to keep the site secure and working."),
        ("Cookies", "The site itself does not set tracking cookies. The calculators run entirely in your browser and don't send your inputs anywhere. Fonts are loaded from Google Fonts, which may receive your IP address as part of delivering them."),
        ("Retention", "We keep contact emails only as long as needed to answer and follow up, then delete them. Server logs are rotated by our host."),
        ("Your choices", "You can ask us to see, correct or delete any message you've sent us by emailing us. Residents of places with specific privacy rights (such as California or the EU/UK) can exercise those rights the same way."),
        ("Children", "This site is intended for a general audience and doesn't knowingly collect information from children under 13."),
        ("Changes", "We may update this policy as the site changes. The date below shows the latest revision."),
    ]),
    "terms-of-service": ("Terms of Service", "The terms for using dukoraidea.com: informational content, safety with electrical projects, intellectual property, calculators and liability.", [
        ("Using this site", "By using dukoraidea.com you agree to these terms. If you don't agree, please don't use the site."),
        ("Information only", "Our projects, guides and calculators are for general information. Results from the calculators are estimates. Always follow the instructions and ratings that come with your lights, batteries and power supplies."),
        ("Safety", "Lighting projects involve electricity, batteries and sometimes heat. Use low-voltage lights for DIY projects, never leave plug-in lights unattended in enclosed containers, keep button cells away from children, and use outdoor-rated products outdoors. If in doubt, ask a qualified electrician."),
        ("Intellectual property", "Text, design and code on this site belong to Dukora Idea unless noted. You may share links and short quotes with credit, but please don't republish whole articles."),
        ("No sales", "Dukora Idea doesn't sell products. Product types described in our guides are generic; we're not responsible for products you buy from other sellers."),
        ("Liability", "To the fullest extent allowed by law, Dukora Idea isn't liable for any loss or damage arising from use of the site or from following its content."),
        ("Contact", f"Questions about these terms? Email <a href=\"mailto:{SITE['email']}\">{SITE['email']}</a>."),
    ]),
}


def build_legal():
    for slug, (title, desc, secs) in LEGAL.items():
        path = f"/policies/{slug}"
        trail = [("Home", "/"), (title, path)]
        inner = "".join(f"<h2>{h}</h2><p>{t}</p>" for h, t in secs) + f"<p><em>Last updated {fmt_date(TODAY)}.</em></p>"
        body = page_hero(E(title), "", "copper-wire-fairy-lights-terrarium", trail) + f'<section class="section"><div class="wrap" style="max-width:820px"><div class="prose">{inner}</div></div></section>'
        emit(path, layout(path=path, title=title, description=desc, body=body, image="copper-wire-fairy-lights-terrarium", schema=[crumbs_schema(trail)]), priority="0.2")


def build_404():
    body = f'''<section class="hero dark" style="min-height:80svh">{firefly_canvas()}<div class="spotlight" aria-hidden="true"></div>
<div class="wrap" style="text-align:center;max-width:760px"><span class="eyebrow">Error 404</span>
<h1>This light <span class="glow-text">went out</span>.</h1>
<p class="lead" style="margin-inline:auto">The page you're looking for has moved or never existed. Try one of these instead.</p>
<div class="hero-actions" style="justify-content:center"><a class="btn" href="/">Back home {ICONS['arrow']}</a><a class="btn btn--ghost" href="/blogs/blog">Browse ideas</a><a class="btn btn--ghost" href="/collections/all">Light guides</a></div>
</div></section>'''
    emit("/404", layout(path="/404", title="Page not found", description="This page could not be found on Dukora Idea.", body=body, noindex=True), sitemap=False)


# ---------------------------------------------------------------- write
def write():
    if OUT.exists():
        shutil.rmtree(OUT)
    for path, (doc, *_r) in PAGES.items():
        f = OUT / "home.html" if path == "/" else OUT / (path.lstrip("/") + ".html")
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(doc, encoding="utf-8")
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for path, (_d, lastmod, prio, inc, images) in sorted(PAGES.items(), key=lambda kv: -float(kv[1][2])):
        if inc:
            imgs, seen = "", set()
            for name, _alt in images:
                if name in IMG and name not in seen:
                    seen.add(name)
                    imgs += f"<image:image><image:loc>{SITE['origin']}/assets/img/{name}.webp</image:loc></image:image>"
            sm.append(f"<url><loc>{url(path)}</loc><lastmod>{lastmod}</lastmod><priority>{prio}</priority>{imgs}</url>")
    sm.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n")
    (OUT / "blogs").mkdir(parents=True, exist_ok=True)
    (OUT / "blogs" / "blog.atom").write_text(atom_feed(), encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /_pages/\nDisallow: /contact\n\nSitemap: {SITE['origin']}/sitemap.xml\n")


def atom_feed():
    """Atom feed at /blogs/blog.atom, the same path the original Shopify blog used."""
    x = lambda t: E(t, quote=False)
    entries = ""
    for p in POSTS:
        link = url(f"/blogs/blog/{p['slug']}")
        entries += (f"<entry><title>{x(p['title'])}</title><link rel=\"alternate\" type=\"text/html\" href=\"{link}\"/>"
                    f"<id>{link}</id><published>{p['published']}T09:00:00Z</published><updated>{p['updated']}T09:00:00Z</updated>"
                    f"<category term=\"{x(p['category'])}\"/><summary>{x(p['excerpt'])}</summary></entry>\n")
    latest = max(p["updated"] for p in POSTS)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="en-US">\n'
            f'<title>Dukora Idea blog</title><subtitle>{x(SITE["tagline"])}</subtitle>\n'
            f'<link rel="self" type="application/atom+xml" href="{url("/blogs/blog.atom")}"/>\n'
            f'<link rel="alternate" type="text/html" href="{url("/blogs/blog")}"/>\n'
            f'<id>{url("/blogs/blog")}</id><updated>{latest}T09:00:00Z</updated><author><name>Dukora Idea</name></author>\n'
            f'{entries}</feed>\n')


ASSET_V = "1"


def main():
    global ASSET_V
    import hashlib
    h = hashlib.md5()
    for f in ("assets/css/site.css", "assets/js/site.js"):
        h.update((ROOT / f).read_bytes())
    ASSET_V = h.hexdigest()[:8]
    build_home()
    for p in POSTS:
        build_post(p)
    for p in PRODUCTS:
        build_product(p)
    for k in COLLECTIONS:
        build_collection(k)
    build_blog_index()
    build_tools()
    build_about()
    build_contact()
    build_legal()
    build_404()
    write()
    print(f"built {len(PAGES)} pages ({len(POSTS)} posts, {len(PRODUCTS)} guides)")


if __name__ == "__main__":
    main()
