"""Shared constants, data and HTML components for the Enforce Interest build.

Imported by build.py and every module in content/. Facts that appear on many
pages (rates, firm details, statute citations) are defined here exactly once.
"""
import html
import json
from datetime import date

SITE = "https://enforceinterest.com"
NAME = "Enforce Interest"
EMAIL = "info@enforceinterest.com"
FIRM = "Rise Public Adjusting"
LICENSE = "3356839"
CITY = "Austin"
BUILD_DATE = date.today().isoformat()
YEAR = BUILD_DATE[:4]
ASSET_V = BUILD_DATE.replace("-", "")

# Texas Finance Code §304.003 postjudgment rates published by the OCCC
# (Historical Table of Postjudgment Interest Rates, rev. 9/17/2026, plus the
# November 2026 rate from the Texas Credit Letter of 10/21/2026).
# One value per month, January..December; None = not published.
OCCC_RATES = {
    1983: [None, None, None, None, None, None, None, None, 10.00, 10.00, 10.00, 10.00],
    1984: [10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.92, 10.99, 10.79, 10.84, 10.32, 10.00],
    1985: [10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00],
    1986: [10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00],
    1987: [10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00],
    1988: [10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00],
    1989: [10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00],
    1990: [10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00],
    1991: [10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00],
    1992: [10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00],
    1993: [10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00],
    1994: [10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00],
    1995: [10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00],
    1996: [10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00],
    1997: [10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00],
    1998: [10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00],
    1999: [10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00],
    2000: [10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00],
    2001: [10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00],
    2002: [10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00],
    2003: [10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 5.00, 5.00, 5.00, 5.00, 5.00],
    2004: [5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00],
    2005: [5.25, 5.25, 5.50, 5.50, 5.75, 6.00, 6.00, 6.25, 6.50, 6.50, 6.75, 7.00],
    2006: [7.25, 7.25, 7.50, 7.50, 7.75, 8.00, 8.00, 8.25, 8.25, 8.25, 8.25, 8.25],
    2007: [8.25, 8.25, 8.25, 8.25, 8.25, 8.25, 8.25, 8.25, 8.25, 8.25, 7.75, 7.50],
    2008: [7.25, 7.25, 6.00, 6.00, 5.25, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00],
    2009: [5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00],
    2010: [5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00],
    2011: [5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00],
    2012: [5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00],
    2013: [5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00],
    2014: [5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00],
    2015: [5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00],
    2016: [5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00],
    2017: [5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00],
    2018: [5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.25, 5.25],
    2019: [5.25, 5.50, 5.50, 5.50, 5.50, 5.50, 5.50, 5.50, 5.25, 5.25, 5.00, 5.00],
    2020: [5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00],
    2021: [5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00],
    2022: [5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.50, 5.50, 6.25, 7.00],
    2023: [7.50, 7.50, 7.75, 7.75, 8.00, 8.25, 8.25, 8.25, 8.50, 8.50, 8.50, 8.50],
    2024: [8.50, 8.50, 8.50, 8.50, 8.50, 8.50, 8.50, 8.50, 8.50, 8.50, 8.00, 7.75],
    2025: [7.75, 7.50, 7.50, 7.50, 7.50, 7.50, 7.50, 7.50, 7.50, 7.50, 7.25, 7.00],
    2026: [6.75, 6.75, 6.75, 6.75, 6.75, 6.75, 6.75, 6.75, 6.75, 6.75, 7.00],
}

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]


def latest_rate():
    """(year, month_index, rate) of the most recent published §304.003 rate."""
    y = max(OCCC_RATES)
    vals = OCCC_RATES[y]
    return y, len(vals) - 1, vals[-1]


RATE_Y, RATE_M, JUDG_RATE = latest_rate()
RATE_MONTH = f"{MONTHS[RATE_M]} {RATE_Y}"            # "November 2026"
FLOAT_RATE = JUDG_RATE + 5                           # §542.060(c) = §304.003 + 5
JUDG_RATE_S = f"{JUDG_RATE:.2f}%"                    # "7.00%"
FLOAT_RATE_S = f"{FLOAT_RATE:.2f}%"                  # "12.00%"


