"""Free claim tools for Missouri Insurance Appraiser: markup + copy.
All logic lives in static/assets/js/app.js and runs in the browser; nothing is stored or sent."""

C_DARK, C_TEAL, C_SAND, C_RUST = "#2A1A0E", "#1f7a80", "#e6d9c6", "#b5652b"


def _head(title, note="Runs in your browser · nothing stored"):
    return f'<div class="calc-top"><p class="calc-name">{title}</p><p class="calc-note">{note}</p></div>'


PAYOUT = f"""
<div class="calc" data-tool="payout">
  {_head("Award &amp; net payout estimator")}
  <div class="calc-grid">
    <div class="calc-in">
      <div class="two">
        <div><label for="p-ins">Insurer’s estimate (RCV)</label><input id="p-ins" name="insurer" inputmode="decimal" value="24800"></div>
        <div><label for="p-own">Your estimate (RCV)</label><input id="p-own" name="yours" inputmode="decimal" value="41300"></div>
      </div>
      <div><label for="p-land">Where might the award land between the two?</label>
        <div class="slide"><input id="p-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <p class="hint">0% means the insurer’s number stands; 100% means your full estimate is awarded.</p></div>
      <div class="two">
        <div><label for="p-ded">Deductible</label><input id="p-ded" name="deduct" inputmode="decimal" value="2500"></div>
        <div><label for="p-paid">Already paid by the insurer</label><input id="p-paid" name="paid" inputmode="decimal" value="14600"><p class="hint">Checks received so far (ACV payments).</p></div>
      </div>
      <div class="two">
        <div><label for="p-ft">Your appraiser’s fee</label><select id="p-ft" name="feetype"><option value="flat">Flat / hourly total ($)</option><option value="pct">Percent of the increase (%)</option></select></div>
        <div><label for="p-fee">Fee amount</label><input id="p-fee" name="fee" inputmode="decimal" value="3200"></div>
      </div>
      <div class="two">
        <div><label for="p-ump">Umpire’s total fee</label><input id="p-ump" name="umpire" inputmode="decimal" value="3000"></div>
        <div class="tick-wrap"><label class="tick"><input type="checkbox" name="useump" checked> Count my half of the umpire fee</label></div>
      </div>
    </div>
    <div class="calc-out" aria-live="polite">
      <div class="headline"><small>Estimated new money after fees</small><b data-o="net">$0</b></div>
      <div class="bar" aria-hidden="true"><span style="background:{C_SAND}"></span><span style="background:{C_TEAL}"></span><span style="background:{C_RUST}"></span></div>
      <div class="key"><span><i style="background:{C_SAND}"></i>Insurer’s number</span><span><i style="background:{C_TEAL}"></i>Your net increase</span><span><i style="background:{C_RUST}"></i>Appraisal costs</span></div>
      <dl class="lines">
        <div><dt>Amount in dispute</dt><dd data-o="gap">$0</dd></div>
        <div><dt>Gap vs. insurer’s estimate</dt><dd data-o="pct">—</dd></div>
        <div><dt>Projected award (RCV)</dt><dd data-o="award">$0</dd></div>
        <div><dt>Award less deductible</dt><dd data-o="afterded">$0</dd></div>
        <div><dt>Still owed after prior checks</dt><dd data-o="owed">$0</dd></div>
        <div><dt>Your appraisal costs</dt><dd data-o="cost">$0</dd></div>
      </dl>
      <p class="mini-h">New money after fees at three outcomes</p>
      <div class="trio"><div><small>Low (25%)</small><b data-o="s25">$0</b></div><div><small>Middle (50%)</small><b data-o="s50">$0</b></div><div><small>High (75%)</small><b data-o="s75">$0</b></div></div>
      <p class="say" data-o="msg"></p>
    </div>
  </div>
</div>"""

GAP_MINI = f"""
<div class="calc calc-mini" data-tool="payout">
  {_head("Two-number gap check", "Illustrative · no sign-up")}
  <div class="calc-grid">
    <div class="calc-in">
      <div><label for="m-ins">Insurer’s estimate</label><input id="m-ins" name="insurer" inputmode="decimal" value="18200"></div>
      <div><label for="m-own">Your contractor’s estimate</label><input id="m-own" name="yours" inputmode="decimal" value="31700"></div>
      <div><label for="m-land">Award lands at</label><div class="slide"><input id="m-land" type="range" name="land" min="0" max="100" step="5" value="50" data-unit="%"><output>50%</output></div><p class="hint">of the disputed amount</p></div>
    </div>
    <div class="calc-out" aria-live="polite">
      <div class="headline"><small>Amount in dispute</small><b data-o="gap">$0</b></div>
      <dl class="lines">
        <div><dt>Gap vs. insurer’s estimate</dt><dd data-o="pct">—</dd></div>
        <div><dt>Projected award</dt><dd data-o="award">$0</dd></div>
        <div><dt>Increase before fees</dt><dd data-o="gain">$0</dd></div>
      </dl>
      <p class="say" data-o="msg"></p>
    </div>
  </div>
</div>"""

