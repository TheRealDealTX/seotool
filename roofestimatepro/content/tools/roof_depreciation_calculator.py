"""Roof Depreciation Calculator — straight-line depreciation by material, age
and condition, with a year-by-year ACV schedule and chart.

Script: static/assets/js/tools/roof-depreciation-calculator.js
"""

from content.ui import num, select, seg, group
from siteconfig import MATERIALS

SLUG = "roof-depreciation-calculator"

# Low-slope systems (shared brief): service-life range and installed $/sf range.
# "life" is the midpoint used as the default; JS keeps the same table.
LOW_SLOPE = [
    {"key": "tpo", "name": "TPO membrane (60-mil)", "life": 22, "lives": "20–25", "sf": [7.00, 10.00]},
    {"key": "pvc", "name": "PVC membrane (60-mil)", "life": 27, "lives": "25–30", "sf": [9.00, 13.00]},
    {"key": "epdm", "name": "EPDM membrane (60-mil)", "life": 27, "lives": "25–30", "sf": [7.00, 10.50]},
    {"key": "modbit", "name": "Modified bitumen (2-ply)", "life": 17, "lives": "15–20", "sf": [7.50, 11.00]},
    {"key": "bur", "name": "Built-up roof (BUR)", "life": 25, "lives": "20–30", "sf": [7.50, 11.50]},
    {"key": "silicone", "name": "Silicone roof coating", "life": 12, "lives": "10–15", "sf": [3.50, 6.00]},
    {"key": "acrylic", "name": "Acrylic roof coating", "life": 10, "lives": "8–12", "sf": [2.75, 5.00]},
]

MAT_OPTS = ([(m["key"], m["name"]) for m in MATERIALS]
            + [(m["key"], m["name"] + " (low slope)") for m in LOW_SLOPE])

form = (
    group("Roof material & age",
          select("material", "Roofing material", MAT_OPTS, "arch", cls="full"),
          num("life", "Life expectancy", 30, unit="years", min=1, max=100,
              tip="Fills in from the material. Change it to match the life your carrier's estimate or the manufacturer uses.",
              help="Auto-filled for the material; edit to match the carrier's estimate."),
          num("age_y", "Roof age", 12, unit="years", min=0, step=1),
          num("age_m", "Plus months", 0, unit="months", min=0, max=11, step=1),
          seg("condition", "Condition before the loss",
              [("good", "Well maintained"), ("average", "Average"), ("poor", "Poor / neglected")], "average",
              tip="Adjusters may lengthen or shorten the effective life for condition. Well maintained = less depreciation."),
          num("cond_adj", "Life adjustment for condition", 0, unit="%", min=-50, max=50,
              help="Auto-set to +10% (well maintained), 0% (average) or −15% (poor). Positive lengthens the life and lowers depreciation."),
          ),
    group("Replacement cost (optional)",
          seg("rcv_mode", "Replacement cost value (RCV)",
              [("squares", "Squares × price"), ("dollars", "I know the RCV"), ("none", "Percent only")], "squares"),
          num("squares", "Roof size", 30, unit="squares", min=0, show="rcv_mode=squares",
              tip="1 square = 100 sq ft of roof surface."),
          num("rcv_sq", "Replacement cost", 550, pre="$", unit="/sq", min=0, show="rcv_mode=squares",
              help="Fills in with the Texas 2026 installed midpoint for the material; replace it with your estimate's figure."),
          num("rcv", "RCV of the roof", 16500, pre="$", min=0, show="rcv_mode=dollars",
              help="From the carrier's estimate or your contractor's replacement bid."),
          num("cap", "Maximum depreciation", 100, unit="%", min=0, max=100,
              tip="Leave at 100% for no cap. Some estimates or policies limit depreciation; enter that limit here."),
          ),
)


def _life_table():
    rows = []
    for m in MATERIALS:
        rows.append(f"<tr><td>{m['name']}</td><td>{m['life']} yrs</td><td>{100 / m['life']:.1f}%</td></tr>")
    for m in LOW_SLOPE:
        rows.append(f"<tr><td>{m['name']}</td><td>{m['lives']} yrs (calculator uses {m['life']})</td>"
                    f"<td>{100 / m['life']:.1f}%</td></tr>")
    return ("<div class=\"table-wrap\"><table><thead><tr><th>Roofing system</th><th>Typical life</th>"
            "<th>Straight-line per year</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table></div>")


