"""Shared layout, UI components and JSON-LD builders.

Content modules build page dicts with these helpers; build.py renders them
through `render_page()`.
"""

import html
import json

from siteconfig import BIZ, CITIES, NAV, RESOURCES, SERVICES, TODAY, TOOLS

ORIGIN = BIZ["origin"]
ORG_ID = ORIGIN + "/#organization"
SITE_ID = ORIGIN + "/#website"
ASSET_VER = "20261105"

esc = html.escape


def url(path):
    return ORIGIN + path


# --------------------------------------------------------------------------
# Icons (Lucide-style outline paths, 24x24, stroke=currentColor)
# --------------------------------------------------------------------------
ICONS = {
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "home": '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
    "building": '<rect width="16" height="20" x="4" y="2" rx="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01M16 6h.01M12 6h.01M12 10h.01M12 14h.01M16 10h.01M16 14h.01M8 10h.01M8 14h.01"/>',
    "calculator": '<rect width="16" height="20" x="4" y="2" rx="2"/><path d="M8 6h8M16 14v4M16 10h.01M12 10h.01M8 10h.01M12 14h.01M8 14h.01M12 18h.01M8 18h.01"/>',
    "file": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4M10 9H8M16 13H8M16 17H8"/>',
    "cube": '<path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5M12 22V12"/>',
    "hail": '<path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"/><path d="M16 14v2M8 14v2M16 20h.01M8 20h.01M12 16v2M12 22h.01"/>',
    "storm": '<path d="M6 16.326A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 .5 8.973"/><path d="m13 12-3 5h4l-3 5"/>',
    "wind": '<path d="M12.8 19.6A2 2 0 1 0 14 16H2M17.5 8a2.5 2.5 0 1 1 2 4H2M9.8 4.4A2 2 0 1 1 11 8H2"/>',
    "droplets": '<path d="M7 16.3c2.2 0 4-1.83 4-4.05 0-1.16-.57-2.26-1.71-3.19S7.29 6.75 7 5.3c-.29 1.45-1.14 2.84-2.29 3.76S3 11.1 3 12.25c0 2.22 1.8 4.05 4 4.05z"/><path d="M12.56 6.6A10.97 10.97 0 0 0 14 3.02c.5 2.5 2 4.9 4 6.5s3 3.5 3 5.5a6.98 6.98 0 0 1-11.91 4.97"/>',
    "flame": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "pin": '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
    "scale": '<path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1ZM2 16l3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10M12 3v18M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>',
    "ruler": '<path d="M21.3 15.3a2.4 2.4 0 0 1 0 3.4l-2.6 2.6a2.4 2.4 0 0 1-3.4 0L2.7 8.7a2.41 2.41 0 0 1 0-3.4l2.6-2.6a2.41 2.41 0 0 1 3.4 0Z"/><path d="m14.5 12.5 2-2M11.5 9.5l2-2M8.5 6.5l2-2M17.5 15.5l2-2"/>',
    "percent": '<path d="M19 5 5 19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
    "list": '<path d="m3 17 2 2 4-4M3 7l2 2 4-4M13 6h8M13 12h8M13 18h8"/>',
    "book": '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2zM22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
    "help": '<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3M12 17h.01"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "layers": '<path d="M12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83ZM2 12l8.58 3.91a2 2 0 0 0 1.66 0L21 12M2 17l8.58 3.91a2 2 0 0 0 1.66 0L21 17"/>',
    "compare": '<circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><path d="M13 6h3a2 2 0 0 1 2 2v7M11 18H8a2 2 0 0 1-2-2V9"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "chevron": '<path d="m6 9 6 6 6-6"/>',
    "umbrella": '<path d="M22 12a10.06 10.06 1 0 0-20 0Z"/><path d="M12 12v8a2 2 0 0 0 4 0M12 2v1"/>',
    "clipboard": '<rect width="8" height="4" x="8" y="2" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="m9 14 2 2 4-4"/>',
    "trending": '<path d="m22 17-8.5-8.5-5 5L2 7"/><path d="M16 17h6v-6"/>',
    "camera": '<path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "map": '<path d="M14.106 5.553a2 2 0 0 0 1.788 0l3.659-1.83A1 1 0 0 1 21 4.619v12.764a1 1 0 0 1-.553.894l-4.553 2.277a2 2 0 0 1-1.788 0l-4.212-2.106a2 2 0 0 0-1.788 0l-3.659 1.83A1 1 0 0 1 3 19.381V6.618a1 1 0 0 1 .553-.894l4.553-2.277a2 2 0 0 1 1.788 0z"/><path d="M15 5.764v15M9 3.236v15"/>',
    "alert": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4M12 17h.01"/>',
    "send": '<path d="M14.536 21.686a.5.5 0 0 0 .937-.024l6.5-19a.496.496 0 0 0-.635-.635l-19 6.5a.5.5 0 0 0-.024.937l7.93 3.18a2 2 0 0 1 1.112 1.11z"/><path d="m21.854 2.147-10.94 10.939"/>',
    "print": '<path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><path d="M6 9V3a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v6"/><rect x="6" y="14" width="12" height="8" rx="1"/>',
}


