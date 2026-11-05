#!/usr/bin/env python3
"""Generate the rebuilt sbarates.com pages and refresh shared parts of the site.

    python3 _build/build.py

What it does, in order:
  1. Renders lender pages from _build/content/lenders_*.json
  2. Renders industry pages from _build/content/industries_*.json
  3. Renders the blog posts in _build/content/blog.json and /get-matched/
  4. Rebuilds the lender and industry hub lists and the sitemaps
  5. Injects the lender-match CTA into every directory page and refreshes
     "Other SBA lenders in <state>" lists, bumping the CSS version everywhere

Only the Python standard library is used. Output is written into the repo root
(the web root). The _build folder itself is blocked from the web in .htaccess.
"""
import glob
import hashlib
import html
import json
import os
import re
import sys
from urllib.parse import unquote

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import shell  # noqa: E402
from shell import e, page, cta, var_table, industry_path, lender_path, SITE, PRIME, pct, cap_for, payment, SOURCES, faq_html, faq_node  # noqa: E402

STATES = {"AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", "CO": "Colorado", "CT": "Connecticut",
          "DE": "Delaware", "DC": "District of Columbia", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois",
          "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
          "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri", "MT": "Montana",
          "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
          "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania",
          "PR": "Puerto Rico", "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas",
          "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming"}
ST_BY_NAME = {v: k for k, v in STATES.items()}

# real headquarters for lenders listed under another state in SBA data
HQ_STATE = {"banc-of-california-co": "California", "lake-michigan-cu-fl": "Michigan", "centennial-bank-fl": "Arkansas"}

NATIONAL = [("live-oak-banking-company-nc", "Live Oak Bank"), ("the-huntington-national-bank-oh", "Huntington Bank"),
            ("newtek-bank-national-association-fl", "Newtek Bank"), ("wells-fargo-bank-national-association-sd", "Wells Fargo")]

PROGRAM_TEXT = {
    "7(a)": "The SBA's main loan, up to $5 million, for working capital, equipment, buying a business, refinancing and real estate.",
    "504": "Long-term fixed-rate financing for owner-occupied real estate and heavy equipment. The bank funds about 50%, a CDC up to 40%, and you put in about 10%.",
    "SBA Express": "A 7(a) loan up to $500,000 that the lender approves under its own authority, so it closes faster. The rate cap is the same as standard 7(a).",
    "Microloan": "Loans up to $50,000 through nonprofit intermediaries, usually with free coaching. Good for start-ups and very small businesses.",
    "Community Advantage": "Mission-based 7(a) lending for borrowers that banks often turn down: newer businesses, thin credit files and underserved communities.",
}


def write(path, text):
    full = os.path.join(ROOT, unquote(path).lstrip("/"))
    if full.endswith("/"):
        full += "index.html"
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)


def load(pattern):
    out = []
    for p in sorted(glob.glob(os.path.join(HERE, "content", pattern))):
        with open(p, encoding="utf-8") as f:
            out.extend(json.load(f))
    return out


def title_with_site(t):
    full = f"{t} | SBARates.com"
    return full if len(full) <= 60 else t


# ---------------------------------------------------------------- inventory
def existing_lenders():
    """Lenders already on the hub page: path -> dict(name, type, st, data)."""
    t = open(os.path.join(ROOT, "SBA-Loans/index.html"), encoding="utf-8").read()
    out = {}
    for sec in re.findall(r"<section data-state-group><h3>(.*?)</h3>(.*?)</section>", t, re.S):
        state = html.unescape(sec[0])
        for dn, href, name, typ in re.findall(r'<li data-name="([^"]*)"><a href="([^"]+)">(.*?)</a> <small>(.*?)</small></li>', sec[1]):
            out[href] = {"name": html.unescape(name), "type": html.unescape(typ), "state": state, "st": ST_BY_NAME.get(state, ""),
                         "data": html.unescape(dn)}
    return out


def existing_industries():
    t = open(os.path.join(ROOT, "SBA-Loan/index.html"), encoding="utf-8").read()
    out = {}
    for href, label, small in re.findall(r'<li><a href="(/SBA-Loan/[^"]+)">(.*?)</a> <small>(.*?)</small></li>', t):
        out[href] = {"short": html.unescape(label), "small": html.unescape(small).rstrip(")")}
    return out