_DEP_ROW = """<tr><td><input name="item" value="{0}" aria-label="Item"></td><td><input name="rcv" inputmode="decimal" value="{1}" aria-label="Replacement cost"></td><td><input name="age" inputmode="decimal" value="{2}" aria-label="Age in years"></td><td><input name="life" inputmode="decimal" value="{3}" aria-label="Expected life in years"></td><td class="num" data-o="row">$0</td><td><button type="button" class="rm" aria-label="Remove row">×</button></td></tr>"""

DEPREC = """
<div class="calc calc-wide" data-tool="dep">
  """ + _head("Depreciation &amp; recovery calculator", "Add a row for each line item") + """
  <div class="calc-grid">
    <div class="calc-in">
      <div class="table-wrap rows-table"><table><thead><tr><th scope="col">Item</th><th scope="col">Replacement cost ($)</th><th scope="col">Age (yrs)</th><th scope="col">Life (yrs)</th><th scope="col">ACV</th><th scope="col"><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Architectural shingle roof", 19800, 9, 30), ("Aluminum gutters &amp; downspouts", 2400, 12, 25), ("Fiber-cement siding, south wall", 5600, 7, 40), ("Interior drywall &amp; paint", 3300, 6, 15)]) + """
      </tbody></table></div>
      <p><button type="button" class="btn btn-line btn-sm" data-add data-run>+ Add a line item</button></p>
      <div class="two">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="2000"></div>
        <div><label for="d-cap">Depreciation cap</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="100">No cap</option></select><p class="hint">Estimates often cap depreciation; check yours.</p></div>
      </div>
      <label class="tick"><input type="checkbox" name="nonrec"> My policy pays actual cash value only (depreciation isn’t recoverable)</label>
    </div>
    <div class="calc-out" aria-live="polite">
      <div class="headline"><small>First check (ACV less deductible)</small><b data-o="first">$0</b></div>
      <dl class="lines">
        <div><dt>Replacement cost total</dt><dd data-o="rcv">$0</dd></div>
        <div><dt>Depreciation withheld</dt><dd data-o="dep">$0</dd></div>
        <div><dt>Depreciation as share of RCV</dt><dd data-o="deppct">0%</dd></div>
        <div><dt>Actual cash value</dt><dd data-o="acv">$0</dd></div>
        <div><dt>Holdback you can recover after repairs</dt><dd data-o="held">$0</dd></div>
        <div><dt>Total if the holdback is released</dt><dd data-o="total">$0</dd></div>
      </dl>
      <p class="say">Recovery usually requires finishing repairs and asking for the holdback within the time your policy sets. Figures are illustrative.</p>
    </div>
  </div>
</div>"""

ROOF = """
<div class="calc" data-tool="roof">
  """ + _head("Roof measurement calculator") + """
  <div class="calc-grid">
    <div class="calc-in">
      <fieldset class="seg"><legend>Measure from</legend>
        <label><input type="radio" name="mode" value="dims" checked> House footprint</label>
        <label><input type="radio" name="mode" value="area"> Known flat area</label>
      </fieldset>
      <div class="two" data-mode="dims">
        <div><label for="r-len">Footprint length (ft)</label><input id="r-len" name="len" inputmode="decimal" value="56"></div>
        <div><label for="r-wid">Footprint width (ft)</label><input id="r-wid" name="wid" inputmode="decimal" value="32"></div>
      </div>
      <div data-mode="dims"><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="12"></div>
      <div data-mode="area" hidden><label for="r-area">Flat (plan) area in sq ft</label><input id="r-area" name="area" inputmode="decimal" value="2050"></div>
      <div><label for="r-pitch">Pitch (rise per 12 in. of run)</label><select id="r-pitch" name="pitch">""" + "".join(f'<option value="{p}"{" selected" if p == 7 else ""}>{p}/12</option>' for p in range(2, 15)) + """</select></div>
      <div class="two">
        <div><label for="r-waste">Waste allowance</label><select id="r-waste" name="waste"><option value="10">10% (gable)</option><option value="12" selected>12% (some hips)</option><option value="15">15% (hip / cut-up)</option><option value="18">18% (complex)</option></select></div>
        <div><label for="r-layers">Layers to tear off</label><select id="r-layers" name="layers"><option value="1" selected>1</option><option value="2">2</option><option value="3">3</option></select></div>
      </div>
      <div><label for="r-price">Installed price per square (optional, $)</label><input id="r-price" name="price" inputmode="decimal" value="465"><p class="hint">An illustrative figure. Use a local contractor’s number or your estimate’s unit price.</p></div>
    </div>
    <div class="calc-out" aria-live="polite">
      <div class="headline"><small>Roof squares (before waste)</small><b data-o="sq">0</b></div>
      <dl class="lines">
        <div><dt>Pitch multiplier</dt><dd data-o="mult">1.000</dd></div>
        <div><dt>Sloped surface area</dt><dd data-o="surface">0 sq ft</dd></div>
        <div><dt>Squares to order (with waste)</dt><dd data-o="order">0</dd></div>
        <div><dt>Shingle bundles (3 per square)</dt><dd data-o="bundles">0</dd></div>
        <div><dt>Extra tear-off layers to price</dt><dd data-o="tear">0</dd></div>
        <div><dt>Illustrative material &amp; labor</dt><dd data-o="cost">—</dd></div>
      </dl>
      <p class="say" data-o="steep"></p>
    </div>
  </div>
