"""Free claim calculators: markup + explanatory copy. Logic lives in static/assets/js/app.js.
Everything runs in the browser; nothing is sent or stored."""

BASE = "/free-appraisal-tools/"


def _f(i, label, name, value="", hint="", extra="", attrs='inputmode="decimal"'):
    h = f'<span class="hint">{hint}</span>' if hint else ""
    return f'<div{extra}><label for="{i}">{label}</label><input id="{i}" name="{name}" {attrs} value="{value}">{h}</div>'


GAP_FULL = f"""
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Claim gap &amp; fee estimator</span><i>Three outcomes, net of fees</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">{_f("g-ins", "Carrier’s estimate (RCV, $)", "insurer", "21600", "The replacement-cost total on the insurer’s estimate.")}{_f("g-own", "Your estimate (RCV, $)", "yours", "36900", "From your contractor or an independent estimator.")}</div>
      <div><label for="g-land">Most likely landing point within the gap</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">The tool also shows a cautious case (30 points lower) and a strong case (25 points higher).</span></div>
      <div class="row2">
        <div><label for="g-ft">Your appraiser’s fee</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of the increase (%)</option><option value="hourly">Hourly (hours × rate)</option></select></div>
        {_f("g-fee", "Fee amount or hourly rate", "fee", "2800")}
      </div>
      {_f("g-hrs", "Hours (hourly fee only)", "hours", "20", "", ' data-show="hourly" hidden')}
      <label class="check"><input type="checkbox" name="useump" checked> An umpire is needed (you pay half)</label>
      {_f("g-ump", "Umpire’s total fee ($)", "umpire", "3200")}
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Likely net increase to you</small><b data-o="net">$0</b></div>
      <div class="scen">
        <div><small>Cautious</small><b data-o="s-low">$0</b></div>
        <div class="on"><small>Likely</small><b data-o="s-mid">$0</b></div>
        <div><small>Strong</small><b data-o="s-high">$0</b></div>
      </div>
      <div class="stack" aria-hidden="true"><span class="c1"></span><span class="c2"></span><span class="c3"></span></div>
      <div class="legend"><span><i class="c1"></i>Carrier’s number</span><span><i class="c2"></i>Your net gain</span><span><i class="c3"></i>Appraisal costs</span></div>
      <div class="out-rows">
        <div><span>Amount in dispute</span><b data-o="gap">$0</b></div>
        <div><span>Gap as % of carrier estimate</span><b data-o="pct">—</b></div>
        <div><span>Likely award (RCV)</span><b data-o="award">$0</b></div>
        <div><span>Your appraisal costs</span><b data-o="cost">$0</b></div>
        <div><span>Break-even landing point</span><b data-o="be">—</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

GAP_MINI = f"""
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Side-by-side gap check</span><i>No sign-up</i></div>
  <div class="tool-body">
    <div class="tool-in">
      {_f("m-ins", "Carrier’s estimate ($)", "insurer", "17350")}
      {_f("m-own", "Your contractor’s estimate ($)", "yours", "29800")}
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
  <div class="tool-head"><span>RCV / ACV &amp; holdback calculator</span><i>Line by line</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Standing-seam metal roof", 24800, 12, 40), ("Vinyl siding — two elevations", 6900, 15, 30), ("Hardwood flooring — kitchen", 5200, 8, 25)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn ghost small" data-add data-run>+ Add a line</button></div>
      <div class="row2">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="1000"></div>
        <div><label for="d-cap">Depreciation cap</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="90">90%</option></select><span class="hint">Many estimates stop depreciating at a ceiling.</span></div>
      </div>
      <div class="row2">
        <div><label for="d-days">Days your policy allows to finish repairs</label><input id="d-days" name="days" inputmode="numeric" value="180"><span class="hint">Check the replacement-cost condition in your policy.</span></div>
        <div><label for="d-start">First ACV check date (optional)</label><input id="d-start" name="start" type="date"></div>
      </div>
      <label class="check"><input type="checkbox" name="nonrec"> My policy settles at actual cash value only (no recoverable depreciation)</label>
    </div>
    <div class="tool-out wide" aria-live="polite">
      <div class="out-big"><small>First check (ACV − deductible)</small><b data-o="first">$0</b></div>
      <div class="out-big"><small>Held back until repairs</small><b data-o="held">$0</b></div>
      <div class="out-big"><small>Total if fully recovered</small><b data-o="total">$0</b></div>
      <div class="out-rows span">
        <div><span>Replacement cost (RCV)</span><b data-o="rcv">$0</b></div>
        <div><span>Total depreciation</span><b data-o="dep">$0</b></div>
        <div><span>Depreciation as share of RCV</span><b data-o="deppct">0%</b></div>
        <div><span>Actual cash value (ACV)</span><b data-o="acv">$0</b></div>
        <div><span>Finish repairs and claim the holdback by</span><b data-o="by">—</b></div>
      </div>
    </div>
  </div>
