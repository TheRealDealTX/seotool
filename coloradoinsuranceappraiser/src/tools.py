"""Interactive claim planning tools: markup + explanatory copy. Logic lives in static/assets/js/app.js.
Every tool runs in the browser; nothing is stored or sent. Default figures are illustrative."""

# ---------------------------------------------------------------- 1. award gap & fee estimator
GAP_FULL = """
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Award gap &amp; fee estimator</span><i>Runs in your browser</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Insurer’s estimate (RCV, $)</label><input id="g-ins" name="insurer" inputmode="decimal" value="21800"><span class="hint">Replacement cost total on the carrier’s estimate.</span></div>
        <div><label for="g-own">Your estimate (RCV, $)</label><input id="g-own" name="yours" inputmode="decimal" value="38400"><span class="hint">Your contractor’s or independent estimate.</span></div>
      </div>
      <div><label for="g-land">Where might the award land within the gap?</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% means the carrier’s number holds; 100% means your full number is awarded.</span></div>
      <div class="row2">
        <div><label for="g-ft">Your appraiser’s fee basis</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of the increase (%)</option><option value="hourly">Hourly ($/hour × hours)</option></select></div>
        <div><label for="g-fee">Fee amount or hourly rate</label><input id="g-fee" name="fee" inputmode="decimal" value="2750"></div>
      </div>
      <div class="row2">
        <div data-show="hourly" hidden><label for="g-hrs">Estimated hours</label><input id="g-hrs" name="hours" inputmode="decimal" value="20"></div>
        <div><label for="g-ump">Umpire’s total fee ($, split 50/50)</label><input id="g-ump" name="umpire" inputmode="decimal" value="3200"></div>
      </div>
      <label class="check"><input type="checkbox" name="useump" checked> Assume an umpire is needed</label>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated net increase to you</small><b data-o="net">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s1"></span><span class="s2"></span><span class="s3"></span></div>
      <div class="legend"><span><i class="s1"></i>Carrier’s number</span><span><i class="s2"></i>Your net gain</span><span><i class="s3"></i>Appraisal costs</span></div>
      <div class="out-rows">
        <div><span>Amount in dispute</span><b data-o="gap">$0</b></div>
        <div><span>Gap as % of carrier estimate</span><b data-o="pct">—</b></div>
        <div><span>Projected award (RCV)</span><b data-o="award">$0</b></div>
        <div><span>Your appraisal costs</span><b data-o="cost">$0</b></div>
        <div><span>Break-even landing point</span><b data-o="breakeven">—</b></div>
      </div>
      <table class="scen"><caption>Three landing scenarios</caption><thead><tr><th scope="col">Award lands at</th><th scope="col">Award</th><th scope="col">Net to you</th></tr></thead>
      <tbody><tr><th scope="row">25% of gap</th><td data-o="a25">$0</td><td data-o="n25">$0</td></tr><tr><th scope="row">50% of gap</th><td data-o="a50">$0</td><td data-o="n50">$0</td></tr><tr><th scope="row">75% of gap</th><td data-o="a75">$0</td><td data-o="n75">$0</td></tr></tbody></table>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

GAP_MINI = """
<div class="tool tool-mini" data-tool="gap">
  <div class="tool-head"><span>Quick gap check</span><i>Illustrative figures</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="m-ins">Insurer’s estimate ($)</label><input id="m-ins" name="insurer" inputmode="decimal" value="16900"></div>
      <div><label for="m-own">Your contractor’s estimate ($)</label><input id="m-own" name="yours" inputmode="decimal" value="29300"></div>
      <div><label for="m-land">Award lands at</label><div class="range"><input id="m-land" type="range" name="land" min="0" max="100" step="5" value="50" data-unit="%"><output>50%</output></div><span class="hint">of the disputed amount</span></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Amount in dispute</small><b data-o="gap">$0</b></div>
      <div class="out-rows">
        <div><span>Gap vs. carrier estimate</span><b data-o="pct">—</b></div>
        <div><span>Projected award</span><b data-o="award">$0</b></div>
        <div><span>Increase before fees</span><b data-o="gain">$0</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

# ---------------------------------------------------------------- 2. RCV / ACV holdback
_DEP_ROW = """<tr><td><input name="item" value="{0}" aria-label="Item"></td><td><input name="rcv" inputmode="decimal" value="{1}" aria-label="Replacement cost"></td><td><input name="age" inputmode="decimal" value="{2}" aria-label="Age in years"></td><td><input name="life" inputmode="decimal" value="{3}" aria-label="Expected life in years"></td><td class="mono" data-o="row">$0</td><td><button type="button" class="x" aria-label="Remove row">×</button></td></tr>"""