</div>"""

DEDUCT = f"""
<div class="calc" data-tool="deduct">
  {_head("Wind &amp; hail deductible calculator")}
  <div class="calc-grid">
    <div class="calc-in">
      <div><label for="w-cova">Dwelling limit (Coverage A)</label><input id="w-cova" name="cova" inputmode="decimal" value="315000"><p class="hint">From your declarations page. Percentage deductibles are figured on this, not on the loss.</p></div>
      <div class="two">
        <div><label for="w-pct">Your wind/hail percentage</label><select id="w-pct" name="pct"><option value="0.5">0.5%</option><option value="1" selected>1%</option><option value="2">2%</option><option value="3">3%</option><option value="5">5%</option></select></div>
        <div><label for="w-flat">All-other-perils deductible ($)</label><input id="w-flat" name="flat" inputmode="decimal" value="1500"></div>
      </div>
      <div><label for="w-loss">Estimated hail or wind loss (RCV)</label><input id="w-loss" name="loss" inputmode="decimal" value="17900"></div>
    </div>
    <div class="calc-out" aria-live="polite">
      <div class="headline"><small>Your wind/hail deductible</small><b data-o="pd">$0</b></div>
      <div class="bar" aria-hidden="true"><span style="background:{C_RUST}"></span><span style="background:{C_TEAL}"></span></div>
      <div class="key"><span><i style="background:{C_RUST}"></i>You pay (deductible)</span><span><i style="background:{C_TEAL}"></i>Policy pays</span></div>
      <dl class="lines">
        <div><dt>Payment under your percentage deductible</dt><dd data-o="pdpay">$0</dd></div>
        <div><dt>Payment if the flat deductible applied</dt><dd data-o="flatpay">$0</dd></div>
        <div><dt>Extra cost of the percentage deductible</dt><dd data-o="diff">$0</dd></div>
      </dl>
      <div class="table-wrap"><table class="cmp"><thead><tr><th scope="col">Percentage</th><th scope="col">Deductible</th><th scope="col">Payment on this loss</th></tr></thead><tbody data-o="table"></tbody></table></div>
      <p class="say" data-o="below"></p>
    </div>
  </div>
