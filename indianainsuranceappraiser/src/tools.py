"""Interactive claim tools: markup + explanatory copy. Logic lives in static/assets/js/app.js."""

TB = "/claim-gap-tools/"

GAP_FULL = """
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Claim gap &amp; net recovery estimator</span><i>Runs in your browser · nothing stored</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Insurer’s estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="16900"><span class="hint">Replacement cost total on the carrier’s estimate.</span></div>
        <div><label for="g-own">Your estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="29400"><span class="hint">Contractor or independent line-item estimate.</span></div>
      </div>
      <div><label for="g-land">Your best guess: where does the award land inside the gap?</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% means the carrier’s number holds; 100% means your full number is awarded.</span></div>
      <div class="row2">
        <div><label for="g-ft">Appraiser fee structure</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of the increase (%)</option></select></div>
        <div><label for="g-fee">Fee amount</label><input id="g-fee" name="fee" inputmode="decimal" value="2200"></div>
      </div>
      <label class="check"><input type="checkbox" name="useump" checked> Include my half of an umpire’s fee</label>
      <div><label for="g-ump">Umpire’s total fee</label><input id="g-ump" name="umpire" inputmode="decimal" value="2800"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated net increase at your guess</small><b data-o="net">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="seg-a"></span><span class="seg-b"></span><span class="seg-c"></span></div>
      <div class="legend"><span><i class="seg-a"></i>Carrier’s number</span><span><i class="seg-b"></i>Your net gain</span><span><i class="seg-c"></i>Appraisal costs</span></div>
      <div class="out-rows">
        <div><span>Amount in dispute</span><b data-o="gap">$0</b></div>
        <div><span>Gap as a share of the carrier estimate</span><b data-o="pct">—</b></div>
        <div><span>Projected award (RCV)</span><b data-o="award">$0</b></div>
        <div><span>Your appraisal costs</span><b data-o="cost">$0</b></div>
      </div>
      <p class="scen-h">Three scenarios side by side</p>
      <div class="scen"><div><small>Cautious (30%)</small><b data-o="s30">$0</b></div><div><small>Middle (55%)</small><b data-o="s55">$0</b></div><div><small>Strong (80%)</small><b data-o="s80">$0</b></div></div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

GAP_MINI = """
<div class="tool tool-mini" data-tool="gap">
  <div class="tool-head"><span>Two-number gap check</span><i>No sign-up</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="m-ins">Carrier’s estimate</label><input id="m-ins" name="insurer" inputmode="decimal" value="12800"></div>
      <div><label for="m-own">Your contractor’s estimate</label><input id="m-own" name="yours" inputmode="decimal" value="24100"></div>
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
  <div class="tool-head"><span>RCV / ACV holdback calculator</span><i>Add or remove line items</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Laminated shingle roof", 16800, 11, 30), ("Vinyl siding — two elevations", 6400, 14, 35), ("Basement carpet and pad", 2900, 7, 10)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn ghost small" data-add data-run>+ Add a line item</button></div>
      <div class="row2">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="1500"></div>
        <div><label for="d-cap">Depreciation cap</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="90">90%</option></select><span class="hint">Many estimates cap depreciation; check yours.</span></div>
      </div>
      <label class="check"><input type="checkbox" name="nonrec"> My policy pays actual cash value only (no recoverable depreciation)</label>
    </div>
    <div class="tool-out tool-out-3" aria-live="polite">
      <div class="out-big"><small>First check (ACV − deductible)</small><b data-o="first">$0</b></div>
      <div class="out-big"><small>Held back until repairs are done</small><b data-o="held">$0</b></div>
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
  <div class="tool-head"><span>Roof pitch &amp; squares calculator</span><i>Check the carrier’s roof math</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <fieldset class="plain"><legend class="sr-only">Measurement method</legend>
        <div class="btn-row">
          <label class="check"><input type="radio" name="mode" value="dims" checked> Footprint length × width</label>
          <label class="check"><input type="radio" name="mode" value="area"> I know the footprint area</label>
        </div></fieldset>
      <div class="row2" data-mode="dims">
        <div><label for="r-l">Footprint length (ft)</label><input id="r-l" name="len" inputmode="decimal" value="62"></div>
        <div><label for="r-w">Footprint width (ft)</label><input id="r-w" name="wid" inputmode="decimal" value="32"></div>
      </div>
      <div data-mode="dims"><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="12"></div>
      <div data-mode="area" hidden><label for="r-a">Footprint area incl. overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="2200"></div>
      <div class="row2">
        <div><label for="r-p">Roof pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 7 else "", p) for p in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16]) + """</select></div>
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="10">10% — plain gable</option><option value="12" selected>12% — gable with dormers</option><option value="15">15% — hip roof</option><option value="18">18% — cut-up or complex</option></select></div>
      </div>
      <div class="row2">
        <div><label for="r-c">Squares on the carrier’s estimate (optional)</label><input id="r-c" name="carrier" inputmode="decimal" placeholder="e.g. 22.5"></div>
        <div><label for="r-pr">Installed price per square (optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 540"></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Roof squares before waste</small><b data-o="sq">0</b></div>
      <div class="out-rows">
        <div><span>Pitch multiplier</span><b data-o="mult">1.000</b></div>
        <div><span>Roof surface area</span><b data-o="surface">0</b></div>
        <div><span>Squares with waste</span><b data-o="order">0</b></div>
        <div><span>Shingle bundles (3 per square)</span><b data-o="bundles">0</b></div>
        <div><span>Difference vs. carrier squares</span><b data-o="vs">—</b></div>
        <div><span>Rough replacement cost</span><b data-o="cost">—</b></div>
      </div>
      <p class="out-msg" data-o="steep"></p>
    </div>
  </div>
</div>"""

