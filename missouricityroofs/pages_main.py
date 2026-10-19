"""Every page except the homepage."""
import build as B
from build import e, icon, img, TEL, PHONE, SITE, EMAIL


def service_tiles(exclude=None):
    out = ""
    for i, s in enumerate(x for x in B.SERVICES if x["slug"] != exclude):
        out += (f'<a class="tile" href="/services/{s["slug"]}/" data-reveal><span class="tile-ico">{icon(s.get("icon", "home"))}</span>'
                f'<b>{e(s["name"])}</b><span>{e(s["short"])}</span><span class="tile-go">Learn more {icon("arrow")}</span></a>')
    return out


def post_card(p):
    return (f'<article class="post-card" data-reveal><a class="pc-img" href="/blog/{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(p["image"], p.get("image_alt", p["h1"]))}</a>'
            f'<div class="pc-body"><div class="pc-meta"><span class="tag">{e(p.get("category", "Guide"))}</span><span>{B.fmt_date(p["date"])} · {p.get("read_minutes", 6)} min</span></div>'
            f'<h3><a href="/blog/{p["slug"]}/">{e(p["h1"])}</a></h3><p>{e(p["excerpt"])}</p></div></article>')


def link_box(title, links):
    items = "".join(f'<li><a href="{h}">{e(l)} {icon("arrow")}</a></li>' for h, l in links)
    return f'<div class="box"><h3>{e(title)}</h3><ul class="link-list">{items}</ul></div>'


def prose_page(item, crumbs, aside, eyebrow, meta="", after_body=""):
    body = B.prep_body(item["body"])
    return (B.page_hero(crumbs, e(item["h1"]), item["intro"], bg=item["image"], eyebrow=eyebrow, meta=meta) +
            f'<section class="section"><div class="wrap layout"><article class="prose">{body}{after_body}</article>'
            f'<aside class="aside">{aside}</aside></div></section>')


def ticks(items):
    return '<ul class="ticks">' + "".join(f"<li>{icon('check')} {x}</li>" for x in items) + "</ul>"


# --------------------------------------------------------------------------- services
def build_services():
    for s in B.SERVICES:
        url = f"/services/{s['slug']}/"
        crumbs = [("Home", "/"), ("Services", "/services/"), (s["name"], url)]
        aside = (f'<div class="box"><h3>What\'s included</h3>{ticks([e(b) for b in s.get("bullets", [])])}</div>' + B.aside_phone() +
                 link_box("Other services", [("/free-roof-inspection/", "Free Roof Inspection")] +
                          [(f"/services/{o['slug']}/", o["name"]) for o in B.SERVICES if o is not s]))
        main = prose_page(s, crumbs, aside, eyebrow=f"Missouri City roofing · {s['name']}")
        main += B.faq_html(s["faqs"], f"{s['name']} questions")
        main += B.form_section("svc-form")
        main += B.final_cta()
        schema = [B.crumbs_schema(crumbs), B.faq_schema(s["faqs"]),
                  {"@type": "Service", "name": s["h1"], "serviceType": s["name"], "url": SITE + url, "description": s["description"],
                   "provider": {"@id": SITE + "/#business"}, "areaServed": {"@type": "City", "name": "Missouri City, TX"}}]
        B.add(url, B.page(url, s["title"], s["description"], main, active="/services/", schema=schema, og_image=s["image"] + ".webp"), priority="0.9")

    url = "/services/"
    crumbs = [("Home", "/"), ("Services", url)]
    main = (B.page_hero(crumbs, "Missouri City Roofing Services", "Every roofing service a Missouri City home or business needs, starting with a free, photo-documented roof inspection.",
                        bg="tear-off", eyebrow="What we do") +
            f"""<section class="section"><div class="wrap"><div class="sec-head" data-reveal><h2>Repairs, replacements and storm restoration</h2>
<p>We handle everything from one cracked pipe boot to complete tear-offs on large two-story homes and light commercial buildings. Pick a service to see how we approach it, or <a href="/free-roof-inspection/">book a free inspection</a> and we'll tell you what your roof actually needs.</p></div>
<div class="tiles">{service_tiles()}</div></div></section>""" +
            B.form_section("services-form") + B.final_cta())
    B.add(url, B.page(url, "Roofing Services in Missouri City, TX | Missouri City Roofers",
                      "Roof repair, roof replacement, storm and hail damage, insurance claim help, metal roofing, commercial roofing and gutters in Missouri City, TX.",
                      main, schema=[B.crumbs_schema(crumbs)]), priority="0.8")