DEP = """
<div class="tool tool-wide" data-tool="dep">
  <div class="tool-head"><span>RCV / ACV holdback calculator</span><i>Add as many line items as you need</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th scope="col">Item</th><th scope="col">Replacement cost ($)</th><th scope="col">Age (yrs)</th><th scope="col">Life (yrs)</th><th scope="col">ACV</th><th scope="col"><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Laminated shingle roof", 24600, 11, 30), ("Gutters & downspouts", 2900, 11, 25), ("Exterior paint — south & west elevations", 4100, 5, 8)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn btn-line btn-sm" data-add data-run>+ Add line item</button></div>
      <div class="row3">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="2500"></div>
        <div><label for="d-prior">Prior payments ($)</label><input id="d-prior" name="prior" inputmode="decimal" value="0"><span class="hint">Checks already received.</span></div>
        <div><label for="d-cap">Depreciation cap</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="100">No cap</option></select></div>
      </div>
      <label class="check"><input type="checkbox" name="op"> Add 10% overhead + 10% profit to the replacement cost</label>
      <label class="check"><input type="checkbox" name="nonrec"> Roof is settled at actual cash value only (no recoverable depreciation on these items)</label>
    </div>
    <div class="tool-out tool-out-3" aria-live="polite">
      <div class="out-big"><small>Next check (ACV − deductible − prior)</small><b data-o="first">$0</b></div>
      <div class="out-big"><small>Held back until repairs</small><b data-o="held">$0</b></div>
      <div class="out-big"><small>Total if fully recovered</small><b data-o="total">$0</b></div>
      <div class="out-rows span-all">
        <div><span>Replacement cost (RCV)</span><b data-o="rcv">$0</b></div>
        <div><span>Total depreciation</span><b data-o="dep">$0</b></div>
        <div><span>Depreciation as share of RCV</span><b data-o="deppct">0%</b></div>
        <div><span>Actual cash value (ACV)</span><b data-o="acv">$0</b></div>
      </div>
    </div>
  </div>
</div>"""

# ---------------------------------------------------------------- 3. roof pitch & squares (multi-plane)
_PLANE = """<tr><td><input name="pname" value="{0}" aria-label="Roof plane"></td><td><input name="parea" inputmode="decimal" value="{1}" aria-label="Plan-view area in square feet"></td><td><select name="ppitch" aria-label="Pitch">{2}</select></td><td class="mono" data-o="prow">0</td><td><button type="button" class="x" aria-label="Remove plane">×</button></td></tr>"""


def _pitch_opts(sel):
    return "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == sel else "", p) for p in [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18])


ROOF = """
<div class="tool tool-wide" data-tool="roof">
  <div class="tool-head"><span>Roof pitch &amp; squares calculator</span><i>Plane by plane, like an aerial report</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <p class="hint">Enter each roof plane’s flat, plan-view area (what you’d measure on a site plan or satellite image) and its pitch. The tool converts it to true surface area.</p>
      <div class="table-wrap items-table"><table><thead><tr><th scope="col">Plane</th><th scope="col">Plan area (sq ft)</th><th scope="col">Pitch</th><th scope="col">Squares</th><th scope="col"><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_PLANE.format(n, a, _pitch_opts(p)) for n, a, p in [("Main front & back", 1480, 6), ("Garage", 620, 6), ("Rear addition", 310, 9)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn btn-line btn-sm" data-add data-run>+ Add plane</button></div>
      <div class="row2">
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="10">10% — simple gable</option><option value="14" selected>14% — hips or dormers</option><option value="18">18% — complex / cut-up</option></select></div>
        <div><label for="r-pr">Installed price per square ($, optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 640"></div>
      </div>
      <div><label for="r-cmp">Squares on the carrier’s estimate (optional)</label><input id="r-cmp" name="carrier" inputmode="decimal" placeholder="e.g. 24.5"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Roof squares (before waste)</small><b data-o="sq">0</b></div>
      <div class="out-rows">
        <div><span>Total plan-view area</span><b data-o="plan">0</b></div>
        <div><span>True surface area</span><b data-o="surface">0</b></div>
        <div><span>Squares with waste</span><b data-o="order">0</b></div>
        <div><span>Shingle bundles (3 per square)</span><b data-o="bundles">0</b></div>
        <div><span>Steep area (7/12 and up)</span><b data-o="steepsq">0</b></div>
        <div><span>Rough replacement cost</span><b data-o="cost">—</b></div>
        <div><span>Difference vs. carrier squares</span><b data-o="vs">—</b></div>
      </div>
      <p class="out-msg" data-o="steep"></p>
    </div>
  </div>
</div>"""

