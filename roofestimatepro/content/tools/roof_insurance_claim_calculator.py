"""Roof Insurance Claim Calculator — RCV, O&P, tax, depreciation, settlement
type, deductible and prior payments → first check, holdback, out-of-pocket.

Script: static/assets/js/tools/roof-insurance-claim-calculator.js
"""

from content.ui import num, select, seg, switch, group
from siteconfig import MATERIALS
from content.tools.roof_depreciation_calculator import LOW_SLOPE

SLUG = "roof-insurance-claim-calculator"

MAT_OPTS = ([(m["key"], m["name"]) for m in MATERIALS]
            + [(m["key"], m["name"] + " (low slope)") for m in LOW_SLOPE])

# Illustrative roof payment schedule (percent of roof RCV paid by roof age).
# Real schedules vary by carrier, policy form and roof material.
SCHEDULE = [("sch1", "Age 0–2 yrs", 100), ("sch2", "Age 3–5 yrs", 90), ("sch3", "Age 6–8 yrs", 75),
            ("sch4", "Age 9–11 yrs", 60), ("sch5", "Age 12–14 yrs", 45), ("sch6", "Age 15+ yrs", 30)]

form = (
    group("Replacement cost value (RCV)",
          seg("rcv_mode", "How do you want to enter the RCV?",
              [("build", "Build it from squares"), ("direct", "I have the estimate total")], "build"),
          num("rcv_direct", "Line-item total (RCV)", 18000, pre="$", min=0, show="rcv_mode=direct", cls="full",
              help="Total of the line items before sales tax and O&amp;P. If your figure already includes them, switch O&amp;P off and set tax to 0%."),
          num("squares", "Roof size", 30, unit="squares", min=0, show="rcv_mode=build",
              tip="1 square = 100 sq ft of roof surface. Use the measured area, not the footprint."),
          num("rcv_sq", "Roof RCV per square", 425, pre="$", unit="/sq", min=0, show="rcv_mode=build",
              tip="Tear-off, shingles, underlayment, starter, ridge, drip edge, flashing and labor, before tax and O&P.",
              help="About $350–$450/sq for architectural shingles in Texas carrier estimates."),
          num("gutters", "Gutters &amp; downspouts", 1200, pre="$", min=0, show="rcv_mode=build"),
          num("fence", "Fence", 0, pre="$", min=0, show="rcv_mode=build"),
          num("interior", "Interior (ceiling, paint, insulation)", 0, pre="$", min=0, show="rcv_mode=build"),
          num("other", "Other items", 0, pre="$", min=0, show="rcv_mode=build",
              help="Windows, siding, AC fins, screens."),
          ),
    group("Sales tax and overhead &amp; profit",
          num("mat_share", "Share of line items that is materials", 45, unit="%", min=0, max=100,
              help="Roof estimates typically run 40–50% materials."),
          num("tax_rate", "Sales tax rate", 8.25, unit="%", min=0, max=15,
              help="Texas: 6.25% state plus up to 2% local, so 8.25% at most."),
          switch("op", "Include overhead &amp; profit (O&amp;P)", checked=False),
          num("ovh", "Overhead", 10, unit="%", min=0, max=30, show="op=true"),
          num("prf", "Profit", 10, unit="%", min=0, max=30, show="op=true"),
          ),
    group("Depreciation",
          seg("dep_mode", "How is depreciation set?",
              [("age", "From roof age & material"), ("pct", "I know the %")], "age"),
          select("material", "Roofing material", MAT_OPTS, "arch", cls="full", show="dep_mode=age"),
          num("life", "Life expectancy", 30, unit="years", min=1, show="dep_mode=age",
              help="Fills in from the material; edit to match the estimate."),
          num("age", "Roof age at date of loss", 12, unit="years", min=0,
              tip="Also used to pick the percentage on a roof payment schedule."),
          num("dep_pct", "Depreciation", 40, unit="%", min=0, max=100, show="dep_mode=pct",
              help="From the line items of the carrier's estimate."),
          num("cap", "Maximum depreciation", 100, unit="%", min=0, max=100, show="dep_mode=age",
              help="100% = no cap."),
          seg("dep_base", "Depreciation applies to",
              [("all", "All line items (incl. labor)"), ("materials", "Materials only")], "all",
              tip="Whether labor can be depreciated varies by state and policy. Compare both to see the difference."),
          ),
    group("Policy settlement on the roof",
          seg("settle", "How does your policy pay for the roof?",
              [("rcv", "Replacement cost"), ("acv", "ACV only (roof)"), ("schedule", "Roof payment schedule")], "rcv",
              tip="Check the declarations page and endorsements. ACV-roof and payment-schedule endorsements usually apply to the roof only."),
          *[num(k, f"Schedule: {lbl}", val, unit="% of RCV", min=0, max=100, show="settle=schedule")
            for k, lbl, val in SCHEDULE],
          ),
    group("Deductible &amp; prior payments",
          seg("ded_mode", "Deductible type",
              [("pct", "% of Coverage A (dwelling)"), ("flat", "Flat dollar amount")], "pct"),
          num("cov_a", "Coverage A (dwelling limit)", 350000, pre="$", min=0, show="ded_mode=pct",
              help="On the declarations page."),
          num("ded_pct", "Wind/hail deductible", 1, unit="%", min=0, max=15, step="0.5", show="ded_mode=pct",
              help="Often 1–2% in Texas; 5% or more in some coastal policies."),
          num("ded_flat", "Deductible", 2500, pre="$", min=0, show="ded_mode=flat"),
          num("prior", "Prior payments on this claim", 0, pre="$", min=0,
              help="Advances or earlier checks already issued."),
          ),
)


