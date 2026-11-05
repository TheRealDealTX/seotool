"""Shared page shell for sbarates.com, copied from the live templates.

Every generated page uses the same <head>, header, footer and rate data as the
pages already on the site, so new pages are indistinguishable from old ones.
"""
import html
import json
from urllib.parse import quote

SITE = "https://sbarates.com"
TODAY = "2026-11-05"
CSS_V = "c208366f"   # bumped by build.py when site.css changes
JS_V = "9a8dc950"

PRIME = 7.00
PRIME_DATE = "October 28, 2026"
VAR_CAPS = [("$50,000 or less", 50000, 6.5), ("$50,001 to $250,000", 250000, 6.0),
            ("$250,001 to $350,000", 350000, 4.5), ("Over $350,000", 5000000, 3.0)]
FIX_CAPS = [("$25,000 or less", 25000, 8.0), ("$25,001 to $50,000", 50000, 7.0),
            ("$50,001 to $250,000", 250000, 6.0), ("Over $250,000", 5000000, 5.0)]
RATE_504_25 = 6.97

SOURCES = ('<p class="src">Sources: <a href="https://www.sba.gov/partners/lenders/7a-loan-program/terms-conditions-eligibility" rel="nofollow">SBA 7(a) terms, conditions and maximum variable rates</a>; '
           '<a href="https://www.federalreserve.gov/releases/h15/" rel="nofollow">Federal Reserve H.15 selected interest rates (bank prime loan rate)</a>; '
           '<a href="https://somercor.com/october-2026-sba-504-interest-rates/" rel="nofollow">October 2026 SBA 504 debenture pricing, as published by CDCs</a>; '
           '<a href="https://data.sba.gov/dataset/7-a-504-foia" rel="nofollow">SBA FOIA 7(a) and 504 loan-level data</a>.</p>')


def e(s):
    """HTML-escape text the same way the original generator did."""
    return html.escape(str(s), quote=True)


def seg(name):
    """Encode a folder name for use in a URL path segment (matches live canonicals)."""
    return quote(name, safe="-._~")


def industry_path(folder):
    return f"/SBA-Loan/{seg(folder)}/"


def lender_path(slug):
    return f"/SBA-Loans/{slug}/"


def pct(x):
    return f"{x:.2f}%"


def cap_for(amount):
    for band, mx, sp in VAR_CAPS:
        if amount <= mx:
            return PRIME + sp
    return PRIME + VAR_CAPS[-1][2]


def payment(p, rate, years):
    r = rate / 100 / 12
    n = years * 12
    return p * r / (1 - (1 + r) ** -n)


def var_table():
    rows = "".join(f'<tr><td>{e(b)}</td><td class="r num">Prime + {s:.1f}</td><td class="r num"><strong>{pct(PRIME + s)}</strong></td></tr>'
                   for b, _, s in VAR_CAPS)
    return ('<div class="tbl-wrap"><table><thead><tr><th>Loan amount</th><th class="r">Maximum spread</th>'
            f'<th class="r">Maximum variable rate today</th></tr></thead><tbody>{rows}</tbody></table></div>')


ORG = {"@type": "Organization", "@id": f"{SITE}/#organization", "name": "SBARates.com", "url": f"{SITE}/",
       "logo": {"@type": "ImageObject", "url": f"{SITE}/icon-512.png", "width": 512, "height": 512},
       "description": "Independent reference for SBA loan rates and SBA lenders. Not a lender, broker or government agency."}
WEBSITE = {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": "SBARates.com", "inLanguage": "en-US",
           "publisher": {"@id": f"{SITE}/#organization"}}


def faq_node(url, faqs):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs],
            "@id": f"{url}#faq", "isPartOf": {"@id": f"{url}#webpage"}}


def faq_html(faqs):
    return "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faqs)


