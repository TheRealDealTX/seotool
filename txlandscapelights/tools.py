"""Interactive tool pages (/tools/...). Behaviour lives in src/assets/js/tools.js."""
import json

import photos
import svgart
from build import cta_band, esc, faq_block, faq_schema, page, phero, quote_section
from siteconf import BASE, TOOLS, WEATHER, icon


def rng(key, label, mn, mx, step, val, unit_out=True, cls=""):
    return (f'<div class="rng"><label for="{key}-{label[:3]}"><span>{label}</span><output data-out="{key}"></output></label>'
            f'<input class="{cls}" id="{key}-{label[:3]}" type="range" min="{mn}" max="{mx}" step="{step}" value="{val}" data-in="{key}"></div>') if unit_out else (
            f'<div class="rng"><div class="rng__h"><span>{label}</span><b data-show="{key}"></b></div><input type="range" min="{mn}" max="{mx}" step="{step}" value="{val}" data-in="{key}" aria-label="{label}"></div>')


def num_in(key, label, val, step="any", mn="0"):
    return f'<label class="fld"><span>{label}</span><input class="inp" type="number" inputmode="decimal" min="{mn}" step="{step}" value="{val}" data-in="{key}"></label>'


def sel(key, label, options, val):
    o = "".join(f'<option value="{v}"{" selected" if str(v) == str(val) else ""}>{esc(t)}</option>' for v, t in options)
    return f'<label class="fld"><span>{label}</span><select data-in="{key}">{o}</select></label>'


def kv(*pairs):
    return '<div class="kv">' + "".join(f'<div><span>{a}</span><b data-out="{b}">—</b></div>' for a, b in pairs) + "</div>"


def visualizer_box(pid):
    tog = "".join(f'<label class="tog"><input type="checkbox" data-layer="{k}" checked><span>{n}</span></label>' for k, n in (("arch", "Architecture"), ("path", "Pathways"), ("tree", "Trees"), ("patio", "Patio")))
    pre = "".join(f'<button type="button" class="chip{" is-on" if k == "balanced" else ""}" data-preset="{k}">{n}</button>' for k, n in (("subtle", "Subtle"), ("balanced", "Balanced"), ("showcase", "Showcase"), ("welcome", "Welcome home")))
    return f"""<div class="vis" data-tool="visualizer">
<div class="frame">{svgart.scene(pid, "Interactive lighting visualizer: a home with switchable lighting layers")}</div>
<div class="vis__panel"><h3>Lighting layers</h3><div class="toggles">{tog}</div>
<h3>Presets</h3><div class="presets">{pre}</div>
{rng("k", "Color temperature", 2200, 5000, 100, 2700, cls="k-range")}
{rng("int", "Brightness", 20, 100, 1, 100)}
<p class="mut" style="font-size:.9rem;margin:-6px 0 0" data-out="kname"></p>
<div class="readout"><div><span>Fixtures</span><b data-out="fx">—</b></div><div><span>LED load</span><b data-out="w">—</b></div><div><span>Monthly cost*</span><b data-out="mo">—</b></div><div><span>Transformer</span><b data-out="tx">—</b></div></div>
<p class="tsmall">*6 hours a night at 15¢/kWh. Planning estimate only.</p></div>
</div>"""


