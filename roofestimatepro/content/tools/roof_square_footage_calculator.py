"""Roof Square Footage Calculator — footprint or plane-by-plane roof area,
squares, waste and bundles. Script: static/assets/js/tools/roof-square-footage-calculator.js
"""

import math

from content.ui import num, select, seg, text, group, rows, prices

SLUG = "roof-square-footage-calculator"


def _pitch_label(r):
    if r == 0:
        return "Flat (0/12)"
    tag = " low slope" if r < 3 else " walkable" if r <= 6 else " steep" if r <= 9 else " very steep"
    return f"{r}/12 ·{tag}"


PITCHES = [(r, _pitch_label(r)) for r in range(0, 19)]
ROW_PITCHES = [(r, f"{r}/12") for r in range(0, 19)]

plane_fields = (
    text("name", "Plane", "", row=True, autoname="Plane")
    + select("shape", "Shape", [("rect", "Rectangle"), ("tri", "Triangle"), ("trap", "Trapezoid")], "rect", row=True)
    + num("a", "Eave / base length", 40, unit="ft", min=0, row=True)
    + num("b", "Ridge length (trapezoid)", 0, unit="ft", min=0, row=True)
    + num("h", "Eave to ridge", 15, unit="ft", min=0, row=True)
    + select("pitch", "Pitch", ROW_PITCHES, 6, numeric=True, row=True)
    + num("qty", "Qty", 1, min=1, step=1, row=True)
)

# Plane rows have seven inputs; lay them out on a 6-column grid (2 on phones)
# instead of the default auto-fit so selects never collapse.
ROW_CSS = ("<style>#tool-form[data-tool='roof-square-footage-calculator'] .row-item{grid-template-columns:repeat(6,minmax(0,1fr))}"
           "#tool-form[data-tool='roof-square-footage-calculator'] .row-item>.field{grid-column:span 2}"
           "#tool-form[data-tool='roof-square-footage-calculator'] .row-item>.field:first-child{grid-column:span 4}"
           "#tool-form[data-tool='roof-square-footage-calculator'] .row-item>.row-del{grid-column:span 2;justify-self:end}"
           "@media(max-width:560px){#tool-form[data-tool='roof-square-footage-calculator'] .row-item{grid-template-columns:1fr 1fr}"
           "#tool-form[data-tool='roof-square-footage-calculator'] .row-item>.field{grid-column:span 1}"
           "#tool-form[data-tool='roof-square-footage-calculator'] .row-item>.field:first-child{grid-column:span 2}"
           "#tool-form[data-tool='roof-square-footage-calculator'] .row-item>.row-del{grid-column:span 1}}</style>")

form = (
    group("How to measure",
          seg("mode", "Measuring method",
              [("footprint", "From the house footprint"), ("planes", "Plane by plane")], "footprint"),
          ),
    ROW_CSS,
    '<div data-show="mode=footprint" style="margin-bottom:22px">',
    group("Footprint",
          seg("fp_input", "Footprint input", [("dims", "Length × width"), ("area", "Total footprint sq ft")], "dims"),
          num("length", "Footprint length", 60, unit="ft", min=0, show="fp_input=dims",
              tip="Long side of the house, wall to wall, including attached garage."),
          num("width", "Footprint width", 32, unit="ft", min=0, show="fp_input=dims",
              tip="Short side, wall to wall. Eaves normally run along the long sides."),
          num("fp_area", "Footprint area", 1900, unit="sq ft", min=0, show="fp_input=area", cls="full",
              help="Ground-floor area under the roof, including garage and covered porches. Assumes a roughly square footprint for the overhang."),
          num("eave", "Eave overhang", 18, unit="in", min=0,
              help="Horizontal distance the roof extends past the wall at the gutters. 12–24 in. is typical in Texas."),
          num("rake", "Rake overhang", 12, unit="in", min=0,
              help="Overhang at gable ends. On a hip roof, enter the same as the eave."),
          select("pitch", "Roof pitch", PITCHES, 6, numeric=True, cls="full",
                 tip="Inches of rise per 12 inches of run. Not sure? Use the roof pitch calculator."),
          ),
    '</div><div data-show="mode=planes" style="margin-bottom:22px">',
    group("Roof planes",
          seg("dims", "How were the planes measured?",
              [("sloped", "On the roof (sloped)"), ("plan", "From a plan / aerial (horizontal)")], "plan",
              tip="Sloped: measured with a tape on the roof surface, so no pitch factor is applied. Plan: measured from drawings or a satellite image, so each plane is multiplied by its pitch factor."),
          ),
    rows("planes", plane_fields, start=2, min=1, add_label="Add a roof plane",
         legend="Roof planes"),
    '<p style="margin:-10px 0 0;font-size:.78rem;line-height:1.45;color:var(--muted)">Rectangle: eave length × eave-to-ridge. Triangle (hip end): base × height. '
    'Trapezoid (hip side): eave length + ridge length, × height. Qty repeats identical planes.</p></div>',
    group("Waste & ordering",
          seg("style", "Roof style (waste factor)",
              [("gable", "Gable 10%"), ("hip", "Hip 15%"), ("complex", "Complex 18%"), ("custom", "Custom")], "hip",
              tip="Shingle waste for cuts at rakes, hips and valleys. Cut-up roofs with many valleys and dormers run 18–20%."),
          num("waste_custom", "Custom waste factor", 12, unit="%", min=0, max=40, show="style=custom"),
          ),
    prices("Ordering assumptions",
           num("bundles_per_sq", "Bundles per square", 3, min=1, step=1,
               tip="Most architectural and 3-tab shingles are 3 bundles per square. Some heavy designer shingles are 4 or 5."),
           note="Squares to order are rounded up to the next full bundle. Starter, ridge cap and hip cap are separate; the shingle calculator counts them."),
)

