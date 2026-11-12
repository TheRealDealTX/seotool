"""Free claim calculators: markup + explanatory copy. The math lives in static/assets/js/app.js."""

B = "/appraisal-calculators/"

GAP_FULL = """
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Claim gap &amp; fee estimator</span><i>Private · runs in your browser</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Carrier’s estimate (RCV total)</label><input id="g-ins" name="insurer" inputmode="decimal" value="22600"><span class="hint">Replacement cost before depreciation and deductible.</span></div>
        <div><label for="g-own">Your contractor’s estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="37900"><span class="hint">A line-item estimate, not a lump-sum bid.</span></div>
      </div>
      <div><label for="g-land">Scenario: where the award lands inside the gap</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% means the carrier’s figure stands; 100% means your whole figure is awarded. Test several values.</span></div>
      <div class="row2">
        <div><label for="g-ft">How your appraiser charges</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of the increase (%)</option></select></div>
        <div><label for="g-fee">Fee amount</label><input id="g-fee" name="fee" inputmode="decimal" value="3000"></div>
      </div>
      <label class="check"><input type="checkbox" name="useump" checked> Add my half of an umpire’s fee</label>
      <div><label for="g-ump">Umpire’s total fee (shared 50/50)</label><input id="g-ump" name="umpire" inputmode="decimal" value="3500"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Illustrative net increase after costs</small><b data-o="net">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s1"></span><span class="s2"></span><span class="s3"></span></div>
      <div class="legend"><span><i class="s1"></i>Carrier’s figure</span><span><i class="s2"></i>Your net gain</span><span><i class="s3"></i>Appraisal costs</span></div>
      <div class="out-rows">
        <div><span>Amount in dispute</span><b data-o="gap">$0</b></div>
        <div><span>Dispute as % of carrier figure</span><b data-o="pct">—</b></div>
        <div><span>Scenario award (RCV)</span><b data-o="award">$0</b></div>
        <div><span>Gross increase</span><b data-o="gain">$0</b></div>
        <div><span>Your appraisal costs</span><b data-o="cost">$0</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

GAP_MINI = """
<div class="tool tool-mini" data-tool="gap">
  <div class="tool-head"><span>Two-number gap check</span><i>No sign-up</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="m-ins">Carrier’s estimate</label><input id="m-ins" name="insurer" inputmode="decimal" value="16800"></div>
      <div><label for="m-own">Your contractor’s estimate</label><input id="m-own" name="yours" inputmode="decimal" value="29400"></div>
      <div><label for="m-land">Scenario award lands at</label><div class="range"><input id="m-land" type="range" name="land" min="0" max="100" step="5" value="50" data-unit="%"><output>50%</output></div><span class="hint">of the disputed amount</span></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Amount in dispute</small><b data-o="gap">$0</b></div>
      <div class="out-rows">
        <div><span>Dispute vs. carrier figure</span><b data-o="pct">—</b></div>
        <div><span>Scenario award</span><b data-o="award">$0</b></div>
        <div><span>Increase before fees</span><b data-o="gain">$0</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

_DEP_ROW = """<tr><td><input name="item" value="{0}" aria-label="Item"></td><td><input name="rcv" inputmode="decimal" value="{1}" aria-label="Replacement cost"></td><td><input name="age" inputmode="decimal" value="{2}" aria-label="Age in years"></td><td><input name="life" inputmode="decimal" value="{3}" aria-label="Expected life in years"></td><td class="mono" data-o="row">$0</td><td><button type="button" class="x" aria-label="Remove row">×</button></td></tr>"""