def slug_state(slug):
    st = slug.rsplit("-", 1)[-1].upper()
    return st if st in STATES else None


# ---------------------------------------------------------------- lenders
def render_lender(L, lenders_inv):
    slug = L["slug"]
    path = lender_path(slug)
    url = SITE + path
    st = slug_state(slug) or L["st"]
    state = STATES[st]
    name = L["name"]
    title = title_with_site(L["title"])
    desc = L["description"]
    faqs = [(f["q"], f["a"]) for f in L["faqs"]]
    faqs.append((f"What rate will I get on an SBA loan from {name}?",
                 f"{name} sets your rate at or below the SBA maximum. With prime at {PRIME:.2f}%, variable 7(a) caps run from "
                 f"{pct(PRIME + 3)} on loans over $350,000 to {pct(PRIME + 6.5)} on loans of $50,000 or less. Your rate depends on loan size, term, collateral, credit and cash flow."))

    others = [(p, d["name"]) for p, d in sorted(lenders_inv.items(), key=lambda x: x[1]["name"]) if d["st"] == st and p != path]
    if others:
        aside_list = f"<h2>Other SBA lenders in {e(state)}</h2><ul>" + "".join(f'<li><a href="{p}">{e(n)}</a></li>' for p, n in others[:8]) + "</ul>"
    else:
        aside_list = "<h2>SBA lenders that lend nationwide</h2><ul>" + "".join(f'<li><a href="{lender_path(s)}">{e(n)}</a></li>' for s, n in NATIONAL) + "</ul>"

    progs = [p for p in L.get("programs", []) if p in PROGRAM_TEXT] or ["7(a)"]
    prog_html = "".join(f"<li><strong>{e(p)}.</strong> {e(PROGRAM_TEXT[p])}</li>" for p in progs)
    former = L.get("former_names") or []
    former_html = f'<p class="src">Formerly known as {e(", ".join(former))}.</p>' if former else ""
    about = "".join(f"<p>{e(p)}</p>" for p in L["about"])
    known = "".join(f"<li>{e(k)}</li>" for k in L["known_for"])

    main = (f'<div class="band"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="/SBA-Loans/">SBA lenders</a> / {e(name)}</nav>'
            f'<h1>{e(L["h1"])}</h1>\n<p class="lede">{e(L["lede"])}</p></div></div><div class="wrap body"><div class="cols"><div>\n'
            f'{about}{former_html}\n'
            f'<h2>What {e(name)} is known for</h2><ul>{known}</ul>\n'
            f'<h2>How business owners use SBA loans here</h2><p>{e(L["sba_fit"])}</p>\n'
            f'<h2>SBA programs to ask {e(name)} about</h2><ul>{prog_html}</ul><p>Program availability changes. Ask the lender which SBA programs it closes most often and whether it has SBA Preferred Lender status, which lets it approve loans in-house.</p>\n'
            f'<h2>Maximum SBA rates at {e(name)}</h2><p>Every SBA lender has to stay at or below the SBA\'s caps, which are tied to the prime rate ({PRIME:.2f}%). '
            f'A loan over $350,000 can\'t carry a variable rate above {pct(PRIME + 3)}.</p>{var_table()}'
            f'<p>Ask {e(name)} for its spread over prime. Two lenders can both be under the cap and still be a full point apart. See <a href="/">today\'s SBA loan rates</a> for fixed-rate caps and the <a href="/sba-504-loan-rates/">SBA 504 rate</a>.</p>\n'
            + cta(f"lender:{slug}", state=st) +
            f'<h2>Before you apply</h2><ol class="steps"><li>Ask whether {e(name)} is an SBA Preferred Lender and how many SBA loans it closed last year in your industry.</li>'
            f'<li>Request the spread over prime, the fixed-rate option and every fee in writing.</li>'
            f'<li>Get at least one more quote. Our <a href="/SBA-Loans/">SBA lenders list</a> shows other lenders in {e(state)}, and the <a href="/sba-loan-calculator/">payment calculator</a> shows what a quarter point costs you.</li></ol>\n'
            f'<h2>Questions</h2>{faq_html(faqs)}\n'
            f'</div><aside class="aside"><h2>Today\'s SBA rates</h2><p class="num">Prime {PRIME:.2f}%<br>7(a) variable caps {pct(PRIME + 3)}–{pct(PRIME + 6.5)}<br>504, 25-year {pct(shell.RATE_504_25)}</p>'
            f'<p><a href="/sba-loan-calculator/">Payment calculator</a></p>'
            f'<a class="btn-match" href="/get-matched/?from=lender-aside&amp;state={st}">Compare SBA lenders</a>\n'
            f'{aside_list}</aside></div>{SOURCES}</div>')

    ltype = L.get("type", "bank")
    lender_node = {"@type": "BankOrCreditUnion" if ltype in ("bank", "credit union") else "FinancialService",
                   "@id": f"{url}#lender", "name": L.get("legal") or name, "alternateName": [name] + former,
                   "areaServed": {"@type": "State", "name": state}, "description": L["about"][0][:300],
                   "address": {"@type": "PostalAddress", "addressLocality": L.get("city", ""), "addressRegion": HQ_STATE.get(slug, L.get("state", state)), "addressCountry": "US"}}
    crumbs = [("Home", "/"), ("SBA lenders", "/SBA-Loans/"), (name, path)]
    write(path, page(path, title, desc, crumbs, main, extra_nodes=[faq_node(url, faqs), lender_node], nav="/SBA-Loans/", about_id=f"{url}#lender"))
    return path, {"name": name, "type": ltype, "state": state, "st": st,
                  "data": f'{(L.get("legal") or name).lower()} {name.lower()} {L.get("city", "").lower()}, {HQ_STATE.get(slug, L.get("state", state)).lower()}'}


