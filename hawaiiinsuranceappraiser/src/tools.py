"""Interactive claim tools for Hawaii Insurance Appraiser: markup + explanatory copy.
Logic lives in static/assets/js/app.js. Everything runs in the browser; nothing is stored or sent."""

BASE = "/island-claim-tools/"

GAP_FULL = """
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Claim gap &amp; fee estimator</span><i>Runs in your browser</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Carrier’s estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="42600"><span class="hint">Replacement cost total before depreciation.</span></div>
        <div><label for="g-own">Your estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="68900"><span class="hint">Contractor’s or independent line-item estimate.</span></div>
      </div>
      <div><label for="g-land">Test an award landing point within the gap</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% means the carrier’s number holds; 100% means your full number is awarded.</span></div>
      <div class="row2">
        <div><label for="g-ft">Your appraiser’s fee basis</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of the increase (%)</option><option value="hourly">Hourly (hours × rate)</option></select></div>
        <div><label for="g-fee">Fee amount or rate</label><input id="g-fee" name="fee" inputmode="decimal" value="3500"></div>
      </div>
      <div class="row2">
        <div><label for="g-hrs">Hours (hourly basis only)</label><input id="g-hrs" name="hours" inputmode="decimal" value="20"></div>
        <div><label for="g-trv">Inter-island travel ($)</label><input id="g-trv" name="travel" inputmode="decimal" value="0"><span class="hint">Flights or car rental if the property is on a neighbor island.</span></div>
      </div>
      <div><label for="g-ump">Umpire’s total fee (you pay half)</label><input id="g-ump" name="umpire" inputmode="decimal" value="4000"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated net increase to you</small><b data-o="net">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s1"></span><span class="s2"></span><span class="s3"></span></div>
      <div class="legend"><span><i class="s1"></i>Carrier’s number</span><span><i class="s2"></i>Your net gain</span><span><i class="s3"></i>Appraisal costs</span></div>
      <div class="out-rows">
        <div><span>Amount in dispute</span><b data-o="gap">$0</b></div>
        <div><span>Gap as % of carrier estimate</span><b data-o="pct">—</b></div>
        <div><span>Projected award (RCV)</span><b data-o="award">$0</b></div>
        <div><span>Your appraisal costs</span><b data-o="cost">$0</b></div>
      </div>
      <div class="scen"><p class="todo-h">Net at three landing points</p><div class="scen-row"><span>30%<b data-o="s30">$0</b></span><span>50%<b data-o="s50">$0</b></span><span>80%<b data-o="s80">$0</b></span></div></div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

GAP_MINI = """
<div class="tool" data-tool="gap" style="margin:0">
  <div class="tool-head"><span>Two-number gap check</span><i>No sign-up</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="m-ins">Carrier’s estimate</label><input id="m-ins" name="insurer" inputmode="decimal" value="23800"></div>
      <div><label for="m-own">Your contractor’s estimate</label><input id="m-own" name="yours" inputmode="decimal" value="39400"></div>
      <div><label for="m-land">Award lands at</label><div class="range"><input id="m-land" type="range" name="land" min="0" max="100" step="5" value="50" data-unit="%"><output>50%</output></div><span class="hint">of the disputed amount</span></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Amount in dispute</small><b data-o="gap">$0</b></div>
      <div class="out-rows">
        <div><span>Gap vs. carrier estimate</span><b data-o="pct">—</b></div>
        <div><span>Projected award</span><b data-o="award">$0</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

_DEP_ROW = """<tr><td><input name="item" value="{0}" aria-label="Item"></td><td><input name="rcv" inputmode="decimal" value="{1}" aria-label="Replacement cost"></td><td><input name="age" inputmode="decimal" value="{2}" aria-label="Age in years"></td><td><input name="life" inputmode="decimal" value="{3}" aria-label="Expected life in years"></td><td class="mono" data-o="row">$0</td><td><button type="button" class="x" aria-label="Remove row">×</button></td></tr>"""

