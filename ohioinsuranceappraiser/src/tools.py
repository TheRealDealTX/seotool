"""Ohio claim workbench: tool markup + explanatory copy. Logic lives in static/assets/js/app.js."""

TB = "/appraisal-workbench/"

GAP_FULL = """
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Claim gap &amp; fee estimator</span><i>Three outcomes, side by side</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Insurer’s estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="21600"><span class="hint">Replacement cost total before depreciation and deductible.</span></div>
        <div><label for="g-own">Your estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="36900"><span class="hint">Your contractor’s or independent line-item estimate.</span></div>
      </div>
      <div class="row2">
        <div><label for="g-ft">Your appraiser’s fee type</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of the increase (%)</option></select></div>
        <div><label for="g-fee">Fee amount</label><input id="g-fee" name="fee" inputmode="decimal" value="2750"></div>
      </div>
      <div class="row2">
        <div><label for="g-ump">Umpire’s total fee</label><input id="g-ump" name="umpire" inputmode="decimal" value="3200"><span class="hint">Usually split 50/50 between the two sides.</span></div>
        <div><label class="check" style="margin-top:28px"><input type="checkbox" name="useump" checked> An umpire will be needed</label></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Amount in dispute</small><b data-o="gap">$0</b><span class="sub" data-o="pct"></span></div>
      <div class="table-wrap scen"><table><thead><tr><th>If the award lands at…</th><th>Award</th><th>Your costs</th><th>Net to you</th></tr></thead><tbody>
        <tr><th>35% of the gap <small>cautious</small></th><td data-o="a35">$0</td><td data-o="c35">$0</td><td data-o="n35">$0</td></tr>
        <tr><th>60% of the gap <small>middle</small></th><td data-o="a60">$0</td><td data-o="c60">$0</td><td data-o="n60">$0</td></tr>
        <tr><th>85% of the gap <small>well documented</small></th><td data-o="a85">$0</td><td data-o="c85">$0</td><td data-o="n85">$0</td></tr>
      </tbody></table></div>
      <div class="out-rows"><div><span>Break-even landing point</span><b data-o="be">—</b></div></div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

GAP_MINI = """
<div class="tool tool-mini" data-tool="gap">
  <div class="tool-head"><span>Quick gap check</span><i>Nothing is stored</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="m-ins">Insurer’s estimate</label><input id="m-ins" name="insurer" inputmode="decimal" value="17400"></div>
        <div><label for="m-own">Your contractor’s estimate</label><input id="m-own" name="yours" inputmode="decimal" value="29800"></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Amount in dispute</small><b data-o="gap">$0</b><span class="sub" data-o="pct"></span></div>
      <div class="out-rows">
        <div><span>Award at 35% of the gap</span><b data-o="a35">$0</b></div>
        <div><span>Award at 60% of the gap</span><b data-o="a60">$0</b></div>
        <div><span>Award at 85% of the gap</span><b data-o="a85">$0</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

_DEP_ROW = """<tr><td><input name="item" value="{0}" aria-label="Item"></td><td><input name="rcv" inputmode="decimal" value="{1}" aria-label="Replacement cost"></td><td><input name="age" inputmode="decimal" value="{2}" aria-label="Age in years"></td><td><input name="life" inputmode="decimal" value="{3}" aria-label="Expected life in years"></td><td class="mono" data-o="row">$0</td><td><button type="button" class="x" aria-label="Remove row">×</button></td></tr>"""

