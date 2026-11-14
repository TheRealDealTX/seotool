"""Interactive claim tools: markup, copy and FAQs. Logic lives in static/assets/js/app.js.
Every tool runs in the browser. Nothing is sent or stored."""


def _sel(name, id_, opts, selected):
    return f'<select id="{id_}" name="{name}">' + "".join(
        f'<option value="{v}"{" selected" if str(v) == str(selected) else ""}>{label}</option>' for v, label in opts) + "</select>"


GAP_FULL = """
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Award gap &amp; fee estimator</span><i>Private · runs in your browser</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Carrier’s estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="16800"><span class="hint">Replacement cost total on the insurer’s estimate.</span></div>
        <div><label for="g-own">Your estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="29400"><span class="hint">Contractor’s or independent estimate.</span></div>
      </div>
      <div><label for="g-land">Where you expect the award to land in the gap</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% means the carrier’s number holds; 100% means your full number is awarded.</span></div>
      <div class="row2">
        <div><label for="g-ft">How your appraiser charges</label>""" + _sel("feetype", "g-ft", [("flat", "Flat fee ($)"), ("pct", "Percent of the increase (%)"), ("hourly", "Hourly (hours × rate)")], "flat") + """</div>
        <div><label for="g-fee">Fee amount</label><input id="g-fee" name="fee" inputmode="decimal" value="2400"><span class="hint">Dollars, percent, or hours depending on the fee type.</span></div>
      </div>
      <div data-fee-hourly hidden><label for="g-rate">Hourly rate ($)</label><input id="g-rate" name="rate" inputmode="decimal" value="150"></div>
      <label class="check"><input type="checkbox" name="useump" checked> Add my half of an umpire’s fee</label>
      <div><label for="g-ump">Umpire’s total fee</label><input id="g-ump" name="umpire" inputmode="decimal" value="3200"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated net increase to you</small><b data-o="net">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s-a"></span><span class="s-b"></span><span class="s-c"></span></div>
      <div class="legend"><span><i class="s-a"></i>Carrier’s number</span><span><i class="s-b"></i>Your net gain</span><span><i class="s-c"></i>Appraisal costs</span></div>
      <div class="out-rows">
        <div><span>Amount in dispute</span><b data-o="gap">$0</b></div>
        <div><span>Gap as % of carrier estimate</span><b data-o="pct">—</b></div>
        <div><span>Projected award (RCV)</span><b data-o="award">$0</b></div>
        <div><span>Your appraisal costs</span><b data-o="cost">$0</b></div>
      </div>
      <table class="scen"><caption>Net to you if the award lands at…</caption><thead><tr><th scope="col">25%</th><th scope="col">50%</th><th scope="col">75%</th></tr></thead><tbody><tr><td data-o="s25">$0</td><td data-o="s50">$0</td><td data-o="s75">$0</td></tr></tbody></table>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

GAP_MINI = """
<div class="tool tool-mini" data-tool="gap">
  <div class="tool-head"><span>Quick gap check</span><i>No sign-up</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="m-ins">Carrier’s estimate</label><input id="m-ins" name="insurer" inputmode="decimal" value="13900"></div>
      <div><label for="m-own">Your contractor’s estimate</label><input id="m-own" name="yours" inputmode="decimal" value="24600"></div>
      <div><label for="m-land">Award lands at</label><div class="range"><input id="m-land" type="range" name="land" min="0" max="100" step="5" value="50" data-unit="%"><output>50%</output></div><span class="hint">of the disputed amount</span></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Amount in dispute</small><b data-o="gap">$0</b></div>
      <div class="out-rows">
        <div><span>Gap vs. carrier estimate</span><b data-o="pct">—</b></div>
        <div><span>Projected award</span><b data-o="award">$0</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

_DEP_ROW = """<tr><td><input name="item" value="{0}" aria-label="Item"></td><td><input name="rcv" inputmode="decimal" value="{1}" aria-label="Replacement cost"></td><td><input name="year" inputmode="numeric" value="{2}" aria-label="Year installed or bought"></td><td><input name="life" inputmode="decimal" value="{3}" aria-label="Expected life in years"></td><td class="mono" data-o="row">$0</td><td><button type="button" class="x" aria-label="Remove row">×</button></td></tr>"""

