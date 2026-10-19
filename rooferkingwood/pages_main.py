"""Every page except the homepage."""
import build as B
from build import e, icon, img, TEL, PHONE, SITE


def service_tiles(exclude=None, cls="g4"):
    out = ""
    for i, s in enumerate(x for x in B.SERVICES if x["slug"] != exclude):
        out += (f'<article class="tile" data-reveal style="--d:{(i % 4) * 0.06:.2f}s"><div class="ico">{icon(s.get("icon", "home"))}</div>'
                f'<h3><a href="/services/{s["slug"]}/">{e(s["name"])}</a></h3><p>{e(s["short"])}</p>'
                f'<span class="link-arrow">Learn more {icon("arrow")}</span></article>')
    return f'<div class="grid {cls}">{out}</div>'


def post_card(p, i=0):
    return (f'<article class="post-card" data-reveal style="--d:{(i % 3) * 0.08:.2f}s"><div class="img">{img(p["image"], p.get("image_alt", p["h1"]))}</div>'
            f'<div class="body"><div class="meta"><span class="cat">{e(p.get("category", "Guide"))}</span><span>{B.fmt_date(p["date"])}</span></div>'
            f'<h3><a href="/blog/{p["slug"]}/">{e(p["h1"])}</a></h3><p>{e(p["excerpt"])}</p>'
            f'<span class="link-arrow" style="margin-top:auto">Read · {p.get("read_minutes", 6)} min {icon("arrow")}</span></div></article>')


def prose_page(item, crumbs, aside, kicker, meta="", after_body=""):
    body = B.prep_body(item["body"])
    lead = f'<div class="lead-img">{img(item["image"], item.get("image_alt", item["h1"]))}</div>'
    return (B.page_hero(crumbs, e(item["h1"]), item["intro"], image=item["image"], alt=item.get("image_alt", ""), kicker=kicker, meta=meta) +
            f'<section class="section"><div class="wrap layout"><article class="prose">{lead}{body}{after_body}</article>'
            f'<aside class="aside">{aside}</aside></div></section>')


def links_box(title, items):
    lis = "".join(f'<li><a href="{h}">{e(l)} {icon("arrow")}</a></li>' for h, l in items)
    return f'<div class="box"><h3>{e(title)}</h3><ul>{lis}</ul></div>'


# --------------------------------------------------------------------------- services
def build_services():
    for s in B.SERVICES:
        url = f"/services/{s['slug']}/"
        crumbs = [("Home", "/"), ("Services", "/services/"), (s["name"], url)]
        bullets = "".join(f"<li>{icon('check')}<span>{e(b)}</span></li>" for b in s.get("bullets", []))
        others = [("/free-roof-inspection/", "Free Roof Inspection")] + [(f"/services/{o['slug']}/", o["name"]) for o in B.SERVICES if o is not s]
        aside = (f'<div class="box"><h3>What\'s included</h3><ul class="ticks">{bullets}</ul></div>' + B.box_call() + links_box("Other services", others))
        main = prose_page(s, crumbs, aside, kicker=f"Kingwood roofing · {s['name']}")
        main += B.faq_html(s["faqs"], f"{s['name']}: common questions")
        main += B.form_section("svc-form")
        main += B.closer()
        schema = [B.crumbs_schema(crumbs), B.faq_schema(s["faqs"]),
                  {"@type": "Service", "name": s["h1"], "serviceType": s["name"], "url": SITE + url, "description": s["description"],
                   "provider": {"@id": SITE + "/#business"}, "areaServed": {"@type": "City", "name": "Kingwood, TX"}}]
        B.add(url, B.page(url, s["title"], s["description"], main, active="/services/", schema=schema, og_image=s["image"] + ".webp"), priority="0.9")

    url = "/services/"
    crumbs = [("Home", "/"), ("Services", url)]
    main = (B.page_hero(crumbs, "Roofing Services in Kingwood, TX", "Every roofing service a Kingwood home or business needs, starting with a free, photo-documented roof inspection.",
                        image="roofer-work", kicker="What we do") +
            f"""<section class="section"><div class="wrap"><div class="head" data-reveal><span class="kicker">Eight services, one standard</span><h2>Repair, replace, restore after storms and fallen trees</h2>
<p>We handle everything from a single cracked pipe boot to a complete tear-off on a large two-story home or a light commercial building. Pick a service to see how we approach it, or <a href="/free-roof-inspection/">book a free inspection</a> and we'll tell you what your roof actually needs.</p></div>
{service_tiles()}</div></section>""" + B.form_section("services-form") + B.closer())
    B.add(url, B.page(url, "Roofing Services in Kingwood, TX | (512) 297-7580",
                      "Roof repair, replacement, storm, hail and tree damage, insurance claim help, metal, commercial roofing and gutters in Kingwood, TX. Free roof inspections.",
                      main, schema=[B.crumbs_schema(crumbs)]), priority="0.8")


# --------------------------------------------------------------------------- areas
def build_areas():
    for a in B.AREAS:
        url = f"/areas/{a['slug']}/"
        crumbs = [("Home", "/"), ("Service Areas", "/areas/"), (a["name"], url)]
        hoods = "".join(f"<span>{e(n)}</span>" for n in a.get("neighborhoods", []))
        others = [("/", "Kingwood, TX")] + [(f"/areas/{o['slug']}/", o["name"]) for o in B.AREAS if o is not a]
        aside = (f"""<div class="box"><h3>{e(a['name'])} at a glance</h3><ul class="ticks">
<li>{icon('pin')}<span><strong>County:</strong> {e(a.get('county', ''))}</span></li>
<li>{icon('home')}<span><strong>ZIP codes:</strong> {e(a.get('zips', ''))}</span></li>
<li>{icon('clock')}<span>{e(a.get('drive', ''))}</span></li></ul>
<div class="villages" style="gap:6px">{hoods}</div></div>""" + B.box_call() + links_box("Nearby areas", others))
        main = prose_page(a, crumbs, aside, kicker=f"Service area · {a['name']}, TX")
        main += (f'<section class="section bg-cream"><div class="wrap"><div class="head" data-reveal><span class="kicker">Services in {e(a["name"])}</span>'
                 f'<h2>What we do in {e(a["name"])}</h2></div>{service_tiles()}</div></section>')
        main += B.faq_html(a["faqs"], f"Roofing in {a['name']}: FAQs", bg="")
        main += B.form_section("area-form")
        main += B.closer()
        schema = [B.crumbs_schema(crumbs), B.faq_schema(a["faqs"]),
                  {"@type": "Service", "name": a["h1"], "serviceType": "Roofing", "url": SITE + url, "provider": {"@id": SITE + "/#business"},
                   "areaServed": {"@type": "City", "name": a["name"] + ", TX"}}]
        B.add(url, B.page(url, a["title"], a["description"], main, active="/areas/", schema=schema, og_image=a["image"] + ".webp"), priority="0.8")

    url = "/areas/"
    crumbs = [("Home", "/"), ("Service Areas", url)]
    cards = "".join(f'<a class="area-card" href="/areas/{a["slug"]}/"><small>{e(a.get("county", ""))} County · {e(a.get("zips", ""))}</small><b>{e(a["name"])}</b><p>{e(a["short"])}</p></a>'
                    for a in B.AREAS)
    villages = "".join(f"<span>{e(v)}</span>" for v in B.VILLAGES)
    main = (B.page_hero(crumbs, "Areas We Serve Around Kingwood, TX", "Based in Kingwood and working around Lake Houston, from the San Jacinto River to Crosby and up US-59 to New Caney.",
                        image="tree-street", kicker="Service areas") +
            f"""<section class="section"><div class="wrap cols top">
<div data-reveal><span class="kicker">Home base</span><h2>Kingwood, TX: every village</h2>
<p>Kingwood is where we work most. We cover 77339, 77345 and the Kingwood part of 77346, from the original villages along Kingwood Drive to Kings Mill and Kingwood Lakes on the Montgomery County side.</p>
<p>Because almost every village has its own deed restrictions and architectural review, we keep track of the shingle colors and materials each one tends to approve, so your new roof gets signed off the first time.</p>
<a class="btn" href="/free-roof-inspection/">Free inspection in Kingwood {icon('arrow')}</a></div>
<div data-reveal style="--d:.1s"><div class="villages">{villages}</div></div>
</div></section>
<section class="section bg-pine"><div class="wrap"><div class="head" data-reveal><span class="kicker light">Nearby communities</span><h2>Around Lake Houston</h2>
<p>Each town has its own housing stock, lot sizes and storm exposure. Here's what we see in each.</p></div>
<div class="area-cards" data-reveal>{cards}</div></div></section>""" + B.form_section("areas-form") + B.closer())
    B.add(url, B.page(url, "Roofing Service Areas Near Kingwood, TX | Kingwood Roofers",
                      "Kingwood Roofers serves every Kingwood village plus Atascocita, Humble, Porter, New Caney, Huffman and Crosby. Free roof inspections around Lake Houston.",
                      main, schema=[B.crumbs_schema(crumbs)]), priority="0.7")


