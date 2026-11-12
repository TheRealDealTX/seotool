"""Free claim tools: markup + copy. Logic lives in static/assets/js/app.js (everything runs in the browser)."""

C_PINE, C_CLAY, C_SAGE = "#1f5136", "#d9683f", "#cfdcd2"

GAP_FULL = f"""
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Settlement gap estimator</span><i>Runs in your browser · nothing stored</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Carrier’s estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="22600"><span class="hint">Replacement cost total before depreciation.</span></div>
        <div><label for="g-own">Your estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="38900"><span class="hint">Contractor or independent estimate.</span></div>
      </div>
      <div><label for="g-land">Where might the award land inside the gap?</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% means the carrier’s number holds; 100% means your full number is awarded.</span></div>
      <div class="row2">
        <div><label for="g-ft">Appraiser fee structure</label><select id="g-ft" name="feetype"><option value="flat">Flat or hourly total ($)</option><option value="pct">Percent of the increase (%)</option></select></div>
        <div><label for="g-fee">Fee amount</label><input id="g-fee" name="fee" inputmode="decimal" value="3000"></div>
      </div>
      <label class="check"><input type="checkbox" name="useump" checked> Include my half of an umpire’s fee</label>
      <div><label for="g-ump">Umpire’s total fee</label><input id="g-ump" name="umpire" inputmode="decimal" value="3500"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated net gain after fees</small><b data-o="net">$0</b></div>
      <div class="stack" aria-hidden="true"><span style="background:{C_SAGE}"></span><span style="background:{C_PINE}"></span><span style="background:{C_CLAY}"></span></div>
      <div class="legend"><span><i style="background:{C_SAGE}"></i>Carrier’s number</span><span><i style="background:{C_PINE}"></i>Your net gain</span><span><i style="background:{C_CLAY}"></i>Appraisal costs</span></div>
      <div class="out-rows">
        <div><span>Amount in dispute</span><b data-o="gap">$0</b></div>
        <div><span>Gap as share of carrier estimate</span><b data-o="pct">—</b></div>
        <div><span>Projected award (RCV)</span><b data-o="award">$0</b></div>
        <div><span>Your appraisal costs</span><b data-o="cost">$0</b></div>
      </div>
      <p class="todo-h">Net gain at three outcomes</p>
      <div class="scen"><div><small>Award at 30%</small><b data-o="s30">$0</b></div><div><small>Award at 50%</small><b data-o="s50">$0</b></div><div><small>Award at 80%</small><b data-o="s80">$0</b></div></div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

GAP_MINI = f"""
<div class="tool" data-tool="gap" style="margin:0">
  <div class="tool-head"><span>60-second gap check</span><i>Illustrative · no sign-up</i></div>
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
  <div class="tool-head"><span>RCV / ACV holdback calculator</span><i>Add a row for each item</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Dimensional shingle roof", 21400, 11, 30), ("Vinyl siding, two elevations", 6800, 14, 35), ("Hardwood floor refinish", 3900, 8, 25), ("Interior paint", 2100, 5, 10)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn ghost small" data-add data-run>+ Add item</button></div>
      <div class="row2">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="1500"></div>
        <div><label for="d-cap">Depreciation cap</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="90">90%</option></select><span class="hint">Many estimates cap depreciation; check yours.</span></div>
      </div>
      <label class="check"><input type="checkbox" name="nonrec"> My policy settles at actual cash value only (no holdback is recoverable)</label>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-trio">
        <div class="out-big"><small>First payment (ACV − deductible)</small><b data-o="first">$0</b></div>
        <div class="out-big"><small>Held back until repairs</small><b data-o="held">$0</b></div>
        <div class="out-big"><small>Total once recovered</small><b data-o="total">$0</b></div>
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
  <div class="tool-head"><span>Roof area &amp; pitch estimator</span><i>Check the carrier’s squares</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <fieldset class="bare"><legend class="sr-only">Measurement method</legend>
        <div class="btn-row">
          <label class="check"><input type="radio" name="mode" value="dims" checked> Length × width</label>
          <label class="check"><input type="radio" name="mode" value="area"> I know the footprint area</label>
        </div></fieldset>
      <div class="row2" data-mode="dims">
        <div><label for="r-l">Footprint length (ft)</label><input id="r-l" name="len" inputmode="decimal" value="64"></div>
        <div><label for="r-w">Footprint width (ft)</label><input id="r-w" name="wid" inputmode="decimal" value="36"></div>
      </div>
      <div data-mode="dims"><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="12"></div>
      <div data-mode="area" hidden><label for="r-a">Footprint area incl. overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="2400"></div>
      <div class="row2">
        <div><label for="r-p">Pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 8 else "", p) for p in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16]) + """</select></div>
        <div><label for="r-wst">Waste allowance</label><select id="r-wst" name="waste"><option value="10">10% — plain gable</option><option value="12">12% — gable with dormers</option><option value="15" selected>15% — hip roof</option><option value="18">18% — cut-up / valleys</option></select></div>
      </div>
      <div><label for="r-pr">Installed price per square (optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 560"><span class="hint">Use a local quote for a rough replacement figure.</span></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Roof squares (before waste)</small><b data-o="sq">0</b></div>
      <div class="out-rows">
        <div><span>Pitch multiplier</span><b data-o="mult">1.000</b></div>
        <div><span>Roof surface area</span><b data-o="surface">0</b></div>
        <div><span>Squares with waste</span><b data-o="order">0</b></div>
        <div><span>Shingle bundles (3 per square)</span><b data-o="bundles">0</b></div>
        <div><span>Rough replacement cost</span><b data-o="cost">—</b></div>
      </div>
      <p class="out-msg" data-o="steep"></p>
    </div>
  </div>
</div>"""