</div>"""

CALENDAR = """
<div class="calc" data-tool="dates">
  """ + _head("Claim calendar builder", "Exports to your calendar · nothing stored") + """
  <div class="calc-grid">
    <div class="calc-in">
      <div><label for="c-dol">Date of loss</label><input id="c-dol" name="dol" type="date"></div>
      <div class="two">
        <div><label for="c-notice">Report the claim within (days)</label><input id="c-notice" name="notice" inputmode="numeric" value="3"></div>
        <div><label for="c-mitig">Temporary repairs within (days)</label><input id="c-mitig" name="mitig" inputmode="numeric" value="7"></div>
      </div>
      <div class="two">
        <div><label for="c-pol">Proof of loss due (days after loss)</label><input id="c-pol" name="pol" inputmode="numeric" value="60"><p class="hint">Often counted from the insurer’s written request instead. Check your letter.</p></div>
        <div><label for="c-appr">Name your appraiser within (days after demand)</label><input id="c-appr" name="appr" inputmode="numeric" value="20"></div>
      </div>
      <div><label for="c-dem">Date appraisal was demanded (optional)</label><input id="c-dem" name="dem" type="date"></div>
      <div class="two">
        <div><label for="c-rcd">Claim the holdback within (days)</label><input id="c-rcd" name="rcd" inputmode="numeric" value="180"></div>
        <div><label for="c-suit">Suit-limitation period (years)</label><input id="c-suit" name="suit" inputmode="decimal" value="2"><p class="hint">Enter the period in your policy; Missouri law can affect how it applies.</p></div>
      </div>
      <p><button type="button" class="btn btn-teal" data-ics>Download .ics calendar file</button></p>
    </div>
    <div class="calc-out" aria-live="polite">
      <p class="mini-h">Your milestones</p>
      <ol class="when" data-o="timeline"><li><b>Pick your date of loss</b><span>Milestones will appear here.</span></li></ol>
      <p class="say">Dates come from the numbers you enter, not from your policy. They aren’t legal advice; ask a Missouri attorney about any deadline that matters.</p>
    </div>
  </div>
</div>"""

_Q = [
    (3, "Has the insurer accepted that the loss is covered (at least in part)?", "Get a clear written coverage position first. Appraisal values a covered loss; it doesn’t decide coverage."),
    (3, "Do you have the insurer’s full, itemized estimate?", "Ask in writing for the complete line-item estimate, not just the summary page."),
    (2, "Do you have an independent, itemized estimate for the same scope?", "Get a line-item estimate from a contractor or estimator who inspected the property."),
    (2, "Is the gap more than about 10% or several thousand dollars?", "With a small gap, a documented supplement request may be cheaper than appraisal."),
    (2, "Do you have dated photos of the damage before repairs?", "Pull together every photo and video, with dates, before anything else is torn out."),
    (1, "Have you read the appraisal clause in your own policy?", "Find the clause (usually under Conditions) and note any time limits it sets."),
    (1, "Are you well inside your policy’s suit-limitation period?", "If a deadline is close, talk with a Missouri attorney before doing anything else."),
    (1, "Have you kept receipts for emergency repairs and extra living costs?", "Gather receipts for tarps, drying, board-up and any hotel or meal costs."),
    (1, "Can you describe exactly which items or prices you disagree with?", "List the specific items: missed slopes, matching, code items, pricing or O&amp;P."),
]

READY = """
<div class="calc" data-tool="ready">
  """ + _head("Appraisal readiness score", "9 questions · nothing stored") + """
  <div class="calc-grid">
    <div class="calc-in">
      <ol class="qs">""" + "".join(
    f'<li data-w="{w}" data-fix="{fix}"><span class="q">{q}</span><span class="yn" role="group" aria-label="Answer"><button type="button" class="yes" aria-pressed="false">Yes</button><button type="button" class="no" aria-pressed="false">No</button></span></li>'
    for w, q, fix in _Q) + """</ol>
      <p><button type="button" class="btn btn-line btn-sm" data-reset>Clear answers</button></p>
    </div>
    <div class="calc-out" aria-live="polite">
      <div class="dial"><svg width="120" height="120" viewBox="0 0 100 100" aria-hidden="true" focusable="false"><circle cx="50" cy="50" r="40" fill="none" stroke="#e6d9c6" stroke-width="10"/><circle data-o="arc" cx="50" cy="50" r="40" fill="none" stroke="#1f7a80" stroke-width="10" stroke-linecap="round" stroke-dasharray="251.3" stroke-dashoffset="251.3" transform="rotate(-90 50 50)"/></svg><div><b data-o="score">–</b><small>out of 100</small></div></div>
      <p class="mini-c" data-o="count">0 / 9</p>
      <p class="say" data-o="verdict"></p>
      <p class="mini-h">What to fix first</p>
      <ul class="fix" data-o="todo"></ul>
    </div>
  </div>
