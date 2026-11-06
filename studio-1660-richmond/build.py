#!/usr/bin/env python3
"""Static site generator for the Studio at 1660 Richmond concept site.

    python3 build.py          -> writes the finished site to ./dist

Everything (pages, shared header/footer, schema, SEO tags) lives here so the
site stays plain HTML/CSS/JS with no runtime. Edit P / FAQS below, re-run,
and upload ./dist. Reuses the build approach of the Los Arcos demo.

Anything not confirmed by the property is marked with an HTML comment
containing [confirm]. Search the source for it before launch.
"""
import json, os, re, shutil, html, hashlib
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
DIST = os.path.join(ROOT, "dist")

# ---------------------------------------------------------------------------
# Property facts
# Sources: Rise Apartments listing (submitted by the property) and the
# manager's pages at fatproperty.com (building page, Unit 01 listing, contact).
# ---------------------------------------------------------------------------
P = {
    "name": "Studio at 1660 Richmond",
    "short": "1660 Richmond",
    "street": "1660 Richmond Ave",
    "city": "Houston", "state": "TX", "zip": "77006",
    "area": "Montrose",
    "lat": 29.73443, "lng": -95.40141,          # OpenStreetMap geocode of the address
    # Leasing line and email of the management company (Fat Property). [confirm] property wants this as its public number
    "phone": "(832) 640-4444", "tel": "+18326404444",
    "email": "leasing@fatproperty.com",
    "manager": "Fat Property",
    "office": "3800 Garrott St, Houston, TX 77006",
    "units": 16, "built": 1970, "stories": 2,
    "sqft": 475, "rent": 900,                    # Unit 01 listing; MLS syndications also show $875–$925 [confirm]
}
ADDR = f'{P["street"]}, {P["city"]}, {P["state"]} {P["zip"]}'
ADDR_Q = "1660+Richmond+Ave,+Houston,+TX+77006"
GMAPS = f"https://www.google.com/maps/search/?api=1&query={ADDR_Q}"
DIRECTIONS = f"https://www.google.com/maps/dir/?api=1&destination={ADDR_Q}"
MAP_EMBED = f"https://www.google.com/maps?q={ADDR_Q}&z=15&output=embed"

# Placeholder links: replace with live URLs at launch.
# Fat Property already runs applications and the resident portal on Buildium
# (fatproperty.managebuilding.com), so these can point there.
APPLY_URL = "#apply-online"
PAY_URL = "#pay-rent"
MAINT_URL = "#maintenance-request"
PORTAL_URL = "#resident-portal"

NAV = [
    ("/studios/", "The Studios"), ("/amenities/", "Amenities"), ("/gallery/", "Gallery"),
    ("/neighborhood/", "Neighborhood"), ("/residents/", "Residents"), ("/faqs/", "FAQs"),
    ("/contact/", "Contact"),
]

# ---------------------------------------------------------------------------
# Icons (24x24 line icons, stroke = currentColor)
# ---------------------------------------------------------------------------
_I = {
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "arrow-ur": '<path d="M7 17 17 7M8 7h9v9"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/>',
    "car": '<path d="M5 17H3v-5l2-5h14l2 5v5h-2"/><circle cx="7.5" cy="17" r="2"/><circle cx="16.5" cy="17" r="2"/><path d="M3 12h18"/>',
    "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10z"/><path d="M2 21c0-3 1.9-5.4 5.1-6"/>',
    "paw": '<circle cx="11" cy="4" r="2"/><circle cx="18" cy="8" r="2"/><circle cx="20" cy="16" r="2"/><path d="M9 10a5 5 0 0 1 5 5v3.5a3.5 3.5 0 0 1-6.8 1.2 3.4 3.4 0 0 0-2.4-2.4A3.5 3.5 0 0 1 6 10.4 5 5 0 0 1 9 10z"/>',
    "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "fan": '<path d="M10.8 10.4C9.7 7.8 10.4 3 13.6 3c2.6 0 3 3.7.6 6.4M13.6 13.6c2.6 1.1 7.4.4 7.4-2.8 0-2.6-3.7-3-6.4-.6M13.2 13.6c1.1 2.6.4 7.4-2.8 7.4-2.6 0-3-3.7-.6-6.4M10.4 10.8C7.8 9.7 3 10.4 3 13.6c0 2.6 3.7 3 6.4.6"/><circle cx="12" cy="12" r="1"/>',
    "kitchen": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M7 6h.01M11 6h.01M8 13h8v5H8z"/>',
    "snow": '<path d="M2 12h20M12 2v20M20 16l-4-4 4-4M4 8l4 4-4 4M16 4l-4 4-4-4M8 20l4-4 4 4"/>',
    "closet": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M12 2v20M9 11v2M15 11v2"/>',
    "balcony": '<path d="M3 21h18M5 21v-8M19 21v-8M3 13h18M9 21v-8M15 21v-8M8 13V5a4 4 0 0 1 8 0v8"/>',
    "grid": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
    "bed": '<path d="M2 4v16M2 8h18a2 2 0 0 1 2 2v10M2 17h20M6 8v9"/>',
    "bath": '<path d="M9 6 6.5 3.5a1.5 1.5 0 0 0-2.1 0L3.5 4.4A1.5 1.5 0 0 0 3 5.5V17a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-5H3M7 19v2M17 19v2"/>',
    "ruler": '<path d="M21.3 15.3a2.4 2.4 0 0 1 0 3.4l-2.6 2.6a2.4 2.4 0 0 1-3.4 0L2.7 8.7a2.4 2.4 0 0 1 0-3.4l2.6-2.6a2.4 2.4 0 0 1 3.4 0zM14.5 12.5l2-2M11.5 9.5l2-2M8.5 6.5l2-2M17.5 15.5l2-2"/>',
    "card": '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/>',
    "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.8-3.8a6 6 0 0 1-7.9 7.9l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a6 6 0 0 1 7.9-7.9z"/>',
    "home": '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "bag": '<path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4zM3 6h18M16 10a4 4 0 0 1-8 0"/>',
    "fork": '<path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2M7 2v20M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3zm0 0v7"/>',
    "palette": '<circle cx="13.5" cy="6.5" r="1"/><circle cx="17.5" cy="10.5" r="1"/><circle cx="8.5" cy="7.5" r="1"/><circle cx="6.5" cy="12.5" r="1"/><path d="M12 2a10 10 0 0 0 0 20 2 2 0 0 0 2-2c0-.5-.2-1-.5-1.4a2 2 0 0 1 1.5-3.3H17a5 5 0 0 0 5-5C22 5.8 17.5 2 12 2z"/>',
    "walk": '<circle cx="13" cy="4" r="2"/><path d="m7 22 3-7 3 2v5M10 15l1-6 4 3 3 1M8 10l3-1"/>',
    "school": '<path d="M22 10 12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "left": '<path d="m15 18-6-6 6-6"/>',
    "right": '<path d="m9 18 6-6-6-6"/>',
    "megaphone": '<path d="m3 11 18-5v12L3 14v-3zM11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
    "bolt": '<path d="M13 2 3 14h9l-1 8 10-12h-9z"/>',
    "key": '<circle cx="7.5" cy="15.5" r="5.5"/><path d="m21 2-9.6 9.6M15.5 7.5l3 3L22 7l-3-3"/>',
    "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4M8 6h.01M16 6h.01M12 6h.01M12 10h.01M12 14h.01M16 10h.01M16 14h.01M8 10h.01M8 14h.01"/>',
    "pulse": '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
    "map": '<path d="m3 6 6-3 6 3 6-3v15l-6 3-6-3-6 3z"/><path d="M9 3v15M15 6v15"/>',
    "box": '<path d="M21 8 12 3 3 8v8l9 5 9-5z"/><path d="M3 8l9 5 9-5M12 13v8"/>',
    "window": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 12h18M12 3v18"/>',
}
def icon(name, cls="", size=None):
    c = f' class="{cls}"' if cls else ""
    s = f' style="width:{size}px;height:{size}px"' if size else ""
    return f'<svg{c}{s} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_I[name]}</svg>'

SOCIAL = {
    "Instagram": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".6" fill="currentColor"/></svg>',
    "Facebook": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14 8.5V6.8c0-.8.2-1.3 1.4-1.3H17V2.3c-.3 0-1.3-.1-2.4-.1-2.4 0-4 1.4-4 4.1v2.2H8v3.6h2.6V22H14v-9.9h2.7l.4-3.6z"/></svg>',
}

# Breeze-block logo mark (mid-century Montrose courtyard screen)
LOGO_MARK = ('<svg viewBox="0 0 44 44" aria-hidden="true" focusable="false"><rect width="44" height="44" rx="11" fill="#1E5560"/>'
             '<g fill="none" stroke="#E7A93A" stroke-width="2.6"><circle cx="15" cy="15" r="7"/><circle cx="29" cy="15" r="7"/>'
             '<circle cx="15" cy="29" r="7"/><circle cx="29" cy="29" r="7"/></g><circle cx="22" cy="22" r="2.2" fill="#F4EFE6"/></svg>')
def logo(extra=""):
    return (f'<a class="logo" href="/"{extra}>{LOGO_MARK}<span class="logo__text"><span class="logo__sub">Studio at</span>'
            f'<span class="logo__name">1660 Richmond</span></span><span class="sr-only"> (home)</span></a>')

EHO = ('<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true">'
       '<path d="M4 22 24 6l20 16"/><path d="M9 19v24h30V19"/><path d="M16 27h16M16 34h16"/></svg>')
ADA = ('<svg viewBox="0 0 48 48" fill="currentColor" aria-hidden="true"><circle cx="22" cy="7" r="4"/>'
       '<path d="M19 14h6v10h10l5 13-4 1.5-4-9.5H19z"/><path d="M15 21.5v4.6a8.5 8.5 0 1 0 12.4 10.6l3.7 2.3A12.8 12.8 0 1 1 15 21.5z"/></svg>')