DEDUCT = f"""
<div class="tool" data-tool="deduct">
  <div class="tool-head"><span>Named-storm deductible calculator</span><i>Percent vs. flat, in dollars</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling coverage (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="420000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Named-storm / hurricane deductible</label><select id="w-p" name="pct"><option value="1">1%</option><option value="2" selected>2%</option><option value="3">3%</option><option value="5">5%</option><option value="10">10%</option></select></div>
        <div><label for="w-f">All-other-perils deductible ($)</label><input id="w-f" name="flat" inputmode="decimal" value="1000"></div>
      </div>
      <div><label for="w-l">Estimated storm damage ($)</label><input id="w-l" name="loss" inputmode="decimal" value="26500"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your percentage deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span style="background:{C_CLAY}"></span><span style="background:{C_PINE}"></span></div>
      <div class="legend"><span><i style="background:{C_CLAY}"></i>You absorb</span><span><i style="background:{C_PINE}"></i>Policy pays</span></div>
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
      <p class="hint">Edit each window to match your own policy. Defaults are common figures, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report the claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="2"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="10"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Often counted from the carrier’s request.</span></div>
        <div><label for="t-r">Depreciation recovery (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="180"></div>
        <div><label for="t-s">Suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="1095"><span class="hint">Many property forms say three years (1,095 days). Check yours.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download calendar (.ics)</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the carrier accepted coverage for at least part of the loss in writing?", "Get written confirmation of what was accepted. If the whole claim was denied, speak with a North Carolina attorney before considering appraisal."),
    (3, "Do you have the carrier’s full line-item estimate, not just a summary letter?", "Ask the adjuster for the complete itemized estimate, including the price list date."),
    (3, "Do you have your own itemized estimate from a contractor or estimator?", "Get a line-item estimate. A one-line lump-sum bid carries little weight with a panel."),
    (2, "Do you have dated photos taken soon after the loss?", "Collect every photo, note the dates and add photos of current conditions."),
    (2, "Have you found and read the appraisal paragraph in your policy?", "Locate the ‘Appraisal’ condition and note any deadline to name your appraiser."),
    (2, "Do you know the suit-limitation date in your policy?", "Find the ‘Suit Against Us’ condition and put the date on your calendar with our timeline planner."),
    (2, "Were temporary repairs made, with receipts kept?", "Make reasonable temporary repairs (tarps, drying) and keep every invoice."),
    (1, "Do you have your current declarations page, including deductibles?", "Download or request the declarations page, and note any named-storm or wind/hail deductible."),
    (2, "Has hidden damage (attic, decking, crawlspace, wet walls) been opened and documented?", "Have concealed areas inspected so the scope isn’t missing whole trades."),
    (1, "Is your correspondence with the carrier organized by date?", "Put letters, emails and claim notes in date order in one folder."),
    (2, "Is the gap more than roughly 10% of the carrier’s number or several thousand dollars?", "Test the gap in our settlement gap estimator; small gaps may not justify appraisal costs."),
    (1, "If the carrier requested a sworn proof of loss, was it submitted on time?", "If a proof of loss was requested, complete and return it before the stated deadline."),
]

READY = """
<div class="tool tool-wide" data-tool="ready">
  <div class="tool-head"><span>Appraisal preparedness checkup</span><i>12 questions · about two minutes</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <ol class="quiz">""" + "".join(
    '<li data-w="%d" data-fix="%s"><span>%s</span><span class="yn"><button type="button" class="yes" aria-pressed="false">Yes</button><button type="button" class="no" aria-pressed="false">No</button></span></li>' % (w, f, q)
    for w, q, f in _QUIZ) + """
      </ol>
      <div class="btn-row"><button type="button" class="btn ghost small" data-reset>Clear answers</button></div>
    </div>
    <div class="tool-out ready-out" aria-live="polite">
      <div>
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#e3ebe5" stroke-width="18"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#d9683f" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3" style="transition:stroke-dashoffset .5s,stroke .3s"/></svg>
        <div class="gauge-num"><span data-o="score">–</span></div>
        <p class="hint center">Answered <span data-o="count">0 / 12</span></p>
      </div>
      <div>
        <p class="out-msg" data-o="verdict"></p>
        <p class="todo-h">What to do next</p>
        <ul data-o="todo" class="todo"></ul>
      </div>
    </div>
  </div>
