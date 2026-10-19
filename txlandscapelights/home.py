"""Homepage for txlandscapelights.com. Primary keyword: "texas landscape lights" (14+ uses in visible copy)."""
import json

import svgart
from build import (cta_band, esc, faq_block, faq_schema, map_block, page, post_card, process_rail, quote_section, service_card)
from siteconf import PHONE, SERVICES, TEL, TOOLS, WEATHER, icon
from tools import visualizer_box

TITLE = f"Texas Landscape Lights | Landscape Lighting Experts | {PHONE}"
DESC = ("Texas Landscape Lights designs, installs and repairs custom LED landscape lighting for homes across Texas. "
        f"Free lighting plan and night demo. Call {PHONE}.")

FAQS = [
    ("What does Texas Landscape Lights do?", "Texas Landscape Lights designs, installs, repairs and upgrades low-voltage LED landscape lighting: architectural uplighting, path and driveway lights, tree and garden lighting, patio and pool lighting, smart controls and commercial or HOA lighting."),
    ("Which parts of Texas do you serve?", "We work with homeowners across Texas, including Houston, Dallas, Fort Worth, Austin, San Antonio, Plano, Frisco, Katy, Sugar Land, The Woodlands, Round Rock and New Braunfels. If your city is not listed, call and ask."),
    ("How much does landscape lighting cost in Texas?", "Most professionally installed low-voltage LED systems are priced per fixture, and the total depends on fixture quality, wire runs, soil and rock, controls and design. Our cost guide gives typical planning ranges, and your written proposal gives an exact number."),
    ("How much does it cost to run LED landscape lighting?", "Very little. A 20-fixture LED system drawing about 100 watts for six hours a night uses roughly 18 kWh a month, which is a few dollars at typical Texas residential rates. Try our energy cost calculator with your own numbers."),
    ("Will the lights survive Texas heat, hail and storms?", "That is what we design for. We specify solid brass, copper or heavy powder-coated aluminum fixtures, sealed waterproof connections, direct-burial wire and GFCI-protected transformers mounted above flood level."),
    ("Do you repair systems another company installed?", "Yes. We diagnose dead zones, cut or corroded wire, failing transformers and voltage drop on any brand, and we convert old halogen systems to LED."),
    ("Can I control the lights from my phone?", "Yes. Astronomical timers follow sunset automatically, and Wi-Fi or smart-home controls add zones, dimming, scenes and away modes you can run from an app."),
    ("How do I get started?", f"Request a quote online or call {PHONE}. We start with a short conversation about your goals, then visit the property and, where it helps, show you a night demo before you decide."),
]

REGIONS = [
    ("gulf", "Gulf Coast", "Houston, Katy, Sugar Land, The Woodlands, Galveston",
     ["Humidity", "Salt air", "Hurricanes", "Flood risk"],
     "Heavy rain, tropical storms and year-round humidity are the enemy of cheap fixtures and taped splices. Coastal and Houston-area systems need sealed connections and corrosion-resistant metals.",
     ["Solid brass or copper fixtures that patina instead of rusting", "Gel-filled waterproof connectors on every splice", "Transformers mounted well above standing water, on GFCI", "Moonlighting in tall pines and live oaks"],
     ["Live oaks and loblolly pines", "Sabal and Mexican fan palms", "Brick traditionals and stucco", "Pools and covered patios"]),
    ("north", "North Texas", "Dallas, Fort Worth, Plano, Frisco",
     ["Hail", "Ice storms", "Clay soil", "HOAs"],
     "DFW lighting has to shrug off hail, the occasional hard freeze and expansive clay that heaves fixtures out of level. Strong HOA standards also reward subtle, glare-free design.",
     ["Heavy-wall fixtures with tempered glass lenses", "Stakes and hubs set for shifting clay", "Warm 2700K on red brick and Austin stone", "Astronomical timers for HOA-friendly schedules"],
     ["Pecans, cedar elms and Shumard oaks", "Red brick and stone traditionals", "Long front elevations", "Master-planned neighborhoods"]),
    ("hill", "Hill Country", "Austin, Round Rock, New Braunfels, San Marcos",
     ["Limestone", "Flash floods", "Dark skies", "Slopes"],
     "Limestone ledges, caliche and steep lots make wire runs harder, and many communities value dark skies. The best Hill Country systems are shielded, downward-aware and very warm.",
     ["Fully shielded fixtures aimed to avoid sky glow", "Grazing light on limestone and stone walls", "Routing wire through rock without scarring the site", "Flood-smart transformer placement near creeks"],
     ["Live oaks, cedar and Texas mountain laurel", "White limestone and metal roofs", "Hillside decks and views", "Native beds, agave and yucca"]),
    ("south", "South Texas", "San Antonio, Corpus Christi, McAllen, Laredo",
     ["Extreme heat", "UV", "Palms", "Outdoor living"],
     "Long, hot seasons mean people live outside after dark. Fixtures must handle intense UV and heat, and patios, courtyards and palms become the stars of the design.",
     ["Integrated LED fixtures rated for high ambient heat", "Courtyard and patio layers on dimmers", "Palm uplighting with wide, warm beams", "Insect-aware color temperatures near seating"],
     ["Palms, mesquite and live oaks", "Spanish revival and stucco", "Courtyards and pergolas", "Tile roofs and arches"]),
    ("west", "West Texas & Panhandle", "El Paso, Lubbock, Midland, Amarillo",
     ["Wind", "Dust", "Dry cold", "Wide open sites"],
     "Big wind, blowing dust and wide-open ranch properties call for sturdy, low-profile fixtures and long, carefully calculated wire runs to keep voltage steady.",
     ["Low-profile, wind-resistant path and well lights", "Heavier-gauge wire for long ranch drives", "Lens choices that stay clean in dust", "Respectful lighting under famously dark skies"],
     ["Desert willow, yucca and agave", "Stucco and adobe-style homes", "Long gated drives", "Xeriscape beds and rock"]),
]


