#!/usr/bin/env python3
"""Static site generator for claimsconsultant.com.

Every page is rendered from the shared chrome in this file plus the page data
in content/. Output is plain HTML with one stylesheet and one script — upload
the folder and it runs.

    python3 build.py      # writes the whole site into this directory
    python3 validate.py   # check the output before you upload it
"""

import json
import os
import re
import shutil
from datetime import date

from siteconfig import (BIZ, STANDARDS, FEES, NAV, FOOTER_SERVING, TODAY, YEAR,
                        license_line)

from content.industries import INDUSTRIES
from content.services import SERVICES
from content.losstypes import LOSS_TYPES
from content.tools import TOOLS
from content.areas import AREAS
from content.blog import POSTS
from content import pages as staticpages

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = ROOT

PHONE = BIZ["phone_display"]
PHONE_HREF = BIZ["phone_href"]
EMAIL = BIZ["email"]
ORIGIN = BIZ["origin"].rstrip("/")


# ===========================================================================
# Small helpers
# ===========================================================================

def esc(text):
    return (str(text).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def attr(text):
    """Escape for an attribute where the source already contains entities."""
    return str(text).replace('"', "&quot;")


def url(path):
    return ORIGIN + path


def strip_tags(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", str(html))).strip()


def anchor(text):
    s = strip_tags(text).lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    return re.sub(r"\s+", "-", s).strip("-")[:60]


def write(path, html):
    """Write one page. path is a site path like '/services/' or '/404.html'."""
    if path.endswith(".html"):
        dest = os.path.join(OUT, path.lstrip("/"))
    else:
        dest = os.path.join(OUT, path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(html)
    return dest


# ===========================================================================
# Structured data
# ===========================================================================

def org_node():
    node = {
        "@type": ["ProfessionalService", "LocalBusiness"],
        "@id": url("/#organization"),
        "name": BIZ["name"],
        "legalName": BIZ["legal_name"],
        "url": url("/"),
        "description": (
            f"{BIZ['name']} is a firm of {BIZ['descriptor']}. We assess, scope, quantify and "
            f"document large commercial and institutional property losses across "
            f"{BIZ['region']}."
        ),
        "telephone": PHONE,
        "email": EMAIL,
        "priceRange": "Hourly, fixed-fee or per-project",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": BIZ["city"],
            "addressRegion": BIZ["state"],
            "addressCountry": "US",
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": BIZ["latitude"],
            "longitude": BIZ["longitude"],
        },
        "areaServed": [{"@type": "State", "name": "Texas"}]
                      + [{"@type": "City", "name": a["city"]} for a in AREAS],
        "knowsAbout": [
            "claims consulting", "property damage assessment", "commercial property claims",
            "construction cost estimating", "insurance appraisal", "expert witness",
            "business interruption", "hail and windstorm damage",
            "ordinance and law coverage", "damage causation", "contents valuation",
        ],
        "openingHours": BIZ["hours"],
        "sameAs": [],
    }
    creds = [c for c in (BIZ.get("license_ia") and "Texas adjuster licence",
                         BIZ.get("license_pa") and "Texas public insurance adjuster licence",
                         BIZ.get("credential")) if c]
    if creds:
        node["hasCredential"] = creds
    if BIZ.get("founded"):
        node["foundingDate"] = BIZ["founded"]
    return node


def website_node():
    return {
        "@type": "WebSite",
        "@id": url("/#website"),
        "url": url("/"),
        "name": BIZ["name"],
        "publisher": {"@id": url("/#organization")},
        "inLanguage": "en-US",
    }


def breadcrumb_node(trail, path):
    items = []
    for i, (label, href) in enumerate(trail, start=1):
        item = {"@type": "ListItem", "position": i, "name": strip_tags(label)}
        if href:
            item["item"] = url(href)
        items.append(item)
    return {"@type": "BreadcrumbList", "@id": url(path) + "#breadcrumb", "itemListElement": items}


def faq_node(faqs, path):
    return {
        "@type": "FAQPage",
        "@id": url(path) + "#faq",
        "mainEntity": [
            {
                "@type": "Question",
                "name": strip_tags(q),
                "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)},
            }
            for q, a in faqs
        ],
    }


def graph_for(page):
    nodes = [org_node(), website_node()]
    path = page["path"]

    webpage = {
        "@type": page.get("page_type", "WebPage"),
        "@id": url(path) + "#webpage",
        "url": url(path),
        "name": strip_tags(page["title"]),
        "description": strip_tags(page["description"]),
        "isPartOf": {"@id": url("/#website")},
        "about": {"@id": url("/#organization")},
        "inLanguage": "en-US",
        "datePublished": page.get("published", "2024-01-15"),
        "dateModified": page.get("modified", TODAY),
    }
    if page.get("trail"):
        webpage["breadcrumb"] = {"@id": url(path) + "#breadcrumb"}
        nodes.append(breadcrumb_node(page["trail"], path))
    nodes.append(webpage)

    if page.get("faqs"):
        nodes.append(faq_node(page["faqs"], path))

    for extra in page.get("schema", []):
        nodes.append(extra)

    return json.dumps({"@context": "https://schema.org", "@graph": nodes},
                      indent=None, separators=(",", ":"))


def service_schema(name, description, path, service_type=None):
    return {
        "@type": "Service",
        "@id": url(path) + "#service",
        "name": strip_tags(name),
        "serviceType": service_type or strip_tags(name),
        "description": strip_tags(description),
        "provider": {"@id": url("/#organization")},
        "areaServed": {"@type": "State", "name": "Texas"},
        "audience": {"@type": "BusinessAudience", "audienceType":
                     "Institutional and commercial property owners"},
    }


def tool_schema(tool):
    return {
        "@type": "SoftwareApplication",
        "@id": url(tool["path"]) + "#app",
        "name": strip_tags(tool["h1_plain"]),
        "applicationCategory": "BusinessApplication",
        "operatingSystem": "Any modern web browser",
        "url": url(tool["path"]),
        "description": strip_tags(tool["description"]),
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "publisher": {"@id": url("/#organization")},
    }


def article_schema(post):
    return {
        "@type": "Article",
        "@id": url(post["path"]) + "#article",
        "headline": strip_tags(post["h1_plain"]),
        "description": strip_tags(post["description"]),
        "datePublished": post["published"],
        "dateModified": post.get("modified", post["published"]),
        "author": {"@type": "Organization", "@id": url("/#organization"), "name": BIZ["name"]},
        "publisher": {"@id": url("/#organization")},
        "mainEntityOfPage": {"@id": url(post["path"]) + "#webpage"},
        "articleSection": post.get("category", "Claim strategy"),
        "wordCount": post.get("words", 1400),
        "inLanguage": "en-US",
    }


def itemlist_schema(path, name, items):
    return {
        "@type": "ItemList",
        "@id": url(path) + "#list",
        "name": name,
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": strip_tags(t), "url": url(h)}
            for i, (t, h) in enumerate(items, start=1)
        ],
    }


# ===========================================================================
# Chrome
# ===========================================================================

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    'family=Newsreader:ital,opsz,wght@0,6..72,300..600;1,6..72,300..500'
    '&amp;family=IBM+Plex+Sans:wght@400;500;600'
    '&amp;family=IBM+Plex+Mono:wght@400;500&amp;display=swap">'
)


