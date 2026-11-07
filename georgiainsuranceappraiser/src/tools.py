"""Interactive claim tools: markup + explanatory copy. Logic lives in static/assets/js/app.js."""

GAP_FULL = """
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Appraisal value estimator</span><i>Runs in your browser</i></div>
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
      <div class="stack" aria-hidden="true"><span style="background:#d4c3c7"></span><span style="background:#e3a94f"></span><span style="background:#7a1d33"></span></div>
      <div class="legend"><span><i style="background:#d4c3c7"></i>Carrier’s number</span><span><i style="background:#e3a94f"></i>Your net gain</span><span><i style="background:#7a1d33"></i>Appraisal costs</span></div>
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
  <div class="tool-head"><span>Wind &amp; hail deductible calculator</span><i>Percentage vs. flat</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling coverage (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="385000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Wind/hail or named-storm deductible</label><select id="w-p" name="pct"><option value="1">1%</option><option value="2" selected>2%</option><option value="3">3%</option><option value="5">5%</option><option value="10">10%</option></select></div>
        <div><label for="w-f">All-other-perils flat deductible</label><input id="w-f" name="flat" inputmode="decimal" value="1000"></div>
      </div>
      <div><label for="w-l">Estimated storm damage</label><input id="w-l" name="loss" inputmode="decimal" value="21500"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your percentage deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span style="background:#7a1d33"></span><span style="background:#d4c3c7"></span></div>
      <div class="legend"><span><i style="background:#7a1d33"></i>You pay</span><span><i style="background:#d4c3c7"></i>Policy pays</span></div>
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
  <div class="tool-head"><span>Georgia claim deadline planner</span><i>Exports to your calendar</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
      <p class="hint" style="margin:0">Adjust each window to match your policy. Defaults are common figures, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="3"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="14"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Often 60 days from the carrier’s request.</span></div>
        <div><label for="t-r">Depreciation recovery (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="365"></div>
        <div><label for="t-s">Suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="730"><span class="hint">Two years = 730 days.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download .ics calendar file</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the insurer accepted coverage for at least part of the loss?", "Get written confirmation that coverage is accepted. If the claim was denied, talk to a Georgia attorney before considering appraisal."),
    (3, "Do you have the carrier’s complete, itemized estimate?", "Request the full line-item estimate (not just the summary) in writing."),
    (3, "Do you have your own itemized estimate from a contractor or estimator?", "Get an independent, line-item estimate — a lump-sum bid won’t hold up before a panel."),
    (2, "Do you have dated photos of the damage taken soon after the loss?", "Gather every photo you have and note when each was taken. Add new photos of current conditions."),
    (2, "Have you read your policy’s appraisal clause?", "Find the ‘Appraisal’ paragraph in the conditions section and note any deadlines."),
    (2, "Do you know your policy’s suit-limitation date?", "Locate the ‘Suit Against Us’ clause and calendar the date — our deadline planner can help."),
    (2, "Have temporary repairs been made and receipts saved?", "Complete reasonable temporary repairs and keep every receipt."),
    (1, "Do you have your declarations page?", "Download or request your current declarations page."),
    (2, "Is all hidden damage opened up and documented?", "Make sure wet walls, attics and decking have been inspected so the scope is complete."),
    (1, "Is your correspondence with the carrier organized by date?", "Collect emails, letters and claim notes in date order."),
    (2, "Is the gap between estimates more than about 10% or $5,000?", "Run the numbers in our appraisal value estimator — a small gap may not justify appraisal costs."),
    (1, "Has a sworn proof of loss been submitted if the carrier asked for one?", "If a proof of loss was requested, submit it on time."),
]

READY = """
<div class="tool tool-wide" data-tool="ready">
  <div class="tool-head"><span>Appraisal readiness score</span><i>12 questions · about two minutes</i></div>
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
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#f3e6e9" stroke-width="18"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#e3a94f" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3" style="transition:stroke-dashoffset .5s,stroke .3s"/></svg>
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

