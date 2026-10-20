"""Roof Repair Cost Calculator — builds an itemized repair ticket from common
Texas repair items, each priced low/high with a budget/typical/premium point.
Script: static/assets/js/tools/roof-repair-cost-calculator.js
"""

from content.ui import num, select, seg, group, prices, switch
from siteconfig import TEXAS_REGIONS, US_REGIONS

SLUG = "roof-repair-cost-calculator"

REGION_OPTS = ([(r["key"], f"Texas — {r['name']}") for r in TEXAS_REGIONS]
               + [(r["key"], r["name"]) for r in US_REGIONS])

# key, label, qty unit, default on, default qty, low, high, price unit, qty step
ITEMS = [
    ("shg", "Replace missing / damaged shingles", "patches of 100 sq ft", True, 1, 350, 650, "/sq", 0.5),
    ("ridge", "Ridge cap replacement", "ln ft", False, 10, 9, 16, "/lf", 1),
    ("boot", "Pipe boot (plumbing vent) replacement", "boots", True, 2, 125, 275, "each", 1),
    ("chim", "Chimney flashing (step + counter)", "chimneys", False, 1, 450, 1100, "each", 1),
    ("step", "Step / wall flashing", "ln ft", False, 10, 15, 30, "/lf", 1),
    ("valley", "Valley repair", "ln ft", False, 10, 20, 40, "/lf", 1),
    ("deck", "Decking replacement (4×8 sheet)", "sheets", False, 1, 90, 150, "/sht", 1),
    ("drip", "Drip edge", "ln ft", False, 20, 5, 9, "/lf", 1),
    ("sky", "Skylight re-flash", "skylights", False, 1, 350, 750, "each", 1),
    ("vent", "Box vent / turbine replacement", "vents", False, 1, 125, 325, "each", 1),
]


def _items_form():
    out = []
    for key, label, qunit, on, q, lo, hi, punit, step in ITEMS:
        out.append(switch(f"use_{key}", label, checked=on))
        out.append(num(f"q_{key}", "Quantity", q, unit=qunit, min=0, step=step, show=f"use_{key}=true", cls="full"))
    out.append(switch("use_tarp", "Emergency tarp (dry-in)", checked=False))
    out.append(num("q_tarp", "Area to tarp", 300, unit="sq ft", min=0, step=10, show="use_tarp=true", cls="full",
                   help="Billed as a trip/setup charge plus a per-sq-ft rate."))
    out.append(switch("use_leak", "Leak investigation / inspection fee", checked=False))
    return out


def _price_fields():
    out = []
    for key, label, qunit, on, q, lo, hi, punit, step in ITEMS:
        short = label.split(" (")[0]
        out.append(num(f"lo_{key}", f"{short} — low", lo, pre="$", unit=(None if punit == "each" else punit), min=0))
        out.append(num(f"hi_{key}", f"{short} — high", hi, pre="$", unit=(None if punit == "each" else punit), min=0))
    out += [
        num("lo_tarpb", "Tarp setup — low", 250, pre="$", min=0),
        num("hi_tarpb", "Tarp setup — high", 450, pre="$", min=0),
        num("lo_tarps", "Tarp area — low", 0.75, pre="$", unit="/sf", min=0),
        num("hi_tarps", "Tarp area — high", 1.75, pre="$", unit="/sf", min=0),
        num("lo_leak", "Leak investigation — low", 150, pre="$", min=0),
        num("hi_leak", "Leak investigation — high", 350, pre="$", min=0),
    ]
    return out


form = (
    group("Repair items", *_items_form()),
    group("Pricing & access",
          seg("tier", "Price point", [("budget", "Budget"), ("typical", "Typical"), ("premium", "Premium")], "typical",
              tip="Budget uses the low unit prices, premium the high, typical the midpoint."),
          select("pitch", "Roof pitch", [("walk", "Walkable (up to 6/12)"), ("p8", "7/12 – 8/12"),
                                         ("p10", "9/12 – 10/12"), ("p12", "11/12 and steeper")], "walk"),
          select("stories", "Stories", [(1, "1 story"), (2, "2 stories"), (3, "3+ stories")], 1, numeric=True),
          select("region", "Project location", REGION_OPTS, "dfw", cls="full"),
          num("minimum", "Minimum service charge", 350, pre="$", min=0,
              help="Small repairs are billed at the contractor's minimum. $300–$500 is common in Texas."),
          ),
    group("Repair or replace? (optional)",
          num("roof_sqft", "Total roof area", 2400, unit="sq ft", min=0,
              help="Used to estimate a full replacement for comparison. Enter 0 to skip."),
          num("age", "Roof age", 12, unit="years", min=0, step=1),
          ),
    prices("Edit unit prices", *_price_fields(),
           note="Prices are installed (labor, material and the contractor's margin) for a DFW-baseline asphalt shingle roof. "
                "The pitch, story and region factors are applied on top; the investigation fee is not scaled."),
)