</div>"""

_SLOPES = [("Front (street) slope", 9, 4), ("Back slope", 9, 1.5), ("Left side", 5, 0.5), ("Right side", 5, 2)]

REPAIR = f"""
<div class="calc calc-wide" data-tool="rr">
  {_head("Roof repair-or-replace splitter")}
  <div class="calc-grid">
    <div class="calc-in">
      <div class="table-wrap rows-table"><table><thead><tr><th scope="col">Roof slope</th><th scope="col">Slope size (squares)</th><th scope="col">Damaged squares</th><th scope="col">Share hit</th></tr></thead><tbody>
      """ + "".join(f'<tr><td><input name="slope" value="{n}" aria-label="Slope name"></td><td><input name="size" inputmode="decimal" value="{s}" aria-label="Slope size in squares"></td><td><input name="hit" inputmode="decimal" value="{h}" aria-label="Damaged squares"></td><td class="num" data-o="share">0%</td></tr>' for n, s, h in _SLOPES) + f"""
      </tbody></table></div>
      <div class="two">
        <div><label for="x-rep">Repair price per square ($)</label><input id="x-rep" name="rep" inputmode="decimal" value="610"><p class="hint">Spot repairs cost more per square than a full roof.</p></div>
        <div><label for="x-new">Full replacement price per square ($)</label><input id="x-new" name="new" inputmode="decimal" value="470"></div>
      </div>
      <div class="two">
        <div><label for="x-min">Minimum charge per repair visit ($)</label><input id="x-min" name="min" inputmode="decimal" value="450"></div>
        <div><label for="x-ded">Deductible ($)</label><input id="x-ded" name="ded" inputmode="decimal" value="2500"></div>
      </div>
      <label class="tick"><input type="checkbox" name="nomatch"> Matching shingles are discontinued or can’t be found</label>
    </div>
    <div class="calc-out" aria-live="polite">
      <div class="headline"><small>Difference between the two scopes</small><b data-o="diff">$0</b></div>
      <div class="bar" aria-hidden="true"><span style="background:{C_TEAL}"></span><span style="background:{C_SAND}"></span></div>
      <div class="key"><span><i style="background:{C_TEAL}"></i>Repair scope</span><span><i style="background:{C_SAND}"></i>Added by full replacement</span></div>
      <dl class="lines">
        <div><dt>Total roof size</dt><dd data-o="total">0 sq</dd></div>
        <div><dt>Damaged squares (share of roof)</dt><dd data-o="hitall">0</dd></div>
        <div><dt>Repair-only scope</dt><dd data-o="repair">$0</dd></div>
        <div><dt>Full replacement scope</dt><dd data-o="full">$0</dd></div>
        <div><dt>Payment on repair scope after deductible</dt><dd data-o="reppay">$0</dd></div>
        <div><dt>Payment on full scope after deductible</dt><dd data-o="fullpay">$0</dd></div>
      </dl>
      <p class="say" data-o="msg"></p>
    </div>
  </div>
</div>"""

_DISC = "This tool is for planning only. It doesn’t interpret your policy, and the figures you enter are illustrative."

TOOLS = [
    {
        "slug": "award-net-payout-estimator", "name": "Award & Net Payout Estimator", "kind": "Estimator", "markup": PAYOUT,
        "short": "Model where an appraisal award might land and what reaches you after the deductible, prior checks and fees.",
        "h1": "Appraisal Award & Net Payout Estimator",
        "lede": "Most people only compare two estimates. This one also takes out the deductible, the checks you’ve already cashed and the cost of appraisal, so you see the new money that might actually reach you.",
        "title": "Appraisal Award & Net Payout Estimator | Free Tool",
        "desc": "Estimate a Missouri appraisal award and your net payout after the deductible, prior insurer payments, appraiser fees and half the umpire fee.",
        "explain": f"""<h2>What the estimator does</h2>
<p>An appraisal award is a replacement-cost figure for the whole covered loss. It isn’t the size of your next check. To get from one to the other you subtract the deductible and everything the insurer has already paid, then the cost of getting there: your appraiser and, if one is needed, half the umpire. This tool lays those steps out in order.</p>
<h2>How to use it</h2>
<ol><li>Enter the insurer’s replacement-cost total and your own itemized estimate for the same scope.</li><li>Move the slider to where you think the award might land. Try several positions; nobody can predict it.</li><li>Add your deductible and the total of the checks you’ve received.</li><li>Enter your appraiser’s fee as a flat amount or a percentage of the increase, and the umpire’s total fee.</li></ol>
<h3>Reading the three outcomes</h3>
<p>The low, middle and high figures show the new money after fees if the award lands a quarter, half or three quarters of the way between the two estimates. If even the high case barely clears your costs, a line-by-line <a href="/appraisal-help/insurer-estimate-review/">estimate review</a> and a supplement request are usually the better first step.</p>
<h2>What it leaves out</h2>
<p>Recoverable depreciation that’s released later, mortgage company endorsements on checks, and any separate payments for contents or living expenses aren’t modeled here. {_DISC}</p>""",
        "faqs": [("Is the award the same as my payment?", "No. The award sets the amount of loss. Your payment is generally that amount less the deductible, prior payments and any depreciation still held back until repairs are done."),
                 ("Who pays the umpire?", "Most appraisal clauses say each side pays its own appraiser and the two sides split the umpire’s fee equally. Check your policy’s wording."),
                 ("Why does the tool show a negative number?", "If appraisal costs are larger than the likely increase, the net is negative. That’s a sign appraisal may not be worth it for this gap.")],
    },
    {
        "slug": "depreciation-recovery-calculator", "name": "Depreciation & Recovery Calculator", "kind": "Calculator", "markup": DEPREC,
        "short": "Split each line item into actual cash value and recoverable depreciation, then see your first check and the holdback.",
        "h1": "Depreciation & Holdback Recovery Calculator",
        "lede": "Replacement-cost policies usually pay in two steps: actual cash value first, then the withheld depreciation once repairs are done. Enter your items to see both figures.",
        "title": "RCV vs. ACV Depreciation Calculator | Holdback Recovery",
        "desc": "Free RCV and ACV calculator for Missouri property claims: depreciation by line item, your first check, the recoverable holdback and the total.",
        "explain": f"""<h2>How depreciation works on a claim</h2>
