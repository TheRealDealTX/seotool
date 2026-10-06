"""Reader tools: /tools/ hub and one page per calculator. Logic lives in public/assets/js/tools.js."""

TOOLS = [
    dict(path="/tools/stone-coated-roof-cost-calculator/", short="Roof cost calculator", name="Stone Coated Roof Cost Calculator",
         title="Stone Coated Steel Roof Cost Calculator (Texas)", keyword="stone coated steel roofing cost",
         description="Estimate stone coated steel roofing cost for your Texas home: enter footprint, pitch, profile and tear-off to see an installed price range vs asphalt.",
         teaser="Footprint, pitch and profile in — an installed price range out, with an asphalt comparison.",
         icon="M4 20h16M6 20V9l6-5 6 5v11M10 20v-6h4v6", related=["/stone-coated-roofing-cost-texas/", "/is-stone-coated-roofing-worth-the-cost-in-texas/", "/stone-coated-vs-asphalt-shingle/"]),
    dict(path="/tools/lifetime-roof-cost-calculator/", short="Lifetime cost calculator", name="Lifetime Roof Cost Calculator",
         title="Lifetime Roof Cost Calculator: Stone Coated vs Asphalt", keyword="stone coated steel roofing vs asphalt shingles",
         description="Compare the 30–70 year cost of a stone coated steel roof vs repeated asphalt replacements, including insurance savings and storm repairs. Find your break-even year.",
         teaser="See the break-even year once asphalt replacements and insurance savings are counted.",
         icon="M3 3v18h18M7 15l4-4 3 3 6-6", related=["/are-stone-coated-roofs-worth-it/", "/stone-coated-steel-roof-lifespan/", "/what-homeowners-regret-about-cheap-roofing-systems/"]),
    dict(path="/tools/insurance-discount-estimator/", short="Insurance discount estimator", name="Class 4 Roof Insurance Discount Estimator",
         title="Class 4 Roof Insurance Discount Calculator (Texas)", keyword="class 4 roof insurance discount",
         description="Estimate how much a Class 4 impact-resistant roof could save on Texas homeowners insurance — yearly, monthly and over the years you own the home.",
         teaser="What a Class 4 roof discount could be worth on your premium, year by year.",
         icon="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6zM9 12l2 2 4-4", related=["/insurance-discounts-for-class-4-roofing/", "/roof-types-for-insurance/", "/can-stone-coated-roofing-lower-insurance-premiums/"]),
    dict(path="/tools/hail-damage-roof-checklist/", short="Hail damage checklist", name="Hail Damage Roof Checklist",
         title="Hail Damage Roof Checklist: Do You Need a New Roof?", keyword="do i need a new roof after hail",
         description="Is your roof hail storm ready? Check the signs of hail damage and get a score that tells you whether to monitor, inspect or plan a roof replacement after hail.",
         teaser="Tick the signs you see and get a replace-or-monitor verdict in seconds.",
         icon="M7 16a4 4 0 1 1 1-7.9A5 5 0 0 1 18 9a3.5 3.5 0 0 1 0 7M8 19v.01M12 20v.01M16 19v.01", related=["/roof-replacement-after-hail-storm/", "/storm-damage-roof-replacement/", "/stone-coated-roofs-vs-asphalt-during-hail/"]),
    dict(path="/tools/roof-maintenance-checklist-log/", short="Maintenance checklist & log", name="Roof Maintenance Checklist & Log",
         title="Roof Maintenance Checklist, Schedule & Log (Free)", keyword="roof maintenance checklist",
         description="A free roof maintenance checklist, seasonal schedule and printable log. Track inspections, cleanings and storm checks for stone coated, coated and shingle roofs.",
         teaser="Seasonal checklist plus a log you can save, print or export to CSV.",
         icon="M9 5h10M9 12h10M9 19h10M4 5l1 1 2-2M4 12l1 1 2-2M4 19l1 1 2-2", related=["/stone-coated-roof-maintenance-checklist/", "/stone-coated-roof-maintenance/", "/long-lifespan-commercial-roofing/"]),
    dict(path="/tools/roof-weight-calculator/", short="Roof weight calculator", name="Roof Weight Calculator",
         title="Roof Weight Calculator: Steel vs Tile, Slate & Shingle", keyword="roof weight calculator",
         description="Calculate the total weight of your roof in stone coated steel, asphalt, wood shake, concrete tile, clay tile and slate — and see why lighter roofs skip upgrades.",
         teaser="Compare total roof weight across seven materials for your roof size.",
         icon="M6 7h12l2 13H4zM9 7a3 3 0 0 1 6 0", related=["/stone-coated-vs-concrete-tile/", "/stone-coated-vs-clay-tile/", "/slate-roof/"]),
]
BY_PATH = {t["path"]: t for t in TOOLS}