</div>"""

_SPLIT_ROW = """<tr><td><input name="item" value="{0}" aria-label="Damage item"></td><td><input name="amt" inputmode="decimal" value="{1}" aria-label="Repair cost"></td><td><select name="cause" aria-label="Likely cause"><option value="wind"{2}>Wind / wind-driven rain</option><option value="flood"{3}>Flood / surge</option><option value="mixed"{4}>Unclear / both</option></select></td><td><button type="button" class="x" aria-label="Remove row">×</button></td></tr>"""


def _split_row(item, amt, cause):
    return _SPLIT_ROW.format(item, amt, *(" selected" if cause == c else "" for c in ("wind", "flood", "mixed")))


SPLIT = f"""
<div class="tool tool-wide" data-tool="split">
  <div class="tool-head"><span>Wind vs. flood damage splitter</span><i>Illustrative allocation · two policies</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Damage item</th><th>Repair cost ($)</th><th>Likely cause</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_split_row(*r) for r in [("Roof covering and decking", 18500, "wind"), ("Upstairs ceilings and insulation (roof leak)", 6200, "wind"), ("First-floor drywall below water line", 14800, "flood"), ("Flooring, first floor", 11200, "flood"), ("Exterior doors and trim", 3400, "mixed")]) + f"""
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn ghost small" data-add data-run>+ Add item</button></div>
      <div><label for="s-mix">Share of “unclear” items assigned to wind</label><div class="range"><input id="s-mix" type="range" name="mix" min="0" max="100" step="5" value="50" data-unit="%"><output>50%</output></div><span class="hint">Real allocations come from evidence, not a slider. Use this to see how much the split matters.</span></div>
      <div class="row2">
        <div><label for="s-a">Homeowners Coverage A ($)</label><input id="s-a" name="cova" inputmode="decimal" value="350000"></div>
        <div><label for="s-p">Named-storm deductible</label><select id="s-p" name="pct"><option value="0">Flat deductible instead</option><option value="1">1%</option><option value="2" selected>2%</option><option value="5">5%</option></select></div>
      </div>
      <div class="row2">
        <div><label for="s-fd">Flat deductible if no % applies ($)</label><input id="s-fd" name="flat" inputmode="decimal" value="1000"></div>
        <div><label class="check" style="margin-top:30px"><input type="checkbox" name="hasflood" checked> I have a flood policy</label></div>
      </div>
      <div class="row2" data-flood>
        <div><label for="s-fl">Flood building limit ($)</label><input id="s-fl" name="flimit" inputmode="decimal" value="250000"></div>
        <div><label for="s-fded">Flood deductible ($)</label><input id="s-fded" name="fded" inputmode="decimal" value="2000"></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-trio">
        <div class="out-big"><small>Homeowners policy pays</small><b data-o="hopay">$0</b></div>
        <div class="out-big"><small>Flood policy pays</small><b data-o="flpay">$0</b></div>
        <div class="out-big"><small>Left with you</small><b data-o="gap">$0</b></div>
      </div>
      <div class="stack" aria-hidden="true"><span style="background:{C_PINE}"></span><span style="background:#4f7fa3"></span><span style="background:{C_CLAY}"></span></div>
      <div class="legend"><span><i style="background:{C_PINE}"></i>Homeowners (wind)</span><span><i style="background:#4f7fa3"></i>Flood policy</span><span><i style="background:{C_CLAY}"></i>Uninsured / deductibles</span></div>
      <div class="out-rows">
        <div><span>Total damage</span><b data-o="total">$0</b></div>
        <div><span>Allocated to wind</span><b data-o="wind">$0</b></div>
        <div><span>Allocated to flood</span><b data-o="flood">$0</b></div>
        <div><span>Homeowners deductible applied</span><b data-o="hded">$0</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "settlement-gap-estimator", "name": "Settlement Gap Estimator", "icon": "gap", "kind": "Estimator",
        "short": "Size the dispute, project an award and see your net after appraiser and umpire fees at three outcomes.",
        "title": "Settlement Gap Estimator | Is Appraisal Worth the Fees?",
        "desc": "Free settlement gap estimator: compare your estimate with the carrier’s, project an appraisal award and net out appraiser and umpire fees.",
        "h1": "Settlement Gap Estimator: Will Appraisal Pay Off After Fees?",
        "lede": "Enter both estimates, choose where an award might land and add realistic fees. The estimator shows your net at that outcome and at three benchmark outcomes, so you can see how fragile the case is.",
        "markup": GAP_FULL,
        "explain": """
