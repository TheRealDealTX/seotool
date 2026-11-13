"""Interactive claim tools: markup + explanatory copy. Logic lives in static/assets/js/app.js.
Every tool runs in the browser; nothing is sent or stored."""

C1, C2, C3 = "var(--stack-1)", "var(--stack-2)", "var(--stack-3)"

GAP_FULL = f"""
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Settlement gap estimator</span><i>Runs in your browser</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Carrier’s estimate, replacement cost</label><input id="g-ins" name="insurer" inputmode="decimal" value="22600"><span class="hint">The RCV total on the insurer’s estimate.</span></div>
        <div><label for="g-own">Your estimate, replacement cost</label><input id="g-own" name="yours" inputmode="decimal" value="37900"><span class="hint">Your contractor’s or an independent estimate.</span></div>
      </div>
      <div><label for="g-land">Where in the gap might the award land?</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% means the carrier’s number holds; 100% means your full number is awarded.</span></div>
      <div class="row2">
        <div><label for="g-ft">How your appraiser charges</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of the increase (%)</option><option value="hourly">Hourly (hours × rate)</option></select></div>
        <div><label for="g-fee">Fee, percent or hours</label><input id="g-fee" name="fee" inputmode="decimal" value="3000"></div>
      </div>
      <div data-hourly hidden><label for="g-rate">Hourly rate ($)</label><input id="g-rate" name="rate" inputmode="decimal" value="175"></div>
      <label class="check"><input type="checkbox" name="useump" checked> Add my half of an umpire’s fee</label>
      <div><label for="g-ump">Umpire’s total fee</label><input id="g-ump" name="umpire" inputmode="decimal" value="3600"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated net increase to you</small><b data-o="net">$0</b></div>
      <div class="stack" aria-hidden="true"><span style="background:{C1}"></span><span style="background:{C2}"></span><span style="background:{C3}"></span></div>
      <div class="legend"><span><i style="background:{C1}"></i>Carrier’s number</span><span><i style="background:{C2}"></i>Your net gain</span><span><i style="background:{C3}"></i>Appraisal costs</span></div>
      <div class="out-rows">
        <div><span>Amount in dispute</span><b data-o="gap">$0</b></div>
        <div><span>Gap as a share of the carrier’s estimate</span><b data-o="pct">—</b></div>
        <div><span>Projected award (RCV)</span><b data-o="award">$0</b></div>
        <div><span>Gross increase</span><b data-o="gain">$0</b></div>
        <div><span>Your appraisal costs</span><b data-o="cost">$0</b></div>
        <div><span>Costs as a share of the increase</span><b data-o="costpct">—</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

GAP_MINI = """
<div class="tool tool-mini" data-tool="gap">
  <div class="tool-head"><span>Quick gap check</span><i>No sign-up</i></div>
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
  <div class="tool-head"><span>RCV / ACV holdback calculator</span><i>Add a row per item</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th scope="col">Item</th><th scope="col">Replacement cost ($)</th><th scope="col">Age (yrs)</th><th scope="col">Life (yrs)</th><th scope="col">ACV</th><th scope="col"><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Asphalt shingle roof", 21400, 12, 25), ("Vinyl siding — two elevations", 7800, 15, 30), ("Plaster ceiling & paint — second floor", 4300, 20, 50)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn line small" data-add data-run>+ Add item</button></div>
      <div class="row2">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="1500"></div>
        <div><label for="d-cap">Depreciation cap</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="60">60%</option><option value="75" selected>75%</option><option value="80">80%</option><option value="90">90%</option></select><span class="hint">Estimates often cap how much an item can depreciate.</span></div>
      </div>
      <label class="check"><input type="checkbox" name="nonrec"> My policy pays actual cash value only (depreciation isn’t recoverable)</label>
    </div>
    <div class="tool-out tool-out-grid" aria-live="polite">
      <div class="out-big"><small>First payment (ACV − deductible)</small><b data-o="first">$0</b></div>
      <div class="out-big"><small>Held back until repairs</small><b data-o="held">$0</b></div>
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
  <div class="tool-head"><span>Roof area &amp; pitch converter</span><i>Check the squares on your estimate</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <fieldset class="bare"><legend class="sr-only">Measurement method</legend>
        <div class="btn-row">
          <label class="check"><input type="radio" name="mode" value="dims" checked> Footprint length × width</label>
          <label class="check"><input type="radio" name="mode" value="area"> I know the footprint area</label>
        </div></fieldset>
      <div class="row2" data-mode="dims">
        <div><label for="r-l">Footprint length (ft)</label><input id="r-l" name="len" inputmode="decimal" value="44"></div>
        <div><label for="r-w">Footprint width (ft)</label><input id="r-w" name="wid" inputmode="decimal" value="28"></div>
      </div>
      <div data-mode="dims"><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="10"></div>
      <div data-mode="area" hidden><label for="r-a">Footprint area including overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="1450"></div>
      <div class="row2">
        <div><label for="r-p">Roof pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 9 else "", p) for p in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 18]) + """</select><span class="hint">Capes and colonials here often run 8/12 to 12/12.</span></div>
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="10">10% — simple gable</option><option value="14" selected>14% — gable with dormers</option><option value="15">15% — hip roof</option><option value="20">20% — cut-up / turrets</option></select></div>
      </div>
      <div><label for="r-pr">Installed price per square (optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 640"><span class="hint">Use a local contractor’s quote for a rough figure.</span></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Roof squares before waste</small><b data-o="sq">0</b></div>
      <div class="out-rows">
        <div><span>Pitch multiplier</span><b data-o="mult">1.000</b></div>
        <div><span>Roof pitch angle</span><b data-o="deg">0°</b></div>
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
  <div class="tool-head"><span>Hurricane deductible calculator</span><i>Percentage vs. standard</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling coverage (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="465000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Hurricane / named-storm deductible</label><select id="w-p" name="pct"><option value="1">1%</option><option value="2" selected>2%</option><option value="3">3%</option><option value="5">5%</option><option value="10">10%</option></select></div>
        <div><label for="w-f">Standard (all-other-perils) deductible</label><input id="w-f" name="flat" inputmode="decimal" value="1000"></div>
      </div>
      <div><label for="w-l">Estimated wind damage</label><input id="w-l" name="loss" inputmode="decimal" value="27500"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Hurricane deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span style="background:{C3}"></span><span style="background:{C2}"></span></div>
      <div class="legend"><span><i style="background:{C3}"></i>You pay</span><span><i style="background:{C2}"></i>Policy pays</span></div>
      <div class="out-rows">
        <div><span>Payment with the hurricane deductible</span><b data-o="pdpay">$0</b></div>
        <div><span>Payment if the standard deductible applied</span><b data-o="flatpay">$0</b></div>
        <div><span>Extra out of pocket</span><b data-o="diff">$0</b></div>
        <div><span>Damage needed before the policy pays</span><b data-o="break">$0</b></div>
      </div>
      <p class="out-msg" data-o="below"></p>
    </div>
  </div>
</div>"""

