"""Interactive claim tools: markup + explanatory copy. Logic lives in static/assets/js/app.js.
Every tool runs in the browser; nothing is sent or stored."""

T = "/claim-toolbox/"

GAP_FULL = """
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Claim gap &amp; net recovery estimator</span><i>Runs in your browser</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Insurer’s estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="22600"><span class="hint">Replacement cost total on the carrier’s estimate.</span></div>
        <div><label for="g-own">Your estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="38900"><span class="hint">Your contractor’s or independent estimate.</span></div>
      </div>
      <div><label for="g-land">Where might the award land inside the gap?</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% means the carrier’s number holds. 100% means your full number is awarded.</span></div>
      <div class="row2">
        <div><label for="g-ft">Your appraiser’s fee type</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of increase (%)</option><option value="hourly">Hourly (hours × rate)</option></select></div>
        <div><label for="g-fee">Fee amount, % or hours</label><input id="g-fee" name="fee" inputmode="decimal" value="2800"></div>
      </div>
      <div class="row2">
        <div><label for="g-rate">Hourly rate (if hourly)</label><input id="g-rate" name="rate" inputmode="decimal" value="175"></div>
        <div><label for="g-ump">Umpire’s total fee</label><input id="g-ump" name="umpire" inputmode="decimal" value="3500"></div>
      </div>
      <label class="check"><input type="checkbox" name="useump" checked> <span>An umpire will be needed (you pay half)</span></label>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated net increase to you</small><b data-o="net">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s-a"></span><span class="s-b"></span><span class="s-c"></span></div>
      <div class="legend"><span><i class="s-a"></i>Carrier’s number</span><span><i class="s-b"></i>Your net gain</span><span><i class="s-c"></i>Appraisal costs</span></div>
      <div class="out-rows">
        <div><span>Amount in dispute</span><b data-o="gap">$0</b></div>
        <div><span>Gap as % of carrier estimate</span><b data-o="pct">—</b></div>
        <div><span>Projected award (RCV)</span><b data-o="award">$0</b></div>
        <div><span>Gross increase</span><b data-o="gain">$0</b></div>
        <div><span>Your appraisal costs</span><b data-o="cost">$0</b></div>
      </div>
      <div class="scen"><p class="todo-h">Net at three outcomes</p>
        <div class="scen-row"><span>Cautious (30%)</span><b data-o="s30">$0</b></div>
        <div class="scen-row"><span>Middle (55%)</span><b data-o="s55">$0</b></div>
        <div class="scen-row"><span>Strong (80%)</span><b data-o="s80">$0</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

GAP_MINI = """
<div class="tool" data-tool="gap" style="margin:0">
  <div class="tool-head"><span>60-second gap check</span><i>No sign-up</i></div>
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
  <div class="tool-head"><span>ACV &amp; holdback calculator</span><i>Add as many line items as you need</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Architectural shingle roof", 21400, 11, 30), ("Kitchen ceiling & walls (plaster)", 3900, 20, 50), ("Oak flooring, first floor", 9600, 15, 50), ("Interior paint", 2700, 5, 10)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn ghost small" data-add data-run>+ Add line item</button></div>
      <div class="row3">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="1500"></div>
        <div><label for="d-cap">Depreciation cap</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="90">90%</option></select></div>
        <div><label for="d-lab">Labor share not depreciated</label><select id="d-lab" name="labor"><option value="0" selected>None (depreciate all)</option><option value="30">30% labor</option><option value="40">40% labor</option><option value="50">50% labor</option></select></div>
      </div>
      <p class="hint" style="margin:0">Some estimates depreciate only materials. The labor option shows how much that choice changes the first check.</p>
      <label class="check"><input type="checkbox" name="nonrec"> <span>My policy pays actual cash value only (no recoverable depreciation)</span></label>
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
  <div class="tool-head"><span>Roof pitch &amp; squares calculator</span><i>Check the carrier’s measurements</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <fieldset class="plain"><legend class="sr-only">Measurement method</legend>
        <div class="btn-row">
          <label class="check"><input type="radio" name="mode" value="dims" checked> <span>Footprint length × width</span></label>
          <label class="check"><input type="radio" name="mode" value="area"> <span>I know the footprint area</span></label>
        </div></fieldset>
      <div class="row2" data-mode="dims">
        <div><label for="r-l">Footprint length (ft)</label><input id="r-l" name="len" inputmode="decimal" value="44"></div>
        <div><label for="r-w">Footprint width (ft)</label><input id="r-w" name="wid" inputmode="decimal" value="28"></div>
      </div>
      <div data-mode="dims"><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="12"></div>
      <div data-mode="area" hidden><label for="r-a">Footprint area incl. overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="1450"></div>
      <div class="row2">
        <div><label for="r-p">Roof pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 8 else "", p) for p in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 18]) + """</select></div>
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="10">10% · simple gable</option><option value="13" selected>13% · gable with dormers</option><option value="15">15% · hip roof</option><option value="18">18% · complex roof</option></select></div>
      </div>
      <div class="row2">
        <div><label for="r-ly">Existing layers to tear off</label><select id="r-ly" name="layers"><option value="1">1 layer</option><option value="2" selected>2 layers</option><option value="3">3 layers</option></select><span class="hint">Older New Jersey homes often have two.</span></div>
        <div><label for="r-pr">Installed price per square (optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 640"></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Roof squares (before waste)</small><b data-o="sq">0</b></div>
      <div class="out-rows">
        <div><span>Pitch multiplier</span><b data-o="mult">1.000</b></div>
        <div><span>Roof surface area</span><b data-o="surface">0</b></div>
        <div><span>Squares to order (with waste)</span><b data-o="order">0</b></div>
        <div><span>Shingle bundles (3 per square)</span><b data-o="bundles">0</b></div>
        <div><span>Tear-off squares (all layers)</span><b data-o="tear">0</b></div>
        <div><span>Rough replacement cost</span><b data-o="cost">—</b></div>
      </div>
      <p class="out-msg" data-o="steep"></p>
    </div>
  </div>
</div>"""

