"""Interactive claim tools: markup + explanatory copy. Logic lives in static/assets/js/app.js.
Tool headings inside widgets are <p class="tool-title"> (not headings) so page heading order stays clean."""

TB = "/calculators-for-policyholders/"

GAP_FULL = """
<div class="tool" data-tool="gap">
  <div class="tool-head"><p class="tool-title">Claim gap &amp; fee estimator</p><i>Runs in your browser</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Insurer’s estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="21600"><span class="hint">Replacement cost total on the carrier’s estimate.</span></div>
        <div><label for="g-own">Your estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="34900"><span class="hint">Your contractor’s or independent estimate.</span></div>
      </div>
      <div><label for="g-land">Where might the award land within the gap?</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% means the carrier’s number holds. 100% means your full number is awarded.</span></div>
      <div class="row2">
        <div><label for="g-ft">Your appraiser’s fee type</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of increase (%)</option></select></div>
        <div><label for="g-fee">Fee amount</label><input id="g-fee" name="fee" inputmode="decimal" value="2800"></div>
      </div>
      <label class="check"><input type="checkbox" name="useump" checked> Include half of an umpire’s fee</label>
      <div><label for="g-ump">Umpire’s total fee (split 50/50)</label><input id="g-ump" name="umpire" inputmode="decimal" value="3200"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated net increase to you</small><b data-o="net">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s1"></span><span class="s2"></span><span class="s3"></span></div>
      <div class="legend"><span><i class="s1"></i>Carrier’s number</span><span><i class="s2"></i>Your net gain</span><span><i class="s3"></i>Appraisal costs</span></div>
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
<div class="tool" data-tool="gap">
  <div class="tool-head"><p class="tool-title">Two-number gap check</p><i>Nothing is stored</i></div>
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
  <div class="tool-head"><p class="tool-title">Holdback recovery calculator</p><i>Add as many items as you need</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Architectural shingle roof", 19800, 11, 30), ("Gutters and downspouts", 2600, 11, 25), ("Interior ceiling paint", 1450, 5, 10)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn ghost small" data-add data-run>+ Add item</button></div>
      <div class="row2">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="1000"></div>
        <div><label for="d-cap">Maximum depreciation</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="90">90%</option></select><span class="hint">Many estimates cap depreciation. Check yours.</span></div>
      </div>
      <label class="check"><input type="checkbox" name="nonrec"> My policy pays actual cash value only (no recoverable depreciation)</label>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-trio">
        <div class="out-big"><small>First check (ACV − deductible)</small><b data-o="first">$0</b></div>
        <div class="out-big"><small>Held back until repairs</small><b data-o="held">$0</b></div>
        <div class="out-big"><small>Total if fully recovered</small><b data-o="total">$0</b></div>
      </div>
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
  <div class="tool-head"><p class="tool-title">Roof pitch &amp; squares checker</p><i>Compare against your estimate</i></div>
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
        <div><label for="r-p">Roof pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 8 else "", p) for p in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16]) + """</select></div>
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="10">10% — simple gable</option><option value="12" selected>12% — gable with dormers</option><option value="15">15% — hip roof</option><option value="18">18% — complex roof</option></select></div>
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

