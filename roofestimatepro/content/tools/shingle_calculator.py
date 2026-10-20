"""Shingle & Materials Calculator — full order list for an asphalt shingle roof.

Script: static/assets/js/tools/shingle-calculator.js
"""

from content.ui import num, select, seg, switch, group, prices
from siteconfig import WASTE

SLUG = "shingle-calculator"

PITCHES = [(r, f"{r}/12" + (" (low slope)" if r < 4 else " (walkable)" if r <= 6 else " (steep)" if r <= 9 else " (very steep)"))
           for r in range(2, 15)]
W = WASTE["shingle"]

form = (
    group("Roof size & waste",
          seg("area_mode", "Roof size", [("sqft", "Square feet"), ("squares", "Squares")], "sqft"),
          num("roof_sqft", "Roof area", 2400, unit="sq ft", min=0, show="area_mode=sqft",
              tip="True sloped surface area from a measurement report or the roof square footage calculator, not the floor area."),
          num("squares", "Roof squares", 24, unit="sq", min=0, show="area_mode=squares",
              help="1 square = 100 sq ft of roof surface."),
          select("pitch", "Roof pitch", PITCHES, 6, numeric=True,
                 tip="Used to estimate rake and hip lengths when you don't have measurements, and for low-slope warnings."),
          seg("style", "Roof style",
              [("gable", f"Simple gable ({W['simple']}%)"), ("hip", f"Hip / some valleys ({W['moderate']}%)"),
               ("complex", f"Cut-up ({W['complex']}%)")], "hip"),
          seg("waste_mode", "Waste factor", [("style", "Use roof style"), ("custom", "Custom %")], "style"),
          num("waste_custom", "Custom waste", 12, unit="%", min=0, max=40, show="waste_mode=custom",
              help="Measurement reports list a suggested waste. 10% gable, 12–15% hip, 15–20% cut-up."),
          ),
    group("Edges & intersections (linear feet)",
          seg("lf_mode", "Linear footage", [("estimate", "Estimate from area"), ("measured", "I have measurements")], "estimate"),
          num("eave_lf", "Eaves", 180, unit="ln ft", min=0, show="lf_mode=measured",
              help="Level bottom edges where the gutters hang. Gets drip edge and starter."),
          num("rake_lf", "Rakes", 40, unit="ln ft", min=0, show="lf_mode=measured",
              help="Sloped edges at gable ends. Gets drip edge (and starter if checked)."),
          num("ridge_lf", "Ridges", 30, unit="ln ft", min=0, show="lf_mode=measured",
              help="Level peaks at the top. Gets ridge cap and ridge vent."),
          num("hip_lf", "Hips", 80, unit="ln ft", min=0, show="lf_mode=measured",
              help="Sloped outside corners where two planes meet. Gets hip cap."),
          num("valley_lf", "Valleys", 24, unit="ln ft", min=0, show="lf_mode=measured",
              help="Inside corners where two planes drain together. Gets ice &amp; water shield."),
          ),
    group("Shingles & underlayment",
          select("line", "Shingle line",
                 [("arch", "Architectural (laminated)"), ("class4", "Impact-resistant Class 4"), ("3tab", "3-tab")],
                 "arch", cls="full"),
          seg("bpsq", "Bundles per square", [(3, "3 bundles"), (4, "4 bundles")], 3, numeric=True,
              tip="Most architectural and 3-tab lines are 3 bundles per square. Some heavy designer and Class 4 lines are 4."),
          seg("nails", "Nails per shingle", [(4, "4 nails (standard)"), (6, "6 nails (high wind)")], 4, numeric=True,
              tip="Use 6 nails for the manufacturer's high-wind application, typical on the Texas coast and required for many windstorm inspections."),
          select("und", "Underlayment",
                 [("syn", "Synthetic (10 sq / roll)"), ("f15", "#15 felt (4 sq / roll)"), ("f30", "#30 felt (2 sq / roll)")],
                 "syn", cls="full"),
          switch("iw_valleys", "Ice &amp; water shield in valleys", True),
          switch("iw_eaves", "Ice &amp; water shield along eaves", False),
          switch("starter_rakes", "Starter strip on rakes too", True),
          seg("ridge_type", "Hip and ridge cap", [("ded", "Dedicated ridge cap"), ("cut", "Cut from 3-tab")], "ded"),
          ),
    group("Vents, penetrations & flashing",
          seg("vent", "Exhaust ventilation",
              [("box", "Replace box vents / turbines"), ("ridge", "Switch to ridge vent"), ("keep", "Reuse existing")], "box"),
          num("box_vents", "Box vents", 4, min=0, step=1),
          num("turbines", "Turbines", 0, min=0, step=1),
          num("rv_lf", "Ridge vent length", 0, unit="ln ft", min=0, show="vent=ridge",
              help="Leave 0 to run vent along all ridges, stopping 1 ft short of each end."),
          num("pipes", "Pipe penetrations", 4, min=0, step=1, help="Plumbing vents that get new pipe boots."),
          switch("flash_on", "Replace step &amp; headwall flashing", False),
          num("wall_lf", "Sidewall (step flashing)", 20, unit="ln ft", min=0, show="flash_on=true",
              help="Where a sloped roof runs up beside a wall."),
          num("head_lf", "Headwall (apron flashing)", 12, unit="ln ft", min=0, show="flash_on=true",
              help="Where the top of a roof plane meets a wall."),
          ),
    prices("Edit unit prices & coverage",
           num("p_arch", "Architectural shingles", 42, pre="$", unit="/bundle", min=0),
           num("p_class4", "Class 4 shingles", 58, pre="$", unit="/bundle", min=0),
           num("p_3tab", "3-tab shingles", 32, pre="$", unit="/bundle", min=0),
           num("p_starter", "Starter strip", 48, pre="$", unit="/bundle", min=0),
           num("starter_lf", "Starter coverage", 110, unit="ln ft/bdl", min=1),
           num("p_ridge", "Hip &amp; ridge cap", 72, pre="$", unit="/bundle", min=0),
           num("ridge_lf_ded", "Ridge cap coverage", 30, unit="ln ft/bdl", min=1),
           num("ridge_lf_cut", "Cut 3-tab coverage", 25, unit="ln ft/bdl", min=1),
           num("p_syn", "Synthetic underlayment", 95, pre="$", unit="/roll", min=0),
           num("cov_syn", "Synthetic coverage", 10, unit="sq/roll", min=0.5),
           num("p_f15", "#15 felt", 28, pre="$", unit="/roll", min=0),
           num("cov_f15", "#15 felt coverage", 4, unit="sq/roll", min=0.5),
           num("p_f30", "#30 felt", 32, pre="$", unit="/roll", min=0),
           num("cov_f30", "#30 felt coverage", 2, unit="sq/roll", min=0.5),
           num("p_iw", "Ice &amp; water shield", 95, pre="$", unit="/roll", min=0),
           num("iw_lf", "Ice &amp; water coverage", 65, unit="ln ft/roll", min=1, tip="A 2-square roll of 36-inch membrane runs about 65–67 ft."),
           num("p_drip", "Drip edge (10 ft)", 11, pre="$", unit="/piece", min=0),
           num("p_nails", "Coil nails", 62, pre="$", unit="/box", min=0),
           num("nails_box", "Nails per box", 7200, min=1, step=1),
           num("nails_sq", "Nails per square (4-nail)", 320, min=0, step=1,
               tip="Includes starter, hip and ridge and normal loss. 6-nail installs use 1.5 times this."),
           num("p_cap", "Cap nails (underlayment)", 45, pre="$", unit="/box", min=0),
           num("cap_box", "Cap nails per box", 2000, min=1, step=1),
           num("cap_sq", "Cap nails per square", 100, min=0, step=1),
           num("p_rv", "Ridge vent (4 ft)", 22, pre="$", unit="/piece", min=0),
           num("p_box", "Box vent", 28, pre="$", unit="each", min=0),
           num("p_turb", "Turbine vent", 60, pre="$", unit="each", min=0),
           num("p_boot", "Pipe boot", 14, pre="$", unit="each", min=0),
           num("p_step", "Step flashing", 45, pre="$", unit="/100 pcs", min=0),
           num("p_head", "Apron flashing (10 ft)", 16, pre="$", unit="/piece", min=0),
           num("p_cement", "Roof cement / sealant", 8, pre="$", unit="/tube", min=0),
           num("tax", "Sales tax", 8.25, unit="%", min=0, max=15),
           note="Quantities round up to whole packages. Prices are typical Texas supply-house prices for 2026 before contractor markup."),
)

