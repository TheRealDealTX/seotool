"""Free claim calculators: markup + explanatory copy. Logic lives in static/assets/js/app.js.
All tools run in the browser; nothing is stored or sent."""

C_NAVY, C_GOLD, C_BRICK, C_MIST = "#002A86", "#FFCE00", "#C4512A", "#C9D3EA"

GAP_FULL = f"""
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Claim gap &amp; fee projector</span><i>Runs in your browser</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Insurer’s estimate (RCV, $)</label><input id="g-ins" name="insurer" inputmode="decimal" value="21600"><span class="hint">The replacement cost total on the carrier’s estimate.</span></div>
        <div><label for="g-own">Your estimate (RCV, $)</label><input id="g-own" name="yours" inputmode="decimal" value="36400"><span class="hint">Your contractor’s or independent line-item estimate.</span></div>
      </div>
      <div><label for="g-land">Where might the award land inside the gap?</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% means the carrier’s number holds; 100% means your full number is awarded.</span></div>
      <div class="row2">
        <div><label for="g-ft">Appraiser fee arrangement</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of the increase (%)</option></select></div>
        <div><label for="g-fee">Fee amount</label><input id="g-fee" name="fee" inputmode="decimal" value="2800"></div>
      </div>
      <label class="check"><input type="checkbox" name="useump" checked> Add my half of an umpire’s fee</label>
      <div><label for="g-ump">Umpire’s total fee ($, split 50/50)</label><input id="g-ump" name="umpire" inputmode="decimal" value="3200"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Projected net increase to you</small><b data-o="net">$0</b></div>
      <div class="stack" aria-hidden="true"><span style="background:{C_MIST}"></span><span style="background:{C_GOLD}"></span><span style="background:{C_BRICK}"></span></div>
      <div class="legend"><span><i style="background:{C_MIST}"></i>Carrier’s number</span><span><i style="background:{C_GOLD}"></i>Your net gain</span><span><i style="background:{C_BRICK}"></i>Appraisal costs</span></div>
      <div class="out-rows">
        <div><span>Amount in dispute</span><b data-o="gap">$0</b></div>
        <div><span>Gap as a share of the carrier’s estimate</span><b data-o="pct">—</b></div>
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
  <div class="tool-head"><span>Quick gap check</span><i>No sign-up</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="m-ins">Insurer’s estimate ($)</label><input id="m-ins" name="insurer" inputmode="decimal" value="16800"></div>
      <div><label for="m-own">Your contractor’s estimate ($)</label><input id="m-own" name="yours" inputmode="decimal" value="29500"></div>
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
  <div class="tool-head"><span>RCV vs. ACV holdback calculator</span><i>Add as many line items as you need</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Modified-bitumen flat roof", 9800, 8, 20), ("Plaster repair & paint — two rooms", 3200, 6, 12), ("Hardwood floor refinish", 2600, 10, 25), ("Water heater", 1450, 7, 12)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn ghost small" data-add data-run>+ Add line item</button></div>
      <div class="row2">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="1000"></div>
        <div><label for="d-cap">Depreciation cap</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="60">60%</option><option value="75" selected>75%</option><option value="80">80%</option><option value="90">90%</option></select><span class="hint">Many estimates cap depreciation; check yours.</span></div>
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
        <div><span>Replacement cost value (RCV)</span><b data-o="rcv">$0</b></div>
        <div><span>Total depreciation</span><b data-o="dep">$0</b></div>
        <div><span>Depreciation as a share of RCV</span><b data-o="deppct">0%</b></div>
        <div><span>Actual cash value (ACV)</span><b data-o="acv">$0</b></div>
      </div>
    </div>
  </div>
</div>"""

