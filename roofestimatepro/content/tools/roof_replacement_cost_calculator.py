"""Roof Replacement Cost Calculator — the flagship tool and the reference
implementation every other tool module follows.

A tool module exposes TOOL with:
  slug, title, description, h1, lede      page meta and hero
  form                                    HTML built from content.ui helpers
  body                                    explainer article (HTML, h2 with ids)
  faqs                                    [(question, answer_html)]
  related                                 [tool slugs]
The matching script is static/assets/js/tools/<slug>.js.
"""

from content.ui import num, select, seg, rng, group, prices, switch
from siteconfig import MATERIALS, WASTE, TEXAS_REGIONS, US_REGIONS

SLUG = "roof-replacement-cost-calculator"

PITCHES = [(r, f"{r}/12" + (" (low slope)" if r < 3 else " (walkable)" if r <= 6 else " (steep)" if r <= 9 else " (very steep)")) for r in range(2, 15)]
REGION_OPTS = ([(r["key"], f"Texas — {r['name']}") for r in TEXAS_REGIONS]
               + [(r["key"], r["name"]) for r in US_REGIONS])

form = (
    group("Roof size",
          seg("area_mode", "How do you want to size the roof?",
              [("known", "I know the roof area"), ("footprint", "Estimate from home footprint")], "footprint"),
          num("roof_sqft", "Roof area", 2400, unit="sq ft", min=0,
              tip="True sloped surface area from a measurement report (EagleView, Hover, etc.) or the square footage calculator.",
              show="area_mode=known"),
          num("footprint", "Home footprint incl. garage", 2100, unit="sq ft", min=0,
              help="Ground-floor area under the roof, plus attached garage and covered porches.", show="area_mode=footprint"),
          num("overhang", "Eave overhang", 18, unit="in", min=0, show="area_mode=footprint"),
          select("pitch", "Roof pitch", PITCHES, 6, numeric=True,
                 tip="Inches of rise per 12 inches of run. Most Texas homes are 5/12 to 8/12."),
          select("stories", "Stories", [(1, "1 story"), (2, "2 stories"), (3, "3+ stories")], 1, numeric=True),
          seg("complexity", "Roof complexity",
              [("simple", "Simple gable"), ("moderate", "Hip / some valleys"), ("complex", "Cut-up, many facets")],
              "moderate"),
          ),
    group("Materials & tear-off",
          select("material", "New roofing material", [(m["key"], m["name"]) for m in MATERIALS], "arch", cls="full"),
          select("layers", "Layers to tear off", [(0, "None (new deck / overlay)"), (1, "1 layer"), (2, "2 layers"), (3, "3 layers")], 1, numeric=True),
          select("existing", "Existing roof type",
                 [("asphalt", "Asphalt shingles"), ("shake", "Wood shake"), ("metal", "Metal"), ("tile", "Tile")], "asphalt"),
          rng("deck_pct", "Decking to replace", 5, 0, 100, 1, "%",
              help="Rotted or delaminated sheathing found at tear-off. 0–10% is typical; older Texas homes with plank decking can need full re-decking."),
          ),
    group("Location & extras",
          select("region", "Project location", REGION_OPTS, "dfw", cls="full"),
          num("skylights", "Skylights to re-flash", 0, min=0, step=1),
          num("chimneys", "Chimneys to re-flash", 0, min=0, step=1),
          num("gutter_lf", "New gutters (optional)", 0, unit="ln ft", min=0, step=1),
          num("permit", "Permit & inspection", 350, pre="$", min=0,
              help="Most Texas cities charge $150–$500. Many unincorporated county areas need no permit."),
          ),
    prices("Edit unit prices",
           num("mat_price", "Roofing product", 140, pre="$", unit="/sq", min=0),
           num("acc_price", "Accessories", 60, pre="$", unit="/sq", min=0,
               tip="Underlayment, starter, ridge cap, drip edge, pipe boots, vents and fasteners."),
           num("lab_price", "Install labor", 170, pre="$", unit="/sq", min=0),
           num("tear1", "Tear-off, first layer", 75, pre="$", unit="/sq", min=0),
           num("tear_add", "Each extra layer", 45, pre="$", unit="/sq", min=0),
           num("deck_price", "Decking (4×8 OSB)", 85, pre="$", unit="/sheet", min=0),
           num("sky_price", "Skylight re-flash", 450, pre="$", unit="each", min=0),
           num("chim_price", "Chimney re-flash", 575, pre="$", unit="each", min=0),
           num("gutter_price", "Seamless gutters", 11, pre="$", unit="/ln ft", min=0),
           num("tax", "Sales tax on materials", 8.25, unit="%", min=0, max=15),
           num("op", "Overhead & profit", 20, unit="%", min=0, max=60,
               tip="Contractor overhead and profit. 10% + 10% is the insurance-industry convention; retail jobs often run 20–30%."),
           note="Product, accessory and labor prices refill when you change the material. Labor items are scaled by pitch, stories, complexity and region."),
)


