"""Free claim tools: markup + explanatory copy. Calculation logic lives in static/assets/js/app.js."""

T = "/calculators-and-planners/"

GAP_FULL = """
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Claim gap &amp; fee estimator</span><i>Runs in your browser</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Carrier’s estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="16800"><span class="hint">Replacement cost total before depreciation.</span></div>
        <div><label for="g-own">Your estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="29400"><span class="hint">Contractor’s or independent line-item estimate.</span></div>
      </div>
      <div><label for="g-land">Where might the award land inside the gap?</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% = the carrier’s figure holds. 100% = your full figure is awarded.</span></div>
      <div class="row2">
        <div><label for="g-ft">Your appraiser’s fee basis</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of the increase (%)</option><option value="hourly">Hourly (rate × hours)</option></select></div>
        <div><label for="g-fee">Fee amount or hourly rate</label><input id="g-fee" name="fee" inputmode="decimal" value="2400"></div>
      </div>
      <div data-hours hidden><label for="g-hrs">Estimated hours</label><input id="g-hrs" name="hours" inputmode="decimal" value="14"></div>
      <label class="check"><input type="checkbox" name="useump" checked> Include my half of an umpire’s fee</label>
      <div><label for="g-ump">Umpire’s total fee (usually split 50/50)</label><input id="g-ump" name="umpire" inputmode="decimal" value="3200"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated net increase to you</small><b data-o="net">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s1"></span><span class="s2"></span><span class="s3"></span></div>
      <div class="legend"><span><i class="s1"></i>Carrier’s figure</span><span><i class="s2"></i>Your net gain</span><span><i class="s3"></i>Appraisal costs</span></div>
      <div class="out-rows">
        <div><span>Amount in dispute</span><b data-o="gap">$0</b></div>
        <div><span>Gap as a share of the carrier’s figure</span><b data-o="pct">—</b></div>
        <div><span>Projected award (RCV)</span><b data-o="award">$0</b></div>
        <div><span>Gross increase</span><b data-o="gain">$0</b></div>
        <div><span>Your appraisal costs</span><b data-o="cost">$0</b></div>
        <div><span>Net return per $1 of fees</span><b data-o="ratio">—</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

GAP_MINI = """
<div class="tool tool-mini" data-tool="gap">
  <div class="tool-head"><span>Two-number gap check</span><i>No sign-up</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="m-ins">Carrier’s estimate</label><input id="m-ins" name="insurer" inputmode="decimal" value="12900"></div>
      <div><label for="m-own">Your contractor’s estimate</label><input id="m-own" name="yours" inputmode="decimal" value="24300"></div>
      <div><label for="m-land">Award lands at</label><div class="range"><input id="m-land" type="range" name="land" min="0" max="100" step="5" value="50" data-unit="%"><output>50%</output></div><span class="hint">of the disputed amount</span></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Amount in dispute</small><b data-o="gap">$0</b></div>
      <div class="out-rows">
        <div><span>Gap vs. carrier’s figure</span><b data-o="pct">—</b></div>
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
  <div class="tool-head"><span>RCV / ACV &amp; holdback calculator</span><i>Add as many line items as you need</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Laminated shingle roof", 17200, 8, 30), ("Gutters and downspouts", 1650, 8, 25), ("Interior drywall and paint", 2900, 5, 12)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn ghost small" data-add data-run>+ Add line item</button></div>
      <div class="row3">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="2500"></div>
        <div><label for="d-cap">Depreciation cap</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="90">90%</option></select></div>
        <div><label for="d-lab">Labor share of cost</label><select id="d-lab" name="labor"><option value="30">30%</option><option value="40" selected>40%</option><option value="50">50%</option></select></div>
      </div>
      <label class="check"><input type="checkbox" name="nolabor"> Depreciate materials only (leave labor undepreciated)</label>
      <label class="check"><input type="checkbox" name="nonrec"> My policy pays actual cash value only (no recoverable depreciation)</label>
    </div>
    <div class="tool-out tool-out-grid" aria-live="polite">
      <div class="out-big"><small>First check (ACV − deductible)</small><b data-o="first">$0</b></div>
      <div class="out-big"><small>Held back until repairs</small><b data-o="held">$0</b></div>
      <div class="out-big"><small>Total if fully recovered</small><b data-o="total">$0</b></div>
      <div class="out-rows span-all">
        <div><span>Replacement cost (RCV)</span><b data-o="rcv">$0</b></div>
        <div><span>Total depreciation</span><b data-o="dep">$0</b></div>
        <div><span>Depreciation as a share of RCV</span><b data-o="deppct">0%</b></div>
        <div><span>Actual cash value (ACV)</span><b data-o="acv">$0</b></div>
      </div>
    </div>
  </div>
