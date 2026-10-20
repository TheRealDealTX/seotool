"""Gutter & Downspout Calculator — sizes K-style gutters for design rainfall,
counts downspouts and prices seamless aluminum, steel or copper.
Script: static/assets/js/tools/gutter-calculator.js
"""

from content.ui import num, select, seg, group, prices, switch, rows, text
from siteconfig import TEXAS_REGIONS, US_REGIONS

SLUG = "gutter-calculator"

REGION_OPTS = ([(r["key"], f"Texas — {r['name']}") for r in TEXAS_REGIONS]
               + [(r["key"], r["name"]) for r in US_REGIONS])

# Approximate design rainfall intensities (in/hr) used as presets.
RAIN = [
    ("houston", "Houston & Gulf Coast", 7.0),
    ("dfw", "Dallas–Fort Worth", 6.5),
    ("central", "Austin & Central Texas", 6.5),
    ("sa", "San Antonio & Hill Country", 6.5),
    ("south", "Rio Grande Valley & South Texas", 6.5),
    ("east", "East Texas", 6.5),
    ("west", "West Texas & Panhandle", 5.0),
    ("other", "Other U.S. location (check local data)", 6.0),
]

# Installed prices per material: gutter $/lf (5", 6"), downspout $/lf (2×3, 3×4), elbows $/ea.
GUTTER_PRICES = {
    "aluminum": {"g5": (8, 14), "g6": (10, 18), "d23": (7, 11), "d34": (9, 14), "el": (8, 15)},
    "steel": {"g5": (10, 16), "g6": (12, 20), "d23": (9, 14), "d34": (11, 17), "el": (10, 18)},
    "copper": {"g5": (25, 35), "g6": (30, 40), "d23": (20, 30), "d34": (25, 38), "el": (25, 45)},
}
MAT_NAMES = [("aluminum", "Seamless aluminum (.027–.032 in)"), ("steel", "Galvalume / galvanized steel"),
             ("copper", "Copper (16 oz)")]

PITCH_OPTS = [(3, "Flat to 3/12"), (5, "4/12 – 5/12"), (8, "6/12 – 8/12"), (11, "9/12 – 11/12"), (12, "12/12 and steeper")]

run_fields = (text("name", "Run", "", placeholder="e.g. Front", row=True, autoname="Run")
              + num("lf", "Length", 40, unit="ft", min=0, step=1, row=True)
              + num("area", "Area drained", 600, unit="sf", min=0, step=10, row=True))

