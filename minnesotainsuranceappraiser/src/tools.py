"""Free claim tools for Minnesota Insurance Appraiser: widget markup + explanatory copy.
All logic runs in the browser (static/assets/js/app.js). Nothing is stored or sent."""

GAP_FULL = """
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Claim gap &amp; fee estimator</span><i>Runs in your browser</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Carrier’s estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="21600"><span class="hint">Replacement cost total on the insurer’s estimate.</span></div>
        <div><label for="g-own">Your estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="34900"><span class="hint">Your contractor’s or independent estimate.</span></div>
      </div>
      <div><label for="g-land">Where in the gap might the award land?</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% = the carrier’s number stands. 100% = your full number is awarded.</span></div>
      <div class="row2">
        <div><label for="g-ft">How your appraiser charges</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of the increase (%)</option></select></div>
        <div><label for="g-fee">Fee amount</label><input id="g-fee" name="fee" inputmode="decimal" value="2800"></div>
      </div>
      <label class="check"><input type="checkbox" name="useump" checked> Add my half of an umpire’s fee</label>
      <div><label for="g-ump">Umpire’s total fee</label><input id="g-ump" name="umpire" inputmode="decimal" value="3200"><span class="hint">Usually split 50/50 between you and the insurer.</span></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated net gain after fees</small><b data-o="net">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s-base"></span><span class="s-gain"></span><span class="s-cost"></span></div>
      <div class="legend"><span><i class="s-base"></i>Carrier’s number</span><span><i class="s-gain"></i>Your net gain</span><span><i class="s-cost"></i>Appraisal costs</span></div>
      <div class="out-rows">
        <div><span>Amount in dispute</span><b data-o="gap">$0</b></div>
        <div><span>Gap vs. carrier estimate</span><b data-o="pct">—</b></div>
        <div><span>Projected award (RCV)</span><b data-o="award">$0</b></div>
        <div><span>Gross increase</span><b data-o="gain">$0</b></div>
        <div><span>Your appraisal costs</span><b data-o="cost">$0</b></div>
        <div><span>Break-even point in the gap</span><b data-o="breakeven">—</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

GAP_MINI = """
<div class="tool" data-tool="gap" style="margin:0">
  <div class="tool-head"><span>60-second gap check</span><i>No sign-up</i></div>
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
  <div class="tool-head"><span>RCV / ACV &amp; holdback calculator</span><i>Add a row for each item</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Asphalt shingle roof", 16400, 11, 25), ("Steel siding — two elevations", 7300, 18, 40), ("Gutters &amp; downspouts", 1650, 11, 20)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn ghost small" data-add data-run>+ Add item</button></div>
      <div class="row2">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="2500"></div>
        <div><label for="d-cap">Depreciation cap</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="90">90%</option></select><span class="hint">Many estimates cap depreciation on an item. Check yours.</span></div>
      </div>
      <label class="check"><input type="checkbox" name="nonrec"> My policy (or this item) pays actual cash value only</label>
    </div>
    <div class="tool-out wide-out" aria-live="polite">
      <div class="out-big"><small>First payment (ACV − deductible)</small><b data-o="first">$0</b></div>
      <div class="out-big"><small>Held back until repairs</small><b data-o="held">$0</b></div>
      <div class="out-big"><small>Total if fully recovered</small><b data-o="total">$0</b></div>
      <div class="out-rows span-all">
        <div><span>Replacement cost value (RCV)</span><b data-o="rcv">$0</b></div>
        <div><span>Total depreciation</span><b data-o="dep">$0</b></div>
        <div><span>Depreciation as share of RCV</span><b data-o="deppct">0%</b></div>
        <div><span>Actual cash value (ACV)</span><b data-o="acv">$0</b></div>
      </div>
    </div>
  </div>
