"""Every page except the homepage."""
import build as B
from build import e, icon, img, TEL, PHONE, SITE


def card_grid_services(exclude=None):
    out = ""
    for i, s in enumerate(x for x in B.SERVICES if x["slug"] != exclude):
        out += (f'<article class="card" data-reveal style="--d:{(i % 3) * 0.08:.2f}s"><div class="ico">{icon(s.get("icon", "home"))}</div>'
                f'<h3><a class="card-link" href="/services/{s["slug"]}/" style="color:inherit;text-decoration:none">{e(s["name"])}</a></h3>'
                f'<p>{e(s["short"])}</p><span class="more">Learn more {icon("arrow")}</span></article>')
    return out


def post_card(p, i=0):
    return (f'<article class="card img-card" style="--d:{(i % 3) * 0.08:.2f}s"><div class="img">{img(p["image"], p.get("image_alt", p["h1"]))}</div>'
            f'<div class="body"><span class="tag">{e(p.get("category", "Guide"))}</span>'
            f'<div class="meta-row"><span>{icon("calendar")} {B.fmt_date(p["date"])}</span><span>{icon("clock")} {p.get("read_minutes", 6)} min</span></div>'
            f'<h3><a class="card-link" href="/blog/{p["slug"]}/" style="color:inherit;text-decoration:none">{e(p["h1"])}</a></h3>'
            f'<p>{e(p["excerpt"])}</p><span class="more">Read article {icon("arrow")}</span></div></article>')


def prose_page(item, crumbs, aside, eyebrow, meta="", lead_img=True, after_body=""):
    body = B.prep_body(item["body"])
    lead = f'<div class="lead-img">{img(item["image"], item.get("image_alt", item["h1"]), eager=False, sizes="(max-width: 1080px) 100vw, 760px")}</div>' if lead_img else ""
    return (B.page_hero(crumbs, e(item["h1"]), item["intro"], bg=item["image"], eyebrow=eyebrow, meta=meta) +
            f'<section class="section"><div class="wrap layout"><article class="prose">{lead}{body}{after_body}</article>'
            f'<aside class="aside">{aside}</aside></div></section>')


# --------------------------------------------------------------------------- services
def build_services():
    for s in B.SERVICES:
        url = f"/services/{s['slug']}/"
        crumbs = [("Home", "/"), ("Services", "/services/"), (s["name"], url)]
        bullets = "".join(f"<li>{icon('check')}<span>{e(b)}</span></li>" for b in s.get("bullets", []))
        others = "".join(f'<li><a href="/services/{o["slug"]}/">{e(o["name"])} {icon("arrow")}</a></li>' for o in B.SERVICES if o is not s)
        aside = (f'<div class="box"><h3>What\'s included</h3><ul class="checks" style="margin:0">{bullets}</ul></div>' + B.aside_phone() +
                 f'<div class="box"><h3>Other services</h3><ul><li><a href="/free-roof-inspection/">Free Roof Inspection {icon("arrow")}</a></li>{others}</ul></div>')
        main = prose_page(s, crumbs, aside, eyebrow=f"Katy roofing · {s['name']}")
        main += B.faq_html(s["faqs"], f"{s['name']} FAQs")
        main += B.form_section("svc-form", service=None)
        main += B.final_cta()
        schema = [B.crumbs_schema(crumbs), B.faq_schema(s["faqs"]),
                  {"@type": "Service", "name": s["h1"], "serviceType": s["name"], "url": SITE + url, "description": s["description"],
                   "provider": {"@id": SITE + "/#business"}, "areaServed": {"@type": "City", "name": "Katy, TX"}}]
        B.add(url, B.page(url, s["title"], s["description"], main, active="/services/", schema=schema, og_image=s["image"] + ".webp"), priority="0.9")

    url = "/services/"
    crumbs = [("Home", "/"), ("Services", url)]
    main = (B.page_hero(crumbs, "Katy Roofing Services", "Every roofing service a Katy home or business needs, starting with a free, photo-documented roof inspection.",
                        bg="roofer-shingles", eyebrow="What we do") +
            f"""<section class="section"><div class="wrap"><div class="section-head" data-reveal><h2>Roof repair, replacement and storm restoration</h2>
<p>As a full-service Katy roofer, we handle everything from a single cracked pipe boot to complete tear-offs on large homes and light commercial buildings. Pick a service to learn how we approach it, or <a href="/free-roof-inspection/">book a free inspection</a> and we'll tell you what your roof actually needs.</p></div>
<div class="grid g3">{card_grid_services()}</div></div></section>""" +
            B.form_section("services-form") + B.final_cta())
    B.add(url, B.page(url, "Roofing Services in Katy, TX | Katy Roofer",
                      "Roof repair, roof replacement, hail damage, insurance claim help, metal roofing, commercial roofing and gutters in Katy, TX. Free roof inspections.",
                      main, schema=[B.crumbs_schema(crumbs)]), priority="0.8")