# ---------------------------------------------------------------- 4. hail percentage deductible
HAILDED = """
<div class="tool" data-tool="deduct">
  <div class="tool-head"><span>Hail percentage deductible calculator</span><i>1%, 2% and 3% side by side</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling coverage — Coverage A ($)</label><input id="w-a" name="cova" inputmode="decimal" value="565000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Your wind/hail deductible</label><select id="w-p" name="pct"><option value="0.5">0.5%</option><option value="1">1%</option><option value="2" selected>2%</option><option value="3">3%</option><option value="5">5%</option></select></div>
        <div><label for="w-f">All-other-perils deductible ($)</label><input id="w-f" name="flat" inputmode="decimal" value="1500"></div>
      </div>
      <div><label for="w-l">Estimated hail damage ($)</label><input id="w-l" name="loss" inputmode="decimal" value="27800"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your hail deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s3"></span><span class="s1"></span></div>
      <div class="legend"><span><i class="s3"></i>You pay</span><span><i class="s1"></i>Policy pays</span></div>
      <div class="out-rows">
        <div><span>Payment with your % deductible</span><b data-o="pdpay">$0</b></div>
        <div><span>Payment if the flat deductible applied</span><b data-o="flatpay">$0</b></div>
        <div><span>Extra out-of-pocket from the % deductible</span><b data-o="diff">$0</b></div>
      </div>
      <table class="scen"><caption>Same loss, different deductibles</caption><thead><tr><th scope="col">Deductible</th><th scope="col">In dollars</th><th scope="col">Policy pays</th></tr></thead>
      <tbody><tr><th scope="row">1%</th><td data-o="d1">$0</td><td data-o="p1">$0</td></tr><tr><th scope="row">2%</th><td data-o="d2">$0</td><td data-o="p2">$0</td></tr><tr><th scope="row">3%</th><td data-o="d3">$0</td><td data-o="p3">$0</td></tr></tbody></table>
      <p class="out-msg" data-o="below"></p>
    </div>
  </div>
</div>"""

# ---------------------------------------------------------------- 5. claim timeline builder (.ics)
DATES = """
<div class="tool tool-wide" data-tool="dates">
  <div class="tool-head"><span>Claim timeline builder</span><i>Exports an .ics calendar file</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
        <div><label for="t-e">Date of the carrier’s estimate (optional)</label><input id="t-e" type="date" name="est"><span class="hint">Used for the appraisal-demand and umpire milestones.</span></div>
      </div>
      <p class="hint">Edit each window to match your policy and the insurer’s letters. Defaults are common planning figures, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report the claim (days after loss)</label><input id="t-n" name="notice" inputmode="numeric" value="3"></div>
        <div><label for="t-m">Temporary repairs (days after loss)</label><input id="t-m" name="mitig" inputmode="numeric" value="10"></div>
        <div><label for="t-p">Proof of loss (days after loss)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Often counted from the insurer’s request.</span></div>
        <div><label for="t-a">Decide on appraisal (days after estimate)</label><input id="t-a" name="appr" inputmode="numeric" value="30"></div>
        <div><label for="t-u">Name your appraiser (days after demand)</label><input id="t-u" name="name" inputmode="numeric" value="20"><span class="hint">Many appraisal clauses use 20 days.</span></div>
        <div><label for="t-r">Recover depreciation (days after loss)</label><input id="t-r" name="rcd" inputmode="numeric" value="365"></div>
        <div><label for="t-s">Suit limitation (days after loss)</label><input id="t-s" name="suit" inputmode="numeric" value="730"><span class="hint">Read the “Suit Against Us” clause; confirm with an attorney.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="plan" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn btn-navy btn-sm" data-ics>Download .ics calendar file</button></div>
    </div>
  </div>
</div>"""

# ---------------------------------------------------------------- 6. appraisal file readiness check (yes / partly / no)
_QUIZ = [
    (3, "Has the insurer accepted coverage for at least part of the loss?", "Get written confirmation of what the insurer accepted. If the claim was denied outright, speak with a Colorado attorney before considering appraisal."),
    (3, "Do you have the carrier’s complete, line-item estimate?", "Ask in writing for the full itemized estimate, not just the summary page or payment letter."),
    (3, "Do you have your own itemized estimate from a contractor or estimator?", "Get an independent line-item estimate. A one-line roofing bid rarely holds up in front of a panel."),
    (2, "Do you have dated photos taken soon after the storm or fire?", "Gather every photo and note the date. For hail, include soft metals, gutters, vents and window wraps."),
    (2, "Have you found and read the policy’s appraisal clause?", "Look for the “Appraisal” paragraph in the policy conditions and note any time limits it sets."),
    (2, "Do you know the policy’s suit-limitation date?", "Find the “Suit Against Us” clause and calendar the date with the timeline builder."),
    (2, "Is hidden damage opened up and documented (attic, decking, wet walls)?", "Make sure concealed damage has been inspected so the scope is complete before values are argued."),
    (2, "Have temporary repairs been made and receipts saved?", "Tarp, dry out and secure the property, and keep every receipt — mitigation is part of the claim."),
    (1, "Is your correspondence with the carrier organized by date?", "Collect letters, emails and adjuster notes in date order."),
    (2, "Is the gap more than roughly 10% or several thousand dollars?", "Run the award gap & fee estimator; a narrow gap may be better handled by a supplement request."),
]