def head(page):
    canonical = url(page["path"])
    robots = page.get("robots", "index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1")
    extra = ""
    if page.get("published"):
        extra += (f'<meta property="article:published_time" content="{page["published"]}">\n'
                  f'<meta property="article:modified_time" content="{page.get("modified", page["published"])}">\n')
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{attr(page["title"])}</title>
<meta name="description" content="{attr(page["description"])}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta name="author" content="{esc(BIZ['name'])}">
<meta property="og:type" content="{page.get('og_type', 'website')}">
<meta property="og:site_name" content="{esc(BIZ['name'])}">
<meta property="og:title" content="{attr(page["title"])}">
<meta property="og:description" content="{attr(page["description"])}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{attr(page["title"])}">
<meta name="twitter:description" content="{attr(page["description"])}">
{extra}<meta name="theme-color" content="#101a22">
<meta name="format-detection" content="telephone=yes">
{FONTS}
<link rel="stylesheet" href="/assets/css/site.css">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="sitemap" type="application/xml" href="/sitemap.xml">
<script type="application/ld+json">{graph_for(page)}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def topbar():
    lic = license_line()
    lic = f" &middot; {lic}" if lic else ""
    return f"""<div class="topbar">
  <div class="wrap">
    <div class="tb-left">
      <span><span class="dot"></span><span class="tb-long">Texas &amp; Gulf Coast &middot; statewide response</span><span class="tb-short">Statewide Texas</span></span>
      <span class="tb-hide">Expert witness &amp; damage consulting &middot; either side of a file{lic}</span>
    </div>
    <div><a href="tel:{PHONE_HREF}">{PHONE}</a></div>
  </div>
</div>
"""


def nav_html(current):
    out = []
    for label, href in NAV:
        aria = ' aria-current="page"' if current.startswith(href) and href != "/" else ""
        out.append(f'<a href="{href}"{aria}>{label}</a>')
    return "".join(out)


def drawer_groups():
    groups = [
        ("Who We Serve", "/who-we-serve/",
         [(i["nav_label"], i["path"]) for i in INDUSTRIES]),
        ("Services", "/services/",
         [(s["nav_label"], s["path"]) for s in SERVICES]),
        ("Loss Types", "/loss-types/",
         [(l["nav_label"], l["path"]) for l in LOSS_TYPES]),
        ("Tools &amp; Calculators", "/tools/",
         [(t["nav_label"], t["path"]) for t in TOOLS]),
        ("Service Areas", "/service-areas/",
         [(a["nav_label"], a["path"]) for a in AREAS]),
        ("Insights", "/blog/", [("All articles", "/blog/")]),
        ("Firm", "/about/",
         [("About", "/about/"), ("How we work", "/how-we-work/"),
          ("Fees &amp; engagement", "/fees/"), ("FAQ", "/faq/"),
          ("Glossary", "/glossary/"), ("Contact", "/contact/")]),
    ]
    html = []
    for label, href, kids in groups:
        subs = "".join(f'<a href="{h}">{t}</a>' for t, h in kids)
        html.append(f'<div class="dgroup"><a href="{href}">{label}</a>'
                    f'<div class="dsub">{subs}</div></div>')
    return "".join(html)


def header(page):
    current = page["path"]
    return f"""{topbar()}<header class="masthead">
  <div class="wrap">
    <a class="wordmark" href="/" aria-label="{esc(BIZ['name'])} — home">
      <span class="wm-name">Claims<b>Consultant</b></span>
      <span class="wm-sub">{esc(BIZ['tagline'])}</span>
    </a>
    <nav class="nav" aria-label="Primary">{nav_html(current)}</nav>
    <div class="mast-cta">
      <a class="mast-phone" href="tel:{PHONE_HREF}">{PHONE}</a>
      <a class="btn btn--sm" href="/contact/">Discuss a matter</a>
    </div>
    <button class="burger" type="button" aria-expanded="false" aria-controls="drawer" aria-label="Open menu">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>
<div class="drawer-scrim" role="presentation"></div>
<div class="drawer" id="drawer" aria-hidden="true" aria-label="Site menu">
  <div class="drawer-head">
    <span class="kicker">Menu</span>
    <button class="drawer-close" type="button" aria-label="Close menu">&times;</button>
  </div>
  <nav aria-label="All pages">{drawer_groups()}</nav>
  <div class="drawer-foot">
    <a class="btn" href="/contact/">Discuss a matter <span class="arw">&rarr;</span></a>
    <p style="margin-top:18px;font-family:var(--mono);font-size:14px;">
      <a href="tel:{PHONE_HREF}" style="text-decoration:none;">{PHONE}</a><br>
      <a href="mailto:{EMAIL}" style="text-decoration:none;">{EMAIL}</a>
    </p>
  </div>
</div>
"""


def crumbs(trail):
    if not trail:
        return ""
    lis = []
    for label, href in trail:
        if href:
            lis.append(f'<li><a href="{href}">{label}</a></li>')
        else:
            lis.append(f'<li aria-current="page">{label}</li>')
    return ('<nav class="crumbs" aria-label="Breadcrumb"><div class="wrap"><ol>'
            + "".join(lis) + "</ol></div></nav>\n")


