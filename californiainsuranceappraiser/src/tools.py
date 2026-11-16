"""Interactive claim tools: markup + explanatory copy. Logic lives in static/assets/js/app.js.
Every tool runs in the browser; nothing is sent or stored."""

T = "/claim-check-tools/"

GAP_FULL = """
<div class="tool" data-tool="gap">
  <div class="tool-head"><h2 class="tool-t">Appraisal payoff estimator</h2><i>Runs in your browser</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Carrier’s estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="42600"><span class="hint">Replacement cost total on the insurer’s estimate.</span></div>
        <div><label for="g-own">Your estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="68900"><span class="hint">Your contractor’s or independent estimate.</span></div>
      </div>
      <div><label for="g-land">Where might the award land inside the gap?</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% means the carrier’s number holds. 100% means your full number is awarded.</span></div>
      <div class="row2">
        <div><label for="g-ft">Appraiser fee type</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of the increase (%)</option></select></div>
        <div><label for="g-fee">Fee amount</label><input id="g-fee" name="fee" inputmode="decimal" value="3500"></div>
      </div>
      <label class="check"><input type="checkbox" name="useump" checked> Include my half of the umpire’s fee</label>
      <div><label for="g-ump">Umpire’s total fee (split 50/50)</label><input id="g-ump" name="umpire" inputmode="decimal" value="4000"></div>
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
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

GAP_MINI = """
<div class="tool tool-mini" data-tool="gap">
  <div class="tool-head"><h3 class="tool-t">Two-number gap check</h3><i>Nothing is stored</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="m-ins">Carrier’s estimate</label><input id="m-ins" name="insurer" inputmode="decimal" value="31800"></div>
      <div><label for="m-own">Your contractor’s estimate</label><input id="m-own" name="yours" inputmode="decimal" value="52400"></div>
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
  <div class="tool-head"><h2 class="tool-t">ACV &amp; holdback calculator</h2><i>Add as many lines as you need</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Concrete tile roof — underlayment & reset", 24800, 14, 30), ("Interior paint — smoke-affected rooms", 6900, 5, 10), ("Wool area rugs", 3200, 7, 15)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn ghost small" data-add data-run>+ Add a line</button></div>
      <div class="row2">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="2500"></div>
        <div><label for="d-cap">Depreciation cap</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="90">90%</option></select><span class="hint">Many estimates cap depreciation; check yours.</span></div>
      </div>
      <label class="check"><input type="checkbox" name="nonrec"> My policy pays actual cash value only (for example, many FAIR Plan dwelling policies)</label>
    </div>
    <div class="tool-out tool-out-3" aria-live="polite">
      <div class="out-big"><small>First check (ACV − deductible)</small><b data-o="first">$0</b></div>
      <div class="out-big"><small>Held back until you replace</small><b data-o="held">$0</b></div>
      <div class="out-big"><small>Total if fully recovered</small><b data-o="total">$0</b></div>
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
  <div class="tool-head"><h2 class="tool-t">Roof area &amp; pitch calculator</h2><i>Check the squares on your estimate</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <fieldset class="bare"><legend class="sr-only">Measurement method</legend>
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
        <div><label for="r-p">Roof pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 5 else "", p) for p in [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14]) + """</select></div>
        <div><label for="r-mat">Roofing material</label><select id="r-mat" name="mat"><option value="tile" selected>Concrete or clay tile</option><option value="shingle">Composition shingle</option><option value="shake">Wood shake</option><option value="low">Low-slope membrane</option></select></div>
      </div>
      <div class="row2">
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="8">8% — simple gable</option><option value="12" selected>12% — gable with hips</option><option value="15">15% — hip roof</option><option value="20">20% — cut-up / complex</option></select></div>
        <div><label for="r-pr">Installed price per square (optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 1150"></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Roof squares (before waste)</small><b data-o="sq">0</b></div>
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

QUAKE = """
<div class="tool" data-tool="deduct">
  <div class="tool-head"><h2 class="tool-t">Earthquake deductible calculator</h2><i>Percentage vs. flat</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling limit on the earthquake policy</label><input id="w-a" name="cova" inputmode="decimal" value="650000"><span class="hint">From your earthquake policy declarations.</span></div>
      <div class="row2">
        <div><label for="w-p">Earthquake deductible</label><select id="w-p" name="pct"><option value="5">5%</option><option value="10">10%</option><option value="15" selected>15%</option><option value="20">20%</option><option value="25">25%</option></select></div>
        <div><label for="w-f">Your regular homeowner deductible</label><input id="w-f" name="flat" inputmode="decimal" value="2500"><span class="hint">For comparison only.</span></div>
      </div>
      <div><label for="w-l">Estimated earthquake damage to the dwelling</label><input id="w-l" name="loss" inputmode="decimal" value="138000"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your earthquake deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s3"></span><span class="s1"></span></div>
      <div class="legend"><span><i class="s3"></i>You pay</span><span><i class="s1"></i>Policy pays</span></div>
      <div class="out-rows">
        <div><span>Dwelling payment after % deductible</span><b data-o="pdpay">$0</b></div>
        <div><span>Payment if a flat deductible applied</span><b data-o="flatpay">$0</b></div>
        <div><span>Extra out-of-pocket from the % deductible</span><b data-o="diff">$0</b></div>
      </div>
      <p class="out-msg" data-o="below"></p>
    </div>
  </div>