DEP = """
<div class="tool tool-wide" data-tool="dep">
  <div class="tool-head"><span>ACV holdback calculator</span><i>Uses install year, not guesses</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="d-yr">Year of the loss</label><input id="d-yr" name="lossyear" inputmode="numeric" value="2026"></div>
        <div><label for="d-cap">Depreciation cap</label>""" + _sel("cap", "d-cap", [(50, "50%"), (70, "70%"), (80, "80%"), (90, "90%")], 80) + """<span class="hint">Many estimates cap depreciation; check yours.</span></div>
      </div>
      <div class="table-wrap items-table"><table><thead><tr><th scope="col">Item</th><th scope="col">Replacement cost ($)</th><th scope="col">Year installed</th><th scope="col">Life (yrs)</th><th scope="col">ACV</th><th scope="col"><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Laminated shingle roof", 17600, 2016, 30), ("Steel siding — north and west walls", 6400, 2009, 40), ("Basement carpet and pad", 2100, 2020, 10)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn line small" data-add>+ Add item</button></div>
      <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="2500"></div>
      <label class="check"><input type="checkbox" name="nonrec"> My policy pays actual cash value only (nothing held back to recover)</label>
    </div>
    <div class="tool-out wide-out" aria-live="polite">
      <div class="out-big"><small>First payment (ACV − deductible)</small><b data-o="first">$0</b></div>
      <div class="out-big"><small>Held back until repairs</small><b data-o="held">$0</b></div>
      <div class="out-big"><small>Total if fully recovered</small><b data-o="total">$0</b></div>
      <div class="out-rows">
        <div><span>Replacement cost (RCV)</span><b data-o="rcv">$0</b></div>
        <div><span>Total depreciation</span><b data-o="dep">$0</b></div>
        <div><span>Depreciation as share of RCV</span><b data-o="deppct">0%</b></div>
        <div><span>Actual cash value (ACV)</span><b data-o="acv">$0</b></div>
      </div>
    </div>
  </div>
</div>"""

_PITCH = [(p, f"{p}/12") for p in [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14]]
_PLANE = """<tr><td><input name="pname" value="{0}" aria-label="Section name"></td><td><input name="parea" inputmode="decimal" value="{1}" aria-label="Footprint area in square feet"></td><td>{2}</td><td class="mono" data-o="psq">0</td></tr>"""

ROOF = """
<div class="tool" data-tool="roof">
  <div class="tool-head"><span>Roof square &amp; pitch converter</span><i>Up to three roof sections</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th scope="col">Section</th><th scope="col">Flat footprint (sq ft)</th><th scope="col">Pitch</th><th scope="col">Squares</th></tr></thead><tbody>
      """ + "".join(_PLANE.format(n, a, _sel("ppitch", f"r-p{i}", _PITCH, p).replace(f'id="r-p{i}"', f'id="r-p{i}" aria-label="Pitch for {n}"')) for i, (n, a, p) in enumerate([("Main house", 1850, 7), ("Garage", 620, 5), ("Porch", 180, 3)])) + """
      </tbody></table></div>
      <div class="row2">
        <div><label for="r-wst">Waste factor</label>""" + _sel("waste", "r-wst", [(10, "10% — simple gable"), (12, "12% — gable with dormers"), (15, "15% — hip roof"), (18, "18% — cut-up / many valleys")], 15) + """</div>
        <div><label for="r-pr">Installed price per square (optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 560"></div>
      </div>
      <span class="hint">Footprint area is the flat area the roof covers, overhangs included. Measure from a plan, an aerial report or a tape.</span>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Total roof squares (before waste)</small><b data-o="sq">0</b></div>
      <div class="out-rows">
        <div><span>Roof surface area</span><b data-o="surface">0</b></div>
        <div><span>Squares to order (with waste)</span><b data-o="order">0</b></div>
        <div><span>Shingle bundles (3 per square)</span><b data-o="bundles">0</b></div>
        <div><span>Steepest section</span><b data-o="steepest">—</b></div>
        <div><span>Rough replacement cost</span><b data-o="cost">—</b></div>
      </div>
      <p class="out-msg" data-o="steep"></p>
    </div>
  </div>
</div>"""

