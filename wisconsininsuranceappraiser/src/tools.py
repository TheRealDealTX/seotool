"""Free claim calculators for Wisconsin property owners: markup + explanatory copy.
Logic lives in static/assets/js/app.js. Everything runs in the browser; nothing is stored or sent."""

TB = "/insurance-claim-calculators/"


def _head(title, note):
    return f'<div class="calc-head"><span class="calc-t">{title}</span><span class="calc-n">{note}</span></div>'


GAP_FULL = """
<div class="calc" data-tool="gap">""" + _head("Settlement gap calculator", "Private · runs in your browser") + """
  <div class="calc-body">
    <div class="calc-in">
      <div class="row2">
        <div><label for="g-ins">Insurer’s estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="21600"><span class="hint">Replacement-cost total from the carrier’s estimate.</span></div>
        <div><label for="g-own">Your estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="34900"><span class="hint">Contractor or independent estimate, also at RCV.</span></div>
      </div>
      <div><label for="g-land">Scenario: where the award lands inside the gap</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% means the carrier’s figure stands; 100% means your full figure is awarded.</span></div>
      <div class="row2">
        <div><label for="g-ft">Your appraiser’s fee</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of increase (%)</option><option value="hourly">Hourly (hours × rate)</option></select></div>
        <div><label for="g-fee">Fee amount, % or hours</label><input id="g-fee" name="fee" inputmode="decimal" value="2800"></div>
      </div>
      <div data-hourly hidden><label for="g-rate">Hourly rate ($)</label><input id="g-rate" name="rate" inputmode="decimal" value="150"></div>
      <label class="check"><input type="checkbox" name="useump" checked> <span>Include my half of an umpire’s fee</span></label>
      <div><label for="g-ump">Umpire’s total fee (shared 50/50)</label><input id="g-ump" name="umpire" inputmode="decimal" value="3200"></div>
    </div>
    <div class="calc-out" aria-live="polite">
      <div class="big"><small>Estimated net increase to you</small><b data-o="net">$0</b></div>
      <div class="bar" aria-hidden="true"><span class="b1"></span><span class="b2"></span><span class="b3"></span></div>
      <div class="key"><span><i class="b1"></i>Carrier’s figure</span><span><i class="b2"></i>Your net gain</span><span><i class="b3"></i>Appraisal costs</span></div>
      <dl class="rows">
        <div><dt>Amount in dispute</dt><dd data-o="gap">$0</dd></div>
        <div><dt>Gap vs. carrier estimate</dt><dd data-o="pct">—</dd></div>
        <div><dt>Projected award (RCV)</dt><dd data-o="award">$0</dd></div>
        <div><dt>Gross increase</dt><dd data-o="gain">$0</dd></div>
        <div><dt>Your appraisal costs</dt><dd data-o="cost">$0</dd></div>
        <div class="hl"><dt>Break-even landing point</dt><dd data-o="breakeven">—</dd></div>
      </dl>
      <p class="msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

GAP_MINI = """
<div class="calc calc-mini" data-tool="gap">""" + _head("Two-number gap check", "No sign-up") + """
  <div class="calc-body">
    <div class="calc-in">
      <div><label for="m-ins">Insurer’s estimate</label><input id="m-ins" name="insurer" inputmode="decimal" value="16300"></div>
      <div><label for="m-own">Your contractor’s estimate</label><input id="m-own" name="yours" inputmode="decimal" value="27450"></div>
      <div><label for="m-land">Award lands at</label><div class="range"><input id="m-land" type="range" name="land" min="0" max="100" step="5" value="50" data-unit="%"><output>50%</output></div><span class="hint">of the disputed amount</span></div>
    </div>
    <div class="calc-out" aria-live="polite">
      <div class="big"><small>Amount in dispute</small><b data-o="gap">$0</b></div>
      <dl class="rows">
        <div><dt>Gap vs. carrier estimate</dt><dd data-o="pct">—</dd></div>
        <div><dt>Projected award</dt><dd data-o="award">$0</dd></div>
        <div><dt>Increase before fees</dt><dd data-o="gain">$0</dd></div>
      </dl>
      <p class="msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