ROOF = """
<div class="tool" data-tool="roof">
  <div class="tool-head"><span>Roof pitch &amp; squares estimator</span><i>Check the carrier’s measurements</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <fieldset class="bare"><legend class="sr-only">Measurement method</legend>
        <div class="btn-row">
          <label class="check"><input type="radio" name="mode" value="dims" checked> Footprint length × width</label>
          <label class="check"><input type="radio" name="mode" value="area"> I know the footprint area</label>
        </div></fieldset>
      <div class="row2" data-mode="dims">
        <div><label for="r-l">Footprint length (ft)</label><input id="r-l" name="len" inputmode="decimal" value="48"></div>
        <div><label for="r-w">Footprint width (ft)</label><input id="r-w" name="wid" inputmode="decimal" value="30"></div>
      </div>
      <div data-mode="dims"><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="12"></div>
      <div data-mode="area" hidden><label for="r-a">Footprint area incl. overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="1650"></div>
      <div class="row2">
        <div><label for="r-p">Roof pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 8 else "", p) for p in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18]) + """</select></div>
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="5">5% — low-slope / flat</option><option value="10">10% — simple gable</option><option value="13" selected>13% — gable with dormers</option><option value="15">15% — hip roof</option><option value="20">20% — slate or very cut-up</option></select></div>
      </div>
      <div><label for="r-pr">Installed price per square (optional, $)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 575"><span class="hint">Use a local contractor’s quote for a rough replacement figure.</span></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Roof squares (before waste)</small><b data-o="sq">0</b></div>
      <div class="out-rows">
        <div><span>Pitch multiplier</span><b data-o="mult">1.000</b></div>
        <div><span>Roof surface area</span><b data-o="surface">0</b></div>
        <div><span>Squares to order (with waste)</span><b data-o="order">0</b></div>
        <div><span>Shingle bundles (3 per square)</span><b data-o="bundles">0</b></div>
        <div><span>Rough replacement cost</span><b data-o="cost">—</b></div>
      </div>
      <p class="out-msg" data-o="steep"></p>
    </div>
  </div>
</div>"""

DEDUCT = f"""
<div class="tool" data-tool="deduct">
  <div class="tool-head"><span>Deductible impact calculator</span><i>Percentage vs. flat dollar</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling coverage (Coverage A, $)</label><input id="w-a" name="cova" inputmode="decimal" value="310000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Percentage deductible (wind/hail or similar)</label><select id="w-p" name="pct"><option value="0.5">0.5%</option><option value="1" selected>1%</option><option value="2">2%</option><option value="3">3%</option><option value="5">5%</option></select></div>
        <div><label for="w-f">Flat all-other-perils deductible ($)</label><input id="w-f" name="flat" inputmode="decimal" value="1000"></div>
      </div>
      <div><label for="w-l">Estimated covered damage ($)</label><input id="w-l" name="loss" inputmode="decimal" value="14800"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your percentage deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span style="background:{C_BRICK}"></span><span style="background:{C_MIST}"></span></div>
      <div class="legend"><span><i style="background:{C_BRICK}"></i>You pay</span><span><i style="background:{C_MIST}"></i>Policy pays</span></div>
      <div class="out-rows">
        <div><span>Payment with the % deductible</span><b data-o="pdpay">$0</b></div>
        <div><span>Payment if the flat deductible applied</span><b data-o="flatpay">$0</b></div>
        <div><span>Extra out-of-pocket from the % deductible</span><b data-o="diff">$0</b></div>
      </div>
      <p class="out-msg" data-o="below"></p>
    </div>
  </div>
