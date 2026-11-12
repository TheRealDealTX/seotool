"""Seven free claim tools for South Carolina property owners: markup + explanatory copy.
All logic runs in the browser (static/assets/js/app.js). Nothing is stored or sent."""

C_NAVY, C_CU, C_PALE, C_SKY = "var(--navy)", "var(--copper)", "#c9d4e3", "var(--sky)"


def _sw(c):
    return f'<span style="background:{c}"></span>'


def _lg(c, t):
    return f'<span><i style="background:{c}"></i>{t}</span>'


GAP_FULL = f"""
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Claim gap &amp; fee estimator</span><i>Runs in your browser</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Carrier’s estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="23600"><span class="hint">Replacement cost total before depreciation.</span></div>
        <div><label for="g-own">Your estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="38900"><span class="hint">Contractor or independent estimate.</span></div>
      </div>
      <div><label for="g-land">Where might an award land inside the gap?</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% means the carrier’s number holds; 100% means yours does. Test several points.</span></div>
      <div class="row2">
        <div><label for="g-ft">Appraiser fee basis</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of the increase (%)</option></select></div>
        <div><label for="g-fee">Fee amount</label><input id="g-fee" name="fee" inputmode="decimal" value="2800"></div>
      </div>
      <label class="check"><input type="checkbox" name="useump" checked> Add my half of an umpire’s fee</label>
      <div><label for="g-ump">Umpire’s total fee</label><input id="g-ump" name="umpire" inputmode="decimal" value="3200"><span class="hint">Usually split evenly between the two sides.</span></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated net gain after fees</small><b data-o="net">$0</b></div>
      <div class="stack" aria-hidden="true">{_sw(C_PALE)}{_sw(C_NAVY)}{_sw(C_CU)}</div>
      <div class="legend">{_lg(C_PALE, "Carrier’s figure")}{_lg(C_NAVY, "Your net gain")}{_lg(C_CU, "Appraisal costs")}</div>
      <div class="out-rows">
        <div><span>Amount in dispute</span><b data-o="gap">$0</b></div>
        <div><span>Gap as a share of the carrier’s figure</span><b data-o="pct">—</b></div>
        <div><span>Projected award (RCV)</span><b data-o="award">$0</b></div>
        <div><span>Gross increase</span><b data-o="gain">$0</b></div>
        <div><span>Your appraisal costs</span><b data-o="cost">$0</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

GAP_MINI = f"""
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Quick gap check</span><i>Illustrative figures</i></div>
  <div class="tool-body" style="grid-template-columns:minmax(0,1fr)">
    <div class="tool-in">
      <div class="row2">
        <div><label for="m-ins">Carrier’s estimate</label><input id="m-ins" name="insurer" inputmode="decimal" value="23600"></div>
        <div><label for="m-own">Your estimate</label><input id="m-own" name="yours" inputmode="decimal" value="38900"></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite" style="border-left:0;border-top:1px solid var(--line)">
      <div class="out-rows">
        <div><span>Amount in dispute</span><b data-o="gap">$0</b></div>
        <div><span>Gap vs. the carrier’s figure</span><b data-o="pct">—</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

_DEP_ROW = '<tr><td><input name="item" aria-label="Item" placeholder="Item"></td><td><input name="rcv" aria-label="Replacement cost" inputmode="decimal" value="{r}"></td><td><input name="age" aria-label="Age in years" inputmode="decimal" value="{a}"></td><td><input name="life" aria-label="Expected life in years" inputmode="decimal" value="{l}"></td><td data-o="row">$0</td><td><button type="button" class="x" aria-label="Remove row">×</button></td></tr>'

