"""Roof Pitch Calculator — rise/run, degrees, level reading or rafter length to
pitch, angle, grade, multipliers and material/labor class.
Script: static/assets/js/tools/roof-pitch-calculator.js
"""

import math

from content.ui import num, select, seg, group

SLUG = "roof-pitch-calculator"

form = (
    group("What do you know?",
          seg("method", "Find the pitch from",
              [("rise", "Rise & run"), ("angle", "Angle (degrees)"), ("level", "Level reading"), ("rafter", "Rafter & run")],
              "rise"),
          num("rise", "Rise", 6, min=0, show="method=rise",
              tip="Vertical change. For a pitch like 6/12, rise is 6 and run is 12."),
          num("run", "Run", 12, min=0, show="method=rise",
              tip="Horizontal distance for that rise. Use the same unit as the rise."),
          seg("units", "Rise and run are in", [("in", "Inches"), ("ft", "Feet")], "in", show="method=rise"),
          num("angle", "Roof angle", 26.57, unit="°", min=0, max=89, show="method=angle", cls="full",
              help="From a digital angle finder or a phone level app laid on the roof deck or a rafter."),
          num("level_len", "Level length (horizontal)", 24, unit="in", min=0, show="method=level",
              tip="Hold the level horizontal with one end touching the roof or rafter. A 24 in. level is common; any length works."),
          num("level_rise", "Gap at the end of the level", 12, unit="in", min=0, show="method=level",
              tip="Measure straight down (plumb) from the free end of the level to the roof surface."),
          num("raf_len", "Rafter length (sloped)", 16.77, unit="ft", min=0, show="method=rafter",
              tip="Measured along the top of the rafter from the wall plate line to the ridge, not including the overhang."),
          num("raf_run", "Horizontal run of that rafter", 15, unit="ft", min=0, show="method=rafter",
              tip="Usually half the building width, wall to wall, for a gable roof."),
          ),
    group("Optional: rafter length",
          num("calc_run", "Horizontal run to size", 15, unit="ft", min=0,
              help="Half the span for a common rafter. Leave 0 to skip."),
          num("calc_oh", "Overhang (horizontal)", 18, unit="in", min=0,
              help="Eave overhang past the wall, measured level."),
          ),
)

# Pitch chart rows 1/12 .. 18/12
_rows = []
for r in range(1, 19):
    pf = math.sqrt(1 + (r / 12) ** 2)
    hv = math.sqrt(r * r + 288) / 12
    deg = math.degrees(math.atan(r / 12))
    _rows.append(f"<tr><td>{r}/12</td><td>{deg:.2f}°</td><td>{r / 12 * 100:.1f}%</td><td>{pf:.3f}</td><td>{hv:.3f}</td></tr>")
PITCH_CHART = ("<div class=\"table-wrap\"><table><thead><tr><th>Pitch</th><th>Angle</th><th>Grade</th>"
               "<th>Pitch multiplier</th><th>Hip/valley factor</th></tr></thead><tbody>" + "".join(_rows) + "</tbody></table></div>")