# Pitch factor reference table (2/12 to 18/12)
_rows = []
for r in range(2, 19):
    pf = math.sqrt(1 + (r / 12) ** 2)
    deg = math.degrees(math.atan(r / 12))
    _rows.append(f"<tr><td>{r}/12</td><td>{deg:.1f}°</td><td>{pf:.3f}</td><td>+{(pf - 1) * 100:.1f}%</td>"
                 f"<td>{2000 * pf:,.0f}</td></tr>")
PITCH_TABLE = ("<div class=\"table-wrap\"><table><thead><tr><th>Pitch</th><th>Angle</th><th>Pitch factor</th>"
               "<th>Extra area vs. flat</th><th>Roof sq ft on 2,000 sq ft of plan</th></tr></thead><tbody>"
               + "".join(_rows) + "</tbody></table></div>")

body = f"""
<h2 id="how-it-works">How this roof square footage calculator works</h2>
<p>A roof is always bigger than the floor under it. Two things make it bigger: the <strong>overhang</strong> past the
walls, and the <strong>slope</strong>, because a sloped plane covers more surface than its shadow on the ground. The
calculator handles both, in either of two ways.</p>
<ul>
  <li><strong>From the house footprint.</strong> Enter the wall-to-wall length and width (or the total footprint), the eave
  and rake overhangs and one pitch. This is the fastest method and works well for simple gable and hip roofs where every
  plane has the same slope.</li>
  <li><strong>Plane by plane.</strong> Break the roof into rectangles, triangles and trapezoids and enter each one with its
  own pitch. Use this for roofs that mix slopes, porches at a lower pitch, or when you are working from a measurement
  report or a drawing.</li>
</ul>
<p>Both methods end in the same place: total roof area, <em>squares</em> (one square = 100 sq ft), a waste factor and
the number of squares and bundles to order.</p>
<div class="formula">Plan area      = (length + 2 × rake overhang) × (width + 2 × eave overhang)
Pitch factor   = √(1 + (rise ÷ 12)²)
Roof area      = plan area × pitch factor
Rectangle = L × H   ·   Triangle = ½ × B × H   ·   Trapezoid = ½ × (eave + ridge) × H
Squares        = roof area ÷ 100
Order          = squares × (1 + waste %), rounded up to the next bundle
Bundles        = order squares × 3</div>

<h3 id="worked-example">Worked example</h3>
<p>A 60 × 32 ft single-story house in San Antonio with 18-inch eaves, 12-inch rakes and a 6/12 hip roof: plan area is
(60 + 2) × (32 + 3) = 2,170 sq ft. The 6/12 pitch factor is 1.118, so the roof is about 2,426 sq ft, or 24.3 squares.
At 15% waste for a hip roof that is 27.9 squares, rounded up to 84 bundles (28 squares) to order.</p>

<h2 id="pitch-factor">Pitch factor table</h2>
<p>The pitch factor (also called the slope factor or pitch multiplier) converts horizontal area to sloped area. It is the
length of a rafter for every foot of horizontal run. Multiply plan area by the factor for your pitch:</p>
{PITCH_TABLE}
<p>A hip roof and a gable roof over the same footprint with the same pitch have the same area. The hip roof has more
hip and ridge length and more cutting waste, which is why the waste factor goes up, not the area.</p>

<h2 id="sloped-vs-plan">Sloped measurements vs. plan measurements</h2>
<p>In plane-by-plane mode, tell the calculator how your numbers were taken:</p>
<ul>
  <li><strong>On the roof (sloped).</strong> If you pulled a tape from the drip edge up to the ridge, that length already
  includes the slope. No pitch factor is applied; the pitch per plane is used only for reporting.</li>
  <li><strong>From a plan or aerial (horizontal).</strong> Dimensions from house plans, a satellite image or a site plan
  are horizontal. Each plane is multiplied by its own pitch factor.</li>
</ul>
<p>Mixing the two is the most common mistake we see: applying a pitch factor to a tape measurement taken on the roof
overstates the area by the same 5–40% the factor adds.</p>
<p>For a hip roof measured from a plan, the two long sides are trapezoids (eave length, ridge length and the horizontal
distance from wall line to ridge) and the two ends are triangles. The default rows show a 50 × 30 ft hip roof that way.</p>

<h2 id="waste">Choosing a waste factor</h2>
<div class="table-wrap"><table><thead><tr><th>Roof style</th><th>Shingle waste</th><th>Why</th></tr></thead><tbody>
<tr><td>Simple gable</td><td>10%</td><td>Straight cuts at the rakes only</td></tr>
<tr><td>Hip roof</td><td>15%</td><td>Angled cuts on every hip, both sides</td></tr>
<tr><td>Complex / cut-up</td><td>18–20%</td><td>Valleys, dormers, turrets, short runs between features</td></tr>
<tr><td>Metal panels</td><td>5–12%</td><td>Panels are cut to length; waste is mostly at hips and valleys</td></tr>
</tbody></table></div>
<p>Measurement reports from EagleView, Hover and similar services list a suggested waste percentage based on the roof's
geometry. Insurance estimates written in Xactimate show the measured area and the waste-adjusted quantity separately, so
you can check both against this calculator.</p>

<h2 id="texas-notes">Texas notes</h2>
<ul>
  <li><strong>Pitches.</strong> Most Texas homes built since the 1990s are 6/12 to 8/12; newer two-story homes in DFW,
  Austin and Houston suburbs often have 8/12 to 10/12 front gables over a 6/12 main roof. That is exactly where
  plane-by-plane mode pays off.</li>
  <li><strong>Covered patios.</strong> Low-slope patio covers (2/12–3/12) are common and often need a different product.
  Enter them as their own plane so you can price them separately.</li>
  <li><strong>Garages.</strong> County appraisal district square footage usually excludes the garage. Add it back before you
  use the appraisal number as a footprint.</li>
</ul>

<h2 id="using-results">How to use the result</h2>
<p>Take the squares-to-order number to the <a href="/tools/shingle-calculator/">shingle &amp; materials calculator</a>
for starter, ridge cap, underlayment and nails, or to the <a href="/tools/roof-replacement-cost-calculator/">roof
replacement cost calculator</a> for a full installed price. If you are checking an insurance estimate, compare the
measured area (before waste) to the carrier's roof area line; a difference of more than about 3–5% is worth questioning.
Our <a href="/services/insurance-claim-estimate-review/">claim estimate review</a> does that comparison against a
measurement report for you.</p>
"""