READY = """
<div class="tool tool-wide" data-tool="ready">
  <div class="tool-head"><span>Appraisal file readiness check</span><i>10 questions · Yes, Partly or No</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <ol class="quiz">""" + "".join(
    '<li data-w="%d" data-fix="%s"><span class="q">%s</span><span class="ypn" role="group" aria-label="Answer"><button type="button" data-v="1" aria-pressed="false">Yes</button><button type="button" data-v="0.5" aria-pressed="false">Partly</button><button type="button" data-v="0" aria-pressed="false">No</button></span></li>' % (w, f, q)
    for w, q, f in _QUIZ) + """
      </ol>
      <div class="btn-row"><button type="button" class="btn btn-line btn-sm" data-reset>Reset answers</button></div>
    </div>
    <div class="tool-out tool-out-gauge" aria-live="polite">
      <div class="gauge"><svg viewBox="0 0 100 100" width="180" height="180" aria-hidden="true" focusable="false"><circle cx="50" cy="50" r="40" fill="none" stroke="#e3e9f3" stroke-width="10"/><circle data-o="arc" cx="50" cy="50" r="40" fill="none" stroke="#002868" stroke-width="10" stroke-linecap="round" stroke-dasharray="251.3" stroke-dashoffset="251.3" transform="rotate(-90 50 50)"/></svg><div class="gauge-n"><b data-o="score">–</b><small>out of 100</small></div></div>
      <div><p class="count">Answered: <b data-o="count">0 / 10</b></p><p class="out-msg" data-o="verdict"></p><p class="todo-t">Your to-do list</p><ul class="todo" data-o="todo"><li>Nothing flagged yet.</li></ul></div>
    </div>
  </div>
</div>"""

# ---------------------------------------------------------------- 7. hail size & roof impact checker (Colorado tool)
_SIZES = [("0.75", "¾ in — penny"), ("1", "1 in — quarter"), ("1.25", "1¼ in — half dollar"), ("1.5", "1½ in — walnut"), ("1.75", "1¾ in — golf ball"),
          ("2", "2 in — hen egg"), ("2.5", "2½ in — tennis ball"), ("2.75", "2¾ in — baseball"), ("3", "3 in — teacup"), ("4", "4 in — softball")]
_ROOFS = [("1", "3-tab asphalt shingles"), ("1.25", "Laminated (architectural) shingles"), ("1.75", "Class 4 impact-resistant shingles"),
          ("1.25", "Concrete or clay tile"), ("1.5", "Wood shakes"), ("1.5", "Slate"), ("1.75", "Standing-seam metal (functional)"), ("1", "Metal panels (cosmetic dents)")]

HAILSIZE = """
<div class="tool" data-tool="hail">
  <div class="tool-head"><span>Hail size &amp; roof impact checker</span><i>Illustrative reference values</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="h-s">Largest hail reported at the property</label><select id="h-s" name="size">""" + "".join('<option value="%s"%s>%s</option>' % (v, " selected" if v == "1.75" else "", t) for v, t in _SIZES) + """</select><span class="hint">Check storm reports, photos of stones next to a coin or ruler, and dents on soft metals.</span></div>
      <div><label for="h-r">Roof covering</label><select id="h-r" name="roof">""" + "".join('<option value="%s" data-name="%s"%s>%s</option>' % (v, t, " selected" if i == 1 else "", t) for i, (v, t) in enumerate(_ROOFS)) + """</select></div>
      <div class="row2">
        <div><label for="h-a">Roof age (years)</label><input id="h-a" name="age" inputmode="numeric" value="9"></div>
        <div><label for="h-w">Wind during the storm</label><select id="h-w" name="wind"><option value="0">Calm or light</option><option value="1" selected>Gusty</option><option value="2">Strong, wind-driven hail</option></select></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Damage likelihood (reference only)</small><b data-o="band">—</b></div>
      <div class="meter" aria-hidden="true"><span data-o="meter"></span></div>
      <div class="out-rows">
        <div><span>Approx. impact energy</span><b data-o="energy">—</b></div>
        <div><span>Approx. fall speed</span><b data-o="speed">—</b></div>
        <div><span>Commonly cited damage threshold</span><b data-o="thresh">—</b></div>
        <div><span>Hail size vs. threshold</span><b data-o="ratio">—</b></div>
      </div>
      <p class="out-msg" data-o="advice"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "award-gap-fee-estimator", "name": "Award Gap & Fee Estimator", "kind": "Calculator", "photo": "calc", "step": 5,
        "order": "test whether the dispute is big enough to justify appraisal costs.",
        "short": "Project an appraisal award across three landing scenarios and net out appraiser and umpire fees.",
        "title": "Award Gap & Fee Estimator | Is Appraisal Worth It?",
        "desc": "Free award gap and fee estimator: compare estimates, project an appraisal award in three scenarios and net out appraiser and umpire fees.",
        "h1": "Award Gap & Fee Estimator",
        "lede": "Compare your estimate with the carrier’s, choose where an award might land, and see what you’d keep after appraiser and umpire fees — flat, percentage or hourly.",
        "markup": GAP_FULL,
        "explain": """