# --------------------------------------------------------------------------- blog
def build_blog():
    for p in B.POSTS:
        url = f"/blog/{p['slug']}/"
        crumbs = [("Home", "/"), ("Blog", "/blog/"), (p["h1"], url)]
        meta = (f'<div class="post-meta"><span>{icon("calendar")} {B.fmt_date(p["date"])}</span><span>{icon("clock")} {p.get("read_minutes", 6)} min read</span>'
                f'<span>{icon("users")} Kingwood Roofers team</span></div>')
        related = [x for x in B.POSTS if x is not p and x.get("category") == p.get("category")]
        related += [x for x in B.POSTS if x is not p and x not in related]
        aside = ('<div class="box toc"><h3>In this article</h3><ul></ul></div>' + B.box_call() +
                 links_box("Roofing services", [("/free-roof-inspection/", "Free Roof Inspection")] + [(f"/services/{s['slug']}/", s["name"]) for s in B.SERVICES[:5]]) +
                 links_box("Free tools", B.NAV_TOOLS))
        author = (f'<div class="author" data-reveal><div class="ico">{B.CREST}</div>'
                  f'<div><strong style="font-family:var(--serif);color:var(--ink);font-size:1.1rem">Written by the Kingwood Roofers team</strong><p>Local roofers serving Kingwood, Atascocita, Humble and the Lake Houston area. '
                  f'Questions about your roof? Call <a href="tel:{TEL}">{PHONE}</a> or <a href="/free-roof-inspection/">book a free inspection</a>.</p></div></div>')
        main = prose_page(p, crumbs, aside, kicker=p.get("category", "Guide"), meta=meta, after_body=author)
        main += B.faq_html(p["faqs"], "Frequently asked questions")
        main += (f'<section class="section"><div class="wrap"><div class="head" data-reveal><span class="kicker">Keep reading</span><h2>More Kingwood roofing guides</h2></div>'
                 f'<div class="grid g3">{"".join(post_card(x, i) for i, x in enumerate(related[:3]))}</div></div></section>')
        main += B.closer()
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
    rows = "".join(f"""<article class="post-row" data-reveal><div class="img">{img(p['image'], p.get('image_alt', p['h1']))}</div>
<div><div class="meta"><span class="cat">{e(p.get('category', 'Guide'))}</span><span>{B.fmt_date(p['date'])}</span><span>{p.get('read_minutes', 6)} min read</span></div>
<h3><a href="/blog/{p['slug']}/">{e(p['h1'])}</a></h3><p>{e(p['excerpt'])}</p><span class="link-arrow">Read the guide {icon('arrow')}</span></div></article>""" for p in B.POSTS)
    main = (B.page_hero(crumbs, "Kingwood Roofing Blog", "Practical guides for Kingwood homeowners on pine trees and roofs, storm prep, insurance claims, HOA approvals, materials and costs.",
                        image="forest-home", kicker="Guides & advice") +
            f'<section class="section"><div class="wrap">{rows}</div></section>' + B.closer())
    items = {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{SITE}/blog/{p['slug']}/"} for i, p in enumerate(B.POSTS)]}
    B.add(url, B.page(url, "Kingwood Roofing Blog: Guides for Kingwood, TX Homeowners",
                      "Roofing advice from Kingwood roofers: pine tree damage, hurricane prep, replacement costs, HOA approval, hail, insurance claims and maintenance.",
                      main, schema=[B.crumbs_schema(crumbs), items]), lastmod=B.POSTS[0]["date"], priority="0.7")


# --------------------------------------------------------------------------- free inspection
INSPECTION_FAQS = [
    {"q": "Why is your roof inspection free?", "a": "Because homeowners shouldn't have to pay to find out whether they have a problem. If your roof needs work, we hope you'll hire us. If it doesn't, we'll tell you so."},
    {"q": "How long does a free roof inspection take?", "a": "Most Kingwood homes take 30 to 60 minutes, depending on roof size, pitch, tree cover and whether we check the attic. We review the photos with you afterward."},
    {"q": "Do I need to be home?", "a": "It helps for the attic check and walkthrough, but it isn't required for the exterior inspection. We'll send the photos and findings either way."},
    {"q": "Will an inspection affect my insurance?", "a": "No. A contractor inspection is not a claim. You decide whether to file, and our findings help you make that decision with real information."},
    {"q": "Is it useful when buying or selling a home in Kingwood?", "a": "Yes. A roofer's inspection goes deeper on the roof than a general home inspection, and the photo report helps in negotiations and future village ACC applications."},
]


def build_inspection():
    url = "/free-roof-inspection/"
    crumbs = [("Home", "/"), ("Free Roof Inspection", url)]
    checks = [("cloud-hail", "Hail & impact", "Bruised or cracked shingles, granule loss, dented vents and soft metals."),
              ("wind", "Wind damage", "Lifted, creased or missing shingles and ridge caps; broken seal strips."),
              ("tree", "Trees & debris", "Limb strikes, needle-packed valleys, overhanging branches and rodent damage."),
              ("layers", "Flashing & valleys", "Step, wall, chimney and valley flashing; exposed nails and failed sealant."),
              ("droplets", "Leaks & moisture", "Attic stains, damp insulation, rusted nails and soft decking."),
              ("leaf", "Algae, moss & gutters", "Black streaks, moss mats, clogged gutters, fascia rot and overflow staining.")]
    tiles = "".join(f'<div class="tile" data-reveal style="--d:{(i % 3) * 0.08:.2f}s"><div class="ico">{icon(ic)}</div><h3>{e(t)}</h3><p>{e(d)}</p></div>'
                    for i, (ic, t, d) in enumerate(checks))
    main = f"""
<section class="hero"><div class="wrap">
<div>{B.crumbs_html(crumbs).replace('class="crumbs"', 'class="crumbs" style="color:var(--muted)"').replace('<a ', '<a style="color:var(--maroon)" ')}
<span class="kicker">$0 · No obligation</span>
<h1>Free Roof Inspections in <em>Kingwood, TX</em></h1>
<p class="lead">A local roofer will inspect your roof from ridge to gutter, photograph every issue and give you an honest, written recommendation, at no cost.</p>
<div class="proofs"><div>{icon('camera')}<span><b>Photo report</b>Yours to keep</span></div><div>{icon('file-check')}<span><b>Written findings</b>Plain English</span></div>
<div>{icon('shield')}<span><b>Storm documentation</b>For your insurer</span></div></div>
</div>
<div class="form-card">{B.lead_form('inspect-form', heading='Book your free roof inspection', sub="Pick a time that works. We'll confirm by phone.", full=True, service='Free roof inspection', hlevel='h2')}</div>
</div></section>

<section class="section"><div class="wrap">
<div class="head" data-reveal><span class="kicker">What we check</span><h2>A six-point inspection, not a glance from the driveway</h2>
<p>Under Kingwood's tree canopy, the evidence hides in valleys, behind debris and in the attic. That's where we look.</p></div>
<div class="grid g3">{tiles}</div></div></section>

<section class="section bg-pine"><div class="wrap">
<div class="head center" data-reveal><span class="kicker light">How it works</span><h2>From booking to photo report</h2></div>
<div class="process" style="--pc:#fff">
<div class="pstep" data-reveal><div class="dot">1</div><h3>Book</h3><p style="color:#b9cdc2">Use the form or call {PHONE}. Tell us about leaks, storms or fallen limbs.</p></div>
<div class="pstep" data-reveal style="--d:.08s"><div class="dot">2</div><h3>We inspect</h3><p style="color:#b9cdc2">Every slope, flashing, vents and gutters, plus the attic if you're home.</p></div>
<div class="pstep" data-reveal style="--d:.16s"><div class="dot">3</div><h3>You see photos</h3><p style="color:#b9cdc2">We review close-ups with you and send them for your records.</p></div>
<div class="pstep" data-reveal style="--d:.24s"><div class="dot">4</div><h3>Honest advice</h3><p style="color:#b9cdc2">No damage? We say so. Repair? We quote it. Storm damage? We explain the claim process.</p></div>
<div class="pstep" data-reveal style="--d:.32s"><div class="dot">5</div><h3>Your call</h3><p style="color:#b9cdc2">No pressure and no expiring "today only" pricing. Decide on your own time.</p></div>
</div></div></section>

<section class="section"><div class="wrap cols">
<div class="photo offset-frame" data-reveal>{img('roofer-work', 'Roofer on a shingle roof during a free roof inspection in Kingwood')}</div>
<div data-reveal style="--d:.1s"><span class="kicker">When to book</span><h2>Good times to get a free roof inspection</h2>
<ul class="ticks">
<li>{icon('check')}<span><strong>After hail, high wind or a limb strike</strong>, even if nothing looks wrong from the ground</span></li>
<li>{icon('check')}<span><strong>Before hurricane season</strong>, when loose shingles and weak flashing can still be fixed</span></li>
<li>{icon('check')}<span><strong>Roof older than 10 years</strong>, especially under heavy tree cover</span></li>
<li>{icon('check')}<span><strong>Buying or selling a home</strong>, so you know exactly what you're getting</span></li>
<li>{icon('check')}<span><strong>A stain on a ceiling or wall</strong>, to find the source before it spreads</span></li>
</ul>
<p>Not sure? Run the <a href="/tools/storm-damage-checklist/">storm damage self-check</a> or check the <a href="/weather/">Kingwood storm desk</a> for recent severe weather.</p></div>
</div></section>
{B.faq_html(INSPECTION_FAQS, "Free roof inspection FAQs")}
{B.closer("Book your free roof inspection today")}"""
    schema = [B.crumbs_schema(crumbs), B.faq_schema(INSPECTION_FAQS),
              {"@type": "Service", "name": "Free Roof Inspection in Kingwood, TX", "serviceType": "Roof inspection", "url": SITE + url,
               "provider": {"@id": SITE + "/#business"}, "areaServed": {"@type": "City", "name": "Kingwood, TX"},
               "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}]
    B.add(url, B.page(url, "Free Roof Inspection Kingwood, TX | (512) 297-7580",
                      "Book a free roof inspection in Kingwood, TX. Local roofers check for hail, wind, tree and leak damage and give you a photo report. No cost, no obligation.",
                      main, schema=schema, og_image="roofer-work.webp"), priority="0.9")


# --------------------------------------------------------------------------- weather
WEATHER_FAQS = [
    {"q": "Where does this Kingwood weather data come from?", "a": "Current conditions, the hourly outlook and the 7-day forecast come from Open-Meteo, which blends national weather models including NOAA's. Active alerts come straight from the National Weather Service feed for Kingwood's coordinates (Houston/Galveston office)."},
    {"q": "What does the roof risk rating mean?", "a": "It's our plain read of each day's forecast: thunderstorms with possible hail or gusts of 50 mph or more rate High; ordinary thunderstorms, heavy showers or gusts above 35 mph rate Moderate. It's informational, not an official warning."},
    {"q": "How strong does wind need to be to drop pine limbs?", "a": "Dead or weakened limbs can fall in gusts of 30 to 40 mph, and healthy limbs and whole trees come down in stronger thunderstorm and tropical gusts, especially when soil is saturated. That's why gusts weigh heavily in our risk rating."},
    {"q": "What should I do after a severe storm passes?", "a": "Stay off the roof. From the ground, look for missing shingles, limbs on the roof, dented gutters and granules at downspouts. Photograph anything you see, check ceilings for stains and book a free roof inspection."},
]


def build_weather():
    url = "/weather/"
    crumbs = [("Home", "/"), ("Storm Desk", url)]
    main = f"""{B.page_hero(crumbs, "Kingwood, TX Weather &amp; Storm Desk", "Live conditions, National Weather Service alerts, a 24-hour wind and rain outlook and a 7-day forecast for Kingwood, with a daily roof-risk rating.", image="lightning", alt="Lightning over a dark sky near Kingwood", kicker="Live weather")}
<section class="section tight"><div class="wrap">
<div data-wx-alerts class="alert-strip" data-reveal><h3>Checking National Weather Service alerts for Kingwood…</h3></div>
</div></section>
<section class="section tight bg-pine"><div class="wrap">
<div class="desk" data-wx-desk data-wx-full>
<div class="desk-now"><span class="kicker light">Right now in Kingwood</span><p class="loading">Loading current conditions…</p></div>
<div class="desk-days">{''.join('<div class="desk-day loading">·</div>' for _ in range(5))}</div>
<div class="desk-foot"><span data-wx-alertline>Checking alerts…</span><span data-wx-updated></span></div>
</div></div></section>
<section class="section"><div class="wrap">
<div class="head" data-reveal><span class="kicker">Next 24 hours</span><h2>Hourly wind gusts and rain chance</h2>
<p>Gusts above about 35 mph are when weak pine limbs start coming down; above 50 mph, shingles and whole trees are at risk.</p></div>
<div class="chart-tabs" role="group" aria-label="Chart"><button type="button" aria-pressed="true" data-chart="gust">Wind gusts (mph)</button><button type="button" aria-pressed="false" data-chart="rain">Rain chance (%)</button></div>
<div class="hourly" data-wx-hourly><div class="skeleton" style="grid-column:1/-1"></div></div>
<div class="hourly-x" data-wx-hours></div>
<div class="chart-legend"><span><i style="background:var(--maroon)"></i>Wind gust</span><span><i style="background:#6c8fb3"></i>Rain chance</span><span><i style="background:var(--bad)"></i>35+ mph limb-risk gusts</span></div>
</div></section>
<section class="section bg-cream"><div class="wrap">
<div class="head" data-reveal><span class="kicker">7-day forecast</span><h2>Kingwood 7-day weather forecast</h2>
<p data-wx-outlook>Loading this week's roof outlook…</p></div>
<div class="fc" data-wx-forecast>{''.join('<div class="skeleton"></div>' for _ in range(7))}</div>
<div class="prose" style="margin-top:36px" data-reveal><table><thead><tr><th>Day</th><th>Conditions</th><th>High / Low</th><th>Rain chance</th><th>Wind / Gusts</th><th>UV</th></tr></thead>
<tbody data-wx-table><tr><td colspan="6">Loading…</td></tr></tbody></table>
<p style="font-size:.9rem;color:var(--muted)">Forecast data: <a href="https://open-meteo.com/" rel="noopener" target="_blank">Open-Meteo</a> (CC BY 4.0). Alerts: <a href="https://www.weather.gov/hgx/" rel="noopener" target="_blank">National Weather Service Houston/Galveston</a>. Times in Central Time. Roof-risk ratings are informational, not official warnings.</p></div>
</div></section>
<section class="section"><div class="wrap">
<div class="head" data-reveal><span class="kicker">Be ready</span><h2>Protect your roof when storms are in the forecast</h2></div>
<div class="grid g3">
<div class="tile" data-reveal><div class="ico">{icon('camera')}</div><h3>Before the storm</h3><p>Take dated photos of each roof slope, clear gutters and valleys of needles, have dead limbs over the roof trimmed and tie down patio furniture.</p></div>
<div class="tile" data-reveal style="--d:.08s"><div class="ico">{icon('alert')}</div><h3>During the storm</h3><p>Park cars in the garage, stay away from windows and rooms under big trees, and catch any drips. Never climb on a wet roof.</p></div>
<div class="tile" data-reveal style="--d:.16s"><div class="ico">{icon('clipboard')}</div><h3>After the storm</h3><p>Walk the property, photograph limbs, dents and debris, run the <a href="/tools/storm-damage-checklist/">storm damage self-check</a> and book a <a href="/free-roof-inspection/">free roof inspection</a>.</p></div>
</div></div></section>
<section class="section bg-sand"><div class="wrap cols">
<div data-reveal><span class="kicker">Kingwood's roofing seasons</span><h2>What each season means for your roof</h2>
<div class="prose"><table><thead><tr><th>Season</th><th>Main roof threat</th><th>What to do</th></tr></thead><tbody>
<tr><td>Mar–Jun</td><td>Hail, severe thunderstorms, straight-line wind</td><td>Inspect after every hail report</td></tr>
<tr><td>Jun–Nov</td><td>Tropical storms, hurricanes, falling trees</td><td>Pre-season inspection, trim limbs over the roof</td></tr>
<tr><td>Jul–Sep</td><td>Heat, UV and attic heat build-up</td><td>Check ventilation, pipe boots and sealants</td></tr>
<tr><td>Oct–Feb</td><td>Needle drop, cold fronts with wind, occasional freezes</td><td>Clear gutters and valleys, check flashing</td></tr>
</tbody></table></div>
<p>Read the <a href="/blog/hurricane-season-roof-prep-kingwood-tx/">hurricane season roof prep guide</a> and <a href="/blog/pine-trees-and-your-roof-kingwood/">pine trees and your roof</a>.</p></div>
<div class="photo offset-frame" data-reveal style="--d:.1s">{img('storm-sky', 'Dark storm clouds building over the Kingwood area')}</div>
</div></section>
{B.faq_html(WEATHER_FAQS, "Kingwood weather & roof FAQs", bg="")}
{B.closer("Storm just passed? Get a free roof inspection")}"""
    B.add(url, B.page(url, "Kingwood, TX Weather: Live Forecast, Alerts & Roof Risk",
                      "Live Kingwood, TX weather: current conditions, NWS alerts, hourly wind gusts and a 7-day forecast with a daily roof-risk rating. Free inspections after storms.",
                      main, active="/weather/", schema=[B.crumbs_schema(crumbs), B.faq_schema(WEATHER_FAQS)], scripts=("weather",), og_image="lightning.webp"), priority="0.8")


# --------------------------------------------------------------------------- tools
def seg(name, options, checked):
    return '<div class="seg">' + "".join(
        f'<label><input type="radio" name="{name}" value="{v}"{" checked" if v == checked else ""}><span>{e(l)}</span></label>' for v, l in options) + "</div>"


def tool_page(url, crumbs_name, h1, lead, title, desc, tool_html, body_html, faqs, image, app_name):
    crumbs = [("Home", "/"), ("Tools", "/tools/"), (crumbs_name, url)]
    others = "".join(f'<article class="tile" data-reveal><div class="ico">{icon(ic)}</div><h3><a href="{h}">{e(l)}</a></h3><span class="link-arrow">Open tool {icon("arrow")}</span></article>'
                     for (h, l), ic in zip(B.NAV_TOOLS, ["calculator", "ruler", "clipboard", "hourglass"]) if h != url)
    main = (B.page_hero(crumbs, h1, lead, image=image, kicker="Free homeowner tool") +
            f'<section class="section bg-cream"><div class="wrap"><div class="tool" data-reveal>{tool_html}</div></div></section>' +
            f'<section class="section"><div class="wrap layout"><article class="prose">{body_html}{B.cta_band()}</article>'
            f'<aside class="aside">{B.box_call()}</aside></div></section>' +
            B.faq_html(faqs, "Questions about this tool") +
            f'<section class="section"><div class="wrap"><div class="head"><span class="kicker">Keep planning</span><h2>More free tools</h2></div><div class="grid g3">{others}</div></div></section>' +
            B.closer())
    schema = [B.crumbs_schema(crumbs), B.faq_schema(faqs),
              {"@type": "WebApplication", "name": app_name, "url": SITE + url, "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any",
               "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": SITE + "/#business"}}]
    B.add(url, B.page(url, title, desc, main, active="/tools/", schema=schema, scripts=("tools",)), priority="0.7")


def build_tools():
    # 1. cost calculator
    cost_tool = f"""<form data-tool="cost" onsubmit="return false"><div class="tool-grid">
<div>
<h2 style="font-size:1.5rem">Your home</h2>
<div class="field-row"><label for="sqft">Living area <output for="sqft"></output></label><input type="range" id="sqft" name="sqft" min="1000" max="6000" step="50" value="2800" data-fmt=" sq ft"></div>
<div class="field-row"><span class="lbl">Stories</span>{seg('stories', [('1', '1 story'), ('2', '2 stories'), ('3', '3 stories')], '2')}</div>
<div class="field-row"><span class="lbl">Roof pitch</span>{seg('pitch', [('low', 'Low (≤4/12)'), ('med', 'Medium (5–7/12)'), ('steep', 'Steep (8/12+)')], 'med')}</div>
<div class="field-row"><span class="lbl">Roofing material</span>{seg('material', [('3tab', '3-tab shingle'), ('arch', 'Architectural'), ('class4', 'Class 4 impact'), ('metal', 'Standing-seam metal'), ('stone', 'Stone-coated steel'), ('tile', 'Concrete tile')], 'arch')}</div>
<div class="field-row"><span class="lbl">Layers to tear off</span>{seg('layers', [('1', '1 layer'), ('2', '2 layers'), ('shake', 'Old wood shake')], '1')}</div>
<div class="field-row"><label for="deck">Decking to replace <output for="deck"></output></label><input type="range" id="deck" name="deck" min="0" max="50" step="5" value="10" data-fmt="%"></div>
<div class="field-row"><span class="lbl">Tree cover over the driveway / roof</span>{seg('trees', [('0', 'Open'), ('1', 'Some trees'), ('2', 'Heavy canopy')], '1')}</div>
</div>
<div class="result" aria-live="polite">
<span class="kicker">Estimated installed cost</span>
<div class="big" data-out="range">—</div>
<dl><dt>Material</dt><dd data-out="mat"></dd><dt>Est. roof area</dt><dd data-out="area"></dd><dt>Roofing squares</dt><dd data-out="squares"></dd>
<dt>Per square (100 sq ft)</dt><dd data-out="persq"></dd><dt>Typical lifespan here</dt><dd data-out="life"></dd></dl>
<a class="btn btn-brass btn-block" href="/free-roof-inspection/">Get an exact quote, free {icon('arrow')}</a>
<small>Planning range for the Kingwood / Lake Houston market in 2026, not a quote. Measurements, roof complexity, ventilation, flashing, code items and access around trees change the price. Insurance-approved claims are priced from your adjuster's scope.</small>
</div></div></form>"""
    cost_body = f"""<h2>How this roof cost calculator works</h2>
<p>The calculator turns your living area into an estimated roof area. It divides by the number of stories to approximate the footprint, adds about 12% for overhangs and multiplies by a slope factor for your pitch. Then it applies a 2026 installed-price range per square foot for your material, adjusts labor for steep or multi-story roofs, adds tear-off for extra layers or old wood shake, adds decking replacement, and allows a little extra for tree-heavy lots where debris protection and material handling take longer.</p>
<h2>Typical roof replacement costs in Kingwood, TX</h2>
<p>A typical Kingwood two-story has roughly 2,200 to 3,400 square feet of roof area. Architectural shingles are the most common choice and usually land in the low-to-mid five figures. Class 4 impact-resistant shingles cost a little more, and many Texas insurers offer a premium discount for them. Standing-seam metal costs roughly twice as much but can last 40 years or more. Our <a href="/blog/roof-replacement-cost-kingwood-tx/">Kingwood roof replacement cost guide</a> breaks it down further.</p>
<h2>What the calculator can't see</h2>
<ul><li>Complex roofs with many valleys, dormers and hips take more labor and material</li>
<li>Rotted decking under needle-packed valleys only shows up during tear-off</li>
<li>Code items such as drip edge, ventilation upgrades and ice-and-water membrane in valleys</li>
<li>Village association color and material requirements</li></ul>
<p>That's why every real estimate starts with a measured inspection. A <a href="/free-roof-inspection/">free roof inspection</a> includes measurements and an itemized estimate, or call <a href="tel:{TEL}">{PHONE}</a>.</p>"""
    cost_faqs = [
        {"q": "How accurate is this roof cost calculator?", "a": "It's built to land in a realistic range for most Kingwood homes, but it's a planning tool, not a quote. Measurements, roof complexity and decking condition move the final price."},
        {"q": "Does homeowners insurance pay for a new roof?", "a": "If the damage comes from a covered peril like hail, wind or a falling tree, insurance typically pays the approved scope minus your deductible. Wear and age usually aren't covered. Check your policy."},
        {"q": "What is a roofing square?", "a": "A square is 100 square feet of roof surface. Roofers price and order materials by the square."},
        {"q": "Why does removing an old wood shake roof cost more?", "a": "Shakes are heavier and slower to tear off than shingles, and the spaced board decking underneath usually has to be covered with new plywood or OSB before shingles can go on."},
    ]
    tool_page("/tools/roof-cost-calculator/", "Roof Cost Calculator", "Kingwood Roof Replacement Cost Calculator",
              "Estimate what a new roof costs on your Kingwood home in under a minute, from 3-tab shingles to standing-seam metal.",
              "Roof Replacement Cost Calculator for Kingwood, TX (2026)",
              "Free roof replacement cost calculator for Kingwood, TX homes. Estimate by size, pitch, material and tree cover, then book a free inspection for an exact quote.",
              cost_tool, cost_body, cost_faqs, "brick-home", "Kingwood Roof Replacement Cost Calculator")

    # 2. pitch calculator
    pitch_tool = f"""<form data-tool="pitch" onsubmit="return false"><div class="tool-grid">
<div>
<div class="pitch-vis"><svg viewBox="0 0 300 200" role="img" aria-label="Roof pitch diagram">
<line x1="10" y1="190" x2="290" y2="190" stroke="#e5d9c9" stroke-width="2"/>
<polygon data-pitch-tri points="20,190 150,120 280,190" fill="rgba(123,30,43,.12)" stroke="#7b1e2b" stroke-width="3" stroke-linejoin="round"/>
<line data-pitch-rise x1="150" y1="120" x2="150" y2="190" stroke="#c9973f" stroke-dasharray="5 5" stroke-width="2"/>
<text data-pitch-label x="150" y="110" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-weight="600" font-size="17" fill="#231a17">6/12</text>
</svg></div>
<div class="field-row"><label for="rise">Roof pitch (rise per 12" run) <output for="rise"></output></label><input type="range" id="rise" name="rise" min="1" max="18" step="1" value="7" data-fmt="/12"></div>
<div class="field-row"><label for="length">House length (ft) <output for="length"></output></label><input type="range" id="length" name="length" min="20" max="120" step="1" value="60" data-fmt=" ft"></div>
<div class="field-row"><label for="width">House width (ft) <output for="width"></output></label><input type="range" id="width" name="width" min="15" max="80" step="1" value="40" data-fmt=" ft"></div>
<div class="field-row"><label for="overhang">Eave overhang (ft) <output for="overhang"></output></label><input type="range" id="overhang" name="overhang" min="0" max="3" step="0.5" value="1.5" data-fmt=" ft"></div>
<div class="field-row"><span class="lbl">Roof shape</span>{seg('shape', [('gable', 'Simple gable'), ('hip', 'Hip roof'), ('complex', 'Complex / many valleys')], 'complex')}</div>
</div>
<div class="result" aria-live="polite">
<span class="kicker">Your roof</span>
<div class="big"><span data-out="pitch"></span> = <span data-out="deg"></span></div>
<dl><dt>Slope multiplier</dt><dd data-out="mult"></dd><dt>Roof surface area</dt><dd data-out="area"></dd><dt>Roofing squares</dt><dd data-out="squares"></dd>
<dt>Squares to order</dt><dd data-out="order"></dd><dt>Shingle bundles (3/sq)</dt><dd data-out="bundles"></dd><dt>Walkability</dt><dd data-out="walk"></dd></dl>
<p data-out="walknote" style="font-size:.9rem"></p>
<a class="btn btn-brass btn-block" href="/free-roof-inspection/">Get it measured for free {icon('arrow')}</a>
<small>Footprint-based estimate. Dormers, multiple roof planes and porches change the total; a measured inspection is the only exact number.</small>
</div></div></form>"""
    pitch_body = f"""<h2>What roof pitch means</h2>
<p>Roof pitch is how many inches a roof rises for every 12 inches of horizontal run. A 6/12 roof rises 6 inches per foot, about 26.6 degrees. Many Kingwood two-stories built in the 1980s and 1990s have 7/12 to 10/12 main roofs with steeper front gables, while older ranch homes in the original villages often sit closer to 5/12 or 6/12.</p>
<h2>Why pitch matters for your roof</h2>
<ul><li><strong>Material choice:</strong> asphalt shingles need at least 2/12 with special underlayment, and 4/12 or more is standard. Lower slopes need membrane or low-slope metal systems.</li>
<li><strong>Cost:</strong> steeper roofs have more surface area and need extra safety gear, which raises labor.</li>
<li><strong>Debris:</strong> low-slope sections and valleys under pines hold needles and water longer, so they wear out first.</li></ul>
<h2>How to find your pitch</h2>
<p>Safely, from a ladder at a gable end: hold a level horizontally against the roof edge, measure 12 inches along it, then measure straight up to the roof surface. That number is your rise. Or skip the ladder and let us measure during a <a href="/free-roof-inspection/">free roof inspection</a>, then plug the numbers into the <a href="/tools/roof-cost-calculator/">roof cost calculator</a>.</p>"""
    pitch_faqs = [
        {"q": "What is the most common roof pitch in Kingwood?", "a": "Most Kingwood two-stories have main roofs between about 7/12 and 10/12, with steeper decorative gables. Single-story homes in the older villages are often lower."},
        {"q": "How many bundles of shingles are in a square?", "a": "Most architectural shingles come three bundles to a square (100 sq ft). Some heavier designer shingles need four or five."},
        {"q": "How much waste should I add?", "a": "About 10% for a simple gable roof, 15% for hip roofs and up to 20% for complex roofs with many valleys and dormers."},
    ]
    tool_page("/tools/roof-pitch-calculator/", "Roof Pitch Calculator", "Roof Pitch &amp; Area Calculator",
              "Convert roof pitch to degrees, find your slope multiplier and estimate roof squares and shingle bundles from your home's footprint.",
              "Roof Pitch Calculator: Degrees, Squares & Bundles | Kingwood",
              "Free roof pitch calculator: convert pitch to degrees and get the slope multiplier, roof area, roofing squares and shingle bundles. Made for Kingwood homeowners.",
              pitch_tool, pitch_body, pitch_faqs, "home-classic" if "home-classic" in B.IMG_SIZES else "tree-street", "Roof Pitch & Area Calculator")

    # 3. storm damage checklist
    items = [(3, "A limb or tree hit the roof", "Even a small branch can crack shingles or puncture decking"),
             (3, "Dented gutters, downspouts or roof vents", "Soft metals show hail size and direction"),
             (3, "Shingle pieces or ridge caps in the yard", "A sign of wind damage or lifted shingles"),
             (2, "Granules piled at downspout outlets", "Looks like coarse black sand; shingles losing protection"),
             (3, "Water stains or drips on a ceiling", "Active leak; call soon to avoid decking and drywall damage"),
             (2, "Dented AC fins, mailbox or patio furniture", "Confirms hail hit your property"),
             (2, "Cracked window screens or siding", "Strong indicator of hail or debris impacts"),
             (1, "Neighbors are getting roof work or adjuster visits", "Storms hit whole villages at once"),
             (2, "Visible missing, lifted or creased shingles", "Wind breaks the seal strip and shingles start flapping"),
             (1, "Hail 1 inch (quarter-size) or larger was reported", "Check NWS storm reports for your area")]
    checks = "".join(f'<label><input type="checkbox" value="{w}"><span><strong>{e(t)}</strong><small>{e(s)}</small></span></label>' for w, t, s in items)
    storm_tool = f"""<form data-tool="storm" onsubmit="return false"><div class="tool-grid">
<div><h2 style="font-size:1.5rem">What do you see from the ground?</h2><p style="color:var(--muted)">Stay off the roof. Walk the property and tick everything that applies.</p>
<div class="check-list">{checks}</div>
<div class="field-row" style="margin-top:20px"><label for="age">Roof age (years) <output for="age"></output></label><input type="range" id="age" name="age" min="0" max="30" step="1" value="10" data-fmt=" yrs"></div>
</div>
<div class="result" aria-live="polite">
<span class="kicker">Damage likelihood</span>
<div class="big" data-out="pct">0%</div>
<div class="meter"><span data-out="meter"></span></div>
<h3 style="margin:0 0 8px" data-out="level"></h3>
<p data-out="advice"></p>
<a class="btn btn-brass btn-block" href="/free-roof-inspection/">Book a free damage inspection {icon('arrow')}</a>
<small>A guide, not a diagnosis. Only an up-close inspection can confirm storm damage. Nothing you enter is saved or sent.</small>
</div></div></form>"""
    storm_body = f"""<h2>Why most storm damage goes unnoticed</h2>
<p>Hail damage on asphalt shingles usually shows up as small dark spots where granules were knocked off, or soft bruises you can only feel by hand. From the driveway, a hail-damaged roof often looks fine, and under Kingwood's trees you may not even see most of the roof. The clues are on softer things around your home: gutters, vents, AC fins, screens and the limbs lying in the yard.</p>
<h2>What to do after hail, wind or a fallen limb</h2>
<ol><li><strong>Stay safe.</strong> Avoid downed lines, don't climb on the roof and keep clear of hanging limbs.</li>
<li><strong>Document.</strong> Photograph dents, debris and any interior water spots, with dates.</li>
<li><strong>Prevent more damage.</strong> If water is coming in, call us for an emergency tarp.</li>
<li><strong>Get an inspection.</strong> A <a href="/free-roof-inspection/">free roof inspection</a> confirms whether there's damage worth claiming.</li>
<li><strong>Then decide on a claim.</strong> See our <a href="/blog/roof-insurance-claim-guide-kingwood-tx/">roof insurance claim guide</a>.</li></ol>
<h2>Watch out for storm chasers</h2>
<p>After big storms, out-of-town crews knock on doors across Kingwood. Be careful with anyone who offers to "cover your deductible" (illegal in Texas), pushes you to sign that day, or can't give you a local number. Read <a href="/blog/how-to-choose-kingwood-roofers/">how to choose Kingwood roofers</a>, check the <a href="/weather/">storm desk</a> for recent alerts, or call <a href="tel:{TEL}">{PHONE}</a>.</p>"""
    storm_faqs = [
        {"q": "How soon after a storm should I get my roof inspected?", "a": "As soon as practical, ideally within a few weeks. Many Texas policies set deadlines for reporting storm damage, and small breaks can leak with the next rain."},
        {"q": "Can I see hail damage from the ground?", "a": "Usually not on the shingles themselves. Dents in gutters, vents and AC fins are the best ground-level clues."},
        {"q": "Is a tree falling on my roof covered by insurance?", "a": "Many Texas homeowner policies cover damage when a tree falls on the house during a storm, but terms vary. Document everything and check your policy or ask your agent."},
    ]
    tool_page("/tools/storm-damage-checklist/", "Storm Damage Self-Check", "Storm Damage Roof Self-Check",
              "Just had hail, high wind or a limb come down in Kingwood? Tick what you see from the ground and get an instant damage-likelihood score and next steps.",
              "Storm & Hail Damage Roof Checklist | Kingwood Roofers",
              "Free storm damage self-check for Kingwood homeowners. Answer a few questions after hail, wind or a fallen limb to see how likely roof damage is.",
              storm_tool, storm_body, storm_faqs, "hail", "Storm Damage Roof Self-Check")

    # 4. roof age estimator
    age_tool = f"""<form data-tool="age" onsubmit="return false"><div class="tool-grid">
<div>
<h2 style="font-size:1.5rem">About your roof</h2>
<div class="field-row"><label for="year">Year installed <output for="year"></output></label><input type="range" id="year" name="year" min="1990" max="2026" step="1" value="2010"></div>
<div class="field-row"><span class="lbl">Material</span>{seg('material', [('3tab', '3-tab shingle'), ('arch', 'Architectural'), ('class4', 'Class 4 impact'), ('metal', 'Metal'), ('shake', 'Wood shake')], 'arch')}</div>
<div class="field-row"><span class="lbl">Tree cover over the roof</span>{seg('trees', [('0', 'Open sun'), ('1', 'Some shade'), ('2', 'Heavy canopy')], '2')}</div>
<div class="field-row"><span class="lbl">Attic ventilation</span>{seg('vent', [('good', 'Ridge + soffit vents'), ('some', 'Some vents'), ('poor', 'Hot attic / not sure')], 'some')}</div>
<div class="field-row"><span class="lbl">Major hail or wind since install?</span>{seg('storms', [('0', 'None'), ('1', 'Once'), ('2', 'More than once')], '1')}</div>
<div class="field-row"><span class="lbl">Gutters &amp; valleys kept clear?</span>{seg('clean', [('1', 'Yes, yearly'), ('0', 'Sometimes'), ('-1', 'Rarely')], '0')}</div>
</div>
<div class="result" aria-live="polite">
<span class="kicker">Estimated useful life left</span>
<div class="big" data-out="left">—</div>
<div class="life-bar"><span class="used" data-out="used"></span><span class="left" data-out="leftbar"></span></div>
<dl><dt>Roof age</dt><dd data-out="age"></dd><dt>Expected life in these conditions</dt><dd data-out="life"></dd><dt>Plan replacement around</dt><dd data-out="when"></dd></dl>
<h3 style="margin:0 0 8px" data-out="level"></h3>
<p data-out="advice" style="font-size:.95rem"></p>
<a class="btn btn-brass btn-block" href="/free-roof-inspection/">Check my roof for free {icon('arrow')}</a>
<small>A rule-of-thumb estimate for the Houston climate. Installation quality and hidden damage matter more than age; only an inspection tells you the real condition.</small>
</div></div></form>"""
    age_body = f"""<h2>How long roofs really last in Kingwood</h2>
<p>Manufacturers advertise 25, 30 and even "lifetime" ratings, but those numbers assume ideal conditions. In Kingwood, three things shorten a shingle roof's life: heat and UV in summer, shade and moisture under the tree canopy that feed algae and moss, and debris that holds water in valleys and gutters. Storm hits add up too. A roof that has taken hail once or twice may look fine but lose years of life.</p>
<h2>What this estimator weighs</h2>
<ul><li><strong>Material:</strong> 3-tab shingles commonly give 15 to 20 years here, architectural 20 to 28, Class 4 a little longer, metal 40 or more.</li>
<li><strong>Tree cover:</strong> heavy canopy keeps the roof cooler but wetter and dirtier, and it raises the odds of limb damage.</li>
<li><strong>Ventilation:</strong> a hot, poorly vented attic bakes shingles from below.</li>
<li><strong>Storms and upkeep:</strong> each major hail or wind event takes something away; clean valleys and gutters give some back.</li></ul>
<h2>Signs it's time regardless of age</h2>
<p>Curling or cracked shingles, bald spots with granules gone, repeated leaks, soft spots underfoot or daylight in the attic all mean it's time to look closely. Our blog post on <a href="/blog/black-streaks-moss-on-roof-kingwood/">black streaks and moss</a> explains what's cosmetic and what isn't. When in doubt, book a <a href="/free-roof-inspection/">free roof inspection</a> or run the <a href="/tools/roof-cost-calculator/">roof cost calculator</a> to start budgeting.</p>"""
    age_faqs = [
        {"q": "How do I find out when my roof was installed?", "a": "Check closing documents, the seller's disclosure, permit records or your village association's ACC approval records. Roofers can also estimate age from shingle style and wear during an inspection."},
        {"q": "Does shade from trees make a roof last longer?", "a": "Shade lowers heat and UV, which helps, but it also keeps the roof damp and covered in debris, which feeds algae, moss and rot. Under heavy canopy the trade-off usually shortens life unless the roof is kept clean."},
        {"q": "Will my insurance company care about roof age?", "a": "Many Texas insurers look at roof age when writing or renewing policies, and some pay older roofs on an actual-cash-value basis. Check your policy and ask your agent."},
    ]
    tool_page("/tools/roof-age-estimator/", "Roof Age Estimator", "Roof Age &amp; Lifespan Estimator",
              "Find out roughly how much life your roof has left under Kingwood's heat, humidity and tree canopy, and when to start planning a replacement.",
              "Roof Age & Lifespan Estimator | Kingwood Roofers",
              "Free roof lifespan estimator for Kingwood, TX. Enter install year, material, tree cover and ventilation to see how many years your roof likely has left.",
              age_tool, age_body, age_faqs, "forest-home", "Roof Age & Lifespan Estimator")

    url = "/tools/"
    crumbs = [("Home", "/"), ("Tools", url)]
    cards = [("/tools/roof-cost-calculator/", "calculator", "Roof Cost Calculator", "Estimate a replacement price range by size, pitch, material and tree cover."),
             ("/tools/roof-pitch-calculator/", "ruler", "Roof Pitch & Area Calculator", "Pitch to degrees, slope multiplier, roof squares and shingle bundles."),
             ("/tools/storm-damage-checklist/", "clipboard", "Storm Damage Self-Check", "After hail, wind or a fallen limb, score how likely your roof is damaged."),
             ("/tools/roof-age-estimator/", "hourglass", "Roof Age & Lifespan Estimator", "See how many years your roof likely has left in Kingwood conditions."),
             ("/weather/", "cloud-rain", "Kingwood Storm Desk", "Live conditions, NWS alerts, hourly gusts and a 7-day roof-risk forecast.")]
    grid = "".join(f'<article class="tile" data-reveal style="--d:{(i % 3) * 0.08:.2f}s"><div class="ico">{icon(ic)}</div><h3><a href="{h}">{e(t)}</a></h3><p>{e(d)}</p><span class="link-arrow">Open {icon("arrow")}</span></article>'
                   for i, (h, ic, t, d) in enumerate(cards))
    main = (B.page_hero(crumbs, "Free Roofing Tools for Kingwood Homeowners", "Calculators and checklists to help you plan, budget and protect your roof. Free, instant and private.", image="shingles", kicker="Tools") +
            f'<section class="section"><div class="wrap"><div class="grid g3">{grid}</div></div></section>' + B.closer())
    B.add(url, B.page(url, "Free Roofing Calculators & Tools | Kingwood Roofers",
                      "Free roofing tools for Kingwood, TX homeowners: roof cost calculator, pitch and area calculator, storm damage self-check, roof lifespan estimator and weather.",
                      main, active="/tools/", schema=[B.crumbs_schema(crumbs)]), priority="0.7")


# --------------------------------------------------------------------------- about / contact / legal
def build_about():
    url = "/about/"
    crumbs = [("Home", "/"), ("About", url)]
    practices = [("camera", "Photos of everything", "Every inspection and every job is photo-documented, so you never have to take our word for it."),
                 ("shield", "No-pressure advice", "If a repair will do, we say so. If your roof is fine, we say that too."),
                 ("file-check", "Insurance done honestly", "We document damage and meet adjusters, and we follow Texas law: no waived or rebated deductibles."),
                 ("clipboard", "Itemized estimates", "Underlayment, flashing, ventilation, decking and disposal spelled out line by line."),
                 ("tree", "Care around your trees", "Tarps over beds and shrubs, careful material drops and a magnetic nail sweep before we leave."),
                 ("phone", "We pick up the phone", "Questions after the job? Call the same number you called the first time.")]
    tiles = "".join(f'<div class="tile" data-reveal style="--d:{(i % 3) * 0.08:.2f}s"><div class="ico">{icon(ic)}</div><h3>{e(t)}</h3><p>{e(d)}</p></div>'
                    for i, (ic, t, d) in enumerate(practices))
    main = (B.page_hero(crumbs, "About Kingwood Roofers", "A local roofing company for Kingwood homeowners who want straight answers, careful work and a roofer who'll still be here next storm season.",
                        image="hero-pines", kicker="Who we are") +
            f"""<section class="section"><div class="wrap cols">
<div data-reveal><span class="kicker">Our story</span><h2>Roofing the way we'd want it done on our own homes</h2>
<p>Kingwood Roofers started with a simple idea: homeowners in the Livable Forest deserve a roofer who explains things clearly, prices fairly and doesn't disappear when storm season ends. Too many families here have dealt with door-knockers who rush a claim, rush a roof and leave town.</p>
<p>We do it differently. Every job starts with a <a href="/free-roof-inspection/">free roof inspection</a> and a photo report. We recommend what your roof needs, not what makes the biggest invoice, and we build roofs for Kingwood's real conditions: heat, humidity, falling limbs, hail and hurricane-force wind.</p>
<p>From Bear Branch and Elm Grove to Atascocita, Porter and Crosby, we're proud to be the roofers neighbors recommend to neighbors.</p>
<a class="btn" href="tel:{TEL}">{icon('phone')} {PHONE}</a></div>
<div class="photo offset-frame" data-reveal style="--d:.1s">{img('roofer-work', 'Kingwood Roofers crew member working on a shingle roof')}</div>
</div></section>
<section class="section bg-cream"><div class="wrap"><div class="head" data-reveal><span class="kicker">How we work</span><h2>Six promises on every roof</h2></div>
<div class="grid g3">{tiles}</div></div></section>
<section class="section"><div class="wrap"><div class="head" data-reveal><span class="kicker">What we do</span><h2>Our roofing services</h2></div>
{service_tiles()}</div></section>""" + B.closer())
    B.add(url, B.page(url, "About Kingwood Roofers | Local Roofing Company in Kingwood, TX",
                      "Meet Kingwood Roofers, a local roofing company in Kingwood, TX. Free roof inspections, photo-documented work, honest estimates and storm damage help.",
                      main, schema=[B.crumbs_schema(crumbs)]), priority="0.6")


def build_contact():
    url = "/contact/"
    crumbs = [("Home", "/"), ("Contact", url)]
    main = (B.page_hero(crumbs, "Contact Kingwood Roofers", "Call, text or send a request. We'll get back to you quickly to schedule your free roof inspection.", image="lake-sunset", kicker="Get in touch") +
            f"""<section class="section"><div class="wrap cols top">
<div data-reveal><h2>Talk to a Kingwood roofer</h2>
<p>Active leak, a limb on the roof, storm damage or just planning ahead, we're happy to help. The fastest way to reach us is by phone.</p>
<a class="foot-phone" style="color:var(--maroon)!important;font-size:2.1rem" href="tel:{TEL}">{icon('phone')} {PHONE}</a>
<ul class="ticks" style="margin-top:18px">
<li>{icon('pin')}<span><strong>Service area:</strong> Kingwood, Atascocita, Humble, Porter, New Caney, Huffman and Crosby</span></li>
<li>{icon('home')}<span><strong>ZIP codes:</strong> 77339, 77345, 77346 and surrounding</span></li>
<li>{icon('alert')}<span><strong>Active leak or tree on the roof?</strong> Call us. We can arrange emergency tarping to prevent further damage.</span></li>
</ul>
<div class="desk" data-wx-desk data-wx-compact style="margin-top:28px;background:var(--pine);color:#d8e3dc"><div class="desk-now"><span class="kicker light">Kingwood right now</span><p class="loading">Loading Kingwood weather…</p></div></div>
</div>
<div class="form-card" data-reveal style="--d:.1s">{B.lead_form('contact-form', heading='Send us a message', sub='We usually respond the same business day.', full=True)}</div>
</div></section>""")
    B.add(url, B.page(url, "Contact Kingwood Roofers | Call (512) 297-7580",
                      "Contact Kingwood Roofers for a free roof inspection, roof repair or replacement quote in Kingwood, TX. Call (512) 297-7580 or send a request online.",
                      main, schema=[B.crumbs_schema(crumbs), {"@type": "ContactPage", "url": SITE + url}], scripts=("weather",)), priority="0.6")


def build_simple():
    main = f"""<section class="phero no-img" style="text-align:center"><div class="wrap" style="padding:110px 0;margin:0 auto">
<div><span class="kicker">Request received</span><h1>Thank you!</h1>
<p class="lead" style="margin:0 auto 28px">Your request is on its way. A Kingwood roofer will call you shortly to schedule your free roof inspection. Need us sooner?</p>
<div class="hero-actions" style="justify-content:center"><a class="btn btn-brass" href="tel:{TEL}">{icon('phone')} Call {PHONE}</a><a class="btn btn-ghost-light" href="/blog/">Read our roofing guides</a></div></div></div></section>"""
    B.add("/thank-you/", B.page("/thank-you/", "Thank You | Kingwood Roofers", "Thanks for contacting Kingwood Roofers. We'll be in touch shortly.", main,
                                noindex=True, popup=False), sitemap=False)

    main = f"""<section class="phero no-img" style="text-align:center"><div class="wrap" style="padding:110px 0;margin:0 auto">
<div><span class="kicker">Error 404</span><h1>This page blew away</h1>
<p class="lead" style="margin:0 auto 28px">The page you're looking for doesn't exist or has moved. Let's get you back under a solid roof.</p>
<div class="hero-actions" style="justify-content:center"><a class="btn btn-brass" href="/">Back to home</a><a class="btn btn-ghost-light" href="/free-roof-inspection/">Free roof inspection</a></div></div></div></section>"""
    B.write("/404.html", B.page("/404.html", "Page Not Found | Kingwood Roofers", "This page could not be found.", main, noindex=True))

    legal = {
        "/privacy-policy/": ("Privacy Policy", f"""<p>Last updated: {B.fmt_date(B.TODAY.isoformat())}</p>
<p>This Privacy Policy explains how Kingwood Roofers ("we", "us") collects and uses information through rooferkingwood.com.</p>
<h2>Information we collect</h2><p>When you submit a form, we collect the details you provide, such as your name, phone number, email address, property address and message, along with the page you submitted from, the time, and your IP address for spam prevention.</p>
<h2>How we use it</h2><p>We use your information only to respond to your request, schedule inspections, provide estimates and service, and keep basic business records. We may call or text you about your request.</p>
<h2>Sharing</h2><p>We do not sell or rent your personal information. We share it only with service providers who help us operate (such as email delivery), when required by law, or with your permission (for example, with your insurance adjuster at your request).</p>
<h2>Third-party services</h2><p>Our weather features load forecast data from Open-Meteo and alerts from the National Weather Service, and our pages load fonts from Google Fonts. Those services may receive your IP address as part of normal web requests. Our calculators run entirely in your browser; nothing you enter in them is stored or sent.</p>
<h2>Cookies and storage</h2><p>We don't use advertising cookies. Your browser's session storage is used only to remember that you've already seen or closed our inspection pop-up, so it doesn't keep reappearing.</p>
<h2>Your choices</h2><p>To ask us to update or delete information you've sent us, call {PHONE} or email info@rooferkingwood.com.</p>
<h2>Changes</h2><p>We may update this policy from time to time. The date at the top shows the latest version.</p>"""),
        "/terms/": ("Terms of Use", f"""<p>Last updated: {B.fmt_date(B.TODAY.isoformat())}</p>
<p>By using rooferkingwood.com you agree to these terms.</p>
<h2>Informational content</h2><p>Articles, calculators, cost ranges and weather information on this site are for general information only. They are not quotes, engineering advice, insurance advice or legal advice. Weather data comes from third parties and may be delayed or inaccurate; always follow official National Weather Service warnings.</p>
<h2>Estimates and services</h2><p>Any roofing work is governed by a separate written agreement. Prices shown on this site are planning ranges and may differ from your written estimate.</p>
<h2>Insurance</h2><p>Kingwood Roofers is a roofing contractor, not a public adjuster or insurance company. Coverage decisions are made by your insurer. In accordance with Texas Business &amp; Commerce Code §27.02, we do not waive, rebate or pay any portion of an insurance deductible.</p>
<h2>Intellectual property</h2><p>Site content is owned by Kingwood Roofers or used under license. Photos are free-license stock images and may not depict our own projects.</p>
<h2>Limitation of liability</h2><p>The site is provided "as is" without warranties of any kind. To the extent permitted by law, Kingwood Roofers is not liable for damages arising from use of the site.</p>
<h2>Contact</h2><p>Questions about these terms? Call {PHONE}.</p>"""),
    }
    for url, (name, body) in legal.items():
        crumbs = [("Home", "/"), (name, url)]
        main = (B.page_hero(crumbs, name, f"{name} for rooferkingwood.com.") +
                f'<section class="section"><div class="wrap"><article class="prose" style="max-width:820px">{body}</article></div></section>')
        B.add(url, B.page(url, f"{name} | Kingwood Roofers", f"{name} for Kingwood Roofers (rooferkingwood.com), a roofing company serving Kingwood, TX.", main,
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