</div>"""

DATES = """
<div class="tool" data-tool="dates">
  <div class="tool-head"><span>Claim deadline calendar</span><i>Exports an .ics file</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
      <p class="hint">Adjust each window to match your policy. Defaults are common figures, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report the claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="2"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="10"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Often counted from the carrier’s request.</span></div>
        <div><label for="t-r">Depreciation recovery (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="180"></div>
        <div><label for="t-s">Suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="365"><span class="hint">One year = 365 days, a common clause.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download .ics calendar file</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the insurer accepted coverage for at least part of the loss?", "Get written confirmation of what is covered. If the claim was denied outright, talk to a Pennsylvania attorney before considering appraisal."),
    (3, "Do you have the carrier’s full, line-item estimate?", "Ask in writing for the complete itemized estimate, not just the payment summary."),
    (3, "Do you have your own itemized estimate?", "Get a line-item estimate from a contractor or estimator; a one-line bid won’t carry weight with a panel."),
    (3, "Do you know your policy’s suit-limitation date?", "Find the ‘Suit Against Us’ condition (often one year in Pennsylvania policies) and put the date on your calendar."),
    (2, "Do you have dated photos taken soon after the loss?", "Collect every photo and video, note the dates, and add photos of current conditions."),
    (2, "Have you read the appraisal clause in your policy?", "Find the ‘Appraisal’ paragraph in the conditions section and note any time limits for naming an appraiser."),
    (2, "Have temporary repairs been made, with receipts saved?", "Tarp, dry out or board up as needed and keep every receipt."),
    (2, "Has hidden damage been opened up and documented?", "Make sure wet walls, attics, decking and party walls have been checked so the scope is complete."),
    (2, "Is the gap more than roughly 10% or $5,000?", "Run the numbers in the claim gap & fee projector; a small gap may not justify appraisal costs."),
    (1, "Do you have your current declarations page?", "Download or request the declarations page that was in force on the date of loss."),
    (1, "Is your correspondence with the carrier organized by date?", "Put letters, emails and claim notes in date order."),
    (1, "If the carrier asked for a sworn proof of loss, was it returned on time?", "If a proof of loss was requested, complete it and keep proof of delivery."),
]

READY = """
<div class="tool tool-wide" data-tool="ready">
  <div class="tool-head"><span>Appraisal readiness checkup</span><i>12 questions · about two minutes</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <ol class="quiz">""" + "".join(
    '<li data-w="%d" data-fix="%s"><span>%s</span><span class="yn"><button type="button" class="yes" aria-pressed="false">Yes</button><button type="button" class="no" aria-pressed="false">No</button></span></li>' % (w, f, q)
    for w, q, f in _QUIZ) + f"""
      </ol>
      <div class="btn-row"><button type="button" class="btn ghost small" data-reset>Reset answers</button></div>
    </div>
    <div class="tool-out tool-out-score" aria-live="polite">
      <div>
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#E4E9F5" stroke-width="18"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="{C_GOLD}" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3" style="transition:stroke-dashoffset .5s,stroke .3s"/></svg>
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
  <div class="tool-head"><span>Roof snow load estimator</span><i>Illustrative only</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="s-a">Roof area, measured flat (footprint, sq ft)</label><input id="s-a" name="area" inputmode="decimal" value="1400"><span class="hint">Snow load is measured on the horizontal footprint, not the sloped surface.</span></div>
      <div class="row2">
        <div><label for="s-f">Fresh, fluffy snow (inches)</label><input id="s-f" name="fresh" inputmode="decimal" value="14"></div>
        <div><label for="s-p">Settled or wet snow (inches)</label><input id="s-p" name="packed" inputmode="decimal" value="8"></div>
      </div>
      <div class="row2">
        <div><label for="s-i">Ice layer (inches)</label><input id="s-i" name="ice" inputmode="decimal" value="1"></div>
        <div><label for="s-d">Roof design snow load (psf)</label><input id="s-d" name="design" inputmode="decimal" value="30"><span class="hint">Ask your builder or local code office; it varies by town and building age.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated load on the roof</small><b data-o="psf">0 psf</b></div>
      <div class="meter" aria-hidden="true"><span data-o="bar"></span></div>
      <div class="out-rows">
        <div><span>Total weight of snow and ice</span><b data-o="lbs">0 lb</b></div>
        <div><span>In tons</span><b data-o="tons">0</b></div>
        <div><span>Share of design load</span><b data-o="share">0%</b></div>
      </div>
      <p class="out-msg" data-o="snowmsg"></p>
    </div>
  </div>
</div>"""