</div>"""

ROOF = """
<div class="tool" data-tool="roof">
  <div class="tool-head"><span>Roof pitch &amp; squares calculator</span><i>Check the carrier’s measurements</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <fieldset class="bare"><legend class="sr-only">Measurement method</legend>
        <div class="btn-row">
          <label class="check"><input type="radio" name="mode" value="dims" checked> Footprint length × width</label>
          <label class="check"><input type="radio" name="mode" value="area"> I know the footprint area</label>
        </div></fieldset>
      <div class="row2" data-mode="dims">
        <div><label for="r-l">Footprint length (ft)</label><input id="r-l" name="len" inputmode="decimal" value="62"></div>
        <div><label for="r-w">Footprint width (ft)</label><input id="r-w" name="wid" inputmode="decimal" value="36"></div>
      </div>
      <div data-mode="dims"><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="16"></div>
      <div data-mode="area" hidden><label for="r-a">Footprint area incl. overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="2400"></div>
      <div class="row2">
        <div><label for="r-p">Roof pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 7 else "", p) for p in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16]) + """</select></div>
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="10">10% — plain gable</option><option value="13" selected>13% — gable with valleys</option><option value="15">15% — hip roof</option><option value="18">18% — cut-up / many facets</option></select></div>
      </div>
      <div class="row2">
        <div><label for="r-st">Stories at the eave</label><select id="r-st" name="stories"><option value="1" selected>One story</option><option value="2">Two stories or more</option></select></div>
        <div><label for="r-pr">Installed price per square (optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 560"></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Roof squares (before waste)</small><b data-o="sq">0</b></div>
      <div class="out-rows">
        <div><span>Pitch multiplier</span><b data-o="mult">1.000</b></div>
        <div><span>Roof surface area</span><b data-o="surface">0</b></div>
        <div><span>Squares with waste</span><b data-o="order">0</b></div>
        <div><span>Shingle bundles (3 per square)</span><b data-o="bundles">0</b></div>
        <div><span>Approx. eave + rake drip edge</span><b data-o="edge">—</b></div>
        <div><span>Rough replacement cost</span><b data-o="cost">—</b></div>
      </div>
      <p class="out-msg" data-o="steep"></p>
    </div>
  </div>
</div>"""

DEDUCT = """
<div class="tool" data-tool="deduct">
  <div class="tool-head"><span>Percentage deductible calculator</span><i>See 1%, 2% and 5% side by side</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling coverage (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="310000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Your wind/hail deductible</label><select id="w-p" name="pct"><option value="1">1%</option><option value="2" selected>2%</option><option value="3">3%</option><option value="5">5%</option></select></div>
        <div><label for="w-f">All-other-perils flat deductible</label><input id="w-f" name="flat" inputmode="decimal" value="1500"></div>
      </div>
      <div><label for="w-l">Estimated storm damage (RCV)</label><input id="w-l" name="loss" inputmode="decimal" value="19800"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your percentage deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s3"></span><span class="s1"></span></div>
      <div class="legend"><span><i class="s3"></i>You absorb</span><span><i class="s1"></i>Policy pays</span></div>
      <div class="out-rows">
        <div><span>Payment with your % deductible</span><b data-o="pdpay">$0</b></div>
        <div><span>Payment if the flat deductible applied</span><b data-o="flatpay">$0</b></div>
        <div><span>Extra out-of-pocket from the % deductible</span><b data-o="diff">$0</b></div>
      </div>
      <div class="table-wrap compare"><table><thead><tr><th>Deductible</th><th>In dollars</th><th>Claim pays</th></tr></thead><tbody data-o="compare"></tbody></table></div>
      <p class="out-msg" data-o="below"></p>
    </div>
  </div>
</div>"""