# ---------------------------------------------------------------------------
# Images  (images.json: key, source file, category, alt, credit)
# ---------------------------------------------------------------------------
IMAGES = {r[0]: {"cat": r[2], "alt": r[3], "credit": r[4]} for r in json.load(open(os.path.join(ROOT, "images.json")))}
_dims = {}
def dims(key, w):
    k = (key, w)
    if k not in _dims:
        with Image.open(os.path.join(SRC, "img", f"{key}-{w}.webp")) as im:
            _dims[k] = im.size
    return _dims[k]

def srcset(key):
    # the "-1600" file is capped at the source width, so use real widths in the descriptor
    return ", ".join(f"/img/{key}-{w}.webp {dims(key, w)[0]}w" for w in (500, 900, 1600))

def img(key, sizes="100vw", cls="", eager=False, alt=None, lazy_src=False):
    a = html.escape(alt if alt is not None else IMAGES[key]["alt"], quote=True)
    w, h = dims(key, 900)
    c = f' class="{cls}"' if cls else ""
    if lazy_src:  # hero slides 2/3: swapped in by JS so they never compete with the LCP image
        return (f'<img{c} src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" '
                f'data-src="/img/{key}-1600.webp" data-srcset="{srcset(key)}" sizes="{sizes}" width="{w}" height="{h}" alt="{a}" decoding="async">')
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img{c} src="/img/{key}-900.webp" srcset="{srcset(key)}" sizes="{sizes}" width="{w}" height="{h}" alt="{a}" {load} decoding="async">'

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------
def property_schema():
    return {
        "@type": ["ApartmentComplex", "LocalBusiness"],
        "@id": "/#property",
        "name": P["name"],
        "description": "A 16-home, two-story courtyard building of studio apartments in Houston's Montrose neighborhood, inside the Loop.",
        "url": "/",
        "telephone": P["phone"],
        "email": P["email"],
        "image": ["/img/court-deck-1600.webp", "/img/court-screen-1600.webp"],
        "logo": "/logo.svg",
        "priceRange": "$$",
        "address": {"@type": "PostalAddress", "streetAddress": P["street"], "addressLocality": P["city"],
                    "addressRegion": P["state"], "postalCode": P["zip"], "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": P["lat"], "longitude": P["lng"]},
        "hasMap": GMAPS,
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "17:30"}],
        "numberOfAccommodationUnits": P["units"],
        "petsAllowed": True,
        "tourBookingPage": "/contact/",
        "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": n, "value": True} for n in
                           ["Courtyard", "Parking included", "Pet friendly", "Ceiling fans", "Tile floors"]],
        "containedInPlace": {"@type": "Place", "name": "Montrose, Houston, TX"},
        "parentOrganization": {"@type": "Organization", "name": P["manager"], "url": "https://fatproperty.com/"},
    }

def schema(page_name, url_path, desc, extra=None):
    graph = [property_schema(),
             {"@type": "WebPage", "name": page_name, "description": desc, "url": url_path, "about": {"@id": "/#property"}}]
    if extra:
        graph.append(extra)
    data = {"@context": "https://schema.org", "@graph": graph}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "</script>"

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
def header(active):
    links = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a></li>' for h, t in NAV)
    return f'''<a class="skip" href="#main">Skip to main content</a>
<div class="announce" role="region" aria-label="Announcement">
  <div class="wrap">
    <p>{icon("megaphone").replace('<svg', '<svg style="width:16px;height:16px;vertical-align:-3px;margin-right:6px"', 1)}Studios now leasing in Montrose. Parking included, pets welcome. <a href="/contact/#tour">Book a tour</a></p>
    <!-- [confirm] current special / availability message with management -->
    <button class="announce__close" type="button" aria-label="Dismiss announcement">{icon("x")}</button>
  </div>
</div>
<div class="utility">
  <div class="wrap">
    <span class="utility__addr">{ADDR} · {P["area"]}</span>
    <a class="hide-sm" href="{DIRECTIONS}" target="_blank" rel="noopener">{icon("pin")}<span>Directions</span></a>
    <a href="/contact/#tour">{icon("calendar")}<span>Schedule a Tour</span></a>
    <a href="tel:{P["tel"]}">{icon("phone")}{P["phone"]}</a>
  </div>
</div>
<header class="header">
  <div class="wrap">
    {logo()}
    <nav class="nav" id="site-nav" aria-label="Main">
      <ul>{links}</ul>
      <div class="nav__extra">
        <a class="btn" href="/studios/#availability">Check Availability {icon("arrow")}</a>
        <a class="btn btn--teal" href="/apply/">Apply Now</a>
        <a class="btn btn--ghost" href="tel:{P["tel"]}">{icon("phone")} Call {P["phone"]}</a>
      </div>
    </nav>
    <a class="btn header__cta" href="/studios/#availability">Check Availability</a>
    <button class="menu-btn" type="button" aria-controls="site-nav" aria-expanded="false" aria-label="Open menu"><span></span></button>
  </div>
</header>'''

def hours_table(style=""):
    # Fat Property office hours (fatproperty.com/contact). The Rise listing says 9 AM–6 PM. [confirm]
    return f'''<table class="hours"{style}><caption class="sr-only">Leasing office hours</caption><tbody>
          <tr><td>Mon – Fri</td><td>9:00 AM – 5:30 PM</td></tr>
          <tr><td>Saturday</td><td>By appointment</td></tr>
          <tr><td>Sunday</td><td>Closed</td></tr>
        </tbody></table><!-- [confirm] weekend hours -->'''

def footer():
    social = "".join(f'<a href="#{n.lower()}" aria-label="{n} (link coming soon)" data-placeholder="Demo: this will link to the community\'s {n} page.">{s}</a>' for n, s in SOCIAL.items())
    navl = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in [("/", "Home")] + NAV[:4])
    navr = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV[4:] + [("/apply/", "Apply Now")])
    return f'''<footer class="footer">
  <div class="wrap">
    <p class="footer__big" aria-hidden="true">1660 Richmond</p>
    <div class="footer__grid">
      <div class="footer__brand">
        {logo()}
        <address><strong style="color:#fff;font-weight:600">{P["name"]}</strong><br>{P["street"]}<br>{P["city"]}, {P["state"]} {P["zip"]}<br><a href="tel:{P["tel"]}">{P["phone"]}</a> · <a href="mailto:{P["email"]}">{P["email"]}</a></address>
        <a class="link-arrow" href="{DIRECTIONS}" target="_blank" rel="noopener">Get Directions {icon("arrow-ur")}</a>
        <div class="social" style="display:flex;gap:10px;margin-top:18px">{social}</div>
      </div>
      <div><h2>Explore</h2><ul>{navl}</ul></div>
      <div><h2>Living Here</h2><ul>{navr}</ul></div>
      <div>
        <h2>Leasing Office</h2>
        {hours_table(' style="color:#B9C7C3"')}
        <p style="margin-top:18px"><a class="btn btn--sm" href="/contact/#tour">Schedule a Tour</a></p>
        <p style="font-size:.82rem;margin:0">Professionally managed by {P["manager"]}</p>
      </div>
    </div>
    <div class="footer__bottom">
      <div class="fair">
        <span role="img" aria-label="Equal Housing Opportunity">{EHO}</span>
        <span role="img" aria-label="Accessibility">{ADA}</span>
        <p>Equal Housing Opportunity. We are pledged to the letter and spirit of U.S. policy for the achievement of equal housing opportunity throughout the nation. We do not discriminate on the basis of race, color, religion, sex, disability, familial status or national origin.</p>
      </div>
      <nav class="legal" aria-label="Legal">
        <span>© <span data-year>2026</span> {P["name"]}</span>
        <a href="/privacy-policy/">Privacy Policy</a><a href="/terms/">Terms</a><a href="/accessibility/">Accessibility</a><a href="/site-map/">Site Map</a>
      </nav>
    </div>
    <p class="concept">Concept site prepared for {P["name"]}.</p>
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

PAGES = []
# Hostinger's CDN caches plain .html for a year and its purge does not reach every edge.
# index.php takes priority over index.html, so each page is served through a tiny PHP file
# that sends no-cache headers. Hostinger also routes unknown URLs to the nearest/root
# index.php (front-controller fallback; .htaccess is ignored), so each script answers 404
# unless the request path is exactly its own page.
PAGE_PHP = """<?php
header('Cache-Control: no-cache, must-revalidate, max-age=0');
header('X-Robots-Tag: noindex, nofollow'); // demo only: remove at launch
header('Content-Type: text/html; charset=utf-8');
$path = rtrim(preg_replace('#/index\\.(php|html)$#', '/', parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH)), '/') . '/';
if ($path !== '%s') {
    http_response_code(404);
    readfile('%s/404.html');
    exit;
}
readfile(__DIR__ . '/index.html');
"""

# Hostinger answers unknown URLs with the root index.html itself (no PHP involved), so the
# homepage sends any path other than "/" to the real 404 page before it renders.
SOFT404 = "<script>(function(p){if(p!=='/'&&p!=='/index.html'&&p!=='/index.php')location.replace('/404.html')})(location.pathname)</script>\n"

def page(path, title, desc, body, active=None, preload=None, extra_schema=None, og="court-deck"):
    pre = ""
    if preload:
        pre = (f'<link rel="preload" as="image" href="/img/{preload}-900.webp" '
               f'imagesrcset="{srcset(preload)}" imagesizes="100vw" fetchpriority="high">')
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc, quote=True)}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#1E5560">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{P["name"]}">
<meta property="og:title" content="{html.escape(title, quote=True)}">
<meta property="og:description" content="{html.escape(desc, quote=True)}">
<meta property="og:image" content="/img/{og}-1600.webp">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{SOFT404 if path == "/" else ""}<link rel="preload" href="/fonts/bricolage.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/instrument-sans.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/instrument-serif-italic.woff2" as="font" type="font/woff2" crossorigin>
{pre}
<link rel="stylesheet" href="/css/style.css?v={_ver("css/style.css")}">
{schema(title, path, desc, extra_schema)}
</head>
<body>
{header(active if active is not None else path)}
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
    if out.endswith("index.html"):
        with open(out[:-4] + "php", "w", encoding="utf-8") as f:
            depth = path.strip("/").count("/") + 1 if path.strip("/") else 0
            root_dir = "__DIR__" if depth == 0 else "dirname(__DIR__" + (", %d" % depth if depth > 1 else "") + ")"
            f.write((PAGE_PHP % (path, "%s")).replace("'%s/404.html'", root_dir + " . '/404.html'"))
    PAGES.append((path, title, desc))

def page_hero(eyebrow, h1, lead, img_key=None, crumbs=None, extra=""):
    cr = f'<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <span aria-current="page">{crumbs}</span></nav>' if crumbs else ""
    media = f'<div class="page-hero__img">{img(img_key, sizes="340px", eager=True)}</div>' if img_key else ""
    return f'''<section class="page-hero">
  <div class="wrap">
    <div>{cr}<span class="eyebrow">{eyebrow}</span><h1>{h1}</h1><p class="lead">{lead}</p>{extra}</div>
    {media}
  </div>