_DEP_ROW = """<tr><td><input name="item" value="{0}" aria-label="Item"></td><td><input name="rcv" inputmode="decimal" value="{1}" aria-label="Replacement cost"></td><td><input name="age" inputmode="decimal" value="{2}" aria-label="Age in years"></td><td><input name="life" inputmode="decimal" value="{3}" aria-label="Expected life in years"></td><td class="mono" data-o="row">$0</td><td><button type="button" class="x" aria-label="Remove row">×</button></td></tr>"""

DEP = """
<div class="calc calc-wide" data-tool="dep">""" + _head("RCV / ACV holdback calculator", "Add as many line items as you need") + """
  <div class="calc-body">
    <div class="calc-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Laminated shingle roof", 19800, 11, 30), ("Kitchen ceiling drywall & paint", 2650, 6, 12), ("Basement carpet & pad", 2100, 7, 10)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn line small" data-add data-run>+ Add item</button></div>
      <div class="row2">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="1000"></div>
        <div><label for="d-cap">Depreciation cap</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="90">90%</option></select><span class="hint">Many estimates cap depreciation; check yours.</span></div>
      </div>
      <label class="check"><input type="checkbox" name="nonrec"> <span>My policy pays actual cash value only (depreciation isn’t recoverable)</span></label>
    </div>
    <div class="calc-out calc-out-3" aria-live="polite">
      <div class="big"><small>First check (ACV − deductible)</small><b data-o="first">$0</b></div>
      <div class="big"><small>Held back until repairs are done</small><b data-o="held">$0</b></div>
      <div class="big"><small>Total if fully recovered</small><b data-o="total">$0</b></div>
      <dl class="rows span-all">
        <div><dt>Replacement cost (RCV)</dt><dd data-o="rcv">$0</dd></div>
        <div><dt>Total depreciation</dt><dd data-o="dep">$0</dd></div>
        <div><dt>Depreciation as share of RCV</dt><dd data-o="deppct">0%</dd></div>
        <div><dt>Actual cash value (ACV)</dt><dd data-o="acv">$0</dd></div>
        <div class="hl"><dt>Share of the total paid up front</dt><dd data-o="upfront">—</dd></div>
      </dl>
    </div>
  </div>
</div>"""