DEP = f"""
<div class="tool" data-tool="dep">
  <div class="tool-head"><span>RCV vs. ACV holdback calculator</span><i>Straight-line depreciation</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap" style="margin:0;border:0"><table class="dep-table"><thead><tr><th>Item</th><th>RCV ($)</th><th>Age</th><th>Life</th><th>ACV</th><th><span class="hint" style="margin:0">Del</span></th></tr></thead><tbody>
        {_DEP_ROW.format(r=16800, a=11, l=25).replace('placeholder="Item"', 'placeholder="Item" value="Roof covering"')}
        {_DEP_ROW.format(r=4200, a=6, l=10).replace('placeholder="Item"', 'placeholder="Item" value="Interior paint"')}
        {_DEP_ROW.format(r=6900, a=9, l=12).replace('placeholder="Item"', 'placeholder="Item" value="Carpet &amp; pad"')}
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn line sm" data-add>Add a line</button></div>
      <div class="row2">
        <div><label for="d-ded">Deductible</label><input id="d-ded" name="deduct" inputmode="decimal" value="2500"></div>
        <div><label for="d-cap">Maximum depreciation</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="100">100%</option></select></div>
      </div>
      <label class="check"><input type="checkbox" name="nonrec"> My policy pays actual cash value only (depreciation not recoverable)</label>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>First check (ACV less deductible)</small><b data-o="first">$0</b></div>
      <div class="out-rows">
        <div><span>Replacement cost value</span><b data-o="rcv">$0</b></div>
        <div><span>Depreciation taken</span><b data-o="dep">$0</b></div>
        <div><span>Depreciation as % of RCV</span><b data-o="deppct">0%</b></div>
        <div><span>Actual cash value</span><b data-o="acv">$0</b></div>
        <div><span>Holdback released after repairs</span><b data-o="held">$0</b></div>
        <div><span>Total once repairs are done</span><b data-o="total">$0</b></div>
      </div>
      <p class="out-msg">Holdback is usually released when you show the work is finished within the policy’s time limit. Keep invoices and completion photos.</p>
    </div>
  </div>
</div>"""