<h2>How the estimator works</h2>
<p>Appraisal panels rarely award either side’s full number. They work through the estimates line by line and usually land somewhere in between. The slider lets you test that: choose a landing point within the disputed amount, and the tool projects an award and subtracts what appraisal would cost you.</p>
<ul>
<li><strong>Amount in dispute</strong> is your estimate minus the carrier’s.</li>
<li><strong>Projected award</strong> is the carrier’s number plus your chosen share of the gap.</li>
<li><strong>Your costs</strong> are your appraiser’s fee — flat, a percentage of the increase, or an hourly rate times hours — plus half the umpire’s fee if you expect one.</li>
<li><strong>Break-even landing point</strong> is the share of the gap the award must reach just to cover your costs.</li>
</ul>
<h2>Reading the three scenarios</h2>
<p>The scenario table runs the same math at 25%, 50% and 75% of the gap. If your net is negative even at 50%, a documented supplement request or a professional <a href="/colorado-claim-appraisal/carrier-estimate-review/">carrier estimate review</a> is usually the better first step. If it’s solidly positive at 25%, appraisal is worth a serious conversation.</p>
<div class="callout"><p class="callout-t">Illustrative example</p><p>With the default figures — a $21,800 carrier estimate and a $38,400 contractor estimate — the gap is $16,600. At a 55% landing point the projected award is about $30,930. These numbers are illustrative only, not a result from any real claim.</p></div>
<h2>What the estimator can’t tell you</h2>
<p>It can’t judge whether your estimate is defensible. An inflated estimate makes the gap look large and the award land low. Before relying on any number, make sure each line item is supported by photos, measurements and local pricing.</p>""",
        "faqs": [
            ("Where do awards usually land?", "There’s no reliable average. Results depend on documentation, pricing support and how many items are truly disputed. Use the scenarios to see a range rather than a prediction."),
            ("Why include an hourly option?", "Some appraisers bill hourly on complex commercial or contents-heavy files. Enter your rate and an estimate of hours to compare it with a flat or percentage fee."),
            ("Does a bigger gap always mean appraisal is worth it?", "Not if the gap comes from coverage questions — exclusions, wear and tear or late notice. Appraisal values covered damage; it doesn’t decide coverage."),
        ],
    },
    {
        "slug": "rcv-acv-holdback-calculator", "name": "RCV / ACV Holdback Calculator", "kind": "Calculator", "photo": "calc2", "step": 3,
        "order": "see what the first check should be and what’s held back until repairs.",
        "short": "List damaged items with age and life to estimate the next ACV check, the holdback and the full RCV total.",
        "title": "RCV / ACV Holdback Calculator | Depreciation Checks",
        "desc": "Free RCV / ACV holdback calculator: list items with age and life, add O&P and prior payments, and see your next check and the holdback.",
        "h1": "RCV / ACV Holdback Calculator",
        "lede": "Replacement-cost policies usually pay in two parts: actual cash value first, depreciation later. Add your line items to estimate both checks — including prior payments and O&P.",
        "markup": DEP,
        "explain": """