a = GUTTER_PRICES["aluminum"]
form = (
    group("Eaves & roof",
          seg("mode", "How do you want to enter the gutters?",
              [("runs", "Run by run"), ("total", "Totals only")], "runs"),
          num("total_lf", "Total gutter length", 160, unit="ln ft", min=0, step=1, show="mode=total"),
          num("n_runs", "Number of separate runs", 4, min=1, step=1, show="mode=total",
              help="Each stretch of eave that ends at a corner or roof edge."),
          num("total_area", "Total roof area (plan view)", 2100, unit="sq ft", min=0, step=10,
              tip="Horizontal area of the roof, like the footprint plus overhangs, not the sloped surface. Pitch is added below.",
              help="In run-by-run mode this is only used for runs whose area is left at 0."),
          select("pitch", "Roof pitch", PITCH_OPTS, 8, numeric=True,
                 tip="Steeper roofs catch more wind-driven rain, so the drainage area is increased by a pitch factor."),
          select("stories", "Stories (gutter height)", [(1, "1 story"), (2, "2 stories"), (3, "3 stories")], 1, numeric=True),
          ),
    '<div data-show="mode=runs">'
    + rows("runs", run_fields, start=4, min=1, add_label="Add a gutter run",
           legend="Gutter runs (length and the roof area that drains into each)")
    + "</div>",
    group("Rainfall & sizing",
          select("rain", "Design rainfall preset (approximate)", [(k, f"{n} — about {i:g} in/hr") for k, n, i in RAIN],
                 "dfw", cls="full"),
          num("intensity", "Design rainfall intensity", 6.5, unit="in/hr", min=0.5, max=15, step=0.1,
              help="Presets are approximate short-duration downpour rates. Override with local data if you have it."),
          seg("size", "Gutter size", [("auto", "Recommend"), ("5", '5" K-style'), ("6", '6" K-style')], "auto"),
          seg("ds", "Downspouts", [("auto", "Match gutter"), ("23", "2×3 in"), ("34", "3×4 in")], "auto"),
          num("spacing", "Max gutter length per downspout", 40, unit="ln ft", min=10, step=1),
          num("story_h", "Height per story", 10, unit="ft", min=6, step=0.5),
          ),
    group("Material & extras",
          select("material", "Gutter material", MAT_NAMES, "aluminum", cls="full"),
          select("region", "Project location", REGION_OPTS, "dfw", cls="full"),
          switch("guards", "Add gutter guards", checked=False),
          switch("removal", "Remove & haul off old gutters", checked=True),
          ),
    prices("Edit unit prices & sizing rules",
           num("g5_lo", '5" gutter — low', a["g5"][0], pre="$", unit="/lf", min=0),
           num("g5_hi", '5" gutter — high', a["g5"][1], pre="$", unit="/lf", min=0),
           num("g6_lo", '6" gutter — low', a["g6"][0], pre="$", unit="/lf", min=0),
           num("g6_hi", '6" gutter — high', a["g6"][1], pre="$", unit="/lf", min=0),
           num("d23_lo", "2×3 downspout — low", a["d23"][0], pre="$", unit="/lf", min=0),
           num("d23_hi", "2×3 downspout — high", a["d23"][1], pre="$", unit="/lf", min=0),
           num("d34_lo", "3×4 downspout — low", a["d34"][0], pre="$", unit="/lf", min=0),
           num("d34_hi", "3×4 downspout — high", a["d34"][1], pre="$", unit="/lf", min=0),
           num("el_lo", "Elbow — low", a["el"][0], pre="$", min=0),
           num("el_hi", "Elbow — high", a["el"][1], pre="$", min=0),
           num("gd_lo", "Gutter guards — low", 6, pre="$", unit="/lf", min=0),
           num("gd_hi", "Gutter guards — high", 12, pre="$", unit="/lf", min=0),
           num("rm_lo", "Old gutter removal — low", 1, pre="$", unit="/lf", min=0),
           num("rm_hi", "Old gutter removal — high", 2, pre="$", unit="/lf", min=0),
           num("elbows", "Elbows per downspout", 3, min=0, step=1),
           num("cap23", "Roof area per 2×3 downspout", 600, unit="sq ft", min=50, step=10),
           num("cap34", "Roof area per 3×4 downspout", 1200, unit="sq ft", min=50, step=10),
           num("k5", '5" gutter capacity at 1 in/hr', 5520, unit="sq ft", min=100, step=10),
           num("k6", '6" gutter capacity at 1 in/hr', 7960, unit="sq ft", min=100, step=10),
           note="Gutter, downspout and elbow prices refill when you change the material. Gutter prices include hangers, "
                "end caps, miters and outlets. All prices are scaled by the region factor."),
)


def _price_table():
    r = []
    for key, name in MAT_NAMES:
        p = GUTTER_PRICES[key]
        r.append(f"<tr><td>{name}</td><td>${p['g5'][0]}–${p['g5'][1]}</td><td>${p['g6'][0]}–${p['g6'][1]}</td>"
                 f"<td>${p['d23'][0]}–${p['d23'][1]} / ${p['d34'][0]}–${p['d34'][1]}</td></tr>")
    return ('<div class="table-wrap"><table><thead><tr><th>Material</th><th>5" gutter per ln ft</th><th>6" gutter per ln ft</th>'
            "<th>Downspout per ln ft (2×3 / 3×4)</th></tr></thead><tbody>" + "".join(r) + "</tbody></table></div>")


