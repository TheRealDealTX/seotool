"""Interactive claim tools: markup + explanatory copy. Logic lives in static/assets/js/app.js.

Headings inside widgets are deliberately avoided (labels/spans only) so page heading order stays valid.
"""

PAYOFF = """
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Appraisal payoff estimator</span><i>Runs in your browser · nothing saved</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Carrier’s estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="21600"><span class="hint">Replacement cost total before depreciation and deductible.</span></div>
        <div><label for="g-own">Your estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="38900"><span class="hint">Your contractor’s or an independent estimate.</span></div>
      </div>
      <div><label for="g-doc">How well documented is your number?</label><select id="g-doc" name="docs"><option value="30">Thin: lump-sum bid, few photos</option><option value="50" selected>Moderate: itemized estimate, some photos</option><option value="70">Strong: itemized, measured, dated photos</option></select><span class="hint">Sets a starting point for the slider below. Adjust it freely.</span></div>
      <div><label for="g-land">Share of the gap the award recovers</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="50" data-unit="%"><output>50%</output></div>
        <span class="hint">0% means the carrier’s number holds; 100% means your full number is awarded.</span></div>
      <div class="row2">
        <div><label for="g-ft">Appraiser fee type</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of the increase (%)</option></select></div>
        <div><label for="g-fee">Fee amount</label><input id="g-fee" name="fee" inputmode="decimal" value="3000"></div>
      </div>
      <label class="check"><input type="checkbox" name="useump" checked> Include my half of an umpire’s fee</label>
      <div><label for="g-ump">Umpire’s total fee</label><input id="g-ump" name="umpire" inputmode="decimal" value="3500"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><span class="out-k">Estimated net increase</span><b data-o="net">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s-a"></span><span class="s-b"></span><span class="s-c"></span></div>
      <div class="legend"><span><i class="s-a"></i>Carrier’s number</span><span><i class="s-b"></i>Your net gain</span><span><i class="s-c"></i>Appraisal costs</span></div>
      <div class="out-rows">
        <div><span>Amount in dispute</span><b data-o="gap">$0</b></div>
        <div><span>Gap vs. carrier estimate</span><b data-o="pct">—</b></div>
        <div><span>Projected award (RCV)</span><b data-o="award">$0</b></div>
        <div><span>Your appraisal costs</span><b data-o="cost">$0</b></div>
        <div><span>Break-even recovery</span><b data-o="breakeven">—</b></div>
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
      <div><label for="m-land">Award recovers</label><div class="range"><input id="m-land" type="range" name="land" min="0" max="100" step="5" value="50" data-unit="%"><output>50%</output></div><span class="hint">of the disputed amount</span></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><span class="out-k">Amount in dispute</span><b data-o="gap">$0</b></div>
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
  <div class="tool-head"><span>Depreciation recovery calculator</span><i>Add as many line items as you need</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th scope="col">Item</th><th scope="col">Replacement cost ($)</th><th scope="col">Age (yrs)</th><th scope="col">Life (yrs)</th><th scope="col">ACV</th><th scope="col"><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Concrete tile roof underlayment", 14800, 18, 25), ("Interior paint — great room", 2600, 5, 10), ("Evaporative cooler", 1900, 7, 12)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn line small" data-add data-run>+ Add item</button></div>
      <div class="row2">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="2500"></div>
        <div><label for="d-cap">Maximum depreciation</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="90">90%</option></select><span class="hint">Many estimates cap depreciation. Check yours.</span></div>
      </div>
      <label class="check"><input type="checkbox" name="nonrec"> My policy pays actual cash value only (no recoverable depreciation)</label>
    </div>
    <div class="tool-out tool-out-3" aria-live="polite">
      <div class="out-big"><span class="out-k">First check (ACV − deductible)</span><b data-o="first">$0</b></div>
      <div class="out-big"><span class="out-k">Held back until repairs</span><b data-o="held">$0</b></div>
      <div class="out-big"><span class="out-k">Total if fully recovered</span><b data-o="total">$0</b></div>
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
  <div class="tool-head"><span>Roof pitch, squares &amp; material calculator</span><i>Check the carrier’s roof math</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <fieldset class="plain"><legend class="sr-only">Measurement method</legend>
        <div class="btn-row">
          <label class="check"><input type="radio" name="mode" value="dims" checked> Footprint length × width</label>
          <label class="check"><input type="radio" name="mode" value="area"> I know the footprint area</label>
        </div></fieldset>
      <div class="row2" data-mode="dims">
        <div><label for="r-l">Footprint length (ft)</label><input id="r-l" name="len" inputmode="decimal" value="64"></div>
        <div><label for="r-w">Footprint width (ft)</label><input id="r-w" name="wid" inputmode="decimal" value="38"></div>
      </div>
      <div data-mode="dims"><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="18"></div>
      <div data-mode="area" hidden><label for="r-a">Footprint area incl. overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="2600"></div>
      <div class="row2">
        <div><label for="r-p">Roof pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 4 else "", p) for p in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]) + """</select></div>
        <div><label for="r-m">Roof material</label><select id="r-m" name="mat"><option value="tile" selected>Concrete or clay tile</option><option value="shingle">Asphalt shingle</option><option value="metal">Metal panel</option><option value="foam">Spray foam / low slope</option></select></div>
      </div>
      <div class="row2">
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="8">8% — simple gable</option><option value="12" selected>12% — gable with hips</option><option value="15">15% — full hip roof</option><option value="18">18% — complex / cut-up</option></select></div>
        <div><label for="r-pr">Installed price per square (optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 850"></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><span class="out-k">Roof squares (before waste)</span><b data-o="sq">0</b></div>
      <div class="out-rows">
        <div><span>Pitch multiplier</span><b data-o="mult">1.000</b></div>
        <div><span>Roof surface area</span><b data-o="surface">0</b></div>
        <div><span>Squares with waste</span><b data-o="order">0</b></div>
        <div><span data-o="unitlabel">Approx. field tiles</span><b data-o="units">0</b></div>
        <div><span>Rough replacement cost</span><b data-o="cost">—</b></div>
      </div>
      <p class="out-msg" data-o="steep"></p>
    </div>
  </div>
</div>"""

DEDUCT = """
<div class="tool" data-tool="deduct">
  <div class="tool-head"><span>Percentage deductible calculator</span><i>Percent vs. flat, side by side</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling coverage (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="465000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Wind/hail or all-peril percentage</label><select id="w-p" name="pct"><option value="0.5">0.5%</option><option value="1" selected>1%</option><option value="2">2%</option><option value="3">3%</option><option value="5">5%</option></select></div>
        <div><label for="w-f">Flat deductible (other perils)</label><input id="w-f" name="flat" inputmode="decimal" value="2500"></div>
      </div>
      <div><label for="w-l">Estimated storm damage</label><input id="w-l" name="loss" inputmode="decimal" value="18700"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><span class="out-k">Your percentage deductible in dollars</span><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s-c"></span><span class="s-a"></span></div>
      <div class="legend"><span><i class="s-c"></i>You pay</span><span><i class="s-a"></i>Policy pays</span></div>
      <div class="out-rows">
        <div><span>Payment with % deductible</span><b data-o="pdpay">$0</b></div>
        <div><span>Payment if the flat deductible applied</span><b data-o="flatpay">$0</b></div>
        <div><span>Extra out-of-pocket from the %</span><b data-o="diff">$0</b></div>
      </div>
      <p class="out-msg" data-o="below"></p>
    </div>
  </div>
</div>"""

DATES = """
<div class="tool" data-tool="dates">
  <div class="tool-head"><span>Claim deadline calendar</span><i>Download as an .ics file</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
      <p class="hint m0">Change each window to match your policy. Defaults are common figures, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report the claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="2"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="7"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Often counted from the carrier’s request.</span></div>
        <div><label for="t-r">Depreciation recovery (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="180"></div>
        <div><label for="t-s">Suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="365"><span class="hint">Many policies use one or two years.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download .ics calendar file</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the insurer accepted coverage for at least part of the loss?", "Get the carrier’s coverage position in writing. If the claim was denied outright, talk to an Arizona attorney before thinking about appraisal."),
    (3, "Do you have the carrier’s complete line-item estimate, not just a summary?", "Ask the adjuster in writing for the full itemized estimate, including the price list it uses."),
    (3, "Do you have your own itemized estimate?", "Get a line-item estimate from a contractor or estimator. A one-line bid rarely persuades an umpire."),
    (2, "Do you have dated photos taken soon after the storm or event?", "Collect every photo and note the date each was taken. Add photos of current conditions."),
    (2, "Have you found and read the Appraisal condition in your policy?", "Locate the Appraisal paragraph in the policy conditions and note any deadlines it sets."),
    (2, "Do you know your policy’s deadline to file suit?", "Find the ‘Suit Against Us’ condition and put the date on your calendar. Our deadline calendar can help."),
    (2, "Have temporary repairs been made, with receipts kept?", "Tarp, dry out or board up as needed and keep every receipt. Mitigation protects the claim."),
    (2, "For tile roofs, has the underlayment condition been checked?", "Ask your roofer to lift tiles in several areas and photograph the underlayment. Its condition often decides repair versus replacement."),
    (1, "Do you have your current declarations page?", "Download it from your insurer’s portal or ask your agent."),
    (2, "Has hidden damage (attic, walls, decking, slab) been opened and documented?", "Make sure concealed areas are inspected so the scope is complete before you lock in a number."),
    (1, "Is your correspondence with the carrier organized by date?", "Collect letters, emails and claim notes into one dated file."),
    (2, "Is the gap more than roughly 10% or $5,000?", "Run the numbers in the appraisal payoff estimator. A small gap may not justify fees."),
]

READY = """
<div class="tool tool-wide" data-tool="ready">
  <div class="tool-head"><span>Claim file readiness check</span><i>12 questions · about two minutes</i></div>
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
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#f1e4df" stroke-width="18"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#1f9e95" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3" style="transition:stroke-dashoffset .5s,stroke .3s"/></svg>
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

TILE = """
<div class="tool" data-tool="tile">
  <div class="tool-head"><span>Tile roof repair-or-replace checker</span><i>Illustrative figures you can edit</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="k-sq">Roof size (squares)</label><input id="k-sq" name="sq" inputmode="decimal" value="32"><span class="hint">1 square = 100 sq ft of roof.</span></div>
        <div><label for="k-tps">Tiles per square</label><input id="k-tps" name="tps" inputmode="decimal" value="90"><span class="hint">About 90 for many standard concrete profiles.</span></div>
      </div>
      <div class="row2">
        <div><label for="k-br">Broken or cracked tiles counted</label><input id="k-br" name="broken" inputmode="decimal" value="140"></div>
        <div><label for="k-sl">Slopes with storm damage</label><select id="k-sl" name="slopes"><option value="25">About a quarter of the roof</option><option value="50" selected>About half</option><option value="75">About three quarters</option><option value="100">All slopes</option></select></div>
      </div>
      <div class="row2">
        <div><label for="k-ua">Underlayment age (years)</label><input id="k-ua" name="uage" inputmode="decimal" value="19"></div>
        <div><label for="k-av">Is the same tile still made?</label><select id="k-av" name="avail"><option value="yes">Yes, exact match available</option><option value="unknown" selected>Not sure</option><option value="no">No, discontinued</option></select></div>
      </div>
      <div class="row2">
        <div><label for="k-rp">Repair cost per tile (remove, replace, reset)</label><input id="k-rp" name="ptile" inputmode="decimal" value="28"></div>
        <div><label for="k-rr">Tear-off &amp; re-lay cost per square</label><input id="k-rr" name="psq" inputmode="decimal" value="925"></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><span class="out-k">Replacement argument strength</span><b data-o="verdict">—</b></div>
      <div class="meter" aria-hidden="true"><span data-o="meter"></span></div>
      <div class="out-rows">
        <div><span>Broken tiles as share of roof</span><b data-o="share">0%</b></div>
        <div><span>Spot repair (broken tiles only)</span><b data-o="repair">$0</b></div>
        <div><span>Replace damaged slopes</span><b data-o="slope">$0</b></div>
        <div><span>Replace whole roof</span><b data-o="full">$0</b></div>
      </div>
      <p class="out-msg" data-o="why"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "appraisal-payoff-estimator", "name": "Appraisal Payoff Estimator", "icon": "$↑", "kind": "Calculator",
        "short": "Size the dispute, project an award, subtract fees and find the break-even point where appraisal starts to pay.",
        "title": "Appraisal Payoff Estimator | Fees, Award & Break-Even",
        "desc": "Free calculator for Arizona claims: compare estimates, project an appraisal award, subtract appraiser and umpire fees and see your break-even point.",
        "h1": "Appraisal Payoff Estimator: What Would You Net After Fees?",
        "lede": "Enter the carrier’s number and yours, choose how well your estimate is documented, and add realistic fees. The estimator shows what you might net and the minimum recovery at which appraisal pays for itself.",
        "markup": PAYOFF,
        "explain": """
<h2>How to read the result</h2>
<ol><li><strong>Amount in dispute</strong> is simply your estimate minus the carrier’s, both at replacement cost.</li>
<li><strong>Projected award</strong> assumes the panel recovers the share of that gap you set with the slider.</li>
<li><strong>Your appraisal costs</strong> combine your appraiser’s fee with half the umpire’s fee, if you include it.</li>
<li><strong>Break-even recovery</strong> is the smallest share of the gap the award must recover before you come out ahead.</li></ol>
<h2>Why documentation matters</h2>
<p>Awards rarely match either side’s opening number. Line items backed by measurements, photographs and current pricing tend to survive; lump sums and guesses tend not to. The documentation selector moves the slider to a reasonable starting point, but test several values. If appraisal only makes sense at 90%, the case is fragile. If it still works at 35%, it is much sturdier.</p>
<h2>What it leaves out</h2>
<p>Deductibles, depreciation holdback and policy limits affect what you are paid, not the size of the disagreement. For those, use the <a href="/claim-calculators/depreciation-recovery-calculator/">depreciation recovery calculator</a> and the <a href="/claim-calculators/percentage-deductible-calculator/">percentage deductible calculator</a>. All figures here are illustrative.</p>
""",
        "faqs": [("Is the projected award a prediction?", "No. It is a scenario you choose. Real awards depend on the evidence, the appraisers, the umpire and your policy."), ("Why does a percentage fee change the break-even point?", "A percentage fee grows with the recovery, so it never wipes out the whole gain by itself. The umpire share is then the main fixed cost to overcome.")],
    },
    {
        "slug": "depreciation-recovery-calculator", "name": "Depreciation Recovery Calculator", "icon": "ACV", "kind": "Calculator",
        "short": "Estimate the first ACV check, the depreciation held back and the total once repairs are finished.",
        "title": "Depreciation Recovery Calculator | RCV, ACV & Holdback",
        "desc": "List damaged items with age and expected life to estimate your first ACV payment, recoverable depreciation holdback and total replacement cost.",
        "h1": "Depreciation Recovery Calculator (RCV, ACV and Holdback)",
        "lede": "Replacement cost policies usually pay twice: an actual cash value check now and the held-back depreciation after repairs. Enter your items to see how the money splits.",
        "markup": DEP,
        "explain": """
<h2>How depreciation is estimated</h2>
<p>This calculator uses straight-line depreciation, age divided by expected life, capped at the maximum you choose. Carrier estimates may use different life expectancies, condition adjustments or non-depreciable items such as permits, so treat the result as a planning figure.</p>
<h2>Life expectancies in the Arizona sun</h2>
<p>Desert heat and ultraviolet light shorten the life of some materials. Ranges seen in estimates vary, but these are common starting points:</p>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Common range</th></tr></thead><tbody>
<tr><th scope="row">Concrete or clay tile (the tile itself)</th><td>40–50+ years</td></tr><tr><th scope="row">Tile roof underlayment</th><td>20–25 years</td></tr><tr><th scope="row">Foam roof coating</th><td>5–10 years between recoats</td></tr><tr><th scope="row">Asphalt shingles</th><td>15–25 years</td></tr><tr><th scope="row">Evaporative cooler</th><td>10–15 years</td></tr><tr><th scope="row">Exterior paint on stucco</th><td>7–10 years</td></tr>
</tbody></table></div>
<h2>Getting the holdback released</h2>
<p>Most policies release recoverable depreciation once repairs are finished within a set time. Send invoices and completion photos. The <a href="/claim-calculators/claim-deadline-calendar/">claim deadline calendar</a> can remind you before that window closes.</p>
""",
        "faqs": [("Can labor be depreciated in Arizona?", "Practice varies by policy and carrier, and the law on this question differs from state to state. Ask the carrier to explain in writing how labor was treated in your estimate."), ("What happens if I never repair?", "Under most replacement cost policies you keep the ACV payment but may not collect the held-back depreciation.")],
    },
    {
        "slug": "roof-squares-by-material", "name": "Roof Pitch, Squares & Material Calculator", "icon": "▲", "kind": "Calculator",
        "short": "Turn a footprint into true roof squares, then see field tiles, bundles or panels for your roof type.",
        "title": "Roof Squares Calculator for Tile, Shingle & Foam Roofs",
        "desc": "Estimate true roof area and squares from footprint and pitch, then see approximate tiles, bundles or panels for tile, shingle, metal or foam roofs.",
        "h1": "Roof Pitch, Squares and Material Calculator",
        "lede": "Measurement errors are one of the most common reasons a roof claim comes up short. Use your footprint and pitch to estimate true roof area, then see what that means for your roof material.",
        "markup": ROOF,
        "explain": """
<h2>The math</h2>
<p>A sloped roof has more surface than the ground beneath it. The pitch multiplier is √(1 + (rise ÷ 12)²). A 4/12 roof, common on Arizona tile homes, is about 5.4% larger than its footprint; a 12/12 roof is about 41.4% larger.</p>
<h2>Material notes</h2>
<ul><li><strong>Tile:</strong> field-tile counts here are approximate. Many standard concrete profiles run near 90 tiles per square; ridge, hip and rake trim are counted separately.</li>
<li><strong>Shingle:</strong> most architectural shingles come three bundles to a square.</li>
<li><strong>Metal:</strong> panel counts assume a common 3-foot coverage width and full-length panels; real counts depend on panel runs.</li>
<li><strong>Foam:</strong> low-slope foam is priced by area and thickness, so squares are what matter most.</li></ul>
<h2>Checking the estimate</h2>
<p>Compare the squares and waste in the carrier’s roof section with this result. Differences beyond about 5–10% deserve a closer look, as do missing ridge, starter, drip edge, underlayment and steep or high-roof charges. For complex roofs, aerial or field measurements beat any footprint calculation.</p>
""",
        "faqs": [("Why is my tile roof waste factor lower than a shingle roof’s?", "It is not always lower. Waste depends on hips, valleys and cuts. Complex tile roofs can carry substantial waste because broken pieces and cut tiles add up."), ("Does a 4/12 tile roof get a steep charge?", "Usually not. Steep charges typically start around 7/12 or 8/12, depending on the estimating system and carrier.")],
    },
    {
        "slug": "percentage-deductible-calculator", "name": "Percentage Deductible Calculator", "icon": "%", "kind": "Calculator",
        "short": "Convert a 1% or 2% wind/hail or all-peril deductible into dollars and see what a storm claim would pay.",
        "title": "Percentage Deductible Calculator | Wind, Hail & All-Peril",
        "desc": "Turn a percentage wind/hail or all-peril deductible into dollars and compare what an Arizona storm claim pays against a flat-dollar deductible.",
        "h1": "Percentage Deductible Calculator for Arizona Storm Claims",
        "lede": "A 1% deductible sounds tiny until you multiply it by your dwelling limit. See your deductible in real dollars and how it changes what a monsoon or hail claim pays.",
        "markup": DEDUCT,
        "explain": """
<h2>Why percentage deductibles surprise people</h2>
<p>Some Arizona homeowners policies apply a separate wind/hail deductible, or an all-peril deductible, calculated as a percentage of Coverage A. On a $465,000 dwelling limit, a 1% deductible is $4,650, not $1,000. As rebuilding costs rise, so do Coverage A limits, and so does the deductible.</p>
<h2>Where to find yours</h2>
<p>Look on the declarations page for “wind/hail,” “windstorm or hail” or a percentage next to the deductible. The endorsement later in the policy explains when it applies.</p>
<h2>How it affects appraisal</h2>
<p>The deductible does not change the amount of loss the panel decides, but it changes what you receive. A loss just over the deductible may not justify a dispute; one well above it may. Example figures here are illustrative.</p>
""",
        "faqs": [("Does the percentage apply to contents too?", "Usually the percentage is calculated from Coverage A but applied once to the whole covered wind or hail loss. Check your policy wording."), ("Can I change to a flat deductible?", "Often at renewal, if your carrier offers it. A lower deductible usually means a higher premium.")],
    },
    {
        "slug": "claim-deadline-calendar", "name": "Claim Deadline Calendar", "icon": "◷", "kind": "Planner",
        "short": "Map notice, proof-of-loss, holdback and suit dates from your date of loss, then download them to your calendar.",
        "title": "Claim Deadline Calendar | Proof of Loss & Suit Dates",
        "desc": "Enter your date of loss to map proof-of-loss, depreciation and suit-limitation dates for an Arizona property claim, then download an .ics file.",
        "h1": "Arizona Property Claim Deadline Calendar",
        "lede": "Policy deadlines keep running while you argue about the number. Enter your date of loss and your policy’s time limits to build a timeline you can drop into any calendar app.",
        "markup": DATES,
        "explain": """
<h2>The dates that matter</h2>
<ul><li><strong>Prompt notice.</strong> Policies require prompt notice of a loss. Late notice is one of the most common defenses an insurer raises.</li>
<li><strong>Proof of loss.</strong> If the carrier asks for a sworn proof of loss, many policies give 60 days to return it.</li>
<li><strong>Depreciation recovery.</strong> Replacement cost policies often require repairs within a set period, commonly 180 days to a year or more, to collect the holdback.</li>
<li><strong>Suit limitation.</strong> Many policies require any lawsuit within one or two years of the loss. Invoking appraisal does not automatically pause that clock.</li></ul>
<div class="note"><b class="h">Important</b>This calendar uses only the numbers you enter. It is not legal advice, and deadlines can be interpreted differently. If a deadline is close, talk to an Arizona attorney now.</div>
""",
        "faqs": [("Is the date of loss when I noticed the damage?", "Usually it is the date of the storm or event. Weather records for your address can help pin it down."), ("Does the .ics file upload anywhere?", "No. It is created in your browser and saved straight to your device.")],
    },
    {
        "slug": "claim-file-readiness-check", "name": "Claim File Readiness Check", "icon": "✓", "kind": "Checklist",
        "short": "Twelve yes/no questions that score your file and build a to-do list before you invoke appraisal.",
        "title": "Claim File Readiness Check | Ready for Appraisal?",
        "desc": "Answer twelve questions to score how ready your Arizona property claim is for appraisal, and get a personal to-do list of what to fix first.",
        "h1": "Claim File Readiness Check: Is Your File Ready for Appraisal?",
        "lede": "Appraisals are won or lost on the file you bring. Answer twelve quick questions to see where yours stands and what to fix before anyone signs a demand.",
        "markup": READY,
        "explain": """
<h2>How the score is weighted</h2>
<p>Coverage, estimates and evidence carry the most weight, because they decide whether appraisal is even the right tool and how well your number will hold up. The tile underlayment question is specific to Arizona: on tile roofs it often decides whether repair is possible at all.</p>
<h2>What to do with your score</h2>
<ul><li><strong>75 or higher:</strong> your file is in good shape. A professional review of the dollar gap is the logical next step.</li>
<li><strong>45 to 74:</strong> close the open items first. Each one strengthens your position.</li>
<li><strong>Below 45:</strong> invoking appraisal now risks locking in a low number. Build the file first.</li></ul>
""",
        "faqs": [("Are my answers saved?", "No. The check runs entirely in your browser and nothing is stored or sent."), ("Can I share the result?", "Yes. Take a screenshot of your score and to-do list and bring it to your consultation.")],
    },
    {
        "slug": "tile-roof-repair-or-replace-checker", "name": "Tile Roof Repair-or-Replace Checker", "icon": "◩", "kind": "Arizona tool",
        "short": "Weigh broken-tile share, underlayment age and tile availability, and compare spot repair with slope or full replacement.",
        "title": "Tile Roof Repair or Replace Checker | Arizona Claims",
        "desc": "Free Arizona tool: weigh broken tiles, underlayment age and discontinued profiles, then compare spot repair, slope and full tile roof replacement.",
        "h1": "Tile Roof Repair-or-Replace Checker",
        "lede": "On Arizona tile roofs the real question is rarely the tile. It is whether the roof can be repaired at all without destroying aging underlayment or leaving a patch that doesn’t match. This checker weighs those factors.",
        "markup": TILE,
        "explain": """
<h2>The three factors</h2>
<ul><li><strong>Breakage share.</strong> A handful of broken tiles on a large roof points toward repair. Breakage across many slopes points the other way.</li>
<li><strong>Underlayment age.</strong> Tiles shed most water, but the underlayment is the waterproofing. After roughly 20 years in desert heat, felt underlayment can be too brittle to survive tiles being lifted and reset.</li>
<li><strong>Tile availability.</strong> Concrete tile profiles and colors are discontinued regularly. A patch of mismatched tile on a visible slope is a matching question, not just a cosmetic one.</li></ul>
<h2>How the cost comparison works</h2>
<p>Spot repair multiplies broken tiles by a per-tile remove-and-reset figure. Slope and full replacement multiply squares by a tear-off-and-re-lay figure, which should include new underlayment, battens where needed and reuse or replacement of tile. All unit prices are editable and illustrative. Ask local roofers for current figures.</p>
<div class="note"><b class="h">Not a coverage opinion</b>Whether your policy pays for matching or for replacing undamaged sections depends on its wording and on Arizona law. This tool organizes the valuation facts so you can discuss them clearly.</div>
""",
        "faqs": [("Why does the checker care about underlayment if the storm only broke tiles?", "Because repairing broken tiles means lifting surrounding tiles. If the underlayment can’t survive that, a true repair may require replacing it, which changes the cost dramatically."), ("Where do I find tiles per square?", "Ask your roofer or check the manufacturer’s data for your profile. About 90 is common for many standard concrete tiles, but flat and specialty profiles differ.")],
    },
]
