"""Interactive claim tools: markup + explanatory copy. Logic lives in static/assets/js/app.js."""

BASE = "/vermont-claim-tools/"

GAP_FULL = """
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Claim gap &amp; fee estimator</span><i>Runs in your browser</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Carrier’s estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="21600"><span class="hint">Replacement cost total before depreciation and deductible.</span></div>
        <div><label for="g-own">Your estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="36900"><span class="hint">Your contractor’s or independent estimate.</span></div>
      </div>
      <div><label for="g-land">Where might an award land inside the gap?</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% means the carrier’s number holds; 100% means your full number is awarded.</span></div>
      <div class="row2">
        <div><label for="g-ft">Your appraiser’s fee type</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="hourly">Hourly (hours × rate)</option><option value="pct">Percent of increase (%)</option></select></div>
        <div><label for="g-fee">Fee amount / hours</label><input id="g-fee" name="fee" inputmode="decimal" value="2800"></div>
      </div>
      <div data-show="hourly" hidden><label for="g-rate">Hourly rate ($)</label><input id="g-rate" name="rate" inputmode="decimal" value="150"></div>
      <label class="check"><input type="checkbox" name="useump" checked> Add half of an umpire’s fee</label>
      <div><label for="g-ump">Umpire’s total fee (split 50/50)</label><input id="g-ump" name="umpire" inputmode="decimal" value="3200"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated net increase to you</small><b data-o="net">$0</b></div>
      <div class="stack" aria-hidden="true"><span style="background:#cfdcd4"></span><span style="background:#ffcc33"></span><span style="background:#a8323e"></span></div>
      <div class="legend"><span><i style="background:#cfdcd4"></i>Carrier’s number</span><span><i style="background:#ffcc33"></i>Your net gain</span><span><i style="background:#a8323e"></i>Appraisal costs</span></div>
      <div class="out-rows">
        <div><span>Amount in dispute</span><b data-o="gap">$0</b></div>
        <div><span>Gap as % of carrier estimate</span><b data-o="pct">—</b></div>
        <div><span>Projected award (RCV)</span><b data-o="award">$0</b></div>
        <div><span>Your appraisal costs</span><b data-o="cost">$0</b></div>
      </div>
      <div class="scen"><p class="todo-h">Three outcomes side by side</p><table><thead><tr><th>Lands at</th><th>Award</th><th>Net to you</th></tr></thead><tbody data-o="scen"></tbody></table></div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

GAP_MINI = """
<div class="tool tool-mini" data-tool="gap">
  <div class="tool-head"><span>Two-number gap check</span><i>No sign-up</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="m-ins">Carrier’s estimate</label><input id="m-ins" name="insurer" inputmode="decimal" value="21600"></div>
        <div><label for="m-own">Your contractor’s estimate</label><input id="m-own" name="yours" inputmode="decimal" value="36900"></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Amount in dispute</small><b data-o="gap">$0</b></div>
      <div class="out-rows"><div><span>Gap as % of carrier estimate</span><b data-o="pct">—</b></div></div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

_DEP_ROW = """<tr><td><input name="item" value="{0}" aria-label="Item"></td><td><input name="rcv" inputmode="decimal" value="{1}" aria-label="Replacement cost"></td><td><input name="age" inputmode="decimal" value="{2}" aria-label="Age in years"></td><td><input name="life" inputmode="decimal" value="{3}" aria-label="Expected life in years"></td><td class="mono" data-o="row">$0</td><td><button type="button" class="x" aria-label="Remove row">×</button></td></tr>"""