DATES = """
<div class="tool" data-tool="dates">
  <div class="tool-head"><span>Claim timeline planner</span><i>Exports to your calendar (.ics)</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
        <div><label for="t-q">Date carrier requested proof of loss (optional)</label><input id="t-q" type="date" name="req"></div>
      </div>
      <p class="hint flush">Set each window to match your own policy. Defaults are common figures, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report the claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="2"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="10"></div>
        <div><label for="t-p">Proof of loss due (days after request)</label><input id="t-p" name="pol" inputmode="numeric" value="60"></div>
        <div><label for="t-a">Review the estimate &amp; decide on appraisal (days)</label><input id="t-a" name="appr" inputmode="numeric" value="90"></div>
        <div><label for="t-r">Recover depreciation by (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="180"></div>
        <div><label for="t-s">Policy suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="730"><span class="hint">Check your policy’s “Suit Against Us” wording.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download .ics calendar file</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the carrier accepted coverage for at least part of the loss in writing?", "Get written confirmation that coverage is accepted. If the claim was denied outright, speak with an Oklahoma attorney before thinking about appraisal."),
    (3, "Do you have the carrier’s full line-item estimate, not just a payment summary?", "Ask the adjuster for the complete itemized estimate, including the roof diagram or measurement report."),
    (3, "Do you have an independent line-item estimate (not a one-line bid)?", "Get an itemized estimate — a lump-sum contractor bid is hard to defend in front of an umpire."),
    (2, "Do you have dated photos from the days right after the storm or event?", "Pull every photo and video with its date. Add current photos and note anything that has worsened."),
    (2, "Do you know the date of loss and can you support it (storm report, hail map, NWS warning)?", "Pin down the storm date. Hail-swath reports or National Weather Service storm data can corroborate it."),
    (2, "Have you read the appraisal paragraph and the deductible section of your policy?", "Find the ‘Appraisal’ condition and the wind/hail deductible on the declarations page; note any time limits."),
    (2, "Do you know your policy’s suit-limitation date?", "Locate the ‘Suit Against Us’ condition and put the date on a calendar — our timeline planner can help."),
    (2, "Has hidden damage been opened up and documented (attic, decking, wall cavities)?", "Make sure the full scope is visible. Appraisers value what can be seen and measured."),
    (1, "Are temporary repairs done and receipts saved?", "Finish reasonable temporary repairs and keep every receipt and invoice."),
    (2, "Is the gap between estimates more than roughly 10% or several thousand dollars?", "Run the numbers in the claim gap & fee estimator — a small gap may be cheaper to close with a supplement."),
]

READY = """
<div class="tool tool-wide" data-tool="ready">
  <div class="tool-head"><span>Appraisal readiness check</span><i>10 questions · about two minutes</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <ol class="quiz">""" + "".join(
    '<li data-w="%d" data-fix="%s"><span>%s</span><span class="yn"><button type="button" class="yes" aria-pressed="false">Yes</button><button type="button" class="no" aria-pressed="false">No</button></span></li>' % (w, f, q)
    for w, q, f in _QUIZ) + """
      </ol>
      <div class="btn-row"><button type="button" class="btn ghost small" data-reset>Reset answers</button></div>
    </div>
    <div class="tool-out tool-out-split" aria-live="polite">
      <div class="grade-box">
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path class="g-track" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke-width="18"/><path class="g-arc" data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3"/></svg>
        <div class="gauge-num"><span data-o="score">–</span><small data-o="grade"></small></div>
        <p class="hint center">Answered <span data-o="count">0 / 10</span></p>
      </div>
      <div>
        <p class="out-msg" data-o="verdict"></p>
        <p class="todo-h">Your to-do list</p>
        <ul class="todo" data-o="todo"></ul>
      </div>
    </div>
  </div>
