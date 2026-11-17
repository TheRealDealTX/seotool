"""Interactive claim tools: markup + explanatory copy. Logic lives in static/assets/js/app.js."""

GAP_FULL = """
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Claim gap &amp; fee estimator</span><i>Runs in your browser</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Insurer’s estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="18400"><span class="hint">Replacement cost total on the carrier’s estimate.</span></div>
        <div><label for="g-own">Your estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="31750"><span class="hint">Your contractor’s or independent estimate.</span></div>
      </div>
      <div><label for="g-land">Where might the award land within the gap?</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="60" data-unit="%"><output>60%</output></div>
        <span class="hint">0% = carrier’s number holds. 100% = your full number is awarded. Panels often land in between.</span></div>
      <div class="row2">
        <div><label for="g-ft">Your appraiser’s fee type</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of increase (%)</option></select></div>
        <div><label for="g-fee">Fee amount</label><input id="g-fee" name="fee" inputmode="decimal" value="2500"></div>
      </div>
      <label class="check"><input type="checkbox" name="useump" checked> Include half of an umpire’s fee</label>
      <div><label for="g-ump">Umpire’s total fee (split 50/50)</label><input id="g-ump" name="umpire" inputmode="decimal" value="3000"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated net increase to you</small><b data-o="net">$0</b></div>
      <div class="stack" aria-hidden="true"><span style="background:#c9d3e2"></span><span style="background:#cc0000"></span><span style="background:#002d65"></span></div>
      <div class="legend"><span><i style="background:#c9d3e2"></i>Carrier’s number</span><span><i style="background:#cc0000"></i>Your net gain</span><span><i style="background:#002d65"></i>Appraisal costs</span></div>
      <div class="out-rows">
        <div><span>Amount in dispute</span><b data-o="gap">$0</b></div>
        <div><span>Gap as % of carrier estimate</span><b data-o="pct">—</b></div>
        <div><span>Projected award (RCV)</span><b data-o="award">$0</b></div>
        <div><span>Gross increase</span><b data-o="gain">$0</b></div>
        <div><span>Your appraisal costs</span><b data-o="cost">$0</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

GAP_MINI = """
<div class="tool" data-tool="gap" style="margin:0">
  <div class="tool-head"><span>Quick gap check</span><i>No sign-up</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="m-ins">Insurer’s estimate</label><input id="m-ins" name="insurer" inputmode="decimal" value="14200"></div>
      <div><label for="m-own">Your contractor’s estimate</label><input id="m-own" name="yours" inputmode="decimal" value="26900"></div>
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

_DEP_ROW = """<tr><td><input name="item" value="{0}" aria-label="Item"></td><td><input name="rcv" inputmode="decimal" value="{1}" aria-label="Replacement cost"></td><td><input name="age" inputmode="decimal" value="{2}" aria-label="Age in years"></td><td><input name="life" inputmode="decimal" value="{3}" aria-label="Expected life in years"></td><td class="mono" data-o="row">$0</td><td><button type="button" class="x" aria-label="Remove row">×</button></td></tr>"""

DEP = """
<div class="tool tool-wide" data-tool="dep">
  <div class="tool-head"><span>Depreciation &amp; holdback calculator</span><i>Add as many items as you need</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Architectural shingle roof", 18500, 9, 30), ("Interior paint — living areas", 2400, 4, 10), ("Carpet — two bedrooms", 1850, 6, 10)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn ghost small" data-add data-run>+ Add item</button></div>
      <div class="row2">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="1000"></div>
        <div><label for="d-cap">Maximum depreciation</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="90">90%</option></select><span class="hint">Most estimates cap depreciation; check yours.</span></div>
      </div>
      <label class="check"><input type="checkbox" name="nonrec"> My policy pays actual cash value only (no recoverable depreciation)</label>
    </div>
    <div class="tool-out" aria-live="polite" style="grid-template-columns:repeat(auto-fit,minmax(200px,1fr))">
      <div class="out-big"><small>First check (ACV − deductible)</small><b data-o="first">$0</b></div>
      <div class="out-big"><small>Held back until repairs</small><b data-o="held">$0</b></div>
      <div class="out-big"><small>Total if fully recovered</small><b data-o="total">$0</b></div>
      <div class="out-rows" style="grid-column:1/-1">
        <div><span>Replacement cost (RCV)</span><b data-o="rcv">$0</b></div>
        <div><span>Total depreciation</span><b data-o="dep">$0</b></div>
        <div><span>Depreciation as share of RCV</span><b data-o="deppct">0%</b></div>
        <div><span>Actual cash value (ACV)</span><b data-o="acv">$0</b></div>
      </div>
    </div>
  </div>
</div>"""

