#!/usr/bin/env python3
"""Static site generator for the Los Arcos Apartments concept site.

    python3 build.py          -> writes the finished site to ./dist

Everything (pages, shared header/footer, schema, SEO tags) is defined here so
the site stays plain HTML/CSS/JS with no runtime. Edit PROPERTY / PLANS below,
re-run, and upload ./dist.
"""
import json, os, shutil, html, hashlib
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
DIST = os.path.join(ROOT, "dist")

# ---------------------------------------------------------------------------
# Property facts (verified by the agency; anything else is marked [confirm])
# ---------------------------------------------------------------------------
P = {
    "name": "Los Arcos Apartments & Townhomes",
    "short": "Los Arcos",
    "street": "11315 Fondren Rd",
    "city": "Houston", "state": "TX", "zip": "77035",
    "area": "Brays Oaks / Fondren Southwest",
    "lat": 29.653, "lng": -95.507,
    "phone": "(713) 729-6274", "tel": "+17137296274",
    "hours": "Mon–Sat 9:00 AM–5:00 PM · Sun closed",
    "units": 516, "built": 1977,
    "sqft": "550–1,498",
    "rating": "4.6", "reviews": "350+", "five_star": "304",
}
ADDR_Q = "Los+Arcos+Apartments+11315+Fondren+Rd+Houston+TX+77035"
GMAPS = f"https://www.google.com/maps/search/?api=1&query={ADDR_Q}"
DIRECTIONS = "https://www.google.com/maps/dir/?api=1&destination=11315+Fondren+Rd+Houston+TX+77035"
MAP_EMBED = "https://www.google.com/maps?q=Los+Arcos+Apartments,+11315+Fondren+Rd,+Houston,+TX+77035&ll=29.653,-95.507&z=15&output=embed"
# Placeholder links — replace with the property's live URLs
APPLY_URL = "#apply-portal"
PAY_URL = "#pay-rent"
MAINT_URL = "#maintenance"
PORTAL_URL = "#resident-portal"

NAV = [
    ("/amenities/", "Amenities"), ("/floor-plans/", "Floor Plans"), ("/gallery/", "Gallery"),
    ("/neighborhood/", "Neighborhood"), ("/residents/", "Residents"), ("/faqs/", "FAQs"),
    ("/contact/", "Contact"),
]

# ---------------------------------------------------------------------------
# Icons (simple line icons, 24x24, stroke = currentColor)
# ---------------------------------------------------------------------------
_I = {
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "cube": '<path d="M21 16V8a2 2 0 0 0-1-1.7l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.7l7 4a2 2 0 0 0 2 0l7-4a2 2 0 0 0 1-1.7z"/><path d="M3.3 7 12 12l8.7-5M12 22V12"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "arrow-ur": '<path d="M7 17 17 7M8 7h9v9"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/>',
    "pool": '<path d="M2 18c1.5 1 3 1 4.5 0s3-1 4.5 0 3 1 4.5 0 3-1 4.5 0M2 14c1.5 1 3 1 4.5 0s3-1 4.5 0 3 1 4.5 0 3-1 4.5 0M8 12V5a2 2 0 0 1 4 0M16 12V5a2 2 0 0 0-4 0M8 8h8"/>',
    "car": '<path d="M5 17H3v-5l2-5h14l2 5v5h-2"/><circle cx="7.5" cy="17" r="2"/><circle cx="16.5" cy="17" r="2"/><path d="M3 12h18"/>',
    "access": '<circle cx="12" cy="4" r="2"/><path d="M19 13v-2a7 7 0 0 0-5-1H8M8 8v6h6l3 6M8 14a5 5 0 1 0 5 5"/>',
    "gate": '<path d="M3 21V8l4-3 4 3v13M13 21V8l4-3 4 3v13M3 12h18M3 17h18"/>',
    "laundry": '<rect x="4" y="2" width="16" height="20" rx="2"/><circle cx="12" cy="13" r="5"/><path d="M8 6h.01M11 6h.01"/>',
    "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10z"/><path d="M2 21c0-3 1.9-5.4 5.1-6"/>',
    "paw": '<circle cx="11" cy="4" r="2"/><circle cx="18" cy="8" r="2"/><circle cx="20" cy="16" r="2"/><path d="M9 10a5 5 0 0 1 5 5v3.5a3.5 3.5 0 0 1-6.8 1.2 3.4 3.4 0 0 0-2.4-2.4A3.5 3.5 0 0 1 6 10.4 5 5 0 0 1 9 10z"/>',
    "tools": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.8-3.8a6 6 0 0 1-7.9 7.9l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a6 6 0 0 1 7.9-7.9z"/>',
    "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "fan": '<path d="M10.8 10.4C9.7 7.8 10.4 3 13.6 3c2.6 0 3 3.7.6 6.4M13.6 13.6c2.6 1.1 7.4.4 7.4-2.8 0-2.6-3.7-3-6.4-.6M13.2 13.6c1.1 2.6.4 7.4-2.8 7.4-2.6 0-3-3.7-.6-6.4M10.4 10.8C7.8 9.7 3 10.4 3 13.6c0 2.6 3.7 3 6.4.6"/><circle cx="12" cy="12" r="1"/>',
    "door": '<path d="M13 4h3a2 2 0 0 1 2 2v14M2 20h3M13 20h9M10 12v.01M13 4.6v16.2a1 1 0 0 1-1.2 1L5 20V5.6a2 2 0 0 1 1.5-1.9l4-1A2 2 0 0 1 13 4.6z"/>',
    "kitchen": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M7 6h.01M11 6h.01M8 13h8v5H8z"/>',
    "snow": '<path d="M2 12h20M12 2v20M20 16l-4-4 4-4M4 8l4 4-4 4M16 4l-4 4-4-4M8 20l4-4 4 4"/>',
    "closet": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M12 2v20M9 11v2M15 11v2"/>',
    "balcony": '<path d="M3 21h18M5 21v-8M19 21v-8M3 13h18M9 21v-8M15 21v-8M8 13V5a4 4 0 0 1 8 0v8"/>',
    "wash": '<path d="M3 6h18M3 12h18M3 18h18" stroke-dasharray="2 3"/>',
    "bed": '<path d="M2 4v16M2 8h18a2 2 0 0 1 2 2v10M2 17h20M6 8v9"/>',
    "bath": '<path d="M9 6 6.5 3.5a1.5 1.5 0 0 0-2.1 0L3.5 4.4A1.5 1.5 0 0 0 3 5.5V17a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-5H3M7 19v2M17 19v2"/>',
    "ruler": '<path d="M21.3 15.3a2.4 2.4 0 0 1 0 3.4l-2.6 2.6a2.4 2.4 0 0 1-3.4 0L2.7 8.7a2.4 2.4 0 0 1 0-3.4l2.6-2.6a2.4 2.4 0 0 1 3.4 0zM14.5 12.5l2-2M11.5 9.5l2-2M8.5 6.5l2-2M17.5 15.5l2-2"/>',
    "card": '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/>',
    "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.8-3.8a6 6 0 0 1-7.9 7.9l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a6 6 0 0 1 7.9-7.9z"/>',
    "home": '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "moon": '<path d="M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8z"/>',
    "sparkle": '<path d="M12 3l1.9 5.8L20 11l-6.1 2.2L12 19l-1.9-5.8L4 11l6.1-2.2z"/>',
    "heart": '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l1 1.1L12 21l7.8-7.5 1-1.1a5.5 5.5 0 0 0 0-7.8z"/>',
    "smile": '<circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2M9 9h.01M15 9h.01"/>',
    "bag": '<path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4zM3 6h18M16 10a4 4 0 0 1-8 0"/>',
    "fork": '<path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2M7 2v20M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3zm0 0v7"/>',
    "tree": '<path d="M12 22v-7M17 8a5 5 0 0 0-10 0 4 4 0 0 0-2 7.5A4 4 0 0 0 9 18h6a4 4 0 0 0 4-2.5A4 4 0 0 0 17 8z"/>',
    "school": '<path d="M22 10 12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "left": '<path d="m15 18-6-6 6-6"/>',
    "right": '<path d="m9 18 6-6-6-6"/>',
    "play": '<path d="M6 4l14 8-14 8z" fill="currentColor"/>',
    "star": '<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/>',
    "megaphone": '<path d="m3 11 18-5v12L3 14v-3zM11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
    "trash": '<path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>',
    "bolt": '<path d="M13 2 3 14h9l-1 8 10-12h-9z"/>',
}
def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_I[name]}</svg>'

SOCIAL = {
    "Instagram": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".6" fill="currentColor"/></svg>',
    "Facebook": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14 8.5V6.8c0-.8.2-1.3 1.4-1.3H17V2.3c-.3 0-1.3-.1-2.4-.1-2.4 0-4 1.4-4 4.1v2.2H8v3.6h2.6V22H14v-9.9h2.7l.4-3.6z"/></svg>',
    "TikTok": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.6 5.8A4.3 4.3 0 0 1 15.5 3h-3.1v12.4a2.6 2.6 0 1 1-2.6-2.6c.3 0 .5 0 .8.1V9.7a5.8 5.8 0 1 0 4.9 5.7V9.1a7.4 7.4 0 0 0 4.3 1.4V7.4a4.3 4.3 0 0 1-3.2-1.6z"/></svg>',
}