DEDUCT = """
<div class="tool" data-tool="deduct">
  <div class="tool-head"><p class="tool-title">Hurricane &amp; wind deductible converter</p><i>Percentage vs. flat</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling coverage (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="420000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Hurricane, named-storm or wind deductible</label><select id="w-p" name="pct"><option value="1">1%</option><option value="2" selected>2%</option><option value="3">3%</option><option value="5">5%</option><option value="10">10%</option></select></div>
        <div><label for="w-f">All-other-perils flat deductible</label><input id="w-f" name="flat" inputmode="decimal" value="1000"></div>
      </div>
      <div><label for="w-l">Estimated storm damage</label><input id="w-l" name="loss" inputmode="decimal" value="23800"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your percentage deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s3"></span><span class="s1"></span></div>
      <div class="legend"><span><i class="s3"></i>You pay</span><span><i class="s1"></i>Policy pays</span></div>
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
  <div class="tool-head"><p class="tool-title">Claim clock &amp; calendar builder</p><i>Exports to your calendar</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
      <p class="hint">Adjust each window to match your policy. Defaults are common figures, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="3"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="10"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Often 60 days from the insurer’s request.</span></div>
        <div><label for="t-r">Depreciation recovery (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="365"></div>
        <div><label for="t-s">Suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="730"><span class="hint">Two years is 730 days.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"><li><b>Pick your date of loss</b><span>Milestones will appear here.</span></li></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download .ics calendar file</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the insurer accepted coverage for at least part of the loss?", "Get written confirmation that coverage is accepted. If the claim was denied, talk to a Virginia attorney before considering appraisal."),
    (3, "Do you have the insurer’s complete, itemized estimate?", "Request the full line-item estimate, not just the summary page, in writing."),
    (3, "Do you have your own itemized estimate from a contractor or estimator?", "Get an independent line-item estimate. A lump-sum bid won’t hold up before a panel."),
    (2, "Do you have dated photos of the damage taken soon after the loss?", "Gather every photo you have and note when each was taken. Add photos of current conditions."),
    (2, "Have you read your policy’s appraisal clause?", "Find the ‘Appraisal’ paragraph in the policy conditions and note any deadlines."),
    (2, "Do you know your policy’s suit-limitation date?", "Locate the ‘Suit Against Us’ clause and calendar the date. Our claim calendar builder can help."),
    (2, "Have temporary repairs been made and receipts saved?", "Complete reasonable temporary repairs, such as tarps and water extraction, and keep every receipt."),
    (1, "Do you have your current declarations page?", "Download or request your declarations page from your agent or insurer."),
    (2, "Has all hidden damage been opened up and documented?", "Make sure wet walls, attics, crawlspaces and decking have been inspected so the scope is complete."),
    (1, "Is your correspondence with the insurer organized by date?", "Collect emails, letters and claim notes in date order."),
    (2, "Is the gap between estimates more than about 10% or $5,000?", "Run the numbers in our claim gap estimator. A small gap may not justify appraisal costs."),
    (1, "If the insurer asked for a sworn proof of loss, was it submitted on time?", "If a proof of loss was requested, return it before the deadline in the request."),
]

READY = """
<div class="tool tool-wide" data-tool="ready">
  <div class="tool-head"><p class="tool-title">Appraisal readiness scorecard</p><i>12 questions · about two minutes</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <ol class="quiz">""" + "".join(
    '<li data-w="%d" data-fix="%s"><span>%s</span><span class="yn"><button type="button" class="yes" aria-pressed="false">Yes</button><button type="button" class="no" aria-pressed="false">No</button></span></li>' % (w, f, q)
    for w, q, f in _QUIZ) + """
      </ol>
      <div class="btn-row"><button type="button" class="btn ghost small" data-reset>Reset answers</button></div>
    </div>
    <div class="tool-out score-out" aria-live="polite">
      <div>
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#e3e9f6" stroke-width="18"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#00297b" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3" style="transition:stroke-dashoffset .5s,stroke .3s"/></svg>
        <div class="gauge-num"><span data-o="score">–</span></div>
        <p class="hint center">Answered <span data-o="count">0 / 12</span></p>
      </div>
      <div>
        <p class="out-msg" data-o="verdict"></p>
        <p class="todo-h">Your to-do list</p>
        <ul class="todo" data-o="todo"></ul>
      </div>
    </div>
  </div>