DEDUCT = """
<div class="tool" data-tool="deduct">
  <div class="tool-head"><span>Hail deductible calculator</span><i>Percentage vs. flat dollar</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling limit (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="340000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Wind/hail deductible</label>""" + _sel("pct", "w-p", [(0.5, "0.5%"), (1, "1%"), (2, "2%"), (3, "3%"), (5, "5%")], 1) + """</div>
        <div><label for="w-f">All-other-perils deductible ($)</label><input id="w-f" name="flat" inputmode="decimal" value="1500"></div>
      </div>
      <div><label for="w-l">Estimated hail or wind damage ($)</label><input id="w-l" name="loss" inputmode="decimal" value="19800"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your wind/hail deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s-c"></span><span class="s-a"></span></div>
      <div class="legend"><span><i class="s-c"></i>You pay</span><span><i class="s-a"></i>Policy pays</span></div>
      <div class="out-rows">
        <div><span>Claim payment with the % deductible</span><b data-o="pdpay">$0</b></div>
        <div><span>Payment if a flat deductible applied</span><b data-o="flatpay">$0</b></div>
        <div><span>Extra you carry under the % deductible</span><b data-o="diff">$0</b></div>
        <div><span>Your share of this loss</span><b data-o="share">—</b></div>
      </div>
      <p class="out-msg" data-o="below"></p>
    </div>
  </div>
</div>"""

DATES = """
<div class="tool tool-wide" data-tool="dates">
  <div class="tool-head"><span>Claim calendar builder</span><i>Exports to your calendar</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="c-dol">Date of loss</label><input id="c-dol" name="dol" type="date"></div>
        <div><label for="c-not">Report the claim within (days)</label><input id="c-not" name="notice" inputmode="numeric" value="7"></div>
      </div>
      <div class="row2">
        <div><label for="c-mit">Finish temporary repairs within (days)</label><input id="c-mit" name="mitig" inputmode="numeric" value="14"></div>
        <div><label for="c-pol">Proof of loss target (days)</label><input id="c-pol" name="pol" inputmode="numeric" value="60"><span class="hint">Many forms count from the carrier’s request.</span></div>
      </div>
      <div class="row2">
        <div><label for="c-rcd">Repairs done to recover depreciation (days)</label><input id="c-rcd" name="rcd" inputmode="numeric" value="180"></div>
        <div><label for="c-suit">Policy suit-limitation period (months)</label><input id="c-suit" name="suit" inputmode="numeric" value="24"><span class="hint">Use the period stated in your policy.</span></div>
      </div>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download .ics calendar</button></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"><li><b>Pick your date of loss</b><span>Your milestones will appear here.</span></li></ol>
    </div>
  </div>
</div>"""

_Q = [
    (3, "Has the insurer accepted that the loss is covered?", "Get the coverage position in writing. Appraisal values a covered loss; it does not decide coverage."),
    (3, "Do you have the carrier’s complete, itemized estimate?", "Ask for the full line-item estimate, not just the payment letter."),
    (2, "Do you have a contractor’s or independent estimate?", "Get a detailed, itemized estimate from a qualified contractor or estimator."),
    (2, "Are there date-stamped photos of every damaged area?", "Photograph every slope, elevation and room, plus soft metals and outbuildings."),
    (2, "Do you know the date of loss and the storm that caused it?", "Pin down the storm date with weather records or news reports."),
    (1, "Have you read the appraisal clause in your own policy?", "Find the appraisal condition in your policy and note any deadlines."),
    (1, "Have you made temporary repairs and saved receipts?", "Tarp, board up or dry out the property and keep every receipt."),
    (1, "Is the dispute larger than a few thousand dollars?", "Run the award gap estimator to see whether fees would eat the recovery."),
    (1, "Are you sure no policy deadline has passed?", "Use the claim calendar builder, and talk to an attorney if a suit deadline is close."),
    (1, "Have you asked the adjuster in writing to reconsider?", "Send a written supplement request with your evidence first; it may close the gap."),
]