</div>"""

DATES = """
<div class="tool" data-tool="dates">
  <div class="tool-head"><h2 class="tool-t">California claim timeline builder</h2><i>Exports to your calendar</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
      <div><label for="t-c">Date you reported the claim (optional)</label><input id="t-c" type="date" name="reported"><span class="hint">Leave blank to assume the date of loss.</span></div>
      <label class="check"><input type="checkbox" name="emerg"> The loss is tied to a declared state of emergency (for example, a major wildfire)</label>
      <div class="days-grid">
        <div><label for="t-r">Replacement cost window (months)</label><input id="t-r" name="rcm" inputmode="numeric" value="12"><span class="hint">Becomes 36 when the box above is checked.</span></div>
        <div><label for="t-s">Suit limitation (months)</label><input id="t-s" name="suitm" inputmode="numeric" value="12"><span class="hint">Becomes 24 when the box above is checked.</span></div>
      </div>
      <p class="hint">Defaults reflect common California rules, not legal advice. Policies and statutes can differ, and some periods are tolled while a claim is open. Confirm every date with your policy or an attorney.</p>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download .ics calendar file</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the insurer accepted coverage for at least part of the loss?", "Get written confirmation that coverage is accepted. If the claim was denied, talk to a California attorney before considering appraisal."),
    (3, "Do you have the carrier’s complete, itemized estimate?", "Ask for the full line-item estimate in writing, not just the summary page."),
    (3, "Do you have your own itemized estimate?", "Get an independent line-item estimate. A lump-sum bid is hard for a panel to compare."),
    (2, "Do you have dated photos taken soon after the loss?", "Gather every photo and note when each was taken. Add photos of current conditions."),
    (2, "Have you found the appraisal paragraph in your policy?", "Find ‘Appraisal’ in the conditions section and note the 20-day and 15-day windows."),
    (2, "Do you know your suit-limitation date?", "Find the ‘Suit Against Us’ clause and calendar it. Our timeline builder can help."),
    (2, "Have temporary repairs been made and receipts saved?", "Complete reasonable temporary repairs, such as tarping or drying, and keep every receipt."),
    (1, "Do you have your current declarations page?", "Download or request your declarations page, including any endorsements."),
    (2, "Has hidden damage been opened up and documented?", "Make sure wet walls, attics, ducts and roof decking are inspected so the scope is complete."),
    (1, "Is your correspondence with the carrier organized by date?", "Collect emails, letters and claim notes in date order."),
    (2, "Is the gap between estimates more than about 10% or $5,000?", "Run the numbers in our appraisal payoff estimator. A small gap may not justify appraisal costs."),
    (1, "Do you know whether you have a FAIR Plan, DIC or earthquake policy too?", "List every policy that might apply, including FAIR Plan, difference-in-conditions and earthquake policies."),
]