def rng(id_, name, label, lo, hi, step, value, fmt=""):
    return (f'<div class="range"><div class="top"><label for="{id_}">{label}</label><output for="{id_}"></output></div>'
            f'<input type="range" id="{id_}" name="{name}" min="{lo}" max="{hi}" step="{step}" value="{value}" data-fmt="{fmt}"></div>')


def seg(name, label, opts, checked=0, pfx=""):
    items = "".join(f'<input type="radio" id="{pfx}{name}-{i}" name="{name}" value="{v}"{" checked" if i == checked else ""}><label for="{pfx}{name}-{i}">{t}</label>'
                    for i, (t, v) in enumerate(opts))
    return f'<fieldset style="border:0;padding:0;margin:0"><legend style="font-weight:600;font-size:.88rem;margin-bottom:8px">{label}</legend><div class="seg">{items}</div></fieldset>'


def cost_tool(pfx="c", compact=False):
    extra = "" if compact else (seg("tear", "Existing roof to remove", [("None (new build)", -0.6), ("1 layer", 0), ("2 layers", 0.8)], 1, pfx)
                                + seg("method", "Install method", [("Direct-to-deck", 0.95), ("Batten", 1.0), ("Foam-set (coastal)", 1.1)], 1, pfx))
    if compact:
        extra = f'<input type="hidden" name="tear" value="0"><input type="hidden" name="method" value="1">'
    return f"""<div class="tool" data-tool="cost"><div class="tool-grid"><div class="tool-in">
{rng(pfx + "-foot", "foot", "Home footprint (incl. garage &amp; porches)", 800, 6000, 50, 2200, "sf")}
{seg("pitch", "Roof pitch", [("Low (≤4/12)", 1.06), ("Medium (5–8/12)", 1.15), ("Steep (9/12+)", 1.32)], 1, pfx)}
{seg("complex", "Roof shape", [("Simple gable/hip", -0.06), ("Average", 0), ("Complex (many valleys)", 0.12)], 1, pfx)}
{seg("profile", "Profile", [("Shingle", 1.0), ("Shake", 1.04), ("Tile", 1.08), ("Slate", 1.1)], 0, pfx)}
{extra}</div>
<div class="tool-out" aria-live="polite"><span class="eyebrow">Estimated installed cost</span><div class="big" data-o="range">—</div>
<div class="out-row"><span>Roof size</span><b data-o="squares"></b></div>
<div class="out-row"><span>Average per square</span><b data-o="persq"></b></div>
<div class="out-row"><span>Asphalt shingle, same roof</span><b data-o="asphalt"></b></div>
<div class="out-row"><span>Cost spread over a 55-year life</span><b data-o="life"></b></div>
<div class="bars"></div>
<p class="tool-note">Planning range based on $10–$18 per sq ft installed (one-layer tear-off included) for stone coated steel and $4.50–$7.50 for asphalt in Texas. Not a quote — decking repairs, permits and access change the price. <a href="/free-quote/" style="color:#f2c4a6">Get an exact estimate →</a></p>
</div></div></div>"""