</div>"""

ROOF = """
<div class="tool" data-tool="roof">
  <div class="tool-head"><span>Roof area &amp; pitch calculator</span><i>Check the squares on your estimate</i></div>
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
      <div data-mode="dims"><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="16"></div>
      <div data-mode="area" hidden><label for="r-a">Footprint area incl. overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="1900"></div>
      <div class="row2">
        <div><label for="r-p">Roof pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 7 else "", p) for p in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16]) + """</select></div>
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="10">10% — simple gable</option><option value="12" selected>12% — gable with dormers</option><option value="15">15% — hip roof</option><option value="18">18% — cut-up / complex</option></select></div>
      </div>
      <div><label for="r-pr">Installed price per square (optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 560"><span class="hint">Use a local contractor’s quote for a rough figure.</span></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Roof squares (before waste)</small><b data-o="sq">0</b></div>
      <div class="out-rows">
        <div><span>Pitch multiplier</span><b data-o="mult">1.000</b></div>
        <div><span>Roof surface area</span><b data-o="surface">0</b></div>
        <div><span>Squares with waste</span><b data-o="order">0</b></div>
        <div><span>Shingle bundles (3 per square)</span><b data-o="bundles">0</b></div>
        <div><span>Rough replacement cost</span><b data-o="cost">—</b></div>
      </div>
      <p class="out-msg" data-o="steep"></p>
    </div>
  </div>
</div>"""

DEDUCT = """
<div class="tool" data-tool="deduct">
  <div class="tool-head"><span>Percentage deductible calculator</span><i>Percent vs. flat dollar</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling coverage (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="410000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Wind/hail percentage deductible</label><select id="w-p" name="pct"><option value="0.5">0.5%</option><option value="1" selected>1%</option><option value="2">2%</option><option value="3">3%</option><option value="5">5%</option></select></div>
        <div><label for="w-f">Flat deductible for comparison</label><input id="w-f" name="flat" inputmode="decimal" value="1500"></div>
      </div>
      <div><label for="w-l">Estimated hail or wind damage</label><input id="w-l" name="loss" inputmode="decimal" value="18700"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your percentage deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s-cost"></span><span class="s-base"></span></div>
      <div class="legend"><span><i class="s-cost"></i>You pay</span><span><i class="s-base"></i>Policy pays</span></div>
      <div class="out-rows">
        <div><span>Claim payment with % deductible</span><b data-o="pdpay">$0</b></div>
        <div><span>Payment if the flat deductible applied</span><b data-o="flatpay">$0</b></div>
        <div><span>Extra out-of-pocket from the % deductible</span><b data-o="diff">$0</b></div>
      </div>
      <p class="out-msg" data-o="below"></p>
    </div>
  </div>
</div>"""