def weather_section():
    data = {slug: {"n": n, "la": la, "lo": lo} for slug, n, la, lo in WEATHER}
    opts = "".join(f'<option value="{slug}"{" selected" if slug == "houston-tx" else ""}>{esc(n)}</option>' for slug, n, la, lo in WEATHER)
    cell = lambda k, label: f'<div class="wx__cell"><span>{label}</span><b data-w="{k}">—</b></div>'
    return f"""<section class="sec" id="weather"><div class="wrap">
<div class="head head--row"><div><span class="eyebrow">Live Texas weather</span><h2>Tonight's lighting forecast</h2>
<p class="lead">Texas weather swings hard, and it shapes how a lighting system should be built. Pick your city for tonight's sunset, low, rain and wind, plus a quick tip from Texas Landscape Lights on what it means for your lights.</p></div></div>
<div class="wx" data-weather='{esc(json.dumps(data))}'>
<div class="wx__main">
<div class="wx__top"><label>City <select class="sel" aria-label="Choose a Texas city">{opts}</select></label><span class="wx__live">Live forecast</span></div>
<div class="wx__now"><span data-w="ico">{icon("moon", "wx__ico")}</span><div><span class="wx__city" data-w="city">Houston, TX</span><div class="wx__temp" data-w="temp">—</div><div class="wx__cond" data-w="cond">Loading the latest forecast…</div></div></div>
<div class="wx__grid">{cell("sunset", "Sunset")}{cell("on", "Lights on")}{cell("low", "Tonight's low")}{cell("rain", "Rain chance")}</div>
<div class="wx__tip" data-w="tip">{icon("bulb")}<div><b>Lighting tip for tonight</b><p>Choose a city to see what tonight's weather means for your outdoor lights.</p></div></div>
</div>
<div class="wx__side"><h3>5-day outlook</h3><div class="wx__days" data-w="days"></div>
<div class="kv" style="margin:0"><div><span>Wind now</span><b data-w="wind">—</b></div><div><span>Status</span><b data-w="upd" style="font-size:1rem">—</b></div></div>
<p class="wx__note">Forecast data from Open-Meteo. "Lights on" is sunset plus 15 minutes, a common astronomical timer setting. Plan a full year with the <a href="/tools/sunset-timer-planner/">sunset &amp; timer planner</a>.</p></div>
</div></div></section>"""


def regions_section():
    tabs, panels = [], []
    for i, (k, name, cities, pills, intro, how, see) in enumerate(REGIONS):
        on = i == 0
        tabs.append(f'<button class="tab" role="tab" id="tab-{k}" aria-controls="rg-{k}" aria-selected="{str(on).lower()}" tabindex="{0 if on else -1}"><span>{name}<small>{cities}</small></span>{icon("arrow")}</button>')
        pl = "".join(f'<span class="pill{" pill--rust" if j < 2 else ""}">{p}</span>' for j, p in enumerate(pills))
        panels.append(f'<div class="tabpanel" role="tabpanel" id="rg-{k}" aria-labelledby="tab-{k}"{"" if on else " hidden"}><h3>{name}</h3><div class="pill-row">{pl}</div><p>{intro}</p>'
                      f'<div class="cols"><div><h4>How we build it</h4><ul>{"".join(f"<li>{x}</li>" for x in how)}</ul></div><div><h4>What we light</h4><ul>{"".join(f"<li>{x}</li>" for x in see)}</ul></div></div></div>')
    return f"""<section class="sec sec--light"><div class="wrap">
<div class="head"><span class="eyebrow">One state, five climates</span><h2>Built for the Texas you live in</h2>
<p class="lead">A system that thrives in Galveston salt air would be overbuilt in Lubbock and wrong for a limestone hillside in Austin. Texas Landscape Lights designs every project around its region's weather, soil, trees and architecture.</p></div>
<div class="tabs" data-tabs><div class="tabs__list" role="tablist" aria-label="Texas regions">{"".join(tabs)}</div><div>{"".join(panels)}</div></div>
</div></section>"""