body = f"""
<h2 id="how-it-works">How roof pitch is expressed</h2>
<p>Roof pitch is the vertical rise of a roof for every 12 inches of horizontal run. A 6/12 roof (said "six in twelve")
rises 6 inches for each foot it runs in from the wall. The same slope can be written three other ways, and this
calculator converts between all of them:</p>
<ul>
  <li><strong>Angle in degrees</strong>, from a digital angle finder or phone app. 6/12 is 26.57°.</li>
  <li><strong>Percent grade</strong>, rise ÷ run × 100. 6/12 is 50%. Common on commercial and low-slope drawings.</li>
  <li><strong>Pitch multiplier</strong> (slope factor), the sloped length per foot of run. 6/12 is 1.118, meaning the roof
  surface is 11.8% bigger than its footprint.</li>
</ul>
<p>Strictly, <em>pitch</em> once meant rise over the full span, and <em>slope</em> meant rise over run. In everyday
roofing, estimating and insurance work, "pitch" means rise per 12 of run, and that is what this tool uses.</p>
<div class="formula">Pitch (x/12)      = rise ÷ run × 12
Angle (°)         = arctan(rise ÷ run)          Rise per 12 = 12 × tan(angle)
Percent grade     = rise ÷ run × 100
Pitch multiplier  = √(1 + (x ÷ 12)²)
Hip/valley factor = √(x² + 288) ÷ 12             (regular hip, both sides same pitch)
Common rafter     = run × pitch multiplier
Hip/valley rafter = run of the common rafter × hip/valley factor</div>
<p>From a level reading: an 8-inch gap under the end of a 24-inch level is 8 ÷ 24 × 12 = 4/12. From a rafter: a 16.77 ft
rafter over a 15 ft run rises √(16.77² − 15²) = 7.5 ft, which is 7.5 ÷ 15 × 12 = 6/12.</p>

<h2 id="pitch-chart">Roof pitch chart</h2>
{PITCH_CHART}
<p>The hip/valley factor applies to a hip or valley where the two roof planes have the same pitch. It gives the length
of the hip or valley per foot of the common rafter's run, which is how estimators get hip, ridge and valley footage for
ridge cap and valley metal.</p>

<h2 id="measure-safely">How to measure roof pitch safely</h2>
<p>You do not need to climb on the roof.</p>
<ol>
  <li><strong>From the attic.</strong> Hold a level horizontally against the bottom edge of a rafter with one end touching
  it. Measure plumb from the 12-inch mark on the level up to the rafter. That number is the rise per 12. Use the
  <em>level reading</em> method above for any other level length.</li>
  <li><strong>At the rake from a ladder.</strong> On a gable end, hold the level against the fascia or rake board and do
  the same thing. Keep the ladder at a 4:1 angle and three points of contact.</li>
  <li><strong>With a phone.</strong> Most phones have a level in the built-in measure app. Lay the phone on a rafter in
  the attic, on the rake board, or on a straightedge held to the roof line, and read the angle. Enter it under
  <em>Angle</em>. Phone readings are typically within about a degree, close enough to pick the right whole pitch.</li>
  <li><strong>From the ground.</strong> Photograph the gable end straight on and measure rise and run on the photo. It is
  rough, but good enough to tell a 6/12 from a 9/12.</li>
</ol>
<p>Measurement reports from EagleView, Hover and similar services list the pitch of every facet, which is the best source
for an estimate or an insurance claim.</p>

<h2 id="materials-labor">What your pitch means for materials and labor</h2>
<div class="table-wrap"><table><thead><tr><th>Pitch</th><th>Class</th><th>Suitable roofing</th><th>Labor</th></tr></thead><tbody>
<tr><td>Under 2/12</td><td>Low slope</td><td>Membranes: TPO, PVC, EPDM, modified bitumen, built-up, coatings (minimum 1/4:12 for drainage)</td><td>Walkable</td></tr>
<tr><td>2/12 – under 4/12</td><td>Shingle minimum</td><td>Asphalt shingles only with double underlayment; standing seam; tile from 2.5/12 with double underlayment</td><td>Walkable</td></tr>
<tr><td>4/12 – 6/12</td><td>Conventional</td><td>All steep-slope products with standard underlayment</td><td>Walkable, no steep charge</td></tr>
<tr><td>7/12 – 9/12</td><td>Steep</td><td>All steep-slope products</td><td>Steep charge; roof jacks and harnesses</td></tr>
<tr><td>10/12 – 12/12</td><td>Very steep</td><td>All steep-slope products</td><td>Higher steep charge</td></tr>
<tr><td>Over 12/12</td><td>Extreme / mansard</td><td>Shingles need extra nails per the manufacturer</td><td>Highest steep charge</td></tr>
</tbody></table></div>
<p>Minimum slopes for metal depend on the panel: mechanically seamed standing seam can go as low as 1/4:12 to 1/2:12,
many snap-lock standing seam panels are rated by their manufacturer for 3/12 or steeper, and lapped exposed-fastener panels
need 3/12 under the residential code (1/2:12 with applied lap sealant). Always follow the panel manufacturer and local code.</p>
<p>Insurance estimates in Xactimate add steep-roof labor as separate line items, starting at 7/12 and stepping up at
10/12 and above 12/12. If your roof is 7/12 or steeper and the carrier's estimate has no steep charge, ask why. Our
<a href="/services/insurance-claim-estimate-review/">claim estimate review</a> checks that line along with the rest.</p>

<h2 id="texas-pitches">Common roof pitches in Texas</h2>
<p>Ranch homes from the 1960s–1980s across Texas are often 4/12 to 6/12. Most tract homes built in DFW, Houston, Austin and
San Antonio suburbs since the 1990s have 6/12 to 8/12 main roofs, with 8/12 to 12/12 front gables on two-story homes.
Hill Country and custom homes push 10/12 and up. Low-slope 1/12 to 3/12 patio covers and porches tied into the main roof
are common everywhere and often need a different product than the main roof.</p>

<h2 id="using-results">How to use the result</h2>
<p>Take the pitch multiplier to the <a href="/tools/roof-square-footage-calculator/">roof square footage calculator</a> to
turn a footprint into roof area, then to the <a href="/tools/roof-replacement-cost-calculator/">roof replacement cost
calculator</a>, which adds steep labor automatically. The rafter length here is the line length from the wall to the
ridge plus the overhang; it does not deduct half the ridge board, so framers should subtract that before cutting.</p>
"""