def rates_js():
    flat = {}
    for y, vals in OCCC_RATES.items():
        for i, v in enumerate(vals):
            if v is not None:
                flat[f"{y}-{i + 1:02d}"] = v
    return ("/* Generated by build.py from lib.OCCC_RATES. Tex. Fin. Code §304.003 monthly rates. */\n"
            f"window.EI_RATES={json.dumps(flat, separators=(',', ':'))};\n")


def money(x, cents=True):
    return f"${x:,.2f}" if cents else f"${x:,.0f}"


def interest(principal, rate_pct, days):
    return principal * rate_pct / 100 / 365 * days


esc = html.escape

# ---------------------------------------------------------------- icons
# Simple stroke icons (24px grid). Kept small and consistent.
_ICONS = {
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "calc": '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 11h2M12 11h2M16 11h0M8 15h2M12 15h2M8 18h2M12 18h4"/>',
    "hail": '<path d="M7 15a4 4 0 0 1-.5-8A5.5 5.5 0 0 1 17 8a3.5 3.5 0 0 1 .5 7"/><circle cx="8" cy="19" r="1"/><circle cx="12" cy="21" r="1"/><circle cx="16" cy="19" r="1"/><circle cx="12" cy="17" r="1"/>',
    "wind": '<path d="M3 8h11a3 3 0 1 0-3-3M3 12h15a3 3 0 1 1-3 3M3 16h7"/>',
    "hurricane": '<path d="M12 12m-2.5 0a2.5 2.5 0 1 0 5 0a2.5 2.5 0 1 0-5 0"/><path d="M14.5 12c0-5 3-8 7-9-4 0-9 1.5-11 6M9.5 12c0 5-3 8-7 9 4 0 9-1.5 11-6"/>',
    "flame": '<path d="M12 3c1 3 5 5 5 10a5 5 0 0 1-10 0c0-2 1-3.5 2-4.5 0 2 1 3 2 3 0-3-1-5 1-8.5z"/>',
    "drop": '<path d="M12 3.5c3.5 4.5 6 7.6 6 10.5a6 6 0 0 1-12 0c0-2.9 2.5-6 6-10.5z"/><path d="M9 14.5a3 3 0 0 0 3 3"/>',
    "scale": '<path d="M12 4v16M7 20h10M5 8h14M5 8l-3 6a3 3 0 0 0 6 0zM19 8l-3 6a3 3 0 0 0 6 0z"/>',
    "doc": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
    "shield": '<path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/><path d="M9 12l2 2 4-4"/>',
    "gavel": '<path d="M14 4l6 6M11 7l6 6M12.5 5.5l-5 5M18.5 11.5l-5 5M9 13l-6 6"/>',
    "calendar": '<rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M8 3v4M16 3v4M3.5 10h17M8 14h2M12 14h2M16 14h0M8 17h2"/>',
    "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    "layers": '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>',
    "check": '<path d="M5 12l5 5 9-10"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
    "percent": '<path d="M19 5L5 19"/><circle cx="7" cy="7" r="2.5"/><circle cx="17" cy="17" r="2.5"/>',
    "home": '<path d="M4 11l8-7 8 7v9a1 1 0 0 1-1 1h-5v-6h-4v6H5a1 1 0 0 1-1-1z"/>',
    "list": '<path d="M9 6h11M9 12h11M9 18h11M4 6h.01M4 12h.01M4 18h.01"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "snow": '<path d="M12 3v18M4.2 7.5l15.6 9M4.2 16.5l15.6-9M9 4l3 2 3-2M9 20l3-2 3 2"/>',
    "smoke": '<path d="M5 18c2-2 4 0 6-2s0-4 2-6 4 0 6-2"/><path d="M4 13c2-2 4 0 6-2"/>',
    "pin": '<path d="M12 21s-7-6-7-11a7 7 0 0 1 14 0c0 5-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
}


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_ICONS[name]}</svg>')