def _capacity_table():
    r = []
    for k, n, i in RAIN[:-1]:
        r.append(f"<tr><td>{n.replace('&', '&amp;')}</td><td>{i:g} in/hr</td><td>{round(5520 / i):,} sq ft</td><td>{round(7960 / i):,} sq ft</td></tr>")
    return ('<div class="table-wrap"><table><thead><tr><th>Texas region (approximate design rate)</th><th>Rainfall</th>'
            '<th>Max adjusted area, 5" gutter</th><th>Max adjusted area, 6" gutter</th></tr></thead><tbody>'
            + "".join(r) + "</tbody></table></div>")


body = f"""
<h2 id="how-it-works">How gutter sizing works</h2>
<p>A gutter has to carry the water from the roof area that drains into it during a hard, short downpour, not an average
rain. Sizing comes down to three numbers: how much roof drains into each run, how steep the roof is, and how hard it
rains where you live. The calculator follows the method used in common sheet-metal sizing tables:</p>
<ol>
  <li><strong>Drainage area per run.</strong> Enter the plan-view (horizontal) roof area that sheds water into each
  gutter run. On a simple gable, each side drains half the roof; on a hip roof the long sides take most of it.</li>
  <li><strong>Pitch factor.</strong> Wind drives rain onto steep roofs, so the area is increased: 1.0 up to 3/12, 1.05 at
  4–5/12, 1.1 at 6–8/12, 1.2 at 9–11/12 and 1.3 at 12/12 and steeper.</li>
  <li><strong>Rainfall intensity.</strong> The adjusted area is compared to the gutter's capacity at your design
  rainfall rate. A 5" K-style gutter handles about 5,520 sq ft at 1 in/hr and a 6" about 7,960 sq ft; divide by the
  local rate in inches per hour.</li>
</ol>
<div class="formula">Adjusted area   = drainage area × pitch factor
5" capacity     = 5,520 ÷ rainfall (in/hr)     6" capacity = 7,960 ÷ rainfall (in/hr)
Downspouts/run  = max(1, run length ÷ 40 ft, adjusted area ÷ area per downspout)
Downspout length = stories × 10 ft + 2 ft each</div>
<p>Each run is checked as if it drains to a single outlet, which is conservative. If a run is too big even for a 6"
gutter, the calculator adds downspouts so each section carries less water.</p>

<h2 id="texas-rain">Texas rainfall and gutter size</h2>
<p>Texas storms are short and intense. Gulf moisture can produce rainfall rates well above what a gutter sized for a
national average can carry, and an overflowing gutter dumps water at the foundation, which matters on expansive Texas
clay soils. These presets are approximate design rates; use local data from your city or a civil engineer for
commercial work.</p>
{_capacity_table()}
<p>In practice, many Houston-area homes need 6" gutters on the long eaves, while a typical DFW or Central Texas home is
borderline: 5" works on short runs, 6" on long runs below big roof planes. Valleys that dump into a gutter concentrate
water at one point; put a downspout near the valley or add a diverter.</p>

<h3 id="downspouts">Downspouts</h3>
<p>Downspouts are usually the bottleneck. A 2×3 in downspout serves roughly 600 sq ft of roof at typical Texas rates and
a 3×4 in about 1,200 sq ft. Plan at least one downspout per run and one for every 35–40 ft of gutter. Pair 3×4
downspouts with 6" gutters; they also clog less with leaves and oak catkins.</p>

<h2 id="cost">Gutter installation cost in Texas (2026)</h2>
<p>Installed prices for seamless gutters in the DFW baseline, including hangers, end caps, miters and outlets:</p>
{_price_table()}
<p>Elbows run about $8–$15 each in aluminum, gutter guards $6–$12 per linear foot and removal of old gutters $1–$2 per
linear foot. A typical one-story Texas home with 150–180 ft of seamless aluminum gutter usually costs $1,800–$3,500
installed. Copper is mostly used on historic and high-end homes; expect about three times the cost of aluminum.</p>
<ul>
  <li><strong>Aluminum</strong> is the standard. Ask for .027 in or heavier; .032 in resists ladder dents and hail better.</li>
  <li><strong>Steel</strong> is stronger but rusts at cut edges, especially near the coast.</li>
  <li><strong>Copper</strong> lasts the longest and needs no paint.</li>
</ul>

<h2 id="insurance">Gutters on insurance claims</h2>
<p>Hail that damages the roof often dents gutters and downspouts too, and carriers commonly pay to replace dented
gutters on a covered hail claim. Gutter guards, fascia damage and downspouts are easy to leave out of an estimate, so
check that they are listed. Wear, sagging and clogging are maintenance and are not covered. Photograph dents with a
reference (a coin or tape measure) before anything is removed.</p>
<p>If your carrier's estimate leaves gutters off, or prices 6" gutters as 5", our
<a href="/services/insurance-claim-estimate-review/">claim estimate review</a> lists what is missing. For the roof itself,
use the <a href="/tools/roof-replacement-cost-calculator/">roof replacement cost calculator</a> or the
<a href="/tools/roof-insurance-claim-calculator/">insurance claim calculator</a>.</p>

<div class="callout"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
<p><strong>Measure along the eave, not the wall.</strong> Gutter length is the length of the fascia board, which includes
the overhang at each end. Add a few feet per run for miters if you are pricing materials only.</p></div>
"""