<h2>How to read the results</h2>
<ol><li><strong>Amount in dispute</strong> is your replacement cost estimate minus the carrier’s. Appraisal can only move money inside that gap.</li>
<li><strong>Projected award</strong> applies your slider to the gap. Panels rarely land exactly on either side’s number.</li>
<li><strong>Net gain</strong> subtracts your appraiser’s fee and, if you tick the box, your half of the umpire.</li>
<li><strong>Three outcomes</strong> show the net at 30%, 50% and 80% of the gap. If the net is negative at 30%, the claim depends on a strong result.</li></ol>
<h2>Why the benchmarks matter more than the slider</h2>
<p>It’s tempting to set the slider at 100% and stop there. In practice, well-documented line items tend to hold and unsupported ones tend to fall away. A case that still makes sense at 30% to 50% of the gap is usually one worth discussing with an appraiser.</p>
<h2>What this estimator ignores</h2>
<p>Depreciation timing, deductibles and policy limits change what you’re paid, not the size of the dispute. For payment timing, use the <a href="/calculators/rcv-acv-holdback-calculator/">RCV/ACV holdback calculator</a>; for deductibles, the <a href="/calculators/named-storm-deductible-calculator/">named-storm deductible calculator</a>. All figures are illustrative.</p>
""",
        "faqs": [("Is the projected award a prediction?", "No. It’s a scenario you choose. Real awards depend on documentation, the panel and the policy language."),
                 ("How are appraisers usually paid?", "Arrangements vary: flat fees, hourly rates and, in some cases, a percentage of the increase. Get the arrangement in writing and compare it here before you sign."),
                 ("What size gap usually justifies appraisal?", "There’s no rule, but gaps under about 10% of the carrier’s estimate or a few thousand dollars are often better handled with a documented supplement request.")],
    },
    {
        "slug": "rcv-acv-holdback-calculator", "name": "RCV/ACV Holdback Calculator", "icon": "acv", "kind": "Calculator",
        "short": "Work out the first ACV check, the depreciation held back and the total once repairs are finished.",
        "title": "RCV/ACV Depreciation & Holdback Calculator | Free",
        "desc": "Free RCV/ACV calculator: estimate depreciation item by item, your first actual cash value check and the holdback you can recover after repairs.",
        "h1": "RCV/ACV Depreciation and Holdback Calculator",
        "lede": "Replacement cost policies usually pay in two stages: actual cash value first, then the depreciation held back once repairs are done. Add your items to see both payments and where depreciation is doing the most damage.",
        "markup": DEP,
        "explain": """