READY = """
<div class="tool tool-wide" data-tool="ready">
  <div class="tool-head"><span>Appraisal readiness check</span><i>10 questions · about 2 minutes</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <ol class="quiz">""" + "".join(
    f'<li data-w="{w}" data-fix="{fix}"><span>{q}</span><span class="yn"><button type="button" class="yes" aria-pressed="false">Yes</button><button type="button" class="no" aria-pressed="false">No</button></span></li>'
    for w, q, fix in _Q) + """</ol>
      <div class="btn-row"><button type="button" class="btn line small" data-reset>Start over</button></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="gauge"><svg viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="40" class="g-bg"/><circle cx="50" cy="50" r="40" class="g-fg" data-o="arc"/></svg><div><b data-o="score">–</b><small>readiness</small></div></div>
      <p class="out-msg" data-o="verdict"></p>
      <p class="count">Answered: <b data-o="count">0 / 10</b></p>
      <p class="todo-h">To do before you demand appraisal</p>
      <ul class="todo" data-o="todo"><li>Nothing flagged yet.</li></ul>
    </div>
  </div>
</div>"""

SLOPE = """
<div class="tool" data-tool="slope">
  <div class="tool-head"><span>Slope-by-slope repair gap calculator</span><i>Partial repair vs. full roof</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="s-tot">Total roof squares</label><input id="s-tot" name="total" inputmode="decimal" value="34"></div>
        <div><label for="s-app">Squares the carrier approved</label><input id="s-app" name="approved" inputmode="decimal" value="12"></div>
      </div>
      <div class="row2">
        <div><label for="s-pr">Installed price per square ($)</label><input id="s-pr" name="price" inputmode="decimal" value="560"></div>
        <div><label for="s-rp">Repair premium on partial work</label>""" + _sel("prem", "s-rp", [(0, "None"), (10, "10%"), (20, "20%"), (30, "30%")], 20) + """<span class="hint">Small repairs often cost more per square.</span></div>
      </div>
      <div><label for="s-ex">Whole-roof items not in a partial scope ($)</label><input id="s-ex" name="extras" inputmode="decimal" value="2800"><span class="hint">Ridge, starter, drip edge, vents, gutters or permits that only appear on a full replacement.</span></div>
      <div><label for="s-ded">Deductible ($)</label><input id="s-ded" name="deduct" inputmode="decimal" value="3400"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Gap between partial and full roof</small><b data-o="gap">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s-a"></span><span class="s-b"></span></div>
      <div class="legend"><span><i class="s-a"></i>Approved slopes</span><span><i class="s-b"></i>Disputed slopes</span></div>
      <div class="out-rows">
        <div><span>Share of roof approved</span><b data-o="share">—</b></div>
        <div><span>Partial repair value</span><b data-o="partial">$0</b></div>
        <div><span>Full replacement value</span><b data-o="full">$0</b></div>
        <div><span>Payment after deductible — partial</span><b data-o="ppay">$0</b></div>
        <div><span>Payment after deductible — full</span><b data-o="fpay">$0</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""


TOOLS = [
    {
        "slug": "award-gap-fee-estimator", "name": "Award Gap & Fee Estimator", "kind": "Estimator", "icon": "$",
        "short": "See the disputed amount, a likely award range and what is left after appraiser and umpire fees.",
        "title": "Award Gap & Fee Estimator | Free Appraisal Tool",
        "desc": "Estimate the disputed amount on your Nebraska claim, a likely award range and your net after appraiser and umpire fees with this free tool.",
        "h1": "Award Gap and Fee Estimator",
        "lede": "Before you demand appraisal, check whether the gap is big enough to survive the fees. Enter both estimates and your expected costs to see a realistic net.",
        "markup": GAP_FULL,
        "explain": """
