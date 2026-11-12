"""Interactive claim tools: markup + explanatory copy. Logic lives in static/assets/js/app.js.
Every figure the tools show is computed in the browser from what the visitor types; nothing is stored or sent."""

TB = "/toolkit/"

GAP_FULL = """
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Claim gap &amp; fee estimator</span><i>Private · runs in your browser</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Insurer’s estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="21600"><span class="hint">Replacement cost total on the insurer’s estimate.</span></div>
        <div><label for="g-own">Your estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="38900"><span class="hint">Your contractor’s or independent estimate.</span></div>
      </div>
      <div><label for="g-land">Where might an award land within the gap?</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% means the insurer’s number holds; 100% means your full number is awarded.</span></div>
      <div class="row2">
        <div><label for="g-ft">Appraiser fee type</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of the increase (%)</option></select></div>
        <div><label for="g-fee">Fee amount</label><input id="g-fee" name="fee" inputmode="decimal" value="2800"></div>
      </div>
      <label class="check"><input type="checkbox" name="useump" checked> Include my half of an umpire’s fee</label>
      <div><label for="g-ump">Umpire’s total fee (usually split 50/50)</label><input id="g-ump" name="umpire" inputmode="decimal" value="3200"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated net increase to you</small><b data-o="net">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s-a"></span><span class="s-b"></span><span class="s-c"></span></div>
      <div class="legend"><span><i class="s-a"></i>Insurer’s number</span><span><i class="s-b"></i>Your net gain</span><span><i class="s-c"></i>Appraisal costs</span></div>
      <div class="out-rows">
        <div><span>Amount in dispute</span><b data-o="gap">$0</b></div>
        <div><span>Gap as % of insurer estimate</span><b data-o="pct">—</b></div>
        <div><span>Projected award (RCV)</span><b data-o="award">$0</b></div>
        <div><span>Your appraisal costs</span><b data-o="cost">$0</b></div>
        <div><span>Break-even: award must reach</span><b data-o="breakeven">—</b></div>
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
      <div><label for="m-ins">Insurer’s estimate</label><input id="m-ins" name="insurer" inputmode="decimal" value="16400"></div>
      <div><label for="m-own">Your contractor’s estimate</label><input id="m-own" name="yours" inputmode="decimal" value="29800"></div>
      <div><label for="m-land">Award lands at</label><div class="range"><input id="m-land" type="range" name="land" min="0" max="100" step="5" value="50" data-unit="%"><output>50%</output></div><span class="hint">of the disputed amount</span></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Amount in dispute</small><b data-o="gap">$0</b></div>
      <div class="out-rows">
        <div><span>Gap vs. insurer estimate</span><b data-o="pct">—</b></div>
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
  <div class="tool-head"><span>Depreciation recovery calculator</span><i>Add as many line items as you need</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Concrete tile roof underlayment", 16800, 14, 25), ("Exterior stucco & paint", 5200, 8, 15), ("Luxury vinyl plank flooring", 3900, 5, 20)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn ghost small" data-add data-run>+ Add item</button></div>
      <div class="row2">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="2500"></div>
        <div><label for="d-cap">Depreciation cap</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="90">90%</option></select><span class="hint">Many estimates cap depreciation. Check yours.</span></div>
      </div>
      <label class="check"><input type="checkbox" name="nonrec"> My policy pays actual cash value only (no recoverable depreciation)</label>
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
  <div class="tool-head"><span>Roof squares &amp; tile calculator</span><i>Check the measurements on your estimate</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <fieldset class="bare"><legend class="sr-only">Measurement method</legend>
        <div class="btn-row">
          <label class="check"><input type="radio" name="mode" value="dims" checked> Footprint length × width</label>
          <label class="check"><input type="radio" name="mode" value="area"> I know the footprint area</label>
        </div></fieldset>
      <div class="row2" data-mode="dims">
        <div><label for="r-l">Footprint length (ft)</label><input id="r-l" name="len" inputmode="decimal" value="62"></div>
        <div><label for="r-w">Footprint width (ft)</label><input id="r-w" name="wid" inputmode="decimal" value="38"></div>
      </div>
      <div data-mode="dims"><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="18"></div>
      <div data-mode="area" hidden><label for="r-a">Footprint area incl. overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="2600"></div>
      <div class="row2">
        <div><label for="r-p">Roof pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 4 else "", p) for p in [2, 3, 4, 5, 6, 7, 8, 9, 10, 12]) + """</select></div>
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="10">10% · simple gable</option><option value="12">12% · gable with returns</option><option value="15" selected>15% · hip roof</option><option value="18">18% · cut-up / many valleys</option></select></div>
      </div>
      <div class="row2">
        <div><label for="r-t">Roof covering</label><select id="r-t" name="rtype"><option value="tile" selected>Concrete tile</option><option value="clay">Clay tile</option><option value="shingle">Composition shingle</option></select></div>
        <div data-rt="tile"><label for="r-tps">Tiles per square (approx.)</label><input id="r-tps" name="tps" inputmode="decimal" value="90"><span class="hint">Varies by profile; check the manufacturer.</span></div>
      </div>
      <div data-rt="tile"><label for="r-br">Broken or displaced tiles counted</label><input id="r-br" name="broken" inputmode="decimal" value="140"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Roof squares (before waste)</small><b data-o="sq">0</b></div>
      <div class="out-rows">
        <div><span>Pitch multiplier</span><b data-o="mult">1.000</b></div>
        <div><span>Roof surface area</span><b data-o="surface">0</b></div>
        <div><span>Squares with waste</span><b data-o="order">0</b></div>
        <div><span data-o="unitlabel">Field tiles (approx.)</span><b data-o="units">0</b></div>
        <div data-rt="tile"><span>Broken tiles as share of roof</span><b data-o="brokenpct">—</b></div>
      </div>
      <p class="out-msg" data-o="steep"></p>
    </div>
  </div>