# ---------------------------------------------------------------- industries
def render_industry(I, ind_inv):
    folder = I["folder"]
    path = industry_path(folder)
    url = SITE + path
    short = I["short"]
    title = title_with_site(I["title"])
    faqs = [(f["q"], f["a"]) for f in I["faqs"]]
    amt = int(I.get("example_amount") or 150000)
    yrs = int(I.get("example_years") or 10)
    rate = cap_for(amt)
    pay = payment(amt, rate, yrs)
    naics = I.get("naics") or ""
    lede = f'{e(folder)}{" · NAICS " + e(naics) if naics else ""} · Program that usually fits: {e(I["program"])}'
    progs = "".join(f'<h3>{e(p["h"])}</h3><p>{e(p["p"])}</p>' for p in I["programs"])
    uses = "".join(f"<li>{e(u)}</li>" for u in I["uses"])
    rel = []
    for r in I.get("related", []):
        rp = industry_path(r)
        if rp in ind_inv and rp != path:
            rel.append(f'<li><a href="{rp}">{e(ind_inv[rp]["short"])}</a></li>')
    risks = I.get("risks") or {}
    risks_html = f'<h2>{e(risks["h"])}</h2><p>{e(risks["p"])}</p>\n' if risks.get("h") else ""

    main = (f'<div class="band"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="/SBA-Loan/">Industries</a> / {e(short)}</nav>'
            f'<h1>{e(I["h1"])}</h1>\n<p class="lede">{lede}</p></div></div><div class="wrap body">\n'
            f'<p class="note">{e(I["note"])}</p>\n'
            f'<h2>Who qualifies</h2><p>{e(I["who"])}</p>\n'
            f'<h2>Which SBA program fits</h2>{progs}\n'
            f'<h2>What borrowers use the money for</h2><ul>{uses}</ul>\n'
            f'<h2>Typical loan amounts, down payment and terms</h2><p>{e(I["amounts"])}</p>\n'
            f'{risks_html}'
            f'<h2>Example: a ${amt:,} loan</h2><p>At today\'s maximum variable 7(a) rate of {pct(rate)} over {yrs} years, the payment would be about '
            f'<strong class="num">${pay:,.0f}</strong> a month. Most well-qualified borrowers get a lower rate. <a href="/sba-loan-calculator/">Try your own numbers</a>.</p>\n'
            + cta(f"industry:{folder}", industry=folder, amount=amt) +
            f'<h2>Today\'s rate caps</h2><p>These are the SBA\'s maximum 7(a) rates with prime at {PRIME:.2f}%. See <a href="/">current SBA loan rates</a> and '
            f'<a href="/sba-504-loan-rates/">SBA 504 rates</a> for the full picture.</p>{var_table()}\n'
            f'<h2>Related industries and lenders</h2><div class="cols"><div><h3>Related industries</h3><ul>{"".join(rel)}</ul><p><a href="/SBA-Loan/">All industries</a></p></div>'
            f'<div><h3>SBA lenders active nationwide</h3><ul>' + "".join(f'<li><a href="{lender_path(s)}">{e(n)}</a></li>' for s, n in NATIONAL) +
            f'</ul><p><a href="/SBA-Loans/">All SBA lenders by state</a> · <a href="/pages/top-sba-lenders-in-2025/">Top SBA lenders by volume</a></p></div></div>\n'
            f'<h2>Questions about {e(short.lower())} loans</h2>{faq_html(faqs)}{SOURCES}</div>')
    crumbs = [("Home", "/"), ("Industries", "/SBA-Loan/"), (short, path)]
    write(path, page(path, title, I["description"], crumbs, main, extra_nodes=[faq_node(url, faqs)], nav="/SBA-Loan/"))
    return path, {"short": short, "small": f"NAICS {naics}" if naics else folder}