PUNIT_LONG = {"/sq": "per 100 sq ft patch", "/sht": "per 4×8 sheet", "/lf": "per ln ft", "each": "each"}


def _price_table():
    rows = "".join(f"<tr><td>{label}</td><td>${lo:,}–${hi:,} {PUNIT_LONG.get(punit, punit)}</td></tr>"
                   for key, label, qunit, on, q, lo, hi, punit, step in ITEMS)
    rows += "<tr><td>Emergency tarp</td><td>$250–$450 setup + $0.75–$1.75/sq ft</td></tr>"
    rows += "<tr><td>Leak investigation / inspection</td><td>$150–$350, often credited toward the repair</td></tr>"
    return ('<div class="table-wrap"><table><thead><tr><th>Repair item</th><th>Texas 2026 installed price</th></tr></thead>'
            f"<tbody>{rows}</tbody></table></div>")


body = f"""
<h2 id="how-it-works">How the repair cost calculator works</h2>
<p>Roofers price repairs differently from replacements. A replacement is priced per square across the whole roof; a
repair is a ticket of individual items, each with its own setup time, materials and trip cost. That is why a two-hour
pipe boot job can cost more per square foot than a whole new roof. This calculator builds the ticket the same way:</p>
<ol>
  <li><strong>Pick the repair items</strong> and enter quantities: number of 100 sq ft shingle patches, linear feet of
  flashing or ridge, number of boots, sheets of decking and so on.</li>
  <li><strong>Choose a price point.</strong> Each item has a low and a high Texas 2026 installed price. <em>Budget</em>
  uses the low end, <em>premium</em> the high end and <em>typical</em> the midpoint.</li>
  <li><strong>Access factors.</strong> Steep and tall roofs take longer to set up and work safely, so every line is scaled
  by a pitch and story factor and by the regional labor factor.</li>
  <li><strong>Minimum charge.</strong> If the ticket comes in under the contractor's minimum service charge, the job is
  billed at the minimum.</li>
</ol>
<div class="formula">Line item   = quantity × unit price × pitch factor × story factor × region factor
Ticket      = Σ line items + investigation fee
Billed      = max(ticket, minimum service charge)
Repair ratio = billed repair ÷ estimated full replacement</div>
<p>Pitch factors are 1.00 for walkable roofs (up to 6/12), 1.15 at 7–8/12, 1.30 at 9–10/12 and 1.45 at 11/12 and
steeper. Two stories add 10% and three stories 20%.</p>

<h2 id="repair-prices">Roof repair prices in Texas (2026)</h2>
<p>These are installed prices for an asphalt shingle roof in the Dallas–Fort Worth area, including the contractor's
overhead and profit. Tile, metal and wood shake repairs cost more and need a specialist.</p>
{_price_table()}
<p>A typical service call in Texas (a couple of pipe boots and one shingle patch on a one-story house) usually runs
$700–$1,200. Chimney and skylight flashing jobs, valley rebuilds and storm tarps are the most common tickets over
$1,000.</p>

<h3 id="what-is-in-a-patch">What a "patch" includes</h3>
<p>A 100 sq ft patch (one square) covers removing the damaged shingles, sliding new underlayment under the courses
above, installing new shingles woven into the existing roof and sealing the tabs. Decking is extra: if the wood under
the patch is soft or rotted, add sheets on the decking line.</p>

<h2 id="repair-or-replace">Repair or replace?</h2>
<p>Enter the total roof area and roof age and the calculator compares the repair to a full replacement priced from the
architectural shingle range in our <a href="/tools/roof-replacement-cost-calculator/">roof replacement cost
calculator</a>. Two signals suggest you should at least get a replacement price:</p>
<ul>
  <li><strong>The repair costs more than about 25–30% of a new roof.</strong> Past that point you are spending
  replacement money on a roof that is still old everywhere else.</li>
  <li><strong>The roof is 15–20+ years old.</strong> Texas heat shortens shingle life. In the Panhandle and North Texas
  hail belt, a 15-year-old roof has usually taken several hail seasons. Old shingles crack when lifted, so a repair can
  damage the area around it.</li>
</ul>
<p>Leaks from a single pipe boot or a failed flashing detail are almost always worth repairing, even on an older
roof. Widespread granule loss, curling and brittle shingles are a replacement problem.</p>

<h2 id="insurance">When insurance pays for roof repairs</h2>
<p>Most Texas homeowner policies cover <em>sudden and accidental</em> damage, such as hail, wind that lifts or tears
shingles, or a fallen limb. They do not cover wear and tear: cracked pipe boots, dried-out sealant, rusted flashing,
granule loss from age or a roof that was installed badly. Check your policy; many Texas policies now pay roofs at
actual cash value or use a separate wind/hail deductible, which is often 1–2% of the dwelling limit.</p>
<ul>
  <li><strong>Document first.</strong> Photograph the damage, the date and the storm before anything is repaired.</li>
  <li><strong>Mitigate.</strong> Your policy requires you to prevent further damage. A reasonable emergency tarp is
  normally reimbursable, so keep the invoice.</li>
  <li><strong>Compare the repair to the deductible.</strong> If the ticket is under your deductible, a claim pays
  nothing and still goes on your claims history.</li>
</ul>
<p>If the carrier offers a spot repair where you believe the damage is wider, our
<a href="/services/insurance-claim-estimate-review/">claim estimate review</a> compares their estimate to your photos
and lists what is missing. The <a href="/tools/roof-insurance-claim-calculator/">insurance claim calculator</a> shows
how the deductible and depreciation affect the check.</p>

<h2 id="matching">Matching shingles on an older roof</h2>
<p>Shingle lines are discontinued and colors fade, so a repair on a roof more than about 8–10 years old rarely
matches. Even the same product in the same color looks different next to shingles that have weathered in the Texas sun.
Many Texas policies do not require the carrier to replace undamaged slopes just to get a match, and the rules differ by
policy form and endorsement, so read your policy and ask the adjuster how matching is handled. On the front slope of the
house a visible mismatch can be reason enough to price the whole slope or the whole roof.</p>

<div class="callout"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
<p><strong>Get the ticket itemized.</strong> Ask the roofer to list each item with a quantity, just like the ticket
above. A one-line "repair roof — $1,800" gives you nothing to compare, and nothing to send your carrier.</p></div>
"""

