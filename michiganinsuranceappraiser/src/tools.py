"""Free claim tools for Michigan Insurance Appraiser. Markup only; the math lives in static/assets/js/app.js.
Every tool runs in the browser. Nothing typed into a tool is sent anywhere or stored."""


def _f(name, label, value="", unit="", hint="", kind="money", attrs=""):
    """A labelled numeric input. kind: money | num | pct."""
    pre = '<span class="affix">$</span>' if kind == "money" else ""
    post = f'<span class="affix">{unit}</span>' if unit else ""
    h = f'<small class="hint">{hint}</small>' if hint else ""
    return (f'<div class="fld"><label for="{{u}}-{name}">{label}</label><div class="inp">{pre}'
            f'<input id="{{u}}-{name}" name="{name}" inputmode="decimal" value="{value}"{attrs}>{post}</div>{h}</div>')


def _out(key, label, big=False, val="$0"):
    return f'<div class="res{" res-big" if big else ""}"><span>{label}</span><b data-o="{key}">{val}</b></div>'


GAP_FULL = ("""
<div class="tool" data-tool="gap">
<div class="tool-grid">
<fieldset class="tool-in"><legend class="tool-h">Your claim figures</legend>
""" + _f("insurer", "Carrier’s estimate (RCV)", "18500") + _f("yours", "Your contractor or appraiser estimate", "31200") + """
<div class="fld"><label for="{u}-land">Where might an award land inside the gap?</label><div class="range"><input id="{u}-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div><small class="hint">0% = the carrier’s number, 100% = yours. Purely a planning assumption.</small></div>
<div class="fld"><label for="{u}-feetype">Appraiser fee arrangement</label><select id="{u}-feetype" name="feetype"><option value="pct">Percentage of the increase</option><option value="flat">Flat fee</option><option value="hourly">Hourly</option></select></div>
""" + _f("fee", "Fee amount (%, $ or hourly rate)", "12", hint="Enter a percent, a flat dollar fee, or an hourly rate.", kind="num") + _f("rate", "Hours (hourly only)", "20", kind="num") + """
<div class="fld chk"><label class="check"><input type="checkbox" name="useump" checked> <span>Include a half share of an umpire’s fee</span></label></div>
""" + _f("umpire", "Total umpire fee", "3000") + """
</fieldset>
<div class="tool-out" aria-live="polite"><p class="tool-h">What the numbers say</p>
""" + _out("gap", "Disputed amount") + _out("pct", "Gap vs. carrier estimate", val="—") + _out("award", "Illustrative award") + _out("gain", "Increase over the carrier") + _out("cost", "Estimated appraisal cost") + _out("net", "Illustrative net gain", True) + _out("breakeven", "Break-even point", val="—") + """
<div class="stack" aria-hidden="true"><i class="s-ins"></i><i class="s-net"></i><i class="s-cost"></i></div>
<ul class="legend" aria-hidden="true"><li><i class="s-ins"></i>Carrier</li><li><i class="s-net"></i>Your net increase</li><li><i class="s-cost"></i>Costs</li></ul>
<p class="tool-msg" data-o="msg"></p>
</div></div></div>""")

GAP_MINI = ("""
<div class="tool tool-mini" data-tool="gap">
<div class="mini-row">
""" + _f("insurer", "Carrier’s estimate", "14800") + _f("yours", "Your estimate", "26500") + """
<div class="fld"><label for="{u}-land">Award lands at</label><div class="range"><input id="{u}-land" type="range" name="land" min="0" max="100" step="5" value="50" data-unit="%"><output>50%</output></div></div>
</div>
<div class="mini-res" aria-live="polite">""" + _out("gap", "Disputed amount") + _out("award", "Illustrative award") + _out("gain", "Increase", True) + """</div>
<p class="tool-msg" data-o="msg"></p>
</div>""")

_DEP_ROW = ('<tr><td><input name="item" value="{0}" aria-label="Item"></td>'
            '<td><input name="rcv" inputmode="decimal" value="{1}" aria-label="Replacement cost"></td>'
            '<td><input name="age" inputmode="decimal" value="{2}" aria-label="Age in years"></td>'
            '<td><input name="life" inputmode="decimal" value="{3}" aria-label="Expected life in years"></td>'
            '<td class="mono" data-o="row">$0</td><td><button type="button" class="x" aria-label="Remove row">×</button></td></tr>')

