"""Interactive claim calculators: markup + explanatory copy. Logic lives in static/assets/js/app.js.
Everything runs in the browser; nothing is stored or sent."""

T = "/free-claim-calculators/"

GAP_FULL = """
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Appraisal payoff calculator</span><i>Runs in your browser</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Insurer’s estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="23600"><span class="hint">Replacement cost total on the insurer’s estimate.</span></div>
        <div><label for="g-own">Your estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="38900"><span class="hint">Your contractor’s or independent estimate.</span></div>
      </div>
      <div><label for="g-land">Where might the award land within the gap?</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% means the insurer’s number holds. 100% means your full number is awarded.</span></div>
      <div class="row2">
        <div><label for="g-ft">Your appraiser’s fee type</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of increase (%)</option></select></div>
        <div><label for="g-fee">Fee amount</label><input id="g-fee" name="fee" inputmode="decimal" value="3000"></div>
      </div>
      <label class="check"><input type="checkbox" name="useump" checked> Include half of an umpire’s fee</label>
      <div><label for="g-ump">Umpire’s total fee (split 50/50)</label><input id="g-ump" name="umpire" inputmode="decimal" value="3600"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated net increase to you</small><b data-o="net">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s1"></span><span class="s2"></span><span class="s3"></span></div>
      <div class="legend"><span><i class="s1"></i>Insurer’s number</span><span><i class="s2"></i>Your net gain</span><span><i class="s3"></i>Appraisal costs</span></div>
      <div class="out-rows">
        <div><span>Amount in dispute</span><b data-o="gap">$0</b></div>
        <div><span>Gap as % of insurer’s estimate</span><b data-o="pct">—</b></div>
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
      <div><label for="m-ins">Insurer’s estimate</label><input id="m-ins" name="insurer" inputmode="decimal" value="23600"></div>
      <div><label for="m-own">Your contractor’s estimate</label><input id="m-own" name="yours" inputmode="decimal" value="38900"></div>
      <div><label for="m-land">Award lands at</label><div class="range"><input id="m-land" type="range" name="land" min="0" max="100" step="5" value="50" data-unit="%"><output>50%</output></div><span class="hint">of the disputed amount</span></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Amount in dispute</small><b data-o="gap">$0</b></div>
      <div class="out-rows">
        <div><span>Gap vs. insurer’s estimate</span><b data-o="pct">—</b></div>
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
  <div class="tool-head"><span>Replacement cost holdback calculator</span><i>Add as many items as you need</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Composition roof (30-year)", 21000, 11, 30), ("Interior paint, main floor", 2800, 5, 10), ("Carpet and pad, bedrooms", 2600, 7, 12)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn ghost small" data-add data-run>+ Add item</button></div>
      <div class="row2">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="1500"></div>
        <div><label for="d-cap">Maximum depreciation</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="90">90%</option></select><span class="hint">Many estimates cap depreciation. Check yours.</span></div>
      </div>
      <label class="check"><input type="checkbox" name="nonrec"> My policy pays actual cash value only (no recoverable depreciation)</label>
    </div>
    <div class="tool-out tool-out-3" aria-live="polite">
      <div class="out-big"><small>First check (ACV − deductible)</small><b data-o="first">$0</b></div>
      <div class="out-big"><small>Held back until repairs</small><b data-o="held">$0</b></div>
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
  <div class="tool-head"><span>Roof pitch &amp; squares calculator</span><i>Compare against your estimate</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <fieldset class="bare"><legend class="sr-only">Measurement method</legend>
        <div class="btn-row">
          <label class="check"><input type="radio" name="mode" value="dims" checked> Footprint length × width</label>
          <label class="check"><input type="radio" name="mode" value="area"> I know the footprint area</label>
        </div></fieldset>
      <div class="row2" data-mode="dims">
        <div><label for="r-l">Footprint length (ft)</label><input id="r-l" name="len" inputmode="decimal" value="52"></div>
        <div><label for="r-w">Footprint width (ft)</label><input id="r-w" name="wid" inputmode="decimal" value="30"></div>
      </div>
      <div data-mode="dims"><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="18"><span class="hint">Deep overhangs are common on Northwest homes.</span></div>
      <div data-mode="area" hidden><label for="r-a">Footprint area incl. overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="2000"></div>
      <div class="row2">
        <div><label for="r-p">Roof pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 8 else "", p) for p in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16]) + """</select></div>
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="10">10%: simple gable</option><option value="12" selected>12%: gable with dormers</option><option value="15">15%: hip roof</option><option value="18">18%: complex or cut-up</option></select></div>
      </div>
      <div><label for="r-pr">Installed price per square (optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 640"><span class="hint">Use a local contractor’s quote for a rough replacement figure.</span></div>
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

DEDUCT = """
<div class="tool" data-tool="deduct">
  <div class="tool-head"><span>Percentage deductible calculator</span><i>Earthquake, wind or hail</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling coverage (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="520000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Percentage deductible</label><select id="w-p" name="pct"><optgroup label="Wind or hail"><option value="1">1%</option><option value="2">2%</option><option value="5">5%</option></optgroup><optgroup label="Earthquake"><option value="10" selected>10%</option><option value="15">15%</option><option value="20">20%</option><option value="25">25%</option></optgroup></select></div>
        <div><label for="w-f">All-other-perils flat deductible</label><input id="w-f" name="flat" inputmode="decimal" value="1000"></div>
      </div>
      <div><label for="w-l">Estimated damage</label><input id="w-l" name="loss" inputmode="decimal" value="68000"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your percentage deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s3"></span><span class="s1"></span></div>
      <div class="legend"><span><i class="s3"></i>You pay</span><span><i class="s1"></i>Policy pays</span></div>
      <div class="out-rows">
        <div><span>Payment with % deductible</span><b data-o="pdpay">$0</b></div>
        <div><span>Payment if the flat deductible applied</span><b data-o="flatpay">$0</b></div>
        <div><span>Extra out-of-pocket from % deductible</span><b data-o="diff">$0</b></div>
      </div>
      <p class="out-msg" data-o="below"></p>
    </div>
  </div>
</div>"""

DATES = """
<div class="tool" data-tool="dates">
  <div class="tool-head"><span>Claim timeline planner</span><i>Exports to your calendar</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
      <p class="hint flush">Adjust each window to match your policy. Defaults are common figures, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="3"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="10"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Often counted from the insurer’s request.</span></div>
        <div><label for="t-r">Depreciation recovery (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="180"></div>
        <div><label for="t-s">Suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="365"><span class="hint">Many Washington homeowner policies use one year.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download .ics calendar file</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the insurer accepted coverage for at least part of the loss?", "Get written confirmation that coverage is accepted. If the claim was denied, talk to a Washington attorney or the OIC before considering appraisal."),
    (3, "Do you have the insurer’s complete, itemized estimate?", "Ask for the full line-item estimate in writing, not just the summary page."),
    (3, "Do you have your own itemized estimate from a contractor or estimator?", "Get an independent, line-item estimate. A lump-sum bid won’t hold up in front of a panel."),
    (2, "Do you have dated photos of the damage taken soon after the loss?", "Gather every photo and note when each was taken. Add new photos of current conditions."),
    (2, "Have you read your policy’s appraisal clause?", "Find the Appraisal paragraph in the policy conditions and note any deadlines."),
    (2, "Do you know your policy’s suit-limitation date?", "Find the Suit Against Us clause and calendar the date. Our timeline planner can help."),
    (2, "Have temporary repairs been made and receipts saved?", "Make reasonable temporary repairs and keep every receipt."),
    (1, "Do you have your current declarations page?", "Download or request your current declarations page."),
    (2, "Has hidden damage been opened up and documented?", "Make sure wet walls, attics, crawl spaces and roof decking have been inspected so the scope is complete."),
    (1, "Is your correspondence with the insurer organized by date?", "Collect emails, letters and claim notes in date order."),
    (2, "Is the gap between estimates more than about 10% or $5,000?", "Run the numbers in our appraisal payoff calculator. A small gap may not justify appraisal costs."),
    (1, "Has a sworn proof of loss been sent if the insurer asked for one?", "If a proof of loss was requested, send it on time."),
]

READY = """
<div class="tool tool-wide" data-tool="ready">
  <div class="tool-head"><span>Appraisal readiness quiz</span><i>12 questions · about two minutes</i></div>
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
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#e3efe9" stroke-width="18"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#008457" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3" style="transition:stroke-dashoffset .5s,stroke .3s"/></svg>
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

FIRE = """
<div class="tool tool-wide" data-tool="fire">
  <div class="tool-head"><span>Wildfire total-loss coverage check</span><i>Rebuild cost vs. your limits</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="f-sf">Home size (finished sq ft)</label><input id="f-sf" name="sqft" inputmode="decimal" value="2200"></div>
        <div><label for="f-ps">Rebuild cost per sq ft ($)</label><input id="f-ps" name="psf" inputmode="decimal" value="325"><span class="hint">Ask a local builder. Post-fire demand can push this up.</span></div>
      </div>
      <div class="row2">
        <div><label for="f-cu">Code upgrades (% of rebuild)</label><input id="f-cu" name="code" inputmode="decimal" value="10"></div>
        <div><label for="f-db">Debris removal &amp; site prep ($)</label><input id="f-db" name="debris" inputmode="decimal" value="35000"></div>
      </div>
      <div class="row2">
        <div><label for="f-a">Dwelling limit (Coverage A)</label><input id="f-a" name="cova" inputmode="decimal" value="560000"></div>
        <div><label for="f-er">Extended replacement cost</label><select id="f-er" name="erc"><option value="0">None</option><option value="10">10%</option><option value="20">20%</option><option value="25" selected>25%</option><option value="50">50%</option></select></div>
      </div>
      <div class="row2">
        <div><label for="f-ol">Ordinance or law coverage</label><select id="f-ol" name="ol"><option value="0">None</option><option value="10" selected>10% of Coverage A</option><option value="25">25% of Coverage A</option></select></div>
        <div><label for="f-cp">Contents limit (% of Coverage A)</label><input id="f-cp" name="cpct" inputmode="decimal" value="50"></div>
      </div>
      <div><label for="f-ce">Your estimate of contents value ($)</label><input id="f-ce" name="contents" inputmode="decimal" value="260000"></div>
    </div>
    <div class="tool-out tool-out-3" aria-live="polite">
      <div class="out-big"><small>Estimated cost to rebuild</small><b data-o="need">$0</b></div>
      <div class="out-big"><small>Dwelling coverage available</small><b data-o="have">$0</b></div>
      <div class="out-big"><small data-o="gaplabel">Shortfall</small><b data-o="short">$0</b></div>
      <div class="out-rows span-all">
        <div><span>Base rebuild (size × cost)</span><b data-o="base">$0</b></div>
        <div><span>Code upgrades</span><b data-o="codeamt">$0</b></div>
        <div><span>Debris removal &amp; site prep</span><b data-o="deb">$0</b></div>
        <div><span>Coverage A + extended replacement</span><b data-o="aext">$0</b></div>
        <div><span>Ordinance or law amount</span><b data-o="olamt">$0</b></div>
        <div><span>Contents limit / gap</span><b data-o="cgap">$0</b></div>
      </div>
      <p class="out-msg span-all" data-o="firemsg"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "appraisal-payoff-calculator", "name": "Appraisal Payoff Calculator", "kind": "Calculator", "photo": "calculator-paperwork",
        "short": "See the disputed amount, a projected award and what you’d keep after appraiser and umpire fees.",
        "title": "Appraisal Payoff Calculator | Is Appraisal Worth It?",
        "desc": "Free appraisal payoff calculator: compare your estimate with the insurer’s, project an award and subtract fees to see what you would net.",
        "h1": "Appraisal Payoff Calculator: Will Appraisal Pay Off for You?",
        "lede": "Enter the insurer’s estimate and yours, choose where an award might land, and add realistic fees. The calculator shows whether appraisal is likely to leave you better off.",
        "markup": GAP_FULL,
        "explain": f"""
<h2>How to use it</h2>
<ol><li><strong>Enter the insurer’s RCV total</strong>, the replacement cost before depreciation and deductible.</li>
<li><strong>Enter your estimate</strong> from a contractor or independent estimator, also at RCV.</li>
<li><strong>Move the slider</strong> to test outcomes. Try 30%, 50% and 80% to see a range instead of one answer.</li>
<li><strong>Add fees</strong> using your appraiser’s quoted arrangement and a realistic umpire fee.</li></ol>
<h2>Why test a range</h2>
<p>Awards rarely match either side’s opening number. Well-documented items tend to hold and unsupported ones tend to fall. If appraisal only pays off at 90% or 100%, the case is fragile. If it still works at 40%, it’s more likely worth pursuing.</p>
<h2>What it leaves out</h2>
<p>The calculator doesn’t account for depreciation timing, limits or deductibles, which affect what you’re paid but not the size of the dispute. For holdback math, use the <a href="{T}replacement-cost-holdback-calculator/">replacement cost holdback calculator</a>.</p>
<p class="hint">Example figures loaded in the calculator are illustrative only.</p>
""",
        "faqs": [("Is the projected award a guarantee?", "No. It’s a planning scenario. Real awards depend on documentation, the panel and the policy."), ("What’s a typical umpire fee?", "It varies with the size and complexity of the claim. The appraisers can get a quote once an umpire is proposed, and the cost is usually split evenly.")],
    },
    {
        "slug": "replacement-cost-holdback-calculator", "name": "Replacement Cost Holdback Calculator", "kind": "Calculator", "photo": "calculator-desk",
        "short": "Estimate your first ACV check, the depreciation held back and the total once repairs are done.",
        "title": "RCV vs ACV Holdback Calculator | Depreciation Recovery",
        "desc": "List damaged items with age and life expectancy to estimate your first ACV check, the depreciation held back and your total after repairs.",
        "h1": "Replacement Cost Holdback Calculator (RCV vs. ACV)",
        "lede": "Replacement cost policies usually pay in two parts: an actual cash value check now and recoverable depreciation after repairs. Enter your items to see how the money splits.",
        "markup": DEP,
        "explain": f"""
<h2>How depreciation is estimated here</h2>
<p>The calculator uses straight-line depreciation, age divided by expected life, capped at the maximum you choose. Real estimates may adjust for condition, use different life expectancies or treat some items as non-depreciable, so treat the result as a planning figure.</p>
<h2>Typical life expectancies</h2>
<div class="table-wrap"><table><thead><tr><th>Item</th><th>Common range</th></tr></thead><tbody>
<tr><th>Composition shingles (30-year)</th><td>25–30 years</td></tr><tr><th>Cedar shake roofing</th><td>20–30 years</td></tr><tr><th>Interior paint</th><td>8–12 years</td></tr><tr><th>Carpet</th><td>8–12 years</td></tr><tr><th>Fiber cement siding</th><td>30–50 years</td></tr><tr><th>Water heater</th><td>10–15 years</td></tr>
</tbody></table></div>
<h2>Getting holdback released</h2>
<p>Most policies pay recoverable depreciation once repairs are finished within a time limit. Send invoices and photos of the completed work. The <a href="{T}claim-timeline-planner/">claim timeline planner</a> can remind you before the window closes.</p>
""",
        "faqs": [("Should labor be depreciated?", "Practice varies by insurer and policy wording. If your estimate depreciates labor, ask the insurer to explain its approach in writing."), ("What if I don’t repair?", "Under most replacement cost policies, you keep the ACV payment but may not recover the held-back depreciation.")],
    },
    {
        "slug": "roof-pitch-squares-calculator", "name": "Roof Pitch & Squares Calculator", "kind": "Calculator", "photo": "roof-shingles",
        "short": "Turn a footprint into true roof squares using pitch and waste, then check the insurer’s figures.",
        "title": "Roof Pitch & Squares Calculator for Insurance Claims",
        "desc": "Work out roof squares from footprint, pitch and waste, then check the true surface area and steep charges against your insurance estimate.",
        "h1": "Roof Pitch and Squares Calculator for Insurance Claims",
        "lede": "Measurement errors are a common reason roof claims come up short. Use your home’s footprint, overhang and pitch to estimate true roof area, squares and bundles.",
        "markup": ROOF,
        "explain": """
<h2>How the math works</h2>
<p>A roof’s surface is larger than the footprint below it, and the steeper the pitch the bigger the difference. The pitch multiplier is √(1 + (rise ÷ 12)²). An 8/12 roof is about 20% larger than its footprint. A 12/12 roof is about 41% larger.</p>
<h2>Northwest roofs</h2>
<p>Many Washington homes have deep eave overhangs to shed rain and steeper pitches to handle snow, especially in the Cascade foothills and Spokane. Both add area that a quick estimate can miss.</p>
<h2>Checking your estimate</h2>
<ul><li>Find the roof section of the insurer’s estimate and note total squares and the waste percentage.</li>
<li>Compare those figures with the result here. Differences over 5% to 10% deserve a closer look.</li>
<li>Check for steep charges, often from 7/12 up, and high-roof charges on two-story sections.</li>
<li>Confirm ridge cap, starter, drip edge and valley materials are listed separately.</li></ul>
<h2>Limits of a footprint calculation</h2>
<p>Complex roofs with several pitches, dormers and valleys need measuring plane by plane. An aerial measurement report or field measurement will always beat a footprint estimate. Use this as a check.</p>
""",
        "faqs": [("What’s a square?", "100 square feet of roof surface. A typical two-story Washington home might have 22 to 40 squares."), ("Why does waste change with roof type?", "Hips, valleys and dormers need more cutting, so more material ends up as scrap.")],
    },
    {
        "slug": "percentage-deductible-calculator", "name": "Percentage Deductible Calculator", "kind": "Calculator", "photo": "seattle-skyline",
        "short": "Turn a percentage earthquake, wind or hail deductible into dollars and see what a claim would pay.",
        "title": "Earthquake & Percentage Deductible Calculator | WA",
        "desc": "Turn a percentage earthquake, wind or hail deductible into dollars and compare what your policy would pay with a flat deductible.",
        "h1": "Percentage Deductible Calculator for Earthquake, Wind and Hail",
        "lede": "A 10% earthquake deductible sounds abstract until you multiply it by your dwelling limit. See your deductible in dollars and how it changes what a claim pays.",
        "markup": DEDUCT,
        "explain": """
<h2>Why Washington owners should check this</h2>
<p>Earthquake coverage in Washington is usually bought separately or by endorsement, and it almost always carries a percentage deductible, often 10% to 20% of the dwelling limit. Some policies also use a percentage deductible for wind or hail. On a $520,000 dwelling limit, a 10% deductible is $52,000.</p>
<h2>Where to find yours</h2>
<p>Look on the declarations page and in any earthquake endorsement. Check whether the deductible applies separately to the dwelling, other structures and contents, or to the loss as a whole.</p>
<h2>How it affects appraisal</h2>
<p>A deductible doesn’t change the amount of loss a panel decides, but it changes what you receive. A loss just above the deductible may not be worth disputing. One well above it may be.</p>
<p class="hint">Example figures loaded in the calculator are illustrative only.</p>
""",
        "faqs": [("Does the earthquake deductible apply to contents too?", "Some endorsements apply separate deductibles to each coverage; others apply one to the whole loss. Read the endorsement carefully."), ("Can I lower my deductible?", "Usually at renewal, if the insurer offers it. A lower deductible raises the premium.")],
    },
    {
        "slug": "claim-timeline-planner", "name": "Claim Timeline Planner", "kind": "Planner", "photo": "clipboard-inspection",
        "short": "Map notice, proof of loss, depreciation and suit-limitation dates from your date of loss, then export them.",
        "title": "Claim Timeline Planner | Washington Policy Deadlines",
        "desc": "Map proof-of-loss, depreciation and suit-limitation dates for a Washington property claim from your date of loss, then export a calendar file.",
        "h1": "Washington Property Claim Timeline Planner",
        "lede": "Policy deadlines keep running while you argue about a number. Enter your date of loss and your policy’s windows to build a timeline you can add to your calendar.",
        "markup": DATES,
        "explain": """
<h2>The deadlines that matter most</h2>
<ul><li><strong>Prompt notice.</strong> Policies require you to report losses promptly. Late notice is a common defense.</li>
<li><strong>Proof of loss.</strong> If the insurer asks for a sworn proof of loss, many policies give 60 days to send it.</li>
<li><strong>Depreciation recovery.</strong> Replacement cost policies often require repairs within a set period to collect holdback.</li>
<li><strong>Suit limitation.</strong> Washington law doesn’t allow policies to set less than one year to sue, and many homeowner policies use exactly one year. Appraisal may not pause that clock.</li></ul>
<div class="note"><b class="h">Important</b>This planner uses the numbers you enter. It isn’t legal advice, and courts can read policy deadlines differently. If a deadline is close, contact a Washington attorney.</div>
""",
        "faqs": [("Is the date of loss the day I noticed the damage?", "Usually it’s the date of the storm or event. Weather records for your address can help pin it down."), ("Does demanding appraisal extend my suit deadline?", "Not automatically. Some policies or written agreements address it, but many don’t. Protect the deadline separately.")],
    },
    {
        "slug": "appraisal-readiness-quiz", "name": "Appraisal Readiness Quiz", "kind": "Checklist", "photo": "consultation-table",
        "short": "Answer 12 yes-or-no questions to score your claim file and get a to-do list before you demand appraisal.",
        "title": "Appraisal Readiness Quiz | Is Your Claim File Ready?",
        "desc": "Twelve quick questions that score how ready your property claim is for insurance appraisal, plus a personal to-do list of what to finish first.",
        "h1": "Appraisal Readiness Quiz: Is Your Claim File Ready?",
        "lede": "Strong appraisals are built before they start, with a complete file. Answer twelve quick questions to see where yours stands and what to fix first.",
        "markup": READY,
        "explain": """
<h2>How the score is weighted</h2>
<p>Questions about coverage, estimates and evidence carry the most weight because they decide whether appraisal is the right tool and how well your number will hold up. Paperwork items matter too, but they’re easier to fix.</p>
<h2>What your result means</h2>
<ul><li><strong>75 and above:</strong> your file is in good shape. A professional review of the gap is the logical next step.</li>
<li><strong>45 to 74:</strong> close the open items first. Each one strengthens your position.</li>
<li><strong>Below 45:</strong> demanding appraisal now could lock in a low number. Build the file first.</li></ul>
""",
        "faqs": [("Is my information saved or sent anywhere?", "No. The quiz runs entirely in your browser and nothing is stored."), ("Can I share my result with an appraiser?", "Yes. Take a screenshot or note your to-do list and bring it to your consultation.")],
    },
    {
        "slug": "wildfire-total-loss-coverage-check", "name": "Wildfire Total-Loss Coverage Check", "kind": "Calculator", "photo": "wildfire-hillside",
        "short": "Compare the real cost to rebuild after a wildfire with your dwelling, code and contents limits.",
        "title": "Wildfire Total-Loss Coverage Check | Rebuild vs. Limits",
        "desc": "A free wildfire coverage check for Washington homes: compare rebuild, code and debris costs with your dwelling, extended and contents limits.",
        "h1": "Wildfire Total-Loss Coverage Check for Washington Homes",
        "lede": "After a wildfire total loss, the first question is often whether your limits will rebuild the house. Enter your numbers to compare rebuild costs with the coverage on your declarations page.",
        "markup": FIRE,
        "explain": """
<h2>How the check works</h2>
<p>It adds the base rebuild cost (size times cost per square foot), code upgrades and debris removal. It compares that total with your dwelling limit plus any extended replacement cost, plus ordinance or law coverage. It also compares your contents estimate with your contents limit.</p>
<h2>Why limits fall short</h2>
<ul><li>Limits set years ago may not reflect current construction costs.</li>
<li>After a large wildfire, demand for builders and materials can push prices up across a region.</li>
<li>Current energy and building codes add cost when a home is rebuilt from the ground up.</li>
<li>Debris removal after a fire can be expensive and may have its own limit.</li></ul>
<h2>Policies differ</h2>
<p>Some policies pay debris removal within the dwelling limit, some add a percentage on top, and some have a separate limit. Extended replacement cost and ordinance or law coverage vary too. Use your own policy’s terms.</p>
<div class="note"><b class="h">If there’s a shortfall</b>A shortfall caused by your limits is a coverage issue, not something appraisal can change. If you think limits were set improperly, the OIC’s consumer advocates or a Washington attorney can help. If the insurer’s rebuild estimate is too low, an estimate review or appraisal may help.</div>
<p class="hint">Example figures loaded in the calculator are illustrative only.</p>
""",
        "faqs": [("Where do I find a realistic cost per square foot?", "Ask local builders who rebuild after fires. Online averages may not reflect your area or post-fire demand."), ("Does this tool account for land value?", "No. Homeowner policies insure the structure and contents, not the land. Leave land value out of your estimate.")],
    },
]
