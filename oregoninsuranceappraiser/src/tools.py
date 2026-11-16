"""Interactive claim tools: markup + explanatory copy. Logic lives in static/assets/js/app.js.
Everything runs in the browser; nothing is stored or sent."""

TB = "/oregon-claim-calculators/"

PAYOFF_FULL = """
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Appraisal payoff estimator</span><i>Runs in your browser</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Insurer’s estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="21600"><span class="hint">Replacement cost total on the insurer’s estimate.</span></div>
        <div><label for="g-own">Your estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="38900"><span class="hint">Your contractor’s or independent estimate.</span></div>
      </div>
      <div><label for="g-land">Likely landing point within the gap</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% means the insurer’s number holds; 100% means your number is awarded in full.</span></div>
      <div class="row2">
        <div><label for="g-ft">Appraiser fee arrangement</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of the increase (%)</option></select></div>
        <div><label for="g-fee">Fee amount</label><input id="g-fee" name="fee" inputmode="decimal" value="3000"></div>
      </div>
      <label class="check"><input type="checkbox" name="useump" checked> Add my half of an umpire’s fee</label>
      <div><label for="g-ump">Umpire’s total fee</label><input id="g-ump" name="umpire" inputmode="decimal" value="3500"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated net gain at your landing point</small><b data-o="net">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s1"></span><span class="s2"></span><span class="s3"></span></div>
      <div class="legend"><span><i class="s1"></i>Insurer’s number</span><span><i class="s2"></i>Your net gain</span><span><i class="s3"></i>Appraisal costs</span></div>
      <div class="scen"><div><small>Cautious (30%)</small><b data-o="lo">$0</b></div><div><small>Middle (55%)</small><b data-o="mid">$0</b></div><div><small>Strong (80%)</small><b data-o="hi">$0</b></div></div>
      <div class="out-rows">
        <div><span>Amount in dispute</span><b data-o="gap">$0</b></div>
        <div><span>Gap as % of insurer’s estimate</span><b data-o="pct">—</b></div>
        <div><span>Projected award (RCV)</span><b data-o="award">$0</b></div>
        <div><span>Gross increase</span><b data-o="gain">$0</b></div>
        <div><span>Your appraisal costs</span><b data-o="cost">$0</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

PAYOFF_MINI = """
<div class="tool" data-tool="gap" style="margin:0">
  <div class="tool-head"><span>Two-number gap check</span><i>No sign-up</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="m-ins">Insurer’s estimate</label><input id="m-ins" name="insurer" inputmode="decimal" value="16800"></div>
      <div><label for="m-own">Your contractor’s estimate</label><input id="m-own" name="yours" inputmode="decimal" value="29400"></div>
      <div><label for="m-land">Award lands at</label><div class="range"><input id="m-land" type="range" name="land" min="0" max="100" step="5" value="50" data-unit="%"><output>50%</output></div><span class="hint">of the disputed amount</span></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Amount in dispute</small><b data-o="gap">$0</b></div>
      <div class="out-rows">
        <div><span>Gap vs. insurer’s estimate</span><b data-o="pct">—</b></div>
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
  <div class="tool-head"><span>Depreciation &amp; holdback tracker</span><i>Add as many line items as you need</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Composition roof (30-yr)", 21400, 12, 30), ("Cedar fence, 140 ft", 6200, 8, 20), ("Interior paint, main floor", 3100, 5, 10)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn ghost small" data-add data-run>+ Add line item</button></div>
      <div class="row2">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="2500"></div>
        <div><label for="d-cap">Depreciation cap</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="90">90%</option></select><span class="hint">Many estimates cap depreciation; check yours.</span></div>
      </div>
      <div class="row2">
        <div><label for="d-lab">Labor share of each item (%)</label><input id="d-lab" name="labor" inputmode="decimal" value="45"></div>
        <div><label for="d-dl">Is labor depreciated?</label><select id="d-dl" name="deplabor"><option value="yes" selected>Yes, on the whole line</option><option value="no">No, materials only</option></select><span class="hint">Estimates differ; compare both settings.</span></div>
      </div>
      <label class="check"><input type="checkbox" name="nonrec"> My policy pays actual cash value only (no recoverable depreciation)</label>
    </div>
    <div class="tool-out" aria-live="polite">
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

