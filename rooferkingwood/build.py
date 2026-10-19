#!/usr/bin/env python3
"""Build rooferkingwood.com (Kingwood Roofers) into dist/ and package a Hostinger upload zip.

    python3 build.py            # build dist/ + rooferkingwood-hostinger-upload.zip
    python3 check.py            # validate the build

Source layout:
    src/         static files copied verbatim (assets, PHP, icons)
    content/     page copy: blog/, services/, areas/ (JSON header + HTML body)
    build.py     layout, shared blocks, schema
    pages_home.py / pages_main.py   page templates
"""
import datetime as dt
import html
import json
import os
import re
import shutil
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
CONTENT = os.path.join(ROOT, "content")
DIST = os.path.join(ROOT, "dist")
ZIP = os.path.join(ROOT, "rooferkingwood-hostinger-upload.zip")

SITE = "https://rooferkingwood.com"
NAME = "Kingwood Roofers"
PHONE = "(512) 297-7580"
TEL = "+15122977580"
TODAY = dt.date(2026, 10, 19)
GEO = (30.0499, -95.1847)

e = html.escape


# --------------------------------------------------------------------------- icons
ICONS = {
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "hammer": '<path d="m15 12-8.5 8.5a2.1 2.1 0 0 1-3-3L12 9"/><path d="M17.6 15 22 10.6"/><path d="m20.9 11.7-1.3-1.3a2 2 0 0 1-.6-1.4V7.9l-2.3-2.3a5.5 5.5 0 0 0-3.9-1.6H9l.9.8a5.4 5.4 0 0 1 1.9 4.1v1.6l2 2h2.2c.5 0 1 .2 1.4.6l1.3 1.3"/>',
    "cloud-hail": '<path d="M20 16.6A5 5 0 0 0 18 7h-1.3A8 8 0 1 0 4 15.3"/><path d="M16 14v2M8 14v2M16 20h.01M8 20h.01M12 16v2M12 22h.01"/>',
    "file-check": '<path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><path d="M14 2v6h6"/><path d="m9 15 2 2 4-4"/>',
    "layers": '<path d="m12.8 2.2a2 2 0 0 0-1.6 0L2.6 6.1a1 1 0 0 0 0 1.8l8.6 3.9a2 2 0 0 0 1.6 0l8.6-3.9a1 1 0 0 0 0-1.8z"/><path d="m22 17.6-9.2 4.2a2 2 0 0 1-1.6 0L2 17.6"/><path d="m22 12.6-9.2 4.2a2 2 0 0 1-1.6 0L2 12.6"/>',
    "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4M8 6h.01M16 6h.01M12 6h.01M12 10h.01M12 14h.01M16 10h.01M16 14h.01M8 10h.01M8 14h.01"/>',
    "droplets": '<path d="M7 16.3c2.2 0 4-1.8 4-4 0-1.2-.6-2.3-1.8-3.3S7.1 6.6 7 5.3c-.1 1.3-1 2.6-2.2 3.6S3 11.1 3 12.3c0 2.2 1.8 4 4 4z"/><path d="M12.6 6.6A11 11 0 0 0 14 3c.5 2.5 2 4.9 4 6.5s3 3.5 3 5.5a6.98 6.98 0 0 1-11.9 5"/>',
    "home": '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
    "tree": '<path d="m17 14 3 3.3a1 1 0 0 1-.7 1.7H4.7a1 1 0 0 1-.7-1.7L7 14h-.3a1 1 0 0 1-.7-1.7L9 9h-.2A1 1 0 0 1 8 7.3L12 3l4 4.3a1 1 0 0 1-.8 1.7H15l3 3.3a1 1 0 0 1-.7 1.7H17Z"/><path d="M12 22v-3"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "check-circle": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    "arrow": '<path d="M5 12h14M12 5l7 7-7 7"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M6.3 17.7l-1.4 1.4M19.1 4.9l-1.4 1.4"/>',
    "wind": '<path d="M17.7 7.7a2.5 2.5 0 1 1 1.8 4.3H2M9.6 4.6A2 2 0 1 1 11 8H2M12.6 19.4A2 2 0 1 0 14 16H2"/>',
    "cloud-rain": '<path d="M4 14.9A7 7 0 1 1 15.7 8h1.8a4.5 4.5 0 0 1 2.5 8.2"/><path d="M16 14v6M8 14v6M12 16v6"/>',
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "chevron": '<path d="m6 9 6 6 6-6"/>',
    "calculator": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6h8M16 14v4M16 10h.01M12 10h.01M8 10h.01M12 14h.01M8 14h.01M12 18h.01M8 18h.01"/>',
    "ruler": '<path d="M21.3 15.3a2.4 2.4 0 0 1 0 3.4l-2.6 2.6a2.4 2.4 0 0 1-3.4 0L2.7 8.7a2.4 2.4 0 0 1 0-3.4l2.6-2.6a2.4 2.4 0 0 1 3.4 0Z"/><path d="m14.5 12.5 2-2M11.5 9.5l2-2M8.5 6.5l2-2M17.5 15.5l2-2"/>',
    "clipboard": '<rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="m9 14 2 2 4-4"/>',
    "camera": '<path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
    "alert": '<path d="m21.7 18-8-14a2 2 0 0 0-3.5 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.7-3z"/><path d="M12 9v4M12 17h.01"/>',
    "hourglass": '<path d="M5 22h14M5 2h14M17 22v-4.2a2 2 0 0 0-.6-1.4L12 12l-4.4 4.4a2 2 0 0 0-.6 1.4V22M7 2v4.2a2 2 0 0 0 .6 1.4L12 12l4.4-4.4a2 2 0 0 0 .6-1.4V2"/>',
    "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10Z"/><path d="M2 21c0-3 1.9-5.4 5.1-6"/>',
}