def lifetime_tool():
    return f"""<div class="tool" data-tool="lifetime"><div class="tool-grid"><div class="tool-in">
{rng("l-area", "area", "Roof area", 1200, 6000, 100, 2600, "sf")}
{rng("l-years", "years", "How long you'll own it", 10, 70, 1, 40, "yr")}
{rng("l-sc", "sc", "Stone coated cost per sq ft", 10, 18, 0.5, 14, "$sf")}
{rng("l-as", "as", "Asphalt cost per sq ft", 4, 8, 0.25, 6, "$sf")}
{rng("l-alife", "alife", "Asphalt lifespan in Texas", 10, 25, 1, 15, "yr")}
{rng("l-prem", "prem", "Annual home insurance premium", 1000, 9000, 100, 3800, "$")}
{rng("l-disc", "disc", "Class 4 roof discount", 0, 25, 1, 10, "%")}
</div><div class="tool-out" aria-live="polite"><span class="eyebrow">Total cost over your ownership</span>
<div class="out-row"><span>Stone coated steel, installed once</span><b data-o="stone"></b></div>
<div class="out-row"><span>Class 4 insurance savings over the period</span><b data-o="sav"></b></div>
<div class="out-row"><span>Asphalt shingle (with replacements)</span><b data-o="asph"></b></div>
<div class="out-row"><span>Net difference</span><b data-o="diff"></b></div>
<div class="out-row"><span>Break-even</span><b data-o="even"></b></div>
<div class="out-row"><span>Asphalt roofs you'd pay for</span><b data-o="reroofs"></b></div>
<svg class="chart" viewBox="0 -10 600 270" style="width:100%;margin-top:18px" role="img" aria-label="Cumulative cost chart"></svg>
<p class="tool-note"><span style="color:#d98a63">━</span> Stone coated &nbsp; <span style="color:#8a8077">┅</span> Asphalt. Chart shows roof spending; break-even also counts insurance savings. Assumes 3%/yr cost inflation, tear-off on each asphalt replacement and a storm repair every 7 years. Planning estimate only.</p>
</div></div></div>"""


def insurance_tool():
    return f"""<div class="tool" data-tool="insurance"><div class="tool-grid"><div class="tool-in">
{rng("i-prem", "prem", "Your annual premium", 1000, 10000, 100, 3800, "$")}
{rng("i-disc", "disc", "Discount your carrier offers for Class 4", 5, 25, 1, 12, "%")}
{rng("i-years", "years", "Years you plan to stay", 1, 30, 1, 15, "yr")}
{rng("i-home", "home", "Dwelling coverage (Coverage A)", 150000, 1500000, 10000, 450000, "$")}
{rng("i-ded", "ded", "Wind/hail deductible", 1, 5, 0.5, 2, "%")}
</div><div class="tool-out" aria-live="polite"><span class="eyebrow">Estimated savings</span><div class="big" data-o="year">—</div><p style="margin:0;color:#b8ada1">per year</p>
<div class="out-row"><span>Per month</span><b data-o="month"></b></div>
<div class="out-row"><span>Over your stay (premiums trend +4%/yr)</span><b data-o="total"></b></div>
<div class="out-row"><span>Out-of-pocket per wind/hail claim</span><b data-o="ded"></b></div>
<div class="bars"></div>
<p class="tool-note">Texas carriers commonly discount impact-resistant (UL 2218 Class 4) roofs by roughly 5%–25%; your carrier sets the actual figure. A roof that avoids a claim also avoids paying that deductible again.</p>
</div></div></div>"""


HAIL_SIGNS = [
    ("A storm with 1-inch (quarter-size) or larger hail hit your area", 3),
    ("Dents on gutters, downspouts, vents or the AC unit", 3),
    ("Granules collecting in gutters or at downspout exits", 3),
    ("Dark, bruised or shiny spots on shingles", 4),
    ("Cracked, split or missing shingles or tiles", 4),
    ("Neighbors are getting roof inspections or replacements", 2),
    ("Water stains on ceilings or in the attic", 4),
    ("Roof is 12+ years old (asphalt)", 3),
    ("Previous hail claim on this roof", 2),
    ("Your carrier has asked for a roof inspection or sent a non-renewal notice", 3),
]