DATES = """
<div class="tool" data-tool="dates">
  <div class="tool-head"><span>Claim timeline builder</span><i>Export to your calendar</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
      <div><label for="t-r2">Date the carrier requested a proof of loss (optional)</label><input id="t-r2" type="date" name="req"><span class="hint">If set, the proof-of-loss date counts from this request.</span></div>
      <p class="hint flush">Change each window to match your policy. These defaults are common figures, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report the claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="2"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="10"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"></div>
        <div><label for="t-a">Name an appraiser within (days of a demand)</label><input id="t-a" name="appr" inputmode="numeric" value="20"></div>
        <div><label for="t-rc">Depreciation recovery (days)</label><input id="t-rc" name="rcd" inputmode="numeric" value="180"></div>
        <div><label for="t-s">Suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="730"><span class="hint">Two years = 730 days. Confirm in your policy.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download .ics calendar file</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the insurer accepted coverage for at least part of the loss?", "Get written confirmation that coverage is accepted. If the claim was denied, talk to a Rhode Island attorney before thinking about appraisal."),
    (3, "Do you have the carrier’s complete, itemized estimate?", "Ask in writing for the full line-item estimate, not just the summary page."),
    (3, "Do you have your own itemized estimate?", "Get an independent line-item estimate. A one-line contractor bid won’t hold up in front of a panel."),
    (2, "Do you have dated photos taken soon after the loss?", "Collect every photo and note when each was taken. Add photos of current conditions."),
    (2, "Have you read the appraisal paragraph in your policy?", "Find ‘Appraisal’ in the policy conditions and note any timelines."),
    (2, "Do you know which deductible applies (standard or hurricane)?", "Check the declarations page and the hurricane deductible endorsement, then run our hurricane deductible calculator."),
    (2, "Have temporary repairs been made and receipts kept?", "Make reasonable temporary repairs, such as tarping or water extraction, and keep every receipt."),
    (2, "Has hidden damage been opened up and documented?", "Make sure wet walls, attics, insulation and roof decking have been checked so the scope is complete."),
    (2, "If the storm brought water, have you separated wind damage from flood damage?", "Mark flood water lines and list wind and rain damage separately. Our wind vs. flood splitter can help."),
    (1, "Is your correspondence with the carrier in date order?", "Gather emails, letters and claim notes in one dated file."),
    (2, "Is the gap more than about 10% of the carrier’s estimate, or several thousand dollars?", "Run the settlement gap estimator. A small gap may not justify appraisal costs."),
    (1, "Do you know your policy’s suit-limitation date?", "Find the ‘Suit Against Us’ condition and put the date on your calendar."),
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
      <div class="btn-row"><button type="button" class="btn line small" data-reset>Reset answers</button></div>
    </div>
    <div class="tool-out ready-out" aria-live="polite">
      <div class="gauge"><svg viewBox="0 0 100 100" width="160" height="160" aria-hidden="true"><circle cx="50" cy="50" r="40" fill="none" stroke="var(--line)" stroke-width="10"/><circle data-o="arc" cx="50" cy="50" r="40" fill="none" stroke="var(--sun)" stroke-width="10" stroke-linecap="round" stroke-dasharray="251.3" stroke-dashoffset="251.3" transform="rotate(-90 50 50)"/></svg><div class="gauge-n"><b data-o="score">–</b><small>score</small></div></div>
      <div><p class="out-msg" data-o="verdict"></p><p class="hint">Answered: <span data-o="count">0 / 12</span></p><p class="todo-t">To do before appraisal</p><ul class="todo" data-o="todo"></ul></div>
    </div>
  </div>
</div>"""