<h2>How the estimator works</h2>
<p>The disputed amount is your estimate minus the carrier’s. Appraisal panels rarely award everything one side asks for, so the slider lets you pick where the award might land inside that gap. The tool then subtracts your appraiser’s fee and, if you choose, half of an umpire’s fee, and shows the net increase. The scenario table repeats the math at 25%, 50% and 75% so you can see the range at a glance.</p>
<h2>Reading the result</h2>
<ul>
<li><strong>Large gap, healthy net:</strong> appraisal may be worth a professional look.</li>
<li><strong>Narrow gap:</strong> a documented supplement request may close it faster and cheaper.</li>
<li><strong>Net near zero or negative:</strong> fees could absorb the recovery. Start with an estimate review.</li>
</ul>
<h2>Illustrative example</h2>
<p>The default figures are illustrative only: a $16,800 carrier estimate against a $29,400 contractor estimate. They are not results from any real claim.</p>
""",
        "faqs": [
            ("Is the award usually in the middle?", "There is no rule. Awards depend on the evidence. The slider is a planning assumption, not a prediction."),
            ("Do I always pay half the umpire?", "Many policies split umpire fees evenly. Check your policy’s appraisal clause."),
            ("Is anything I type saved?", "No. The calculation runs in your browser and nothing is sent or stored."),
        ],
    },
    {
        "slug": "acv-holdback-calculator", "name": "ACV Holdback Calculator", "kind": "Calculator", "icon": "%",
        "short": "Turn install years into depreciation, then see your first payment and the amount held back.",
        "title": "ACV Holdback Calculator | RCV vs ACV Depreciation",
        "desc": "Use install years to estimate depreciation, actual cash value and the recoverable holdback on a Nebraska property claim with this free tool.",
        "h1": "ACV Holdback and Depreciation Calculator",
        "lede": "Replacement cost policies often pay in two steps: actual cash value first, the rest after repairs. Enter what you know about each item to see both payments.",
        "markup": DEP,
        "explain": """
<h2>RCV, ACV and holdback</h2>
<p><strong>Replacement cost value (RCV)</strong> is what it costs to repair or replace with like kind and quality today. <strong>Actual cash value (ACV)</strong> is RCV minus depreciation. Many replacement cost policies pay ACV minus the deductible first, then release the depreciation, often called recoverable depreciation or holdback, once repairs are complete.</p>
<h2>Why install year instead of age</h2>
<p>Owners usually remember when a roof went on or carpet was installed better than they know its exact age. The calculator subtracts the install year from the year of loss, divides by the expected life, and applies the depreciation cap you choose.</p>
<h2>Things to check on your estimate</h2>
<ul>
<li>Labor depreciated along with materials</li>
<li>Life expectancies shorter than the product warranty</li>
<li>Depreciation applied to items that do not wear, such as permits</li>
<li>The deadline for completing repairs to recover the holdback</li>
</ul>
""",
        "faqs": [
            ("Does every policy hold back depreciation?", "No. Actual cash value policies pay ACV only. Many roof endorsements in hail-prone states also change how roofs are valued."),
            ("Can depreciation be disputed in appraisal?", "In many cases, yes. How much depreciation applies is often part of the amount of loss."),
            ("Is the default data real?", "No. The sample items are illustrative only."),
        ],
    },
    {
        "slug": "roof-square-pitch-converter", "name": "Roof Square & Pitch Converter", "kind": "Calculator", "icon": "▲",
        "short": "Convert flat footprints and pitches for up to three roof sections into squares and order quantities.",
        "title": "Roof Square & Pitch Converter | Free Roof Calculator",
        "desc": "Convert flat footprints and pitches for up to three roof sections into squares, waste and bundles, then check them against your claim estimate.",
        "h1": "Roof Square and Pitch Converter",
        "lede": "Most hail claims start with a roof measurement. Enter each section’s flat footprint and pitch to see roof squares, order quantities and whether steep charges may apply.",
        "markup": ROOF,
        "explain": """