ROOF = """
<div class="tool" data-tool="roof">
  <div class="tool-head"><span>Roof squares &amp; pitch calculator</span><i>Compare against your estimate</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <fieldset style="border:0;padding:0;margin:0"><legend class="sr-only">Measurement method</legend>
        <div class="btn-row">
          <label class="check"><input type="radio" name="mode" value="dims" checked> Footprint length × width</label>
          <label class="check"><input type="radio" name="mode" value="area"> I know the footprint area</label>
        </div></fieldset>
      <div class="row2" data-mode="dims">
        <div><label for="r-l">Footprint length (ft)</label><input id="r-l" name="len" inputmode="decimal" value="58"></div>
        <div><label for="r-w">Footprint width (ft)</label><input id="r-w" name="wid" inputmode="decimal" value="34"></div>
      </div>
      <div data-mode="dims"><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="12"></div>
      <div data-mode="area" hidden><label for="r-a">Footprint area incl. overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="2200"></div>
      <div class="row2">
        <div><label for="r-p">Roof pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 6 else "", p) for p in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16]) + """</select></div>
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="10">10% — simple gable</option><option value="12" selected>12% — gable with dormers</option><option value="15">15% — hip roof</option><option value="18">18% — complex / cut-up</option></select></div>
      </div>
      <div><label for="r-pr">Installed price per square (optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 525"><span class="hint">Use a local contractor’s quote for a rough replacement figure.</span></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Roof squares (before waste)</small><b data-o="sq">0</b></div>
      <div class="out-rows">
        <div><span>Pitch multiplier</span><b data-o="mult">1.000</b></div>
        <div><span>Roof surface area</span><b data-o="surface">0</b></div>
        <div><span>Squares to order (with waste)</span><b data-o="order">0</b></div>
        <div><span>Shingle bundles (3 per square)</span><b data-o="bundles">0</b></div>
        <div><span>Rough replacement cost</span><b data-o="cost">—</b></div>
      </div>
      <p class="out-msg" data-o="steep"></p>
    </div>
  </div>
</div>"""

DEDUCT = """
<div class="tool" data-tool="deduct">
  <div class="tool-head"><span>Percentage deductible calculator</span><i>Percentage vs. flat</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling coverage (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="340000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Percentage deductible</label><select id="w-p" name="pct"><option value="1">1% (wind/hail)</option><option value="2" selected>2% (wind/hail)</option><option value="5">5% (wind/hail or earthquake)</option><option value="10">10% (earthquake)</option><option value="15">15% (earthquake)</option></select><span class="hint">Wind/hail percentages are common; earthquake endorsements often use 5–15%.</span></div>
        <div><label for="w-f">All-other-perils flat deductible</label><input id="w-f" name="flat" inputmode="decimal" value="1000"></div>
      </div>
      <div><label for="w-l">Estimated storm damage</label><input id="w-l" name="loss" inputmode="decimal" value="18900"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your percentage deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span style="background:#002d65"></span><span style="background:#c9d3e2"></span></div>
      <div class="legend"><span><i style="background:#002d65"></i>You pay</span><span><i style="background:#c9d3e2"></i>Policy pays</span></div>
      <div class="out-rows">
        <div><span>Payment with % deductible</span><b data-o="pdpay">$0</b></div>
        <div><span>Payment if the flat deductible applied</span><b data-o="flatpay">$0</b></div>
        <div><span>Extra out-of-pocket from % deductible</span><b data-o="diff">$0</b></div>
      </div>
      <p class="out-msg" data-o="below"></p>
    </div>
  </div>
</div>"""

DATES = """
<div class="tool" data-tool="dates">
  <div class="tool-head"><span>Tennessee claim deadline calendar</span><i>Exports to your calendar</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
      <p class="hint" style="margin:0">Adjust each window to match your policy. Defaults are common figures, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="3"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="14"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Often 60 days from the carrier’s request.</span></div>
        <div><label for="t-r">Depreciation recovery (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="365"></div>
        <div><label for="t-s">Suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="730"><span class="hint">Many forms use one or two years (365 or 730 days). Check yours.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download .ics calendar file</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the insurer accepted coverage for at least part of the loss?", "Get written confirmation that coverage is accepted. If the claim was denied, talk to a Tennessee attorney before considering appraisal."),
    (3, "Do you have the carrier’s complete, itemized estimate?", "Request the full line-item estimate (not just the summary) in writing."),
    (3, "Do you have your own itemized estimate from a contractor or estimator?", "Get an independent, line-item estimate — a lump-sum bid won’t hold up before a panel."),
    (2, "Do you have dated photos of the damage taken soon after the loss?", "Gather every photo you have and note when each was taken. Add new photos of current conditions."),
    (2, "Have you read your policy’s appraisal clause?", "Find the ‘Appraisal’ paragraph in the conditions section and note any deadlines."),
    (2, "Do you know your policy’s suit-limitation date?", "Locate the ‘Suit Against Us’ clause and calendar the date — our deadline calendar can help."),
    (2, "Have temporary repairs been made and receipts saved?", "Complete reasonable temporary repairs and keep every receipt."),
    (1, "Do you have your declarations page?", "Download or request your current declarations page."),
    (2, "Is all hidden damage opened up and documented?", "Make sure wet walls, attics and decking have been inspected so the scope is complete."),
    (1, "Is your correspondence with the carrier organized by date?", "Collect emails, letters and claim notes in date order."),
    (2, "Is the gap between estimates more than about 10% or $5,000?", "Run the numbers in our claim gap estimator — a small gap may not justify appraisal costs."),
    (1, "Has a sworn proof of loss been submitted if the carrier asked for one?", "If a proof of loss was requested, submit it on time."),
]

READY = """
<div class="tool tool-wide" data-tool="ready">
  <div class="tool-head"><span>Appraisal readiness check</span><i>12 questions · about two minutes</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <ol class="quiz">""" + "".join(
    '<li data-w="%d" data-fix="%s"><span>%s</span><span class="yn"><button type="button" class="yes" aria-pressed="false">Yes</button><button type="button" class="no" aria-pressed="false">No</button></span></li>' % (w, f, q)
    for w, q, f in _QUIZ) + """
      </ol>
      <div class="btn-row"><button type="button" class="btn ghost small" data-reset>Reset answers</button></div>
    </div>
    <div class="tool-out" aria-live="polite" style="grid-template-columns:minmax(220px,300px) 1fr;align-items:start">
      <div>
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#e6ecf5" stroke-width="18"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#cc0000" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3" style="transition:stroke-dashoffset .5s,stroke .3s"/></svg>
        <div class="gauge-num"><span data-o="score">–</span></div>
        <p class="hint" style="text-align:center">Answered <span data-o="count">0 / 12</span></p>
      </div>
      <div>
        <p class="out-msg" data-o="verdict"></p>
        <p class="todo-h">Your to-do list</p>
        <ul data-o="todo" style="margin:0;padding-left:1.1em"></ul>
      </div>
    </div>
  </div>
</div>"""

TREE = """
<div class="tool" data-tool="tree">
  <div class="tool-head"><span>Tree &amp; debris allowance calculator</span><i>Illustrative policy limits</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="tr-s">Where did the tree land?</label><select id="tr-s" name="scene"><option value="hit" selected>On the house or another covered structure</option><option value="block">Across the driveway or an accessibility ramp</option><option value="yard">In the yard — nothing damaged or blocked</option></select></div>
      <div class="row2">
        <div><label for="tr-n">Trees down</label><input id="tr-n" name="trees" inputmode="numeric" value="2"></div>
        <div><label for="tr-c">Removal cost per tree ($)</label><input id="tr-c" name="cost" inputmode="decimal" value="1800"><span class="hint">Crane jobs often cost far more.</span></div>
      </div>
      <div class="row2">
        <div><label for="tr-p">Policy limit per tree ($)</label><input id="tr-p" name="pertree" inputmode="decimal" value="500"></div>
        <div><label for="tr-cap">Limit per loss ($)</label><input id="tr-cap" name="cap" inputmode="decimal" value="1000"></div>
      </div>
      <div class="row2">
        <div><label for="tr-a">Dwelling coverage (Coverage A)</label><input id="tr-a" name="cova" inputmode="decimal" value="290000"></div>
        <div><label for="tr-d">Building damage estimate ($)</label><input id="tr-d" name="damage" inputmode="decimal" value="36500"></div>
      </div>
      <span class="hint">Defaults are illustrative figures similar to many standard homeowner forms. Your policy’s numbers control.</span>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Likely tree removal allowance</small><b data-o="allow">$0</b></div>
      <div class="out-rows">
        <div><span>Estimated removal cost</span><b data-o="removal">$0</b></div>
        <div><span>Removal cost not covered</span><b data-o="oop">$0</b></div>
        <div><span>Damage + debris, before deductible</span><b data-o="paid">$0</b></div>
        <div><span>Extra debris amount if limit is exhausted (5% of Cov. A)</span><b data-o="extra">$0</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

_T = "/tennessee-claim-tools/"

TOOLS = [
    {
        "slug": "claim-gap-calculator", "name": "Claim Gap & Fee Estimator", "icon": "Δ", "kind": "Calculator", "markup": GAP_FULL,
        "short": "Measure the dispute, test where an award could land and subtract appraiser and umpire fees to see your net.",
        "title": "Claim Gap & Appraisal Fee Estimator | Free Tool",
        "desc": "Free claim gap estimator: compare your estimate with the insurer’s, test possible awards and subtract appraisal fees to see your net.",
        "h1": "Claim Gap and Appraisal Fee Estimator",
        "lede": "Before you spend money on appraisal, check whether the math works. Enter both estimates, slide the likely award and add realistic fees to see what you might actually net.",
        "explain": f"""
<h2>Reading the result</h2>
<ol><li><strong>Amount in dispute</strong> is simply your estimate minus the carrier’s, both at replacement cost.</li>
<li><strong>Projected award</strong> assumes the panel lands at the percentage you choose between the two numbers.</li>
<li><strong>Net increase</strong> subtracts your appraiser’s fee and, if you tick the box, half of the umpire’s fee.</li></ol>
<h2>Stress-test the slider</h2>
<p>Run the estimator at 30%, 50% and 70%. A file that only makes sense at 90% is fragile; one that still nets a meaningful amount at 40% is usually worth a professional look. All figures shown are illustrative.</p>
<h2>What it leaves out</h2>
<p>Deductibles, depreciation timing and policy limits change what you’re paid, not the size of the dispute. For those, use the <a href="{_T}rcv-acv-holdback-calculator/">RCV/ACV holdback calculator</a> and the <a href="{_T}percentage-deductible-calculator/">percentage deductible calculator</a>.</p>
""",
        "faqs": [("Is the projected award a prediction?", "No. It’s a scenario you set with the slider. Real awards depend on documentation, the panel and the policy."), ("How are appraiser fees usually structured?", "Some appraisers charge a flat or hourly fee; others charge a percentage of the increase. Get the arrangement in writing before work starts.")],
    },
    {
        "slug": "rcv-acv-holdback-calculator", "name": "RCV/ACV Holdback Calculator", "icon": "ACV", "kind": "Calculator", "markup": DEP,
        "short": "List damaged items by age and life to estimate your first check, the depreciation held back and the full payout.",
        "title": "RCV vs ACV Depreciation & Holdback Calculator",
        "desc": "RCV vs ACV calculator: enter items with age and life expectancy to estimate your first check, recoverable depreciation and full payout.",
        "h1": "RCV vs. ACV Depreciation and Holdback Calculator",
        "lede": "Replacement cost policies usually pay twice: an actual cash value check now, then the held-back depreciation once repairs are done. Build your item list and see how the money splits.",
        "explain": f"""
<h2>The method behind the numbers</h2>
<p>Each line uses straight-line depreciation: age divided by expected life, capped at the maximum you pick. Carrier estimates may use condition adjustments or treat some charges as non-depreciable, so treat the output as a planning figure.</p>
<h2>Useful life ranges</h2>
<div class="table-wrap"><table><thead><tr><th>Item</th><th>Typical range</th></tr></thead><tbody>
<tr><th>Architectural asphalt shingles</th><td>25–30 years</td></tr><tr><th>Three-tab shingles</th><td>18–25 years</td></tr><tr><th>Standing-seam metal roof</th><td>40–60 years</td></tr><tr><th>Interior paint</th><td>8–12 years</td></tr><tr><th>Carpet</th><td>8–12 years</td></tr><tr><th>Central HVAC condenser</th><td>12–18 years</td></tr>
</tbody></table></div>
<h2>Collecting the holdback</h2>
<p>Most policies release recoverable depreciation after repairs are finished within a stated time. Send final invoices and photos. The <a href="{_T}claim-deadline-calendar/">claim deadline calendar</a> can remind you before the window closes.</p>
""",
        "faqs": [("Can labor be depreciated?", "Treatment of labor depreciation varies by policy form and by court decisions in different jurisdictions. Ask the carrier to explain in writing how labor was handled in your estimate."), ("What happens if I don’t repair?", "Under most replacement cost policies, you keep the ACV payment but may not collect the held-back depreciation.")],
    },
    {
        "slug": "roof-area-pitch-calculator", "name": "Roof Area & Pitch Calculator", "icon": "▲", "kind": "Calculator", "markup": ROOF,
        "short": "Turn a footprint into true roof squares using pitch, overhang and waste, then compare with the estimate.",
        "title": "Roof Area & Pitch Calculator for Roof Claims",
        "desc": "Roof area and pitch calculator for insurance claims: convert a footprint into true squares with waste, then check the estimate’s numbers.",
        "h1": "Roof Area and Pitch Calculator for Roof Claims",
        "lede": "Undercounted squares quietly shrink many roof settlements. Use your footprint, overhang and pitch to estimate true roof area, then hold it up against the carrier’s figures.",
        "explain": """
<h2>The pitch multiplier</h2>
<p>Roof surface grows with slope. The multiplier is √(1 + (rise ÷ 12)²). A 6/12 roof is about 12% larger than its footprint; an 8/12 roof about 20% larger; a 12/12 roof about 41% larger.</p>
<h2>Checking an estimate against your result</h2>
<ul><li>Find total squares and the waste percentage in the roof section of the carrier’s estimate.</li>
<li>Compare against the figures here; a difference above 5–10% is worth a closer look.</li>
<li>Look for steep-slope charges (often starting around 7/12) and high-roof charges on two-story sections.</li>
<li>Confirm starter, ridge cap, drip edge and valley lining appear as separate lines.</li></ul>
<h2>When a footprint isn’t enough</h2>
<p>Roofs with several pitches, dormers and valleys need plane-by-plane measuring. A field measurement or aerial report will always be more precise; this calculator is a sanity check.</p>
""",
        "faqs": [("What’s a roofing square?", "100 square feet of roof surface. Many Tennessee single-family homes fall between 20 and 45 squares."), ("Why does the waste factor change?", "Hips, valleys and dormers require more cuts, so more material is wasted than on a simple gable.")],
    },
    {
        "slug": "percentage-deductible-calculator", "name": "Percentage Deductible Calculator", "icon": "%", "kind": "Calculator", "markup": DEDUCT,
        "short": "See a wind/hail or earthquake percentage deductible in dollars and what a claim would actually pay.",
        "title": "Percentage Deductible Calculator | Wind, Hail, Quake",
        "desc": "Percentage deductible calculator: turn a wind/hail or earthquake deductible into dollars and compare the payout with a flat deductible.",
        "h1": "Percentage Deductible Calculator for Wind, Hail and Earthquake",
        "lede": "A 2% deductible sounds small until you multiply it by your dwelling limit. Earthquake endorsements in West Tennessee can run far higher. See your deductible in real dollars.",
        "explain": """
<h2>Two kinds of percentage deductibles in Tennessee</h2>
<p>Some Tennessee homeowner policies carry a separate <strong>wind/hail deductible</strong> calculated as a percentage of Coverage A — often 1% or 2%, sometimes more. Owners who buy an <strong>earthquake endorsement</strong>, most common near the New Madrid Seismic Zone in West Tennessee, usually face a percentage deductible as well, frequently in the 5% to 15% range. Both are illustrated here.</p>
<h2>Finding your deductible</h2>
<p>The declarations page lists each deductible. Look for “wind/hail,” “windstorm,” or “earthquake.” The endorsement itself explains exactly when the percentage applies.</p>
<h2>Why it matters for appraisal</h2>
<p>A deductible doesn’t change the amount of loss a panel decides, but it changes what lands in your account. A loss only slightly above the deductible may not justify appraisal costs; one well above it may.</p>
""",
        "faqs": [("Is the percentage based on the loss or my coverage?", "Usually on Coverage A, the dwelling limit, not on the size of the loss. Check your endorsement’s wording."), ("Is earthquake coverage included in my homeowner policy?", "Generally no. Standard policies exclude earth movement; earthquake coverage is added by endorsement or a separate policy.")],
    },
    {
        "slug": "claim-deadline-calendar", "name": "Claim Deadline Calendar", "icon": "◷", "kind": "Planner", "markup": DATES,
        "short": "Map notice, proof-of-loss, holdback and suit-limitation dates from your date of loss, then export to a calendar.",
        "title": "Tennessee Claim Deadline Calendar | .ics Export",
        "desc": "Tennessee claim deadline calendar: map proof-of-loss, depreciation and suit-limitation dates from your date of loss and export to .ics.",
        "h1": "Tennessee Insurance Claim Deadline Calendar",
        "lede": "Policy deadlines keep running while you dispute the number. Enter your date of loss and your policy’s windows, then download every milestone straight into your calendar.",
        "explain": """
<h2>Deadlines worth protecting</h2>
<ul><li><strong>Prompt notice.</strong> Policies require notice “as soon as practical” or similar. Late notice is a common carrier defense.</li>
<li><strong>Proof of loss.</strong> If the carrier asks for a sworn proof of loss, many forms allow 60 days to return it.</li>
<li><strong>Holdback recovery.</strong> Replacement cost policies typically require repairs within a stated period to recover depreciation.</li>
<li><strong>Suit limitation.</strong> Many property policies contain a contractual limit on when you can sue, often measured from the date of loss. Courts generally enforce these provisions, so calendar yours and don’t assume appraisal pauses it.</li></ul>
<div class="note"><b class="h">Planning only</b>This calendar uses the numbers you enter. It isn’t legal advice, and policy deadlines can be interpreted differently. If one is near, talk with a Tennessee attorney promptly.</div>
""",
        "faqs": [("Which date is the date of loss?", "Usually the date the storm or event happened, not the date you noticed damage. Weather reports for your address can confirm it."), ("Does appraisal stop the suit-limitation clock?", "Not automatically. Some policies or written agreements address it, but many don’t. Protect the deadline separately.")],
    },
    {
        "slug": "appraisal-readiness-check", "name": "Appraisal Readiness Check", "icon": "✓", "kind": "Checklist", "markup": READY,
        "short": "Twelve yes/no questions that score your claim file and build a to-do list before you demand appraisal.",
        "title": "Appraisal Readiness Check | Is Your Claim Ready?",
        "desc": "Appraisal readiness check: twelve quick questions score your property claim file and build a to-do list before you demand appraisal.",
        "h1": "Appraisal Readiness Check for Your Claim File",
        "lede": "Appraisal rewards preparation. Answer twelve questions to score your file, spot the gaps and get a short list of what to finish before anyone sends a demand letter.",
        "explain": """
<h2>How the questions are weighted</h2>
<p>Coverage, estimates and evidence carry the most weight because they decide whether appraisal fits at all and how well your number will hold. Paperwork items matter too, but they’re quicker to fix.</p>
<h2>Using your score</h2>
<ul><li><strong>75 or more:</strong> a solid file. A professional review of the dollar gap is the logical next step.</li>
<li><strong>45 to 74:</strong> close the open items first; each one strengthens your position.</li>
<li><strong>Under 45:</strong> demanding appraisal now risks locking in a low number. Build the file first.</li></ul>
""",
        "faqs": [("Is anything I enter saved?", "No. The check runs entirely in your browser and nothing is stored or sent."), ("Can I bring my results to a consultation?", "Yes. A screenshot of your score and to-do list is a useful starting point for a conversation.")],
    },
    {
        "slug": "tree-debris-allowance-calculator", "name": "Tree & Debris Allowance Calculator", "icon": "♣", "kind": "Calculator", "markup": TREE,
        "short": "New for Tennessee storms: see how tree-removal limits and debris coverage apply to where the tree landed.",
        "title": "Tree Removal & Debris Allowance Calculator",
        "desc": "Tree removal and debris allowance calculator: see how per-tree limits and debris coverage apply when a storm drops trees on your property.",
        "h1": "Tree Removal and Debris Allowance Calculator",
        "lede": "Tennessee’s ice storms and squall lines drop a lot of trees. What the policy pays to remove them depends on where they landed. Try the common scenarios with illustrative limits.",
        "explain": """
<h2>Three scenarios, three answers</h2>
<ul><li><strong>Tree hits the house or another covered structure.</strong> Removing the tree from the structure is generally treated as part of the covered loss. Many forms add extra debris-removal coverage — often 5% of the dwelling limit — if the loss plus debris exceeds the limit.</li>
<li><strong>Tree blocks a driveway or accessibility ramp.</strong> Many homeowner forms pay a limited amount per tree, with a cap per loss. The defaults here use $500 per tree and $1,000 per loss as illustrations.</li>
<li><strong>Tree falls in the yard and hits nothing.</strong> Removal usually isn’t covered.</li></ul>
<h2>Why this matters after Tennessee storms</h2>
<p>After an ice storm or derecho, tree crews are in heavy demand and crane work on tight urban lots can be expensive. Knowing which costs fall under the loss and which hit a small allowance helps you plan and spot an estimate that lumps everything into one low line.</p>
<div class="note"><b class="h">Illustrative figures</b>Limits vary by carrier and policy form. Check the “Trees, Shrubs and Other Plants” and “Debris Removal” sections of your own policy.</div>
""",
        "faqs": [("Is stump removal included?", "Usually not. Policies typically cover removing the debris, not grinding stumps or replanting."), ("Does the deductible apply to tree removal?", "Typically the deductible applies to the loss as a whole. How it interacts with tree allowances depends on the policy wording.")],
    },
]