DEP = """
<div class="tool tool-wide" data-tool="dep">
  <div class="tool-head"><span>RCV / ACV &amp; holdback worksheet</span><i>Add a row for each damaged item</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Low-slope membrane roof (rowhouse)", 14200, 11, 20), ("Plaster repair &amp; repaint — 2 rooms", 3600, 6, 12), ("Hardwood refinish — hallway", 2250, 8, 25)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn line small" data-add data-run>+ Add a row</button></div>
      <div class="row2">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="1500"></div>
        <div><label for="d-cap">Depreciation cap</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="90">90%</option></select><span class="hint">Many estimates cap depreciation per line; check yours.</span></div>
      </div>
      <label class="check"><input type="checkbox" name="nonrec"> My policy pays actual cash value only (nothing is held back for later)</label>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-trio">
        <div class="out-big"><small>First payment (ACV − deductible)</small><b data-o="first">$0</b></div>
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
  <div class="tool-head"><span>Roof square &amp; pitch calculator</span><i>Check the carrier’s roof math</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <fieldset class="bare"><legend class="sr-only">Measurement method</legend>
        <div class="btn-row">
          <label class="check"><input type="radio" name="mode" value="dims" checked> Footprint length × width</label>
          <label class="check"><input type="radio" name="mode" value="area"> I know the footprint area</label>
        </div></fieldset>
      <div class="row2" data-mode="dims">
        <div><label for="r-l">Footprint length (ft)</label><input id="r-l" name="len" inputmode="decimal" value="48"></div>
        <div><label for="r-w">Footprint width (ft)</label><input id="r-w" name="wid" inputmode="decimal" value="30"></div>
      </div>
      <div data-mode="dims"><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="12"></div>
      <div data-mode="area" hidden><label for="r-a">Footprint area incl. overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="1650"></div>
      <div class="row2">
        <div><label for="r-p">Roof pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 8 else "", p) for p in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18]) + """</select><span class="hint">Rowhouse membrane roofs are often 1/12 or less.</span></div>
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="5">5% — low-slope membrane</option><option value="10">10% — simple gable</option><option value="13" selected>13% — gable with dormers</option><option value="15">15% — hip roof</option><option value="18">18% — cut-up / turrets</option></select></div>
      </div>
      <div><label for="r-pr">Installed price per square (optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 575"><span class="hint">Use a local contractor’s quote for a rough figure.</span></div>
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
  <div class="tool-head"><span>Hurricane deductible calculator</span><i>Percentage vs. flat</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling limit (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="425000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Hurricane / named-storm deductible</label><select id="w-p" name="pct"><option value="1">1%</option><option value="2" selected>2%</option><option value="3">3%</option><option value="5">5%</option><option value="10">10%</option></select></div>
        <div><label for="w-f">All-other-perils deductible ($)</label><input id="w-f" name="flat" inputmode="decimal" value="1000"></div>
      </div>
      <div><label for="w-l">Estimated storm damage ($)</label><input id="w-l" name="loss" inputmode="decimal" value="18750"></div>
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
  <div class="tool-head"><span>Claim timeline planner</span><i>Exports an .ics calendar file</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
      <p class="hint">Set each window to match your own policy and letters. Defaults are common figures, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report the claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="2"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="10"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Often counted from the insurer’s request.</span></div>
        <div><label for="t-r">Recover depreciation (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="365"></div>
        <div><label for="t-s">Time to sue (days)</label><input id="t-s" name="suit" inputmode="numeric" value="1095"><span class="hint">Three years = 1,095 days. Confirm with an attorney.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download .ics calendar file</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the insurer accepted coverage for at least part of the loss?", "Get written confirmation that coverage is accepted. If the claim was denied, speak with a Maryland attorney before considering appraisal."),
    (3, "Do you have the insurer’s full, itemized estimate?", "Ask in writing for the complete line-item estimate, not just the summary page."),
    (3, "Do you have your own line-item estimate?", "Get an itemized estimate from a contractor or estimator — a one-line bid won’t carry weight with a panel."),
    (2, "Do you have dated photos taken soon after the loss?", "Collect every photo and video, note the dates, and add photos of current conditions."),
    (2, "Have you found and read the appraisal clause in your policy?", "Find the ‘Appraisal’ paragraph in the policy conditions and note any time limits it sets."),
    (2, "Do you know when your time to sue runs out?", "Find the ‘Suit Against Us’ condition and put the date on a calendar — the timeline planner can help."),
    (2, "Have temporary repairs been made and receipts saved?", "Make reasonable temporary repairs (tarps, drying, board-up) and keep every invoice."),
    (1, "Do you have the current declarations page?", "Download or request your current declarations page."),
    (2, "Has hidden damage been opened up and documented?", "Make sure wet walls, attics, decking and crawlspaces were inspected so the scope is complete."),
    (1, "Are your letters and emails with the insurer in date order?", "Gather all correspondence and claim notes into one dated file."),
    (2, "Is the gap more than roughly 10% or $5,000?", "Run the numbers in the claim gap & fee estimator — a small gap may not justify appraisal costs."),
    (1, "If the insurer asked for a sworn proof of loss, was it sent?", "If a proof of loss was requested, send it on time and keep proof of delivery."),
]

READY = """
<div class="tool tool-wide" data-tool="ready">
  <div class="tool-head"><span>Appraisal readiness checklist</span><i>12 questions · about two minutes</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <ol class="quiz">""" + "".join(
    '<li data-w="%d" data-fix="%s"><span>%s</span><span class="yn"><button type="button" class="yes" aria-pressed="false">Yes</button><button type="button" class="no" aria-pressed="false">No</button></span></li>' % (w, f, q)
    for w, q, f in _QUIZ) + """
      </ol>
      <div class="btn-row"><button type="button" class="btn line small" data-reset>Reset answers</button></div>
    </div>
    <div class="tool-out ready-out" aria-live="polite">
      <div>
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#e9e3cc" stroke-width="18"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#b39a45" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3" style="transition:stroke-dashoffset .5s,stroke .3s"/></svg>
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
  <div class="tool-head"><span>Snow &amp; ice roof load estimator</span><i>Illustrative — not an engineering check</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="s-d">Snow depth on the roof (inches)</label><input id="s-d" name="depth" inputmode="decimal" value="24"></div>
        <div><label for="s-t">Snow type</label><select id="s-t" name="dens"><option value="7">Fresh, powdery (~7 lb/ft³)</option><option value="15" selected>Settled (~15 lb/ft³)</option><option value="21">Wet or packed (~21 lb/ft³)</option></select></div>
      </div>
      <div class="row2">
        <div><label for="s-i">Ice layer (inches)</label><input id="s-i" name="ice" inputmode="decimal" value="1"><span class="hint">Ice weighs about 57 lb/ft³.</span></div>
        <div><label for="s-a">Roof area (sq ft, plan view)</label><input id="s-a" name="area" inputmode="decimal" value="1400"></div>
      </div>
      <div><label for="s-c">Reference roof snow load (psf)</label><select id="s-c" name="cap"><option value="20">20 psf — older or light framing</option><option value="25" selected>25 psf — common central/eastern figure</option><option value="30">30 psf</option><option value="40">40 psf</option><option value="60">60 psf — mountain-built framing</option></select><span class="hint">Your actual design load depends on code, age and framing. Ask an engineer or your local building office.</span></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated load on the roof</small><b data-o="psf">0 psf</b></div>
      <div class="stack" aria-hidden="true"><span class="s3"></span><span class="s1"></span></div>
      <div class="legend"><span><i class="s3"></i>Estimated load</span><span><i class="s1"></i>Remaining to reference load</span></div>
      <div class="out-rows">
        <div><span>Snow weight per sq ft</span><b data-o="snowpsf">0</b></div>
        <div><span>Ice weight per sq ft</span><b data-o="icepsf">0</b></div>
        <div><span>Total weight on the roof</span><b data-o="total">0 lb</b></div>
        <div><span>Share of reference load</span><b data-o="share">0%</b></div>
      </div>
      <p class="out-msg" data-o="snowmsg"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "claim-gap-fee-estimator", "name": "Claim Gap & Fee Estimator", "icon": "gap", "kind": "Estimator",
        "keyword": "insurance appraisal cost calculator",
        "short": "Size the dispute, test a scenario award and subtract appraiser and umpire fees to see a realistic net.",
        "title": "Insurance Appraisal Cost Calculator: Gap & Fees",
        "desc": "Free insurance appraisal cost calculator: compare two estimates, test where an award might land and subtract appraiser and umpire fees.",
        "h1": "Insurance Appraisal Cost Calculator: Claim Gap & Fee Estimator",
        "lede": "Enter the insurer’s estimate and your own, slide the scenario, and add the fees. The estimator shows whether appraisal is likely to leave you ahead once its costs are paid.",
        "markup": GAP_FULL,
        "explain": f"""
<h2>Reading the result</h2>
<p>The <strong>amount in dispute</strong> is simply your figure minus the insurer’s. The <strong>scenario award</strong> assumes the panel lands part of the way between the two. Subtract your appraiser’s fee and your half of the umpire and you get an illustrative <strong>net increase</strong>. None of these numbers is a prediction — they help you see whether appraisal makes economic sense at all.</p>
<h2>Stress-test the slider</h2>
<p>Run the estimator at 30%, 50% and 75%. If appraisal only pays off when you win nearly everything, the case is thin. If it still pays at 40%, it’s worth a conversation. Documented line items — measured roof slopes, matching problems, code items your county enforces — tend to hold up; round-number allowances tend to fall.</p>
<h2>What this tool doesn’t include</h2>
<ul><li>Deductibles, policy limits and sub-limits — they change what you’re paid, not the size of the dispute.</li><li>Depreciation timing — use the <a href="{B}rcv-acv-holdback-worksheet/">RCV / ACV &amp; holdback worksheet</a>.</li><li>Time and inconvenience, or interest.</li></ul>
""",
        "faqs": [("Is the scenario award a forecast?", "No. It’s a what-if. Real awards depend on the evidence, the appraisers and the umpire, and on your policy wording."),
                 ("Are appraiser fees in Maryland usually flat or a percentage?", "Both arrangements exist. Whatever the structure, ask for it in writing before you sign, and think about whether a contingent fee could be questioned under a ‘disinterested appraiser’ requirement in your policy.")],
    },
    {
        "slug": "rcv-acv-holdback-worksheet", "name": "RCV / ACV & Holdback Worksheet", "icon": "acv", "kind": "Worksheet",
        "keyword": "RCV ACV depreciation calculator",
        "short": "List damaged items with age and life expectancy to see the first payment, the holdback and the full RCV.",
        "title": "RCV vs ACV Depreciation Calculator & Holdback",
        "desc": "Free RCV vs ACV depreciation calculator: list items with age and life to estimate your first payment, recoverable holdback and full claim value.",
        "h1": "RCV vs. ACV Depreciation Calculator & Holdback Worksheet",
        "lede": "Most replacement-cost policies pay in two steps: actual cash value now, the rest once repairs are done. This worksheet shows how big each step is likely to be.",
        "markup": DEP,
        "explain": f"""
<h2>How the worksheet does the math</h2>
<p>For each row, depreciation is <em>age ÷ expected life</em> times the replacement cost, capped at the percentage you choose. ACV is replacement cost minus depreciation. Your first payment is total ACV minus the deductible; the difference between that and the full replacement cost (less deductible) is what’s typically held back until the work is complete.</p>
<h2>Where Maryland estimates get argued</h2>
<ul><li><strong>Low-slope rowhouse roofs</strong> — expected life assumptions for modified bitumen, TPO and coatings vary a lot, and so does depreciation.</li><li><strong>Labor depreciation</strong> — whether labor can be depreciated is a policy and legal question; flag it rather than assume.</li><li><strong>Plaster and older finishes</strong> — a 1910 plaster wall shouldn’t be depreciated as if it were 1990 drywall at the end of its life.</li></ul>
<p>If you want the size of the overall dispute rather than the payment schedule, try the <a href="{B}claim-gap-fee-estimator/">claim gap &amp; fee estimator</a>.</p>
""",
        "faqs": [("When do I get the held-back amount?", "Usually after repairs are complete and you send proof such as invoices. Your policy sets the time limit, so check it before you start work."),
                 ("Why is my depreciation higher than the worksheet shows?", "The carrier may be using different life expectancies, a higher cap or depreciating labor. Compare line by line; those choices are often negotiable or reviewable in appraisal.")],
    },
    {
        "slug": "roof-square-pitch-calculator", "name": "Roof Square & Pitch Calculator", "icon": "roof", "kind": "Calculator",
        "keyword": "roof squares calculator",
        "short": "Turn a footprint into true roof squares with pitch and waste, from flat rowhouse roofs to steep Victorians.",
        "title": "Roof Squares Calculator with Pitch & Waste",
        "desc": "Roof squares calculator for insurance claims: convert footprint, pitch and waste into true surface area, squares, bundles and a rough cost.",
        "h1": "Roof Squares Calculator for Maryland Roof Claims",
        "lede": "Roof claims are often argued in squares. Convert a simple footprint into true surface area with pitch and waste, then compare the result with the insurer’s diagram.",
        "markup": ROOF,
        "explain": f"""
<h2>Why pitch changes everything</h2>
<p>A roof square is 100 sq ft of actual roof surface. Steeper roofs have more surface than their footprint suggests: an 8/12 roof is about 20% larger than its plan area, a 12/12 roof about 41% larger. If an estimate was built from a satellite footprint without the right pitch, the square count — and every line tied to it — will be low.</p>
<h2>Waste factors in practice</h2>
<p>Waste covers the shingles cut away at hips, valleys and rakes. A simple gable might need 10%; a cut-up Queen Anne roof in Frederick or Hagerstown may need 18% or more. Flat membrane roofs on Baltimore rowhouses need far less. Check that the estimate’s waste matches the roof you actually have.</p>
<h2>Steep and high charges</h2>
<p>Most estimating platforms add steep-roof labor from about 7/12 and high-roof charges for two-story eaves. These lines are easy to miss. See our <a href="/property-claim-services/roof-hail-damage-appraisal/">roof &amp; hail damage appraisal</a> page for other common gaps.</p>
""",
        "faqs": [("How do I find my roof pitch?", "Measure the rise over 12 inches of run with a level and tape from the attic or at a gable end, or check aerial measurement reports. Don’t climb a roof to measure it."),
                 ("Does this replace a roof measurement report?", "No. It’s a reasonableness check. For appraisal, use a measured diagram or an aerial report.")],
    },
    {
        "slug": "hurricane-deductible-calculator", "name": "Hurricane Deductible Calculator", "icon": "pct", "kind": "Calculator",
        "keyword": "hurricane deductible calculator",
        "short": "Convert a percentage hurricane or named-storm deductible into dollars and compare it with a flat deductible.",
        "title": "Hurricane Deductible Calculator: % to Dollars",
        "desc": "Hurricane deductible calculator for Bay and coastal properties: turn a percentage deductible into dollars and see what a storm claim would pay.",
        "h1": "Hurricane Deductible Calculator for Bay & Coastal Homes",
        "lede": "Percentage deductibles are common near the Chesapeake Bay and the ocean. A 2% deductible sounds small until you multiply it by your dwelling limit.",
        "markup": DEDUCT,
        "explain": """
<h2>How a percentage deductible works</h2>
<p>A percentage deductible is calculated on your dwelling limit (Coverage A), not on the size of the loss. On an illustrative $425,000 limit, a 2% deductible is $8,500. If the storm damage is $18,750, the policy would pay about $10,250 — compared with $17,750 if a $1,000 flat deductible applied.</p>
<h2>When it applies</h2>
<p>Trigger language varies by insurer: some apply the percentage only to a named hurricane, some to any named storm, and some for a set period around a storm watch or warning. A nor’easter, a derecho or a summer thunderstorm usually falls under the regular deductible. Read the endorsement — and check whether the insurer applied the right one.</p>
<h2>Appraisal and deductibles</h2>
<p>Appraisal sets the amount of loss; the deductible is then applied according to the policy. If the loss is close to the deductible, small valuation differences decide whether anything is paid at all.</p>
""",
        "faqs": [("Can my insurer apply the hurricane deductible to a tropical storm?", "It depends on your endorsement’s trigger wording. Some forms apply to named storms of any strength; others only to hurricanes. Compare the wording with the official storm advisories for your date of loss."),
                 ("Is flood damage subject to this deductible?", "Flood is generally excluded from homeowners policies and covered separately, usually through the National Flood Insurance Program, with its own deductible.")],
    },
    {
        "slug": "claim-timeline-planner", "name": "Claim Timeline Planner", "icon": "cal", "kind": "Planner",
        "keyword": "insurance claim deadline calculator",
        "short": "Map notice, proof-of-loss, depreciation and time-to-sue dates from your date of loss, then export them.",
        "title": "Insurance Claim Deadline Calculator & Planner",
        "desc": "Enter your date of loss to map notice, proof of loss, depreciation recovery and suit dates for a Maryland property claim, then export to a calendar.",
        "h1": "Insurance Claim Deadline Calculator & Timeline Planner",
        "lede": "Missed dates sink more claims than bad estimates. Pick your date of loss, adjust each window to your policy, and download the milestones to your calendar.",
        "markup": DATES,
        "explain": """
<h2>The dates that matter</h2>
<ol><li><strong>Notice</strong> — policies require prompt notice. Treat it as days, not weeks.</li><li><strong>Mitigation</strong> — reasonable temporary repairs protect the property and the claim.</li><li><strong>Proof of loss</strong> — if requested, a sworn statement is usually due within a set number of days of the request.</li><li><strong>Depreciation recovery</strong> — replacement-cost policies set a window to finish repairs and claim the holdback.</li><li><strong>Time to sue</strong> — Maryland’s general contract limitations period is three years, and Maryland law generally doesn’t let property policies shorten it, but when the clock starts can be disputed. Ask a Maryland attorney.</li></ol>
<h2>Appraisal doesn’t pause the clock by itself</h2>
<p>Unless your policy or a written agreement says otherwise, invoking appraisal doesn’t necessarily stop other deadlines from running. Keep them on the calendar.</p>
<div class="note"><b class="h">Privacy</b>The calendar file is generated on your device. Nothing you enter is sent to us.</div>
""",
        "faqs": [("Do these defaults apply to my policy?", "They are common figures only. Your policy, endorsements and the insurer’s letters control. Change any value to match."),
                 ("What if a date has already passed?", "The planner flags past dates. Don’t assume the right is lost — speak with a Maryland attorney about your options.")],
    },
    {
        "slug": "appraisal-readiness-checklist", "name": "Appraisal Readiness Checklist", "icon": "check", "kind": "Checklist",
        "keyword": "insurance appraisal checklist",
        "short": "Twelve yes/no questions score your file and build a to-do list before you invoke appraisal.",
        "title": "Insurance Appraisal Checklist & Readiness Score",
        "desc": "A 12-question insurance appraisal checklist that scores how ready your property claim file is and builds a to-do list of gaps to close first.",
        "h1": "Insurance Appraisal Checklist: Is Your File Ready?",
        "lede": "An appraisal panel works from evidence. Answer twelve questions and see which documents and steps would make your file stronger before anyone signs a demand.",
        "markup": READY,
        "explain": f"""
<h2>Why readiness matters</h2>
<p>Once two of three panel members sign, the amount is set. A file with a full line-item estimate, dated photos and complete correspondence gives your appraiser something to argue from. A thin file invites a low award.</p>
<h2>How the score is weighted</h2>
<p>Coverage acceptance and the two estimates carry the most weight, because appraisal can’t work without them. Photos, policy deadlines and hidden-damage inspections come next. Housekeeping items count, but less.</p>
<p>When you’re done, run the <a href="{B}claim-timeline-planner/">claim timeline planner</a> so nothing lapses while you fill the gaps.</p>
""",
        "faqs": [("Is a high score a guarantee?", "No. It means your file has the pieces appraisal usually needs. The outcome still depends on the facts and the panel."),
                 ("Are my answers saved?", "No. The checklist runs in your browser and nothing is stored or sent.")],
    },
    {
        "slug": "snow-load-roof-estimator", "name": "Snow & Ice Roof Load Estimator", "icon": "snow", "kind": "Estimator",
        "keyword": "roof snow load calculator",
        "short": "Estimate how much snow and ice weigh on your roof after a big storm, compared with a reference design load.",
        "title": "Roof Snow Load Calculator for Maryland Winters",
        "desc": "Roof snow load calculator: estimate the weight of snow and ice on your roof in pounds per square foot and compare it with a reference design load.",
        "h1": "Roof Snow Load Calculator for Maryland Winter Storms",
        "lede": "After storms like the February 2010 blizzards, roof collapses and sagging ceilings followed the snow. Estimate the weight sitting on your roof — and know when to call a professional.",
        "markup": SNOW,
        "explain": f"""
<h2>How the estimate works</h2>
<p>Snow weight is depth (in feet) times density. Fresh powder can be under 10 lb/ft³; wet, settled snow can be twice that or more, and ice is about 57 lb/ft³. The estimator adds snow and ice to give pounds per square foot (psf), then compares the result with the reference load you choose. Two feet of settled snow is roughly 30 psf — already above a common 25 psf reference.</p>
<h2>Why Western Maryland is different</h2>
<p>Garrett and western Allegany counties see far more snow than the Bay counties, and buildings there are often framed for heavier loads. A lake cabin near Deep Creek and a 1950s rambler in Bowie can respond very differently to the same storm total.</p>
<div class="note"><b class="h">Safety first</b>This is an illustrative estimate, not an engineering assessment. Don’t climb onto a snow-covered roof. If you see sagging, new cracks or doors that suddenly stick, leave the area and call a contractor or structural engineer.</div>
<h2>When it becomes a claim</h2>
<p>Collapse, ice-dam leaks and burst pipes are frequent winter claims, and coverage often turns on policy wording about weight of snow and ice. See <a href="/property-claim-services/snow-ice-dam-freeze-appraisal/">snow, ice dam &amp; freeze appraisal</a> for how these losses are valued.</p>
""",
        "faqs": [("What design snow load does my house have?", "It depends on when and where it was built and how it was framed. Your county building office or a structural engineer can tell you; the reference values here are only illustrative."),
                 ("Does homeowners insurance cover roof collapse from snow?", "Many policies address collapse caused by the weight of snow or ice, but wording and exclusions vary. Read the collapse and ‘weight of ice, snow or sleet’ provisions and ask your insurer or an attorney.")],
    },
]