def icon(name, cls="i"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'


CREST = ('<svg viewBox="0 0 46 52" aria-hidden="true"><path d="M23 1 44 8v17c0 13-9 22-21 26C11 47 2 38 2 25V8z" fill="#7b1e2b"/>'
         '<path d="M23 1 44 8v17c0 13-9 22-21 26C11 47 2 38 2 25V8z" fill="none" stroke="#c9973f" stroke-width="2"/>'
         '<path d="M9 27 23 15l14 12" fill="none" stroke="#e4bf73" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'
         '<path d="m23 21 5 6h-2.6l3.6 4.4h-3l3.4 4.6H16.6l3.4-4.6h-3l3.6-4.4H18z" fill="#fff"/><path d="M23 36v4" stroke="#fff" stroke-width="2"/></svg>')

LOGO = (f'<a class="logo" href="/" aria-label="{NAME} home">{CREST}'
        f'<span class="wm"><b>Kingwood</b><small>Roofers</small></span></a>')

IMG_SIZES = {}


def img(key, alt, cls="", eager=False):
    w, h = IMG_SIZES.get(key, (1600, 1067))
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return f'<img src="/assets/img/{key}.webp" alt="{e(alt)}" width="{w}" height="{h}" {load}{c}>'


# --------------------------------------------------------------------------- content
def load_dir(kind):
    items = []
    folder = os.path.join(CONTENT, kind)
    for fn in sorted(os.listdir(folder)):
        if not fn.endswith(".html"):
            continue
        raw = open(os.path.join(folder, fn), encoding="utf-8").read()
        m = re.match(r"\s*<!--\s*(\{.*?\})\s*-->\s*(.*)$", raw, re.S)
        if not m:
            raise SystemExit(f"bad content header: {kind}/{fn}")
        meta = json.loads(m.group(1))
        meta["body"] = m.group(2).strip()
        meta.setdefault("slug", fn[:-5])
        items.append(meta)
    return items


SERVICE_ORDER = ["roof-replacement-kingwood-tx", "roof-repair-kingwood-tx", "storm-damage-roof-repair-kingwood-tx",
                 "tree-damage-roof-repair-kingwood-tx", "insurance-claim-help-kingwood-tx", "metal-roofing-kingwood-tx",
                 "commercial-roofing-kingwood-tx", "gutters-kingwood-tx"]
AREA_ORDER = ["roofing-atascocita-tx", "roofing-humble-tx", "roofing-porter-tx", "roofing-new-caney-tx",
              "roofing-huffman-tx", "roofing-crosby-tx"]
VILLAGES = ["Kingwood Forest", "Bear Branch", "Elm Grove", "Forest Cove", "Greentree Village", "Trailwood", "Woodland Hills",
            "Sand Creek", "Hunters Ridge", "Kings Forest", "Kingwood Lakes", "Kings Mill", "Mills Branch", "Fosters Mill",
            "Deer Ridge Estates", "Royal Shores", "Kingwood Greens", "Barrington", "Kingwood Place", "North Woods"]

SERVICES, AREAS, POSTS = [], [], []


def cta_band(title="Free roof inspection in Kingwood", text="Photo report, straight answers, no obligation. Most inspections are on the calendar within a few days."):
    return (f'<div class="cta-band shingle-bg" data-reveal><div><h3>{e(title)}</h3><p>{e(text)}</p></div>'
            f'<a class="btn btn-brass" href="/free-roof-inspection/">Book it free {icon("arrow")}</a></div>')


def prep_body(body):
    return body.replace('<div class="cta-inline"></div>', cta_band())


def fmt_date(d):
    d = dt.date.fromisoformat(d)
    return d.strftime("%B ") + str(d.day) + d.strftime(", %Y")


# --------------------------------------------------------------------------- layout
NAV_TOOLS = [("/tools/roof-cost-calculator/", "Roof Cost Calculator"), ("/tools/roof-pitch-calculator/", "Roof Pitch & Area Calculator"),
             ("/tools/storm-damage-checklist/", "Storm Damage Self-Check"), ("/tools/roof-age-estimator/", "Roof Age & Lifespan Estimator")]


def nav_html(active):
    def a(href, label):
        cur = ' aria-current="page"' if active == href else ""
        return f'<a href="{href}"{cur}>{e(label)}</a>'
    svc = "".join(f"<li>{a('/services/' + s['slug'] + '/', s['name'])}</li>" for s in SERVICES)
    ars = "".join(f"<li>{a('/areas/' + s['slug'] + '/', s['name'])}</li>" for s in AREAS)
    tools = "".join(f"<li>{a(h, l)}</li>" for h, l in NAV_TOOLS)
    return f"""<nav class="nav" aria-label="Main"><ul>
<li>{a('/', 'Home')}</li>
<li class="has-sub">{a('/services/', 'Services')}<ul class="sub"><li>{a('/free-roof-inspection/', 'Free Roof Inspection')}</li>{svc}</ul></li>
<li class="has-sub">{a('/areas/', 'Areas')}<ul class="sub"><li>{a('/', 'Kingwood, TX')}</li>{ars}</ul></li>
<li>{a('/weather/', 'Storm Desk')}</li>
<li class="has-sub">{a('/tools/', 'Tools')}<ul class="sub">{tools}</ul></li>
<li>{a('/blog/', 'Blog')}</li>
<li>{a('/about/', 'About')}</li>
<li>{a('/contact/', 'Contact')}</li>
</ul></nav>"""


def mobile_menu_html(active):
    def a(href, label):
        cur = ' aria-current="page"' if active == href else ""
        return f'<a href="{href}"{cur}>{e(label)}</a>'

    def group(label, href, items, is_open):
        links = "".join(a(h, l) for h, l in items)
        return (f'<details{" open" if is_open else ""}><summary>{e(label)}{icon("chevron")}</summary>'
                f'<div class="mm-sub">{a(href, "All " + label.lower())}{links}</div></details>')

    svc = [("/free-roof-inspection/", "Free Roof Inspection")] + [("/services/" + s["slug"] + "/", s["name"]) for s in SERVICES]
    ars = [("/", "Kingwood, TX")] + [("/areas/" + s["slug"] + "/", s["name"]) for s in AREAS]
    return f"""<div class="mm" id="mobile-menu" aria-hidden="true" role="dialog" aria-modal="true" aria-label="Menu">
<div class="mm-head">{LOGO}<a class="mm-close" href="#" data-menu-close aria-label="Close menu">{icon("x")}</a></div>
<nav class="mm-body" aria-label="Mobile">
{a('/', 'Home')}
{group('Services', '/services/', svc, active.startswith('/services/'))}
{group('Service Areas', '/areas/', ars, active.startswith('/areas/'))}
{a('/weather/', 'Kingwood Storm Desk')}
{group('Tools', '/tools/', NAV_TOOLS, active.startswith('/tools/'))}
{a('/blog/', 'Blog')}
{a('/about/', 'About')}
{a('/contact/', 'Contact')}
</nav>
<div class="mm-foot"><a class="btn btn-brass" href="/free-roof-inspection/">Book a free inspection {icon("arrow")}</a>
<a class="btn btn-ghost-light" href="tel:{TEL}">{icon("phone")} {PHONE}</a></div>
</div>"""


def header_html(active):
    return f"""<div class="utility"><div class="wrap">
{LOGO}
<div class="util-mid"><span>{icon('pin')} Kingwood, Atascocita, Humble &amp; Lake Houston</span><span>{icon('clipboard')} Free roof inspections</span></div>
<a class="util-call" href="tel:{TEL}"><span class="ring">{icon('phone')}</span><span><small>Call or text</small><b>{PHONE}</b></span></a>
</div></div>
<header class="navbar"><div class="wrap">
<div class="nav-logo">{LOGO}</div>
{nav_html(active)}
<div class="nav-cta"><a class="nav-phone" href="tel:{TEL}">{icon('phone')} <span>{PHONE}</span></a>
<a class="btn btn-brass" href="/free-roof-inspection/">Free Inspection</a>
<a class="menu-btn" href="#mobile-menu" data-menu-open role="button" aria-controls="mobile-menu" aria-expanded="false">{icon('menu')} Menu</a></div>
</div></header>"""


def footer_html():
    svc = "".join(f'<li><a href="/services/{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES)
    ars = "".join(f'<li><a href="/areas/{s["slug"]}/">{e(s["name"])}</a></li>' for s in AREAS)
    return f"""<footer class="site-footer">
<div class="wrap foot-grid">
<div>{LOGO}
<p>Roof inspections, repairs, replacements and storm-damage help for Kingwood, TX and the Lake Houston area. Built for tall pines, Gulf storms and village association rules.</p>
<a class="foot-phone" href="tel:{TEL}">{icon("phone")} {PHONE}</a>
<p><a class="btn btn-brass btn-sm" href="/free-roof-inspection/">Free Roof Inspection</a></p>
</div>
<div><h4>Services</h4><ul><li><a href="/free-roof-inspection/">Free Roof Inspection</a></li>{svc}</ul></div>
<div><h4>Service Areas</h4><ul><li><a href="/">Kingwood, TX</a></li>{ars}</ul></div>
<div><h4>Company</h4><ul>
<li><a href="/about/">About Us</a></li><li><a href="/blog/">Roofing Blog</a></li><li><a href="/weather/">Kingwood Storm Desk</a></li>
<li><a href="/tools/">Homeowner Tools</a></li><li><a href="/contact/">Contact</a></li>
<li><a href="/privacy-policy/">Privacy Policy</a></li><li><a href="/terms/">Terms of Use</a></li><li><a href="/sitemap.xml">Sitemap</a></li></ul></div>
</div>
<div class="wrap foot-bottom"><span>© <span data-year>{TODAY.year}</span> {NAME} · Kingwood, TX 77339 · 77345 · 77346</span>
<span>Texas law prohibits contractors from waiving or rebating insurance deductibles. We never do.</span></div>
</footer>
<div class="mobile-bar"><a href="tel:{TEL}">{icon("phone")} Call</a><a href="/free-roof-inspection/">{icon("clipboard")} Free inspection</a></div>"""


SERVICE_OPTIONS = ["Free roof inspection", "Roof repair / leak", "Roof replacement", "Storm or hail damage", "Tree or limb damage",
                   "Insurance claim help", "Metal roofing", "Commercial roofing", "Gutters / gutter guards", "Other"]


def lead_form(form_id, heading="Book your free roof inspection", sub="Tell us about your roof and we'll call to schedule. No cost, no pressure.",
              full=False, hlevel="h2", service=None, button="Request my free inspection"):
    opts = "".join(f'<option{" selected" if o == service else ""}>{e(o)}</option>' for o in SERVICE_OPTIONS)
    extra = ""
    if full:
        extra = """<div class="field"><label for="{0}-timing">When works best?</label><select id="{0}-timing" name="timing">
<option>As soon as possible</option><option>This week</option><option>Next week or later</option><option>Just researching</option></select></div>
<div class="field full"><label for="{0}-msg">What's happening with your roof? (optional)</label><textarea id="{0}-msg" name="message" placeholder="Pine limb came down on the back slope during the last storm, small leak in the garage..."></textarea></div>""".format(form_id)
    return f"""<form class="lead-form" action="/send.php" method="post" id="{form_id}">
<{hlevel}>{e(heading)}</{hlevel}>
<p class="sub">{e(sub)}</p>
<div class="form-grid">
<div class="field"><label for="{form_id}-name">Full name *</label><input id="{form_id}-name" name="name" autocomplete="name" required></div>
<div class="field"><label for="{form_id}-phone">Phone *</label><input id="{form_id}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="field"><label for="{form_id}-email">Email</label><input id="{form_id}-email" name="email" type="email" autocomplete="email"></div>
<div class="field"><label for="{form_id}-addr">Address or ZIP</label><input id="{form_id}-addr" name="address" autocomplete="street-address"></div>
<div class="field{'' if full else ' full'}"><label for="{form_id}-svc">I need help with</label><select id="{form_id}-svc" name="service">{opts}</select></div>
{extra}
</div>
{form_hidden(form_id, heading)}
<button class="btn" type="submit">{e(button)} {icon("arrow")}</button>
<div class="form-status" role="status" aria-live="polite"></div>
<p class="form-note">By submitting, you agree we may call or text you about your request. We never sell or share your information.</p>
</form>"""


def form_hidden(form_id, label):
    return (f'<div class="hp" aria-hidden="true"><label for="{form_id}-web">Leave this empty</label><input id="{form_id}-web" name="website" tabindex="-1" autocomplete="off"></div>'
            f'<input type="hidden" name="t" value=""><input type="hidden" name="page" value=""><input type="hidden" name="form" value="{e(label)}">')


def quick_form(form_id="quick-form"):
    opts = "".join(f"<option>{e(o)}</option>" for o in SERVICE_OPTIONS)
    return f"""<form class="lead-form quick-form" action="/send.php" method="post" id="{form_id}" aria-label="Quick inspection request">
<input id="{form_id}-name" name="name" placeholder="Your name" autocomplete="name" required aria-label="Your name">
<input id="{form_id}-phone" name="phone" type="tel" placeholder="Phone number" autocomplete="tel" required aria-label="Phone number">
<input id="{form_id}-addr" name="address" placeholder="ZIP code" autocomplete="postal-code" inputmode="numeric" aria-label="ZIP code">
<select id="{form_id}-svc" name="service" aria-label="I need help with">{opts}</select>
{form_hidden(form_id, "Quick request bar")}
<button class="btn btn-brass" type="submit">Get my free inspection {icon("arrow")}</button>
<div class="form-status" role="status" aria-live="polite"></div>
</form>"""


def popup_html():
    """Lead popup. site.js opens it 4 seconds after page load (once per browser session)."""
    return f"""<div class="popup" id="lead-popup" role="dialog" aria-modal="true" aria-labelledby="popup-title" aria-hidden="true">
<div class="popup-bg" data-popup-close></div>
<div class="popup-box">
<button class="popup-close" type="button" data-popup-close aria-label="Close">{icon("x")}</button>
<div class="popup-side shingle-bg">
<div class="stamp-sm"><span><b>$0</b>Roof<br>inspection</span></div>
<div><h2 id="popup-title">Is your roof ready for the next Kingwood storm?</h2>
<p style="margin:12px 0 0">Get a free, photo-documented inspection from local Kingwood roofers.</p></div>
<ul class="ticks"><li>{icon("check")}<span>Every slope, valley and vent checked</span></li>
<li>{icon("check")}<span>Photo report you keep</span></li><li>{icon("check")}<span>No pressure, no obligation</span></li></ul>
<p style="margin:0;font-size:.9rem">Rather talk? <a href="tel:{TEL}">{PHONE}</a></p>
</div>
<div class="popup-form">{lead_form("popup-form", heading="Claim your free inspection", sub="Takes 30 seconds. We'll call to set a time.", button="Book my free inspection")}</div>
</div></div>"""


def business_schema():
    return {
        "@type": "RoofingContractor",
        "@id": SITE + "/#business",
        "name": NAME,
        "url": SITE + "/",
        "telephone": "+1-512-297-7580",
        "email": "info@rooferkingwood.com",
        "image": SITE + "/assets/img/og-image.jpg",
        "logo": SITE + "/web-app-manifest-512x512.png",
        "priceRange": "$$",
        "description": "Kingwood roofers offering free roof inspections, roof repair, roof replacement, storm, hail and tree damage repair and insurance claim help in Kingwood, TX.",
        "address": {"@type": "PostalAddress", "addressLocality": "Kingwood", "addressRegion": "TX", "postalCode": "77339", "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": GEO[0], "longitude": GEO[1]},
        "areaServed": [{"@type": "City", "name": n} for n in
                       ["Kingwood, TX", "Atascocita, TX", "Humble, TX", "Porter, TX", "New Caney, TX", "Huffman, TX", "Crosby, TX"]],
        "makesOffer": {"@type": "Offer", "name": "Free Roof Inspection", "price": "0", "priceCurrency": "USD",
                       "url": SITE + "/free-roof-inspection/"},
    }


def crumbs_schema(crumbs):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(crumbs)]}