def cta_band(heading=None, dek=None, primary=("Discuss a matter", "/contact/"),
             secondary=("See how we work", "/how-we-work/")):
    heading = heading or "Get the number established before it becomes <em>a dispute</em>."
    dek = dek or ("The first inspection sets the shape of the whole file. We can join a matter at "
                  "any stage and from either side, but the earlier the loss is documented "
                  "properly, the less of it has to be argued later.")
    return f"""<section class="ctaband">
  <div class="wrap">
    <div class="cols cols--7-5">
      <div>
        <p class="eyebrow">Talk to a consultant</p>
        <h2>{heading}</h2>
        <p class="dek">{dek}</p>
        <div class="btn-row">
          <a class="btn btn--brass" href="{primary[1]}">{primary[0]} <span class="arw">&rarr;</span></a>
          <a class="btn btn--ghost" href="{secondary[1]}">{secondary[0]}</a>
        </div>
      </div>
      <div class="cta-side">
        <p class="kicker" style="color:#9aa3a9;">Direct line</p>
        <a class="cta-phone" href="tel:{PHONE_HREF}">{PHONE}</a>
        <p style="margin-top:14px;font-size:14.5px;">
          <a href="mailto:{EMAIL}" style="color:#cfd5d9;">{EMAIL}</a>
        </p>
        <ul class="checks" style="margin-top:26px;">
          <li>Retained by policyholders, insurers, pools, brokers and counsel.</li>
          <li>Hourly or fixed fee &mdash; never a percentage of the settlement.</li>
          <li>Conflict check before we discuss any matter in detail.</li>
        </ul>
      </div>
    </div>
  </div>
</section>
"""


def footer():
    ind = "".join(f'<li><a href="{i["path"]}">{i["nav_label"]}</a></li>' for i in INDUSTRIES)
    srv = "".join(f'<li><a href="{s["path"]}">{s["nav_label"]}</a></li>' for s in SERVICES)
    lts = "".join(f'<li><a href="{l["path"]}">{l["nav_label"]}</a></li>' for l in LOSS_TYPES)
    tls = "".join(f'<li><a href="{t["path"]}">{t["nav_label"]}</a></li>' for t in TOOLS)
    ars = "".join(f'<li><a href="{a["path"]}">{a["nav_label"]}</a></li>' for a in AREAS)
    lic = license_line()
    lic = f"<br>{lic}" if lic else ""
    return f"""<footer class="footer">
  <div class="wrap">
    <div class="footer-top">
      <div class="footer-brand">
        <span class="wm-name">Claims<b>Consultant</b></span>
        <span class="wm-sub">{esc(BIZ['tagline'])}</span>
        <p>Expert witnesses and damage consultants on large institutional and commercial
           property losses across Texas &mdash; churches, school districts, municipalities,
           campuses and portfolios. Retained by either side. The method does not change
           with the client.</p>
        <div class="footer-contact">
          <a href="tel:{PHONE_HREF}">{PHONE}</a>
          <a href="mailto:{EMAIL}">{EMAIL}</a>
        </div>
      </div>
      <div class="fnav">
        <div><h4>Property types</h4><ul>{ind}</ul></div>
        <div><h4>Services</h4><ul>{srv}</ul>
            <h4 style="margin-top:26px;">Loss types</h4><ul>{lts}</ul></div>
        <div><h4>Tools &amp; calculators</h4><ul>{tls}</ul></div>
        <div>
          <h4>Service areas</h4><ul>{ars}</ul>
          <h4 style="margin-top:26px;">Firm</h4>
          <ul>
            <li><a href="/about/">About the firm</a></li>
            <li><a href="/who-we-work-for/">Who we work for</a></li>
            <li><a href="/how-we-work/">How we work</a></li>
            <li><a href="/fees/">Fees &amp; engagement</a></li>
            <li><a href="/blog/">Insights</a></li>
            <li><a href="/glossary/">Claims glossary</a></li>
            <li><a href="/faq/">FAQ</a></li>
            <li><a href="/contact/">Contact</a></li>
          </ul>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <div>&copy; <span data-year>{YEAR}</span> {esc(BIZ['legal_name'])}. All rights reserved.{lic}</div>
      <div class="legal-links">
        <a href="/privacy-policy/">Privacy</a>
        <a href="/terms/">Terms</a>
        <a href="/disclaimer/">Disclaimer</a>
        <a href="/accessibility/">Accessibility</a>
        <a href="/sitemap/">Sitemap</a>
      </div>
    </div>
    <p class="disclaimer">
      {esc(BIZ['name'])} provides expert witness and damage consulting services: causation
      analysis, damage assessment, construction cost estimating, testing and reporting, contents
      valuation, appraisal and testimony. We
      hold Texas adjuster and public insurance adjuster licences, which is what allows us to be
      retained by either party; on any individual matter we act in one capacity only, stated in
      the engagement letter, and we never act for both parties to the same loss. We are not a
      law firm and do not provide legal advice. Calculators,
      timelines and figures published on this site are planning aids built from published
      industry cost conventions and published standards. They are not appraisals, not coverage
      opinions, and not a substitute for reading the policy. Coverage is determined by the policy
      or coverage document in force at the date of loss. Serving {FOOTER_SERVING}.
    </p>
  </div>
</footer>
<script src="/assets/js/site.js" defer></script>
</body>
</html>
"""


# ===========================================================================
# Block renderer — the vocabulary content/ is written in
# ===========================================================================

