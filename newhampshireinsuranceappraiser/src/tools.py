"""Free claim tools: markup + explanatory copy. Logic lives in static/assets/js/app.js. Nothing is stored or sent."""

TB = "/nh-claim-calculators/"

GAP_FULL = """
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Dispute size &amp; net recovery estimator</span><i>Runs only in your browser</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Insurer’s estimate (replacement cost)</label><input id="g-ins" name="insurer" inputmode="decimal" value="21600"><span class="hint">The RCV total on the carrier’s estimate.</span></div>
        <div><label for="g-own">Your estimate (replacement cost)</label><input id="g-own" name="yours" inputmode="decimal" value="34900"><span class="hint">Your contractor’s or an independent line-item estimate.</span></div>
      </div>
      <div><label for="g-land">Where could an award land inside the gap?</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% means the insurer’s number stands; 100% means yours is awarded in full. Test several points.</span></div>
      <div class="row2">
        <div><label for="g-ft">Appraiser fee structure</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of the increase (%)</option></select></div>
        <div><label for="g-fee">Fee amount</label><input id="g-fee" name="fee" inputmode="decimal" value="2800"></div>
      </div>
      <label class="check"><input type="checkbox" name="useump" checked> Include my half of an umpire’s fee</label>
      <div><label for="g-ump">Umpire’s total fee (usually split evenly)</label><input id="g-ump" name="umpire" inputmode="decimal" value="3200"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated net increase to you</small><b data-o="net">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s-a"></span><span class="s-b"></span><span class="s-c"></span></div>
      <div class="legend"><span><i class="s-a"></i>Insurer’s number</span><span><i class="s-b"></i>Your net gain</span><span><i class="s-c"></i>Appraisal costs</span></div>
      <div class="out-rows">
        <div><span>Amount in dispute</span><b data-o="gap">$0</b></div>
        <div><span>Gap as a share of the insurer’s estimate</span><b data-o="pct">—</b></div>
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
  <div class="tool-head"><span>Thirty-second gap check</span><i>Nothing is saved</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="m-ins">Insurer’s estimate</label><input id="m-ins" name="insurer" inputmode="decimal" value="16800"></div>
      <div><label for="m-own">Your contractor’s estimate</label><input id="m-own" name="yours" inputmode="decimal" value="29400"></div>
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

_DEP_ROW = """<tr><td data-l="Item"><input name="item" value="{0}" aria-label="Item"></td><td data-l="Replacement $"><input name="rcv" inputmode="decimal" value="{1}" aria-label="Replacement cost"></td><td data-l="Age (yrs)"><input name="age" inputmode="decimal" value="{2}" aria-label="Age in years"></td><td data-l="Life (yrs)"><input name="life" inputmode="decimal" value="{3}" aria-label="Expected life in years"></td><td class="mono" data-l="ACV" data-o="row">$0</td><td><button type="button" class="x" aria-label="Remove row">×</button></td></tr>"""

DEP = """
<div class="tool tool-wide" data-tool="dep">
  <div class="tool-head"><span>Two-check holdback planner</span><i>Add as many line items as you need</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Architectural shingle roof", 19800, 11, 30), ("Ice &amp; water shield and drip edge", 2600, 11, 30), ("Kitchen ceiling drywall &amp; paint", 1900, 6, 12)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn ghost small" data-add data-run>+ Add a line item</button></div>
      <div class="row2">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="1000"></div>
        <div><label for="d-cap">Depreciation cap</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="90">90%</option></select><span class="hint">Many estimates cap depreciation; check yours.</span></div>
      </div>
      <label class="check"><input type="checkbox" name="nonrec"> My policy pays actual cash value only (no recoverable depreciation)</label>
    </div>
    <div class="tool-out tool-out-3" aria-live="polite">
      <div class="out-big"><small>First payment (ACV − deductible)</small><b data-o="first">$0</b></div>
      <div class="out-big"><small>Held back until repairs</small><b data-o="held">$0</b></div>
      <div class="out-big"><small>Total if fully recovered</small><b data-o="total">$0</b></div>
      <div class="out-rows span-all">
        <div><span>Replacement cost (RCV)</span><b data-o="rcv">$0</b></div>
        <div><span>Total depreciation</span><b data-o="dep">$0</b></div>
        <div><span>Depreciation as a share of RCV</span><b data-o="deppct">0%</b></div>
        <div><span>Actual cash value (ACV)</span><b data-o="acv">$0</b></div>
      </div>
    </div>
  </div>
