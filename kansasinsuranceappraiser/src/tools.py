"""Interactive claim tools: markup + explanatory copy. Logic lives in static/assets/js/app.js."""

T = "/claim-calculators-kansas/"

GAP_FULL = """
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Appraisal payoff projector</span><i>Runs in your browser</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Insurer’s estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="16800"><span class="hint">Replacement cost total on the carrier’s estimate.</span></div>
        <div><label for="g-own">Your estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="29400"><span class="hint">Your contractor’s or independent estimate.</span></div>
      </div>
      <div><label for="g-land">Where might the award land within the gap?</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% = the carrier’s number holds. 100% = your full number is awarded.</span></div>
      <div class="row2">
        <div><label for="g-ft">Your appraiser’s fee type</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of increase (%)</option></select></div>
        <div><label for="g-fee">Fee amount</label><input id="g-fee" name="fee" inputmode="decimal" value="2200"></div>
      </div>
      <label class="check"><input type="checkbox" name="useump" checked> Include half of an umpire’s fee</label>
      <div><label for="g-ump">Umpire’s total fee (split 50/50)</label><input id="g-ump" name="umpire" inputmode="decimal" value="2800"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Projected net increase to you</small><b data-o="net">$0</b></div>
      <div class="stack" aria-hidden="true"><span style="background:#c9d3e6"></span><span style="background:#f1ad02"></span><span style="background:#002569"></span></div>
      <div class="legend"><span><i style="background:#c9d3e6"></i>Carrier’s number</span><span><i style="background:#f1ad02"></i>Your net gain</span><span><i style="background:#002569"></i>Appraisal costs</span></div>
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
  <div class="tool-head"><span>Two-number gap check</span><i>No sign-up</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="m-ins">Insurer’s estimate</label><input id="m-ins" name="insurer" inputmode="decimal" value="12900"></div>
      <div><label for="m-own">Your contractor’s estimate</label><input id="m-own" name="yours" inputmode="decimal" value="24600"></div>
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
  <div class="tool-head"><span>Holdback recovery calculator</span><i>Add as many items as you need</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Laminated shingle roof", 16200, 8, 30), ("Steel siding — two elevations", 5400, 15, 40), ("Seamless gutters", 1650, 12, 25)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn ghost small" data-add data-run>+ Add item</button></div>
      <div class="row2">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="2500"></div>
        <div><label for="d-cap">Maximum depreciation</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="90">90%</option></select><span class="hint">Many estimates cap depreciation; check yours.</span></div>
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
  <div class="tool-head"><span>Roof square footage &amp; pitch</span><i>Check the carrier’s measurements</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <fieldset class="plain"><legend class="sr-only">Measurement method</legend>
        <div class="btn-row">
          <label class="check"><input type="radio" name="mode" value="dims" checked> Footprint length × width</label>
          <label class="check"><input type="radio" name="mode" value="area"> I know the footprint area</label>
        </div></fieldset>
      <div class="row2" data-mode="dims">
        <div><label for="r-l">Footprint length (ft)</label><input id="r-l" name="len" inputmode="decimal" value="64"></div>
        <div><label for="r-w">Footprint width (ft)</label><input id="r-w" name="wid" inputmode="decimal" value="30"></div>
      </div>
      <div data-mode="dims"><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="16"></div>
      <div data-mode="area" hidden><label for="r-a">Footprint area incl. overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="2100"></div>
      <div class="row2">
        <div><label for="r-p">Roof pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 5 else "", p) for p in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16]) + """</select></div>
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="10" selected>10% — simple gable</option><option value="12">12% — gable with dormers</option><option value="15">15% — hip roof</option><option value="18">18% — complex / cut-up</option></select></div>
      </div>
      <div><label for="r-pr">Installed price per square (optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 480"><span class="hint">Use a local contractor’s quote for a rough replacement figure.</span></div>
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
  <div class="tool-head"><span>Percentage deductible converter</span><i>Wind/hail vs. flat</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling coverage (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="310000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Wind/hail deductible</label><select id="w-p" name="pct"><option value="0.5">0.5%</option><option value="1" selected>1%</option><option value="2">2%</option><option value="3">3%</option><option value="5">5%</option></select></div>
        <div><label for="w-f">All-other-perils flat deductible</label><input id="w-f" name="flat" inputmode="decimal" value="1500"></div>
      </div>
      <div><label for="w-l">Estimated hail or wind damage</label><input id="w-l" name="loss" inputmode="decimal" value="18200"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your percentage deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span style="background:#002569"></span><span style="background:#c9d3e6"></span></div>
      <div class="legend"><span><i style="background:#002569"></i>You pay</span><span><i style="background:#c9d3e6"></i>Policy pays</span></div>
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
  <div class="tool-head"><span>Claim timeline builder</span><i>Exports to your calendar</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
      <p class="hint" style="margin:0">Replace each window with the number in your own policy. Defaults are placeholders, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="2"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="10"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Often counted from the carrier’s request.</span></div>
        <div><label for="t-r">Depreciation recovery (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="180"></div>
        <div><label for="t-s">Suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="730"><span class="hint">Use the period in your “Suit Against Us” clause.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download .ics calendar file</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the insurer accepted coverage for at least part of the loss?", "Get written confirmation that coverage is accepted. If the claim was denied outright, talk to a Kansas attorney before thinking about appraisal."),
    (3, "Do you have the carrier’s complete, itemized estimate?", "Ask in writing for the full line-item estimate, not just the payment summary."),
    (3, "Do you have your own itemized estimate from a contractor or estimator?", "Get an independent line-item estimate. A one-line bid won’t hold up in front of a panel."),
    (2, "Do you have dated photos taken soon after the storm or event?", "Collect every photo and note the date each was taken. Add photos of current conditions."),
    (2, "Have you found and read the appraisal clause in your policy?", "Look in the Conditions section for the paragraph titled ‘Appraisal’ and note any deadlines."),
    (2, "Do you know the deadline in your policy’s ‘Suit Against Us’ clause?", "Find the clause and put the date on your calendar. The claim timeline builder can help."),
    (2, "Have temporary repairs been made, with receipts saved?", "Finish reasonable temporary repairs, such as tarps, and keep every receipt."),
    (1, "Do you have your current declarations page?", "Download it from your insurer’s portal or ask your agent."),
    (2, "Has hidden damage (decking, attic, wall cavities) been checked?", "Make sure wet insulation, decking and interior cavities are inspected so the scope is complete."),
    (1, "Is your correspondence with the insurer organized by date?", "Gather letters, emails and claim notes in date order."),
    (2, "Is the gap between estimates more than about 10% or $5,000?", "Run your numbers in the appraisal payoff projector. A small gap may not justify fees."),
    (1, "If a sworn proof of loss was requested, has it been sent on time?", "Return any requested proof of loss before the deadline in the request."),
]

READY = """
<div class="tool tool-wide" data-tool="ready">
  <div class="tool-head"><span>Appraisal prep scorecard</span><i>12 questions · about two minutes</i></div>
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
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#e3e9f5" stroke-width="18"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#f1ad02" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3" style="transition:stroke-dashoffset .5s,stroke .3s"/></svg>
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

SCHED = """
<div class="tool" data-tool="sched">
  <div class="tool-head"><span>Roof age payment schedule</span><i>Illustrative schedules</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="s-rcv">Roof replacement cost (RCV)</label><input id="s-rcv" name="roof" inputmode="decimal" value="17500"><span class="hint">Roof portion of the estimate only.</span></div>
        <div><label for="s-age">Roof age (years)</label><input id="s-age" name="age" inputmode="decimal" value="11"></div>
      </div>
      <div><label for="s-pre">Schedule</label><select id="s-pre" name="preset"><option value="a" selected>A (illustrative): full 2 yrs, −5%/yr, min 30%</option><option value="b">B (illustrative): −6%/yr from new, min 25%</option><option value="c">C (illustrative): full 5 yrs, −7%/yr, min 20%</option><option value="custom">Custom: my policy’s schedule</option></select><span class="hint">Real schedules differ by insurer. Use the table in your roof endorsement.</span></div>
      <div class="row3" data-custom hidden>
        <div><label for="s-gr">Full-pay years</label><input id="s-gr" name="grace" inputmode="decimal" value="2"></div>
        <div><label for="s-rt">Reduction per year (%)</label><input id="s-rt" name="rate" inputmode="decimal" value="5"></div>
        <div><label for="s-fl">Minimum (%)</label><input id="s-fl" name="floor" inputmode="decimal" value="30"></div>
      </div>
      <div class="row2">
        <div><label for="s-oth">Other covered damage (RCV)</label><input id="s-oth" name="other" inputmode="decimal" value="4300"><span class="hint">Gutters, siding, screens and so on.</span></div>
        <div><label for="s-ded">Deductible ($)</label><input id="s-ded" name="ded" inputmode="decimal" value="3100"></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Roof paid under the schedule</small><b data-o="roofpay">$0</b></div>
      <div class="stack" aria-hidden="true"><span style="background:#002569"></span><span style="background:#f1ad02"></span></div>
      <div class="legend"><span><i style="background:#002569"></i>Schedule pays</span><span><i style="background:#f1ad02"></i>Reduced by schedule</span></div>
      <div class="out-rows">
        <div><span>Schedule percentage at this age</span><b data-o="spct">—</b></div>
        <div><span>Reduction from roof RCV</span><b data-o="cut">$0</b></div>
        <div><span>Claim payment with schedule</span><b data-o="net">$0</b></div>
        <div><span>Claim payment at full RCV</span><b data-o="full">$0</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "appraisal-payoff-projector", "name": "Appraisal Payoff Projector", "icon": "$", "kind": "Calculator",
        "short": "Size the dispute, test where an award might land and subtract appraiser and umpire fees.",
        "title": "Appraisal Payoff Projector | Net Gain After Fees",
        "desc": "Free appraisal payoff projector: size the gap between estimates, test where an award might land and see your net after appraisal fees.",
        "h1": "Appraisal Payoff Projector: What Would You Net?",
        "lede": "Enter the carrier’s number and yours, slide the award between them and add realistic fees. The projector shows whether appraisal is likely to leave you ahead.",
        "markup": GAP_FULL,
        "explain": """
<h2>How to use the projector</h2>
<ol><li><strong>Enter the insurer’s RCV total</strong>, the replacement cost before depreciation and deductible.</li>
<li><strong>Enter your estimate</strong>, also at replacement cost.</li>
<li><strong>Test several landing points.</strong> Try 30%, 50% and 75% rather than trusting one answer.</li>
<li><strong>Add fees</strong> using your appraiser’s quoted arrangement and a realistic umpire fee.</li></ol>
<h2>Reading the result</h2>
<p>If appraisal only pays off when you win nearly everything, the case is fragile. If it still makes sense at 40%, the dispute is more likely worth pursuing. Well-documented line items tend to survive; unsupported ones tend to fall.</p>
<div class="note"><b class="h">Illustrative figures</b>The default numbers are an example only, not a client result or a typical award.</div>
<h2>What it leaves out</h2>
<p>Deductibles, depreciation timing and policy limits change what you are paid, not the size of the dispute. For holdback math, use the <a href=\"""" + T + """holdback-recovery-calculator/">holdback recovery calculator</a>.</p>
""",
        "faqs": [("Is the projected award a prediction?", "No. It is a planning scenario based on the numbers you enter."), ("What does an umpire usually charge?", "It varies with claim size and complexity. Ask for a quote once an umpire is proposed; the fee is commonly split evenly.")],
    },
    {
        "slug": "holdback-recovery-calculator", "name": "Holdback Recovery Calculator", "icon": "ACV", "kind": "Calculator",
        "short": "Split a replacement cost claim into the first ACV check and the depreciation released after repairs.",
        "title": "Holdback Recovery Calculator | RCV vs ACV",
        "desc": "Free RCV vs ACV holdback calculator: list items with age and life to estimate your first check, recoverable depreciation and total payout.",
        "h1": "Holdback Recovery Calculator (RCV vs. ACV)",
        "lede": "Replacement cost policies usually pay twice: an actual cash value check now and the held-back depreciation after repairs. List your items to see the split.",
        "markup": DEP,
        "explain": """
<h2>How depreciation is estimated</h2>
<p>The calculator uses straight-line depreciation, age divided by expected life, capped at the maximum you choose. Real estimates may use condition adjustments, different life tables or non-depreciable items, so treat the result as a planning figure.</p>
<h2>Common life expectancies in estimates</h2>
<div class="table-wrap"><table><thead><tr><th>Item</th><th>Common range</th></tr></thead><tbody>
<tr><th>3-tab asphalt shingles</th><td>20–25 years</td></tr><tr><th>Laminated shingles</th><td>25–30 years</td></tr><tr><th>Steel siding</th><td>40–50 years</td></tr><tr><th>Vinyl siding</th><td>30–40 years</td></tr><tr><th>Seamless gutters</th><td>20–30 years</td></tr><tr><th>Interior paint</th><td>8–12 years</td></tr>
</tbody></table></div>
<h2>Getting holdback released</h2>
<p>Most policies release recoverable depreciation after repairs are complete within a time limit. Send invoices and photos of finished work, and set a reminder with the <a href=\"""" + T + """claim-timeline-builder/">claim timeline builder</a>.</p>
""",
        "faqs": [("Should labor be depreciated?", "Practices vary by policy and jurisdiction. Ask your insurer to explain its approach in writing and check how your estimate treats labor."), ("What if I don’t repair?", "Under most replacement cost policies you keep the ACV payment but may not recover the held-back depreciation.")],
    },
    {
        "slug": "roof-square-footage-pitch-calculator", "name": "Roof Square Footage & Pitch Calculator", "icon": "▲", "kind": "Calculator",
        "short": "Turn a footprint and pitch into true roof squares, bundles and a rough replacement figure.",
        "title": "Roof Square Footage & Pitch Calculator",
        "desc": "Roof square footage and pitch calculator: convert a footprint into true roof squares, waste and bundles, then check your claim estimate.",
        "h1": "Roof Square Footage and Pitch Calculator",
        "lede": "Measurement errors quietly shrink roof claims. Use your home’s footprint and pitch to estimate the true roof surface and compare it with the insurer’s numbers.",
        "markup": ROOF,
        "explain": """
<h2>The math</h2>
<p>A sloped roof has more surface than the ground it covers. The pitch multiplier is √(1 + (rise ÷ 12)²). A 5/12 roof is about 8.3% larger than its footprint; an 8/12 roof is about 20.2% larger; a 12/12 roof is about 41.4% larger.</p>
<h2>Checking an estimate</h2>
<ul><li>Find total squares and the waste percentage in the roof section of the carrier’s estimate.</li>
<li>Compare with the result here. Differences over 5–10% deserve a closer look.</li>
<li>Look for steep charges (often 7/12 and up) and high-roof charges on two-story sections.</li>
<li>Check that starter, ridge cap, drip edge and ice-and-water shield appear as separate lines.</li></ul>
<h2>Limits of a footprint method</h2>
<p>Roofs with several pitches, dormers or valleys should be measured plane by plane. Aerial reports or field measurements beat a footprint estimate; treat this as a sanity check.</p>
""",
        "faqs": [("What is a roofing square?", "One hundred square feet of roof surface. Many Kansas single-story ranch homes fall between 20 and 30 squares."), ("Why does waste vary?", "Hips, valleys and dormers require more cutting, so more material becomes scrap.")],
    },
    {
        "slug": "percentage-deductible-converter", "name": "Percentage Deductible Converter", "icon": "%", "kind": "Calculator",
        "short": "See a 1% or 2% wind/hail deductible in real dollars and what a hail claim would actually pay.",
        "title": "Percentage Deductible Converter | Wind & Hail",
        "desc": "Convert a percentage wind and hail deductible into dollars and compare what a Kansas storm claim pays against a flat deductible.",
        "h1": "Percentage Wind and Hail Deductible Converter",
        "lede": "A 1% deductible sounds small until it is multiplied by your dwelling limit. See your deductible in dollars and how it changes a storm payout.",
        "markup": DEDUCT,
        "explain": """
<h2>Why percentage deductibles matter in Kansas</h2>
<p>Because hail and wind claims are so common in Kansas, many policies use a separate wind/hail deductible set as a percentage of Coverage A. On a $310,000 dwelling limit, a 1% deductible is $3,100 and a 2% deductible is $6,200.</p>
<h2>Where to find yours</h2>
<p>Look on your declarations page for “wind/hail” or “windstorm or hail” deductible. The policy defines when it applies; it usually covers any loss caused by wind or hail, not just tornadoes.</p>
<h2>How it affects appraisal</h2>
<p>The deductible doesn’t change the amount of loss a panel decides, but it changes what you receive. A loss barely above the deductible may not be worth disputing; one well above it may be.</p>
""",
        "faqs": [("Is the percentage based on the loss or the coverage?", "Usually on Coverage A, the dwelling limit, not on the size of the loss. Check your policy wording."), ("Can I change my deductible?", "Usually at renewal. A higher deductible lowers the premium but raises your share of every storm loss.")],
    },
    {
        "slug": "claim-timeline-builder", "name": "Claim Timeline Builder", "icon": "◷", "kind": "Planner",
        "short": "Map notice, proof of loss, holdback and suit dates from your date of loss, then export them.",
        "title": "Claim Timeline Builder | Kansas Claim Dates",
        "desc": "Build a Kansas claim timeline from your date of loss: notice, proof of loss, holdback and suit dates, exported to your calendar as .ics.",
        "h1": "Claim Timeline Builder for Kansas Property Claims",
        "lede": "Policy deadlines keep running while a dispute drags on. Enter your date of loss and the windows in your policy to build a timeline you can drop into your calendar.",
        "markup": DATES,
        "explain": """
<h2>The dates that matter</h2>
<ul><li><strong>Prompt notice.</strong> Policies require losses to be reported promptly. Late notice is a common defense.</li>
<li><strong>Proof of loss.</strong> If the insurer requests a sworn proof of loss, many forms allow 60 days to return it.</li>
<li><strong>Depreciation recovery.</strong> Replacement cost policies often require repairs within a set period to release holdback.</li>
<li><strong>Suit limitation.</strong> Most policies include a “Suit Against Us” clause with its own time limit. Appraisal may not pause it.</li></ul>
<div class="note"><b class="h">Important</b>The timeline uses only the numbers you enter. It isn’t legal advice, and courts can read policy deadlines differently. If a deadline is close, contact a Kansas attorney.</div>
""",
        "faqs": [("Is the date of loss when I noticed the damage?", "Usually it is the date of the storm or event. Hail and wind reports for your address can help confirm it."), ("Does appraisal extend my suit deadline?", "Not automatically. Protect the deadline independently and ask an attorney if you are unsure.")],
    },
    {
        "slug": "appraisal-prep-scorecard", "name": "Appraisal Prep Scorecard", "icon": "✓", "kind": "Checklist",
        "short": "Answer 12 yes/no questions to score your claim file and get a to-do list before you demand appraisal.",
        "title": "Appraisal Prep Scorecard | Is Your File Ready?",
        "desc": "Twelve yes-or-no questions that score your claim file before insurance appraisal and build a to-do list of what to finish first.",
        "h1": "Appraisal Prep Scorecard: Is Your Claim File Ready?",
        "lede": "Strong appraisals start with complete files. Answer twelve quick questions to see where yours stands and which gaps to close first.",
        "markup": READY,
        "explain": """
<h2>How the score is weighted</h2>
<p>Coverage, estimates and evidence carry the most weight because they decide whether appraisal is the right tool and how well your number will hold up. Paperwork matters too, but it is easier to fix.</p>
<h2>Reading your score</h2>
<ul><li><strong>75 and up:</strong> a solid file. A professional review of the gap is the logical next step.</li>
<li><strong>45 to 74:</strong> close the open items first; each one strengthens your position.</li>
<li><strong>Under 45:</strong> demanding appraisal now could lock in a low number. Build the file first.</li></ul>
""",
        "faqs": [("Is anything saved or sent?", "No. The scorecard runs entirely in your browser and nothing is stored."), ("Can I share my result?", "Yes. Take a screenshot of your to-do list and bring it to a consultation.")],
    },
    {
        "slug": "roof-age-payment-schedule-calculator", "name": "Roof Age Payment Schedule Calculator", "icon": "Yr", "kind": "Calculator",
        "short": "See how a roof payment schedule tied to roof age cuts a Kansas hail payout, and by how much.",
        "title": "Roof Age Payment Schedule Calculator | Kansas",
        "desc": "See how a roof payment schedule based on roof age reduces a Kansas hail claim, using illustrative schedules or the one in your policy.",
        "h1": "Roof Age Payment Schedule Calculator",
        "lede": "Many policies sold in hail-heavy states now pay roofs on a schedule that shrinks as the roof ages. Enter your roof’s cost and age to see what a schedule does to the check.",
        "markup": SCHED,
        "explain": """
<h2>What a roof payment schedule is</h2>
<p>A roof surfacing payment schedule is an endorsement that pays a percentage of the roof’s replacement cost based on its age and sometimes its material. A new roof may be paid in full; a 15-year-old roof might be paid at a fraction of replacement cost, with no recoverable depreciation.</p>
<h2>Why it matters in Kansas</h2>
<p>Hail is the leading source of property claims in much of Kansas, and insurers have responded with roof schedules, cosmetic damage exclusions and higher wind/hail deductibles. Knowing which of these is on your policy tells you what an appraisal award will actually pay.</p>
<h2>Schedule versus amount of loss</h2>
<p>A schedule limits payment; it doesn’t change the amount of damage. Appraisal sets the full replacement cost of the roof, and the schedule is then applied to that number. A higher, accurate roof valuation still raises a scheduled payment.</p>
<div class="note"><b class="h">Illustrative schedules only</b>Schedules A, B and C are examples, not any insurer’s actual table. Use “Custom” and the figures in your endorsement for a real comparison.</div>
""",
        "faqs": [("How do I know if my policy has a roof schedule?", "Look for an endorsement named something like “roof surfacing payment schedule” or “roof ACV” on your declarations page, or ask your agent."), ("Is roof age measured from installation?", "Usually yes. Keep your installation invoice or permit, since a wrong roof age can reduce the payment.")],
    },
]