READY = """
<div class="tool tool-wide" data-tool="ready">
  <div class="tool-head"><h2 class="tool-t">Appraisal readiness check</h2><i>12 questions · about two minutes</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <ol class="quiz">""" + "".join(
    '<li data-w="%d" data-fix="%s"><span>%s</span><span class="yn"><button type="button" class="yes" aria-pressed="false">Yes</button><button type="button" class="no" aria-pressed="false">No</button></span></li>' % (w, f, q)
    for w, q, f in _QUIZ) + """
      </ol>
      <div class="btn-row"><button type="button" class="btn ghost small" data-reset>Reset answers</button></div>
    </div>
    <div class="tool-out tool-out-gauge" aria-live="polite">
      <div>
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#efe3d6" stroke-width="18"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#b58150" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3" style="transition:stroke-dashoffset .5s,stroke .3s"/></svg>
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

REBUILD = """
<div class="tool" data-tool="rebuild">
  <div class="tool-head"><h2 class="tool-t">Rebuild cost &amp; underinsurance check</h2><i>For total-loss planning</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="b-sf">Living area (sq ft)</label><input id="b-sf" name="sqft" inputmode="decimal" value="2150"></div>
        <div><label for="b-ps">Rebuild cost per sq ft ($)</label><input id="b-ps" name="psf" inputmode="decimal" value="525"><span class="hint">Use a local builder’s figure. Hillside and custom homes run higher.</span></div>
      </div>
      <div class="row2">
        <div><label for="b-a">Dwelling limit (Coverage A)</label><input id="b-a" name="cova" inputmode="decimal" value="890000"></div>
        <div><label for="b-e">Extended replacement cost</label><select id="b-e" name="erc"><option value="0">None</option><option value="10">10%</option><option value="20">20%</option><option value="25" selected>25%</option><option value="50">50%</option><option value="100">100%</option></select></div>
      </div>
      <div class="row2">
        <div><label for="b-c">Building code upgrade limit (% of A)</label><select id="b-c" name="code"><option value="0">None</option><option value="10" selected>10%</option><option value="25">25%</option><option value="50">50%</option></select></div>
        <div><label for="b-cc">Estimated code-required work ($)</label><input id="b-cc" name="codecost" inputmode="decimal" value="85000"></div>
      </div>
      <div class="row2">
        <div><label for="b-d">Debris removal cost ($)</label><input id="b-d" name="debris" inputmode="decimal" value="60000"></div>
        <div><label for="b-dl">Debris removal additional limit (% of A)</label><select id="b-dl" name="debrispct"><option value="0">None / within A</option><option value="5" selected>5%</option><option value="10">10%</option></select></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated shortfall</small><b data-o="short">$0</b></div>
      <div class="meter" aria-hidden="true"><span data-o="meter"></span></div>
      <div class="out-rows">
        <div><span>Estimated rebuild cost</span><b data-o="rebuild">$0</b></div>
        <div><span>Dwelling limit incl. extended RC</span><b data-o="avail">$0</b></div>
        <div><span>Code upgrade coverage used</span><b data-o="codeused">$0</b></div>
        <div><span>Debris removal covered</span><b data-o="debrisused">$0</b></div>
        <div><span>Total project cost</span><b data-o="project">$0</b></div>
        <div><span>Coverage as % of project</span><b data-o="ratio">—</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "appraisal-payoff-estimator", "name": "Appraisal Payoff Estimator", "icon": "scale", "kind": "Estimator",
        "short": "See the disputed amount, a projected award and what you’d net after appraiser and umpire fees.",
        "title": "Appraisal Payoff Estimator | Is Appraisal Worth It?",
        "desc": "Free appraisal payoff estimator: compare two estimates, project an award and subtract appraiser and umpire fees to see your net gain.",
        "h1": "Appraisal Payoff Estimator: Will Appraisal Be Worth the Cost?",
        "lede": "Enter the carrier’s estimate and yours, choose where an award might land, and add realistic fees. The estimator shows whether appraisal is likely to leave you ahead.",
        "markup": GAP_FULL,
        "explain": f"""
<h2>How to use the payoff estimator</h2>
<ol><li><strong>Enter the carrier’s RCV total,</strong> the replacement cost figure before depreciation and deductible.</li>
<li><strong>Enter your estimate,</strong> also at replacement cost.</li>
<li><strong>Move the slider</strong> to test outcomes. Try 30%, 50% and 80% to see a range.</li>
<li><strong>Add fees.</strong> Use your appraiser’s quoted arrangement and a realistic umpire fee.</li></ol>
<h2>Reading the result</h2>
<p>Awards rarely match either opening number. Documented line items tend to hold and unsupported ones tend to fall. If your result only works at 90% or more, the case is fragile. If it still makes sense at 40%, appraisal is more likely to be worthwhile. All default figures are illustrative.</p>
<h2>What it leaves out</h2>
<p>It doesn’t model depreciation timing, policy limits or deductibles. For holdback math, use the <a href="{T}acv-holdback-calculator/">ACV and holdback calculator</a>; for total losses, try the <a href="{T}rebuild-cost-underinsurance-check/">rebuild cost check</a>.</p>
""",
        "faqs": [("Is the projected award a prediction?", "No. It’s a planning scenario. Real awards depend on documentation, the panel and the policy."), ("How much is a typical umpire fee?", "It varies with the size and complexity of the dispute. Under the standard California wording, the umpire’s fee is split equally.")],
    },
    {
        "slug": "acv-holdback-calculator", "name": "ACV & Holdback Calculator", "icon": "file", "kind": "Calculator",
        "short": "Estimate the first ACV check, the depreciation held back and the total once you replace or rebuild.",
        "title": "ACV & Holdback Calculator | Recoverable Depreciation",
        "desc": "Free ACV and holdback calculator: estimate your first check, recoverable depreciation and total payment under a replacement cost policy.",
        "h1": "ACV and Holdback Calculator for Replacement Cost Claims",
        "lede": "Replacement cost policies usually pay in two stages. This calculator estimates both, line by line, so you know what to expect and what to collect later.",
        "markup": DEP,
        "explain": """
<h2>How the two payments work</h2>
<p>With replacement cost coverage, the carrier generally pays the actual cash value first: replacement cost minus depreciation, minus your deductible. The depreciation is held back until you repair or replace, then paid up to what you actually spend.</p>
<h2>California time limits</h2>
<p>Insurance Code §2051.5 generally gives you at least 12 months from the first actual cash value payment to collect the holdback, and at least 36 months after a loss tied to a declared state of emergency, with extensions for good cause. Your policy may give you longer. These are legal rules, so confirm them for your loss.</p>
<h2>Checking depreciation</h2>
<ul><li>Depreciation should reflect condition and life, not a flat rate for every item.</li><li>Some carriers depreciate labor; whether that is appropriate depends on the policy and the item.</li><li>Use the cap selector to match the maximum depreciation shown on your estimate.</li></ul>
""",
        "faqs": [("Why is my first check so much smaller than the estimate?", "Because depreciation and the deductible are subtracted first. The holdback is paid after you replace or repair."), ("What if my policy is actual cash value only?", "Check the box. You won’t receive a holdback, so the first check is the total. Many FAIR Plan dwelling policies are written that way unless replacement cost was added.")],
    },
    {
        "slug": "roof-area-pitch-calculator", "name": "Roof Area & Pitch Calculator", "icon": "home", "kind": "Calculator",
        "short": "Convert a footprint and pitch into roof squares, with tile or shingle counts and a rough cost.",
        "title": "Roof Area & Pitch Calculator | Squares for Tile Roofs",
        "desc": "Free roof area and pitch calculator: turn a footprint and pitch into roof squares, waste and tile or shingle counts to check an estimate.",
        "h1": "Roof Area and Pitch Calculator for Tile and Shingle Roofs",
        "lede": "Check the square count on the carrier’s estimate. Enter the footprint and pitch, pick your roofing, and see squares, waste and a rough material count.",
        "markup": ROOF,
        "explain": f"""
<h2>How roof squares work</h2>
<p>A roofing square is 100 square feet of roof surface. Because roofs slope, the surface is larger than the footprint. The pitch multiplier converts one into the other: a 5/12 roof has about 8% more surface than its footprint, a 12/12 roof about 41% more.</p>
<h2>Tile versus shingle</h2>
<p>Standard concrete tile runs roughly 85 to 95 field pieces per square, depending on profile; composition shingles usually come three bundles to a square. Tile roofs also need underlayment, battens, hip and ridge pieces and bird stops that are priced separately. The material counts here are approximate.</p>
<h2>What to compare</h2>
<p>If the estimate’s squares are well below the calculator’s figure, check whether a slope, a porch roof or a garage was left out, and whether waste was applied. Then read about <a href="/disputed-claim-services/roof-damage-appraisal/">roof damage appraisal</a>.</p>
""",
        "faqs": [("Is this as accurate as a measurement report?", "No. It is a quick check. Aerial reports and field measurements are more precise, especially on complex roofs."), ("Why does waste differ by roof shape?", "Hips, valleys and cut-up sections require more cutting, so more material is wasted.")],
    },
    {
        "slug": "earthquake-deductible-calculator", "name": "Earthquake Deductible Calculator", "icon": "storm", "kind": "Calculator",
        "short": "Turn a percentage earthquake deductible into dollars and see what the policy would actually pay.",
        "title": "Earthquake Deductible Calculator | Percent to Dollars",
        "desc": "Free earthquake deductible calculator: convert a 5% to 25% deductible into dollars and see what a California earthquake policy would pay.",
        "h1": "Earthquake Deductible Calculator for California Policies",
        "lede": "Earthquake deductibles are a percentage of the dwelling limit, so they can be far larger than you expect. See the real number before you need it.",
        "markup": QUAKE,
        "explain": """
<h2>Why earthquake deductibles are different</h2>
<p>Standard homeowner policies exclude earthquake damage. Earthquake coverage comes from a separate policy, such as one from the California Earthquake Authority or a private insurer. Those policies typically use a percentage deductible, commonly between 5% and 25% of the dwelling limit. On a $650,000 dwelling limit, an illustrative 15% deductible is $97,500.</p>
<h2>What the calculator shows</h2>
<ul><li>The deductible in dollars.</li><li>What the dwelling coverage would pay on the damage you enter.</li><li>How that compares with a flat deductible, to show why the difference matters.</li></ul>
<p>Some earthquake policies apply deductibles differently to contents or loss of use. Check your declarations page.</p>
<h2>Fire following an earthquake</h2>
<p>Fire that follows an earthquake is generally covered under the standard homeowner fire coverage, not the earthquake policy, so the earthquake deductible would not apply to that part of the loss.</p>
""",
        "faqs": [("Does the earthquake deductible apply to contents?", "It depends on the policy. Some earthquake policies apply the deductible only to dwelling losses. Read your declarations page."), ("Can I lower my earthquake deductible?", "Many earthquake policies offer several deductible options at different premiums. Ask your agent.")],
    },
    {
        "slug": "claim-timeline-builder", "name": "Claim Timeline Builder", "icon": "clock", "kind": "Planner",
        "short": "Map California claim milestones from your date of loss and export them to your calendar.",
        "title": "California Claim Timeline Builder | .ics Export",
        "desc": "Free California claim timeline builder: map insurer response windows, replacement cost and suit deadlines, then export them to a calendar.",
        "h1": "California Claim Timeline Builder with Calendar Export",
        "lede": "Enter your date of loss, flag whether it was a declared disaster, and get a dated list of milestones you can download to your calendar.",
        "markup": DATES,
        "explain": """
<h2>What the timeline includes</h2>
<ul>
<li><strong>Insurer acknowledgment:</strong> California’s Fair Claims Settlement Practices Regulations generally require insurers to acknowledge a claim within 15 calendar days of notice.</li>
<li><strong>Coverage decision:</strong> they generally require insurers to accept or deny within 40 days of receiving proof of claim.</li>
<li><strong>Appraisal windows:</strong> 20 days to name an appraiser after a written demand under the standard wording.</li>
<li><strong>Replacement cost window:</strong> at least 12 months, or at least 36 months after a declared state of emergency.</li>
<li><strong>Suit limitation:</strong> commonly 12 months, or 24 months for losses tied to a declared state of emergency, with tolling while the claim is open.</li>
</ul>
<h2>Important limits</h2>
<p>These are general rules. Your policy may give you more time, and tolling depends on facts. Use this tool to stay organized, and confirm critical dates with an attorney.</p>
""",
        "faqs": [("Is the suit date exact?", "No. California tolls the limitation period from notice until the claim is denied in writing, so the real date may be later. Get legal advice before relying on it."), ("Is my data sent anywhere?", "No. The dates stay in your browser, and the calendar file is created on your device.")],
    },
    {
        "slug": "appraisal-readiness-check", "name": "Appraisal Readiness Check", "icon": "doc", "kind": "Checklist",
        "short": "Twelve questions that score your file and list what to fix before you demand appraisal.",
        "title": "Appraisal Readiness Check | 12-Question Claim Score",
        "desc": "Free appraisal readiness check: answer 12 questions, get a score and a to-do list of what your file needs before you demand appraisal.",
        "h1": "Appraisal Readiness Check: Is Your File Ready for a Panel?",
        "lede": "A panel decides on what’s in the file. Answer twelve questions to see where yours stands and what to fix before you send a demand.",
        "markup": READY,
        "explain": """
<h2>Why readiness matters</h2>
<p>California appraisal is informal: there’s no discovery and no testimony under oath. The panel works from estimates, photos, invoices and reports. Gaps in the file usually become gaps in the award.</p>
<h2>How the score works</h2>
<p>Each question is weighted by how much it typically affects an appraisal. Coverage, estimates and photos carry the most weight. The to-do list shows only the items you answered “no.”</p>
<h2>After the check</h2>
<p>Close the gaps, then run the <a href="/claim-check-tools/appraisal-payoff-estimator/">payoff estimator</a>. If both look good, it’s a good time to talk to us.</p>
""",
        "faqs": [("Is a high score a guarantee?", "No. It means your file has the basics a panel expects. The outcome still depends on the facts."), ("Are my answers saved?", "No. Everything runs in your browser and resets when you leave.")],
    },
    {
        "slug": "rebuild-cost-underinsurance-check", "name": "Rebuild Cost & Underinsurance Check", "icon": "flame", "kind": "Estimator",
        "short": "Compare a rebuild estimate with your dwelling limit, extended replacement cost, code and debris coverage.",
        "title": "Rebuild Cost & Underinsurance Check | Wildfire Losses",
        "desc": "Free rebuild cost and underinsurance check: compare the cost to rebuild with your dwelling limit, extended replacement and code coverage.",
        "h1": "Rebuild Cost and Underinsurance Check for Total Losses",
        "lede": "After a wildfire, the question is whether the policy can pay for the rebuild. Enter your square footage, a local cost per foot and your limits to see the likely gap.",
        "markup": REBUILD,
        "explain": """
<h2>Why underinsurance is so common in California</h2>
<p>Dwelling limits are often set when a policy is written and adjusted by inflation factors that don’t track local construction costs. After major wildfires, demand for builders and materials can push costs higher still. Many owners who lost homes in the Tubbs, Camp and 2025 Los Angeles fires found their limits fell short.</p>
<h2>What the check includes</h2>
<ul>
<li><strong>Extended replacement cost:</strong> an extra percentage above the dwelling limit when the rebuild costs more.</li>
<li><strong>Building code upgrade coverage:</strong> a separate amount, often a percentage of the dwelling limit, for code-required work.</li>
<li><strong>Debris removal:</strong> many policies add a percentage of the dwelling limit for debris removal; otherwise it comes out of the dwelling limit.</li>
</ul>
<h2>Using the result</h2>
<p>Appraisal cannot raise limits. It can establish the full rebuild cost, which determines whether extended replacement cost and code coverage are reached. If the shortfall is large, talk to us about a <a href="/disputed-claim-services/wildfire-total-loss-appraisal/">wildfire total loss appraisal</a>. Figures in the tool are illustrative.</p>
""",
        "faqs": [("Where do I get a cost per square foot?", "From local builders who rebuild after fires, or from a professional estimate. Generic online figures are often too low for California."), ("Does this include contents and ALE?", "No. It covers the dwelling, code upgrades and debris removal only.")],
    },
]