<p>Insurers depreciate many line items by age and expected life. A nine-year-old roof with a 30-year life might lose close to a third of its value on paper. On a replacement-cost policy that amount is usually <strong>withheld, not lost</strong>: you get it back after the work is done, if you ask within the time the policy allows.</p>
<h2>Using the calculator</h2>
<ul><li>Add one row per item, with its replacement cost, age and a realistic life expectancy.</li><li>Set the depreciation cap to match your estimate. Many estimates won’t depreciate an item past a set percentage.</li><li>Tick the box if your policy settles at actual cash value only, such as some older-roof endorsements or basic policy forms.</li></ul>
<h3>Where disputes usually start</h3>
<p>Depreciation on labor, life expectancies that are too short for the material, and ages that don’t match the property’s records all shrink the first check. Those are fair points to raise, and they can be part of an <a href="/appraisal-help/appraisal-demand-representation/">appraisal</a> when the policy’s wording allows it.</p>
<h2>Limits</h2>
<p>This is straight-line depreciation. Real estimates may use different methods by item. {_DISC}</p>""",
        "faqs": [("Is depreciation gone for good?", "Not on most replacement-cost policies. It’s typically recoverable once repairs are complete and documented, within the deadline in your policy."),
                 ("Can labor be depreciated?", "Practice varies by policy and insurer. If your estimate depreciates labor, it’s worth asking how the policy language supports it."),
                 ("What life expectancy should I use?", "Use a realistic figure for the specific material, like the manufacturer’s rating or the life in the insurer’s estimate, and compare them.")],
    },
    {
        "slug": "roof-measurement-calculator", "name": "Roof Measurement Calculator", "kind": "Calculator", "markup": ROOF,
        "short": "Turn a footprint and pitch into roof squares, waste, bundles and tear-off layers to check the insurer’s numbers.",
        "h1": "Roof Squares, Pitch & Tear-Off Calculator",
        "lede": "Roof claims often turn on measurements. Enter the footprint, overhang and pitch to get sloped area, squares with waste, bundles and extra tear-off layers.",
        "title": "Roof Square & Pitch Calculator | Missouri Hail Claims",
        "desc": "Calculate roof squares from footprint and pitch, add waste and tear-off layers, and compare the result with the roof figures in your Missouri claim.",
        "explain": f"""<h2>Why measurements matter</h2>
