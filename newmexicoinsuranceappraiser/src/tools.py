"""Interactive claim estimators for New Mexico Insurance Appraiser. Markup + copy; logic in static/assets/js/app.js.
Everything runs in the browser and nothing is stored or sent."""

GAP_FULL = """
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Claim gap net-recovery estimator</span><i>Private · in-browser</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Insurer’s estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="21600"><span class="hint">Replacement cost total on the carrier’s estimate.</span></div>
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
      <div class="stack" aria-hidden="true"><span style="background:#e6dccb"></span><span style="background:#f2c200"></span><span style="background:#bf0a30"></span></div>
      <div class="legend"><span><i style="background:#e6dccb"></i>Carrier’s number</span><span><i style="background:#f2c200"></i>Your net gain</span><span><i style="background:#bf0a30"></i>Appraisal costs</span></div>
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
  <div class="tool-head"><span>Two-number gap check</span><i>Nothing is stored</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="m-ins">Insurer’s estimate</label><input id="m-ins" name="insurer" inputmode="decimal" value="16800"></div>
      <div><label for="m-own">Your contractor’s estimate</label><input id="m-own" name="yours" inputmode="decimal" value="27500"></div>
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
  <div class="tool-head"><span>Depreciation holdback splitter</span><i>Add rows as needed</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Modified-bitumen flat roof", 14800, 8, 20), ("Evaporative cooler", 1650, 6, 15), ("Exterior stucco color coat", 6200, 7, 25)]) + """
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
  <div class="tool-head"><span>Roof area &amp; pitch converter</span><i>Check the estimate’s squares</i></div>
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
  <div class="tool-head"><span>Percentage deductible converter</span><i>Percent → dollars</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling coverage (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="320000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Wind/hail percentage deductible</label><select id="w-p" name="pct"><option value="1">1%</option><option value="2" selected>2%</option><option value="3">3%</option><option value="5">5%</option><option value="10">10%</option></select></div>
        <div><label for="w-f">All-other-perils flat deductible</label><input id="w-f" name="flat" inputmode="decimal" value="1000"></div>
      </div>
      <div><label for="w-l">Estimated storm damage</label><input id="w-l" name="loss" inputmode="decimal" value="18600"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your percentage deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span style="background:#bf0a30"></span><span style="background:#e6dccb"></span></div>
      <div class="legend"><span><i style="background:#bf0a30"></i>You pay</span><span><i style="background:#e6dccb"></i>Policy pays</span></div>
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
  <div class="tool-head"><span>Claim calendar builder</span><i>.ics export</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
      <p class="hint" style="margin:0">Adjust each window to match your policy. Defaults are common figures, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="3"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="14"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Often 60 days from the carrier’s request.</span></div>
        <div><label for="t-r">Depreciation recovery (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="365"></div>
        <div><label for="t-s">Suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="730"><span class="hint">Use the period in your policy’s “Suit Against Us” clause.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download .ics calendar file</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the insurer accepted coverage for at least part of the loss?", "Get written confirmation that coverage is accepted. If the claim was denied, talk to a New Mexico attorney before considering appraisal."),
    (3, "Do you have the carrier’s complete, itemized estimate?", "Request the full line-item estimate (not just the summary) in writing."),
    (3, "Do you have your own itemized estimate from a contractor or estimator?", "Get an independent, line-item estimate — a lump-sum bid won’t hold up before a panel."),
    (2, "Do you have dated photos of the damage taken soon after the loss?", "Gather every photo you have and note when each was taken. Add new photos of current conditions."),
    (2, "Have you read your policy’s appraisal clause?", "Find the ‘Appraisal’ paragraph in the conditions section and note any deadlines."),
    (2, "Do you know your policy’s suit-limitation date?", "Locate the ‘Suit Against Us’ clause and calendar the date — the claim calendar builder can help."),
    (2, "Have temporary repairs been made and receipts saved?", "Complete reasonable temporary repairs and keep every receipt."),
    (1, "Do you have your declarations page?", "Download or request your current declarations page."),
    (2, "Is all hidden damage opened up and documented?", "Make sure wet walls, attics and decking have been inspected so the scope is complete."),
    (1, "Is your correspondence with the carrier organized by date?", "Collect emails, letters and claim notes in date order."),
    (2, "Is the gap between estimates more than about 10% or $5,000?", "Run the numbers in the claim gap net-recovery estimator — a small gap may not justify appraisal costs."),
    (1, "Has a sworn proof of loss been submitted if the carrier asked for one?", "If a proof of loss was requested, submit it on time."),
]

READY = """
<div class="tool tool-wide" data-tool="ready">
  <div class="tool-head"><span>Appraisal file checkup</span><i>12 questions · two minutes</i></div>
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
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#f3ece0" stroke-width="18"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#f2c200" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3" style="transition:stroke-dashoffset .5s,stroke .3s"/></svg>
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


_INV_ROW = """<tr><td><input name="item" value="{0}" aria-label="Room or category"></td><td><input name="qty" inputmode="decimal" value="{1}" aria-label="Number of items"></td><td><input name="each" inputmode="decimal" value="{2}" aria-label="Average replacement cost per item"></td><td class="mono" data-o="row">$0</td><td><button type="button" class="x" aria-label="Remove row">×</button></td></tr>"""

CONTENTS = """
<div class="tool tool-wide" data-tool="inv">
  <div class="tool-head"><span>Wildfire contents inventory estimator</span><i>Room by room · nothing saved</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Room or category</th><th>Items</th><th>Avg. cost each ($)</th><th>Replacement total</th><th></th></tr></thead><tbody>
      """ + "".join(_INV_ROW.format(*r) for r in [("Kitchen &amp; pantry", 180, 45), ("Living room", 60, 160), ("Primary bedroom &amp; closet", 140, 85), ("Second bedroom", 70, 70), ("Garage, tools &amp; outdoor", 120, 95)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn ghost small" data-add data-run>+ Add room</button></div>
      <div class="row2">
        <div><label for="i-c">Personal property limit (Coverage C)</label><input id="i-c" name="covc" inputmode="decimal" value="120000"><span class="hint">From your declarations page.</span></div>
        <div><label for="i-a">Dwelling limit (Coverage A)</label><input id="i-a" name="cova" inputmode="decimal" value="260000"></div>
      </div>
      <div><label for="i-d">Average depreciation on contents</label>
        <div class="range"><input id="i-d" type="range" name="dep" min="0" max="70" step="5" value="35" data-unit="%"><output>35%</output></div>
        <span class="hint">Used only to show a rough actual-cash-value figure before replacement.</span></div>
    </div>
    <div class="tool-out" aria-live="polite" style="grid-template-columns:repeat(auto-fit,minmax(200px,1fr))">
      <div class="out-big"><small>Inventory at replacement cost</small><b data-o="rcv">$0</b></div>
      <div class="out-big"><small>Rough actual cash value</small><b data-o="acv">$0</b></div>
      <div class="out-big"><small>Room left under Coverage C</small><b data-o="room">$0</b></div>
      <div class="out-rows" style="grid-column:1/-1">
        <div><span>Items counted</span><b data-o="items">0</b></div>
        <div><span>Coverage C as % of Coverage A</span><b data-o="cpct">—</b></div>
        <div><span>Inventory as % of Coverage C</span><b data-o="used">—</b></div>
      </div>
      <p class="out-msg" data-o="msg" style="grid-column:1/-1"></p>
    </div>
  </div>
</div>"""

_FAQ_PRIV = ("Is anything I type saved or sent?", "No. The tool runs entirely in your browser. Close the page and the numbers are gone.")

TOOLS = [
    {
        "slug": "claim-gap-net-recovery-estimator", "name": "Claim Gap Net-Recovery Estimator", "icon": "Δ", "kind": "Estimator",
        "keyword": "insurance appraisal cost calculator",
        "short": "Measure the dispute, test where an award might land and subtract appraiser and umpire fees to see the net.",
        "title": "Insurance Appraisal Cost Calculator | Net Recovery",
        "desc": "Free insurance appraisal cost calculator: compare two estimates, test a likely award and subtract appraiser and umpire fees to see your net.",
        "h1": "Claim Gap Net-Recovery Estimator",
        "lede": "Two estimates, one slider and your fee arrangement. See whether appraisal is likely to leave more money in your pocket after it pays for itself.",
        "markup": GAP_FULL,
        "explain": """
<h2>Reading the result</h2>
<p>The estimator measures the dispute (your replacement-cost number minus the carrier’s), places a hypothetical award somewhere inside that gap, then takes away what you would spend to get there: your appraiser’s fee and half of a typical umpire fee. What remains is the net change a successful appraisal might produce.</p>
<h3>Run three scenarios, not one</h3>
<p>Slide the award to 30%, 50% and 75%. If the net only turns positive near 100%, the dispute probably depends on items that are hard to prove. If it stays positive at 30%, appraisal is more likely to be worth the time and fees.</p>
<h2>What the estimator doesn’t include</h2>
<ul><li>Deductibles and policy limits — use the <a href="/claim-estimators/percentage-deductible-converter/">percentage deductible converter</a>.</li>
<li>Depreciation timing — use the <a href="/claim-estimators/depreciation-holdback-splitter/">depreciation holdback splitter</a>.</li>
<li>Coverage questions. Appraisal values a covered loss; it doesn’t decide what’s covered.</li></ul>
<p><strong>Illustrative example:</strong> the default figures (a $21,600 carrier estimate against a $34,900 contractor estimate) are invented to show how the math works. They are not a real claim or a predicted result.</p>
""",
        "faqs": [("Is the projected award a prediction?", "No. It is a scenario you choose with the slider. Real awards depend on documentation, the panel and the policy wording."), ("Why include half of an umpire fee?", "Most appraisal clauses split the umpire’s cost equally between you and the insurer, even if the umpire is never needed for every item."), _FAQ_PRIV],
    },
    {
        "slug": "depreciation-holdback-splitter", "name": "Depreciation Holdback Splitter", "icon": "½", "kind": "Calculator",
        "keyword": "RCV ACV depreciation calculator",
        "short": "Split a replacement-cost claim into the first ACV check and the depreciation held back until repairs.",
        "title": "RCV vs ACV Depreciation Calculator | Holdback Splitter",
        "desc": "RCV vs ACV depreciation calculator: list damaged items by age and lifespan to estimate the first check, the holdback and the full recovery.",
        "h1": "Depreciation Holdback Splitter (RCV vs. ACV)",
        "lede": "Replacement-cost policies usually pay twice: actual cash value first, then the held-back depreciation after the work is done. Add your items and see the split.",
        "markup": DEP,
        "explain": """
<h2>How the split is calculated</h2>
<p>Each row is depreciated straight-line: age divided by expected life, capped at the maximum you pick. The first payment is the depreciated total minus your deductible. The holdback is the depreciation you can usually recover once repairs are complete — unless the policy pays actual cash value only.</p>
<h2>Life expectancies that come up in New Mexico estimates</h2>
<div class="table-wrap"><table><thead><tr><th>Item</th><th>Range often used</th></tr></thead><tbody>
<tr><th>Built-up or modified-bitumen flat roof</th><td>15–25 years</td></tr><tr><th>Elastomeric roof coating</th><td>5–10 years</td></tr><tr><th>Architectural shingles</th><td>25–30 years</td></tr><tr><th>Evaporative cooler</th><td>10–15 years</td></tr><tr><th>Stucco finish coat</th><td>20–30 years</td></tr><tr><th>Interior paint</th><td>8–12 years</td></tr>
</tbody></table></div>
<p>These ranges are general reference points, not rules. Estimating software and adjusters may use different figures, and condition matters as much as age.</p>
<h2>Don’t miss the recovery window</h2>
<p>Most replacement-cost policies set a time limit to finish repairs and claim the holdback. Put it on your calendar with the <a href="/claim-estimators/claim-calendar-builder/">claim calendar builder</a>.</p>
""",
        "faqs": [("Can labor be depreciated?", "Practices vary by policy and by court decision. Ask the carrier to explain in writing how its estimate treats labor, and talk to a New Mexico attorney if the answer matters to your claim."), ("What if I decide not to rebuild?", "Under most replacement-cost policies you keep the actual cash value payment but may give up the held-back depreciation."), _FAQ_PRIV],
    },
    {
        "slug": "roof-area-pitch-converter", "name": "Roof Area & Pitch Converter", "icon": "◿", "kind": "Converter",
        "keyword": "roof squares calculator",
        "short": "Turn a footprint and pitch into true roof squares, order quantity and a steep-charge check.",
        "title": "Roof Squares Calculator | Pitch & Waste Converter",
        "desc": "Roof squares calculator for insurance claims: convert footprint, pitch and waste into true roof area, then check the squares in your estimate.",
        "h1": "Roof Area & Pitch Converter for Claim Estimates",
        "lede": "A short measurement is one of the quietest ways a roof claim comes up short. Convert your footprint into real roof squares and compare.",
        "markup": ROOF,
        "explain": """
<h2>The math behind the multiplier</h2>
<p>Roof surface grows with slope. The pitch multiplier is √(1 + (rise ÷ 12)²). A 4/12 roof is about 5.4% larger than its footprint; an 8/12 roof is about 20.2% larger; a 12/12 roof about 41.4%.</p>
<h2>Flat and low-slope roofs</h2>
<p>Many New Mexico homes have flat roofs behind parapets. Pick 2/12 or lower for a close approximation, but remember that parapet walls, cants, crickets and flashing are measured and priced separately from the field of the roof. Those are the items most often missing from a carrier’s flat-roof scope.</p>
<h2>Checking an estimate</h2>
<ul><li>Compare total squares and the waste percentage with this result; a gap over 5–10% is worth asking about.</li>
<li>Look for steep charges (commonly 7/12 and up) and two-story charges.</li>
<li>Confirm drip edge, starter, ridge cap, valley metal and flashing are listed.</li></ul>
""",
        "faqs": [("What is a roofing square?", "One square is 100 square feet of roof surface, measured on the slope rather than on the ground."), ("Is this as good as an aerial report?", "No. Roofs with several planes, dormers or valleys need to be measured plane by plane. Use this as a sanity check."), _FAQ_PRIV],
    },
    {
        "slug": "percentage-deductible-converter", "name": "Percentage Deductible Converter", "icon": "%", "kind": "Converter",
        "keyword": "percentage deductible calculator",
        "short": "See a 1–10% wind/hail deductible in dollars and what a storm claim would actually pay.",
        "title": "Percentage Deductible Calculator | Wind & Hail Dollars",
        "desc": "Percentage deductible calculator: turn a wind or hail deductible into dollars and compare what a storm claim pays against a flat deductible.",
        "h1": "Percentage Deductible Converter for Wind & Hail Claims",
        "lede": "A 2% deductible sounds modest until it is multiplied by your dwelling limit. Convert it to dollars before you file or dispute a storm claim.",
        "markup": DEDUCT,
        "explain": """
<h2>Why it matters for hail-belt policies</h2>
<p>Insurers writing in hail-prone parts of New Mexico — the eastern plains, the Albuquerque metro and the Four Corners — sometimes use a separate wind/hail deductible set as a percentage of Coverage A. On a $320,000 dwelling limit, 2% is $6,400, not the $1,000 printed elsewhere on the declarations page.</p>
<h2>Where to find yours</h2>
<p>Check the declarations page for “wind/hail,” “windstorm or hail” or a percentage next to a deductible. Endorsements later in the policy explain when it applies.</p>
<h2>What it means for appraisal</h2>
<p>The deductible doesn’t change the amount of loss an appraisal panel sets, but it changes what you receive. A loss barely above the deductible may not justify appraisal fees; one far above it might.</p>
<p><strong>Illustrative example:</strong> the default numbers are made up to show the calculation.</p>
""",
        "faqs": [("Is the percentage taken from the claim or from my coverage?", "Usually from the Coverage A dwelling limit, then applied to the whole wind or hail loss. Your policy wording controls."), ("Can I lower it?", "Typically only at renewal, and a lower deductible usually costs more in premium."), _FAQ_PRIV],
    },
    {
        "slug": "claim-calendar-builder", "name": "Claim Calendar Builder", "icon": "▦", "kind": "Planner",
        "keyword": "insurance claim deadline calculator",
        "short": "Build a date-of-loss timeline for notice, repairs, proof of loss, holdback and suit dates, then export .ics.",
        "title": "Insurance Claim Deadline Calculator | .ics Calendar",
        "desc": "Insurance claim deadline calculator: enter the date of loss and your policy’s windows, see each milestone and export them as a calendar file.",
        "h1": "Claim Calendar Builder for New Mexico Property Claims",
        "lede": "Deadlines keep running while a claim is in dispute. Enter your date of loss and the windows in your policy, then download the milestones to your calendar.",
        "markup": DATES,
        "explain": """
<h2>Milestones worth tracking</h2>
<ul><li><strong>Notice.</strong> Policies require prompt notice. Late notice is a common carrier defense.</li>
<li><strong>Temporary repairs.</strong> Mitigation protects the property and the claim; keep receipts.</li>
<li><strong>Proof of loss.</strong> If the insurer asks for a sworn proof of loss, the policy sets a response window — often counted from the request.</li>
<li><strong>Depreciation recovery.</strong> Replacement-cost holdback usually requires repairs within a set time.</li>
<li><strong>Suit limitation.</strong> Policies contain a “Suit Against Us” clause. How New Mexico law treats that period is a legal question for a New Mexico attorney.</li></ul>
<div class="note"><b class="h">Not legal advice</b>The calendar uses the numbers you enter. It doesn’t interpret your policy or New Mexico law, and invoking appraisal doesn’t automatically pause any deadline.</div>
""",
        "faqs": [("Which date is the date of loss?", "Usually the day the storm, fire or leak happened, not the day you noticed it. Weather records can help pin down a hail date."), ("Does the .ics file work with my phone?", "Yes. Google Calendar, Apple Calendar and Outlook all import .ics files as all-day events."), _FAQ_PRIV],
    },
    {
        "slug": "appraisal-file-checkup", "name": "Appraisal File Checkup", "icon": "✓", "kind": "Checklist",
        "keyword": "appraisal readiness checklist",
        "short": "Twelve yes/no questions that score your claim file and build a to-do list before you demand appraisal.",
        "title": "Appraisal Readiness Checklist | File Checkup Score",
        "desc": "Appraisal readiness checklist: answer twelve yes-or-no questions to score your claim file and get a to-do list before you demand appraisal.",
        "h1": "Appraisal File Checkup: Is Your Claim Ready?",
        "lede": "Appraisals are decided by the file you bring to the panel. Answer twelve quick questions to see what is ready and what still needs work.",
        "markup": READY,
        "explain": """
<h2>How the checkup is weighted</h2>
<p>Coverage, itemized estimates and evidence count most, because they decide whether appraisal is the right tool and how well your number holds up. Paperwork items count less because they are easier to fix.</p>
<h2>What your score suggests</h2>
<ul><li><strong>75 or higher:</strong> a solid file. A professional look at the dollar gap is the next step.</li>
<li><strong>45 to 74:</strong> close the open items first — each one strengthens your position.</li>
<li><strong>Under 45:</strong> demanding appraisal now could lock in a low number. Build the file first.</li></ul>
""",
        "faqs": [("Is my score saved?", "No. Answers stay in your browser and disappear when you leave the page."), ("Should I share the result with an appraiser?", "Yes. A screenshot of your to-do list is a useful starting point for a first conversation."), ("Does a high score mean I will win?", "No. It measures preparation, not outcome. No appraiser can guarantee an award.")],
    },
    {
        "slug": "wildfire-contents-inventory-estimator", "name": "Wildfire Contents Inventory Estimator", "icon": "▤", "kind": "Estimator",
        "keyword": "wildfire contents inventory calculator",
        "short": "Rough out a room-by-room personal property inventory and compare it with your Coverage C limit.",
        "title": "Wildfire Contents Inventory Calculator | Coverage C",
        "desc": "Wildfire contents inventory calculator: estimate personal property room by room and compare the total with your Coverage C limit.",
        "h1": "Wildfire Contents Inventory Estimator",
        "lede": "After a total loss, the contents claim is often the hardest part. Rough out your inventory by room to see how it compares with your personal property limit.",
        "markup": CONTENTS,
        "explain": """
<h2>Why a rough inventory helps</h2>
<p>When a home is lost to wildfire, the insurer still expects a personal property inventory. Families who lived through fires like Hermits Peak/Calf Canyon or the 2024 South Fork and Salt fires near Ruidoso know how overwhelming that list is. Starting with room totals shows whether you are near your Coverage C limit — which tells you how much detail the full inventory will need.</p>
<h2>How to use the result</h2>
<ul><li><strong>Inventory well above the limit:</strong> the limit is likely the ceiling. Focus on documenting enough to reach it.</li>
<li><strong>Inventory below the limit:</strong> every item you remember adds value. Work room by room, closet by closet.</li>
<li><strong>Check the policy:</strong> some policies waive itemization or pay a percentage of Coverage C after a total loss. Ask the carrier in writing.</li></ul>
<h2>What it leaves out</h2>
<p>Special-limit items (jewelry, firearms, cash, collectibles), additional living expense and debris removal are separate. The averages you enter are yours; the defaults are illustrative only.</p>
""",
        "faqs": [("Do I need receipts for everything?", "Usually not, but you need a reasonable description, age and replacement price for each item. Photos, videos, bank records and online order histories all help."), ("Can appraisal resolve a contents dispute?", "Often, if the disagreement is about value rather than coverage. Contents appraisals turn on item descriptions and pricing support."), _FAQ_PRIV],
    },
]