body = f"""
<h2 id="straight-line">How roof depreciation is calculated</h2>
<p>Insurance carriers and adjusters almost always depreciate a roof on a <strong>straight line</strong>: the roof loses
the same share of its value every year of its expected life. Divide the roof's age by its life expectancy and you have
the depreciation percentage. Multiply that by the replacement cost value (RCV) and you have the dollars withheld. What is
left is the actual cash value (ACV).</p>
<div class="formula">Depreciation %  = age ÷ (life expectancy × (1 + condition adjustment))   capped at the max %
Depreciation $  = RCV × depreciation %
ACV             = RCV − depreciation $
Remaining life  = effective life − age</div>
<p><strong>Worked example.</strong> A 12-year-old architectural shingle roof with a 30-year life is 12 ÷ 30 = 40%
depreciated. If replacing it costs $16,500 (30 squares at $550), depreciation is $6,600 and the ACV is $9,900. If the
adjuster agrees the roof was well maintained and uses a 10% longer effective life (33 years), depreciation drops to
36.4%, or $6,000, and the ACV rises to $10,500. That is the calculator's default setup; change any input to match your
roof.</p>
<p>Two details matter more than people expect. First, <strong>age is measured to the date of loss</strong>, not the
date of the inspection or the estimate. Second, the life expectancy is a choice the estimator makes. In Xactimate the
estimator sets the age and life on each line item, so two adjusters can depreciate the same roof very differently.</p>

<h2 id="life-expectancy">Roof life expectancy by material</h2>
<p>These are the default lives the calculator uses. Steep-slope figures match the ones used across our tools; low-slope
figures use the midpoint of the typical range. Your carrier's estimate may use different numbers, and you can edit the
life field to match.</p>
{_life_table()}
<p>Coatings are a special case. A silicone or acrylic coating is designed to be renewed, so a 12-year-old coating is
not necessarily at the end of its useful life if it was recoated on schedule. Bring the recoat records if a carrier
depreciates a coated roof as if it were original.</p>

<h2 id="how-adjusters-apply">How adjusters apply age and condition</h2>
<p>Most carrier estimates apply one depreciation percentage to the roofing line items: tear-off, shingles or membrane,
underlayment, starter, ridge cap and flashings. Some items are often treated differently. Disposal, permits and some
labor-only items may carry no depreciation in some estimates, and newer components (a ridge vent replaced three years
ago, new pipe boots) should carry their own age, not the age of the original roof.</p>
<p>Condition is where adjusters have the most discretion. A roof with granule loss, curled tabs, prior repairs or poor
ventilation can be given a shorter effective life, which raises depreciation. A roof with maintenance records and no
pre-existing wear can justify a longer one. The calculator expresses this as a percentage change to the life: +10% for a
well-maintained roof, −15% for a neglected one, and 0% for average. Those are starting points, not rules; type your
own adjustment if the estimate shows a different effective life.</p>
<p>Many estimates also set a <strong>maximum depreciation</strong>, so a roof past its expected life still keeps some
value. Whether a cap applies, and at what level, depends on the carrier and the estimate. Enter it in the
<em>Maximum depreciation</em> field to see its effect; at 100% there is no cap.</p>

<h2 id="dispute">Disputing excessive depreciation</h2>
<p>Depreciation is an estimate, not a fixed fact, and it can be questioned with evidence. Start with the line items:
the carrier's estimate should show the age, life and depreciation percentage it used. Then gather what supports a lower
number:</p>
<ul>
  <li><strong>Proof of age.</strong> The permit record, the installation invoice or the closing documents from when you
  bought the home. A roof the estimate calls 18 years old that was replaced 11 years ago is worth correcting.</li>
  <li><strong>Maintenance records.</strong> Inspections, repair invoices, gutter cleaning and recoats show the roof was
  cared for and support a longer effective life.</li>
  <li><strong>Manufacturer data.</strong> The product line, its rated life and its warranty terms. A designer shingle
  or a Class 4 product often carries a longer published life than the generic figure in an estimate.</li>
  <li><strong>Pre-loss photos.</strong> Listing photos, drone shots or inspection reports showing the roof's condition
  before the storm counter claims of pre-existing wear.</li>
</ul>
<p>Put the request in writing, attach the documents and ask the adjuster to revise the age, life or condition used.
If you are a public adjuster or contractor handling the claim, a line-item comparison makes the conversation shorter.
Our <a href="/services/insurance-claim-estimate-review/">claim estimate review</a> checks depreciation along with the
missing line items for $50; <a href="/claim/">send the carrier's estimate and photos</a> and we will tell you what we
would change.</p>

<h2 id="labor-depreciation">Should labor be depreciated?</h2>
<p>This is one of the most argued points in property claims. The case against depreciating labor is that labor does not
wear out; only the shingles do. The case for it is that ACV is meant to reflect the value of the roof as it stood, and
the installed roof includes the labor that put it there. Courts and regulators in different states have come down on
different sides, some states restrict labor depreciation by statute or regulation, and some policies address it
directly in their definition of actual cash value.</p>
<p>Because the rules vary by state and by policy wording, check your policy's ACV definition and your state's current
rules, or ask a licensed public adjuster or attorney, before assuming either way. To see what is at stake, run the
<a href="/tools/roof-insurance-claim-calculator/">roof insurance claim calculator</a> with depreciation on all line
items and then on materials only; the difference is the labor depreciation in dollars.</p>

<div class="callout callout--peach"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
<p><strong>Depreciation is often money you get back.</strong> On a replacement cost policy, depreciation is usually
withheld from the first check and paid after the roof is replaced, up to what you actually spend. On an ACV-only roof
or a roof payment schedule, it usually is not. Check your declarations page and endorsements to see which applies to
your roof.</p></div>

<h2 id="using-the-schedule">Reading the year-by-year schedule</h2>
<p>The table and chart show how the ACV falls each year of the roof's effective life, with a marker at today's age. Use
it to see what a claim would pay at different ages, to check a carrier's figure, or to explain to a homeowner why an
older roof gets a smaller first check. Pair it with the
<a href="/tools/roof-replacement-cost-calculator/">roof replacement cost calculator</a> if you need a starting RCV.</p>
"""