<p>A roofing square is 100 square feet of roof surface. Because a roof slopes, its surface is larger than the footprint below it. The steeper the pitch, the bigger the difference. A missing slope, a pitch entered too low, or too little waste can take thousands of dollars off a hail estimate.</p>
<h2>How the math works</h2>
<p>The pitch multiplier is √(1 + (rise ÷ 12)²). A 7/12 roof has a multiplier of about 1.158, so a 2,000 sq ft plan area becomes roughly 2,316 sq ft of roof. Waste covers starter, ridge and the cutting that hips and valleys require. Extra tear-off layers matter because removing two layers of shingles is more work than removing one.</p>
<h3>Comparing with the insurer’s estimate</h3>
<ul><li>Check the total squares and the waste percentage listed in the estimate.</li><li>Look for steep-roof and high-roof charges where the pitch or height calls for them.</li><li>Confirm that every slope, including garage and porch roofs, is included.</li></ul>
<p>For a damaged roof, the <a href="/toolkit/roof-repair-or-replace-splitter/">repair-or-replace splitter</a> shows what partial repairs and full replacement cost side by side. {_DISC}</p>""",
        "faqs": [("How accurate is a footprint estimate?", "It’s a reasonable check for simple roofs. Complex roofs with dormers, valleys and multiple levels need a field or aerial measurement."),
                 ("What waste factor is normal?", "Simple gable roofs often use around 10%, hip roofs more, and cut-up roofs more still. Your estimate should explain its figure."),
                 ("When do steep charges apply?", "Estimating software typically starts adding steep-roof labor around 7/12 to 8/12, with higher charges at steeper pitches.")],
    },
    {
        "slug": "hail-deductible-calculator", "name": "Wind & Hail Deductible Calculator", "kind": "Calculator", "markup": DEDUCT,
        "short": "See what a percentage wind/hail deductible really costs on your dwelling limit, next to a flat deductible.",
        "h1": "Wind & Hail Percentage Deductible Calculator",
        "lede": "Many Missouri policies use a separate wind/hail deductible set as a percentage of the dwelling limit. Here’s what 1%, 2% or 5% means in dollars on your home.",
        "title": "Wind & Hail Deductible Calculator | Percentage vs. Flat",
        "desc": "Work out a percentage wind and hail deductible on your Missouri dwelling limit, compare it with a flat deductible, and see the payment on a loss.",
        "explain": f"""<h2>How percentage deductibles work</h2>
<p>A 2% wind/hail deductible on a home insured for $300,000 is $6,000, whatever the size of the loss. That’s why a hail claim that looks big on paper can pay surprisingly little. The percentage applies to the dwelling limit (Coverage A) on your declarations page, not to the damage.</p>
<h2>Using the calculator</h2>
<ol><li>Enter Coverage A from the declarations page.</li><li>Pick the wind/hail percentage your policy lists, and your regular deductible for other perils.</li><li>Enter the estimated loss to see what the policy would pay under each deductible.</li></ol>
<p>The table shows the same loss under several common percentages, so you can see how much the choice matters when it’s time to renew.</p>
<h3>Deductibles and appraisal</h3>
<p>When a loss sits just above the deductible, small estimate differences decide whether anything is paid at all. That’s often when a careful <a href="/appraisal-help/hail-roof-damage-appraisal/">hail damage appraisal</a> or estimate review is worth a look. {_DISC}</p>""",
        "faqs": [("Is the deductible a percentage of the damage?", "No. A percentage deductible is figured on the dwelling coverage limit. The damage amount doesn’t change it."),
                 ("Does it apply to every storm?", "It typically applies per occurrence to wind or hail losses. Read how your policy defines the occurrence and which perils it covers."),
                 ("Can I change my deductible?", "Usually at renewal, through your agent or insurer. A lower deductible generally means a higher premium.")],
    },
    {
        "slug": "claim-calendar-builder", "name": "Claim Calendar Builder", "kind": "Planner", "markup": CALENDAR,
        "short": "Turn your date of loss and policy time limits into a dated milestone list, and download it to your calendar.",
        "h1": "Claim Calendar Builder With Calendar Export",
        "lede": "Claims are lost on missed dates as often as on bad estimates. Enter the date of loss and the time limits from your policy, then save the milestones to your phone’s calendar.",
        "title": "Insurance Claim Deadline Calendar | Free .ics Export",
        "desc": "Build a dated milestone list for your Missouri property claim: notice, proof of loss, naming an appraiser, holdback and suit dates, with .ics export.",
        "explain": f"""<h2>What goes on the calendar</h2>
<ul><li><strong>Notice and temporary repairs.</strong> Policies require prompt notice and reasonable steps to prevent more damage. The targets here are yours to set.</li><li><strong>Proof of loss.</strong> Some insurers request a sworn proof of loss with a due date, often counted from their written request.</li><li><strong>Naming your appraiser.</strong> Many appraisal clauses give each side a set number of days, often 20, to name an appraiser after a written demand.</li><li><strong>Holdback recovery.</strong> Replacement-cost policies usually set a window to finish repairs and claim withheld depreciation.</li><li><strong>Suit limitation.</strong> Policies state a period to file suit. Missouri law can affect how that period applies, which is a question for a Missouri attorney.</li></ul>
<h2>Saving it to your calendar</h2>
<p>The download button creates an <code>.ics</code> file that works with Google Calendar, Apple Calendar and Outlook. Each milestone becomes an all-day event. The file is built in your browser and never sent to us.</p>
<h3>Next steps</h3>
<p>Read the <a href="/appraisal-roadmap/">appraisal roadmap</a> for what happens at each stage. {_DISC}</p>""",
        "faqs": [("Are these legal deadlines?", "No. The dates come only from the numbers you enter. Your policy and Missouri law control, and an attorney can tell you how they apply."),
                 ("Is my information saved?", "No. Everything runs in your browser. The calendar file is created on your device."),
                 ("What if I don’t know my policy’s time limits?", "Ask your agent or insurer for a complete copy of the policy, including endorsements, and look under the Conditions section.")],
    },
    {
        "slug": "appraisal-readiness-score", "name": "Appraisal Readiness Score", "kind": "Checklist", "markup": READY,
        "short": "Nine yes-or-no questions that score how ready your claim is for appraisal, plus what to fix first.",
        "h1": "Appraisal Readiness Score for Your Claim",
        "lede": "Demanding appraisal before your file is ready can lock in a weak number. Answer nine questions to get a score and a short list of what to gather first.",
        "title": "Appraisal Readiness Score | Is Your Claim Ready?",
        "desc": "Score how ready your Missouri property claim is for appraisal with nine quick questions, and get a list of documents and steps to handle first.",
        "explain": f"""<h2>Why readiness matters</h2>