</div>"""

TREE = """
<div class="tool" data-tool="tree">
  <div class="tool-head"><p class="tool-title">Fallen tree claim splitter</p><i>See what the policy limits leave you</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row3">
        <div><label for="x-hit">Trees that hit a covered structure</label><input id="x-hit" name="hit" inputmode="numeric" value="1"></div>
        <div><label for="x-blk">Trees blocking a driveway or ramp</label><input id="x-blk" name="block" inputmode="numeric" value="1"></div>
        <div><label for="x-oth">Trees down that hit nothing</label><input id="x-oth" name="other" inputmode="numeric" value="2"></div>
      </div>
      <div class="row2">
        <div><label for="x-rm">Removal &amp; haul-away cost per tree</label><input id="x-rm" name="per" inputmode="decimal" value="1400"><span class="hint">Cutting, hauling and stump work in the yard.</span></div>
        <div><label for="x-cr">Crane / lift-off from the house</label><input id="x-cr" name="crane" inputmode="decimal" value="3800"><span class="hint">Usually part of the dwelling repair, not debris removal.</span></div>
      </div>
      <div><label for="x-st">Structural repair estimate (roof, framing, interior)</label><input id="x-st" name="struct" inputmode="decimal" value="26500"></div>
      <div class="row3">
        <div><label for="x-cpt">Removal limit per tree</label><input id="x-cpt" name="cap1" inputmode="decimal" value="500"></div>
        <div><label for="x-cpl">Removal limit per loss</label><input id="x-cpl" name="cap2" inputmode="decimal" value="1000"></div>
        <div><label for="x-ded">Deductible</label><input id="x-ded" name="ded" inputmode="decimal" value="1000"></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated policy payment</small><b data-o="pay">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s1"></span><span class="s2"></span><span class="s3"></span></div>
      <div class="legend"><span><i class="s1"></i>Dwelling repair</span><span><i class="s2"></i>Covered removal</span><span><i class="s3"></i>You pay</span></div>
      <div class="out-rows">
        <div><span>Dwelling repair (crane + structure)</span><b data-o="dwell">$0</b></div>
        <div><span>Tree removal you’ll be billed</span><b data-o="rmall">$0</b></div>
        <div><span>Removal the policy covers</span><b data-o="rmcov">$0</b></div>
        <div><span>Removal not covered</span><b data-o="rmgap">$0</b></div>
        <div><span>Your total out-of-pocket</span><b data-o="oop">$0</b></div>
      </div>
      <p class="out-msg" data-o="tmsg"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "claim-gap-and-fee-estimator", "kw": "insurance appraisal cost calculator", "name": "Claim Gap & Fee Estimator", "icon": "Δ", "kind": "Estimator",
        "photo": "calculator-papers",
        "short": "Measure the disputed amount, test where an award might land and subtract realistic appraisal fees.",
        "title": "Insurance Appraisal Cost Calculator | Gap & Fees",
        "desc": "Insurance appraisal cost calculator: compare two estimates, test a likely award and subtract appraiser and umpire fees to see your net.",
        "h1": "Claim Gap & Fee Estimator: An Insurance Appraisal Cost Calculator",
        "lede": "Enter the insurer’s number and yours, move the slider to test outcomes, and add fees. You’ll see whether appraisal is likely to leave you ahead once its costs are paid.",
        "markup": GAP_FULL,
        "explain": """
<h2>Using the insurance appraisal cost calculator</h2>
<ol><li><strong>Enter the insurer’s replacement cost total</strong>, before depreciation and deductible.</li>
<li><strong>Enter your estimate</strong>, also at replacement cost, from a contractor or independent estimator.</li>
<li><strong>Test several outcomes.</strong> Try 30%, 55% and 80% on the slider instead of trusting one answer.</li>
<li><strong>Add fees</strong> using your appraiser’s quoted arrangement and a realistic umpire fee.</li></ol>
<h2>Reading the result</h2>
<p>If your net only turns positive near 100%, the case depends on winning every item, and that’s fragile. If it stays positive at 40% or 50%, the dispute is large enough that appraisal may be worth discussing. Example figures in the tool are illustrative.</p>
<h2>What it leaves out</h2>
<p>Deductibles, depreciation timing and policy limits change what you’re paid, not the size of the dispute. For those, use the <a href="/calculators-for-policyholders/holdback-recovery-calculator/">holdback recovery calculator</a> and the <a href="/calculators-for-policyholders/hurricane-wind-deductible-converter/">deductible converter</a>.</p>
""",
        "faqs": [("Is the projected award a prediction?", "No. It’s a scenario you choose. Real awards depend on documentation, the panel and your policy."), ("What do appraisers typically charge?", "Arrangements vary: flat fees, hourly rates or a percentage of the increase. Get the fee in writing before you sign, and compare it with the gap you’re trying to close.")],
    },
    {
        "slug": "holdback-recovery-calculator", "kw": "RCV vs ACV calculator", "name": "Holdback Recovery Calculator", "icon": "ACV", "kind": "Calculator",
        "photo": "laptop-estimate",
        "short": "Split a claim into the first ACV check, the depreciation held back and the total after repairs.",
        "title": "RCV vs ACV Calculator | Depreciation Holdback",
        "desc": "RCV vs ACV calculator for Virginia claims: list items with age and life to estimate your first check, depreciation holdback and full payout.",
        "h1": "Holdback Recovery Calculator (RCV vs. ACV)",
        "lede": "Replacement cost policies usually pay twice: an actual cash value check now and the held-back depreciation after repairs. List your items to see how the money splits.",
        "markup": DEP,
        "explain": """
<h2>How this RCV vs ACV calculator estimates depreciation</h2>
<p>It uses straight-line depreciation, age divided by expected life, capped at the maximum you choose. Real estimates may adjust for condition, use different life tables or leave items like permits undepreciated, so treat the result as a planning number.</p>
<h2>Common life expectancies in estimates</h2>
<div class="table-wrap"><table><thead><tr><th>Item</th><th>Common range</th></tr></thead><tbody>
<tr><th>Architectural shingles</th><td>25–30 years</td></tr><tr><th>3-tab shingles</th><td>18–25 years</td></tr><tr><th>Aluminum gutters</th><td>20–30 years</td></tr><tr><th>Interior paint</th><td>8–12 years</td></tr><tr><th>Carpet</th><td>8–12 years</td></tr><tr><th>Heat pump</th><td>12–18 years</td></tr>
</tbody></table></div>
<h2>Getting the holdback released</h2>
<p>Most replacement cost policies release depreciation after the work is complete, often within a set time. Send invoices and photos of the finished work. The <a href="/calculators-for-policyholders/claim-clock-calendar-builder/">claim calendar builder</a> can remind you before that window closes.</p>
""",
        "faqs": [("Can labor be depreciated in Virginia?", "Practices differ by insurer and policy, and courts in different states have reached different conclusions. Ask the insurer to show in writing whether labor was depreciated and why."), ("What if I decide not to repair?", "Under most replacement cost policies you keep the ACV payment but may not collect the held-back depreciation.")],
    },
    {
        "slug": "roof-pitch-and-squares-checker", "kw": "roof squares calculator", "name": "Roof Pitch & Squares Checker", "icon": "▲", "kind": "Calculator",
        "photo": "roofer-shingles",
        "short": "Turn a footprint into true roof squares with pitch and waste, then check the estimate’s numbers.",
        "title": "Roof Squares Calculator | Pitch & Waste Checker",
        "desc": "Roof squares calculator: turn a footprint, pitch and waste factor into true roof area, then check squares and steep charges in your estimate.",
        "h1": "Roof Pitch & Squares Checker: A Roof Squares Calculator",
        "lede": "Measurement errors quietly shrink roof claims. Use your home’s footprint and pitch to estimate true roof area, squares and bundles, then compare with the insurer’s numbers.",
        "markup": ROOF,
        "explain": """
<h2>The math behind the roof squares calculator</h2>
<p>A sloped roof has more surface than the footprint under it. The pitch multiplier is √(1 + (rise ÷ 12)²). An 8/12 roof is about 20% larger than its footprint, and a 12/12 roof about 41% larger.</p>
<h2>Checking the insurer’s estimate</h2>
<ul><li>Find the roof section and note total squares and the waste percentage.</li>
<li>Compare with the result here. Differences over 5–10% deserve a closer look.</li>
<li>Look for steep charges (often from 7/12) and high-roof charges for two-story sections.</li>
<li>Confirm starter, ridge cap, drip edge and ice-and-water barrier are listed.</li></ul>
<h2>Where a footprint estimate falls short</h2>
<p>Roofs with several pitches, dormers and valleys need to be measured plane by plane. An aerial report or a field measurement will be more accurate, so use this as a sanity check.</p>
""",
        "faqs": [("What is a roofing ‘square’?", "100 square feet of roof surface. Many two-story Virginia homes have between 20 and 40 squares."), ("Why does waste vary with roof shape?", "Hips, valleys and dormers require more cutting, so more material is lost.")],
    },
    {
        "slug": "hurricane-wind-deductible-converter", "kw": "hurricane deductible calculator", "name": "Hurricane & Wind Deductible Converter", "icon": "%", "kind": "Converter",
        "photo": "storm-sky",
        "short": "Turn a percentage hurricane, named-storm or wind deductible into dollars and see what a claim pays.",
        "title": "Hurricane Deductible Calculator | % to Dollars",
        "desc": "Hurricane deductible calculator: convert a percentage named-storm or wind deductible to dollars and compare the payout with a flat deductible.",
        "h1": "Hurricane & Wind Deductible Converter",
        "lede": "A 2% deductible sounds small until you multiply it by your dwelling coverage. See your hurricane or wind deductible in real dollars and how it changes a storm payment.",
        "markup": DEDUCT,
        "explain": """
<h2>Why this hurricane deductible calculator matters in Virginia</h2>
<p>Many policies in Hampton Roads, on the Eastern Shore and along the tidal rivers carry a hurricane or named-storm deductible calculated as a percentage of Coverage A. On a $420,000 dwelling limit, 2% is $8,400, not $1,000. Some inland policies use a percentage wind/hail deductible too.</p>
<h2>Finding yours</h2>
<p>Check the declarations page for “hurricane,” “named storm,” “windstorm” or “wind/hail.” The endorsement defines when it applies. Hurricane deductibles are often triggered by a National Weather Service hurricane watch or warning and last for a set period afterward.</p>
<h2>How it affects appraisal</h2>
<p>The deductible doesn’t change the amount of loss a panel decides, but it changes what you receive. A loss barely above the deductible may not be worth disputing, while one well above it may be.</p>
""",
        "faqs": [("Does the percentage apply to my contents too?", "The percentage is usually figured from Coverage A but applied to the whole storm loss. Check your endorsement’s wording."), ("Can I lower my hurricane deductible?", "Sometimes, at renewal and for a higher premium. Ask your agent which options your insurer offers in your area.")],
    },
    {
        "slug": "claim-clock-calendar-builder", "kw": "insurance claim deadline calculator", "name": "Claim Clock & Calendar Builder", "icon": "◷", "kind": "Planner",
        "photo": "tape-measure",
        "short": "Map notice, proof-of-loss, holdback and suit dates from your date of loss, then export an .ics file.",
        "title": "Insurance Claim Deadline Calculator | Virginia",
        "desc": "Insurance claim deadline calculator for Virginia: map proof-of-loss, holdback and suit dates from your loss date and export a calendar file.",
        "h1": "Claim Clock & Calendar Builder for Virginia Claims",
        "lede": "Policy deadlines keep running while you argue about a number. Enter your date of loss and your policy’s windows to build a timeline you can save to your phone’s calendar.",
        "markup": DATES,
        "explain": """
<h2>The dates this insurance claim deadline calculator tracks</h2>
<ul><li><strong>Prompt notice.</strong> Policies require you to report a loss promptly. Late notice is a common insurer defense.</li>
<li><strong>Proof of loss.</strong> If the insurer requests a sworn proof of loss, many policies give 60 days to return it.</li>
<li><strong>Depreciation recovery.</strong> Replacement cost policies usually require repairs within a set period to collect holdback.</li>
<li><strong>Suit limitation.</strong> Virginia’s standard fire policy provisions commonly allow two years from the date of loss to file suit. Appraisal may not stop that clock.</li></ul>
<div class="note"><b class="h">Important</b>This planner only uses the numbers you enter. It isn’t legal advice, and courts may read policy deadlines differently. If a deadline is close, contact a Virginia attorney.</div>
""",
        "faqs": [("Is the date of loss the day I noticed the damage?", "Usually it’s the date of the storm or event. Weather records for your address can help confirm it."), ("Does demanding appraisal extend my suit deadline?", "Not automatically. Some policies or written agreements address it, but many don’t. Protect the deadline separately.")],
    },
    {
        "slug": "appraisal-readiness-scorecard", "kw": "insurance appraisal checklist", "name": "Appraisal Readiness Scorecard", "icon": "✓", "kind": "Checklist",
        "photo": "consult-table",
        "short": "Answer 12 yes/no questions to score your claim file and get a to-do list before demanding appraisal.",
        "title": "Insurance Appraisal Checklist | Readiness Score",
        "desc": "Insurance appraisal checklist: twelve yes-or-no questions score how ready your claim is and build a to-do list before you demand appraisal.",
        "h1": "Appraisal Readiness Scorecard: An Insurance Appraisal Checklist",
        "lede": "Strong appraisals start with a complete file. Answer twelve quick questions to see where yours stands and what to fix before anyone signs a demand letter.",
        "markup": READY,
        "explain": """
<h2>How the insurance appraisal checklist is weighted</h2>
<p>Coverage, estimates and evidence carry the most weight. They decide whether appraisal is the right tool at all and how well your number will hold up. Paperwork items matter too, but they’re easier to fix.</p>
<h2>What your score means</h2>
<ul><li><strong>75 and up:</strong> your file is in good shape. A professional review of the gap is the logical next step.</li>
<li><strong>45 to 74:</strong> close the open items first. Each one strengthens your position.</li>
<li><strong>Below 45:</strong> demanding appraisal now could lock in a low number. Build the file first.</li></ul>
""",
        "faqs": [("Are my answers saved or sent anywhere?", "No. The scorecard runs in your browser and nothing is stored or transmitted."), ("Can I share the result with an appraiser?", "Yes. Take a screenshot of your score and to-do list and bring it to your consultation.")],
    },
    {
        "slug": "fallen-tree-claim-splitter", "kw": "fallen tree insurance calculator", "name": "Fallen Tree Claim Splitter", "icon": "♣", "kind": "Calculator",
        "photo": "tree-on-house",
        "short": "Split a tree claim into dwelling repair, capped removal and what you pay, using your policy’s limits.",
        "title": "Fallen Tree Insurance Calculator | Removal Limits",
        "desc": "Fallen tree insurance calculator: split a tree claim into dwelling repair, capped debris removal and your share using your policy’s limits.",
        "h1": "Fallen Tree Claim Splitter: A Fallen Tree Insurance Calculator",
        "lede": "Virginia’s hardwood canopy makes tree claims common, and policy limits make them confusing. Enter your trees, costs and limits to see what the policy pays and what you pay.",
        "markup": TREE,
        "explain": """
<h2>How the fallen tree insurance calculator works</h2>
<p>Many homeowners policies treat a tree claim as two different things. Repairing the house, including lifting the tree off it, is part of the dwelling claim. Cutting and hauling the tree away is debris removal, often limited to something like $500 per tree and $1,000 per loss, and only for trees that hit a covered structure or block a driveway or ramp. This tool applies those limits so you can see the split.</p>
<h2>Example (illustrative)</h2>
<p>With the default figures, the crane and structural repair are paid as dwelling repair less the deductible. Two trees qualify for removal coverage, but the $1,000 per-loss cap applies. The two trees that hit nothing aren’t covered for removal at all.</p>
<h2>Check your own policy</h2>
<ul><li>Find the “Trees, shrubs and other plants” and “Debris removal” sections in your policy.</li>
<li>Note the per-tree and per-loss limits and which perils they apply to.</li>
<li>Ask whether crane and lift-off costs were included in the dwelling estimate.</li></ul>
<p>For a disputed tree claim, see our <a href="/appraisal-and-umpire-services/tree-fall-and-ice-storm-appraisal/">fallen tree damage appraisal</a> service.</p>
""",
        "faqs": [("Are the default limits right for my policy?", "They’re common figures, not universal ones. Replace them with the limits in your policy before relying on the result."), ("Does the deductible apply to tree removal too?", "Usually one deductible applies to the whole loss. This tool subtracts it once from the combined covered amount.")],
    },
]