ARROW = icon("arrow")

MARK_SVG = ('<svg class="mark" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="31" fill="#6f1818"/>'
            '<text x="32" y="43" text-anchor="middle" font-family="Fraunces,Georgia,serif" font-style="italic" '
            'font-size="31" font-weight="500" fill="#fffdf8">EI</text></svg>')


def btn(href, text, kind="primary", arrow=True, extra=""):
    a = ARROW if arrow else ""
    return f'<a class="btn btn-{kind}" href="{href}"{extra}>{text}{a}</a>'


def cite(text):
    return f'<span class="cite">{text}</span>'


DISCLAIMER = ("We are not a law firm and do not provide legal advice. Our work is limited to public-adjusting "
              "services, claim documentation, timeline analysis and claim presentations to the carrier.")


def disclaim(dark=False):
    return f'<p class="disclaim">{DISCLAIMER}</p>'


# ---------------------------------------------------------------- page parts

def breadcrumbs(trail):
    """trail: list of (name, path). Returns (html, schema)."""
    parts = []
    for i, (n, u) in enumerate(trail):
        if i < len(trail) - 1:
            parts.append(f'<a href="{u}">{esc(n)}</a><span aria-hidden="true">/</span>')
        else:
            parts.append(f'<span aria-current="page">{esc(n)}</span>')
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(trail)]}
    return f'<nav class="crumbs" aria-label="Breadcrumb">{"".join(parts)}</nav>', ld


def page_hero(trail, eyebrow, h1, lede, ctas="", aside="", meta=""):
    crumbs, _ = breadcrumbs(trail)
    inner = f'''{crumbs}
    <span class="eyebrow">{eyebrow}</span>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>{meta}
    {f'<div class="btn-row">{ctas}</div>' if ctas else ""}'''
    if aside:
        inner = f'<div class="hero-2col"><div>{inner}</div><div data-reveal="right">{aside}</div></div>'
    return f'''<section class="page-hero dark">
  <div class="hero-sect" aria-hidden="true" data-parallax="0.15">§</div>
  <div class="wrap">{inner}</div>
</section>'''


def facts(rows):
    return '<div class="hero-facts">' + "".join(f'<div><span>{a}</span><b>{b}</b></div>' for a, b in rows) + '</div>'


def faq_block(items, dark=False):
    """items: list of (question, answer_html). Returns (html, schema)."""
    det = "".join(f'<details><summary>{q}</summary><div class="ans">{a}</div></details>' for q, a in items)
    import re
    plain = lambda t: html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).strip())
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": plain(q),
         "acceptedAnswer": {"@type": "Answer", "text": plain(a)}}
        for q, a in items]}
    return f'<div class="faq">{det}</div>', ld


def cta_band(title="Think your claim was paid late? Let&rsquo;s run the timeline.",
             text="Send us your claim file for a free review. We rebuild the dates, calculate the statutory interest "
                  "and tell you plainly whether there is anything to recover. No upfront cost. Texas claims only.",
             primary=("/contact/", "Start a free claim review"),
             secondary=("/statutory-damages-calculator/", "Calculate interest")):
    sec = btn(secondary[0], secondary[1], "ghost", arrow=False) if secondary else ""
    return f'''<section class="section tight"><div class="wrap"><div class="cta-band" data-reveal="zoom">
  <div class="sect" aria-hidden="true">§</div>
  <span class="eyebrow">Free claim review</span>
  <h2>{title}</h2>
  <p>{text}</p>
  <div class="btn-row">{btn(primary[0], primary[1], "gold")}{sec}</div>
</div></div></section>'''


def section(inner, cls="", wrap="wrap", id_=""):
    i = f' id="{id_}"' if id_ else ""
    return f'<section class="section {cls}"{i}><div class="{wrap}">{inner}</div></section>'


def sec_head(eyebrow, h2, lede="", center=False):
    c = " center" if center else ""
    l = f'<p class="lede">{lede}</p>' if lede else ""
    return f'<div class="sec-head{c}" data-reveal><span class="eyebrow">{eyebrow}</span><h2>{h2}</h2>{l}</div>'