def t_visualizer():
    return visualizer_box("tool-vis"), [
        ("How the visualizer works", "<p>Each switch represents one lighting layer on a typical Texas home: architectural uplights on the stone facade and gable, path lights along the front walk, uplights in the live oak, and bistro lights over the patio. Turning a layer on adds a realistic number of fixtures and LED wattage for that part of the property.</p><p>The color temperature slider uses a true Kelvin-to-RGB conversion, so 2700K looks like the warm white most homes use, while 4000K and above starts to read cool and moonlike. Brightness scales the LED load, which feeds the monthly cost and the transformer suggestion.</p>"),
        ("Using it to plan your own yard", "<p>Start with the <strong>Balanced</strong> preset, then turn layers off to see what each contributes. Most homeowners discover that the tree and architecture layers create the drama, while path lights mostly add safety. If you are budgeting in phases, the layers you would miss most are the ones to install first.</p><p>When you are ready for numbers specific to your property, the <a href=\"/tools/fixture-estimator/\">fixture estimator</a> takes your real measurements, and a <a href=\"/quote/\">free consultation</a> with a night demo shows the real thing on your home.</p>"),
    ], [("Is the visualizer accurate for my home?", "It is a planning illustration. Fixture counts and wattages are typical for a medium home, so use it to compare layers and color temperatures, then get a site-specific design."),
         ("What color temperature should I choose?", "Most Texas homes look best between 2700K and 3000K. Warmer flatters brick and wood, slightly cooler suits white limestone and silver foliage."),
         ("Why does the patio layer add so many fixtures?", "String and bistro lights count every bulb, but each one draws very little power, which is why the wattage barely moves.")]


def t_energy():
    sets = [("Small LED (10 × 4 W)", {"n": 10, "w": 4}), ("Medium LED (20 × 5 W)", {"n": 20, "w": 5}), ("Large LED (40 × 6 W)", {"n": 40, "w": 6}), ("Old halogen (20 × 35 W)", {"n": 20, "w": 35})]
    chips = "".join(f"<button type=\"button\" class=\"chip\" data-set='{json.dumps(v)}'>{esc(n)}</button>" for n, v in sets)
    box = f"""<div class="tbox" data-tool="energy">
<div class="tpanel"><h2>Your system</h2><div class="presets">{chips}</div>
<div class="inrow">{num_in("n", "Number of fixtures", 20, "1")}{num_in("w", "Watts per fixture", 5, "0.5")}</div>
{rng("h", "Hours on per night", 1, 14, 0.5, 6)}
{rng("r", "Electricity rate (¢/kWh)", 8, 30, 0.5, 15)}
<p class="tsmall">15¢/kWh is a round planning figure for Texas residential electricity. Check your bill for your actual rate.</p></div>
<div class="tpanel tpanel--out"><span class="eyebrow">Estimated monthly cost</span><span class="big" data-out="mo">—</span>
{kv(("Total load", "tw"), ("Per night", "kn"), ("Per month", "km"), ("Per year", "ky"), ("Cost per night", "cn"), ("Cost per year", "cy"))}
<p class="msg" data-out="msg"></p></div></div>"""
    return box, [
        ("How landscape lighting energy cost is calculated", "<p>The math is simple: <strong>watts × hours ÷ 1,000 = kWh</strong>, then kWh × your rate = cost. A 20-fixture LED system at 5 watts each draws 100 watts. Running six hours a night, it uses 0.6 kWh per night, about 18 kWh a month, which is under $3 at 15¢/kWh.</p><p>Halogen is a different story. The same 20 fixtures with 35-watt MR16 lamps draw 700 watts and cost about seven times as much to run, before you count lamp replacements. Compare both with the <a href=\"/tools/led-savings-calculator/\">LED savings calculator</a>.</p>"),
        ("Trimming the bill without losing the look", "<p>Use an astronomical timer so lights follow the sunset instead of running on a fixed clock. Split the system into zones so path and security lights run later while accent lighting turns off at bedtime. Dimming a layer by even 20% saves energy and often looks better. Read more in <a href=\"/blog/how-much-electricity-does-landscape-lighting-use/\">how much electricity landscape lighting uses</a>.</p>"),
    ], [("How much does LED landscape lighting cost to run per month?", "Most residential LED systems cost a few dollars a month at typical Texas rates. Large estates with 50+ fixtures may run $10 to $15."),
        ("Does running lights dusk to dawn cost much more?", "In Texas winter that can mean 13 hours a night instead of 6, so roughly double. Many owners run accents until midnight and leave only path or security zones on all night."),
        ("Do transformers use power when lights are off?", "Modern transformers draw very little at idle. The bigger loss is running a transformer far below its capacity with old magnetic units, which a professional sizing avoids.")]