faqs = [
    ("How do I calculate the square footage of my roof?",
     "<p>Measure the house footprint, add the overhang on every side, and multiply by the pitch factor for your slope. "
     "A 2,000 sq ft footprint with 18-inch overhangs all around and a 6/12 pitch is about 2,550 sq ft of roof. For roofs with several "
     "pitches, measure each plane separately.</p>"),
    ("How many squares is a 2,000 sq ft house?",
     "<p>For a single-story home, usually 22 to 30 squares. A single-story 2,000 sq ft home with a 6/12 roof and normal overhangs is about 25–26 "
     "squares of roof area, or 28–30 squares to order after waste. A two-story 2,000 sq ft home has a smaller footprint, "
     "so it has a smaller roof, often 12–16 squares.</p>"),
    ("What is a pitch factor?",
     "<p>The ratio between the sloped length of a roof and its horizontal run: √(1 + (rise ÷ 12)²). At 6/12 it is 1.118, "
     "meaning each foot of horizontal run is 1.118 ft of roof. Multiply plan area by the factor to get roof area.</p>"),
    ("Should I include waste in the roof area?",
     "<p>No. Keep the measured area and the waste separate. The measured area is what gets covered; waste is extra "
     "material for cuts. Contractors and insurance estimates order on area plus waste, but labor is priced on the "
     "measured area.</p>"),
    ("Can I measure my roof from Google Maps or a satellite image?",
     "<p>Yes, for a plan-view estimate. Measure the outside edges of the roof (which already include the overhang), enter "
     "the planes as plan dimensions and choose the right pitch for each. Expect satellite measurements to land within "
     "5–10% of a professional measurement report.</p>"),
    ("How many bundles of shingles do I need per square?",
     "<p>Three bundles per square for most architectural and 3-tab shingles. Some heavyweight designer shingles are four "
     "or five bundles per square; check the wrapper and change the number in the ordering assumptions.</p>"),
]

TOOL = {
    "slug": SLUG,
    "title": "Roof Square Footage & Squares Calculator | Roof Estimate Pro",
    "description": "Free roof square footage calculator. Turn a footprint or plane-by-plane measurements into true roof area, squares, waste factor and shingle bundles.",
    "h1": "Roof Square Footage Calculator",
    "lede": "Get true sloped roof area from a house footprint or plane by plane, with pitch factors, overhangs, a waste factor for your roof style and the squares and bundles to order.",
    "form": form,
    "body": body,
    "faqs": faqs,
    "related": ["roof-pitch-calculator", "shingle-calculator", "roof-replacement-cost-calculator"],
}