DEDUCT = """
<div class="tool" data-tool="deduct">
  <div class="tool-head"><span>Percentage deductible calculator</span><i>Percent vs. flat, in dollars</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling coverage (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="310000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Wind/hail percentage deductible</label><select id="w-p" name="pct"><option value="0.5">0.5%</option><option value="1" selected>1%</option><option value="2">2%</option><option value="3">3%</option><option value="5">5%</option></select></div>
        <div><label for="w-f">All-other-perils flat deductible</label><input id="w-f" name="flat" inputmode="decimal" value="1000"></div>
      </div>
      <div><label for="w-l">Estimated storm damage</label><input id="w-l" name="loss" inputmode="decimal" value="18700"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your percentage deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="seg-c"></span><span class="seg-a"></span></div>
      <div class="legend"><span><i class="seg-c"></i>You pay</span><span><i class="seg-a"></i>Policy pays</span></div>
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
  <div class="tool-head"><span>Indiana claim timeline builder</span><i>Exports an .ics calendar file</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
      <p class="hint flush">Change each window to match your own policy. Defaults are common figures, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report the claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="2"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="10"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Often counted from the carrier’s request.</span></div>
        <div><label for="t-r">Depreciation recovery (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="180"></div>
        <div><label for="t-s">Suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="730"><span class="hint">Two years is 730 days.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download .ics calendar file</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the insurer accepted coverage for at least part of the loss?", "Get the carrier’s coverage position in writing. If the claim was denied outright, talk to an Indiana attorney before considering appraisal."),
    (3, "Do you have the carrier’s complete line-item estimate?", "Ask in writing for the full itemized estimate, not just the summary page."),
    (3, "Do you have your own itemized estimate?", "Get a line-item estimate from a contractor or estimator. A one-line bid won’t carry weight with a panel."),
    (2, "Do you have dated photos taken soon after the loss?", "Collect every photo and note its date. Add new photos of current conditions."),
    (2, "Have you found and read the appraisal clause in your policy?", "Locate the ‘Appraisal’ paragraph in the policy conditions and note any deadlines it sets."),
    (2, "Do you know your policy’s suit-limitation date?", "Find the ‘Suit Against Us’ condition and put the date on your calendar with our timeline builder."),
    (2, "Have temporary repairs been made, with receipts saved?", "Make reasonable temporary repairs, such as tarps or water extraction, and keep every receipt."),
    (1, "Do you have a current declarations page?", "Download or request your declarations page from your agent or carrier."),
    (2, "Has hidden damage been opened up and documented?", "Make sure attics, wet walls and roof decking have been checked so the scope is complete."),
    (1, "Is your claim correspondence organized by date?", "Gather emails, letters and claim notes in date order."),
    (2, "Is the gap between estimates more than about 10% or $5,000?", "Run the numbers in our claim gap estimator. A small gap may not justify appraisal costs."),
    (1, "If the carrier requested a sworn proof of loss, has it been submitted?", "If a proof of loss was requested, return it on time."),
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
    <div class="tool-out tool-out-gauge" aria-live="polite">
      <div>
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path class="gauge-track" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke-width="18"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3"/></svg>
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

SNOW = """
<div class="tool" data-tool="snow">
  <div class="tool-head"><span>Roof snow load estimator</span><i>Rough weight of snow and ice</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="s-a">Roof area (sq ft)</label><input id="s-a" name="area" inputmode="decimal" value="2100"><span class="hint">Use the roof squares calculator if you only know the footprint (1 square = 100 sq ft).</span></div>
      <div class="row2">
        <div><label for="s-d">Snow depth on the roof (inches)</label><input id="s-d" name="depth" inputmode="decimal" value="18"></div>
        <div><label for="s-t">Snow type</label><select id="s-t" name="density"><option value="7">Fresh, light powder (~7 lb/ft³)</option><option value="15" selected>Settled snow (~15 lb/ft³)</option><option value="25">Wet or packed snow (~25 lb/ft³)</option></select></div>
      </div>
      <div class="row2">
        <div><label for="s-i">Ice layer (inches)</label><input id="s-i" name="ice" inputmode="decimal" value="1"><span class="hint">Ice weighs roughly 57 lb/ft³.</span></div>
        <div><label for="s-r">Reference design load (lb/sq ft)</label><input id="s-r" name="ref" inputmode="decimal" value="20"><span class="hint">Illustrative. Ask an engineer for your building’s actual value.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated load on the roof</small><b data-o="psf">0 lb/sq ft</b></div>
      <div class="meter" aria-hidden="true"><span data-o="meter"></span></div>
      <div class="out-rows">
        <div><span>From snow</span><b data-o="snowpsf">0</b></div>
        <div><span>From ice</span><b data-o="icepsf">0</b></div>
        <div><span>Total weight on the roof</span><b data-o="lbs">0</b></div>
        <div><span>Share of the reference load</span><b data-o="ratio">—</b></div>
      </div>
      <p class="out-msg" data-o="smsg"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "claim-gap-net-recovery-estimator", "name": "Claim Gap & Net Recovery Estimator", "icon": "Δ", "kind": "Estimator",
        "short": "Size the dispute, project an award and subtract appraiser and umpire fees, with three scenarios side by side.",
        "title": "Claim Gap & Net Recovery Estimator | Free Tool",
        "desc": "Claim gap estimator: compare your estimate with the insurer’s, project an appraisal award and see your net after appraiser and umpire fees.",
        "h1": "Claim Gap and Net Recovery Estimator",
        "lede": "Enter the carrier’s number and yours, guess where an award might land and add realistic fees. Three scenarios show whether appraisal is likely to leave you ahead.",
        "markup": GAP_FULL,
        "explain": f"""
<h2>Using the estimator</h2>
<ol><li><strong>Enter the insurer’s RCV total</strong>, the replacement cost figure before depreciation and the deductible.</li>
<li><strong>Enter your own RCV estimate</strong> from a contractor or independent estimator.</li>
<li><strong>Set your best guess</strong> on the slider, then compare it with the cautious, middle and strong scenarios.</li>
<li><strong>Add fees</strong> using your appraiser’s quoted arrangement and a realistic umpire figure.</li></ol>
<h2>Read the cautious scenario first</h2>
<p>Panels rarely award either side’s opening number in full. Well-supported line items tend to survive and unsupported ones tend to fall away. If your net only looks good in the strong scenario, the file may need more documentation before you demand appraisal. If the cautious scenario still leaves you ahead, appraisal is more likely to be worthwhile.</p>
<h2>What this tool doesn’t include</h2>
<p>Depreciation timing, deductibles and policy limits change what you are paid, not the size of the dispute. For the payment split, use the <a href="{TB}rcv-acv-holdback-calculator/">RCV/ACV holdback calculator</a>. All figures are illustrative.</p>
""",
        "faqs": [("Is the projected award a prediction?", "No. It is a planning scenario based on numbers you choose. Actual awards depend on documentation, the panel and your policy."), ("What do umpires typically charge?", "Umpire fees vary with the size and complexity of the dispute. Ask for a quote when an umpire is proposed; most policies split the cost evenly.")],
    },
    {
        "slug": "rcv-acv-holdback-calculator", "name": "RCV/ACV Holdback Calculator", "icon": "ACV", "kind": "Calculator",
        "short": "Line-item depreciation that shows your first ACV check, the holdback and the total once repairs are done.",
        "title": "RCV vs ACV Holdback Calculator | Depreciation",
        "desc": "RCV vs ACV holdback calculator: list items with ages and lifespans to estimate your first check, recoverable depreciation and final total.",
        "h1": "RCV vs. ACV Depreciation and Holdback Calculator",
        "lede": "Replacement cost policies usually pay twice: an actual cash value check now and recoverable depreciation once repairs are finished. List your items to see the split.",
        "markup": DEP,
        "explain": f"""
<h2>How depreciation is figured here</h2>
<p>The calculator uses straight-line depreciation, age divided by expected life, capped at the percentage you pick. Real estimates may adjust for condition, use different lifespans or treat some items as non-depreciable, so treat the result as a planning figure.</p>
<h2>Lifespans often used in estimates</h2>
<div class="table-wrap"><table><thead><tr><th>Item</th><th>Common range</th></tr></thead><tbody>
<tr><th>Three-tab shingles</th><td>20–25 years</td></tr><tr><th>Laminated (architectural) shingles</th><td>25–30 years</td></tr><tr><th>Vinyl siding</th><td>30–40 years</td></tr><tr><th>Interior paint</th><td>8–12 years</td></tr><tr><th>Carpet and pad</th><td>8–12 years</td></tr><tr><th>Water heater</th><td>10–15 years</td></tr>
</tbody></table></div>
<h2>Getting the holdback released</h2>
<p>Most policies pay recoverable depreciation after repairs are completed within a set period. Send invoices and photos of the finished work, and use the <a href="{TB}claim-timeline-builder/">claim timeline builder</a> so the window doesn’t close on you.</p>
""",
        "faqs": [("Can labor be depreciated in Indiana?", "Practices differ by policy and carrier, and the question has been litigated in several states. Ask your carrier to explain in writing how labor was treated, and talk to an attorney if it matters to your claim."), ("What happens if I don’t repair?", "Under most replacement cost policies you keep the ACV payment but may not recover the depreciation that was held back.")],
    },
    {
        "slug": "roof-pitch-squares-calculator", "name": "Roof Pitch & Squares Calculator", "icon": "▲", "kind": "Calculator",
        "short": "Turn a footprint into true roof squares by pitch and waste, then compare with the carrier’s figure.",
        "title": "Roof Pitch & Squares Calculator for Claims",
        "desc": "Roof pitch and squares calculator: turn footprint, pitch and waste into roof squares and compare the result with your insurance estimate.",
        "h1": "Roof Pitch and Squares Calculator",
        "lede": "Short measurements quietly shrink roof claims. Use your home’s footprint and pitch to estimate true roof area, then compare it with the squares on the carrier’s estimate.",
        "markup": ROOF,
        "explain": """
<h2>The math behind it</h2>
<p>A pitched roof has more surface than the footprint beneath it. The pitch multiplier is √(1 + (rise ÷ 12)²): a 6/12 roof is about 11.8% larger than its footprint, a 9/12 roof about 25% larger and a 12/12 roof about 41.4% larger.</p>
<h2>Checking the carrier’s estimate</h2>
<ul><li>Find total squares and the waste percentage in the roofing section of the estimate.</li>
<li>Enter the carrier’s squares above to see the difference in squares and percent.</li>
<li>Look for steep charges, which estimating software commonly adds starting around 7/12, and high-roof charges on two-story sections.</li>
<li>Check that starter, ridge cap, drip edge, valley metal and ice and water shield are listed.</li></ul>
<h2>Where footprint math falls short</h2>
<p>Roofs with several pitches, dormers and valleys should be measured plane by plane. An aerial measurement report or field measurement always beats a footprint estimate, so use this as a sanity check.</p>
""",
        "faqs": [("What is a roofing square?", "One hundred square feet of roof surface. A typical Indiana two-story home might have roughly 20 to 35 squares."), ("Why does waste depend on roof shape?", "Hips, valleys and dormers require more cutting, so more shingles end up as scrap.")],
    },
    {
        "slug": "percentage-deductible-calculator", "name": "Percentage Deductible Calculator", "icon": "%", "kind": "Calculator",
        "short": "See a percentage wind/hail deductible in dollars and how much a storm claim would actually pay.",
        "title": "Percentage Deductible Calculator | Wind & Hail",
        "desc": "Percentage deductible calculator: convert a wind or hail deductible into dollars and compare what a storm claim pays against a flat deductible.",
        "h1": "Percentage Deductible Calculator for Wind and Hail Claims",
        "lede": "A 1% or 2% deductible sounds small until it is multiplied by your dwelling limit. See your deductible in real dollars and how it changes a storm payout.",
        "markup": DEDUCT,
        "explain": """
<h2>Why percentage deductibles catch people off guard</h2>
<p>Some Indiana homeowners policies use a separate wind or hail deductible calculated as a percentage of Coverage A, the dwelling limit. On a $310,000 limit, a 2% deductible is $6,200, not the $1,000 many people assume.</p>
<h2>Where to find yours</h2>
<p>Check the declarations page for a “wind/hail” or “windstorm or hail” deductible. An endorsement later in the policy explains when it applies.</p>
<h2>What it means for appraisal</h2>
<p>The deductible doesn’t change the amount of loss a panel decides, but it changes what you receive. A loss just above the deductible may not be worth disputing; one well above it may be. Figures shown are illustrative.</p>
""",
        "faqs": [("Is the percentage based on my contents limit too?", "Usually it is calculated from Coverage A but applied to the whole wind or hail loss. Read your policy’s wording."), ("Can I switch to a flat deductible?", "Often at renewal, depending on your carrier. A lower deductible usually means a higher premium.")],
    },
    {
        "slug": "claim-timeline-builder", "name": "Claim Timeline Builder", "icon": "◷", "kind": "Planner",
        "short": "Build a dated timeline of notice, proof of loss, holdback and suit dates and download it as a calendar file.",
        "title": "Indiana Claim Timeline Builder | .ics Export",
        "desc": "Build an Indiana property claim timeline from your date of loss, with proof of loss, holdback and suit dates you can export as an .ics file.",
        "h1": "Indiana Property Claim Timeline Builder",
        "lede": "Policy deadlines keep running while you argue about the number. Enter your date of loss and your policy’s windows, then download the dates to your calendar.",
        "markup": DATES,
        "explain": """
<h2>The dates that matter</h2>
<ul><li><strong>Prompt notice.</strong> Policies require losses to be reported promptly. Late notice is a common defense.</li>
<li><strong>Proof of loss.</strong> If the carrier requests a sworn proof of loss, many policies allow 60 days to return it.</li>
<li><strong>Depreciation recovery.</strong> Replacement cost policies often require repairs within a set period to collect the holdback.</li>
<li><strong>Suit limitation.</strong> Many Indiana property policies require any lawsuit within two years of the loss, and Indiana courts have generally enforced reasonable contractual limits. Appraisal may not pause that clock.</li></ul>
<div class="note"><b class="h">Important</b>This tool only uses the numbers you enter. It isn’t legal advice, and courts can read policy deadlines differently. If a deadline is near, contact an Indiana attorney promptly.</div>
""",
        "faqs": [("Is the date of loss the day I noticed the damage?", "Usually it is the day the storm or event occurred. Public weather reports for your area can help pin it down."), ("Does demanding appraisal extend the suit deadline?", "Not automatically. Some policies or written agreements address it, but many don’t. Protect the deadline separately.")],
    },
    {
        "slug": "appraisal-readiness-checkup", "name": "Appraisal Readiness Checkup", "icon": "✓", "kind": "Checklist",
        "short": "Twelve yes/no questions that score your claim file and build a to-do list before you demand appraisal.",
        "title": "Appraisal Readiness Checkup | Is Your File Ready?",
        "desc": "Appraisal readiness checkup: twelve questions that score your property claim file and build a to-do list before you invoke appraisal.",
        "h1": "Appraisal Readiness Checkup",
        "lede": "Strong appraisals are built before the demand letter goes out. Answer twelve quick questions to see where your file stands and what to fix first.",
        "markup": READY,
        "explain": """
<h2>How answers are weighted</h2>
<p>Coverage, estimates and evidence carry the most weight because they decide whether appraisal is the right tool and how well your number will hold up. Paperwork items still matter, but they are easier to fix.</p>
<h2>Reading your score</h2>
<ul><li><strong>75 or higher:</strong> the file is in good shape. A professional review of the gap is the sensible next step.</li>
<li><strong>45 to 74:</strong> close the open items first. Each one strengthens your position.</li>
<li><strong>Below 45:</strong> demanding appraisal now could lock in a low number. Build the file first.</li></ul>
""",
        "faqs": [("Are my answers saved anywhere?", "No. The checkup runs entirely in your browser and nothing is stored or sent."), ("Can I share the result with an appraiser?", "Yes. Take a screenshot of your score and to-do list and bring it to your consultation.")],
    },
    {
        "slug": "roof-snow-load-estimator", "name": "Roof Snow Load Estimator", "icon": "❄", "kind": "Estimator",
        "short": "Estimate the weight of snow and ice on your roof, a real concern in Indiana’s lake-effect counties.",
        "title": "Roof Snow Load Estimator | Indiana Winter Claims",
        "desc": "Roof snow load estimator for Indiana winters: estimate pounds per square foot of snow and ice on your roof and the total weight it carries.",
        "h1": "Roof Snow Load Estimator for Indiana Winters",
        "lede": "Lake-effect snow in northern Indiana and ice storms in the south put real weight on roofs. Estimate how much your roof is carrying in pounds per square foot.",
        "markup": SNOW,
        "explain": """
<h2>How the estimate works</h2>
<p>Snow weight depends on density. Fresh powder is light, settled snow is heavier, and wet or packed snow is heavier still. The tool multiplies depth by a typical density for each type, adds any ice layer at about 57 pounds per cubic foot and spreads the result over your roof area.</p>
<h2>Why Indiana roofs see real loads</h2>
<p>Lake Michigan’s snow belt reaches LaPorte, Porter, St. Joseph and Elkhart counties, where drifting against walls and on lower roofs can pile snow far deeper than on the ground. In southern Indiana, freezing rain can coat roofs and trees with ice. Low-slope additions, porch roofs, carports and pole barns are especially vulnerable.</p>
<h2>Use it as a warning light, not a verdict</h2>
<p>The reference design load in the tool is illustrative. Homes are designed for different snow loads depending on location, code edition and construction, and drifts concentrate weight unevenly. If you see sagging, new cracks, doors that stick or creaking sounds, get people out and call a professional. Figures are estimates only.</p>
<div class="note"><b class="h">If damage happens</b>Collapse and snow-load damage are covered differently from other perils in many policies. See our <a href="/indiana-claim-appraisal/ice-dam-freeze-snow-load-appraisal/">ice dam, freeze and snow-load appraisal</a> page.</div>
""",
        "faqs": [("Should I climb up and shovel my roof?", "Climbing onto a snow-covered roof is dangerous. Roof rakes used from the ground or professional snow removal are safer options."), ("Is roof collapse from snow covered?", "Many homeowners policies cover collapse caused by the weight of ice, snow or sleet, often under specific conditions. Read the collapse section of your policy.")],
    },
]