# --------------------------------------------------------------------------- areas
def build_areas():
    for a in B.AREAS:
        url = f"/areas/{a['slug']}/"
        crumbs = [("Home", "/"), ("Service Areas", "/areas/"), (a["name"], url)]
        hoods = "".join(f"<span>{e(n)}</span>" for n in a.get("neighborhoods", []))
        aside = (f"""<div class="box"><h3>{e(a['name'])} at a glance</h3><dl class="facts">
<dt>{icon('pin')} County</dt><dd>{e(a.get('county', ''))}</dd>
<dt>{icon('home')} ZIP codes</dt><dd>{e(a.get('zips', ''))}</dd>
<dt>{icon('clock')} Drive</dt><dd>{e(a.get('drive', ''))}</dd></dl>
<div class="chips">{hoods}</div></div>""" + B.aside_phone() +
                 link_box("Nearby areas", [("/", "Missouri City, TX")] + [(f"/areas/{o['slug']}/", o["name"]) for o in B.AREAS if o is not a]))
        main = prose_page(a, crumbs, aside, eyebrow=f"Service area · {a['name']}, TX")
        main += (f'<section class="section sec-cream"><div class="wrap"><div class="sec-head" data-reveal><span class="kicker">Services in {e(a["name"])}</span>'
                 f'<h2>What we do in {e(a["name"])}</h2></div><div class="tiles">{service_tiles()}</div></div></section>')
        main += B.faq_html(a["faqs"], f"Roofing in {a['name']}: questions")
        main += B.form_section("area-form")
        main += B.final_cta()
        schema = [B.crumbs_schema(crumbs), B.faq_schema(a["faqs"]),
                  {"@type": "Service", "name": a["h1"], "serviceType": "Roofing", "url": SITE + url, "provider": {"@id": SITE + "/#business"},
                   "areaServed": {"@type": "City", "name": a["name"] + ", TX"}}]
        B.add(url, B.page(url, a["title"], a["description"], main, active="/areas/", schema=schema, og_image=a["image"] + ".webp"), priority="0.8")

    url = "/areas/"
    crumbs = [("Home", "/"), ("Service Areas", url)]
    cards = "".join(f"""<article class="post-card" data-reveal><a class="pc-img" href="/areas/{a['slug']}/" tabindex="-1" aria-hidden="true">{img(a['image'], a.get('image_alt', a['name']))}</a>
<div class="pc-body"><div class="pc-meta"><span class="tag">{e(a.get('county', '').split(' (')[0])} County</span><span>{e(a.get('zips', ''))}</span></div>
<h3><a href="/areas/{a['slug']}/">Roofing in {e(a['name'])}</a></h3><p>{e(a['short'])}</p></div></article>""" for a in B.AREAS)
    main = (B.page_hero(crumbs, "Areas We Serve Around Missouri City, TX", "Based in Missouri City and working across Fort Bend County and the southwest Houston suburbs, from the Brazos River to Beltway 8.",
                        bg="suburb", eyebrow="Service areas") +
            f"""<section class="section"><div class="wrap">
<div class="intro-grid" style="margin-bottom:64px"><div data-reveal><span class="kicker">Home base</span><h2>Missouri City, TX</h2>
<p>We cover both Missouri City ZIP codes, 77459 and 77489: the established neighborhoods of Quail Valley, Hunters Glen, Fondren Park, Lake Olympia, Vicksburg and Lexington Village, plus master-planned Sienna and Riverstone with their HOA review rules.</p>
<p>Older homes here often need ventilation and decking attention at replacement time, while newer ones need HOA-approved materials and careful documentation for builder or insurance questions. We plan for both.</p>
<a class="btn" href="/free-roof-inspection/">Free inspection in Missouri City {icon('arrow')}</a></div>
<div class="intro-img" data-reveal>{img('home-trees', 'Home shaded by mature trees in an established Missouri City neighborhood')}</div></div>
<div class="sec-head" data-reveal><h2>Nearby communities</h2><p>Each community has its own housing stock, HOA rules and storm exposure. Here's what we see in each.</p></div>
<div class="post-grid">{cards}</div></div></section>""" + B.form_section("areas-form") + B.final_cta())
    B.add(url, B.page(url, "Service Areas Near Missouri City, TX | Missouri City Roofers",
                      "Missouri City Roofers serves Missouri City, Sienna, Sugar Land, Stafford, Pearland, Fresno and Richmond. Free roof inspections in 77459 and 77489.",
                      main, schema=[B.crumbs_schema(crumbs)]), priority="0.7")


