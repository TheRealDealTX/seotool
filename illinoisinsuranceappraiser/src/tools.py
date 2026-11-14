"""Interactive claim tools: markup + explanatory copy. Logic lives in static/assets/js/app.js."""

C_NEUTRAL, C_BRAND, C_DEEP = "#e7dcd3", "#ff5f0f", "#2b1105"

GAP_FULL = f"""
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Disputed amount &amp; net recovery estimator</span><i>Runs in your browser</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Carrier’s estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="21600"><span class="hint">Replacement cost total on the insurer’s estimate.</span></div>
        <div><label for="g-own">Your estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="36400"><span class="hint">Your contractor’s or independent line-item estimate.</span></div>
      </div>
      <div><label for="g-land">Where could the award land inside the gap?</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% = the carrier’s figure stands. 100% = your full figure is awarded. Most awards land somewhere between.</span></div>
      <div class="row2">
        <div><label for="g-ft">Appraiser fee basis</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of the increase (%)</option></select></div>
        <div><label for="g-fee">Fee amount</label><input id="g-fee" name="fee" inputmode="decimal" value="2800"></div>
      </div>
      <label class="check"><input type="checkbox" name="useump" checked> Add my half of an umpire’s fee</label>
      <div><label for="g-ump">Umpire’s total fee (shared 50/50)</label><input id="g-ump" name="umpire" inputmode="decimal" value="3200"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated net increase after costs</small><b data-o="net">$0</b></div>
      <div class="stack" aria-hidden="true"><span style="background:{C_NEUTRAL}"></span><span style="background:{C_BRAND}"></span><span style="background:{C_DEEP}"></span></div>
      <div class="legend"><span><i style="background:{C_NEUTRAL}"></i>Carrier’s figure</span><span><i style="background:{C_BRAND}"></i>Your net gain</span><span><i style="background:{C_DEEP}"></i>Appraisal costs</span></div>
      <div class="out-rows">
        <div><span>Disputed amount</span><b data-o="gap">$0</b></div>
        <div><span>Gap vs. carrier estimate</span><b data-o="pct">—</b></div>
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
  <div class="tool-head"><span>60-second gap check</span><i>Nothing is stored</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="m-ins">Carrier’s estimate</label><input id="m-ins" name="insurer" inputmode="decimal" value="17800"></div>
      <div><label for="m-own">Your contractor’s estimate</label><input id="m-own" name="yours" inputmode="decimal" value="31200"></div>
      <div><label for="m-land">Award lands at</label><div class="range"><input id="m-land" type="range" name="land" min="0" max="100" step="5" value="50" data-unit="%"><output>50%</output></div><span class="hint">of the disputed amount (illustrative)</span></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Disputed amount</small><b data-o="gap">$0</b></div>
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
  <div class="tool-head"><span>Recoverable depreciation planner</span><i>Add a row for each item</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Laminated shingle roof", 16900, 11, 30), ("Vinyl siding — two elevations", 7400, 14, 35), ("Basement carpet & pad", 3100, 5, 10)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn ghost small" data-add data-run>+ Add item</button></div>
      <div class="row2">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="1500"></div>
        <div><label for="d-cap">Depreciation cap</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="90">90%</option></select><span class="hint">Many estimates cap depreciation; check yours.</span></div>
      </div>
      <label class="check"><input type="checkbox" name="nonrec"> My policy pays actual cash value only (no recoverable depreciation)</label>
    </div>
    <div class="tool-out" aria-live="polite" style="grid-template-columns:repeat(auto-fit,minmax(200px,1fr))">
      <div class="out-big"><small>First payment (ACV − deductible)</small><b data-o="first">$0</b></div>
      <div class="out-big"><small>Held back until repairs</small><b data-o="held">$0</b></div>
      <div class="out-big"><small>Total once recovered</small><b data-o="total">$0</b></div>
      <div class="out-rows" style="grid-column:1/-1">
        <div><span>Replacement cost (RCV)</span><b data-o="rcv">$0</b></div>
        <div><span>Total depreciation</span><b data-o="dep">$0</b></div>
        <div><span>Depreciation share of RCV</span><b data-o="deppct">0%</b></div>
        <div><span>Actual cash value (ACV)</span><b data-o="acv">$0</b></div>
      </div>
    </div>
  </div>
</div>"""

