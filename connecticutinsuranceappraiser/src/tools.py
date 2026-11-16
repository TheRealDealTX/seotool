"""Interactive claim tools: markup + explanatory copy. Logic lives in static/assets/js/app.js.
Tool headings use <p class="tool-t"> (not <h*>) so they never break the page's heading order."""

GAP_FULL = """
<div class="tool" data-tool="gap">
  <div class="tool-head"><span class="tool-t">Claim gap &amp; fee estimator</span><i>Runs in your browser</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Carrier’s estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="22600"><span class="hint">Replacement cost total before depreciation and deductible.</span></div>
        <div><label for="g-own">Your estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="38900"><span class="hint">Contractor or independent estimate, also at RCV.</span></div>
      </div>
      <div><label for="g-land">Where might the award land inside the gap?</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% = the carrier’s number holds. 100% = your full number is awarded.</span></div>
      <div class="row2">
        <div><label for="g-ft">Appraiser fee type</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of increase (%)</option><option value="hourly">Hourly (hours × rate)</option></select></div>
        <div><label for="g-fee">Fee amount or hours</label><input id="g-fee" name="fee" inputmode="decimal" value="2800"></div>
      </div>
      <div class="row2">
        <div><label for="g-rate">Hourly rate (if hourly)</label><input id="g-rate" name="rate" inputmode="decimal" value="175"></div>
        <div><label for="g-ump">Umpire’s total fee</label><input id="g-ump" name="umpire" inputmode="decimal" value="3200"></div>
      </div>
      <label class="check"><input type="checkbox" name="useump" checked> The panel needs an umpire (you pay half)</label>
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
  <div class="tool-head"><span class="tool-t">Two-number gap check</span><i>No sign-up</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="m-ins">Carrier’s estimate</label><input id="m-ins" name="insurer" inputmode="decimal" value="17300"></div>
      <div><label for="m-own">Your contractor’s estimate</label><input id="m-own" name="yours" inputmode="decimal" value="29800"></div>
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
  <div class="tool-head"><span class="tool-t">RCV vs. ACV holdback calculator</span><i>Add as many items as you need</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Asphalt shingle roof", 21400, 12, 25), ("Plaster ceiling & paint — dining room", 3900, 6, 15), ("Oak strip flooring refinish", 2650, 8, 20)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn line small" data-add data-run>+ Add item</button></div>
      <div class="row2">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="1000"></div>
        <div><label for="d-cap">Maximum depreciation</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="90">90%</option></select><span class="hint">Most estimates cap depreciation; check yours.</span></div>
      </div>
      <div class="row2">
        <div><label for="d-paid">Already paid by the carrier ($)</label><input id="d-paid" name="paid" inputmode="decimal" value="0"><span class="hint">Leave at 0 if nothing has been paid yet.</span></div>
        <div><label for="d-win">Days allowed to finish repairs</label><input id="d-win" name="window" inputmode="numeric" value="180"><span class="hint">Your policy’s window to claim holdback.</span></div>
      </div>
      <label class="check"><input type="checkbox" name="nonrec"> My policy pays actual cash value only (no recoverable depreciation)</label>
    </div>
    <div class="tool-out tool-out-3" aria-live="polite">
      <div class="out-big"><small>First check (ACV − deductible − paid)</small><b data-o="first">$0</b></div>
      <div class="out-big"><small>Held back until repairs</small><b data-o="held">$0</b></div>
      <div class="out-big"><small>Total if fully recovered</small><b data-o="total">$0</b></div>
      <div class="out-rows full-row">
        <div><span>Replacement cost (RCV)</span><b data-o="rcv">$0</b></div>
        <div><span>Total depreciation</span><b data-o="dep">$0</b></div>
        <div><span>Depreciation as share of RCV</span><b data-o="deppct">0%</b></div>
        <div><span>Actual cash value (ACV)</span><b data-o="acv">$0</b></div>
        <div><span>Finish repairs by (from today)</span><b data-o="by">—</b></div>
      </div>
    </div>
  </div>
</div>"""

