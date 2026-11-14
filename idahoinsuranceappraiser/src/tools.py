"""Interactive claim tools: markup + explanatory copy. Logic lives in static/assets/js/app.js.

Every tool runs in the browser. Nothing is sent or stored.
"""

TOOL_BASE = "/policy-math-tools/"

# Palette used inside tool charts (keep in sync with style.css tokens)
NAVY, YEL, ORG, MIST = "#003776", "#FFE835", "#d9622b", "#c9d6e6"

GAP_FULL = f"""
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Claim gap &amp; net recovery estimator</span><i>Runs in your browser</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Insurer’s estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="21600"><span class="hint">Replacement cost total on the carrier’s estimate.</span></div>
        <div><label for="g-own">Your estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="36400"><span class="hint">Your contractor’s or independent estimate.</span></div>
      </div>
      <div><label for="g-land">Where might the award land within the gap?</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% means the carrier’s number holds; 100% means your full number is awarded.</span></div>
      <div class="row2">
        <div><label for="g-ft">Your appraiser’s fee type</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of increase (%)</option><option value="hourly">Hourly (hours × rate)</option></select></div>
        <div><label for="g-fee">Fee amount (or hourly rate)</label><input id="g-fee" name="fee" inputmode="decimal" value="2800"></div>
      </div>
      <div data-hourly hidden><label for="g-hrs">Estimated hours</label><input id="g-hrs" name="hours" inputmode="decimal" value="20"></div>
      <label class="check"><input type="checkbox" name="useump" checked> Include my half of an umpire’s fee</label>
      <div><label for="g-ump">Umpire’s total fee (split 50/50)</label><input id="g-ump" name="umpire" inputmode="decimal" value="3200"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated net increase to you</small><b data-o="net">$0</b></div>
      <div class="stack" aria-hidden="true"><span style="background:{MIST}"></span><span style="background:{YEL}"></span><span style="background:{ORG}"></span></div>
      <div class="legend"><span><i style="background:{MIST}"></i>Carrier’s number</span><span><i style="background:{YEL}"></i>Your net gain</span><span><i style="background:{ORG}"></i>Appraisal costs</span></div>
      <div class="out-rows">
        <div><span>Amount in dispute</span><b data-o="gap">$0</b></div>
        <div><span>Gap as % of carrier estimate</span><b data-o="pct">—</b></div>
        <div><span>Projected award (RCV)</span><b data-o="award">$0</b></div>
        <div><span>Gross increase</span><b data-o="gain">$0</b></div>
        <div><span>Your appraisal costs</span><b data-o="cost">$0</b></div>
        <div><span>Break-even landing point</span><b data-o="breakeven">—</b></div>
      </div>
      <p class="todo-h">Net at three landing points</p>
      <div class="scen" data-o="scen"></div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

GAP_MINI = f"""
<div class="tool tool-mini" data-tool="gap">
  <div class="tool-head"><span>Quick gap check</span><i>No sign-up, nothing stored</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="m-ins">Insurer’s estimate</label><input id="m-ins" name="insurer" inputmode="decimal" value="16800"></div>
      <div><label for="m-own">Your contractor’s estimate</label><input id="m-own" name="yours" inputmode="decimal" value="29500"></div>
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
  <div class="tool-head"><span>RCV vs. ACV holdback calculator</span><i>Add as many items as you need</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Laminated shingle roof", 21400, 11, 30), ("Vinyl siding — north and west walls", 6800, 14, 40), ("Interior paint — great room", 2100, 5, 10)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn ghost small" data-add data-run>+ Add item</button></div>
      <div class="row2">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="2500"></div>
        <div><label for="d-cap">Maximum depreciation</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="90">90%</option></select><span class="hint">Most estimates cap depreciation; check yours.</span></div>
      </div>
      <label class="check"><input type="checkbox" name="nonrec"> My policy pays actual cash value only (no recoverable depreciation)</label>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>First check (ACV − deductible)</small><b data-o="first">$0</b></div>
      <div class="out-big"><small>Held back until repairs</small><b data-o="held">$0</b></div>
      <div class="out-big"><small>Total if fully recovered</small><b data-o="total">$0</b></div>
      <div class="out-rows wide">
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
  <div class="tool-head"><span>Roof pitch &amp; squares calculator</span><i>Compare against your estimate</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <fieldset class="plain"><legend class="sr-only">Measurement method</legend>
        <div class="btn-row">
          <label class="check"><input type="radio" name="mode" value="dims" checked> Footprint length × width</label>
          <label class="check"><input type="radio" name="mode" value="area"> I know the footprint area</label>
        </div></fieldset>
      <div class="row2" data-mode="dims">
        <div><label for="r-l">Footprint length (ft)</label><input id="r-l" name="len" inputmode="decimal" value="62"></div>
        <div><label for="r-w">Footprint width (ft)</label><input id="r-w" name="wid" inputmode="decimal" value="36"></div>
      </div>
      <div data-mode="dims"><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="18"></div>
      <div data-mode="area" hidden><label for="r-a">Footprint area incl. overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="2400"></div>
      <div class="row2">
        <div><label for="r-p">Roof pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 5 else "", p) for p in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16]) + """</select></div>
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="10">10% — simple gable</option><option value="12" selected>12% — gable with dormers</option><option value="15">15% — hip roof</option><option value="18">18% — complex / cut-up</option></select></div>
      </div>
      <div class="row2">
        <div><label for="r-pr">Installed price per square (optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 560"></div>
        <div><label for="r-cs">Squares on the carrier’s estimate (optional)</label><input id="r-cs" name="carrier" inputmode="decimal" placeholder="e.g. 26.5"></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Roof squares (before waste)</small><b data-o="sq">0</b></div>
      <div class="out-rows">
        <div><span>Pitch multiplier</span><b data-o="mult">1.000</b></div>
        <div><span>Pitch angle</span><b data-o="deg">0°</b></div>
        <div><span>Roof surface area</span><b data-o="surface">0</b></div>
        <div><span>Squares to order (with waste)</span><b data-o="order">0</b></div>
        <div><span>Shingle bundles (3 per square)</span><b data-o="bundles">0</b></div>
        <div><span>Rough replacement cost</span><b data-o="cost">—</b></div>
        <div><span>Difference vs. carrier squares</span><b data-o="vs">—</b></div>
      </div>
      <p class="out-msg" data-o="steep"></p>
    </div>
  </div>
</div>"""