<h2>Why the first check feels short</h2>
<p>On most replacement-cost policies, the insurer first pays the <strong>actual cash value</strong> — replacement cost minus depreciation — less your deductible. The depreciation is “held back” and paid once repairs are done and documented. On an older roof, that holdback can be a large share of the claim.</p>
<h2>How the math works</h2>
<ul>
<li>Each item’s depreciation is its age divided by its expected life, times its replacement cost, up to the cap you choose.</li>
<li>The optional O&amp;P box adds 10% overhead and 10% profit to replacement cost, a common convention when a general contractor coordinates several trades.</li>
<li>The next check is ACV minus the deductible and any payments you’ve already received.</li>
<li>If your roof is settled at ACV only — some policies use a roof payment schedule or ACV endorsement — tick the box and the holdback becomes zero.</li>
</ul>
<h2>Colorado roofs and depreciation</h2>
<p>Intense high-altitude sun ages asphalt shingles, and many Front Range roofs have been replaced after earlier hail. Depreciation disputes often turn on the roof’s real age, the expected life used, and whether the policy has a roof schedule. Check your declarations page and endorsements, then compare the carrier’s figures with the estimate.</p>
<div class="callout"><p class="callout-t">Deadlines matter</p><p>Most policies set a time limit to complete repairs and claim recoverable depreciation. Put it on your calendar with the <a href="/claim-planning-tools/claim-timeline-builder/">claim timeline builder</a>.</p></div>""",
        "faqs": [
            ("Is labor depreciated in Colorado?", "Practice varies by insurer and estimate, and the policy language matters. If labor is depreciated on your estimate, ask the adjuster which policy provision they are relying on."),
            ("What life should I use for a shingle roof?", "Use the expected life the carrier used if it’s on the estimate, then test a different figure. Material, manufacturer, ventilation and exposure all affect real service life."),
            ("Does appraisal set depreciation?", "An appraisal award often states both replacement cost and actual cash value, which is why disputed depreciation can be part of an appraisal."),
        ],
    },
    {
        "slug": "roof-pitch-squares-calculator", "name": "Roof Pitch & Squares Calculator", "kind": "Calculator", "photo": "shingles", "step": 2,
        "order": "measure the roof plane by plane and compare squares with the estimate.",
        "short": "Add each roof plane’s plan area and pitch to get true squares, steep area and waste — then compare with the carrier.",
        "title": "Roof Pitch & Squares Calculator | Plane by Plane",
        "desc": "Free roof pitch and squares calculator: enter each plane’s area and pitch to get true squares, steep area, waste and a carrier comparison.",
        "h1": "Roof Pitch & Squares Calculator",
        "lede": "Roof estimates are measured in squares of 100 square feet of true roof surface. Enter each plane separately to see total squares, waste, steep area and how your number compares with the carrier’s.",
        "markup": ROOF,
        "explain": """
<h2>From plan area to true surface</h2>
<p>A pitched roof has more surface than the flat footprint beneath it. The pitch multiplier is √(1 + (rise ÷ 12)²): about 1.118 for a 6/12 roof and 1.25 for 9/12. Multiply each plane’s plan area by its multiplier, add them up and divide by 100 to get squares.</p>
<h2>Why plane by plane?</h2>
<p>Many Colorado homes mix pitches: a 6/12 main roof, a low-slope porch and a steeper addition or garage. Averaging a single pitch over the whole roof can understate the steep area — and steep area matters because most estimating software adds charges for labor on steeper slopes.</p>
<ul>
<li><strong>Waste</strong> accounts for cutting at hips, valleys and rakes. Complex roofs need more.</li>
<li><strong>Steep area</strong> sums planes at 7/12 and above, where steep charges commonly start.</li>
<li><strong>Carrier comparison</strong> shows the difference between your squares and the squares on the estimate.</li>
</ul>
<h2>Using the result</h2>
<p>If your measured squares differ from the estimate by more than a few percent, ask how the carrier measured — aerial imagery, a field sketch or a contractor report. Measurement differences are among the easiest disputes to resolve with good documentation.</p>""",
        "faqs": [
            ("Where do I find plan-view areas?", "Aerial measurement reports, site plans, or a satellite image with a scale bar. You can also measure the building footprint and split it into planes."),
            ("Is a 10% waste factor always right?", "No. Simple gables can be near 10%; hip roofs with valleys and dormers often run higher. Estimates should reflect the roof’s actual complexity."),
            ("Do steep charges apply at 7/12?", "Conventions vary. Many estimates add steep labor at 7/12 and higher steps above 10/12 or 12/12. Check how your estimate treats each plane."),
        ],
    },
    {
        "slug": "hail-percentage-deductible-calculator", "name": "Hail Percentage Deductible Calculator", "kind": "Calculator", "photo": "hailroof", "step": 4,
        "order": "turn a percentage wind/hail deductible into dollars.",
        "short": "Convert a 1–5% wind/hail deductible into dollars and compare what the policy pays at 1%, 2% and 3%.",
        "title": "Hail Percentage Deductible Calculator | Colorado",
        "desc": "Free hail percentage deductible calculator: turn a 1–5% wind/hail deductible into dollars and compare payouts at 1%, 2% and 3% of Coverage A.",
        "h1": "Hail Percentage Deductible Calculator",
        "lede": "Many Colorado homeowners policies now carry a separate wind/hail deductible set as a percentage of dwelling coverage. See what yours means in dollars — and what a claim would actually pay.",
        "markup": HAILDED,
        "explain": """