<h2>The math</h2>
<p>A roofing square is 100 square feet of roof surface. Because a pitched roof is longer than its flat footprint, each section’s footprint is multiplied by a pitch factor: the square root of 1 plus (rise ÷ 12) squared. A 6/12 roof uses a factor of about 1.118; a 10/12 roof uses about 1.302.</p>
<h2>Why sections matter</h2>
<p>Many Nebraska homes combine a steep main roof with a lower-pitch garage or porch. Treating the whole house as one pitch can understate or overstate the total. Entering each section separately gives a more accurate number to compare with the carrier’s measurement report.</p>
<h2>Waste and steep charges</h2>
<p>Waste covers cutting at hips, valleys and edges. Steep pitches and tall eaves often carry additional labor charges in estimating software. If your roof is steep and the estimate shows no steep or high charges, ask why.</p>
""",
        "faqs": [
            ("Where do I find my footprint area?", "From building plans, an aerial measurement report, county assessor sketches or a tape measure around the eaves."),
            ("What pitch triggers steep charges?", "Estimating software commonly adds steep charges starting around 7/12 or 8/12, but practices vary by carrier and estimate."),
            ("Does this replace a measurement report?", "No. It is a check, not a substitute for a professional measurement."),
        ],
    },
    {
        "slug": "hail-deductible-calculator", "name": "Hail Deductible Calculator", "kind": "Calculator", "icon": "◆",
        "short": "Translate a percentage wind/hail deductible into dollars and see what you pay on a given loss.",
        "title": "Hail Deductible Calculator | Percentage vs Flat",
        "desc": "See what a percentage wind and hail deductible costs in dollars and how it changes the payment on a Nebraska storm claim with this tool.",
        "h1": "Hail Deductible Calculator for Percentage Deductibles",
        "lede": "A 1% or 2% wind/hail deductible sounds small until you multiply it by your dwelling limit. See what yours really means before the next storm.",
        "markup": DEDUCT,
        "explain": """
<h2>How percentage deductibles work</h2>
<p>Many policies in hail-prone states apply a separate wind/hail deductible equal to a percentage of the dwelling limit (Coverage A), not the loss. On a $340,000 limit, a 1% deductible is $3,400; a 2% deductible is $6,800. Your all-other-perils deductible may still be a flat amount.</p>
<h2>Why it matters for appraisal</h2>
<p>The deductible comes off the final amount of loss. A disputed gap that looks large can shrink once a percentage deductible is applied, and a loss that falls below the deductible produces no payment at all. Knowing the dollar figure helps you decide whether a dispute is worth pursuing.</p>
<h2>Check your declarations</h2>
<p>Look for wording such as “windstorm or hail deductible” and the percentage or amount. Some policies apply the percentage only to certain perils or certain structures.</p>
""",
        "faqs": [
            ("Is the percentage based on the loss or the limit?", "Usually the dwelling limit (Coverage A). Some policies differ, so read your declarations."),
            ("Can I change my deductible?", "Often at renewal, with a premium change. Ask your agent before storm season."),
            ("Do farm policies use percentage deductibles?", "Some do. Farm and commercial policies vary widely."),
        ],
    },
    {
        "slug": "claim-calendar-builder", "name": "Claim Calendar Builder", "kind": "Planner", "icon": "▦",
        "short": "Build a claim timeline from your date of loss and export it to Google, Outlook or Apple Calendar.",
        "title": "Claim Calendar Builder | Deadline Planner With .ics",
        "desc": "Turn your date of loss into a claim timeline with reporting, proof of loss, repair and suit milestones, then export it to your calendar.",
        "h1": "Claim Calendar Builder with Calendar Export",
        "lede": "Insurance claims run on deadlines that are easy to miss. Enter your date of loss and the periods in your policy to build a timeline you can add to your calendar.",
        "markup": DATES,
        "explain": """