ROOF = """
<div class="calc" data-tool="roof">""" + _head("Roof pitch, squares &amp; ice-shield calculator", "Check the roof section of your estimate") + """
  <div class="calc-body">
    <div class="calc-in">
      <fieldset class="plain"><legend class="sr-only">Measurement method</legend>
        <div class="btn-row">
          <label class="check"><input type="radio" name="mode" value="dims" checked> <span>Footprint length × width</span></label>
          <label class="check"><input type="radio" name="mode" value="area"> <span>I know the footprint area</span></label>
        </div></fieldset>
      <div class="row2" data-mode="dims">
        <div><label for="r-l">Footprint length (ft)</label><input id="r-l" name="len" inputmode="decimal" value="52"></div>
        <div><label for="r-w">Footprint width (ft)</label><input id="r-w" name="wid" inputmode="decimal" value="30"></div>
      </div>
      <div data-mode="dims"><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="12"></div>
      <div data-mode="area" hidden><label for="r-a">Footprint area incl. overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="1900"></div>
      <div data-mode="area" hidden><label for="r-e">Total eave length (ft)</label><input id="r-e" name="eave" inputmode="decimal" value="120"></div>
      <div class="row2">
        <div><label for="r-p">Roof pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 8 else "", p) for p in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16]) + """</select></div>
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="10">10% — plain gable</option><option value="13" selected>13% — gable with dormers</option><option value="15">15% — hip roof</option><option value="18">18% — complex, many valleys</option></select></div>
      </div>
      <div class="row2">
        <div><label for="r-ice">Ice barrier reach up the roof (ft)</label><select id="r-ice" name="ice"><option value="3">3 ft (one course)</option><option value="6" selected>6 ft (two courses)</option></select><span class="hint">Cold-climate codes generally require an ice barrier from the eave to a point inside the wall line.</span></div>
        <div><label for="r-pr">Installed price per square (optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 560"></div>
      </div>
    </div>
    <div class="calc-out" aria-live="polite">
      <div class="big"><small>Roof squares (before waste)</small><b data-o="sq">0</b></div>
      <dl class="rows">
        <div><dt>Pitch multiplier</dt><dd data-o="mult">1.000</dd></div>
        <div><dt>Roof surface area</dt><dd data-o="surface">0</dd></div>
        <div><dt>Squares with waste</dt><dd data-o="order">0</dd></div>
        <div><dt>Shingle bundles (3 per square)</dt><dd data-o="bundles">0</dd></div>
        <div class="hl"><dt>Ice &amp; water barrier at eaves</dt><dd data-o="iceSq">0</dd></div>
        <div><dt>Rough replacement cost</dt><dd data-o="cost">—</dd></div>
      </dl>
      <p class="msg" data-o="steep"></p>
    </div>
  </div>
</div>"""

DEDUCT = """
<div class="calc" data-tool="deduct">""" + _head("Percentage deductible calculator", "Percent vs. flat, side by side") + """
  <div class="calc-body">
    <div class="calc-in">
      <div><label for="w-a">Dwelling coverage (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="320000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Wind/hail percentage deductible</label><select id="w-p" name="pct"><option value="0.5">0.5%</option><option value="1" selected>1%</option><option value="2">2%</option><option value="3">3%</option><option value="5">5%</option></select></div>
        <div><label for="w-f">All-other-perils flat deductible</label><input id="w-f" name="flat" inputmode="decimal" value="1000"></div>
      </div>
      <div><label for="w-l">Estimated storm damage</label><input id="w-l" name="loss" inputmode="decimal" value="14800"></div>
    </div>
    <div class="calc-out" aria-live="polite">
      <div class="big"><small>Your percentage deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="bar" aria-hidden="true"><span class="b3"></span><span class="b1"></span></div>
      <div class="key"><span><i class="b3"></i>You pay</span><span><i class="b1"></i>Policy pays</span></div>
      <dl class="rows">
        <div><dt>Payment with % deductible</dt><dd data-o="pdpay">$0</dd></div>
        <div><dt>Payment if the flat deductible applied</dt><dd data-o="flatpay">$0</dd></div>
        <div class="hl"><dt>Extra out-of-pocket from % deductible</dt><dd data-o="diff">$0</dd></div>
      </dl>
      <div class="table-wrap mini-table"><table><caption>The same loss at other percentages</caption><thead><tr><th>Deductible</th><th>In dollars</th><th>Claim pays</th></tr></thead><tbody data-o="ladder"></tbody></table></div>
      <p class="msg" data-o="below"></p>
    </div>
  </div>
</div>"""

DATES = """
<div class="calc" data-tool="dates">""" + _head("Wisconsin claim timeline planner", "Downloads to your calendar (.ics)") + """
  <div class="calc-body">
    <div class="calc-in">
      <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
      <p class="hint">Change each window to match your own policy. The defaults are placeholders, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report the claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="2"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="10"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Often counted from the insurer’s request.</span></div>
        <div><label for="t-r">Depreciation recovery (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="180"></div>
        <div><label for="t-s">Suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="730"><span class="hint">Copy the period in your “Suit Against Us” clause.</span></div>
      </div>
      <label class="check"><input type="checkbox" name="winter"> <span>Add a reminder to re-inspect for hidden damage after the spring thaw</span></label>
    </div>
    <div class="calc-out" aria-live="polite">
      <ol class="tl" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download .ics calendar file</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the insurer accepted coverage for at least part of the loss?", "Get written confirmation of what the insurer accepts. If the whole claim was denied, speak with a Wisconsin attorney before thinking about appraisal."),
    (3, "Do you have the insurer’s full, itemized estimate?", "Ask in writing for the complete line-item estimate, not just the payment summary."),
    (3, "Do you have your own itemized estimate?", "Get a line-item estimate from a contractor or estimator. A one-line bid is hard to defend in front of a panel."),
    (2, "Do you have dated photos taken soon after the loss?", "Pull together every photo and video with dates. Add current photos of the same areas."),
    (2, "Have you found and read the appraisal paragraph in your policy?", "Look in the Conditions section for “Appraisal” and note any time limits it sets."),
    (2, "Do you know the deadline in your policy’s “Suit Against Us” clause?", "Find the clause and put the date on your calendar. The timeline planner can export it."),
    (2, "Have you made temporary repairs and kept the receipts?", "Tarp, dry out or board up as needed, and save every receipt and invoice."),
    (2, "Has hidden damage been opened up and documented (attic, walls, decking)?", "Make sure wet insulation, framing and roof decking have been checked so nothing is left out of the scope."),
    (1, "Do you have your current declarations page?", "Download it from your insurer’s portal or ask your agent for a copy."),
    (1, "Is your correspondence with the insurer saved in date order?", "Gather letters, emails and adjuster notes into one dated file."),
    (2, "Is the gap more than roughly 10% or $5,000?", "Run both numbers through the settlement gap calculator. A small gap may not justify appraisal costs."),
    (1, "If the insurer asked for a sworn proof of loss, did you send it on time?", "If one was requested, complete and return it within the stated period."),
]

READY = """
<div class="calc calc-wide" data-tool="ready">""" + _head("Appraisal readiness quiz", "12 questions · about two minutes") + """
  <div class="calc-body">
    <div class="calc-in">
      <ol class="quiz">""" + "".join(
    '<li data-w="%d" data-fix="%s"><span>%s</span><span class="yn"><button type="button" class="yes" aria-pressed="false">Yes</button><button type="button" class="no" aria-pressed="false">No</button></span></li>' % (w, f, q)
    for w, q, f in _QUIZ) + """
      </ol>
      <div class="btn-row"><button type="button" class="btn line small" data-reset>Clear answers</button></div>
    </div>
    <div class="calc-out calc-out-gauge" aria-live="polite">
      <div>
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#e3e8f4" stroke-width="18"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#FFCC18" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3" style="transition:stroke-dashoffset .5s,stroke .3s"/></svg>
        <div class="gauge-num"><span data-o="score">–</span></div>
        <p class="hint center">Answered <span data-o="count">0 / 12</span></p>
      </div>
      <div>
        <p class="msg" data-o="verdict"></p>
        <p class="todo-h">Your to-do list</p>
        <ul data-o="todo" class="todo"></ul>
      </div>
    </div>
  </div>
</div>"""

SNOW = """
<div class="calc" data-tool="snow">""" + _head("Roof snow load calculator", "Weight of what’s on your roof") + """
  <div class="calc-body">
    <div class="calc-in">
      <div class="row2">
        <div><label for="s-d">Snow depth on the roof (inches)</label><input id="s-d" name="depth" inputmode="decimal" value="18"></div>
        <div><label for="s-t">Type of snow</label><select id="s-t" name="dens"><option value="7">Fresh, light powder (~7 lb/ft³)</option><option value="15" selected>Settled snow (~15 lb/ft³)</option><option value="21">Wet or wind-packed (~21 lb/ft³)</option></select></div>
      </div>
      <div class="row2">
        <div><label for="s-i">Ice layer thickness (inches)</label><input id="s-i" name="ice" inputmode="decimal" value="1"><span class="hint">Glazed ice weighs about 57 lb/ft³.</span></div>
        <div><label for="s-a">Roof area (sq ft, plan view)</label><input id="s-a" name="area" inputmode="decimal" value="1600"></div>
      </div>
      <div><label for="s-c">Roof design snow load (psf)</label><input id="s-c" name="design" inputmode="decimal" value="30"><span class="hint">Placeholder. Your building department, plans or an engineer can give the actual figure for your roof.</span></div>
    </div>
    <div class="calc-out" aria-live="polite">
      <div class="big"><small>Estimated load on the roof</small><b data-o="psf">0 psf</b></div>
      <div class="bar" aria-hidden="true"><span class="b2" data-o="fill"></span></div>
      <div class="key"><span><i class="b2"></i>Share of the design load you entered</span></div>
      <dl class="rows">
        <div><dt>Snow portion</dt><dd data-o="snowpsf">0 psf</dd></div>
        <div><dt>Ice portion</dt><dd data-o="icepsf">0 psf</dd></div>
        <div><dt>Total weight on the roof</dt><dd data-o="total">0 lb</dd></div>
        <div class="hl"><dt>Share of design load</dt><dd data-o="share">—</dd></div>
      </dl>
      <p class="msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "settlement-gap-calculator", "name": "Settlement Gap Calculator", "icon": "$", "kind": "Calculator",
        "short": "Size the disputed amount, test award scenarios, subtract fees and find the break-even point.",
        "title": "Settlement Gap Calculator | Is Appraisal Worth the Fees?",
        "desc": "Free settlement gap calculator: compare your estimate with the insurer’s, test award scenarios, subtract fees and find your break-even point.",
        "h1": "Settlement Gap Calculator: Will Appraisal Pay for Itself?",
        "lede": "Enter the insurer’s estimate and yours, pick a scenario for where an award might land, and add realistic fees. The calculator shows your likely net and the landing point where appraisal stops paying for itself.",
        "markup": GAP_FULL,
        "explain": """
<h2>Reading the break-even line</h2>
<p>The break-even landing point is the share of the disputed amount an award has to reach before your appraisal costs are covered. If the break-even sits at 15% of the gap, even a cautious panel result probably leaves you ahead. If it sits at 70%, the dispute depends on winning most of your line items, and a documented supplement request may be the smarter first step.</p>
<h2>Running honest scenarios</h2>
<ol><li><strong>Use RCV totals on both sides</strong> so you compare like with like, before depreciation and deductible.</li>
<li><strong>Try three landing points</strong> (say 30%, 55% and 80%) instead of trusting a single answer.</li>
<li><strong>Price fees the way they’re quoted.</strong> Flat, percentage and hourly arrangements behave very differently on small and large gaps.</li>
<li><strong>Keep the umpire in.</strong> Many panels settle without one, but planning for the cost keeps the result conservative.</li></ol>
<h2>What this tool doesn’t cover</h2>
<p>Deductibles, policy limits, sub-limits and depreciation timing change what you’re paid, not the size of the dispute. Use the <a href="/insurance-claim-calculators/rcv-acv-holdback-calculator/">RCV/ACV holdback calculator</a> and the <a href="/insurance-claim-calculators/percentage-deductible-calculator/">percentage deductible calculator</a> for those.</p>
<p class="small">All figures shown are illustrative defaults. Replace them with the numbers from your own claim.</p>
""",
        "faqs": [("Is the projected award a prediction?", "No. It’s a scenario you choose. Real awards depend on the evidence, the policy and the people on the panel."), ("Why does the fee type matter so much?", "A percentage fee shrinks when the increase is small and grows when it’s large, while a flat fee doesn’t move. On a narrow gap, a flat fee can absorb most of the recovery."), ("Does Wisconsin set appraiser fees?", "Fees are agreed between you and your appraiser. Ask for the arrangement in writing before any work starts.")],
    },
    {
        "slug": "rcv-acv-holdback-calculator", "name": "RCV/ACV Holdback Calculator", "icon": "ACV", "kind": "Calculator",
        "short": "Split a replacement-cost claim into the first check, the depreciation held back and the final total.",
        "title": "RCV vs ACV Holdback Calculator | Recoverable Depreciation",
        "desc": "List damaged items with age and expected life to estimate your first ACV check, the depreciation held back and the total after repairs.",
        "h1": "RCV/ACV Holdback Calculator for Replacement-Cost Claims",
        "lede": "Replacement-cost policies usually pay in two stages: an actual-cash-value check first and the held-back depreciation after the work is finished. Enter your line items to see how the money splits.",
        "markup": DEP,
        "explain": """
<h2>How the calculator depreciates</h2>
<p>Each line uses straight-line depreciation (age ÷ expected life), capped at the maximum you choose. Real estimates may adjust for condition, use different life tables or leave some items such as permits undepreciated. Treat the output as a planning figure, not a payment promise.</p>
<h2>Life expectancies often seen in estimates</h2>
<div class="table-wrap"><table><thead><tr><th>Item</th><th>Common range</th></tr></thead><tbody>
<tr><th>Laminated asphalt shingles</th><td>25–30 years</td></tr><tr><th>Steel roofing panels</th><td>40–50 years</td></tr><tr><th>Interior paint</th><td>8–12 years</td></tr><tr><th>Carpet and pad</th><td>8–12 years</td></tr><tr><th>Vinyl siding</th><td>30–40 years</td></tr><tr><th>Gas furnace</th><td>15–20 years</td></tr>
</tbody></table></div>
<h2>Collecting the holdback</h2>
<p>Most replacement-cost policies release recoverable depreciation once repairs are complete, often within a set number of days. Send final invoices and photos of finished work. The <a href="/insurance-claim-calculators/claim-timeline-planner/">claim timeline planner</a> can remind you before your window closes.</p>
""",
        "faqs": [("Should labor be depreciated?", "Approaches differ by insurer, policy wording and court decisions. Ask your insurer to explain in writing whether and how labor was depreciated in your estimate."), ("What happens if I don’t repair?", "Under most replacement-cost policies you keep the actual cash value payment but give up the depreciation that was held back."), ("Can depreciation itself be appraised?", "Often yes, since depreciation is part of the value of a loss. Policy language and the facts of the claim control.")],
    },
    {
        "slug": "roof-pitch-squares-calculator", "name": "Roof Pitch & Squares Calculator", "icon": "▲", "kind": "Calculator",
        "short": "Turn a footprint into true roof squares, bundles and the ice-and-water barrier a cold-climate roof needs.",
        "title": "Roof Pitch & Squares Calculator | Ice Barrier Included",
        "desc": "Estimate roof squares from footprint, pitch and waste, plus eave ice-and-water barrier, then check the roof section of your insurance estimate.",
        "h1": "Roof Pitch and Squares Calculator with Ice-Barrier Estimate",
        "lede": "Roof claims often come up short on measurements. Use the footprint and pitch to estimate the true surface, squares and bundles, plus the eave ice-and-water barrier a Wisconsin roof normally needs.",
        "markup": ROOF,
        "explain": """
<h2>The math behind the numbers</h2>
<p>A roof surface is larger than the footprint under it, and the gap grows with pitch. The multiplier is √(1 + (rise ÷ 12)²). An 8/12 roof is about 20% larger than its footprint; a 12/12 roof is about 41% larger.</p>
<h2>Why the ice barrier line matters here</h2>
<p>Cold-climate building codes generally call for a self-adhering ice barrier along the eaves, running from the edge to a point inside the exterior wall line. On a full replacement that membrane is a real cost, and it’s easy to leave off an estimate that was written from a standard template. The calculator multiplies your eave length by the reach you choose and converts it to squares.</p>
<h2>Checking the estimate</h2>
<ul><li>Compare total squares and the waste percentage with the results here. A difference over 5–10% deserves a closer look.</li>
<li>Look for steep charges (often from 7/12) and high-roof charges for two-story sections.</li>
<li>Confirm ice and water barrier, starter, drip edge, ridge cap and valley metal are listed.</li>
<li>Check whether the felt or synthetic underlayment covers the full roof.</li></ul>
<p>Complex roofs with several planes need measuring plane by plane; use this tool as a sanity check, not a substitute for a field measurement.</p>
""",
        "faqs": [("What’s a roofing square?", "One hundred square feet of roof surface. Most ranch and two-story homes fall somewhere between 18 and 40 squares."), ("Does my insurer have to pay for ice barrier?", "That depends on your policy and whether code requires it for the repair. Ordinance or law coverage, if you have it, may apply to code-driven items."), ("Why does waste change by roof shape?", "Hips, valleys and dormers mean more cutting, so more material ends up as scrap.")],
    },
    {
        "slug": "percentage-deductible-calculator", "name": "Percentage Deductible Calculator", "icon": "%", "kind": "Calculator",
        "short": "See a wind/hail percentage deductible in dollars and how much less a storm claim would pay.",
        "title": "Percentage Deductible Calculator | Wind & Hail in Dollars",
        "desc": "Turn a wind or hail percentage deductible into dollars, compare it with a flat deductible and see the same loss at 0.5% to 5% side by side.",
        "h1": "Percentage Deductible Calculator for Wind and Hail Claims",
        "lede": "A 1% or 2% deductible sounds small until it’s multiplied by your dwelling limit. Convert yours into dollars and see how it changes what a storm claim actually pays.",
        "markup": DEDUCT,
        "explain": """
<h2>Why percentage deductibles catch people off guard</h2>
<p>Some Wisconsin homeowners policies carry a separate wind or hail deductible figured as a percentage of Coverage A rather than a flat amount. On a $320,000 dwelling limit (an illustrative figure), a 2% deductible is $6,400. That is the first $6,400 of a hailstorm loss you would absorb before the policy pays.</p>
<h2>Finding yours</h2>
<p>Check the declarations page for a “wind/hail” or “windstorm or hail” deductible, then read the endorsement that defines when it applies. Some apply to any wind or hail loss; others only to certain storms.</p>
<h2>What it means for appraisal</h2>
<p>A deductible doesn’t change the amount of loss a panel decides, but it does change what lands in your account. A dispute just above the deductible may not be worth the fees; one well above it often is. Pair this tool with the <a href="/insurance-claim-calculators/settlement-gap-calculator/">settlement gap calculator</a>.</p>
""",
        "faqs": [("Is the percentage taken from the loss amount?", "Usually not. It’s typically a percentage of your dwelling coverage limit, applied to the covered wind or hail loss. Your policy wording controls."), ("Can I switch to a flat deductible?", "Sometimes, at renewal. Ask your agent how the premium changes."), ("Does the deductible apply to each storm?", "Generally it applies per occurrence, so two separate storms can mean two deductibles.")],
    },
    {
        "slug": "claim-timeline-planner", "name": "Claim Timeline Planner", "icon": "◷", "kind": "Planner",
        "short": "Map notice, proof-of-loss, depreciation and suit dates from your date of loss, then export them.",
        "title": "Wisconsin Claim Timeline Planner | Calendar Export",
        "desc": "Enter your date of loss to map notice, proof-of-loss, depreciation and suit-limitation dates for a Wisconsin claim, then save them to a calendar.",
        "h1": "Wisconsin Property Claim Timeline Planner",
        "lede": "Policy deadlines keep running while you argue about a number. Enter your date of loss and the windows from your policy to build a timeline you can drop straight into your calendar.",
        "markup": DATES,
        "explain": """
<h2>The dates worth protecting</h2>
<ul><li><strong>Notice.</strong> Policies ask for prompt notice of a loss. Reporting quickly avoids a common dispute.</li>
<li><strong>Proof of loss.</strong> If your insurer asks for a sworn proof of loss, the policy usually sets a period to return it.</li>
<li><strong>Depreciation recovery.</strong> Replacement-cost policies often set a window to finish repairs and claim the holdback.</li>
<li><strong>Suit limitation.</strong> Your policy’s “Suit Against Us” clause limits how long you have to sue. Appraisal doesn’t automatically pause it.</li></ul>
<h2>The Wisconsin winter twist</h2>
<p>Snow cover hides roof and siding damage, and ice dams often reveal interior leaks weeks after a cold snap. Tick the spring-thaw box to add a reminder to re-inspect once the snow is gone, so late-appearing damage can be reported promptly.</p>
<div class="note"><b class="h">Important</b>The planner only uses the numbers you type in. It isn’t legal advice, and Wisconsin law and court decisions can affect how policy deadlines apply. If a deadline is close, talk to a Wisconsin attorney.</div>
""",
        "faqs": [("Is the date of loss the day I noticed the damage?", "Usually it’s the day the storm or event happened. Weather records for your address can help pin it down."), ("Does demanding appraisal stop the suit deadline?", "Not automatically. Protect the date on its own unless you have a written agreement that extends it."), ("What does the .ics file work with?", "Google Calendar, Apple Calendar, Outlook and most other calendar apps can import it.")],
    },
    {
        "slug": "appraisal-readiness-quiz", "name": "Appraisal Readiness Quiz", "icon": "✓", "kind": "Checklist",
        "short": "Answer 12 yes/no questions to score your claim file and get a to-do list before demanding appraisal.",
        "title": "Appraisal Readiness Quiz | Is Your Claim File Ready?",
        "desc": "Twelve yes-or-no questions that score how ready your property claim file is for appraisal and list exactly what to gather before you demand it.",
        "h1": "Appraisal Readiness Quiz: Score Your Claim File",
        "lede": "Strong appraisals are usually won on paper before the panel meets. Answer twelve quick questions to see where your file stands and what to fix first.",
        "markup": READY,
        "explain": """
<h2>How the questions are weighted</h2>
<p>Coverage, the two estimates and dated evidence carry the most weight, because they decide whether appraisal is the right tool and how well your number will hold up. Paperwork items still matter, but they’re quick to fix.</p>
<h2>What your score means</h2>
<ul><li><strong>75 or higher:</strong> the file is in good shape. A professional look at the dollar gap is the logical next step.</li>
<li><strong>45 to 74:</strong> close the open items before you send a demand.</li>
<li><strong>Under 45:</strong> demanding appraisal now could lock in a low number. Build the file first.</li></ul>
""",
        "faqs": [("Are my answers saved?", "No. The quiz runs in your browser and nothing is stored or sent."), ("Can I bring my results to a consultation?", "Yes. A screenshot of your to-do list is a useful starting point for a conversation.")],
    },
    {
        "slug": "roof-snow-load-calculator", "name": "Roof Snow Load Calculator", "icon": "❄", "kind": "Calculator",
        "short": "Estimate how heavy the snow and ice on your roof are and compare them with a design load.",
        "title": "Roof Snow Load Calculator | Snow & Ice Weight in Wisconsin",
        "desc": "Estimate the weight of snow and ice on your roof in pounds per square foot and compare it with a design load. Built for Wisconsin winters.",
        "h1": "Roof Snow Load Calculator for Wisconsin Winters",
        "lede": "A foot of fluffy powder and a foot of wet, wind-packed snow are very different loads. Enter depth, snow type and any ice layer to estimate the weight your roof is carrying.",
        "markup": SNOW,
        "explain": """
<h2>How the estimate works</h2>
<p>The calculator multiplies depth by a typical density for the snow type you pick, then adds the weight of any ice layer. Densities are rough averages: fresh powder can be lighter than 7 lb/ft³, and late-season snow soaked by rain can be heavier than 21 lb/ft³. Drifts against walls, parapets and lower roofs can be far deeper than the average depth you measure.</p>
<h2>Why it matters for a claim</h2>
<p>Collapse and snow-weight damage are often covered perils under property policies, but insurers look closely at whether the damage came from the weight of snow and ice or from deterioration, poor design or old repairs. A dated record of the snow depth, the type of snow and the date of any sagging or cracking can help when the cause is debated. See our <a href="/appraisal-solutions/snow-load-roof-collapse-appraisal/">snow load and roof collapse appraisal</a> page for how those disputes are valued.</p>
<div class="note"><b class="h">Safety first</b>Don’t climb onto a snow-covered roof. If you see sagging, new cracks, doors that suddenly stick or hear popping, leave the building and call a professional. This calculator is a rough guide, not an engineering assessment.</div>
""",
        "faqs": [("What design snow load does my roof have?", "It depends on where you live, when the building was built and how it was designed. Building plans, your municipality or a structural engineer can tell you."), ("Is roof collapse from snow covered?", "Many property policies cover collapse caused by the weight of snow or ice, subject to their own conditions and exclusions. Read your policy’s collapse provision."), ("Should I rake snow off my roof?", "A roof rake used from the ground can reduce load near the eaves and help with ice dams. Avoid climbing onto the roof.")],
    },
]