def t_estimator():
    box = f"""<div class="tbox" data-tool="estimator">
<div class="tpanel"><h2>Describe your property</h2>
{rng("facade", "Front facade width (ft)", 0, 200, 5, 70)}
{rng("cols", "Columns, gables & entry features", 0, 12, 1, 3)}
{rng("walk", "Walkway length (ft)", 0, 200, 5, 40)}
{rng("drive", "Driveway length to light (ft)", 0, 400, 10, 60)}
{rng("big", "Large trees (live oak, pecan)", 0, 10, 1, 2)}
{rng("small", "Small trees, palms, specimen plants", 0, 15, 1, 3)}
{rng("patio", "Patio / outdoor living (sq ft)", 0, 1200, 20, 300)}
{rng("steps", "Steps or wall lights", 0, 20, 1, 0)}
{sel("style", "Design style", [(0.75, "Subtle and minimal"), (1, "Balanced"), (1.3, "Dramatic showcase")], 1)}
</div>
<div class="tpanel tpanel--out"><span class="eyebrow">Estimated fixtures</span><span class="big" data-out="total">—</span>
<div class="table-wrap"><table><thead><tr><th>Area</th><th>Fixtures</th><th>LED watts</th></tr></thead><tbody data-out="rows"></tbody></table></div>
<div class="kv"><div><span>Total LED load</span><b data-out="watts">—</b></div><div><span>Suggested transformer</span><b data-out="tx">—</b></div></div>
<p class="msg" data-out="sum"></p><p class="tsmall">*6 hours a night at 15¢/kWh. Planning estimate only; your design may differ.</p></div></div>"""
    return box, [
        ("Rules of thumb behind the estimate", "<p>The estimator uses common professional spacing guidelines: roughly one facade uplight per 10 feet of elevation, path lights every 8 to 10 feet, driveway markers every 15 to 20 feet, and two or three uplights for a large spreading tree like a mature live oak. Patio lighting is estimated by area. The style setting scales everything up or down.</p><p>Read the reasoning in our guides to <a href=\"/blog/path-light-spacing/\">path light spacing</a> and <a href=\"/blog/tree-uplighting-guide/\">how to uplight a tree</a>.</p>"),
        ("From fixture count to budget", "<p>Professional installs are usually priced per fixture installed, so the count is the biggest driver of cost. Our <a href=\"/blog/landscape-lighting-cost-texas/\">Texas landscape lighting cost guide</a> gives typical per-fixture planning ranges. For an exact number, a <a href=\"/quote/\">free consultation</a> turns this estimate into a written proposal.</p>"),
    ], [("How many lights does an average Texas home need?", "A typical front yard with a facade, walkway and one or two trees lands between 15 and 30 fixtures. Full front and back designs often run 30 to 60."),
        ("Is more fixtures always better?", "No. Balance matters more than quantity. A well-designed system uses enough fixtures to avoid hot spots and dark gaps, and no more."),
        ("Can I install in phases?", "Yes. Size the transformer and main wire runs for the full plan, then add fixtures as budget allows.")]