LOGO_MARK = ('<svg viewBox="0 0 40 44" aria-hidden="true" focusable="false">'
             '<path d="M3 43V20a17 17 0 0 1 34 0v23" fill="none" stroke="#A24A2E" stroke-width="3"/>'
             '<path d="M11 43V22a9 9 0 0 1 18 0v21" fill="none" stroke="#4A5636" stroke-width="3"/>'
             '<path d="M0 43h40" stroke="#A24A2E" stroke-width="2"/>'
             '<circle cx="20" cy="9.5" r="1.8" fill="#C4673F"/></svg>')

EHO = ('<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true">'
       '<path d="M4 22 24 6l20 16"/><path d="M9 19v24h30V19"/><path d="M16 27h16M16 34h16"/></svg>')
ADA = ('<svg viewBox="0 0 48 48" fill="currentColor" aria-hidden="true"><circle cx="22" cy="7" r="4"/>'
       '<path d="M19 14h6v10h10l5 13-4 1.5-4-9.5H19z"/><path d="M15 21.5v4.6a8.5 8.5 0 1 0 12.4 10.6l3.7 2.3A12.8 12.8 0 1 1 15 21.5z"/></svg>')

# ---------------------------------------------------------------------------
# Images
# ---------------------------------------------------------------------------
IMAGES = {r[0]: {"id": r[1], "cat": r[2], "alt": r[3]} for r in json.load(open(os.path.join(ROOT, "images.json")))}
_dims = {}
def dims(key, w):
    k = (key, w)
    if k not in _dims:
        with Image.open(os.path.join(SRC, "img", f"{key}-{w}.webp")) as im:
            _dims[k] = im.size
    return _dims[k]

def img(key, sizes="100vw", cls="", eager=False, alt=None, lazy_src=False, nolazy=False):
    a = html.escape(alt if alt is not None else IMAGES[key]["alt"], quote=True)
    w, h = dims(key, 900)
    srcset = f"/img/{key}-500.webp 500w, /img/{key}-900.webp 900w, /img/{key}-1600.webp 1600w"
    c = f' class="{cls}"' if cls else ""
    if lazy_src:  # used for hero slides 2/3 (swapped in by JS)
        return (f'<img{c} src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" '
                f'data-src="/img/{key}-1600.webp" data-srcset="{srcset}" sizes="{sizes}" width="{w}" height="{h}" alt="{a}" decoding="async">')
    load = 'fetchpriority="high"' if eager else ('' if nolazy else 'loading="lazy"')
    return f'<img{c} src="/img/{key}-900.webp" srcset="{srcset}" sizes="{sizes}" width="{w}" height="{h}" alt="{a}" {load} decoding="async">'

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------
def schema(page_name, url_path, desc):
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": ["ApartmentComplex", "LocalBusiness"],
                "@id": "#property",
                "name": P["name"],
                "description": "A quiet, gated garden-style community of 516 apartments and townhomes in Southwest Houston's Brays Oaks / Fondren Southwest area.",
                "telephone": P["phone"],
                "image": "/img/hero-pool-1600.webp",
                "logo": "/logo.svg",
                "priceRange": "$$",
                "address": {"@type": "PostalAddress", "streetAddress": P["street"], "addressLocality": P["city"],
                            "addressRegion": P["state"], "postalCode": P["zip"], "addressCountry": "US"},
                "geo": {"@type": "GeoCoordinates", "latitude": P["lat"], "longitude": P["lng"]},
                "hasMap": GMAPS,
                "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                    "opens": "09:00", "closes": "17:00"}],
                "numberOfAccommodationUnits": P["units"],
                "yearBuilt": P["built"],
                "petsAllowed": None,
                "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": n, "value": True} for n in
                                   ["Swimming pool", "On-site parking", "Wheelchair-accessible entrance",
                                    "Wheelchair-accessible parking", "Gated community", "Laundry facilities"]],
                "areaServed": "Southwest Houston, TX",
            },
            {"@type": "WebPage", "name": page_name, "description": desc, "url": url_path,
             "about": {"@id": "#property"}},
        ],
    }
    data["@graph"][0].pop("petsAllowed")  # pet policy not confirmed yet [confirm]
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "</script>"

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
def header(active):
    links = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a></li>' for h, t in NAV)
    return f'''<a class="skip" href="#main">Skip to main content</a>
<div class="announce" role="region" aria-label="Announcement">
  <div class="wrap">
    <p style="margin:0">{icon("megaphone").replace('<svg', '<svg style="width:16px;height:16px;vertical-align:-3px;margin-right:6px"')}Ask about our current move-in specials. <a href="/contact/#tour">Schedule a tour</a></p>
    <!-- [confirm] current special / pet-policy message with management -->
    <button class="announce__close" type="button" aria-label="Dismiss announcement">{icon("x").replace('<svg', '<svg style="width:18px;height:18px"')}</button>
  </div>
</div>
<div class="utility">
  <div class="wrap">
    <span class="utility__addr">{P["street"]}, {P["city"]}, {P["state"]} {P["zip"]}</span>
    <a href="/virtual-tours/">{icon("cube")}Virtual Tours</a>
    <a class="hide-sm" href="/contact/#tour">{icon("calendar")}<span>Schedule a Tour</span></a>
    <a href="tel:{P["tel"]}">{icon("phone")}{P["phone"]}</a>
  </div>
</div>
<header class="header">
  <div class="wrap">
    <a class="logo" href="/">{LOGO_MARK}<span class="logo__text"><span class="logo__name">Los Arcos</span><span class="logo__sub">Apartments &amp; Townhomes</span></span></a>
    <nav class="nav" id="site-nav" aria-label="Main">
      <ul>{links}</ul>
      <div class="nav__extra">
        <a class="btn" href="/floor-plans/">Find Your Home {icon("arrow")}</a>
        <a class="btn btn--ghost" href="tel:{P["tel"]}">{icon("phone")} Call {P["phone"]}</a>
      </div>
    </nav>
    <a class="btn header__cta" href="/floor-plans/">Find Your Home</a>
    <button class="menu-btn" type="button" aria-controls="site-nav" aria-expanded="false" aria-label="Open menu"><span></span></button>
  </div>
</header>'''

def footer():
    social = "".join(f'<a href="#{n.lower()}" aria-label="{n} (link coming soon)" data-placeholder="Demo: this will link to the community\'s {n} page.">{s}</a>' for n, s in SOCIAL.items())
    navl = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in [("/", "Home")] + NAV[:4])
    navr = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in [("/virtual-tours/", "Virtual Tours")] + NAV[4:] + [("/apply/", "Apply Now")])
    return f'''<footer class="footer">
  <div class="arcade" aria-hidden="true"></div>
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__brand">
        <a class="logo" href="/">{LOGO_MARK}<span class="logo__text"><span class="logo__name">Los Arcos</span><span class="logo__sub">Apartments &amp; Townhomes</span></span></a>
        <address><strong style="color:#fff;font-weight:600">Los Arcos Apartments</strong><br>{P["street"]}<br>{P["city"]}, {P["state"]} {P["zip"]}<br><a href="tel:{P["tel"]}">{P["phone"]}</a></address>
        <a class="link-arrow" style="color:var(--clay-soft)" href="{DIRECTIONS}" target="_blank" rel="noopener">Get Directions {icon("arrow-ur").replace('<svg', '<svg style="width:16px;height:16px"')}</a>
        <div class="social">{social}</div>
      </div>
      <div><h2>Explore</h2><ul>{navl}</ul></div>
      <div><h2>Living Here</h2><ul>{navr}</ul></div>
      <div>
        <h2>Leasing Office</h2>
        <table class="hours" style="color:#CFC5B3"><tbody>
          <tr><td>Mon – Fri</td><td>9:00 AM – 5:00 PM</td></tr>
          <tr><td>Saturday</td><td>9:00 AM – 5:00 PM</td></tr>
          <tr><td>Sunday</td><td>Closed</td></tr>
        </tbody></table>
        <p style="margin-top:18px"><a class="btn btn--sm" href="/contact/#tour">Schedule a Tour</a></p>
      </div>
    </div>
    <div class="footer__bottom">
      <div class="fair">
        <span role="img" aria-label="Equal Housing Opportunity">{EHO}</span>
        <span role="img" aria-label="Wheelchair accessible">{ADA}</span>
        <p>We are pledged to the letter and spirit of U.S. policy for the achievement of equal housing opportunity throughout the nation. We do not discriminate on the basis of race, color, religion, sex, handicap, familial status or national origin.</p>
      </div>
      <nav class="legal" aria-label="Legal">
        <span>© <span data-year>2026</span> {P["name"]}</span>
        <a href="/privacy-policy/">Privacy Policy</a><a href="/terms/">Terms</a><a href="/accessibility/">Accessibility</a><a href="/site-map/">Site Map</a>
      </nav>
    </div>
    <p class="concept">Concept site prepared for Los Arcos Apartments.</p>
  </div>
</footer>
<nav class="mobile-bar" aria-label="Quick actions">
  <a href="tel:{P["tel"]}">{icon("phone")}Call</a>
  <a href="/contact/#tour">{icon("calendar")}Tour</a>
  <a href="/apply/">{icon("file")}Apply</a>
</nav>'''