<h2>How depreciation is calculated here</h2>
<p>For each row, depreciation equals the item’s age divided by its expected life, multiplied by its replacement cost, capped at the percentage you choose. Actual cash value is replacement cost minus that depreciation. This straight-line approach is common, but carriers may use other schedules, so compare the result with the depreciation column in your estimate.</p>
<h2>The two payments</h2>
<ul><li><strong>First payment:</strong> total ACV minus your deductible.</li>
<li><strong>Holdback:</strong> recoverable depreciation, usually released after you complete repairs and send proof within the time the policy allows.</li>
<li><strong>Total:</strong> replacement cost minus the deductible, if every dollar of holdback is recovered.</li></ul>
<h2>Where disputes start</h2>
<p>Excessive depreciation on labor, on items with long useful lives, or on materials that were nearly new is a frequent source of underpayment. If the depreciation share looks high, an <a href="/claim-appraisal/carrier-estimate-audit/">estimate audit</a> can check it line by line. Figures are illustrative.</p>
""",
        "faqs": [("Does depreciation apply to labor?", "Policy wording and carrier practice vary. Some estimates depreciate materials only; others depreciate labor too. Check how your estimate treats it."),
                 ("When must I claim the holdback?", "Many policies set a deadline to complete repairs and request recoverable depreciation. Read the loss settlement section and put the date on your calendar."),
                 ("What if my policy is actual cash value only?", "Tick the ACV-only box. The holdback won’t be recoverable, so the first payment is the full settlement for that coverage.")],
    },
    {
        "slug": "roof-area-pitch-estimator", "name": "Roof Area & Pitch Estimator", "icon": "roof", "kind": "Estimator",
        "short": "Turn a footprint and pitch into roof squares, bundles and a rough replacement figure to check the estimate.",
        "title": "Roof Area & Pitch Estimator | Squares, Waste & Bundles",
        "desc": "Free roof area estimator: convert footprint and pitch into roof squares, waste, shingle bundles and a rough replacement cost to check your claim.",
        "h1": "Roof Area and Pitch Estimator for Insurance Claims",
        "lede": "Roof measurement errors are one of the quickest ways a claim loses money. Enter the footprint and pitch to estimate surface area and squares, then compare them with the carrier’s roof report.",
        "markup": ROOF,
        "explain": """
<h2>How the estimator works</h2>
<p>Roof surface area equals the footprint area (including overhangs) multiplied by a pitch factor: the square root of 1 + (rise ÷ 12)². A 6/12 roof has a factor of about 1.118; an 8/12 roof about 1.202; a 12/12 roof about 1.414. One square is 100 square feet of roof surface.</p>
<h2>Waste and accessories</h2>
<p>Hips, valleys and dormers waste material. Carriers commonly allow 10% to 15% depending on complexity, while cut-up roofs may need more. Starter, ridge cap, drip edge and underlayment are usually separate line items; check that each appears in your estimate.</p>
<h2>Steep and high charges</h2>
<p>Estimating software typically adds labor for roofs at 7/12 and steeper and for two-story eaves. Many newer homes around Charlotte and the Triangle have 8/12 to 12/12 main roofs, so confirm those charges are included. Results are rough and illustrative; a measured report or inspection is more precise.</p>
""",
        "faqs": [("Why doesn’t my result match the carrier’s report exactly?", "Footprint estimates can’t capture every hip, valley and dormer. Differences of a few percent are normal; larger gaps are worth questioning."),
                 ("How do I find my pitch?", "Check the roof report in your estimate, a contractor’s measurement, or use a pitch gauge app on a gable end from a safe spot. Don’t climb a damaged roof."),
                 ("Do I include the garage and porch?", "Yes, if their roofs are part of the claim. Enter them separately and add the results, since pitches often differ.")],
    },
    {
        "slug": "named-storm-deductible-calculator", "name": "Named-Storm Deductible Calculator", "icon": "pct", "kind": "Calculator",
        "short": "Convert a 1% to 10% hurricane or named-storm deductible into dollars and compare it with a flat deductible.",
        "title": "Named-Storm Deductible Calculator | Hurricane % in Dollars",
        "desc": "Free named-storm deductible calculator: see your hurricane percentage deductible in dollars and what the policy pays compared with a flat one.",
        "h1": "Named-Storm and Hurricane Deductible Calculator",
        "lede": "Coastal and many inland policies apply a percentage deductible when a named storm causes the loss. Percentages look small on paper and large on the check. See yours in dollars.",
        "markup": DEDUCT,
        "explain": """