def t_transformer():
    box = f"""<div class="tbox" data-tool="transformer">
<div class="tpanel"><h2>1 · Transformer size</h2>
<div class="inrow">{num_in("n", "Number of fixtures", 24, "1")}{num_in("w", "Watts per fixture", 5, "0.5")}</div>
<div class="kv"><div><span>Minimum transformer</span><b data-out="tx">—</b></div><div><span>Math</span><b data-out="txs" style="font-size:.95rem">—</b></div></div>
<h2 style="margin-top:26px">2 · Voltage drop on one run</h2>
{rng("load", "Load on this run (W)", 10, 300, 5, 60)}
{rng("len", "Distance to first fixture (ft)", 10, 300, 5, 100)}
{sel("g", "Wire gauge", [(2.525, "14 AWG"), (1.588, "12 AWG"), (0.999, "10 AWG"), (0.628, "8 AWG")], 1.588)}
{sel("tap", "Transformer tap", [(12, "12 V"), (13, "13 V"), (14, "14 V"), (15, "15 V")], 12)}
</div>
<div class="tpanel tpanel--out"><span class="eyebrow">Voltage at the fixtures</span><span class="big" data-out="vend">—</span>
{kv(("Current on run", "amps"), ("Voltage drop", "vd"), ("Suggested tap", "best"))}
<p class="msg" data-out="msg"></p>
<p class="tsmall">Formula: drop = amps × (2 × length × ohms per 1,000 ft) ÷ 1,000, using a 12 V nominal load. Integrated LED fixtures often accept a wide range (for example 9–15 V); always check the spec sheet.</p></div></div>"""
    return box, [
        ("Why the 80% rule matters", "<p>Transformers last longest and run coolest below their rated capacity. Professionals size them so the connected load is no more than about 80% of the rating, which also leaves headroom to add fixtures later. In a Texas summer, when the transformer box can sit in full sun, that headroom matters even more.</p>"),
        ("Fixing voltage drop", "<p>Low-voltage systems lose voltage over long wire runs. Too much drop makes the far fixtures dim or flicker. The fixes are a higher transformer tap, heavier wire, shorter runs, or wiring methods like a hub or T split that feed fixtures from the middle. See the full <a href=\"/blog/landscape-lighting-transformer-sizing/\">transformer sizing guide</a>, or let us <a href=\"/services/landscape-lighting-repair/\">diagnose an existing system</a>.</p>"),
    ], [("What size transformer do I need for 20 LED lights?", "At 5 W each, 20 fixtures draw 100 W. Divided by 0.8 that is 125 W, so a 150 W transformer works, with a 200 W unit leaving room to grow."),
        ("Is 12 gauge wire enough?", "12 AWG is the workhorse for most residential runs. Long runs or heavy loads may need 10 or 8 AWG to keep voltage in range."),
        ("Can I plug a transformer into any outdoor outlet?", "It should be a weatherproof, GFCI-protected outlet. New outlets or circuits should be installed by a licensed electrician.")]


def t_led():
    box = f"""<div class="tbox" data-tool="led">
<div class="tpanel"><h2>Your current system</h2>
<div class="inrow">{num_in("n", "Number of fixtures", 20, "1")}{num_in("hw", "Halogen watts each", 35, "1")}</div>
<div class="inrow">{num_in("lw", "LED watts each", 5, "0.5")}{num_in("lamp", "Halogen lamp cost ($)", 8, "0.5")}</div>
{rng("h", "Hours on per night", 1, 14, 0.5, 6)}
{rng("r", "Electricity rate (¢/kWh)", 8, 30, 0.5, 15)}
{num_in("cost", "LED upgrade cost per fixture ($, optional)", 0, "1")}
</div>
<div class="tpanel tpanel--out"><span class="eyebrow">Estimated yearly savings</span><span class="big" data-out="save">—</span><p class="mut" data-out="pct"></p>
<div class="bars"><div>Halogen energy cost / yr: <b data-out="ch"></b><i data-out="bh"></i></div><div>LED energy cost / yr: <b data-out="cl"></b><i data-out="bl"></i></div></div>
{kv(("kWh saved / yr", "kwh"), ("Halogen lamps / yr", "lamps"), ("Lamp cost avoided", "lampc"), ("Payback", "pay"))}
<p class="tsmall">Assumes halogen lamps last about 3,000 hours. LED fixtures typically last many years longer.</p></div></div>"""
    return box, [
        ("Where the savings come from", "<p>An LED lamp or integrated LED fixture produces similar light with roughly 80 to 90% less power than a halogen MR16. On top of the energy, halogen lamps burn out every year or two in normal use and run hot, which cooks gaskets and lenses in a Texas summer. LED removes most of that maintenance.</p>"),
        ("Retrofit or replace?", "<p>If your fixtures are solid brass or copper and in good shape, an LED lamp retrofit is often the best value. Corroded aluminum fixtures, cracked lenses or failing sockets usually justify replacing the fixture with integrated LED. Old magnetic transformers may also need attention. Read <a href=\"/blog/halogen-to-led-landscape-lighting/\">halogen to LED: what to know</a> or <a href=\"/services/landscape-lighting-repair/\">book an upgrade assessment</a>.</p>"),
    ], [("How much can I save switching landscape lighting to LED?", "A 20-fixture halogen system at 35 W running six hours a night at 15¢/kWh costs about $230 a year in energy. The LED version costs about $33, before counting lamp replacements."),
        ("Will LED lamps work with my old transformer?", "Usually, but magnetic transformers and very light loads can cause flicker. We check transformer type, tap voltage and load during a retrofit."),
        ("Do LED lamps look as warm as halogen?", "Quality LED lamps at 2700K closely match the warm look of halogen. We match color temperature across the whole system so nothing looks mismatched.")]