def _ver(rel):
    with open(os.path.join(SRC, rel), "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]

def page(path, title, desc, body, active=None, preload=None, extra_head=""):
    pre = ""
    if preload:
        pre = (f'<link rel="preload" as="image" href="/img/{preload}-900.webp" '
               f'imagesrcset="/img/{preload}-500.webp 500w, /img/{preload}-900.webp 900w, /img/{preload}-1600.webp 1600w" imagesizes="100vw" fetchpriority="high">')
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc, quote=True)}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#1F241A">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title, quote=True)}">
<meta property="og:description" content="{html.escape(desc, quote=True)}">
<meta property="og:image" content="/img/hero-pool-1600.webp">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/fonts/fraunces.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/manrope.woff2" as="font" type="font/woff2" crossorigin>
{pre}
<link rel="stylesheet" href="/css/style.css?v={_ver("css/style.css")}">
{extra_head}
{schema(title, path, desc)}
</head>
<body>
{header(active or path)}
<main id="main">
{body}
</main>
{footer()}
<script src="/js/main.js?v={_ver("js/main.js")}" defer></script>
</body>
</html>
'''
    out = os.path.join(DIST, path.strip("/"), "index.html") if path.endswith("/") else os.path.join(DIST, path.lstrip("/"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    PAGES.append((path, title, desc))

PAGES = []

def page_hero(eyebrow, h1, lead, img_key=None, crumbs=None, extra=""):
    cr = ""
    if crumbs:
        cr = f'<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <span aria-current="page">{crumbs}</span></nav>'
    media = f'<div class="page-hero__img">{img(img_key, sizes="360px", eager=True)}</div>' if img_key else ""
    return f'''<section class="page-hero">
  <div class="wrap">
    <div>{cr}<span class="eyebrow">{eyebrow}</span><h1>{h1}</h1><p class="lead">{lead}</p>{extra}</div>
    {media}
  </div>
</section>
<div class="arcade" aria-hidden="true" style="background-color:var(--sand)"></div>'''

def cta_band(h="Your quiet retreat in <em>Southwest Houston</em> is waiting.", p="Tour Los Arcos Apartments in person or online, and our leasing team will help you find the floor plan that fits your life."):
    return f'''<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="cta reveal">
      <span class="eyebrow" style="color:#FFD9C4">Come see it for yourself</span>
      <h2>{h}</h2>
      <p>{p}</p>
      <div class="btn-row">
        <a class="btn btn--light" href="/contact/#tour">{icon("calendar")} Schedule a Tour</a>
        <a class="btn btn--outline-light" href="/floor-plans/">Find Your Home {icon("arrow")}</a>
      </div>
    </div>
  </div>
</section>'''

# ---------------------------------------------------------------------------
# Floor plans  (rents are ILLUSTRATIVE placeholders — [confirm] with owner)
# ---------------------------------------------------------------------------
PLANS = [
    # name, beds key, beds, baths, sqft, start price, kind
    ("The Sevilla", "1", 1, 1, 550, 1025, "Apartment"),
    ("The Granada", "1", 1, 1, 720, 1095, "Apartment"),
    ("The Valencia", "2", 2, 1, 880, 1195, "Apartment"),
    ("The Toledo", "2", 2, 2, 1040, 1295, "Apartment"),
    ("The Córdoba", "3", 3, 2, 1260, 1450, "Apartment"),
    ("The Marbella", "th", 2, 1.5, 1180, 1395, "Townhome"),
    ("The Ronda", "th", 3, 2.5, 1498, 1595, "Townhome"),
]

def plan_svg(beds, kind):
    """Simple illustrative floor-plan diagram (not to scale)."""
    st = 'fill="#FBF8F3" stroke="#4A5636" stroke-width="2"'
    lbl = 'font-family="Manrope,sans-serif" font-size="11" fill="#6B6358" text-anchor="middle"'
    def room(x, y, w, h, t):
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" {st}/><text x="{x + w/2}" y="{y + h/2 + 4}" {lbl}>{t}</text>'
    if kind == "Townhome":
        g = (room(10, 20, 140, 80, "Living") + room(10, 100, 80, 60, "Kitchen") + room(90, 100, 60, 60, "½ Bath") +
             f'<text x="80" y="185" {lbl} font-weight="700">Level 1</text>')
        up = room(170, 20, 75, 70, "Bedroom") + room(245, 20, 65, 70, "Bath")
        up += room(170, 90, 140, 70, "Primary Suite" if beds == 2 else "Bedroom")
        if beds == 3:
            up = room(170, 20, 70, 70, "Bedroom") + room(240, 20, 70, 70, "Bedroom") + room(170, 90, 90, 70, "Primary") + room(260, 90, 50, 70, "Bath")
        g += up + f'<text x="240" y="185" {lbl} font-weight="700">Level 2</text>'
        return f'<svg viewBox="0 0 320 195" role="img" aria-label="Illustrative two-level townhome layout">{g}</svg>'
    if beds == 1:
        g = room(20, 20, 150, 100, "Living") + room(170, 20, 130, 100, "Bedroom") + room(20, 120, 100, 55, "Kitchen") + room(120, 120, 80, 55, "Bath") + room(200, 120, 100, 55, "Closet")
    elif beds == 2:
        g = room(20, 20, 120, 155, "Living") + room(140, 20, 90, 80, "Bedroom") + room(230, 20, 80, 80, "Bedroom") + room(140, 100, 90, 75, "Kitchen") + room(230, 100, 80, 75, "Bath")
    else:
        g = room(20, 20, 110, 100, "Living") + room(130, 20, 90, 75, "Bedroom") + room(220, 20, 90, 75, "Bedroom") + room(20, 120, 110, 55, "Kitchen") + room(130, 95, 90, 80, "Primary") + room(220, 95, 90, 80, "Bath")
    return f'<svg viewBox="0 0 330 195" role="img" aria-label="Illustrative {beds}-bedroom layout">{g}</svg>'

def fmt_baths(b):
    return str(int(b)) if b == int(b) else str(b)

def plan_cards(limit=None):
    out = []
    for name, key, beds, baths, sqft, price, kind in PLANS[:limit]:
        tag = "Townhome" if kind == "Townhome" else f"{beds} Bedroom"
        slug = name.replace("The ", "").replace("ó", "o").lower()
        out.append(f'''<article class="plan reveal" data-cat="{key}">
  <div class="plan__drawing"><span class="plan__tag">{tag}</span>{plan_svg(beds, kind)}</div>
  <div class="plan__body">
    <h3>{name}</h3>
    <ul class="plan__specs">
      <li>{icon("bed")}{beds} Bed</li><li>{icon("bath")}{fmt_baths(baths)} Bath</li><li>{icon("ruler")}{sqft:,} sq ft</li>
    </ul>
    <!-- [confirm] beds/baths/sq ft per plan and current starting rent; market range ~$1,000–$1,600 -->
    <p class="plan__price">Starting at<strong>${price:,}<span style="font-size:.9rem;color:var(--muted)">/mo*</span></strong></p>
    <a class="btn" href="/contact/?plan={slug}#tour">Check Availability</a>
  </div>