DEDUCT = """
<div class="tool" data-tool="deduct">
  <div class="tool-head"><span>Percentage deductible calculator</span><i>Percent vs. flat, in dollars</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling coverage (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="465000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Wind/hail percentage deductible</label><select id="w-p" name="pct"><option value="0.5">0.5%</option><option value="1" selected>1%</option><option value="2">2%</option><option value="3">3%</option><option value="5">5%</option></select></div>
        <div><label for="w-f">All-other-perils flat deductible</label><input id="w-f" name="flat" inputmode="decimal" value="1500"></div>
      </div>
      <div><label for="w-l">Estimated storm damage</label><input id="w-l" name="loss" inputmode="decimal" value="18900"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your percentage deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span style="background:#d9622b"></span><span style="background:#003776"></span></div>
      <div class="legend"><span><i style="background:#d9622b"></i>You pay</span><span><i style="background:#003776"></i>Policy pays</span></div>
      <div class="out-rows">
        <div><span>Payment with % deductible</span><b data-o="pdpay">$0</b></div>
        <div><span>Payment if the flat deductible applied</span><b data-o="flatpay">$0</b></div>
        <div><span>Extra out-of-pocket from % deductible</span><b data-o="diff">$0</b></div>
        <div><span>Damage needed before any payment</span><b data-o="thresh">$0</b></div>
      </div>
      <p class="todo-h">The same loss at other percentages</p>
      <div class="scen" data-o="ladder"></div>
      <p class="out-msg" data-o="below"></p>
    </div>
  </div>
</div>"""