faqs = [
    ("How do insurance companies calculate roof depreciation?",
     "<p>Usually on a straight line: roof age divided by life expectancy, applied to the replacement cost. A 10-year-old "
     "roof with a 30-year life is 33.3% depreciated. The adjuster may adjust the life for condition and may cap the "
     "maximum depreciation. The age, life and percentage should appear on the line items of the estimate.</p>"),
    ("What is the life expectancy of an asphalt shingle roof for insurance?",
     "<p>Estimates commonly use about 20 years for 3-tab shingles and 25–30 years for architectural shingles, with "
     "longer lives for designer and some impact-resistant lines. This calculator defaults to 20 and 30 years; edit the "
     "life to match the carrier's estimate or the manufacturer's data.</p>"),
    ("Is roof depreciation recoverable?",
     "<p>On a replacement cost policy, depreciation is usually recoverable: the carrier holds it back and pays it after "
     "the work is done, up to what you actually spend and within the policy's time limit. If your roof is covered at "
     "actual cash value or under a roof payment schedule, the withheld amount is usually not recoverable. Check your "
     "declarations page and endorsements.</p>"),
    ("Can a roof be 100% depreciated?",
     "<p>If no cap applies, a roof at or past its life expectancy reaches 100% on a straight line, so the ACV is zero. "
     "Many estimates limit depreciation so an old but functioning roof keeps some value. Set the cap in the calculator "
     "to see the effect of a limit used in your estimate.</p>"),
    ("Does good maintenance reduce depreciation?",
     "<p>It can. Adjusters have discretion on condition, and records of inspections, repairs and recoats support a longer "
     "effective life. In the calculator, a well-maintained roof lengthens the life by 10% by default, which lowers the "
     "depreciation percentage.</p>"),
    ("Should labor be depreciated on a roof claim?",
     "<p>It depends on your state and your policy. Some states restrict depreciating labor and some policies define "
     "actual cash value in a way that includes it. Check your policy and your state's current rules, or ask a licensed "
     "public adjuster or attorney.</p>"),
    ("What if the carrier used the wrong roof age?",
     "<p>Send proof of the installation date, such as the permit, invoice or closing documents, and ask for the age and "
     "depreciation to be revised. Age is measured to the date of loss. Our $50 "
     "<a href=\"/services/insurance-claim-estimate-review/\">claim estimate review</a> flags age and depreciation errors "
     "along with missing line items.</p>"),
]

TOOL = {
    "slug": SLUG,
    "title": "Roof Depreciation Calculator (ACV by Age) | Roof Estimate Pro",
    "description": "Free roof depreciation calculator: straight-line depreciation by material, age and condition, actual cash value and a year-by-year ACV schedule.",
    "h1": "Roof Depreciation Calculator",
    "lede": "See how much an insurance carrier is likely to depreciate your roof: straight-line depreciation from material life, age and condition, the actual cash value, remaining life and a year-by-year ACV schedule.",
    "form": form,
    "body": body,
    "faqs": faqs,
    "related": ["roof-insurance-claim-calculator", "roof-replacement-cost-calculator", "roof-repair-cost-calculator"],
}