def page(path, title, desc, crumbs, main, extra_nodes=(), nav=None, about_id=None, robots=None, page_type="WebPage"):
    """crumbs: list of (name, path) ending with the current page."""
    url = SITE + path
    crumb_node = {"@type": "BreadcrumbList", "@id": f"{url}#breadcrumb",
                  "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(crumbs)]}
    wp = {"@type": page_type, "@id": f"{url}#webpage", "url": url, "name": title, "description": desc, "inLanguage": "en-US",
          "isPartOf": {"@id": f"{SITE}/#website"}, "publisher": {"@id": f"{SITE}/#organization"}, "dateModified": TODAY,
          "breadcrumb": {"@id": f"{url}#breadcrumb"}}
    if about_id:
        wp["about"] = {"@id": about_id}
    graph = {"@context": "https://schema.org", "@graph": [ORG, WEBSITE, wp, crumb_node, *extra_nodes]}
    t, d = e(title), e(desc)
    navs = [("/sba-loan-rates/", "7(a) rates"), ("/sba-504-loan-rates/", "504 rates"), ("/sba-loan-calculator/", "Calculator"),
            ("/SBA-Loans/", "Lenders"), ("/SBA-Loan/", "Industries"), ("/pages/top-sba-lenders-in-2025/", "Top lenders")]
    nav_html = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == nav else ""}>{n}</a>' for h, n in navs)
    robots_tag = f'<meta name="robots" content="{robots}">\n' if robots else ""
    rates_js = json.dumps({"prime": PRIME,
                           "variable_caps": [{"band": b, "max": m, "spread": s} for b, m, s in VAR_CAPS],
                           "fixed_caps": [{"band": b, "max": m, "spread": s} for b, m, s in FIX_CAPS]})
    return f"""<!doctype html>
<html lang="en"><head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-7LRVD5GNK6"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', 'G-7LRVD5GNK6');
</script>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
{robots_tag}<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:title" content="{t}"><meta property="og:description" content="{d}"><meta property="og:url" content="{url}"><meta property="og:site_name" content="SBARates.com"><meta property="og:locale" content="en_US">
<meta property="og:image" content="https://sbarates.com/assets/og-image.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:type" content="image/png"><meta property="og:image:alt" content="SBARates.com: SBA loan rates today">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{t}"><meta name="twitter:description" content="{d}"><meta name="twitter:image" content="https://sbarates.com/assets/og-image.png"><meta name="twitter:image:alt" content="SBARates.com: SBA loan rates today">
<meta name="theme-color" content="#0B1F3A">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v={CSS_V}">
<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False)}</script>
</head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head"><div class="wrap">
<a class="brand" href="/"><svg class="mark" viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8"/><path d="M8 23h4v-8H8zm6 0h4V11h-4zm6 0h4V7h-4z"/></svg><span class="bt">SBA<b>Rates</b>.com</span></a>
<nav class="nav" aria-label="Main">{nav_html}</nav>
<span class="prime-chip"><i class="dot" aria-hidden="true"></i>Prime <strong class="num">{PRIME:.2f}%</strong><span class="upd"> · updated {PRIME_DATE}</span></span>
</div></header>
<main id="main">{main}</main>
<footer class="site-foot"><div class="wrap foot-grid">
<div><p><strong>SBARates.com</strong> tracks the SBA's maximum loan rates and public SBA lending data so you can compare lenders before you apply. We're not a lender or a government site, and nothing here is a loan offer.</p><p>Rates last checked {PRIME_DATE}. Lenders set your actual rate below the SBA maximum.</p></div>
<div><strong>Rates</strong><br><a href="/sba-loan-rates/">SBA 7(a) rates</a><br><a href="/sba-504-loan-rates/">SBA 504 rates</a><br><a href="/sba-loan-calculator/">Payment calculator</a></div>
<div><strong>Research</strong><br><a href="/SBA-Loans/">Lender directory</a><br><a href="/SBA-Loan/">Industries</a><br><a href="/blog/Small%20Business%20Administration/">What is the SBA?</a><br><a href="/about/">About &amp; sources</a></div>
</div></footer>
<script>window.SBA_RATES={rates_js};</script>
<script src="/assets/site.js?v={JS_V}" defer></script>
</body></html>"""


def cta(source, state=None, industry=None, amount=None):
    """The lender-match call to action that goes on every directory page."""
    q = [f"from={quote(source, safe='')}"]
    if state:
        q.append(f"state={state}")
    if industry:
        q.append(f"industry={quote(industry, safe='')}")
    if amount:
        q.append(f"amount={amount}")
    href = "/get-matched/?" + "&amp;".join(q)
    return (f'<!--cta--><section class="match" aria-labelledby="match-h"><div class="match-txt"><p class="match-k">Free · takes 1 minute · no credit check</p>'
            f'<h2 id="match-h">Get matched with an SBA lender</h2>'
            f'<p>Answer four questions and see SBA lenders that fit your state, loan size and industry, with your maximum rate. '
            f'Compare at least two quotes before you sign. Rates move monthly: check <a href="/">current SBA loan rates</a> and the <a href="/sba-504-loan-rates/">504 rate</a>.</p></div>'
            f'<a class="btn-match" href="{href}" data-cta="{e(source)}">Find my SBA lender</a></section><!--/cta-->')