ROOF = """
<div class="tool" data-tool="roof">
  <div class="tool-head"><span>Pitch-adjusted roof squares</span><i>Check the carrier’s measurements</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <fieldset class="bare"><legend class="sr-only">Measurement method</legend>
        <div class="btn-row">
          <label class="check"><input type="radio" name="mode" value="dims" checked> Footprint length × width</label>
          <label class="check"><input type="radio" name="mode" value="area"> I know the footprint area</label>
        </div></fieldset>
      <div class="row2" data-mode="dims">
        <div><label for="r-l">Footprint length (ft)</label><input id="r-l" name="len" inputmode="decimal" value="52"></div>
        <div><label for="r-w">Footprint width (ft)</label><input id="r-w" name="wid" inputmode="decimal" value="30"></div>
      </div>
      <div data-mode="dims"><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="12"></div>
      <div data-mode="area" hidden><label for="r-a">Footprint area incl. overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="1900"></div>
      <div class="row2">
        <div><label for="r-p">Roof pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 7 else "", p) for p in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16]) + """</select></div>
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="10">10% — simple gable</option><option value="12">12% — gable with dormers</option><option value="15" selected>15% — hip roof (common on bungalows)</option><option value="18">18% — cut-up / complex</option></select></div>
      </div>
      <div><label for="r-pr">Installed price per square (optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 560"><span class="hint">Use a local contractor’s quote for a rough replacement figure.</span></div>
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

DEDUCT = f"""
<div class="tool" data-tool="deduct">
  <div class="tool-head"><span>Deductible dollars converter</span><i>Percentage vs. flat</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling coverage (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="340000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Wind/hail percentage deductible</label><select id="w-p" name="pct"><option value="0.5">0.5%</option><option value="1" selected>1%</option><option value="2">2%</option><option value="3">3%</option><option value="5">5%</option></select></div>
        <div><label for="w-f">All-other-perils deductible ($)</label><input id="w-f" name="flat" inputmode="decimal" value="1000"></div>
      </div>
      <div><label for="w-l">Estimated wind or hail damage</label><input id="w-l" name="loss" inputmode="decimal" value="18900"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your percentage deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span style="background:{C_DEEP}"></span><span style="background:{C_BRAND}"></span></div>
      <div class="legend"><span><i style="background:{C_DEEP}"></i>You pay</span><span><i style="background:{C_BRAND}"></i>Policy pays</span></div>
      <div class="out-rows">
        <div><span>Payment with the % deductible</span><b data-o="pdpay">$0</b></div>
        <div><span>Payment if the flat deductible applied</span><b data-o="flatpay">$0</b></div>
        <div><span>Extra out-of-pocket from the % deductible</span><b data-o="diff">$0</b></div>
      </div>
      <p class="out-msg" data-o="below"></p>
    </div>
  </div>
</div>"""

DATES = """
<div class="tool" data-tool="dates">
  <div class="tool-head"><span>Illinois claim deadline calendar</span><i>Exports to your calendar</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
      <p class="hint" style="margin:0">Change each window to match your policy. Defaults are common figures, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report the claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="3"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="10"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Often counted from the carrier’s request.</span></div>
        <div><label for="t-r">Depreciation recovery (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="180"></div>
        <div><label for="t-s">Suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="730"><span class="hint">Check your policy: often one or two years.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download .ics calendar file</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the carrier accepted coverage for at least part of the loss?", "Get written confirmation that coverage is accepted. If the claim was denied, talk to an Illinois attorney before considering appraisal."),
    (3, "Do you have the carrier’s full line-item estimate, not just a summary?", "Ask the adjuster in writing for the complete itemized estimate."),
    (3, "Do you have your own itemized estimate from a contractor or estimator?", "Get an independent line-item estimate — a one-line bid won’t carry weight with a panel."),
    (2, "Do you have dated photos taken soon after the loss?", "Collect every photo and note when each was taken. Add photos of current conditions."),
    (2, "Have you read the appraisal paragraph in your policy?", "Find ‘Appraisal’ in the policy conditions and note any timing rules."),
    (2, "Have you calendared your policy’s suit-limitation date?", "Find the ‘Suit Against Us’ condition and put the date on your calendar — our deadline calendar can help."),
    (2, "Are temporary repairs done and receipts saved?", "Make reasonable temporary repairs and keep every receipt."),
    (1, "Do you have your current declarations page?", "Download or request the declarations page from your agent or carrier."),
    (2, "Has hidden damage been opened up and documented?", "Make sure wet walls, attics, decking and basements have been inspected so the scope is complete."),
    (1, "Is your correspondence with the carrier saved in date order?", "Gather emails, letters and claim notes in date order."),
    (2, "Is the gap between estimates more than about 10% or $5,000?", "Run the disputed amount estimator — a small gap may not justify appraisal costs."),
    (1, "If the carrier asked for a sworn proof of loss, has it been sent?", "If a proof of loss was requested, return it on time."),
]

READY = """
<div class="tool tool-wide" data-tool="ready">
  <div class="tool-head"><span>Appraisal file strength score</span><i>12 questions · about two minutes</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <ol class="quiz">""" + "".join(
    '<li data-w="%d" data-fix="%s"><span>%s</span><span class="yn"><button type="button" class="yes" aria-pressed="false">Yes</button><button type="button" class="no" aria-pressed="false">No</button></span></li>' % (w, f, q)
    for w, q, f in _QUIZ) + f"""
      </ol>
      <div class="btn-row"><button type="button" class="btn ghost small" data-reset>Reset answers</button></div>
    </div>
    <div class="tool-out" aria-live="polite" style="grid-template-columns:minmax(220px,300px) 1fr;align-items:start">
      <div>
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#f3e7de" stroke-width="18"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="{C_BRAND}" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3" style="transition:stroke-dashoffset .5s,stroke .3s"/></svg>
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

BACKUP = f"""
<div class="tool" data-tool="backup">
  <div class="tool-head"><span>Sewer backup endorsement gap checker</span><i>Built for basement losses</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="b-fin">Finished-basement rebuild cost</label><input id="b-fin" name="finish" inputmode="decimal" value="24500"><span class="hint">Drywall, flooring, trim, paint, built-ins.</span></div>
        <div><label for="b-mit">Water extraction &amp; drying</label><input id="b-mit" name="mitig" inputmode="decimal" value="5200"></div>
      </div>
      <div class="row2">
        <div><label for="b-con">Damaged contents</label><input id="b-con" name="contents" inputmode="decimal" value="8300"></div>
        <div><label for="b-eq">Furnace, water heater &amp; appliances</label><input id="b-eq" name="equip" inputmode="decimal" value="3600"></div>
      </div>
      <div class="row2">
        <div><label for="b-lim">Water backup endorsement limit</label><select id="b-lim" name="limit"><option value="5000">$5,000</option><option value="10000" selected>$10,000</option><option value="15000">$15,000</option><option value="25000">$25,000</option><option value="50000">$50,000</option><option value="0">No endorsement</option></select></div>
        <div><label for="b-ded">Deductible ($)</label><input id="b-ded" name="deduct" inputmode="decimal" value="1000"></div>
      </div>
      <label class="check"><input type="checkbox" name="dedin" checked> The deductible is subtracted before the endorsement limit applies</label>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated uncovered amount</small><b data-o="gapb">$0</b></div>
      <div class="stack" aria-hidden="true"><span style="background:{C_BRAND}"></span><span style="background:{C_DEEP}"></span></div>
      <div class="legend"><span><i style="background:{C_BRAND}"></i>Endorsement pays</span><span><i style="background:{C_DEEP}"></i>Left with you</span></div>
      <div class="out-rows">
        <div><span>Total basement loss</span><b data-o="totalb">$0</b></div>
        <div><span>Endorsement payment (estimated)</span><b data-o="paidb">$0</b></div>
        <div><span>Share of the loss covered</span><b data-o="shareb">0%</b></div>
        <div><span>Limit needed to cover this loss</span><b data-o="needb">$0</b></div>
      </div>
      <p class="out-msg" data-o="msgb"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "disputed-amount-net-estimator", "name": "Disputed Amount Estimator", "icon": "Δ", "kind": "Calculator",
        "short": "Size the gap between estimates, project an award and subtract appraiser and umpire fees to see your net.",
        "title": "Disputed Amount & Net Recovery Estimator | Free Tool",
        "desc": "Free tool for Illinois claims: compare your estimate with the carrier’s, project an appraisal award and subtract fees to see your net increase.",
        "h1": "Disputed Amount and Net Recovery Estimator",
        "lede": "Enter the carrier’s estimate and yours, pick where an award might land, and add realistic fees. The estimator shows whether appraisal is likely to leave you ahead.",
        "markup": GAP_FULL,
        "explain": """
<h2>How to use it</h2>
<ol><li><strong>Enter the carrier’s RCV total</strong> — the replacement cost figure before depreciation and the deductible.</li>
<li><strong>Enter your estimate</strong>, also at replacement cost.</li>
<li><strong>Test several outcomes</strong> with the slider: try 30%, 55% and 80%.</li>
<li><strong>Add fees</strong> using the arrangement your appraiser quotes and a realistic umpire fee.</li></ol>
<h2>Read the result as a range</h2>
<p>Awards rarely match either side’s opening figure. Documented line items tend to hold and unsupported ones tend to fall. If appraisal only pays off at 90% or more, your position is fragile. If it still pays at 40%, it’s more likely worth pursuing. All figures here are illustrative.</p>
<h2>What it leaves out</h2>
<p>Deductibles, policy limits, sublimits and depreciation timing change what you’re paid, not the size of the dispute. For the payment split, use the <a href="/calculators-and-planners/recoverable-depreciation-planner/">recoverable depreciation planner</a>.</p>
""",
        "faqs": [("Is the projected award a prediction?", "No. It’s a scenario you control with the slider. Real awards depend on documentation, the panel and your policy."), ("What does an umpire usually charge?", "It varies with the claim’s size and complexity. Ask for a written quote once an umpire is proposed; most policies split the fee evenly.")],
    },
    {
        "slug": "recoverable-depreciation-planner", "name": "Recoverable Depreciation Planner", "icon": "ACV", "kind": "Calculator",
        "short": "Split a replacement-cost claim into the first ACV payment, the holdback and the total once repairs are done.",
        "title": "Recoverable Depreciation Planner | RCV vs ACV Payments",
        "desc": "Free RCV vs ACV planner for Illinois claims: list items by age and life to estimate your first payment, the holdback and your total recovery.",
        "h1": "Recoverable Depreciation Planner (RCV vs. ACV)",
        "lede": "Replacement-cost policies usually pay in two parts: actual cash value now, and the depreciation held back after repairs. List your items to see how the money splits.",
        "markup": DEP,
        "explain": """
<h2>The method used</h2>
<p>This planner applies straight-line depreciation — age divided by expected life — capped at the maximum you choose. Real estimates may adjust for condition, use different life expectancies or treat some items as non-depreciable, so treat the result as a planning figure.</p>
<h2>Common life expectancies</h2>
<div class="table-wrap"><table><thead><tr><th>Item</th><th>Typical range</th></tr></thead><tbody>
<tr><th>Three-tab shingles</th><td>18–25 years</td></tr><tr><th>Laminated shingles</th><td>25–30 years</td></tr><tr><th>Vinyl siding</th><td>30–40 years</td></tr><tr><th>Interior paint</th><td>8–12 years</td></tr><tr><th>Carpet</th><td>8–12 years</td></tr><tr><th>Furnace</th><td>15–20 years</td></tr>
</tbody></table></div>
<h2>Getting the holdback paid</h2>
<p>Most policies release recoverable depreciation once repairs are finished within a set time. Send invoices and photos of the completed work, and use the <a href="/calculators-and-planners/illinois-claim-deadline-calendar/">deadline calendar</a> so the window doesn’t close on you.</p>
""",
        "faqs": [("Can labor be depreciated in Illinois?", "Practices and court decisions on labor depreciation vary. Check whether your estimate depreciates labor and ask the carrier to explain its approach in writing, or ask an attorney."), ("What if I don’t make repairs?", "Under most replacement-cost policies, you keep the ACV payment but may not collect the held-back depreciation.")],
    },
    {
        "slug": "pitch-adjusted-roof-squares", "name": "Pitch-Adjusted Roof Squares", "icon": "▲", "kind": "Calculator",
        "short": "Turn a footprint and pitch into true roof squares, bundles and a rough cost, then compare with the estimate.",
        "title": "Pitch-Adjusted Roof Squares Calculator for Claims",
        "desc": "Convert a home’s footprint, pitch and waste factor into true roof squares and bundles, then check the measurements in your insurance estimate.",
        "h1": "Pitch-Adjusted Roof Squares Calculator",
        "lede": "Under-measured roofs are one of the most common reasons roof claims fall short. Use your footprint and pitch to estimate true surface area, squares and bundles.",
        "markup": ROOF,
        "explain": """
<h2>The math</h2>
<p>A pitched roof has more surface than the footprint under it. The pitch multiplier is √(1 + (rise ÷ 12)²). A 7/12 roof is about 15.8% larger than its footprint; a 12/12 roof is about 41.4% larger.</p>
<h2>Checking the carrier’s numbers</h2>
<ul><li>Find total squares and the waste percentage in the roof section of the estimate.</li>
<li>Compare them with this result. A difference over 5–10% is worth a closer look.</li>
<li>Look for steep charges (often from 7/12) and high-roof charges for two-story sections.</li>
<li>Confirm ridge cap, starter, drip edge and ice-and-water shield are listed separately.</li></ul>
<h2>Limits of a footprint method</h2>
<p>Roofs with several pitches, dormers and valleys need measuring plane by plane. An aerial measurement report or field measurement beats any footprint estimate — use this as a sanity check.</p>
""",
        "faqs": [("What is a square?", "100 square feet of roof surface. A typical Illinois two-story home might have 22 to 40 squares."), ("Why is waste higher on hip roofs?", "Hips and valleys need more cutting, so more shingle ends up as scrap. Chicago bungalows with hip roofs often need about 15%.")],
    },
    {
        "slug": "deductible-dollars-converter", "name": "Deductible Dollars Converter", "icon": "%", "kind": "Calculator",
        "short": "Turn a percentage wind/hail deductible into dollars and see what a storm claim would actually pay.",
        "title": "Wind & Hail Percentage Deductible Converter | Free Tool",
        "desc": "Convert a percentage wind or hail deductible into dollars and compare what your Illinois policy would pay against a flat deductible.",
        "h1": "Wind and Hail Deductible Dollars Converter",
        "lede": "A 1% deductible sounds tiny until you multiply it by your dwelling limit. See your wind or hail deductible in real dollars and how it changes a storm payout.",
        "markup": DEDUCT,
        "explain": """
<h2>Percentage deductibles in Illinois</h2>
<p>Illinois has no hurricane deductibles, but many carriers selling in the state now use a separate wind/hail deductible set as a percentage of Coverage A, especially in hail-prone areas. On a $340,000 dwelling limit, a 1% deductible is $3,400 — and a 2% deductible is $6,800.</p>
<h2>Where to find yours</h2>
<p>Check the declarations page for “wind/hail,” “windstorm or hail” or a similar deductible line. Endorsements later in the policy explain exactly when it applies.</p>
<h2>How it affects appraisal</h2>
<p>The deductible doesn’t change the amount of loss an appraisal panel decides, but it changes what you receive. A loss just above the deductible may not be worth disputing; a loss well above it may be.</p>
""",
        "faqs": [("Does the percentage apply to the whole claim?", "It’s usually calculated from Coverage A but applied to the whole wind or hail loss. Check your policy wording."), ("Can I lower it?", "Usually at renewal, for a higher premium. Ask your agent to price the options.")],
    },
    {
        "slug": "illinois-claim-deadline-calendar", "name": "Illinois Claim Deadline Calendar", "icon": "◷", "kind": "Planner",
        "short": "Map notice, proof-of-loss, depreciation and suit dates from your date of loss — then export them.",
        "title": "Illinois Claim Deadline Calendar | Export Key Dates (.ics)",
        "desc": "Enter your date of loss to map proof-of-loss, depreciation and suit-limitation dates for an Illinois property claim, then export them as .ics.",
        "h1": "Illinois Insurance Claim Deadline Calendar",
        "lede": "Policy deadlines keep running while you argue about the number. Enter your date of loss and your policy’s windows to build a timeline you can drop into any calendar.",
        "markup": DATES,
        "explain": """
<h2>The dates that matter</h2>
<ul><li><strong>Prompt notice.</strong> Policies require you to report losses promptly. Late notice is a common defense.</li>
<li><strong>Proof of loss.</strong> If the carrier asks for a sworn proof of loss, many policies allow 60 days to send it.</li>
<li><strong>Depreciation recovery.</strong> Replacement-cost policies often set a deadline for finishing repairs to collect the holdback.</li>
<li><strong>Suit limitation.</strong> Illinois policies commonly limit lawsuits to one or two years. Illinois law can pause that period in some situations while a claim is pending, but don’t rely on it without legal advice.</li></ul>
<div class="note"><b class="h">Important</b>This calendar uses the numbers you enter. It isn’t legal advice, and courts can read policy deadlines differently. If a deadline is close, talk to an Illinois attorney.</div>
""",
        "faqs": [("Is the date of loss the day I noticed the damage?", "Usually it’s the date of the storm or event. Weather records for your address can help pin it down."), ("Does demanding appraisal pause the suit deadline?", "Not automatically. Protect the deadline independently and get legal advice if it’s approaching.")],
    },
    {
        "slug": "appraisal-file-strength-score", "name": "Appraisal File Strength Score", "icon": "✓", "kind": "Checklist",
        "short": "Answer 12 yes-or-no questions to score your claim file and get a to-do list before invoking appraisal.",
        "title": "Appraisal File Strength Score | Is Your Claim Ready?",
        "desc": "Twelve quick questions that score how ready your Illinois property claim is for appraisal, with a personal to-do list of what to finish first.",
        "h1": "Appraisal File Strength Score",
        "lede": "Strong appraisals are built before anyone signs a demand. Answer twelve questions to see where your file stands and what to fix first.",
        "markup": READY,
        "explain": """
<h2>How it’s weighted</h2>
<p>Coverage, estimates and evidence carry the most weight because they decide whether appraisal is the right tool and how well your number will hold up. Paperwork items still matter but are easier to fix.</p>
<h2>Reading your score</h2>
<ul><li><strong>75 and up:</strong> a solid file. A professional review of the gap is the next step.</li>
<li><strong>45 to 74:</strong> finish the open items first; each one strengthens your position.</li>
<li><strong>Under 45:</strong> invoking appraisal now could lock in a low number. Build the file first.</li></ul>
""",
        "faqs": [("Is anything I enter saved?", "No. The score runs entirely in your browser and nothing is stored or sent."), ("Can I share my result?", "Yes — take a screenshot of your score and to-do list and bring it to your consultation.")],
    },
    {
        "slug": "sewer-backup-endorsement-gap", "name": "Sewer Backup Endorsement Gap Checker", "icon": "≋", "kind": "Calculator",
        "short": "Compare a realistic basement loss with your water backup endorsement limit and see what’s left with you.",
        "title": "Sewer Backup Endorsement Gap Checker | Basement Losses",
        "desc": "See how far a water backup endorsement limit goes on a flooded Illinois basement: covered share, uncovered amount and the limit you would need.",
        "h1": "Sewer Backup Endorsement Gap Checker",
        "lede": "Basement backups are a signature Chicago-area loss, and endorsement limits are often far below rebuild costs. Enter a realistic loss to see the gap before the next storm.",
        "markup": BACKUP,
        "explain": """
<h2>Why this tool exists</h2>
<p>When combined sewers surcharge in a heavy rain, water comes up through floor drains in basements across Cook, DuPage and the older suburbs. Most homeowners policies cover that only through a water backup endorsement, and many endorsements carry limits of $5,000 to $25,000 — far less than a finished basement costs to rebuild.</p>
<h2>How the estimate works</h2>
<p>The tool adds your rebuild, drying, contents and equipment figures, subtracts the deductible and caps the payment at the endorsement limit. Some endorsements apply the deductible differently, and some losses may also fall partly under other coverages, so treat the result as illustrative.</p>
<h2>What appraisal can and can’t do</h2>
<p>Appraisal can’t raise an endorsement limit. It can settle a dispute about how much a covered loss costs — useful when the carrier underprices the rebuild, or when part of the loss falls under another coverage such as a burst pipe. Read more in our guide to <a href="/policyholder-articles/basement-backup-vs-flood-in-illinois/">basement backup versus flood</a>.</p>
""",
        "faqs": [("Is a flooded basement from outside water covered by this endorsement?", "Usually not. Surface water entering from outside is typically flood, which needs flood insurance. Backup endorsements cover water backing up through drains or sewers."), ("When should I raise my limit?", "Review it at renewal, especially if you’ve finished the basement. Ask your agent to price higher limits.")],
    },
]