body = """
<h2 id="how-it-works">How the shingle calculator builds your order</h2>
<p>A shingle roof is more than bundles. A typical 24-square re-roof needs a dozen different products, and every one of
them is driven by either the roof <em>area</em> or a <em>linear footage</em>: the length of the eaves, rakes, ridges,
hips and valleys. This calculator works the way a supplier's takeoff does:</p>
<ol>
  <li><strong>Area items</strong> (field shingles, underlayment, nails) come from the roof area in squares. Shingles get
  a waste factor; underlayment and nails are figured on the net or ordered squares.</li>
  <li><strong>Edge items</strong> come from linear feet: drip edge on eaves and rakes, starter on eaves (and rakes),
  hip and ridge cap on hips and ridges, ice &amp; water shield in valleys.</li>
  <li><strong>Count items</strong> are pipe boots, vents and flashing.</li>
  <li>Every quantity is rounded <em>up</em> to a whole bundle, roll, box or piece, because that is how you buy it.</li>
</ol>
<div class="formula">Squares          = roof area ÷ 100
Shingle bundles  = ⌈squares × (1 + waste %) × bundles per square⌉
Starter bundles  = ⌈(eaves + rakes) ÷ starter ln ft per bundle⌉
Ridge cap bundles= ⌈(ridges + hips) ÷ cap ln ft per bundle⌉
Underlayment     = ⌈squares × 1.05 ÷ squares per roll⌉
Drip edge pieces = ⌈(eaves + rakes) × 1.05 ÷ 10⌉
Coil nail boxes  = ⌈ordered squares × nails per square ÷ nails per box⌉</div>

<h2 id="measuring">How to measure the linear-foot items</h2>
<p>A measurement report from EagleView, Hover or a similar service lists every one of these totals. If you are
measuring yourself, walk the roof edges with a tape or measure from the ground and add the slope for rakes and hips.</p>
<div class="table-wrap"><table><thead><tr><th>Item</th><th>Where it is</th><th>What it drives</th></tr></thead><tbody>
<tr><td>Eaves</td><td>Level bottom edges, where gutters hang</td><td>Drip edge, starter, optional ice &amp; water</td></tr>
<tr><td>Rakes</td><td>Sloped edges at gable ends</td><td>Drip edge, starter (recommended)</td></tr>
<tr><td>Ridges</td><td>Level peaks</td><td>Ridge cap, ridge vent</td></tr>
<tr><td>Hips</td><td>Sloped outside corners</td><td>Hip cap</td></tr>
<tr><td>Valleys</td><td>Sloped inside corners</td><td>Ice &amp; water shield, extra waste</td></tr>
</tbody></table></div>
<p>No measurements? Choose <em>Estimate from area</em>. The calculator assumes a rectangular house about 1.6 times as long
as it is wide, works out the footprint from your area and pitch, and sizes the edges for a gable, hip or cut-up roof.
It shows the lengths it used in the notes. It is fine for a budget; for an actual order, use measured numbers.</p>

<h2 id="bundles">How shingle bundles work</h2>
<p>Most architectural and 3-tab shingles are packaged three bundles to the square, so each bundle covers about
33.3 sq ft. Some heavier designer and impact-resistant lines are four bundles to the square. Check the wrapper. Field
shingles are the only item that gets the full waste factor. Starter and ridge cap are separate products sized by
linear feet, so do not double count them by adding extra squares.</p>
<p>Dedicated hip and ridge cap typically covers 20–33 linear feet per bundle depending on the profile; the default
here is 30. Cutting caps from 3-tab shingles yields about 25 feet per bundle and is cheaper, but many manufacturers
require their own cap product for the full system warranty.</p>

<h2 id="waste">How much waste to add</h2>
<p>Waste covers cut-offs at rakes, hips and valleys plus starter courses and breakage. These are the defaults:</p>
<div class="table-wrap"><table><thead><tr><th>Roof type</th><th>Typical waste</th></tr></thead><tbody>
<tr><td>Simple gable, few penetrations</td><td>10%</td></tr>
<tr><td>Hip roof or a few valleys</td><td>14%</td></tr>
<tr><td>Cut-up roof, many hips, valleys and dormers</td><td>18%</td></tr>
</tbody></table></div>
<p>A measurement report's suggested waste is usually a good starting point. On an insurance claim, the carrier's
estimate should carry a waste factor on the shingle line; if it does not, ask why.</p>

<h2 id="underlayment">Underlayment, ice &amp; water and drip edge</h2>
<p>Synthetic underlayment has largely replaced felt: a 10-square roll weighs less than a 2-square roll of #30 and
does not wrinkle in the Texas sun. On slopes from 2/12 up to 4/12, shingle manufacturers and the International
Residential Code call for two layers of underlayment, so double the rolls (the calculator flags this). Ice &amp; water
shield is not required for ice dams in most of Texas, but it is standard practice in valleys and around penetrations;
a 2-square roll covers about 65 feet of a 36-inch valley. In the Panhandle, check whether your city requires an ice
barrier at the eaves.</p>
<p>Drip edge at eaves and rakes is required by the IRC for shingle roofs, and most Texas cities enforce the IRC.
It is also one of the most commonly missed items on insurance estimates.</p>

<h2 id="texas">Texas notes: high-wind nailing and impact-resistant shingles</h2>
<p>On the Gulf Coast, homes in the Texas Windstorm Insurance Association (TWIA) area need a roof built to the Texas
Department of Insurance windstorm requirements and a certificate of compliance (WPI-8) to keep TWIA coverage. In
practice that means the shingle manufacturer's high-wind application, typically six nails per shingle, high-wind
rated starter at eaves and rakes, and corrosion-resistant fasteners near salt water. Confirm the exact requirements with
the appointed inspector or engineer before ordering.</p>
<p>Elsewhere in Texas, hail drives the decision. Class 4 impact-resistant lines (UL 2218) cost roughly 35–40% more
per bundle, but many Texas insurers offer a premium discount for them. Ask your agent for the number before you choose.</p>

<div class="callout"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
<p><strong>Checking an insurance estimate?</strong> Compare its starter, ridge cap, drip edge, ice &amp; water and
pipe boot lines to this order list. If any are missing, our <a href="/services/insurance-claim-estimate-review/">claim
estimate review</a> ($50) goes through the carrier's estimate line by line.</p></div>
"""