def faq_schema(faqs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in faqs]}


def crumbs_html(crumbs):
    items = "".join(
        f'<li><a href="{u}">{e(n)}</a></li>' if i < len(crumbs) - 1 else f'<li aria-current="page">{e(n)}</li>'
        for i, (n, u) in enumerate(crumbs))
    return f'<ol class="crumbs">{items}</ol>'


def page(path, title, desc, main, active=None, schema=(), og_image="og-image.jpg", og_type="website",
         scripts=(), noindex=False, preload=None, extra_head="", popup=True):
    canonical = SITE + path
    graph = [business_schema(),
             {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": NAME,
              "publisher": {"@id": SITE + "/#business"}}] + list(schema)
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large"
    pre = f'<link rel="preload" as="image" href="/assets/img/{preload}.webp" fetchpriority="high">\n' if preload else ""
    js = "".join(f'<script src="/assets/js/{s}.js?v=1" defer></script>' for s in ("site",) + tuple(scripts))
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
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/assets/img/{og_image}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{SITE}/assets/img/{og_image}">
<meta name="geo.region" content="US-TX">
<meta name="geo.placename" content="Kingwood">
<meta name="geo.position" content="{GEO[0]};{GEO[1]}">
<meta name="theme-color" content="#7b1e2b">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;1,9..144,500&family=Manrope:wght@400;500;600;700;800&display=swap">
{pre}<link rel="stylesheet" href="/assets/css/site.css?v=1">
{extra_head}<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header_html(active or path)}
{mobile_menu_html(active or path)}
<main id="main">
{main}
</main>
{footer_html()}
{popup_html() if popup else ""}
{js}
</body>
</html>
"""


# --------------------------------------------------------------------------- shared blocks
def faq_html(faqs, heading="Frequently asked questions", bg="bg-cream"):
    items = "".join(f'<details><summary>{e(f["q"])}</summary><p>{e(f["a"])}</p></details>' for f in faqs)
    return (f'<section class="section {bg}"><div class="wrap"><div class="head" data-reveal><span class="kicker">FAQ</span><h2>{e(heading)}</h2></div>'
            f'<div class="faq" data-reveal>{items}</div></div></section>')


def closer(title="Get a straight answer about your roof", text=None):
    text = text or "Book a free roof inspection with local Kingwood roofers. You'll get photos of what we find, a plain-English explanation and an honest recommendation."
    return f"""<section class="closer shingle-bg"><div class="wrap" data-reveal><span class="kicker">Free · No obligation</span><h2>{e(title)}</h2><p>{e(text)}</p>