def render_blocks(blocks, prose=False):
    out = []
    for b in blocks:
        kind = b[0]

        if kind == "p":
            out.append(f"<p>{b[1]}</p>")

        elif kind == "lede":
            out.append(f'<p class="lede">{b[1]}</p>')

        elif kind == "h2":
            out.append(f'<h2 id="{anchor(b[1])}">{b[1]}</h2>')

        elif kind == "h3":
            out.append(f'<h3 id="{anchor(b[1])}">{b[1]}</h3>')

        elif kind == "h4":
            out.append(f"<h4>{b[1]}</h4>")

        elif kind == "ul":
            items = "".join(f"<li>{i}</li>" for i in b[1])
            out.append(f"<ul>{items}</ul>")

        elif kind == "ol":
            items = "".join(f"<li>{i}</li>" for i in b[1])
            out.append(f"<ol>{items}</ol>")

        elif kind == "checks":
            items = "".join(f"<li>{i}</li>" for i in b[1])
            out.append(f'<ul class="checks">{items}</ul>')

        elif kind == "callout":
            out.append(f'<div class="callout"><h4>{b[1]}</h4>{render_blocks(b[2])}</div>')

        elif kind == "quote":
            cite = f"<cite>{b[2]}</cite>" if len(b) > 2 and b[2] else ""
            out.append(f'<blockquote class="pullquote">{b[1]}{cite}</blockquote>')

        elif kind == "table":
            caption, headers, rows = b[1], b[2], b[3]
            numcls = ' class="num"'
            thead = "".join(
                "<th scope=\"col\"%s>%s</th>" % (numcls if h.startswith("~") else "", h.lstrip("~"))
                for h in headers)
            body = []
            for r in rows:
                cells = []
                for j, c in enumerate(r):
                    c = str(c)
                    cls = ' class="num"' if c.startswith("~") else ""
                    c = c.lstrip("~")
                    tag = "th" if j == 0 and len(r) > 1 else "td"
                    scope = ' scope="row"' if tag == "th" else ""
                    cells.append(f"<{tag}{scope}{cls}>{c}</{tag}>")
                body.append("<tr>" + "".join(cells) + "</tr>")
            cap = f"<caption>{caption}</caption>" if caption else ""
            out.append('<div class="tablewrap"><table class="data">' + cap +
                       f"<thead><tr>{thead}</tr></thead><tbody>" + "".join(body) +
                       "</tbody></table></div>")

        elif kind == "steps":
            items = "".join(
                f'<div class="step"><div><h3>{t}</h3></div><div>{body}</div></div>'
                for t, body in b[1])
            out.append(f'<div class="steps">{items}</div>')

        elif kind == "stats":
            cls = "stats stats--%d" % (4 if len(b[1]) % 4 == 0 else 3)
            items = "".join(
                f'<div class="stat"><span class="sv">{v}</span><span class="sl">{l}</span></div>'
                for v, l in b[1])
            out.append(f'<div class="{cls}">{items}</div>')

        elif kind == "cards":
            items = []
            for n, (t, body, href) in enumerate(b[1], start=1):
                items.append(
                    f'<a class="card" href="{href}"><span class="cnum">{n:02d}</span>'
                    f"<h3>{t}</h3><p>{body}</p>"
                    f'<span class="tlink">Read more <span class="arw">&rarr;</span></span></a>')
            cols = 3 if len(b[1]) % 3 == 0 or len(b[1]) > 4 else 2
            out.append(f'<div class="cardgrid cardgrid--{cols}">' + "".join(items) + "</div>")

        elif kind == "links":
            items = []
            for n, (t, desc, href) in enumerate(b[1], start=1):
                items.append(
                    f'<li><a href="{href}"><span class="ll-n">{n:02d}</span>'
                    f'<span><span class="ll-t">{t}</span><br><span class="ll-d">{desc}</span></span>'
                    f'<span class="arw">&rarr;</span></a></li>')
            out.append('<ul class="linklist">' + "".join(items) + "</ul>")

        elif kind == "faq":
            items = "".join(
                f'<details><summary>{q}<span class="sign">+</span></summary>'
                f'<div class="acc-body">{a}</div></details>'
                for q, a in b[1])
            out.append(f'<div class="acc" data-exclusive>{items}</div>')

        elif kind == "feature":
            out.append(f'<div class="feature"><h3>{b[1]}</h3><div class="stack mt-m">'
                       + render_blocks(b[2]) + "</div></div>")

        elif kind == "ledger":
            title, rows = b[1], b[2]
            body = "".join(f'<div class="ledger-row"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in rows)
            foot = f'<div class="ledger-foot">{b[3]}</div>' if len(b) > 3 and b[3] else ""
            out.append('<div class="ledger"><div class="ledger-head"><b>' + title +
                       '</b><span>Ref.</span></div><dl style="margin:0;">' + body + "</dl>" + foot + "</div>")

        elif kind == "html":
            out.append(b[1])

        elif kind == "spacer":
            out.append('<div class="mt-l"></div>')

        else:
            raise ValueError("unknown block: %r" % (kind,))

    sep = "\n" if prose else "\n"
    return sep.join(out)


def section(sec):
    """Render one page section from a dict."""
    band = sec.get("band", "")
    cls = "section"
    if sec.get("tight"):
        cls += " section--tight"
    if sec.get("flush"):
        cls += " section--flush"
    if band == "paper2":
        cls += " band band--ruled"
    elif band == "ink":
        cls += " band band--ink on-ink"
    sid = f' id="{sec["id"]}"' if sec.get("id") else ""
    wrap = sec.get("wrap", "")
    wcls = "wrap" + (f" wrap--{wrap}" if wrap else "")

    headbits = []
    if sec.get("eyebrow"):
        headbits.append(f'<p class="eyebrow">{sec["eyebrow"]}</p>')
    if sec.get("h2"):
        headbits.append(f'<h2 id="{sec.get("id") or anchor(sec["h2"])}">{sec["h2"]}</h2>')
    if sec.get("dek"):
        headbits.append(f'<p class="dek">{sec["dek"]}</p>')
    head_html = f'<div class="head-block">{"".join(headbits)}</div>' if headbits else ""

    body = render_blocks(sec.get("blocks", []))

    if sec.get("aside"):
        inner = (f'<div class="cols cols--7-5"><div class="stack">{head_html}{body}</div>'
                 f'<div class="stack">{render_blocks(sec["aside"])}</div></div>')
    elif head_html and body:
        inner = f'{head_html}<div class="mt-l stack">{body}</div>'
    else:
        inner = head_html + body

    return f'<section class="{cls}"{sid}><div class="{wcls}">{inner}</div></section>\n'


def sections(seclist):
    return "".join(section(s) for s in seclist)


# ===========================================================================
# Page templates
# ===========================================================================

def page_shell(page, body):
    return head(page) + header(page) + crumbs(page.get("trail")) + \
        f'<main id="main">\n{body}</main>\n' + \
        (cta_band(**page["cta"]) if page.get("cta") else cta_band()) + footer()


def standard_page(page):
    """A page built from a pagehead plus a list of sections."""
    ph = []
    if page.get("eyebrow"):
        ph.append(f'<p class="eyebrow">{page["eyebrow"]}</p>')
    ph.append(f'<h1>{page["h1"]}</h1>')
    if page.get("lede"):
        ph.append(f'<p class="lede">{page["lede"]}</p>')
    aside = page.get("head_aside")
    head_inner = "".join(ph)
    if aside:
        head_inner = (f'<div class="cols cols--7-5"><div>{head_inner}</div>'
                      f'<div>{render_blocks(aside)}</div></div>')
    if page.get("head_meta"):
        head_inner += ('<div class="hero-meta">'
                       + "".join(f"<span>{m}</span>" for m in page["head_meta"]) + "</div>")
    body = (f'<section class="pagehead"><div class="wrap">{head_inner}</div></section>\n'
            + sections(page.get("sections", [])))
    return page_shell(page, body)


def article_page(post, related):
    toc = [(strip_tags(b[1]), anchor(b[1])) for b in post["body"] if b[0] == "h2"]
    toc_html = ""
    if len(toc) > 2:
        lis = "".join(f'<li><a href="#{a}">{t}</a></li>' for t, a in toc)
        toc_html = f'<div class="toc toc--sticky"><h4>On this page</h4><ol>{lis}</ol></div>'

    rel = "".join(
        f'<li><a href="{p["path"]}"><span class="ll-n">{i:02d}</span>'
        f'<span><span class="ll-t">{p["h1_plain"]}</span><br>'
        f'<span class="ll-d">{p["blurb"]}</span></span>'
        f'<span class="arw">&rarr;</span></a></li>'
        for i, p in enumerate(related, start=1))

    body = f"""<article>
<section class="article-head"><div class="wrap wrap--mid">
  <p class="eyebrow">{post.get('category', 'Claim strategy')}</p>
  <h1>{post['h1']}</h1>
  <p class="lede mt-m">{post['lede']}</p>
  <div class="article-meta">
    <span>Published {date.fromisoformat(post['published']).strftime('%B %-d, %Y')}</span>
    <span>{post.get('read', '9')} min read</span>
    <span>By the {esc(BIZ['name'])} claims desk</span>
  </div>
</div></section>
<section class="section section--tight"><div class="wrap">
  <div class="cols cols--8-4">
    <div class="prose">{render_blocks(post['body'], prose=True)}</div>
    <div class="stack">{toc_html}
      <div class="feature feature--wash">
        <p class="kicker">Working a live file?</p>
        <h3 style="margin-top:10px;">Have the loss measured independently.</h3>
        <p style="font-size:15px;color:var(--slate);margin-top:12px;">
          Policy read, scope measured, conclusions stated in writing. Hourly or fixed fee.</p>
        <a class="btn btn--sm mt-m" href="/contact/">Discuss a matter <span class="arw">&rarr;</span></a>
      </div>
    </div>
  </div>
</div></section>
<section class="section band band--ruled"><div class="wrap">
  <p class="eyebrow">Keep reading</p>
  <h2>Related from the claims desk</h2>
  <ul class="linklist mt-l">{rel}</ul>
</div></section>
</article>
"""
    return page_shell(post, body)


# ===========================================================================
# Homepage
# ===========================================================================

def homepage():
    page = {
        "path": "/",
        "title": "Texas Expert Witness &amp; Damage Consultants | Property Loss",
        "description": (
            "Expert witness and damage consulting on large Texas commercial property losses. "
            "Causation, cost estimating, appraisal and testimony — retained by either side."
        ),
        "page_type": "WebPage",
        "schema": [
            service_schema(
                "Expert witness and damage consulting",
                "Expert witness, causation and damage consulting on institutional and large commercial property losses in Texas.",
                "/", "Expert Witness and Damage Consulting"),
            itemlist_schema("/", "Industries served",
                            [(i["nav_label"], i["path"]) for i in INDUSTRIES]),
        ],
        "faqs": staticpages.HOME_FAQS,
    }

    ind_cards = "".join(
        f'<a class="card" href="{i["path"]}"><span class="cnum">{n:02d}</span>'
        f'<h3>{i["card_title"]}</h3><p>{i["card_blurb"]}</p>'
        f'<span class="tlink">{i["nav_label"]} claims <span class="arw">&rarr;</span></span></a>'
        for n, i in enumerate(INDUSTRIES, start=1))

    svc_links = "".join(
        f'<li><a href="{s["path"]}"><span class="ll-n">{n:02d}</span>'
        f'<span><span class="ll-t">{s["nav_label"]}</span><br>'
        f'<span class="ll-d">{s["card_blurb"]}</span></span>'
        f'<span class="arw">&rarr;</span></a></li>'
        for n, s in enumerate(SERVICES, start=1))

    tool_cards = "".join(
        f'<a class="card" href="{t["path"]}"><span class="cnum">{n:02d}</span>'
        f'<h3>{t["nav_label"]}</h3><p>{t["card_blurb"]}</p>'
        f'<span class="tlink">Open the calculator <span class="arw">&rarr;</span></span></a>'
        for n, t in enumerate(TOOLS, start=1))

    recent = "".join(
        f'<a class="postitem" href="{p["path"]}">'
        f'<div class="pmeta"><b>{p.get("category", "Claim strategy")}</b>'
        f'{date.fromisoformat(p["published"]).strftime("%b %Y")} &middot; {p.get("read", "9")} min</div>'
        f'<div><h3>{p["h1_plain"]}</h3><p>{p["blurb"]}</p></div></a>'
        for p in POSTS[:4])

    area_tags = "".join(f'<a class="tag" href="{a["path"]}">{a["nav_label"]}</a>' for a in AREAS)

    body = f"""<section class="hero">
  <div class="wrap">
    <div class="cols cols--7-5">
      <div>
        <p class="eyebrow">Expert witness &amp; damage consulting &middot; Texas</p>
        <h1>Two parties.<br>Two estimates.<br><em>One</em> set of facts.</h1>
        <p class="lede">We are damage consultants and testifying experts on large commercial
          property losses. Causation, scope, cost and contents &mdash; established from the
          building rather than asserted from a position, and written to survive a deposition.
          Policyholders, insurers, risk pools and counsel all retain us for the same thing.</p>
        <div class="btn-row">
          <a class="btn" href="/contact/">Discuss a matter <span class="arw">&rarr;</span></a>
          <a class="btn btn--ghost" href="/tools/">Run the numbers first</a>
        </div>
        <div class="hero-meta">
          <span>Large commercial &amp; institutional only</span>
          <span>Retained by either side</span>
          <span>Expert work never contingent</span>
        </div>
      </div>
      <div>
        <div class="ledger">
          <div class="ledger-head"><b>Evidence half-life</b><span>Typical</span></div>
          <dl style="margin:0;">
            <div class="ledger-row"><dt>High-water marks, before cleaning</dt><dd>2&ndash;5 days</dd></div>
            <div class="ledger-row"><dt>The failed pipe, before the plumber discards it</dt><dd>Hours</dd></div>
            <div class="ledger-row"><dt>Building management system logs</dt><dd>30&ndash;90 days</dd></div>
            <div class="ledger-row"><dt>Contents, before disposal</dt><dd>Days</dd></div>
            <div class="ledger-row"><dt>Cabinet substrate, before demolition</dt><dd>Days</dd></div>
            <div class="ledger-row"><dt>Roof test cuts, before the re-roof</dt><dd>Until repair</dd></div>
          </dl>
          <div class="ledger-foot">Every one of these settles an argument, and every one is gone
            within weeks of the loss. It is the reason an early inspection is worth more than a
            late opinion &mdash; whichever side is asking.
            <a href="/blog/first-72-hours-after-a-commercial-property-loss/">The first 72 hours &rarr;</a></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section band band--ruled">
  <div class="wrap">
    <div class="cols cols--5-7">
      <div>
        <p class="eyebrow">Why large files stall</p>
        <h2>Most claim disputes are not about coverage.<br><em>They are about scope.</em></h2>
      </div>
      <div class="stack">
        <p>Two competent people can walk the same damaged building and produce estimates that differ
        by a third. Not because either is dishonest, but because a large loss contains dozens of
        judgment calls and nobody wrote down the evidence for any of them. A missed layer of decking.
        Code upgrades treated as betterment. Overhead and profit on a job that may or may not need a
        general contractor. Business interruption modeled on a revenue trend nobody tested.</p>
        <p>Each of those is answerable with facts. Most of them never get answered, because the
        people arguing are also the people with a position, and the underlying measurements were
        never taken to a standard that would settle anything.</p>
        <p>That is the work: a measured survey, a line-item scope, laboratory analysis where the
        question is a laboratory question, and a written basis for every judgment call &mdash;
        produced to the same standard regardless of which party retained us. An opinion that only
        holds up for the side that paid for it is not an opinion, and a competent cross-examiner
        will establish that in about four minutes.</p>
        <a class="tlink" href="/how-we-work/">How a file gets built <span class="arw">&rarr;</span></a>
      </div>
    </div>
  </div>
</section>

<section class="section band band--ink on-ink">
  <div class="wrap">
    <div class="head-block">
      <p class="eyebrow">Where we work</p>
      <h2>Institutions and large commercial property. <em>Nothing smaller.</em></h2>
      <p class="dek">A 40,000-square-foot sanctuary, a district with nineteen campuses and one
      blanket limit, a city hall with a FEMA obligation running alongside the insurance claim &mdash;
      these are not big houses. They are different losses, with different wording, different
      valuation rules and different politics.</p>
    </div>
    <div class="stats stats--4 mt-l">
      <div class="stat"><span class="sv">0%</span><span class="sl">Contingency on expert and consulting work. The opinion does not move with the outcome, which is the first question on cross and the reason either side can rely on it.</span></div>
      <div class="stat"><span class="sv">702</span><span class="sl">The evidence rule an opinion has to satisfy. Reliability is a question about method, which is why ours is written down before the conclusion is.</span></div>
      <div class="stat"><span class="sv">3</span><span class="sl">Roles on an appraisal panel &mdash; two appraisers and an umpire. We serve in any of them, disclosing prior engagements first.</span></div>
      <div class="stat"><span class="sv">0</span><span class="sl">Referral money taken from contractors, restoration firms or vendors, in either direction. You choose who does the work.</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="head-block">
      <p class="eyebrow">Who we serve</p>
      <h2>Nine kinds of building, nine different arguments.</h2>
      <p class="dek">The policy language, the governing body, the valuation method and the political
      cost of getting it wrong all change with the property type. Pick yours.</p>
    </div>
    <div class="cardgrid cardgrid--3 mt-l">{ind_cards}</div>
  </div>
</section>

<section class="section band band--ruled">
  <div class="wrap">
    <div class="cols cols--5-7">
      <div>
        <p class="eyebrow">Services</p>
        <h2>Retained to answer a specific question.</h2>
        <p class="dek">Most engagements begin narrow: is this hail or wear, can the casework be
        saved, is that estimate complete, what is this inventory actually worth. Nine of those
        questions come up often enough to have their own page.</p>
        <div class="btn-row"><a class="btn btn--ghost" href="/services/">All services</a></div>
      </div>
      <div><ul class="linklist">{svc_links}</ul></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="head-block">
      <p class="eyebrow">Tools</p>
      <h2>Six calculators we actually use on live files.</h2>
      <p class="dek">Built for commercial numbers, not householder ones. Nothing is stored, nothing
      is emailed, and no figure here is a substitute for a policy read &mdash; but they will tell you
      quickly whether the offer on your desk is in the right ballpark.</p>
    </div>
    <div class="cardgrid cardgrid--3 mt-l">{tool_cards}</div>
  </div>
</section>

<section class="section band band--ruled">
  <div class="wrap">
    <div class="cols cols--7-5">
      <div>
        <p class="eyebrow">Process</p>
        <h2>What the first thirty days look like.</h2>
        <div class="steps mt-l">
          <div class="step"><div><h3>Policy before property</h3></div><div>
            <p>We read the declarations, the forms, the endorsements and the schedule of values
            before we walk the building. Half of what gets argued about later is already settled by
            wording sitting in the file &mdash; coinsurance, valuation basis, ordinance and law
            limits, named-storm deductibles, the period of indemnity.</p></div></div>
          <div class="step"><div><h3>Document while it is still true</h3></div><div>
            <p>Full photographic and measured survey, drone and moisture mapping where it helps,
            engineers or forensic accountants engaged where the loss warrants them. Evidence degrades:
            tarps go up, crews clean, and the thing you needed to prove disappears into a dumpster.</p></div></div>
          <div class="step"><div><h3>Build the estimate, then the argument</h3></div><div>
            <p>A line-item scope in the industry-standard estimating platform, priced to the
            local market, with code upgrades, soft costs and time-element losses carried
            separately so nothing disappears into a lump-sum allowance.</p></div></div>
          <div class="step"><div><h3>State the basis in writing</h3></div><div>
            <p>Every judgment call recorded with the evidence behind it, differences between
            positions itemized rather than described. Where a gap will not close on the facts, we
            say what we think it needs &mdash; appraisal, a specialist, or counsel &mdash; early
            rather than after another six months of letters.</p></div></div>
        </div>
      </div>
      <div class="stack">
        <div class="feature feature--wash">
          <p class="kicker">Start here</p>
          <h3 style="margin-top:10px;">Three documents decide most of the file.</h3>
          <ul class="checks mt-m">
            <li>The <strong>declarations page</strong> &mdash; limits, deductibles, valuation basis,
              and whether the schedule is blanket or per-location.</li>
            <li>The <strong>loss notice</strong> &mdash; its date anchors every other date in
              the file, including how long the evidence had to degrade.</li>
            <li>The <strong>first estimate</strong> &mdash; not for its total, but for what it is
              silent about.</li>
          </ul>
          <a class="btn btn--sm mt-m" href="/how-we-work/">See the full method <span class="arw">&rarr;</span></a>
        </div>
        <div class="callout">
          <h4>A note on timing</h4>
          <p>We can be brought in at any point &mdash; before notice, mid-file, after a coverage
          position has been taken, even after a partial payment. What nobody can do is
          un-photograph a building that has already been repaired.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="cols cols--5-7">
      <div>
        <p class="eyebrow">Insights</p>
        <h2>Written for the people who have to explain the number to somebody else.</h2>
        <p class="dek">No listicles. Policy wording, Texas statute, and the evidence that actually
        resolves disputes on institutional files.</p>
        <div class="btn-row"><a class="btn btn--ghost" href="/blog/">All articles</a></div>
      </div>
      <div class="postlist">{recent}</div>
    </div>
  </div>
</section>

<section class="section band band--ruled">
  <div class="wrap">
    <div class="head-block">
      <p class="eyebrow">Common questions</p>
      <h2>What boards, councils, carriers and counsel ask first.</h2>
    </div>
    <div class="mt-l">{render_blocks([("faq", staticpages.HOME_FAQS)])}</div>
    <div class="mt-l rule-top">
      <p class="kicker" style="margin-bottom:14px;">Service areas</p>
      <div class="tagrow">{area_tags}<a class="tag" href="/service-areas/">All of Texas &rarr;</a></div>
    </div>
  </div>
</section>
"""
    return page_shell(page, body)


# ===========================================================================
# Hub + detail builders
# ===========================================================================

def build_hub(path, eyebrow, h1, lede, items, intro_sections, trail, title, description,
              card_mode="links", closing=None, schema=None, faqs=None, head_aside=None):
    listing = []
    if card_mode == "cards":
        listing.append(("cards", [(i["card_title"], i["card_blurb"], i["path"]) for i in items]))
    else:
        listing.append(("links", [(i["card_title"], i["card_blurb"], i["path"]) for i in items]))

    secs = [{"band": "paper2", "eyebrow": "Index", "h2": "Every page in this section",
             "blocks": listing}]
    secs += intro_sections
    if faqs:
        secs.append({"eyebrow": "Questions", "h2": "Frequently asked", "band": "",
                     "blocks": [("faq", faqs)]})
    if closing:
        secs.append(closing)

    page = {
        "path": path, "title": title, "description": description,
        "eyebrow": eyebrow, "h1": h1, "lede": lede, "trail": trail,
        "sections": secs, "schema": schema or [], "faqs": faqs,
        "head_aside": head_aside,
        "page_type": "CollectionPage",
    }
    return standard_page(page)


# ===========================================================================
# Sitemap / robots / misc
# ===========================================================================

def all_pages():
    """(path, priority, changefreq) for every indexable page."""
    out = [("/", "1.0", "weekly")]
    out += [("/who-we-serve/", "0.9", "monthly")]
    out += [(i["path"], "0.8", "monthly") for i in INDUSTRIES]
    out += [("/services/", "0.9", "monthly")]
    out += [(s["path"], "0.8", "monthly") for s in SERVICES]
    out += [("/loss-types/", "0.8", "monthly")]
    out += [(l["path"], "0.7", "monthly") for l in LOSS_TYPES]
    out += [("/tools/", "0.9", "monthly")]
    out += [(t["path"], "0.8", "monthly") for t in TOOLS]
    out += [("/service-areas/", "0.8", "monthly")]
    out += [(a["path"], "0.7", "monthly") for a in AREAS]
    out += [("/blog/", "0.8", "weekly")]
    out += [(p["path"], "0.7", "monthly") for p in POSTS]
    out += [("/about/", "0.7", "yearly"), ("/who-we-work-for/", "0.8", "yearly"),
            ("/how-we-work/", "0.8", "yearly"),
            ("/fees/", "0.7", "yearly"), ("/faq/", "0.7", "monthly"),
            ("/glossary/", "0.7", "yearly"), ("/contact/", "0.8", "yearly"),
            ("/privacy-policy/", "0.2", "yearly"), ("/terms/", "0.2", "yearly"),
            ("/disclaimer/", "0.2", "yearly"), ("/accessibility/", "0.2", "yearly"),
            ("/sitemap/", "0.3", "monthly")]
    return out


def build_sitemap():
    rows = []
    for path, prio, freq in all_pages():
        lastmod = TODAY
        for p in POSTS:
            if p["path"] == path:
                lastmod = p.get("modified", p["published"])
        rows.append(
            f"  <url>\n    <loc>{url(path)}</loc>\n    <lastmod>{lastmod}</lastmod>\n"
            f"    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(rows) + "\n</urlset>\n")
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write(xml)


def build_robots():
    txt = f"""User-agent: *
Allow: /

# Nothing here is behind a login; crawl it all.
Sitemap: {url('/sitemap.xml')}
"""
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write(txt)


def build_htaccess():
    txt = """# claimsconsultant.com — Apache config for a plain static upload.

Options -Indexes
DirectoryIndex index.html

<IfModule mod_rewrite.c>
  RewriteEngine On

  # https + non-www canonical host
  RewriteCond %{HTTPS} !=on [OR]
  RewriteCond %{HTTP:X-Forwarded-Proto} =http
  RewriteRule ^ https://claimsconsultant.com%{REQUEST_URI} [L,R=301]
  RewriteCond %{HTTP_HOST} ^www\\.claimsconsultant\\.com$ [NC]
  RewriteRule ^ https://claimsconsultant.com%{REQUEST_URI} [L,R=301]

  # every page is a directory with a trailing slash
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteCond %{REQUEST_URI} !(/$|\\.[a-zA-Z0-9]{1,5}$)
  RewriteRule ^(.*)$ /$1/ [L,R=301]
</IfModule>

ErrorDocument 404 /404.html

<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css text/plain text/xml application/javascript application/json image/svg+xml
</IfModule>

<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/css "access plus 1 year"
  ExpiresByType application/javascript "access plus 1 year"
  ExpiresByType image/svg+xml "access plus 1 year"
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType text/html "access plus 1 hour"
</IfModule>

<IfModule mod_headers.c>
  Header set X-Content-Type-Options "nosniff"
  Header set Referrer-Policy "strict-origin-when-cross-origin"
  Header set X-Frame-Options "SAMEORIGIN"
  Header set Permissions-Policy "geolocation=(), microphone=(), camera=()"
</IfModule>
"""
    with open(os.path.join(OUT, ".htaccess"), "w", encoding="utf-8") as fh:
        fh.write(txt)


def build_manifest():
    data = {
        "name": BIZ["name"] + " — " + BIZ["tagline"],
        "short_name": BIZ["name"],
        "start_url": "/",
        "display": "standalone",
        "background_color": "#fbf8f3",
        "theme_color": "#101a22",
        "icons": [
            {"src": "/favicon.svg", "sizes": "any", "type": "image/svg+xml"},
            {"src": "/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"},
        ],
    }
    with open(os.path.join(OUT, "site.webmanifest"), "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
        fh.write("\n")


# The mark: a ruled ledger in a brass frame. Defined once, in a 64-unit grid,
# and rendered both as SVG (favicon) and as raw PNG (touch icon).
INK = (0x10, 0x1a, 0x22)
BRASS = (0xb9, 0x8a, 0x3c)
PAPER = (0xfb, 0xf8, 0xf3)
MARK = [                      # (x, y, w, h, color)
    (6.0, 6.0, 52.0, 1.6, BRASS),      # frame top
    (6.0, 56.4, 52.0, 1.6, BRASS),     # frame bottom
    (6.0, 6.0, 1.6, 52.0, BRASS),      # frame left
    (56.4, 6.0, 1.6, 52.0, BRASS),     # frame right
    (17.0, 22.0, 30.0, 3.0, PAPER),    # rule one
    (17.0, 30.5, 21.0, 3.0, PAPER),    # rule two
    (17.0, 39.0, 30.0, 3.0, BRASS),    # rule three, the total
]


def build_touch_icon(size=180, path="apple-touch-icon.png"):
    """Write the mark as a PNG with no image library."""
    import struct
    import zlib

    scale = size / 64.0
    px = [[INK for _ in range(size)] for _ in range(size)]
    for x, y, w, h, color in MARK:
        x0, y0 = int(round(x * scale)), int(round(y * scale))
        x1, y1 = int(round((x + w) * scale)), int(round((y + h) * scale))
        for yy in range(max(y0, 0), min(y1, size)):
            row = px[yy]
            for xx in range(max(x0, 0), min(x1, size)):
                row[xx] = color

    raw = bytearray()
    for row in px:
        raw.append(0)                       # filter type 0
        for r, g, b in row:
            raw += bytes((r, g, b))

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff))

    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
           + chunk(b"IEND", b""))
    with open(os.path.join(OUT, path), "wb") as fh:
        fh.write(png)