faqs = [
    ("How many bundles of shingles do I need per square?",
     "<p>Three bundles per square for most architectural and 3-tab shingles, so a 24-square roof with 14% waste needs "
     "about 83 bundles. Some heavy designer and Class 4 lines are packaged four bundles per square.</p>"),
    ("How do I calculate shingles for my roof?",
     "<p>Divide the roof area by 100 to get squares, add a waste factor (10–18%), and multiply by the bundles per square. "
     "Use the true sloped roof area, not the house's floor area; the "
     "<a href=\"/tools/roof-square-footage-calculator/\">roof square footage calculator</a> converts a footprint and pitch.</p>"),
    ("Do I need starter shingles, or can I cut them?",
     "<p>You can cut starter from 3-tab shingles, but dedicated starter strip has its sealant in the right place and is "
     "required by most manufacturers for the full warranty and for high-wind installs. One bundle covers roughly "
     "100–120 linear feet.</p>"),
    ("How many nails do I need for a shingle roof?",
     "<p>About 320 coil nails per square at four nails per shingle, including starter and ridge, and about 480 at six "
     "nails. A 7,200-count box covers roughly 22 squares at four nails or 15 squares at six.</p>"),
    ("Is ice and water shield required in Texas?",
     "<p>Ice barrier for ice dams is generally not required in most of Texas, but it is standard in valleys and around "
     "penetrations and is often required by the shingle manufacturer there. Some Panhandle jurisdictions do require it "
     "at the eaves, so check local code.</p>"),
    ("Should I use synthetic underlayment or felt?",
     "<p>Synthetic is lighter, stronger, safer to walk on and lies flat in heat; it is the default on most Texas re-roofs. "
     "#30 felt is still accepted and is cheaper per roll, but covers only two squares per roll.</p>"),
]

TOOL = {
    "slug": SLUG,
    "title": "Shingle & Roofing Materials Calculator | Roof Estimate Pro",
    "description": "Free shingle calculator: bundles, starter, ridge cap, underlayment, ice & water, drip edge, nails and vents, rounded to packages with Texas 2026 prices.",
    "h1": "Shingle & Roofing Materials Calculator",
    "lede": "Turn a roof area and its edge lengths into a full order list: shingle bundles, starter, hip and ridge cap, underlayment, ice &amp; water shield, drip edge, nails, vents and boots, with editable Texas 2026 prices.",
    "form": form,
    "body": body,
    "faqs": faqs,
    "related": ["roof-square-footage-calculator", "attic-ventilation-calculator", "roof-replacement-cost-calculator"],
}