def _sched_rows():
    return "".join(f"<tr><td>{lbl.replace('Age ', '')}</td><td>{val}%</td></tr>" for _, lbl, val in SCHEDULE)


body = f"""
<h2 id="how-it-works">How a roof claim payment is calculated</h2>
<p>Every roof claim follows the same arithmetic, whether the estimate was written by a carrier's desk adjuster, an
independent adjuster or a public adjuster. The calculator walks through it in the order the carrier's estimate
summary does:</p>
<div class="formula">RCV            = line items + sales tax on materials + overhead &amp; profit
ACV            = RCV − depreciation
First payment  = ACV − deductible − prior payments
Holdback       = recoverable depreciation, paid after the work is done
Out-of-pocket  = deductible (+ any non-recoverable depreciation)</div>
<p>Enter the RCV directly from an estimate, or build it from the number of squares and a per-square price plus other
damaged items such as gutters, fence or interior. Then choose how depreciation is set, how your policy settles the roof
and what your deductible is.</p>

<h2 id="rcv-vs-acv">RCV vs. ACV, with a worked example</h2>
<p><strong>Replacement cost value (RCV)</strong> is what it costs today to replace the damaged roof with like kind and
quality. <strong>Actual cash value (ACV)</strong> is RCV minus depreciation for age and condition. Which one you are
ultimately paid depends on the policy.</p>
<p>Take a 12-year-old architectural shingle roof with an RCV of $20,000, a 30-year life and a 1% deductible on a
$300,000 dwelling limit ($3,000):</p>
<ul>
  <li>Depreciation is 12 ÷ 30 = 40%, or $8,000, so the ACV is $12,000.</li>
  <li><strong>Replacement cost policy:</strong> the first check is $12,000 − $3,000 = $9,000. After the roof is replaced,
  the $8,000 holdback is released. The carrier pays $17,000 in all and you pay the $3,000 deductible.</li>
  <li><strong>ACV-only roof:</strong> the $8,000 is not recoverable. The carrier pays $9,000 and you cover $11,000 of
  the replacement.</li>
  <li><strong>Roof payment schedule at 45%:</strong> the carrier pays 45% of $20,000 = $9,000, less the $3,000
  deductible, so $6,000. You cover $14,000.</li>
</ul>
<p>Enter those numbers in the calculator (<em>I have the estimate total</em>, $20,000, tax 0%, O&amp;P off) to check
each result.</p>

<h2 id="depreciation">How depreciation is set</h2>
<p>Carriers use straight-line depreciation: roof age divided by its life expectancy, applied to the line items. The
estimate should show the age, life and percentage on each line. The calculator fills the life from the material
(30 years for architectural shingles, 20 for 3-tab, 50 for standing seam, 22 for TPO), and you can override it, set a
cap, or type the percentage straight from the estimate. To see how age, life and condition move the number year by
year, use the <a href="/tools/roof-depreciation-calculator/">roof depreciation calculator</a>.</p>
<p>Whether labor can be depreciated is argued in many states, and the rules vary by state and policy. The
<em>Materials only</em> option shows what is at stake in dollars. Check your policy's definition of actual cash value
and your state's current rules.</p>

<h2 id="holdback">Why carriers hold back depreciation</h2>
<p>On a replacement cost policy the carrier owes the full replacement cost only once the property is actually replaced.
Until then it owes the ACV. That is why the first check is ACV minus the deductible, and the depreciation is released
when you show the work is done, usually with the contractor's final invoice. The recoverable amount is limited to what
you actually spend, so if the roof is replaced for less than the RCV, the holdback shrinks too. Policies also set a
deadline to complete repairs and claim the holdback; check yours and ask for an extension in writing if the work will
run late.</p>
<p>Some Texas policies cover the roof differently from the rest of the house. An <strong>ACV roof endorsement</strong>
pays the roof at actual cash value only, with no depreciation recovered. A <strong>roof payment schedule</strong> pays a
fixed percentage of the roof's RCV based on its age (and sometimes its material), regardless of the actual depreciation.
These schedules vary by carrier and policy form. The calculator's defaults are illustrative only:</p>
<div class="table-wrap"><table><thead><tr><th>Roof age</th><th>Illustrative % of RCV paid</th></tr></thead>
<tbody>{_sched_rows()}</tbody></table></div>
<p>To use your own schedule, choose <em>Roof payment schedule</em> and replace each percentage with the one in your
policy's schedule for your roof type. Other damaged items (gutters, fence, interior) are still settled at replacement
cost with recoverable depreciation in the calculator, which is typical, but check your endorsement.</p>

<h2 id="texas-prompt-pay">Texas Prompt Payment of Claims Act deadlines</h2>
<p>Texas Insurance Code chapter 542, subchapter B, sets deadlines for most first-party property claims. In general
terms, after the insurer receives notice of a claim it must:</p>
<ul>
  <li><strong>Within 15 days:</strong> acknowledge the claim, begin its investigation and request the items it
  reasonably needs from you.</li>
  <li><strong>Within 15 business days</strong> after receiving all the requested items: accept or reject the claim in
  writing. If it needs more time, it must notify you and explain why, and then it generally has up to 45 more days.</li>
  <li><strong>Within 5 business days</strong> after notifying you that it will pay: pay the claim.</li>
</ul>
<p>Late payment can expose the insurer to statutory interest and attorney's fees, subject to other provisions of the
code. Some insurers and claims follow different rules (TWIA claims, for example, fall under chapter 2210). This is a
general summary, not legal advice; for a specific claim, talk to a licensed public adjuster or a Texas attorney.</p>

<h2 id="deductible">Your deductible, and why a roofer cannot waive it in Texas</h2>
<p>Texas wind and hail deductibles are often a percentage of Coverage A, commonly 1–2%, and 5% or more in some coastal
and TWIA-area policies. On a $350,000 dwelling limit, 1% is $3,500 and 2% is $7,000. Texas Insurance Code chapter 707
prohibits a contractor from paying, waiving, rebating or absorbing the insured's deductible, including through fake
discounts or "advertising" credits. Budget for the deductible as your share of the job.</p>

<h2 id="line-items">Line items carrier estimates commonly miss</h2>
<p>Most underpaid roof claims are not about depreciation. They are about missing or under-measured line items:</p>
<ul>
  <li><strong>Drip edge</strong> at eaves and rakes, required for shingle roofs by the International Residential Code
  adopted by most Texas cities.</li>
  <li><strong>Starter course</strong> and <strong>ridge cap</strong> as their own lines; the waste factor does not
  cover them.</li>
  <li><strong>Steep and high charges</strong> for 7/12 and steeper slopes and for two-story roofs.</li>
  <li><strong>Each layer of tear-off</strong>, ice &amp; water barrier in valleys, step and counter flashing, pipe jacks,
  vents, and detach &amp; reset of satellite dishes and solar.</li>
  <li><strong>Waste</strong> from a measured report, not a guess, and the actual squares (check against EagleView or
  Hover).</li>
  <li><strong>Overhead &amp; profit.</strong> Carriers commonly include 10% + 10% when a general contractor is reasonably
  needed to coordinate the work, which is often the case when three or more trades are involved. The "three-trade" idea
  is an industry rule of thumb, not a statute; it depends on the claim facts and the policy.</li>
  <li><strong>Matching.</strong> If replacement shingles cannot reasonably match the undamaged slopes, ask whether the
  policy requires a uniform appearance. Some states have matching regulations; in Texas it generally turns on the policy
  wording.</li>
</ul>

<h2 id="review">When to get the estimate reviewed</h2>
<p>Get a second set of eyes when the carrier's RCV is well below a contractor's bid or the
<a href="/tools/roof-replacement-cost-calculator/">replacement cost calculator</a>, when the squares do not match a
measurement report, when O&amp;P was left out on a multi-trade loss, or when the age used for depreciation looks wrong.
Our <a href="/services/insurance-claim-estimate-review/">claim estimate review</a> is $50 per claim: <a href="/claim/">send
the carrier's estimate and photos</a> and we compare it line by line and list what is missing, in the format the carrier
uses. This calculator is a planning tool, not a coverage determination; check your policy.</p>
"""