DEP = ("""
<div class="tool" data-tool="dep">
<p class="tool-h">Line items</p>
<div class="tbl-wrap"><table class="dep-tbl"><thead><tr><th scope="col">Item</th><th scope="col">Replacement cost ($)</th><th scope="col">Age (yrs)</th><th scope="col">Life (yrs)</th><th scope="col">ACV</th><th scope="col"><span class="sr">Remove</span></th></tr></thead><tbody>
""" + _DEP_ROW.format("Architectural shingle roof", "16400", "11", "25") + _DEP_ROW.format("Basement carpet &amp; pad", "3900", "6", "10")
       + _DEP_ROW.format("Drywall &amp; paint", "5200", "0", "50") + """
</tbody></table></div>
<button type="button" class="btn btn-sm btn-line" data-add>+ Add a line</button>
<div class="tool-grid">
<fieldset class="tool-in"><legend class="tool-h">Policy terms</legend>
""" + _f("cap", "Maximum depreciation per item", "80", "%", kind="pct") + _f("deduct", "Deductible", "1000") + _f("paid", "Already paid by the carrier", "0") + _f("window", "Days allowed to finish repairs and claim holdback", "180", "days", "Check your policy and the carrier’s letter; periods vary.", kind="num") + """
<div class="fld chk"><label class="check"><input type="checkbox" name="nonrec"> <span>Policy pays ACV only (depreciation not recoverable)</span></label></div>
</fieldset>
<div class="tool-out" aria-live="polite"><p class="tool-h">Payment picture</p>
""" + _out("rcv", "Replacement cost (RCV)") + _out("dep", "Depreciation withheld") + _out("deppct", "Depreciation as % of RCV", val="0%") + _out("acv", "Actual cash value (ACV)") + _out("first", "First check (ACV − deductible − paid)", True) + _out("held", "Holdback still to recover") + _out("total", "Total if repairs are completed") + _out("by", "Holdback request target date", val="—") + """
</div></div></div>""")

ROOF = ("""
<div class="tool" data-tool="roof">
<div class="tool-grid">
<fieldset class="tool-in"><legend class="tool-h">Roof footprint</legend>
<div class="seg" role="radiogroup" aria-label="Measurement method"><label><input type="radio" name="mode" value="dims" checked> <span>Length × width</span></label><label><input type="radio" name="mode" value="area"> <span>Known area</span></label></div>
<div data-mode="dims">""" + _f("len", "Building length", "52", "ft", kind="num") + _f("wid", "Building width", "30", "ft", kind="num") + _f("oh", "Eave &amp; rake overhang", "12", "in", kind="num") + """</div>
<div data-mode="area" hidden>""" + _f("area", "Flat footprint area", "1700", "sq ft", kind="num") + """</div>
<div class="fld"><label for="{u}-pitch">Roof pitch (rise per 12 in of run)</label><select id="{u}-pitch" name="pitch">""" + "".join(
    f'<option value="{p}"{" selected" if p == 6 else ""}>{p}/12</option>' for p in range(2, 17)) + """</select></div>
""" + _f("waste", "Waste factor", "12", "%", "Hip roofs and many valleys need more.", kind="pct") + _f("eave", "Total eave length (gutter edges)", "104", "ft", "Used for the ice-barrier estimate below.", kind="num") + _f("bar", "Ice barrier must reach inside the wall line", "24", "in", kind="num") + _f("est", "Squares in the carrier’s estimate (optional)", "", "sq", kind="num") + """
</fieldset>
<div class="tool-out" aria-live="polite"><p class="tool-h">Results</p>
""" + _out("mult", "Pitch multiplier", val="1.000") + _out("surface", "Roof surface area", val="0 sq ft") + _out("sq", "Squares (no waste)", val="0.00") + _out("order", "Squares with waste (rounded to ⅓)", True, "0.00") + _out("bundles", "Shingle bundles (3 per square)", val="0") + _out("ice", "Ice-barrier rows &amp; area", val="—") + _out("vs", "Difference from carrier", val="—") + """
<p class="tool-msg" data-o="steep"></p>
</div></div></div>""")