<h2>How percentage deductibles work</h2>
<p>The percentage is usually applied to your dwelling coverage (Coverage A), not to the size of the loss. With $420,000 of dwelling coverage, a 2% named-storm deductible is $8,400, whether the damage is $9,000 or $90,000. These figures are illustrative.</p>
<h2>When it applies</h2>
<p>Policies define the trigger differently: some use a storm named by the National Hurricane Center, some a declared hurricane, some any windstorm or hail. Some apply it once per storm, others once per season. Read the deductible endorsement and your declarations page closely.</p>
<h2>Why it matters in appraisal</h2>
<p>A dispute worth $6,000 on paper may make little difference to your recovery if the loss is still near the deductible. Run this calculator alongside the <a href="/calculators/settlement-gap-estimator/">settlement gap estimator</a> before deciding to invoke appraisal.</p>
""",
        "faqs": [("Is the percentage based on the damage or my coverage?", "In most forms it’s based on dwelling coverage (Coverage A) shown on the declarations page. Check your endorsement for the exact basis."),
                 ("Do coastal pool policies use percentage deductibles?", "Wind and hail policies for beach and coastal properties commonly carry percentage options. Your declarations page shows what you selected."),
                 ("Does the deductible apply to other structures and contents?", "Usually one deductible applies to the whole occurrence, but some policies apply it per building or per coverage. Wording varies.")],
    },
    {
        "slug": "claim-timeline-planner", "name": "Claim Timeline Planner", "icon": "cal", "kind": "Planner",
        "short": "Lay out reporting, proof-of-loss, holdback and suit-limitation dates and export them to your calendar.",
        "title": "Claim Timeline Planner | Deadlines with Calendar Export",
        "desc": "Free claim timeline planner: map reporting, proof of loss, depreciation and suit-limitation dates from your date of loss and export an .ics file.",
        "h1": "Claim Timeline Planner with Calendar Export",
        "lede": "Property claims run on deadlines that start the day of the loss. Enter your date, adjust each window to your policy, and download every milestone to your phone’s calendar.",
        "markup": DATES,
        "explain": """
<h2>The milestones</h2>
<ul><li><strong>Report the claim:</strong> policies require prompt notice. Report as soon as you safely can; this target is self-imposed.</li>
<li><strong>Temporary repairs:</strong> tarping, drying and board-up protect the property and are usually part of the claim.</li>
<li><strong>Proof of loss:</strong> many forms give a set number of days after the carrier requests one.</li>
<li><strong>Depreciation recovery:</strong> the window to finish repairs and claim the holdback.</li>
<li><strong>Suit limitation:</strong> the last day to file suit under the policy. Many North Carolina property forms say three years from the loss, but forms differ, so confirm yours and talk to an attorney well before it.</li></ul>
<h2>Calendar export</h2>
<p>The download button creates a standard .ics file that Google Calendar, Apple Calendar and Outlook can import. The file is generated in your browser; nothing is uploaded. Dates are planning aids, not legal advice.</p>
""",
        "faqs": [("Does invoking appraisal pause the suit-limitation clock?", "Not necessarily. Whether the period is tolled depends on the policy and the law. Ask a North Carolina attorney if the date is getting close."),
                 ("Where do I find my policy’s deadlines?", "In the conditions section: look for duties after loss, loss payment, loss settlement and suit against us."),
                 ("Is any information saved?", "No. The planner runs entirely in your browser and the calendar file is created on your device.")],
    },
    {
        "slug": "appraisal-preparedness-checkup", "name": "Appraisal Preparedness Checkup", "icon": "chk", "kind": "Checkup",
        "short": "Twelve yes-or-no questions that score your file and build a to-do list before you invoke appraisal.",
        "title": "Appraisal Preparedness Checkup | Is Your Claim Ready?",
        "desc": "Free appraisal preparedness checkup: answer 12 questions about coverage, estimates, photos and deadlines to score your file and get a to-do list.",
        "h1": "Appraisal Preparedness Checkup: Is Your Claim File Ready?",
        "lede": "Appraisal rewards preparation. Answer twelve questions and the checkup scores your file, weighs the items panels care about most and lists exactly what to gather next.",
        "markup": READY,
        "explain": """