def icon(name, cls="ico", size=24):
    return (f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true">{ICONS[name]}</svg>')


# --------------------------------------------------------------------------
# Small building blocks
# --------------------------------------------------------------------------
def btn(label, href, kind="primary", ico="arrow", attrs=""):
    i = icon(ico, "ico ico-sm") if ico else ""
    return f'<a class="btn btn-{kind} magnetic" href="{href}"{attrs}><span>{label}</span>{i}</a>'


def call_btn(kind="primary", label=None):
    return btn(label or f"Call {BIZ['phone_short']}", f"tel:{BIZ['phone_href']}", kind, "phone")


def kicker(text):
    return f'<span class="kicker">{text}</span>'


def section_head(k, title, lead="", center=False, tag="h2"):
    c = " center" if center else ""
    lead_html = f'<p class="section-lead">{lead}</p>' if lead else ""
    return f'<div class="section-head{c} reveal">{kicker(k)}<{tag}>{title}</{tag}>{lead_html}</div>'


def checklist(items, cls="checklist"):
    lis = "".join(f"<li>{icon('check', 'ico ico-check')}<span>{i}</span></li>" for i in items)
    return f'<ul class="{cls}">{lis}</ul>'


def card(title, body, href=None, ico=None, tag="h3", link_label="Learn more", extra_cls=""):
    i = f'<span class="card-ico">{icon(ico)}</span>' if ico else ""
    link = (f'<span class="card-link">{link_label} {icon("arrow", "ico ico-sm")}</span>' if href else "")
    inner = f'{i}<{tag}>{title}</{tag}><p>{body}</p>{link}'
    if href:
        return f'<a class="card spot tilt reveal {extra_cls}" href="{href}">{inner}</a>'
    return f'<div class="card spot reveal {extra_cls}">{inner}</div>'


def grid(items, cols=3, cls=""):
    return f'<div class="grid grid-{cols} {cls}">{"".join(items)}</div>'


def callout(html_body, kind="info", title=None):
    t = f"<strong>{title}</strong>" if title else ""
    ico = {"info": "shield", "warn": "alert", "tip": "target"}[kind]
    return f'<aside class="callout callout-{kind}">{icon(ico)}<div>{t}{html_body}</div></aside>'


def figure(img, alt, caption=None, w=1600, h=1067, cls="", eager=False):
    src_small = img.replace(".webp", "-720.webp")
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return (f'<figure class="figure reveal {cls}"><img src="/assets/img/{img}" '
            f'srcset="/assets/img/{src_small} 720w, /assets/img/{img} {w}w" sizes="(max-width: 800px) 100vw, 800px" '
            f'width="{w}" height="{h}" alt="{esc(alt)}" {load} decoding="async">{cap}</figure>')


IMG = {  # name -> (file, width, height)
    "home": ("alabama-insurance-appraiser-home.webp", 1600, 1067),
    "roof": ("roof-water-damage-appraisal.webp", 1500, 1000),
    "commercial": ("commercial-property-appraisal-alabama.webp", 1000, 482),
    "residential": ("residential-property-claim-alabama.webp", 1200, 800),
    "flood": ("flood-water-damage-claim.webp", 1500, 1126),
    "storm": ("storm-damage-alabama-homes.webp", 1600, 1066),
    "inspect": ("insurance-appraiser-inspecting-roof.webp", 1000, 667),
}


def fig(key, alt, caption=None, cls="", eager=False):
    f, w, h = IMG[key]
    return figure(f, alt, caption, w, h, cls, eager)


def faq_html(faqs, open_first=True):
    out = []
    for n, (q, a) in enumerate(faqs):
        op = " open" if (open_first and n == 0) else ""
        out.append(f'<details class="faq-item reveal"{op}><summary><span>{q}</span>'
                   f'<span class="faq-toggle" aria-hidden="true"></span></summary>'
                   f'<div class="faq-a">{a}</div></details>')
    return f'<div class="faq">{"".join(out)}</div>'


def steps_html(steps):
    out = []
    for n, (t, b) in enumerate(steps, 1):
        out.append(f'<li class="step reveal"><span class="step-n">{n:02d}</span>'
                   f'<div><h3>{t}</h3><p>{b}</p></div></li>')
    return f'<ol class="steps">{"".join(out)}</ol>'


def table(head, rows, cls="table"):
    th = "".join(f"<th scope=\"col\">{h}</th>" for h in head)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="table-wrap reveal"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


def contact_form(compact=False):
    """Lead form. Posts to /api/contact.php; JS upgrades it to fetch()."""
    loss_opts = "".join(f"<option>{o}</option>" for o in
                        ["Hail", "Wind / Storm / Tornado", "Hurricane", "Water / Plumbing", "Fire / Smoke",
                         "Roof damage", "Commercial loss", "Other"])
    role_opts = "".join(f"<option>{o}</option>" for o in
                        ["Homeowner / policyholder", "Commercial property owner", "Property manager",
                         "Contractor", "Attorney", "Other claim professional"])
    city_opts = "".join(f"<option>{c}</option>" for c, _ in CITIES) + "<option>Other Alabama location</option>"
    return f'''<form class="lead-form{' compact' if compact else ''}" action="/api/contact.php" method="post" novalidate data-lead-form>
  <div class="form-grid">
    <label class="field"><span>Full name *</span><input type="text" name="name" autocomplete="name" required maxlength="100"></label>
    <label class="field"><span>Email *</span><input type="email" name="email" autocomplete="email" required maxlength="150"></label>
    <label class="field"><span>Phone *</span><input type="tel" name="phone" autocomplete="tel" required maxlength="20" placeholder="(205) 555-0123"></label>
    <label class="field"><span>I am a…</span><select name="role">{role_opts}</select></label>
    <label class="field"><span>Type of loss *</span><select name="loss_type" required><option value="">Select…</option>{loss_opts}</select></label>
    <label class="field"><span>Property location</span><select name="location"><option value="">Select…</option>{city_opts}</select></label>
    <label class="field field-full"><span>Tell us about the claim *</span><textarea name="message" rows="{3 if compact else 5}" required maxlength="4000" placeholder="Date of loss, property type, where the claim stands, approximate difference between estimates…"></textarea></label>
  </div>
  <div class="hp" aria-hidden="true"><label>Leave this empty<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
  <input type="hidden" name="ts" value="">
  <input type="hidden" name="page" value="">
  <label class="consent"><input type="checkbox" name="consent" value="1" required><span>I agree to be contacted about my claim. Submitting this form does not create an appraiser-client relationship. See the <a href="/privacy-policy/">Privacy Policy</a>.</span></label>
  <button class="btn btn-primary btn-lg magnetic" type="submit"><span>Send my claim details</span>{icon("send", "ico ico-sm")}</button>
  <p class="form-status" role="status" aria-live="polite"></p>
</form>'''


def cta_band(title="Talk to an Alabama Insurance Appraiser",
             text="Tell us about the property, the type of loss and the gap between estimates. We'll tell you plainly whether appraisal, an estimate review or documentation makes sense."):
    return f'''<section class="cta-band"><div class="container"><div class="cta-inner reveal">
  <div class="cta-glow" aria-hidden="true"></div>
  <div class="cta-copy">{kicker("Free claim conversation")}<h2>{title}</h2><p>{text}</p></div>
  <div class="cta-actions">{call_btn("light")}{btn("Send claim details", "/contact/", "ghost-light", "mail")}</div>
</div></div></section>'''


def related_links(title, links):
    lis = "".join(f'<li><a href="{h}">{t} {icon("arrow", "ico ico-sm")}</a></li>' for t, h in links)
    return f'<div class="related reveal"><h2 class="h4">{title}</h2><ul>{lis}</ul></div>'


# --------------------------------------------------------------------------
# Header / footer
# --------------------------------------------------------------------------
def _dropdown(key):
    if key == "services":
        items = [(f"/services/{s}/", n, b, i) for s, n, b, i in SERVICES]
        foot = ("/services/", "All appraisal services")
        cols = 2
    elif key == "areas":
        items = [(f"/service-areas/{s}/", c, "Insurance appraisal in " + c, "pin") for c, s in CITIES]
        foot = ("/service-areas/", "All Alabama service areas")
        cols = 3
    elif key == "tools":
        items = [(f"/tools/{s}/", n, b, i) for s, n, b, i in TOOLS]
        foot = ("/tools/", "All free claim tools")
        cols = 1
    else:
        items = list(RESOURCES)
        foot = ("/what-does-an-insurance-appraiser-do/", "What does an insurance appraiser do?")
        cols = 1
    lis = []
    for h, n, b, i in items:
        if key == "areas":
            lis.append(f'<li><a href="{h}">{icon("pin", "ico ico-sm")}<span>{n}</span></a></li>')
        else:
            lis.append(f'<li><a href="{h}"><span class="dd-ico">{icon(i, "ico ico-sm")}</span>'
                       f'<span><strong>{n}</strong><small>{b}</small></span></a></li>')
    return (f'<div class="dropdown dd-{key}"><ul class="dd-cols-{cols}">{"".join(lis)}</ul>'
            f'<a class="dd-foot" href="{foot[0]}">{foot[1]} {icon("arrow", "ico ico-sm")}</a></div>')


def header(active):
    links = []
    for label, href, dd in NAV:
        cur = ' aria-current="page"' if active == href else ""
        if dd:
            links.append(f'<li class="has-dd"><a href="{href}"{cur}>{label}</a>'
                         f'<button class="dd-btn" aria-expanded="false" aria-label="Open {label} menu">{icon("chevron", "ico ico-xs")}</button>'
                         f'{_dropdown(dd)}</li>')
        else:
            links.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"><span></span></div>
<div class="topbar"><div class="container topbar-inner">
  <p>{icon("shield", "ico ico-xs")} Independent property insurance appraisal &amp; estimating &mdash; statewide across Alabama</p>
  <div class="topbar-links"><a href="tel:{BIZ['phone_href']}">{icon("phone", "ico ico-xs")} {BIZ['phone_display']}</a><a href="mailto:{BIZ['email']}">{icon("mail", "ico ico-xs")} {BIZ['email']}</a></div>
</div></div>
<header class="site-header" data-header><div class="container header-inner">
  <a class="brand" href="/" aria-label="{BIZ['name']} home"><img src="/assets/img/alabama-insurance-appraiser-logo.webp" width="600" height="135" alt="{BIZ['name']} logo"></a>
  <nav class="main-nav" aria-label="Main" data-nav><ul>{"".join(links)}</ul>
    <div class="nav-mobile-cta">{call_btn()}</div></nav>
  <div class="header-cta">{btn("Call now", "tel:" + BIZ["phone_href"], "primary", "phone")}</div>
  <button class="nav-toggle" aria-label="Open menu" aria-expanded="false" data-nav-toggle>{icon("menu")}{icon("x")}</button>
</div></header>'''


def footer():
    svc = "".join(f'<li><a href="/services/{s}/">{n}</a></li>' for s, n, _, _ in SERVICES[:7])
    areas = "".join(f'<li><a href="/service-areas/{s}/">{c}</a></li>' for c, s in CITIES)
    tools = "".join(f'<li><a href="/tools/{s}/">{n}</a></li>' for s, n, _, _ in TOOLS)
    return f'''<footer class="site-footer">
<div class="footer-wave" aria-hidden="true"></div>
<div class="container footer-grid">
  <div class="footer-brand">
    <a href="/" class="brand"><img src="/assets/img/alabama-insurance-appraiser-logo-white.webp" width="600" height="133" alt="{BIZ['name']}" loading="lazy"></a>
    <p>Independent property insurance appraisal, Xactimate and Symbility estimating, and Matterport claim documentation for residential and commercial losses throughout Alabama.</p>
    <ul class="footer-contact">
      <li><a href="tel:{BIZ['phone_href']}">{icon("phone", "ico ico-sm")} {BIZ['phone_display']}</a></li>
      <li><a href="mailto:{BIZ['email']}">{icon("mail", "ico ico-sm")} {BIZ['email']}</a></li>
      <li>{icon("map", "ico ico-sm")} Serving all 67 Alabama counties</li>
    </ul>
  </div>
  <div><h2 class="footer-h">Services</h2><ul>{svc}<li><a href="/services/">All services &rarr;</a></li></ul></div>
  <div><h2 class="footer-h">Service Areas</h2><ul class="footer-cols">{areas}</ul></div>
  <div><h2 class="footer-h">Free Tools</h2><ul>{tools}</ul>
    <h2 class="footer-h">Company</h2><ul><li><a href="/about-us/">About Us</a></li><li><a href="/insurance-appraisal-process/">Appraisal Process</a></li><li><a href="/faq/">FAQ</a></li><li><a href="/glossary/">Glossary</a></li><li><a href="/blog/">Blog</a></li><li><a href="/contact/">Contact</a></li></ul></div>
</div>
<div class="container footer-legal">
  <p>&copy; {TODAY[:4]} {BIZ['name']}. All rights reserved. Information on this site is general and educational; it is not legal advice and does not interpret any specific insurance policy.</p>
  <ul><li><a href="/privacy-policy/">Privacy Policy</a></li><li><a href="/terms-of-use/">Terms of Use</a></li><li><a href="/disclaimer/">Disclaimer</a></li><li><a href="/sitemap/">Sitemap</a></li></ul>
</div>
</footer>
<a class="float-call" href="tel:{BIZ['phone_href']}" aria-label="Call {BIZ['name']}">{icon("phone")}</a>
<button class="to-top" aria-label="Back to top" data-to-top>{icon("chevron")}</button>'''


# --------------------------------------------------------------------------
# Page heroes
# --------------------------------------------------------------------------
def breadcrumbs_html(crumbs):
    parts = []
    for n, (name, href) in enumerate(crumbs):
        if n == len(crumbs) - 1:
            parts.append(f'<li aria-current="page">{name}</li>')
        else:
            parts.append(f'<li><a href="{href}">{name}</a></li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(parts)}</ol></nav>'


def inner_hero(page):
    img = IMG[page.get("hero_img", "storm")][0]
    lead = f'<p class="hero-lead">{page["lead"]}</p>' if page.get("lead") else ""
    k = kicker(page["kicker"]) if page.get("kicker") else ""
    meta = page.get("hero_meta", "")
    actions = page.get("hero_actions")
    if actions is None:
        actions = f'<div class="hero-actions">{call_btn()}{btn("Send claim details", "/contact/", "ghost-light", "mail")}</div>'
    return f'''<section class="page-hero">
  <div class="page-hero-bg" style="background-image:url('/assets/img/{img}')" aria-hidden="true"></div>
  <div class="aurora" aria-hidden="true"><span></span><span></span><span></span></div>
  <div class="container page-hero-inner">
    {breadcrumbs_html(page["crumbs"])}
    {k}<h1>{page["h1"]}</h1>{lead}{meta}{actions}
  </div>
</section>'''


def sidebar(page):
    related = page.get("sidebar_links") or [(n, f"/services/{s}/") for s, n, _, _ in SERVICES[:6]]
    rl = "".join(f'<li><a href="{h}">{t}</a></li>' for t, h in related)
    return f'''<aside class="sidebar">
  <div class="side-card side-toc" data-toc hidden><h2 class="h5">On this page</h2><ol></ol></div>
  <div class="side-card side-cta">
    <span class="side-badge">{icon("phone", "ico ico-sm")} Free consultation</span>
    <h2 class="h4">Estimates far apart?</h2>
    <p>Talk with an Alabama Insurance Appraiser about the gap before you decide on appraisal.</p>
    {call_btn("primary")}
    <a class="side-link" href="/contact/">or send claim details &rarr;</a>
  </div>
  <div class="side-card"><h2 class="h5">{page.get("sidebar_title", "Appraisal services")}</h2><ul class="side-list">{rl}</ul></div>
  <div class="side-card side-tool"><h2 class="h5">Free tool</h2><p>Measure the difference between two estimates in seconds.</p><a class="btn btn-soft" href="/tools/claim-gap-calculator/"><span>Claim Gap Calculator</span>{icon("calculator", "ico ico-sm")}</a></div>
</aside>'''


# --------------------------------------------------------------------------
# Schema
# --------------------------------------------------------------------------
def org_schema():
    return {
        "@type": ["ProfessionalService", "LocalBusiness"],
        "@id": ORG_ID,
        "name": BIZ["name"],
        "alternateName": "AIA",
        "url": ORIGIN + "/",
        "logo": {"@type": "ImageObject", "@id": ORIGIN + "/#logo",
                 "url": url("/assets/img/alabama-insurance-appraiser-logo.webp"), "width": 600, "height": 135,
                 "caption": BIZ["name"]},
        "image": [url("/assets/img/alabama-insurance-appraiser-og.jpg"), url("/assets/img/alabama-insurance-appraiser-home.webp")],
        "description": "Independent property insurance appraisal, Xactimate and Symbility estimating, and Matterport claim documentation for residential and commercial property losses throughout Alabama.",
        "telephone": BIZ["phone_href"],
        "email": BIZ["email"],
        "address": {"@type": "PostalAddress", "addressRegion": "AL", "addressCountry": "US"},
        "areaServed": [{"@type": "State", "name": "Alabama", "sameAs": "https://en.wikipedia.org/wiki/Alabama"}]
        + [{"@type": "City", "name": f"{c}, Alabama"} for c, _ in CITIES],
        "contactPoint": [{"@type": "ContactPoint", "telephone": BIZ["phone_href"], "email": BIZ["email"],
                          "contactType": "customer service", "areaServed": "US-AL", "availableLanguage": "English"}],
        "knowsAbout": ["Property insurance appraisal", "Appraisal clause", "Amount of loss", "Insurance umpire",
                       "Xactimate", "Symbility", "Matterport", "Hail damage", "Wind damage", "Hurricane damage",
                       "Water damage", "Fire and smoke damage", "Commercial property claims"],
        "hasOfferCatalog": {
            "@type": "OfferCatalog", "name": "Insurance appraisal and estimating services",
            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "@id": url(f"/services/{s}/#service"), "name": n}}
                                for s, n, _, _ in SERVICES],
        },
        "slogan": "A closer look at the property, the scope and the numbers.",
    }


def website_schema():
    return {"@type": "WebSite", "@id": SITE_ID, "url": ORIGIN + "/", "name": BIZ["name"],
            "description": BIZ["tagline"], "publisher": {"@id": ORG_ID}, "inLanguage": "en-US"}


def breadcrumb_schema(page):
    return {"@type": "BreadcrumbList", "@id": url(page["path"]) + "#breadcrumb",
            "itemListElement": [{"@type": "ListItem", "position": n, "name": html.unescape(name), "item": url(href)}
                                for n, (name, href) in enumerate(page["crumbs"], 1)]}


def faq_schema(page, faqs):
    import re
    def strip(s):
        return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()
    return {"@type": "FAQPage", "@id": url(page["path"]) + "#faq",
            "mainEntity": [{"@type": "Question", "name": strip(q),
                            "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faqs]}


def service_schema(page, name, service_type, area=None, desc=None):
    s = {"@type": "Service", "@id": url(page["path"]) + "#service", "name": name, "serviceType": service_type,
         "description": desc or page["description"], "provider": {"@id": ORG_ID}, "url": url(page["path"]),
         "areaServed": area or {"@type": "State", "name": "Alabama"},
         "audience": {"@type": "Audience", "audienceType": "Property owners, policyholders, contractors and claim professionals"}}
    return s


def page_graph(page):
    pid = url(page["path"])
    wp_type = page.get("schema_type", "WebPage")
    img_key = page.get("hero_img")
    webpage = {"@type": wp_type, "@id": pid + "#webpage", "url": pid,
               "name": html.unescape(page["title"]), "description": page["description"],
               "isPartOf": {"@id": SITE_ID}, "inLanguage": "en-US",
               "dateModified": page.get("modified", TODAY)}
    if page["path"] != "/":
        webpage["breadcrumb"] = {"@id": pid + "#breadcrumb"}
    else:
        webpage["about"] = {"@id": ORG_ID}
    if img_key:
        webpage["primaryImageOfPage"] = {"@type": "ImageObject", "url": url("/assets/img/" + IMG[img_key][0]),
                                         "width": IMG[img_key][1], "height": IMG[img_key][2]}
    if page.get("published"):
        webpage["datePublished"] = page["published"]
    graph = [org_schema(), website_schema(), webpage]
    if page["path"] != "/":
        graph.append(breadcrumb_schema(page))
    for extra in page.get("schema", []):
        graph.append(extra)
    return {"@context": "https://schema.org", "@graph": graph}


# --------------------------------------------------------------------------
# Full page
# --------------------------------------------------------------------------
def render_page(page):
    title = page["title"]
    desc = page["description"]
    canonical = url(page["path"])
    og_img = url("/assets/img/alabama-insurance-appraiser-og.jpg")
    robots = "noindex, follow" if page.get("noindex") else "index, follow, max-image-preview:large, max-snippet:-1"
    scripts = "".join(f'<script src="{s}?v={ASSET_VER}" defer></script>' for s in page.get("scripts", []))
    layout = page.get("layout", "prose")
    if layout == "raw":
        main = page["body"]
    elif layout == "prose":
        main = (inner_hero(page) + f'<div class="container layout-sidebar"><article class="prose" data-prose>{page["body"]}</article>'
                f'{sidebar(page)}</div>' + page.get("after", "") + (cta_band() if page.get("cta", True) else ""))
    else:  # wide
        main = inner_hero(page) + page["body"] + (cta_band() if page.get("cta", True) else "")
    og_type = "article" if page.get("published") and page.get("is_post") else "website"
    art_meta = ""
    if og_type == "article":
        art_meta = (f'<meta property="article:published_time" content="{page["published"]}">'
                    f'<meta property="article:modified_time" content="{page.get("modified", page["published"])}">')
    schema = json.dumps(page_graph(page), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'''<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#173042">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{BIZ['name']}">
<meta property="og:title" content="{esc(page.get('og_title', title))}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="675">
<meta property="og:image:alt" content="{BIZ['name']}">
{art_meta}<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(page.get('og_title', title))}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{og_img}">
<meta name="geo.region" content="US-AL">
<meta name="geo.placename" content="Alabama">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" href="/favicon-96x96.png" sizes="96x96">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,500&display=swap">
{page.get("preload", "")}<link rel="stylesheet" href="/assets/css/site.css?v={ASSET_VER}">
<script type="application/ld+json">{schema}</script>
</head>
<body class="{page.get('body_class', '')}">
{header(page.get("nav_active", ""))}
<main id="main">
{main}
</main>
{footer()}
<script src="/assets/js/site.js?v={ASSET_VER}" defer></script>{scripts}
</body>
</html>
'''
