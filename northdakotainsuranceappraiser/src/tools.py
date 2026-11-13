"""Free claim tools: markup + explanatory copy. Logic lives in static/assets/js/app.js.

Everything runs in the visitor's browser; nothing is sent or stored.
"""

TOOL_BASE = "/claim-planning-tools/"

GAP_FULL = """
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Award break-even calculator</span><i>Runs in your browser</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Carrier’s estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="22600"><span class="hint">Replacement cost total before depreciation and deductible.</span></div>
        <div><label for="g-own">Your estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="37900"><span class="hint">Contractor or independent line-item estimate.</span></div>
      </div>
      <div><label for="g-land">Where might the award land inside the gap?</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% means the carrier’s number holds; 100% means your full number is awarded.</span></div>
      <div class="row2">
        <div><label for="g-ft">Appraiser fee basis</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of the increase (%)</option></select></div>
        <div><label for="g-fee">Fee amount</label><input id="g-fee" name="fee" inputmode="decimal" value="2800"></div>
      </div>
      <label class="check"><input type="checkbox" name="useump" checked> Add my half of an umpire’s fee</label>
      <div><label for="g-ump">Umpire’s total fee</label><input id="g-ump" name="umpire" inputmode="decimal" value="3200"><span class="hint">Usually split evenly between you and the carrier.</span></div>
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
        <div><span>Break-even landing point</span><b data-o="breakeven">—</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

GAP_MINI = """
<div class="tool tool-mini" data-tool="gap">
  <div class="tool-head"><span>Thirty-second gap check</span><i>No sign-up</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="m-ins">Carrier’s estimate</label><input id="m-ins" name="insurer" inputmode="decimal" value="16800"></div>
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
  <div class="tool-head"><span>Two-check payout calculator</span><i>Add as many line items as you need</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Laminated shingle roof", 21400, 11, 30), ("Steel siding — two elevations", 9600, 14, 40), ("Basement carpet & pad", 2300, 5, 10)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn ghost small" data-add data-run>+ Add line item</button></div>
      <div class="row2">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="1500"></div>
        <div><label for="d-cap">Depreciation cap</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="90">90%</option></select><span class="hint">Many estimates limit depreciation; check yours.</span></div>
      </div>
      <label class="check"><input type="checkbox" name="nonrec"> My policy (or this coverage) pays actual cash value only</label>
    </div>
    <div class="tool-out out-3" aria-live="polite">
      <div class="out-big"><small>First check (ACV − deductible)</small><b data-o="first">$0</b></div>
      <div class="out-big"><small>Held back until repairs</small><b data-o="held">$0</b></div>
      <div class="out-big"><small>Total once fully recovered</small><b data-o="total">$0</b></div>
      <div class="out-rows span-all">
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
  <div class="tool-head"><span>Roof area &amp; ice-barrier calculator</span><i>With an eave ice-barrier estimate</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <fieldset class="plain"><legend class="sr-only">Measurement method</legend>
        <div class="btn-row">
          <label class="check"><input type="radio" name="mode" value="dims" checked> Footprint length × width</label>
          <label class="check"><input type="radio" name="mode" value="area"> I know the footprint area</label>
        </div></fieldset>
      <div class="row2" data-mode="dims">
        <div><label for="r-l">Footprint length (ft)</label><input id="r-l" name="len" inputmode="decimal" value="52"></div>
        <div><label for="r-w">Footprint width (ft)</label><input id="r-w" name="wid" inputmode="decimal" value="30"></div>
      </div>
      <div data-mode="dims"><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="16"></div>
      <div data-mode="area" hidden><label for="r-a">Footprint area incl. overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="1900"></div>
      <div class="row2">
        <div><label for="r-p">Roof pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 5 else "", p) for p in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16]) + """</select></div>
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="10">10% — plain gable</option><option value="12" selected>12% — gable with a dormer or two</option><option value="15">15% — hip roof</option><option value="18">18% — cut-up / complex</option></select></div>
      </div>
      <div class="row2">
        <div><label for="r-in">Ice barrier reaches inside the wall (inches)</label><input id="r-in" name="inside" inputmode="decimal" value="24"><span class="hint">Cold-climate codes commonly call for 24″; confirm locally.</span></div>
        <div><label for="r-pr">Installed price per square (optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 560"></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Roof squares (before waste)</small><b data-o="sq">0</b></div>
      <div class="out-rows">
        <div><span>Pitch multiplier</span><b data-o="mult">1.000</b></div>
        <div><span>Roof surface area</span><b data-o="surface">0</b></div>
        <div><span>Squares to order (with waste)</span><b data-o="order">0</b></div>
        <div><span>Shingle bundles (3 per square)</span><b data-o="bundles">0</b></div>
        <div><span>Eave ice-barrier courses</span><b data-o="courses">—</b></div>
        <div><span>Ice-barrier linear feet</span><b data-o="icelf">—</b></div>
        <div><span>Rough replacement cost</span><b data-o="cost">—</b></div>
      </div>
      <p class="out-msg" data-o="steep"></p>
    </div>
  </div>
</div>"""