</div>"""

ROOF = """
<div class="tool" data-tool="roof">
  <div class="tool-head"><span>Roof square &amp; pitch estimator</span><i>Check the carrier’s count</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <fieldset class="plain"><legend class="sr-only">Measurement method</legend>
        <div class="btn-row">
          <label class="check"><input type="radio" name="mode" value="dims" checked> Footprint length × width</label>
          <label class="check"><input type="radio" name="mode" value="area"> I know the footprint area</label>
        </div></fieldset>
      <div class="row2" data-mode="dims">
        <div><label for="r-l">Footprint length (ft)</label><input id="r-l" name="len" inputmode="decimal" value="46"></div>
        <div><label for="r-w">Footprint width (ft)</label><input id="r-w" name="wid" inputmode="decimal" value="30"></div>
      </div>
      <div data-mode="dims"><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="12"></div>
      <div data-mode="area" hidden><label for="r-a">Footprint area incl. overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="1600"></div>
      <div class="row2">
        <div><label for="r-p">Roof pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 8 else "", p) for p in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16]) + """</select><span class="hint">Older two-story homes in river towns are often 8/12 to 12/12.</span></div>
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="5">5% — metal panels, simple gable</option><option value="10">10% — simple gable</option><option value="12" selected>12% — gable with dormers</option><option value="15">15% — hip roof</option><option value="18">18% — cut-up / valleys</option></select></div>
      </div>
      <div class="row2">
        <div><label for="r-c">Squares on the carrier’s estimate (optional)</label><input id="r-c" name="carrier" inputmode="decimal" placeholder="e.g. 18.5"></div>
        <div><label for="r-pr">Installed price per square (optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 560"></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Roof squares (before waste)</small><b data-o="sq">0</b></div>
      <div class="out-rows">
        <div><span>Pitch multiplier</span><b data-o="mult">1.000</b></div>
        <div><span>Roof surface area</span><b data-o="surface">0</b></div>
        <div><span>Squares with waste</span><b data-o="order">0</b></div>
        <div><span>Shingle bundles (3 per square)</span><b data-o="bundles">0</b></div>
        <div><span>Difference vs. carrier’s squares</span><b data-o="vs">—</b></div>
        <div><span>Rough replacement cost</span><b data-o="cost">—</b></div>
      </div>
      <p class="out-msg" data-o="steep"></p>
    </div>
  </div>
</div>"""

DEDUCT = """
<div class="tool" data-tool="deduct">
  <div class="tool-head"><span>Percentage deductible checker</span><i>1% to 5% side by side</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling coverage (Coverage A, $)</label><input id="w-a" name="cova" inputmode="decimal" value="265000"><span class="hint">On your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Your percentage deductible</label><select id="w-p" name="pct"><option value="0.5">0.5%</option><option value="1" selected>1%</option><option value="2">2%</option><option value="3">3%</option><option value="5">5%</option></select></div>
        <div><label for="w-f">Your flat deductible ($)</label><input id="w-f" name="flat" inputmode="decimal" value="1000"></div>
      </div>
      <div><label for="w-l">Estimated covered damage ($)</label><input id="w-l" name="loss" inputmode="decimal" value="14800"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your percentage deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="c3"></span><span class="c1"></span></div>
      <div class="legend"><span><i class="c3"></i>You pay</span><span><i class="c1"></i>Policy pays</span></div>
      <div class="out-rows">
        <div><span>Payment with the % deductible</span><b data-o="pdpay">$0</b></div>
        <div><span>Payment with the flat deductible</span><b data-o="flatpay">$0</b></div>
        <div><span>Extra out of pocket</span><b data-o="diff">$0</b></div>
      </div>
      <div class="table-wrap mini"><table><thead><tr><th>Deductible</th><th>You pay</th><th>Policy pays</th></tr></thead><tbody data-o="ladder"></tbody></table></div>
      <p class="out-msg" data-o="below"></p>
    </div>
  </div>
</div>"""