<p>An appraisal panel can only work with the evidence in front of it. The questions here are weighted toward what decides most awards: a clear coverage position, two itemized estimates for the same scope, and photos that show the damage before repairs.</p>
<h2>How the score works</h2>
<p>Each question carries a weight from one to three. Your score is the share of weighted points you’ve earned. A score of 75 or more suggests the file is in good shape. Below 45, it usually pays to fill the gaps before invoking the clause.</p>
<h3>Things the score can’t judge</h3>
<p>It can’t judge how strong your estimate is, how your policy is worded, or whether a legal issue such as a denial or a near deadline needs an attorney first. If coverage itself is disputed, appraisal usually isn’t the right tool. See <a href="/questions-answered/">questions answered</a> for more. {_DISC}</p>""",
        "faqs": [("What score should I aim for?", "Seventy-five or more is a good sign. A lower score points to specific gaps, listed under the score."),
                 ("Does a high score mean I’ll win?", "No. It means your file has the basics an appraisal panel expects. The result depends on the facts and the estimates."),
                 ("Are my answers stored?", "No. The score is calculated in your browser and disappears when you leave the page.")],
    },
    {
        "slug": "roof-repair-or-replace-splitter", "name": "Roof Repair-or-Replace Splitter", "kind": "Estimator", "markup": REPAIR,
        "short": "Enter damaged squares slope by slope and compare a repair-only scope with a full roof replacement.",
        "h1": "Roof Repair-or-Replace Splitter for Hail Claims",
        "lede": "After a Missouri hailstorm, the biggest dispute is often whether the roof gets spot repairs or a full replacement. Enter the damage on each slope and compare both scopes in dollars.",
        "title": "Roof Repair vs. Replace Calculator | Missouri Hail Claims",
        "desc": "Compare a repair-only scope with full roof replacement for a Missouri hail claim, slope by slope, with matching, minimum charges and deductible.",
        "explain": f"""<h2>Why this dispute is so common here</h2>
<p>Missouri sees hail most springs, from the Kansas City suburbs to the St. Louis metro and the Ozarks. Hail rarely hits every slope evenly, so estimates often split the difference: replace one slope, repair a few squares on another. Whether that’s a reasonable repair depends on the damage, the materials and, often, whether matching shingles exist.</p>
<h2>How to use the splitter</h2>
<ol><li>List each roof slope with its size in squares and the number of damaged squares.</li><li>Enter a repair price per square and a full replacement price per square. Repairs usually cost more per square.</li><li>Add the minimum charge a roofer would bill per repair visit, and your deductible.</li><li>Tick the matching box if the existing shingle is discontinued.</li></ol>
<h3>What the numbers tell you</h3>
<p>When damaged squares spread across most slopes, or matching materials aren’t available, the repair scope can approach the cost of replacement while leaving a patched roof. That’s a common subject of <a href="/appraisal-help/hail-roof-damage-appraisal/">hail damage appraisal</a>. Whether your policy requires matching, and how far, depends on its wording. {_DISC}</p>""",
        "faqs": [("Is there a rule for when a roof must be replaced?", "Not a single number. It depends on the damage, repairability, material availability and policy wording. Many disputes turn on those facts."),
                 ("Does my policy have to pay for matching?", "That depends on the policy language and the facts. Some policies address matching directly; others don’t. A Missouri attorney can explain the legal side."),
                 ("Why is repair priced higher per square?", "Small repairs carry set-up time, minimum charges and careful work around existing shingles, so the per-square cost runs higher.")],
    },
]