faqs = [
    ("What is the most common roof pitch?",
     "<p>On homes in Texas and most of the U.S., 6/12 is the most common, with 4/12 to 9/12 covering the large majority of "
     "houses. Newer two-story homes often mix a 6/12 main roof with steeper 8/12 to 12/12 front gables.</p>"),
    ("How do I convert roof pitch to degrees?",
     "<p>Divide the rise by 12 and take the arctangent: angle = arctan(rise ÷ 12). A 4/12 roof is 18.43°, 6/12 is 26.57°, "
     "8/12 is 33.69° and 12/12 is 45°.</p>"),
    ("What pitch is too low for shingles?",
     "<p>Asphalt shingles need at least 2/12. From 2/12 up to 4/12, code requires two layers of underlayment. Below 2/12, "
     "use a low-slope membrane such as TPO, EPDM or modified bitumen.</p>"),
    ("What is a pitch multiplier?",
     "<p>The ratio of sloped length to horizontal run, √(1 + (pitch ÷ 12)²). Multiply plan area by it to get roof area, or "
     "multiply a run by it to get the common rafter length. A 6/12 multiplier is 1.118; 12/12 is 1.414.</p>"),
    ("At what pitch is a roof considered steep?",
     "<p>For labor and safety, 7/12 and up. Above 6/12 most crews need roof jacks or harnesses, and insurance estimates "
     "add steep-roof charges at 7/12–9/12, 10/12–12/12 and over 12/12.</p>"),
    ("Can I find my roof pitch from the ground?",
     "<p>Roughly. A straight-on photo of a gable end lets you measure rise and run on the image. For an exact number, "
     "use a level and tape on a rafter in the attic or a phone level app, or get a measurement report.</p>"),
]

TOOL = {
    "slug": SLUG,
    "title": "Roof Pitch Calculator: Degrees, Multiplier | Roof Estimate Pro",
    "description": "Free roof pitch calculator. Convert rise and run, degrees or a level reading to x/12 pitch, angle, grade, pitch multiplier, hip/valley factor and rafters.",
    "h1": "Roof Pitch Calculator",
    "lede": "Find your roof pitch from rise and run, an angle, a level reading or a rafter, and get the angle, percent grade, pitch multiplier, hip/valley factor, rafter length and what the slope means for materials and labor.",
    "form": form,
    "body": body,
    "faqs": faqs,
    "related": ["roof-square-footage-calculator", "shingle-calculator", "metal-roof-calculator"],
}