def build(posts):
    hero = f"""<section class="hero"><div class="wrap">
<div>
<span class="eyebrow">Landscape lighting design &amp; installation</span>
<h1>Texas Landscape Lights <span class="hl">for homes that shine after dark</span></h1>
<p class="lead">Texas Landscape Lights designs, installs and maintains custom low-voltage LED landscape lighting for homeowners across Texas. Warm, balanced light on your architecture, trees, walkways and outdoor living spaces, built to handle Texas heat, hail and storms.</p>
<div class="hero__cta"><a class="btn" href="/quote/">{icon("sparkles")} Get my free lighting plan</a><a class="btn btn--ghost" href="{TEL}">{icon("phone")} {PHONE}</a></div>
<ul class="chips"><li>{icon("moon")} Free night demo</li><li>{icon("shield")} Built for Texas weather</li><li>{icon("bulb")} Warm 12V LED</li><li>{icon("pin")} Statewide service</li></ul>
</div>
<div class="hero__art"><div class="frame">{svgart.scene("hero")}<button class="switch" type="button" data-switch="hero-scene" aria-pressed="false"><span class="switch__t"></span><b>Lights off</b></button></div>
<div class="hero__badge">Free lighting plan<small>Houston · DFW · Austin · SA</small></div></div>
</div></section>
<section class="strip"><div class="wrap">
<div class="strip__i"><b>12<em>V</em></b><span>Safe low-voltage LED systems</span></div>
<div class="strip__i"><b><span data-count="80">80</span><em>%+</em></b><span>Less energy than old halogen lamps</span></div>
<div class="strip__i"><b>2700<em>K</em></b><span>Warm white, our most-specified color</span></div>
<div class="strip__i"><b><span data-count="7">7</span></b><span>Free planning tools for homeowners</span></div>
</div></section>"""

    intro = f"""<section class="sec"><div class="wrap intro">
<div class="intro__k" data-reveal><span class="eyebrow">Why it matters</span><h2>Lighting that changes how you use your home</h2>
<p class="quote-mark">"The goal is not more light. It is the right light, in the right places, at the right warmth."</p></div>
<div class="prose" data-reveal>
<p>A great lighting plan turns a house into a home you look forward to pulling up to. Texas Landscape Lights uses layered, low-glare light to bring out stonework and rooflines, guide guests along walkways, show off mature trees and make patios and pool decks comfortable long after the sun goes down.</p>
<p>Every property is different, so we never install a preset package. We look at how you arrive, where you sit, what you see from inside and which features deserve attention. Then we design a balanced system with the right fixtures, beam spreads, color temperature and controls. The result feels natural: warm, inviting and never like a parking lot.</p>
<p>Texas is also hard on outdoor equipment. Triple-digit summers, Gulf Coast humidity, North Texas hail, Hill Country flash floods and the occasional hard freeze all take a toll. That is why Texas Landscape Lights specifies solid brass, copper and heavy aluminum fixtures, sealed waterproof connections, properly sized transformers and wire that is buried where edgers and aerators will not find it.</p>
<h3>What you get with Texas Landscape Lights</h3>
<ul class="checks"><li>A custom design built around your architecture, trees and how you use the yard</li><li>Professional low-voltage LED fixtures chosen for Texas heat, UV and moisture</li><li>Clean installation with concealed wire and protected beds and roots</li><li>Smart controls that follow the sunset all year, with optional app and zone control</li><li>A final visit after dark to aim and balance every fixture</li></ul>
</div></div></section>"""

    svc_cards = "".join(service_card(s, i, "svc--wide" if i in (0, 6) else "") for i, s in enumerate(SERVICES))
    services = f"""<section class="sec sec--alt" id="services"><div class="wrap">
<div class="head head--row"><div><span class="eyebrow">Services</span><h2>Every layer of light your property needs</h2>
<p class="lead">From the first uplight on your facade to the last bistro bulb over the patio, Texas Landscape Lights handles design, installation, controls, repairs and upgrades.</p></div>
<a class="btn btn--ghost" href="/services/">All services {icon("arrow")}</a></div>
<div class="bento">{svc_cards}<a class="svc svc--full" href="/quote/" style="background:linear-gradient(150deg,#d0663d,#a8461f);border-color:transparent"><span class="svc__n" style="color:#fff">FREE</span><h3>Not sure where to start?</h3><p style="color:#ffe6d9">Tell us what you love about your home and we will design the lighting around it.</p><span class="svc__go" style="color:#fff">Request a lighting plan {icon("arrow")}</span></a></div>
</div></section>"""

    visual = f"""<section class="sec sec--grid" id="visualizer"><div class="wrap">
<div class="head head--center"><span class="eyebrow">Interactive</span><h2>Design your own night in seconds</h2>
<p class="lead">Switch each lighting layer on and off, slide the color temperature and brightness, and watch the fixture count, wattage and monthly running cost update live. This is how Texas Landscape Lights thinks about a property: one layer at a time.</p></div>
{visualizer_box("home-vis")}
</div></section>"""

    tool_cards = "".join(f'<a class="tool" href="/tools/{t["slug"]}/"><span class="tool__i">{icon(t["icon"])}</span><h3>{esc(t["name"])}</h3><p>{esc(t["short"])}</p><span class="go">Open tool →</span></a>' for t in TOOLS)
    tools_sec = f"""<section class="sec sec--alt" id="tools"><div class="wrap">
<div class="head head--row"><div><span class="eyebrow">Free planning tools</span><h2>Plan smarter before you spend a dollar</h2>
<p class="lead">Texas Landscape Lights built these calculators so homeowners can estimate fixtures, transformer size, energy cost and LED savings, and see sunset times for 22 Texas cities.</p></div>
<a class="btn btn--ghost" href="/tools/">All tools {icon("arrow")}</a></div>
<div class="tools">{tool_cards}</div></div></section>"""

    areas = f'<section class="sec" id="areas"><div class="wrap">{map_block(True)}</div></section>'

    why = f"""<section class="sec"><div class="wrap">
<div class="head head--center"><span class="eyebrow">The difference</span><h2>Why Texas homeowners choose Texas Landscape Lights</h2></div>
<div class="cards cards--3">
<article class="card"><span class="card__k">01 · Listen first</span><h3>Designed around you</h3><p>We ask how you use your home after dark before we pick a single fixture. The plan supports your life, not a sales package.</p></article>
<article class="card"><span class="card__k">02 · Restraint</span><h3>Balance over brightness</h3><p>Contrast, shadow and comfortable levels make a property look its best. We light what matters and let darkness do the rest.</p></article>
<article class="card"><span class="card__k">03 · Texas-tough</span><h3>Built for the weather</h3><p>Heat, hail, humidity, floods and freezes are part of the spec, from fixture metals to connector seals and transformer placement.</p></article>
<article class="card"><span class="card__k">04 · Clean work</span><h3>Respect for the landscape</h3><p>Wire is concealed, roots are avoided, beds are protected and the site is left cleaner than we found it.</p></article>
<article class="card"><span class="card__k">05 · After dark</span><h3>We finish at night</h3><p>Glare and balance can only be judged after sunset, so every Texas Landscape Lights project ends with a night aiming visit.</p></article>
<article class="card"><span class="card__k">06 · Honest advice</span><h3>Clear, written proposals</h3><p>You see fixture locations, scope and price in writing. If a repair beats a replacement, we will tell you.</p></article>
</div></div></section>"""

    blog = f"""<section class="sec sec--light"><div class="wrap">
<div class="head head--row"><div><span class="eyebrow">From the blog</span><h2>Guides for lighting a Texas home</h2><p class="lead">Honest cost advice, design ideas and maintenance checklists from the Texas Landscape Lights team.</p></div><a class="btn btn--rust" href="/blog/">Read the blog {icon("arrow")}</a></div>
<div class="posts">{"".join(post_card(p) for p in posts[:3])}</div></div></section>"""

    closing = f"""<section class="sec sec--tight"><div class="wrap"><div class="prose" style="max-width:900px;margin-inline:auto;text-align:center">
<p class="lead">Whether you are in a Houston bungalow, a Frisco new build, a limestone home west of Austin or a ranch outside San Antonio, Texas Landscape Lights can design a system that fits your home, your budget and your climate. Call <a href="{TEL}">{PHONE}</a> or <a href="/quote/">request your free lighting plan</a> today.</p>
</div></div></section>"""

    main = (hero + intro + services + weather_section() + visual + regions_section() + process_rail() + areas + why + tools_sec
            + blog + quote_section("/", "Free lighting plan", "Tell Texas Landscape Lights about your project") + faq_block(FAQS, "Questions about Texas Landscape Lights", light=True)
            + closing + cta_band("Ready to see your home in a new light?", "Talk to Texas Landscape Lights about a custom lighting plan for your property, anywhere in Texas."))
    page("/", TITLE, DESC, main, schema=[faq_schema(FAQS)], priority="1.0", scripts=("site", "tools"))