faqs = [
    ("How much does a roof repair cost in Texas?",
     "<p>Most Texas roof repairs cost $350–$1,500. Small jobs such as one or two pipe boots usually hit the contractor's "
     "minimum charge of about $300–$500. Chimney flashing, valley repairs, decking replacement and emergency tarps often "
     "push a ticket to $1,000–$2,500, and steep or two-story roofs cost 10–45% more.</p>"),
    ("Why is there a minimum charge for small roof repairs?",
     "<p>Every repair needs a truck, a ladder, a crew of one or two, safety gear and materials, plus travel time. A $90 "
     "boot still takes half a day once you count driving and setup, so most roofers bill a minimum of $300–$500.</p>"),
    ("When should I replace my roof instead of repairing it?",
     "<p>Get a replacement price when the repair passes about 25–30% of a new roof, when the roof is more than 15–20 "
     "years old, or when the problem is spread across the roof (granule loss, curling, brittle shingles, many leaks). "
     "A single leaking boot or flashing detail is almost always worth repairing.</p>"),
    ("Will homeowners insurance pay for a roof leak repair?",
     "<p>Insurance usually pays when the leak comes from sudden storm damage such as hail, wind or a fallen tree, and the "
     "repair exceeds your deductible. It does not pay for wear and tear, such as old pipe boots, failed sealant or "
     "age-related shingle damage. Interior water damage may be covered even when the roof repair itself is not; check "
     "your policy.</p>"),
    ("Can new shingles match my existing roof?",
     "<p>Rarely on a roof older than about 8–10 years. Products are discontinued and existing shingles fade. A good "
     "roofer will find the closest color, and may suggest repairing a less visible slope with salvaged shingles.</p>"),
    ("How accurate is this roof repair estimate?",
     "<p>It gives you a realistic Texas price range for the items you choose. The real price depends on what the roofer "
     "finds once shingles are lifted, especially rotted decking or hidden flashing problems. All unit prices are editable "
     "so contractors can use their own numbers.</p>"),
]

TOOL = {
    "slug": SLUG,
    "title": "Roof Repair Cost Calculator (Texas 2026) | Roof Estimate Pro",
    "description": "Free roof repair cost calculator with Texas 2026 prices. Itemize shingles, boots, flashing, decking and tarps, and see whether to repair or replace.",
    "h1": "Roof Repair Cost Calculator",
    "lede": "Build an itemized repair ticket the way a roofer prices one: shingle patches, pipe boots, flashing, decking, vents and tarps, scaled for pitch and height, with Texas 2026 prices and a repair-or-replace check.",
    "form": form,
    "body": body,
    "faqs": faqs,
    "related": ["roof-replacement-cost-calculator", "roof-insurance-claim-calculator", "shingle-calculator"],
}