# ---------------------------------------------------------------- blog
def render_blog(B):
    path = B["path"]
    url = SITE + path
    faqs = [(f["q"], f["a"]) for f in B.get("faqs", [])]
    main = (f'<div class="band"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="/blog/Small%20Business%20Administration/">SBA guides</a> / {e(B["crumb"])}</nav>'
            f'<h1>{e(B["h1"])}</h1>\n<p class="lede">{e(B["lede"])}</p></div></div><div class="wrap body">\n{B["body"]}\n'
            + cta(f"blog:{B['crumb']}") +
            (f'<h2>Questions</h2>{faq_html(faqs)}' if faqs else "") + f'{SOURCES}</div>')
    art = {"@type": "Article", "@id": f"{url}#article", "headline": B["h1"], "datePublished": shell.TODAY, "dateModified": shell.TODAY,
           "author": {"@id": f"{SITE}/#organization"}, "publisher": {"@id": f"{SITE}/#organization"}, "mainEntityOfPage": {"@id": f"{url}#webpage"},
           "image": f"{SITE}/assets/og-image.png"}
    nodes = [art] + ([faq_node(url, faqs)] if faqs else [])
    crumbs = [("Home", "/"), ("SBA guides", "/blog/Small%20Business%20Administration/"), (B["crumb"], path)]
    write(path, page(path, B["title"], B["description"], crumbs, main, extra_nodes=nodes))