</section>'''

def cta_band(h="Your Montrose studio is <em>waiting.</em>",
             p="Tour Studio at 1660 Richmond in person, see the courtyard for yourself and find out which studio is open now."):
    return f'''<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="cta reveal">
      <span class="eyebrow">Come see it</span>
      <h2>{h}</h2>
      <p>{p}</p>
      <div class="btn-row">
        <a class="btn" href="/contact/#tour">{icon("calendar")} Schedule a Tour</a>
        <a class="btn btn--outline-light" href="/studios/#availability">Check Availability {icon("arrow")}</a>
      </div>
    </div>
  </div>
</section>'''

def marquee(items, cls="", label="Highlights"):
    g = "".join(f"<span>{t}</span><i></i>" for t in items)
    return (f'<div class="marquee {cls}" role="region" aria-label="{label}"><div class="marquee__track">'
            f'<div class="marquee__group">{g}</div><div class="marquee__group" aria-hidden="true">{g}</div></div></div>')

# ---------------------------------------------------------------------------
# Representative studio floor plan (illustrative, not to scale)
# ---------------------------------------------------------------------------
def plan_svg(small=False):
    wall = 'fill="none" stroke="#15211F" stroke-width="5" stroke-linejoin="round"'
    thin = 'fill="none" stroke="#15211F" stroke-width="2"'
    lbl = 'font-family="Instrument Sans,Arial,sans-serif" font-size="13" font-weight="700" fill="#15211F" text-anchor="middle"'
    sub = 'font-family="Instrument Sans,Arial,sans-serif" font-size="10.5" fill="#545D59" text-anchor="middle"'
    g = f'''<rect x="20" y="20" width="360" height="270" rx="4" fill="#FFFDF8"/>
<rect x="20" y="20" width="230" height="170" fill="#F6E3BC" opacity=".55"/>
<rect x="250" y="20" width="130" height="105" fill="#D5E4E3" opacity=".8"/>
<path d="M20 20h360v270H20z" {wall}/>
<path d="M250 20v105M250 150v40M250 125h130M250 190h130M20 190h112M178 190h72" {wall}/>
<path d="M60 20h70M150 20h70" stroke="#3B8DB0" stroke-width="7"/>
<path d="M380 55v40" stroke="#3B8DB0" stroke-width="7"/>
<rect x="28" y="198" width="34" height="84" {thin}/><circle cx="45" cy="218" r="7" {thin}/><circle cx="45" cy="240" r="7" {thin}/>
<rect x="62" y="198" width="60" height="22" {thin}/><rect x="62" y="260" width="60" height="22" {thin}/>
<rect x="262" y="30" width="34" height="80" rx="10" {thin}/><circle cx="355" cy="100" r="10" {thin}/>
<rect x="338" y="30" width="34" height="22" rx="4" {thin}/>
<path d="M265 135h105M265 145h105" stroke="#15211F" stroke-width="1.5" stroke-dasharray="4 4"/>
<path d="M178 290a46 46 0 0 1 46-46" {thin} stroke-dasharray="3 3"/><path d="M178 290v-46" stroke="#15211F" stroke-width="2"/>
<circle cx="135" cy="105" r="18" fill="none" stroke="#1E5560" stroke-width="1.5"/>
<path d="M135 87v36M117 105h36" stroke="#1E5560" stroke-width="1.2"/>'''
    if not small:
        g += f'''<text x="135" y="62" {lbl}>LIVING / SLEEPING</text><text x="135" y="78" {sub}>Ceiling fan · window wall</text>