</div>"""

DEDUCT = """
<div class="tool" data-tool="deduct">
  <div class="tool-head"><span>Percentage deductible calculator</span><i>Wind, hail or earthquake</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-k">Which deductible?</label><select id="w-k" name="kind"><option value="wind">Wind / hail percentage deductible</option><option value="quake">Earthquake percentage deductible</option></select></div>
      <div><label for="w-a">Dwelling coverage (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="465000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Percentage</label><select id="w-p" name="pct"><option value="1">1%</option><option value="2" selected>2%</option><option value="5">5%</option><option value="10">10%</option><option value="15">15%</option><option value="20">20%</option><option value="25">25%</option></select></div>
        <div><label for="w-f">All-other-perils flat deductible</label><input id="w-f" name="flat" inputmode="decimal" value="1000"></div>
      </div>
      <div><label for="w-l">Estimated damage</label><input id="w-l" name="loss" inputmode="decimal" value="24800"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your percentage deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s-c"></span><span class="s-a"></span></div>
      <div class="legend"><span><i class="s-c"></i>You pay</span><span><i class="s-a"></i>Policy pays</span></div>
      <div class="out-rows">
        <div><span>Payment with % deductible</span><b data-o="pdpay">$0</b></div>
        <div><span>Payment if the flat deductible applied</span><b data-o="flatpay">$0</b></div>
        <div><span>Extra out-of-pocket from % deductible</span><b data-o="diff">$0</b></div>
        <div><span>Share of the loss you absorb</span><b data-o="share">—</b></div>
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
      <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
      <p class="hint">Set each window to match your policy. The defaults are placeholders, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="2"></div>
        <div><label for="t-m">Mitigation done within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="10"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Often counted from the insurer’s request.</span></div>
        <div><label for="t-r">Depreciation recovery (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="180"></div>
        <div><label for="t-s">Suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="365"><span class="hint">Many property policies use one year. Check yours.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download calendar (.ics)</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the insurer accepted coverage for at least part of the loss?", "Get written confirmation of what the insurer accepts. If the claim was denied outright, talk to a Nevada attorney before considering appraisal."),
    (3, "Do you have the insurer’s full line-item estimate, not just a summary?", "Ask in writing for the complete itemized estimate, including the price list it used."),
    (3, "Do you have your own itemized estimate?", "Get a line-item estimate from a contractor or estimator. A lump-sum bid is hard to defend before a panel."),
    (2, "Do you have dated photos taken soon after the loss?", "Gather every photo and note when each was taken. Add current photos too."),
    (2, "Have you found and read the ‘Appraisal’ paragraph in your policy?", "Locate it in the policy conditions and note any time limits for naming an appraiser."),
    (2, "Do you know the date by which a lawsuit must be filed under your policy?", "Find the ‘Suit Against Us’ wording and calendar it with our claim calendar builder."),
    (2, "Was the damage mitigated (tarp, drying, board-up) with receipts saved?", "Finish reasonable temporary repairs and keep every invoice and photo."),
    (2, "For tile roofs, smoke or water: has hidden damage been opened up and checked?", "Make sure underlayment, attics, ductwork or wall cavities were inspected so the scope is complete."),
    (1, "Do you have your current declarations page?", "Download it from your insurer’s portal or ask your agent."),
    (1, "Is your correspondence with the insurer saved in date order?", "Collect letters, emails and claim notes in one folder by date."),
    (2, "Is the gap between estimates more than roughly 10% or $5,000?", "Run the claim gap & fee estimator. A small gap may not justify appraisal costs."),
    (1, "If the insurer requested a sworn proof of loss, was it submitted on time?", "Submit any requested proof of loss before the deadline in the request."),
]

READY = """
<div class="tool tool-wide" data-tool="ready">
  <div class="tool-head"><span>Appraisal file scorecard</span><i>12 questions · about two minutes</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <ol class="quiz">""" + "".join(
    '<li data-w="%d" data-fix="%s"><span>%s</span><span class="yn"><button type="button" class="yes" aria-pressed="false">Yes</button><button type="button" class="no" aria-pressed="false">No</button></span></li>' % (w, f, q)
    for w, q, f in _QUIZ) + """
      </ol>
      <div class="btn-row"><button type="button" class="btn ghost small" data-reset>Reset answers</button></div>
    </div>
    <div class="tool-out score-out" aria-live="polite">
      <div>
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#efe6cf" stroke-width="18"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#c8961f" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3" style="transition:stroke-dashoffset .5s,stroke .3s"/></svg>
        <div class="gauge-num"><span data-o="score">–</span></div>
        <p class="hint center">Answered <span data-o="count">0 / 12</span></p>
      </div>
      <div>
        <p class="out-msg" data-o="verdict"></p>
        <p class="todo-h">What to fix first</p>
        <ul data-o="todo" class="todo"></ul>
      </div>
    </div>
  </div>
</div>"""

SMOKE = """
<div class="tool tool-wide" data-tool="smoke">
  <div class="tool-head"><span>Smoke &amp; ash cleaning scope estimator</span><i>Illustrative unit prices · edit them</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="s-sf">Home floor area (sq ft)</label><input id="s-sf" name="sf" inputmode="decimal" value="2200"></div>
        <div><label for="s-ch">Ceiling height (ft)</label><input id="s-ch" name="ch" inputmode="decimal" value="9"></div>
      </div>
      <div class="row2">
        <div><label for="s-lv">Residue level</label><select id="s-lv" name="level"><option value="light">Light: odor, faint film</option><option value="moderate" selected>Moderate: visible soot or ash</option><option value="heavy">Heavy: dense residue throughout</option></select></div>
        <div><label for="s-hv">HVAC systems</label><input id="s-hv" name="hvac" inputmode="numeric" value="1"></div>
      </div>
      <div class="row2">
        <div><label for="s-rm">Rooms of contents to clean</label><input id="s-rm" name="rooms" inputmode="numeric" value="8"></div>
        <div><label for="s-dy">Air scrubber days</label><input id="s-dy" name="days" inputmode="numeric" value="4"></div>
      </div>
      <details class="prices"><summary>Edit unit prices (illustrative)</summary>
        <div class="row2">
          <div><label for="s-p1">Surface cleaning ($ / sq ft of wall + ceiling)</label><input id="s-p1" name="p_surface" inputmode="decimal" value="0.45"></div>
          <div><label for="s-p2">HVAC &amp; duct cleaning ($ / system)</label><input id="s-p2" name="p_hvac" inputmode="decimal" value="950"></div>
        </div>
        <div class="row2">
          <div><label for="s-p3">Contents cleaning ($ / room)</label><input id="s-p3" name="p_room" inputmode="decimal" value="420"></div>
          <div><label for="s-p4">Air scrubber ($ / day)</label><input id="s-p4" name="p_day" inputmode="decimal" value="110"></div>
        </div>
        <div class="row2">
          <div><label for="s-p5">Carpet &amp; upholstery ($ / sq ft floor)</label><input id="s-p5" name="p_floor" inputmode="decimal" value="0.55"></div>
          <div><label for="s-p6">Exterior wash ($ / sq ft floor)</label><input id="s-p6" name="p_ext" inputmode="decimal" value="0.30"></div>
        </div>
      </details>
      <label class="check"><input type="checkbox" name="attic"> Include attic insulation removal &amp; replacement</label>
      <div><label for="s-p7">Attic insulation ($ / sq ft floor)</label><input id="s-p7" name="p_attic" inputmode="decimal" value="2.10"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Illustrative cleaning scope total</small><b data-o="total">$0</b></div>
      <div class="out-rows">
        <div><span>Wall &amp; ceiling surface area</span><b data-o="area">0</b></div>
        <div><span>Surface cleaning</span><b data-o="surface">$0</b></div>
        <div><span>HVAC &amp; ducts</span><b data-o="hvac">$0</b></div>
        <div><span>Contents cleaning</span><b data-o="contents">$0</b></div>
        <div><span>Air scrubbing</span><b data-o="air">$0</b></div>
        <div><span>Carpet &amp; upholstery</span><b data-o="floor">$0</b></div>
        <div><span>Exterior wash</span><b data-o="ext">$0</b></div>
        <div><span>Attic insulation</span><b data-o="attic">$0</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "claim-gap-estimator", "name": "Claim Gap & Fee Estimator", "kind": "Calculator", "photo": "calculator-pencil",
        "short": "Measure the disputed amount, project an award and find the break-even point after appraisal fees.",
        "title": "Claim Gap & Appraisal Fee Estimator | Free Tool",
        "desc": "Compare your estimate with the insurer’s, project an award, subtract appraiser and umpire fees and find the break-even point for appraisal.",
        "h1": "Claim Gap and Appraisal Fee Estimator",
        "lede": "Enter the insurer’s estimate and yours, choose where an award might land and add realistic fees. The estimator shows your likely net and how much of the gap you must win just to break even.",
        "markup": GAP_FULL,
        "explain": """
<h2>How to use it</h2>
<ol><li><strong>Insurer’s RCV total.</strong> Use the replacement cost figure before depreciation and the deductible.</li>
<li><strong>Your RCV total.</strong> Use a line-item estimate from a contractor or estimator, also at replacement cost.</li>
<li><strong>Slide the landing point.</strong> Try several values, such as 30%, 55% and 80%, to see a range of outcomes.</li>
<li><strong>Add fees.</strong> Use the arrangement your appraiser quotes and a realistic umpire fee.</li></ol>
<h2>The break-even line</h2>
<p>The break-even figure tells you what share of the disputed amount an award must capture before appraisal pays for itself. If you break even at 15% of the gap, the decision is easy. If you need 85%, the case depends on winning almost every item, and a documented supplement request or a second opinion may be the smarter first step.</p>
<h2>What it leaves out</h2>
<p>The estimator measures the size of the dispute. It ignores deductibles, depreciation timing, policy limits and sub-limits, which affect what you are paid. For those, use the <a href="/toolkit/depreciation-recovery-calculator/">depreciation recovery calculator</a> and the <a href="/toolkit/percentage-deductible-calculator/">percentage deductible calculator</a>.</p>
<p class="hint">All example figures are illustrative.</p>
""",
        "faqs": [("Is the projected award a prediction?", "No. It is a scenario you choose. Real awards depend on documentation, the panel and your policy."), ("What do umpires charge?", "It varies with the size and complexity of the claim. The appraisers can get a quote once an umpire is proposed; most policies split the fee equally.")],
    },
    {
        "slug": "depreciation-recovery-calculator", "name": "Depreciation Recovery Calculator", "kind": "Calculator", "photo": "calculator-closeup",
        "short": "Estimate your first ACV check, the depreciation held back and the total once repairs are finished.",
        "title": "Depreciation Recovery Calculator | RCV, ACV & Holdback",
        "desc": "Estimate actual cash value, recoverable depreciation and your first insurance check, line by line, with a depreciation cap and deductible.",
        "h1": "Depreciation Recovery Calculator: RCV, ACV and Holdback",
        "lede": "Replacement cost policies usually pay in two steps: actual cash value first, then the depreciation held back once repairs are done. Add line items to see both checks.",
        "markup": DEP,
        "explain": """
<h2>How depreciation works on a claim</h2>
<p>Depreciation is the reduction for age and condition. On a replacement cost policy, the first payment is usually replacement cost minus depreciation minus the deductible. The depreciation is ‘held back’ and paid once you complete repairs and submit proof, if you do so within the policy’s time limit.</p>
<h2>Why Nevada roofs depreciate fast on paper</h2>
<p>Insurers often assign short lifespans to roofing components in desert climates. A concrete tile may last for decades while the underlayment beneath it is depreciated much faster. Check the age and life used for each line; small changes make a big difference.</p>
<h2>Things to check on your estimate</h2>
<ul><li>Are ages and lifespans realistic for each item?</li><li>Is depreciation applied to labor? Some policies and practices differ on that.</li><li>Is a depreciation cap applied?</li><li>What is the deadline to complete repairs and claim the holdback?</li></ul>
<p class="hint">All example figures are illustrative.</p>
""",
        "faqs": [("Can depreciation be disputed in appraisal?", "Often yes, because it affects the amount of loss. Ages, lifespans and condition are common panel topics."), ("What if I don’t repair?", "On many replacement cost policies you receive only the actual cash value until repairs are completed.")],
    },
    {
        "slug": "roof-squares-tile-calculator", "name": "Roof Squares & Tile Calculator", "kind": "Calculator", "photo": "tile-roof-sky",
        "short": "Turn footprint and pitch into roof squares, waste, tile counts and the share of broken tile.",
        "title": "Roof Squares & Tile Calculator | Pitch, Waste, Tile Count",
        "desc": "Free roof calculator: turn footprint and pitch into roof squares, add waste, estimate tile or bundle counts and see broken tile as a share.",
        "h1": "Roof Squares and Tile Calculator",
        "lede": "Check the roof measurements on your estimate. Enter the footprint, pitch and covering to get squares, waste and an approximate tile or bundle count, plus how much of the roof your broken tiles represent.",
        "markup": ROOF,
        "explain": """
<h2>How the math works</h2>
<p>A roofing square is 100 square feet of roof surface. Pitch adds area: a 4/12 roof has about 5.4% more surface than its footprint, an 8/12 roof about 20% more. Waste covers cutting at hips, valleys and edges. Hip roofs, which are common in Southern Nevada, usually need more waste than simple gables.</p>
<h2>Why tile counts matter</h2>
<p>On a tile roof, the number of broken or displaced tiles helps frame the repair-or-replace question. If breakage is scattered across many slopes, lifting and resetting courses to replace individual tiles can approach the cost of a full re-roof, especially when the underlayment is aged.</p>
<h2>Limits</h2>
<p>Real roofs have dormers, multiple pitches and complex intersections. Use the calculator for a sanity check, not a bid. Tiles per square varies by manufacturer and profile.</p>
<p class="hint">All example figures are illustrative.</p>
""",
        "faqs": [("My estimate shows fewer squares than this calculator. Why?", "The estimate may have measured a different area, used a lower pitch or omitted waste. Ask how it was measured."), ("Does pitch change the price?", "Steeper roofs often carry steep-roof labor charges in estimating software, typically starting around 7/12 or 8/12.")],
    },
    {
        "slug": "percentage-deductible-calculator", "name": "Percentage Deductible Calculator", "kind": "Calculator", "photo": "desert-lightning",
        "short": "See a wind, hail or earthquake percentage deductible in dollars and compare it to a flat deductible.",
        "title": "Percentage Deductible Calculator | Wind & Earthquake",
        "desc": "Turn a wind, hail or earthquake percentage deductible into dollars, compare it with a flat deductible and see the share of a loss you absorb.",
        "h1": "Percentage Deductible Calculator for Wind, Hail and Earthquake",
        "lede": "A 2% wind deductible or a 15% earthquake deductible is a percentage of your dwelling limit, not of the damage. This calculator shows what that means in real dollars.",
        "markup": DEDUCT,
        "explain": """
<h2>How percentage deductibles work</h2>
<p>A percentage deductible is calculated on your dwelling coverage limit (Coverage A). On a $465,000 dwelling limit, a 2% deductible is $9,300, no matter how much damage there is. Earthquake policies and endorsements commonly use much higher percentages.</p>
<h2>Earthquake coverage in Nevada</h2>
<p>Nevada is among the most seismically active states, with damaging events like the 2008 Wells earthquake and the 2020 Monte Cristo Range earthquake. Standard homeowners policies usually exclude earth movement, so earthquake damage typically requires a separate policy or endorsement, often with a deductible between 5% and 25% of the dwelling limit.</p>
<h2>Why this matters for appraisal</h2>
<p>If the disputed amount sits mostly inside your deductible, appraisal may not change your payment. Run your numbers here before deciding.</p>
<p class="hint">All example figures are illustrative.</p>
""",
        "faqs": [("Does Nevada require wind deductibles?", "No statewide rule requires them, but some insurers include percentage wind or hail deductibles. Check your declarations page."), ("Is the deductible taken from the total loss or per item?", "Usually from the total covered loss for the occurrence. Read your policy for exact terms.")],
    },
    {
        "slug": "claim-calendar-builder", "name": "Claim Calendar Builder", "kind": "Planner", "photo": "signing-papers",
        "short": "Turn your date of loss into dated milestones and download them to your calendar.",
        "title": "Insurance Claim Calendar Builder | Deadline .ics Export",
        "desc": "Enter your date of loss and policy deadlines to build a claim timeline, see how many days remain and export every milestone to your calendar app.",
        "h1": "Insurance Claim Calendar Builder with .ics Export",
        "lede": "Missed deadlines sink more claims than bad estimates do. Enter your date of loss, set each window to match your policy and download the milestones to your calendar.",
        "markup": DATES,
        "explain": """
<h2>Milestones to track</h2>
<ul><li><strong>Notice.</strong> Policies require prompt notice. Report as soon as you can.</li>
<li><strong>Mitigation.</strong> Reasonable steps to prevent further damage, with receipts.</li>
<li><strong>Proof of loss.</strong> If the insurer requests a sworn proof of loss, the deadline usually runs from the request.</li>
<li><strong>Depreciation recovery.</strong> The window to complete repairs and claim held-back depreciation.</li>
<li><strong>Suit limitation.</strong> The deadline in your policy to file a lawsuit. Talk to a Nevada attorney well before it.</li></ul>
<h2>Using the .ics file</h2>
<p>The download works with Google Calendar, Apple Calendar and Outlook. Each milestone becomes an all-day event. Nothing is uploaded; the file is created in your browser.</p>
<div class="note"><b class="h">Not legal advice</b>Deadlines depend on your policy and Nevada law, and courts interpret them. When a deadline matters, confirm it with a Nevada attorney.</div>
""",
        "faqs": [("Why are the default numbers different from my policy?", "They’re placeholders. Replace each with the number in your policy or the insurer’s letters."), ("Does appraisal pause my lawsuit deadline?", "Not necessarily. Ask a Nevada attorney about your specific deadline.")],
    },
    {
        "slug": "appraisal-file-scorecard", "name": "Appraisal File Scorecard", "kind": "Checklist", "photo": "drafting-plans",
        "short": "Twelve yes-or-no questions that score how ready your file is for an appraisal panel.",
        "title": "Appraisal File Scorecard | Is Your Claim Ready?",
        "desc": "Answer 12 quick questions to score your claim file for appraisal and get a prioritized to-do list before you invoke the appraisal clause.",
        "h1": "Appraisal File Scorecard: Is Your Claim Ready?",
        "lede": "An appraisal panel can only work with what is in the file. Answer twelve questions to see how ready yours is, and get a to-do list ranked by what matters most.",
        "markup": READY,
        "explain": """
<h2>How the score works</h2>
<p>Each question carries a weight. Coverage acceptance and itemized estimates count most because appraisal can’t work without them. Photos, deadlines and hidden-damage checks come next. A score above about 75 suggests a strong file; below 45 suggests work to do first.</p>
<h2>What to do with your to-do list</h2>
<p>Work from the top. Most items take a phone call or an email. When the list is short, use the <a href="/toolkit/claim-gap-estimator/">claim gap &amp; fee estimator</a> to decide whether appraisal makes financial sense.</p>
""",
        "faqs": [("Does a high score mean I’ll win?", "No. It means your file is organized. The outcome depends on the evidence and the panel."), ("Is anything saved?", "No. Answers stay in your browser and disappear when you leave the page.")],
    },
    {
        "slug": "smoke-ash-cleaning-estimator", "name": "Smoke & Ash Cleaning Estimator", "kind": "Estimator", "photo": "burned-sagebrush",
        "short": "Build an illustrative smoke and ash cleaning scope after a wildfire or house fire.",
        "title": "Smoke & Ash Cleaning Scope Estimator | Wildfire Claims",
        "desc": "Build an illustrative smoke and ash cleaning scope: walls, ceilings, HVAC, contents, air scrubbing, carpet and attic insulation, at editable prices.",
        "h1": "Smoke and Ash Cleaning Scope Estimator",
        "lede": "After a wildfire near Reno, Carson City or Lake Tahoe, insurers often offer a light wipe-down. This estimator builds a fuller illustrative scope so you can see what a complete cleaning might involve.",
        "markup": SMOKE,
        "explain": """
<h2>What the estimator includes</h2>
<ul><li><strong>Surface cleaning</strong> of walls and ceilings, calculated from floor area and ceiling height.</li>
<li><strong>HVAC and ducts</strong>, per system.</li>
<li><strong>Contents cleaning</strong>, per room.</li>
<li><strong>Air scrubbing</strong> with HEPA units, per day.</li>
<li><strong>Carpet and upholstery</strong> and an <strong>exterior wash</strong>.</li>
<li><strong>Attic insulation</strong> removal and replacement, if residue reached the attic.</li></ul>
<p>The residue level scales labor: light residue reduces surface and contents effort, heavy residue increases it.</p>
<h2>Prices are illustrative</h2>
<p>The default unit prices are placeholders to show how a scope adds up. Real prices depend on your contractor, the residue and your area. Replace them with figures from your own estimate.</p>
<h2>When cleaning isn’t enough</h2>
<p>Some materials can’t be restored: heavily contaminated insulation, porous items and flex duct with embedded residue. Testing by a qualified professional can help define the right scope. See our <a href="/appraisal/wildfire-claims/">wildfire and ash damage service</a>.</p>
""",
        "faqs": [("Is this an estimate I can send my insurer?", "No. It is an illustration to help you understand scope. A professional estimate is needed for a claim."), ("Why does residue level matter so much?", "Heavier residue takes more passes, more labor and sometimes replacement instead of cleaning.")],
    },
]