ROOF = """
<div class="tool" data-tool="roof">
  <div class="tool-head"><span class="tool-t">Roof square &amp; pitch converter</span><i>Check the square count</i></div>
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
      <div data-mode="dims"><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="12"></div>
      <div data-mode="area" hidden><label for="r-a">Footprint area incl. overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="1650"></div>
      <div class="row2">
        <div><label for="r-p">Roof pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 9 else "", p) for p in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 18]) + """</select><span class="hint">Steep 9/12–12/12 roofs are common on Connecticut colonials and capes.</span></div>
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="10">10% — simple gable</option><option value="13" selected>13% — gable with dormers</option><option value="16">16% — hip roof</option><option value="20">20% — complex / cut-up</option></select></div>
      </div>
      <div class="row2">
        <div><label for="r-mat">Roofing material</label><select id="r-mat" name="mat"><option value="3">Asphalt shingles (3 bundles/sq)</option><option value="4">Heavy architectural (4 bundles/sq)</option><option value="0">Slate, cedar or metal (no bundles)</option></select></div>
        <div><label for="r-pr">Installed price per square (optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 640"></div>
      </div>
      <div><label for="r-est">Squares on the carrier’s estimate (optional)</label><input id="r-est" name="est" inputmode="decimal" placeholder="e.g. 16.5"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Roof squares (before waste)</small><b data-o="sq">0</b></div>
      <div class="out-rows">
        <div><span>Pitch multiplier</span><b data-o="mult">1.000</b></div>
        <div><span>Roof surface area</span><b data-o="surface">0</b></div>
        <div><span>Squares to order (with waste)</span><b data-o="order">0</b></div>
        <div><span>Bundles</span><b data-o="bundles">—</b></div>
        <div><span>Rough replacement cost</span><b data-o="cost">—</b></div>
        <div><span>Difference vs. carrier’s squares</span><b data-o="vs">—</b></div>
      </div>
      <p class="out-msg" data-o="steep"></p>
    </div>
  </div>
</div>"""

DEDUCT = """
<div class="tool" data-tool="deduct">
  <div class="tool-head"><span class="tool-t">Hurricane &amp; windstorm deductible calculator</span><i>Percentage vs. flat</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling coverage (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="465000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Hurricane / windstorm deductible</label><select id="w-p" name="pct"><option value="1">1%</option><option value="2" selected>2%</option><option value="3">3%</option><option value="5">5%</option><option value="10">10%</option></select></div>
        <div><label for="w-f">All-other-perils flat deductible</label><input id="w-f" name="flat" inputmode="decimal" value="1000"></div>
      </div>
      <div><label for="w-l">Estimated storm damage</label><input id="w-l" name="loss" inputmode="decimal" value="27500"></div>
      <label class="check"><input type="checkbox" name="trig" checked> The policy’s hurricane trigger was met for this storm</label>
      <span class="hint">Triggers are often tied to an official hurricane warning or watch. If it wasn’t met, the flat deductible usually applies.</span>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Deductible that applies, in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s3"></span><span class="s1"></span></div>
      <div class="legend"><span><i class="s3"></i>You pay</span><span><i class="s1"></i>Policy pays</span></div>
      <div class="out-rows">
        <div><span>Percentage deductible in dollars</span><b data-o="pctd">$0</b></div>
        <div><span>Claim payment under this deductible</span><b data-o="pdpay">$0</b></div>
        <div><span>Payment if the flat deductible applied</span><b data-o="flatpay">$0</b></div>
        <div><span>Extra out-of-pocket from the percentage</span><b data-o="diff">$0</b></div>
      </div>
      <p class="out-msg" data-o="below"></p>
    </div>
  </div>
</div>"""

DATES = """
<div class="tool" data-tool="dates">
  <div class="tool-head"><span class="tool-t">Claim calendar builder</span><i>Exports an .ics file</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
      <p class="hint flush">Set each window to match your own policy. Defaults are planning placeholders, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report the claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="2"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="10"></div>
        <div><label for="t-i">Contents inventory target (days)</label><input id="t-i" name="inv" inputmode="numeric" value="45"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Often counted from the carrier’s request.</span></div>
        <div><label for="t-r">Depreciation recovery (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="180"></div>
        <div><label for="t-s">Suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="365"><span class="hint">Read your policy; periods vary by form.</span></div>
      </div>
      <label class="check"><input type="checkbox" name="remind" checked> Add a reminder 14 days before each date</label>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download .ics calendar file</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the insurer accepted coverage for at least part of the loss?", "Get written confirmation that coverage is accepted. If the claim was denied, talk to a Connecticut attorney before considering appraisal."),
    (3, "Do you have the carrier’s complete, line-item estimate?", "Ask in writing for the full itemized estimate, not just the payment summary."),
    (3, "Do you have your own itemized estimate from a contractor or estimator?", "Get an independent line-item estimate. A one-line lump-sum bid won’t hold up in front of a panel."),
    (2, "Do you have dated photos taken soon after the loss?", "Collect every photo and note when each was taken. Add new photos of current conditions."),
    (2, "Have you found and read the appraisal clause in your policy?", "Look in the policy conditions for the paragraph titled “Appraisal” and note any time limits."),
    (2, "Do you know your policy’s suit-limitation period?", "Find the “Suit Against Us” condition and put the date on your calendar. Our claim calendar builder can help."),
    (2, "Were temporary repairs made, with receipts saved?", "Tarp, dry out or board up as needed and keep every invoice."),
    (1, "Do you have your current declarations page?", "Download it from your insurer’s portal or ask your agent."),
    (2, "Has hidden damage been opened up and documented?", "Make sure attics, wall cavities, subfloors and decking have been checked so the scope is complete."),
    (1, "Is your correspondence with the carrier organized by date?", "Gather letters, emails and claim notes in date order."),
    (2, "Is the gap more than about 10% or several thousand dollars?", "Run the claim gap & fee estimator. A small gap may not justify appraisal costs."),
    (1, "If a sworn proof of loss was requested, was it submitted on time?", "Submit any requested proof of loss before the deadline in the carrier’s letter."),
]

READY = """
<div class="tool tool-wide" data-tool="ready">
  <div class="tool-head"><span class="tool-t">Appraisal readiness checkup</span><i>12 questions · about two minutes</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <ol class="quiz">""" + "".join(
    '<li data-w="%d" data-fix="%s"><span>%s</span><span class="yn"><button type="button" class="yes" aria-pressed="false">Yes</button><button type="button" class="no" aria-pressed="false">No</button></span></li>' % (w, f, q)
    for w, q, f in _QUIZ) + """
      </ol>
      <div class="btn-row"><button type="button" class="btn line small" data-reset>Reset answers</button></div>
    </div>
    <div class="tool-out tool-out-gauge" aria-live="polite">
      <div>
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#e3eafb" stroke-width="18"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#1F64E5" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3" style="transition:stroke-dashoffset .5s,stroke .3s"/></svg>
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

TREE = """
<div class="tool" data-tool="tree">
  <div class="tool-head"><span class="tool-t">Fallen tree claim calculator</span><i>Structure vs. debris removal</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="tr-hit">Trees that hit a covered structure</label><input id="tr-hit" name="hit" inputmode="numeric" value="1"></div>
        <div><label for="tr-blk">Trees blocking a driveway or ramp</label><input id="tr-blk" name="blk" inputmode="numeric" value="1"></div>
      </div>
      <div class="row2">
        <div><label for="tr-yard">Trees down that hit nothing</label><input id="tr-yard" name="yard" inputmode="numeric" value="1"></div>
        <div><label for="tr-cost">Haul-away cost per tree ($)</label><input id="tr-cost" name="cost" inputmode="decimal" value="1400"></div>
      </div>
      <div class="row2">
        <div><label for="tr-per">Debris limit per tree ($)</label><input id="tr-per" name="per" inputmode="decimal" value="500"><span class="hint">Common homeowners forms use $500.</span></div>
        <div><label for="tr-tot">Debris limit per loss ($)</label><input id="tr-tot" name="tot" inputmode="decimal" value="1000"><span class="hint">Often $1,000 per occurrence.</span></div>
      </div>
      <div class="row2">
        <div><label for="tr-crane">Removing tree from the house, incl. crane ($)</label><input id="tr-crane" name="crane" inputmode="decimal" value="3800"><span class="hint">Usually part of the dwelling loss, not the debris limit.</span></div>
        <div><label for="tr-rep">Structure repairs ($)</label><input id="tr-rep" name="rep" inputmode="decimal" value="24500"></div>
      </div>
      <div><label for="tr-ded">Deductible ($)</label><input id="tr-ded" name="ded" inputmode="decimal" value="1000"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated claim payment (illustrative)</small><b data-o="pay">$0</b></div>
      <div class="out-rows">
        <div><span>Dwelling loss (removal from house + repairs)</span><b data-o="dwell">$0</b></div>
        <div><span>Debris removal you’re billed</span><b data-o="billed">$0</b></div>
        <div><span>Debris removal the limits allow</span><b data-o="allowed">$0</b></div>
        <div><span>Tree cleanup likely on you</span><b data-o="oop">$0</b></div>
      </div>
      <p class="out-msg" data-o="tmsg"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "claim-gap-fee-estimator", "name": "Claim Gap & Fee Estimator", "icon": "Δ", "kind": "Calculator",
        "kw": "insurance appraisal cost calculator",
        "short": "Size the dispute, project an award and subtract flat, percentage or hourly appraisal fees to see your net.",
        "title": "Claim Gap & Appraisal Fee Estimator | Free Calculator",
        "desc": "Free insurance appraisal cost calculator: size the gap, project an award and subtract flat, percentage or hourly fees to see your real net.",
        "h1": "Claim Gap and Appraisal Fee Estimator",
        "lede": "Enter the carrier’s estimate and yours, pick where an award might land, and add realistic fees. The estimator shows your net, plus the break-even point where appraisal stops paying for itself.",
        "markup": GAP_FULL,
        "explain": """
<h2>How to use the estimator</h2>
<ol><li><strong>Enter both totals at replacement cost.</strong> Use RCV figures before depreciation and deductible, so you compare like with like.</li>
<li><strong>Move the slider.</strong> Test 30%, 50% and 75% to see a range of outcomes rather than one answer.</li>
<li><strong>Choose the fee arrangement</strong> your appraiser quoted: a flat fee, a percentage of the increase, or hours times a rate.</li>
<li><strong>Decide whether an umpire is likely.</strong> Many panels settle without one; complex claims often need one.</li></ol>
<h2>The break-even landing point</h2>
<p>This figure shows how far into the gap the award has to land before your costs are covered. If the break-even is 15%, almost any reasonable outcome helps. If it is 70%, the case only works if most of your number holds, which is a warning sign.</p>
<h2>What the estimator leaves out</h2>
<p>It ignores deductibles, depreciation timing, policy limits and sub-limits. Those change what you are paid, not the size of the dispute. For payment timing use the <a href="/ct-claim-tools/rcv-acv-holdback-calculator/">RCV vs. ACV holdback calculator</a>.</p>
""",
        "faqs": [("Is the projected award a prediction?", "No. It is a scenario you choose with the slider. Real awards depend on documentation, the panel and the policy."), ("Why offer an hourly option?", "Some appraisers bill by the hour, especially on commercial or umpire work. Enter the expected hours in the fee field and the rate in the hourly rate field.")],
    },
    {
        "slug": "rcv-acv-holdback-calculator", "name": "RCV vs. ACV Holdback Calculator", "icon": "ACV", "kind": "Calculator",
        "kw": "RCV vs ACV calculator",
        "short": "Split a replacement cost claim into the first ACV check and the depreciation held back, with a repair-by date.",
        "title": "RCV vs ACV Holdback Calculator | Depreciation Split",
        "desc": "Free RCV vs ACV calculator: list items with age and life to see the first check, recoverable depreciation held back and a repair-by date.",
        "h1": "RCV vs. ACV Holdback Calculator",
        "lede": "Replacement cost policies usually pay in two stages: an actual cash value check now and recoverable depreciation after repairs. List your items to see the split and the date you need to finish by.",
        "markup": DEP,
        "explain": """
<h2>How depreciation is estimated</h2>
<p>The calculator uses straight-line depreciation, which is age divided by expected life, capped at the maximum you choose. Real estimates may use condition adjustments, different life tables or non-depreciable items such as permits and debris removal, so treat the result as a planning figure.</p>
<h2>Typical life expectancies in estimates</h2>
<div class="table-wrap"><table><thead><tr><th>Item</th><th>Common range</th></tr></thead><tbody>
<tr><th>Asphalt architectural shingles</th><td>25–30 years</td></tr><tr><th>Slate roof</th><td>60–100+ years</td></tr><tr><th>Cedar shingle roof</th><td>20–30 years</td></tr><tr><th>Interior paint</th><td>8–12 years</td></tr><tr><th>Carpet</th><td>8–12 years</td></tr><tr><th>Hardwood flooring</th><td>Long life; refinishing 15–25 years</td></tr>
</tbody></table></div>
<h2>Getting the holdback released</h2>
<p>Most policies release recoverable depreciation once repairs are completed within a set time. Send final invoices and photos of the finished work. The <a href="/ct-claim-tools/claim-calendar-builder/">claim calendar builder</a> can remind you before that window closes.</p>
""",
        "faqs": [("Should labor be depreciated?", "Treatment of labor depreciation varies by policy, state and court decisions. Ask your carrier to explain its approach in writing and compare it with your policy."), ("What happens if I don’t repair?", "Under most replacement cost policies you keep the ACV payment but may not recover the held-back depreciation.")],
    },
    {
        "slug": "roof-square-pitch-converter", "name": "Roof Square & Pitch Converter", "icon": "▲", "kind": "Calculator",
        "kw": "roof squares calculator",
        "short": "Turn a footprint into true roof squares by pitch and waste, then compare against the carrier’s square count.",
        "title": "Roof Squares Calculator by Pitch | Check Your Estimate",
        "desc": "Free roof squares calculator: convert a footprint to true roof area by pitch and waste factor, then compare it with the carrier’s squares.",
        "h1": "Roof Square and Pitch Converter",
        "lede": "Measurement errors are one of the most common reasons roof claims come up short, especially on steep Connecticut colonials. Convert your footprint into true squares and compare.",
        "markup": ROOF,
        "explain": """
<h2>How the math works</h2>
<p>A pitched roof has more surface than the footprint under it. The pitch multiplier is √(1 + (rise ÷ 12)²). A 6/12 roof is about 11.8% larger than its footprint; a 9/12 roof is 25% larger; a 12/12 roof is about 41.4% larger.</p>
<h2>Checking your estimate</h2>
<ul><li>Find the roofing section of the carrier’s estimate and note the total squares and waste percentage.</li>
<li>Enter the carrier’s squares in the last field to see the difference instantly.</li>
<li>Look for steep-roof charges (often from 7/12 up) and high-roof charges for two-story walls.</li>
<li>Check that starter, ridge cap, drip edge, ice-and-water shield and valley metal are listed.</li></ul>
<h2>Limits of a footprint calculation</h2>
<p>Roofs with several pitches, dormers and valleys should be measured plane by plane. A field measurement or aerial report always beats a footprint estimate. Use this as a sanity check.</p>
""",
        "faqs": [("What’s a roofing square?", "100 square feet of roof surface. Many Connecticut colonials have roughly 18 to 35 squares."), ("Why is ice-and-water shield important here?", "Connecticut’s building code generally requires an ice barrier at the eaves when a roof is replaced, so it belongs in a replacement estimate.")],
    },
    {
        "slug": "hurricane-deductible-calculator", "name": "Hurricane Deductible Calculator", "icon": "%", "kind": "Calculator",
        "kw": "hurricane deductible calculator Connecticut",
        "short": "Convert a percentage hurricane or windstorm deductible into dollars and see whether the trigger changes it.",
        "title": "Hurricane Deductible Calculator for Connecticut Policies",
        "desc": "Hurricane deductible calculator for Connecticut: convert a percentage deductible into dollars and see how the trigger changes your payout.",
        "h1": "Hurricane Deductible Calculator for Connecticut Policies",
        "lede": "A 2% hurricane deductible sounds small until you multiply it by your dwelling limit. See it in dollars, compare it with your flat deductible and test what happens if the trigger wasn’t met.",
        "markup": DEDUCT,
        "explain": """
<h2>How hurricane deductibles work in Connecticut</h2>
<p>Many Connecticut homeowners policies, especially near Long Island Sound, include a hurricane or windstorm deductible stated as a percentage of Coverage A. On a $465,000 dwelling limit, 2% is $9,300, not $1,000. Whether that deductible applies depends on the trigger in your policy, which is commonly tied to the National Weather Service issuing a hurricane warning or watch for part of Connecticut.</p>
<h2>Where to find yours</h2>
<p>Check the declarations page for a hurricane, windstorm or named-storm deductible, then read the endorsement that defines when it applies and for how long after the storm. The Connecticut Insurance Department publishes consumer guidance on these deductibles.</p>
<h2>How it affects appraisal</h2>
<p>The deductible doesn’t change the amount of loss the panel decides, but it changes what you receive. A loss just above a percentage deductible may not be worth disputing; one far above it may be.</p>
""",
        "faqs": [("Did Tropical Storm Isaias or Henri trigger hurricane deductibles?", "It depended on the policy wording and the official warnings issued at the time. Check your own policy’s trigger and the carrier’s explanation in writing."), ("Can I lower my hurricane deductible?", "Usually at renewal, by choosing a different option if your insurer offers one. A lower deductible typically raises the premium.")],
    },
    {
        "slug": "claim-calendar-builder", "name": "Claim Calendar Builder", "icon": "◷", "kind": "Planner",
        "kw": "insurance claim deadline calendar",
        "short": "Build a dated timeline of notice, inventory, proof-of-loss, holdback and suit dates and export it as .ics.",
        "title": "Insurance Claim Deadline Calendar | Free .ics Builder",
        "desc": "Free insurance claim deadline calendar: enter your date of loss to map inventory, proof of loss, holdback and suit dates, then export an .ics.",
        "h1": "Insurance Claim Deadline Calendar Builder",
        "lede": "Policy deadlines keep running while you argue about the number. Enter your date of loss and your policy’s windows, and download a calendar file with optional reminders two weeks ahead.",
        "markup": DATES,
        "explain": """
<h2>Dates worth tracking</h2>
<ul><li><strong>Prompt notice.</strong> Policies require you to report losses promptly. Late notice is a common carrier defense.</li>
<li><strong>Contents inventory.</strong> Carriers often ask for an inventory; set your own target so it doesn’t drift.</li>
<li><strong>Proof of loss.</strong> If the carrier requests a sworn proof of loss, the policy usually sets a time to return it, frequently 60 days from the request.</li>
<li><strong>Depreciation recovery.</strong> Replacement cost policies typically require repairs within a set period to collect holdback.</li>
<li><strong>Suit limitation.</strong> Connecticut policies contain a time limit for filing suit, which varies by form. Appraisal does not necessarily pause it.</li></ul>
<div class="note"><b class="h">Important</b>This planner only uses the numbers you enter. It isn’t legal advice, and courts can read policy deadlines differently. If a deadline is close, contact a Connecticut attorney.</div>
""",
        "faqs": [("Is the date of loss the day I noticed damage?", "Usually it is the date of the storm or event. Weather records for your address can help pin it down."), ("Does the .ics file work with Google, Apple and Outlook calendars?", "Yes. The file uses the standard iCalendar format that all major calendar apps import.")],
    },
    {
        "slug": "appraisal-readiness-checkup", "name": "Appraisal Readiness Checkup", "icon": "✓", "kind": "Checklist",
        "kw": "appraisal readiness checklist",
        "short": "Twelve yes/no questions score your claim file and build a to-do list before you demand appraisal.",
        "title": "Appraisal Readiness Checklist | Score Your Claim File",
        "desc": "A free appraisal readiness checklist: answer twelve questions to score your claim file and get a to-do list before you demand appraisal.",
        "h1": "Appraisal Readiness Checkup",
        "lede": "Strong appraisals are built before the demand letter goes out. Answer twelve questions to see how complete your file is and what to fix first.",
        "markup": READY,
        "explain": """
<h2>How the score is weighted</h2>
<p>Questions about coverage, estimates and evidence count most, because they decide whether appraisal is the right tool and how well your number will hold. Administrative items matter too, but they’re easier to fix.</p>
<h2>Reading your result</h2>
<ul><li><strong>75 and above:</strong> a solid file. A professional review of the gap is the logical next step.</li>
<li><strong>45 to 74:</strong> close the open items first. Each one strengthens your position.</li>
<li><strong>Below 45:</strong> demanding appraisal now risks locking in a low number. Build the file first.</li></ul>
""",
        "faqs": [("Is anything saved or sent?", "No. The checkup runs entirely in your browser and nothing is stored."), ("Can I bring my result to a consultation?", "Yes. A screenshot of the to-do list is a helpful starting point.")],
    },
    {
        "slug": "fallen-tree-claim-calculator", "name": "Fallen Tree Claim Calculator", "icon": "⌂", "kind": "Calculator",
        "kw": "fallen tree insurance claim calculator",
        "short": "Separate tree removal from the house, structure repairs and capped debris removal to see what’s typically paid.",
        "title": "Fallen Tree Insurance Claim Calculator | Free Tool",
        "desc": "Free fallen tree insurance claim calculator: separate removal from the house, repairs and capped debris removal to see a likely payment.",
        "h1": "Fallen Tree Insurance Claim Calculator",
        "lede": "After a nor’easter or tropical storm, tree claims mix three different coverages. This calculator separates them so you can see why the check may not match the tree service bill.",
        "markup": TREE,
        "explain": """
<h2>The three pieces of a tree claim</h2>
<ol><li><strong>Removing the tree from the structure.</strong> Lifting a tree off a roof or porch so repairs can be made is generally part of the dwelling loss, including reasonable crane and rigging costs.</li>
<li><strong>Repairing the structure.</strong> Roof, framing, siding, gutters and interior damage are valued like any other covered dwelling loss.</li>
<li><strong>Debris removal of the tree itself.</strong> Many homeowners forms pay to haul away fallen trees only in specific cases, such as when a tree damaged a covered structure or blocks a driveway or ramp, and only up to a per-tree and per-loss limit.</li></ol>
<h2>Why the numbers surprise people</h2>
<p>A tree service bill that bundles crane work on the house with hauling and stump grinding can look unpaid when, in fact, part of it belongs to the dwelling claim and part falls under a small sub-limit. Ask your contractor to split the invoice into those categories.</p>
<div class="note"><b class="h">Illustrative only</b>Limits vary by policy form and endorsement. Defaults shown reflect amounts commonly found in standard homeowners forms. Your policy controls; check its debris removal and trees, shrubs and plants provisions.</div>
""",
        "faqs": [("Is stump grinding covered?", "Often not. Many policies limit debris removal to the fallen tree and exclude stump removal. Check your form."), ("Does the deductible apply to the debris removal amount?", "The deductible generally applies once per occurrence to the covered loss. This calculator subtracts it once from the combined amount.")],
    },
]