<h2>What a percentage deductible is</h2>
<p>Instead of a flat dollar amount, a percentage deductible is calculated from your dwelling coverage (Coverage A). On a $565,000 home, a 2% wind/hail deductible is $11,300 — far more than a typical $1,000 or $2,500 all-other-perils deductible. These figures are illustrative.</p>
<h2>Why it matters in Colorado</h2>
<p>Hail is the state’s most frequent large property loss, and insurers have shifted more of that risk to owners through percentage deductibles. Rising home values push the dollar amount up automatically, even if the percentage never changes.</p>
<ul>
<li>The calculator shows your deductible in dollars, the payment after it, and the payment if your flat deductible applied instead.</li>
<li>The table compares 1%, 2% and 3% so you can weigh deductible choices at renewal.</li>
<li>If the loss falls below the deductible, the tool says so — no payment would be owed under that deductible.</li>
</ul>
<h2>Deductibles and appraisal</h2>
<p>A high deductible makes accuracy more important, not less. When a carrier’s estimate lands near your deductible, small omissions — gutters, screens, paint, soft metals — decide whether any payment is owed at all.</p>""",
        "faqs": [
            ("Is the deductible based on my claim or my coverage?", "On your Coverage A dwelling limit, not the size of the loss. Check your declarations page to confirm how your policy words it."),
            ("Can I change my wind/hail deductible?", "Options vary by insurer and are usually set at purchase or renewal. Ask your agent what choices are available and the premium difference."),
            ("Does the deductible apply to each storm?", "Usually per occurrence. Two separate hailstorms in a season can mean two deductibles, which is why the date of loss matters."),
        ],
    },
    {
        "slug": "claim-timeline-builder", "name": "Claim Timeline Builder", "kind": "Planner", "photo": "clipboard", "step": 1,
        "order": "start here so no policy deadline slips past.",
        "short": "Build a dated timeline from the loss and estimate dates — notice, proof of loss, appraisal, suit — and export it.",
        "title": "Claim Timeline Builder | Deadlines to Your Calendar",
        "desc": "Free claim timeline builder: map notice, proof of loss, appraisal and suit-limitation dates from your loss date, then export an .ics file.",
        "h1": "Claim Timeline Builder",
        "lede": "Enter your date of loss (and the estimate date, if you have it) to build a dated timeline of the milestones that matter — then download it straight into your calendar.",
        "markup": DATES,
        "explain": """
<h2>Why a timeline matters</h2>
<p>Property claims run on deadlines: prompt notice, proof of loss when requested, the window to name an appraiser after a demand, the time to complete repairs and recover depreciation, and the policy’s limit on lawsuits. Missing one can cost far more than any pricing dispute.</p>
<h2>How to use it</h2>
<ol>
<li>Enter the date of loss — the storm, fire or freeze date.</li>
<li>If you have the carrier’s estimate, enter its date to place the appraisal milestones.</li>
<li>Edit each window to match your policy and the insurer’s letters.</li>
<li>Download the .ics file and open it in Google Calendar, Outlook or Apple Calendar.</li>
</ol>
<div class="callout"><p class="callout-t">Planning tool, not legal advice</p><p>Colorado law and your policy may set different time limits than the defaults shown, and some deadlines run from a letter rather than the loss date. Confirm critical dates with a Colorado attorney.</p></div>
<h2>Nothing leaves your browser</h2>
<p>The calendar file is generated on your device. We never see your dates.</p>""",
        "faqs": [
            ("Which date is the date of loss for hail?", "The date of the storm that caused the damage. If several storms hit, weather data and inspection findings help tie damage to a specific date."),
            ("Do Colorado deadlines differ from the defaults?", "They can. Read your policy’s conditions and any statutory notices in the insurer’s letters, and confirm with an attorney if a date is close."),
            ("Will the .ics file work on my phone?", "Yes. Open the downloaded file and your phone’s calendar app should offer to add the events."),
        ],
    },
    {
        "slug": "appraisal-file-readiness-check", "name": "Appraisal File Readiness Check", "kind": "Checklist", "photo": "inspect", "step": 6,
        "order": "finish by checking the file is ready before anyone invokes appraisal.",
        "short": "Answer ten questions with Yes, Partly or No to score your file and get a personal to-do list.",
        "title": "Appraisal File Readiness Check | Score Your Claim",
        "desc": "Free appraisal file readiness check: answer ten questions Yes, Partly or No to score your claim file and get a to-do list before appraisal.",
        "h1": "Appraisal File Readiness Check",
        "lede": "Appraisal rewards preparation. Answer ten questions honestly — Yes, Partly or No — to score your file and get a personal list of what to finish first.",
        "markup": READY,
        "explain": """