# --------------------------------------------------------------------------- blog
def build_blog():
    for p in B.POSTS:
        url = f"/blog/{p['slug']}/"
        crumbs = [("Home", "/"), ("Blog", "/blog/"), (p["h1"], url)]
        meta = (f'<div class="post-meta"><span>{icon("calendar")} {B.fmt_date(p["date"])}</span><span>{icon("clock")} {p.get("read_minutes", 6)} min read</span>'
                f'<span>{icon("users")} Missouri City Roofers team</span></div>')
        related = [x for x in B.POSTS if x is not p and x.get("category") == p.get("category")]
        related += [x for x in B.POSTS if x is not p and x not in related]
        aside = ('<div class="box toc"><h3>In this article</h3><ul></ul></div>' + B.aside_phone() +
                 link_box("Roofing services", [("/free-roof-inspection/", "Free Roof Inspection")] + [(f"/services/{s['slug']}/", s["name"]) for s in B.SERVICES[:5]]) +
                 link_box("Free tools", B.NAV_TOOLS))
        author = (f'<div class="author" data-reveal><span class="tile-ico">{icon("roof")}</span><div><b>Written by the Missouri City Roofers team</b>'
                  f'<p>Local roofers serving Missouri City, Sienna, Sugar Land and Fort Bend County. Questions about your roof? Call <a href="tel:{TEL}">{PHONE}</a> or '
                  f'<a href="/free-roof-inspection/">book a free inspection</a>.</p></div></div>')
        main = prose_page(p, crumbs, aside, eyebrow=p.get("category", "Guide"), meta=meta, after_body=author)
        main += B.faq_html(p["faqs"], "Frequently asked questions")
        main += (f'<section class="section"><div class="wrap"><div class="sec-head" data-reveal><span class="kicker">Keep reading</span><h2>More roofing guides</h2></div>'
                 f'<div class="post-grid">{"".join(post_card(x) for x in related[:3])}</div></div></section>')
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
    feature = f"""<article class="feature" data-reveal><a class="pc-img" href="/blog/{first['slug']}/" tabindex="-1" aria-hidden="true">{img(first['image'], first.get('image_alt', first['h1']))}</a>
<div class="pc-body"><div class="pc-meta"><span class="tag">Latest · {e(first.get('category', ''))}</span><span>{B.fmt_date(first['date'])} · {first.get('read_minutes', 6)} min</span></div>
<h2><a href="/blog/{first['slug']}/">{e(first['h1'])}</a></h2><p>{e(first['excerpt'])}</p><a class="link-arrow" href="/blog/{first['slug']}/">Read the article {icon('arrow')}</a></div></article>"""
    cards = "".join(post_card(p) for p in B.POSTS[1:])
    main = (B.page_hero(crumbs, "Missouri City Roofing Blog", "Practical guides for Missouri City homeowners on roof costs, hail and hurricane damage, insurance claims, materials and maintenance.",
                        bg="home-modern", eyebrow="Guides & advice") +
            f'<section class="section"><div class="wrap">{feature}<div class="post-grid">{cards}</div></div></section>' + B.final_cta())
    items = {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{SITE}/blog/{p['slug']}/"} for i, p in enumerate(B.POSTS)]}
    B.add(url, B.page(url, "Missouri City Roofing Blog: Guides for Homeowners",
                      "Roofing advice from Missouri City roofers: replacement costs, hail damage, Fort Bend insurance claims, hurricane prep, shingles and maintenance.",
                      main, schema=[B.crumbs_schema(crumbs), items]), lastmod=B.POSTS[0]["date"], priority="0.7")


# --------------------------------------------------------------------------- free inspection
INSPECTION_FAQS = [
    {"q": "Why is the roof inspection free?", "a": "Because you shouldn't have to pay to find out whether you have a problem. A free inspection is how homeowners get to know us; if your roof needs work, we hope you'll hire us, and if it doesn't, we'll say so."},
    {"q": "How long does a free roof inspection take?", "a": "Most Missouri City homes take 30 to 60 minutes, depending on roof size, pitch and whether we check the attic. You stay on the ground and we walk you through the photos afterward."},
    {"q": "Do I need to be home?", "a": "It helps for the attic check and the walkthrough, but it isn't required for the exterior inspection. We'll send the photos and findings either way."},
    {"q": "Does an inspection count as an insurance claim?", "a": "No. Having a contractor inspect your roof is not a claim. You decide whether to file, and you'll make that decision with real photos and measurements."},
    {"q": "Is it useful when buying or selling a home?", "a": "Yes. A roofer's inspection goes deeper on the roof than a general home inspection, and the photo report helps in negotiations or for planning maintenance."},
]


def build_inspection():
    url = "/free-roof-inspection/"
    crumbs = [("Home", "/"), ("Free Roof Inspection", url)]
    checks = [("cloud-hail", "Hail & impact damage", "Bruised or fractured shingles, granule loss, dented vents and soft metals."),
              ("wind", "Wind damage", "Lifted, creased or missing shingles and ridge caps; broken seal strips."),
              ("layers", "Flashing & valleys", "Step, wall, chimney and valley flashing; exposed nails and failed sealant."),
              ("droplets", "Leaks & moisture", "Attic stains, damp insulation, rusted nails and soft decking."),
              ("thermo", "Ventilation & heat", "Intake and exhaust balance, attic heat, blocked soffits."),
              ("leaf", "Gutters, trees & algae", "Clogged downspouts, fascia rot, overhanging limbs and black streaks.")]
    cards = "".join(f'<div class="tile static" data-reveal><span class="tile-ico">{icon(ic)}</span><b>{e(t)}</b><span>{e(d)}</span></div>' for ic, t, d in checks)
    main = f"""
<section class="page-hero ph-form">
<div class="wrap ph-grid">
<div class="ph-text">{B.crumbs_html(crumbs)}
<div data-reveal><span class="kicker">$0 · No obligation</span>
<h1>Free Roof Inspections in Missouri City, TX</h1>
<p class="lead">A local roofer inspects your roof top to bottom, photographs every issue and gives you an honest, written recommendation, all at no cost.</p>
<ul class="hero-points"><li>{icon('camera')} Photo report</li><li>{icon('file-check')} Written findings</li><li>{icon('shield')} Storm-damage documentation</li></ul></div></div>
<div class="form-card" data-reveal>{B.lead_form('inspect-form', heading='Book your free roof inspection', sub="Pick a time that works. We'll confirm by phone.", full=True, service='Free roof inspection')}</div>
</div></section>

<section class="section"><div class="wrap">
<div class="sec-head" data-reveal><span class="kicker">What we check</span><h2>A 6-point inspection, not a glance from the driveway</h2>
<p>Plenty of roofers will "inspect" a roof from a ladder in five minutes. Ours is a walk of every slope plus an attic check, because that's where the evidence is.</p></div>
<div class="tiles">{cards}</div></div></section>

<section class="section sec-cream"><div class="wrap">
<div class="sec-head center" data-reveal><span class="kicker">How it works</span><h2>From booking to photo report</h2></div>
<ol class="timeline four">
<li data-reveal><span>1</span><h3>Book online or call</h3><p>Use the form above or call {PHONE}. Tell us about any leaks or recent storms.</p></li>
<li data-reveal><span>2</span><h3>We inspect</h3><p>A roofer walks every slope, checks flashing, vents and gutters, and looks in the attic if you're home.</p></li>
<li data-reveal><span>3</span><h3>You see the photos</h3><p>We go over findings with you, with close-ups of anything that matters, and send the photos for your records.</p></li>
<li data-reveal><span>4</span><h3>Honest recommendation</h3><p>No damage? We say so. A repair? We quote it. Storm damage? We explain the claim process and can meet your adjuster.</p></li>
</ol></div></section>

<section class="section"><div class="wrap intro-grid">
<div class="intro-img" data-reveal>{img('roofer-work', 'Roofers on a Missouri City-area home during a roof inspection')}</div>
<div data-reveal><span class="kicker">When to book</span><h2>Good times to get a free roof inspection</h2>
{ticks(['<b>After hail or high winds</b>, even if nothing looks wrong from the ground', '<b>Before hurricane season</b>: loose shingles and weak flashing fail first',
        '<b>Roof older than 10 years</b>: catch small problems before they leak', '<b>Buying or selling a home</b>: know exactly what you are getting',
        '<b>Stains on a ceiling or wall</b>: find the source before it spreads'])}
<p>Not sure? Run the <a href="/tools/storm-damage-checklist/">storm damage self-check</a> or look at <a href="/weather/">Storm Watch</a> for recent severe weather.</p></div>
</div></section>
{B.faq_html(INSPECTION_FAQS, "Free roof inspection questions")}
{B.final_cta("Book your free roof inspection today")}"""
    schema = [B.crumbs_schema(crumbs), B.faq_schema(INSPECTION_FAQS),
              {"@type": "Service", "name": "Free Roof Inspection in Missouri City, TX", "serviceType": "Roof inspection", "url": SITE + url,
               "provider": {"@id": SITE + "/#business"}, "areaServed": {"@type": "City", "name": "Missouri City, TX"},
               "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}]
    B.add(url, B.page(url, "Free Roof Inspection in Missouri City, TX | No Obligation",
                      "Book a free roof inspection in Missouri City, TX. Local roofers check for hail, wind and leak damage and give you a photo report. No cost, no obligation.",
                      main, schema=schema, og_image="roofer-work.webp", popup=False), priority="0.9")


# --------------------------------------------------------------------------- weather
WEATHER_FAQS = [
    {"q": "Where does this Missouri City weather data come from?", "a": "Current conditions and the 7-day forecast come from Open-Meteo, which blends national weather models including NOAA's. Active alerts come directly from the National Weather Service feed for Missouri City's coordinates (Houston/Galveston office)."},
    {"q": "What does the roof-risk rating mean?", "a": "It's a simple read of each day's forecast: thunderstorms with possible hail, or wind gusts of 50 mph or more, rate High; ordinary thunderstorms, heavy showers or gusts above 35 mph rate Moderate. It's informational, not an official warning."},
    {"q": "When is hail season in Missouri City?", "a": "Most damaging hail around Fort Bend County falls between March and June, when spring storm systems meet warm Gulf moisture, though hail can happen in any month."},
    {"q": "What should I do after a severe storm passes?", "a": "Stay off the roof. From the ground, look for missing shingles, dented gutters and granules at downspouts, photograph what you see, check ceilings for stains, and book a free roof inspection."},
]


def build_weather():
    url = "/weather/"
    crumbs = [("Home", "/"), ("Storm Watch", url)]
    main = f"""{B.page_hero(crumbs, "Missouri City, TX Weather &amp; Storm Watch", "Live conditions, National Weather Service alerts and a 7-day forecast for Missouri City, with a daily roof-risk rating for hail and high wind.", bg="lightning", eyebrow="Live weather")}
<section class="section" style="padding-bottom:32px"><div class="wrap">
<div data-wx-alerts class="alert-box" data-reveal><h3>Checking National Weather Service alerts for Missouri City…</h3></div>
</div></section>
<section class="section storm" style="padding:64px 0"><div class="wrap">
<div class="sec-head" style="margin-bottom:28px"><span class="kicker light"><span class="dot"></span> Right now in Missouri City</span><h2>Current conditions</h2></div>
<div class="wx-current" data-wx-current><div class="skeleton dark"></div></div>
</div></section>
<section class="section"><div class="wrap">
<div class="sec-head" data-reveal><span class="kicker">7-day forecast</span><h2>Missouri City 7-day weather forecast</h2>
<p data-wx-outlook>Loading this week's roof outlook…</p></div>
<div class="wx-forecast" data-wx-forecast>{''.join('<div class="skeleton"></div>' for _ in range(7))}</div>
<div class="prose wide" style="margin-top:40px" data-reveal><div class="table-scroll"><table><thead><tr><th>Day</th><th>Conditions</th><th>High / Low</th><th>Rain chance</th><th>Wind / Gusts</th><th>UV</th></tr></thead>
<tbody data-wx-table><tr><td colspan="6">Loading…</td></tr></tbody></table></div>
<p class="fine">Forecast data: <a href="https://open-meteo.com/" rel="noopener" target="_blank">Open-Meteo</a> (CC BY 4.0). Alerts: <a href="https://www.weather.gov/hgx/" rel="noopener" target="_blank">National Weather Service Houston/Galveston</a>. Times in Central Time. Roof-risk ratings are informational, not official warnings.</p></div>
</div></section>
<section class="section sec-cream"><div class="wrap">
<div class="sec-head" data-reveal><span class="kicker">Be ready</span><h2>Protect your roof when storms are in the forecast</h2></div>
<div class="tiles three">
<div class="tile static" data-reveal><span class="tile-ico">{icon('camera')}</span><b>Before the storm</b><span>Take dated photos of each roof slope from the ground, clean gutters, trim limbs over the roof and tie down patio furniture.</span></div>
<div class="tile static" data-reveal><span class="tile-ico">{icon('alert')}</span><b>During the storm</b><span>Park cars in the garage, stay away from windows during hail, and if water comes in, move valuables and catch drips. Never climb on a wet roof.</span></div>
<div class="tile static" data-reveal><span class="tile-ico">{icon('clipboard')}</span><b>After the storm</b><span>Walk the property, photograph dents and debris, run the <a href="/tools/storm-damage-checklist/">storm damage self-check</a> and book a <a href="/free-roof-inspection/">free roof inspection</a>.</span></div>
</div></div></section>
<section class="section"><div class="wrap intro-grid">
<div data-reveal><span class="kicker">Roofing seasons</span><h2>What each season means for a Missouri City roof</h2>
<div class="prose"><div class="table-scroll"><table><thead><tr><th>Season</th><th>Main roof threat</th><th>What to do</th></tr></thead><tbody>
<tr><td>Mar–Jun</td><td>Hail, severe thunderstorms, straight-line wind</td><td>Inspect after every hail report</td></tr>
<tr><td>Jun–Nov</td><td>Tropical storms &amp; hurricanes, flooding rain</td><td>Pre-season inspection, secure loose shingles</td></tr>
<tr><td>Jul–Sep</td><td>Extreme heat and UV, attic heat buildup</td><td>Check ventilation, pipe boots and sealants</td></tr>
<tr><td>Dec–Feb</td><td>Cold fronts with wind, occasional hard freezes</td><td>Clear gutters, check flashing before spring</td></tr>
</tbody></table></div></div>
<p>Read the <a href="/blog/hurricane-roof-prep-missouri-city-tx/">hurricane roof prep guide</a> and <a href="/blog/hail-damage-signs-missouri-city-roof/">how to spot hail damage</a>.</p></div>
<div class="intro-img" data-reveal>{img('storm-sky', 'Dark storm clouds building over a road outside Missouri City, Texas')}</div>
</div></section>
{B.faq_html(WEATHER_FAQS, "Missouri City weather &amp; roof questions".replace('&amp;', '&'))}
{B.final_cta("Storm just passed? Get a free roof inspection", bg="rain")}"""
    B.add(url, B.page(url, "Missouri City, TX Weather: Live 7-Day Forecast & Storm Alerts",
                      "Live Missouri City, TX weather: current conditions, NWS alerts and a 7-day forecast with a daily hail and wind roof-risk rating. Free inspections after storms.",
                      main, schema=[B.crumbs_schema(crumbs), B.faq_schema(WEATHER_FAQS)], scripts=("weather",), og_image="lightning.webp"), priority="0.8")


# --------------------------------------------------------------------------- tools
def seg(name, options, checked):
    return '<div class="seg">' + "".join(
        f'<label><input type="radio" name="{name}" value="{v}"{" checked" if v == checked else ""}><span>{e(l)}</span></label>' for v, l in options) + "</div>"


def tool_page(url, crumbs_name, h1, lead, title, desc, tool_html, body_html, faqs, bg, app_name):
    crumbs = [("Home", "/"), ("Tools", "/tools/"), (crumbs_name, url)]
    others = "".join(f'<a class="tile" href="{h}" data-reveal><b>{e(l)}</b><span class="tile-go">Open tool {icon("arrow")}</span></a>'
                     for h, l in B.NAV_TOOLS if h != url)
    main = (B.page_hero(crumbs, h1, lead, bg=bg, eyebrow="Free homeowner tool") +
            f'<section class="section"><div class="wrap"><div class="tool" data-reveal>{tool_html}</div></div></section>' +
            f'<section class="section sec-cream"><div class="wrap layout"><article class="prose">{body_html}{B.cta_band()}</article>'
            f'<aside class="aside">{B.aside_phone()}</aside></div></section>' +
            B.faq_html(faqs, "Questions about this tool") +
            f'<section class="section"><div class="wrap"><div class="sec-head"><h2>More free tools</h2></div><div class="tiles two">{others}'
            f'<a class="tile" href="/weather/" data-reveal><b>Storm Watch: live weather</b><span class="tile-go">Open {icon("arrow")}</span></a></div></div></section>' +
            B.final_cta())
    schema = [B.crumbs_schema(crumbs), B.faq_schema(faqs),
              {"@type": "WebApplication", "name": app_name, "url": SITE + url, "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any",
               "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": SITE + "/#business"}}]
    B.add(url, B.page(url, title, desc, main, active="/tools/", schema=schema, scripts=("tools",)), priority="0.7")


def build_tools():
    cost_tool = f"""<form data-tool="cost" onsubmit="return false"><div class="tool-grid">
<div>
<h2 class="tool-h">Your home</h2>
<div class="range-row"><label for="sqft">Living area <output for="sqft"></output></label><input type="range" id="sqft" name="sqft" min="1000" max="6000" step="50" value="2600" data-fmt=" sq ft"></div>
<div class="range-row"><label>Stories</label>{seg('stories', [('1', '1 story'), ('2', '2 stories'), ('3', '3 stories')], '2')}</div>
<div class="range-row"><label>Roof pitch</label>{seg('pitch', [('low', 'Low (≤4/12)'), ('med', 'Medium (5–7/12)'), ('steep', 'Steep (8/12+)')], 'med')}</div>
<div class="range-row"><label>Roofing material</label>{seg('material', [('3tab', '3-tab shingle'), ('arch', 'Architectural'), ('class4', 'Class 4 impact'), ('metal', 'Standing-seam metal'), ('stone', 'Stone-coated steel'), ('tile', 'Concrete tile')], 'arch')}</div>
<div class="range-row"><label>Layers to tear off</label>{seg('layers', [('1', '1 layer'), ('2', '2 layers')], '1')}</div>
<div class="range-row"><label for="deck">Decking to replace <output for="deck"></output></label><input type="range" id="deck" name="deck" min="0" max="50" step="5" value="10" data-fmt="%"></div>
</div>
<div class="result" aria-live="polite">
<span class="kicker light">Estimated installed cost</span>
<div class="big" data-out="range">—</div>
<dl><dt>Material</dt><dd data-out="mat"></dd><dt>Est. roof area</dt><dd data-out="area"></dd><dt>Roofing squares</dt><dd data-out="squares"></dd>
<dt>Per square (100 sq ft)</dt><dd data-out="persq"></dd><dt>Typical lifespan here</dt><dd data-out="life"></dd></dl>
<a class="btn btn-brass btn-block" href="/free-roof-inspection/">Get an exact quote, free {icon('arrow')}</a>
<small>Planning range for the Missouri City / Fort Bend market in 2026, not a quote. Actual price depends on measurements, roof complexity, ventilation, flashing and code items. Insurance claims are priced from your adjuster's scope.</small>
</div></div></form>"""
    cost_body = f"""<h2>How this roof cost calculator works</h2>
<p>The calculator turns your home's living area into an estimated roof area. It divides by the number of stories to approximate the footprint, adds about 12% for overhangs, then multiplies by a slope factor for your pitch. It applies a 2026 installed-price range per square foot for the material you pick, adjusts labor for steep or multi-story roofs, and adds tear-off for extra layers plus any decking you expect to replace.</p>
<h2>Typical roof replacement costs in Missouri City, TX</h2>
<p>For a typical Missouri City home with 2,200 to 3,200 square feet of roof area, architectural shingles are the most common choice and usually land in the low-to-mid five figures. Class 4 impact-resistant shingles cost somewhat more, and many Texas insurers offer a premium discount for them. Standing-seam metal costs roughly double but can last 40 to 50 years. Read the full <a href="/blog/roof-replacement-cost-missouri-city-tx/">Missouri City roof replacement cost guide</a> for a breakdown.</p>
<h2>What the calculator can't see</h2>
<ul><li>Complex roofs with many valleys, dormers and hips take more labor and material</li>
<li>Rotted decking, common on older Quail Valley and Hunters Glen roofs, only shows up during tear-off</li>
<li>Code-required items such as drip edge, ventilation and underlayment upgrades</li>
<li>HOA material or color requirements in communities like Sienna and Riverstone</li></ul>
<p>That's why every real estimate starts with a measured inspection. A <a href="/free-roof-inspection/">free roof inspection</a> includes measurements and an itemized written estimate, or call <a href="tel:{TEL}">{PHONE}</a>.</p>"""
    cost_faqs = [
        {"q": "How accurate is this roof cost calculator?", "a": "It's built to land in a realistic range for most Missouri City homes, but it's a planning tool, not a quote. Measurements, roof complexity and decking condition can move the final price."},
        {"q": "Does homeowners insurance pay for a new roof?", "a": "If the damage comes from a covered peril like hail or wind, insurance typically pays the approved scope minus your deductible. Wear and age aren't covered. A free inspection tells you whether storm damage is present."},
        {"q": "What is a roofing square?", "a": "A square is 100 square feet of roof surface. Roofers price and order materials by the square."},
        {"q": "Why do steep roofs cost more?", "a": "Steep roofs need safety equipment, roof jacks and slower work, and they have more surface area than their footprint suggests."},
    ]
    tool_page("/tools/roof-cost-calculator/", "Roof Cost Calculator", "Missouri City Roof Replacement Cost Calculator",
              "Estimate what a new roof costs on your Missouri City home in under a minute, from 3-tab shingles to standing-seam metal.",
              "Roof Replacement Cost Calculator: Missouri City, TX (2026)",
              "Free roof replacement cost calculator for Missouri City, TX homes. Estimate by size, pitch and material, then book a free roof inspection for an exact quote.",
              cost_tool, cost_body, cost_faqs, "hero-home", "Missouri City Roof Replacement Cost Calculator")

    pitch_tool = f"""<form data-tool="pitch" onsubmit="return false"><div class="tool-grid">
<div>
<div class="pitch-vis"><svg viewBox="0 0 300 200" role="img" aria-label="Roof pitch diagram">
<line x1="10" y1="190" x2="290" y2="190" stroke="#c9d3cc" stroke-width="2"/>
<polygon data-pitch-tri points="20,190 150,120 280,190" fill="rgba(200,144,46,.18)" stroke="#c8902e" stroke-width="3" stroke-linejoin="round"/>
<line data-pitch-rise x1="150" y1="120" x2="150" y2="190" stroke="#123d2f" stroke-dasharray="5 5" stroke-width="2"/>
<text data-pitch-label x="150" y="110" text-anchor="middle" font-family="Manrope, sans-serif" font-weight="800" font-size="16" fill="#123d2f">6/12</text>
</svg></div>
<div class="range-row"><label for="rise">Roof pitch (rise per 12" run) <output for="rise"></output></label><input type="range" id="rise" name="rise" min="1" max="18" step="1" value="6" data-fmt="/12"></div>
<div class="range-row"><label for="length">House length <output for="length"></output></label><input type="range" id="length" name="length" min="20" max="120" step="1" value="60" data-fmt=" ft"></div>
<div class="range-row"><label for="width">House width <output for="width"></output></label><input type="range" id="width" name="width" min="15" max="80" step="1" value="40" data-fmt=" ft"></div>
<div class="range-row"><label for="overhang">Eave overhang <output for="overhang"></output></label><input type="range" id="overhang" name="overhang" min="0" max="3" step="0.5" value="1.5" data-fmt=" ft"></div>
<div class="range-row"><label>Roof shape</label>{seg('shape', [('gable', 'Simple gable'), ('hip', 'Hip roof'), ('complex', 'Complex / many valleys')], 'hip')}</div>
</div>
<div class="result" aria-live="polite">
<span class="kicker light">Your roof</span>
<div class="big"><span data-out="pitch"></span> = <span data-out="deg"></span></div>
<dl><dt>Slope multiplier</dt><dd data-out="mult"></dd><dt>Roof surface area</dt><dd data-out="area"></dd><dt>Roofing squares</dt><dd data-out="squares"></dd>
<dt>Squares to order</dt><dd data-out="order"></dd><dt>Shingle bundles (3/sq)</dt><dd data-out="bundles"></dd><dt>Walkability</dt><dd data-out="walk"></dd></dl>
<p data-out="walknote" class="small"></p>
<a class="btn btn-brass btn-block" href="/free-roof-inspection/">Get it measured for free {icon('arrow')}</a>
<small>Footprint-based estimate. Dormers, multiple roof planes and porches change the total; a measured inspection is the only exact number.</small>
</div></div></form>"""
    pitch_body = f"""<h2>What roof pitch means</h2>
<p>Roof pitch is how many inches a roof rises for every 12 inches of horizontal run. A 6/12 roof rises 6 inches per foot, about 26.6 degrees. Many single-story ranch homes in Quail Valley and Hunters Glen sit around 5/12 or 6/12, while newer two-stories in Sienna and Riverstone often run 7/12 to 10/12 with steeper front gables.</p>
<h2>Why pitch matters</h2>
<ul><li><strong>Material choice:</strong> asphalt shingles need at least 2/12 with special underlayment, and 4/12 or more is standard. Lower slopes need membrane or low-slope metal systems.</li>
<li><strong>Cost:</strong> steeper roofs have more surface area and need extra safety gear, which raises labor.</li>
<li><strong>Drainage:</strong> steeper slopes shed Gulf Coast downpours faster and resist wind-driven rain better.</li></ul>
<h2>How to find your pitch</h2>
<p>Safely, from a ladder at the gable end: hold a level horizontally against the roof edge, measure 12 inches along it, then measure straight up to the roof surface. That number is your rise. Or skip the ladder and let us measure it during a <a href="/free-roof-inspection/">free roof inspection</a>, then plug the numbers into the <a href="/tools/roof-cost-calculator/">roof cost calculator</a>.</p>"""
    pitch_faqs = [
        {"q": "What roof pitch is common in Missouri City?", "a": "Older ranch homes often sit around 5/12 to 6/12, while newer two-story homes in master-planned communities commonly run 7/12 to 10/12."},
        {"q": "How many bundles of shingles are in a square?", "a": "Most architectural shingles come three bundles to a square (100 sq ft). Some heavier designer shingles need four or five."},
        {"q": "How much waste should I add?", "a": "About 10% for a simple gable roof, 15% for hip roofs and up to 20% for complex roofs with many valleys and dormers."},
    ]
    tool_page("/tools/roof-pitch-calculator/", "Roof Pitch Calculator", "Roof Pitch &amp; Area Calculator",
              "Convert roof pitch to degrees, find your slope multiplier and estimate roof squares and shingle bundles from your home's footprint.",
              "Roof Pitch Calculator: Degrees, Squares & Bundles (Free Tool)",
              "Free roof pitch calculator: convert pitch to degrees and get the slope multiplier, roof area, squares and shingle bundles. Built for Missouri City homeowners.",
              pitch_tool, pitch_body, pitch_faqs, "suburb", "Roof Pitch & Area Calculator")

    items = [(3, "Dented gutters, downspouts or roof vents", "Soft metals show hail size and direction"),
             (3, "Shingle pieces or ridge caps in the yard", "A sign of wind damage or lifted shingles"),
             (2, "Granules piled at downspout outlets", "Looks like coarse black sand; shingles losing protection"),
             (3, "Water stains or drips on a ceiling", "Active leak; call soon to avoid decking and drywall damage"),
             (2, "Dented AC condenser fins, mailbox or patio furniture", "Confirms hail hit your property"),
             (2, "Cracked or torn window screens or siding", "A strong sign of hail impacts"),
             (1, "Neighbors are getting roof work or adjuster visits", "Storms hit whole neighborhoods"),
             (2, "Visible missing, lifted or creased shingles", "Wind breaks the seal strip and shingles start flapping"),
             (2, "Large limbs fell on or brushed the roof", "Common after tropical storms in tree-lined neighborhoods"),
             (1, "Hail 1 inch (quarter-size) or larger was reported", "Check the NWS storm reports for your area")]
    checks = "".join(f'<label><input type="checkbox" value="{w}"><span><strong>{e(t)}</strong><small>{e(s)}</small></span></label>' for w, t, s in items)
    storm_tool = f"""<form data-tool="storm" onsubmit="return false"><div class="tool-grid">
<div><h2 class="tool-h">What do you see from the ground?</h2><p class="muted">Stay off the roof. Walk the property and tick everything that applies.</p>
<div class="check-list">{checks}</div>
<div class="range-row" style="margin-top:20px"><label for="age">Roof age <output for="age"></output></label><input type="range" id="age" name="age" min="0" max="30" step="1" value="10" data-fmt=" yrs"></div>
</div>
<div class="result" aria-live="polite">
<span class="kicker light">Damage likelihood</span>
<div class="big" data-out="pct">0%</div>
<div class="meter"><span data-out="meter"></span></div>
<h3 data-out="level"></h3>
<p data-out="advice"></p>
<a class="btn btn-brass btn-block" href="/free-roof-inspection/">Book a free damage inspection {icon('arrow')}</a>
<small>This self-check is a guide, not a diagnosis. Only an up-close inspection can confirm storm damage. Nothing you enter is saved or sent.</small>
</div></div></form>"""
    storm_body = f"""<h2>Why most storm damage goes unnoticed</h2>
<p>Hail damage on asphalt shingles usually looks like small dark spots where granules were knocked off, or soft "bruises" you can only feel by hand. From the driveway, a hail-hit roof often looks fine. The clues are on the softer things around your home: gutters, vents, AC fins and screens.</p>
<h2>What to do after hail or high wind in Missouri City</h2>
<ol><li><strong>Stay safe.</strong> Avoid downed power lines and don't climb on the roof.</li>
<li><strong>Document.</strong> Photograph dents, debris and any interior water spots, with dates.</li>
<li><strong>Prevent more damage.</strong> If water is coming in, call us about an emergency tarp.</li>
<li><strong>Get an inspection.</strong> A <a href="/free-roof-inspection/">free roof inspection</a> confirms whether there's damage worth claiming.</li>
<li><strong>Then decide on a claim.</strong> See the <a href="/blog/filing-a-roof-insurance-claim-in-fort-bend-county/">Fort Bend County roof insurance claim guide</a>.</li></ol>
<h2>Watch out for storm chasers</h2>
<p>After big storms, out-of-town crews knock on doors across Missouri City. Be cautious with anyone who offers to "cover your deductible" (illegal in Texas), pushes you to sign that day, or can't give you a local address. Read <a href="/blog/how-to-hire-a-roofer-in-missouri-city/">how to hire a roofer in Missouri City</a>, check <a href="/weather/">Storm Watch</a> for recent alerts, or call <a href="tel:{TEL}">{PHONE}</a>.</p>"""
    storm_faqs = [
        {"q": "How soon after a storm should I get my roof inspected?", "a": "As soon as practical, ideally within a few weeks. Many Texas policies set deadlines for reporting storm damage, and small breaks can leak with the next rain."},
        {"q": "Can I see hail damage from the ground?", "a": "Usually not on the shingles themselves. Dents in gutters, vents and AC fins are the best ground-level clues."},
        {"q": "Will filing a claim raise my premium?", "a": "Weather claims are generally treated differently from at-fault claims, but every insurer is different. Ask your agent, and get an inspection first so you only file when there's real damage."},
    ]
    tool_page("/tools/storm-damage-checklist/", "Storm Damage Self-Check", "Storm Damage Roof Self-Check",
              "Just had hail or high wind in Missouri City? Tick what you see from the ground and get an instant damage-likelihood score and next steps.",
              "Storm & Hail Damage Roof Checklist | Missouri City Roofers",
              "Free storm damage self-check for Missouri City homeowners. Answer a few questions after hail or wind to see how likely roof damage is, then book an inspection.",
              storm_tool, storm_body, storm_faqs, "storm-sky", "Storm Damage Roof Self-Check")

    url = "/tools/"
    crumbs = [("Home", "/"), ("Tools", url)]
    cards = [("/tools/roof-cost-calculator/", "calculator", "Roof Cost Calculator", "Estimate a replacement price range for your Missouri City home by size, pitch and material."),
             ("/tools/roof-pitch-calculator/", "ruler", "Roof Pitch & Area Calculator", "Pitch to degrees, slope multiplier, roof squares and shingle bundles."),
             ("/tools/storm-damage-checklist/", "clipboard", "Storm Damage Self-Check", "After hail or wind, score how likely your roof is to be damaged."),
             ("/weather/", "cloud-rain", "Storm Watch: Live Weather", "Current conditions, NWS alerts and a 7-day forecast with roof-risk ratings.")]
    grid = "".join(f'<a class="tile" href="{h}" data-reveal><span class="tile-ico">{icon(ic)}</span><b>{e(t)}</b><span>{e(d)}</span><span class="tile-go">Open {icon("arrow")}</span></a>'
                   for h, ic, t, d in cards)
    main = (B.page_hero(crumbs, "Free Roofing Tools for Missouri City Homeowners", "Calculators and checklists to help you plan, budget and protect your roof. Free, instant and private.", bg="home-modern", eyebrow="Tools") +
            f'<section class="section"><div class="wrap"><div class="tiles two">{grid}</div></div></section>' + B.final_cta())
    B.add(url, B.page(url, "Free Roofing Calculators & Tools | Missouri City Roofers",
                      "Free roofing tools for Missouri City, TX homeowners: roof replacement cost calculator, roof pitch and area calculator, storm damage self-check and live weather.",
                      main, schema=[B.crumbs_schema(crumbs)]), priority="0.7")


# --------------------------------------------------------------------------- about / contact / legal
def build_about():
    url = "/about/"
    crumbs = [("Home", "/"), ("About", url)]
    practices = [("camera", "Photos of everything", "Every inspection and every job is photo-documented, so you never have to take our word for it."),
                 ("shield", "No-pressure advice", "If a repair will do, we say so. If your roof is fine, we say that too."),
                 ("file-check", "Insurance done honestly", "We document damage and meet adjusters, and we follow Texas law: no waived or rebated deductibles."),
                 ("clipboard", "Itemized estimates", "Underlayment, flashing, ventilation, decking and disposal, spelled out line by line."),
                 ("home", "Respect for your property", "Tarps over landscaping, daily cleanup and a magnetic nail sweep before we leave."),
                 ("phone", "We pick up the phone", "Questions after the job? Call the same number you called the first time.")]
    cards = "".join(f'<div class="tile static" data-reveal><span class="tile-ico">{icon(ic)}</span><b>{e(t)}</b><span>{e(d)}</span></div>' for ic, t, d in practices)
    main = (B.page_hero(crumbs, "About Missouri City Roofers", "A local roofing company for Missouri City homeowners who want straight answers, careful work and a roofer who'll still be here next storm season.", bg="crew", eyebrow="Who we are") +
            f"""<section class="section"><div class="wrap intro-grid">
<div data-reveal><span class="kicker">Our approach</span><h2>Roofing the way we'd want it done on our own homes</h2>
<p>Missouri City Roofers started with a simple idea: homeowners here deserve a roofer who explains things clearly, prices fairly and doesn't vanish when storm season ends. Too many Fort Bend County families have dealt with door-knockers who rush a claim, rush a roof and leave town.</p>
<p>We do it differently. Every job starts with a <a href="/free-roof-inspection/">free roof inspection</a> and a photo report. We recommend what your roof needs, not what makes the biggest invoice, and we build for real local conditions: heat, humidity, hail, hurricane-force wind and the big trees that shade so many Missouri City streets.</p>
<p>From Quail Valley and Lake Olympia to Sienna, Riverstone and across Fort Bend County, we want to be the roofer neighbors recommend to neighbors.</p>
<a class="btn" href="tel:{TEL}">{icon('phone')} {PHONE}</a></div>
<div class="intro-img" data-reveal>{img('roofer-work', 'Roofing crew working on a brick home')}</div>
</div></section>
<section class="section sec-cream"><div class="wrap"><div class="sec-head" data-reveal><span class="kicker">How we work</span><h2>Six promises on every roof</h2></div>
<div class="tiles three">{cards}</div></div></section>
<section class="section"><div class="wrap"><div class="sec-head" data-reveal><span class="kicker">What we do</span><h2>Our roofing services</h2></div>
<div class="tiles">{service_tiles()}</div></div></section>""" + B.final_cta())
    B.add(url, B.page(url, "About Missouri City Roofers | Local Roofing Company",
                      "Meet Missouri City Roofers, a local roofing company in Missouri City, TX. Free roof inspections, photo-documented work, honest estimates and storm help.",
                      main, schema=[B.crumbs_schema(crumbs)]), priority="0.6")


def build_contact():
    url = "/contact/"
    crumbs = [("Home", "/"), ("Contact", url)]
    main = (B.page_hero(crumbs, "Contact Missouri City Roofers", "Call, text or send a request. We'll get back to you quickly to schedule your free roof inspection.", bg="home-dusk", eyebrow="Get in touch") +
            f"""<section class="section"><div class="wrap form-split">
<div data-reveal><h2>Talk to a Missouri City roofer</h2>
<p>Active leak, storm damage or just planning ahead, we're glad to help. The fastest way to reach us is by phone.</p>
<a class="contact-line" href="tel:{TEL}">{icon('phone')} {PHONE}</a>
<a class="contact-line small" href="mailto:{EMAIL}">{icon('mail')} {EMAIL}</a>
<dl class="facts">
<dt>{icon('pin')} Service area</dt><dd>Missouri City, Sienna, Sugar Land, Stafford, Pearland, Fresno and Richmond</dd>
<dt>{icon('home')} ZIP codes</dt><dd>77459, 77489 and surrounding</dd>
<dt>{icon('alert')} Active leak?</dt><dd>Call us. We can arrange emergency tarping to prevent further damage.</dd>
</dl>
<div class="wx-panel" data-wx-mini style="margin-top:28px"><p>Loading Missouri City weather…</p></div>
</div>
<div class="form-card" data-reveal>{B.lead_form('contact-form', heading='Send us a message', sub='We usually respond the same business day.', full=True)}</div>
</div></section>""")
    B.add(url, B.page(url, "Contact Missouri City Roofers | Call (512) 297-7580",
                      "Contact Missouri City Roofers for a free roof inspection, roof repair or replacement quote in Missouri City, TX. Call (512) 297-7580 or send a request online.",
                      main, schema=[B.crumbs_schema(crumbs), {"@type": "ContactPage", "url": SITE + url}], scripts=("weather",), popup=False), priority="0.6")


def build_simple():
    main = f"""<section class="center-hero"><div class="wrap" data-reveal><span class="kicker">Request received</span><h1>Thank you!</h1>
<p class="lead">Your request is on its way. A Missouri City roofer will call you shortly to schedule your free roof inspection. Need us sooner?</p>
<div class="actions"><a class="btn" href="tel:{TEL}">{icon('phone')} Call {PHONE}</a><a class="btn btn-line" href="/blog/">Read our roofing guides</a></div></div></section>"""
    B.add("/thank-you/", B.page("/thank-you/", "Thank You | Missouri City Roofers", "Thanks for contacting Missouri City Roofers. A local roofer will call you shortly to schedule your free roof inspection in Missouri City, TX.", main, noindex=True, popup=False), sitemap=False)

    main = f"""<section class="center-hero"><div class="wrap"><span class="kicker">Error 404</span><h1>This page blew off the roof</h1>
<p class="lead">The page you're looking for doesn't exist or has moved. Let's get you back on solid ground.</p>
<div class="actions"><a class="btn" href="/">Back to home</a><a class="btn btn-line" href="/free-roof-inspection/">Free roof inspection</a></div></div></section>"""
    B.write("/404.html", B.page("/404.html", "Page Not Found | Missouri City Roofers", "This page could not be found. Head back to Missouri City Roofers for free roof inspections, roof repair and roof replacement in Missouri City, TX.", main, noindex=True, popup=False))

    legal = {
        "/privacy-policy/": ("Privacy Policy", f"""<p>Last updated: {B.fmt_date(B.TODAY.isoformat())}</p>
<p>This Privacy Policy explains how Missouri City Roofers ("we", "us") collects and uses information through missouricityroofs.com.</p>
<h2>Information we collect</h2><p>When you submit a form, we collect the details you provide, such as your name, phone number, email address, property address and message, along with the page you submitted from, the time, and your IP address for spam prevention.</p>
<h2>How we use it</h2><p>We use your information only to respond to your request, schedule inspections, provide estimates and service, and keep basic business records. We may call or text you about your request.</p>
<h2>Sharing</h2><p>We do not sell or rent your personal information. We share it only with service providers who help us operate (such as email delivery), when required by law, or with your permission (for example, with your insurance adjuster at your request).</p>
<h2>Third-party services</h2><p>Our weather features load forecast data from Open-Meteo and alerts from the National Weather Service, and our pages load fonts from Google Fonts. Those services may receive your IP address as part of normal web requests. Our calculators run entirely in your browser; nothing you enter in them is stored or sent.</p>
<h2>Cookies and storage</h2><p>We do not use advertising cookies. Your browser's session storage remembers whether you've closed our inspection pop-up so it doesn't reappear on every page.</p>
<h2>Your choices</h2><p>To ask us to update or delete information you've sent us, call {PHONE} or email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Changes</h2><p>We may update this policy from time to time. The date at the top shows the latest version.</p>"""),
        "/terms/": ("Terms of Use", f"""<p>Last updated: {B.fmt_date(B.TODAY.isoformat())}</p>
<p>By using missouricityroofs.com you agree to these terms.</p>
<h2>Informational content</h2><p>Articles, calculators, cost ranges and weather information on this site are for general information only. They are not quotes, engineering advice, insurance advice or legal advice. Weather data comes from third parties and may be delayed or inaccurate; always follow official National Weather Service warnings.</p>
<h2>Estimates and services</h2><p>Any roofing work is governed by a separate written agreement. Prices shown on this site are planning ranges and may differ from your written estimate.</p>
<h2>Insurance</h2><p>Missouri City Roofers is a roofing contractor, not a public adjuster or insurance company. Coverage decisions are made by your insurer. In accordance with Texas Business &amp; Commerce Code §27.02, we do not waive, rebate or pay any portion of an insurance deductible.</p>
<h2>Intellectual property</h2><p>Site content is owned by Missouri City Roofers or used under license. Photos are licensed stock or public-domain images and may not depict our own projects.</p>
<h2>Limitation of liability</h2><p>The site is provided "as is" without warranties of any kind. To the extent permitted by law, Missouri City Roofers is not liable for damages arising from use of the site.</p>
<h2>Contact</h2><p>Questions about these terms? Call {PHONE} or email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>"""),
    }
    for url, (name, body) in legal.items():
        crumbs = [("Home", "/"), (name, url)]
        main = (f'<section class="center-hero slim"><div class="wrap">{B.crumbs_html(crumbs)}<h1>{name}</h1></div></section>'
                f'<section class="section"><div class="wrap"><article class="prose narrow">{body}</article></div></section>')
        B.add(url, B.page(url, f"{name} | Missouri City Roofers", f"{name} for Missouri City Roofers (missouricityroofs.com), a local roofing company offering free roof inspections, repairs and replacements in Missouri City, TX.", main,
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