ROOF = """
<div class="tool" data-tool="roof">
  <div class="tool-head"><span>Roof area &amp; pitch estimator</span><i>Squares, waste &amp; steep check</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="seg" role="radiogroup" aria-label="Measurement method"><label><input type="radio" name="mode" value="dims" checked> Length × width</label><label><input type="radio" name="mode" value="area"> Footprint area</label></div>
      <div class="row2" data-mode="dims">
        <div><label for="r-l">Building length (ft)</label><input id="r-l" name="len" inputmode="decimal" value="58"></div>
        <div><label for="r-w">Building width (ft)</label><input id="r-w" name="wid" inputmode="decimal" value="34"></div>
      </div>
      <div data-mode="dims"><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="16"></div>
      <div data-mode="area" hidden><label for="r-a">Footprint incl. overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="2250"></div>
      <div class="row2">
        <div><label for="r-p">Pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 7 else "", p) for p in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16]) + """</select></div>
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="10">10% · plain gable</option><option value="13" selected>13% · gable + dormers</option><option value="15">15% · hip roof</option><option value="19">19% · cut-up roof</option></select></div>
      </div>
      <div><label for="r-pr">Installed price per square (optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 560"><span class="hint">Use a current local quote for a rough replacement figure.</span></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Roof squares before waste</small><b data-o="sq">0</b></div>
      <div class="out-rows">
        <div><span>Pitch factor</span><b data-o="mult">1.000</b></div>
        <div><span>Sloped surface area</span><b data-o="surface">0</b></div>
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
  <div class="tool-head"><span>Hurricane deductible calculator</span><i>Percentage vs. flat</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling limit (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="410000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Hurricane / named-storm deductible</label><select id="w-p" name="pct"><option value="1">1%</option><option value="2" selected>2%</option><option value="3">3%</option><option value="5">5%</option><option value="10">10%</option></select></div>
        <div><label for="w-f">All-other-perils deductible</label><input id="w-f" name="flat" inputmode="decimal" value="1500"></div>
      </div>
      <div><label for="w-l">Estimated wind damage</label><input id="w-l" name="loss" inputmode="decimal" value="26400"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your hurricane deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true">{_sw(C_CU)}{_sw(C_NAVY)}</div>
      <div class="legend">{_lg(C_CU, "Your share")}{_lg(C_NAVY, "Policy pays")}</div>
      <div class="out-rows">
        <div><span>Paid with the hurricane deductible</span><b data-o="pdpay">$0</b></div>
        <div><span>Paid if the flat deductible applied</span><b data-o="flatpay">$0</b></div>
        <div><span>Extra out of pocket</span><b data-o="diff">$0</b></div>
      </div>
      <p class="out-msg" data-o="below"></p>
    </div>
  </div>
</div>"""

DATES = """
<div class="tool" data-tool="dates">
  <div class="tool-head"><span>Claim timeline builder</span><i>Exports an .ics calendar file</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
      <p class="hint" style="margin:0">Replace each default with the number of days in your own policy. Defaults are common reference points, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report the claim (days)</label><input id="t-n" name="notice" inputmode="numeric" value="2"></div>
        <div><label for="t-m">Temporary repairs (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="10"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Often counted from the carrier’s request.</span></div>
        <div><label for="t-r">Finish repairs for holdback (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="180"></div>
        <div><label for="t-s">Suit deadline reference (days)</label><input id="t-s" name="suit" inputmode="numeric" value="1095"><span class="hint">Three years = 1,095 days. Confirm yours with a South Carolina attorney.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"><li><b>Pick your date of loss</b><span>Milestones will appear here.</span></li></ol>
      <div class="btn-row"><button type="button" class="btn sm" data-ics>Download calendar (.ics)</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the carrier accepted coverage for at least part of the loss in writing?", "Get written confirmation of what is covered. If the claim was denied outright, speak with a South Carolina attorney before thinking about appraisal."),
    (3, "Do you have the carrier’s full line-item estimate, not just a payment letter?", "Ask the adjuster for the complete itemized estimate, including the measurements or diagram it relies on."),
    (3, "Do you have your own itemized estimate?", "Get a line-item estimate from a contractor or estimator. A one-line bid is hard to defend in front of a panel."),
    (2, "Do you know which policy pays which part (homeowners, wind pool, flood)?", "List every policy that could respond — homeowners, an SCWHUA wind policy, flood — and which damage each one is being asked to pay."),
    (2, "Do you have dated photos taken soon after the storm?", "Pull every photo and video you have, note the dates and add current photos of the same areas."),
    (2, "Have you found and read the appraisal clause in your policy?", "Find the ‘Appraisal’ condition and note any time limits for naming an appraiser."),
    (2, "Have you put the policy’s deadlines on a calendar?", "Use the claim timeline builder to calendar proof-of-loss, holdback and suit dates."),
    (2, "Were temporary repairs made, with receipts kept?", "Tarp, dry out and secure the property, and keep every receipt and invoice."),
    (2, "Has hidden damage (attic, decking, wall cavities) been opened up and documented?", "Make sure concealed damage is inspected so the scope is complete before values are argued."),
    (1, "Do you have the current declarations page?", "Download or request your declarations page, including deductibles and endorsements."),
    (2, "Is the gap between estimates more than roughly 10% or several thousand dollars?", "Run both numbers through the claim gap & fee estimator — a small gap may not justify the cost of appraisal."),
    (1, "Is your correspondence with the carrier saved in date order?", "Collect letters, emails and claim notes in one folder, oldest first."),
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
      <div class="btn-row"><button type="button" class="btn line sm" data-reset>Clear answers</button></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div>
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#dbe3ee" stroke-width="16"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#c2773a" stroke-width="16" stroke-dasharray="251.3" stroke-dashoffset="251.3" style="transition:stroke-dashoffset .5s,stroke .3s"/></svg>
        <div class="gauge-num"><span data-o="score">–</span></div>
        <p class="hint" style="text-align:center">Answered <span data-o="count">0 / 12</span></p>
      </div>
      <p class="out-msg" data-o="verdict"></p>
      <div><p class="todo-h">Before you demand appraisal</p><ul data-o="todo" style="margin:0;padding-left:1.1em"></ul></div>
    </div>
  </div>
</div>"""

SPLIT = """
<div class="tool" data-tool="split">
  <div class="tool-head"><span>Wind vs. flood damage splitter</span><i>Hurricane losses with two policies</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="s-t">Total repair estimate for the storm</label><input id="s-t" name="total" inputmode="decimal" value="96000"></div>
      <div><label for="s-w">Share caused by wind (roof, windows, wind-driven rain)</label>
        <div class="range"><input id="s-w" type="range" name="wind" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">The rest is treated as rising water or surge — the part a flood policy is asked to pay.</span></div>
      <div class="row2">
        <div><label for="s-a">Wind policy dwelling limit</label><input id="s-a" name="cova" inputmode="decimal" value="420000"><span class="hint">Homeowners or SCWHUA wind policy.</span></div>
        <div><label for="s-p">Hurricane deductible</label><select id="s-p" name="pct"><option value="1">1%</option><option value="2" selected>2%</option><option value="3">3%</option><option value="5">5%</option></select></div>
      </div>
      <div class="row2">
        <div><label for="s-f">Flood building limit</label><input id="s-f" name="flim" inputmode="decimal" value="250000"><span class="hint">NFIP building coverage tops out at $250,000.</span></div>
        <div><label for="s-fd">Flood deductible</label><input id="s-fd" name="fded" inputmode="decimal" value="5000"></div>
      </div>
      <label class="check"><input type="checkbox" name="noflood"> I don’t carry flood insurance</label>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Left for you to cover</small><b data-o="gapown">$0</b></div>
      <div class="split-bars">
        <div><span>Wind policy</span><span class="bar"><i data-bar="wind" style="background:var(--navy)"></i></span><b data-o="windpay">$0</b></div>
        <div><span>Flood policy</span><span class="bar"><i data-bar="flood" style="background:var(--sky)"></i></span><b data-o="floodpay">$0</b></div>
        <div><span>Out of pocket</span><span class="bar"><i data-bar="own" style="background:var(--copper)"></i></span><b data-o="own">$0</b></div>
      </div>
      <div class="out-rows">
        <div><span>Wind portion of the damage</span><b data-o="windpart">$0</b></div>
        <div><span>Hurricane deductible in dollars</span><b data-o="hded">$0</b></div>
        <div><span>Water portion of the damage</span><b data-o="floodpart">$0</b></div>
      </div>
      <p class="out-msg" data-o="smsg"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "claim-gap-fee-estimator", "name": "Claim Gap & Fee Estimator", "kind": "Calculator",
        "kw": "insurance appraisal cost calculator",
        "short": "Measure the dispute, test where an award might land and net out appraiser and umpire fees.",
        "title": "Insurance Appraisal Cost Calculator: Gap, Fees & Net",
        "desc": "Free insurance appraisal cost calculator for South Carolina claims: size the gap, project an award and subtract appraiser and umpire fees.",
        "h1": "Insurance Appraisal Cost Calculator: Is the Gap Worth It?",
        "lede": "This insurance appraisal cost calculator compares the carrier’s estimate with yours, lets you test where an award could land, and subtracts realistic fees so you see the net, not just the gap.",
        "markup": GAP_FULL,
        "explain": """
<h2>Reading the result</h2>
<p>The calculator multiplies the gap between the two replacement-cost estimates by the slider percentage to project an award, then subtracts your appraiser’s fee and, if you tick the box, half of an umpire’s fee. All figures are illustrative and depend entirely on what you enter.</p>
<h2>Test a range, not a single point</h2>
<p>Panels seldom adopt either side’s number outright. Try the slider at 30%, 50% and 75%. If appraisal only makes sense near 100%, your position depends on every line item surviving, which is a fragile place to start. If the net still looks sensible at 40%, the dispute is more likely to justify the cost.</p>
<h2>What it doesn’t include</h2>
<ul><li>Deductibles, policy limits and sub-limits, which change what you are paid but not the size of the dispute.</li>
<li>Timing of recoverable depreciation — use the <a href="/free-claim-tools/rcv-acv-holdback-calculator/">RCV vs. ACV holdback calculator</a> for that.</li>
<li>Your time, and any attorney’s or contractor’s fees.</li></ul>
""",
        "faqs": [("Is the projected award a prediction?", "No. It is a planning scenario based on the percentage you choose. Real awards depend on documentation, the panel and the policy."), ("How are appraisal fees usually structured?", "Some appraisers charge a flat or hourly fee and others a percentage of the increase. Whatever the arrangement, get it in writing before work starts.")],
    },
    {
        "slug": "rcv-acv-holdback-calculator", "name": "RCV vs. ACV Holdback Calculator", "kind": "Calculator",
        "kw": "RCV vs ACV calculator",
        "short": "List damaged items by age and life to estimate your first check, the holdback and the final total.",
        "title": "RCV vs ACV Calculator: Depreciation Holdback Estimate",
        "desc": "RCV vs ACV calculator: enter each item’s cost, age and life to estimate depreciation, your first check and the holdback paid after repairs.",
        "h1": "RCV vs. ACV Calculator for Depreciation and Holdback",
        "lede": "Use this RCV vs. ACV calculator to see how a replacement-cost policy splits a payment into an actual-cash-value check now and recoverable depreciation once the work is done.",
        "markup": DEP,
        "explain": """
<h2>How the calculator depreciates items</h2>
<p>Each line is depreciated in a straight line: age divided by expected life, capped at the maximum you choose. Carrier estimates may also adjust for condition or leave some items undepreciated, so treat the output as a planning figure.</p>
<h2>Life expectancies you’ll often see</h2>
<div class="table-wrap"><table><thead><tr><th>Item</th><th>Common range used in estimates</th></tr></thead><tbody>
<tr><th>Architectural shingles</th><td>25–30 years</td></tr><tr><th>3-tab shingles</th><td>20–25 years</td></tr><tr><th>Metal roofing</th><td>40–50 years</td></tr><tr><th>Interior paint</th><td>8–12 years</td></tr><tr><th>Carpet</th><td>8–12 years</td></tr><tr><th>Exterior wood siding</th><td>25–40 years</td></tr></tbody></table></div>
<h2>Getting the holdback paid</h2>
<p>Most replacement-cost policies release recoverable depreciation when you show the repair or replacement is complete within a stated period. Calendar that period with the <a href="/free-claim-tools/claim-timeline-builder/">claim timeline builder</a> and keep invoices and completion photos.</p>
""",
        "faqs": [("Can labor be depreciated?", "Treatment of labor depreciation varies by policy wording and jurisdiction. Ask the carrier to explain its approach in writing and raise it with a South Carolina attorney if it matters to your claim."), ("What happens if I don’t repair?", "Under most replacement-cost policies you keep the actual cash value payment, but the held-back depreciation may not be paid.")],
    },
    {
        "slug": "roof-area-pitch-estimator", "name": "Roof Area & Pitch Estimator", "kind": "Calculator",
        "kw": "roof squares calculator",
        "short": "Turn a footprint and pitch into sloped area, squares, bundles and a steep-charge check.",
        "title": "Roof Squares Calculator With Pitch & Waste for Claims",
        "desc": "Free roof squares calculator: turn footprint and pitch into sloped area, squares with waste and bundles, then check steep charges on your estimate.",
        "h1": "Roof Squares Calculator With Pitch and Waste",
        "lede": "Short measurements quietly shrink roof claims. This roof squares calculator converts a footprint and pitch into sloped area, squares with waste and shingle bundles.",
        "markup": ROOF,
        "explain": """
<h2>The pitch factor</h2>
<p>A sloped roof has more surface than the ground it covers. The factor is √(1 + (rise ÷ 12)²): roughly 1.118 at 6/12, 1.158 at 7/12 and 1.414 at 12/12. Multiply the footprint (including overhangs) by that factor and divide by 100 to get squares.</p>
<h2>Comparing against the carrier’s estimate</h2>
<ul><li>Find the roof section and note total squares and the waste percentage used.</li>
<li>A difference of more than about 5–10% from your own figure deserves a closer look at the measurements.</li>
<li>Check for steep charges at steeper pitches and high-roof charges on two-story sections.</li>
<li>Look for starter, ridge cap, drip edge, valley metal and underlayment as their own lines.</li></ul>
<h2>When a footprint isn’t enough</h2>
<p>Roofs with several pitches, dormers or turrets — common on Lowcountry and Upstate custom homes — need to be measured plane by plane, from an aerial report or by hand. Use this as a sanity check, not as the measurement of record.</p>
""",
        "faqs": [("What is a roofing square?", "One hundred square feet of roof surface. Many single-family homes fall somewhere between 20 and 45 squares."), ("Why does waste vary?", "Hips, valleys and dormers mean more cutting, so more material ends up as scrap.")],
    },
    {
        "slug": "hurricane-deductible-calculator", "name": "Hurricane Deductible Calculator", "kind": "Calculator",
        "kw": "hurricane deductible calculator",
        "short": "Convert a percentage hurricane or named-storm deductible into dollars and see what a claim pays.",
        "title": "Hurricane Deductible Calculator for South Carolina Homes",
        "desc": "Hurricane deductible calculator: turn a 1–10% named-storm deductible into dollars and compare what a South Carolina wind claim would actually pay.",
        "h1": "Hurricane Deductible Calculator: Your Percentage in Dollars",
        "lede": "A 2% deductible sounds small until it’s multiplied by your dwelling limit. This hurricane deductible calculator shows the dollar figure and what a storm claim would pay.",
        "markup": DEDUCT,
        "explain": """
<h2>Why the number surprises people</h2>
<p>Many South Carolina policies — and nearly all coastal ones — carry a separate hurricane or named-storm deductible set as a percentage of Coverage A. On an illustrative $410,000 dwelling limit, 2% is $8,200, not the $1,500 that applies to a kitchen fire.</p>
<h2>When the percentage applies</h2>
<p>The trigger is defined in the policy, not by the weather. Some forms apply it from the time a hurricane watch or warning is issued for any part of the state until a set period after it ends; others tie it to a named storm. The declarations page and the hurricane deductible endorsement control. Inland owners were surprised to find this after Helene in 2024.</p>
<h2>How it fits with appraisal</h2>
<p>Appraisal decides the amount of loss; the deductible then comes off that amount. A loss only slightly above the deductible may not be worth a formal dispute, while one well above it often is. Run both numbers through the <a href="/free-claim-tools/claim-gap-fee-estimator/">claim gap &amp; fee estimator</a>.</p>
""",
        "faqs": [("Does the percentage apply to contents too?", "It is usually calculated from the dwelling limit but applied to the whole hurricane loss. Check your policy’s wording."), ("Can I lower my hurricane deductible?", "Sometimes at renewal, usually for a higher premium. Mitigation such as an SC Safe Home upgrade may also affect pricing; ask your agent.")],
    },
    {
        "slug": "claim-timeline-builder", "name": "Claim Timeline Builder", "kind": "Planner",
        "kw": "insurance claim deadline calculator",
        "short": "Map notice, proof of loss, holdback and suit dates from your date of loss, then export to a calendar.",
        "title": "Insurance Claim Deadline Calculator With Calendar Export",
        "desc": "Insurance claim deadline calculator for South Carolina: map proof-of-loss, holdback and suit reference dates and export them to your calendar.",
        "h1": "Insurance Claim Deadline Calculator and Timeline Builder",
        "lede": "Deadlines keep running while you argue about the number. This insurance claim deadline calculator turns your date of loss and policy windows into a dated timeline you can download.",
        "markup": DATES,
        "explain": """
<h2>The dates worth protecting</h2>
<ul><li><strong>Notice.</strong> Policies require prompt notice of a loss; late notice is a common carrier defense.</li>
<li><strong>Proof of loss.</strong> If the carrier asks for a sworn proof of loss, many forms allow 60 days to return it. Flood policies have their own strict rules.</li>
<li><strong>Holdback.</strong> Replacement-cost policies often require repairs within a set period to collect recoverable depreciation.</li>
<li><strong>Suit.</strong> South Carolina contract claims generally carry a three-year limitation period, but policy terms and other rules can matter, and appraisal does not automatically stop the clock.</li></ul>
<div class="note"><b class="h">Important</b>The timeline uses only the numbers you enter. It isn’t legal advice. If a deadline is close, contact a South Carolina attorney.</div>
""",
        "faqs": [("What counts as the date of loss?", "Usually the date the storm or event happened, not the day you noticed damage. Weather records for your address can help pin it down."), ("Does the .ics file send my data anywhere?", "No. The file is created in your browser and saved straight to your device.")],
    },
    {
        "slug": "appraisal-readiness-checkup", "name": "Appraisal Readiness Checkup", "kind": "Checklist",
        "kw": "appraisal readiness checklist",
        "short": "Twelve yes/no questions that score your claim file and build a to-do list before you demand appraisal.",
        "title": "Appraisal Readiness Checklist: Score Your Claim File",
        "desc": "Appraisal readiness checklist: answer twelve questions to score your South Carolina claim file and get a to-do list before you demand appraisal.",
        "h1": "Appraisal Readiness Checklist: Is Your File Ready?",
        "lede": "Appraisals are won on paperwork. Work through this appraisal readiness checklist to see how complete your file is and what to finish before you send a demand.",
        "markup": READY,
        "explain": """
<h2>How answers are weighted</h2>
<p>Coverage, the two estimates and early photos carry the most weight because they decide whether appraisal is the right tool and how well your number will stand up. Administrative items matter, but they are quicker to fix.</p>
<h2>What your score suggests</h2>
<ul><li><strong>75 or higher:</strong> the file is in good shape; a professional look at the dollar gap is the next step.</li>
<li><strong>45 to 74:</strong> close the open items first — each one strengthens your position.</li>
<li><strong>Below 45:</strong> demanding appraisal now risks locking in a low number.</li></ul>
""",
        "faqs": [("Are my answers saved?", "No. The checklist runs entirely in your browser and nothing is stored or sent."), ("Why does it ask about wind pool and flood policies?", "Coastal South Carolina losses often involve two or three policies, and appraisal under one does not bind the others.")],
    },
    {
        "slug": "wind-flood-damage-splitter", "name": "Wind vs. Flood Damage Splitter", "kind": "Calculator",
        "kw": "wind vs flood damage calculator",
        "short": "Split a hurricane loss between a wind policy and a flood policy to see who pays what — and what’s left.",
        "title": "Wind vs Flood Damage Calculator for Hurricane Claims",
        "desc": "Wind vs flood damage calculator: split a South Carolina hurricane loss between wind and flood policies, apply both deductibles and see the shortfall.",
        "h1": "Wind vs. Flood Damage Calculator for Hurricane Losses",
        "lede": "After surge and wind hit the same house, two policies each pay only their part. This wind vs. flood damage calculator shows how the split and the deductibles shape what you collect.",
        "markup": SPLIT,
        "explain": """
<h2>Why the split matters on the coast</h2>
<p>Homeowners and SCWHUA wind policies exclude flood; flood policies exclude wind. When Hugo, Matthew or Ian drove water into homes that also lost shingles and windows, each carrier valued only its own share, and every point of the split moved real money. This calculator lets you see how sensitive your recovery is to that allocation, using illustrative numbers you control.</p>
<h2>How the math works</h2>
<ol><li>The wind share of the total is reduced by your hurricane deductible (a percentage of the dwelling limit).</li>
<li>The water share is reduced by the flood deductible and capped at the flood building limit.</li>
<li>Whatever neither policy pays is your shortfall.</li></ol>
<h2>Where appraisal fits</h2>
<p>Appraisal under the wind policy can settle the <em>amount</em> of wind damage, but whether a given item was caused by wind or water can be treated as a causation or coverage question. Flood policies have their own claim and appraisal rules. Good documentation — water lines, interior photos, debris lines, roof and window damage — is what supports a fair split. See our guide to <a href="/appraisal-guides/wind-pool-claims-and-appraisal/">wind pool claims and appraisal</a>.</p>
""",
        "faqs": [("Is the wind percentage something I decide?", "No. The split is determined from evidence by the adjusters, appraisers or, if disputed, others. The slider just shows how sensitive your recovery is to it."), ("Does this include contents?", "No. It models building damage only. Contents have separate limits and deductible rules on both policies.")],
    },
]