DATES = """
<div class="tool" data-tool="dates">
  <div class="tool-head"><span>Idaho claim timeline builder</span><i>Exports to your calendar</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
      <p class="hint flush">Set each window to match your policy. Defaults are placeholders, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report the claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="2"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="10"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Many policies say 60 days after the insurer’s request.</span></div>
        <div><label for="t-a">Name your appraiser (days after a demand)</label><input id="t-a" name="appr" inputmode="numeric" value="20"><span class="hint">Counted from an assumed demand 45 days after the loss.</span></div>
        <div><label for="t-r">Depreciation recovery (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="180"></div>
        <div><label for="t-s">Suit limitation in your policy (days)</label><input id="t-s" name="suit" inputmode="numeric" value="730"><span class="hint">Use the number in your policy’s “Suit Against Us” clause.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download .ics calendar file</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the insurer accepted coverage for at least part of the loss?", "Get written confirmation of what the insurer has accepted. If the claim was denied, talk with an Idaho attorney before thinking about appraisal."),
    (3, "Do you have the insurer’s complete, itemized estimate?", "Ask in writing for the full line-item estimate, not just the payment summary."),
    (3, "Do you have your own line-item estimate?", "Get an itemized estimate from a contractor or estimator. A one-line bid won’t carry weight with a panel."),
    (2, "Did you photograph the damage soon after the loss?", "Collect every photo and note the date of each. Take new photos of current conditions too."),
    (2, "Have you found and read the appraisal clause in your policy?", "Look in the policy conditions for a paragraph titled ‘Appraisal’ and note any time limits it sets."),
    (2, "Do you know the suit-limitation period in your policy?", "Find the ‘Suit Against Us’ clause and put the date on your calendar. Our timeline builder can help."),
    (2, "Are temporary repairs done, with receipts saved?", "Finish reasonable temporary repairs, like tarps or water extraction, and keep every receipt."),
    (2, "Has hidden damage been opened up and documented?", "Make sure attics, wall cavities, framing and subfloors were inspected so the scope is complete."),
    (1, "Do you have a current declarations page?", "Download or request your declarations page from the insurer or agent."),
    (1, "Is your correspondence with the insurer organized by date?", "Gather letters, emails and claim notes in date order in one folder."),
    (2, "Is the gap more than about 10% of the estimate, or several thousand dollars?", "Run the numbers in our claim gap estimator. A small gap may not justify appraisal costs."),
    (1, "If the insurer requested a sworn proof of loss, has it been sent on time?", "If a proof of loss was requested, return it within the time the policy allows."),
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
      <div class="btn-row"><button type="button" class="btn ghost small" data-reset>Reset answers</button></div>
    </div>
    <div class="tool-out ready-out" aria-live="polite">
      <div>
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#e3ebf5" stroke-width="18"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#FFE835" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3" style="transition:stroke-dashoffset .5s,stroke .3s"/></svg>
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

SNOW = """
<div class="tool" data-tool="snow">
  <div class="tool-head"><span>Roof snow load estimator</span><i>Rough planning figure only</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="s-d">Snow depth on the roof (inches)</label><input id="s-d" name="depth" inputmode="decimal" value="20"></div>
        <div><label for="s-t">Type of snow</label><select id="s-t" name="type"><option value="7">Fresh, light powder (~7 lb/ft³)</option><option value="15" selected>Settled snow (~15 lb/ft³)</option><option value="25">Wet or wind-packed (~25 lb/ft³)</option></select></div>
      </div>
      <div class="row2">
        <div><label for="s-i">Ice layer thickness (inches)</label><input id="s-i" name="ice" inputmode="decimal" value="1"><span class="hint">Ice weighs about 57 lb/ft³.</span></div>
        <div><label for="s-r">Rain on snow (inches, optional)</label><input id="s-r" name="rain" inputmode="decimal" value="0"><span class="hint">Absorbed rain adds about 5.2 lb/ft² per inch.</span></div>
      </div>
      <div class="row2">
        <div><label for="s-dl">Roof design snow load (lb/ft²)</label><input id="s-dl" name="design" inputmode="decimal" value="30"><span class="hint">Ask your building department or check the plans.</span></div>
        <div><label for="s-a">Roof footprint (sq ft, optional)</label><input id="s-a" name="area" inputmode="decimal" value="2000"></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated load on the roof</small><b data-o="psf">0 lb/ft²</b></div>
      <div class="meter" aria-hidden="true"><span data-o="bar"></span><i></i></div>
      <div class="out-rows">
        <div><span>Snow layer</span><b data-o="snowpsf">0</b></div>
        <div><span>Ice layer</span><b data-o="icepsf">0</b></div>
        <div><span>Absorbed rain</span><b data-o="rainpsf">0</b></div>
        <div><span>Share of design load</span><b data-o="share">0%</b></div>
        <div><span>Total weight on the roof</span><b data-o="total">—</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "claim-gap-net-estimator", "name": "Claim Gap & Net Recovery Estimator", "keyword": "claim gap estimator",
        "icon": "Δ", "kind": "Calculator",
        "short": "Size the dispute, project an award and see your net after appraiser and umpire fees at three landing points.",
        "title": "Claim Gap Estimator | Net Recovery After Appraisal Fees",
        "desc": "Free claim gap estimator: compare your estimate with the insurer’s, project an award and subtract appraisal fees to see your likely net.",
        "h1": "Claim Gap Estimator: What Would Appraisal Net You?",
        "lede": "Enter the insurer’s estimate and yours, pick where an award might land and add realistic fees. The estimator shows your net at three landing points and the break-even point for your costs.",
        "markup": GAP_FULL,
        "explain": """
<h2>How to read the results</h2>
<ol><li><strong>Amount in dispute</strong> is your estimate minus the insurer’s, both at replacement cost.</li>
<li><strong>Projected award</strong> assumes the panel lands at the percentage you choose within that gap.</li>
<li><strong>Net increase</strong> subtracts your appraiser’s fee and, if checked, half the umpire’s fee.</li>
<li><strong>Break-even landing point</strong> is the percentage at which your costs equal your gain. Below it, appraisal costs more than it recovers.</li></ol>
<h2>Why we show three landing points</h2>
<p>Panels rarely award either side’s exact number. Documented items tend to survive and padded ones tend not to. If your result only works at 80% or more, the case depends on near-total success. If it still works at 30%, it’s more robust. The three-scenario table makes that visible at a glance.</p>
<h2>What it doesn’t include</h2>
<p>Deductibles, depreciation timing and policy limits affect what you’re paid, not the size of the dispute. For holdback math, use the <a href="/policy-math-tools/rcv-acv-holdback-calculator/">RCV vs. ACV holdback calculator</a>. All figures are illustrative.</p>
""",
        "faqs": [("Is the projected award a prediction?", "No. It’s a planning scenario based on the percentage you choose. Real awards depend on evidence, the panel and the policy."), ("How are appraiser fees usually structured?", "Arrangements vary: flat fees, hourly billing and percentage fees all exist. Get any fee in writing before work starts, and check whether percentage fees are allowed on your type of claim.")],
    },
    {
        "slug": "rcv-acv-holdback-calculator", "name": "RCV vs. ACV Holdback Calculator", "keyword": "RCV vs ACV calculator",
        "icon": "ACV", "kind": "Calculator",
        "short": "Estimate the first actual-cash-value check, the depreciation held back and the total after repairs.",
        "title": "RCV vs ACV Calculator | Depreciation Holdback Estimator",
        "desc": "Free RCV vs ACV calculator: list damaged items with age and expected life to estimate your first check, recoverable depreciation and total.",
        "h1": "RCV vs. ACV Calculator for Depreciation Holdback",
        "lede": "Replacement-cost policies usually pay in two parts: actual cash value now and recoverable depreciation after repairs. Enter your damaged items to see how the money splits.",
        "markup": DEP,
        "explain": """
<h2>The method behind the numbers</h2>
<p>This calculator applies straight-line depreciation, age divided by expected life, capped at the maximum you select. Real estimates may adjust for condition, use different life tables or treat some items, such as permits or debris removal, as non-depreciable. Treat the result as a planning figure.</p>
<h2>Common life expectancies</h2>
<div class="table-wrap"><table><thead><tr><th>Item</th><th>Typical range</th></tr></thead><tbody>
<tr><th>Laminated asphalt shingles</th><td>25–30 years</td></tr><tr><th>Three-tab shingles</th><td>15–25 years</td></tr><tr><th>Standing-seam metal roofing</th><td>40–60 years</td></tr><tr><th>Vinyl siding</th><td>30–40 years</td></tr><tr><th>Interior paint</th><td>8–12 years</td></tr><tr><th>Carpet</th><td>8–12 years</td></tr>
</tbody></table></div>
<h2>Collecting the holdback</h2>
<p>Most replacement cost policies pay recoverable depreciation once repairs are complete, often within a set number of days. Send the insurer invoices and photos of the finished work. Our <a href="/policy-math-tools/idaho-claim-timeline-builder/">claim timeline builder</a> can remind you before that window closes.</p>
""",
        "faqs": [("Can labor be depreciated?", "Practices differ by policy and jurisdiction. Ask the insurer to explain in writing how its estimate treats labor depreciation."), ("What if I decide not to repair?", "Under most replacement cost policies you keep the ACV payment but may not collect the held-back depreciation.")],
    },
    {
        "slug": "roof-pitch-squares-calculator", "name": "Roof Pitch & Squares Calculator", "keyword": "roof squares calculator",
        "icon": "▲", "kind": "Calculator",
        "short": "Turn a footprint into true roof squares with pitch and waste, then compare against the carrier’s count.",
        "title": "Roof Squares Calculator | Pitch, Waste & Carrier Check",
        "desc": "Roof squares calculator for insurance claims: turn footprint and pitch into true roof area, add waste and compare it with the carrier’s count.",
        "h1": "Roof Squares Calculator With Pitch and Waste",
        "lede": "Measurement errors are a common reason roof claims come up short. Enter your footprint and pitch to estimate true roof area, then compare it with the squares on the insurer’s estimate.",
        "markup": ROOF,
        "explain": """
<h2>The math</h2>
<p>Roof surface is larger than the footprint underneath it. The pitch multiplier is √(1 + (rise ÷ 12)²). A 5/12 roof is about 8.3% larger than its footprint; a 12/12 roof is about 41.4% larger. Idaho’s deep eaves add area too, so include overhangs.</p>
<h2>Checking the insurer’s estimate</h2>
<ul><li>Find total squares and the waste percentage in the roofing section.</li>
<li>Enter the carrier’s squares here to see the difference. Gaps over 5–10% deserve a closer look.</li>
<li>Look for steep charges, often starting around 7/12, and high-roof charges for two-story sections.</li>
<li>Check that ridge cap, starter, drip edge and ice-and-water shield appear as separate lines.</li></ul>
<h2>Limits</h2>
<p>Roofs with several pitches, dormers and valleys need plane-by-plane measurement. Aerial reports or a field measurement will be more accurate. Use this as a sanity check.</p>
""",
        "faqs": [("What is a roofing square?", "One square is 100 square feet of roof surface. Many Idaho single-family homes fall somewhere between 20 and 45 squares."), ("Why does waste change by roof style?", "Hips, valleys and dormers need more cutting, so more material is lost as scrap.")],
    },
    {
        "slug": "percentage-deductible-calculator", "name": "Percentage Deductible Calculator", "keyword": "percentage deductible calculator",
        "icon": "%", "kind": "Calculator",
        "short": "See a percentage wind/hail deductible in dollars, the damage threshold for any payment and a 0.5–5% ladder.",
        "title": "Percentage Deductible Calculator | Wind & Hail in Dollars",
        "desc": "Free percentage deductible calculator: turn a wind/hail deductible into dollars, compare it with a flat deductible and see what a claim pays.",
        "h1": "Percentage Deductible Calculator for Wind and Hail",
        "lede": "A 1% deductible sounds small until you multiply it by your dwelling limit. See your deductible in dollars, what a storm claim would pay and how the answer changes at other percentages.",
        "markup": DEDUCT,
        "explain": """
<h2>Why percentage deductibles catch people off guard</h2>
<p>Some Idaho homeowners policies, especially in hail-prone areas, use a separate wind/hail deductible calculated as a percentage of Coverage A. On a $465,000 dwelling limit, a 1% deductible is $4,650, not the $1,500 flat amount that applies to other perils.</p>
<h2>Where to find yours</h2>
<p>Check the declarations page for “wind/hail” or “windstorm or hail” deductible. Endorsements in the policy explain when it applies. If you don’t see one, your policy may use a single flat deductible for all perils.</p>
<h2>How it affects a dispute</h2>
<p>The deductible doesn’t change the amount of loss an appraisal panel decides, but it changes what you receive. The “damage needed before any payment” line shows the threshold, so you can judge whether a dispute is worth pursuing.</p>
""",
        "faqs": [("Is the percentage based on the loss or on my coverage?", "Usually on Coverage A, the dwelling limit, not on the size of the loss. Check your policy wording."), ("Can I change it?", "Usually at renewal. A lower percentage costs more in premium but reduces your share of each storm loss.")],
    },
    {
        "slug": "idaho-claim-timeline-builder", "name": "Idaho Claim Timeline Builder", "keyword": "claim timeline builder",
        "icon": "◷", "kind": "Planner",
        "short": "Map notice, proof-of-loss, appraiser, holdback and suit dates from your loss date, then export to a calendar.",
        "title": "Idaho Claim Timeline Builder | Deadlines to Your Calendar",
        "desc": "Idaho claim timeline builder: enter your date of loss to map proof-of-loss, appraisal, holdback and suit dates, then export an .ics file.",
        "h1": "Idaho Claim Timeline Builder With Calendar Export",
        "lede": "Policy deadlines keep running while you argue about the number. Enter your date of loss and the windows in your policy to build a timeline you can download straight to your calendar.",
        "markup": DATES,
        "explain": """
<h2>The dates that matter</h2>
<ul><li><strong>Notice.</strong> Policies require prompt notice of a loss. Late reporting is a defense insurers raise often.</li>
<li><strong>Proof of loss.</strong> If the insurer asks for a sworn proof of loss, many policies allow 60 days to return it.</li>
<li><strong>Naming an appraiser.</strong> Many appraisal clauses give each side 20 days after a written demand to name its appraiser.</li>
<li><strong>Depreciation recovery.</strong> Replacement cost policies typically require repairs within a set period to collect holdback.</li>
<li><strong>Suit limitation.</strong> Policies set a period for filing suit. Idaho law can affect how those provisions apply, so confirm the deadline with an Idaho attorney. Appraisal may not pause it.</li></ul>
<div class="note"><b class="h">Important</b>This builder uses the numbers you enter. It isn’t legal advice, and courts can interpret policy deadlines differently. If a deadline is close, contact an Idaho attorney.</div>
""",
        "faqs": [("Is the date of loss the day I found the damage?", "Usually it’s the date the storm or event happened. Weather records for your address can help pin it down."), ("Does invoking appraisal pause the suit deadline?", "Not automatically. Some policies or written agreements address it; many don’t. Protect the deadline independently.")],
    },
    {
        "slug": "appraisal-readiness-checkup", "name": "Appraisal Readiness Checkup", "keyword": "appraisal readiness checkup",
        "icon": "✓", "kind": "Checklist",
        "short": "Twelve yes/no questions that score your claim file and build a personal to-do list before you demand appraisal.",
        "title": "Appraisal Readiness Checkup | Is Your Claim File Ready?",
        "desc": "Appraisal readiness checkup: twelve quick questions score how ready your property claim is for appraisal and list what to finish first.",
        "h1": "Appraisal Readiness Checkup for Your Claim File",
        "lede": "Strong appraisals are built before the demand letter goes out. Answer twelve quick questions to see where your file stands and what to fix first.",
        "markup": READY,
        "explain": """
<h2>How the score is weighted</h2>
<p>Questions about coverage, estimates and evidence carry the most weight. They decide whether appraisal is even the right tool and how well your number will hold up. Paperwork items matter too, but they’re easier to fix.</p>
<h2>Reading your result</h2>
<ul><li><strong>75 and above:</strong> your file is in good shape. A professional review of the gap is a sensible next step.</li>
<li><strong>45 to 74:</strong> close the open items first. Each one strengthens your position.</li>
<li><strong>Below 45:</strong> demanding appraisal now could lock in a low number. Build the file first.</li></ul>
""",
        "faqs": [("Is anything I enter saved?", "No. The checkup runs entirely in your browser. Nothing is stored or sent."), ("Can I share the result?", "Yes. Take a screenshot or copy your to-do list and bring it to a consultation.")],
    },
    {
        "slug": "roof-snow-load-estimator", "name": "Roof Snow Load Estimator", "keyword": "roof snow load estimator",
        "icon": "❄", "kind": "Estimator",
        "short": "Estimate the weight of snow, ice and rain on your roof and compare it with the design load. Built for Idaho winters.",
        "title": "Roof Snow Load Estimator | Snow & Ice Weight in lb/ft²",
        "desc": "Free roof snow load estimator for Idaho winters: estimate snow, ice and rain weight in pounds per square foot and compare it with design load.",
        "h1": "Roof Snow Load Estimator for Idaho Winters",
        "lede": "Snow weight depends on how wet and packed it is, not just how deep. Enter the depth, the type of snow and any ice to estimate the load on your roof and how close it is to the design figure.",
        "markup": SNOW,
        "explain": """
<h2>How the estimate works</h2>
<p>Load in pounds per square foot equals depth in feet times density in pounds per cubic foot. Light, fresh snow may weigh around 7 lb/ft³, settled snow around 15 and wet or wind-packed snow 25 or more. Ice is about 57 lb/ft³. Rain soaking into a snowpack adds about 5.2 lb/ft² for every inch absorbed. These densities are typical values; real snow varies.</p>
<h2>Design loads vary widely in Idaho</h2>
<p>Required roof snow loads differ by county, elevation and roof type. A home in Lewiston is designed for far less snow than one in Ketchum or Sandpoint. Your local building department can tell you the design load used in your area, and building plans often list it.</p>
<h2>If your roof is near its limit</h2>
<ul><li>Watch for sagging ceilings, cracking sounds, doors that suddenly stick and new cracks in drywall.</li>
<li>Hire insured professionals for snow removal. Roof work in winter is dangerous.</li>
<li>If you see signs of structural stress, leave the building and call for help.</li>
<li>If damage occurs, photograph it and report it to your insurer promptly. See <a href="/property-claim-appraisal/snow-load-ice-dam-appraisal/">snow load damage appraisal</a>.</li></ul>
<div class="note"><b class="h">Not an engineering tool</b>This estimator is for general awareness. It doesn’t account for drifting, sliding snow, roof shape or the condition of the structure. Only a qualified engineer can evaluate a specific roof.</div>
""",
        "faqs": [("How much does a foot of snow weigh?", "It depends on density. A foot of light powder might weigh around 7 lb/ft², while a foot of wet, packed snow could weigh 25 lb/ft² or more."), ("Is snow-load damage covered by insurance?", "Many policies cover collapse caused by the weight of snow or ice, but conditions and exclusions vary. Read the collapse section of your policy.")],
    },
]