DATES = """
<div class="tool" data-tool="dates">
  <div class="tool-head"><span>Claim timeline planner</span><i>Exports an .ics calendar</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
      <p class="hint flush">Change each window to match your policy and letters. Defaults are placeholders, not legal deadlines.</p>
      <div class="days-grid">
        <div><label for="t-n">Report the claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="3"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="10"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Usually counted from the insurer’s request.</span></div>
        <div><label for="t-a">Name your appraiser within (days of a demand)</label><input id="t-a" name="appr" inputmode="numeric" value="20"></div>
        <div><label for="t-r">Repairs for depreciation holdback (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="180"></div>
        <div><label for="t-s">Suit-limitation clause (days)</label><input id="t-s" name="suit" inputmode="numeric" value="365"><span class="hint">Use the shorter figure until you confirm yours.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download the .ics file</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the insurer accepted coverage for at least part of the loss?", "Get coverage confirmed in writing. If the claim was denied, talk with a West Virginia attorney before thinking about appraisal."),
    (3, "Do you have the insurer’s full line-item estimate (not just a summary letter)?", "Ask the adjuster for the complete itemized estimate as a PDF."),
    (3, "Do you have your own itemized estimate?", "Get a line-item estimate from a contractor or estimator. A one-line bid is hard to defend before a panel."),
    (2, "Are there dated photos from the first days after the loss?", "Collect every photo and video and note the date each was taken."),
    (2, "Have you read the Appraisal paragraph in your policy conditions?", "Find it, and write down any deadline it sets for naming an appraiser."),
    (2, "Have you put the suit-limitation date on a calendar?", "Look for the “Suit Against Us” condition and calendar the date with our timeline planner."),
    (2, "Were temporary repairs made, with receipts saved?", "Make reasonable temporary repairs (tarps, drying, board-up) and keep every receipt."),
    (2, "Has hidden damage been opened and documented?", "Make sure wet walls, attic framing, decking and crawlspaces were checked so the scope is complete."),
    (1, "Do you have the current declarations page?", "Download it or ask your agent for a copy."),
    (1, "Is your correspondence with the insurer saved in date order?", "Gather emails, letters and claim notes in one folder."),
    (2, "Is the gap more than roughly 10% or several thousand dollars?", "Run the numbers in the claim gap & fee estimator. A small gap may not justify appraisal costs."),
    (1, "Is it clear which items are disputed on price versus scope?", "Mark each disputed line as “price” or “scope.” Appraisers resolve both, but you should know which is which."),
]

READY = """
<div class="tool tool-wide" data-tool="ready">
  <div class="tool-head"><span>Appraisal readiness scorecard</span><i>12 questions · two minutes</i></div>
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
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true" width="200" height="110"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#e3ebdd" stroke-width="18"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#15370d" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3"/></svg>
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