</div>"""

SCHED = """
<div class="tool" data-tool="sched">
  <div class="tool-head"><span>Roof payment schedule calculator</span><i>Illustrative schedules — check your endorsement</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="s-rcv">Roof replacement cost (RCV)</label><input id="s-rcv" name="rcv" inputmode="decimal" value="18600"></div>
        <div><label for="s-age">Roof age at date of loss (years)</label><input id="s-age" name="age" inputmode="decimal" value="11"></div>
      </div>
      <div><label for="s-sch">Payment schedule</label><select id="s-sch" name="sched"><option value="a" selected>Illustrative A — 100% to age 3, then −5% a year, floor 30%</option><option value="b">Illustrative B — 100% to age 1, then −6% a year, floor 25%</option><option value="c">Illustrative C — steps: 100% / 80% / 60% / 40% by age band</option><option value="custom">Custom — I know the percentage</option></select></div>
      <div data-custom hidden><label for="s-pct">Percent of roof RCV the schedule pays</label><input id="s-pct" name="pct" inputmode="decimal" value="55"></div>
      <div class="row2">
        <div><label for="s-cova">Coverage A (for a % deductible)</label><input id="s-cova" name="cova" inputmode="decimal" value="280000"></div>
        <div><label for="s-ded">Wind/hail deductible</label><select id="s-ded" name="ded"><option value="0">Flat amount below</option><option value="1" selected>1% of Coverage A</option><option value="2">2% of Coverage A</option><option value="5">5% of Coverage A</option></select></div>
      </div>
      <div><label for="s-flat">Flat deductible ($)</label><input id="s-flat" name="flat" inputmode="decimal" value="1000"><span class="hint">Used only when “Flat amount” is selected.</span></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated roof payment after deductible</small><b data-o="pay">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s1"></span><span class="s3"></span><span class="s4"></span></div>
      <div class="legend"><span><i class="s1"></i>Paid</span><span><i class="s3"></i>Deductible</span><span><i class="s4"></i>Reduced by schedule</span></div>
      <div class="out-rows">
        <div><span>Schedule percentage at this age</span><b data-o="pct">—</b></div>
        <div><span>Scheduled roof value</span><b data-o="val">$0</b></div>
        <div><span>Deductible applied</span><b data-o="ded">$0</b></div>
        <div><span>Reduction vs. full replacement cost</span><b data-o="cut">$0</b></div>
        <div><span>Your share of the roof replacement</span><b data-o="share">$0</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "claim-gap-fee-estimator", "name": "Claim Gap & Fee Estimator", "icon": "gap", "kind": "Calculator",
        "short": "Size the dispute, test where an award might land and subtract flat, percentage or hourly appraisal fees.",
        "title": "Claim Gap & Appraisal Fee Estimator | Oklahoma",
        "desc": "Free claim gap estimator: compare your estimate with the carrier’s, project an award and subtract appraisal fees to see a realistic net.",
        "h1": "Claim Gap and Appraisal Fee Estimator",
        "lede": "Two estimates, one slider and your fee arrangement. See whether appraisal is likely to leave you meaningfully ahead after costs — before you commit to it.",
        "markup": GAP_FULL,
        "explain": f"""
<h2>Reading the result</h2>
<p>The estimator answers one question: after paying your appraiser and half an umpire, how much more might you end up with? The <strong>net return per $1 of fees</strong> line is the quickest gut check. Below about 2-to-1, the dispute is thin; above 4-to-1, appraisal usually deserves a serious conversation.</p>
<h2>Test a range, not a single outcome</h2>
<p>Awards rarely land on either side’s opening figure. Run the slider at 30%, 55% and 80%. If your plan only works at the top of the range, the file probably needs better documentation first. If it still works near the bottom, the numbers are on your side.</p>
<h3>Comparing fee arrangements</h3>
<ul><li><strong>Flat fee:</strong> predictable; best on mid-sized, clearly scoped residential claims.</li>
<li><strong>Percentage of the increase:</strong> aligns incentives but costs more on large wins. Oklahoma practice varies, so read any agreement carefully.</li>
<li><strong>Hourly:</strong> common on commercial and complex losses where time is hard to predict.</li></ul>
<h2>What it leaves out</h2>
<p>Deductibles, depreciation timing and policy limits change what you’re paid, not the size of the dispute. For those, use the <a href="{T}rcv-acv-holdback-calculator/">RCV/ACV holdback calculator</a> and the <a href="{T}percentage-deductible-calculator/">percentage deductible calculator</a>.</p>
""",
        "faqs": [("Is the projected award a prediction?", "No. It’s a planning scenario based on numbers you enter. Real awards depend on documentation, the panel and your policy."), ("Who pays the umpire?", "Most appraisal clauses split the umpire’s fee equally between you and the carrier, with each side paying its own appraiser. Check your policy’s wording."), ("Are the default figures real claims?", "No. The starting numbers are illustrative only, so the tool shows a working example when it loads.")],
    },
    {
        "slug": "rcv-acv-holdback-calculator", "name": "RCV/ACV Holdback Calculator", "icon": "acv", "kind": "Calculator",
        "short": "List damaged items to estimate the first ACV check, recoverable holdback and total — with a labor depreciation toggle.",
        "title": "RCV vs ACV Depreciation & Holdback Calculator",
        "desc": "Free RCV vs ACV calculator: list items with age and life to estimate your first check, the depreciation holdback and the total once repaired.",
        "h1": "RCV / ACV Depreciation and Holdback Calculator",
        "lede": "Replacement cost policies usually pay twice: an actual cash value check now and the held-back depreciation after repairs. Enter line items to see how the money splits.",
        "markup": DEP,
        "explain": f"""
<h2>How depreciation is modeled</h2>
<p>Each line uses straight-line depreciation — age divided by expected life — limited by the cap you choose. Real estimates may use condition adjustments or treat some items, such as permits or debris removal, as non-depreciable, so treat the output as a planning figure.</p>
<h2>The labor question</h2>
<p>Whether labor can be depreciated has been argued in courts across the country, and answers differ by state, policy form and endorsement. The toggle lets you see the difference both ways. If labor depreciation is a large share of your holdback, ask the carrier to explain its basis in writing.</p>
<h2>Common life expectancies in estimates</h2>
<div class="table-wrap"><table><thead><tr><th>Item</th><th>Typical range</th></tr></thead><tbody>
<tr><th>Laminated (architectural) shingles</th><td>25–30 years</td></tr><tr><th>Impact-resistant Class 4 shingles</th><td>30+ years</td></tr><tr><th>Gutters and downspouts</th><td>20–30 years</td></tr><tr><th>Interior paint</th><td>8–12 years</td></tr><tr><th>Carpet</th><td>8–12 years</td></tr><tr><th>Central HVAC condenser</th><td>12–18 years</td></tr>
</tbody></table></div>
<h2>Collecting the holdback</h2>
<p>Most policies release recoverable depreciation once repairs are finished within a set window. Put that date on your calendar with the <a href="{T}claim-timeline-planner/">claim timeline planner</a>.</p>
""",
        "faqs": [("What if my roof is paid on a schedule instead?", "Many Oklahoma policies settle roofs on an age-based payment schedule rather than RCV/ACV. Use the roof payment schedule calculator for that situation."), ("What happens if I don’t repair?", "Under most replacement cost policies you keep the ACV payment but may not recover the held-back depreciation."), ("Is my data saved?", "No. Everything runs in your browser and nothing is stored or sent.")],
    },
    {
        "slug": "roof-pitch-squares-calculator", "name": "Roof Pitch & Squares Calculator", "icon": "roof", "kind": "Calculator",
        "short": "Turn a footprint into true roof squares with pitch, waste and drip edge — then compare with the carrier’s diagram.",
        "title": "Roof Pitch & Squares Calculator for Hail Claims",
        "desc": "Estimate roof squares from footprint, pitch and waste, plus drip edge and steep or high-roof flags, and compare them with your claim estimate.",
        "h1": "Roof Pitch and Squares Calculator for Storm Claims",
        "lede": "Short measurements quietly shrink roof claims. Use your home’s footprint and pitch to estimate true surface area, squares, bundles and edge metal.",
        "markup": ROOF,
        "explain": f"""
<h2>The math behind it</h2>
<p>Roof surface is always larger than the footprint underneath. The pitch multiplier is √(1 + (rise ÷ 12)²). A 7/12 roof is about 15.8% larger than its footprint; a 12/12 roof is about 41.4% larger.</p>
<h2>Checking the carrier’s roof section</h2>
<ul><li>Compare total squares and the waste percentage with the result here. Gaps over 5–10% deserve a second look.</li>
<li>Steep charges commonly start around 7/12 or 8/12; high-roof charges apply to two-story eaves.</li>
<li>Look for separate lines for starter, ridge cap, drip edge, valley metal and ice-and-water barrier.</li>
<li>If you have impact-resistant Class 4 shingles, confirm the estimate prices that product, not a standard shingle.</li></ul>
<h2>Where a footprint estimate falls short</h2>
<p>Multi-pitch roofs, dormers and porches need measuring plane by plane. An aerial report or field measurement will always beat a footprint calculation, so use this as a sanity check before a <a href="/appraiser-services/carrier-estimate-review/">professional estimate review</a>.</p>
""",
        "faqs": [("What’s a roofing square?", "One hundred square feet of roof surface. Many single-story brick ranch homes in Oklahoma fall somewhere around 20 to 35 squares, depending on pitch and layout."), ("Why does waste depend on roof shape?", "Hips, valleys and dormers require more cutting, so more material ends up as scrap.")],
    },
    {
        "slug": "percentage-deductible-calculator", "name": "Percentage Deductible Calculator", "icon": "pct", "kind": "Calculator",
        "short": "Convert a 1%, 2% or 5% wind/hail deductible into dollars and see what a storm claim would actually pay.",
        "title": "Percentage Wind & Hail Deductible Calculator",
        "desc": "Convert a percentage wind and hail deductible into real dollars and compare what a storm claim pays at 1%, 2% and 5% against a flat deductible.",
        "h1": "Percentage Wind and Hail Deductible Calculator",
        "lede": "A 2% deductible sounds small until you multiply it by your dwelling limit. See your deductible in dollars and how 1%, 2% and 5% change a storm claim.",
        "markup": DEDUCT,
        "explain": f"""
<h2>Why percentage deductibles catch people off guard</h2>
<p>In hail country, many homeowners policies carry a separate wind/hail deductible written as a percentage of Coverage A. On an illustrative $310,000 dwelling limit, 2% is $6,200 — even if the all-other-perils deductible is $1,500.</p>
<h2>Where to find yours</h2>
<p>Look on the declarations page for “wind/hail,” “windstorm or hail” or a similar label. The endorsement later in the policy explains when it applies.</p>
<h2>How it interacts with appraisal</h2>
<p>An appraisal panel decides the amount of loss; the deductible is subtracted afterward. A loss that barely clears a percentage deductible may not justify appraisal fees. Run the result through the <a href="{T}claim-gap-fee-estimator/">claim gap &amp; fee estimator</a> before deciding.</p>
""",
        "faqs": [("Does the percentage apply to the whole claim?", "It’s usually calculated from Coverage A but applied to the entire wind or hail loss, including other structures and contents. Policy wording controls."), ("Can I change it?", "Usually at renewal. A higher deductible lowers premium but raises your share of every storm loss.")],
    },
    {
        "slug": "claim-timeline-planner", "name": "Claim Timeline Planner", "icon": "cal", "kind": "Planner",
        "short": "Map notice, proof of loss, appraisal decision, holdback and suit dates from your date of loss — then export them.",
        "title": "Insurance Claim Timeline Planner with .ics Export",
        "desc": "Build an insurance claim timeline from your date of loss, with proof of loss, holdback and suit dates, then save it to your calendar.",
        "h1": "Insurance Claim Timeline Planner",
        "lede": "Policy deadlines keep running while you argue about the number. Enter your dates and windows to build a timeline you can download straight into your calendar.",
        "markup": DATES,
        "explain": """
<h2>The dates that matter most</h2>
<ul><li><strong>Prompt notice.</strong> Policies require you to report a loss promptly. Late reporting is one of the most common reasons claims get harder.</li>
<li><strong>Proof of loss.</strong> If the carrier asks for a sworn proof of loss, many policies allow 60 days from the request.</li>
<li><strong>Appraisal decision.</strong> Not a policy deadline — a self-set checkpoint so a disagreement doesn’t drift for months.</li>
<li><strong>Depreciation recovery.</strong> Replacement cost policies typically require repairs within a set window to release holdback.</li>
<li><strong>Suit limitation.</strong> Many policies limit when a lawsuit can be filed. Appraisal may not pause that clock.</li></ul>
<div class="note"><b class="h">Important</b>This planner uses only the numbers you enter. It isn’t legal advice, and courts can read deadlines differently. If one is close, talk to an Oklahoma attorney now.</div>
""",
        "faqs": [("Is the date of loss the day I noticed the damage?", "Usually it’s the date of the storm or event. Storm reports for your address can help pin it down."), ("Does demanding appraisal extend my suit deadline?", "Not automatically. Protect the suit-limitation date on its own track."), ("What does the .ics file do?", "It adds each milestone as an all-day event in Google Calendar, Outlook or Apple Calendar. The file is created in your browser.")],
    },
    {
        "slug": "appraisal-readiness-check", "name": "Appraisal Readiness Check", "icon": "chk", "kind": "Checklist",
        "short": "Ten yes/no questions grade your claim file and build a to-do list before you demand appraisal.",
        "title": "Appraisal Readiness Check | Grade Your Claim File",
        "desc": "Answer ten quick questions to grade how ready your property claim is for insurance appraisal and get a to-do list of what to finish first.",
        "h1": "Appraisal Readiness Check for Your Claim File",
        "lede": "Strong appraisals are built before the demand letter goes out. Ten quick questions grade your file and turn the gaps into a short to-do list.",
        "markup": READY,
        "explain": f"""
<h2>How the grade is weighted</h2>
<p>Coverage, estimates and evidence carry the most weight because they decide whether appraisal is the right tool and how well your figure will hold up. Paperwork items matter too, but they’re quicker to fix.</p>
<h2>What your grade means</h2>
<ul><li><strong>A or B:</strong> the file is in good shape. A professional look at the dollar gap is the logical next step.</li>
<li><strong>C:</strong> close the open items first; each one strengthens your position.</li>
<li><strong>D or F:</strong> demanding appraisal now could lock in a low number. Build the file, then decide.</li></ul>
<p>Pair the result with the <a href="{T}claim-gap-fee-estimator/">claim gap &amp; fee estimator</a> to see whether the money justifies the process.</p>
""",
        "faqs": [("Is anything I answer stored?", "No. The check runs entirely in your browser."), ("Can I share my result?", "Yes — screenshot the grade and to-do list and bring it to your first call.")],
    },
    {
        "slug": "roof-payment-schedule-calculator", "name": "Roof Payment Schedule Calculator", "icon": "sched", "kind": "Calculator",
        "short": "See how an age-based roof payment schedule and a percentage deductible shrink a hail claim on an older roof.",
        "title": "Roof Payment Schedule Calculator | Roof Age & Hail",
        "desc": "Estimate what an age-based roof payment schedule pays on a hail or wind claim after a percentage deductible, versus full replacement cost.",
        "h1": "Roof Payment Schedule Calculator for Older Roofs",
        "lede": "Many Oklahoma homeowners policies now pay roof claims on a schedule tied to roof age. Model an illustrative schedule — or enter your own percentage — to see what a claim would pay.",
        "markup": SCHED,
        "explain": f"""
<h2>What a roof payment schedule is</h2>
<p>A roof surfacing payment schedule (the name varies by carrier) replaces ordinary replacement cost settlement for the roof with a percentage that falls as the roof ages. A ten-year-old roof might be paid at well under full replacement cost even if the policy pays replacement cost for everything else.</p>
<div class="note"><b class="h">Illustrative schedules only</b>The three preset schedules are examples built for this tool, not any carrier’s actual table. Your endorsement’s table is what counts — enter its percentage with the Custom option.</div>
<h2>Where appraisal fits</h2>
<p>Appraisal can resolve the <em>amount of loss</em> — the full replacement cost of the roof and related items. It doesn’t rewrite the schedule. But because the schedule percentage applies to the appraised figure, an accurate replacement cost still matters. Measurement errors, missing accessories and the wrong shingle grade all shrink the base number.</p>
<h2>Roof age disputes</h2>
<p>Schedules make roof age a money question. Permits, invoices, real estate records and dated photos help establish when the roof was installed. Read more in our guide to <a href="/storm-claim-guides/roof-payment-schedules-and-cosmetic-exclusions/">roof payment schedules and cosmetic damage exclusions</a>.</p>
""",
        "faqs": [("Is a roof payment schedule the same as ACV?", "No. ACV subtracts depreciation that may be recoverable later. A schedule usually sets the final roof payment as a percentage, with nothing held back to recover."), ("Can appraisal change my schedule percentage?", "Generally no. Appraisal decides the amount of loss; the endorsement then applies its percentage to that figure."), ("How do I prove my roof’s age?", "Roofing invoices, permits, closing documents, inspection reports and dated photos are the usual evidence.")],
    },
]
