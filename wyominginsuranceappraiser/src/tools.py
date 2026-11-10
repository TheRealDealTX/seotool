"""Interactive claim tools: markup + explanatory copy. Logic lives in static/assets/js/app.js."""

GAP_FULL = """
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Award net-gain projector</span><i>Runs in your browser</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Insurer’s estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="21300"><span class="hint">Replacement cost total on the carrier’s estimate.</span></div>
        <div><label for="g-own">Your estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="34900"><span class="hint">Your contractor’s or independent estimate.</span></div>
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
      <div class="stack" aria-hidden="true"><span style="background:#d9cfc4"></span><span style="background:#d4621a"></span><span style="background:#2a1206"></span></div>
      <div class="legend"><span><i style="background:#d9cfc4"></i>Carrier’s number</span><span><i style="background:#d4621a"></i>Your net gain</span><span><i style="background:#2a1206"></i>Appraisal costs</span></div>
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
      <div><label for="m-ins">Insurer’s estimate</label><input id="m-ins" name="insurer" inputmode="decimal" value="16800"></div>
      <div><label for="m-own">Your contractor’s estimate</label><input id="m-own" name="yours" inputmode="decimal" value="29400"></div>
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
  <div class="tool-head"><span>ACV &amp; holdback worksheet</span><i>Add as many items as you need</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Architectural shingle roof", 21400, 11, 30), ("Fiber-cement siding — west wall", 6800, 14, 50), ("Window screens (12)", 960, 8, 20)]) + """
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
  <div class="tool-head"><span>Roof area, pitch &amp; waste</span><i>Compare against your estimate</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <fieldset style="border:0;padding:0;margin:0"><legend class="sr-only">Measurement method</legend>
        <div class="btn-row">
          <label class="check"><input type="radio" name="mode" value="dims" checked> Footprint length × width</label>
          <label class="check"><input type="radio" name="mode" value="area"> I know the footprint area</label>
        </div></fieldset>
      <div class="row2" data-mode="dims">
        <div><label for="r-l">Footprint length (ft)</label><input id="r-l" name="len" inputmode="decimal" value="62"></div>
        <div><label for="r-w">Footprint width (ft)</label><input id="r-w" name="wid" inputmode="decimal" value="36"></div>
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
  <div class="tool-head"><span>Deductible comparison</span><i>Percentage vs. flat</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling coverage (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="420000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Wind/hail percentage deductible</label><select id="w-p" name="pct"><option value="0.5">0.5%</option><option value="1">1%</option><option value="2" selected>2%</option><option value="3">3%</option><option value="5">5%</option></select></div>
        <div><label for="w-f">All-other-perils flat deductible</label><input id="w-f" name="flat" inputmode="decimal" value="1000"></div>
      </div>
      <div><label for="w-l">Estimated storm damage</label><input id="w-l" name="loss" inputmode="decimal" value="24800"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your percentage deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span style="background:#2a1206"></span><span style="background:#d9cfc4"></span></div>
      <div class="legend"><span><i style="background:#2a1206"></i>You pay</span><span><i style="background:#d9cfc4"></i>Policy pays</span></div>
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
  <div class="tool-head"><span>Wyoming claim timeline builder</span><i>Exports to your calendar</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
      <p class="hint" style="margin:0">Adjust each window to match your policy. Defaults are common figures, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="3"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="14"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Often 60 days from the carrier’s request.</span></div>
        <div><label for="t-r">Depreciation recovery (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="365"></div>
        <div><label for="t-s">Suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="730"><span class="hint">Check your policy: one or two years is common.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download .ics calendar file</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the insurer accepted coverage for at least part of the loss?", "Get written confirmation that coverage is accepted. If the claim was denied, talk to a Wyoming attorney before considering appraisal."),
    (3, "Do you have the carrier’s complete, itemized estimate?", "Request the full line-item estimate (not just the summary) in writing."),
    (3, "Do you have your own itemized estimate from a contractor or estimator?", "Get an independent, line-item estimate — a lump-sum bid won’t hold up before a panel."),
    (2, "Do you have dated photos of the damage taken soon after the loss?", "Gather every photo you have and note when each was taken. Add new photos of current conditions."),
    (2, "Have you read your policy’s appraisal clause?", "Find the ‘Appraisal’ paragraph in the conditions section and note any deadlines."),
    (2, "Do you know your policy’s suit-limitation date?", "Locate the ‘Suit Against Us’ clause and calendar the date — our timeline builder can help."),
    (2, "Have temporary repairs been made and receipts saved?", "Complete reasonable temporary repairs and keep every receipt."),
    (1, "Do you have your declarations page?", "Download or request your current declarations page."),
    (2, "Is all hidden damage opened up and documented?", "Make sure wet walls, attics and decking have been inspected so the scope is complete."),
    (1, "Is your correspondence with the carrier organized by date?", "Collect emails, letters and claim notes in date order."),
    (2, "Is the gap between estimates more than about 10% or $5,000?", "Run the numbers in our award net-gain projector — a small gap may not justify appraisal costs."),
    (1, "Has a sworn proof of loss been submitted if the carrier asked for one?", "If a proof of loss was requested, submit it on time."),
]

READY = """
<div class="tool tool-wide" data-tool="ready">
  <div class="tool-head"><span>Appraisal ready-meter</span><i>12 questions · about two minutes</i></div>
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
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#f6e6da" stroke-width="18"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#d4621a" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3" style="transition:stroke-dashoffset .5s,stroke .3s"/></svg>
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


_HAIL_ROW = """<tr><td><input name="slope" value="{0}" aria-label="Slope or elevation"></td><td><input name="sq" inputmode="decimal" value="{1}" aria-label="Squares on this slope"></td><td><input name="hits" inputmode="decimal" value="{2}" aria-label="Hail hits in test square"></td><td class="mono" data-o="ok">—</td><td><button type="button" class="x" aria-label="Remove slope">×</button></td></tr>"""

HAIL = """
<div class="tool tool-wide" data-tool="hail">
  <div class="tool-head"><span>Hail test-square scorer</span><i>One row per roof facet</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Slope / facet</th><th>Squares</th><th>Hits in 10×10 ft square</th><th>Meets threshold?</th><th></th></tr></thead><tbody>
      """ + "".join(_HAIL_ROW.format(*r) for r in [("West slope", 9.4, 14), ("North slope", 7.8, 9), ("East slope", 9.4, 5), ("South slope", 7.8, 3)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn ghost small" data-add data-run>+ Add facet</button></div>
      <div class="row2">
        <div><label for="h-th">Hits per test square to qualify</label><input id="h-th" name="thresh" inputmode="decimal" value="8"><span class="hint">Carriers often use 8–10. Ask yours which figure it applied.</span></div>
        <div><label for="h-pr">Price per square, installed (optional)</label><input id="h-pr" name="price" inputmode="decimal" placeholder="e.g. 560"></div>
      </div>
      <label class="check"><input type="checkbox" name="match"> The shingle can’t be matched (discontinued color or style)</label>
    </div>
    <div class="tool-out" aria-live="polite" style="grid-template-columns:repeat(auto-fit,minmax(200px,1fr))">
      <div class="out-big"><small>Squares on qualifying slopes</small><b data-o="qsq">0</b></div>
      <div class="out-big"><small>Share of the whole roof</small><b data-o="share">0%</b></div>
      <div class="out-big"><small>Rough cost of qualifying slopes</small><b data-o="cost">—</b></div>
      <div class="out-rows" style="grid-column:1/-1">
        <div><span>Facets that meet the threshold</span><b data-o="qn">0 of 0</b></div>
        <div><span>Total roof squares entered</span><b data-o="tsq">0</b></div>
        <div><span>Cost if every slope is replaced</span><b data-o="full">—</b></div>
      </div>
      <p class="out-msg" data-o="msg" style="grid-column:1/-1"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "award-net-gain-projector", "name": "Award Net-Gain Projector", "icon": "Δ$", "kind": "Calculator",
        "kw": "insurance appraisal calculator",
        "short": "Size the disputed amount, test where an award might land and subtract appraiser and umpire fees.",
        "title": "Insurance Appraisal Calculator | Award Net-Gain Projector",
        "desc": "Free insurance appraisal calculator: compare two estimates, test where an award could land and subtract appraiser and umpire fees to see your net.",
        "h1": "Insurance Appraisal Calculator: Award Net-Gain Projector",
        "lede": "Appraisal costs money on both sides. Enter the carrier’s number, your number and realistic fees to see what a range of awards would actually put in your pocket.",
        "markup": GAP_FULL,
        "explain": """
<h2>How to read the projection</h2>
<ol><li><strong>Start with replacement cost totals.</strong> Use the RCV line on both estimates, before depreciation and deductible.</li>
<li><strong>Test a range.</strong> Slide the landing point to 30%, 50% and 75%. If appraisal only pays off near 100%, the case is thin.</li>
<li><strong>Use real fees.</strong> Ask any appraiser — including us — for the fee in writing, and assume half of an umpire’s fee if the panel may need one.</li></ol>
<h2>An illustrative example</h2>
<p>Illustrative figures only: a carrier estimate of $21,300 against a contractor estimate of $34,900 leaves $13,600 in dispute. If an award lands at 60% of that gap, the increase is $8,160. Subtract a $2,500 flat appraiser fee and half of a $3,000 umpire fee and the net gain is $4,160. The same claim at 30% nets very little — which is why the slider matters more than any single number.</p>
<h2>What this projector ignores</h2>
<p>Deductibles, policy limits and depreciation timing change what you are paid, not the size of the dispute. Run the <a href="/free-calculators/acv-holdback-worksheet/">ACV &amp; holdback worksheet</a> and the <a href="/free-calculators/deductible-comparison/">deductible comparison</a> for those.</p>
""",
        "faqs": [("Is the projected award a prediction?", "No. It is a scenario you control. Real awards depend on documentation, the panel and your policy."), ("Should I pay an appraiser a percentage of the increase?", "Some appraisers charge that way, but many policies require an appraiser to be disinterested, and a contingency fee can be challenged. A flat or hourly fee avoids that argument.")],
    },
    {
        "slug": "acv-holdback-worksheet", "name": "ACV & Holdback Worksheet", "icon": "ACV", "kind": "Calculator",
        "kw": "RCV vs ACV calculator",
        "short": "List damaged items with age and life to estimate the first ACV check and the depreciation held back.",
        "title": "RCV vs ACV Calculator | Depreciation Holdback Worksheet",
        "desc": "Free RCV vs ACV calculator: enter damaged items with age and life expectancy to estimate your first check, recoverable depreciation and final total.",
        "h1": "RCV vs. ACV Calculator and Depreciation Holdback Worksheet",
        "lede": "Replacement cost policies usually pay in two installments. Itemize the loss to see how much arrives now, how much is held back and what you collect after repairs.",
        "markup": DEP,
        "explain": """
<h2>How the worksheet estimates depreciation</h2>
<p>It applies straight-line depreciation — age divided by expected life — up to the cap you choose. Carriers may adjust for condition or treat some items, like permits, as non-depreciable, so treat the result as a planning number.</p>
<h2>Life expectancies you’ll see in estimates</h2>
<div class="table-wrap"><table><thead><tr><th>Item</th><th>Common range</th></tr></thead><tbody>
<tr><th>Architectural asphalt shingles</th><td>25–30 years</td></tr><tr><th>Impact-resistant (Class 4) shingles</th><td>30+ years</td></tr><tr><th>Exposed-fastener metal roofing</th><td>30–40 years</td></tr><tr><th>Vinyl siding</th><td>25–40 years</td></tr><tr><th>Fiber-cement siding</th><td>40–50 years</td></tr><tr><th>Interior paint</th><td>8–12 years</td></tr>
</tbody></table></div>
<h2>Collecting the holdback</h2>
<p>Most replacement cost policies release recoverable depreciation after repairs are finished within a time limit. Send invoices and completion photos, and put the deadline on a calendar with the <a href="/free-calculators/claim-timeline-builder/">claim timeline builder</a>. Wyoming’s short building season can make a one-year window tight after a late-summer storm — ask for an extension in writing if you need one.</p>
""",
        "faqs": [("Is labor depreciated in Wyoming?", "Practices vary by carrier and policy, and courts in different states have reached different answers. Ask the carrier to explain in writing whether and how labor was depreciated."), ("What if I decide not to repair?", "Under most replacement cost policies you keep the actual cash value payment but give up the held-back depreciation.")],
    },
    {
        "slug": "roof-area-pitch-waste", "name": "Roof Area, Pitch & Waste Calculator", "icon": "▲", "kind": "Calculator",
        "kw": "roof squares calculator",
        "short": "Turn a footprint into true roof squares using pitch and waste, then check the estimate’s numbers.",
        "title": "Roof Squares Calculator | Pitch & Waste for Claims",
        "desc": "Free roof squares calculator for claims: turn footprint, pitch and waste into roof area, squares and bundles to check the carrier’s estimate.",
        "h1": "Roof Squares Calculator with Pitch and Waste",
        "lede": "Short measurements quietly shrink a roof claim. Use the footprint and pitch to estimate true surface area, then compare it with the squares on your estimate.",
        "markup": ROOF,
        "explain": """
<h2>The math behind the numbers</h2>
<p>Roof surface is the footprint multiplied by a pitch factor of √(1 + (rise ÷ 12)²). A 4/12 roof is about 5.4% larger than its footprint, a 6/12 roof about 11.8% larger, and a 12/12 roof about 41.4% larger. One square is 100 square feet.</p>
<h2>Comparing with the carrier’s estimate</h2>
<ul><li>Find total roof squares and the waste percentage in the roofing section.</li>
<li>Differences of more than 5–10% deserve a second look.</li>
<li>Look for steep and high-roof charges on steeper or two-story sections.</li>
<li>Check that starter, ridge cap, drip edge, ice and water shield and valley metal are listed. Ice and water shield at the eaves is often required by local code in snowy parts of Wyoming.</li></ul>
<h2>When a footprint isn’t enough</h2>
<p>Cut-up roofs with several pitches, dormers and valleys need to be measured plane by plane. Treat this as a sanity check, and rely on a field measurement or aerial report for the real number.</p>
""",
        "faqs": [("How many squares does a typical house have?", "A single-story Wyoming ranch might have 20 to 30 squares; a larger two-story with a complex roof can have 40 or more."), ("Why does waste vary?", "Hips, valleys and dormers require more cutting, so more material ends up as scrap. Simple gables waste the least.")],
    },
    {
        "slug": "deductible-comparison", "name": "Deductible Comparison Calculator", "icon": "%", "kind": "Calculator",
        "kw": "percentage deductible calculator",
        "short": "Convert a percentage wind/hail deductible to dollars and compare it with a flat deductible.",
        "title": "Percentage Deductible Calculator | Wind & Hail",
        "desc": "Free percentage deductible calculator: turn a wind/hail deductible into dollars and compare what a storm claim pays against a flat deductible.",
        "h1": "Percentage Deductible Calculator for Wind and Hail",
        "lede": "Many Wyoming policies carry a separate wind/hail deductible set as a percentage of dwelling coverage. See it in dollars and what it does to a storm payment.",
        "markup": DEDUCT,
        "explain": """
<h2>Why percentage deductibles catch people off guard</h2>
<p>A 1% or 2% deductible sounds small. On $420,000 of dwelling coverage, 2% is $8,400 — and in hail-prone parts of Wyoming, that deductible can apply to every hail and windstorm claim. Some policies use a percentage for wind and hail and a flat amount for everything else.</p>
<h2>Finding yours</h2>
<p>Look at the declarations page for “wind/hail,” “windstorm or hail” or a similar deductible line. The endorsement that creates it explains when it applies. Note whether it is triggered by any windstorm, which in Wyoming includes winter wind events, not only summer hail.</p>
<h2>What it means for appraisal</h2>
<p>A panel values the loss; the deductible comes off afterward. A dispute where both estimates sit near the deductible may not be worth appraising. One well above it may be.</p>
""",
        "faqs": [("Is the percentage based on my loss or my coverage?", "Usually on Coverage A, the dwelling limit, regardless of the size of the loss. Read the endorsement to confirm."), ("Can I change it?", "Usually at renewal. A lower deductible raises the premium; a higher one lowers it but increases your share of each storm loss.")],
    },
    {
        "slug": "claim-timeline-builder", "name": "Claim Timeline Builder", "icon": "◷", "kind": "Planner",
        "kw": "insurance claim deadline calculator",
        "short": "Map notice, proof-of-loss, holdback and suit dates from your date of loss and export an .ics file.",
        "title": "Insurance Claim Deadline Calculator | Timeline Builder",
        "desc": "Free insurance claim deadline calculator: enter your date of loss to map proof-of-loss, holdback and suit dates, then download them as an .ics file.",
        "h1": "Insurance Claim Deadline Calculator and Timeline Builder",
        "lede": "Deadlines keep running while a claim is in dispute. Enter your date of loss and your policy’s windows to build a timeline you can add to any calendar.",
        "markup": DATES,
        "explain": """
<h2>Deadlines worth protecting</h2>
<ul><li><strong>Prompt notice.</strong> Late notice is one of the most common defenses a carrier raises. Report losses as soon as you discover them.</li>
<li><strong>Proof of loss.</strong> If the carrier asks for a sworn proof of loss, policies commonly allow about 60 days to return it.</li>
<li><strong>Depreciation recovery.</strong> Replacement cost policies set a time limit to finish repairs and claim the holdback.</li>
<li><strong>Suit limitation.</strong> Most property policies limit the time to sue. One or two years from the loss is common, but read the “Suit Against Us” condition in your own policy. Appraisal does not automatically pause it.</li></ul>
<div class="note"><b class="h">Important</b>This builder uses the numbers you enter. It is not legal advice. If a deadline is close, contact a Wyoming-licensed attorney.</div>
""",
        "faqs": [("What date should I use as the date of loss?", "Usually the date the storm or event happened, not the date you noticed the damage. Local weather records can help pin it down."), ("Does the .ics file send my data anywhere?", "No. The calendar file is created in your browser and downloaded directly to your device.")],
    },
    {
        "slug": "appraisal-ready-meter", "name": "Appraisal Ready-Meter", "icon": "✓", "kind": "Checklist",
        "kw": "appraisal readiness checklist",
        "short": "Twelve yes-or-no questions that score your claim file and build a to-do list before a demand.",
        "title": "Appraisal Readiness Checklist | Ready-Meter Score",
        "desc": "A free appraisal readiness checklist: answer 12 questions to score your property claim file and get a to-do list before you demand appraisal.",
        "h1": "Appraisal Readiness Checklist: The Ready-Meter",
        "lede": "A panel can only work with the evidence in front of it. Answer twelve questions to see how complete your file is and what to tackle first.",
        "markup": READY,
        "explain": """
<h2>How the score is weighted</h2>
<p>Coverage, estimates and evidence carry the most weight, because they decide whether appraisal is the right tool and how well your number will hold up in front of an umpire. Paperwork items matter too, but they are easier to fix.</p>
<h2>Reading your result</h2>
<ul><li><strong>75 or higher:</strong> the file is in good shape. Have a professional review the dollar gap next.</li>
<li><strong>45 to 74:</strong> close the open items first — each one strengthens your number.</li>
<li><strong>Under 45:</strong> a demand now could lock in a low award. Build the file before you start.</li></ul>
""",
        "faqs": [("Is anything I answer stored?", "No. The checklist runs entirely in your browser and nothing is saved or sent."), ("Can I share the to-do list?", "Yes. Take a screenshot or copy the list and bring it to your consultation.")],
    },
    {
        "slug": "hail-test-square-scorer", "name": "Hail Test-Square Scorer", "icon": "▦", "kind": "Calculator",
        "kw": "hail test square calculator",
        "short": "Enter hits per test square on each roof facet to see which slopes qualify and how much roof that is.",
        "title": "Hail Test Square Calculator | Slope-by-Slope Scorer",
        "desc": "Free hail test square calculator: enter hits per 10×10 square on each roof slope to see which facets qualify, how many squares and a rough cost.",
        "h1": "Hail Test Square Calculator: Score Every Slope",
        "lede": "On Wyoming’s high plains hail usually rides a west wind, so one side of a roof takes most of the hits. Score each facet the way carriers do and see what share of the roof qualifies.",
        "markup": HAIL,
        "explain": """
<h2>What a test square is</h2>
<p>A test square is a 10-by-10-foot area (one roofing square) marked on a roof slope. The inspector counts hail hits that fracture the shingle mat or displace granules down to the asphalt inside that square. Many carriers approve replacement of a slope when the count reaches a threshold — often 8 to 10 hits — though guidelines vary and are not written into most policies.</p>
<h2>Why the direction of the storm matters</h2>
<p>In Laramie, Platte and Goshen counties, hail commonly arrives on a west or northwest wind. West and north slopes can be heavily damaged while east and south slopes barely qualify. Enter every facet separately — including small ones over porches and garages — rather than averaging across the roof.</p>
<h2>When the threshold isn’t the whole story</h2>
<ul><li>If the remaining slopes can’t be matched, your policy’s language on matching and uniform appearance may matter more than the count.</li>
<li>Older, brittle shingles may not survive spot repairs on a slope that doesn’t technically qualify.</li>
<li>Siding, windows, gutters and soft metals on the windward side often show damage even when shingle counts are low.</li></ul>
<p>Illustrative figures only: the default rows show a 34.4-square roof where the west and north slopes qualify at 8 hits — 17.2 squares, or 50% of the roof.</p>
""",
        "faqs": [("Is the 8-hit threshold in my policy?", "Usually not. It is a common carrier guideline. Ask the adjuster in writing what threshold was applied to your roof."), ("Should I count hits myself?", "Only if you can do it safely from the ground or with a professional. Roofs are dangerous; a contractor or appraiser can mark and photograph test squares for you.")],
    },
]