DEDUCT = """
<div class="tool" data-tool="deduct">
  <div class="tool-head"><span>Hurricane &amp; windstorm deductible calculator</span><i>Percentage vs. flat</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling coverage (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="465000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Hurricane / windstorm deductible</label><select id="w-p" name="pct"><option value="1">1%</option><option value="2" selected>2%</option><option value="3">3%</option><option value="5">5%</option><option value="10">10%</option></select></div>
        <div><label for="w-min">Minimum dollar amount (if any)</label><input id="w-min" name="min" inputmode="decimal" value="2500"></div>
      </div>
      <div class="row2">
        <div><label for="w-f">All-other-perils deductible</label><input id="w-f" name="flat" inputmode="decimal" value="1000"></div>
        <div><label for="w-l">Estimated storm damage</label><input id="w-l" name="loss" inputmode="decimal" value="27800"></div>
      </div>
      <fieldset class="plain"><legend>Does the hurricane deductible apply to this storm?</legend>
        <div class="btn-row">
          <label class="check"><input type="radio" name="trig" value="yes" checked> <span>Yes, the trigger was met</span></label>
          <label class="check"><input type="radio" name="trig" value="no"> <span>No, it was a nor’easter or the trigger wasn’t met</span></label>
        </div></fieldset>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Deductible that applies</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s-c"></span><span class="s-a"></span></div>
      <div class="legend"><span><i class="s-c"></i>You pay</span><span><i class="s-a"></i>Policy pays</span></div>
      <div class="out-rows">
        <div><span>Hurricane deductible in dollars</span><b data-o="hd">$0</b></div>
        <div><span>Payment with hurricane deductible</span><b data-o="pdpay">$0</b></div>
        <div><span>Payment with the flat deductible</span><b data-o="flatpay">$0</b></div>
        <div><span>Difference the trigger makes</span><b data-o="diff">$0</b></div>
      </div>
      <p class="out-msg" data-o="below"></p>
    </div>
  </div>
</div>"""