_SPLIT_ROW = """<tr><td><input name="item" value="{0}" aria-label="Damaged item"></td><td><input name="amt" inputmode="decimal" value="{1}" aria-label="Repair cost"></td><td><select name="cause" aria-label="Cause">{2}</select></td><td><input name="wpct" inputmode="decimal" value="{3}" aria-label="Wind share percent"></td><td><button type="button" class="x" aria-label="Remove row">×</button></td></tr>"""
_CAUSES = [("wind", "Wind / wind-driven rain"), ("flood", "Flood / storm surge"), ("mixed", "Mixed — set wind %")]


def _cause_opts(sel):
    return "".join(f'<option value="{v}"{" selected" if v == sel else ""}>{t}</option>' for v, t in _CAUSES)


SPLIT = f"""
<div class="tool tool-wide" data-tool="split">
  <div class="tool-head"><span>Wind vs. flood damage splitter</span><i>Organize a mixed coastal loss</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th scope="col">Damaged item</th><th scope="col">Repair cost ($)</th><th scope="col">Cause</th><th scope="col">Wind share (%)</th><th scope="col"><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_SPLIT_ROW.format(i, a, _cause_opts(c), w) for i, a, c, w in [("Roof shingles & underlayment", 14800, "wind", 100), ("First-floor drywall & flooring", 23500, "flood", 0), ("Second-floor ceiling (rain through roof)", 3900, "wind", 100), ("Exterior siding", 6200, "mixed", 60)]) + f"""
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn line small" data-add data-run>+ Add item</button></div>
      <div class="row2">
        <div><label for="s-cova">Dwelling coverage (Coverage A)</label><input id="s-cova" name="cova" inputmode="decimal" value="420000"></div>
        <div><label for="s-hp">Hurricane deductible</label><select id="s-hp" name="hpct"><option value="0">Not triggered — use standard</option><option value="1">1%</option><option value="2" selected>2%</option><option value="3">3%</option><option value="5">5%</option></select></div>
      </div>
      <div class="row2">
        <div><label for="s-std">Standard homeowner deductible</label><input id="s-std" name="std" inputmode="decimal" value="1000"></div>
        <div><label for="s-fd">Flood policy deductible</label><input id="s-fd" name="fded" inputmode="decimal" value="2000"></div>
      </div>
    </div>
    <div class="tool-out tool-out-grid" aria-live="polite">
      <div class="out-big"><small>Homeowner (wind) portion</small><b data-o="wind">$0</b></div>
      <div class="out-big"><small>Flood portion</small><b data-o="flood">$0</b></div>
      <div class="stack span-all" aria-hidden="true"><span style="background:{C2}"></span><span style="background:{C1}"></span></div>
      <div class="legend span-all"><span><i style="background:{C2}"></i>Wind / rain</span><span><i style="background:{C1}"></i>Flood / surge</span></div>
      <div class="out-rows span-all">
        <div><span>Homeowner deductible used</span><b data-o="hded">$0</b></div>
        <div><span>Homeowner policy, after deductible</span><b data-o="hnet">$0</b></div>
        <div><span>Flood policy, after deductible</span><b data-o="fnet">$0</b></div>
        <div><span>Total you carry in deductibles</span><b data-o="ded">$0</b></div>
      </div>
      <p class="out-msg span-all" data-o="msg"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "settlement-gap-estimator", "name": "Settlement Gap Estimator", "kind": "Estimator", "icon": "$",
        "short": "See the disputed amount, a projected award and what appraisal fees would leave you.",
        "h1": "Settlement Gap Estimator for Rhode Island Claims",
        "lede": "Enter the carrier’s estimate and yours, pick a fee arrangement and see what a realistic appraisal result might look like after costs.",
        "markup": GAP_FULL,
        "title": "Settlement Gap Estimator | Appraisal Fees & Net",
        "desc": "Free settlement gap estimator: compare the carrier’s estimate with yours, project an award and subtract appraisal and umpire fees to see the net.",
        "explain": """
<h2>How the estimator works</h2>
<p>The disputed amount is your replacement cost estimate minus the carrier’s. Appraisal panels rarely award either side’s full number, so the slider lets you choose where in that gap an award might land. The estimator then subtracts your appraiser’s fee, whether flat, a percentage of the increase or hourly, and, if you choose, half of an umpire’s fee.</p>
<h2>Reading the result</h2>
<ul>
<li><strong>Net increase</strong> is what you might gain after appraisal costs at the inputs you chose.</li>
<li><strong>Costs as a share of the increase</strong> shows how much of the gain fees would absorb.</li>
<li>If the gap is small, a documented supplement request to the carrier may close it faster and for less.</li>
</ul>
<p>All figures are illustrative. They aren’t a prediction of any award.</p>""",
        "faqs": [("What’s a typical appraisal outcome?", "There isn’t one. Results depend on the documentation and the facts. That’s why the slider lets you test a range."), ("Should I include the umpire?", "Many appraisals settle between the two appraisers without an umpire. Including half an umpire fee gives you a more cautious estimate."), ("Does the estimator use ACV or RCV?", "It uses replacement cost totals. Use the RCV / ACV holdback calculator to see how depreciation affects payments.")],
    },
    {
        "slug": "rcv-acv-holdback-calculator", "name": "RCV / ACV Holdback Calculator", "kind": "Calculator", "icon": "%",
        "short": "Itemize depreciation and see the first payment, the holdback and the total once repairs are done.",
        "h1": "RCV and ACV Depreciation Holdback Calculator",
        "lede": "Most replacement cost policies pay actual cash value first and hold back depreciation until repairs are done. See both figures item by item.",
        "markup": DEP,
        "title": "RCV / ACV Depreciation Holdback Calculator",
        "desc": "Free RCV and ACV calculator: itemize depreciation by age and life, apply a cap and deductible, and see the first payment and the holdback.",
        "explain": """
<h2>How depreciation is estimated here</h2>
<p>For each item, depreciation is the item’s age divided by its expected life, multiplied by its replacement cost, up to the cap you choose. Actual cash value is replacement cost minus depreciation. The first payment is ACV minus your deductible.</p>
<h2>Recoverable depreciation</h2>
<p>Many replacement cost policies let you recover the held-back depreciation after repairs are completed, often within a set number of days. Some policies, especially on roofs or older homes, pay actual cash value only. Tick the box if yours does.</p>
<h3>Questions to ask about depreciation</h3>
<ul><li>Was labor depreciated, or only materials?</li><li>Is the age right? Roofs and siding are often older or newer than the estimate assumes.</li><li>Is the expected life realistic for the material?</li></ul>""",
        "faqs": [("Is depreciation the same as wear and tear?", "Not exactly. Depreciation is an estimate of lost value due to age and condition. Wear and tear itself usually isn’t covered damage."), ("Can depreciation be disputed in appraisal?", "Where the policy and the panel treat actual cash value as part of the amount of loss, depreciation can be part of the discussion."), ("How long do I have to recover depreciation?", "Your policy sets the deadline. Check the loss settlement condition, then put the date in the claim timeline builder.")],
    },
    {
        "slug": "roof-area-pitch-converter", "name": "Roof Area & Pitch Converter", "kind": "Calculator", "icon": "◭",
        "short": "Turn a footprint and pitch into roof squares, waste, bundles and a rough replacement cost.",
        "h1": "Roof Area and Pitch Converter: Squares, Waste, Bundles",
        "lede": "Rhode Island’s capes and colonials often have steep roofs. Check how pitch and waste change the squares on your estimate.",
        "markup": ROOF,
        "title": "Roof Area & Pitch Converter | Squares & Waste",
        "desc": "Free roof area and pitch converter: turn a footprint and pitch into roof squares, waste, bundles and a rough cost to compare with your estimate.",
        "explain": """
<h2>The math</h2>
<p>A roof’s surface is larger than its footprint because it slopes. The pitch multiplier is the square root of 1 + (rise ÷ 12)². Multiply the footprint, including overhangs, by that factor to get the surface area, then divide by 100 for squares. Waste covers cutting at hips, valleys and dormers.</p>
<h2>Why it matters</h2>
<p>A difference of a few squares, or a waste factor that’s too low for a cut-up roof, adds up quickly. Steep pitches usually also carry steep charges in estimating software, and two-story or three-story roofs may carry high charges.</p>
<p>This converter treats the roof as a single plane over the footprint. Complex roofs should be measured slope by slope.</p>""",
        "faqs": [("What is a roofing square?", "One square is 100 square feet of roof surface."), ("Why does my estimate show more squares than my footprint?", "Pitch and waste both increase the quantity. A 12/12 roof has about 41% more surface than its footprint."), ("When do steep charges apply?", "Estimating software commonly adds steep charges starting around 7/12 or 8/12, and more at higher pitches. Check how your estimate treats your pitch.")],
    },
    {
        "slug": "hurricane-deductible-calculator", "name": "Hurricane Deductible Calculator", "kind": "Calculator", "icon": "◎",
        "short": "Convert a percentage hurricane deductible into dollars and compare it with your standard deductible.",
        "h1": "Hurricane Deductible Calculator for Rhode Island Policies",
        "lede": "Many Rhode Island policies use a percentage deductible for hurricanes or named storms. See what yours means in dollars.",
        "markup": DEDUCT,
        "title": "Hurricane Deductible Calculator | Rhode Island",
        "desc": "Free hurricane deductible calculator for Rhode Island: turn a percentage deductible into dollars and compare payments with your standard deductible.",
        "explain": """
<h2>How percentage deductibles work</h2>
<p>A hurricane or named-storm deductible is usually a percentage of your dwelling coverage, not of the loss. A 2% deductible on $465,000 of dwelling coverage is $9,300, whatever the size of the claim. The policy pays only the amount above that.</p>
<h2>When it applies</h2>
<p>Your policy defines the trigger: often a hurricane or named storm, sometimes tied to National Weather Service or National Hurricane Center warnings and a time window around the storm. A nor’easter normally falls under the standard deductible. Read the deductible endorsement or ask us to look at it.</p>
<h3>Why the total loss still matters</h3>
<p>Because the deductible is fixed, every dollar of missed damage comes straight out of what you’re paid. Getting the full wind scope right matters more, not less, when a large deductible applies.</p>""",
        "faqs": [("Is a hurricane deductible the same as a windstorm deductible?", "Not always. Some policies use a separate wind/hail deductible; others apply a percentage only to named storms or hurricanes. The policy wording controls."), ("Does it apply to inland homes?", "If the trigger is met, a hurricane deductible usually applies wherever the house is located within the state."), ("Can I change my deductible?", "Options depend on your insurer and location. Talk to your agent before the next storm season.")],
    },
    {
        "slug": "claim-timeline-builder", "name": "Claim Timeline Builder", "kind": "Planner", "icon": "▦",
        "short": "Build a dated list of claim milestones from your date of loss and download it as a calendar file.",
        "h1": "Claim Timeline Builder with Calendar Export",
        "lede": "Enter your date of loss, adjust the windows to match your policy and download every milestone to your calendar.",
        "markup": DATES,
        "title": "Claim Timeline Builder | Calendar (.ics) Export",
        "desc": "Free claim timeline builder: enter your date of loss, match your policy’s windows and download claim milestones as an .ics calendar file.",
        "explain": """
<h2>What the timeline includes</h2>
<ul>
<li>A target date for reporting the claim. Policies require prompt notice.</li>
<li>Temporary repairs to protect the property from further damage</li>
<li>Proof of loss, counted from the carrier’s request if you enter one</li>
<li>A reminder window for naming an appraiser after a demand, if your policy sets one</li>
<li>The deadline to recover held-back depreciation</li>
<li>The policy’s suit-limitation date</li>
</ul>
<h2>Important</h2>
<p>These defaults are common figures, not Rhode Island legal deadlines. Your policy, and in some cases state law, controls. If a suit-limitation date is approaching, consult a Rhode Island attorney promptly. Nothing you enter leaves your browser.</p>""",
        "faqs": [("Is the two-year suit limit a rule in Rhode Island?", "Many property policies here use two years from the date of loss, but you need to check your own policy. An attorney can confirm what applies."), ("Does the .ics file work with my phone?", "Yes. Most calendar apps, including Google, Apple and Outlook calendars, can import .ics files."), ("Is anything saved?", "No. The timeline is built in your browser, and the calendar file is created on your device.")],
    },
    {
        "slug": "appraisal-readiness-checkup", "name": "Appraisal Readiness Checkup", "kind": "Checklist", "icon": "✓",
        "short": "Twelve yes-or-no questions that score how prepared your file is for an appraisal panel.",
        "h1": "Appraisal Readiness Checkup: Is Your Claim File Ready?",
        "lede": "Answer twelve questions to see how ready your claim is for appraisal and get a to-do list for anything missing.",
        "markup": READY,
        "title": "Appraisal Readiness Checkup | 12-Question Score",
        "desc": "Free appraisal readiness checkup: answer 12 questions about your claim file, get a score and a to-do list of documents to gather before appraisal.",
        "explain": """
<h2>Why readiness matters</h2>
<p>An appraisal award is binding on the amount of loss once two members of the panel sign. If your documentation is thin when appraisal starts, the result can be lower than it should be, and it’s hard to undo. The checkup weights the items that matter most: accepted coverage, both itemized estimates and photos.</p>
<h2>How the score works</h2>
<p>Each question has a weight from one to three. Your score is the share of weighted points answered “yes.” A “no” adds an item to your to-do list.</p>""",
        "faqs": [("What score should I aim for?", "Above about 75 means the essentials are in place. Below that, work through the to-do list first."), ("Can I invoke appraisal with a low score?", "You can, but it’s risky. Gaps in documentation tend to work against the party with the burden of showing the damage."), ("Is my information stored?", "No. Answers stay in your browser.")],
    },
    {
        "slug": "wind-flood-damage-splitter", "name": "Wind vs. Flood Damage Splitter", "kind": "Organizer", "icon": "≋",
        "short": "Sort a coastal storm loss into wind and flood portions, apply each deductible and see what each policy might pay.",
        "h1": "Wind vs. Flood Damage Splitter for Coastal Storm Claims",
        "lede": "After a hurricane or nor’easter, the same house can have wind damage and flood damage. List each item, tag the cause and see how the loss divides.",
        "markup": SPLIT,
        "title": "Wind vs. Flood Damage Splitter | Coastal Claims",
        "desc": "Free wind vs. flood damage splitter: tag each item by cause, apply homeowner, hurricane and flood deductibles and see how a coastal loss divides.",
        "explain": """
<h2>Why split the loss?</h2>
<p>Standard homeowner policies exclude flood, including storm surge. Wind and wind-driven rain damage may be covered by the homeowner policy, while rising water is covered, if at all, by a separate flood policy. Organizing the loss by cause before you meet either adjuster helps each claim go to the right place.</p>
<h2>How it works</h2>
<ul>
<li>Tag each item as wind, flood or mixed. For mixed items, enter the share you attribute to wind.</li>
<li>The homeowner portion uses the hurricane deductible if you choose one, otherwise your standard deductible.</li>
<li>The flood portion uses the flood policy deductible you enter.</li>
</ul>
<h3>A caution</h3>
<p>This is an organizing tool, not a coverage decision. Insurers and adjusters decide causation, and disputes about the cause of damage can fall outside appraisal. Flood policy limits and contents coverage are not modeled. Figures are illustrative.</p>""",
        "faqs": [("Who decides whether damage was caused by wind or flood?", "Each insurer investigates causation under its own policy. If the two disagree, a Rhode Island attorney can explain your options."), ("Does the National Flood Insurance Program have appraisal?", "NFIP policies contain their own appraisal provision with specific rules, separate from your homeowner policy."), ("Why is the hurricane deductible so large here?", "Because it’s a percentage of dwelling coverage, not of the loss. Use the hurricane deductible calculator to see the dollar figure.")],
    },
]