</article>''')
    return "\n".join(out)

# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def build_home():
    slides = [
        ("hero-pool", "Resort-style days", "Sunlit pool days, <em>steps from home.</em>",
         "Unwind by the sparkling pool at Los Arcos Apartments, a gated, garden-style community residents call peaceful.",
         "/amenities/", "Explore Amenities"),
        ("hero-living", "Space to breathe", "Apartments &amp; townhomes <em>with room to grow.</em>",
         "Los Arcos Apartments offers one-, two- and three-bedroom homes plus townhomes, from 550 to nearly 1,500 square feet.",
         "/floor-plans/", "View Floor Plans"),
        ("hero-skyline", "Southwest Houston", "Quiet streets. <em>Quick commutes.</em>",
         "Los Arcos Apartments is tucked into Brays Oaks, with easy drives to the Galleria, the Texas Medical Center and downtown.",
         "/neighborhood/", "See the Neighborhood"),
    ]
    sl, msgs, dots = [], [], []
    for n, (k, eb, h, p, href, btn) in enumerate(slides):
        sl.append(f'<div class="hero__slide{" is-active" if n == 0 else ""}">{img(k, eager=(n == 0), lazy_src=(n > 0), alt="")}</div>')
        tag = "p"
        msgs.append(f'''<div class="hero__msg{" is-active" if n == 0 else ""}" aria-hidden="{"false" if n == 0 else "true"}">
          <span class="eyebrow">{eb}</span>
          <{tag} class="hero__title" style="font-family:var(--serif);line-height:1.05;letter-spacing:-.02em">{h}</{tag}>
          <p>{p}</p>
          <div class="btn-row"><a class="btn" href="{href}">{btn} {icon("arrow")}</a><a class="btn btn--outline-light" href="/contact/#tour">Schedule a Tour</a></div>
        </div>''')
        dots.append(f'<button class="hero__dot{" is-active" if n == 0 else ""}" type="button" aria-label="Show slide {n + 1}: {eb}"><span></span></button>')

    tiles = [
        ("am-pool-plants", "Amenities", "Pool, gated grounds &amp; on-site laundry", "/amenities/"),
        ("in-living-warm", "Floor Plans", "1, 2 &amp; 3 bedrooms plus townhomes", "/floor-plans/"),
        ("ext-garden", "Gallery", "Take a look around the community", "/gallery/"),
    ]
    tile_html = "".join(f'''<a class="tile reveal" data-delay="{i}" href="{href}">
      <div class="tile__img">{img(k, sizes="(max-width:900px) 100vw, 400px")}</div>
      <div class="tile__body"><div><h2>{t}</h2><p>{s}</p></div><span class="tile__go">{icon("arrow-ur")}</span></div>
    </a>''' for i, (k, t, s, href) in enumerate(tiles))

    strip_keys = ["in-kitchen-white", "am-pool-city", "in-bed-classic", "ext-path", "in-living-blue", "am-laundry", "in-arches", "ext-townhome"]
    strip = "".join(f'<a href="/gallery/" aria-label="View gallery: {html.escape(IMAGES[k]["alt"])}">{img(k, sizes="320px", alt="")}</a>' for k in strip_keys)

    themes = [
        ("moon", "Quiet &amp; peaceful", "The word residents use most. Los Arcos Apartments is a calm, low-key place to come home to."),
        ("leaf", "Clean, cared-for grounds", "Well-kept landscaping and tidy common areas come up again and again."),
        ("smile", "Friendly, helpful staff", "Reviewers regularly mention a leasing and maintenance team that makes them feel welcome."),
        ("home", "Beautiful, cozy homes", "Spacious layouts with a warm, comfortable feel, from one-bedrooms to two-story townhomes."),
    ]
    theme_html = "".join(f'<div class="theme reveal" data-delay="{i % 2}">{icon(ic)}<h3>{t}</h3><p>{d}</p></div>' for i, (ic, t, d) in enumerate(themes))

    mq_items = ["Gated community", "Sparkling pool", "Garden courtyards", "1, 2 &amp; 3 bedrooms", "Townhomes", "On-site laundry", "Quiet &amp; peaceful", "Southwest Houston"]
    mq_group = "".join(f"<span>{t}</span><i></i>" for t in mq_items)
    marquee = (f'<div class="marquee" aria-label="Community highlights"><div class="marquee__track">'
               f'<div class="marquee__group">{mq_group}</div><div class="marquee__group" aria-hidden="true">{mq_group}</div></div></div>')
    body = f'''<section class="hero" aria-roledescription="carousel" aria-label="Welcome to Los Arcos">
  <div class="hero__slides">{"".join(sl)}</div>
  <div class="hero__inner">
    <div class="wrap">
      <div aria-live="polite">{"".join(msgs)}</div>
      <div class="hero__controls">
        <div class="hero__dots">{"".join(dots)}</div>
        <button class="hero__pause" type="button" aria-label="Pause slideshow"></button>
      </div>
    </div>
  </div>
  <a class="scroll-cue" href="#intro" aria-label="Scroll to introduction"><span></span></a>
  <a class="hero__arch" href="{GMAPS}" target="_blank" rel="noopener" style="color:#fff;text-decoration:none">
    <strong>{P["rating"]}</strong><span class="sr-only"> out of 5 stars from</span><div class="stars" aria-hidden="true">★★★★★</div><small>{P["reviews"]} Google reviews</small><span class="sr-only"> (opens Google Maps)</span>
  </a>
</section>

<div class="wrap"><div class="tiles">{tile_html}</div></div>

<section class="section" id="intro">
  <div class="wrap split">
    <div class="split__media reveal">
      <div class="arch-img">{img("ext-garden", sizes="(max-width:860px) 90vw, 560px", alt="Garden-style apartment buildings surrounded by mature trees")}</div>
      <div class="arch-img arch-img--small">{img("am-pool-plants", sizes="240px", alt="Community swimming pool framed by plants")}</div>
      <div class="badge"><strong data-count="{P["units"]}">{P["units"]}</strong><span>homes on a<br>gated, garden-style campus</span></div>
    </div>
    <div class="reveal" data-delay="1">
      <span class="eyebrow">A quiet retreat in Southwest Houston</span>
      <h1>Spacious Apartments &amp; Townhomes in <em>Southwest Houston</em></h1>
      <p class="lead">Los Arcos Apartments is a gated, garden-style community on Fondren Road in the Brays Oaks neighborhood, where tree-shaded courtyards, a sparkling pool and genuinely friendly neighbors set a slower, calmer pace.</p>
      <p>Choose from one-, two- and three-bedroom apartments or two-story townhomes ranging from 550 to 1,498 square feet. Residents tell us what they love most about Los Arcos Apartments is the peace and quiet, the clean, well-kept grounds and a leasing team that knows them by name.</p>
      <div class="stats">
        <div><strong><span data-count="{P["rating"]}">{P["rating"]}</span>★</strong><span>{P["reviews"]} Google reviews</span></div>
        <div><strong>550–1,498</strong><span>square feet</span></div>
        <div><strong>1–3 BR</strong><span>plus townhomes</span></div>
      </div>
      <div class="btn-row"><a class="btn" href="/floor-plans/">Explore Floor Plans {icon("arrow")}</a><a class="btn btn--ghost" href="/amenities/">View Amenities</a></div>
    </div>
  </div>
</section>

<section aria-label="Photo highlights" style="padding-bottom:clamp(48px,7vw,96px)">
  <div class="wrap section-head reveal" style="margin-bottom:28px">
    <div><span class="eyebrow">Life at Los Arcos Apartments</span><h2>Light-filled rooms, <em>shaded courtyards</em></h2></div>
    <a class="link-arrow" href="/gallery/">Open the full gallery {icon("arrow").replace('<svg', '<svg style="width:18px;height:18px"')}</a>
  </div>
  <div class="strip">{strip}</div>
</section>

{marquee}
<section class="section section--dark arch-top" id="reviews">
  <div class="wrap reviews">
    <div class="rating-card reveal">
      <span class="g-mark">{icon("star").replace('<svg', '<svg style="width:18px;height:18px"')} Google Reviews</span>
      <div class="big">{P["rating"]}</div>
      <div class="stars" aria-hidden="true">★★★★★</div>
      <p>Los Arcos Apartments averages {P["rating"]} stars from <strong style="color:#fff"><span data-count="350" data-suffix="+">350+</span> reviews</strong>, including <strong style="color:#fff"><span data-count="{P["five_star"]}">{P["five_star"]}</span> five-star</strong> ratings.</p>
      <a class="btn btn--light" href="{GMAPS}" target="_blank" rel="noopener">Read reviews on Google {icon("arrow-ur")}</a>
    </div>
    <div>
      <span class="eyebrow">What residents say</span>
      <h2 class="reveal">Rated <em>{P["rating"]} stars</em> by the people who live here.</h2>
      <p class="lead reveal">Across hundreds of Google reviews of Los Arcos Apartments, the same themes keep coming up.</p>
      <div class="themes">{theme_html}</div>
      <p class="disclaimer">Themes summarized from public Google reviews. Rating and review count as listed on Google Maps.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <div><span class="eyebrow">Floor plans</span><h2>Find the layout that <em>feels like home</em></h2><p class="lead" style="margin-top:14px">Every home at Los Arcos Apartments is designed for easy, comfortable living, with generous closets and natural light.</p></div>
      <a class="btn btn--ghost" href="/floor-plans/">See all floor plans</a>
    </div>
    <div class="plans">{plan_cards(3)}</div>
    <p class="note" style="margin-top:18px">*Pricing shown is illustrative and subject to change. Contact the leasing office for current availability and rates.</p>
  </div>
</section>

{cta_band()}'''
    page("/", "Los Arcos Apartments & Townhomes | Southwest Houston, TX 77035",
         "Gated garden-style apartments and townhomes on Fondren Rd in Southwest Houston. 1, 2 & 3 bedrooms, pool, on-site laundry. Rated 4.6★ on Google. Schedule a tour.",
         body, active="/", preload="hero-pool")


def build_amenities():
    community = [
        ("pool", "Swimming pool", "A sparkling pool for slow summer afternoons"),
        ("gate", "Gated community", "Controlled-access entry for added peace of mind"),
        ("car", "On-site parking", "Convenient resident and guest parking"),
        ("access", "Accessible entrance &amp; parking", "Wheelchair-accessible entry and designated parking"),
        ("laundry", "Laundry facilities", "On-site laundry rooms for residents"),
        ("leaf", "Garden courtyards", "Tree-shaded green space between buildings", True),
        ("users", "On-site management", "A friendly leasing and maintenance team close by", True),
        ("paw", "Pet-friendly community", "Ask about our pet policy, breeds and fees", True),
    ]
    home = [
        ("kitchen", "Full kitchens", "Ample counter and cabinet space"),
        ("snow", "Central air &amp; heat", "Stay comfortable through Houston summers"),
        ("closet", "Generous closets", "Walk-in closets in select plans"),
        ("balcony", "Private patio or balcony", "Outdoor space in select homes"),
        ("fan", "Ceiling fans", "In living areas and bedrooms"),
        ("wash", "Washer/dryer connections", "Available in townhomes and select plans"),
        ("door", "Two-story townhomes", "Private entry and multi-level living"),
        ("sun", "Natural light", "Large windows in every layout"),
    ]
    def li(items):
        out = []
        for it in items:
            ic, t, s = it[0], it[1], it[2]
            conf = len(it) > 3
            c = "<!-- [confirm] amenity not on verified list -->" if conf else ""
            out.append(f'<li>{c}{icon(ic)}<div><strong>{t}</strong><span>{s}</span></div></li>')
        return "".join(out)
    body = page_hero("Amenities", "Amenities designed for <em>easy, everyday living</em>",
                     "Gated grounds, a sparkling pool and comfortable homes with room to spread out: everything you need for a calm, connected life in Southwest Houston.",
                     "am-pool-plants", "Amenities") + f'''