def t_kelvin():
    presets = "".join(f'<button type="button" class="chip" data-k="{k}">{k}K</button>' for k in (2200, 2700, 3000, 4000, 5000))
    mats = [("Red brick", "#8c3b2a"), ("Austin limestone", "#d8cfb8"), ("Stucco", "#e9e2d4"), ("Cedar", "#9a6238"), ("Live oak leaf", "#3e5a2e"), ("Texas sage", "#9fa79a")]
    sw = "".join(f'<div class="swatch"><div class="swatch__s" style="--m:{c}"></div><span>{n}</span></div>' for n, c in mats)
    box = f"""<div class="tbox" data-tool="kelvin">
<div class="tpanel"><h2>Choose a color temperature</h2><div class="presets">{presets}</div>
{rng("k", "Color temperature", 2200, 5000, 100, 2700, cls="k-range")}
<div class="ktint" data-out="tint"><span data-out="kbig"></span></div>
<p class="mut" data-out="kdesc"></p></div>
<div class="tpanel tpanel--out"><span class="eyebrow">At this temperature</span><span class="big" data-out="kname" style="font-size:2.4rem">—</span>
<div class="kv"><div><span>Feel</span><b data-out="kfeel" style="font-size:1.05rem">—</b></div><div><span>Best for</span><b data-out="kbest" style="font-size:.95rem;font-family:inherit;font-weight:500">—</b></div></div>
<h3 style="font-size:1rem;text-transform:uppercase;letter-spacing:.08em;color:var(--mut)">How common Texas materials look</h3><div class="swatches">{sw}</div></div></div>"""
    return box, [
        ("Kelvin in plain English", "<p>Color temperature describes how warm or cool white light looks, measured in Kelvin (K). Candlelight is about 1900K, a classic halogen landscape lamp about 2800–3000K, and noon daylight about 5500K. Lower numbers look golden and cozy; higher numbers look crisp and blue.</p><p>Most residential landscape lighting in Texas is designed between <strong>2700K and 3000K</strong>. That range flatters red brick, Austin stone, cedar and the deep greens of live oaks, and it feels like home rather than a commercial parking lot.</p>"),
        ("When to mix temperatures", "<p>Experienced designers sometimes use slightly cooler light, around 4000K, for moonlighting high in a tree or on silver plants like Texas sage and agave, while keeping the house warm. The key is intention and consistency. Learn more in <a href=\"/blog/warm-white-vs-cool-white-landscape-lighting/\">warm white vs cool white landscape lighting</a>.</p>"),
    ], [("What is the best color temperature for landscape lighting?", "2700K is the most common choice for homes. 3000K is a good option for white limestone, light stucco and modern architecture."),
        ("Does cool white attract more bugs?", "Insects are generally more attracted to the blue end of the spectrum, so warmer light near patios tends to draw fewer bugs."),
        ("Can you change color temperature later?", "With some fixtures and smart lamps, yes. Many quality fixtures also offer interchangeable lamps in different Kelvin ratings.")]