faqs = [
    ("Do I need 5-inch or 6-inch gutters in Texas?",
     "<p>It depends on the roof area draining into each run and your local rainfall rate. At about 6.5 in/hr (DFW, "
     "Austin, San Antonio) a 5\" K-style gutter carries roughly 850 sq ft of adjusted roof area and a 6\" about 1,225 sq ft. "
     "Large roof planes, steep pitches and the Gulf Coast often call for 6\".</p>"),
    ("How many downspouts do I need?",
     "<p>At least one per gutter run, one for every 35–40 ft of gutter, and enough that each 2×3 downspout drains no more "
     "than about 600 sq ft of roof (about 1,200 sq ft for a 3×4). Corners where two big roof planes meet usually need one.</p>"),
    ("How much do seamless gutters cost in Texas?",
     "<p>Seamless aluminum gutters usually cost $8–$14 per linear foot for 5\" and $10–$18 for 6\", installed, plus "
     "downspouts. Most Texas homes land between $1,800 and $3,500. Steel costs a little more and copper $25–$40 per foot.</p>"),
    ("What is a pitch factor for gutters?",
     "<p>Rain falls at an angle in a storm, so steep roofs catch more of it. The drainage area is multiplied by 1.05 at "
     "4–5/12, 1.1 at 6–8/12, 1.2 at 9–11/12 and 1.3 at 12/12 and steeper.</p>"),
    ("Does insurance pay for hail-damaged gutters?",
     "<p>Often, yes. Dented gutters and downspouts from a covered hail storm are commonly included in the claim, subject "
     "to your deductible and policy terms. Wear, sagging and clogging are not covered.</p>"),
    ("Are gutter guards worth it in Texas?",
     "<p>Under live oaks, pecans and pines they save repeated cleanings and reduce overflow. They add about $6–$12 per "
     "linear foot. Choose a guard that can handle heavy downpours without water sheeting over the top.</p>"),
]

TOOL = {
    "slug": SLUG,
    "title": "Gutter & Downspout Calculator (Texas Sizing) | Roof Estimate Pro",
    "description": "Free gutter calculator for Texas: size 5\" or 6\" K-style gutters for local downpours, count downspouts and price seamless aluminum, steel or copper.",
    "h1": "Gutter & Downspout Calculator",
    "lede": "Size gutters for Texas downpours run by run, count downspouts and price seamless aluminum, steel or copper with downspouts, elbows, guards and removal at 2026 Texas prices.",
    "form": form,
    "body": body,
    "faqs": faqs,
    "related": ["roof-replacement-cost-calculator", "roof-square-footage-calculator", "roof-insurance-claim-calculator"],
}