<text x="315" y="78" {lbl} >BATH</text>
<text x="315" y="166" {lbl}>CLOSET</text>
<text x="94" y="245" {lbl}>KITCHEN</text>
<text x="315" y="236" {lbl}>STORAGE</text>
<text x="210" y="225" {lbl}>ENTRY</text>
<text x="200" y="312" {sub}>Courtyard / walkway</text>'''
    vb = "0 0 400 322" if not small else "0 0 400 300"
    label = "Representative studio layout: living and sleeping room, galley kitchen near the entry, bath, closet and storage. Illustrative, not to scale."
    return f'<svg viewBox="{vb}" role="img" aria-label="{label}"{" aria-hidden=\"true\"" if small else ""}>{g}</svg>'

# ---------------------------------------------------------------------------
# FAQs (also used for FAQPage schema). Answers are plain HTML.
# ---------------------------------------------------------------------------
FAQS = [
    ("Leasing", [
        ("What types of apartments are available?",
         f"{P['name']} is a studio building. The current studio has one bath and about {P['sqft']} square feet. Finishes vary by unit, from simple, affordable studios to more heavily upgraded ones. Ask the leasing team which studios are open right now."),
        ("How much is rent?",
         f"Studios currently start at ${P['rent']:,} per month.<!-- [confirm] current rent; MLS syndications show $875–$925 --> Pricing and availability change, so contact leasing for today's rates."),
        ("What lease terms do you offer?",
         "Leases are typically 12 months. Shorter terms are sometimes available for an additional fee."),
        ("Is a security deposit required?",
         "Deposit terms are set per unit and confirmed when you apply. Contact leasing for the current amount.<!-- [confirm] the Rise listing FAQ says no apartment deposit; Fat Property's Unit 01 listing shows a $900 security deposit -->"),
        ("How do I apply?",
         "Applications are completed online through our property management software. Ask leasing for the rental criteria before you apply. Application and admin fees are shared by the leasing team.<!-- [confirm] application/admin fee amounts -->"),
        ("Are the apartments furnished?",
         "No. Studios are rented unfurnished, so you can bring your own style."),
    ]),
    ("Pets & Parking", [
        ("Are pets allowed?",
         "Yes. Dogs and cats are welcome and approved case by case, up to two pets per home. Breed restrictions apply, and a pet fee and monthly pet rent may apply.<!-- [confirm] pet fee, pet rent, pet deposit, weight limits -->"),
        ("Is parking included?",
         "Yes, parking is included with your lease.<!-- [confirm] assigned vs. open, carport, guest parking -->"),
    ]),
    ("The Building", [
        ("How many apartments are in the building?",
         f"{P['name']} has {P['units']} apartments in a two-story, courtyard-style building originally built in {P['built']}."),
        ("What features do the studios have?",
         "Studios include a refrigerator, stove and oven, garbage disposal, ceiling fan, air conditioning and heat, tile floors, window coverings, a pantry and storage space. Finishes vary by unit."),
        ("Which utilities do residents pay?",
         "Residents set up their own electricity service. Ask leasing about any other utilities.<!-- [confirm] full utility breakdown (water, trash, internet) -->"),
        ("Who manages the property?",
         f"{P['name']} is professionally managed by {P['manager']}, whose leasing office is a couple of minutes away at {P['office']}."),
        ("What are the leasing office hours?",
         "The leasing office is open Monday through Friday, 9:00 AM to 5:30 PM. Tours outside those hours may be available by appointment.<!-- [confirm] hours; the Rise listing shows 9 AM–6 PM -->"),
    ]),
    ("Neighborhood", [
        ("What restaurants are nearby?",
         "Favorites within about a mile include 93' Til, Hugo's, The Marigold Club, Southern Yankee Crafthouse and BCN Taste &amp; Tradition."),
        ("Where can I shop nearby?",
         "H-E-B on West Alabama and Alabama Row are about a third of a mile away. Alabama Shepherd Shopping Center, Montrose Collective and The Centre at River Oaks are close by, and The Galleria is about a 10-minute drive."),
        ("Which schools serve the area?",
         "The property is in the Houston Independent School District. Schools listed for the property include MacGregor Elementary, Lanier Middle School and Carnegie Vanguard High School. Please confirm current zoning with HISD.<!-- [confirm] zoning: Zillow lists Poe Elementary, Lanier Middle and Lamar High; Carnegie Vanguard is a magnet school -->"),
        ("How far is it to the Texas Medical Center, Downtown and the Galleria?",
         "By car it's about 2.4 miles to the Texas Medical Center, 3.6 miles to Downtown and 4.8 miles to the Galleria, typically under 10 minutes each in light traffic."),
    ]),
]

def faq_schema():
    def clean(s):
        s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
        return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": clean(a)}}
        for _, items in FAQS for q, a in items]}

# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def build_home():
    N = P["name"]
    slides = [
        ("court-deck", f"{N} · Montrose, Houston", "Studio living, <em>Montrose style.</em>",
         f"{N} is a boutique courtyard building of just {P['units']} studio homes, a few blocks from the Menil Collection.",
         ("/studios/#availability", "Check Availability"), ("/contact/#tour", "Schedule a Tour")),
        ("court-screen", "Mid-century courtyard", "A courtyard to <em>come home to.</em>",
         f"Every front door at {N} opens onto palms, a vintage breeze-block wall and a quiet garden courtyard.",
         ("/gallery/", "Tour the Photos"), ("/amenities/", "See Amenities")),
        ("court-lawn", "Inside the Loop", "Inner-loop living, <em>from $900.</em>",
         f"Parking is included and pets are welcome. {N} keeps Downtown, the Medical Center and the Galleria within easy reach.",
         ("/studios/", "View the Studios"), ("/apply/", "Apply Now")),
    ]
    sl, msgs, dots = [], [], []
    for n, (k, eb, h, p, b1, b2) in enumerate(slides):
        sl.append(f'<div class="hero__slide{" is-active" if n == 0 else ""}">{img(k, eager=(n == 0), lazy_src=(n > 0), alt="")}</div>')
        conf = "<!-- [confirm] starting rent -->" if n == 2 else ""
        msgs.append(f'''<div class="hero__msg{" is-active" if n == 0 else ""}" aria-hidden="{"false" if n == 0 else "true"}">
          <span class="eyebrow">{eb}</span>
          <p class="hero__title" style="font-family:var(--display);font-weight:800;letter-spacing:-.045em">{h}</p>{conf}
          <p>{p}</p>
          <div class="btn-row"><a class="btn" href="{b1[0]}">{b1[1]} {icon("arrow")}</a><a class="btn btn--outline-light" href="{b2[0]}">{b2[1]}</a></div>
        </div>''')
        dots.append(f'<button class="hero__dot{" is-active" if n == 0 else ""}" type="button" aria-label="Show slide {n + 1}: {eb}"><span></span></button>')

    tiles = [
        ("studio-living", "01", "The Studios", f"About {P['sqft']} sq ft · from ${P['rent']}", "/studios/"),
        ("walkway", "02", "The Courtyard", "Palms, decks &amp; garden green", "/amenities/"),
        ("museum", "03", "The Neighborhood", "Museums, dining &amp; Montrose", "/neighborhood/"),
    ]
    tile_html = "".join(f'''<a class="tile reveal" data-delay="{i}" href="{href}">
      <div class="tile__img">{img(k, sizes="(max-width:900px) 100vw, 400px", alt="")}<span class="tile__num">{num}</span></div>
      <div class="tile__body"><div><h2>{t}</h2><p>{s}</p></div><span class="tile__go">{icon("arrow-ur")}</span></div>
    </a>''' for i, (k, num, t, s, href) in enumerate(tiles))

    strip_keys = [("court-screen", "Courtyard"), ("studio-bar", "Studio"), ("walkway", "Boardwalk"), ("kitchen-upgraded", "Upgraded kitchen"),
                  ("court-lawn", "Garden"), ("studio-closet", "Closet space"), ("court-deck", "Deck"), ("kitchen-galley", "Galley kitchen")]
    strip = "".join(f'<a href="/gallery/">{img(k, sizes="330px")}<span>{lbl}</span></a>' for k, lbl in strip_keys)

    why = [
        ("dog-walk", "walk", "Walk it", "0.3<small style='font-size:.5em'> mi</small>", "to H-E-B on West Alabama",
         f"Coffee, groceries and dinner are a short stroll from {N}. Listing data rates the address \"very walkable.\"<!-- [confirm] Walk Score 89 per listing aggregators -->"),
        ("bartender", "fork", "Eat &amp; drink", "0.2<small style='font-size:.5em'> mi</small>", "to 93' Til",
         "Hugo's, The Marigold Club, Southern Yankee Crafthouse and BCN Taste &amp; Tradition are all within about a mile."),
        ("museum", "palette", "Art next door", "0.3<small style='font-size:.5em'> mi</small>", "to the Menil Collection",
         "The Menil campus, the Cy Twombly Gallery and the Rothko Chapel sit just north of Richmond. The Menil's galleries are free to visit."),
        ("skyline", "map", "Inside the Loop", "8<small style='font-size:.5em'> min</small>", "to Downtown by car",
         "Roughly 6 minutes to the Texas Medical Center and 8 minutes to the Galleria in light traffic, so commutes stay short."),
    ]
    why_html = "".join(f'''<article class="card reveal" data-delay="{i % 4}">
      <div class="why__img">{img(k, sizes="(max-width:600px) 100vw, (max-width:1000px) 50vw, 300px", alt="")}</div>
      <span class="eyebrow" style="margin-bottom:.6rem">{t}</span>
      <div class="big">{big}</div><p style="font-weight:700;margin-bottom:.6em">{cap}</p>
      <p class="note" style="font-size:.93rem">{body}</p>
    </article>''' for i, (k, ic, t, big, cap, body) in enumerate(why))

    mq1 = ["Courtyard living", "Parking included", "Pet-friendly", "Inside the Loop", "<em>Montrose,</em> Houston", "16 homes", "Since 1970"]
    mq2 = ["0.3 mi to the Menil", "Studios from $900", "93' Til around the corner", "Walk to H-E-B", "<em>Studio at</em> 1660 Richmond"]

    badge = (f'<a class="badge-spin" href="/studios/#availability" >'
             '<svg class="ring" viewBox="0 0 150 150" aria-hidden="true"><defs><path id="ringpath" d="M75 75m-58 0a58 58 0 1 1 116 0a58 58 0 1 1-116 0"/></defs>'
             '<text><textPath href="#ringpath">Now leasing · Montrose · Inside the Loop · </textPath></text></svg>'
             f'<span><small>Studios from</small>${P["rent"]}<span class="sr-only">: now leasing, check availability</span></span></a><!-- [confirm] starting rent -->')

    body = f'''<section class="hero" aria-roledescription="carousel" aria-label="Welcome to {N}">
  <div class="hero__slides">{"".join(sl)}</div>
  <span class="hero__num" aria-hidden="true">1660</span>
  {badge}
  <div class="hero__inner">
    <div class="wrap">
      <div aria-live="polite">{"".join(msgs)}</div>
      <div class="hero__controls">
        <div class="hero__dots">{"".join(dots)}</div>
        <button class="hero__pause" type="button" aria-label="Pause slideshow"></button>
        <span class="hero__count" aria-hidden="true">01 / 03</span>
      </div>
    </div>
  </div>
  <a class="scroll-cue" href="#intro" aria-label="Scroll to introduction"><span></span></a>
</section>

<div class="wrap"><div class="tiles">{tile_html}</div></div>

<section class="section" id="intro">
  <div class="wrap split">
    <div class="split__media reveal">
      <div class="frame frame--tall">{img("court-screen", sizes="(max-width:860px) 90vw, 560px", alt="Courtyard at Studio at 1660 Richmond with palms, open-air stairs and a breeze-block wall")}</div>
      <div class="frame frame--small">{img("kitchen-upgraded", sizes="240px", alt="Upgraded studio kitchen with stainless appliances")}</div>
      <div class="note-card"><strong data-count="{P["units"]}">{P["units"]}</strong><span>studio homes around one<br>garden courtyard</span></div>
    </div>
    <div class="reveal" data-delay="1">
      <span class="eyebrow">Welcome to {N}</span>
      <h1>Studio Apartments in <em>Montrose, Houston</em></h1>
      <p class="lead">{N} is a boutique, two-story courtyard building on Richmond Avenue, right in the middle of Montrose and inside the Loop.</p>
      <p>Built in {P["built"]} and lovingly kept, {N} has the mid-century bones people hunt for: a palm-filled courtyard, open-air stairs, blue front doors and a brick breeze-block screen. Inside, each studio has about {P["sqft"]} square feet with a full kitchen, a ceiling fan, tile floors and a full bath. Finishes range from simple and affordable to fully upgraded.</p>
      <p>Life at {N} is small-scale and walkable. With only {P["units"]} homes, you'll recognize your neighbors. And with parking included and pets welcome, it's an easy place to settle in.<!-- [confirm] pet policy details --></p>
      <div class="stats">
        <div><strong data-count="{P["units"]}">{P["units"]}</strong><span>homes in the building</span></div>
        <div><strong data-count="{P["sqft"]}">{P["sqft"]}</strong><span>sq ft studios<!-- [confirm] sizes vary by unit --></span></div>
        <div><strong data-count="{P["built"]}" data-nogroup>{P["built"]}</strong><span>mid-century original</span></div>
        <div><strong>0.3<small style="font-size:.5em"> mi</small></strong><span>to the Menil Collection</span></div>
      </div>
      <div class="btn-row"><a class="btn" href="/studios/">Explore the Studios {icon("arrow")}</a><a class="btn btn--ghost" href="/contact/#tour">Schedule a Tour</a></div>
    </div>
  </div>
</section>

<section aria-label="Photo highlights" style="padding-bottom:clamp(40px,6vw,80px)">
  <div class="wrap section-head reveal" style="margin-bottom:28px">
    <div><span class="eyebrow">A look around {N}</span><h2>Palms, porches &amp; <em>light-filled studios</em></h2></div>
    <a class="link-arrow" href="/gallery/">Open the full gallery {icon("arrow")}</a>
  </div>
  <div class="strip">{strip}</div>
</section>

<div class="marquees">{marquee(mq1, label="Building highlights")}{marquee(mq2, "marquee--ochre", "Location highlights")}</div>