ROOF = """
<div class="tool" data-tool="roof">
  <div class="tool-head"><span>Roof pitch &amp; squares converter</span><i>Check the insurer’s count</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <fieldset class="bare"><legend class="sr-only">Measurement method</legend>
        <div class="btn-row">
          <label class="check"><input type="radio" name="mode" value="dims" checked> Footprint length × width</label>
          <label class="check"><input type="radio" name="mode" value="area"> I know the footprint area</label>
        </div></fieldset>
      <div class="row2" data-mode="dims">
        <div><label for="r-l">Footprint length (ft)</label><input id="r-l" name="len" inputmode="decimal" value="52"></div>
        <div><label for="r-w">Footprint width (ft)</label><input id="r-w" name="wid" inputmode="decimal" value="36"></div>
      </div>
      <div data-mode="dims"><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="18"></div>
      <div data-mode="area" hidden><label for="r-a">Footprint area incl. overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="2100"></div>
      <div class="row2">
        <div><label for="r-p">Roof pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 8 else "", p) for p in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16]) + """</select></div>
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="10">10% · simple gable</option><option value="12" selected>12% · gable with dormers</option><option value="15">15% · hip roof</option><option value="18">18% · complex, cut-up</option></select></div>
      </div>
      <div class="row2">
        <div><label for="r-c">Squares on the insurer’s estimate (optional)</label><input id="r-c" name="carrier" inputmode="decimal" placeholder="e.g. 22.5"></div>
        <div><label for="r-pr">Installed price per square (optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 560"></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Roof squares (before waste)</small><b data-o="sq">0</b></div>
      <div class="out-rows">
        <div><span>Pitch angle</span><b data-o="deg">0°</b></div>
        <div><span>Pitch multiplier</span><b data-o="mult">1.000</b></div>
        <div><span>Roof surface area</span><b data-o="surface">0</b></div>
        <div><span>Squares with waste</span><b data-o="order">0</b></div>
        <div><span>Shingle bundles (3 per square)</span><b data-o="bundles">0</b></div>
        <div><span>Difference vs. insurer’s squares</span><b data-o="cmp">—</b></div>
        <div><span>Rough replacement cost</span><b data-o="cost">—</b></div>
      </div>
      <p class="out-msg" data-o="steep"></p>
    </div>
  </div>
</div>"""

DEDUCT = """
<div class="tool" data-tool="deduct">
  <div class="tool-head"><span>Percentage deductible checker</span><i>Earthquake · wind · hail</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-t">Which deductible?</label><select id="w-t" name="dtype"><option value="eq">Earthquake endorsement</option><option value="wind" selected>Wind / hail</option></select></div>
      <div><label for="w-a">Dwelling limit (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="465000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Percentage deductible</label><select id="w-p" name="pct"><option value="1">1%</option><option value="2" selected>2%</option><option value="5">5%</option><option value="10">10%</option><option value="15">15%</option><option value="20">20%</option><option value="25">25%</option></select></div>
        <div><label for="w-f">Standard flat deductible</label><input id="w-f" name="flat" inputmode="decimal" value="1000"></div>
      </div>
      <div><label for="w-l">Estimated damage</label><input id="w-l" name="loss" inputmode="decimal" value="24800"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your percentage deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s3"></span><span class="s1"></span></div>
      <div class="legend"><span><i class="s3"></i>You pay</span><span><i class="s1"></i>Policy pays</span></div>
      <div class="out-rows">
        <div><span>Payment with the % deductible</span><b data-o="pdpay">$0</b></div>
        <div><span>Payment if the flat deductible applied</span><b data-o="flatpay">$0</b></div>
        <div><span>Extra out of pocket</span><b data-o="diff">$0</b></div>
      </div>
      <p class="out-msg" data-o="below"></p>
      <p class="out-msg" data-o="note"></p>
    </div>
  </div>
</div>"""

DATES = """
<div class="tool" data-tool="dates">
  <div class="tool-head"><span>Oregon claim calendar builder</span><i>Exports an .ics file</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
        <div><label for="t-a">Appraisal demand date (optional)</label><input id="t-a" type="date" name="dem"></div>
      </div>
      <p class="hint" style="margin:0">Set each window to match your policy. Defaults are common figures, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report the claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="3"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="10"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Often counted from the insurer’s request.</span></div>
        <div><label for="t-r">Depreciation recovery (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="365"></div>
        <div><label for="t-s">Suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="730"><span class="hint">Two years is 730 days.</span></div>
        <div><label for="t-x">Name your appraiser within (days of demand)</label><input id="t-x" name="nameapp" inputmode="numeric" value="20"></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download .ics calendar file</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the insurer accepted coverage for at least part of the loss?", "Get written confirmation that coverage is accepted. If the claim was denied, talk to an Oregon attorney before considering appraisal."),
    (3, "Do you have the insurer’s complete, line-item estimate?", "Ask in writing for the full itemized estimate, not just the summary page."),
    (3, "Do you have your own itemized estimate?", "Get a line-item estimate from a contractor or estimator. A lump-sum bid is hard to defend in front of a panel."),
    (2, "Do you have dated photos taken soon after the loss?", "Gather every photo and note when each was taken. Add current photos too."),
    (2, "Have you found and read the appraisal clause in your policy?", "Find the ‘Appraisal’ paragraph in the conditions and note any time limits."),
    (2, "Do you know your policy’s deadline to file suit?", "Find the ‘Suit Against Us’ condition and put the date on your calendar."),
    (2, "Are temporary repairs done and receipts saved?", "Make reasonable temporary repairs (tarps, drying) and keep every receipt."),
    (1, "Do you have your current declarations page?", "Download or request your declarations page from your agent or insurer."),
    (2, "Has hidden damage been opened and documented?", "Make sure attics, crawlspaces and wet walls have been checked so the scope is complete."),
    (1, "Is your correspondence with the insurer organized by date?", "Collect letters, emails and claim notes in date order."),
    (2, "Is the gap more than about 10% or $5,000?", "Run your numbers in the appraisal payoff estimator. A small gap may not justify the cost."),
    (1, "If the insurer asked for a sworn proof of loss, has it been sent?", "Return any requested proof of loss on time."),
]

READY = """
<div class="tool tool-wide" data-tool="ready">
  <div class="tool-head"><span>Appraisal readiness checkup</span><i>12 questions · about two minutes</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <ol class="quiz">""" + "".join(
    '<li data-w="%d" data-fix="%s"><span>%s</span><span class="yn"><button type="button" class="yes" aria-pressed="false">Yes</button><button type="button" class="no" aria-pressed="false">No</button></span></li>' % (w, f, q)
    for w, q, f in _QUIZ) + """
      </ol>
      <div class="btn-row"><button type="button" class="btn ghost small" data-reset>Reset answers</button></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="gauge-wrap">
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#e3e8f4" stroke-width="18"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#002a86" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3" style="transition:stroke-dashoffset .5s,stroke .3s"/></svg>
        <div class="gauge-num"><span data-o="score">–</span></div>
        <p class="hint" style="text-align:center">Answered <span data-o="count">0 / 12</span></p>
      </div>
      <div>
        <p class="out-msg" data-o="verdict"></p>
        <p class="todo-h">Your to-do list</p>
        <ul data-o="todo" class="todo"></ul>
      </div>
    </div>
  </div>
</div>"""

_ROOMS = [("bed", "Bedrooms", 3, 9000), ("bath", "Bathrooms", 2, 2200), ("kit", "Kitchen", 1, 16000), ("liv", "Living / family rooms", 2, 11000),
          ("din", "Dining room", 1, 6000), ("off", "Office / den", 1, 7000), ("gar", "Garage / shop", 1, 12000), ("out", "Patio, yard &amp; storage", 1, 5000)]

CONTENTS = """
<div class="tool tool-wide" data-tool="contents">
  <div class="tool-head"><span>Wildfire contents estimator</span><i>Room by room · illustrative values</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Room type</th><th>How many</th><th>Typical replacement value per room ($)</th></tr></thead><tbody>""" + "".join(
    f'<tr><td>{n}</td><td><input name="n-{k}" inputmode="numeric" value="{c}" aria-label="{n} count"></td><td><input name="v-{k}" inputmode="decimal" value="{v}" aria-label="{n} value per room"></td></tr>' for k, n, c, v in _ROOMS) + """
      </tbody></table></div>
      <div class="row2">
        <div><label for="c-lvl">How furnished is the home?</label><select id="c-lvl" name="lvl"><option value="0.7">Lightly</option><option value="1" selected>Typical</option><option value="1.4">Well furnished</option><option value="1.9">Extensively</option></select></div>
        <div><label for="c-yrs">Average age of belongings (years)</label><input id="c-yrs" name="yrs" inputmode="decimal" value="7"></div>
      </div>
      <div class="row2">
        <div><label for="c-a">Dwelling limit (Coverage A)</label><input id="c-a" name="cova" inputmode="decimal" value="420000"></div>
        <div><label for="c-c">Contents limit (Coverage C)</label><input id="c-c" name="covc" inputmode="decimal" value="210000"><span class="hint">Often 50% to 75% of the dwelling limit.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated replacement cost of contents</small><b data-o="rcv">$0</b></div>
      <div class="out-big"><small>Rough actual cash value</small><b data-o="acv">$0</b></div>
      <div class="out-big"><small>Shortfall vs. contents limit</small><b data-o="short">$0</b></div>
      <div class="out-rows">
        <div><span>Contents limit as % of dwelling</span><b data-o="cpct">—</b></div>
        <div><span>Estimate as % of contents limit</span><b data-o="use">—</b></div>
        <div><span>Approx. depreciation applied</span><b data-o="dpct">—</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "appraisal-payoff-estimator", "name": "Appraisal Payoff Estimator", "icon": "$", "kind": "Calculator",
        "short": "Find the disputed amount, test three award scenarios and see your net after appraiser and umpire fees.",
        "title": "Appraisal Payoff Estimator | Free Claim Calculator",
        "desc": "Appraisal payoff estimator: compare your estimate with the insurer’s, test three award scenarios and subtract fees to see what you would net.",
        "h1": "Appraisal Payoff Estimator: Will Appraisal Pay Off?",
        "lede": "Enter the insurer’s estimate and yours, choose where an award might land, and add realistic fees. Three side-by-side scenarios show whether appraisal still makes sense if things go only partly your way.",
        "markup": PAYOFF_FULL,
        "explain": f"""
<h2>Using the estimator</h2>
<ol><li><strong>Enter the insurer’s replacement cost total</strong>, before depreciation and deductible.</li>
<li><strong>Enter your estimate</strong> at replacement cost too, so you compare like with like.</li>
<li><strong>Set a landing point.</strong> The slider is your best guess; the three scenario boxes always show 30%, 55% and 80% so you see a range.</li>
<li><strong>Add fees</strong> using your appraiser’s quote and a realistic umpire fee, usually shared equally.</li></ol>
<h2>Reading the three scenarios</h2>
<p>If appraisal only pays off in the “strong” column, your case depends on everything going right. If the “cautious” column is still comfortably positive, the dispute is more likely worth pursuing. All figures are illustrative and depend entirely on what you enter.</p>
<h2>What it doesn’t include</h2>
<p>Deductibles, policy limits and the timing of recoverable depreciation change what you are paid but not the size of the dispute. For the payment split, use the <a href="{TB}depreciation-holdback-tracker/">depreciation and holdback tracker</a>.</p>
""",
        "faqs": [("Is the projected award a prediction?", "No. It’s a planning scenario based on the numbers you enter. Real awards depend on documentation, the panel and the policy."), ("How much does an umpire cost?", "It varies with the size and complexity of the claim. Ask for a written quote once an umpire is proposed; most policies split the fee equally.")],
    },
    {
        "slug": "depreciation-holdback-tracker", "name": "Depreciation & Holdback Tracker", "icon": "ACV", "kind": "Calculator",
        "short": "List damaged items to estimate the first ACV payment, the holdback and the total once repairs are done.",
        "title": "Depreciation & Holdback Tracker | RCV vs ACV",
        "desc": "Depreciation and holdback tracker: list items by age and life, choose whether labor is depreciated, and see your ACV check, holdback and total.",
        "h1": "Depreciation and Holdback Tracker (RCV vs. ACV)",
        "lede": "Replacement cost policies usually pay twice: an actual cash value payment now and the held-back depreciation after repairs. Add your items, toggle labor depreciation, and see how the money splits.",
        "markup": DEP,
        "explain": f"""
<h2>How the tracker estimates depreciation</h2>
<p>It uses straight-line depreciation (age divided by expected life), capped at the maximum you choose. The labor setting lets you compare an estimate that depreciates the whole line with one that depreciates materials only. Real estimates may use condition adjustments or treat some items as non-depreciable, so treat the result as a planning figure.</p>
<h2>Life expectancies often seen in estimates</h2>
<div class="table-wrap"><table><thead><tr><th>Item</th><th>Common range</th></tr></thead><tbody>
<tr><th>Composition shingles</th><td>20–30 years</td></tr><tr><th>Cedar shake roof</th><td>20–30 years</td></tr><tr><th>Cedar fence</th><td>15–20 years</td></tr><tr><th>Interior paint</th><td>8–12 years</td></tr><tr><th>Carpet</th><td>8–12 years</td></tr><tr><th>Water heater</th><td>10–15 years</td></tr>
</tbody></table></div>
<h2>Collecting the holdback</h2>
<p>Most policies release recoverable depreciation once repairs are finished within a time limit. Send invoices and photos of completed work, and use the <a href="{TB}claim-calendar-builder/">claim calendar builder</a> to track the deadline.</p>
""",
        "faqs": [("Can an insurer depreciate labor in Oregon?", "Practices vary by policy and are the subject of ongoing legal debate in several states. Ask the insurer to explain in writing how its estimate treats labor, and consult an attorney if it matters to your claim."), ("What happens if I don’t repair?", "Under most replacement cost policies you keep the ACV payment but may not collect the held-back depreciation.")],
    },
    {
        "slug": "roof-pitch-squares-converter", "name": "Roof Pitch & Squares Converter", "icon": "▲", "kind": "Calculator",
        "short": "Turn a footprint and pitch into true roof squares and compare them with the insurer’s count.",
        "title": "Roof Pitch & Squares Converter for Claims",
        "desc": "Roof pitch and squares converter: turn footprint, pitch and waste into true roof squares and bundles, then compare with the insurer’s count.",
        "h1": "Roof Pitch and Squares Converter for Insurance Claims",
        "lede": "Steep Oregon roofs hide a lot of surface area. Enter the footprint and pitch to estimate true roof squares, see the pitch angle, and compare the result with the squares on the insurer’s estimate.",
        "markup": ROOF,
        "explain": """
<h2>The math</h2>
<p>A sloped roof has more surface than the footprint under it. The pitch multiplier is √(1 + (rise ÷ 12)²): an 8/12 roof is about 20% larger than its footprint and a 12/12 roof about 41% larger. The converter also shows the pitch as an angle in degrees.</p>
<h2>Comparing with the estimate</h2>
<ul><li>Find the total roof squares and the waste percentage on the insurer’s estimate and enter the squares.</li>
<li>A difference of more than 5–10% deserves a closer look at the measurements.</li>
<li>Check for steep-roof and high-roof charges on steeper and two-story sections.</li>
<li>Make sure starter, ridge, drip edge, underlayment and flashing appear as separate items.</li></ul>
<h2>Limits</h2>
<p>Roofs with several pitches, dormers and valleys need to be measured plane by plane. Use this as a sanity check alongside a field or aerial measurement.</p>
""",
        "faqs": [("What is a roofing square?", "100 square feet of roof surface. Many two-story Oregon homes fall somewhere between 20 and 40 squares."), ("Why does the waste factor change?", "Hips, valleys and dormers require more cutting, so more material is wasted.")],
    },
    {
        "slug": "percentage-deductible-checker", "name": "Percentage Deductible Checker", "icon": "%", "kind": "Calculator",
        "short": "Convert an earthquake or wind/hail percentage deductible into dollars and see what a claim would pay.",
        "title": "Percentage Deductible Checker | Earthquake & Wind",
        "desc": "Percentage deductible checker: convert an earthquake or wind and hail deductible into dollars and compare what a claim pays against a flat one.",
        "h1": "Percentage Deductible Checker for Earthquake and Wind Claims",
        "lede": "In Oregon, percentage deductibles show up most on earthquake endorsements and sometimes on wind or hail. Ten percent of a dwelling limit is a large number. See yours in dollars.",
        "markup": DEDUCT,
        "explain": """
<h2>Why this matters in Oregon</h2>
<p>Standard homeowner policies generally exclude earthquake. Coverage is usually added by endorsement or a separate policy, and it commonly carries a percentage deductible, often 10% or more of the dwelling limit. Some policies also use percentage deductibles for wind or hail. On a $465,000 dwelling limit, a 10% deductible is $46,500.</p>
<h2>Where to find it</h2>
<p>Look on your declarations page for “earthquake,” “wind/hail” or “windstorm” deductible, then read the endorsement that defines when it applies and whether it is calculated on the dwelling limit or on each coverage.</p>
<h2>How it affects appraisal</h2>
<p>The deductible doesn’t change the amount of loss a panel decides, but it changes what you receive. A loss just above the deductible may not justify appraisal; one well above it may.</p>
""",
        "faqs": [("Does an earthquake deductible apply to contents separately?", "Some endorsements apply a separate percentage to each coverage; others apply one deductible to the whole loss. Read your endorsement."), ("Is the Cascadia earthquake risk covered by my homeowner policy?", "Generally not, unless you added earthquake coverage. Check your declarations page.")],
    },
    {
        "slug": "claim-calendar-builder", "name": "Claim Calendar Builder", "icon": "◷", "kind": "Planner",
        "short": "Build a timeline of notice, proof-of-loss, appraisal, holdback and suit dates and export it to your calendar.",
        "title": "Oregon Claim Calendar Builder | Deadline Planner",
        "desc": "Oregon claim calendar builder: enter your loss and appraisal demand dates to map proof-of-loss, holdback and suit deadlines, then export them.",
        "h1": "Oregon Insurance Claim Calendar Builder",
        "lede": "Policy deadlines keep running while you argue about the number. Enter your date of loss, and your appraisal demand date if there is one, to build a timeline you can download as a calendar file.",
        "markup": DATES,
        "explain": """
<h2>Dates worth tracking</h2>
<ul><li><strong>Prompt notice.</strong> Policies require you to report losses promptly. Late notice is a common defense.</li>
<li><strong>Proof of loss.</strong> If the insurer requests a sworn proof of loss, policies often allow 60 days.</li>
<li><strong>Naming an appraiser.</strong> Many appraisal clauses give each side a set number of days after a written demand to name its appraiser, often 20.</li>
<li><strong>Depreciation recovery.</strong> Replacement cost policies usually set a window to finish repairs and collect the holdback.</li>
<li><strong>Suit limitation.</strong> Oregon property policies commonly require a lawsuit within two years of the loss. Appraisal may not pause that clock.</li></ul>
<div class="note"><b class="h">Important</b>The calendar uses the numbers you enter. It isn’t legal advice. Some wildfire losses in declared emergencies may have different time limits under Oregon law. If a date is close, contact an Oregon attorney.</div>
""",
        "faqs": [("Is the date of loss the day I noticed the damage?", "Usually it’s the date of the storm or event. Weather records for your address can help pin it down."), ("Does demanding appraisal stop the suit deadline?", "Not automatically. Protect that date separately and talk to an attorney if it is approaching.")],
    },
    {
        "slug": "appraisal-readiness-checkup", "name": "Appraisal Readiness Checkup", "icon": "✓", "kind": "Checklist",
        "short": "Twelve yes/no questions that score your claim file and build a to-do list before you demand appraisal.",
        "title": "Appraisal Readiness Checkup | Is Your Claim Ready?",
        "desc": "Appraisal readiness checkup: twelve quick questions that score your claim file and give you a to-do list to finish before demanding appraisal.",
        "h1": "Appraisal Readiness Checkup for Your Claim File",
        "lede": "Appraisals are usually won or lost on the file you bring to them. Answer twelve questions to see where yours stands and what to finish before you send a demand.",
        "markup": READY,
        "explain": """
<h2>How the score is weighted</h2>
<p>Coverage, estimates and evidence carry the most weight because they decide whether appraisal is the right tool and how well your number will hold up. Paperwork items matter but are easier to fix.</p>
<h2>What your result means</h2>
<ul><li><strong>75 and up:</strong> a strong file. A professional review of the gap is the next step.</li>
<li><strong>45 to 74:</strong> close the open items first; each one strengthens your position.</li>
<li><strong>Below 45:</strong> demanding appraisal now risks locking in a low number. Build the file first.</li></ul>
""",
        "faqs": [("Are my answers saved?", "No. The checkup runs entirely in your browser and nothing is stored or sent."), ("Can I share the result with an appraiser?", "Yes. Take a screenshot or copy your to-do list and bring it to the first call.")],
    },
    {
        "slug": "wildfire-contents-estimator", "name": "Wildfire Contents Estimator", "icon": "▦", "kind": "Estimator",
        "short": "A room-by-room estimate of what a household’s belongings cost to replace, compared with your contents limit.",
        "title": "Wildfire Contents Estimator | Total-Loss Inventory",
        "desc": "Wildfire contents estimator: a room-by-room guess at what your belongings cost to replace, with rough ACV checked against your contents limit.",
        "h1": "Wildfire Contents Estimator for Total-Loss Claims",
        "lede": "After a total loss, listing every possession from memory is overwhelming. This estimator gives a rough, room-by-room starting figure and compares it with your contents limit, so you know the scale of the inventory ahead.",
        "markup": CONTENTS,
        "explain": f"""
<h2>Why we built this for Oregon</h2>
<p>The 2020 Labor Day fires left thousands of Oregon households with total losses and inventories running to thousands of items. Many families didn’t know whether their contents limit was close to what they had lost until months into the claim. This tool gives an early, rough answer.</p>
<h2>How it works</h2>
<ul><li>Each room type has an <strong>illustrative</strong> replacement value. Edit any value to match your home.</li>
<li>The furnishing level scales the total up or down.</li>
<li>Rough actual cash value applies a simple straight-line depreciation of about 6% a year, capped at 60%, to the average age you enter.</li>
<li>The result is compared with your contents limit to show any likely shortfall.</li></ul>
<div class="note"><b class="h">Illustrative only</b>The default values are examples, not data about any real claim or household. Your real inventory, the policy’s terms and the insurer’s pricing decide the claim.</div>
<h2>Turning the estimate into an inventory</h2>
<p>Work room by room, use photos, videos, bank and card statements and online order histories, and list items by brand, age and quantity. Oregon added protections after 2020 that, in some declared-emergency total losses, change how detailed an inventory must be or allow more time. Check the current rules with the Division of Financial Regulation. Our <a href="/property-appraisals/wildfire-loss-appraisal/">wildfire loss appraisal</a> page explains where contents disputes usually arise.</p>
<p>Track the deadlines with the <a href="{TB}claim-calendar-builder/">claim calendar builder</a>.</p>
""",
        "faqs": [("Are the room values real averages?", "No. They are illustrative starting points to help you think about scale. Replace them with your own figures."), ("Is my contents limit really 50% to 75% of my dwelling limit?", "That range is common on homeowner policies, but yours may differ. Check your declarations page.")],
    },
]