<section class="section">
  <div class="wrap amenity-group">
    <div class="sticky-media reveal">
      <span class="eyebrow">Community amenities</span>
      <h2>Shared spaces with a <em>resort-calm</em> feel</h2>
      <p class="lead">Spend the afternoon by the pool, stroll the shaded courtyards, and come home through a gated entry every evening.</p>
      <div class="arch-img" style="aspect-ratio:4/3;margin-top:28px">{img("hero-pool", sizes="(max-width:900px) 100vw, 480px")}</div>
    </div>
    <!-- Verified amenities: pool, on-site parking, accessible entrance & parking, gated, laundry. Others marked [confirm]. -->
    <ul class="amenity-list">{li(community)}</ul>
  </div>
</section>

<section class="section section--dark arch-top">
  <div class="wrap amenity-group">
    <!-- [confirm] all apartment features below with management before launch -->
    <ul class="amenity-list" style="order:2">{li(home)}</ul>
    <div class="sticky-media reveal">
      <span class="eyebrow">Apartment features</span>
      <h2>Homes that feel <em>spacious and warm</em></h2>
      <p class="lead">Every layout is designed around comfortable living, with generous square footage that runs from 550 to 1,498 square feet.</p>
      <div class="arch-img" style="aspect-ratio:4/3;margin-top:28px">{img("in-living-classic", sizes="(max-width:900px) 100vw, 480px")}</div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap grid-3">
    <div class="card reveal"><div class="icon-chip">{icon("shield")}</div><h3>Peace of mind</h3><p>A gated, garden-style community with a long-standing reputation for being quiet and well kept.</p></div>
    <div class="card reveal" data-delay="1"><div class="icon-chip">{icon("tools")}</div><h3>Responsive service</h3><p>Submit maintenance requests online any time through the resident portal.</p></div>
    <div class="card reveal" data-delay="2"><div class="icon-chip">{icon("pin")}</div><h3>Central location</h3><p>Minutes to Beltway 8, I-69 and US-90A for easy drives across Houston.</p><!-- [confirm] highway access wording --></div>
  </div>
</section>
{cta_band()}'''
    page("/amenities/", "Amenities | Pool, Gated Community & Laundry | Los Arcos Houston",
         "Explore amenities at Los Arcos Apartments in Southwest Houston: swimming pool, gated entry, on-site parking and laundry, accessible features and spacious homes.",
         body)


def build_floorplans():
    body = page_hero("Floor plans", "Floor plans from <em>550 to 1,498 sq ft</em>",
                     "Choose a one-, two- or three-bedroom apartment, or a two-story townhome with room for everyone. Filter by bedrooms to find your fit.",
                     "in-living-warm", "Floor Plans") + f'''
<section class="section">
  <div class="wrap">
    <h2 class="sr-only">Available floor plans</h2>
    <div class="filters" role="group" aria-label="Filter floor plans by bedrooms" data-filter-group="#plan-grid">
      <button class="filter" type="button" data-filter="all" aria-pressed="true">All Plans</button>
      <button class="filter" type="button" data-filter="1" aria-pressed="false">1 Bedroom</button>
      <button class="filter" type="button" data-filter="2" aria-pressed="false">2 Bedrooms</button>
      <button class="filter" type="button" data-filter="3" aria-pressed="false">3 Bedrooms</button>
      <button class="filter" type="button" data-filter="th" aria-pressed="false">Townhomes</button>
      <span class="sr-only" data-filter-status aria-live="polite"></span>
    </div>
    <div class="plans" id="plan-grid">{plan_cards()}</div>
    <p class="note" style="margin-top:24px">*Pricing, square footage and availability are illustrative and subject to change. Floor plan drawings are representative only. Contact the leasing office at <a href="tel:{P["tel"]}">{P["phone"]}</a> for current rates and move-in specials.</p>
  </div>
</section>
<section class="section section--sand">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Not sure which plan?</span>
      <h2>Let us help you <em>find the right fit</em></h2>
      <p class="lead">Tell us your move-in date, budget and must-haves, and our leasing team will match you with available homes, including any current specials.</p>
      <div class="btn-row"><a class="btn" href="/contact/#tour">Schedule a Tour</a><a class="btn btn--ghost" href="/apply/">Apply Now</a></div>
    </div>
    <div class="split__media reveal" data-delay="1"><div class="arch-img" style="aspect-ratio:1">{img("ext-townhome", sizes="(max-width:860px) 90vw, 520px")}</div></div>
  </div>
</section>'''
    page("/floor-plans/", "Floor Plans | 1, 2 & 3 Bedroom Apartments & Townhomes | Los Arcos",
         "Compare 1, 2 and 3 bedroom apartments and townhomes at Los Arcos in Houston, TX 77035. 550–1,498 sq ft. Filter by bedrooms and check availability.",
         body)


def build_gallery():
    order = ["hero-pool", "in-living-warm", "ext-garden", "in-kitchen-white", "am-pool-plants", "in-bed-classic",
             "ext-building", "in-arches", "am-laundry", "in-living-blue", "ext-path", "in-bath", "am-courtyard",
             "in-kitchen-island", "ext-townhome", "in-bed-modern", "am-pool-city", "in-dining", "ext-porch",
             "in-living-plants", "ext-stucco", "in-bed-tufted", "in-kitchen-dark", "ext-street", "in-bath-glass",
             "in-living-dog", "in-bed-hotel", "in-living-open", "hero-living"]
    figs = []
    for n, k in enumerate(order):
        cat = IMAGES[k]["cat"]
        gw, gh = dims(k, 900)
        span = round((400 * gh / gw + 16) / 4)  # rows of 4px at ~400px column width
        figs.append(f'<figure data-cat="{cat}" style="--span:{span}"><button type="button" data-full="/img/{k}-1600.webp" aria-label="Enlarge photo: {html.escape(IMAGES[k]["alt"], quote=True)}">{img(k, sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 400px", eager=(n < 3), nolazy=(n < 6))}</button><figcaption>{cat.title()}</figcaption></figure>')
    body = page_hero("Gallery", "A look around <em>Los Arcos</em>",
                     "Browse interiors, exteriors and amenities. Select any photo to view it larger.", None, "Gallery") + f'''
<section class="section" style="padding-top:48px">
  <div class="wrap">
    <h2 class="sr-only">Community photos</h2>
    <div class="filters" role="group" aria-label="Filter photos" data-filter-group="#gallery-grid">
      <button class="filter" type="button" data-filter="all" aria-pressed="true">All Photos</button>
      <button class="filter" type="button" data-filter="interiors" aria-pressed="false">Interiors</button>
      <button class="filter" type="button" data-filter="exteriors" aria-pressed="false">Exteriors</button>
      <button class="filter" type="button" data-filter="amenities" aria-pressed="false">Amenities</button>
      <span class="sr-only" data-filter-status aria-live="polite"></span>
    </div>
    <!-- Stock photography for concept only; replace with property photos (see IMAGES.md) -->
    <div class="masonry" id="gallery-grid">{"".join(figs)}</div>
  </div>
</section>
<div class="lightbox" role="dialog" aria-modal="true" aria-label="Photo viewer" aria-hidden="true">
  <button class="lb-btn lb-close" type="button" aria-label="Close photo viewer">{icon("x")}</button>
  <button class="lb-btn lb-prev" type="button" aria-label="Previous photo">{icon("left")}</button>
  <img src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" alt="">
  <button class="lb-btn lb-next" type="button" aria-label="Next photo">{icon("right")}</button>
  <p class="lightbox__cap"></p>
</div>
{cta_band()}'''
    page("/gallery/", "Photo Gallery | Interiors, Exteriors & Amenities | Los Arcos Houston",
         "View photos of Los Arcos Apartments & Townhomes in Southwest Houston: interiors, exteriors, pool and community amenities.",
         body)


def build_tours():
    tabs = [("in-living-warm", "1 Bedroom"), ("in-living-open", "2 Bedroom"), ("in-dining", "3 Bedroom"), ("ext-townhome", "Townhome")]
    tab_html = "".join(f'<button class="filter" type="button" data-tour data-img="/img/{k}-1600.webp" data-alt="{html.escape(IMAGES[k]["alt"], quote=True)}" aria-pressed="{"true" if i == 0 else "false"}">{t}</button>' for i, (k, t) in enumerate(tabs))
    body = page_hero("Virtual tours", "Tour Los Arcos <em>from anywhere</em>",
                     "Walk through our homes and grounds at your own pace. Interactive 3D tours and video walkthroughs are coming soon.", "in-arches", "Virtual Tours") + f'''