def hail_tool():
    items = "".join(f'<li><input type="checkbox" id="h{i}" data-w="{w}"><label for="h{i}">{t}</label></li>' for i, (t, w) in enumerate(HAIL_SIGNS))
    return f"""<div class="tool" data-tool="hail"><div class="tool-grid"><div class="tool-in"><h3>What do you see?</h3><ul class="check">{items}</ul>
<p><button type="button" class="btn btn-sm btn-ghost" data-reset>Reset</button></p></div>
<div class="tool-out" aria-live="polite"><span class="eyebrow">Hail damage score</span>
<div class="score-ring"><svg width="170" height="170" viewBox="0 0 170 170"><circle class="bg" cx="85" cy="85" r="70"/><circle class="fg" cx="85" cy="85" r="70"/></svg><b data-o="score">0</b></div>
<h3 data-o="verdict"></h3><p data-o="advice" style="color:#d6ccbf"></p>
<p><a class="btn" href="/free-quote/">Book a free hail inspection <span class="arr">→</span></a></p>
<p class="tool-note">A screening aid, not an inspection. Hail bruising is often invisible from the ground — only a roof-level inspection can confirm damage. Most policies set a deadline for reporting storm damage, so check yours.</p>
</div></div></div>"""


SEASONS = [
    ("Spring (after hail season starts)", ["Walk the perimeter and look for displaced or dented panels", "Clear gutters, valleys and downspouts", "Check ridge and hip caps for lift", "Inspect flashing at chimneys, skylights and walls", "Look for granule wash in gutters"]),
    ("Summer (heat &amp; storms)", ["Check attic ventilation and look for daylight or stains", "Trim branches 6+ ft back from the roof", "Inspect sealant at pipe boots and vents", "Photograph the roof for your records"]),
    ("Fall (before winter)", ["Clear leaves from valleys and gutters", "Check gutter hangers and fascia", "Inspect skylight and chimney flashing", "Confirm vents and turbines are secure"]),
    ("Winter", ["Look for ice dams after hard freezes (North Texas)", "Check attic for condensation", "Review insurance policy and roof documentation"]),
    ("After any major storm", ["Photograph gutters, vents and AC unit for dents", "Look for missing or lifted panels from the ground", "Check ceilings and attic for new stains", "Schedule a professional inspection if hail was 1 inch or larger", "Report damage to your carrier within the policy deadline"]),
]


def maint_tool():
    blocks = ""
    for si, (season, items) in enumerate(SEASONS):
        lis = "".join(f'<li><input type="checkbox" id="m{si}-{i}"><label for="m{si}-{i}">{t}</label></li>' for i, t in enumerate(items))
        blocks += f'<div data-season class="rv" style="margin-bottom:28px"><div style="display:flex;justify-content:space-between;align-items:baseline;gap:12px"><h3>{season}</h3><small class="muted" data-prog></small></div><ul class="check">{lis}</ul></div>'
    return f"""<div class="tool" data-tool="maint"><div class="tool-grid"><div class="tool-in"><h3 style="font-size:1.6rem">Seasonal checklist</h3><p class="muted">Ticks save in this browser so you can come back next season.</p>{blocks}</div>
<div class="tool-out"><h3>Maintenance log</h3><p style="color:#b8ada1">Keep a dated record — insurers and manufacturers ask for one when you file a claim or warranty request.</p>
<form class="log-form" style="color:var(--ink)"><div class="fields"><div class="field"><label for="lg-d" style="color:#fff">Date</label><input id="lg-d" type="date" name="date" required></div>
<div class="field"><label for="lg-t" style="color:#fff">Type</label><select id="lg-t" name="type"><option>Inspection</option><option>Gutter cleaning</option><option>Repair</option><option>Storm check</option><option>Professional inspection</option><option>Insurance claim</option></select></div></div>
<div class="field"><label for="lg-n" style="color:#fff">Notes</label><textarea id="lg-n" name="notes" rows="2" placeholder="What you checked or fixed"></textarea></div>
<button class="btn btn-sm" type="submit">Add to log</button></form>
<div class="table-wrap" style="margin-top:18px"><table class="log-table"><thead><tr><th>Date</th><th>Type</th><th>Notes</th><th></th></tr></thead><tbody></tbody></table></div>
<p class="no-print" style="display:flex;gap:10px;flex-wrap:wrap"><button type="button" class="btn btn-sm btn-ghost" style="color:#fff" data-print>Print checklist &amp; log</button><button type="button" class="btn btn-sm btn-ghost" style="color:#fff" data-csv>Export CSV</button></p>
<p class="tool-note">Saved only in your browser. Clearing site data erases it — export a CSV to keep a copy.</p></div></div></div>"""