def _material_table():
    rows = []
    for m in MATERIALS:
        lo, hi = m["range"]
        rows.append(f"<tr><td>{m['name']}</td><td>${lo:,}–${hi:,}</td><td>${lo/100:.2f}–${hi/100:.2f}</td>"
                    f"<td>{m['life']} yrs</td></tr>")
    return ("<div class=\"table-wrap\"><table><thead><tr><th>Material</th><th>Installed per square</th>"
            "<th>Per sq ft of roof</th><th>Typical life</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table></div>")


def _region_table():
    rows = "".join(f"<tr><td>{r['name']}</td><td>{'+' if r['factor'] > 1 else ''}{round((r['factor'] - 1) * 100)}%</td></tr>"
                   for r in TEXAS_REGIONS)
    return ("<div class=\"table-wrap\"><table><thead><tr><th>Texas region</th><th>Labor vs. DFW baseline</th></tr></thead>"
            f"<tbody>{rows}</tbody></table></div>")


body = f"""
<h2 id="how-it-works">How this roof replacement calculator works</h2>
<p>Most online roof cost calculators multiply your square footage by one number and call it a day. This one works
the way an estimator builds a bid, so you can see where every dollar goes and change any assumption you disagree with:</p>
<ol>
  <li><strong>Roof area.</strong> If you know the true sloped area (from a measurement report or our
  <a href="/tools/roof-square-footage-calculator/">roof square footage calculator</a>), enter it. Otherwise the tool takes
  your footprint, adds the eave overhang around the perimeter and multiplies by the pitch factor for your roof slope.</li>
  <li><strong>Squares and waste.</strong> Roofing is sold by the <em>square</em> (100 sq ft). Material is ordered on area
  plus a waste factor for cuts at hips, valleys and rakes: about 10% on a simple gable, 14% on a typical hip roof and 18%
  on a cut-up roof for shingles, less for metal panels.</li>
  <li><strong>Materials, then labor.</strong> Product and accessories (underlayment, starter, ridge cap, drip edge, vents,
  pipe boots and fasteners) are priced per square, with Texas sales tax on materials. Labor and tear-off are scaled for
  pitch, number of stories, roof complexity and your region.</li>
  <li><strong>Decking, extras and permit.</strong> Rotten sheathing, skylight and chimney flashing, optional gutters and
  the city permit are added as their own lines.</li>
  <li><strong>Overhead &amp; profit.</strong> A contractor's overhead and profit is applied to the subtotal. Insurance
  estimates conventionally use 10% overhead + 10% profit; retail bids often land higher.</li>
</ol>
<div class="formula">Roof area  = (footprint + perimeter × overhang) × pitch factor
Squares    = roof area ÷ 100            Ordered squares = squares × (1 + waste %)
Total      = materials + tax + labor + tear-off + decking + extras + O&amp;P + permit</div>

<h2 id="texas-costs">Roof replacement cost in Texas (2026)</h2>
<p>These are the installed price ranges the calculator is calibrated to for Dallas–Fort Worth. They include
tear-off of one layer, standard accessories, labor and a typical contractor margin, but not decking repairs or permits.</p>
{_material_table()}
<p>Run through the calculator with its defaults, a typical 2,000 sq ft single-story Texas home with a 6/12 hip roof
(about 25 squares of roof) comes to roughly $14,000–$18,000 for architectural shingles, $16,500–$21,000 for Class 4
impact-resistant shingles and $35,000–$44,000 for standing seam metal.</p>
<h3 id="regional">Regional differences across Texas</h3>
<p>Material prices are fairly flat statewide; labor is what moves. The calculator adjusts labor and tear-off by region:</p>
{_region_table()}
<p>After a large hail event, crews and materials in the affected metro can run 10–25% above these numbers for several
months. If you are pricing a job right after a storm, raise the labor rate in <em>Edit unit prices</em>.</p>

<h2 id="cost-drivers">What drives the price up (or down)</h2>
<ul>
  <li><strong>Pitch.</strong> Anything over 7/12 needs roof jacks and harnesses and slows the crew. The calculator adds 10%
  to labor at 7–8/12, 20% at 9–10/12, 30% at 11–12/12 and 45% above that.</li>
  <li><strong>Height.</strong> Two-story homes add about 8% to labor; three stories about 15%.</li>
  <li><strong>Complexity.</strong> Every valley, hip, dormer and wall flashing adds cuts, waste and labor.</li>
  <li><strong>Tear-off.</strong> Each extra layer of old shingles adds disposal weight. Tile and shake tear-offs cost more
  than asphalt.</li>
  <li><strong>Decking.</strong> Hidden rot is the most common change order. A good contract states the per-sheet price
  up front, which is why the calculator lets you set it.</li>
  <li><strong>Code items.</strong> Drip edge, ice barrier in valleys, ventilation upgrades and high-wind nailing on the
  Gulf Coast (where the Texas Windstorm Insurance Association requires WPI-8 certification) all add cost.</li>
</ul>

<h2 id="insurance">If insurance is paying for the roof</h2>
<p>For hail or wind claims, your carrier will write its own estimate, usually in Xactimate, and pay replacement cost minus
depreciation and your deductible. Use the <a href="/tools/roof-insurance-claim-calculator/">roof insurance claim
calculator</a> to see what the first check and the recoverable depreciation should look like. If the carrier's numbers are
far below what you see here, our <a href="/services/insurance-claim-estimate-review/">claim estimate review</a> compares
their estimate line by line against the roof.</p>

<div class="callout"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
<p><strong>Impact-resistant shingles pay you back in Texas.</strong> Many Texas insurers offer premium discounts for roofs
rated UL 2218 Class 4. Ask your agent for the discount on your policy before you choose between architectural and
Class 4 shingles; the upgrade often pays for itself within a few years.</p></div>

<h2 id="compare-quotes">Using the result to compare contractor quotes</h2>
<p>Print or save the estimate and line it up against each bid. Ask every contractor to quote the same things: number of
squares, waste factor, shingle line, underlayment type, ventilation, decking price per sheet, and whether the permit and
disposal are included. A bid that is far below this estimate usually leaves out decking, drip edge or ventilation, or
uses a cheaper product than the one you picked.</p>
"""