DEDUCT = ("""
<div class="tool" data-tool="deduct">
<div class="tool-grid">
<fieldset class="tool-in"><legend class="tool-h">Your deductible</legend>
""" + _f("cova", "Coverage A (dwelling limit)", "340000") + _f("pct", "Percentage deductible", "1", "%", "Shown on your declarations page, e.g. 1% or 2% of Coverage A.", kind="pct") + _f("flat", "Flat deductible it replaced (for comparison)", "1000") + _f("loss", "Estimated covered loss", "21000") + """
<div class="fld chk"><label class="check"><input type="checkbox" name="trig" checked> <span>The percentage deductible applies to this loss (for example, a wind/hail deductible and the loss was wind or hail)</span></label></div>
</fieldset>
<div class="tool-out" aria-live="polite"><p class="tool-h">Side by side</p>
""" + _out("pd", "Deductible that applies", True) + _out("pctd", "Percentage deductible in dollars") + _out("pdpay", "Payment under the percentage deductible") + _out("flatpay", "Payment under the flat deductible") + _out("diff", "Extra out of pocket") + """
<div class="stack" aria-hidden="true"><i class="s-cost"></i><i class="s-net"></i></div>
<ul class="legend" aria-hidden="true"><li><i class="s-cost"></i>You pay</li><li><i class="s-net"></i>Carrier pays</li></ul>
<p class="tool-msg" data-o="below"></p>
</div></div></div>""")

DATES = """
<div class="tool" data-tool="dates">
<div class="tool-grid">
<fieldset class="tool-in"><legend class="tool-h">Your dates</legend>
<div class="fld"><label for="{u}-dol">Date of loss</label><div class="inp"><input id="{u}-dol" name="dol" type="date"></div></div>
<div class="fld"><label for="{u}-ntc">Date you reported the claim (optional)</label><div class="inp"><input id="{u}-ntc" name="ntc" type="date"></div><small class="hint">Used for the tolling estimate below.</small></div>
<div class="fld"><label for="{u}-den">Date of a formal written denial, if any (optional)</label><div class="inp"><input id="{u}-den" name="den" type="date"></div></div>
<div class="fld"><label for="{u}-rcd">Days your policy allows to claim holdback</label><div class="inp"><input id="{u}-rcd" name="rcd" inputmode="decimal" value="180"><span class="affix">days</span></div></div>
<div class="fld"><label for="{u}-inv">Personal target for the contents inventory</label><div class="inp"><input id="{u}-inv" name="inv" inputmode="decimal" value="45"><span class="affix">days</span></div></div>
<div class="fld chk"><label class="check"><input type="checkbox" name="remind" checked> <span>Add a reminder two weeks before each date</span></label></div>
</fieldset>
<div class="tool-out"><p class="tool-h">Your claim calendar</p>
<ol class="cal" data-o="timeline" aria-live="polite"><li><b>Pick your date of loss</b><span>Your milestones will appear here.</span></li></ol>
<button type="button" class="btn btn-blue btn-block" data-ics>Download calendar (.ics)</button>
<p class="hint">The suit-limitation date is a rough planning estimate of the general Michigan rule, not legal advice. Confirm every deadline with a Michigan attorney.</p>
</div></div></div>"""