<div class="hero-actions"><a class="btn btn-brass" href="/free-roof-inspection/">Book free inspection {icon("arrow")}</a>
<a class="btn btn-ghost-light" href="tel:{TEL}">{icon("phone")} {PHONE}</a></div></div></section>"""


def page_hero(crumbs, h1, lead, image=None, alt="", kicker=None, meta=""):
    kb = f'<span class="kicker">{e(kicker)}</span>' if kicker else ""
    pic = f'<div class="ph-img">{img(image, alt or h1, eager=True)}</div>' if image else ""
    return f"""<section class="phero{'' if image else ' no-img'}"><div class="wrap">
<div>{crumbs_html(crumbs)}{kb}<h1>{h1}</h1><p class="lead">{e(lead)}</p>{meta}</div>{pic}</div></section>"""


def form_section(form_id, service=None, title="Book your free roof inspection", text=None):
    text = text or ("A local roofer walks every slope, photographs what matters and explains your options in plain English. "
                    "If there's storm or tree damage, you'll see the evidence before you ever call your insurance company.")
    return f"""<section class="section bg-sand"><div class="wrap cols cols-5-7">
<div data-reveal><span class="kicker">Free roof inspections</span><h2>{e(title)}</h2><p>{e(text)}</p>
<ul class="ticks"><li>{icon("check")}<span>Shingles, flashing, valleys, vents and gutters</span></li>
<li>{icon("check")}<span>Photo report you keep, whether you hire us or not</span></li>
<li>{icon("check")}<span>Written, itemized estimate when work is needed</span></li>
<li>{icon("check")}<span>No pressure, no deductible games</span></li></ul>
<a class="link-arrow" href="tel:{TEL}">{icon("phone")} Prefer to talk? {PHONE}</a></div>
<div class="form-card" data-reveal>{lead_form(form_id, heading="Request your free inspection", hlevel="h3", service=service)}</div>
</div></section>"""


def box_call():
    return f"""<div class="box box-call"><h3>Talk to a Kingwood roofer</h3><p style="margin:0">Leak, storm, fallen limb or estimate question?</p>