MINE = """
<div class="tool" data-tool="mine">
  <div class="tool-head"><span>Mine subsidence limit calculator</span><i>Endorsement cap vs. repair cost</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="s-a">Dwelling coverage (Coverage A, $)</label><input id="s-a" name="cova" inputmode="decimal" value="210000"></div>
        <div><label for="s-c">Mine subsidence cap ($)</label><input id="s-c" name="cap" inputmode="decimal" value="75000"><span class="hint">Commonly described as up to $75,000 — confirm the figure in your endorsement.</span></div>
      </div>
      <div class="row2">
        <div><label for="s-p">Deductible (% of the subsidence limit)</label><input id="s-p" name="dpct" inputmode="decimal" value="2"></div>
        <div><label for="s-mn">Deductible floor / ceiling ($)</label><div class="pair"><input id="s-mn" name="dmin" inputmode="decimal" value="250" aria-label="Deductible minimum"><input name="dmax" inputmode="decimal" value="500" aria-label="Deductible maximum"></div><span class="hint">Placeholders — use your endorsement’s numbers.</span></div>
      </div>
      <div><label for="s-r">Estimated cost to repair subsidence damage ($)</label><input id="s-r" name="repair" inputmode="decimal" value="96000"><span class="hint">Foundation, framing, drywall, doors, utilities — the full structural scope.</span></div>
      <label class="check"><input type="checkbox" name="has" checked> I have the mine subsidence endorsement</label>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Most the endorsement could pay</small><b data-o="pay">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="c1"></span><span class="c3"></span></div>
      <div class="legend"><span><i class="c1"></i>Within the subsidence limit</span><span><i class="c3"></i>Above the limit or deductible</span></div>
      <div class="out-rows">
        <div><span>Subsidence limit (lesser of Coverage A and cap)</span><b data-o="lim">$0</b></div>
        <div><span>Deductible</span><b data-o="ded">$0</b></div>
        <div><span>Repair cost above the limit</span><b data-o="over">$0</b></div>
        <div><span>Share of repair the endorsement covers</span><b data-o="share">—</b></div>
      </div>
      <p class="out-msg" data-o="note"></p>
    </div>
  </div>
</div>"""