T = "/claim-calculators/"

TOOLS = [
    {
        "slug": "claim-gap-fee-projector", "name": "Claim Gap & Fee Projector", "icon": "Δ", "kind": "Calculator",
        "keyword": "appraisal claim gap calculator",
        "short": "Size the dispute, test where an award could land and subtract appraiser and umpire fees to see your net.",
        "title": "Claim Gap & Fee Projector | Is Appraisal Worth It?",
        "desc": "Free appraisal claim gap calculator: compare your estimate with the insurer’s, test award outcomes and subtract fees to see the likely net.",
        "h1": "Claim Gap & Fee Projector: Is Appraisal Worth It in Pennsylvania?",
        "lede": "Enter the carrier’s number and yours, slide the award between them and add realistic fees. The projector shows whether appraisal is likely to leave you ahead after costs.",
        "markup": GAP_FULL,
        "explain": f"""
<h2>Reading the projection</h2>
<ol><li><strong>Use replacement cost totals for both estimates</strong>, before depreciation and the deductible, so you compare like with like.</li>
<li><strong>Test a range, not one number.</strong> Try the slider at 30%, 50% and 75%. Panels rarely adopt either side’s opening figure in full.</li>
<li><strong>Enter the fee you were actually quoted.</strong> Flat-fee and percentage arrangements change the answer more than people expect.</li>
<li><strong>Keep the umpire box on</strong> unless you’re confident the two appraisers will agree without one.</li></ol>
<h2>A quick illustrative example</h2>
<p>Say the insurer wrote a Lancaster County roof and gutter claim at $21,600 and your contractor’s line-item estimate is $36,400. The gap is $14,800. If a panel lands at 55% of the gap, the award is about $29,740 — an increase of roughly $8,140 before costs. Subtract a $2,800 flat fee and half of a $3,200 umpire fee and the projected net is about $3,740. These are illustrative figures, not results for any real claim.</p>
<h2>What this tool doesn’t account for</h2>
<p>Depreciation timing, policy limits, sub-limits and your deductible change what you are paid, not the size of the dispute. Use the <a href="{T}rcv-acv-holdback-calculator/">RCV vs. ACV holdback calculator</a> for that side of the math, and check the <a href="{T}claim-deadline-calendar/">deadline calendar</a> before you decide — a one-year suit clause doesn’t wait for a panel.</p>
""",
        "faqs": [("Is the projected award a prediction?", "No. It is a planning scenario based on the numbers you enter. Real awards depend on documentation, the policy and the panel."),
                 ("How are umpire fees usually paid?", "Most appraisal clauses have each side pay its own appraiser and split the umpire’s fee equally. Read your policy’s wording to confirm."),
                 ("What gap is usually worth appraising?", "There is no fixed threshold. Many owners start the conversation when the gap is more than about 10% of the carrier’s estimate or several thousand dollars.")],
    },
    {
        "slug": "rcv-acv-holdback-calculator", "name": "RCV vs. ACV Holdback Calculator", "icon": "ACV", "kind": "Calculator",
        "keyword": "RCV vs ACV calculator",
        "short": "Split a replacement cost claim into the first ACV check, the recoverable holdback and the total after repairs.",
        "title": "RCV vs ACV Calculator | Depreciation & Holdback",
        "desc": "Free RCV vs ACV calculator: list damaged items by age and life span to estimate your first check, recoverable depreciation and final total.",
        "h1": "RCV vs. ACV Holdback Calculator for Property Claims",
        "lede": "Replacement cost policies usually pay twice: an actual cash value check now and recoverable depreciation after repairs. List your line items to see how the money splits.",
        "markup": DEP,
        "explain": f"""
<h2>How this calculator depreciates</h2>
<p>It uses straight-line depreciation — age divided by expected life — capped at the percentage you pick. Real estimates may adjust for condition, use different life expectancies or leave some items undepreciated, so treat the output as a planning figure, not the carrier’s exact number.</p>
<h2>Life spans that often appear in Pennsylvania estimates</h2>
<div class="table-wrap"><table><thead><tr><th>Item</th><th>Common range</th></tr></thead><tbody>
<tr><th>Architectural asphalt shingles</th><td>25–30 years</td></tr><tr><th>Modified-bitumen flat roof</th><td>15–20 years</td></tr><tr><th>Natural slate</th><td>75 years or more</td></tr><tr><th>Interior paint</th><td>8–12 years</td></tr><tr><th>Carpet</th><td>8–12 years</td></tr><tr><th>Water heater</th><td>10–15 years</td></tr>
</tbody></table></div>
<p>Ranges vary by product and estimating platform; these are general reference points.</p>
<h2>Getting the holdback released</h2>
<p>Most replacement cost policies release recoverable depreciation after repairs are finished within a stated period. Send final invoices and completion photos, and set a reminder in the <a href="{T}claim-deadline-calendar/">claim deadline calendar</a> so the window doesn’t close on you.</p>
""",
        "faqs": [("Should labor be depreciated?", "Practices differ by policy, carrier and court decisions. Ask the carrier to explain in writing how labor is treated in your estimate."),
                 ("What happens if I don’t repair?", "Under most replacement cost policies you keep the actual cash value payment but may not collect the held-back depreciation.")],
    },
    {
        "slug": "roof-pitch-squares-estimator", "name": "Roof Pitch & Squares Estimator", "icon": "▲", "kind": "Calculator",
        "keyword": "roof squares calculator",
        "short": "Turn a footprint and pitch into true roof squares, bundles and a rough cost to check the carrier’s measurements.",
        "title": "Roof Squares Calculator | Pitch, Waste & Bundles",
        "desc": "Free roof squares calculator: convert footprint, pitch and waste factor into true roof area and bundles, then check your insurance estimate.",
        "h1": "Roof Pitch & Squares Estimator for Insurance Claims",
        "lede": "Short measurements quietly shrink a lot of roof claims. Enter the footprint and pitch to estimate true surface area, squares and bundles before you accept the number.",
        "markup": ROOF,
        "explain": """
<h2>The math behind the result</h2>
<p>A sloped roof has more surface than the footprint under it. The pitch multiplier is √(1 + (rise ÷ 12)²). An 8/12 roof — common on Pennsylvania farmhouses and older two-story homes — is about 20% larger than its footprint; a 12/12 roof is about 41% larger.</p>
<h2>Five things to check in the carrier’s roof section</h2>
<ul><li>Total squares and the waste percentage used.</li>
<li>Steep-slope charges, often starting around 7/12 or 8/12.</li>
<li>High-roof or two-story access charges.</li>
<li>Separate lines for ridge cap, starter, drip edge, ice and water shield and valley metal.</li>
<li>Whether a slate or flat-roof section was priced as ordinary asphalt shingles.</li></ul>
<h2>Where a footprint estimate falls short</h2>
<p>Cut-up roofs with several pitches, dormers and valleys need to be measured plane by plane. Rowhome flat roofs need a low-slope (5%) waste figure instead. Treat this as a sanity check alongside a field measurement or aerial report.</p>
""",
        "faqs": [("What is a roofing square?", "One hundred square feet of roof surface. Many two-story Pennsylvania homes fall somewhere between 18 and 35 squares, but sizes vary widely."),
                 ("Why does waste change with roof style?", "Hips, valleys and dormers require more cutting, and slate breakage adds more, so more material ends up as scrap.")],
    },
    {
        "slug": "deductible-impact-calculator", "name": "Deductible Impact Calculator", "icon": "%", "kind": "Calculator",
        "keyword": "percentage deductible calculator",
        "short": "Convert a percentage deductible into dollars and see how much of a storm loss your policy would actually pay.",
        "title": "Percentage Deductible Calculator | Dollars & Payout",
        "desc": "Free percentage deductible calculator: turn a wind, hail or other % deductible into dollars and compare the payout with a flat deductible.",
        "h1": "Deductible Impact Calculator: Percentage vs. Flat Deductibles",
        "lede": "One percent sounds small until you multiply it by your dwelling limit. See your deductible in dollars and how it changes what a covered loss would pay.",
        "markup": DEDUCT,
        "explain": """
<h2>Why a percentage deductible can surprise you</h2>
<p>Most Pennsylvania homeowner policies use a flat deductible, but some carry a separate percentage deductible for wind and hail, and the number is calculated from Coverage A — the dwelling limit. On an illustrative $310,000 dwelling limit, a 1% deductible is $3,100 and a 2% deductible is $6,200.</p>
<h2>Where to find yours</h2>
<p>Look on the declarations page for “windstorm or hail,” “wind/hail” or a percentage next to the deductible line. Endorsements later in the policy explain when it applies. Since Pennsylvania has no state wind pool, these terms come from your own carrier’s policy forms.</p>
<h2>How deductibles interact with appraisal</h2>
<p>Appraisal decides the amount of loss; the deductible then comes off the top. A loss that barely clears the deductible may not justify a dispute, while one well above it may. Run the result through the <a href="/claim-calculators/claim-gap-fee-projector/">claim gap &amp; fee projector</a> before deciding.</p>
""",
        "faqs": [("Does the percentage apply to the whole loss?", "It is usually calculated from Coverage A but subtracted from the entire covered wind or hail loss. Check your policy wording for how it is applied."),
                 ("Can I change my deductible?", "Usually at renewal. A higher deductible lowers the premium but raises your share of each loss.")],
    },
    {
        "slug": "claim-deadline-calendar", "name": "Claim Deadline Calendar", "icon": "◷", "kind": "Planner",
        "keyword": "insurance claim deadline calculator",
        "short": "Map notice, proof-of-loss, holdback and one-year suit dates from your date of loss, then export them.",
        "title": "Insurance Claim Deadline Calculator | .ics Export",
        "desc": "Free insurance claim deadline calculator: map notice, proof of loss, holdback and one-year suit dates, then export them to your calendar.",
        "h1": "Pennsylvania Insurance Claim Deadline Calendar",
        "lede": "Policy deadlines keep running while you argue about the number. Enter your date of loss and your policy’s windows to build a timeline you can download to any calendar app.",
        "markup": DATES,
        "explain": """
<h2>The dates that matter most</h2>
<ul><li><strong>Prompt notice.</strong> Policies require you to report a loss promptly. Late notice is a defense carriers raise often.</li>
<li><strong>Proof of loss.</strong> If the carrier asks for a sworn proof of loss, many policies allow 60 days to return it.</li>
<li><strong>Depreciation recovery.</strong> Replacement cost policies typically require repairs within a set time to release the holdback.</li>
<li><strong>Suit limitation.</strong> Many Pennsylvania property policies limit lawsuits to one year from the date of loss, and Pennsylvania courts have generally enforced those clauses. Appraisal may not pause the clock unless the policy or a written agreement says so.</li></ul>
<div class="note"><b class="h">Important</b>This calendar uses the numbers you enter. It isn’t legal advice, and courts can read policy deadlines differently. If a deadline is close, contact a Pennsylvania attorney promptly.</div>
<p>Read more in our guide to the <a href="/policy-and-claim-guides/one-year-suit-limitation-and-appraisal/">one-year suit clause and appraisal</a>.</p>
""",
        "faqs": [("Is the date of loss the day I noticed the damage?", "Usually it is the date the storm or event happened. Weather records for your address can help pin it down."),
                 ("Does demanding appraisal stop the suit-limitation clock?", "Not automatically. Some policies or written agreements address it, many don’t, so protect the deadline separately.")],
    },
    {
        "slug": "appraisal-readiness-checkup", "name": "Appraisal Readiness Checkup", "icon": "✓", "kind": "Checklist",
        "keyword": "appraisal readiness checklist",
        "short": "Answer twelve yes/no questions to score your claim file and get a to-do list before demanding appraisal.",
        "title": "Appraisal Readiness Checklist | Score Your Claim",
        "desc": "Free appraisal readiness checklist: twelve questions score your property claim file and build a to-do list of what to finish before appraisal.",
        "h1": "Appraisal Readiness Checkup: Is Your Claim File Ready?",
        "lede": "Strong appraisals are built before the demand letter goes out. Answer twelve quick questions to see where your file stands and what to fix first.",
        "markup": READY,
        "explain": """
<h2>How the checkup is weighted</h2>
<p>Coverage, estimates and the suit-limitation date carry the most weight because they decide whether appraisal is the right tool at all and whether you have time to use it. Paperwork items still matter, but they are easier to fix.</p>
<h2>What to do with your score</h2>
<ul><li><strong>75 or higher:</strong> your file is in good shape. A professional review of the gap is the logical next step.</li>
<li><strong>45 to 74:</strong> close the open items first; each one strengthens your number.</li>
<li><strong>Below 45:</strong> demanding appraisal now could lock in a low award. Build the file first.</li></ul>
""",
        "faqs": [("Is anything I enter saved or sent?", "No. The checkup runs entirely in your browser and nothing is stored."),
                 ("Can I share my results with an appraiser?", "Yes. Take a screenshot or copy your to-do list and bring it to a consultation.")],
    },
    {
        "slug": "roof-snow-load-estimator", "name": "Roof Snow Load Estimator", "icon": "❄", "kind": "Estimator",
        "keyword": "roof snow load calculator",
        "short": "Estimate the weight of fresh snow, settled snow and ice on your roof and compare it with a design load.",
        "title": "Roof Snow Load Calculator | Pennsylvania Winters",
        "desc": "Free roof snow load calculator for Pennsylvania winters: estimate the weight of snow and ice on your roof and compare it with a design load.",
        "h1": "Roof Snow Load Estimator for Pennsylvania Winters",
        "lede": "Lake-effect bands, back-to-back nor’easters and a layer of ice can add tons to a roof. Estimate the load before the next storm and know what to document if something gives.",
        "markup": SNOW,
        "explain": """
<h2>How the estimate works</h2>
<p>Snow weight depends far more on density than depth. This estimator uses rough averages: about 0.5 pounds per square foot (psf) for each inch of fresh, fluffy snow, about 1.5 psf per inch of settled or wet snow and about 4.8 psf per inch of ice. It multiplies the result by the roof’s flat footprint and compares it with the design load you enter.</p>
<div class="note"><b class="h">Illustrative only</b>This is not an engineering calculation. Drifts, valleys, parapets and rowhome roofs that sit lower than a neighbor’s can carry far more than the average. If a roof is sagging, cracking or leaking under snow, get people out and call a professional.</div>
<h2>Why it matters for claims</h2>
<p>Collapse and damage from the weight of ice and snow is a named or covered cause in many Pennsylvania homeowner policies, while gradual leaks and wear are usually excluded. If a storm like the February 2010 snowstorms or Erie’s Christmas 2017 lake-effect event damages your roof, photographs of the snow depth, the date and the damage help separate the covered event from old conditions.</p>
<h2>Related help</h2>
<p>See our <a href="/property-appraisal-services/ice-dam-frozen-pipe-appraisal/">ice dam and frozen pipe claim appraisal</a> service and the guide to <a href="/policy-and-claim-guides/ice-dam-and-frozen-pipe-claims/">ice dam and frozen pipe claims</a>.</p>
""",
        "faqs": [("What design snow load does my roof have?", "It depends on where and when the building was built and the code that applied. A builder, engineer or local code office can tell you; this tool only compares against the number you enter."),
                 ("Should I shovel my own roof?", "Roof snow removal is dangerous. Many owners use a roof rake from the ground or hire insured professionals rather than climbing on an icy roof.")],
    },
]