<h2>The milestones</h2>
<ul>
<li><strong>Reporting:</strong> policies require prompt notice; some set a firm window for wind and hail.</li>
<li><strong>Temporary repairs:</strong> protect the property from further damage and keep receipts.</li>
<li><strong>Proof of loss:</strong> many forms require a sworn proof of loss within a set number of days after the carrier asks for it.</li>
<li><strong>Depreciation recovery:</strong> replacement cost policies often require repairs within a set period to recover holdback.</li>
<li><strong>Suit limitation:</strong> policies commonly limit the time to file a lawsuit. Talk to a Nebraska attorney well before this date.</li>
</ul>
<h2>Use your policy’s numbers</h2>
<p>The defaults are placeholders, not legal deadlines. Replace them with the periods in your own policy and in any letters from your carrier. The .ics file works with Google Calendar, Outlook and Apple Calendar.</p>
""",
        "faqs": [
            ("Are these deadlines legal advice?", "No. They are planning dates based on the numbers you enter. Your policy and Nebraska law control."),
            ("Does the calendar file contain my data?", "Only the dates and labels shown. It is created in your browser and never sent to us."),
            ("What if a deadline has already passed?", "Talk to a Nebraska attorney promptly. Some deadlines can be extended in writing; others cannot."),
        ],
    },
    {
        "slug": "appraisal-readiness-check", "name": "Appraisal Readiness Check", "kind": "Checklist", "icon": "✓",
        "short": "Ten yes-or-no questions that score your file and list what to fix before you demand appraisal.",
        "title": "Appraisal Readiness Check | Is Your Claim Ready?",
        "desc": "Answer ten quick questions to score whether your Nebraska property claim is ready for appraisal and get a to-do list of what to fix first.",
        "h1": "Appraisal Readiness Check",
        "lede": "Appraisal works best with a complete file. Answer ten questions to see how ready you are and what to gather before making a demand.",
        "markup": READY,
        "explain": """
<h2>Why readiness matters</h2>
<p>The appraisal award is binding on the amount of loss. If you demand appraisal before you have the carrier’s full estimate, your own estimate and good photos, you risk locking in a number that leaves damage out.</p>
<h2>How the score works</h2>
<p>Questions are weighted. Coverage acceptance and having the carrier’s itemized estimate count most, because appraisal cannot work without them. Each “No” adds a specific task to your list.</p>
<h2>After you score</h2>
<p>A strong score means it may be time for a professional review of the dollar gap. A lower score gives you a checklist. Either way, our <a href="/appraisal-services-nebraska/carrier-estimate-review/">carrier estimate review</a> is a sensible next step.</p>
""",
        "faqs": [
            ("Does a high score mean I will win?", "No. It means your file has the basics an appraisal panel expects. Outcomes depend on the evidence."),
            ("Is my answer list saved?", "No. Everything stays in your browser."),
            ("Can I retake it?", "Yes. Use Start over at any time."),
        ],
    },
    {
        "slug": "slope-repair-gap-calculator", "name": "Slope-by-Slope Repair Gap Calculator", "kind": "Calculator", "icon": "◩",
        "short": "Compare a partial-slope hail repair with a full roof replacement and see the dollar gap in dispute.",
        "title": "Slope Repair Gap Calculator | Partial vs Full Roof",
        "desc": "Compare a partial-slope hail repair with full roof replacement, see the dollar gap and the payment after your deductible with this free tool.",
        "h1": "Slope-by-Slope Repair Gap Calculator",
        "lede": "One of the most common hail disputes in Nebraska is whether a roof gets a few slopes or a full replacement. Put numbers on that disagreement before you argue it.",
        "markup": SLOPE,
        "explain": """
<h2>The partial-roof problem</h2>
<p>After a hailstorm, carriers sometimes approve the slopes that faced the storm and deny the rest. Owners and contractors often argue the whole roof should be replaced because the same storm hit every exposure, because repairs will not match, or because brittle shingles cannot be spot-repaired.</p>
<h2>What the calculator compares</h2>
<p>The partial value is the approved squares times your installed price, plus a repair premium for small jobs. The full value is every square times the price, plus whole-roof items like ridge, starter, drip edge and vents that only show up on a full replacement. The deductible comes off both.</p>
<h2>What decides the dispute</h2>
<p>Policy wording on matching and cosmetic damage, the condition and age of the shingles, availability of matching material, and the evidence of damage on each slope. An appraisal panel weighs those facts slope by slope.</p>
""",
        "faqs": [
            ("Does Nebraska require full replacement for matching?", "We do not offer legal opinions. Matching outcomes depend on your policy wording and the facts; talk to a Nebraska attorney for legal questions."),
            ("What is a repair premium?", "Small partial repairs often cost more per square than a full roof because setup, travel and minimum charges are spread over less work."),
            ("Are the defaults from a real claim?", "No. They are illustrative only."),
        ],
    },
]