<section class="section section--alt" id="why" style="padding-top:clamp(48px,7vw,96px)">
  <div class="wrap">
    <div class="section-head reveal">
      <div><span class="eyebrow">Why live here</span><h2>The best of Montrose, <em>right outside your door</em></h2>
      <p class="lead" style="margin-top:14px">Montrose is Houston's most creative neighborhood, known for galleries, bungalow-lined streets, standout restaurants and late-night patios. {N} puts all of it within walking distance.</p></div>
      <a class="btn btn--ghost" href="/neighborhood/">Explore the neighborhood</a>
    </div>
    <div class="why">{why_html}</div>
    <p class="note" style="margin-top:20px">Distances are straight-line from {P["street"]} (OpenStreetMap). Drive times are typical light-traffic estimates; rush hour takes longer.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <div><span class="eyebrow">The studios</span><h2>Simple, smart <em>studio living</em></h2>
      <p class="lead" style="margin-top:14px">Every home at {N} is a studio: one open room for living and sleeping, a separate kitchen, a full bath and real closet space.</p></div>
    </div>
    <div class="mini-plan reveal">
      {plan_svg(small=True)}
      <div><h3>The Studio</h3><p>Studio · 1 bath · about {P["sqft"]} sq ft · <span class="avail">Available now</span><!-- [confirm] availability --></p></div>
      <div class="btn-row"><span style="font-family:var(--display);font-weight:800;font-size:1.8rem;letter-spacing:-.04em">${P["rent"]}<span class="note" style="font-family:var(--sans);font-weight:600;letter-spacing:0">/mo+</span></span><!-- [confirm] starting rent --><a class="btn btn--teal" href="/studios/">See details</a></div>
    </div>
  </div>
</section>

{cta_band(h="Make Montrose <em>home.</em>", p=f"Book a tour of {N} and see the courtyard, the studios and the neighborhood in person. The leasing team will show you what's open now.")}'''
    page("/", "Studio at 1660 Richmond | Studio Apartments in Montrose, Houston TX",
         "Studio at 1660 Richmond: a 16-home mid-century courtyard building of studio apartments in Montrose, Houston. Parking included, pets welcome, from $900/mo.",
         body, active="/", preload="court-deck")


def build_studios():
    N = P["name"]
    feats = [
        ("fan", "Ceiling fan"), ("grid", "Tile floors throughout"), ("kitchen", "Full kitchen with range and oven"),
        ("box", "Refrigerator &amp; disposal"), ("closet", "Closet, pantry &amp; storage"), ("snow", "A/C and heat"),
        ("window", "Window coverings"), ("sun", "Natural light"), ("bath", "Full bath with tub"),
        ("leaf", "Courtyard views (select units)"),
    ]
    checks = "".join(f'<li>{icon("check")}{t}</li>' for _, t in feats[:8])
    feat_cards = "".join(f'<li>{icon(ic)}<div><strong>{t}</strong></div></li>' for ic, t in feats)
    know = [
        ("car", "Parking included", "Parking comes with your lease.<!-- [confirm] assigned / carport -->"),
        ("paw", "Pets welcome", "Dogs and cats, case by case. Up to two pets; breed restrictions, pet fee and pet rent may apply.<!-- [confirm] -->"),
        ("file", "12-month leases", "Typical lease is 12 months. Shorter terms sometimes available for an extra fee."),
        ("bolt", "Utilities", "Residents set up their own electricity.<!-- [confirm] other utilities -->"),
    ]
    know_html = "".join(f'<article class="card reveal" data-delay="{i}"><div class="icon-chip">{icon(ic)}</div><h3>{t}</h3><p class="note" style="font-size:.95rem">{d}</p></article>' for i, (ic, t, d) in enumerate(know))
    shots = ["studio-living", "studio-bar", "kitchen-galley", "studio-window", "bath", "studio-closet", "kitchen-counter"]
    strip = "".join(f'<a href="/gallery/" aria-label="Open gallery: {html.escape(IMAGES[k]["alt"])}">{img(k, sizes="330px", alt="")}</a>' for k in shots)
    body = page_hero("The Studios", "Montrose studios, <em>thoughtfully simple</em>",
                     f"Every home at {N} is a studio with one bath and about {P['sqft']} square feet. Finishes range from affordable to heavily upgraded.",
                     "studio-living", "The Studios") + f'''
<section class="section" id="availability">
  <div class="wrap">
    <article class="plan-feature reveal">
      <div class="plan__drawing"><span class="plan__tag">Representative layout</span>{plan_svg()}</div>
      <div class="plan__body">
        <span class="avail" style="align-self:flex-start;margin-bottom:16px">Available now</span><!-- [confirm] availability -->
        <h2>The <em>Studio</em></h2>
        <ul class="plan__specs" aria-label="Studio specs">
          <li>{icon("bed")}Studio</li><li>{icon("bath")}1 Bath</li><li>{icon("ruler")}{P["sqft"]} sq ft</li>
        </ul>
        <!-- [confirm] unit sizes: listings show roughly 400–475 sq ft; ask about one-bedroom units mentioned in Fat Property's description -->
        <p class="plan__price"><span>Starting at</span><strong>${P["rent"]:,}</strong><span>per month*</span></p>
        <!-- [confirm] starting rent -->
        <ul class="checks">{checks}</ul>
        <div class="btn-row" style="margin-top:auto">
          <a class="btn" href="/contact/?plan=studio#tour">Check Availability {icon("arrow")}</a>
          <a class="btn btn--ghost" href="/apply/">Apply Now</a>
        </div>
        <p class="note" style="margin-top:18px">*Pricing and availability change without notice. Square footage is approximate and varies by unit. The floor plan is a representative illustration, not to scale.</p>
      </div>
    </article>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap amenity-group">
    <div class="sticky-media reveal">
      <span class="eyebrow">Unit features</span>
      <h2>Everything a studio <em>should have</em></h2>
      <p class="lead">The studios at {N} make the most of their space with a separate kitchen, a full bath and closet storage.</p>
      <div class="frame" style="aspect-ratio:4/3;margin-top:28px">{img("studio-bar", sizes="(max-width:900px) 92vw, 480px")}</div>
    </div>
    <ul class="amenity-list">{feat_cards}</ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><div><span class="eyebrow">Good to know</span><h2>The details, <em>up front</em></h2></div></div>
    <div class="grid-4">{know_html}</div>
  </div>
</section>

<section aria-label="Studio photos" style="padding-bottom:clamp(48px,7vw,96px)">
  <div class="wrap section-head reveal" style="margin-bottom:28px">
    <div><span class="eyebrow">Inside the studios</span><h2>Take a <em>closer look</em></h2></div>
    <a class="link-arrow" href="/gallery/">View all photos {icon("arrow")}</a>
  </div>
  <div class="strip">{strip}</div>
</section>
{cta_band()}'''
    page("/studios/", "Studio Apartments for Rent in Montrose | The Studios | Studio at 1660 Richmond",
         "Montrose studio apartments with one bath and about 475 sq ft, starting at $900/mo. Full kitchen, ceiling fan, tile floors, parking included. Check availability.",
         body, og="studio-living")


def build_amenities():
    N = P["name"]
    community = [
        ("leaf", "Landscaped courtyard", "Palms, a curved wood deck, a garden lawn and a boardwalk to your door"),
        ("car", "Parking included", "Resident parking comes with every lease<!-- [confirm] carport / assigned -->"),
        ("paw", "Pet-friendly", "Dogs and cats welcome, case by case<!-- [confirm] -->"),
        ("balcony", "Open-air walkways", "Shared second-floor balcony walkways overlooking the courtyard"),
        ("building", "Boutique scale", f"Only {P['units']} homes, so the courtyard stays calm and neighbors know each other"),
        ("users", "Local management", f"Managed by {P['manager']} from a Montrose office a couple of minutes away"),
        ("file", "Online applications", "Apply online through the property management portal"),
        ("pin", "Inner-loop address", "Montrose, between the Menil campus and Upper Kirby"),
    ]
    home = [
        ("fan", "Ceiling fans"), ("grid", "Tile floors"), ("kitchen", "Range &amp; oven"), ("box", "Refrigerator"),
        ("wrench", "Garbage disposal"), ("snow", "Air conditioning &amp; heat"), ("closet", "Closet &amp; storage space"),
        ("kitchen", "Pantry"), ("window", "Window coverings"), ("sun", "Natural light"),
    ]
    def li(items):
        return "".join(f'<li>{icon(ic)}<div><strong>{t}</strong>{f"<span>{d}</span>" if d else ""}</div></li>' for ic, t, *rest in items for d in [rest[0] if rest else ""])
    nearby = [("0.2 mi", "93' Til"), ("0.3 mi", "Menil Collection"), ("0.3 mi", "H-E-B, West Alabama"), ("0.3 mi", "Alabama Row"),
              ("0.4 mi", "Rothko Chapel"), ("0.6 mi", "Hugo's")]
    near_html = "".join(f'<div class="card reveal" data-delay="{i % 3}" style="padding:22px"><div class="big" style="font-family:var(--display);font-weight:800;font-size:2rem;letter-spacing:-.04em;color:var(--teal)">{d}</div><p style="margin:0;font-weight:700">{t}</p></div>' for i, (d, t) in enumerate(nearby))
    body = page_hero("Amenities", "Courtyard calm, <em>city at the curb</em>",
                     f"{N} trades big-complex extras for what matters day to day: a lush shared courtyard, included parking, a pet-friendly policy and one of Houston's most walkable addresses.",
                     "court-lawn", "Amenities") + f'''
<section class="section">
  <div class="wrap amenity-group">
    <div class="sticky-media reveal">
      <span class="eyebrow">Community</span>
      <h2>A courtyard <em>at the center</em></h2>
      <p class="lead">Two stories of studios wrap a green, palm-shaded courtyard. It's the kind of mid-century layout that makes coming home feel like an exhale.</p>
      <div class="frame" style="aspect-ratio:4/3;margin-top:28px">{img("court-deck", sizes="(max-width:900px) 92vw, 480px")}</div>
    </div>
    <ul class="amenity-list">{li(community)}</ul>
  </div>
</section>