<a class="big" href="tel:{TEL}">{PHONE}</a><a class="btn btn-brass btn-sm btn-block" href="/free-roof-inspection/">Book a free inspection</a></div>"""


# --------------------------------------------------------------------------- output
def write(path, htmltext):
    rel = "home.html" if path == "/" else path.strip("/") + "/index.html"
    if path.endswith(".html"):
        rel = path.strip("/")
    out = os.path.join(DIST, rel)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    # Relative asset paths: images/CSS/JS load even from a local preview or a subfolder install.
    pre = "/" if rel == "404.html" else "../" * rel.count("/")
    htmltext = re.sub(r'(src|href)="/(assets/|favicon|apple-touch-icon|site\.webmanifest|web-app-manifest)',
                      lambda m: f'{m.group(1)}="{pre}{m.group(2)}', htmltext)
    with open(out, "w", encoding="utf-8") as f:
        f.write(htmltext)


SITEMAP = []


def add(path, htmltext, lastmod=None, priority="0.7", sitemap=True):
    write(path, htmltext)
    if sitemap:
        SITEMAP.append((path, lastmod or TODAY.isoformat(), priority))


def main():
    from pages_home import build_home
    from pages_main import build_main
    svc = {s["slug"]: s for s in load_dir("services")}
    ars = {s["slug"]: s for s in load_dir("areas")}
    SERVICES[:] = [svc[s] for s in SERVICE_ORDER if s in svc]
    AREAS[:] = [ars[s] for s in AREA_ORDER if s in ars]
    POSTS[:] = sorted(load_dir("blog"), key=lambda p: p["date"], reverse=True)

    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    shutil.copytree(SRC, DIST, ignore=shutil.ignore_patterns("CREDITS.md"))
    for fn in os.listdir(os.path.join(DIST, "assets", "img")):
        if fn.endswith(".webp"):
            out = os.popen(f'identify -format "%w %h" "{os.path.join(DIST, "assets", "img", fn)}"').read().split()
            if len(out) == 2:
                IMG_SIZES[fn[:-5]] = (int(out[0]), int(out[1]))

    build_home()
    build_main()

    urls = "".join(f"<url><loc>{SITE}{p}</loc><lastmod>{m}</lastmod><priority>{pr}</priority></url>\n" for p, m, pr in SITEMAP)
    open(os.path.join(DIST, "sitemap.xml"), "w").write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    open(os.path.join(DIST, "robots.txt"), "w").write(
        f"User-agent: *\nAllow: /\nDisallow: /home.html\nDisallow: /includes/\nDisallow: /send.php\nDisallow: /thank-you/\n\nSitemap: {SITE}/sitemap.xml\n")

    if os.path.exists(ZIP):
        os.remove(ZIP)
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for base, _, files in os.walk(DIST):
            for fn in sorted(files):
                full = os.path.join(base, fn)
                z.write(full, os.path.relpath(full, DIST))
    n = sum(len(f) for _, _, f in os.walk(DIST))
    print(f"built {len(SITEMAP)} pages, {n} files -> {os.path.relpath(ZIP, ROOT)} ({os.path.getsize(ZIP)//1024} KB)")


if __name__ == "__main__":
    import sys
    sys.modules["build"] = sys.modules[__name__]
    main()