# ---------------------------------------------------------------- get matched
def render_get_matched(lenders_inv, ind_inv):
    path = "/get-matched/"
    data = sorted([[d["name"], p, d["st"], d["type"]] for p, d in lenders_inv.items()], key=lambda x: x[0])
    inds = sorted(((d["short"], p) for p, d in ind_inv.items()), key=lambda x: x[0])
    st_opts = "".join(f'<option value="{k}">{e(v)}</option>' for k, v in sorted(STATES.items(), key=lambda x: x[1]))
    ind_opts = "".join(f'<option value="{e(p)}">{e(n)}</option>' for n, p in inds)
    faqs = [("Does it cost anything to get matched?", "No. This tool is free and doesn't ask for your name, Social Security number or credit. It shows lenders from our directory and points you to the SBA's own free Lender Match service, where participating lenders contact you."),
            ("Will getting matched affect my credit score?", "Not here. We don't collect personal data or pull credit. A lender will usually do a credit check once you formally apply, and some start with a soft pull that doesn't affect your score. Ask before you authorize it."),
            ("How many lenders should I talk to?", "At least two, ideally three. SBA rates are capped, but lenders still price differently under the cap, and fees, collateral requirements and speed vary a lot. A one-point difference on a $500,000 loan is roughly $250 a month."),
            ("What do I need before I apply for an SBA loan?", "Two to three years of business and personal tax returns, year-to-date financials, a debt schedule, a personal financial statement (SBA Form 413), and for start-ups or acquisitions a business plan with projections. See our SBA loan documentation checklist.")]
    main = ('<div class="band"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / Get matched</nav>'
            '<h1>Get matched with an SBA lender</h1>\n<p class="lede">Four questions. You\'ll see your maximum SBA rate, the program that fits, and SBA lenders for your state and industry. Free, no sign-up, no credit check.</p></div></div>'
            '<div class="wrap body">\n'
            '<form class="calc gm" id="gm" novalidate>'
            f'<div><label for="gm-state">State</label><select id="gm-state" required><option value="">Choose a state</option>{st_opts}</select></div>'
            '<div><label for="gm-amt">Loan amount</label><select id="gm-amt"><option value="40000">Under $50,000</option><option value="150000" selected>$50,000 to $250,000</option><option value="300000">$250,000 to $350,000</option><option value="750000">$350,000 to $1 million</option><option value="2500000">$1 million to $5 million</option><option value="6000000">Over $5 million</option></select></div>'
            '<div><label for="gm-use">What is it for?</label><select id="gm-use"><option value="wc">Working capital or inventory</option><option value="equip">Equipment or vehicles</option><option value="buy">Buying a business or franchise</option><option value="re">Buying or building property</option><option value="refi">Refinancing debt</option><option value="start">Starting a new business</option></select></div>'
            f'<div><label for="gm-ind">Industry</label><select id="gm-ind"><option value="">Other / not listed</option>{ind_opts}</select></div>'
            '<div class="full"><button type="submit" class="btn-match">Show my SBA lender matches</button></div></form>\n'
            '<div class="gm-out" id="gm-out" aria-live="polite"></div>\n'
            '<h2>How this works</h2><p>SBA loans are made by private lenders: banks, credit unions, CDCs and nonprofit microlenders. The SBA guarantees part of the loan and caps the rate, but each lender decides whether to approve you and what to charge under the cap. Matching is about finding lenders that actually close loans like yours: the right size, the right program and, ideally, your industry.</p>'
            '<ol class="steps"><li><strong>Pick the program.</strong> Under $50,000 often means a microloan or a small 7(a). Property and heavy equipment usually fit the fixed-rate 504. Most other needs are 7(a).</li>'
            '<li><strong>Shortlist lenders.</strong> Start with lenders in your state from our <a href="/SBA-Loans/">SBA lenders list</a>, plus a high-volume national SBA lender.</li>'
            '<li><strong>Use SBA Lender Match.</strong> The SBA\'s free referral tool sends your request to participating lenders, who contact you within a few days if interested.</li>'
            '<li><strong>Compare quotes.</strong> Ask each lender for the spread over prime, fees, collateral and timeline in writing.</li></ol>\n'
            f'<h2>Questions</h2>{faq_html(faqs)}{SOURCES}</div>'
            f'<script>window.SBA_LENDERS={json.dumps(data, ensure_ascii=False)};'
            f'window.SBA_NATIONAL={json.dumps([[n, lender_path(s)] for s, n in NATIONAL])};'
            f'window.SBA_STATES={json.dumps(STATES)};</script>'
            '<script src="/assets/match.js?v=MATCHV" defer></script>')
    url = SITE + path
    crumbs = [("Home", "/"), ("Get matched", path)]
    write(path, page(path, "Get Matched With an SBA Lender (Free) | SBARates.com",
                     "Find SBA lenders that fit your state, loan size and industry. See your maximum SBA rate and the program that fits. Free, no sign-up, no credit check.",
                     crumbs, main, extra_nodes=[faq_node(url, faqs)]))


# ---------------------------------------------------------------- hubs
def rebuild_lender_hub(inv):
    p = os.path.join(ROOT, "SBA-Loans/index.html")
    t = open(p, encoding="utf-8").read()
    groups = {}
    for href, d in inv.items():
        groups.setdefault(d["state"], []).append((d["name"], href, d))
    secs = []
    for state in sorted(groups):
        items = "".join(f'<li data-name="{e(d["data"])}"><a href="{href}">{e(n)}</a> <small>{e(d["type"])}</small></li>'
                        for n, href, d in sorted(groups[state], key=lambda x: x[0].lower()))
        secs.append(f'<section data-state-group><h3>{e(state)}</h3><ul class="link-grid">{items}</ul></section>')
    a = t.find("<section data-state-group>")
    b = t.rfind("</section>") + len("</section>")
    t = t[:a] + "".join(secs) + t[b:]
    n = len(inv)
    t = re.sub(r"A list of \d+ SBA-approved", f"A list of {n} SBA-approved", t)
    t = re.sub(r'(<span id="lender-count" class="src">)\d+ lenders', rf"\g<1>{n} lenders", t)
    t = re.sub(r"(list of )\d+( SBA-approved)", rf"\g<1>{n}\2", t)
    open(p, "w", encoding="utf-8").write(t)