<section class="section">
  <div class="wrap">
    <div class="tour-frame reveal">
      <!-- 3D TOUR EMBED: replace this block with the Matterport / YouTube iframe, e.g.
           <iframe src="https://my.matterport.com/show/?m=XXXX" allowfullscreen loading="lazy" title="3D tour"></iframe> -->
      {img("in-living-warm", sizes="(max-width:1240px) 100vw, 1240px", alt="Preview of a one-bedroom living room")}
      <div class="tour-frame__ui">
        <button class="play" type="button" aria-label="Play virtual tour (coming soon)" data-placeholder="Demo: the 3D tour or video walkthrough will play here.">{icon("play")}</button>
        <p data-tour-label>1 Bedroom — 3D tour coming soon</p>
      </div>
    </div>
    <div class="tour-tabs" role="group" aria-label="Choose a tour">{tab_html}</div>
  </div>
</section>
<section class="section section--sand">
  <h2 class="sr-only">Ways to tour</h2>
  <div class="wrap grid-3">
    <div class="card reveal"><div class="icon-chip">{icon("cube")}</div><h3>3D walkthroughs</h3><p>Move room to room and see how each layout flows before you visit.</p></div>
    <div class="card reveal" data-delay="1"><div class="icon-chip">{icon("play")}</div><h3>Video tours</h3><p>Prefer a guided look? Ask us for a live video tour with a leasing professional.</p></div>
    <div class="card reveal" data-delay="2"><div class="icon-chip">{icon("calendar")}</div><h3>In-person visits</h3><p>Nothing beats seeing it yourself. Book a time Monday through Saturday.</p></div>
  </div>
</section>
{cta_band()}'''
    page("/virtual-tours/", "Virtual Tours | 3D & Video Apartment Tours | Los Arcos Houston",
         "Take a virtual tour of Los Arcos Apartments & Townhomes in Southwest Houston. Explore 1, 2 and 3 bedroom homes and townhomes online, then schedule a visit.",
         body)


def build_neighborhood():
    groups = [
        ("bag", "Shopping &amp; errands", [("Fondren Rd shops &amp; groceries", "≈ 2–5 min"), ("Meyerland Plaza", "≈ 10 min"), ("PlazAmericas", "≈ 12 min"), ("The Galleria", "≈ 20 min")]),
        ("fork", "Dining", [("Hillcroft / Mahatma Gandhi District", "≈ 12 min"), ("Bellaire Blvd (Chinatown)", "≈ 15 min"), ("Rice Village", "≈ 20 min"), ("Downtown dining", "≈ 25 min")]),
        ("tree", "Parks &amp; outdoors", [("Willow Waterhole Greenway", "≈ 5 min"), ("Brays Bayou Greenway trails", "≈ 8 min"), ("Hermann Park &amp; Houston Zoo", "≈ 20 min"), ("Buffalo Bayou Park", "≈ 25 min")]),
        ("school", "Schools &amp; education", [("Houston ISD schools (verify zoning)", "Nearby"), ("Houston Christian University", "≈ 10 min"), ("Rice University", "≈ 20 min"), ("Texas Southern / UH", "≈ 25 min")]),
    ]
    cards = "".join(f'''<div class="card reveal" data-delay="{i % 2}"><div class="icon-chip">{icon(ic)}</div><h3>{t}</h3>
      <!-- [confirm] place names and drive times -->
      <ul class="places">{"".join(f"<li><span>{n}</span><span>{d}</span></li>" for n, d in items)}</ul></div>''' for i, (ic, t, items) in enumerate(groups))
    body = page_hero("Neighborhood", "Life in <em>Brays Oaks</em>, Southwest Houston",
                     "A quiet residential pocket off Fondren Road with everyday shopping close by, green trails nearby, and easy drives to Houston's biggest job centers.",
                     "ext-street", "Neighborhood") + f'''
<section class="section">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Find us</span>
      <h2>{P["street"]}<br><em>{P["city"]}, {P["state"]} {P["zip"]}</em></h2>
      <p class="lead">Located in the {P["area"]} area, close to Beltway 8, I-69 and US-90A.</p><!-- [confirm] highway access -->
      <div class="btn-row"><a class="btn" href="{DIRECTIONS}" target="_blank" rel="noopener">Get Directions {icon("arrow-ur")}</a><a class="btn btn--ghost" href="tel:{P["tel"]}">{icon("phone")} {P["phone"]}</a></div>
    </div>
    <div class="map reveal" data-delay="1"><iframe src="{MAP_EMBED}" title="Map showing Los Arcos Apartments at 11315 Fondren Rd, Houston" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
  </div>
</section>
<section class="section section--dark arch-top">
  <div class="wrap">
    <div class="center reveal" style="margin-bottom:44px"><span class="eyebrow">Commute times</span><h2>Close to <em>where Houston works</em></h2></div>
    <!-- [confirm] approximate off-peak drive times -->
    <div class="commute">
      <div class="reveal"><strong>≈ 20</strong><span>minutes to the Galleria / Uptown</span></div>
      <div class="reveal" data-delay="1"><strong>≈ 18</strong><span>minutes to the Texas Medical Center</span></div>
      <div class="reveal" data-delay="2"><strong>≈ 25</strong><span>minutes to Downtown Houston</span></div>
    </div>
    <p class="center disclaimer" style="margin-top:20px">Approximate off-peak drive times. Actual times vary with traffic.</p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><div><span class="eyebrow">Nearby</span><h2>Everything you need, <em>minutes away</em></h2></div></div>
    <div class="grid-2">{cards}</div>
  </div>
</section>
{cta_band()}'''
    page("/neighborhood/", "Neighborhood | Brays Oaks & Fondren Southwest Apartments | Los Arcos",
         "Discover the Brays Oaks / Fondren Southwest neighborhood around Los Arcos Apartments: nearby shopping, dining, parks, schools and commutes to the Galleria, Medical Center and downtown.",
         body)


def build_residents():
    body = page_hero("Residents", "Welcome home, <em>residents</em>",
                     "Pay rent, request maintenance and manage your account online, any time of day.", "in-living-dog", "Residents") + f'''
<section class="section">
  <div class="wrap">
    <!-- [confirm] replace placeholder links with the property's live resident portal URLs -->
    <div class="portal-btns">
      <a class="portal reveal" href="{PAY_URL}" data-placeholder="Demo: Pay Rent will open the resident payment portal.">
        <div class="icon-chip">{icon("card")}</div><h2>Pay Rent</h2><p>Make a one-time payment or set up autopay securely online.</p><span class="link-arrow">Pay now {icon("arrow").replace('<svg', '<svg style="width:16px;height:16px"')}</span></a>
      <a class="portal reveal" data-delay="1" href="{MAINT_URL}" data-placeholder="Demo: Maintenance Request will open the service request form.">
        <div class="icon-chip">{icon("wrench")}</div><h2>Maintenance Request</h2><p>Submit and track service requests, with photos if needed.</p><span class="link-arrow">Submit request {icon("arrow").replace('<svg', '<svg style="width:16px;height:16px"')}</span></a>
      <a class="portal reveal" data-delay="2" href="{PORTAL_URL}" data-placeholder="Demo: Resident Portal will open the resident login.">
        <div class="icon-chip">{icon("home")}</div><h2>Resident Portal</h2><p>View your lease, statements and community notices.</p><span class="link-arrow">Log in {icon("arrow").replace('<svg', '<svg style="width:16px;height:16px"')}</span></a>
    </div>
  </div>
</section>
<section class="section section--sand">
  <div class="wrap">
    <div class="section-head reveal"><div><span class="eyebrow">Resident resources</span><h2>Helpful <em>information</em></h2></div></div>
    <div class="grid-3">
      <div class="card reveal"><div class="icon-chip">{icon("bolt")}</div><h3>Emergency maintenance</h3><p>For fire, flooding, gas leaks or no heat/AC in extreme weather, call the office at <a href="tel:{P["tel"]}">{P["phone"]}</a>. After hours, follow the prompts for the on-call technician. For life-threatening emergencies, call 911.</p><!-- [confirm] after-hours process --></div>
      <div class="card reveal" data-delay="1"><div class="icon-chip">{icon("sun")}</div><h3>Utilities &amp; services</h3><p>Set up electricity with a Texas retail provider of your choice before move-in. Ask the office which utilities are included in your lease.</p><!-- [confirm] utility setup details --></div>
      <div class="card reveal" data-delay="2"><div class="icon-chip">{icon("shield")}</div><h3>Renter's insurance</h3><p>We recommend every household carry renter's insurance to protect personal belongings. Ask the office about lease requirements.</p><!-- [confirm] insurance requirement --></div>
      <div class="card reveal"><div class="icon-chip">{icon("trash")}</div><h3>Trash &amp; recycling</h3><p>Please use the community dumpsters and keep breezeways clear so the grounds stay as clean as residents love them.</p></div>
      <div class="card reveal" data-delay="1"><div class="icon-chip">{icon("laundry")}</div><h3>Laundry facilities</h3><p>On-site laundry rooms are available for residents. Please remove items promptly when cycles finish.</p></div>
      <div class="card reveal" data-delay="2"><div class="icon-chip">{icon("users")}</div><h3>Refer a friend</h3><p>Love living here? Ask the leasing office about referral rewards for new residents you send our way.</p><!-- [confirm] referral program --></div>
    </div>
  </div>