<section class="section section--dark">
  <div class="wrap amenity-group">
    <div class="sticky-media reveal">
      <span class="eyebrow">In your studio</span>
      <h2>Small footprint, <em>full kitchen</em></h2>
      <p class="lead">Each studio comes with a full kitchen and bath, generous storage and a ceiling fan. Select studios feature upgraded finishes.</p>
      <div class="frame" style="aspect-ratio:4/3;margin-top:28px">{img("kitchen-upgraded", sizes="(max-width:900px) 92vw, 480px")}</div>
      <!-- [confirm] which units have the upgraded kitchen shown -->
    </div>
    <ul class="amenity-list">{li([(a, b, "") for a, b in home])}</ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><div><span class="eyebrow">Your neighborhood amenities</span><h2>Walk to the <em>good stuff</em></h2>
    <p class="lead" style="margin-top:14px">Some of the best amenities at {N} are just down the block.</p></div>
    <a class="btn btn--ghost" href="/neighborhood/">See the neighborhood</a></div>
    <div class="grid-3">{near_html}</div>
    <p class="note" style="margin-top:16px">Straight-line distances from {P["street"]} (OpenStreetMap).</p>
  </div>
</section>
{cta_band()}'''
    page("/amenities/", "Amenities | Courtyard, Parking Included & Pet-Friendly | Studio at 1660 Richmond",
         "Amenities at Studio at 1660 Richmond in Montrose: landscaped courtyard, parking included, pet-friendly policy, full kitchens and ceiling fans, steps from the Menil.",
         body, og="court-lawn")


def build_gallery():
    N = P["name"]
    order = ["court-deck", "studio-living", "court-screen", "kitchen-upgraded", "walkway", "studio-bar", "court-lawn", "kitchen-galley",
             "studio-window", "bath", "studio-room", "kitchen-counter", "studio-closet",
             "museum", "coffee", "bartender", "dog-walk", "mural", "cocktail-bar", "skyline"]
    catmap = {"community": "courtyard", "interiors": "interiors", "kitchens": "kitchens", "neighborhood": "neighborhood"}
    labels = {"courtyard": "Courtyard", "interiors": "Interiors", "kitchens": "Kitchens", "neighborhood": "Montrose life"}
    figs = []
    for k in order:
        cat = catmap[IMAGES[k]["cat"]]
        w, h = dims(k, 900)
        span = round((390 * h / w + 16) / 4)
        stock = cat == "neighborhood"
        cap = labels[cat] + (" · representative photo" if stock else "")
        figs.append(f'''<figure data-cat="{cat}" style="--span:{span}">
      <button type="button" data-full="/img/{k}-1600.webp" aria-label="Enlarge photo: {html.escape(IMAGES[k]["alt"], quote=True)}">{img(k, sizes="(max-width:700px) 92vw, (max-width:1100px) 46vw, 400px")}</button>
      <figcaption>{cap}</figcaption>
    </figure>''')
    filters = [("all", "All photos"), ("courtyard", "Courtyard"), ("interiors", "Interiors"), ("kitchens", "Kitchens"), ("neighborhood", "Montrose life")]
    fb = "".join(f'<button class="filter" type="button" data-filter="{v}" aria-pressed="{"true" if v == "all" else "false"}">{t}</button>' for v, t in filters)
    body = page_hero("Gallery", "Take a look <em>around</em>",
                     f"Photos of the courtyard, studios and kitchens at {N}, plus a taste of life in Montrose.", "walkway", "Gallery") + f'''
<section class="section">
  <div class="wrap">
    <div>
      <div class="filters filters--center" role="group" aria-label="Filter photos" data-filter-group="#gallery-grid">{fb}</div>
      <p class="sr-only" aria-live="polite" data-filter-status></p>
    </div>
    <div class="masonry" id="gallery-grid">{"".join(figs)}</div>
    <p class="note center" style="margin-top:18px">Property photos supplied by the owner. Neighborhood images are representative stock photography. Finishes vary by unit.</p>
  </div>
</section>
<div class="lightbox" role="dialog" aria-modal="true" aria-label="Photo viewer" aria-hidden="true">
  <button class="lb-btn lb-close" type="button" aria-label="Close photo viewer">{icon("x")}</button>
  <button class="lb-btn lb-prev" type="button" aria-label="Previous photo">{icon("left")}</button>
  <img src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" alt="" width="1600" height="900">
  <button class="lb-btn lb-next" type="button" aria-label="Next photo">{icon("right")}</button>
  <p class="lightbox__cap"></p>
</div>
{cta_band()}'''
    page("/gallery/", "Photo Gallery | Courtyard & Studio Interiors | Studio at 1660 Richmond",
         "Browse photos of Studio at 1660 Richmond in Montrose: the palm-filled courtyard, studio interiors, kitchens and the surrounding neighborhood.",
         body, og="walkway")


def map_block(title):
    return f'''<div class="map" data-map="{MAP_EMBED}" data-title="{title}">
      <div class="map__load">{icon("pin", size=36)}<p>{ADDR}</p><button class="btn btn--teal btn--sm" type="button">Load interactive map</button>
      <a class="link-arrow" href="{GMAPS}" target="_blank" rel="noopener">Open in Google Maps {icon("arrow-ur")}</a></div>
    </div>'''


def build_neighborhood():
    N = P["name"]
    cats = [
        ("fork", "Dining &amp; drinks", [("93' Til", "0.2 mi"), ("Southern Yankee Crafthouse", "0.5 mi"), ("Hugo's", "0.6 mi"),
                                        ("The Marigold Club", "0.6 mi"), ("BCN Taste &amp; Tradition", "0.7 mi")]),
        ("palette", "Arts &amp; culture", [("Menil Collection", "0.3 mi"), ("Cy Twombly Gallery", "0.3 mi"), ("Menil Park", "0.3 mi"),
                                           ("Rothko Chapel", "0.4 mi"), ("Museum of Fine Arts, Houston", "0.9 mi")]),
        ("bag", "Shopping &amp; errands", [("H-E-B, West Alabama", "0.3 mi"), ("Alabama Row", "0.3 mi"), ("Alabama Shepherd Shopping Center", "0.7 mi"),
                                           ("Montrose Collective", "1.0 mi"), ("The Centre at River Oaks", "1.3 mi"), ("The Galleria", "3.8 mi")]),
    ]
    cards = "".join(f'''<article class="card places-card reveal" data-delay="{i}"><h3>{icon(ic)}{t}</h3>
      <ul class="places">{"".join(f"<li><span>{n}</span><span>{d}</span></li>" for n, d in items)}</ul></article>''' for i, (ic, t, items) in enumerate(cats))
    schools = f'''<article class="card places-card reveal"><h3>{icon("school")}Schools (HISD)</h3>
      <ul class="places"><li><span>MacGregor Elementary School</span><span>HISD</span></li><li><span>Lanier Middle School</span><span>0.6 mi</span></li><li><span>Carnegie Vanguard High School</span><span>HISD</span></li></ul>
      <p class="note" style="margin:12px 0 0">Schools as listed for the property. Confirm current zoning with Houston ISD.</p>
      <!-- [confirm] zoning: Zillow shows Poe Elementary / Lanier Middle / Lamar High; Carnegie Vanguard is a magnet school -->
    </article>'''
    commute = [("2.4", "mi", "Texas Medical Center", "About 6 minutes by car"),
               ("3.6", "mi", "Downtown Houston", "About 8 minutes by car"),
               ("4.8", "mi", "The Galleria", "About 8 minutes by car")]
    com = "".join(f'<div class="reveal" data-delay="{i}"><strong><span data-count="{v}">{v}</span><small>{u}</small></strong><h3>{t}</h3><span>{s}</span></div>' for i, (v, u, t, s) in enumerate(commute))
    body = page_hero("Neighborhood", "Montrose, <em>inside the Loop</em>",
                     f"{N} sits on Richmond Avenue in the heart of Montrose, a few blocks from the Menil campus and minutes from Downtown, the Texas Medical Center and the Galleria.",
                     "skyline", "Neighborhood") + f'''
<section class="section">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Find us</span>
      <h2>{P["street"]}<br><em>{P["city"]}, {P["state"]} {P["zip"]}</em></h2>
      <p class="lead">Montrose is Houston's art-and-food neighborhood: tree-lined streets, mid-century apartments and converted bungalows, galleries and some of the city's most talked-about restaurants.</p>
      <p>From {N}, the Menil Collection's free galleries are about a five-minute walk, H-E-B and Alabama Row are around the corner, and Richmond Avenue connects you east toward Midtown and west toward Upper Kirby and Greenway Plaza.</p>
      <div class="btn-row"><a class="btn" href="{DIRECTIONS}" target="_blank" rel="noopener">Get Directions {icon("arrow-ur")}</a><a class="btn btn--ghost" href="/contact/#tour">Schedule a Tour</a></div>
    </div>
    <div class="reveal" data-delay="1">{map_block(f"Map of {N}, {ADDR}")}</div>
  </div>
</section>

<section class="section section--dark">
  <div class="wrap">
    <div class="section-head reveal"><div><span class="eyebrow">Commute times</span><h2>Minutes to <em>everywhere</em></h2>
    <p class="lead" style="margin-top:14px">Driving distance from {N}.</p></div></div>
    <div class="commute">{com}</div>
    <p class="note" style="margin-top:20px;color:#A9B8B4">Drive distances and light-traffic times from OpenStreetMap routing. Peak-hour traffic takes longer.<!-- [confirm] verify typical rush-hour times --></p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><div><span class="eyebrow">Nearby places</span><h2>What's <em>around the corner</em></h2></div></div>
    <div class="places-grid">{cards}{schools}</div>
    <p class="note" style="margin-top:18px">Straight-line distances from {P["street"]} (OpenStreetMap); walking routes may be longer. Businesses change, so check hours before you go.</p>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap split split--rev">
    <div class="split__media reveal">
      <div class="frame frame--tall">{img("museum", sizes="(max-width:860px) 90vw, 560px")}</div>
      <div class="frame frame--small">{img("coffee", sizes="240px")}</div>
    </div>
    <div class="reveal" data-delay="1">
      <span class="eyebrow">Why Montrose</span>
      <h2>Art, food &amp; <em>character</em></h2>
      <p>Montrose grew up as Houston's creative core, and it still feels that way. The Menil campus, with its museum, the Cy Twombly Gallery and the Rothko Chapel, sits just north of Richmond. Westheimer brings restaurants, bars and shops, and pocket parks dot the side streets.</p>
      <p>For renters, that means less time in the car and more time out. Residents of {N} can walk to groceries, coffee and dinner, then be on the freeway or downtown in minutes.</p>
      <a class="link-arrow" href="/contact/#tour">Come see the neighborhood {icon("arrow")}</a>
    </div>
  </div>