def rebuild_industry_hub(inv):
    p = os.path.join(ROOT, "SBA-Loan/index.html")
    t = open(p, encoding="utf-8").read()
    items = "".join(f'<li><a href="{href}">{e(d["short"])}</a> <small>{e(d["small"])}</small></li>'
                    for href, d in sorted(inv.items(), key=lambda x: x[1]["short"].lower()))
    t = re.sub(r'<ul class="link-grid">.*?</ul>', lambda m: f'<ul class="link-grid">{items}</ul>', t, count=1, flags=re.S)
    t = re.sub(r"SBA loans for \d+ industries", f"SBA loans for {len(inv)} industries", t)
    open(p, "w", encoding="utf-8").write(t)


# ---------------------------------------------------------------- site-wide injection
def inject_everywhere(lenders_inv, css_v, js_v):
    files = [f for f in glob.glob(os.path.join(ROOT, "**/index.html"), recursive=True) if "/_build/" not in f and "/.git/" not in f]
    files.append(os.path.join(ROOT, "404.html"))
    for f in files:
        t = open(f, encoding="utf-8").read()
        rel = "/" + os.path.relpath(os.path.dirname(f), ROOT).replace(os.sep, "/") + "/"
        rel = rel.replace("/./", "/")
        t = re.sub(r"/assets/site\.css\?v=[0-9a-f]+", f"/assets/site.css?v={css_v}", t)
        t = re.sub(r"/assets/site\.js\?v=[0-9a-f]+", f"/assets/site.js?v={js_v}", t)
        if f.endswith("404.html") or rel.startswith("/get-matched/"):
            open(f, "w", encoding="utf-8").write(t)
            continue
        has_cta = "<!--cta-->" in t
        if not has_cta:
            block = None
            if rel.startswith(("/SBA-Loans/", "/listings/")) and rel.count("/") == 3:
                slug = rel.strip("/").split("/")[1]
                st = slug_state(slug) or ""
                block = cta(f"lender:{slug}", state=st or None)
                anchors = ["<h2>Before you apply</h2>", "<h2>Questions</h2>", '<p class="src">']
            elif rel.startswith("/SBA-Loan/") and rel.count("/") == 3:
                folder = html.unescape(rel.strip("/").split("/", 1)[1])
                block = cta(f"industry:{folder}", industry=folder)
                anchors = ["<h2>Today's rate caps</h2>", "<h2>Related industries", '<p class="src">']
            elif rel == "/":
                block = cta("home")
                anchors = ["<h2>Find an SBA lender</h2>"]
            elif rel in ("/sba-loan-rates/", "/sba-504-loan-rates/", "/sba-loan-calculator/"):
                block = cta(rel.strip("/"))
                anchors = ["<h2>Questions</h2>", '<p class="src">']
            else:
                block = cta(rel.strip("/") or "page")
                anchors = ['<p class="src">', "</div></main>"]
            for a in anchors:
                i = t.find(a)
                if i != -1:
                    t = t[:i] + block + t[i:]
                    break
            else:
                print("no CTA anchor:", rel)
        # lender pages with an aside: add a compare button and refresh same-state list
        if rel.startswith(("/SBA-Loans/", "/listings/")) and rel.count("/") == 3:
            slug = rel.strip("/").split("/")[1]
            st = slug_state(slug)
            if '<aside class="aside">' in t and "btn-match" not in t.split('<aside class="aside">', 1)[1]:
                t = t.replace('<p><a href="/sba-loan-calculator/">Payment calculator</a></p>',
                              f'<p><a href="/sba-loan-calculator/">Payment calculator</a></p><a class="btn-match" href="/get-matched/?from=lender-aside{"&amp;state=" + st if st else ""}">Compare SBA lenders</a>', 1)
            m = re.search(r"<h2>Other SBA lenders in ([^<]+)</h2><ul>.*?</ul>", t)
            if m and st:
                others = [(p, d["name"]) for p, d in sorted(lenders_inv.items(), key=lambda x: x[1]["name"]) if d["st"] == st and p != rel]
                if others:
                    new = f"<h2>Other SBA lenders in {m.group(1)}</h2><ul>" + "".join(f'<li><a href="{p}">{e(n)}</a></li>' for p, n in others[:8]) + "</ul>"
                    t = t[:m.start()] + new + t[m.end():]
        open(f, "w", encoding="utf-8").write(t)