</section>
{cta_band("Questions? <em>We're here to help.</em>", f"Stop by the leasing office Monday through Saturday, 9 AM to 5 PM, or call us at {P['phone']}.")}'''
    page("/residents/", "Resident Services | Pay Rent & Maintenance | Los Arcos Houston",
         "Los Arcos resident services: pay rent online, submit maintenance requests, access the resident portal and find helpful community resources.",
         body)


FAQS = [
    ("pets", "Pets", [
        ("Is Los Arcos pet-friendly?", "Please contact the leasing office for our current pet policy, including any breed or weight restrictions, pet deposits and monthly pet rent. <!-- [confirm] pet policy -->"),
        ("Are assistance animals allowed?", "Yes. Assistance animals for residents with disabilities are welcome in accordance with fair housing laws and are not subject to pet fees."),
    ]),
    ("lease", "Lease terms", [
        ("What lease terms do you offer?", "We offer a range of lease lengths. Ask the leasing team about current options and pricing for each term. <!-- [confirm] lease terms -->"),
        ("Do you have move-in specials?", "Specials change throughout the year. Call or visit the office to hear about current move-in offers."),
    ]),
    ("parking", "Parking", [
        ("Is parking available?", "Yes. Los Arcos offers on-site parking for residents, including wheelchair-accessible parking spaces."),
        ("Where can guests park?", "Guests may use designated visitor parking. Please ask the office about any guest parking guidelines. <!-- [confirm] guest parking -->"),
    ]),
    ("utilities", "Utilities", [
        ("Which utilities are included?", "Utility inclusions vary by floor plan. The leasing office can give you a full breakdown for the home you choose. <!-- [confirm] included utilities -->"),
        ("Is there laundry on site?", "Yes. Residents have access to on-site laundry facilities."),
    ]),
    ("apply", "Applying", [
        ("What do I need to apply?", "Typically a completed application for each adult, a government-issued photo ID, proof of income and the application fee. A background and credit check is part of the process. <!-- [confirm] application requirements, income ratio, fees -->"),
        ("How long does approval take?", "Most applications are reviewed within a few business days once all documents are received. <!-- [confirm] -->"),
        ("Can I apply online?", "Yes. Use the Apply Now button to start your application online at any time."),
    ]),
    ("hours", "Office hours", [
        ("When is the leasing office open?", "Monday through Saturday, 9:00 AM to 5:00 PM. The office is closed on Sundays."),
        ("Do I need an appointment to tour?", "Walk-ins are welcome during office hours, but booking ahead guarantees a leasing professional is ready for you."),
    ]),
]

def build_faqs():
    nav = "".join(f'<a href="#faq-{k}">{t}</a>' for k, t, _ in FAQS)
    groups = "".join(f'''<div class="faq-group" id="faq-{k}"><h2>{t}</h2>{"".join(f'<details class="faq"><summary>{q}</summary><div class="faq__a"><p>{a}</p></div></details>' for q, a in qs)}</div>''' for k, t, qs in FAQS)
    def strip_comments(s):
        import re
        return re.sub(r"<!--.*?-->", "", s).strip()
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_comments(a)}} for _, _, qs in FAQS for q, a in qs]}
    body = page_hero("FAQs", "Frequently asked <em>questions</em>",
                     "Quick answers about pets, leases, parking, utilities, applying and office hours. Still curious? Our team is happy to help.", None, "FAQs") + f'''
<section class="section">
  <div class="wrap faq-cats">
    <nav class="faq-nav" aria-label="FAQ topics">{nav}</nav>
    <div>{groups}</div>
  </div>
</section>
{cta_band("Still have <em>questions?</em>", f"Call the leasing office at {P['phone']} or send us a message, and we'll get right back to you.")}'''
    page("/faqs/", "FAQs | Pets, Leases, Parking & Applying | Los Arcos Apartments",
         "Answers to common questions about Los Arcos Apartments in Houston: pet policy, lease terms, parking, utilities, application requirements and office hours.",
         body, extra_head='<script type="application/ld+json">' + json.dumps(faq_ld, ensure_ascii=False) + "</script>")


def build_contact():
    plan_opts = '<option value="">No preference</option>' + "".join(
        f'<option value="{n.replace("The ", "").replace("ó", "o").lower()}">{n} ({"Townhome" if k == "Townhome" else f"{b} BR"})</option>' for n, _, b, _, _, _, k in PLANS)
    times = "".join(f'<option>{t}</option>' for t in ["9:00 AM", "9:30 AM", "10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM", "12:00 PM", "12:30 PM", "1:00 PM", "1:30 PM", "2:00 PM", "2:30 PM", "3:00 PM", "3:30 PM", "4:00 PM", "4:30 PM"])
    success = lambda h, p: f'<div class="form-success" role="status" aria-live="polite"><div class="check">{icon("check")}</div><h3>{h}</h3><p>{p}</p></div>'
    body = page_hero("Contact &amp; tours", "Schedule a tour or <em>say hello</em>",
                     "Pick a day and time to visit, or send us a question. Our leasing team typically responds within one business day.", "ext-porch", "Contact") + f'''
<section class="section" id="tour">
  <div class="wrap split" style="align-items:start">
    <div class="form-card reveal">
      <span class="eyebrow">Schedule a tour</span>
      <h2 style="font-size:clamp(1.7rem,3vw,2.4rem)">Book your <em>visit</em></h2>
      <form data-demo-form aria-label="Schedule a tour">
        <div class="form-grid">
          <div class="field"><label for="t-first">First name</label><input id="t-first" name="first_name" autocomplete="given-name" required><p class="err">Please enter your first name.</p></div>
          <div class="field"><label for="t-last">Last name</label><input id="t-last" name="last_name" autocomplete="family-name" required><p class="err">Please enter your last name.</p></div>
          <div class="field"><label for="t-email">Email</label><input id="t-email" name="email" type="email" autocomplete="email" required><p class="err">Please enter a valid email.</p></div>
          <div class="field"><label for="t-phone">Phone</label><input id="t-phone" name="phone" type="tel" autocomplete="tel" required><p class="err">Please enter your phone number.</p></div>
          <div class="field"><label for="tour-date">Preferred date</label><input id="tour-date" name="tour_date" type="date" required><p class="hint">Tours available Monday–Saturday.</p><p class="err">Please choose a Monday–Saturday date.</p></div>
          <div class="field"><label for="tour-time">Preferred time</label><select id="tour-time" name="tour_time" required><option value="">Select a time</option>{times}</select><p class="err">Please choose a time.</p></div>
          <div class="field full"><label for="tour-plan">Floor plan of interest</label><select id="tour-plan" name="plan">{plan_opts}</select></div>
          <fieldset class="field full" style="border:0;padding:0;margin:0"><legend style="font-weight:700;font-size:.88rem;margin-bottom:8px">Tour type</legend>
            <div class="chips"><label><input type="radio" name="tour_type" value="In person" checked><span>In person</span></label><label><input type="radio" name="tour_type" value="Live video"><span>Live video</span></label><label><input type="radio" name="tour_type" value="Self-guided"><span>Self-guided</span></label></div></fieldset>
          <div class="field full"><button class="btn" type="submit" style="width:100%">{icon("calendar")} Request My Tour</button></div>
        </div>
      </form>
      {success('Your tour request is in<span data-name></span>!', 'Thanks for choosing Los Arcos. We have your request<span data-when></span> and a member of our leasing team will confirm by phone or email shortly.')}
    </div>
    <div class="reveal" data-delay="1">
      <span class="eyebrow">Leasing office</span>
      <h2 style="font-size:clamp(1.7rem,3vw,2.4rem)">Visit, call or <em>write</em></h2>
      <ul class="info-list">
        <li>{icon("pin")}<div><strong>{P["street"]}</strong><br>{P["city"]}, {P["state"]} {P["zip"]}<br><a href="{DIRECTIONS}" target="_blank" rel="noopener">Get directions</a></div></li>
        <li>{icon("phone")}<div><a href="tel:{P["tel"]}" style="font-size:1.25rem">{P["phone"]}</a><br><span class="note">Tap to call the leasing office</span></div></li>
        <li>{icon("clock")}<div style="flex:1"><table class="hours"><tbody><tr><td>Monday – Friday</td><td>9:00 AM – 5:00 PM</td></tr><tr><td>Saturday</td><td>9:00 AM – 5:00 PM</td></tr><tr><td>Sunday</td><td>Closed</td></tr></tbody></table></div></li>
      </ul>
      <div class="map" style="margin-top:28px;aspect-ratio:4/3"><iframe src="{MAP_EMBED}" title="Map to the Los Arcos leasing office" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
    </div>
  </div>