</section>
{cta_band()}'''
    page("/neighborhood/", "Montrose Neighborhood Guide | Nearby Dining, Museums & Commutes | Studio at 1660 Richmond",
         "Live in Montrose at Studio at 1660 Richmond: 0.3 mi to the Menil Collection and H-E-B, steps to 93' Til, and about 8 minutes to Downtown and the Galleria.",
         body, og="skyline")


def build_residents():
    N = P["name"]
    portals = [
        ("card", "Pay Rent", "Pay online by bank transfer or card and set up autopay.", PAY_URL),
        ("wrench", "Maintenance Request", "Submit and track service requests with photos, 24/7.", MAINT_URL),
        ("key", "Resident Portal", "View your lease, balance, documents and community notices.", PORTAL_URL),
    ]
    ptl = "".join(f'''<a class="portal reveal" data-delay="{i}" href="{u}" data-placeholder="Demo: this button will link to the {t.lower()} page of the live resident portal (paid add-on).">
      <div class="icon-chip">{icon(ic)}</div><span class="addon">Portal add-on</span><h2>{t}</h2><p>{d}</p><span class="link-arrow">Open {icon("arrow")}</span></a>''' for i, (ic, t, d, u) in enumerate(portals))
    tips = [
        ("bolt", "Set up electricity", "Residents put electric service in their own name before move-in.<!-- [confirm] -->"),
        ("shield", "Renter's insurance", "Ask leasing whether renter's insurance is required for your lease.<!-- [confirm] -->"),
        ("phone", "Emergencies", f"For urgent maintenance issues, call leasing at <a href=\"tel:{P['tel']}\">{P['phone']}</a>.<!-- [confirm] after-hours emergency line -->"),
    ]
    tip_html = "".join(f'<article class="card reveal" data-delay="{i}"><div class="icon-chip">{icon(ic)}</div><h3>{t}</h3><p class="note" style="font-size:.95rem">{d}</p></article>' for i, (ic, t, d) in enumerate(tips))
    body = page_hero("Residents", "Resident <em>services</em>",
                     f"Everything residents of {N} need, in one place: rent payments, maintenance requests and the resident portal.",
                     "walkway", "Residents") + f'''
<section class="section">
  <div class="wrap">
    <div class="portal-btns">{ptl}</div>
    <p class="note center" style="margin-top:20px">In the live site, these buttons connect to the property's resident portal.</p>
  </div>
</section>
<section class="section section--alt">
  <div class="wrap">
    <div class="section-head reveal"><div><span class="eyebrow">Helpful info</span><h2>Living at <em>{P["short"]}</em></h2></div></div>
    <div class="grid-3">{tip_html}</div>
  </div>
</section>
{cta_band(h="Questions? <em>We're nearby.</em>", p=f"{P['manager']}'s Montrose office is a couple of minutes from {N}. Call, email or stop by during office hours.")}'''
    page("/residents/", "Resident Services | Pay Rent & Maintenance Requests | Studio at 1660 Richmond",
         "Resident services for Studio at 1660 Richmond: pay rent online, submit maintenance requests and access the resident portal.",
         body, og="walkway")


def build_faqs():
    N = P["name"]
    navs, groups = [], []
    for g, items in FAQS:
        gid = re.sub(r"[^a-z]+", "-", g.lower()).strip("-")
        navs.append(f'<a href="#{gid}">{g.replace("&", "&amp;")}</a>')
        qa = "".join(f'<details class="faq"><summary>{q}</summary><div class="faq__a"><p>{a}</p></div></details>' for q, a in items)
        groups.append(f'<div class="faq-group" id="{gid}"><h2>{g.replace("&", "&amp;")}</h2>{qa}</div>')
    body = page_hero("FAQs", "Frequently asked <em>questions</em>",
                     f"Answers about leasing, pets, parking and the neighborhood at {N}. Don't see your question? Just ask.",
                     None, "FAQs") + f'''
<section class="section">
  <div class="wrap faq-cats">
    <nav class="faq-nav" aria-label="FAQ categories">{"".join(navs)}<a class="btn btn--sm" style="margin-top:14px" href="/contact/#question">Ask a question</a></nav>
    <div>{"".join(groups)}</div>
  </div>
</section>
{cta_band()}'''
    page("/faqs/", "FAQs | Rent, Pets, Parking & Leasing | Studio at 1660 Richmond",
         "Frequently asked questions about Studio at 1660 Richmond in Montrose: rent, lease terms, pets, parking, utilities, schools and nearby places.",
         body, extra_schema=faq_schema())


def build_contact():
    N = P["name"]
    slots = ["9:30 AM", "10:30 AM", "11:30 AM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "4:45 PM"]
    slot_html = "".join(f'<label><input type="radio" name="tour_time" value="{s}"{" required" if n == 0 else ""}><span>{s}</span></label>' for n, s in enumerate(slots))
    body = page_hero("Contact", "Schedule a tour <em>or say hello</em>",
                     f"Pick a day and time to see {N}, or send the leasing team a question. A real person reads every message.",
                     None, "Contact") + f'''
<section class="section">
  <div class="wrap split" style="align-items:start">
    <div class="form-card reveal" id="tour">
      <div class="tabs" role="tablist" aria-label="Contact options">
        <button type="button" role="tab" id="tab-tour" aria-controls="panel-tour" aria-selected="true">Schedule a Tour</button>
        <button type="button" role="tab" id="tab-question" aria-controls="panel-question" aria-selected="false" tabindex="-1">Ask a Question</button>
      </div>
      <div role="tabpanel" id="panel-tour" aria-labelledby="tab-tour">
        <form data-demo-form action="#" method="post">
          <div class="form-grid">
            <div class="field"><label for="t-first">First name</label><input id="t-first" name="first_name" autocomplete="given-name" required><p class="err">Please enter your first name.</p></div>
            <div class="field"><label for="t-last">Last name</label><input id="t-last" name="last_name" autocomplete="family-name"></div>
            <div class="field"><label for="t-email">Email</label><input id="t-email" name="email" type="email" autocomplete="email" required><p class="err">Please enter a valid email.</p></div>
            <div class="field"><label for="t-phone">Phone</label><input id="t-phone" name="phone" type="tel" autocomplete="tel"></div>
            <div class="field"><label for="tour-date">Preferred date</label><input id="tour-date" name="tour_date" type="date" required><p class="hint">Tours run Monday to Friday.</p><p class="err">Please pick an available weekday.</p></div>
            <div class="field"><label for="t-move">Ideal move-in</label><select id="t-move" name="move_in"><option value="">Select…</option><option>As soon as possible</option><option>Within 30 days</option><option>1–2 months</option><option>2+ months</option></select></div>
            <div class="field full"><fieldset><legend>Preferred time</legend><div class="slots">{slot_html}</div></fieldset><p class="err">Please choose a time.</p></div>
            <div class="field full"><fieldset><legend>Tour type</legend><div class="chips">
              <label><input type="radio" name="tour_type" value="In person" checked><span>In person</span></label>
              <label><input type="radio" name="tour_type" value="Live video"><span>Live video</span></label></div></fieldset></div>
            <input type="hidden" name="plan" value="studio">
            <div class="field full"><label for="t-msg">Anything we should know? (optional)</label><textarea id="t-msg" name="message" placeholder="Pets, parking needs, budget…"></textarea></div>
            <div class="full"><button class="btn" type="submit" style="width:100%">{icon("calendar")} Request My Tour</button>
            <p class="note" style="margin-top:10px">By submitting, you agree to be contacted about your inquiry. We never sell your information. See our <a href="/privacy-policy/">Privacy Policy</a>.</p></div>
          </div>
        </form>
        <div class="form-success" role="status">
          <div class="check">{icon("check")}</div>
          <h3>Tour requested<span data-name></span>!</h3>
          <p>We've got your request<span data-when></span>. The leasing team will confirm by email or phone shortly.</p>
          <a class="btn btn--ghost btn--sm" href="/studios/">View the studios</a>
        </div>
      </div>
      <div role="tabpanel" id="panel-question" aria-labelledby="tab-question" hidden>
        <form data-demo-form action="#" method="post">
          <div class="form-grid">
            <div class="field"><label for="q-name">Full name</label><input id="q-name" name="name" autocomplete="name" required><p class="err">Please enter your name.</p></div>
            <div class="field"><label for="q-email">Email</label><input id="q-email" name="email" type="email" autocomplete="email" required><p class="err">Please enter a valid email.</p></div>
            <div class="field"><label for="q-phone">Phone (optional)</label><input id="q-phone" name="phone" type="tel" autocomplete="tel"></div>
            <div class="field"><label for="q-topic">Topic</label><select id="q-topic" name="topic"><option>Availability &amp; pricing</option><option>Pets</option><option>Parking</option><option>Applying</option><option>Something else</option></select></div>
            <div class="field full"><label for="q-msg">Your question</label><textarea id="q-msg" name="message" required></textarea><p class="err">Please type your question.</p></div>
            <div class="full"><button class="btn btn--teal" type="submit" style="width:100%">{icon("mail")} Send Message</button></div>
          </div>
        </form>
        <div class="form-success" role="status">
          <div class="check">{icon("check")}</div>
          <h3>Thanks<span data-name></span>!</h3>
          <p>Your message is on its way to the leasing team. Expect a reply within one business day.</p>
        </div>
      </div>
    </div>
    <div class="reveal" data-delay="1">
      <span class="eyebrow">Leasing office</span>
      <h2>Let's <em>talk</em></h2>
      <ul class="info-list">
        <li>{icon("pin")}<div><strong>{P["street"]}</strong><br>{P["city"]}, {P["state"]} {P["zip"]}<br><a href="{DIRECTIONS}" target="_blank" rel="noopener">Get directions</a></div></li>
        <li>{icon("phone")}<div>Call or text<br><a href="tel:{P["tel"]}">{P["phone"]}</a></div></li>
        <li>{icon("mail")}<div>Email<br><a href="mailto:{P["email"]}">{P["email"]}</a></div></li>
        <li>{icon("building")}<div>Managed by {P["manager"]}<br><span class="note">Office: {P["office"]}</span></div></li>
      </ul>
      <h3 style="margin-top:28px">Office hours</h3>
      {hours_table()}
      <div style="margin-top:28px">{map_block(f"Map of {N}")}</div>
    </div>
  </div>