DEP = """
<div class="tool tool-wide" data-tool="dep">
  <div class="tool-head"><span>RCV / ACV holdback calculator</span><i>Add as many items as you need</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Architectural shingle roof", 16800, 11, 30), ("Plaster ceilings, two rooms", 5400, 40, 75), ("Wide-plank floor refinish", 3100, 8, 20)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn ghost small" data-add data-run>+ Add item</button></div>
      <div class="row3">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="1000"></div>
        <div><label for="d-cap">Maximum depreciation</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="90">90%</option></select></div>
        <div><label for="d-lab">Labor share of cost</label><select id="d-lab" name="labor"><option value="0" selected>Depreciate labor too</option><option value="40">Don’t depreciate labor (40% labor)</option><option value="50">Don’t depreciate labor (50% labor)</option><option value="60">Don’t depreciate labor (60% labor)</option></select></div>
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
  <div class="tool-head"><span>Roof pitch &amp; squares calculator</span><i>Check the carrier’s diagram</i></div>
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
      <div data-mode="dims"><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="10"></div>
      <div data-mode="area" hidden><label for="r-a">Footprint area incl. overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="1450"></div>
      <div class="row2">
        <div><label for="r-p">Roof pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 10 else "", p) for p in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 18]) + """</select><span class="hint">Classic Vermont farmhouses often run 10/12 to 12/12.</span></div>
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="10">10% · simple gable</option><option value="12" selected>12% · gable with ell or dormers</option><option value="15">15% · hip roof</option><option value="18">18% · cut-up, multiple wings</option></select></div>
      </div>
      <div class="row2">
        <div><label for="r-ice">Ice barrier up from the eaves (ft)</label><input id="r-ice" name="ice" inputmode="decimal" value="6"><span class="hint">Measured up the slope, on both eaves.</span></div>
        <div><label for="r-pr">Installed price per square (optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 575"></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Roof squares (before waste)</small><b data-o="sq">0</b></div>
      <div class="out-rows">
        <div><span>Pitch multiplier</span><b data-o="mult">1.000</b></div>
        <div><span>Roof surface area</span><b data-o="surface">0</b></div>
        <div><span>Squares with waste</span><b data-o="order">0</b></div>
        <div><span>Shingle bundles (3 per square)</span><b data-o="bundles">0</b></div>
        <div><span>Ice &amp; water barrier (sq ft)</span><b data-o="icearea">0</b></div>
        <div><span>Rough replacement cost</span><b data-o="cost">—</b></div>
      </div>
      <p class="out-msg" data-o="steep"></p>
    </div>
  </div>
</div>"""

DEDUCT = """
<div class="tool" data-tool="deduct">
  <div class="tool-head"><span>Percentage deductible calculator</span><i>Percent vs. flat dollars</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling coverage (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="420000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Percentage deductible</label><select id="w-p" name="pct"><option value="0.5">0.5%</option><option value="1" selected>1%</option><option value="2">2%</option><option value="3">3%</option><option value="5">5%</option></select><span class="hint">Some wind, windstorm or hail deductibles are a percent.</span></div>
        <div><label for="w-f">All-other-perils flat deductible</label><input id="w-f" name="flat" inputmode="decimal" value="1000"></div>
      </div>
      <div><label for="w-l">Estimated covered damage</label><input id="w-l" name="loss" inputmode="decimal" value="14800"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your percentage deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span style="background:#a8323e"></span><span style="background:#cfdcd4"></span></div>
      <div class="legend"><span><i style="background:#a8323e"></i>You pay</span><span><i style="background:#cfdcd4"></i>Policy pays</span></div>
      <div class="out-rows">
        <div><span>Payment with the % deductible</span><b data-o="pdpay">$0</b></div>
        <div><span>Payment if the flat deductible applied</span><b data-o="flatpay">$0</b></div>
        <div><span>Extra out-of-pocket from the % deductible</span><b data-o="diff">$0</b></div>
        <div><span>Loss needed before the policy pays anything</span><b data-o="breakeven">$0</b></div>
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
      <p class="hint">Change each window to match your policy. The defaults are common figures, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report the claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="2"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="7"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Often 60 days from the carrier’s request; flood policies count from the loss.</span></div>
        <div><label for="t-a">Name your appraiser (days after demand)</label><input id="t-a" name="appr" inputmode="numeric" value="20"><span class="hint">Counted from an assumed demand 45 days after loss.</span></div>
        <div><label for="t-r">Depreciation recovery (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="180"></div>
        <div><label for="t-s">Suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="730"><span class="hint">Policy wording and Vermont law both matter here. Ask an attorney.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download .ics calendar file</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the carrier accepted coverage for at least part of the loss?", "Get written confirmation that coverage is accepted. If the whole claim was denied, speak with a Vermont attorney before considering appraisal."),
    (3, "Do you have the carrier’s full, itemized estimate?", "Ask in writing for the complete line-item estimate, not just the summary page."),
    (3, "Do you have your own line-item estimate?", "Get an itemized estimate from a contractor or estimator. A one-line bid will not carry weight before a panel."),
    (2, "Do you have dated photos taken soon after the loss?", "Collect every photo and note the date. For winter losses, photograph ice at the eaves before it melts."),
    (2, "Have you read the appraisal paragraph in your policy?", "Find the ‘Appraisal’ condition and note the deadline to name your appraiser."),
    (2, "Do you know the suit-limitation date in your policy?", "Find the ‘Suit Against Us’ condition and put the date on your calendar."),
    (2, "Is it clear which damage is water or wind and which is flood?", "Separate rising-water damage from wind, rain and plumbing damage. They are usually different policies."),
    (2, "For a freeze loss, can you show heat was maintained or the water was shut off?", "Gather fuel delivery receipts, thermostat or monitoring records and any caretaker notes."),
    (1, "Do you have your current declarations page?", "Download or request your declarations page from your agent or carrier."),
    (2, "Has hidden damage been opened up and recorded?", "Make sure wet insulation, wall cavities and subfloor have been checked so the scope is complete."),
    (2, "Is the gap more than about 10% or several thousand dollars?", "Run the numbers in the claim gap & fee estimator. A small gap may not justify appraisal costs."),
    (1, "Have temporary repairs been made and receipts kept?", "Make reasonable temporary repairs to prevent further damage and keep every receipt."),
]

READY = """
<div class="tool tool-wide" data-tool="ready">
  <div class="tool-head"><span>Appraisal readiness check</span><i>12 questions · about two minutes</i></div>
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
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#e3ebe6" stroke-width="18"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#ffcc33" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3" style="transition:stroke-dashoffset .5s,stroke .3s"/></svg>
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
  <div class="tool-head"><span>Roof snow load estimator</span><i>Illustrative, not engineering</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="s-d">Snow depth on the roof (inches)</label><input id="s-d" name="depth" inputmode="decimal" value="30"></div>
        <div><label for="s-t">Type of snow</label><select id="s-t" name="type"><option value="7">Fresh, light powder (~7 lb/ft³)</option><option value="15">Settled snow (~15 lb/ft³)</option><option value="21" selected>Wet or packed snow (~21 lb/ft³)</option><option value="30">Wet, rain-soaked snow (~30 lb/ft³)</option></select></div>
      </div>
      <div class="row2">
        <div><label for="s-i">Ice layer thickness (inches)</label><input id="s-i" name="ice" inputmode="decimal" value="1"><span class="hint">Ice weighs roughly 57 lb/ft³.</span></div>
        <div><label for="s-a">Roof area carrying snow (sq ft)</label><input id="s-a" name="area" inputmode="decimal" value="1600"><span class="hint">Plan area; use the roof squares tool for help.</span></div>
      </div>
      <div><label for="s-c">Roof design snow load, if known (lb/ft²)</label><input id="s-c" name="cap" inputmode="decimal" value="40"><span class="hint">Ask the builder, an engineer or the town. Older barns may be far lower.</span></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated load on the roof</small><b data-o="psf">0 lb/ft²</b></div>
      <div class="meter" aria-hidden="true"><span data-o="bar"></span></div>
      <div class="out-rows">
        <div><span>Snow layer</span><b data-o="snowpsf">0</b></div>
        <div><span>Ice layer</span><b data-o="icepsf">0</b></div>
        <div><span>Total weight on the roof</span><b data-o="tons">0</b></div>
        <div><span>Share of design load</span><b data-o="share">—</b></div>
      </div>
      <p class="out-msg" data-o="snowmsg"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "claim-gap-fee-estimator", "name": "Claim Gap & Fee Estimator", "icon": "Δ", "kind": "Calculator",
        "short": "See the disputed amount, three possible awards and what you might net after appraiser and umpire fees.",
        "title": "Claim Gap & Fee Estimator | Is Appraisal Worth It?",
        "desc": "Free claim gap and fee estimator: compare two estimates, test three possible awards and net out appraiser and umpire fees in your browser.",
        "h1": "Claim Gap & Fee Estimator: Will Appraisal Pay for Itself?",
        "lede": "Enter the carrier’s estimate and yours, pick a fee arrangement and see a low, middle and strong outcome side by side. Example figures are illustrative.",
        "markup": GAP_FULL,
        "explain": """
<h2>How to read the three outcomes</h2>
<p>Appraisal awards rarely match either side’s opening number. The estimator shows what happens if the award lands at 30%, 60% and 90% of the gap, using your fee arrangement each time. If appraisal only makes sense in the strong column, the case may be fragile. If it still works in the low column, it is more likely worth a conversation.</p>
<h2>Fee arrangements</h2>
<ul><li><strong>Flat fee:</strong> a set amount regardless of outcome.</li><li><strong>Hourly:</strong> hours times rate. Enter the hours you were quoted in the fee box.</li><li><strong>Percent of increase:</strong> a share of the amount the award adds above the carrier’s number. Some policies or circumstances raise impartiality questions about contingent fees; ask about it.</li></ul>
<h2>What it leaves out</h2>
<p>Deductibles, policy limits and depreciation timing change what you are paid, not the size of the dispute. For holdback math, use the <a href="/vermont-claim-tools/rcv-acv-holdback-calculator/">RCV / ACV holdback calculator</a>.</p>
""",
        "faqs": [("Is the projected award a prediction?", "No. It is a planning scenario based on the numbers you enter. Actual awards depend on documentation, the panel and the policy."), ("What does an umpire usually charge?", "It varies with the size and complexity of the dispute. The appraisers get a quote once an umpire is proposed, and the fee is usually split evenly.")],
    },
    {
        "slug": "rcv-acv-holdback-calculator", "name": "RCV / ACV Holdback Calculator", "icon": "ACV", "kind": "Calculator",
        "short": "Split a replacement cost claim into the first check, the held-back depreciation and the final total.",
        "title": "RCV / ACV Holdback Calculator | Depreciation Math",
        "desc": "Free RCV and ACV holdback calculator: list items with age and life to estimate your first check, the depreciation held back and the total.",
        "h1": "RCV / ACV Holdback Calculator for Depreciation",
        "lede": "Replacement cost policies usually pay twice: an actual cash value check now and the held-back depreciation after repairs. See how the money splits, with or without labor depreciation.",
        "markup": DEP,
        "explain": """
<h2>How the math works</h2>
<p>Each item is depreciated in a straight line, age divided by expected life, up to the cap you choose. If you pick a labor share, only the material portion is depreciated. Real estimates may use condition adjustments and different life tables, so treat the result as a planning figure.</p>
<h2>Common life expectancies</h2>
<div class="table-wrap"><table><thead><tr><th>Item</th><th>Common range</th></tr></thead><tbody>
<tr><th>Architectural asphalt shingles</th><td>25–30 years</td></tr><tr><th>Standing-seam metal roof</th><td>40–60 years</td></tr><tr><th>Slate roof</th><td>75–100+ years</td></tr><tr><th>Interior paint</th><td>8–12 years</td></tr><tr><th>Carpet</th><td>8–12 years</td></tr><tr><th>Oil or propane boiler</th><td>20–30 years</td></tr>
</tbody></table></div>
<h2>Getting the holdback released</h2>
<p>Policies usually pay recoverable depreciation after repairs are finished within a set time. Send invoices and photos of completed work, and use the <a href="/vermont-claim-tools/claim-deadline-calendar/">claim deadline calendar</a> to remind you before the window closes.</p>
""",
        "faqs": [("Can labor be depreciated in Vermont?", "Practice varies and the law in this area has been developing in many states. Check whether your estimate depreciates labor and ask the carrier to explain its approach in writing."), ("What if I decide not to repair?", "Under most replacement cost policies you keep the ACV payment but may not recover the held-back depreciation.")],
    },
    {
        "slug": "roof-pitch-squares-calculator", "name": "Roof Pitch & Squares Calculator", "icon": "▲", "kind": "Calculator",
        "short": "Turn a footprint into roof squares with pitch, waste and the ice barrier Vermont roofs usually need.",
        "title": "Roof Pitch & Squares Calculator for Claims",
        "desc": "Free roof pitch and squares calculator: convert a footprint into roof squares with pitch, waste and ice barrier to check a claim estimate.",
        "h1": "Roof Pitch & Squares Calculator for Insurance Claims",
        "lede": "A steep farmhouse roof has far more surface than its footprint suggests. Check whether the estimate’s squares, waste and ice barrier match your roof.",
        "markup": ROOF,
        "explain": """
<h2>Why pitch matters</h2>
<p>A roof’s surface area is its footprint multiplied by a pitch factor. At 4/12 the factor is about 1.05; at 12/12 it is about 1.41. A 1,400 square foot footprint becomes almost 2,000 square feet of roof at 12/12. Estimates that use the wrong pitch, or skip waste, come up short on every slope.</p>
<h2>Ice barrier</h2>
<p>Vermont roofs commonly need self-adhering ice and water barrier along the eaves and in valleys. The calculator estimates eave coverage from the distance you enter. Whether the carrier owes for it depends on the policy and on the code or manufacturer requirements that apply.</p>
<h2>Compare with the estimate</h2>
<p>Find the roof section of the carrier’s estimate. Compare the squares, the waste percentage, the steep charges and whether ice and water barrier appears at all. Large differences are worth raising before anyone invokes appraisal.</p>
""",
        "faqs": [("Is this as accurate as a measurement report?", "No. Aerial measurement reports and hand measurements are more precise. This tool is for a quick check."), ("Why does my estimate show two different roof areas?", "Estimates often list the surface area and then a larger quantity with waste included. Compare like with like.")],
    },
    {
        "slug": "percentage-deductible-calculator", "name": "Percentage Deductible Calculator", "icon": "%", "kind": "Calculator",
        "short": "See a percentage wind or hail deductible in dollars and compare what the policy pays.",
        "title": "Percentage Deductible Calculator | Wind and Hail",
        "desc": "Free percentage deductible calculator: convert a wind or hail deductible to dollars and compare your payout with a flat deductible.",
        "h1": "Percentage Deductible Calculator",
        "lede": "A 1% deductible sounds small until you multiply it by the dwelling limit. Convert yours to dollars and see how it changes the check.",
        "markup": DEDUCT,
        "explain": """
<h2>How percentage deductibles work</h2>
<p>A percentage deductible is calculated on the dwelling limit (Coverage A), not on the size of the loss. On a $420,000 home, a 1% deductible is $4,200, while a 2% deductible is $8,400. That amount is subtracted from the covered loss before payment.</p>
<h2>Are they common in Vermont?</h2>
<p>Most Vermont homeowners policies use flat-dollar deductibles. Some carriers add a separate wind, windstorm or hail deductible, and some commercial policies use percentages. Check your declarations page: a separate deductible line usually names the peril it applies to.</p>
<h2>Why it matters for appraisal</h2>
<p>The deductible does not change the amount of loss, but it does change whether a dispute is worth pursuing. If the gap you are arguing over sits mostly inside the deductible, appraisal may not change your payment much.</p>
""",
        "faqs": [("Is the deductible applied before or after depreciation?", "Usually the deductible is subtracted from the loss payment, after depreciation for the first ACV check. Policy wording controls."), ("Can there be two deductibles on one storm?", "Some policies apply a single deductible per occurrence even when several buildings are damaged. Others differ. Read the deductible section.")],
    },
    {
        "slug": "claim-deadline-calendar", "name": "Claim Deadline Calendar", "icon": "◷", "kind": "Planner",
        "short": "Turn a date of loss into a dated list of claim milestones and download them to your calendar.",
        "title": "Claim Deadline Calendar | Download Dates as .ics",
        "desc": "Free claim deadline calendar: enter a date of loss to map notice, proof of loss, appraisal and suit dates, then download an .ics file.",
        "h1": "Claim Deadline Calendar with Calendar Download",
        "lede": "Claims have more deadlines than most owners expect. Enter the date of loss, match the windows to your policy and save the dates to your phone or computer.",
        "markup": DATES,
        "explain": """
<h2>The dates that matter most</h2>
<ul><li><strong>Notice:</strong> policies require prompt notice. Report as soon as you reasonably can.</li><li><strong>Proof of loss:</strong> often due within 60 days of the carrier’s written request. Flood policies usually count from the date of loss.</li><li><strong>Naming an appraiser:</strong> many appraisal clauses give each side 20 days after a written demand.</li><li><strong>Depreciation recovery:</strong> the time allowed to finish repairs and claim the holdback.</li><li><strong>Suit limitation:</strong> the deadline to file a lawsuit under the policy. Vermont law can affect how this applies, so ask a Vermont attorney.</li></ul>
<h2>How the download works</h2>
<p>The button builds a standard .ics file in your browser with one all-day event per milestone. Open it with Google Calendar, Outlook or Apple Calendar. Nothing is sent to us.</p>
""",
        "faqs": [("Are these legal deadlines?", "No. They are planning dates based on common policy terms. Your policy and Vermont law control."), ("What if a date has already passed?", "The calendar marks it. Talk to a professional promptly; some deadlines can be extended or may not apply.")],
    },
    {
        "slug": "appraisal-readiness-check", "name": "Appraisal Readiness Check", "icon": "✓", "kind": "Checklist",
        "short": "Twelve yes-or-no questions that score how ready your file is for appraisal and build a to-do list.",
        "title": "Appraisal Readiness Check | Is Your Claim Ready?",
        "desc": "Free appraisal readiness check: answer twelve questions about your claim file to get a score and a to-do list before you demand appraisal.",
        "h1": "Appraisal Readiness Check for Your Claim File",
        "lede": "Appraisal rewards preparation. Answer twelve quick questions, including two built for Vermont winters and floods, and get a score with a practical to-do list.",
        "markup": READY,
        "explain": """
<h2>Why readiness matters</h2>
<p>Once appraisal is demanded, timelines start and the panel works with what each side can support. Missing estimates, undated photos and unresolved coverage questions weaken your position. A few weeks of preparation can make a large difference to the award.</p>
<h2>How the score works</h2>
<p>Each question carries a weight from one to three. Coverage acceptance and complete estimates count most. The score is the share of weighted points you have. It is a guide, not a prediction of any result.</p>
""",
        "faqs": [("What score should I aim for?", "Above about 75 means your file has the basics an appraisal panel expects. Below that, work through the to-do list first."), ("Is my answer saved?", "No. Everything runs in your browser and resets when you leave the page.")],
    },
    {
        "slug": "roof-snow-load-estimator", "name": "Roof Snow Load Estimator", "icon": "❄", "kind": "Estimator",
        "short": "Estimate the weight of snow and ice on a roof from depth and snow type, compared with a design load.",
        "title": "Roof Snow Load Estimator | Vermont Snow and Ice",
        "desc": "Free roof snow load estimator: turn snow depth, snow type and ice thickness into pounds per square foot and total tons on your roof.",
        "h1": "Roof Snow Load Estimator for Vermont Winters",
        "lede": "Two feet of powder and two feet of rain-soaked March snow are very different loads. Estimate what your roof was carrying when it sagged or failed.",
        "markup": SNOW,
        "explain": """
<h2>How the estimate works</h2>
<p>The load in pounds per square foot is the snow depth in feet times the snow’s density, plus the ice layer times about 57 pounds per cubic foot. Densities vary widely; the options use typical values for each kind of snow. Multiply by roof area and divide by 2,000 for tons.</p>
<h2>What it is good for</h2>
<p>It helps explain a collapse or sagging claim in plain numbers, and it shows why a carrier’s description of “gradual deterioration” may not fit a roof that failed after a heavy, wet storm. It is not an engineering analysis. Structural claims need an engineer’s report.</p>
<h2>Design snow loads</h2>
<p>Design snow loads in Vermont vary by town and elevation, and many older barns and additions were built before current codes. Ask the builder, the town or an engineer for the right figure for your building.</p>
""",
        "faqs": [("Is my roof safe at less than 100% of design load?", "Not necessarily. Rot, prior damage and drifting all reduce capacity. If a roof is sagging or creaking, get off it and call a professional."), ("Why does rain on snow matter so much?", "Snow absorbs rain like a sponge. A rain-on-snow event can add a large load without adding much depth.")],
    },
]