# --------------------------------------------------------------------------- areas
def build_areas():
    for a in B.AREAS:
        url = f"/areas/{a['slug']}/"
        crumbs = [("Home", "/"), ("Service Areas", "/areas/"), (a["name"], url)]
        hoods = "".join(f"<span>{e(n)}</span>" for n in a.get("neighborhoods", []))
        others = "".join(f'<li><a href="/areas/{o["slug"]}/">{e(o["name"])} {icon("arrow")}</a></li>' for o in B.AREAS if o is not a)
        aside = (f"""<div class="box"><h3>{e(a['name'])} at a glance</h3><ul class="checks" style="margin:0 0 14px">
<li>{icon('pin')}<span><strong>County:</strong> {e(a.get('county', ''))}</span></li>
<li>{icon('home')}<span><strong>ZIP codes:</strong> {e(a.get('zips', ''))}</span></li>
<li>{icon('clock')}<span>{e(a.get('drive', ''))}</span></li></ul>
<div class="chips" style="gap:6px">{hoods}</div></div>""" + B.aside_phone() +
                 f'<div class="box"><h3>Nearby areas</h3><ul><li><a href="/">Katy, TX {icon("arrow")}</a></li>{others}</ul></div>')
        main = prose_page(a, crumbs, aside, eyebrow=f"Service area · {a['name']}, TX")
        main += f'<section class="section section-soft"><div class="wrap"><div class="section-head" data-reveal><span class="eyebrow">Services in {e(a["name"])}</span><h2>What we do in {e(a["name"])}</h2></div><div class="grid g3">{card_grid_services()}</div></div></section>'
        main += B.faq_html(a["faqs"], f"Roofing in {a['name']}: FAQs")
        main += B.form_section("area-form")
        main += B.final_cta()
        schema = [B.crumbs_schema(crumbs), B.faq_schema(a["faqs"]),
                  {"@type": "Service", "name": a["h1"], "serviceType": "Roofing", "url": SITE + url, "provider": {"@id": SITE + "/#business"},
                   "areaServed": {"@type": "City", "name": a["name"] + ", TX"}}]
        B.add(url, B.page(url, a["title"], a["description"], main, active="/areas/", schema=schema, og_image=a["image"] + ".webp"), priority="0.8")

    url = "/areas/"
    crumbs = [("Home", "/"), ("Service Areas", url)]
    cards = "".join(f"""<article class="card img-card" style="--d:{(i % 3) * 0.08:.2f}s"><div class="img">{img(a['image'], a.get('image_alt', a['name']))}</div>
<div class="body"><span class="tag">{e(a.get('county', ''))}</span><h3><a class="card-link" href="/areas/{a['slug']}/" style="color:inherit;text-decoration:none">{e(a['name'])}</a></h3>
<p>{e(a['short'])}</p><span class="more">Roofing in {e(a['name'])} {icon('arrow')}</span></div></article>""" for i, a in enumerate(B.AREAS))
    main = (B.page_hero(crumbs, "Areas We Serve Around Katy, TX", "Based in Katy and working across Harris, Fort Bend and Waller counties, from the Brazos River to the Energy Corridor.",
                        bg="suburban-street", eyebrow="Service areas") +
            f"""<section class="section"><div class="wrap">
<div class="split" style="margin-bottom:56px"><div data-reveal="left"><h2>Katy, TX: our home base</h2>
<p>Katy is where we live and work. We cover every Katy ZIP code (77449, 77450, 77493 and 77494), from older homes around Old Town Katy and Nottingham Country to newer master-planned communities like Cinco Ranch, Cane Island, Elyson, Jordan Ranch, Tamarron and Pine Mill Ranch.</p>
<p>Because Katy spans three counties and dozens of HOAs, we keep track of the shingle color and material rules that apply in each community, so your new roof gets approved the first time.</p>
<a class="btn" href="/free-roof-inspection/">Free inspection in Katy {icon('arrow')}</a></div>
<div class="media">{img('suburban-home', 'Suburban home under storm clouds in Katy, Texas')}</div></div>
<div class="section-head" data-reveal><h2>Nearby communities</h2><p>Each community has its own housing stock, HOA rules and storm exposure. Here's what we see in each.</p></div>
<div class="grid g3">{cards}</div></div></section>""" + B.form_section("areas-form") + B.final_cta())
    B.add(url, B.page(url, "Roofing Service Areas Near Katy, TX | Katy Roofer",
                      "Katy Roofer serves Katy, Cinco Ranch, Fulshear, Brookshire, Cypress, Richmond and West Houston. Free roof inspections across all Katy ZIP codes.",
                      main, schema=[B.crumbs_schema(crumbs)]), priority="0.7")