</section>'''
    page("/contact/", "Contact & Schedule a Tour | Studio at 1660 Richmond, Montrose Houston",
         "Schedule a tour of Studio at 1660 Richmond or ask the leasing team a question. 1660 Richmond Ave, Houston, TX 77006. Call (832) 640-4444.",
         body)


def build_apply():
    N = P["name"]
    need = [("file", "Photo ID", "A valid government-issued ID for each adult applicant"),
            ("card", "Proof of income", "Recent pay stubs, an offer letter or bank statements"),
            ("home", "Rental history", "Current and previous landlord contact details"),
            ("paw", "Pet details", "Breed, weight and vaccination records for any pets")]
    need_html = "".join(f'<li>{icon(ic)}<div><strong>{t}</strong><span>{d}</span></div></li>' for ic, t, d in need)
    body = page_hero("Apply Now", "Apply in <em>minutes</em>",
                     f"Ready to make {N} home? Start your application online. Questions first? The leasing team is happy to help.",
                     "court-screen", "Apply Now",
                     extra=f'<div class="btn-row" style="margin-top:24px"><a class="btn" href="{APPLY_URL}" data-placeholder="Demo: this button will open the online rental application.">Start Application {icon("arrow-ur")}</a><a class="btn btn--outline-light" href="/contact/#question">Ask a question</a></div>') + f'''
<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><div><span class="eyebrow">How it works</span><h2>Three steps to <em>your keys</em></h2></div></div>
    <ol class="steps">
      <li class="reveal"><h3>Pick your studio</h3><p>See what's <a href="/studios/">available now</a> and book a tour.</p></li>
      <li class="reveal" data-delay="1"><h3>Apply online</h3><p>Complete the application for each adult and upload your documents.</p></li>
      <li class="reveal" data-delay="2"><h3>Sign &amp; move in</h3><p>Once approved, sign your lease, set up electricity and get your keys.</p></li>
    </ol>
  </div>
</section>
<section class="section section--alt">
  <div class="wrap amenity-group">
    <div class="reveal"><span class="eyebrow">Before you start</span><h2>What you'll <em>need</em></h2>
      <p class="lead">Have these ready and the application takes just a few minutes.</p>
      <!-- [confirm] application fee, admin fee, income requirement and screening criteria (Fat Property publishes a criteria PDF) -->
      <p class="note">Application fees, deposits and qualification criteria apply. Ask leasing for the rental criteria. {N} is an Equal Housing Opportunity community.</p>
      <div class="btn-row" style="margin-top:20px"><a class="btn" href="{APPLY_URL}" data-placeholder="Demo: this button will open the online rental application.">Start Application {icon("arrow-ur")}</a></div>
    </div>
    <ul class="amenity-list">{need_html}</ul>
  </div>
</section>
{cta_band()}'''
    page("/apply/", "Apply Now | Online Rental Application | Studio at 1660 Richmond",
         "Apply online for a studio apartment at Studio at 1660 Richmond in Montrose, Houston. See what you need and start your rental application.",
         body, og="court-screen")


def legal_page(path, title, desc, h1, crumbs, content):
    body = page_hero(P["name"], h1, desc, None, crumbs) + f'<section class="section"><div class="wrap prose">{content}</div></section>'
    page(path, title, desc, body)


def build_legal():
    N = P["name"]
    legal_page("/privacy-policy/", "Privacy Policy | Studio at 1660 Richmond",
        f"How {N} collects, uses and protects information submitted through this website.",
        "Privacy <em>Policy</em>", "Privacy Policy", f'''
<!-- [confirm] have management / counsel review before launch -->
<p><em>Last updated: November 2026</em></p>
<p>This Privacy Policy explains how {N} and its management company, {P["manager"]} ("we," "us"), handle information collected through this website.</p>
<h2>Information we collect</h2>
<ul><li>Information you provide in forms, such as your name, email, phone number, preferred tour date and message.</li><li>Basic technical data such as browser type and pages visited, collected through standard server logs.</li></ul>
<h2>How we use information</h2>
<ul><li>To respond to inquiries and schedule tours.</li><li>To share information about availability and leasing.</li><li>To operate, maintain and improve this website.</li></ul>
<h2>Text messages</h2><p>If you share your phone number, we may call or text you about your inquiry. Message and data rates may apply. Reply STOP to opt out.</p>
<h2>Sharing</h2><p>We do not sell your personal information. We may share it with service providers who help us operate our leasing systems, under appropriate confidentiality obligations, or when required by law.</p>
<h2>Your choices</h2><p>You may ask us to update or delete information you have provided by emailing <a href="mailto:{P["email"]}">{P["email"]}</a> or calling <a href="tel:{P["tel"]}">{P["phone"]}</a>.</p>
<h2>Contact</h2><p>{N}, {ADDR}.</p>''')
    legal_page("/terms/", "Terms of Use | Studio at 1660 Richmond",
        f"Terms governing use of the {N} website.",
        "Terms of <em>Use</em>", "Terms", f'''
<!-- [confirm] have management / counsel review before launch -->
<p><em>Last updated: November 2026</em></p>
<p>By using this website you agree to these terms.</p>
<h2>Information on this site</h2><p>Floor plans, pricing, photos, amenities and availability are provided for general information. They are subject to change without notice and do not constitute an offer or guarantee. Floor plans are representative illustrations, square footage is approximate and some images are representative. Please confirm all details with the leasing office.</p>
<h2>Use of the site</h2><p>You agree not to misuse the site, interfere with its operation or attempt to access it by unauthorized means.</p>
<h2>Third-party links</h2><p>Links to third-party sites, such as maps or payment portals, are provided for convenience. We are not responsible for their content or practices.</p>
<h2>Limitation of liability</h2><p>The site is provided "as is" without warranties of any kind, to the fullest extent permitted by law.</p>
<h2>Contact</h2><p>Questions about these terms? Email <a href="mailto:{P["email"]}">{P["email"]}</a>.</p>''')
    legal_page("/accessibility/", "Accessibility Statement | Studio at 1660 Richmond",
        f"{N} is committed to an accessible website for everyone, including people with disabilities.",
        "Accessibility <em>Statement</em>", "Accessibility", f'''
<p>{N} is committed to providing a website that is accessible to everyone, including people with disabilities.</p>
<h2>Our website</h2><p>We aim to conform to the Web Content Accessibility Guidelines (WCAG) 2.2 Level AA. This site uses semantic HTML, keyboard-friendly navigation, visible focus states, text alternatives for images and sufficient color contrast, and it respects reduced-motion preferences.</p>
<h2>Reasonable accommodations</h2><p>Applicants and residents may request reasonable accommodations or modifications by contacting the leasing office.</p>
<h2>Feedback</h2><p>If you have trouble accessing any part of this website, please call <a href="tel:{P["tel"]}">{P["phone"]}</a> or email <a href="mailto:{P["email"]}">{P["email"]}</a>. We will work with you to provide the information you need.</p>''')


def build_sitemap():
    descs = {p: d for p, _, d in PAGES}
    order = ["/", "/studios/", "/amenities/", "/gallery/", "/neighborhood/", "/residents/", "/faqs/", "/contact/", "/apply/", "/privacy-policy/", "/terms/", "/accessibility/"]
    names = {"/": "Home", "/studios/": "The Studios", "/amenities/": "Amenities", "/gallery/": "Gallery", "/neighborhood/": "Neighborhood",
             "/residents/": "Residents", "/faqs/": "FAQs", "/contact/": "Contact &amp; Schedule a Tour", "/apply/": "Apply Now",
             "/privacy-policy/": "Privacy Policy", "/terms/": "Terms of Use", "/accessibility/": "Accessibility Statement"}
    items = "".join(f'<li><a href="{p}">{names[p]}</a><small>{html.escape(descs[p])}</small></li>' for p in order)
    body = page_hero(P["name"], "Site <em>Map</em>", f"Every page on the {P['name']} website in one place.", None, "Site Map") + f'<section class="section"><div class="wrap"><ul class="sitemap-list">{items}</ul></div></section>'
    page("/site-map/", "Site Map | Studio at 1660 Richmond", f"A complete list of pages on the {P['name']} website.", body)


def build_404():
    body = page_hero("Page not found", "This door leads <em>nowhere</em>", "The page you're looking for has moved or doesn't exist. Let's get you back to the courtyard.", None, None,
                     extra='<div class="btn-row" style="margin-top:24px"><a class="btn" href="/">Back to home</a><a class="btn btn--outline-light" href="/studios/">View the studios</a></div>')
    page("/404.html", "Page Not Found | Studio at 1660 Richmond", "The page you requested could not be found.", body, active="")


def main():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)
    for d in ("css", "js", "img", "fonts"):
        shutil.copytree(os.path.join(SRC, d), os.path.join(DIST, d))
    for f in ("favicon.svg", "logo.svg", "robots.txt"):
        shutil.copy(os.path.join(SRC, f), os.path.join(DIST, f))
    build_home(); build_studios(); build_amenities(); build_gallery(); build_neighborhood()
    build_residents(); build_faqs(); build_contact(); build_apply(); build_legal(); build_sitemap(); build_404()
    print(f"Built {len(PAGES)} pages -> {DIST}")

if __name__ == "__main__":
    main()