def weight_tool():
    return f"""<div class="tool" data-tool="weight"><div class="tool-grid"><div class="tool-in">
{rng("w-area", "area", "Roof area", 1000, 8000, 100, 2800, "sf")}
<div class="out-row" style="border-color:var(--line)"><span>Stone coated steel total</span><b style="color:var(--ink)" data-o="stone"></b></div>
<div class="out-row" style="border-color:var(--line)"><span>In tons</span><b style="color:var(--ink)" data-o="tons"></b></div>
<div class="out-row" style="border-color:var(--line)"><span>Compared with concrete tile</span><b style="color:var(--ink)" data-o="vs"></b></div>
<p class="muted" style="margin-top:18px;font-size:.92rem">Most homes framed for asphalt shingles can take stone coated steel without structural reinforcement. Concrete and clay tile usually need an engineer's sign-off when replacing a lighter roof.</p></div>
<div class="tool-out"><span class="eyebrow">Total roof weight by material</span><div class="bars"></div>
<p class="tool-note">Typical installed weights per sq ft: stone coated steel 1.6–2.4 lb, standing seam 0.9–1.5, architectural asphalt 2.3–4.3, wood shake 3–4.5, concrete tile 9–10, clay tile 8–12, slate 8–15. Excludes decking and underlayment.</p></div></div></div>"""