DEP = """
<div class="tool tool-wide" data-tool="dep">
  <div class="tool-head"><span>RCV / ACV holdback calculator</span><i>Add a row per damaged item</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Asphalt shingle roof", 16800, 11, 25), ("Gutters and downspouts", 2100, 11, 20), ("Finished basement carpet", 2650, 7, 10), ("Basement drywall and paint", 3900, 7, 15)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn ghost small" data-add data-run>+ Add item</button></div>
      <div class="row3">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="1000"></div>
        <div><label for="d-cap">Depreciation cap</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="90">90%</option></select></div>
        <div><label for="d-lab">Labor share of each item</label><select id="d-lab" name="labor"><option value="0" selected>Depreciate all of it</option><option value="35">35% labor — not depreciated</option><option value="50">50% labor — not depreciated</option><option value="60">60% labor — not depreciated</option></select></div>
      </div>
      <label class="check"><input type="checkbox" name="nonrec"> My policy pays actual cash value only (no recoverable depreciation)</label>
    </div>
    <div class="tool-out tool-out-3" aria-live="polite">
      <div class="out-big"><small>First check (ACV − deductible)</small><b data-o="first">$0</b></div>
      <div class="out-big"><small>Held back until repairs</small><b data-o="held">$0</b></div>
      <div class="out-big"><small>Total once repairs are done</small><b data-o="total">$0</b></div>
      <div class="out-rows full">
        <div><span>Replacement cost (RCV)</span><b data-o="rcv">$0</b></div>
        <div><span>Depreciation taken</span><b data-o="dep">$0</b></div>
        <div><span>Depreciation as a share of RCV</span><b data-o="deppct">0%</b></div>
        <div><span>Actual cash value (ACV)</span><b data-o="acv">$0</b></div>
      </div>
    </div>
  </div>
</div>"""

ROOF = """
<div class="tool" data-tool="roof">
  <div class="tool-head"><span>Roof area &amp; pitch calculator</span><i>Check the squares on your estimate</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <fieldset class="seg"><legend class="sr-only">Measurement method</legend>
        <label class="check"><input type="radio" name="mode" value="dims" checked> Length × width</label>
        <label class="check"><input type="radio" name="mode" value="area"> I know the footprint area</label>
      </fieldset>
      <div class="row2" data-mode="dims">
        <div><label for="r-l">Footprint length (ft)</label><input id="r-l" name="len" inputmode="decimal" value="46"></div>
        <div><label for="r-w">Footprint width (ft)</label><input id="r-w" name="wid" inputmode="decimal" value="30"></div>
      </div>
      <div data-mode="dims"><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="12"></div>
      <div data-mode="area" hidden><label for="r-a">Footprint area incl. overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="1600"></div>
      <div class="row2">
        <div><label for="r-p">Roof pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 8 else "", p) for p in [3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18]) + """</select></div>
        <div><label for="r-st">Stories at the eave</label><select id="r-st" name="stories"><option value="1">One</option><option value="2" selected>Two</option><option value="3">Three or more</option></select></div>
      </div>
      <div class="row2">
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="10">10% — simple gable</option><option value="12" selected>12% — gable with dormers</option><option value="15">15% — hip roof</option><option value="18">18% — cut-up roof</option></select></div>
        <div><label for="r-pr">Installed price per square</label><input id="r-pr" name="price" inputmode="decimal" placeholder="optional, e.g. 560"></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Roof squares before waste</small><b data-o="sq">0</b></div>
      <div class="out-rows">
        <div><span>Pitch multiplier</span><b data-o="mult">1.000</b></div>
        <div><span>Roof angle</span><b data-o="deg">0°</b></div>
        <div><span>Roof surface area</span><b data-o="surface">0</b></div>
        <div><span>Squares with waste</span><b data-o="order">0</b></div>
        <div><span>Shingle bundles (3 per square)</span><b data-o="bundles">0</b></div>
        <div><span>Rough replacement cost</span><b data-o="cost">—</b></div>
      </div>
      <p class="out-msg" data-o="steep"></p>
    </div>
  </div>