<h2>Why readiness matters</h2>
<p>Once appraisal starts, the panel values what can be shown. Missing photos, an unopened attic or a lump-sum contractor bid weaken your side’s number. Invoking too early can lock in a low award on the amount of loss.</p>
<h2>How scoring works</h2>
<p>Each question is weighted by how much it typically affects an appraisal. “Yes” earns full weight, “Partly” half and “No” none. The score is the share of available points you earned. Every “Partly” or “No” adds an item to your to-do list.</p>
<ul>
<li><strong>75 and up:</strong> a strong file — the next step is a professional look at the dollar gap.</li>
<li><strong>45–74:</strong> close the gaps first; each one costs credibility.</li>
<li><strong>Below 45:</strong> not ready. Work through the list before invoking appraisal.</li>
</ul>
<p>Nothing is saved. Refresh the page and your answers are gone.</p>""",
        "faqs": [
            ("Should I invoke appraisal with a low score?", "Usually not. Strengthen the documentation first, unless a policy deadline forces the issue — in which case talk to a professional right away."),
            ("Why is coverage the first question?", "Appraisal sets the amount of a covered loss. If coverage is denied, appraisal generally isn’t the right tool and legal advice may be needed."),
            ("What counts as “Partly”?", "Anything started but incomplete — some photos but not of every elevation, or an estimate missing trades like gutters or interior repairs."),
        ],
    },
    {
        "slug": "hail-size-roof-impact-checker", "name": "Hail Size & Roof Impact Checker", "kind": "Reference", "photo": "hail", "step": 0,
        "order": "after a storm, gauge whether reported hail could plausibly damage your roof type.",
        "short": "Pick the hail size and roof type to see approximate impact energy and commonly cited damage thresholds.",
        "title": "Hail Size & Roof Impact Checker | Colorado Hail",
        "desc": "Free hail size and roof impact checker: compare reported hail with commonly cited damage thresholds for shingles, tile, shakes and metal roofs.",
        "h1": "Hail Size & Roof Impact Checker",
        "lede": "Built for Hail Alley. Choose the largest hail reported at your property and your roof covering to see approximate impact energy, a commonly cited damage threshold and what to document next.",
        "markup": HAILSIZE,
        "explain": """
<h2>What the checker shows</h2>
<p>Hailstones gain energy fast as they grow: a 2-inch stone carries roughly seventeen times the impact energy of a 1-inch stone. The checker uses approximate published reference values for ice spheres falling at terminal speed and compares the stone size you pick with damage thresholds commonly cited in roofing research for each covering.</p>
<ul>
<li><strong>Impact energy and fall speed</strong> are approximations for a solid sphere of ice in still air. Real stones vary in shape and density.</li>
<li><strong>Thresholds</strong> are the approximate hail size at which functional damage to a new covering is often reported. Older or brittle materials can be damaged by smaller hail.</li>
<li><strong>Wind</strong> adds horizontal speed and changes the angle of impact, which is why elevations facing the storm often take the worst damage.</li>
</ul>
<div class="callout"><p class="callout-t">Reference only</p><p>Values are illustrative and rounded. They don’t replace an on-site inspection, and a “low” result doesn’t mean no damage occurred — check gutters, vents, screens, siding and window wraps, which dent at smaller sizes.</p></div>
<h2>Using it in a claim</h2>
<p>Hail size is often disputed. Save photos of stones beside a coin or ruler, note the time of the storm, and look up local storm reports. If the carrier says hail was “too small” for your roof, the comparison here is a starting point for a conversation — not the answer.</p>""",
        "faqs": [
            ("How do I know what size hail hit my house?", "Photos of stones next to a coin or ruler taken during or right after the storm, dent sizes on soft metals like gutters and vents, and local storm reports all help."),
            ("Are Class 4 shingles hail-proof?", "No. Class 4 is a laboratory impact rating. Impact-resistant shingles can still be damaged by large hail, and some policies treat cosmetic damage differently."),
            ("Why does roof age change the result?", "Asphalt shingles lose flexibility as they age under strong sun, so older roofs can be damaged by hail below the thresholds cited for new material."),
        ],
    },
]