DATES = """
<div class="tool" data-tool="dates">
  <div class="tool-head"><span>Claim calendar builder</span><i>Exports an .ics file</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
        <div><label for="t-ad">Appraisal demand date (optional)</label><input id="t-ad" type="date" name="dem"></div>
      </div>
      <p class="hint" style="margin:0">Change each window to match your policy. The defaults are common figures, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report the claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="3"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="10"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Often counted from the carrier’s request.</span></div>
        <div><label for="t-r">Replacement cost claim notice (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="180"></div>
        <div><label for="t-s">Suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="365"><span class="hint">Many New Jersey policies say 12 months.</span></div>
        <div><label for="t-a">Name your appraiser within (days of demand)</label><input id="t-a" name="appr" inputmode="numeric" value="20"></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download .ics calendar file</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the insurer accepted coverage for at least part of the loss?", "Get written confirmation that coverage is accepted. If the claim was denied, talk to a New Jersey attorney before considering appraisal."),
    (3, "Do you have the carrier’s full, itemized estimate?", "Ask in writing for the complete line-item estimate, not just the payment summary."),
    (3, "Do you have your own itemized estimate?", "Get a line-item estimate from a contractor or estimator. A one-line bid won’t hold up in front of a panel."),
    (2, "Do you have dated photos taken soon after the loss?", "Gather every photo and note when each was taken. Add photos of current conditions."),
    (2, "Have you read the appraisal paragraph in your policy?", "Find ‘Appraisal’ in the conditions section and note the deadlines for naming an appraiser."),
    (2, "Do you know your suit-limitation date?", "Find the ‘Suit Against Us’ clause and put the date on your calendar. The claim calendar builder can help."),
    (2, "If wind and flood both hit the property, are the two claims separated?", "List which damage you’re claiming under each policy so nothing is counted twice or missed."),
    (2, "Have temporary repairs been made and receipts saved?", "Make reasonable temporary repairs, such as tarps or drying, and keep every receipt."),
    (2, "Has hidden damage been opened up and documented?", "Make sure wet walls, attics and roof decking have been checked so the scope is complete."),
    (1, "Do you have your current declarations page?", "Download or request your declarations page, including all deductible endorsements."),
    (2, "Is the gap more than about 10% or $5,000?", "Run the claim gap estimator. A small gap may not justify appraisal costs."),
    (1, "Has a sworn proof of loss been sent if the carrier asked for one?", "If a proof of loss was requested, send it on time and keep a copy."),
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
    <div class="tool-out ready-out" aria-live="polite">
      <div>
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#efe6d3" stroke-width="18"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#FFCA66" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3" style="transition:stroke-dashoffset .5s,stroke .3s"/></svg>
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

TREE = """
<div class="tool" data-tool="tree">
  <div class="tool-head"><span>Fallen tree coverage calculator</span><i>Debris limits vs. structure damage</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="tr-n">Trees down on the property</label><input id="tr-n" name="trees" inputmode="numeric" value="3"></div>
        <div><label for="tr-h">How many hit a covered structure or blocked the driveway?</label><input id="tr-h" name="hit" inputmode="numeric" value="1"></div>
      </div>
      <div class="row2">
        <div><label for="tr-c">Average cost to remove & haul each tree</label><input id="tr-c" name="cost" inputmode="decimal" value="1800"></div>
        <div><label for="tr-s">Structure repair estimate (roof, framing, interior)</label><input id="tr-s" name="struct" inputmode="decimal" value="24500"></div>
      </div>
      <div class="row3">
        <div><label for="tr-pt">Debris limit per tree</label><input id="tr-pt" name="per" inputmode="decimal" value="500"></div>
        <div><label for="tr-po">Debris limit per storm</label><input id="tr-po" name="occ" inputmode="decimal" value="1000"></div>
        <div><label for="tr-d">Deductible</label><input id="tr-d" name="ded" inputmode="decimal" value="1000"></div>
      </div>
      <label class="check"><input type="checkbox" name="all" > <span>My policy pays debris removal for every fallen tree, not only ones that hit something</span></label>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated policy payment</small><b data-o="pay">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s-a"></span><span class="s-b"></span><span class="s-c"></span></div>
      <div class="legend"><span><i class="s-a"></i>Structure</span><span><i class="s-b"></i>Tree debris covered</span><span><i class="s-c"></i>You pay</span></div>
      <div class="out-rows">
        <div><span>Trees eligible for debris coverage</span><b data-o="elig">0</b></div>
        <div><span>Tree removal cost (all trees)</span><b data-o="rem">$0</b></div>
        <div><span>Debris removal covered</span><b data-o="cov">$0</b></div>
        <div><span>Tree removal you pay</span><b data-o="oop">$0</b></div>
        <div><span>Structure claim after deductible</span><b data-o="snet">$0</b></div>
      </div>
      <p class="out-msg" data-o="tmsg"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "claim-gap-net-recovery-estimator", "name": "Claim Gap & Net Recovery Estimator", "icon": "Δ", "kind": "Estimator",
        "short": "Compare two estimates, project an award and subtract appraiser and umpire fees to see your net.",
        "title": "Claim Gap & Net Recovery Estimator | Appraisal Math",
        "desc": "Free estimator: compare your estimate with the insurer’s, project an appraisal award and subtract fees to see your net at three outcomes.",
        "h1": "Claim Gap and Net Recovery Estimator",
        "lede": "Enter the carrier’s number and yours, pick where an award might land, and add realistic fees. The estimator shows your net at a cautious, middle and strong outcome so you can judge whether appraisal pays.",
        "markup": GAP_FULL,
        "explain": f"""
<h2>How to use it</h2>
<ol><li><strong>Enter the insurer’s RCV total</strong>, the replacement cost figure before depreciation and deductible.</li>
<li><strong>Enter your estimate</strong> at replacement cost too, so you compare like with like.</li>
<li><strong>Pick a fee arrangement.</strong> Flat, percentage and hourly fees are all common. Use the terms you’ve actually been quoted.</li>
<li><strong>Read the three outcomes.</strong> If appraisal only pays off at the strong outcome, the case is fragile.</li></ol>
<h2>Example figures</h2>
<p>The starting numbers are illustrative only. They don’t come from any real claim or client.</p>
<h2>What the estimator leaves out</h2>
<p>Deductibles, depreciation timing and policy limits affect what you’re paid, not the size of the dispute. For holdback math, use the <a href="{T}acv-holdback-calculator/">ACV &amp; holdback calculator</a>.</p>
""",
        "faqs": [("Is the projected award a prediction?", "No. It’s a planning scenario. Real awards depend on documentation, the panel and the policy."), ("Why show three outcomes?", "Awards rarely match either side’s opening number. Looking at a range shows whether appraisal still makes sense if the panel accepts only part of your estimate.")],
    },
    {
        "slug": "acv-holdback-calculator", "name": "ACV & Holdback Calculator", "icon": "ACV", "kind": "Calculator",
        "short": "Estimate the first ACV check, the depreciation held back and the total after repairs, with a labor option.",
        "title": "ACV & Holdback Calculator | RCV vs ACV Payments",
        "desc": "Free RCV vs ACV calculator: list items with age and life to estimate your first check, depreciation holdback and total, with a labor option.",
        "h1": "ACV and Depreciation Holdback Calculator",
        "lede": "Replacement cost policies usually pay in two steps: an actual cash value check now and the held-back depreciation after repairs. Enter your line items to see the split, and test whether labor is being depreciated.",
        "markup": DEP,
        "explain": f"""
<h2>How depreciation is figured here</h2>
<p>The tool uses straight-line depreciation, age divided by expected life, up to the cap you choose. If you select a labor share, that part of each line isn’t depreciated, which is how some estimates treat labor. Real estimates may use different life spans, condition adjustments or items that aren’t depreciated at all, such as permits.</p>
<h2>Common life spans in estimates</h2>
<div class="table-wrap"><table><thead><tr><th>Item</th><th>Common range</th></tr></thead><tbody>
<tr><th>Architectural shingles</th><td>25–30 years</td></tr><tr><th>Slate roofing</th><td>60–100+ years</td></tr><tr><th>Plaster walls</th><td>50+ years</td></tr><tr><th>Hardwood flooring</th><td>50+ years (refinish cycles)</td></tr><tr><th>Interior paint</th><td>8–12 years</td></tr><tr><th>Vinyl siding</th><td>30–40 years</td></tr>
</tbody></table></div>
<h2>Getting the holdback released</h2>
<p>Many policies require you to repair within a set time, or to notify the insurer that you intend to claim replacement cost, before depreciation is paid. The <a href="{T}claim-calendar-builder/">claim calendar builder</a> can remind you before that window closes.</p>
""",
        "faqs": [("Should labor be depreciated in New Jersey?", "Practice varies by policy and carrier. Ask the insurer to explain in writing whether labor was depreciated, and check the estimate line by line."), ("What if I don’t repair?", "Under most replacement cost policies you keep the ACV payment but may not recover the held-back depreciation.")],
    },
    {
        "slug": "roof-pitch-squares-calculator", "name": "Roof Pitch & Squares Calculator", "icon": "▲", "kind": "Calculator",
        "short": "Turn a footprint into true roof squares using pitch, waste and tear-off layers.",
        "title": "Roof Pitch & Squares Calculator for Roof Claims",
        "desc": "Calculate roof squares from footprint, pitch and waste, plus tear-off for multiple layers, then compare your result with the insurance estimate.",
        "h1": "Roof Pitch and Squares Calculator for Insurance Claims",
        "lede": "Measurement and tear-off mistakes are among the most common reasons New Jersey roof claims come up short. Use the footprint, pitch and number of layers to estimate what the carrier should be pricing.",
        "markup": ROOF,
        "explain": """
<h2>The math behind it</h2>
<p>A roof is larger than the footprint underneath it, and the gap grows with pitch. The pitch multiplier is √(1 + (rise ÷ 12)²). An 8/12 roof is about 20% larger than its footprint. A 12/12 roof is about 41% larger.</p>
<h2>Checking the carrier’s roof section</h2>
<ul><li>Compare total squares and the waste percentage with your result. Differences over 5–10% are worth a closer look.</li>
<li>Check that tear-off includes every existing layer. Older homes often have two.</li>
<li>Look for steep charges, usually from 7/12 or 8/12 up, and high-roof charges on two-story sections.</li>
<li>Confirm starter, ridge, drip edge, ice barrier at the eaves and ventilation are listed.</li></ul>
<h2>Limits of a footprint estimate</h2>
<p>Roofs with several pitches, dormers and valleys need to be measured plane by plane. Treat this as a check, not a substitute for a field or aerial measurement.</p>
""",
        "faqs": [("What is a roofing square?", "100 square feet of roof surface. Many New Jersey colonials and split-levels have roughly 18 to 35 squares."), ("Why does the number of layers matter?", "Each existing layer must be removed and disposed of before the new roof goes on. Missing tear-off is a common gap in roof estimates.")],
    },
    {
        "slug": "hurricane-deductible-calculator", "name": "Hurricane Deductible Calculator", "icon": "%", "kind": "Calculator",
        "short": "See your hurricane or windstorm deductible in dollars, and what changes if the trigger isn’t met.",
        "title": "Hurricane Deductible Calculator for NJ Homeowners",
        "desc": "Turn a percentage hurricane or windstorm deductible into dollars, apply any minimum, and see what changes when the hurricane trigger isn’t met.",
        "h1": "Hurricane and Windstorm Deductible Calculator",
        "lede": "A 2% hurricane deductible on a $465,000 home is $9,300, not $1,000. See your deductible in real dollars and compare what a claim pays when the hurricane trigger is met and when it isn’t.",
        "markup": DEDUCT,
        "explain": """
<h2>Why the trigger matters in New Jersey</h2>
<p>Hurricane deductibles usually apply only when the policy’s trigger language is met, for example a hurricane warning issued for New Jersey or a storm officially classed as a hurricane. After Superstorm Sandy in 2012, the state said hurricane deductibles should not apply because Sandy wasn’t a hurricane when it came ashore. Nor’easters usually fall under the ordinary deductible unless your policy uses a broader windstorm deductible.</p>
<h2>Where to find yours</h2>
<p>Look on the declarations page for “hurricane,” “windstorm” or “named storm” deductible, then find the endorsement that defines it. Note any minimum dollar amount.</p>
<h2>What it means for appraisal</h2>
<p>The deductible doesn’t change the amount of loss a panel decides. It changes what you receive. A loss just above the deductible may not be worth disputing. One far above it may be.</p>
""",
        "faqs": [("Does the percentage apply to my contents too?", "The percentage is usually calculated from the dwelling limit and then applied to the whole storm loss. Check your policy’s wording."), ("Can I lower my hurricane deductible?", "Sometimes, at renewal, for a higher premium. Coastal homes may have fewer options.")],
    },
    {
        "slug": "claim-calendar-builder", "name": "Claim Calendar Builder", "icon": "◷", "kind": "Planner",
        "short": "Map notice, proof of loss, replacement cost, appraisal and suit dates, then export them to your calendar.",
        "title": "NJ Insurance Claim Calendar Builder | .ics Export",
        "desc": "Enter your date of loss and appraisal demand to map proof of loss, appraisal and suit dates for a New Jersey claim, then export an .ics file.",
        "h1": "New Jersey Claim Calendar Builder",
        "lede": "Policy deadlines keep running while you argue about a number. Enter your date of loss, and the appraisal demand date if there is one, to build a timeline you can download to any calendar.",
        "markup": DATES,
        "explain": """
<h2>Deadlines worth tracking</h2>
<ul><li><strong>Prompt notice.</strong> Report losses as soon as you can. Late notice is a common defense.</li>
<li><strong>Proof of loss.</strong> If the carrier asks for a sworn proof of loss, many policies give 60 days.</li>
<li><strong>Replacement cost.</strong> Some forms require you to tell the insurer within 180 days that you plan to claim replacement cost.</li>
<li><strong>Appraisal.</strong> Under language based on the standard fire policy, each side commonly names its appraiser within 20 days of a demand, and the appraisers have 15 days to agree on an umpire.</li>
<li><strong>Suit limitation.</strong> Many New Jersey property policies limit suits to 12 months from the loss. New Jersey courts have allowed that period to pause while a claim is under review, but don’t rely on that without an attorney’s advice.</li></ul>
<div class="note"><b class="h">Important</b>The planner uses the numbers you enter. It isn’t legal advice. If a deadline is close, talk to a New Jersey attorney.</div>
""",
        "faqs": [("Is the date of loss the day I noticed the damage?", "Usually it’s the date the storm or event happened. Weather records for your address can help pin it down."), ("Does the .ics file send my information anywhere?", "No. The file is created in your browser and saved to your device.")],
    },
    {
        "slug": "appraisal-readiness-checkup", "name": "Appraisal Readiness Checkup", "icon": "✓", "kind": "Checklist",
        "short": "Twelve yes/no questions that score your file and build a to-do list before you demand appraisal.",
        "title": "Appraisal Readiness Checkup | Is Your Claim Ready?",
        "desc": "Twelve questions that score how ready your New Jersey property claim is for appraisal, with a personal to-do list of what to fix first.",
        "h1": "Appraisal Readiness Checkup for Your Claim File",
        "lede": "Strong appraisals are mostly won before they start. Answer twelve quick questions, including one about wind-and-flood splits, to see where your file stands and what to fix first.",
        "markup": READY,
        "explain": """
<h2>How the score is weighted</h2>
<p>Coverage, estimates and evidence carry the most weight, because they decide whether appraisal is the right tool and how well your number will hold up. Paperwork such as the declarations page matters but is easy to fix.</p>
<h2>Reading your result</h2>
<ul><li><strong>75 and up:</strong> your file is in good shape. A professional review of the gap is the next step.</li>
<li><strong>45 to 74:</strong> close the open items first. Each one strengthens your position.</li>
<li><strong>Below 45:</strong> demanding appraisal now could lock in a low number. Build the file first.</li></ul>
""",
        "faqs": [("Is anything I answer saved?", "No. The checkup runs entirely in your browser and nothing is stored or sent."), ("Can I share the result?", "Yes. Take a screenshot or copy your to-do list and bring it to a consultation.")],
    },
    {
        "slug": "fallen-tree-coverage-calculator", "name": "Fallen Tree Coverage Calculator", "icon": "TR", "kind": "Calculator",
        "short": "See how per-tree and per-storm debris limits split tree removal costs from structure damage.",
        "title": "Fallen Tree Coverage Calculator | Debris Limits",
        "desc": "Free calculator for fallen tree claims: apply per-tree and per-storm debris limits, separate structure damage and see what you’d pay yourself.",
        "h1": "Fallen Tree Coverage Calculator",
        "lede": "After a nor’easter or ice storm, the tree on your roof and the trees across your yard are handled very differently. Enter your trees, removal costs and policy limits to see what’s likely covered.",
        "markup": TREE,
        "explain": """
<h2>How fallen trees are usually covered</h2>
<p>Damage to the house, garage or fence is part of the dwelling or other-structures claim, and removing the tree from the structure is usually part of that repair. Hauling trees away from the yard is debris removal, which many homeowners forms limit to about $500 per tree and $1,000 per storm, often only for trees that hit a covered structure or blocked a driveway. Some forms are broader. Check yours.</p>
<h2>What this calculator assumes</h2>
<ul><li>The structure repair estimate includes removing the tree from the structure.</li>
<li>Debris limits apply to hauling each eligible tree away, up to the per-tree and per-storm caps.</li>
<li>The deductible is applied once, to the structure claim.</li></ul>
<h2>Example figures</h2>
<p>The starting numbers are illustrative only. Real limits and deductibles depend on your policy.</p>
""",
        "faqs": [("Why was most of my tree removal bill not covered?", "Debris removal limits are small compared with the cost of removing large trees. Trees that hit nothing may not be covered at all under some policies."), ("Does the per-storm limit include the tree on my roof?", "Usually not, if removing it is part of repairing the structure. How your carrier applies the limit is worth asking in writing.")],
    },
]