</div>"""

ROOF = """
<div class="tool" data-tool="roof">
  <div class="tool-head"><span>Steep-roof squares checker</span><i>Check the insurer’s measurements</i></div>
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
      <div data-mode="area" hidden><label for="r-a">Footprint area incl. overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="1450"></div>
      <div class="row2">
        <div><label for="r-p">Roof pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 9 else "", p) for p in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16]) + """</select></div>
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="10">10% — simple gable</option><option value="12" selected>12% — cape with dormers</option><option value="15">15% — hip roof</option><option value="18">18% — cut-up / many valleys</option></select></div>
      </div>
      <div><label for="r-pr">Installed price per square (optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 575"><span class="hint">Use a local contractor’s quote for a rough replacement figure.</span></div>
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
  <div class="tool-head"><span>Percent-to-dollars deductible tool</span><i>Percent vs. flat, in dollars</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling coverage (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="360000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Percentage deductible</label><select id="w-p" name="pct"><option value="1" selected>1%</option><option value="2">2%</option><option value="3">3%</option><option value="5">5%</option><option value="10">10%</option></select></div>
        <div><label for="w-f">All-other-perils flat deductible</label><input id="w-f" name="flat" inputmode="decimal" value="1000"></div>
      </div>
      <div><label for="w-l">Estimated storm damage</label><input id="w-l" name="loss" inputmode="decimal" value="14500"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your percentage deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s-c"></span><span class="s-a"></span></div>
      <div class="legend"><span><i class="s-c"></i>You pay</span><span><i class="s-a"></i>Policy pays</span></div>
      <div class="out-rows">
        <div><span>Payment with the percentage deductible</span><b data-o="pdpay">$0</b></div>
        <div><span>Payment if the flat deductible applied</span><b data-o="flatpay">$0</b></div>
        <div><span>Extra out-of-pocket from the percentage</span><b data-o="diff">$0</b></div>
      </div>
      <p class="out-msg" data-o="below"></p>
    </div>
  </div>
</div>"""