faqs = [
    ("How do I calculate what insurance will pay for my roof?",
     "<p>Start with the replacement cost value (RCV) of the roof, subtract depreciation to get the actual cash value "
     "(ACV), then subtract your deductible and any prior payments. That is the first check. On a replacement cost "
     "policy, the depreciation is paid after the roof is replaced. On an ACV-only roof or a roof payment schedule, it "
     "usually is not.</p>"),
    ("What is recoverable depreciation?",
     "<p>It is the depreciation a replacement cost policy holds back until the work is done. Once you show the roof was "
     "replaced, typically with the final invoice, the carrier releases it, up to what you actually spent and within the "
     "policy's time limit.</p>"),
    ("Is my wind and hail deductible a percentage?",
     "<p>Many Texas policies use a percentage of Coverage A for wind and hail, often 1–2% and 5% or more in some coastal "
     "areas. A 2% deductible on a $350,000 dwelling limit is $7,000. Check the declarations page.</p>"),
    ("Can my roofer pay or waive my deductible in Texas?",
     "<p>No. Texas Insurance Code chapter 707 prohibits contractors from paying, waiving, rebating or absorbing an "
     "insured's deductible, including through disguised discounts. Treat the deductible as your share of the job.</p>"),
    ("When is overhead and profit included on a roof claim?",
     "<p>Carriers commonly include 10% overhead and 10% profit when a general contractor is reasonably needed to "
     "coordinate the work, which is often the case when three or more trades are involved. It depends on the claim "
     "facts and policy; it is not set by a single statute.</p>"),
    ("How long does a Texas insurer have to pay a roof claim?",
     "<p>Under Texas Insurance Code chapter 542, an insurer generally must acknowledge a claim within 15 days of notice, "
     "accept or reject it within 15 business days after receiving the items it requested (with up to 45 more days if it "
     "notifies you why), and pay within 5 business days after accepting. Some claims, such as TWIA claims, follow "
     "different rules.</p>"),
    ("What if my deductible is more than the claim?",
     "<p>If the covered damage is less than your deductible, the carrier would owe nothing on those numbers. Before "
     "deciding what to do, have the damage and estimate checked, since carrier estimates often miss items, and talk to "
     "your agent about how claims affect your policy.</p>"),
    ("Can someone check the carrier's estimate for me?",
     "<p>Yes. Our <a href=\"/services/insurance-claim-estimate-review/\">claim estimate review</a> is $50 per claim. "
     "<a href=\"/claim/\">Upload the carrier's estimate and photos</a> and we list what is missing or under-measured.</p>"),
]

TOOL = {
    "slug": SLUG,
    "title": "Roof Insurance Claim Calculator (RCV, ACV) | Roof Estimate Pro",
    "description": "Free roof insurance claim calculator: RCV, depreciation, O&P, tax and deductible to see your first check, recoverable holdback and out-of-pocket cost.",
    "h1": "Roof Insurance Claim Calculator",
    "lede": "Work out what a roof claim should pay: replacement cost, sales tax and O&P, depreciation, your policy's settlement type and deductible, giving the first check, the recoverable holdback and what you will pay yourself.",
    "form": form,
    "body": body,
    "faqs": faqs,
    "related": ["roof-depreciation-calculator", "roof-replacement-cost-calculator", "roof-square-footage-calculator"],
}