_QUIZ = [
    (3, "The carrier has accepted the claim and the fight is about the amount, not coverage.", "Confirm in writing that coverage is accepted. Coverage denials usually need an attorney, not appraisal."),
    (2, "You have the carrier’s complete, line-item estimate (not just a payment letter).", "Ask the adjuster for the full estimate with every line item and the price list date."),
    (2, "You have your own detailed estimate from a contractor or estimator.", "Get an independent line-item estimate for the same scope."),
    (2, "You’ve photographed the damage, with wide shots and close-ups, dated.", "Photograph every affected room and roof slope before more repairs happen."),
    (1, "You’ve kept receipts for tarps, drying, board-up and other emergency work.", "Gather receipts and invoices for all mitigation and emergency repairs."),
    (2, "You’ve read the appraisal condition in your own policy.", "Find the Appraisal paragraph in your policy and note its deadlines."),
    (2, "You know your claim and suit-limitation dates.", "Use the claim deadline planner and speak with a Michigan attorney about timing."),
    (1, "The disputed amount is meaningful compared with the likely costs of appraisal.", "Run the claim gap and fee estimator before you demand appraisal."),
    (1, "You have the declarations page showing limits and deductibles.", "Download or request your current declarations page."),
    (1, "Your contents list (if any) includes ages and replacement prices.", "Build a room-by-room contents inventory with ages and prices."),
]

READY = """
<div class="tool" data-tool="ready">
<div class="tool-grid">
<div class="tool-in"><p class="tool-h">Ten quick questions</p>
<ol class="quiz">""" + "".join(
    f'<li data-w="{w}" data-fix="{fix}"><span class="q">{q}</span><span class="yn"><button type="button" class="yes" aria-pressed="false">Yes</button><button type="button" class="no" aria-pressed="false">No</button></span></li>'
    for w, q, fix in _QUIZ) + """</ol>
<button type="button" class="btn btn-sm btn-line" data-reset>Start over</button>
</div>
<div class="tool-out" aria-live="polite"><p class="tool-h">Your readiness</p>
<div class="gauge"><svg viewBox="0 0 100 100" width="150" height="150" aria-hidden="true"><circle cx="50" cy="50" r="40" class="g-bg"/><circle cx="50" cy="50" r="40" class="g-arc" data-o="arc" style="stroke-dasharray:251.3;stroke-dashoffset:251.3"/></svg><b data-o="score">–</b></div>
<p class="center"><small>Answered <span data-o="count">0 / 10</span></small></p>
<p class="tool-msg" data-o="verdict"></p>
<p class="tool-h tool-h-sm">To do before you demand appraisal</p>
<ul class="todo" data-o="todo"><li>Nothing flagged yet.</li></ul>
</div></div></div>"""

ICE = ("""
<div class="tool" data-tool="ice">
<div class="tool-grid">
<fieldset class="tool-in"><legend class="tool-h">Your house and winter</legend>
<div class="fld"><label for="{u}-zone">Where is the home?</label><select id="{u}-zone" name="zone"><option value="3">U.P. snow belt (Keweenaw, Marquette, Munising)</option><option value="2">West Michigan lakeshore snow belt</option><option value="1" selected>Southeast or mid-Michigan</option><option value="1.5">Northern Lower Peninsula</option></select></div>
<div class="fld"><label for="{u}-ins">Attic insulation</label><select id="{u}-ins" name="ins"><option value="3">Thin or patchy (under about R-19)</option><option value="1.5" selected>Moderate (about R-30)</option><option value="0">Deep (R-49 or more)</option></select></div>
<div class="fld"><label for="{u}-vent">Attic ventilation</label><select id="{u}-vent" name="vent"><option value="2">Little or none / not sure</option><option value="1" selected>Some soffit or roof vents</option><option value="0">Balanced soffit and ridge vents</option></select></div>
<div class="fld"><label for="{u}-shape">Roof features</label><select id="{u}-shape" name="shape"><option value="0">Simple gable, few penetrations</option><option value="1" selected>Valleys, dormers or skylights</option><option value="2">Low-slope sections or many valleys</option></select></div>
<div class="fld chk"><label class="check"><input type="checkbox" name="barrier"> <span>Ice-and-water barrier known to be installed at the eaves</span></label></div>
<p class="tool-h tool-h-sm">Interior damage (if a dam already leaked)</p>
""" + _f("dry", "Drywall or plaster ceiling/wall area", "180", "sq ft", kind="num") + _f("insul", "Wet attic insulation to replace", "300", "sq ft", kind="num") + _f("floor", "Flooring affected", "120", "sq ft", kind="num") + _f("rooms", "Rooms to repaint", "2", "rooms", kind="num") + """
</fieldset>
<div class="tool-out" aria-live="polite"><p class="tool-h">Risk and illustrative cost</p>
<div class="meter" aria-hidden="true"><i data-o="bar"></i></div>
""" + _out("risk", "Ice dam risk", True, "—") + _out("low", "Illustrative interior repair, low") + _out("high", "Illustrative interior repair, high") + """
<p class="tool-msg" data-o="imsg"></p>
<p class="hint">Unit costs are broad, illustrative Michigan ranges for planning only. Real pricing depends on materials, access and current labor rates.</p>
</div></div></div>""")