</section>
<section class="section section--sand" id="message">
  <div class="wrap narrow">
    <div class="form-card reveal">
      <span class="eyebrow">Send a message</span>
      <h2 style="font-size:clamp(1.7rem,3vw,2.4rem)">Questions? <em>Ask away.</em></h2>
      <form data-demo-form aria-label="Contact form">
        <div class="form-grid">
          <div class="field"><label for="c-name">Full name</label><input id="c-name" name="name" autocomplete="name" required><p class="err">Please enter your name.</p></div>
          <div class="field"><label for="c-email">Email</label><input id="c-email" name="email" type="email" autocomplete="email" required><p class="err">Please enter a valid email.</p></div>
          <div class="field"><label for="c-phone">Phone (optional)</label><input id="c-phone" name="phone" type="tel" autocomplete="tel"></div>
          <div class="field"><label for="c-move">Desired move-in</label><select id="c-move" name="move_in"><option>As soon as possible</option><option>Within 30 days</option><option>1–2 months</option><option>3+ months</option></select></div>
          <div class="field full"><label for="c-msg">Message</label><textarea id="c-msg" name="message" required></textarea><p class="err">Please include a short message.</p></div>
          <div class="field full"><button class="btn" type="submit" style="width:100%">{icon("mail")} Send Message</button></div>
        </div>
      </form>
      {success('Message sent<span data-name></span>!', 'Thank you for reaching out. Our leasing team will reply within one business day.')}
    </div>
  </div>
</section>'''
    page("/contact/", "Contact & Schedule a Tour | Los Arcos Apartments Houston",
         "Schedule a tour of Los Arcos Apartments & Townhomes at 11315 Fondren Rd, Houston, TX 77035. Call (713) 729-6274. Office open Mon–Sat 9 AM–5 PM.",
         body)


def build_apply():
    body = page_hero("Apply now", "Start your <em>application</em>",
                     "Found the one? Apply online in minutes. Have your ID and proof of income ready, and our team will guide you from there.", "in-bed-classic", "Apply Now",
                     extra=f'<div class="btn-row" style="margin-top:24px"><a class="btn" href="{APPLY_URL}" data-placeholder="Demo: this button will open the live online application.">Apply Online {icon("arrow-ur")}</a><a class="btn btn--ghost" href="tel:{P["tel"]}">{icon("phone")} Questions? Call us</a></div>') + f'''
<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><div><span class="eyebrow">How it works</span><h2>Three simple <em>steps</em></h2></div></div>
    <ol class="steps">
      <li class="reveal"><h3>Choose your home</h3><p>Browse <a href="/floor-plans/">floor plans</a> and pick your preferred layout and move-in date.</p></li>
      <li class="reveal" data-delay="1"><h3>Apply online</h3><p>Complete the application for each adult and upload your ID and proof of income.</p></li>
      <li class="reveal" data-delay="2"><h3>Get your keys</h3><p>Once approved, sign your lease, set up utilities and get ready to move in.</p></li>
    </ol>
    <!-- [confirm] application fee, admin fee, income requirement and screening criteria -->
    <p class="note" style="margin-top:28px">Application fees, deposits and qualification criteria apply. Contact the leasing office for full details. Los Arcos is an Equal Housing Opportunity community.</p>
  </div>
</section>
{cta_band()}'''
    page("/apply/", "Apply Now | Online Apartment Application | Los Arcos Houston",
         "Apply online for an apartment or townhome at Los Arcos in Southwest Houston. See what you need to apply and start your application today.",
         body)


def legal_page(path, title, desc, h1, crumbs, content):
    body = page_hero("Los Arcos", h1, desc, None, crumbs) + f'<section class="section"><div class="wrap prose">{content}</div></section>'
    page(path, title, desc, body)


def build_legal():
    legal_page("/privacy-policy/", "Privacy Policy | Los Arcos Apartments & Townhomes",
        "How Los Arcos Apartments & Townhomes collects, uses and protects information submitted through this website.",
        "Privacy <em>Policy</em>", "Privacy Policy", f'''
<!-- [confirm] have management / counsel review before launch -->
<p><em>Last updated: November 2026</em></p>
<p>This Privacy Policy explains how {P["name"]} ("we," "us") handles information collected through this website.</p>
<h2>Information we collect</h2>
<ul><li>Information you provide in forms, such as your name, email, phone number, preferred tour date and message.</li><li>Basic technical data such as browser type and pages visited, collected through standard server logs.</li></ul>
<h2>How we use information</h2>
<ul><li>To respond to inquiries and schedule tours.</li><li>To share information about availability and leasing.</li><li>To operate, maintain and improve this website.</li></ul>
<h2>Sharing</h2><p>We do not sell your personal information. We may share it with service providers who help us operate our leasing systems, under appropriate confidentiality obligations, or when required by law.</p>
<h2>Your choices</h2><p>You may ask us to update or delete information you have provided by calling <a href="tel:{P["tel"]}">{P["phone"]}</a> or visiting the leasing office.</p>
<h2>Contact</h2><p>{P["name"]}, {P["street"]}, {P["city"]}, {P["state"]} {P["zip"]}.</p>''')
    legal_page("/terms/", "Terms of Use | Los Arcos Apartments & Townhomes",
        "Terms governing use of the Los Arcos Apartments & Townhomes website.",
        "Terms of <em>Use</em>", "Terms", f'''
<!-- [confirm] have management / counsel review before launch -->
<p><em>Last updated: November 2026</em></p>
<p>By using this website you agree to these terms.</p>
<h2>Information on this site</h2><p>Floor plans, pricing, photos, amenities and availability are provided for general information, are subject to change without notice and do not constitute an offer or guarantee. Images may be representative. Please confirm all details with the leasing office.</p>
<h2>Use of the site</h2><p>You agree not to misuse the site, interfere with its operation or attempt to access it by unauthorized means.</p>
<h2>Third-party links</h2><p>Links to third-party sites, such as maps or payment portals, are provided for convenience. We are not responsible for their content or practices.</p>
<h2>Limitation of liability</h2><p>The site is provided "as is" without warranties of any kind, to the fullest extent permitted by law.</p>
<h2>Contact</h2><p>Questions about these terms? Call <a href="tel:{P["tel"]}">{P["phone"]}</a>.</p>''')
    legal_page("/accessibility/", "Accessibility Statement | Los Arcos Apartments & Townhomes",
        "Los Arcos is committed to an accessible website and community for everyone, including people with disabilities.",
        "Accessibility <em>Statement</em>", "Accessibility", f'''
<p>{P["name"]} is committed to providing a website and a community that are accessible to everyone, including people with disabilities.</p>
<h2>Our website</h2><p>We aim to conform to the Web Content Accessibility Guidelines (WCAG) 2.2 Level AA. This site uses semantic HTML, keyboard-friendly navigation, visible focus states, text alternatives for images, sufficient color contrast and respects reduced-motion preferences.</p>
<h2>Our community</h2><p>Los Arcos offers a wheelchair-accessible entrance and accessible parking. Residents may request reasonable accommodations or modifications by contacting the leasing office.</p>
<h2>Feedback</h2><p>If you have trouble accessing any part of this website, please call <a href="tel:{P["tel"]}">{P["phone"]}</a> or visit us at {P["street"]}, {P["city"]}, {P["state"]} {P["zip"]}. We will work with you to provide the information you need.</p>''')


def build_sitemap():
    descs = {p: d for p, _, d in PAGES}
    order = ["/", "/amenities/", "/floor-plans/", "/gallery/", "/virtual-tours/", "/neighborhood/", "/residents/", "/faqs/", "/contact/", "/apply/", "/privacy-policy/", "/terms/", "/accessibility/"]
    names = {"/": "Home", "/amenities/": "Amenities", "/floor-plans/": "Floor Plans", "/gallery/": "Gallery", "/virtual-tours/": "Virtual Tours",
             "/neighborhood/": "Neighborhood", "/residents/": "Residents", "/faqs/": "FAQs", "/contact/": "Contact &amp; Schedule a Tour",
             "/apply/": "Apply Now", "/privacy-policy/": "Privacy Policy", "/terms/": "Terms of Use", "/accessibility/": "Accessibility Statement"}
    items = "".join(f'<li><a href="{p}">{names[p]}</a><small>{html.escape(descs[p])}</small></li>' for p in order)
    body = page_hero("Los Arcos", "Site <em>Map</em>", "Every page on the Los Arcos website in one place.", None, "Site Map") + f'<section class="section"><div class="wrap"><ul class="sitemap-list">{items}</ul></div></section>'
    page("/site-map/", "Site Map | Los Arcos Apartments & Townhomes", "A complete list of pages on the Los Arcos Apartments & Townhomes website.", body)


def build_404():
    body = page_hero("Page not found", "This arch leads <em>nowhere</em>", "The page you're looking for has moved or doesn't exist. Let's get you back home.", None, None,
                     extra='<div class="btn-row" style="margin-top:24px"><a class="btn" href="/">Back to home</a><a class="btn btn--ghost" href="/floor-plans/">View floor plans</a></div>')
    page("/404.html", "Page Not Found | Los Arcos Apartments", "The page you requested could not be found.", body, active="")


def main():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)
    for d in ("css", "js", "img", "fonts"):
        shutil.copytree(os.path.join(SRC, d), os.path.join(DIST, d))
    for f in ("favicon.svg", "logo.svg", "robots.txt", ".htaccess"):
        shutil.copy(os.path.join(SRC, f), os.path.join(DIST, f))
    build_home(); build_amenities(); build_floorplans(); build_gallery(); build_tours(); build_neighborhood()
    build_residents(); build_faqs(); build_contact(); build_apply(); build_legal(); build_sitemap(); build_404()
    print(f"Built {len(PAGES)} pages -> {DIST}")

if __name__ == "__main__":
    main()