def t_sunset():
    cities = {slug: {"n": n, "la": la, "lo": lo, **({"tz": "America/Denver"} if slug == "el-paso" else {})} for slug, n, la, lo in WEATHER}
    opts = [(slug, n) for slug, n, la, lo in WEATHER]
    box = f"""<div class="tbox tbox--wide" data-tool="sunset" data-cities='{esc(json.dumps(cities))}'>
<div class="tbox" style="grid-template-columns:.9fr 1.1fr">
<div class="tpanel"><h2>Your city &amp; schedule</h2>
{sel("city", "Texas city", opts, "houston-tx")}
<div style="height:14px"></div>
{sel("on", "Lights turn on", [(0, "At sunset"), (15, "15 min after sunset"), (30, "30 min after sunset"), (-15, "15 min before sunset")], 15)}
<div style="height:14px"></div>
{sel("off", "Lights turn off", [(22, "10:00 pm"), (23, "11:00 pm"), (24, "Midnight"), (25, "1:00 am"), ("dawn", "At sunrise (dusk to dawn)")], 23)}
<div style="height:14px"></div>
{num_in("w", "Total system watts", 100, "5")}
</div>
<div class="tpanel tpanel--out"><span class="eyebrow">Sunset tonight in <span data-out="cname"></span></span><span class="big" data-out="today">—</span>
{kv(("Hours on per year", "hrs"), ("kWh per year", "kwh"), ("Energy cost / yr*", "cost"))}
<p class="tsmall">*At 15¢/kWh. Sunset times are calculated for the 15th of each month and may differ by a few minutes from local almanacs.</p></div></div>
<div class="tpanel" style="margin-top:18px"><h2>Month by month</h2><div class="table-wrap"><table><thead><tr><th>Month</th><th>Sunset</th><th>Sunrise</th><th>Lights on</th><th>Run time</th></tr></thead><tbody data-out="rows"></tbody></table></div></div>
</div>"""
    return box, [
        ("Why a fixed timer gets it wrong in Texas", "<p>Sunset in Texas moves by around three hours across the year, from a little after 5:20 pm in early December in Houston to around 8:30 pm or later in late June in North and West Texas. A mechanical timer set in summer leaves your yard dark for hours in winter, and a winter setting wastes energy in summer. Daylight saving time adds another jump twice a year.</p><p>An <a href=\"/services/smart-lighting-controls/\">astronomical timer</a> solves this by calculating sunset for your exact location every day. Lights come on at the right moment, all year, with no adjustment.</p>"),
        ("Choosing an off time", "<p>Many Texas homeowners run decorative layers until 11 pm or midnight and leave path or security zones on later. Dusk-to-dawn schedules are useful for security but nearly double winter run time. Plug your schedule into the table above and compare the yearly hours and cost, or use the <a href=\"/tools/energy-cost-calculator/\">energy cost calculator</a>.</p>"),
    ], [("What time should landscape lights turn on?", "Around 15 minutes after sunset is a popular setting. The sky still has color, and the lights fade in naturally as it gets dark."),
        ("Do I need to change my timer for daylight saving time?", "Astronomical and smart timers adjust automatically. Older mechanical timers need resetting twice a year."),
        ("How many hours a year do landscape lights run?", "A sunset-to-11 pm schedule in Texas typically runs about 1,500 to 1,800 hours a year. Dusk to dawn is closer to 4,300.")]