def build_favicon():
    """A drawn mark: the firm's initials set in a ruled square. No image files."""
    rects = "\n  ".join(
        '<rect x="%g" y="%g" width="%g" height="%g" fill="#%02x%02x%02x"/>'
        % (x, y, w, h, c[0], c[1], c[2]) for x, y, w, h, c in MARK)
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" '
           'role="img" aria-label="Claims Consultant">\n'
           '  <rect width="64" height="64" fill="#%02x%02x%02x"/>\n  ' % INK
           + rects + "\n</svg>\n")
    with open(os.path.join(OUT, "favicon.svg"), "w", encoding="utf-8") as fh:
        fh.write(svg)


def build_404():
    page = {
        "path": "/404.html",
        "title": f"Page not found | {BIZ['name']}",
        "description": ("That page has moved or never existed. Here is the rest of the site: "
                        "property types, claim services, calculators and service areas."),
        "robots": "noindex,follow",
    }
    links = [(i["nav_label"], i["card_blurb"], i["path"]) for i in INDUSTRIES[:3]]
    links += [(t["nav_label"], t["card_blurb"], t["path"]) for t in TOOLS[:3]]
    body = f"""<section class="pagehead"><div class="wrap">
  <p class="eyebrow">Error 404</p>
  <h1>That page is not<br>in the file.</h1>
  <p class="lede">The link is broken, the page was renamed, or it never existed. Nothing has gone
  wrong with your claim. Try one of these, or call {PHONE} and a person will point you at the
  right page.</p>
  <div class="btn-row">
    <a class="btn" href="/">Back to the homepage <span class="arw">&rarr;</span></a>
    <a class="btn btn--ghost" href="/sitemap/">Full sitemap</a>
  </div>
</div></section>
<section class="section band band--ruled"><div class="wrap">
  <p class="eyebrow">Popular destinations</p>
  {render_blocks([("links", links)])}
</div></section>
"""
    write("/404.html", page_shell(page, body))


# ===========================================================================
# Main
# ===========================================================================

def main():
    from content import builders   # imported late: it uses helpers defined here

    write("/", homepage())
    builders.build_all(globals())
    build_404()
    build_sitemap()
    build_robots()
    build_htaccess()
    build_manifest()
    build_favicon()
    build_touch_icon()

    total = len(all_pages()) + 1
    print(f"built {total} pages into {OUT}")


if __name__ == "__main__":
    main()