<h2>How the score is weighted</h2>
<p>Accepted coverage, the carrier’s full estimate and your own itemized estimate carry the most weight, because appraisal can’t work without them. Photos, policy language, deadlines and hidden-damage documentation come next. Administrative items count, but less.</p>
<h2>Reading your result</h2>
<ul><li><strong>75 and up:</strong> a strong file. The next step is a professional look at the dollar gap.</li>
<li><strong>45–74:</strong> close the gaps on your list before demanding appraisal.</li>
<li><strong>Under 45:</strong> invoking now risks a weak award. Build the file first.</li></ul>
<p>Answers aren’t saved or sent anywhere. When you’re ready, our <a href="/claim-appraisal/carrier-estimate-audit/">estimate audit</a> is a sensible next step.</p>
""",
        "faqs": [("Do I need a perfect score before calling an appraiser?", "No. Many people call with gaps in their file. The checkup simply shows what an appraiser will ask for."),
                 ("Why does accepted coverage matter so much?", "Appraisal values a covered loss. If the carrier denied the claim entirely, the dispute is about coverage and usually needs an attorney."),
                 ("Is this legal advice?", "No. It’s a planning checklist based on common appraisal practice.")],
    },
    {
        "slug": "wind-flood-damage-splitter", "name": "Wind vs. Flood Damage Splitter", "icon": "split", "kind": "Worksheet",
        "short": "Assign hurricane damage to wind or flood and see, in illustrative terms, what each policy might pay.",
        "title": "Wind vs. Flood Damage Splitter | Hurricane Claim Worksheet",
        "desc": "Free hurricane worksheet: split damage between wind and flood, apply deductibles and limits, and see what each policy might pay in illustrative terms.",
        "h1": "Wind vs. Flood Damage Splitter for Hurricane Claims",
        "lede": "After storms like Florence and Helene, many North Carolina homes had wind damage above and flood damage below. List the damage, tag the likely cause and see how two policies, two deductibles and one gap fit together.",
        "markup": SPLIT,
        "explain": """
<h2>Why the split matters</h2>
<p>Homeowners and commercial property policies generally cover windstorm and wind-driven rain through storm-created openings, while flood and storm surge are generally excluded and handled by a separate flood policy, such as one through the National Flood Insurance Program. When a single storm causes both, the allocation decides which policy pays and how much falls through the cracks.</p>
<h2>How the worksheet calculates</h2>
<ul><li>Items tagged wind go to the homeowners side; flood items go to the flood side.</li>
<li>“Unclear” items are divided by the slider so you can see how sensitive the result is.</li>
<li>The homeowners side subtracts the named-storm percentage deductible (or the flat one) and is capped at Coverage A.</li>
<li>The flood side subtracts the flood deductible and is capped at the building limit you enter. Without a flood policy, flood damage stays with you.</li></ul>
<h2>Limits of a worksheet</h2>
<p>Real allocations rest on evidence: water lines, debris, roof openings, weather data and sequence. Policies may also contain anti-concurrent causation wording that affects how mixed causes are treated, which is a coverage issue for the carrier, and possibly an attorney, rather than an appraisal panel. Every figure here is illustrative. Our guide to <a href="/guides/wind-vs-flood-hurricane-claims-nc/">wind vs. flood claims</a> explains documentation in more depth.</p>
""",
        "faqs": [("Can an appraisal panel decide what was wind and what was flood?", "Appraisers can value damage, and some policies let them value it by cause. Whether a cause is covered remains a coverage question outside the panel."),
                 ("Do flood policies cover contents?", "Only if you bought contents coverage. Building and contents are separate limits on most flood policies."),
                 ("Is any of this data stored?", "No. The worksheet runs in your browser and nothing is sent or saved.")],
    },
]