BUILDERS = {
    "lighting-visualizer": (t_visualizer, "Landscape Lighting Visualizer | Texas Landscape Lights", "Switch lighting layers on a Texas home, change color temperature and brightness, and see fixture count, watts and running cost update live. Free tool."),
    "energy-cost-calculator": (t_energy, "Landscape Lighting Energy Cost Calculator | Texas", "Estimate the nightly, monthly and yearly electricity cost of LED or halogen landscape lighting at Texas rates. Free calculator from Texas Landscape Lights."),
    "fixture-estimator": (t_estimator, "Landscape Lighting Fixture Estimator | Texas Landscape Lights", "Describe your facade, walkway, driveway, trees and patio to estimate how many landscape lights you need, total LED watts and transformer size."),
    "transformer-sizing-calculator": (t_transformer, "Transformer & Voltage Drop Calculator | Landscape Lighting", "Size a low-voltage landscape lighting transformer with the 80% rule and check voltage drop by wire gauge, run length and tap. Free calculator."),
    "led-savings-calculator": (t_led, "Halogen to LED Savings Calculator | Texas Landscape Lights", "Compare halogen and LED landscape lighting energy cost, lamp replacements and payback at Texas electricity rates. Free LED savings calculator."),
    "color-temperature-guide": (t_kelvin, "Landscape Lighting Color Temperature Guide | 2200K–5000K", "Slide from 2200K to 5000K and see how warm and cool white light looks on brick, limestone, stucco, cedar and Texas plants. Interactive guide."),
    "sunset-timer-planner": (t_sunset, "Texas Sunset Times & Landscape Lighting Timer Planner", "Month-by-month sunset and sunrise times for 22 Texas cities with suggested timer settings, yearly run hours and energy cost for your lighting."),
}


def build():
    home = ("Home", "/")
    for t in TOOLS:
        fn, title, desc = BUILDERS[t["slug"]]
        box, prose, faqs = fn()
        path = f'/tools/{t["slug"]}/'
        trail = [home, ("Tools", "/tools/"), (t["name"], path)]
        others = "".join(f'<a href="/tools/{o["slug"]}/"><small>Tool</small>{esc(o["name"])}</a>' for o in TOOLS if o is not t)
        body = "".join(f'<div class="prose"><h2>{h}</h2>{p}</div>' for h, p in prose)
        app = {"@type": "WebApplication", "name": t["name"], "url": BASE + path, "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any",
               "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": f"{BASE}/#business"}, "description": desc}
        main = (phero("Free planning tool", t["name"], t["short"], trail, photo=photos.TOOL[t["slug"]])
                + f'<section class="sec"><div class="wrap">{box}</div></section>'
                + f'<section class="sec sec--alt"><div class="wrap"><div class="body">{body}<div class="prose"><h2>More free tools</h2></div><div class="related">{others}</div></div></div></section>'
                + faq_block(faqs, "Questions about this tool", light=True) + quote_section(path) + cta_band())
        page(path, title, desc, main, schema=[app, faq_schema(faqs)], priority="0.7", scripts=("site", "tools"), crumbs=trail, image=photos.TOOL[t["slug"]])
    cards = "".join(f'<a class="tool" href="/tools/{t["slug"]}/"><span class="tool__i">{icon(t["icon"])}</span><h3>{esc(t["name"])}</h3><p>{esc(t["short"])}</p><span class="go">Open tool →</span></a>' for t in TOOLS)
    main = (phero("Free planning tools", "Landscape Lighting Calculators & Tools", "Estimate fixtures, transformer size, voltage drop, energy cost and LED savings, explore color temperature and plan your timer around Texas sunsets.", [home, ("Tools", "/tools/")], photo=photos.PAGE["tools"])
            + f'<section class="sec"><div class="wrap"><div class="tools">{cards}</div></div></section>'
            + f'<section class="sec sec--alt"><div class="wrap"><div class="head"><span class="eyebrow">Try it now</span><h2>Lighting visualizer</h2></div>{visualizer_box("hub-vis")}</div></section>'
            + quote_section("/tools/") + cta_band())
    page("/tools/", "Free Landscape Lighting Calculators | Texas Landscape Lights", "Free landscape lighting calculators: visualizer, fixture estimator, transformer and voltage drop, energy cost, LED savings, color temperature and sunset timer.", main, priority="0.8", scripts=("site", "tools"), crumbs=[home, ("Tools", "/tools/")], image=photos.PAGE["tools"])