# ---------------------------------------------------------------- sitemaps
def sitemaps():
    def urls(prefixes):
        out = []
        for f in sorted(glob.glob(os.path.join(ROOT, "**/index.html"), recursive=True)):
            if "/_build/" in f or "/.git/" in f:
                continue
            rel = "/" + os.path.relpath(os.path.dirname(f), ROOT).replace(os.sep, "/") + "/"
            rel = rel.replace("/./", "/")
            if any(rel.startswith(p) for p in prefixes[0]) and not any(rel.startswith(p) for p in prefixes[1]):
                out.append(SITE + "/".join(shell.seg(s) for s in rel.split("/")))
        return out
    groups = {
        "pages": urls(([""], ["/SBA-Loans/", "/SBA-Loan/", "/listings/", "/blog/"])) + [SITE + "/SBA-Loans/", SITE + "/SBA-Loan/"],
        "lenders": [u for u in urls((["/SBA-Loans/", "/listings/"], [])) if u not in (SITE + "/SBA-Loans/",)],
        "industries": [u for u in urls((["/SBA-Loan/"], [])) if u != SITE + "/SBA-Loan/"],
        "blog": urls((["/blog/"], [])),
    }
    for name, us in groups.items():
        body = "".join(f"<url><loc>{html.escape(u)}</loc><lastmod>{shell.TODAY}</lastmod></url>" for u in sorted(set(us)))
        open(os.path.join(ROOT, f"sitemap-{name}.xml"), "w").write(
            f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{body}</urlset>')
        print(f"sitemap-{name}.xml: {len(set(us))} urls")
    idx = "".join(f"<sitemap><loc>{SITE}/sitemap-{n}.xml</loc><lastmod>{shell.TODAY}</lastmod></sitemap>" for n in groups)
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?><sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{idx}</sitemapindex>')


def short_hash(path):
    return hashlib.md5(open(os.path.join(ROOT, path), "rb").read()).hexdigest()[:8]


def main():
    css_v, js_v = short_hash("assets/site.css"), short_hash("assets/site.js")
    shell.CSS_V, shell.JS_V = css_v, js_v

    lenders_inv = existing_lenders()
    ind_inv = existing_industries()
    lenders = load("lenders_*.json")
    industries = load("industries_*.json")

    # register new pages first so cross-links resolve
    for L in lenders:
        st = slug_state(L["slug"]) or L["st"]
        lenders_inv[lender_path(L["slug"])] = {"name": L["name"], "type": L.get("type", "bank"), "state": STATES[st], "st": st, "data": ""}
    for I in industries:
        ind_inv[industry_path(I["folder"])] = {"short": I["short"], "small": ""}
    for L in lenders:
        p, d = render_lender(L, lenders_inv)
        lenders_inv[p] = d
    for I in industries:
        p, d = render_industry(I, ind_inv)
        ind_inv[p] = d
    for B in load("blog.json"):
        render_blog(B)
    render_get_matched(lenders_inv, ind_inv)
    mv = short_hash("assets/match.js")
    gm = os.path.join(ROOT, "get-matched/index.html")
    txt = open(gm).read().replace("MATCHV", mv)
    open(gm, "w").write(txt)

    rebuild_lender_hub(lenders_inv)
    rebuild_industry_hub(ind_inv)
    inject_everywhere(lenders_inv, css_v, js_v)
    sitemaps()
    print(f"{len(lenders)} lender pages, {len(industries)} industry pages; hub: {len(lenders_inv)} lenders, {len(ind_inv)} industries")


if __name__ == "__main__":
    main()