DEP = """
<div class="tool tool-wide" data-tool="dep">
  <div class="tool-head"><span>RCV / ACV holdback calculator</span><i>Add as many line items as you need</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Corrugated metal roof panels", 24800, 11, 40), ("Interior paint — main living area", 3100, 5, 10), ("Vinyl plank flooring", 6400, 4, 20), ("Window AC units (2)", 1500, 6, 10)]) + """
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
  <div class="tool-head"><span>Roof pitch &amp; squares estimator</span><i>Shingle or metal</i></div>
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
      <div data-mode="dims"><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="18"><span class="hint">Island homes often have deep eaves for shade and rain.</span></div>
      <div data-mode="area" hidden><label for="r-a">Footprint area incl. overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="1900"></div>
      <div class="row2">
        <div><label for="r-p">Roof pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 5 else "", p) for p in [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14]) + """</select></div>
        <div><label for="r-mat">Roof material</label><select id="r-mat" name="mat"><option value="shingle">Asphalt shingles</option><option value="metal" selected>Metal panels</option></select></div>
      </div>
      <div class="row2">
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="5">5% — simple metal gable</option><option value="10" selected>10% — gable</option><option value="15">15% — hip roof</option><option value="18">18% — cut-up / multiple planes</option></select></div>
        <div><label for="r-pr">Installed price per square (optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 1150"></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Roof squares (before waste)</small><b data-o="sq">0</b></div>
      <div class="out-rows">
        <div><span>Pitch multiplier</span><b data-o="mult">1.000</b></div>
        <div><span>Roof surface area</span><b data-o="surface">0</b></div>
        <div><span>Squares to order (with waste)</span><b data-o="order">0</b></div>
        <div><span data-o="unitlabel">Shingle bundles (3 per square)</span><b data-o="bundles">0</b></div>
        <div><span>Rough replacement cost</span><b data-o="cost">—</b></div>
      </div>
      <p class="out-msg" data-o="steep"></p>
    </div>
  </div>
</div>"""

DEDUCT = """
<div class="tool" data-tool="deduct">
  <div class="tool-head"><span>Hurricane deductible calculator</span><i>Percentage vs. flat</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling coverage (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="720000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Hurricane deductible</label><select id="w-p" name="pct"><option value="1">1%</option><option value="2" selected>2%</option><option value="3">3%</option><option value="5">5%</option><option value="10">10%</option></select></div>
        <div><label for="w-f">All-other-perils deductible ($)</label><input id="w-f" name="flat" inputmode="decimal" value="2500"></div>
      </div>
      <div><label for="w-l">Estimated hurricane damage</label><input id="w-l" name="loss" inputmode="decimal" value="38500"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your hurricane deductible in dollars</small><b data-o="pd">$0</b></div>
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
  <div class="tool-head"><span>Claim timeline builder</span><i>Exports an .ics calendar file</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
      <p class="hint nomargin">Change each window to match your own policy. The defaults are common placeholders, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report the claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="3"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="10"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Often counted from the carrier’s written request.</span></div>
        <div><label for="t-r">Depreciation recovery (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="365"></div>
        <div><label for="t-s">Suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="730"><span class="hint">Read the “Suit Against Us” clause for your number.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download .ics calendar file</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the insurer accepted coverage for at least part of the loss in writing?", "Get written confirmation that coverage is accepted. If the claim was denied, speak with a Hawaii attorney before considering appraisal."),
    (3, "Do you have the carrier’s complete, line-item estimate (not just a payment letter)?", "Ask the adjuster for the full itemized estimate in writing, including the price list date."),
    (3, "Do you have your own line-item estimate from a contractor or estimator?", "Get an itemized estimate. A one-line lump-sum bid is hard to defend in front of a panel."),
    (2, "Do you have dated photos and video taken soon after the loss?", "Gather every photo and note when it was taken. Add current photos before repairs change anything."),
    (2, "Have you read the appraisal clause in your policy (or the AOAO master policy)?", "Find the ‘Appraisal’ paragraph in the conditions section and note any deadlines for naming an appraiser."),
    (2, "Do you know your policy’s suit-limitation date?", "Locate the ‘Suit Against Us’ clause and put the date on a calendar — the timeline builder can help."),
    (2, "Were temporary repairs made and receipts saved?", "Complete reasonable temporary repairs such as tarps, dry-out and board-up, and keep every receipt."),
    (1, "Do you have your current declarations page, including any hurricane deductible?", "Download or request the declarations page and note each deductible."),
    (2, "Has hidden damage been opened up and documented (walls, attic, subfloor, ceilings below)?", "Make sure wet materials, roof decking and units below have been inspected so the scope is complete."),
    (2, "Does your estimate include freight, general excise tax and island labor pricing?", "Ask your contractor to show freight, GET and local labor rates separately so they can be compared line by line."),
    (2, "Is the gap between the two estimates more than about 10% or several thousand dollars?", "Run the numbers in the claim gap & fee estimator — a small gap may not justify appraisal costs."),
    (1, "Has a sworn proof of loss been returned if the carrier asked for one?", "If a proof of loss was requested, return it on time and keep a copy."),
]

READY = """
<div class="tool tool-wide" data-tool="ready">
  <div class="tool-head"><span>Appraisal readiness check</span><i>12 questions · about two minutes</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <ol class="quiz">""" + "".join(
    '<li data-w="%d" data-fix="%s"><span>%s</span><span class="yn"><button type="button" class="yes" aria-pressed="false">Yes</button><button type="button" class="no" aria-pressed="false">No</button></span></li>' % (w, f, q)
    for w, q, f in _QUIZ) + """
      </ol>
      <div class="btn-row"><button type="button" class="btn ghost small" data-reset>Reset answers</button></div>
    </div>
    <div class="tool-out ready-out" aria-live="polite">
      <div>
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#ece4f6" stroke-width="18"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#f2b544" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3" style="transition:stroke-dashoffset .5s,stroke .3s"/></svg>
        <div class="gauge-num"><span data-o="score">–</span></div>
        <p class="hint center">Answered <span data-o="count">0 / 12</span></p>
      </div>
      <div>
        <p class="out-msg" data-o="verdict"></p>
        <p class="todo-h">Your to-do list</p>
        <ul data-o="todo" class="todo"></ul>
      </div>
    </div>
  </div>