DEDUCT = """
<div class="tool" data-tool="deduct">
  <div class="tool-head"><span>Hail deductible dollar converter</span><i>Wind &amp; hail vs. flat</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling coverage (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="340000"><span class="hint">Printed on your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Wind/hail deductible</label><select id="w-p" name="pct"><option value="0.5">0.5%</option><option value="1" selected>1%</option><option value="2">2%</option><option value="3">3%</option><option value="5">5%</option></select></div>
        <div><label for="w-f">All-other-perils deductible ($)</label><input id="w-f" name="flat" inputmode="decimal" value="1500"></div>
      </div>
      <div><label for="w-l">Estimated storm damage</label><input id="w-l" name="loss" inputmode="decimal" value="18700"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your percentage deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s3"></span><span class="s1"></span></div>
      <div class="legend"><span><i class="s3"></i>You pay</span><span><i class="s1"></i>Policy pays</span></div>
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
  <div class="tool-head"><span>Policy clock &amp; freeze-up planner</span><i>Exports to your calendar (.ics)</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
      <p class="hint m0">Replace each default with the number in your own policy or letters. Defaults are placeholders, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report the claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="2"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="10"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Often counted from the carrier’s request.</span></div>
        <div><label for="t-r">Depreciation recovery (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="365"></div>
        <div><label for="t-s">Suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="730"><span class="hint">Use your policy’s figure; ask an attorney.</span></div>
        <div><label for="t-w">Construction-season check-in (days)</label><input id="t-w" name="season" inputmode="numeric" value="150"><span class="hint">A reminder to book contractors before freeze-up.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download .ics calendar file</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the insurer accepted coverage for at least part of the loss?", "Get written confirmation that coverage is accepted. If the claim was denied, talk to a North Dakota attorney before thinking about appraisal."),
    (3, "Do you have the carrier’s complete, itemized estimate — not just a summary page?", "Ask in writing for the full line-item estimate, including the price list date."),
    (3, "Do you have your own itemized estimate from a contractor or estimator?", "Get an independent line-item estimate; a one-line lump-sum bid rarely holds up in front of a panel."),
    (2, "Do you have dated photos taken soon after the storm or event?", "Collect every photo with its date, and add current photos of the same areas."),
    (2, "Have you read the appraisal paragraph in your policy’s conditions?", "Find the ‘Appraisal’ condition, note any deadlines and who pays what."),
    (2, "Do you know your policy’s suit-limitation date?", "Locate the ‘Suit Against Us’ condition and put the date in a calendar — the policy clock planner can help."),
    (2, "Were temporary repairs made, with receipts saved?", "Make reasonable temporary repairs (tarps, heat, water extraction) and keep every receipt."),
    (2, "If the loss happened in winter, has snow-covered or frozen damage been re-inspected after thaw?", "Schedule a follow-up inspection once roofs and siding are clear so the scope is complete."),
    (1, "Do you have your current declarations page?", "Download or request the declarations page that was in force on the date of loss."),
    (2, "Is hidden damage (attic, decking, wet walls, basement) opened up and documented?", "Make sure concealed areas were inspected so the scope isn’t missing whole rooms or layers."),
    (1, "Is your correspondence with the carrier organized by date?", "Gather letters, emails and adjuster notes into one dated file."),
    (2, "Is the gap between estimates more than roughly 10% or several thousand dollars?", "Run the award break-even calculator — a narrow gap may not justify appraisal costs."),
]

READY = """
<div class="tool tool-wide" data-tool="ready">
  <div class="tool-head"><span>Claim file strength test</span><i>12 questions · about two minutes</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <ol class="quiz">""" + "".join(
    '<li data-w="%d" data-fix="%s"><span>%s</span><span class="yn"><button type="button" class="yes" aria-pressed="false">Yes</button><button type="button" class="no" aria-pressed="false">No</button></span></li>' % (w, f, q)
    for w, q, f in _QUIZ) + """
      </ol>
      <div class="btn-row"><button type="button" class="btn ghost small" data-reset>Reset answers</button></div>
    </div>
    <div class="tool-out out-gauge" aria-live="polite">
      <div>
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#e3e9f7" stroke-width="18"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#ffd12b" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3" style="transition:stroke-dashoffset .5s,stroke .3s"/></svg>
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
  <div class="tool-head"><span>Snow &amp; ice roof weight estimator</span><i>For awareness, not engineering</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="s-d">Snow depth on the roof (inches)</label><input id="s-d" name="depth" inputmode="decimal" value="20"></div>
        <div><label for="s-t">What kind of snow?</label><select id="s-t" name="dens"><option value="7">Fresh, fluffy (~7 lb/ft³)</option><option value="15" selected>Settled (~15 lb/ft³)</option><option value="20">Wind-packed (~20 lb/ft³)</option><option value="30">Wet, heavy spring snow (~30 lb/ft³)</option></select></div>
      </div>
      <div class="row2">
        <div><label for="s-i">Ice layer thickness (inches)</label><input id="s-i" name="ice" inputmode="decimal" value="1"><span class="hint">Ice weighs roughly 57 lb/ft³.</span></div>
        <div><label for="s-a">Roof area (sq ft, optional)</label><input id="s-a" name="area" inputmode="decimal" value="1800"></div>
      </div>
      <div><label for="s-c">Design roof snow load (psf, optional)</label><input id="s-c" name="design" inputmode="decimal" placeholder="From plans, a truss tag or the building department"><span class="hint">Leave blank if you don’t know it — the tool will still show the weight.</span></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated load on the roof</small><b data-o="psf">0 psf</b></div>
      <div class="meter" aria-hidden="true"><span data-o="bar"></span></div>
      <div class="out-rows">
        <div><span>From snow</span><b data-o="snowpsf">0 psf</b></div>
        <div><span>From ice</span><b data-o="icepsf">0 psf</b></div>
        <div><span>Total weight on the roof</span><b data-o="lbs">—</b></div>
        <div><span>Share of design load</span><b data-o="share">—</b></div>
      </div>
      <p class="out-msg" data-o="smsg"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "award-break-even-calculator", "name": "Award Break-Even Calculator", "icon": "±$", "kind": "Calculator",
        "short": "Size the disputed amount, test where an award might land and see your break-even point after fees.",
        "title": "Award Break-Even Calculator | Is Appraisal Worth It?",
        "desc": "Compare the carrier’s estimate with yours, project an appraisal award and subtract appraiser and umpire fees to see your net and break-even.",
        "h1": "Award Break-Even Calculator for Appraisal Decisions",
        "lede": "Enter both estimates, slide the award between them and add realistic fees. The calculator shows the net increase and the landing point where appraisal stops paying for itself.",
        "markup": GAP_FULL,
        "explain": """
<h2>How to read the result</h2>
<ol><li><strong>Enter both totals at replacement cost</strong>, before depreciation and deductible, so you compare like with like.</li>
<li><strong>Slide the landing point.</strong> Try 30%, 50% and 75%. A dispute that only works at 90% is fragile.</li>
<li><strong>Add the fees you’ve actually been quoted.</strong> Flat and percentage arrangements behave very differently as the award grows.</li>
<li><strong>Check the break-even line.</strong> It shows the share of the gap the panel must award before you come out ahead.</li></ol>
<h2>Why a break-even point matters</h2>
<p>Appraisal costs money on both sides. If the break-even landing point is 20% of the gap, even a modest award helps you. If it’s 70%, you need a well-documented claim and a realistic expectation that most of your line items will survive review. That one figure often settles whether to invoke appraisal or ask for a documented supplement first.</p>
<h2>What this tool leaves out</h2>
<p>It doesn’t model deductibles, depreciation timing, policy limits or sub-limits. Those change what you’re paid, not the size of the dispute. For payment timing, use the <a href="/claim-planning-tools/two-check-payout-calculator/">two-check payout calculator</a>; for storm deductibles, the <a href="/claim-planning-tools/hail-deductible-dollar-converter/">hail deductible dollar converter</a>.</p>
<p class="small">All default figures are illustrative.</p>
""",
        "faqs": [("Is the projected award a prediction?", "No. It’s a what-if scenario based on the landing point you choose. Real awards depend on documentation, the panel and your policy language."), ("Who pays the umpire?", "Most appraisal clauses split the umpire’s fee evenly between you and the insurer, and each side pays its own appraiser. Check your policy’s wording.")],
    },
    {
        "slug": "two-check-payout-calculator", "name": "Two-Check Payout Calculator", "icon": "ACV", "kind": "Calculator",
        "short": "List damaged items with age and life to estimate the first ACV check and the depreciation held back.",
        "title": "Two-Check Payout Calculator | RCV vs ACV Math",
        "desc": "Free RCV/ACV calculator: enter line items with age and expected life to estimate your first check, recoverable depreciation and total payout.",
        "h1": "Two-Check Payout Calculator: ACV Now, Holdback Later",
        "lede": "Replacement-cost policies usually pay in two installments: actual cash value now and recoverable depreciation after repairs. Add your line items to see how the money splits.",
        "markup": DEP,
        "explain": """
<h2>The depreciation method used here</h2>
<p>The calculator applies straight-line depreciation — age divided by expected life — and stops at the cap you choose. Real estimates may adjust for condition, use different life tables or leave items such as permits and debris removal undepreciated, so treat the result as a planning figure.</p>
<h2>Life expectancies you’ll often see</h2>
<div class="table-wrap"><table><thead><tr><th>Item</th><th>Common range</th></tr></thead><tbody>
<tr><th>Laminated asphalt shingles</th><td>25–30 years</td></tr><tr><th>Steel or aluminum siding</th><td>35–50 years</td></tr><tr><th>Vinyl siding</th><td>30–40 years</td></tr><tr><th>Interior paint</th><td>8–12 years</td></tr><tr><th>Carpet and pad</th><td>8–12 years</td></tr><tr><th>Gas furnace</th><td>15–20 years</td></tr>
</tbody></table></div>
<h2>Getting the holdback released</h2>
<p>Most replacement-cost policies release recoverable depreciation after the work is completed within a stated time. With a short building season, a late-summer storm can push repairs into the next year — so note the deadline in the <a href="/claim-planning-tools/policy-clock-freeze-up-planner/">policy clock &amp; freeze-up planner</a> and ask in writing for an extension if a contractor can’t finish before freeze-up.</p>
<p class="small">Default line items and prices are illustrative.</p>
""",
        "faqs": [("Can labor be depreciated?", "Practices vary by policy, carrier and court decisions. Look at whether your estimate depreciates labor and ask the carrier to explain its method in writing."), ("What happens if I don’t repair?", "Under most replacement-cost policies you keep the actual cash value payment, but you may not collect the depreciation that was held back.")],
    },
    {
        "slug": "roof-area-ice-barrier-calculator", "name": "Roof Area & Ice-Barrier Calculator", "icon": "▲", "kind": "Calculator",
        "short": "Turn a footprint into true roof squares, bundles and eave ice-barrier footage for a cold-climate roof.",
        "title": "Roof Area & Ice-Barrier Calculator | Squares",
        "desc": "Estimate roof squares from footprint, pitch and waste, plus eave ice-barrier courses and footage, then compare with the carrier’s roof estimate.",
        "h1": "Roof Area & Ice-Barrier Calculator for Cold-Climate Roofs",
        "lede": "Short measurements and a missing eave membrane are two of the most common gaps in roof claims. Use the footprint and pitch to estimate true squares, bundles and ice-barrier footage.",
        "markup": ROOF,
        "explain": """
<h2>How the math works</h2>
<p>Roof surface is larger than the footprint underneath it. The pitch multiplier is √(1 + (rise ÷ 12)²): a 5/12 roof is about 8.3% larger than its footprint, a 12/12 roof about 41.4% larger. Squares are surface area divided by 100.</p>
<h2>The eave ice-barrier estimate</h2>
<p>Cold-climate building codes commonly require a self-adhering ice barrier from the eave edge to a point at least 24 inches inside the exterior wall. The calculator measures that distance along the slope (overhang plus the inside distance, times the pitch multiplier), divides it by a roughly three-foot roll width to get the number of courses, and multiplies by the eave length of a simple gable roof. Hip roofs have eaves on all four sides, so adjust if yours does.</p>
<h2>Checking the carrier’s roof estimate</h2>
<ul><li>Compare total squares and the waste percentage with the result here; a gap over 5–10% deserves a closer look.</li>
<li>Look for separate line items for ice and water barrier, drip edge, starter, ridge cap and step flashing.</li>
<li>Check for steep charges (often starting around 7/12) and high-roof charges on two-story sections.</li></ul>
<p>Complex roofs with several planes need measuring plane by plane; treat this as a sanity check, not a measurement report.</p>
""",
        "faqs": [("What is a roofing “square”?", "One hundred square feet of roof surface. Waste is added on top because hips, valleys and cuts turn some material into scrap."), ("Is ice barrier required on every North Dakota roof?", "Requirements depend on the code your city or county has adopted and when the roof was installed. Ask the local building department, and check whether ordinance-or-law coverage applies to code upgrades.")],
    },
    {
        "slug": "hail-deductible-dollar-converter", "name": "Hail Deductible Dollar Converter", "icon": "%", "kind": "Calculator",
        "short": "Convert a percentage wind/hail deductible into dollars and see what a storm claim would actually pay.",
        "title": "Hail Deductible Dollar Converter | 1% & 2%",
        "desc": "Turn a 1% or 2% wind/hail deductible into dollars and compare what a storm claim pays against a flat all-other-perils deductible.",
        "h1": "Hail Deductible Dollar Converter: Percentages to Dollars",
        "lede": "A 1% deductible sounds small until you multiply it by your dwelling limit. See the deductible in real dollars and what it does to a hail or wind payment.",
        "markup": DEDUCT,
        "explain": """
<h2>Why percentage deductibles surprise people</h2>
<p>In hail country, some policies carry a separate wind/hail deductible calculated as a percentage of Coverage A, the dwelling limit. On a $340,000 limit (illustrative), a 1% deductible is $3,400 and a 2% deductible is $6,800 — far more than a flat $1,500 deductible for other losses.</p>
<h2>Where to find yours</h2>
<p>Look on the declarations page for “wind/hail,” “windstorm or hail” or a percentage next to the deductible line, then read the endorsement that defines when it applies. Some apply per occurrence; some carriers also use roof-surfacing endorsements that pay roofs on an actual-cash-value schedule.</p>
<h2>How it affects appraisal</h2>
<p>A deductible doesn’t change the amount of loss an appraisal panel decides, but it changes what you receive. A loss just above the deductible may not justify appraisal costs; one well above it might.</p>
""",
        "faqs": [("Does the percentage apply to the whole claim?", "Usually the percentage is calculated from Coverage A and then applied to the wind or hail loss as a whole. Policy wording controls, so read the endorsement."), ("Can I change it?", "Typically at renewal. A higher deductible lowers premium but raises your share of every storm loss.")],
    },
    {
        "slug": "policy-clock-freeze-up-planner", "name": "Policy Clock & Freeze-Up Planner", "icon": "◷", "kind": "Planner",
        "short": "Map notice, proof-of-loss, holdback and suit dates from your date of loss, then export an .ics file.",
        "title": "Policy Clock & Freeze-Up Planner | .ics Export",
        "desc": "Enter your date of loss to build a claim timeline with proof of loss, holdback, suit and construction-season dates, then export it to a calendar.",
        "h1": "Policy Clock & Freeze-Up Planner for North Dakota Claims",
        "lede": "Policy clocks keep running while you argue about a number — and the building season is short. Build a dated timeline from your policy’s windows and download it to your calendar.",
        "markup": DATES,
        "explain": """
<h2>The dates that matter most</h2>
<ul><li><strong>Prompt notice.</strong> Policies require you to report a loss promptly; late notice is a common carrier defense.</li>
<li><strong>Proof of loss.</strong> If the insurer requests a sworn proof of loss, the policy sets the time to return it, often counted from the request.</li>
<li><strong>Depreciation recovery.</strong> Replacement-cost policies typically require repairs within a stated period to release holdback.</li>
<li><strong>Suit limitation.</strong> Policies limit how long you have to sue, and state law can affect how that’s applied. Appraisal doesn’t automatically pause it.</li>
<li><strong>Construction season.</strong> In North Dakota, roofing and exterior work slows sharply once the ground freezes. The extra reminder helps you book contractors early.</li></ul>
<div class="note"><b class="h">Important</b>The planner uses only the numbers you enter. It isn’t legal advice, and courts can read deadlines differently. If a date is close, talk to a North Dakota attorney promptly.</div>
""",
        "faqs": [("Is the date of loss the day I noticed damage?", "Usually it’s the date the storm or event happened. Weather data for your address can help pin down a hail date."), ("Does invoking appraisal stop the suit deadline?", "Not automatically. Some policies or written agreements address it; many don’t. Protect the deadline separately.")],
    },
    {
        "slug": "claim-file-strength-test", "name": "Claim File Strength Test", "icon": "✓", "kind": "Checklist",
        "short": "Twelve yes/no questions that score your claim file and build a to-do list before you invoke appraisal.",
        "title": "Claim File Strength Test | Ready for Appraisal?",
        "desc": "Answer twelve quick questions to score how ready your property claim is for appraisal and get a personal to-do list of what to finish first.",
        "h1": "Claim File Strength Test: Is Your File Appraisal-Ready?",
        "lede": "The strongest appraisals are won with the file you bring to the table. Answer twelve questions to see where yours stands and what to fix before anyone signs a demand.",
        "markup": READY,
        "explain": """
<h2>How the questions are weighted</h2>
<p>Coverage, estimates and evidence carry the most weight because they decide whether appraisal is even the right tool and how well your number will hold up. Administrative items matter too, but they’re quicker to fix. One question is specific to cold-weather losses: snow and ice can hide damage that only shows after thaw.</p>
<h2>What to do with your score</h2>
<ul><li><strong>75 and up:</strong> your file looks solid. A professional review of the gap is the logical next step.</li>
<li><strong>45 to 74:</strong> close the open items first; each one strengthens your position.</li>
<li><strong>Below 45:</strong> invoking appraisal now could lock in a low number. Build the file before you demand.</li></ul>
""",
        "faqs": [("Is anything I enter saved?", "No. The check runs entirely in your browser; nothing is stored or sent."), ("Can I share the result?", "Yes. Take a screenshot of the score and to-do list and bring it to a consultation.")],
    },
    {
        "slug": "snow-ice-roof-weight-estimator", "name": "Snow & Ice Roof Weight Estimator", "icon": "❄", "kind": "Estimator",
        "short": "Estimate pounds per square foot from snow depth, snow type and ice — and compare it with a design load.",
        "title": "Snow & Ice Roof Weight Estimator | PSF Check",
        "desc": "Estimate the weight of snow and ice on your roof from depth and snow type, see total pounds and compare with a design roof snow load you enter.",
        "h1": "Snow & Ice Roof Weight Estimator for Heavy Winters",
        "lede": "A foot of fresh powder and a foot of wet March snow are very different loads. Enter depth, snow type and any ice layer to estimate what your roof is carrying right now.",
        "markup": SNOW,
        "explain": """
<h2>How the estimate works</h2>
<p>Weight per square foot equals depth in feet times density. Densities vary widely: freshly fallen snow can be around 5–8 lb/ft³, settled snow often 15–20, wind-packed drifts more, and wet spring snow 30 or higher. Ice is roughly 57 lb/ft³. The tool adds the snow and ice layers and, if you enter a roof area, multiplies to get total weight.</p>
<h2>What the design load means</h2>
<p>Buildings are designed for a roof snow load set by the code in force when they were built, often shown on truss tags, plans or permits. Drifts behind parapets, valleys and lower roofs next to taller ones can carry far more than the average. If the estimate approaches the design figure, call a qualified contractor or engineer — and never climb onto a loaded roof yourself.</p>
<h2>When snow load becomes a claim</h2>
<p>Sagging ceilings, cracked drywall at the ceiling line, doors that stick, bent trusses and collapsed outbuildings are common snow-load losses. Many policies cover collapse caused by the weight of ice, snow or sleet, subject to their terms. Our <a href="/appraisal-representation/freeze-ice-dam-snow-load-appraisal/">freeze, ice dam &amp; snow load appraisal</a> page explains how these claims are scoped.</p>
<div class="note"><b class="h">Safety first</b>This is an awareness tool, not an engineering analysis. It can’t account for drifting, roof framing condition or uneven loads.</div>
""",
        "faqs": [("Why does wet spring snow matter so much?", "Rain or melt soaking into an existing snowpack can double its density without adding much depth, so the load rises even if the roof looks the same."), ("Where do I find my roof’s design load?", "Check building plans, truss manufacturer tags in the attic, the original permit, or ask your city or county building department.")],
    },
]