BODIES = {
    "/tools/stone-coated-roof-cost-calculator/": (cost_tool, """<h2>How the stone coated steel roofing cost estimate works</h2>
<p>Roofers price by the <strong>square</strong> — 100 sq ft of roof surface. The calculator converts your home's footprint into roof area using a pitch factor (a steeper roof has more surface than the floor beneath it) plus about 10% for overhangs, then applies Texas installed pricing of roughly $10–$18 per sq ft for stone coated steel.</p>
<h3>What moves the price</h3><ul><li><strong>Profile:</strong> shingle is the most economical; tile and slate profiles take more trim and labor.</li><li><strong>Complexity:</strong> valleys, dormers, turrets and skylights add flashing work.</li><li><strong>Tear-off:</strong> removing one or two layers of old roofing and hauling it away.</li><li><strong>Install method:</strong> foam-set systems for high-wind coastal homes cost more than batten or direct-to-deck.</li><li><strong>Brand:</strong> value tiers like Allmet sit at the low end; Tilcor and TEK at the high end.</li></ul>
<p>For a full breakdown by roof size and region, read our <a href="/stone-coated-roofing-cost-texas/">stone coated roofing cost guide for Texas</a>, then compare the long-run numbers in the <a href="/tools/lifetime-roof-cost-calculator/">lifetime cost calculator</a>.</p>"""),
    "/tools/lifetime-roof-cost-calculator/": (lifetime_tool, """<h2>Why upfront price is the wrong comparison</h2>
<p>An asphalt roof in Texas heat and hail typically lasts 12–18 years. A stone coated steel roof carries a 50-year-to-lifetime warranty. Over 40 years, an owner with asphalt usually pays for two or three full replacements — each with tear-off, dumpsters, permits and inflation — plus storm repairs and deductibles in between.</p>
<p>The calculator adds those costs year by year and subtracts any Class 4 insurance discount from the stone coated total, so you can see when the two lines cross. Adjust the sliders to your own quotes and policy.</p>
<p>Want the details behind the assumptions? See <a href="/stone-coated-steel-roof-lifespan/">how long stone coated steel lasts</a> and <a href="/are-stone-coated-roofs-worth-it/">whether stone coated roofs are worth it</a>.</p>"""),
    "/tools/insurance-discount-estimator/": (insurance_tool, """<h2>How Class 4 roof discounts work in Texas</h2>
<p>Many Texas insurers file premium credits for roofs rated <strong>UL 2218 Class 4</strong> — the highest impact-resistance rating. Stone coated steel, Class 4 shingles and some metal roofs qualify. Discounts commonly fall between 5% and 25%, but each carrier sets its own figure, and some apply it only to the wind/hail portion of the premium.</p>
<h3>What your carrier will ask for</h3><ul><li>Proof of the product's Class 4 rating (manufacturer documentation)</li><li>An invoice or certificate showing installation date and product</li><li>Sometimes photos or an inspection</li></ul>
<p>{BRAND} provides the product documentation with every install. Learn more about <a href="/insurance-discounts-for-class-4-roofing/">Class 4 insurance discounts</a> and which <a href="/roof-types-for-insurance/">roof types insurers prefer</a>.</p>"""),
    "/tools/hail-damage-roof-checklist/": (hail_tool, """<h2>Do I need a new roof after hail?</h2>
<p>Not every hailstorm means a replacement. Hail under about an inch rarely damages a sound roof. Larger stones can bruise asphalt shingles — crushing the mat beneath the granules — which won't leak today but shortens the roof's life. Insurers generally pay for functional damage, so documentation matters.</p>
<h3>Next steps if your score is high</h3><ol><li>Photograph dents on soft metals (gutters, vents, AC fins) — they show hail size.</li><li>Book a roof-level inspection before calling your carrier.</li><li>File within your policy's reporting deadline.</li><li>Ask about upgrading to a Class 4 roof so the next storm doesn't repeat the cycle.</li></ol>
<p>Read the full guides: <a href="/roof-replacement-after-hail-storm/">hail damage roof replacement</a> and <a href="/storm-damage-roof-replacement/">storm damage roof replacement</a>.</p>"""),
    "/tools/roof-maintenance-checklist-log/": (maint_tool, """<h2>A roof maintenance schedule that actually gets done</h2>
<p>Whether your roof is stone coated steel, a coated low-slope system or asphalt shingle, most problems start small — a clogged valley, a cracked pipe boot, a lifted ridge cap. Two seasonal walk-arounds and a check after every major storm catch nearly all of them.</p>
<p>The log matters as much as the checklist. Manufacturers and insurers both ask for maintenance records when you file a warranty or storm claim, and a dated log with photos makes those conversations short.</p>
<p>For stone coated specifics, see our <a href="/stone-coated-roof-maintenance-checklist/">stone coated roof maintenance checklist</a> and <a href="/stone-coated-roof-maintenance/">maintenance guide</a>. Never walk a roof you aren't trained to — {BRAND} offers free inspections.</p>"""),
    "/tools/roof-weight-calculator/": (weight_tool, """<h2>Why roof weight matters</h2>
<p>Swapping a lightweight roof for a heavy one can require rafter and deck reinforcement — and an engineer's letter. Concrete and clay tile weigh four to five times as much as stone coated steel. That's why stone coated tile and slate profiles are popular in Texas: the look of a heavy roof on framing built for shingles.</p>
<p>Compare materials in depth: <a href="/stone-coated-vs-concrete-tile/">stone coated vs concrete tile</a>, <a href="/stone-coated-vs-clay-tile/">stone coated vs clay tile</a> and <a href="/slate-roof/">slate roofs</a>.</p>"""),
}

FAQS = {
    "/tools/stone-coated-roof-cost-calculator/": [
        {"q": "How much does a stone coated steel roof cost in Texas?", "a": "Most Texas homes land between $10 and $18 per sq ft installed — roughly $25,000 to $45,000 for a typical 2,500 sq ft roof — depending on profile, pitch, complexity and tear-off."},
        {"q": "Is the calculator a quote?", "a": "No. It's a planning range. A free inspection measures every roof plane and checks decking, which is what a firm quote requires."}],
    "/tools/insurance-discount-estimator/": [
        {"q": "Does a metal roof lower your insurance in Texas?", "a": "A metal roof with a UL 2218 Class 4 rating — including stone coated steel — often qualifies for an impact-resistance discount. The amount depends on your carrier."},
        {"q": "What is a Class 4 roof certificate?", "a": "It's the documentation showing your installed roof carries a Class 4 impact rating — usually the manufacturer's product approval plus the contractor's invoice or certificate of installation."}],
    "/tools/hail-damage-roof-checklist/": [
        {"q": "How much hail damage is needed to replace a roof?", "a": "Insurers look for functional damage — fractured or bruised shingles, broken seals — across enough of a roof slope that repair isn't practical. Adjusters often count hits within a 10×10 ft test square on each slope."},
        {"q": "Is my roof hail storm ready?", "a": "A roof is hail-ready when it carries a Class 4 impact rating, is in sound condition, and you have dated photos of it before storm season. Stone coated steel is the most hail-resistant option most Texas homes can install."}],
    "/tools/roof-maintenance-checklist-log/": [
        {"q": "How often should a roof be inspected?", "a": "Twice a year — spring and fall — and after any storm with hail an inch or larger or winds over about 60 mph."},
        {"q": "What should a roof coating maintenance log include?", "a": "The date, what was inspected or cleaned, any repairs, who did the work, and photos. Keep it with your warranty documents."}],
}