TOOLS = [
    {
        "slug": "appraisal-value-estimator", "name": "Appraisal Value Estimator", "icon": "Δ$", "kind": "Calculator",
        "short": "See the disputed amount, a projected award and what you’d net after appraiser and umpire fees.",
        "title": "Appraisal Value Estimator | Is Insurance Appraisal Worth It?",
        "desc": "Free calculator: compare your estimate with the insurer’s, project an appraisal award and subtract appraiser and umpire fees to see your net.",
        "h1": "Appraisal Value Estimator: Is Appraisal Worth It for Your Claim?",
        "lede": "Plug in the carrier’s estimate and yours, choose where an award might land, and add realistic fees. The estimator shows whether appraisal is likely to put more money in your pocket.",
        "markup": GAP_FULL,
        "explain": """
<h2>How to use the estimator</h2>
<ol><li><strong>Enter the insurer’s RCV total</strong> — the replacement cost figure before depreciation and deductible.</li>
<li><strong>Enter your estimate</strong> from a contractor or independent estimator, also at RCV.</li>
<li><strong>Move the slider</strong> to test outcomes. Try 30%, 50% and 80% to see a range rather than a single answer.</li>
<li><strong>Add fees.</strong> Use your appraiser’s quoted arrangement and a realistic umpire fee.</li></ol>
<h2>Why the slider matters</h2>
<p>Appraisal awards rarely match either side’s opening number exactly. Well-documented line items tend to hold; inflated or unsupported ones tend to fall. If your result only works at 90% or 100%, the case is fragile. If it still makes sense at 40%, appraisal is more likely to be worth pursuing.</p>
<h2>What the estimator leaves out</h2>
<p>It doesn’t account for depreciation timing, policy limits, sub-limits or deductibles — those affect what you’re paid, not the size of the dispute. For holdback math, use the <a href="/claim-tools/depreciation-holdback-calculator/">depreciation &amp; holdback calculator</a>.</p>
""",
        "faqs": [("Is a projected award a guarantee?", "No. It’s a planning scenario. Actual awards depend on documentation, the panel and the policy."), ("What’s a typical umpire fee?", "It varies widely with the size and complexity of the claim. Ask the appraisers for a quote once an umpire is proposed; the cost is usually split evenly.")],
    },
    {
        "slug": "depreciation-holdback-calculator", "name": "Depreciation & Holdback Calculator", "icon": "ACV", "kind": "Calculator",
        "short": "Estimate the first ACV check, the recoverable depreciation held back and the total once repairs are done.",
        "title": "Depreciation & Holdback Calculator | RCV vs ACV Payments",
        "desc": "Free RCV vs ACV calculator. List damaged items with age and life expectancy to estimate your first check, recoverable depreciation and total.",
        "h1": "Depreciation & Holdback Calculator (RCV vs. ACV)",
        "lede": "Replacement-cost policies usually pay in two parts: an actual-cash-value check now and recoverable depreciation after repairs. Enter your items to see how the money is split.",
        "markup": DEP,
        "explain": """
<h2>How depreciation is estimated here</h2>
<p>This tool uses straight-line depreciation — age divided by expected life — capped at the maximum you choose. Real estimates may apply condition adjustments, different life expectancies or non-depreciable items such as permits, so treat the result as a planning figure.</p>
<h2>Typical life expectancies used in estimates</h2>
<div class="table-wrap"><table><thead><tr><th>Item</th><th>Common range</th></tr></thead><tbody>
<tr><th>3-tab asphalt shingles</th><td>20–25 years</td></tr><tr><th>Architectural shingles</th><td>25–30 years</td></tr><tr><th>Interior paint</th><td>8–12 years</td></tr><tr><th>Carpet</th><td>8–12 years</td></tr><tr><th>Vinyl siding</th><td>30–40 years</td></tr><tr><th>Water heater</th><td>10–15 years</td></tr>
</tbody></table></div>
<h2>Getting holdback released</h2>
<p>Most policies pay recoverable depreciation once repairs are completed within a time limit. Send invoices and photos of completed work. Our <a href="/claim-tools/claim-deadline-planner/">claim deadline planner</a> can remind you before that window closes.</p>
""",
        "faqs": [("Should labor be depreciated?", "Practices and court decisions vary by state and policy. Check whether your estimate depreciates labor and ask your carrier to explain its approach in writing."), ("What if I don’t repair?", "Under most replacement cost policies, you keep the ACV payment but may not recover the held-back depreciation.")],
    },
    {
        "slug": "roof-squares-pitch-calculator", "name": "Roof Squares & Pitch Calculator", "icon": "▲", "kind": "Calculator",
        "short": "Convert a footprint into true roof squares using pitch and waste — then check the carrier’s numbers.",
        "title": "Roof Squares & Pitch Calculator for Insurance Claims",
        "desc": "Calculate roof squares from footprint, pitch and waste factor, then compare true surface area and steep charges against your insurance estimate.",
        "h1": "Roof Squares and Pitch Calculator for Insurance Claims",
        "lede": "Measurement errors are one of the most common reasons roof claims come up short. Use your home’s footprint and pitch to estimate true roof area, squares and bundles.",
        "markup": ROOF,
        "explain": """
<h2>How the math works</h2>
<p>A roof’s surface is larger than the footprint beneath it. The steeper the pitch, the bigger the difference. The pitch multiplier is √(1 + (rise ÷ 12)²): a 6/12 roof is about 11.8% larger than its footprint; a 12/12 roof is about 41.4% larger.</p>
<h2>Checking your estimate</h2>
<ul><li>Find the roof section of the carrier’s estimate and note total squares and the waste percentage.</li>
<li>Compare those figures with the result here. Differences over 5–10% deserve a closer look.</li>
<li>Check for steep charges (often 7/12 and up) and high-roof charges for two-story sections.</li>
<li>Confirm ridge cap, starter, drip edge and valley materials are listed separately.</li></ul>
<h2>Limits of a footprint calculation</h2>
<p>Complex roofs with multiple pitches, dormers and valleys need measuring by plane. Aerial measurement reports or a field measurement will always beat a footprint estimate — use this as a sanity check.</p>
""",
        "faqs": [("What’s a ‘square’?", "100 square feet of roof surface. A typical Georgia two-story home might have 25 to 40 squares."), ("Why does waste change by roof type?", "Hips, valleys and dormers require more cutting, so more material ends up as scrap.")],
    },
    {
        "slug": "wind-hail-deductible-calculator", "name": "Wind & Hail Deductible Calculator", "icon": "%", "kind": "Calculator",
        "short": "Turn a percentage wind/hail or named-storm deductible into dollars and see what a claim would actually pay.",
        "title": "Wind & Hail Deductible Calculator | % Deductible in Dollars",
        "desc": "Convert a percentage wind/hail or hurricane deductible into dollars and compare what your policy would pay against a flat deductible.",
        "h1": "Wind, Hail and Named-Storm Deductible Calculator",
        "lede": "A 2% deductible sounds small until you multiply it by your dwelling coverage. See your deductible in real dollars and how it changes what a storm claim pays.",
        "markup": DEDUCT,
        "explain": """
<h2>Why percentage deductibles surprise people</h2>
<p>Many Georgia policies — especially near the coast and in hail-prone metro counties — use a separate wind/hail or named-storm deductible calculated as a percentage of Coverage A. On a $385,000 dwelling limit, a 2% deductible is $7,700, not $1,000.</p>
<h2>Where to find yours</h2>
<p>Look on the declarations page for “wind/hail,” “windstorm,” “hurricane” or “named storm” deductible. Endorsements later in the policy define when it applies — for example, only during a storm the National Hurricane Center has named.</p>
<h2>How it affects appraisal</h2>
<p>The deductible doesn’t change the amount of loss a panel decides, but it changes what you receive. A loss just above the deductible may not be worth disputing; one well above it may be.</p>
""",
        "faqs": [("Does the percentage apply to contents too?", "The percentage is usually calculated from Coverage A but applied to the whole wind or hail loss. Check your policy’s wording."), ("Can I change my deductible?", "Usually at renewal. A higher deductible lowers the premium but raises your share of each storm loss.")],
    },
    {
        "slug": "claim-deadline-planner", "name": "Claim Deadline Planner", "icon": "◷", "kind": "Planner",
        "short": "Map notice, proof-of-loss, depreciation and suit-limitation dates from your date of loss — and export them.",
        "title": "Georgia Claim Deadline Planner | Proof of Loss & Suit Dates",
        "desc": "Enter your date of loss to map proof-of-loss, depreciation and suit-limitation dates for a Georgia property claim, then export them to a calendar.",
        "h1": "Georgia Insurance Claim Deadline Planner",
        "lede": "Policy deadlines don’t pause while you argue about a number. Enter your date of loss and your policy’s windows to build a timeline you can download to your calendar.",
        "markup": DATES,
        "explain": """
<h2>The deadlines that matter most</h2>
<ul><li><strong>Prompt notice.</strong> Policies require you to report losses promptly. Late notice is one of the most common defenses carriers raise.</li>
<li><strong>Proof of loss.</strong> If the carrier requests a sworn proof of loss, many policies give 60 days to return it.</li>
<li><strong>Depreciation recovery.</strong> Replacement cost policies typically require repairs within a set period to collect holdback.</li>
<li><strong>Suit limitation.</strong> Georgia homeowner policies commonly require lawsuits within two years of the loss. Appraisal may not stop that clock.</li></ul>
<div class="note"><b class="h">Important</b>This planner uses the numbers you enter. It isn’t legal advice, and courts can interpret policy deadlines differently. If a deadline is close, contact a Georgia attorney.</div>
""",
        "faqs": [("Is the date of loss the day I noticed the damage?", "Usually it’s the date the storm or event occurred. If you’re not sure, weather data for your address can pin it down."), ("Does invoking appraisal extend my suit deadline?", "Not automatically. Some policies or agreements address it; many don’t. Protect the deadline independently.")],
    },
    {
        "slug": "appraisal-readiness-score", "name": "Appraisal Readiness Score", "icon": "✓", "kind": "Checklist",
        "short": "Answer 12 yes/no questions to score your file and get a personal to-do list before invoking appraisal.",
        "title": "Appraisal Readiness Score | Is Your Claim Ready?",
        "desc": "Twelve questions that score how ready your property claim is for insurance appraisal, with a personal to-do list of what to complete first.",
        "h1": "Appraisal Readiness Score: Is Your Claim File Ready?",
        "lede": "The strongest appraisals are won before they start, with a complete file. Answer twelve quick questions to see where yours stands and what to fix first.",
        "markup": READY,
        "explain": """
<h2>How the score is weighted</h2>
<p>Questions about coverage, estimates and evidence carry the most weight because they decide whether appraisal is even the right tool and how well your number will hold up. Administrative items — correspondence, declarations — matter, but they’re easier to fix.</p>
<h2>What to do with your result</h2>
<ul><li><strong>75 and above:</strong> your file is in good shape. A professional review of the gap is the logical next step.</li>
<li><strong>45 to 74:</strong> close the open items first. Each one strengthens your position.</li>
<li><strong>Below 45:</strong> invoking appraisal now could lock in a low number. Build the file before you demand.</li></ul>
""",
        "faqs": [("Is my information saved or sent anywhere?", "No. The scorecard runs entirely in your browser and nothing is stored."), ("Can I share my result with an appraiser?", "Yes — take a screenshot or note your to-do list and bring it to your consultation.")],
    },
]