T = BASE
TOOLS = [
    {
        "slug": "claim-gap-fee-estimator", "name": "Claim Gap & Fee Estimator", "kind": "Estimator", "icon": "Δ",
        "short": "Compare two estimates, test cautious, likely and strong outcomes, and subtract appraiser and umpire fees.",
        "title": "Claim Gap & Appraisal Fee Estimator (Free) | WV",
        "desc": "Free WV claim gap estimator: compare your estimate with the insurer’s, test three award outcomes and subtract appraiser and umpire fees.",
        "h1": "Claim Gap & Fee Estimator for West Virginia Property Claims",
        "lede": "Two estimates, one slider and your fee arrangement. The estimator shows a cautious, likely and strong outcome so you can see whether appraisal still pays after costs.",
        "markup": GAP_FULL,
        "explain": f"""
<h2>Reading the three outcomes</h2>
<p>Appraisal panels rarely award either side’s opening number. Line items with photos, measurements and local pricing tend to survive; padded or unsupported items tend to fall away. That is why the estimator never shows one answer. The <strong>likely</strong> case uses your slider. The <strong>cautious</strong> case drops it by 30 points, and the <strong>strong</strong> case raises it by 25.</p>
<p>If appraisal only makes sense in the strong case, the file is fragile. If the cautious case still clears your costs, it is worth a closer look.</p>
<h2>The break-even landing point</h2>
<p>The break-even figure is the share of the gap the panel would have to award just to cover your appraisal costs. A break-even of 15% is comfortable. A break-even above 60% means fees could absorb most of any gain.</p>
<h2>What this tool does not include</h2>
<ul><li>Deductibles, depreciation timing and policy limits. These change what you are paid, not the size of the disagreement. Use the <a href="{T}rcv-acv-holdback-calculator/">RCV / ACV &amp; holdback calculator</a> for that.</li>
<li>Coverage questions. Appraisal values a covered loss; it does not decide whether something is covered.</li>
<li>Legal fees or any bad-faith claim, which are matters for a West Virginia attorney.</li></ul>
<p>All figures are illustrative planning numbers based on what you type in.</p>
""",
        "faqs": [("Why does the umpire fee only count half?", "Most appraisal clauses split the umpire’s cost equally between you and the insurer. Check your policy’s wording, because some forms handle costs differently."),
                 ("Which fee type should I choose?", "Use whatever your appraiser quotes in writing. Flat, hourly and percentage arrangements all exist; the estimator lets you compare them on the same claim."),
                 ("Is the likely award a prediction?", "No. It is a scenario you choose with the slider. Real awards depend on documentation, the policy and the panel.")],
    },
    {
        "slug": "rcv-acv-holdback-calculator", "name": "RCV / ACV & Holdback Calculator", "kind": "Calculator", "icon": "ACV",
        "short": "Work out the first actual cash value check, the depreciation held back and the date to finish repairs.",
        "title": "RCV vs ACV Depreciation & Holdback Calculator",
        "desc": "Calculate actual cash value, recoverable depreciation and your first claim check line by line, plus the date repairs must finish by.",
        "h1": "RCV / ACV Depreciation & Holdback Calculator",
        "lede": "Add each damaged item with its replacement cost, age and expected life. The calculator splits your claim into the first check, the holdback and the total once repairs are done.",
        "markup": DEP,
        "explain": """
<h2>How the math works</h2>
<p>For each line, depreciation is <em>age ÷ expected life × replacement cost</em>, capped at the ceiling you choose. Actual cash value (ACV) is replacement cost minus depreciation. Most replacement-cost policies pay ACV minus the deductible first, then release the depreciation once repairs are finished and documented.</p>
<h2>The repair window</h2>
<p>Policies usually give a set number of days to complete repairs and claim the holdback, and some allow an extension if you ask in writing before it runs out. Enter your policy’s figure and the date of the first check to see the target date. Finishing on time matters more in West Virginia than many owners expect: contractors are stretched thin after a statewide event like a derecho, and materials for slate or standing-seam roofs can take weeks to arrive in rural counties.</p>
<h2>Where depreciation disputes start</h2>
<ul><li>Labor depreciated along with materials, where the policy may not allow it.</li>
<li>Expected lives that are too short for metal roofing, brick or hardwood.</li>
<li>Items depreciated that were nearly new, or a roof aged from the house rather than from its last replacement.</li></ul>
<p>Example figures are illustrative.</p>
""",
        "faqs": [("Can depreciation itself be appraised?", "Often the amount of loss includes both replacement cost and actual cash value, so a panel may set both. Read your policy’s appraisal wording and the award form carefully."),
                 ("What if my policy is ACV-only?", "Tick the ACV-only box. There is no holdback to recover, so the first check is the settlement, less the deductible.")],
    },
    {
        "slug": "roof-square-pitch-estimator", "name": "Roof Square & Pitch Estimator", "kind": "Estimator", "icon": "▲",
        "short": "Turn a footprint and pitch into roof squares, add waste and compare your count with the carrier’s.",
        "title": "Roof Squares & Pitch Estimator | Check the Count",
        "desc": "Estimate roof squares from footprint and pitch, add a waste factor and compare your count with the squares on the insurer’s roof estimate.",
        "h1": "Roof Square & Pitch Estimator",
        "lede": "Steep roofs hold far more material than their footprint suggests. Enter the house size and pitch, then compare your square count with the one on the carrier’s estimate.",
        "markup": ROOF,
        "explain": """
<h2>Why pitch matters so much here</h2>
<p>A square is 100 square feet of roof surface. Because a sloped roof is longer than the floor beneath it, the surface grows with pitch: an 8/12 roof has about 20% more surface than its footprint, and a 12/12 roof about 41% more. Many older homes in Wheeling, Charleston’s East End and the river towns are steep two-story houses, so a footprint-based count can come up several squares short.</p>
<h2>Comparing with the carrier</h2>
<p>Enter the squares on the insurer’s estimate to see the difference. A gap of a square or two can come from rounding or waste choices. A bigger gap usually means a missing slope, a porch roof left out, or a pitch measured wrong — exactly the kind of scope issue appraisal can resolve.</p>
<h2>Steep and high charges</h2>
<p>Estimating software typically adds labor for steep pitches and for roofs two or more stories up. Check that those lines are present when your pitch is 7/12 or steeper. Metal panels and slate have their own waste and labor patterns, so treat this tool as a first check rather than a replacement for a field measurement.</p>
""",
        "faqs": [("Is this accurate enough to dispute an estimate?", "It is good for spotting a large discrepancy. For appraisal, use a field measurement or aerial report with each slope drawn."),
                 ("Why does the waste factor change with roof shape?", "Hips, valleys and dormers require more cutting, so more material is wasted. Simple metal-panel gables waste very little.")],
    },
    {
        "slug": "percentage-deductible-checker", "name": "Percentage Deductible Checker", "kind": "Checker", "icon": "%",
        "short": "See what a percentage deductible costs in dollars, with a 0.5% to 5% ladder and a flat-deductible comparison.",
        "title": "Percentage Deductible Calculator | Wind & Hail",
        "desc": "See your wind, hail or all-peril percentage deductible in dollars, compare it with a flat deductible and view a 0.5% to 5% payout ladder.",
        "h1": "Percentage Deductible Checker",
        "lede": "A 1% deductible sounds small until you multiply it by your dwelling limit. Enter Coverage A and the loss to see what you would actually pay at every common percentage.",
        "markup": DEDUCT,
        "explain": """
<h2>How percentage deductibles work</h2>
<p>Some West Virginia policies apply a percentage deductible to wind and hail, or to every peril, instead of a flat dollar amount. The percentage is usually applied to Coverage A (the dwelling limit), not to the size of the loss. On a $265,000 dwelling limit, a 1% deductible is $2,650 and a 2% deductible is $5,300 — illustrative figures that show how quickly the dollars grow.</p>
<h2>Using the ladder</h2>
<p>The ladder shows what you would pay and what the policy would pay at 0.5%, 1%, 2%, 3% and 5%. It is handy at renewal time, when a lower premium sometimes comes with a higher percentage deductible.</p>
<h2>Deductibles and appraisal</h2>
<p>A larger deductible makes the amount of loss more important, not less: every dollar the carrier’s estimate misses comes straight out of your pocket. If the loss sits just above the deductible, a small scope error can decide whether anything is paid at all.</p>
""",
        "faqs": [("Is the percentage based on the loss or the coverage?", "Usually the coverage limit shown on the declarations page. Read the deductible endorsement to be sure."),
                 ("Does appraisal change my deductible?", "No. Appraisal sets the amount of loss; the deductible is then applied under the policy terms.")],
    },
    {
        "slug": "claim-timeline-ics-planner", "name": "Claim Timeline Planner (.ics)", "kind": "Planner", "icon": "◷",
        "short": "Turn your date of loss into dated milestones and download them as an .ics file for any calendar.",
        "title": "Property Claim Timeline Planner with .ics Export",
        "desc": "Map your property claim milestones from the date of loss — notice, proof of loss, appraiser deadlines, repairs — and export them to a calendar.",
        "h1": "Claim Timeline Planner with Calendar Export",
        "lede": "Enter the date of loss, adjust each window to match your policy, and download every milestone as an .ics file for Google, Apple or Outlook calendars.",
        "markup": DATES,
        "explain": """
<h2>Why a timeline helps</h2>
<p>Claim deadlines are scattered through a policy: notice in one condition, proof of loss in another, appraisal in a third, suit limitation at the end. West Virginia law and court decisions can affect how some of these are applied, so the planner treats every window as something you confirm, not something it decides.</p>
<h2>The appraiser deadline</h2>
<p>Many appraisal clauses give each side a set number of days after a written demand to name an appraiser — often 20. If you plan to demand appraisal, or have received a demand, put that date on the calendar first.</p>
<h2>Exporting</h2>
<p>The download button creates a standard .ics file with one all-day event per milestone. Nothing is uploaded; the file is built in your browser. If a date is approaching and you are unsure about it, talk to a West Virginia attorney.</p>
""",
        "faqs": [("Are the default numbers West Virginia deadlines?", "No. They are placeholders that match common policy wording. Replace them with the figures in your policy and your insurer’s letters."),
                 ("Will the planner remind me automatically?", "Your calendar app will, once you import the .ics file and set alerts on the events.")],
    },
    {
        "slug": "appraisal-readiness-scorecard", "name": "Appraisal Readiness Scorecard", "kind": "Scorecard", "icon": "✓",
        "short": "Twelve yes-or-no questions that score your file and build a to-do list before you demand appraisal.",
        "title": "Appraisal Readiness Scorecard | 12-Question Check",
        "desc": "Score your claim file in two minutes: twelve yes-or-no questions on coverage, estimates, photos and deadlines, with a to-do list for gaps.",
        "h1": "Appraisal Readiness Scorecard",
        "lede": "Appraisal rewards preparation. Answer twelve quick questions and get a weighted score plus a to-do list of what to fix before anyone signs a demand.",
        "markup": READY,
        "explain": """
<h2>How the score is weighted</h2>
<p>Questions about coverage and itemized estimates carry the most weight because a panel cannot work without them. Photos, policy reading and hidden-damage checks come next. Organizational items count, but less.</p>
<h2>What a low score means</h2>
<p>A low score does not mean your claim is weak. It means the file is not ready yet. Appraisal awards are binding on the amount of loss, so demanding appraisal before the scope is complete can lock in a number that leaves damage out.</p>
<h2>After you score well</h2>
<p>A strong score is the right moment for an <a href="/wv-appraisal-services/claim-estimate-review/">estimate review</a>: a line-by-line look at where the two estimates differ and what the difference is likely worth.</p>
""",
        "faqs": [("Is my score saved anywhere?", "No. It exists only on this page and disappears when you leave or reset."),
                 ("Can I demand appraisal with a low score?", "You can, but you risk a binding award built on an incomplete scope. Close the gaps first where you can.")],
    },
    {
        "slug": "mine-subsidence-limit-calculator", "name": "Mine Subsidence Limit Calculator", "kind": "Calculator", "icon": "⛏",
        "short": "Compare a subsidence repair estimate with the endorsement cap and deductible to see what is left uncovered.",
        "title": "Mine Subsidence Coverage Limit Calculator | WV",
        "desc": "Compare a mine subsidence repair estimate with your endorsement cap and deductible to see what the coverage could pay and what remains.",
        "h1": "Mine Subsidence Limit Calculator",
        "lede": "West Virginia’s mine subsidence coverage has its own limit and deductible. Enter your figures to see how much of a structural repair the endorsement could reach.",
        "markup": MINE,
        "explain": """
<h2>Why this tool exists</h2>
<p>Large parts of West Virginia sit over old underground coal workings. The state runs a mine subsidence insurance program with the Board of Risk and Insurance Management, and insurers that write dwelling coverage must offer a mine subsidence endorsement. That endorsement is capped — commonly described as up to $75,000 for a dwelling — and carries its own deductible. Foundation and framing repairs can exceed that cap quickly.</p>
<h2>How the calculation works</h2>
<ul><li>The subsidence limit is the lesser of your Coverage A and the cap you enter.</li>
<li>The deductible is a percentage of that limit, kept between the floor and ceiling you enter.</li>
<li>The most the endorsement could pay is the smaller of (repair cost − deductible) and the limit.</li></ul>
<p>Default numbers are placeholders. Your endorsement controls; enter its figures.</p>
<h2>Subsidence versus landslide</h2>
<p>Ground movement from a slip or landslide is usually excluded by the earth-movement exclusion and is not the same as mine subsidence. Whether a loss is subsidence is a coverage question for the insurer and, if disputed, an attorney. Appraisal can value a covered subsidence loss; it cannot make an excluded loss covered. Our guide to <a href="/claim-library/landslide-vs-mine-subsidence-claims/">landslide versus mine subsidence claims</a> explains the difference.</p>
""",
        "faqs": [("Do I automatically have mine subsidence coverage?", "Not necessarily. It is generally offered as an endorsement and may be accepted or rejected depending on the county and your choices. Check your declarations page."),
                 ("Can an appraiser help if the repair exceeds the cap?", "An appraiser can establish the full amount of loss, which matters when other coverages may apply, but cannot raise the endorsement’s limit.")],
    },
]