faqs = [
    ("How much does a new roof cost in Texas in 2026?",
     "<p>Most Texas homeowners pay $450–$650 per square (100 sq ft) for architectural shingles, $550–$800 for Class 4 "
     "impact-resistant shingles and $1,100–$1,700 for standing seam metal, installed with tear-off. A typical "
     "2,000 sq ft home needs about 24–30 squares, so a shingle roof usually lands between $12,000 and $20,000.</p>"),
    ("How accurate is this roof replacement calculator?",
     "<p>With a measured roof area and your actual material choice, it typically lands within 10–15% of a professional "
     "bid. The biggest unknown is decking: you won't know how much needs replacing until the old roof is off. Every unit "
     "price is editable, so contractors can plug in their own numbers.</p>"),
    ("What is a roofing square?",
     "<p>A square is 100 square feet of roof surface. A 2,500 sq ft roof is 25 squares. Shingles are usually sold three "
     "bundles to the square.</p>"),
    ("Does the estimate include tear-off and disposal?",
     "<p>Yes. Tear-off of the layers you choose, plus haul-off and dump fees, is included as its own line. Set layers to "
     "zero for new construction.</p>"),
    ("Why does my roof pitch matter so much?",
     "<p>Pitch changes the true area (a 12/12 roof has 41% more surface than its footprint) and the labor, because steep "
     "roofs need safety equipment and are slower to work. Use the <a href=\"/tools/roof-pitch-calculator/\">roof pitch "
     "calculator</a> if you are not sure of yours.</p>"),
    ("Can a professional estimator check my numbers?",
     "<p>Yes. Use the <em>Have a pro estimator review this</em> button. It sends your inputs to our team, and we can build "
     "a full Xactimate estimate for contractors, adjusters or homeowners anywhere in Texas and most other states.</p>"),
]

TOOL = {
    "slug": SLUG,
    "title": "Roof Replacement Cost Calculator (Texas 2026 Prices) | Roof Estimate Pro",
    "description": "Free roof replacement cost calculator with Texas 2026 pricing. Itemized materials, labor, tear-off, decking, permit and O&P for shingle, metal and tile roofs.",
    "h1": "Roof Replacement Cost Calculator",
    "lede": "Price a full re-roof the way an estimator does: true roof area, waste, materials, labor scaled for pitch and height, tear-off, decking, permit and overhead & profit, with Texas 2026 unit prices you can edit.",
    "form": form,
    "body": body,
    "faqs": faqs,
    "related": ["roof-square-footage-calculator", "roof-insurance-claim-calculator", "shingle-calculator"],
}