TOOLS = [
    {
        "slug": "claim-gap-fee-estimator", "name": "Claim Gap & Fee Estimator", "kind": "Estimator",
        "title": "Claim Gap & Appraisal Fee Estimator | Michigan",
        "desc": "Free Michigan claim gap and appraisal fee estimator: compare two estimates, test where an award might land and see the net after fees.",
        "h1": "Claim Gap and Appraisal Fee Estimator",
        "short": "Measure the gap between two estimates and see what appraisal might net after fees.",
        "lede": "Before you demand appraisal, find out whether the money in dispute is worth the cost of the process. Enter both estimates, choose a fee arrangement and slide the award assumption.",
        "markup": GAP_FULL,
        "explain": """
<h2>How the estimator works</h2>
<p>The disputed amount is your estimate minus the carrier’s. The slider assumes an award somewhere inside that gap; appraisal panels often land between the two numbers, but not always, and an award can also confirm the carrier’s figure. The tool then subtracts the appraiser fee you choose and, if you tick the box, half of an umpire’s fee, because in most policies each side pays its own appraiser and splits the umpire.</p>
<h2>Reading the break-even point</h2>
<p>Break-even tells you how far into the gap an award must land before the increase covers your costs. If break-even is above 70 or 80 percent, a line-by-line <a href="/michigan-claim-appraisal/insurance-estimate-second-opinion/">estimate second opinion</a> and a supplement request may be the smarter first step.</p>
<div class="note"><b class="h">Illustrative only</b>The defaults are made-up figures for demonstration. They don’t describe any client or predict any award.</div>
<h2>What it leaves out</h2>
<p>The estimator doesn’t model coverage disputes, depreciation timing or interest. For the holdback side of the payment, use the <a href="/mi-claim-calculators/rcv-acv-holdback-calculator/">RCV and ACV holdback calculator</a>.</p>""",
        "faqs": [
            ("Does an appraisal award always land between the two estimates?", "No. Panels decide the amount of loss on the evidence, and an award can match either estimate or fall outside both if items were missed. The slider is a planning assumption, not a prediction."),
            ("Who pays the umpire in Michigan?", "Most Michigan policies follow the statutory pattern where each side pays its own appraiser and the umpire’s cost is shared equally. Check the appraisal condition in your policy."),
            ("Is a percentage fee common?", "Fee arrangements vary. Some appraisers charge flat or hourly fees, others a percentage of the increase. Whatever the structure, get it in writing before work starts."),
        ],
    },
    {
        "slug": "rcv-acv-holdback-calculator", "name": "RCV & ACV Holdback Calculator", "kind": "Calculator",
        "title": "RCV vs ACV Holdback Calculator | Michigan Claims",
        "desc": "Free RCV vs ACV holdback calculator for Michigan claims: depreciate each line item, see your first check and the holdback still owed.",
        "h1": "RCV vs. ACV Depreciation and Holdback Calculator",
        "short": "Depreciate line items, see the first check and how much holdback you can recover.",
        "lede": "Most Michigan homeowners policies pay actual cash value first and release the withheld depreciation after repairs. This calculator shows both checks, line by line.",
        "markup": DEP,
        "explain": """
<h2>Why the first check looks small</h2>
<p>Replacement cost value (RCV) is what it costs to repair or replace with like kind and quality today. Actual cash value (ACV) is RCV minus depreciation for age and condition. Under a typical replacement cost policy the carrier pays ACV less your deductible, then releases the recoverable depreciation, often called holdback, once you finish the work and send proof.</p>
<h2>How depreciation is estimated here</h2>
<p>The tool uses straight-line depreciation: age divided by expected life, capped at the maximum you set. Carriers use their own schedules, and some don’t depreciate labor, so your numbers may differ. Large differences in depreciation are a common reason owners ask for an <a href="/michigan-claim-appraisal/insurance-estimate-second-opinion/">estimate second opinion</a>.</p>
<div class="note"><b class="h">Watch the clock</b>Policies set a period to complete repairs and claim holdback. Put it on your calendar with the <a href="/mi-claim-calculators/claim-deadline-planner/">claim deadline planner</a>.</div>""",
        "faqs": [
            ("Can depreciation be disputed in appraisal?", "In many cases the amount of actual cash value, including depreciation, is part of the amount of loss an appraisal panel decides. Read your policy’s appraisal wording, which in Michigan typically refers to actual cash value or the amount of loss."),
            ("Is labor depreciated in Michigan?", "Practices vary by policy and carrier. Ask your adjuster whether labor was depreciated and on what basis, and compare the line items."),
            ("What if my policy is ACV only?", "Tick the ACV-only box. Some older homes and policies for seasonal or rental property pay ACV with no holdback to recover."),
        ],
    },
    {
        "slug": "roof-squares-pitch-calculator", "name": "Roof Squares & Pitch Calculator", "kind": "Calculator",
        "title": "Roof Squares & Pitch Calculator with Ice Barrier",
        "desc": "Free roof squares and pitch calculator for Michigan claims: surface area, squares with waste, bundles and eave ice-barrier rows in seconds.",
        "h1": "Roof Squares and Pitch Calculator (with Ice Barrier Rows)",
        "short": "Convert footprint and pitch into squares, bundles and eave ice-barrier rows.",
        "lede": "Roof claims often turn on a few squares and a missing line for ice-and-water barrier. Check the carrier’s math with your own measurements.",
        "markup": ROOF,
        "explain": """
<h2>Squares, pitch and waste</h2>
<p>One roofing square covers 100 square feet of roof surface. The footprint gets multiplied by a pitch factor (the square root of 1 + (rise/12)²), so a 6/12 roof has about 12 percent more surface than its footprint. A waste factor covers cutting at hips, valleys and rakes. Estimates normally round shingle quantities to the nearest third of a square because shingles come three bundles to a square.</p>
<h2>Why the ice barrier matters in Michigan</h2>
<p>Michigan’s residential code generally calls for an ice barrier at the eaves in areas with a history of ice damming, extending from the edge to a point at least 24 inches inside the exterior wall line. When a damaged roof is replaced, that barrier is often a required item that should appear in the estimate. The calculator converts your eave length and overhang into rows of a standard 3-foot roll so you can check the quantity. Confirm the code with your local building department; requirements can be adopted with local amendments.</p>
<div class="note"><b class="h">Measure safely</b>Use plans, aerial reports or ground measurements. Don’t climb a damaged or icy roof.</div>
<p>For hail and wind roof disputes, see our <a href="/michigan-claim-appraisal/hail-roof-damage-appraisal/">hail and roof damage appraisal</a> page.</p>""",
        "faqs": [
            ("Why does my estimate show fewer squares than my roofer?", "Common causes are a lower waste factor, a wrong pitch, or missed areas such as dormers and porches. Compare the measurements line by line."),
            ("What pitch triggers steep charges?", "Estimating software usually adds steep-roof labor from 7/12 or 8/12 and up, and high-roof charges for two-story walls. Check how your estimate handles both."),
            ("Does every Michigan roof need ice barrier?", "Code requirements depend on the jurisdiction and project. Michigan’s residential code generally requires it where ice damming is a known risk, which covers most of the state."),
        ],
    },
    {
        "slug": "percentage-deductible-calculator", "name": "Percentage Deductible Calculator", "kind": "Calculator",
        "title": "Percentage Deductible Calculator | Michigan Homes",
        "desc": "Free percentage deductible calculator for Michigan homes: turn a 1% or 2% wind/hail deductible into dollars and compare it with a flat one.",
        "h1": "Percentage Deductible Calculator for Michigan Policies",
        "short": "Turn a 1% or 2% deductible into dollars and compare it with a flat deductible.",
        "lede": "More Michigan policies now carry percentage deductibles, often for wind and hail. A 2% deductible on a $340,000 dwelling is $6,800, not $2. See what yours means.",
        "markup": DEDUCT,
        "explain": """
<h2>How percentage deductibles work</h2>
<p>A percentage deductible is calculated from your Coverage A dwelling limit, not from the size of the loss. Some policies apply it to all perils; others apply it only to wind and hail, with a flat deductible for everything else. Your declarations page shows which.</p>
<h2>Why it matters in a dispute</h2>
<p>With a large deductible, small differences in the estimate can decide whether anything is paid at all. That makes an accurate scope more important, not less. If a spring hailstorm or summer wind event left damage close to your deductible, a careful <a href="/michigan-claim-appraisal/insurance-estimate-second-opinion/">estimate second opinion</a> can show whether the carrier missed items.</p>
<div class="note"><b class="h">Check the trigger</b>Read when the percentage deductible applies. Wind-driven rain, a fallen tree or ice damage may fall under a different deductible depending on the policy wording.</div>""",
        "faqs": [
            ("Is the deductible taken from the carrier’s estimate or mine?", "The deductible is subtracted from whatever the amount of loss turns out to be, whether that’s set by agreement or by an appraisal award."),
            ("Can I change a percentage deductible?", "Often yes, at renewal and usually for a higher premium. Talk with your agent; we don’t sell insurance."),
            ("Does the deductible apply per storm?", "Usually per occurrence. If two separate storms damaged the roof, each loss may carry its own deductible, which is one reason dates of loss matter."),
        ],
    },
    {
        "slug": "claim-deadline-planner", "name": "Claim Deadline Planner", "kind": "Planner",
        "title": "Claim Deadline Planner with Calendar | Michigan",
        "desc": "Free Michigan claim deadline planner: map holdback, inventory and estimated suit-limitation dates, then download them as an .ics calendar.",
        "h1": "Michigan Claim Deadline Planner (with .ics Export)",
        "short": "Build a claim calendar, estimate tolling and export every date to your calendar.",
        "lede": "Missed dates sink more claims than bad estimates. Enter your date of loss and the planner builds a calendar you can download, including a rough estimate of the general Michigan suit-limitation rule with tolling.",
        "markup": DATES,
        "explain": """
<h2>What the planner calculates</h2>
<p>The planner adds your policy’s holdback window and a personal inventory target to the date of loss. It also estimates the general Michigan suit-limitation date. Michigan’s Insurance Code generally requires suits under a property policy to be started within one year after the loss, or a longer period if the policy allows, and pauses (tolls) that period from the day you give notice of the loss until the insurer formally denies liability. If you enter a notice date and a denial date, the planner adds that paused time back in.</p>
<div class="note"><b class="h">Not legal advice</b>Deadline rules have exceptions and depend on your exact policy and facts. Use this as a reminder system and confirm every date with a Michigan attorney.</div>
<h2>Using the calendar file</h2>
<p>The .ics download works with Google Calendar, Outlook and Apple Calendar. Each milestone is an all-day event, with an optional reminder two weeks ahead. Nothing you enter leaves your browser.</p>
<p>Next, check how ready your file is with the <a href="/mi-claim-calculators/appraisal-readiness-score/">appraisal readiness score</a>.</p>""",
        "faqs": [
            ("What counts as a formal denial?", "That’s a legal question. A partial payment letter may or may not be a formal denial of liability. Ask a Michigan attorney rather than relying on the planner."),
            ("Does demanding appraisal stop the suit clock?", "Don’t assume it does. Appraisal and the suit-limitation period are separate, so protect your deadline with legal advice while appraisal runs."),
            ("Is my data saved?", "No. The planner runs in your browser and the calendar file is created on your device."),
        ],
    },
    {
        "slug": "appraisal-readiness-score", "name": "Appraisal Readiness Score", "kind": "Checklist",
        "title": "Appraisal Readiness Score: Is Your Claim Ready?",
        "desc": "Free appraisal readiness score for Michigan claims: answer ten questions and get a to-do list of what to fix before you demand appraisal.",
        "h1": "Appraisal Readiness Score",
        "short": "Ten questions that show whether your claim file is ready for appraisal.",
        "lede": "Appraisal rewards preparation. Answer ten yes-or-no questions and get a score plus a short list of what to fix before anyone signs a demand letter.",
        "markup": READY,
        "explain": """
<h2>What the score weighs</h2>
<p>The heaviest question is whether the dispute is about the amount of loss at all. Appraisal can’t resolve a coverage denial. Next come the documents a panel relies on: both estimates, photos and your policy’s appraisal condition. Smaller items, like receipts and a contents list, still affect how well your number holds up.</p>
<h2>What to do with a low score</h2>
<p>Work through the to-do list first. Demanding appraisal with a thin file can lock in a disappointing award. Our <a href="/michigan-appraisal-process/">appraisal process guide</a> explains each stage, and the <a href="/mi-claim-calculators/claim-gap-fee-estimator/">claim gap and fee estimator</a> shows whether the dispute is big enough to pursue.</p>
<div class="note"><b class="h">Private by design</b>Your answers stay in your browser. Nothing is saved or sent.</div>""",
        "faqs": [
            ("What score do I need before demanding appraisal?", "There’s no magic number, but a file scoring under about 45 usually has gaps a panel will notice. Fix the flagged items first."),
            ("Can you review my file after I take the quiz?", "Yes. Send your estimate and photos through the contact page for a free initial review."),
            ("Does a high score mean I’ll win?", "No. It means your file is organized. The award depends on the evidence and the panel."),
        ],
    },
    {
        "slug": "ice-dam-risk-cost-estimator", "name": "Ice Dam Risk & Cost Estimator", "kind": "Estimator",
        "title": "Ice Dam Risk & Repair Cost Estimator | Michigan",
        "desc": "Free Michigan ice dam estimator: rate your home’s ice dam risk by snow belt, insulation and venting, then size illustrative interior repairs.",
        "h1": "Ice Dam Risk and Repair Cost Estimator",
        "short": "Rate ice dam risk by snow belt and attic, and size illustrative interior repairs.",
        "lede": "From the Keweenaw to Monroe, Michigan winters build ice dams. Score your home’s risk and, if a dam already leaked, get an illustrative range for the interior repairs to compare with the carrier’s estimate.",
        "markup": ICE,
        "explain": """
<h2>How the risk score works</h2>
<p>Ice dams form when heat escaping into the attic melts snow on the upper roof and the meltwater refreezes at the cold eaves. The score adds points for heavy-snow regions, thin insulation, poor ventilation and complex roof shapes, and takes points away for an eave ice-and-water barrier. It’s a rough guide, not an inspection.</p>
<h2>The repair estimate</h2>
<p>If water already came inside, enter the areas affected. The tool applies broad, illustrative unit costs for drywall or plaster repair, insulation replacement, flooring and painting to give a low and high range. Use it to judge whether the carrier’s scope seems to be missing whole categories, not to price the job.</p>
<div class="note"><b class="h">Coverage questions</b>Many policies cover sudden interior water damage from an ice dam while excluding wear, tear and maintenance. Learn more in our guide to <a href="/great-lakes-claim-guides/ice-dam-claims-in-michigan/">ice dam claims in Michigan</a> and on the <a href="/michigan-claim-appraisal/ice-dam-frozen-pipe-appraisal/">ice dam and frozen pipe appraisal</a> page.</div>""",
        "faqs": [
            ("Are ice dams covered by homeowners insurance in Michigan?", "Interior damage caused by an ice dam is commonly covered, subject to the policy’s terms, while the cost of fixing insulation or ventilation problems usually isn’t. Read your policy and ask your adjuster how they view the loss."),
            ("Does the tool know my local labor rates?", "No. It uses wide illustrative ranges. A local contractor estimate is the right source for real pricing."),
            ("Should I chip ice off the roof?", "Chipping can damage shingles and is dangerous. Safer options include roof rakes from the ground or hiring a pro to steam ice dams."),
        ],
    },
]