# --------------------------------------------------------------------------- blog
def build_blog():
    for idx, p in enumerate(B.POSTS):
        url = f"/blog/{p['slug']}/"
        crumbs = [("Home", "/"), ("Blog", "/blog/"), (p["h1"], url)]
        meta = (f'<div class="post-meta"><span>{icon("calendar")} {B.fmt_date(p["date"])}</span><span>{icon("clock")} {p.get("read_minutes", 6)} min read</span>'
                f'<span>{icon("users")} By the Katy Roofer team</span></div>')
        related = [x for x in B.POSTS if x is not p and x.get("category") == p.get("category")]
        related += [x for x in B.POSTS if x is not p and x not in related]
        svc_links = "".join(f'<li><a href="/services/{s["slug"]}/">{e(s["name"])} {icon("arrow")}</a></li>' for s in B.SERVICES[:5])
        aside = ('<div class="box toc"><h3>In this article</h3><ul></ul></div>' + B.aside_phone() +
                 f'<div class="box"><h3>Roofing services</h3><ul><li><a href="/free-roof-inspection/">Free Roof Inspection {icon("arrow")}</a></li>{svc_links}</ul></div>'
                 f'<div class="box"><h3>Free tools</h3><ul>' + "".join(f'<li><a href="{h}">{e(l)} {icon("arrow")}</a></li>' for h, l in B.NAV_TOOLS) + '</ul></div>')
        author = (f'<div class="card" style="margin-top:2.5em;flex-direction:row;gap:18px;align-items:center" data-reveal><div class="ico" style="margin:0">{icon("roof")}</div>'
                  f'<div><strong style="font-family:var(--head);color:var(--ink)">Written by the Katy Roofer team</strong><p style="margin:4px 0 0">Local roofers serving Katy, Cinco Ranch, Fulshear and West Houston. '
                  f'Questions about your roof? Call <a href="tel:{TEL}">{PHONE}</a> or <a href="/free-roof-inspection/">book a free inspection</a>.</p></div></div>')
        main = prose_page(p, crumbs, aside, eyebrow=p.get("category", "Guide"), meta=meta, after_body=author)
        main += B.faq_html(p["faqs"], "Frequently asked questions")
        main += (f'<section class="section"><div class="wrap"><div class="section-head" data-reveal><span class="eyebrow">Keep reading</span><h2>More Katy roofing guides</h2></div>'
                 f'<div class="grid g3">{"".join(post_card(x, i) for i, x in enumerate(related[:3]))}</div></div></section>')
        main += B.final_cta()
        schema = [B.crumbs_schema(crumbs), B.faq_schema(p["faqs"]),
                  {"@type": "BlogPosting", "headline": p["h1"], "description": p["description"], "datePublished": p["date"] + "T08:00:00-05:00",
                   "dateModified": p["date"] + "T08:00:00-05:00", "mainEntityOfPage": SITE + url, "image": f"{SITE}/assets/img/{p['image']}.webp",
                   "author": {"@type": "Organization", "name": B.NAME, "url": SITE + "/"}, "publisher": {"@id": SITE + "/#business"},
                   "keywords": p.get("keyword", ""), "articleSection": p.get("category", "")}]
        head = f'<meta property="article:published_time" content="{p["date"]}T08:00:00-05:00">\n'
        B.add(url, B.page(url, p["title"], p["description"], main, active="/blog/", schema=schema, og_image=p["image"] + ".webp",
                          og_type="article", extra_head=head), lastmod=p["date"], priority="0.6")

    url = "/blog/"
    crumbs = [("Home", "/"), ("Blog", url)]
    first = B.POSTS[0]
    feature = f"""<article class="card img-card blog-feature">
<div class="img" style="aspect-ratio:auto;min-height:320px">{img(first['image'], first.get('image_alt', first['h1']))}</div>
<div class="body" style="padding:36px"><span class="tag">Latest · {e(first.get('category', ''))}</span>
<div class="meta-row"><span>{icon('calendar')} {B.fmt_date(first['date'])}</span><span>{icon('clock')} {first.get('read_minutes', 6)} min</span></div>
<h2 style="font-size:1.8rem"><a class="card-link" href="/blog/{first['slug']}/" style="color:inherit;text-decoration:none">{e(first['h1'])}</a></h2>
<p>{e(first['excerpt'])}</p><span class="more">Read article {icon('arrow')}</span></div></article>"""
    cards = "".join(post_card(p, i) for i, p in enumerate(B.POSTS[1:]))
    main = (B.page_hero(crumbs, "Katy Roofing Blog", "Practical guides for Katy homeowners on roof costs, hail and hurricane damage, insurance claims, materials and maintenance.",
                        bg="home-gables", eyebrow="Guides & advice") +
            f'<section class="section"><div class="wrap">{feature}<div class="grid g3">{cards}</div></div></section>' + B.final_cta())
    items = {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{SITE}/blog/{p['slug']}/"} for i, p in enumerate(B.POSTS)]}
    B.add(url, B.page(url, "Katy Roofing Blog: Guides for Katy, TX Homeowners",
                      "Roofing advice from a Katy roofer: replacement costs, hail damage, Texas insurance claims, hurricane prep, materials and maintenance checklists.",
                      main, schema=[B.crumbs_schema(crumbs), items]), lastmod=B.POSTS[0]["date"], priority="0.7")


# --------------------------------------------------------------------------- free inspection
INSPECTION_FAQS = [
    {"q": "Why is your roof inspection free?", "a": "Because most homeowners shouldn't have to pay to find out whether they have a problem. A free inspection is how people get to know us; if your roof needs work, we hope you'll hire us, and if it doesn't, we'll tell you so."},
    {"q": "How long does a free roof inspection take?", "a": "Most Katy homes take 30 to 60 minutes, depending on roof size, pitch and whether we check the attic. You don't need to be on the roof, and you can watch the photos as we review them with you."},
    {"q": "Do I need to be home?", "a": "It helps for the attic check and walkthrough, but it isn't required for the exterior inspection. We'll send the photos and findings either way."},
    {"q": "Will an inspection affect my insurance?", "a": "No. Getting your roof inspected by a contractor is not a claim. You decide whether to file, and we'll explain what we found so you can make that decision with real information."},
    {"q": "Is a free inspection useful when buying or selling a home?", "a": "Yes. A roofer's inspection goes deeper on the roof than a general home inspection, and the photo report is useful in negotiations or to plan maintenance."},
]


def build_inspection():
    url = "/free-roof-inspection/"
    crumbs = [("Home", "/"), ("Free Roof Inspection", url)]
    checks = [("cloud-hail", "Hail & impact damage", "Bruised or fractured shingles, granule loss, dented vents and soft metals."),
              ("wind", "Wind damage", "Lifted, creased or missing shingles and ridge caps; broken seal strips."),
              ("layers", "Flashing & valleys", "Step, wall, chimney and valley flashing; exposed nails and failed sealant."),
              ("droplets", "Leaks & moisture", "Attic stains, damp insulation, rusted nails and soft decking."),
              ("sun", "Ventilation & heat", "Intake and exhaust balance, attic temperature, blocked soffits."),
              ("home", "Gutters & drainage", "Sagging runs, clogged downspouts, fascia rot and overflow staining.")]
    cards = "".join(f'<div class="card" data-reveal style="--d:{(i % 3) * 0.08:.2f}s"><div class="ico">{icon(ic)}</div><h3>{e(t)}</h3><p>{e(d)}</p></div>'
                    for i, (ic, t, d) in enumerate(checks))
    main = f"""
<section class="hero hero-home" style="min-height:auto">
<div class="hero-bg" style="background-image:url(/assets/img/roofer-shingles.webp)"></div>
<div class="wrap">
<div>{B.crumbs_html(crumbs)}
<div data-reveal><span class="eyebrow"><span class="dot"></span> $0 · No obligation</span></div>
<h1 data-reveal style="--d:.1s">Free Roof Inspections in <span class="hl">Katy, TX</span></h1>
<p class="lead" data-reveal style="--d:.2s">A local Katy roofer will inspect your roof top to bottom, photograph every issue and give you an honest, written recommendation, all at no cost.</p>
<div class="hero-trust" data-reveal style="--d:.3s"><span>{icon('camera')} Photo report</span><span>{icon('file-check')} Written findings</span><span>{icon('shield')} Storm-damage documentation</span></div>
</div>
<div class="form-card" data-reveal="zoom">{B.lead_form('inspect-form', heading='Book your free roof inspection', sub="Pick a time that works. We'll confirm by phone.", full=True, service='Free roof inspection')}</div>
</div></section>

<section class="section"><div class="wrap">
<div class="section-head" data-reveal><span class="eyebrow">What we check</span><h2>A 6-point roof inspection, not a glance from the driveway</h2>
<p>Many roofers in Katy will "inspect" a roof from a ladder in five minutes. Ours is a full walk of every slope plus an attic check, because that's where the evidence is.</p></div>
<div class="grid g3">{cards}</div></div></section>

<section class="section section-dark"><div class="wrap split" style="align-items:start">
<div class="sticky" data-reveal="left"><span class="eyebrow">How it works</span><h2>From booking to photo report</h2>
<p>Simple, quick and no-pressure. You get the facts and decide what happens next.</p>
<a class="btn" href="tel:{TEL}">{icon('phone')} {PHONE}</a></div>
<div class="steps"><span class="line" aria-hidden="true"></span>
<div class="step" data-n="1" data-reveal><h3>Book online or call</h3><p>Use the form above or call {PHONE}. Tell us about any leaks or recent storms.</p></div>
<div class="step" data-n="2" data-reveal><h3>We inspect</h3><p>A Katy roofer walks every slope, checks flashing, vents and gutters, and looks in the attic if you're home.</p></div>
<div class="step" data-n="3" data-reveal><h3>You see the photos</h3><p>We review findings with you on the spot, with close-ups of anything that matters, and send the photos for your records.</p></div>
<div class="step" data-n="4" data-reveal><h3>Honest recommendation</h3><p>No damage? We'll say so. A repair? We'll quote it. Storm damage? We'll explain the claim process and can meet your adjuster.</p></div>
</div></div></section>

<section class="section"><div class="wrap split">
<div class="media">{img('hero-roofer', 'Roofer kneeling on a shingle roof during a free roof inspection in Katy')}</div>
<div data-reveal="right"><span class="eyebrow">When to book</span><h2>Good times to get a free roof inspection</h2>
<ul class="checks">
<li>{icon('check-circle')}<span><strong>After hail or high winds</strong> — even if you don't see damage from the ground</span></li>
<li>{icon('check-circle')}<span><strong>Before hurricane season</strong> — loose shingles and weak flashing fail first</span></li>
<li>{icon('check-circle')}<span><strong>Roof older than 10 years</strong> — catch small problems before they turn into leaks</span></li>
<li>{icon('check-circle')}<span><strong>Buying or selling a home</strong> — know exactly what you're getting</span></li>
<li>{icon('check-circle')}<span><strong>Stains on a ceiling or wall</strong> — find the source before it spreads</span></li>
</ul>
<p>Not sure? Run our <a href="/tools/storm-damage-checklist/">storm damage self-check</a> or check the <a href="/weather/">live Katy weather page</a> for recent severe weather.</p></div>
</div></section>
{B.faq_html(INSPECTION_FAQS, "Free roof inspection FAQs")}
{B.final_cta("Book your free roof inspection today")}"""
    schema = [B.crumbs_schema(crumbs), B.faq_schema(INSPECTION_FAQS),
              {"@type": "Service", "name": "Free Roof Inspection in Katy, TX", "serviceType": "Roof inspection", "url": SITE + url,
               "provider": {"@id": SITE + "/#business"}, "areaServed": {"@type": "City", "name": "Katy, TX"},
               "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}]
    B.add(url, B.page(url, "Free Roof Inspection in Katy, TX | Katy Roofer",
                      "Book a free roof inspection in Katy, TX. A local Katy roofer checks for hail, wind and leak damage and gives you a photo report. No cost, no obligation.",
                      main, schema=schema, og_image="roofer-shingles.webp"), priority="0.9")


# --------------------------------------------------------------------------- weather
WEATHER_FAQS = [
    {"q": "Where does this Katy weather data come from?", "a": "Current conditions and the 7-day forecast come from Open-Meteo, which blends national weather models including NOAA's. Active alerts come directly from the National Weather Service Houston/Galveston office feed for Katy's coordinates."},
    {"q": "What does the roof risk rating mean?", "a": "It's our simple read of each day's forecast: thunderstorms with possible hail or wind gusts of 50 mph or more rate High; ordinary thunderstorms, heavy showers or gusts above 35 mph rate Moderate. It's informational, not an official warning."},
    {"q": "When is hail season in Katy?", "a": "Most damaging hail around Katy falls between March and June, when spring storm systems collide with warm Gulf moisture, though hail can occur in any month."},
    {"q": "What should I do after a severe storm passes?", "a": "Stay off the roof. From the ground, look for missing shingles, dented gutters and granules at downspouts, photograph anything you see, check ceilings for stains, and book a free roof inspection."},
]


def build_weather():
    url = "/weather/"
    crumbs = [("Home", "/"), ("Katy Weather", url)]
    main = f"""{B.page_hero(crumbs, "Katy, TX Weather & 7-Day Forecast", "Live conditions, National Weather Service alerts and a 7-day forecast for Katy, with a daily roof-risk rating for hail and high wind.", bg="lightning", eyebrow="Live weather")}
<section class="section" style="padding-bottom:40px"><div class="wrap">
<div data-wx-alerts class="alert-box" data-reveal><h3>Checking National Weather Service alerts for Katy…</h3></div>
</div></section>
<section class="section section-dark" style="padding:60px 0"><div class="wrap">
<div class="section-head" style="margin-bottom:28px"><span class="eyebrow"><span class="dot"></span> Right now in Katy</span><h2>Current conditions</h2></div>
<div class="wx-current" data-wx-current><div class="skeleton" style="background:rgba(255,255,255,.06);grid-column:1/-1"></div></div>
</div></section>
<section class="section"><div class="wrap">
<div class="section-head" data-reveal><span class="eyebrow">7-day forecast</span><h2>Katy 7-day weather forecast</h2>
<p data-wx-outlook>Loading this week's roof outlook…</p></div>
<div class="wx-forecast" data-wx-forecast>{''.join('<div class="skeleton"></div>' for _ in range(7))}</div>
<div class="prose" style="margin-top:40px" data-reveal><table><thead><tr><th>Day</th><th>Conditions</th><th>High / Low</th><th>Rain chance</th><th>Wind / Gusts</th><th>UV</th></tr></thead>
<tbody data-wx-table><tr><td colspan="6">Loading…</td></tr></tbody></table>
<p style="font-size:.9rem;color:var(--muted)">Forecast data: <a href="https://open-meteo.com/" rel="noopener" target="_blank">Open-Meteo</a> (CC BY 4.0). Alerts: <a href="https://www.weather.gov/hgx/" rel="noopener" target="_blank">National Weather Service Houston/Galveston</a>. Times shown in Central Time. Roof-risk ratings are informational, not official warnings.</p></div>
</div></section>
<section class="section section-soft"><div class="wrap">
<div class="section-head" data-reveal><span class="eyebrow">Be ready</span><h2>Protect your roof when storms are in the forecast</h2></div>
<div class="grid g3">
<div class="card" data-reveal><div class="ico">{icon('camera')}</div><h3>Before the storm</h3><p>Take dated photos of each roof slope from the ground, clean gutters, trim branches over the roof and secure patio furniture and trampolines.</p></div>
<div class="card" data-reveal style="--d:.08s"><div class="ico">{icon('alert')}</div><h3>During the storm</h3><p>Park cars in the garage, stay away from windows during hail, and if water comes in, move valuables and catch drips. Never climb on a wet roof.</p></div>
<div class="card" data-reveal style="--d:.16s"><div class="ico">{icon('clipboard')}</div><h3>After the storm</h3><p>Walk the property, photograph dents and debris, run our <a href="/tools/storm-damage-checklist/">storm damage self-check</a>, and book a <a href="/free-roof-inspection/">free roof inspection</a>.</p></div>
</div></div></section>
<section class="section"><div class="wrap split">
<div data-reveal="left"><span class="eyebrow">Katy's roofing seasons</span><h2>What each season means for your roof</h2>
<div class="prose"><table><thead><tr><th>Season</th><th>Main roof threat</th><th>What to do</th></tr></thead><tbody>
<tr><td>Mar–Jun</td><td>Hail, severe thunderstorms, straight-line wind</td><td>Inspect after every hail report</td></tr>
<tr><td>Jun–Nov</td><td>Tropical storms &amp; hurricanes, flooding rain</td><td>Pre-season inspection, secure loose shingles</td></tr>
<tr><td>Jul–Sep</td><td>Extreme heat and UV, attic heat buildup</td><td>Check ventilation, pipe boots and sealants</td></tr>
<tr><td>Dec–Feb</td><td>Occasional freezes, cold fronts with wind</td><td>Clear gutters, check flashing before spring</td></tr>
</tbody></table></div>
<p>Read our <a href="/blog/hurricane-season-roof-prep-katy-tx/">hurricane season roof prep guide</a> and <a href="/blog/how-to-spot-hail-damage-on-your-katy-roof/">how to spot hail damage</a>.</p></div>
<div class="media">{img('storm-clouds', 'Dark storm clouds rolling over Katy, Texas')}</div>
</div></section>
{B.faq_html(WEATHER_FAQS, "Katy weather & roof FAQs")}
{B.final_cta("Storm just passed? Get a free roof inspection", bg="storm-dark")}"""
    B.add(url, B.page(url, "Katy, TX Weather: Live 7-Day Forecast & Storm Alerts",
                      "Live Katy, TX weather: current conditions, NWS alerts and a 7-day forecast with a daily hail and wind roof-risk rating. Free roof inspections after storms.",
                      main, schema=[B.crumbs_schema(crumbs), B.faq_schema(WEATHER_FAQS)], scripts=("weather",), og_image="lightning.webp"), priority="0.8")


# --------------------------------------------------------------------------- tools
def seg(name, options, checked):
    return '<div class="seg">' + "".join(
        f'<label><input type="radio" name="{name}" value="{v}"{" checked" if v == checked else ""}><span>{e(l)}</span></label>' for v, l in options) + "</div>"


def tool_page(url, crumbs_name, h1, lead, title, desc, tool_html, body_html, faqs, bg, app_name):
    crumbs = [("Home", "/"), ("Tools", "/tools/"), (crumbs_name, url)]
    others = "".join(f'<a class="card" href="{h}" style="text-decoration:none;color:inherit" data-reveal><h3>{e(l)}</h3><span class="more">Open tool {icon("arrow")}</span></a>'
                     for h, l in B.NAV_TOOLS if h != url)
    main = (B.page_hero(crumbs, h1, lead, bg=bg, eyebrow="Free homeowner tool") +
            f'<section class="section"><div class="wrap"><div class="tool" data-reveal>{tool_html}</div></div></section>' +
            f'<section class="section section-soft"><div class="wrap layout"><article class="prose">{body_html}{B.cta_band()}</article>'
            f'<aside class="aside">{B.aside_phone()}</aside></div></section>' +
            B.faq_html(faqs, "Questions about this tool") +
            f'<section class="section"><div class="wrap"><div class="section-head"><h2>More free tools</h2></div><div class="grid g2">{others}</div></div></section>' +
            B.final_cta())
    schema = [B.crumbs_schema(crumbs), B.faq_schema(faqs),
              {"@type": "WebApplication", "name": app_name, "url": SITE + url, "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any",
               "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": SITE + "/#business"}}]
    B.add(url, B.page(url, title, desc, main, active="/tools/", schema=schema, scripts=("tools",)), priority="0.7")


def build_tools():
    # 1. cost calculator
    cost_tool = f"""<form data-tool="cost" onsubmit="return false"><div class="tool-grid">
<div>
<h2 style="font-size:1.5rem">Your home</h2>
<div class="range-row"><label for="sqft">Living area (sq ft) <output for="sqft"></output></label><input type="range" id="sqft" name="sqft" min="1000" max="6000" step="50" value="2600" data-fmt=" sq ft"></div>
<div class="range-row"><label>Stories</label>{seg('stories', [('1', '1 story'), ('2', '2 stories'), ('3', '3 stories')], '2')}</div>
<div class="range-row"><label>Roof pitch</label>{seg('pitch', [('low', 'Low (≤4/12)'), ('med', 'Medium (5–7/12)'), ('steep', 'Steep (8/12+)')], 'med')}</div>
<div class="range-row"><label>Roofing material</label>{seg('material', [('3tab', '3-tab shingle'), ('arch', 'Architectural'), ('class4', 'Class 4 impact'), ('metal', 'Standing-seam metal'), ('stone', 'Stone-coated steel'), ('tile', 'Concrete tile')], 'arch')}</div>
<div class="range-row"><label>Layers to tear off</label>{seg('layers', [('1', '1 layer'), ('2', '2 layers')], '1')}</div>
<div class="range-row"><label for="deck">Decking to replace <output for="deck"></output></label><input type="range" id="deck" name="deck" min="0" max="50" step="5" value="10" data-fmt="%"></div>
</div>
<div class="result" aria-live="polite">
<span class="eyebrow" style="color:var(--gold)">Estimated installed cost</span>
<div class="big" data-out="range">—</div>
<dl><dt>Material</dt><dd data-out="mat"></dd><dt>Est. roof area</dt><dd data-out="area"></dd><dt>Roofing squares</dt><dd data-out="squares"></dd>
<dt>Per square (100 sq ft)</dt><dd data-out="persq"></dd><dt>Typical lifespan in Katy</dt><dd data-out="life"></dd></dl>
<a class="btn" style="width:100%" href="/free-roof-inspection/">Get an exact quote, free {icon('arrow')}</a>
<small>Planning range for the Katy / west Houston market in 2026, not a quote. Actual price depends on measurements, roof complexity, ventilation, flashing and code items. Insurance-approved claims are priced from your adjuster's scope.</small>
</div></div></form>"""
    cost_body = f"""<h2>How this roof cost calculator works</h2>
<p>The calculator converts your home's living area into an estimated roof area. It divides by the number of stories to approximate the footprint, adds about 12% for overhangs, then multiplies by a slope factor for your pitch. It then applies a 2026 installed-price range per square foot for the material you choose, adjusts labor for steep or multi-story roofs, and adds tear-off for extra layers and any decking you expect to replace.</p>
<h2>Typical roof replacement costs in Katy, TX</h2>
<p>For a typical two-story Katy home with 2,400 to 3,200 square feet of roof area, architectural shingles are the most common choice and usually land in the low-to-mid five figures. Class 4 impact-resistant shingles cost a bit more, and many Texas insurers offer a premium discount for them. Standing-seam metal costs roughly double but can last 40 to 50 years. Read our full <a href="/blog/roof-replacement-cost-katy-tx/">Katy roof replacement cost guide</a> for a breakdown.</p>
<h2>What the calculator can't see</h2>
<ul><li>Complex roofs with many valleys, dormers and hips take more labor and material</li>
<li>Hidden rotted decking only shows up during tear-off</li>
<li>Code-required upgrades such as drip edge, ventilation and ice-and-water shield</li>
<li>HOA material or color requirements in communities like Cinco Ranch and Cross Creek Ranch</li></ul>
<p>That's why every real estimate starts with a measured inspection. Our <a href="/free-roof-inspection/">free roof inspection</a> includes measurements and an itemized written estimate, or call <a href="tel:{TEL}">{PHONE}</a> to talk with a Katy roofer.</p>"""
    cost_faqs = [
        {"q": "How accurate is this roof cost calculator?", "a": "It's designed to land within a realistic range for most Katy homes, but it's a planning tool, not a quote. Measurements, roof complexity and decking condition can move the final price."},
        {"q": "Does homeowners insurance pay for a new roof?", "a": "If the damage is from a covered peril like hail or wind, insurance typically pays the approved scope minus your deductible. Wear and age aren't covered. A free inspection can tell you whether storm damage is present."},
        {"q": "What is a roofing square?", "a": "A square is 100 square feet of roof surface. Roofers price and order materials by the square."},
        {"q": "Why do steep roofs cost more?", "a": "Steep roofs need safety equipment, roof jacks and slower work, and they have more surface area than their footprint suggests."},
    ]
    tool_page("/tools/roof-cost-calculator/", "Roof Cost Calculator", "Katy Roof Replacement Cost Calculator",
              "Estimate what a new roof costs on your Katy home in under a minute, from 3-tab shingles to standing-seam metal.",
              "Roof Replacement Cost Calculator for Katy, TX (2026)",
              "Free roof replacement cost calculator for Katy, TX homes. Estimate by size, pitch and material, then book a free roof inspection for an exact quote.",
              cost_tool, cost_body, cost_faqs, "brick-homes", "Katy Roof Replacement Cost Calculator")

    # 2. pitch calculator
    pitch_tool = f"""<form data-tool="pitch" onsubmit="return false"><div class="tool-grid">
<div>
<div class="pitch-vis"><svg viewBox="0 0 300 200" role="img" aria-label="Roof pitch diagram">
<line x1="10" y1="190" x2="290" y2="190" stroke="#c7d0dc" stroke-width="2"/>
<polygon data-pitch-tri points="20,190 150,120 280,190" fill="rgba(255,90,31,.15)" stroke="#ff5a1f" stroke-width="3" stroke-linejoin="round"/>
<line data-pitch-rise x1="150" y1="120" x2="150" y2="190" stroke="#0b1626" stroke-dasharray="5 5" stroke-width="2"/>
<text data-pitch-label x="150" y="110" text-anchor="middle" font-family="Plus Jakarta Sans, sans-serif" font-weight="800" font-size="16" fill="#0b1626">6/12</text>
</svg></div>
<div class="range-row"><label for="rise">Roof pitch (rise per 12" run) <output for="rise"></output></label><input type="range" id="rise" name="rise" min="1" max="18" step="1" value="6" data-fmt="/12"></div>
<div class="range-row"><label for="length">House length (ft) <output for="length"></output></label><input type="range" id="length" name="length" min="20" max="120" step="1" value="60" data-fmt=" ft"></div>
<div class="range-row"><label for="width">House width (ft) <output for="width"></output></label><input type="range" id="width" name="width" min="15" max="80" step="1" value="40" data-fmt=" ft"></div>
<div class="range-row"><label for="overhang">Eave overhang (ft) <output for="overhang"></output></label><input type="range" id="overhang" name="overhang" min="0" max="3" step="0.5" value="1.5" data-fmt=" ft"></div>
<div class="range-row"><label>Roof shape</label>{seg('shape', [('gable', 'Simple gable'), ('hip', 'Hip roof'), ('complex', 'Complex / many valleys')], 'hip')}</div>
</div>
<div class="result" aria-live="polite">
<span class="eyebrow" style="color:var(--gold)">Your roof</span>
<div class="big"><span data-out="pitch"></span> = <span data-out="deg"></span></div>
<dl><dt>Slope multiplier</dt><dd data-out="mult"></dd><dt>Roof surface area</dt><dd data-out="area"></dd><dt>Roofing squares</dt><dd data-out="squares"></dd>
<dt>Squares to order</dt><dd data-out="order"></dd><dt>Shingle bundles (3/sq)</dt><dd data-out="bundles"></dd><dt>Walkability</dt><dd data-out="walk"></dd></dl>
<p data-out="walknote" style="font-size:.9rem"></p>
<a class="btn" style="width:100%" href="/free-roof-inspection/">Get it measured for free {icon('arrow')}</a>
<small>Footprint-based estimate. Dormers, multiple roof planes and porches change the total; a measured inspection is the only exact number.</small>
</div></div></form>"""
    pitch_body = f"""<h2>What roof pitch means</h2>
<p>Roof pitch is the number of inches a roof rises for every 12 inches of horizontal run. A 6/12 roof rises 6 inches per foot, about 26.6 degrees. Most homes in Katy subdivisions fall between 6/12 and 9/12, while many older ranch homes near Old Town Katy sit closer to 4/12 or 5/12.</p>
<h2>Why pitch matters for your roof</h2>
<ul><li><strong>Material choice:</strong> asphalt shingles need at least 2/12 with special underlayment, and 4/12 or more is standard. Lower slopes need membrane or low-slope metal systems.</li>
<li><strong>Cost:</strong> steeper roofs have more surface area and need extra safety gear, which raises labor.</li>
<li><strong>Drainage:</strong> steeper slopes shed Katy's heavy rain faster and resist wind-driven water better.</li></ul>
<h2>How to find your pitch</h2>
<p>Safely, from a ladder at the gable end: hold a level horizontally against the roof edge, measure 12 inches along it, then measure straight up to the roof surface. That number is your rise. Or skip the ladder and let us measure it during a <a href="/free-roof-inspection/">free roof inspection</a>. Then plug your numbers into the <a href="/tools/roof-cost-calculator/">roof cost calculator</a>.</p>"""
    pitch_faqs = [
        {"q": "What is the most common roof pitch in Katy?", "a": "Most two-story homes in Katy's master-planned communities have roofs between 6/12 and 9/12, with steeper front gables for curb appeal."},
        {"q": "How many bundles of shingles are in a square?", "a": "Most architectural shingles come three bundles to a square (100 sq ft). Some heavier designer shingles need four or five."},
        {"q": "How much waste should I add?", "a": "About 10% for a simple gable roof, 15% for hip roofs and up to 20% for complex roofs with many valleys and dormers."},
    ]
    tool_page("/tools/roof-pitch-calculator/", "Roof Pitch Calculator", "Roof Pitch &amp; Area Calculator",
              "Convert roof pitch to degrees, find your slope multiplier and estimate roof squares and shingle bundles from your home's footprint.",
              "Roof Pitch Calculator: Degrees, Squares & Bundles | Katy Roofer",
              "Free roof pitch calculator: convert pitch to degrees, get the slope multiplier, roof area, roofing squares and shingle bundles. Made for Katy, TX homeowners.",
              pitch_tool, pitch_body, pitch_faqs, "home-classic", "Roof Pitch & Area Calculator")

    # 3. storm damage checklist
    items = [(3, "Dented gutters, downspouts or roof vents", "Soft metals show hail size and direction"),
             (3, "Shingle pieces or ridge caps in the yard", "A sign of wind damage or lifted shingles"),
             (2, "Granules piled at downspout outlets", "Looks like coarse black sand; shingles losing protection"),
             (3, "Water stains or drips on a ceiling", "Active leak; call soon to avoid decking and drywall damage"),
             (2, "Dented AC condenser fins, mailbox or patio furniture", "Confirms hail hit your property"),
             (2, "Cracked or broken window screens or siding", "Strong indicator of hail impacts"),
             (1, "Neighbors are getting roof work or adjuster visits", "Storms hit whole neighborhoods"),
             (2, "Visible missing, lifted or creased shingles", "Wind breaks the seal strip and shingles start flapping"),
             (1, "Hail 1 inch (quarter-size) or larger was reported", "Check the NWS storm reports for your area")]
    checks = "".join(f'<label><input type="checkbox" value="{w}"><span><strong>{e(t)}</strong><small>{e(s)}</small></span></label>' for w, t, s in items)
    storm_tool = f"""<form data-tool="storm" onsubmit="return false"><div class="tool-grid">
<div><h2 style="font-size:1.5rem">What do you see from the ground?</h2><p style="color:var(--muted)">Stay off the roof. Walk the property and tick everything that applies.</p>
<div class="check-list">{checks}</div>
<div class="range-row" style="margin-top:20px"><label for="age">Roof age (years) <output for="age"></output></label><input type="range" id="age" name="age" min="0" max="30" step="1" value="10" data-fmt=" yrs"></div>
</div>
<div class="result" aria-live="polite">
<span class="eyebrow" style="color:var(--gold)">Damage likelihood</span>
<div class="big" data-out="pct">0%</div>
<div class="meter"><span data-out="meter"></span></div>
<h3 style="color:#fff;margin:0 0 8px" data-out="level"></h3>
<p data-out="advice"></p>
<a class="btn" style="width:100%" href="/free-roof-inspection/">Book a free damage inspection {icon('arrow')}</a>
<small>This self-check is a guide, not a diagnosis. Only an up-close inspection can confirm storm damage. Nothing you enter is saved or sent.</small>
</div></div></form>"""
    storm_body = f"""<h2>Why most storm damage goes unnoticed</h2>
<p>Hail damage on asphalt shingles usually looks like small dark spots where granules were knocked off, or soft "bruises" you can only feel by hand. From the driveway, a hail-damaged roof often looks perfectly fine. The clues are on the softer things around your home: gutters, vents, AC fins and screens.</p>
<h2>What to do after hail or high wind in Katy</h2>
<ol><li><strong>Stay safe.</strong> Avoid downed power lines and don't climb on the roof.</li>
<li><strong>Document.</strong> Photograph dents, debris and any interior water spots with dates.</li>
<li><strong>Prevent more damage.</strong> If water is coming in, call us for an emergency tarp.</li>
<li><strong>Get an inspection.</strong> A <a href="/free-roof-inspection/">free roof inspection</a> confirms whether there's damage worth claiming.</li>
<li><strong>Then decide on a claim.</strong> See our <a href="/blog/texas-roof-insurance-claim-guide-katy/">Texas roof insurance claim guide</a>.</li></ol>
<h2>Watch out for storm chasers</h2>
<p>After big storms, out-of-town crews knock on doors across Katy. Be cautious with anyone who offers to "cover your deductible" (illegal in Texas), pressures you to sign that day, or can't give you a local address. Read <a href="/blog/how-to-choose-a-roofer-in-katy/">how to choose a roofer in Katy</a>, check the <a href="/weather/">live Katy weather page</a> for recent alerts, or call <a href="tel:{TEL}">{PHONE}</a>.</p>"""
    storm_faqs = [
        {"q": "How soon after a storm should I get my roof inspected?", "a": "As soon as practical, ideally within a few weeks. Many Texas policies set deadlines for reporting storm damage, and small breaks can leak with the next rain."},
        {"q": "Can I see hail damage from the ground?", "a": "Usually not on the shingles themselves. Dents in gutters, vents and AC fins are the best ground-level clues."},
        {"q": "Will filing a claim raise my premium?", "a": "Weather claims are generally treated differently from at-fault claims, but every insurer is different. Ask your agent, and get an inspection first so you only file when there's real damage."},
    ]
    tool_page("/tools/storm-damage-checklist/", "Storm Damage Self-Check", "Storm Damage Roof Self-Check",
              "Just had hail or high wind in Katy? Tick what you see from the ground and get an instant damage-likelihood score and next steps.",
              "Storm & Hail Damage Roof Checklist | Katy Roofer",
              "Free storm damage self-check for Katy homeowners. Answer a few questions after hail or wind to see how likely roof damage is, then book a free inspection.",
              storm_tool, storm_body, storm_faqs, "storm-dark", "Storm Damage Roof Self-Check")

    url = "/tools/"
    crumbs = [("Home", "/"), ("Tools", url)]
    cards = [("/tools/roof-cost-calculator/", "calculator", "Roof Cost Calculator", "Estimate a replacement price range for your Katy home by size, pitch and material."),
             ("/tools/roof-pitch-calculator/", "ruler", "Roof Pitch & Area Calculator", "Pitch to degrees, slope multiplier, roof squares and shingle bundles."),
             ("/tools/storm-damage-checklist/", "clipboard", "Storm Damage Self-Check", "After hail or wind, score how likely your roof is to be damaged."),
             ("/weather/", "cloud-rain", "Live Katy Weather", "Current conditions, NWS alerts and a 7-day forecast with roof-risk ratings.")]
    grid = "".join(f'<a class="card" href="{h}" style="text-decoration:none;color:inherit;--d:{i*0.08:.2f}s" data-reveal><div class="ico">{icon(ic)}</div><h3>{e(t)}</h3><p>{e(d)}</p><span class="more">Open {icon("arrow")}</span></a>'
                   for i, (h, ic, t, d) in enumerate(cards))
    main = (B.page_hero(crumbs, "Free Roofing Tools for Katy Homeowners", "Calculators and checklists to help you plan, budget and protect your roof. Free, instant and private.", bg="home-classic", eyebrow="Tools") +
            f'<section class="section"><div class="wrap"><div class="grid g2">{grid}</div></div></section>' + B.final_cta())
    B.add(url, B.page(url, "Free Roofing Calculators & Tools | Katy Roofer",
                      "Free roofing tools for Katy, TX homeowners: roof replacement cost calculator, roof pitch and area calculator, storm damage self-check and live weather.",
                      main, schema=[B.crumbs_schema(crumbs)]), priority="0.7")


# --------------------------------------------------------------------------- about / contact / legal
def build_about():
    url = "/about/"
    crumbs = [("Home", "/"), ("About", url)]
    practices = [("camera", "Photos of everything", "Every inspection and every job is photo-documented, so you never have to take our word for it."),
                 ("shield", "No-pressure advice", "If a repair will do, we say so. If your roof is fine, we say that too."),
                 ("file-check", "Insurance done honestly", "We document damage and meet adjusters, and we follow Texas law: no waived or rebated deductibles."),
                 ("clipboard", "Itemized estimates", "Underlayment, flashing, ventilation, decking and disposal spelled out line by line."),
                 ("home", "Respect for your property", "Tarps over landscaping, daily cleanup and a magnetic nail sweep before we leave."),
                 ("phone", "We pick up the phone", "Questions after the job? Call the same number you called the first time.")]
    cards = "".join(f'<div class="card" data-reveal style="--d:{(i % 3) * 0.08:.2f}s"><div class="ico">{icon(ic)}</div><h3>{e(t)}</h3><p>{e(d)}</p></div>'
                    for i, (ic, t, d) in enumerate(practices))
    main = (B.page_hero(crumbs, "About Katy Roofer", "A local roofing company for Katy homeowners who want straight answers, careful work and a roofer who'll still be here next storm season.", bg="home-porch", eyebrow="Who we are") +
            f"""<section class="section"><div class="wrap split">
<div data-reveal="left"><span class="eyebrow">Our story</span><h2>Roofing the way we'd want it done on our own homes</h2>
<p>Katy Roofer started with a simple idea: homeowners in Katy deserve a roofer who explains things clearly, prices fairly and doesn't disappear when the storm season ends. Too many families here have dealt with door-knockers who rush a claim, rush a roof and leave town.</p>
<p>We do it differently. Every job starts with a <a href="/free-roof-inspection/">free roof inspection</a> and a photo report. We recommend what your roof needs, not what makes the biggest invoice, and we build roofs for Katy's real conditions: heat, humidity, hail and hurricane-force wind.</p>
<p>From Cinco Ranch and Cane Island to Fulshear, Cypress and the Energy Corridor, we're proud to be the Katy roofer neighbors recommend to neighbors.</p>
<a class="btn" href="tel:{TEL}">{icon('phone')} {PHONE}</a></div>
<div class="media">{img('hero-roofer', 'Katy Roofer roofer working on a shingle roof of a brick home')}</div>
</div></section>
<section class="section section-soft"><div class="wrap"><div class="section-head" data-reveal><span class="eyebrow">How we work</span><h2>Six promises on every roof</h2></div>
<div class="grid g3">{cards}</div></div></section>
<section class="section"><div class="wrap"><div class="section-head" data-reveal><span class="eyebrow">What we do</span><h2>Our roofing services</h2></div>
<div class="grid g3">{card_grid_services()}</div></div></section>""" + B.final_cta())
    B.add(url, B.page(url, "About Katy Roofer | Local Roofing Company in Katy, TX",
                      "Meet Katy Roofer, a local roofing company in Katy, TX. Free roof inspections, photo-documented work, honest estimates and storm damage help.",
                      main, schema=[B.crumbs_schema(crumbs)]), priority="0.6")


def build_contact():
    url = "/contact/"
    crumbs = [("Home", "/"), ("Contact", url)]
    main = (B.page_hero(crumbs, "Contact Katy Roofer", "Call, text or send a request. We'll get back to you quickly to schedule your free roof inspection.", bg="suburban-street", eyebrow="Get in touch") +
            f"""<section class="section"><div class="wrap split" style="align-items:start">
<div data-reveal="left"><h2>Talk to a Katy roofer</h2>
<p>Whether it's an active leak, storm damage or you're just planning ahead, we're happy to help. The fastest way to reach us is by phone.</p>
<a class="footer-phone" style="color:var(--ink)!important;font-size:2rem" href="tel:{TEL}">{icon('phone')} {PHONE}</a>
<ul class="checks" style="margin-top:20px">
<li>{icon('pin')}<span><strong>Service area:</strong> Katy, Cinco Ranch, Fulshear, Brookshire, Cypress, Richmond and West Houston</span></li>
<li>{icon('home')}<span><strong>ZIP codes:</strong> 77449, 77450, 77493, 77494 and surrounding</span></li>
<li>{icon('alert')}<span><strong>Active leak?</strong> Call us. We can arrange emergency tarping to prevent further damage.</span></li>
</ul>
<div class="wx-mini" data-wx-mini style="margin-top:28px"><p style="color:#aab8cb">Loading Katy weather…</p></div>
</div>
<div class="form-card" data-reveal="right">{B.lead_form('contact-form', heading='Send us a message', sub='We usually respond the same business day.', full=True)}</div>
</div></section>""")
    B.add(url, B.page(url, "Contact Katy Roofer | Call (512) 297-7580",
                      "Contact Katy Roofer for a free roof inspection, roof repair or replacement quote in Katy, TX. Call (512) 297-7580 or send a request online.",
                      main, schema=[B.crumbs_schema(crumbs), {"@type": "ContactPage", "url": SITE + url}], scripts=("weather",)), priority="0.6")


def build_simple():
    # thank you
    main = f"""<section class="hero hero-page" style="padding:110px 0"><div class="hero-bg" style="background-image:url(/assets/img/home-sunset.webp)"></div>
<div class="wrap" style="text-align:center" data-reveal><span class="eyebrow">Request received</span><h1>Thank you!</h1>
<p class="lead" style="margin:0 auto 28px">Your request is on its way to our team. A Katy roofer will call you shortly to schedule your free roof inspection. Need us sooner?</p>
<div class="hero-actions" style="justify-content:center"><a class="btn" href="tel:{TEL}">{icon('phone')} Call {PHONE}</a><a class="btn btn-outline-light" href="/blog/">Read our roofing guides</a></div></div></section>"""
    B.add("/thank-you/", B.page("/thank-you/", "Thank You | Katy Roofer", "Thanks for contacting Katy Roofer. We'll be in touch shortly.", main, noindex=True), sitemap=False)

    # 404
    main = f"""<section class="hero hero-page" style="padding:110px 0"><div class="hero-bg" style="background-image:url(/assets/img/storm-clouds.webp)"></div>
<div class="wrap" style="text-align:center"><span class="eyebrow">Error 404</span><h1>This page blew away</h1>
<p class="lead" style="margin:0 auto 28px">The page you're looking for doesn't exist or has moved. Let's get you back on solid roofing.</p>
<div class="hero-actions" style="justify-content:center"><a class="btn" href="/">Back to home</a><a class="btn btn-outline-light" href="/free-roof-inspection/">Free roof inspection</a></div></div></section>"""
    B.write("/404.html", B.page("/404.html", "Page Not Found | Katy Roofer", "This page could not be found.", main, noindex=True))

    legal = {
        "/privacy-policy/": ("Privacy Policy", f"""<p>Last updated: {B.fmt_date(B.TODAY.isoformat())}</p>
<p>This Privacy Policy explains how Katy Roofer ("we", "us") collects and uses information through rooferkaty.com.</p>
<h2>Information we collect</h2><p>When you submit a form, we collect the details you provide, such as your name, phone number, email address, property address and message, along with the page you submitted from, the time, and your IP address for spam prevention.</p>
<h2>How we use it</h2><p>We use your information only to respond to your request, schedule inspections, provide estimates and service, and keep basic business records. We may call or text you about your request.</p>
<h2>Sharing</h2><p>We do not sell or rent your personal information. We share it only with service providers who help us operate (such as email delivery), when required by law, or with your permission (for example, with your insurance adjuster at your request).</p>
<h2>Third-party services</h2><p>Our weather pages load forecast data from Open-Meteo and alerts from the National Weather Service, and our pages load fonts from Google Fonts. Those services may receive your IP address as part of normal web requests. Our calculators run entirely in your browser; nothing you enter in them is stored or sent.</p>
<h2>Cookies</h2><p>This site does not use advertising or tracking cookies.</p>
<h2>Your choices</h2><p>To ask us to update or delete information you've sent us, call {PHONE}.</p>
<h2>Changes</h2><p>We may update this policy from time to time. The date at the top shows the latest version.</p>"""),
        "/terms/": ("Terms of Use", f"""<p>Last updated: {B.fmt_date(B.TODAY.isoformat())}</p>
<p>By using rooferkaty.com you agree to these terms.</p>
<h2>Informational content</h2><p>Articles, calculators, cost ranges and weather information on this site are for general information only. They are not quotes, professional engineering advice, insurance advice or legal advice. Weather data is provided by third parties and may be delayed or inaccurate; always follow official National Weather Service warnings.</p>
<h2>Estimates and services</h2><p>Any roofing work is governed by a separate written agreement. Prices shown on this site are planning ranges and may differ from your written estimate.</p>
<h2>Insurance</h2><p>Katy Roofer is a roofing contractor, not a public adjuster or insurance company. Coverage decisions are made by your insurer. In accordance with Texas Business &amp; Commerce Code §27.02, we do not waive, rebate or pay any portion of an insurance deductible.</p>
<h2>Intellectual property</h2><p>Site content is owned by Katy Roofer or used under license. Photos are licensed stock images and may not depict our own projects.</p>
<h2>Limitation of liability</h2><p>The site is provided "as is" without warranties of any kind. To the extent permitted by law, Katy Roofer is not liable for damages arising from use of the site.</p>
<h2>Contact</h2><p>Questions about these terms? Call {PHONE}.</p>"""),
    }
    for url, (name, body) in legal.items():
        crumbs = [("Home", "/"), (name, url)]
        main = (B.page_hero(crumbs, name, f"{name} for rooferkaty.com.", bg="home-classic") +
                f'<section class="section"><div class="wrap"><article class="prose" style="max-width:820px">{body}</article></div></section>')
        B.add(url, B.page(url, f"{name} | Katy Roofer", f"{name} for Katy Roofer (rooferkaty.com), a roofing company serving Katy, TX.", main,
                          schema=[B.crumbs_schema(crumbs)]), priority="0.2")


def build_main():
    build_inspection()
    build_services()
    build_areas()
    build_weather()
    build_tools()
    build_blog()
    build_about()
    build_contact()
    build_simple()