def build(g):
    page, phero, faq_html, cta_band, crumbs_ld, faq_ld = g["page"], g["phero"], g["faq_html"], g["cta_band"], g["crumbs_ld"], g["faq_ld"]
    BRAND, POSTS, post_card, ORIGIN = g["BRAND"], g["POSTS"], g["post_card"], g["ORIGIN"]
    by_path = {p["path"]: p for p in POSTS}
    cards = "".join(
        f'<a class="card tilt rv" style="--d:{i * .06:.2f}s" href="{t["path"]}"><span class="ico"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="{t["icon"]}"/></svg></span><h3>{t["name"]}</h3><p>{t["teaser"]}</p><span class="more">Open tool</span></a>'
        for i, t in enumerate(TOOLS))
    g["TOOL_CARDS"] = cards
    trail = [("Home", "/"), ("Tools", "/tools/")]
    body = (phero(trail, "Free Roofing <span class='it'>Tools</span>", f"Calculators and checklists from {BRAND} — price a stone coated steel roof, see lifetime cost, estimate insurance savings, check hail damage and keep a maintenance log.", "Tools")
            + f'<section class="section"><div class="wrap"><div class="grid g3 tool-cards">{cards}</div></div></section>' + cta_band())
    graph = [crumbs_ld(trail), {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{ORIGIN}{t['path']}", "name": t["name"]} for i, t in enumerate(TOOLS)]}]
    page("/tools/", f"Free Roofing Calculators & Checklists | {BRAND}",
         "Free roofing tools: stone coated roof cost calculator, lifetime cost comparison, Class 4 insurance discount estimator, hail damage checklist and maintenance log.",
         body, graph=graph, scripts=("site", "tools"))
    for t in TOOLS:
        fn, copy = BODIES[t["path"]]
        copy = copy.replace("{BRAND}", BRAND)
        trail = [("Home", "/"), ("Tools", "/tools/"), (t["short"].capitalize(), t["path"])]
        rel = [by_path[u] for u in t["related"] if u in by_path]
        others = "".join(f'<li><a href="{o["path"]}">{o["name"]}</a></li>' for o in TOOLS if o is not t)
        faq = FAQS.get(t["path"], [])
        body = (phero(trail, t["name"], t["description"], "Free tool")
                + f'<section class="section tight"><div class="wrap">{fn()}</div></section>'
                + f'<section class="section tight"><div class="wrap two" style="align-items:start"><article class="prose">{copy}</article><div><div class="side-list"><h4>More free tools</h4><ul class="pill-list" style="margin:0">{others}</ul></div></div></div></section>'
                + faq_html(faq)
                + (f'<section class="section tight sand"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">Related guides</span><h2>Go <span class="it">deeper.</span></h2></div></div><div class="grid g3">{"".join(post_card(p) for p in rel)}</div></div></section>' if rel else "")
                + cta_band())
        graph = [crumbs_ld(trail), {"@type": "WebApplication", "name": t["name"], "url": f"{ORIGIN}{t['path']}", "applicationCategory": "UtilitiesApplication",
                                    "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": f"{ORIGIN}/#business"}}]
        if faq:
            graph.append(faq_ld(faq))
        page(t["path"], g["full_title"](t["title"]), t["description"], body, graph=graph, scripts=("site", "tools"))