DATES = """
<div class="tool" data-tool="dates">
  <div class="tool-head"><span>Claim timeline planner</span><i>Exports an .ics calendar file</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
      <p class="hint flush">Set each window to match your policy and the carrier’s letters. Defaults are common planning figures, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report the claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="2"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="10"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Often counted from the insurer’s request.</span></div>
        <div><label for="t-r">Replacement-cost repair window (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="180"><span class="hint">Policies vary widely. Check yours.</span></div>
        <div><label for="t-s">Suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="730"><span class="hint">Two years = 730 days.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download .ics calendar file</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the insurer accepted coverage for at least part of the loss?", "Get written confirmation that coverage is accepted. If the claim was denied outright, talk with a Minnesota attorney before thinking about appraisal."),
    (3, "Do you have the insurer’s complete, line-item estimate?", "Ask the adjuster in writing for the full itemized estimate, not just the payment summary."),
    (3, "Do you have your own itemized estimate?", "Get a line-item estimate from a contractor or estimator. A one-line bid is hard to defend before a panel."),
    (2, "Do you have dated photos from soon after the loss?", "Collect every photo and note when each was taken. Photograph current conditions too, including attic and interior stains."),
    (2, "Have you read the appraisal paragraph in your policy?", "Find ‘Appraisal’ in the policy conditions and note any notice, timing or selection requirements."),
    (2, "Do you know your suit-limitation date?", "Find the ‘Suit Against Us’ condition and put the date on your calendar. The timeline planner can export it."),
    (2, "Were temporary repairs made, with receipts kept?", "Tarp, dry out and protect the property, and keep every invoice and receipt."),
    (2, "Has hidden damage been opened up and documented?", "Make sure wet insulation, ceilings, decking and wall cavities were inspected so the scope is complete."),
    (1, "Do you have your current declarations page?", "Download or request the declarations page showing limits and deductibles."),
    (1, "Is your correspondence organized by date?", "Put emails, letters and claim notes in date order in one folder."),
    (2, "Is the gap more than roughly 10% or several thousand dollars?", "Run the claim gap & fee estimator. A small gap may not justify appraisal costs."),
    (1, "If the insurer asked for a sworn proof of loss, was it sent on time?", "If a proof of loss was requested, complete and return it within the stated time."),
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
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#e3eef6" stroke-width="18"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#52c9e8" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3" style="transition:stroke-dashoffset .5s,stroke .3s"/></svg>
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

SNOW = """
<div class="tool" data-tool="snow">
  <div class="tool-head"><span>Roof snow load calculator</span><i>Pounds per square foot</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="s-d">Snow depth on the roof (inches)</label><input id="s-d" name="depth" inputmode="decimal" value="22"></div>
        <div><label for="s-t">Type of snow</label><select id="s-t" name="dens"><option value="7">Fresh, light powder (~7 lb/ft³)</option><option value="15" selected>Settled snow (~15 lb/ft³)</option><option value="25">Wet or packed snow (~25 lb/ft³)</option></select></div>
      </div>
      <div class="row2">
        <div><label for="s-i">Ice layer thickness (inches)</label><input id="s-i" name="ice" inputmode="decimal" value="1"><span class="hint">Ice weighs about 57 lb/ft³.</span></div>
        <div><label for="s-a">Roof area (sq ft, optional)</label><input id="s-a" name="area" inputmode="decimal" value="1800"></div>
      </div>
      <div><label for="s-r">Reference roof snow load (psf)</label><select id="s-r" name="ref"><option value="20">20 psf</option><option value="30">30 psf</option><option value="35" selected>35 psf</option><option value="40">40 psf</option><option value="50">50 psf</option></select><span class="hint">Use the design load from your building’s plans or a structural engineer if you have it. These options are examples only.</span></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated roof load</small><b data-o="psf">0 psf</b></div>
      <div class="meter" aria-hidden="true"><span data-o="bar"></span></div>
      <div class="out-rows">
        <div><span>Snow layer</span><b data-o="snowpsf">0 psf</b></div>
        <div><span>Ice layer</span><b data-o="icepsf">0 psf</b></div>
        <div><span>Share of reference load</span><b data-o="share">0%</b></div>
        <div><span>Total weight on the roof</span><b data-o="total">—</b></div>
      </div>
      <p class="out-msg" data-o="advice"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "claim-gap-fee-estimator", "name": "Claim Gap & Fee Estimator", "icon": "Δ", "kind": "Calculator",
        "keyword": "insurance appraisal cost calculator",
        "short": "Find the disputed amount, a projected award, your fees and the break-even point before you invoke appraisal.",
        "title": "Insurance Appraisal Cost Calculator | Gap & Fee Estimator",
        "desc": "Free insurance appraisal cost calculator: compare estimates, project an award, subtract appraiser and umpire fees and find your break-even point.",
        "h1": "Claim Gap & Fee Estimator: An Insurance Appraisal Cost Calculator",
        "lede": "Enter the carrier’s number and yours, pick where an award might land, and add realistic fees. You’ll see the net result and how far into the gap the award must land just to cover costs.",
        "markup": GAP_FULL,
        "explain": """
<h2>What this insurance appraisal cost calculator answers</h2>
<p>Appraisal is not free, and it is not a guaranteed win. The useful question is narrower: <strong>if a panel lands somewhere between the two estimates, will the increase outweigh what you pay to get there?</strong> This insurance appraisal cost calculator puts that question in dollars.</p>
<h2>How the math works</h2>
<ul>
<li><strong>Amount in dispute</strong> = your estimate − the carrier’s estimate.</li>
<li><strong>Projected award</strong> = carrier’s estimate + (dispute × the share you choose on the slider).</li>
<li><strong>Your costs</strong> = your appraiser’s flat fee, or a percentage of the increase, plus half of the umpire’s fee if you include one.</li>
<li><strong>Break-even point</strong> = the share of the gap the award must reach before your costs are covered.</li>
</ul>
<h2>Reading the result</h2>
<p>If the break-even point sits above roughly half the gap, appraisal is a close call and a documented supplement may be the better first move. If it sits low, the dispute is large relative to cost. Either way, the slider is a guess, not a forecast. Panels decide line by line, and a well-supported estimate tends to hold more of its value than an inflated one.</p>
<p>All figures you enter stay in your browser. The default numbers are illustrative.</p>
""",
        "faqs": [
            ("Why does the umpire fee matter?", "Many Minnesota appraisals settle between the two appraisers. When they don’t, an umpire is paid, and most policies split that cost equally. Including it shows a more cautious net figure."),
            ("Is a percentage fee better than a flat fee?", "Neither is automatically better. A percentage fee rises with the increase, while a flat fee is predictable. Compare both here using your own figures and the written fee agreement."),
            ("Does the estimator account for depreciation or the deductible?", "No. It compares replacement cost totals. Use the RCV / ACV & holdback calculator to see how payments are split once an amount is set."),
        ],
    },
    {
        "slug": "rcv-acv-holdback-calculator", "name": "RCV / ACV & Holdback Calculator", "icon": "ACV", "kind": "Calculator",
        "keyword": "RCV ACV calculator",
        "short": "Itemize your loss to see depreciation, the first check and the recoverable holdback after repairs.",
        "title": "RCV ACV Calculator | Depreciation & Holdback, Item by Item",
        "desc": "Free RCV ACV calculator: list items with age and life to see depreciation, your first payment and the holdback you can recover after repairs.",
        "h1": "RCV / ACV & Holdback Calculator for Property Claims",
        "lede": "Most replacement-cost policies pay in two steps: actual cash value first, then the withheld depreciation once repairs are done. This RCV ACV calculator shows both numbers item by item.",
        "markup": DEP,
        "explain": """
<h2>Why the first check looks low</h2>
<p>On a replacement cost policy, the insurer usually pays <strong>actual cash value</strong> first: replacement cost minus depreciation, minus your deductible. The depreciation is held back until you repair or replace, subject to the policy’s conditions and time limits. That holdback can be a large share of a roof or siding claim.</p>
<h2>How this RCV ACV calculator estimates depreciation</h2>
<p>Each row uses straight-line depreciation: age ÷ expected life × replacement cost, limited by the cap you choose. Real estimates may depreciate labor differently, use condition adjustments or apply no depreciation to some items. Treat the result as a way to check whether the carrier’s depreciation looks reasonable, not as the final figure.</p>
<h2>Questions worth asking about depreciation</h2>
<ul>
<li>Is depreciation applied to labor as well as materials, and does your policy allow it?</li>
<li>Does the life used for a 30-year architectural shingle match the product?</li>
<li>Is the age based on records, or an adjuster’s guess?</li>
<li>Does the policy require repairs within a set period to recover the holdback?</li>
</ul>
<p>Tick “actual cash value only” for older roofs or items your policy settles on ACV. Example values are illustrative.</p>
""",
        "faqs": [
            ("What is recoverable depreciation?", "It is the part of the replacement cost withheld from the first payment that the insurer pays after repairs are completed, if the policy provides replacement cost coverage."),
            ("Can depreciation be disputed in appraisal?", "Often yes, as part of the amount of loss, depending on the policy wording. Age, condition and expected life are common disagreement points."),
            ("Why is there a depreciation cap?", "Many estimates limit how much an item can be depreciated so it never drops to zero. The right cap depends on the estimate and the policy."),
        ],
    },
    {
        "slug": "roof-area-pitch-calculator", "name": "Roof Area & Pitch Calculator", "icon": "▲", "kind": "Calculator",
        "keyword": "roof squares calculator",
        "short": "Turn a footprint and pitch into roof squares, waste and bundles to check the measurements on your estimate.",
        "title": "Roof Squares Calculator | Area, Pitch & Waste for Claims",
        "desc": "Free roof squares calculator for hail and wind claims: convert footprint and pitch into surface area, squares with waste and shingle bundles.",
        "h1": "Roof Area & Pitch Calculator: A Roof Squares Calculator for Claims",
        "lede": "Roof measurements drive most of a hail claim’s value. Use this roof squares calculator to sanity-check the area, pitch and waste on the insurer’s estimate before you accept it.",
        "markup": ROOF,
        "explain": """
<h2>Why measurements move the number</h2>
<p>A roof estimate is priced per square (100 square feet). If the carrier’s estimate is short by a few squares, every line tied to area — tear-off, felt, ice and water shield, shingles, disposal — is short too. On steeper roofs, a missed steep charge can add up quickly.</p>
<h2>How this roof squares calculator works</h2>
<ul>
<li><strong>Footprint</strong>: length × width plus the overhang on each side, or an area you already have.</li>
<li><strong>Pitch multiplier</strong>: √(1 + (rise ÷ 12)²). A 7/12 roof has about 15% more surface than its footprint.</li>
<li><strong>Waste</strong>: extra material for cuts at hips, valleys and dormers. Complex roofs need more.</li>
</ul>
<h2>Minnesota details to compare</h2>
<p>Minnesota estimates usually include ice and water shield along the eaves, and many older homes have more than one layer of shingles to remove. Check whether your estimate includes additional layers, drip edge and steep or high-roof charges where they apply.</p>
<p>This tool can’t replace a field measurement or aerial report, but it can flag a large mismatch worth questioning. Default dimensions are illustrative.</p>
""",
        "faqs": [
            ("What is a roofing square?", "A square is 100 square feet of roof surface. Estimates price shingles, underlayment and labor per square."),
            ("Why doesn’t my footprint match the roof area?", "Sloped roofs have more surface than the ground area they cover. The pitch multiplier accounts for that, and overhangs add more."),
            ("What waste factor do insurers use?", "It varies by roof complexity and estimating practice. Simple gables often use around 10%, while hips and cut-up roofs use more."),
        ],
    },
    {
        "slug": "percentage-deductible-calculator", "name": "Percentage Deductible Calculator", "icon": "%", "kind": "Calculator",
        "keyword": "percentage deductible calculator",
        "short": "Convert a wind/hail percentage deductible into dollars and compare it with a flat deductible.",
        "title": "Percentage Deductible Calculator | Wind & Hail in Dollars",
        "desc": "Free percentage deductible calculator: turn a 1% or 2% wind/hail deductible into dollars and compare your claim payment with a flat deductible.",
        "h1": "Percentage Deductible Calculator for Wind & Hail Claims",
        "lede": "A 1% deductible sounds small until it’s multiplied by your dwelling limit. This percentage deductible calculator shows the real dollar amount and what it does to your payment.",
        "markup": DEDUCT,
        "explain": """
<h2>How percentage deductibles work</h2>
<p>Some Minnesota homeowner policies apply a separate wind/hail deductible written as a percentage of Coverage A (dwelling). On a $410,000 dwelling limit, a 1% deductible is $4,100 — compared with a flat deductible that might be $1,000 or $1,500. The percentage deductible usually applies to the whole storm claim, not each item.</p>
<h2>What this percentage deductible calculator shows</h2>
<ul>
<li>Your percentage deductible in dollars.</li>
<li>The claim payment after that deductible.</li>
<li>What the payment would be if the flat deductible applied instead.</li>
<li>Whether the loss falls entirely within the deductible.</li>
</ul>
<h2>Why it matters before appraisal</h2>
<p>Appraisal sets the amount of loss; the deductible comes off afterward. If the loss is close to the deductible, even a successful appraisal may change little. If the loss is well above it, every dollar recovered through appraisal reaches you.</p>
<p>Check your declarations page for the exact deductible and whether it applies to wind, hail or both. Figures shown are illustrative.</p>
""",
        "faqs": [
            ("Where do I find my wind/hail deductible?", "On the declarations page. It may be listed as a percentage, a dollar amount or both, sometimes as a separate line for wind and hail."),
            ("Is the percentage based on the claim amount?", "Usually not. It is normally a percentage of the dwelling coverage limit. Read your policy to confirm."),
            ("Does appraisal change the deductible?", "No. Appraisal decides the amount of loss. The deductible is applied under the policy terms after that amount is set."),
        ],
    },
    {
        "slug": "claim-timeline-planner", "name": "Claim Timeline Planner", "icon": "◷", "kind": "Planner",
        "keyword": "insurance claim deadline calculator",
        "short": "Map notice, proof of loss, repair and suit-limitation dates from your date of loss, then export to your calendar.",
        "title": "Insurance Claim Deadline Calculator | Timeline + .ics Export",
        "desc": "Free insurance claim deadline calculator: enter your date of loss to map key claim milestones and download them as an .ics calendar file.",
        "h1": "Claim Timeline Planner: An Insurance Claim Deadline Calculator",
        "lede": "Policies run on deadlines, and they don’t pause while you negotiate. This insurance claim deadline calculator builds a timeline from your date of loss and exports it to any calendar app.",
        "markup": DATES,
        "explain": """
<h2>The dates that quietly decide claims</h2>
<p>Most claim problems we see aren’t about the estimate at all — they’re about a window that closed. Notice, proof of loss, the time to complete repairs for replacement cost, and the policy’s suit-limitation period all run from different starting points. Missing one can cost far more than any line item.</p>
<h2>How to use this insurance claim deadline calculator</h2>
<ol>
<li>Enter the date of loss (the hail or wind date, the day the pipe burst, or the day you found the ice-dam leak).</li>
<li>Adjust each window to match your policy and any letters from the insurer.</li>
<li>Click <strong>Download .ics</strong> to add the milestones to Google, Apple or Outlook calendars.</li>
</ol>
<h2>About Minnesota suit limitations</h2>
<p>Minnesota’s standard fire policy language commonly limits lawsuits to two years after the loss, and many policies repeat that. Some policies or circumstances differ. Read the “Suit Against Us” condition and talk with a Minnesota attorney well before the date — appraisal doesn’t automatically extend it.</p>
<p>The planner is a reminder tool only. It does not calculate legal deadlines for you.</p>
""",
        "faqs": [
            ("Is the date of loss the day I noticed the damage?", "Usually it is the day the damage happened, such as the storm date. For gradual or hidden damage, the policy and the facts decide, so note both dates."),
            ("Does invoking appraisal pause the suit deadline?", "Don’t assume it does. Ask a Minnesota attorney how the deadline applies to your situation before it gets close."),
            ("Is my data saved?", "No. The planner runs in your browser and the calendar file is generated on your device."),
        ],
    },
    {
        "slug": "appraisal-readiness-checkup", "name": "Appraisal Readiness Checkup", "icon": "✓", "kind": "Checklist",
        "keyword": "insurance appraisal checklist",
        "short": "Twelve yes-or-no questions that score your file and build a to-do list before appraisal is invoked.",
        "title": "Insurance Appraisal Checklist | Readiness Checkup & Score",
        "desc": "Free insurance appraisal checklist: answer 12 quick questions to score your claim file and get a personal to-do list before invoking appraisal.",
        "h1": "Appraisal Readiness Checkup: An Insurance Appraisal Checklist",
        "lede": "A strong appraisal starts with a complete file. Work through this insurance appraisal checklist to see what you already have and what to gather first.",
        "markup": READY,
        "explain": """
<h2>Why readiness matters</h2>
<p>An appraisal award signed by two of the three panel members is binding on the amount of loss. If photos, hidden damage or an itemized estimate are missing when the panel decides, there may be no second chance to add them. This insurance appraisal checklist helps you catch gaps early.</p>
<h2>How the score is weighted</h2>
<p>Questions that decide whether appraisal is even the right path — accepted coverage, two itemized estimates — count three points. Documentation counts two. Housekeeping items count one. A high score doesn’t mean you’ll win; it means the file is complete enough to argue the number.</p>
<h2>What to do with your to-do list</h2>
<ul>
<li>Work from the top: the heavier items unlock the rest.</li>
<li>Send written requests to the insurer, and keep copies.</li>
<li>Use the timeline planner so deadlines don’t slip while you gather records.</li>
</ul>
<p>Your answers are not stored or sent anywhere.</p>
""",
        "faqs": [
            ("What score do I need before invoking appraisal?", "There’s no official threshold. A low score means important evidence may be missing; fix those items first or ask a professional to review the file."),
            ("Can I invoke appraisal if coverage is disputed?", "Appraisal decides the amount of loss, not coverage. If the insurer has denied coverage, speak with a Minnesota attorney first."),
            ("Does a high score guarantee a better award?", "No. It only means the file is well documented. Awards depend on the facts, the estimates and the panel."),
        ],
    },
    {
        "slug": "roof-snow-load-calculator", "name": "Roof Snow Load Calculator", "icon": "❄", "kind": "Calculator",
        "keyword": "roof snow load calculator",
        "short": "Estimate how much the snow and ice on your roof weigh in pounds per square foot — a Minnesota winter essential.",
        "title": "Roof Snow Load Calculator | Snow & Ice Weight in PSF",
        "desc": "Free roof snow load calculator for Minnesota winters: estimate snow and ice weight in pounds per square foot and compare it with a reference load.",
        "h1": "Roof Snow Load Calculator for Minnesota Homes and Buildings",
        "lede": "Snow depth alone says little — weight is what stresses a roof. This roof snow load calculator converts depth, snow type and ice into pounds per square foot.",
        "markup": SNOW,
        "explain": """
<h2>Why Minnesota needs a roof snow load calculator</h2>
<p>Minnesota winters stack snow, thaw it, refreeze it and add more. Wet spring snow and ice layers can weigh several times as much as fresh powder at the same depth. The Metrodome’s fabric roof deflating under heavy snow in December 2010 is the best-known example, but most snow-load claims involve garages, porches, pole buildings and flat commercial roofs.</p>
<h2>How the estimate is calculated</h2>
<ul>
<li><strong>Snow</strong>: depth in feet × typical density for the snow type you choose.</li>
<li><strong>Ice</strong>: thickness in feet × about 57 lb/ft³.</li>
<li><strong>Total</strong>: the sum, compared with the reference load you select, and multiplied by roof area if you enter one.</li>
</ul>
<p>Densities vary widely in real snowpacks; these are rough planning values.</p>
<h2>Snow load, ice dams and your insurance claim</h2>
<p>Collapse from the weight of snow or ice is a covered peril in many homeowner forms, while gradual deterioration is not. Ice dams that push water under shingles are a separate issue covered on our <a href="/appraisal-solutions/ice-dam-winter-damage-appraisal/">ice dam &amp; winter damage</a> page. If a roof is sagging, cracking or leaking, get people out and call a qualified contractor or structural engineer — don’t climb on it.</p>
<p>This calculator is not an engineering evaluation. Reference loads shown are examples, not your building’s rated capacity.</p>
""",
        "faqs": [
            ("How much does a foot of snow weigh on a roof?", "It depends on density. Fresh powder might be around 5–7 pounds per square foot per foot of depth, while wet or packed snow can be 20 pounds or more."),
            ("What is my roof designed to hold?", "Design snow loads depend on building code, location, roof shape and age. Building plans or a structural engineer can tell you; this tool only offers example reference values."),
            ("Is roof collapse from snow covered by insurance?", "Many homeowner policies cover collapse caused by the weight of snow or ice, but terms and exclusions vary. Read your policy’s collapse provisions."),
        ],
    },
]