def card(title, text, href=None, ico=None, extra="", tag=""):
    i = f'<div class="ico">{icon(ico)}</div>' if ico else ""
    t = f'<span class="tag wine">{tag}</span>' if tag else ""
    more = '<span class="more">Read more</span>' if href else ""
    inner = f'{t}{i}<h3>{title}</h3><p>{text}</p>{extra}{more}'
    if href:
        return f'<a class="card" href="{href}">{inner}</a>'
    return f'<div class="card">{inner}</div>'


def org_schema():
    return {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": ["ProfessionalService", "LocalBusiness"], "@id": SITE + "/#org",
             "name": NAME, "alternateName": f"{NAME} by {FIRM}", "url": SITE + "/",
             "logo": SITE + "/assets/img/enforce-interest-logo.png", "image": SITE + "/assets/img/og-default.jpg",
             "email": EMAIL,
             "description": "Texas-licensed public adjusting service focused on prompt-payment (Chapter 542) "
                            "statutory interest on late-paid property insurance claims.",
             "parentOrganization": {"@type": "Organization", "name": FIRM},
             "address": {"@type": "PostalAddress", "addressLocality": CITY, "addressRegion": "TX", "addressCountry": "US"},
             "areaServed": {"@type": "State", "name": "Texas"},
             "knowsAbout": ["Texas Prompt Payment of Claims Act", "Texas Insurance Code Chapter 542",
                            "Texas Insurance Code Chapter 542A", "Insurance appraisal", "Public adjusting",
                            "Hail and wind claims", "Hurricane claims", "Fire and smoke damage claims",
                            "Water damage claims"],
             "hasCredential": {"@type": "EducationalOccupationalCredential", "credentialCategory": "license",
                               "name": f"Texas Department of Insurance public adjuster license #{LICENSE}"}},
            {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": NAME,
             "publisher": {"@id": SITE + "/#org"}, "inLanguage": "en-US"},
        ]}


# ---------------------------------------------------------------- long-form layout
def slugify(t):
    import re
    t = re.sub(r"<[^>]+>|&[a-z]+;|&#\d+;", "", t).lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:60]


def with_toc(prose):
    """Give every <h2> an id and return (prose, toc_html)."""
    import re
    items = []

    def rep(m):
        attrs, text = m.group(1), m.group(2)
        if "id=" in attrs:
            i = re.search(r'id="([^"]+)"', attrs).group(1)
            return m.group(0) if items.append((i, text)) is None else ""
        i = slugify(text)
        items.append((i, text))
        return f'<h2 id="{i}"{attrs}>{text}</h2>'
    prose = re.sub(r"<h2([^>]*)>(.*?)</h2>", rep, prose, flags=re.S)
    toc = ('<nav class="toc" aria-label="On this page"><b>On this page</b><ol>' +
           "".join(f'<li><a href="#{i}">{re.sub(r"<[^>]+>", "", t)}</a></li>' for i, t in items) + '</ol></nav>')
    return prose, toc


def side_cta(title="Free claim review", text="Send us the claim file. We rebuild the timeline and calculate the interest. No upfront cost."):
    return (f'<div class="side-cta"><h3>{title}</h3><p>{text}</p>'
            f'<a class="btn btn-gold btn-sm" href="/contact/">Start a review{ARROW}</a></div>')


def side_tool(href="/statutory-damages-calculator/", title="Statutory interest calculator",
              text="Run the §542.060 math on your own dates and payments."):
    return (f'<div class="side-tool"><h3>{title}</h3><p>{text}</p>'
            f'<a class="link-arrow" href="{href}">Open the calculator</a></div>')


def article_body(prose, side_extra="", tool=None):
    prose, toc = with_toc(prose)
    tool_box = side_tool(*tool) if tool else side_tool()
    return (f'<section class="section"><div class="wrap article-wrap"><article class="prose">{prose}</article>'
            f'<aside class="article-side">{toc}{tool_box}{side_cta()}{side_extra}</aside></div></section>')
