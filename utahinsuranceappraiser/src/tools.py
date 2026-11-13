"""Interactive claim tools: markup + explanatory copy. Logic lives in static/assets/js/app.js."""

GAP_FULL = """
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Claim gap &amp; fee estimator</span><i>Runs in your browser</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Insurer’s estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="22600"><span class="hint">Replacement cost total on the carrier’s estimate.</span></div>
        <div><label for="g-own">Your estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="38900"><span class="hint">Your contractor’s or independent estimate.</span></div>
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
      <div class="stack" aria-hidden="true"><span style="background:#c9d3e6"></span><span style="background:#e0703a"></span><span style="background:#071d49"></span></div>
      <div class="legend"><span><i style="background:#c9d3e6"></i>Carrier’s number</span><span><i style="background:#e0703a"></i>Your net gain</span><span><i style="background:#071d49"></i>Appraisal costs</span></div>
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
  <div class="tool-head"><span>Quick gap check</span><i>Nothing is stored</i></div>
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
  <div class="tool-head"><span>RCV to ACV holdback calculator</span><i>Add as many items as you need</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Laminated shingle roof", 21400, 11, 30), ("Basement carpet & pad", 3100, 5, 10), ("Drywall paint — main floor", 2650, 3, 10)]) + """
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
  <div class="tool-head"><span>Roof pitch &amp; squares estimator</span><i>Compare against your estimate</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <fieldset style="border:0;padding:0;margin:0"><legend class="sr-only">Measurement method</legend>
        <div class="btn-row">
          <label class="check"><input type="radio" name="mode" value="dims" checked> Footprint length × width</label>
          <label class="check"><input type="radio" name="mode" value="area"> I know the footprint area</label>
        </div></fieldset>
      <div class="row2" data-mode="dims">
        <div><label for="r-l">Footprint length (ft)</label><input id="r-l" name="len" inputmode="decimal" value="62"></div>
        <div><label for="r-w">Footprint width (ft)</label><input id="r-w" name="wid" inputmode="decimal" value="38"></div>
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
  <div class="tool-head"><span>Percentage deductible calculator</span><i>Earthquake, wind or hail</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling coverage (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="520000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Percentage deductible</label><select id="w-p" name="pct"><option value="1">1%</option><option value="2">2%</option><option value="5">5%</option><option value="10" selected>10%</option><option value="15">15%</option><option value="20">20%</option><option value="25">25%</option></select></div>
        <div><label for="w-f">All-other-perils flat deductible</label><input id="w-f" name="flat" inputmode="decimal" value="1000"></div>
      </div>
      <div><label for="w-l">Estimated storm damage</label><input id="w-l" name="loss" inputmode="decimal" value="46000"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your percentage deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span style="background:#071d49"></span><span style="background:#c9d3e6"></span></div>
      <div class="legend"><span><i style="background:#071d49"></i>You pay</span><span><i style="background:#c9d3e6"></i>Policy pays</span></div>
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
  <div class="tool-head"><span>Utah claim timeline planner</span><i>Exports to your calendar</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
      <p class="hint" style="margin:0">Adjust each window to match your policy. Defaults are common figures, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="3"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="14"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Often 60 days from the carrier’s request.</span></div>
        <div><label for="t-r">Depreciation recovery (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="365"></div>
        <div><label for="t-s">Suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="1095"><span class="hint">Utah’s statute generally allows three years (1,095 days); check your policy.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download .ics calendar file</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the insurer accepted coverage for at least part of the loss?", "Get written confirmation that coverage is accepted. If the claim was denied, talk to a Utah attorney before considering appraisal."),
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
  <div class="tool-head"><span>Appraisal readiness checkup</span><i>12 questions · about two minutes</i></div>
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
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#e9eef8" stroke-width="18"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#e0703a" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3" style="transition:stroke-dashoffset .5s,stroke .3s"/></svg>
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


SNOW = """
<div class="tool" data-tool="snow">
  <div class="tool-head"><span>Roof snow load estimator</span><i>Illustrative, not engineering</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="s-a">Roof area, measured flat (sq ft)</label><input id="s-a" name="area" inputmode="decimal" value="2400"><span class="hint">The footprint the roof covers, including overhangs.</span></div>
      <div class="row2">
        <div><label for="s-d">Snow depth on the roof (inches)</label><input id="s-d" name="depth" inputmode="decimal" value="30"></div>
        <div><label for="s-t">Type of snow</label><select id="s-t" name="dens"><option value="6">Fresh, light powder</option><option value="15" selected>Settled snow</option><option value="22">Wet or wind-packed</option><option value="30">Old, dense spring snow</option></select></div>
      </div>
      <div><label for="s-i">Ice layer beneath the snow (inches)</label><input id="s-i" name="ice" inputmode="decimal" value="2"><span class="hint">Ice weighs roughly 57 lb per cubic foot.</span></div>
      <div><label for="s-l">Roof design snow load (psf, optional)</label><input id="s-l" name="design" inputmode="decimal" value="40"><span class="hint">Your building department or an engineer can tell you the design load for your address. It rises sharply with elevation in Utah.</span></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated load on the roof</small><b data-o="psf">0 psf</b></div>
      <div class="meter" aria-hidden="true"><span data-o="bar"></span></div>
      <div class="out-rows">
        <div><span>Snow weight per sq ft</span><b data-o="snowpsf">0</b></div>
        <div><span>Ice weight per sq ft</span><b data-o="icepsf">0</b></div>
        <div><span>Total weight on the roof</span><b data-o="lbs">0</b></div>
        <div><span>Share of design load</span><b data-o="share">—</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "claim-gap-fee-estimator", "name": "Claim Gap & Fee Estimator", "icon": "Δ", "kind": "Estimator",
        "short": "Size the dispute, test where an award could land and subtract appraiser and umpire fees to see your net.",
        "title": "Claim Gap & Appraisal Fee Estimator | Utah Claims",
        "desc": "Compare your estimate with the insurer’s, test where an appraisal award could land and subtract appraiser and umpire fees to see a realistic net.",
        "h1": "Claim Gap and Appraisal Fee Estimator",
        "lede": "Enter the insurer’s number and yours, slide to test outcomes and add realistic fees. You’ll see whether appraisal is likely to leave you better off, and by how much.",
        "markup": GAP_FULL,
        "explain": """
<h2>Reading the result</h2>
<p>The big number is the estimated net increase after your appraisal costs. The bar shows how the projected award splits between the insurer’s original number, your net gain and what you’d spend on the process.</p>
<h2>Test a range, not a point</h2>
<p>Panels rarely land exactly on either side’s number. Try the slider at 30%, 50% and 75%. If appraisal only pays off at the high end, your case depends on everything going right. If it still pays at 40%, you have room for error.</p>
<h2>An illustrative example</h2>
<p>With the default figures, the insurer’s estimate is $22,600 and the contractor’s is $38,900, a $16,300 gap. At a 60% outcome and a flat $2,500 fee plus half of a $3,000 umpire fee, the estimated net increase is about $5,780. These numbers are illustrative only.</p>
<h2>What this doesn’t include</h2>
<p>Deductibles, depreciation timing and policy limits affect what you’re paid, not the size of the dispute. Use the <a href="/utah-claim-calculators/rcv-acv-holdback-calculator/">holdback calculator</a> and <a href="/utah-claim-calculators/percentage-deductible-calculator/">deductible calculator</a> for those.</p>
""",
        "faqs": [("Is the projected award a prediction?", "No. It’s a scenario you control with the slider. Real awards depend on evidence, the panel and the policy."), ("Should I choose a flat or percentage fee?", "It depends on the claim. Flat and hourly fees are predictable; percentage fees scale with the result. Compare both in the estimator and get any arrangement in writing.")],
    },
    {
        "slug": "rcv-acv-holdback-calculator", "name": "RCV to ACV Holdback Calculator", "icon": "ACV", "kind": "Calculator",
        "short": "List damaged items by age and life expectancy to see the first check, the depreciation held back and the total.",
        "title": "RCV to ACV Holdback Calculator | Recoverable Depreciation",
        "desc": "List damaged items with age and expected life to estimate actual cash value, recoverable depreciation held back and your total once repairs are done.",
        "h1": "RCV to ACV Holdback Calculator",
        "lede": "Replacement cost policies usually pay in two installments: actual cash value first, then the depreciation held back once repairs are finished. Add your items to see how the money splits.",
        "markup": DEP,
        "explain": """
<h2>The method</h2>
<p>Each item is depreciated in a straight line, age divided by expected life, up to the cap you choose. Real estimates may use condition ratings, different lifespans or treat some items as non-depreciable, so use the result for planning.</p>
<h2>Life expectancies you’ll often see</h2>
<div class="table-wrap"><table><thead><tr><th>Item</th><th>Typical range</th></tr></thead><tbody>
<tr><th>Laminated (architectural) shingles</th><td>25–30 years</td></tr><tr><th>Standing-seam metal roofing</th><td>40–60 years</td></tr><tr><th>Concrete tile roofing</th><td>40–50 years</td></tr><tr><th>Carpet and pad</th><td>8–12 years</td></tr><tr><th>Interior paint</th><td>8–12 years</td></tr><tr><th>Furnace</th><td>15–20 years</td></tr>
</tbody></table></div>
<h2>Collecting the holdback</h2>
<p>Policies typically release recoverable depreciation after repairs are complete, within a time limit. Send final invoices and photos. The <a href="/utah-claim-calculators/claim-timeline-planner/">claim timeline planner</a> can remind you before that window closes.</p>
""",
        "faqs": [("Can labor be depreciated?", "Practices differ by policy and jurisdiction. Ask your insurer to explain in writing how labor was treated in your estimate."), ("What if I decide not to repair?", "Under many replacement cost policies, you keep the ACV payment but may not recover the depreciation that was held back.")],
    },
    {
        "slug": "roof-pitch-squares-estimator", "name": "Roof Pitch & Squares Estimator", "icon": "▲", "kind": "Estimator",
        "short": "Turn a footprint into real roof squares with pitch and waste, then compare against the carrier’s roof section.",
        "title": "Roof Pitch & Squares Estimator for Insurance Claims",
        "desc": "Estimate roof squares from a footprint, pitch and waste factor, then compare surface area, bundles and steep charges against your insurance estimate.",
        "h1": "Roof Pitch and Squares Estimator",
        "lede": "Roof claims are often underpaid because of measurement. Enter the footprint and pitch to estimate true surface area, squares and bundles, then check them against your estimate.",
        "markup": ROOF,
        "explain": """
<h2>The math behind it</h2>
<p>Roof surface area equals footprint times a pitch multiplier of √(1 + (rise ÷ 12)²). At 4/12 the roof is about 5.4% larger than its footprint; at 8/12, about 20.2%; at 12/12, about 41.4%.</p>
<h2>Checking the carrier’s roof section</h2>
<ul><li>Compare total squares and the waste percentage.</li>
<li>Differences above 5–10% deserve a closer look.</li>
<li>Look for steep charges on 7/12 and steeper roofs and high-roof charges on two-story sections.</li>
<li>Confirm ridge cap, starter, drip edge and ice-and-water shield are listed. Ice barrier along eaves is common on Utah roofs.</li></ul>
<h2>Limitations</h2>
<p>Roofs with several pitches, dormers and valleys should be measured plane by plane. A field measurement or aerial report is always more accurate than a footprint estimate.</p>
""",
        "faqs": [("What’s a roofing square?", "100 square feet of roof surface. Many Wasatch Front homes have roughly 25 to 45 squares."), ("Why does waste vary?", "Hips, valleys and dormers require more cutting, so more material is wasted.")],
    },
    {
        "slug": "percentage-deductible-calculator", "name": "Percentage Deductible Calculator", "icon": "%", "kind": "Calculator",
        "short": "Convert an earthquake, wind or hail percentage deductible into dollars and see what a claim would actually pay.",
        "title": "Percentage Deductible Calculator | Earthquake, Wind & Hail",
        "desc": "Turn an earthquake, wind or hail percentage deductible into dollars and compare what your Utah policy would pay against a standard flat deductible.",
        "h1": "Percentage Deductible Calculator for Earthquake, Wind and Hail",
        "lede": "A 10% earthquake deductible on a $520,000 home is $52,000. Percentage deductibles change the math on every claim. See yours in dollars and how it affects what a loss pays.",
        "markup": DEDUCT,
        "explain": """
<h2>Where percentage deductibles show up in Utah</h2>
<p>Earthquake endorsements almost always use a percentage deductible, often 10% to 20% of the dwelling limit. Some Utah policies also use a percentage deductible for wind or hail. Your declarations page lists each deductible and how it’s calculated.</p>
<h2>How it affects a dispute</h2>
<p>The deductible doesn’t change the amount of loss an appraisal panel decides. It changes what you receive. If the loss sits near the deductible, a disputed amount may not be worth the cost of appraisal. If the loss is well above it, every additional dollar of the award reaches you.</p>
<h2>An illustrative example</h2>
<p>With the default figures, a 10% deductible on a $520,000 dwelling limit is $52,000. A $46,000 loss falls entirely within it, so no payment would be owed under that deductible, while the same loss under a $1,000 flat deductible would pay $45,000.</p>
""",
        "faqs": [("Does the percentage apply to contents?", "The percentage is usually calculated from the dwelling limit and applied to the whole loss under that peril. Wording varies, so check your endorsement."), ("Can I lower my earthquake deductible?", "Options depend on the carrier. Lower deductibles generally cost more. Ask your agent at renewal.")],
    },
    {
        "slug": "claim-timeline-planner", "name": "Claim Timeline Planner", "icon": "◷", "kind": "Planner",
        "short": "Map notice, mitigation, proof-of-loss, holdback and suit dates from your date of loss, then export them to a calendar.",
        "title": "Utah Claim Timeline Planner | Deadlines & .ics Export",
        "desc": "Enter your date of loss to map notice, proof-of-loss, holdback and three-year suit dates for a Utah property claim, then export them to a calendar.",
        "h1": "Utah Insurance Claim Timeline Planner",
        "lede": "Policy deadlines keep running while you dispute a number. Enter your date of loss and your policy’s windows to build a timeline, then download it as a calendar file.",
        "markup": DATES,
        "explain": """
<h2>Dates worth tracking</h2>
<ul><li><strong>Notice.</strong> Policies require prompt notice of a loss. Report as soon as you reasonably can.</li>
<li><strong>Mitigation.</strong> Reasonable temporary repairs protect the property and the claim.</li>
<li><strong>Proof of loss.</strong> If the insurer requests a sworn proof of loss, many policies set a deadline, often 60 days from the request.</li>
<li><strong>Depreciation recovery.</strong> Replacement cost policies typically require repairs within a set period to collect holdback.</li>
<li><strong>Suit limitation.</strong> Utah law generally allows three years from the inception of the loss to sue on a first-party property policy. Appraisal doesn’t automatically pause that clock.</li></ul>
<div class="note"><b class="h">Important</b>The planner uses the numbers you enter and isn’t legal advice. Courts can interpret deadlines differently. If a date is close, talk to a Utah attorney.</div>
""",
        "faqs": [("What date should I use as the date of loss?", "Usually the date of the storm or event, not the day you noticed the damage. Weather records for your address can help."), ("Will the .ics file work with my calendar?", "Yes. It’s a standard calendar file that Google Calendar, Outlook and Apple Calendar can import.")],
    },
    {
        "slug": "appraisal-readiness-checkup", "name": "Appraisal Readiness Checkup", "icon": "✓", "kind": "Checklist",
        "short": "Twelve yes/no questions that score your claim file and build a to-do list before you demand appraisal.",
        "title": "Appraisal Readiness Checkup | Is Your Claim File Ready?",
        "desc": "Answer twelve yes-or-no questions to score how ready your Utah property claim is for appraisal and get a personal list of what to finish first.",
        "h1": "Appraisal Readiness Checkup",
        "lede": "Appraisals are often won or lost on the file you bring. Answer twelve quick questions to see where yours stands and what to finish before demanding appraisal.",
        "markup": READY,
        "explain": """
<h2>How the checkup is weighted</h2>
<p>Coverage, itemized estimates and evidence carry the most weight. They decide whether appraisal is the right tool and how well your number will hold up. Organizational items matter but are easier to fix.</p>
<h2>Using your score</h2>
<ul><li><strong>75 or higher:</strong> a well-built file. A professional review of the gap is a logical next step.</li>
<li><strong>45 to 74:</strong> close the open items before you demand appraisal.</li>
<li><strong>Under 45:</strong> demanding appraisal now could lock in a low number. Build the file first.</li></ul>
""",
        "faqs": [("Is anything I enter saved?", "No. The checkup runs entirely in your browser and nothing is stored or sent."), ("Can I share the result?", "Yes. Take a screenshot of your score and to-do list and bring it to your consultation.")],
    },
    {
        "slug": "roof-snow-load-estimator", "name": "Roof Snow Load Estimator", "icon": "❄", "kind": "Estimator",
        "short": "Convert snow depth, snow type and ice into pounds per square foot and total roof weight for a winter claim.",
        "title": "Roof Snow Load Estimator | Utah Winter Claims",
        "desc": "Estimate the weight of snow and ice on a roof in pounds per square foot and total pounds, and compare it with a design load for a Utah winter claim.",
        "h1": "Roof Snow Load Estimator for Utah Winter Claims",
        "lede": "When a carport collapses or a ridge sags after a big storm, it helps to show what the roof was carrying. Enter snow depth, snow type and any ice to estimate the load.",
        "markup": SNOW,
        "explain": """
<h2>How the estimate works</h2>
<p>Snow weight depends on density. Fresh powder can weigh around 6 pounds per cubic foot, settled snow about 15, wet or wind-packed snow 20 or more, and ice about 57. The estimator converts depth and density into pounds per square foot, adds any ice layer and multiplies by the roof area.</p>
<h2>An illustrative example</h2>
<p>Thirty inches of settled snow at 15 lb/ft³ weighs about 37.5 psf. Add two inches of ice at roughly 9.5 psf, and the roof carries about 47 psf, roughly 113,000 pounds on a 2,400 sq ft roof. That’s above a 40 psf design load in this example. These figures are illustrative.</p>
<h2>Why it matters for a claim</h2>
<p>Snow-load claims often turn on whether a structure failed from the weight of snow and ice, which many policies cover, or from deterioration or defects, which they may not. Weather records, photos of snow depth and an engineer’s report are the strongest evidence. This estimator helps you frame the question, not answer it.</p>
<div class="note"><b class="h">Safety first</b>If a roof is sagging, cracking or making noise, get people out and call a professional. Don’t climb onto a loaded roof to clear it.</div>
""",
        "faqs": [("Where do I find my roof’s design snow load?", "Your local building department, the original building plans or a structural engineer. Utah design loads vary widely with elevation."), ("Is this an engineering calculation?", "No. It’s a planning estimate using typical densities. Only an engineer can evaluate a specific structure.")],
    },
]