</div>"""

DEDUCT = """
<div class="tool" data-tool="deduct">
  <div class="tool-head"><span>Percentage deductible calculator</span><i>1%, 2% and 5% compared</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling coverage (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="310000"><span class="hint">From the declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Your wind/hail deductible</label><select id="w-p" name="pct"><option value="1">1%</option><option value="2" selected>2%</option><option value="3">3%</option><option value="5">5%</option></select></div>
        <div><label for="w-f">All-other-perils deductible ($)</label><input id="w-f" name="flat" inputmode="decimal" value="1000"></div>
      </div>
      <div><label for="w-l">Estimated wind or hail damage</label><input id="w-l" name="loss" inputmode="decimal" value="18500"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s-you"></span><span class="s-pol"></span></div>
      <div class="legend"><span><i class="s-you"></i>You pay</span><span><i class="s-pol"></i>Policy pays</span></div>
      <div class="table-wrap scen"><table><thead><tr><th>Deductible</th><th>In dollars</th><th>Claim pays</th></tr></thead><tbody>
        <tr><th>Flat</th><td data-o="flatd">$0</td><td data-o="flatpay">$0</td></tr>
        <tr><th>1% of Coverage A</th><td data-o="d1">$0</td><td data-o="p1">$0</td></tr>
        <tr><th>2% of Coverage A</th><td data-o="d2">$0</td><td data-o="p2">$0</td></tr>
        <tr><th>5% of Coverage A</th><td data-o="d5">$0</td><td data-o="p5">$0</td></tr>
      </tbody></table></div>
      <p class="out-msg" data-o="below"></p>
    </div>
  </div>
</div>"""

DATES = """
<div class="tool" data-tool="dates">
  <div class="tool-head"><span>Ohio claim calendar builder</span><i>Exports an .ics file</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
        <div><label for="t-ad">Appraisal demand date (optional)</label><input id="t-ad" type="date" name="demand"></div>
      </div>
      <p class="hint" style="margin:0">Set each window to match your own policy. The defaults are common figures, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report the claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="3"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="10"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"></div>
        <div><label for="t-r">Depreciation recovery (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="180"></div>
        <div><label for="t-s">Suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="365"><span class="hint">One year = 365 days.</span></div>
        <div><label for="t-a">Name an appraiser within (days of demand)</label><input id="t-a" name="appr" inputmode="numeric" value="20"></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download calendar (.ics)</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the insurer accepted coverage for at least part of the loss?", "Get coverage confirmed in writing. If the claim was denied, talk with an Ohio attorney before thinking about appraisal."),
    (3, "Do you have the insurer’s full line-item estimate, not just a payment letter?", "Ask the adjuster for the complete itemized estimate in writing."),
    (3, "Do you have your own itemized estimate built from a site inspection?", "Get an independent line-item estimate; a one-page contractor bid won’t carry weight with a panel."),
    (2, "Are there dated photos from right after the loss?", "Pull together every photo and note the date each one was taken."),
    (2, "Have you found and read the policy’s appraisal clause?", "Find the ‘Appraisal’ condition and note any appraiser-selection window."),
    (2, "Do you know the date in the policy’s ‘Suit Against Us’ clause?", "Calendar the suit-limitation date — many Ohio policies allow one year."),
    (2, "Were temporary repairs made and receipts kept?", "Make reasonable temporary repairs (tarps, water extraction) and keep every receipt."),
    (2, "Has hidden damage been opened up and documented — attic, wall cavities, basement?", "Make sure the full scope is visible before anyone puts a number on it."),
    (1, "Is the carrier correspondence saved in date order?", "Collect letters, emails and claim notes into one dated file."),
    (2, "Is the gap more than roughly 10% of the insurer’s estimate or $5,000?", "Run the claim gap & fee estimator — a small gap may not cover appraisal costs."),
]

READY = """
<div class="tool tool-wide" data-tool="ready">
  <div class="tool-head"><span>Appraisal readiness checkup</span><i>10 questions · about two minutes</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <ol class="quiz">""" + "".join(
    '<li data-w="%d" data-fix="%s"><span>%s</span><span class="yn"><button type="button" class="yes" aria-pressed="false">Yes</button><button type="button" class="no" aria-pressed="false">No</button></span></li>' % (w, f, q)
    for w, q, f in _QUIZ) + """
      </ol>
      <div class="btn-row"><button type="button" class="btn ghost small" data-reset>Clear answers</button></div>
    </div>
    <div class="tool-out tool-out-score" aria-live="polite">
      <div class="score-box">
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#f1dfe1" stroke-width="18"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#c12637" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3" style="transition:stroke-dashoffset .5s,stroke .3s"/></svg>
        <div class="gauge-num"><span data-o="score">–</span></div>
        <p class="hint" style="text-align:center">Answered <span data-o="count">0 / 10</span></p>
      </div>
      <div>
        <p class="out-msg" data-o="verdict"></p>
        <p class="todo-h">Still to do</p>
        <ul data-o="todo" class="todo"></ul>
      </div>
    </div>
  </div>
</div>"""

BACKUP = """
<div class="tool" data-tool="backup">
  <div class="tool-head"><span>Basement backup sublimit calculator</span><i>Sewer, drain &amp; sump losses</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="b-l">Total basement damage (repairs + contents)</label><input id="b-l" name="loss" inputmode="decimal" value="24500"></div>
      <div><label for="b-c">What caused the water?</label><select id="b-c" name="cause"><option value="backup" selected>Sewer or drain backed up / sump pump failed</option><option value="pipe">A pipe, water heater or appliance burst suddenly</option><option value="flood">Surface water or river flooding came in</option><option value="seep">Slow seepage through the foundation</option></select></div>
      <div class="row2">
        <div><label for="b-e">Backup endorsement limit</label><select id="b-e" name="limit"><option value="0">No endorsement</option><option value="5000">$5,000</option><option value="10000" selected>$10,000</option><option value="15000">$15,000</option><option value="25000">$25,000</option><option value="50000">$50,000</option></select></div>
        <div><label for="b-d">Deductible ($)</label><input id="b-d" name="deduct" inputmode="decimal" value="1000"></div>
      </div>
      <div class="row2">
        <div><label for="b-m">Water extraction / dry-out cost</label><input id="b-m" name="mitig" inputmode="decimal" value="3800"><span class="hint">Included in the total above.</span></div>
        <div><label for="b-f">Flood policy building + contents limit</label><input id="b-f" name="flood" inputmode="decimal" value="0"><span class="hint">0 if you have no flood policy.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Likely payable under the policy</small><b data-o="pay">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s-pol"></span><span class="s-ded"></span><span class="s-you"></span></div>
      <div class="legend"><span><i class="s-pol"></i>Payable</span><span><i class="s-ded"></i>Deductible</span><span><i class="s-you"></i>Not covered</span></div>
      <div class="out-rows">
        <div><span>Coverage that applies</span><b data-o="which">—</b></div>
        <div><span>Cap on this loss</span><b data-o="cap">—</b></div>
        <div><span>Left with you (incl. deductible)</span><b data-o="you">$0</b></div>
        <div><span>Share of the loss covered</span><b data-o="share">0%</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "claim-gap-fee-estimator", "name": "Claim Gap & Fee Estimator", "icon": "gap", "kind": "Estimator", "kw": "insurance appraisal cost calculator",
        "short": "Compare your number with the insurer’s and see three possible awards, net of appraiser and umpire fees.",
        "title": "Insurance Appraisal Cost Calculator | Gap & Fees",
        "desc": "Free insurance appraisal cost calculator: enter both estimates and fees to see three possible awards, your net recovery and the break-even point.",
        "h1": "Insurance Appraisal Cost Calculator: Claim Gap & Fees",
        "lede": "Appraisal only makes sense if the award can outrun the cost of getting it. Enter both estimates and realistic fees to see a cautious, middle and well-documented outcome side by side.",
        "markup": GAP_FULL,
        "explain": """
<h2>Reading the three scenarios</h2>
<p>Panels seldom award either side’s opening figure. Items backed by measurements, photos and local pricing tend to survive; unsupported items tend to drop out. That’s why this estimator shows three landing points instead of one. If appraisal only pays off in the 85% row, the case leans heavily on perfect documentation. If it’s still positive at 35%, the dispute is probably large enough to justify the process.</p>
<h2>The break-even point</h2>
<p>The break-even figure is the share of the disputed amount the award must reach just to cover your appraiser and your half of the umpire. With a percentage fee there’s no true break-even, because the fee shrinks with the result, so the tool reports the fixed umpire share instead.</p>
<h2>What this doesn’t include</h2>
<ul><li>Deductibles and depreciation timing — use the <a href="/appraisal-workbench/rcv-acv-holdback-calculator/">RCV/ACV holdback calculator</a> for that.</li>
<li>Policy limits and sublimits, such as a sewer backup endorsement.</li>
<li>Coverage questions. Appraisal values a covered loss; it doesn’t decide what’s covered.</li></ul>
<div class="note"><b class="h">Illustrative only</b>The default figures are made-up examples, not results from any claim. Replace them with your own numbers.</div>
""",
        "faqs": [
            ("Why three scenarios instead of a slider?", "A single projected award invites false precision. Seeing a cautious, middle and strong outcome together shows how much of the result depends on documentation."),
            ("Who pays the umpire in Ohio appraisals?", "Most policies say each side pays its own appraiser and the umpire’s fee is shared equally. Check the appraisal condition in your own policy."),
            ("Can appraisal lower my claim?", "The panel decides the amount of loss on the evidence, so an award can come in below what you hoped for. It rarely goes below an amount the insurer has already agreed to, but read your policy and any demand carefully."),
        ],
    },
    {
        "slug": "rcv-acv-holdback-calculator", "name": "RCV/ACV Holdback Calculator", "icon": "acv", "kind": "Calculator", "kw": "RCV vs ACV calculator",
        "short": "Work out the first actual-cash-value check, the depreciation held back and the total after repairs.",
        "title": "RCV vs ACV Calculator | Depreciation & Holdback",
        "desc": "RCV vs ACV calculator for property claims: list items by age and life, choose a depreciation cap and labor share, and see the check you get now.",
        "h1": "RCV vs ACV Calculator for Depreciation and Holdback",
        "lede": "Replacement-cost policies usually pay twice: an actual-cash-value check now and the held-back depreciation once repairs are finished. List your damaged items to see how the money splits.",
        "markup": DEP,
        "explain": """
<h2>How the math works</h2>
<p>Each row uses straight-line depreciation: age divided by expected life, multiplied by the replacement cost and capped at the maximum you pick. ACV is replacement cost minus that depreciation. Your first check is total ACV minus the deductible; the difference between RCV and ACV is what a replacement-cost policy typically releases after the work is done.</p>
<h2>The labor setting</h2>
<p>Some estimates depreciate the whole line item, labor included; others depreciate materials only. How that’s handled depends on the policy wording and the law that applies, and it has been argued in courts in several states. Use the labor menu to see how much the choice moves your first check, then ask the adjuster to explain the method used on your estimate in writing.</p>
<h2>Life expectancies you’ll often see</h2>
<div class="table-wrap"><table><thead><tr><th>Item</th><th>Common range</th></tr></thead><tbody>
<tr><th>Asphalt shingles</th><td>20–30 years</td></tr><tr><th>Natural slate</th><td>75 years or more</td></tr><tr><th>Vinyl siding</th><td>30–40 years</td></tr><tr><th>Carpet and pad</th><td>8–12 years</td></tr><tr><th>Interior paint</th><td>8–12 years</td></tr><tr><th>Gutters (aluminum)</th><td>20–30 years</td></tr>
</tbody></table></div>
<h2>Don’t lose the holdback</h2>
<p>Most replacement-cost policies set a window to finish repairs and claim the depreciation. The <a href="/appraisal-workbench/claim-calendar-builder/">claim calendar builder</a> puts that date in your calendar.</p>
""",
        "faqs": [
            ("Is depreciation the same as a lowball estimate?", "No. Depreciation is a normal part of how replacement-cost policies pay. The questions worth checking are whether the life expectancies, ages and cap are reasonable and whether labor was depreciated."),
            ("What if I never make the repairs?", "Under most replacement-cost policies you keep the ACV payment, but the held-back depreciation is usually paid only after repair or replacement within the policy’s time limit."),
            ("Why does the tool ask for a cap?", "Many estimates limit depreciation to a maximum percentage so that even very old items keep some value. If your estimate uses a different cap, choose it from the menu."),
        ],
    },
    {
        "slug": "roof-area-pitch-calculator", "name": "Roof Area & Pitch Calculator", "icon": "roof", "kind": "Calculator", "kw": "roof squares calculator",
        "short": "Turn a footprint and pitch into true roof squares, bundles and steep/high-roof flags.",
        "title": "Roof Squares Calculator | Pitch, Waste & Bundles",
        "desc": "Roof squares calculator for insurance claims: convert footprint and pitch into true surface area, squares with waste, and steep or high-roof flags.",
        "h1": "Roof Squares Calculator with Pitch and Waste",
        "lede": "Short measurements are one of the quietest ways a roof claim gets underpaid. Use the footprint, pitch and number of stories to estimate true squares and see whether steep or high-roof charges should appear.",
        "markup": ROOF,
        "explain": """
<h2>Why pitch changes everything</h2>
<p>A roof is bigger than the ground it covers. The multiplier is √(1 + (rise ÷ 12)²). A 6/12 roof is about 12% larger than its footprint, an 8/12 roof about 20% larger and a 12/12 roof about 41% larger. Plenty of older Ohio homes — Cleveland and Cincinnati Victorians, Columbus foursquares — sit at 10/12 or steeper.</p>
<h2>Steep and high charges</h2>
<p>Estimating software commonly adds labor for roofs at 7/12 and steeper and for slopes two or more stories above the ground. The calculator flags both so you can look for those lines on the insurer’s estimate.</p>
<h2>Comparing against the estimate</h2>
<ul><li>Find total squares and the waste percentage in the roofing section.</li>
<li>A difference of more than about 5–10% from your result is worth asking about.</li>
<li>Check ridge cap, starter, drip edge, ice-and-water barrier and valleys are listed.</li>
<li>Ice-and-water barrier at the eaves matters in Ohio’s snowbelt; see our <a href="/appraisal-practice/ice-dam-frozen-pipe-appraisal/">ice dam appraisal</a> page.</li></ul>
<p>Footprint math is a sanity check. Roofs with several pitches, dormers or turrets need measuring plane by plane or an aerial measurement report.</p>
""",
        "faqs": [
            ("What is a roofing square?", "One square is 100 square feet of roof surface. Shingles are usually sold three bundles to the square."),
            ("Does this work for slate roofs?", "The area math is the same for any roofing material. Slate pricing and repair methods are very different from asphalt, so use a slate contractor’s price per square if you enter one."),
            ("Why ask how many stories?", "Slopes two or more stories above the ground commonly carry an extra labor charge for safety equipment and handling. The tool flags it so you can check the estimate."),
        ],
    },
    {
        "slug": "percentage-deductible-calculator", "name": "Percentage Deductible Calculator", "icon": "pct", "kind": "Calculator", "kw": "percentage deductible calculator",
        "short": "See a 1%, 2% or 5% wind/hail deductible in dollars and what each would leave a claim paying.",
        "title": "Percentage Deductible Calculator | Wind & Hail",
        "desc": "Percentage deductible calculator: see 1%, 2% and 5% wind and hail deductibles in real dollars next to a flat deductible, and what a claim would pay.",
        "h1": "Percentage Deductible Calculator for Wind and Hail Claims",
        "lede": "A 2% deductible sounds small until it’s multiplied by your dwelling limit. Enter Coverage A and a storm estimate to compare flat, 1%, 2% and 5% deductibles at a glance.",
        "markup": DEDUCT,
        "explain": """
<h2>Where percentage deductibles show up</h2>
<p>Some Ohio homeowner policies carry a separate wind/hail deductible written as a percentage of Coverage A, while all other perils keep a flat dollar deductible. On a $310,000 dwelling limit (an illustrative figure), 2% is $6,200 — six times a typical $1,000 deductible.</p>
<h2>Finding yours</h2>
<p>Look on the declarations page for “wind/hail,” “windstorm or hail” or a percentage next to the deductible line, then read the endorsement that defines when it applies. If you can’t tell, ask your agent in writing.</p>
<h2>Why it matters before appraisal</h2>
<p>The deductible doesn’t change the amount of loss a panel decides, but it changes what lands in your account. A dispute worth $4,000 on a claim sitting just above a $6,200 deductible might not be worth appraisal costs; the <a href="/appraisal-workbench/claim-gap-fee-estimator/">claim gap &amp; fee estimator</a> helps you test that.</p>
""",
        "faqs": [
            ("Is the percentage taken from the claim amount?", "Usually no. It is calculated from the Coverage A dwelling limit on the declarations page, then subtracted from the covered loss."),
            ("Does a percentage deductible apply to tornado damage?", "If the policy’s wind/hail deductible covers windstorm, it generally applies to tornado and straight-line wind losses too. The endorsement wording controls."),
            ("Can I switch back to a flat deductible?", "Often at renewal, if the insurer offers it. Expect the premium to change; ask your agent to quote both."),
        ],
    },
    {
        "slug": "claim-calendar-builder", "name": "Ohio Claim Calendar Builder", "icon": "cal", "kind": "Planner", "kw": "insurance claim deadline calculator",
        "short": "Build a dated timeline from your date of loss and appraisal demand, then export it to your calendar.",
        "title": "Insurance Claim Deadline Calculator for Ohio",
        "desc": "Insurance claim deadline calculator for Ohio: map notice, proof of loss, holdback, appraiser and suit dates from your date of loss, then export .ics.",
        "h1": "Ohio Insurance Claim Deadline Calculator and Calendar",
        "lede": "Policy deadlines keep running while you argue about a number. Enter the date of loss — and the appraisal demand date if there is one — to build a timeline you can drop into any calendar.",
        "markup": DATES,
        "explain": """
<h2>The dates on the calendar</h2>
<ul><li><strong>Notice.</strong> Policies ask for prompt notice of a loss. Late reporting is one of the most common reasons claims get harder.</li>
<li><strong>Temporary repairs.</strong> Tarping and water extraction protect the property and the claim; keep every receipt.</li>
<li><strong>Proof of loss.</strong> If the insurer asks for a sworn proof of loss, many policies allow 60 days from the request.</li>
<li><strong>Depreciation recovery.</strong> Replacement-cost policies usually set a window to finish repairs and claim the holdback. Check the number of days in yours.</li>
<li><strong>Appraiser selection.</strong> Many appraisal clauses give each side about 20 days after a written demand to name its appraiser. Enter the demand date to add it.</li>
<li><strong>Suit limitation.</strong> Many Ohio homeowner policies limit lawsuits to one year after the loss, and Ohio courts generally enforce those clauses. Appraisal doesn’t automatically pause that clock.</li></ul>
<div class="note"><b class="h">Not legal advice</b>The calendar uses the numbers you enter. Courts can read policy deadlines differently. If a date is close, talk to an Ohio attorney now rather than later.</div>
<p>Related: <a href="/appraisal-timeline/">how the appraisal timeline works</a>.</p>
""",
        "faqs": [
            ("Is the date of loss the day I found the damage?", "Usually it is the date of the storm or event, not the day you noticed it. Weather records for your address can help pin it down."),
            ("Does demanding appraisal stop the one-year suit clock?", "Not automatically. Some policies or written agreements address it, many don’t. Treat the suit date as live and get legal advice before it gets close."),
            ("What does the .ics file work with?", "Google Calendar, Apple Calendar and Outlook all import .ics files. The file is built in your browser and never sent to us."),
        ],
    },
    {
        "slug": "appraisal-readiness-checkup", "name": "Appraisal Readiness Checkup", "icon": "chk", "kind": "Checklist", "kw": "appraisal readiness checklist",
        "short": "Ten yes/no questions that score your claim file and build a to-do list before you demand appraisal.",
        "title": "Appraisal Readiness Checklist | 10-Question Score",
        "desc": "Appraisal readiness checklist: answer ten yes-or-no questions to score your property claim file and get a to-do list before you demand appraisal.",
        "h1": "Appraisal Readiness Checklist and Score",
        "lede": "Appraisals are usually decided by the file you bring in. Answer ten quick questions to score yours and see what to fix before anyone signs a demand.",
        "markup": READY,
        "explain": """
<h2>How the score is weighted</h2>
<p>Coverage, the two itemized estimates and early photos carry the most weight: without them appraisal is either the wrong tool or a weak one. Housekeeping items like organized correspondence still count, but they’re quicker to fix.</p>
<h2>What your number means</h2>
<ul><li><strong>75 or more:</strong> a solid file. The next step is a professional look at the dollar gap — see our <a href="/appraisal-practice/estimate-audit/">estimate audit</a>.</li>
<li><strong>45–74:</strong> work through the to-do list before demanding appraisal.</li>
<li><strong>Under 45:</strong> demanding now risks locking in a low award. Build the file first.</li></ul>
""",
        "faqs": [
            ("Are my answers saved?", "No. The checkup runs in your browser and nothing is stored or sent."),
            ("Does a high score mean I’ll win appraisal?", "No. It means your file has the pieces a panel expects. The award still depends on the evidence, the pricing and the people on the panel."),
            ("What should I do if coverage was denied?", "Appraisal generally decides the amount of a covered loss, not whether a loss is covered. For a denial, talk with an Ohio attorney."),
        ],
    },
    {
        "slug": "basement-backup-sublimit-calculator", "name": "Basement Backup Sublimit Calculator", "icon": "drop", "kind": "Calculator", "kw": "sewer backup coverage calculator",
        "short": "See how the cause of basement water and your backup endorsement limit change what a claim can pay.",
        "title": "Sewer Backup Coverage Calculator | Basement Claims",
        "desc": "Sewer backup coverage calculator for Ohio basements: see how the water’s cause, your endorsement limit and deductible change what a claim can pay.",
        "h1": "Sewer Backup Coverage Calculator for Ohio Basements",
        "lede": "In a finished Ohio basement, why the water came in matters as much as how much damage it did. Pick the cause and your endorsement limit to see where the coverage likely stops.",
        "markup": BACKUP,
        "explain": """
<h2>Why the cause decides the coverage</h2>
<p>A typical Ohio homeowners policy treats basement water in very different ways depending on the source:</p>
<ul><li><strong>Sudden pipe or appliance discharge</strong> is usually covered under the main policy, subject to the deductible and the policy’s conditions.</li>
<li><strong>Sewer or drain backup and sump pump failure</strong> are usually excluded unless you bought a water backup endorsement — and that endorsement normally has its own limit, often $5,000 to $25,000.</li>
<li><strong>Surface water and river flooding</strong> are excluded from homeowners policies; that’s what NFIP or private flood insurance is for, and flood policies limit basement coverage.</li>
<li><strong>Long-term seepage</strong> is commonly excluded as wear, maintenance or repeated leakage.</li></ul>
<h2>What the calculator assumes</h2>
<p>It applies the deductible once, caps a backup loss at the endorsement limit, and treats flood and seepage as outside the homeowners policy. For flood it applies the limit you enter, but real flood policies restrict which basement items are covered, so the flood result is optimistic. Policies differ; your endorsement may cover the deductible differently or include mitigation in the limit.</p>
<h2>Where appraisal fits</h2>
<p>Appraisal can settle how much a covered basement loss costs, but not which cause applies. If the insurer says the water was flood rather than backup, that’s a coverage question. Read more on our <a href="/appraisal-practice/water-damage-appraisal/">water damage appraisal</a> page.</p>
<div class="note"><b class="h">Illustrative only</b>Default numbers are examples. Check your declarations page for the actual endorsement limit.</div>
""",
        "faqs": [
            ("Is a sump pump failure the same as sewer backup?", "Many endorsements group them together as water that backs up through drains or overflows from a sump. Read the endorsement title and wording on your own policy."),
            ("Does the endorsement limit include water extraction?", "Often yes — dry-out and cleanup usually come out of the same limit as repairs, which is why small limits run out fast in finished basements."),
            ("Can appraisal raise my backup sublimit?", "No. Appraisal sets the amount of loss, but the policy limit still caps the payment. It can matter when the true loss is disputed and still under the limit."),
        ],
    },
]