</div>"""

CONDO = """
<div class="tool" data-tool="condo">
  <div class="tool-head"><span>Condo deductible share calculator</span><i>Master policy + HO-6</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="c-loss">Covered building loss (association claim)</label><input id="c-loss" name="loss" inputmode="decimal" value="180000"></div>
        <div><label for="c-val">Building insured value (for % deductibles)</label><input id="c-val" name="value" inputmode="decimal" value="48000000"></div>
      </div>
      <div class="row2">
        <div><label for="c-dt">Master policy deductible type</label><select id="c-dt" name="dtype"><option value="flat">Flat dollar amount</option><option value="pct">Percent of insured value</option></select></div>
        <div><label for="c-ded">Deductible ($ or %)</label><input id="c-ded" name="ded" inputmode="decimal" value="100000"></div>
      </div>
      <div class="row2">
        <div><label for="c-how">How the association allocates it</label><select id="c-how" name="how"><option value="ci">Across all owners by common interest</option><option value="unit">To the unit(s) where the loss started</option></select></div>
        <div><label for="c-share">Your share (%)</label><input id="c-share" name="share" inputmode="decimal" value="0.85"><span class="hint">Your common-interest % from the declaration, or your share of the origin units.</span></div>
      </div>
      <div class="row2">
        <div><label for="c-la">HO-6 loss assessment limit</label><input id="c-la" name="la" inputmode="decimal" value="50000"></div>
        <div><label for="c-d6">HO-6 deductible on assessments</label><input id="c-d6" name="d6" inputmode="decimal" value="1000"></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your estimated out-of-pocket</small><b data-o="oop">$0</b></div>
      <div class="out-rows">
        <div><span>Master deductible in dollars</span><b data-o="dd">$0</b></div>
        <div><span>Deductible the association absorbs</span><b data-o="absorb">$0</b></div>
        <div><span>Master policy pays</span><b data-o="master">$0</b></div>
        <div><span>Assessed to you</span><b data-o="assess">$0</b></div>
        <div><span>Your HO-6 may pay</span><b data-o="ho6">$0</b></div>
      </div>
      <p class="out-msg" data-o="cmsg"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "claim-gap-fee-estimator", "name": "Claim Gap & Fee Estimator", "icon": "Δ", "kind": "Calculator",
        "short": "Compare the two estimates, test where an award might land and subtract fees, travel and half the umpire.",
        "keyword": "insurance appraisal cost calculator",
        "title": "Insurance Appraisal Cost Calculator | Claim Gap & Fees",
        "desc": "Free insurance appraisal cost calculator: compare both estimates, test award outcomes and subtract fees, travel and the umpire share.",
        "h1": "Claim Gap & Fee Estimator: What Would Appraisal Net You?",
        "lede": "Enter the carrier’s number and yours, test a few landing points, then add realistic fees — including inter-island travel when the property is on a neighbor island.",
        "markup": GAP_FULL,
        "explain": """
<h2>How to use the estimator</h2>
<ol><li><strong>Enter the carrier’s RCV total</strong> — the replacement cost figure before depreciation and the deductible come off.</li>
<li><strong>Enter your own RCV total</strong> from an itemized contractor or independent estimate.</li>
<li><strong>Slide the landing point.</strong> The three-scenario strip shows the net at 30%, 50% and 80% of the gap at the same time.</li>
<li><strong>Add costs</strong> on the basis your appraiser quoted — flat, percentage or hourly — plus travel and half of a realistic umpire fee.</li></ol>
<h2>Reading the three scenarios</h2>
<p>Appraisal panels rarely adopt either side’s opening number in full. Line items backed by photos, measurements and current island pricing tend to survive; unsupported items tend to fall away. If appraisal only pays off at the 80% landing point, the file is fragile. If the 30% scenario is still comfortably positive, the dispute is more likely to be worth pursuing.</p>
<h2>Island cost factors to keep in mind</h2>
<ul><li><strong>Travel.</strong> Inspections on Molokai, Lanai or a different island from your appraiser can add airfare and a rental car.</li>
<li><strong>Umpire availability.</strong> Some neighbor-island panels use an umpire from Oahu, which can affect scheduling and cost.</li>
<li><strong>Pricing basis.</strong> Both estimates should treat freight and <a href="/hawaii-claim-guides/general-excise-tax-and-freight-in-estimates/">general excise tax</a> consistently, or the “gap” is partly an apples-to-oranges problem.</li></ul>
<p>The default figures above are illustrative only. For the payment side of the claim — depreciation and holdback — use the <a href="/island-claim-tools/rcv-acv-holdback-calculator/">RCV/ACV holdback calculator</a>.</p>
""",
        "faqs": [("Is the projected award a prediction?", "No. It is a planning scenario based on the numbers you enter. Real awards depend on documentation, the panel and the policy wording."), ("Who pays the umpire?", "Most appraisal clauses split the umpire’s fee equally between you and the insurer, while each side pays its own appraiser. Check your policy’s wording.")],
    },
    {
        "slug": "rcv-acv-holdback-calculator", "name": "RCV/ACV Holdback Calculator", "icon": "ACV", "kind": "Calculator",
        "short": "List damaged items with age and life to estimate the first ACV check, the holdback and the total after repairs.",
        "keyword": "rcv vs acv calculator",
        "title": "RCV vs ACV Calculator | Depreciation Holdback Estimate",
        "desc": "Use this RCV vs ACV calculator to estimate your first claim check, the depreciation held back and the total once repairs are complete.",
        "h1": "RCV/ACV Holdback Calculator for Property Claims",
        "lede": "Replacement cost policies usually pay in two stages: actual cash value now and recoverable depreciation after repairs. List your items to see how the money splits.",
        "markup": DEP,
        "explain": """
<h2>How depreciation is calculated here</h2>
<p>The calculator uses straight-line depreciation — age divided by expected life — capped at the maximum you choose. Real estimates may use condition adjustments, different life expectancies or non-depreciable items such as permits and some labor, so treat the result as a planning figure.</p>
<h2>Island-specific life expectancy questions</h2>
<p>Salt air, strong UV and constant humidity shorten the life of some materials and lengthen arguments about others. Carriers sometimes apply heavy depreciation to metal roofing, window units or exterior paint near the shoreline. Ask how the life expectancy was chosen and whether it reflects the actual material installed.</p>
<div class="table-wrap"><table><thead><tr><th>Item</th><th>Range often seen in estimates</th></tr></thead><tbody>
<tr><th>Architectural shingles</th><td>25–30 years</td></tr><tr><th>Painted metal roof panels</th><td>30–50 years</td></tr><tr><th>Interior paint</th><td>8–12 years</td></tr><tr><th>Vinyl plank flooring</th><td>15–25 years</td></tr><tr><th>Window or split AC units</th><td>10–15 years</td></tr><tr><th>Water heater</th><td>8–15 years</td></tr>
</tbody></table></div>
<p>Ranges are general and illustrative, not a standard any carrier must use.</p>
<h2>Getting holdback released</h2>
<p>Most policies release recoverable depreciation once repairs are finished within a time limit. Send invoices and photos of completed work, and calendar the deadline with the <a href="/island-claim-tools/claim-timeline-builder/">claim timeline builder</a>.</p>
""",
        "faqs": [("Can labor be depreciated?", "Practice varies by policy and jurisdiction. Ask the carrier to explain in writing whether and how labor was depreciated in your estimate."), ("What happens if I don’t rebuild?", "Under most replacement cost policies you keep the actual cash value payment but may not collect the depreciation that was held back.")],
    },
    {
        "slug": "roof-pitch-squares-estimator", "name": "Roof Pitch & Squares Estimator", "icon": "▲", "kind": "Calculator",
        "short": "Turn a footprint into true roof squares for shingle or metal roofs, then check the carrier’s measurements.",
        "keyword": "roof squares calculator",
        "title": "Roof Squares Calculator | Pitch, Waste & Metal Roofs",
        "desc": "Roof squares calculator for insurance claims: convert footprint, pitch and waste into true roof area for shingle or metal roofing.",
        "h1": "Roof Pitch & Squares Estimator for Insurance Claims",
        "lede": "Measurement errors are a common reason roof claims come up short. Use the footprint, eave depth and pitch to estimate true roof area for shingles or metal panels.",
        "markup": ROOF,
        "explain": """
<h2>The math behind it</h2>
<p>A sloped roof has more surface than the footprint under it. The pitch multiplier is √(1 + (rise ÷ 12)²): a 4/12 roof is about 5.4% larger than its footprint, a 6/12 roof about 11.8% larger and a 12/12 roof about 41.4% larger. Deep eaves, common on island homes, add surface that is easy to leave out.</p>
<h2>Metal versus shingle</h2>
<ul><li><strong>Metal panels</strong> run in continuous lengths, so waste is usually lower on simple gables but climbs fast on hips and cut-up roofs. Estimates should also list trim, ridge, closures and fasteners.</li>
<li><strong>Shingles</strong> are ordered by the bundle (about three per square) plus starter, ridge cap and underlayment.</li></ul>
<h2>Checking the carrier’s estimate</h2>
<ul><li>Find the total squares and waste percentage on the roof page of the estimate.</li>
<li>Differences of more than 5–10% from your result deserve a closer look or a field measurement.</li>
<li>Look for steep and high-roof charges, especially on two-story homes and hillside lots.</li>
<li>Confirm whether the estimate prices full panels or only “repairs” on a metal roof whose panels can’t be matched — see our <a href="/appraisal-specialties/roof-hail-claim-appraisal/">roof claim appraisal</a> page.</li></ul>
""",
        "faqs": [("What is a roofing square?", "One square is 100 square feet of roof surface, measured on the slope rather than the footprint."), ("Is a footprint calculation good enough for appraisal?", "It is a sanity check. Roofs with several pitches, dormers or additions should be measured plane by plane or with an aerial report.")],
    },
    {
        "slug": "hurricane-deductible-calculator", "name": "Hurricane Deductible Calculator", "icon": "%", "kind": "Calculator",
        "short": "Convert a percentage hurricane deductible into dollars and compare what a storm claim would actually pay.",
        "keyword": "hurricane deductible calculator",
        "title": "Hurricane Deductible Calculator | Percent to Dollars",
        "desc": "Free hurricane deductible calculator: turn a percentage deductible into dollars and compare what your policy pays against a flat deductible.",
        "h1": "Hurricane Deductible Calculator for Island Homeowners",
        "lede": "A 2% hurricane deductible sounds small until it’s multiplied by island rebuilding values. See your deductible in real dollars and what a storm claim would pay.",
        "markup": DEDUCT,
        "explain": """
<h2>Why percentage deductibles catch people off guard</h2>
<p>Many island homeowners carry a separate hurricane deductible written as a percentage of dwelling coverage. Because rebuilding costs here are high, Coverage A limits are high too — and so is the deductible. In the illustrative default above, 2% of $720,000 is $14,400, not the $2,500 that applies to most other losses.</p>
<h2>When it applies</h2>
<p>Policies define the trigger differently. Some apply the hurricane deductible only when the National Weather Service has issued a hurricane watch or warning for the islands, others to any named storm, and some for a set period afterward. Wind damage from a Kona low or trade-wind gusts usually falls under the regular deductible. Read the endorsement and our guide to <a href="/hawaii-claim-guides/hurricane-deductibles-in-hawaii/">hurricane deductibles in Hawaii</a>.</p>
<h2>How it affects an appraisal decision</h2>
<p>The deductible doesn’t change the amount of loss a panel decides, but it changes what you receive. A loss just above a large deductible may not be worth disputing; one well above it often is. Combine this result with the <a href="/island-claim-tools/claim-gap-fee-estimator/">claim gap &amp; fee estimator</a>.</p>
""",
        "faqs": [("Does the percentage apply to contents too?", "The dollar amount is usually calculated from Coverage A but applied to the whole hurricane loss. Check your policy’s endorsement for the exact wording."), ("Can I lower my hurricane deductible?", "Options depend on the carrier and are usually available at renewal. A lower deductible typically means a higher premium.")],
    },
    {
        "slug": "claim-timeline-builder", "name": "Claim Timeline Builder", "icon": "◷", "kind": "Planner",
        "short": "Map notice, proof-of-loss, holdback and suit-limitation dates from your date of loss, then export them.",
        "keyword": "insurance claim deadline calculator",
        "title": "Insurance Claim Deadline Calculator | Calendar Export",
        "desc": "Insurance claim deadline calculator: map proof-of-loss, depreciation and suit dates from your date of loss and export them to a calendar.",
        "h1": "Claim Timeline Builder: Map Your Policy Deadlines",
        "lede": "Policy deadlines keep running while you argue about a number. Enter your date of loss and your policy’s windows to build a timeline you can download to any calendar app.",
        "markup": DATES,
        "explain": """
<h2>The dates that matter</h2>
<ul><li><strong>Prompt notice.</strong> Policies require you to report a loss promptly. Late notice is a common carrier defense.</li>
<li><strong>Proof of loss.</strong> If the carrier asks for a sworn proof of loss, many policies give a fixed number of days to return it.</li>
<li><strong>Depreciation recovery.</strong> Replacement cost policies often require repairs within a set period to collect holdback — and after a major island disaster, contractor and permit backlogs can make that tight.</li>
<li><strong>Suit limitation.</strong> Policies limit how long you have to file suit. Invoking appraisal does not automatically pause that clock.</li></ul>
<div class="note"><b class="h">Important</b>The planner uses only the numbers you type in. It isn’t legal advice, and deadlines can be interpreted differently. If a date is close, contact a Hawaii attorney promptly.</div>
<h2>Using the calendar file</h2>
<p>The download is a standard .ics file. Open it on your phone or computer to add every milestone as an all-day event. Nothing is uploaded — the file is created in your browser.</p>
""",
        "faqs": [("Is the date of loss the day I found the damage?", "Usually it is the date of the storm or event. Weather records for your area can help pin it down if you aren’t sure."), ("Does appraisal extend my deadline to sue?", "Not automatically. Some policies or written agreements address it, but many don’t, so protect the date independently.")],
    },
    {
        "slug": "appraisal-readiness-check", "name": "Appraisal Readiness Check", "icon": "✓", "kind": "Checklist",
        "short": "Answer 12 yes/no questions to score your file and get a to-do list before anyone invokes appraisal.",
        "keyword": "appraisal readiness checklist",
        "title": "Appraisal Readiness Checklist | Score Your Claim File",
        "desc": "A 12-question appraisal readiness checklist that scores your property claim file and builds a to-do list of what to finish first.",
        "h1": "Appraisal Readiness Check: Is Your Claim File Ready?",
        "lede": "The strongest appraisals are prepared before anyone sends a demand. Answer twelve quick questions to see where your file stands and what to fix first.",
        "markup": READY,
        "explain": """
<h2>How the score is weighted</h2>
<p>Coverage, estimates and evidence carry the most weight because they decide whether appraisal is the right tool at all and how well your number will hold up. Administrative items matter too, but they are easier to fix later.</p>
<h2>What your result means</h2>
<ul><li><strong>75 and above:</strong> the file is in good shape. A professional review of the dollar gap is the logical next step.</li>
<li><strong>45 to 74:</strong> close the open items first; each one strengthens your number.</li>
<li><strong>Below 45:</strong> demanding appraisal now could lock in a low award. Build the file first.</li></ul>
<p>Condo owners should run the check twice — once for the association’s master policy claim and once for their own HO-6 claim — and then try the <a href="/island-claim-tools/condo-deductible-share-calculator/">condo deductible share calculator</a>.</p>
""",
        "faqs": [("Is anything I answer saved?", "No. The checklist runs entirely in your browser and nothing is stored or sent."), ("Can I bring my result to a consultation?", "Yes. Take a screenshot or note your to-do list and bring it to the call.")],
    },
    {
        "slug": "condo-deductible-share-calculator", "name": "Condo Deductible Share Calculator", "icon": "▦", "kind": "Calculator",
        "short": "Estimate how an AOAO master-policy deductible could be assessed to you and what your HO-6 might cover.",
        "keyword": "condo deductible assessment calculator",
        "title": "Condo Deductible Assessment Calculator | AOAO & HO-6",
        "desc": "Condo deductible assessment calculator: estimate your share of an AOAO master-policy deductible and what HO-6 loss assessment may pay.",
        "h1": "Condo Deductible Share Calculator for AOAO Owners",
        "lede": "High-rise and townhouse associations often carry large master-policy deductibles. Estimate how one could be passed to you and how much your HO-6 loss assessment coverage might absorb.",
        "markup": CONDO,
        "explain": """
<h2>Why this matters for island condo owners</h2>
<p>Condominium associations — called AOAOs in Hawaii — insure the building under a master policy. As premiums have climbed, many associations have accepted much larger deductibles, sometimes a percentage of the building’s insured value. When a loss hits, the association may pay the deductible from reserves or pass it to owners as a special assessment, depending on its declaration, bylaws and board decisions.</p>
<h2>How the calculator works</h2>
<ol><li><strong>Master deductible in dollars</strong> — the flat figure, or the percentage times the insured value.</li>
<li><strong>Association absorbs</strong> the smaller of the deductible and the loss. The master policy pays the rest.</li>
<li><strong>Your assessment</strong> is that absorbed amount times your share — either your common-interest percentage or your share of the units where the loss began.</li>
<li><strong>Your HO-6</strong> may pay the assessment above its own deductible, up to your loss assessment limit.</li></ol>
<div class="note"><b class="h">Check your documents</b>Allocation rules, reserves and HO-6 wording vary. This tool is illustrative. Ask the managing agent how the board intends to handle the deductible, and ask your agent whether your loss assessment coverage applies to deductible assessments.</div>
<h2>Where appraisal fits</h2>
<p>If the association and its insurer disagree on the amount of a covered building loss, the master policy’s appraisal clause may apply — and the result changes every owner’s assessment. See our <a href="/appraisal-specialties/condo-aoao-commercial-appraisal/">condo and AOAO appraisal</a> page and the guide to <a href="/hawaii-claim-guides/condo-master-policy-vs-ho6/">master policies versus HO-6</a>.</p>
""",
        "faqs": [("What is a common-interest percentage?", "It is each unit’s fractional share of the common elements, listed in the condominium declaration. Associations often use it to divide shared expenses."), ("Does every HO-6 cover deductible assessments?", "Not always. Some policies limit loss assessment coverage for deductibles or cap it at a low amount, so check the endorsement with your agent.")],
    },
]