DATES = """
<div class="tool" data-tool="dates">
  <div class="tool-head"><span>Granite State claim clock</span><i>Download as an .ics file</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
      <p class="hint flush">Replace each window with the number in your own policy. The defaults are placeholders, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report the claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="2"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="10"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Often counted from the insurer’s request.</span></div>
        <div><label for="t-r">Depreciation recovery (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="180"></div>
        <div><label for="t-s">Suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="365"><span class="hint">Many forms say one or two years — use yours.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download calendar (.ics)</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the insurer accepted coverage for at least part of the loss?", "Get written confirmation that coverage is accepted. If the claim was denied, speak with a New Hampshire attorney before thinking about appraisal."),
    (3, "Do you have the insurer’s full, itemized estimate — not just a summary page?", "Ask in writing for the complete line-item estimate, including the roof diagram or measurement report."),
    (3, "Do you have your own itemized estimate from a contractor or estimator?", "Get an independent line-item estimate. A one-line lump-sum bid rarely holds up in front of a panel."),
    (2, "Do you have dated photos taken soon after the loss?", "Pull every photo you have, note when each was taken and add current-condition photos."),
    (2, "Have you read the Appraisal paragraph in your policy conditions?", "Find the ‘Appraisal’ condition and note the time limits for naming an appraiser."),
    (2, "Do you know your policy’s suit-limitation date?", "Read the ‘Suit Against Us’ condition and put the date on a calendar — the Granite State claim clock can help."),
    (2, "Were temporary repairs made (tarps, water extraction, heat restored) and receipts kept?", "Finish reasonable temporary repairs and keep every receipt and invoice."),
    (1, "Do you have your current declarations page?", "Download or request your declarations page from your agent or the insurer."),
    (2, "Has hidden damage — attic sheathing, wet insulation, wall cavities — been opened and documented?", "Make sure concealed areas have been inspected so the scope is complete before anyone values it."),
    (1, "Is your correspondence with the insurer saved in date order?", "Collect emails, letters and claim-portal messages in one folder, oldest first."),
    (2, "Is the gap between estimates more than roughly 10% or $5,000?", "Run the dispute size & net recovery estimator. A small gap may not justify appraisal costs."),
    (1, "If the insurer asked for a sworn proof of loss, was it sent on time?", "If a proof of loss was requested, return it within the stated time."),
]

READY = """
<div class="tool tool-wide" data-tool="ready">
  <div class="tool-head"><span>Claim file readiness gauge</span><i>12 questions · two minutes</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <ol class="quiz">""" + "".join(
    '<li data-w="%d" data-fix="%s"><span>%s</span><span class="yn"><button type="button" class="yes" aria-pressed="false">Yes</button><button type="button" class="no" aria-pressed="false">No</button></span></li>' % (w, f, q)
    for w, q, f in _QUIZ) + """
      </ol>
      <div class="btn-row"><button type="button" class="btn ghost small" data-reset>Clear answers</button></div>
    </div>
    <div class="tool-out tool-out-score" aria-live="polite">
      <div>
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#e8eefb" stroke-width="18"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#efae0e" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3" style="transition:stroke-dashoffset .5s,stroke .3s"/></svg>
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
  <div class="tool-head"><span>Snow weight roof calculator</span><i>Illustrative — not a structural test</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="s-l">Roof plan length (ft)</label><input id="s-l" name="len" inputmode="decimal" value="40"></div>
        <div><label for="s-w">Roof plan width (ft)</label><input id="s-w" name="wid" inputmode="decimal" value="26"></div>
      </div>
      <div class="row2">
        <div><label for="s-d">Snow depth on the roof (inches)</label><input id="s-d" name="depth" inputmode="decimal" value="24"></div>
        <div><label for="s-t">Snow type</label><select id="s-t" name="dens"><option value="7">Fresh, light powder (≈7 lb/ft³)</option><option value="15" selected>Settled snow (≈15 lb/ft³)</option><option value="21">Wet or packed snow (≈21 lb/ft³)</option></select></div>
      </div>
      <div class="row2">
        <div><label for="s-i">Ice layer (inches)</label><input id="s-i" name="ice" inputmode="decimal" value="1"><span class="hint">Ice weighs about 57 lb/ft³.</span></div>
        <div><label for="s-b">Benchmark load (lb/ft²)</label><input id="s-b" name="bench" inputmode="decimal" value="40"><span class="hint">Ask your town’s building official — NH figures vary by town and elevation.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated roof snow load</small><b data-o="psf">0 lb/ft²</b></div>
      <div class="meter" aria-hidden="true"><span data-o="bar"></span></div>
      <div class="out-rows">
        <div><span>Roof plan area</span><b data-o="area">0 sq ft</b></div>
        <div><span>Total weight on the roof</span><b data-o="lbs">0 lb</b></div>
        <div><span>Same weight in tons</span><b data-o="tons">0</b></div>
        <div><span>Share of your benchmark</span><b data-o="share">—</b></div>
      </div>
      <p class="out-msg" data-o="smsg"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "gap-and-fee-estimator", "name": "Dispute Size & Net Recovery Estimator", "icon": "Δ", "kind": "Calculator",
        "kw": "insurance appraisal gap calculator",
        "short": "Size the disputed amount, test where an award might land and subtract appraiser and umpire fees.",
        "title": "Insurance Appraisal Gap Calculator | Fees & Net",
        "desc": "Free insurance appraisal gap calculator: compare your estimate with the insurer’s, test award outcomes and subtract fees to see the net.",
        "h1": "Insurance Appraisal Gap Calculator With Fees",
        "lede": "Enter the insurer’s number and yours, slide the award point and add realistic fees. You’ll see whether appraisal is likely to leave more in your pocket.",
        "markup": GAP_FULL,
        "explain": """
<h2>Using the estimator well</h2>
<ol><li><strong>Compare like with like.</strong> Use replacement cost totals on both sides, before depreciation and the deductible.</li>
<li><strong>Run three scenarios.</strong> Try the slider at 30%, 55% and 80%. A dispute that only pays off at 100% is fragile.</li>
<li><strong>Use real fee quotes.</strong> Ask any appraiser for their arrangement in writing and plug it in.</li></ol>
<h2>Why awards land in the middle</h2>
<p>Panels test every line. Measured, photographed and priced items tend to survive; padded or unsupported ones tend to fall away. That’s why the slider exists — it reminds you that the result usually sits somewhere between the two opening numbers.</p>
<div class="note"><b class="h">Illustrative only</b>The default figures are an illustrative example, not a typical result. Your outcome depends on your policy, your documentation and the panel.</div>
<h2>Outside the estimator’s scope</h2>
<p>Deductibles, policy limits and the timing of depreciation change what you are paid, not the size of the dispute. For the payment split, open the <a href="/nh-claim-calculators/depreciation-holdback-planner/">depreciation &amp; holdback planner</a>.</p>
""",
        "faqs": [("Is the projected award a prediction?", "No. It’s a planning scenario you control with the slider. Real awards depend on evidence, pricing support and the panel."), ("How are umpire fees usually paid?", "Most appraisal clauses say each side pays its own appraiser and the umpire’s cost is shared equally. Check the wording of your policy.")],
    },
    {
        "slug": "depreciation-holdback-planner", "name": "Two-Check Holdback Planner", "icon": "ACV", "kind": "Planner",
        "kw": "RCV vs ACV depreciation calculator",
        "short": "List items with age and life to split a claim into the first ACV payment and the depreciation held back.",
        "title": "RCV vs ACV Depreciation Calculator | Holdback",
        "desc": "Free RCV vs ACV depreciation calculator: list damaged items by age and life to estimate the first payment, the holdback and the full total.",
        "h1": "RCV vs. ACV Depreciation & Holdback Calculator",
        "lede": "Replacement cost policies usually pay twice: actual cash value now and recoverable depreciation after the work is done. See how your money splits.",
        "markup": DEP,
        "explain": """
<h2>Straight-line math, with a cap</h2>
<p>The planner uses straight-line depreciation — age divided by expected life — capped at the percentage you pick. Real estimates may adjust for condition or treat some items, like permits or labor, differently, so treat the output as a planning figure.</p>
<h2>Life expectancies you’ll often see</h2>
<div class="table-wrap"><table><thead><tr><th>Item</th><th>Common range</th></tr></thead><tbody>
<tr><td>Architectural asphalt shingles</td><td>25–30 years</td></tr><tr><td>Standing-seam metal roofing</td><td>40–60 years</td></tr><tr><td>Vinyl siding</td><td>30–40 years</td></tr><tr><td>Interior paint</td><td>8–12 years</td></tr><tr><td>Carpet</td><td>8–12 years</td></tr><tr><td>Oil or propane boiler</td><td>20–30 years</td></tr>
</tbody></table></div>
<h2>Collecting the held-back money</h2>
<p>Most replacement cost policies pay the held-back depreciation once repairs are finished within a stated period. New Hampshire’s building season is short — a roof damaged in January may not be replaced until spring — so note the deadline early. The <a href="/nh-claim-calculators/nh-claim-deadline-calendar/">deadline calendar</a> can remind you.</p>
""",
        "faqs": [("Can labor be depreciated?", "Practice differs by policy and jurisdiction. If your estimate depreciates labor, ask the insurer in writing to explain the basis."), ("What if I never repair?", "Under most replacement cost policies you keep the actual cash value payment but may not collect the held-back depreciation.")],
    },
    {
        "slug": "roof-squares-pitch-tool", "name": "Steep-Roof Squares Checker", "icon": "▲", "kind": "Calculator",
        "kw": "roof squares calculator",
        "short": "Turn a footprint and pitch into true roof squares, bundles and steep-roof flags to check an estimate.",
        "title": "Roof Squares Calculator for Insurance Claims",
        "desc": "Free roof squares calculator for insurance claims: convert footprint, pitch and waste into true squares, then compare them with your estimate.",
        "h1": "Roof Squares Calculator for Insurance Claims",
        "lede": "Short measurements are a quiet reason roof claims come up light. Steep New England capes and colonials make the gap bigger. Check the math here.",
        "markup": ROOF,
        "explain": """
<h2>The pitch multiplier</h2>
<p>A pitched roof has more surface than the footprint under it. The multiplier is √(1 + (rise ÷ 12)²). A 9/12 roof — common on older capes — carries about 25% more surface than its footprint; a 12/12 roof about 41% more.</p>
<h2>Comparing against the insurer’s estimate</h2>
<ul><li>Find total squares and the waste percentage in the roof section.</li>
<li>Differences above 5–10% are worth a closer look at the measurement report.</li>
<li>Look for steep and high-roof charges, plus starter, ridge, drip edge and ice &amp; water shield lines.</li></ul>
<h2>Where a footprint falls short</h2>
<p>Roofs with dormers, ells, attached barns or several pitches need plane-by-plane measuring. Use this as a sanity check alongside an aerial report or a tape measure.</p>
""",
        "faqs": [("What is a square?", "One hundred square feet of roof surface. Many New Hampshire single-family roofs fall somewhere between 18 and 35 squares."), ("Why does waste change by roof style?", "Hips, valleys and dormers mean more cutting, so more material becomes scrap.")],
    },
    {
        "slug": "percent-deductible-converter", "name": "Percent-to-Dollars Deductible Tool", "icon": "%", "kind": "Calculator",
        "kw": "percentage deductible calculator",
        "short": "Convert a percentage wind or named-storm deductible into dollars and compare it with a flat deductible.",
        "title": "Percentage Deductible Calculator | Dollars & Payout",
        "desc": "Free percentage deductible calculator: turn a wind or named-storm deductible into dollars and compare the payout with a flat deductible.",
        "h1": "Percentage Deductible Calculator",
        "lede": "Most New Hampshire homeowners have a flat deductible, but some policies — especially near the Seacoast — add a percentage deductible for wind or named storms. See it in dollars.",
        "markup": DEDUCT,
        "explain": """
<h2>Percent of Coverage A, not of the loss</h2>
<p>The percentage is applied to Coverage A, the dwelling limit, not to the size of the loss. An illustrative example: on a $360,000 dwelling limit, a 1% deductible is $3,600 and a 2% deductible is $7,200.</p>
<h2>Finding yours</h2>
<p>Read the declarations page for “windstorm,” “hurricane” or “named storm” deductible wording, then the endorsement that defines when it applies. Many apply only when a storm has been named by the National Hurricane Center.</p>
<h2>Why it matters before appraisal</h2>
<p>The deductible doesn’t change the amount of loss a panel sets, but it changes your check. A dispute that sits mostly inside the deductible may not be worth appraisal fees.</p>
""",
        "faqs": [("Does the percentage apply to contents too?", "It is usually calculated from Coverage A but applied to the whole covered wind loss. Read your endorsement for the exact rule."), ("Can I change it?", "Usually at renewal. Ask your agent how a different deductible changes the premium.")],
    },
    {
        "slug": "nh-claim-deadline-calendar", "name": "Granite State Claim Clock", "icon": "◷", "kind": "Planner",
        "kw": "insurance claim deadline calendar",
        "short": "Map notice, proof of loss, depreciation and suit dates from your date of loss, then export them.",
        "title": "NH Insurance Claim Deadline Calendar | .ics Export",
        "desc": "Free insurance claim deadline calendar for NH property owners: map proof of loss, holdback and suit dates, then download them as an .ics file.",
        "h1": "New Hampshire Insurance Claim Deadline Calendar",
        "lede": "Policy clocks keep running while you argue about the number. Enter your date of loss and your policy’s windows, then send the dates to your calendar.",
        "markup": DATES,
        "explain": """
<h2>Dates worth protecting</h2>
<ul><li><strong>Notice.</strong> Policies require prompt reporting. Late notice is a common defense.</li>
<li><strong>Proof of loss.</strong> When the insurer requests a sworn proof of loss, many forms allow 60 days.</li>
<li><strong>Depreciation recovery.</strong> Repairs often must be completed within a set window to collect holdback — plan around winter.</li>
<li><strong>Suit limitation.</strong> Property policies usually set a contractual deadline for lawsuits. Appraisal doesn’t automatically pause it.</li></ul>
<div class="note"><b class="h">Important</b>This calendar only uses the numbers you type in. It isn’t legal advice, and how a deadline applies can depend on New Hampshire law and the facts. If a date is close, talk to a New Hampshire attorney.</div>
""",
        "faqs": [("Is the date of loss the day I found the damage?", "Usually it’s the day the storm or event happened. Weather records for your address can help pin it down."), ("Does demanding appraisal extend the suit deadline?", "Not automatically. Protect the deadline separately and ask an attorney if it’s getting close.")],
    },
    {
        "slug": "nh-appraisal-readiness-score", "name": "Claim File Readiness Gauge", "icon": "✓", "kind": "Checklist",
        "kw": "appraisal readiness checklist",
        "short": "Twelve yes-or-no questions that score your claim file and build a to-do list before you demand appraisal.",
        "title": "Appraisal Readiness Checklist | Score Your File",
        "desc": "Free appraisal readiness checklist: answer twelve questions to score your claim file and get a to-do list before you demand appraisal.",
        "h1": "Appraisal Readiness Checklist and Score",
        "lede": "Appraisals are won by the file you bring to them. Answer twelve quick questions to see what’s solid and what still needs work.",
        "markup": READY,
        "explain": """
<h2>How the questions are weighted</h2>
<p>Coverage, estimates and evidence count most because they decide whether appraisal fits at all and how well your number will hold up. Paperwork items still matter, but they’re quicker to fix.</p>
<h2>What the score means</h2>
<ul><li><strong>75 or higher:</strong> a well-built file. A professional review of the gap is a sensible next step.</li>
<li><strong>45 to 74:</strong> close the open items first.</li>
<li><strong>Under 45:</strong> demanding appraisal now could lock in a low number.</li></ul>
""",
        "faqs": [("Is anything I click saved?", "No. The checklist runs in your browser and nothing is stored or sent."), ("Can I bring the result to a consultation?", "Yes. Take a screenshot of your score and to-do list.")],
    },
    {
        "slug": "snow-weight-roof-calculator", "name": "Snow Weight Roof Calculator", "icon": "❄", "kind": "Calculator",
        "kw": "roof snow load calculator",
        "short": "Estimate how much the snow and ice on your roof weighs, and compare it with a benchmark you enter.",
        "title": "Roof Snow Load Calculator for NH Homes",
        "desc": "Free roof snow load calculator for New Hampshire homes: estimate the weight of snow and ice on your roof and compare it with a benchmark.",
        "h1": "Roof Snow Load Calculator for New Hampshire Homes",
        "lede": "After a big storm or a long freeze, the question is simple: how heavy is it up there? Enter the depth and type of snow for an illustrative estimate.",
        "markup": SNOW,
        "explain": """
<h2>Depth × density = weight</h2>
<p>Load in pounds per square foot is depth in feet multiplied by the snow’s density. Fresh powder can be light; settled and wet snow is far heavier, and ice is heavier still. Rain falling on an existing snowpack adds weight quickly.</p>
<div class="table-wrap"><table><thead><tr><th>Material</th><th>Approximate density</th><th>Load per foot of depth</th></tr></thead><tbody>
<tr><td>Fresh light snow</td><td>≈7 lb/ft³</td><td>≈7 lb/ft²</td></tr><tr><td>Settled snow</td><td>≈15 lb/ft³</td><td>≈15 lb/ft²</td></tr><tr><td>Wet or packed snow</td><td>≈21 lb/ft³</td><td>≈21 lb/ft²</td></tr><tr><td>Ice</td><td>≈57 lb/ft³</td><td>≈57 lb/ft²</td></tr>
</tbody></table></div>
<h2>Why it matters for a claim</h2>
<p>Snow-load and ice-dam claims often turn on what happened and when: sagging rafters, cracked ceilings, doors that stop closing, water stains under the eaves. Photos and depth measurements taken during the event help show the weight was there.</p>
<div class="note"><b class="h">Safety first</b>This is an illustrative estimate, not a structural evaluation. Don’t climb onto a snow-covered roof. If you see sagging or hear cracking, leave the building and call a professional.</div>
<h2>Related reading</h2>
<p>See our page on <a href="/nh-appraisal-services/ice-dam-roof-snow-appraisal/">ice dam and roof snow claims</a> for how these losses are scoped and valued.</p>
""",
        "faqs": [("What benchmark should I use?", "Your town’s building official can tell you the design snow load used locally. New Hampshire figures vary a lot with town and elevation."), ("Does this tell me if my roof will fail?", "No. Roof capacity depends on framing, condition and drifting. Use the result only as a rough, illustrative weight estimate.")],
    },
]
