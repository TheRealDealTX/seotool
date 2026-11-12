"""Free claim tools for Montana Insurance Appraiser: markup + copy.
All logic lives in static/assets/js/app.js and runs in the browser; nothing is stored or sent."""

C_NAVY, C_AMBER, C_TINT = "#13306b", "#f28c28", "#c9d4ea"

# ---------------------------------------------------------------- 1. claim gap & fee calculator
GAP = f"""
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Claim gap &amp; fee calculator</span><i>Runs in your browser · nothing stored</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Carrier’s estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="18400"><span class="hint">Replacement cost total before depreciation.</span></div>
        <div><label for="g-own">Your estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="31700"><span class="hint">Contractor or independent estimate.</span></div>
      </div>
      <div><label for="g-land">Where might the award land inside the gap?</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% = the carrier’s number holds. 100% = your full number is awarded.</span></div>
      <div class="row2">
        <div><label for="g-ft">Your appraiser’s fee</label><select id="g-ft" name="feetype"><option value="flat">Flat or hourly total ($)</option><option value="pct">Percent of the increase (%)</option></select></div>
        <div><label for="g-fee">Fee amount</label><input id="g-fee" name="fee" inputmode="decimal" value="2800"></div>
      </div>
      <div class="row2">
        <div><label for="g-ump">Umpire’s total fee ($)</label><input id="g-ump" name="umpire" inputmode="decimal" value="3000"></div>
        <div class="check-cell"><label class="check"><input type="checkbox" name="useump" checked> Include my half of the umpire fee</label></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated net gain after fees</small><b data-o="net">$0</b></div>
      <div class="stack" aria-hidden="true"><span style="background:{C_TINT}"></span><span style="background:{C_NAVY}"></span><span style="background:{C_AMBER}"></span></div>
      <div class="legend"><span><i style="background:{C_TINT}"></i>Carrier’s number</span><span><i style="background:{C_NAVY}"></i>Your net gain</span><span><i style="background:{C_AMBER}"></i>Appraisal costs</span></div>
      <div class="out-rows">
        <div><span>Amount in dispute</span><b data-o="gap">$0</b></div>
        <div><span>Gap vs. carrier estimate</span><b data-o="pct">—</b></div>
        <div><span>Projected award (RCV)</span><b data-o="award">$0</b></div>
        <div><span>Your appraisal costs</span><b data-o="cost">$0</b></div>
        <div class="hl"><span>Break-even point inside the gap</span><b data-o="even">—</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

# ---------------------------------------------------------------- 2. depreciation & holdback
_DEP_ROW = """<tr><td><input name="item" value="{0}" aria-label="Item"></td><td><input name="rcv" inputmode="decimal" value="{1}" aria-label="Replacement cost"></td><td><input name="age" inputmode="decimal" value="{2}" aria-label="Age in years"></td><td><input name="life" inputmode="decimal" value="{3}" aria-label="Expected life in years"></td><td class="mono" data-o="row">$0</td><td><button type="button" class="x" aria-label="Remove row">×</button></td></tr>"""

DEP = """
<div class="tool tool-wide" data-tool="dep">
  <div class="tool-head"><span>Depreciation &amp; holdback calculator</span><i>Add a row for each item</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Laminated shingle roof", 19800, 9, 30), ("Steel siding, north & west walls", 7400, 16, 40), ("Seamless gutters", 1650, 9, 25), ("Exterior paint, trim", 1900, 6, 10)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn btn-line btn-sm" data-add data-run>+ Add item</button></div>
      <div class="row2">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="2500"></div>
        <div><label for="d-cap">Depreciation cap</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="90">90%</option></select><span class="hint">Many estimates cap depreciation; check yours.</span></div>
      </div>
      <label class="check"><input type="checkbox" name="nonrec"> My roof is on an actual-cash-value or payment-schedule basis (no holdback is recoverable)</label>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-trio">
        <div><small>First check (ACV − deductible)</small><b data-o="first">$0</b></div>
        <div><small>Held back until repairs</small><b data-o="held">$0</b></div>
        <div><small>Total once repairs are done</small><b data-o="total">$0</b></div>
      </div>
      <div class="out-rows">
        <div><span>Replacement cost (RCV)</span><b data-o="rcv">$0</b></div>
        <div><span>Depreciation taken</span><b data-o="dep">$0</b></div>
        <div><span>Depreciation as share of RCV</span><b data-o="deppct">0%</b></div>
        <div><span>Actual cash value (ACV)</span><b data-o="acv">$0</b></div>
      </div>
    </div>
  </div>
</div>"""

# ---------------------------------------------------------------- 3. roof pitch & squares
_PITCH = "".join(f'<option value="{p}"{" selected" if p == 6 else ""}>{p}/12</option>' for p in range(0, 19))
ROOF = f"""
<div class="tool" data-tool="roof">
  <div class="tool-head"><span>Roof pitch &amp; squares calculator</span><i>Footprint × pitch factor + waste</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <fieldset class="seg"><legend>How do you want to measure?</legend>
        <label><input type="radio" name="mode" value="dims" checked> Length × width</label>
        <label><input type="radio" name="mode" value="area"> I know the footprint</label>
      </fieldset>
      <div class="row2" data-mode="dims">
        <div><label for="r-len">House length (ft)</label><input id="r-len" name="len" inputmode="decimal" value="58"></div>
        <div><label for="r-wid">House width (ft)</label><input id="r-wid" name="wid" inputmode="decimal" value="32"></div>
      </div>
      <div data-mode="dims"><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="16"></div>
      <div data-mode="area" hidden><label for="r-area">Footprint incl. overhangs (sq ft)</label><input id="r-area" name="area" inputmode="decimal" value="2100"></div>
      <div class="row2">
        <div><label for="r-pitch">Roof pitch (rise per 12″)</label><select id="r-pitch" name="pitch">{_PITCH}</select></div>
        <div><label for="r-waste">Waste factor</label><select id="r-waste" name="waste"><option value="10">10% (simple gable)</option><option value="12" selected>12% (gable + valleys)</option><option value="15">15% (hip roof)</option><option value="18">18% (cut-up roof)</option></select></div>
      </div>
      <div><label for="r-price">Installed price per square (optional, $)</label><input id="r-price" name="price" inputmode="decimal" placeholder="e.g. 520"><span class="hint">Use a local contractor’s number; prices vary a lot across Montana.</span></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Squares to order (with waste)</small><b data-o="order">0</b></div>
      <div class="out-rows">
        <div><span>Pitch multiplier</span><b data-o="mult">1.000</b></div>
        <div><span>True roof surface</span><b data-o="surface">0 sq ft</b></div>
        <div><span>Squares before waste</span><b data-o="sq">0</b></div>
        <div><span>Shingle bundles (3 per square)</span><b data-o="bundles">0</b></div>
        <div><span>Rough installed cost</span><b data-o="cost">—</b></div>
      </div>
      <p class="out-msg" data-o="steep"></p>
    </div>
  </div>
</div>"""

# ---------------------------------------------------------------- 4. wind/hail % deductible (with a second storm)
DEDUCT = f"""
<div class="tool" data-tool="deduct">
  <div class="tool-head"><span>Wind/hail percentage deductible calculator</span><i>One storm or two in a season</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="w-cova">Dwelling limit, Coverage A ($)</label><input id="w-cova" name="cova" inputmode="decimal" value="385000"></div>
        <div><label for="w-pct">Wind/hail deductible</label><select id="w-pct" name="pct"><option value="1">1%</option><option value="2" selected>2%</option><option value="3">3%</option><option value="5">5%</option></select></div>
      </div>
      <div class="row2">
        <div><label for="w-flat">All-peril (flat) deductible ($)</label><input id="w-flat" name="flat" inputmode="decimal" value="1500"></div>
        <div><label for="w-loss">Storm 1: estimated damage ($)</label><input id="w-loss" name="loss" inputmode="decimal" value="21500"></div>
      </div>
      <label class="check"><input type="checkbox" name="second"> Add a second, separate storm this season</label>
      <div data-second hidden><label for="w-loss2">Storm 2: estimated damage ($)</label><input id="w-loss2" name="loss2" inputmode="decimal" value="9000"><span class="hint">Most policies apply the deductible to each occurrence. Check yours for an annual aggregate.</span></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your wind/hail deductible</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span style="background:{C_AMBER}"></span><span style="background:{C_NAVY}"></span></div>
      <div class="legend"><span><i style="background:{C_AMBER}"></i>You absorb</span><span><i style="background:{C_NAVY}"></i>Policy pays (illustrative)</span></div>
      <div class="out-rows">
        <div><span>Storm 1 payment under % deductible</span><b data-o="pdpay">$0</b></div>
        <div><span>Same loss under the flat deductible</span><b data-o="flatpay">$0</b></div>
        <div><span>Extra cost of the % deductible</span><b data-o="diff">$0</b></div>
        <div data-second hidden><span>Storm 2 payment</span><b data-o="pay2">$0</b></div>
        <div class="hl"><span>You absorb this season</span><b data-o="season">$0</b></div>
      </div>
      <p class="out-msg" data-o="below"></p>
    </div>
  </div>
</div>"""

# ---------------------------------------------------------------- 5. claim deadline calendar (.ics)
DATES = """
<div class="tool" data-tool="dates">
  <div class="tool-head"><span>Claim deadline calendar</span><i>Download as .ics for any calendar app</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="t-dol">Date of loss</label><input id="t-dol" type="date" name="dol"></div>
      <p class="mini-h">Adjust each window to match your policy and letters (days after the loss)</p>
      <div class="row2">
        <div><label for="t-notice">Report the claim</label><input id="t-notice" name="notice" inputmode="numeric" value="3"></div>
        <div><label for="t-mitig">Temporary repairs done</label><input id="t-mitig" name="mitig" inputmode="numeric" value="10"></div>
      </div>
      <div class="row2">
        <div><label for="t-pol">Proof of loss (if requested)</label><input id="t-pol" name="pol" inputmode="numeric" value="60"></div>
        <div><label for="t-season">Exterior work before winter</label><input id="t-season" name="season" inputmode="numeric" value="120"></div>
      </div>
      <div class="row2">
        <div><label for="t-rcd">Depreciation recovery window</label><input id="t-rcd" name="rcd" inputmode="numeric" value="365"></div>
        <div><label for="t-suit">Policy suit-limitation clause</label><input id="t-suit" name="suit" inputmode="numeric" value="1095"></div>
      </div>
      <span class="hint">Defaults are placeholders, not Montana law. Your policy wording, the carrier’s letters and a Montana attorney control the real dates.</span>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <button type="button" class="btn btn-amber btn-block" data-ics>Download calendar (.ics)</button>
    </div>
  </div>
</div>"""

# ---------------------------------------------------------------- 6. appraisal readiness quiz
_Q = [
    (3, "Has the insurer accepted coverage (in writing) for at least part of the loss?", "Get the carrier’s coverage position in writing; appraisal values a covered loss, it doesn’t decide coverage."),
    (3, "Do you have the carrier’s complete line-item estimate, not just a payment letter?", "Ask the adjuster for the full estimate (PDF) with every line item, quantity and price."),
    (3, "Do you have a competing estimate from a contractor or independent estimator?", "Get a detailed, line-item estimate from a qualified Montana contractor or estimator."),
    (2, "Have you found and read the appraisal paragraph in your policy?", "Find the appraisal clause in your policy (often under ‘Conditions’) and note its demand and timing steps."),
    (2, "Do you have dated photos or video of the damage before repairs?", "Gather every photo, video and drone image of the damage, with dates."),
    (2, "Have you kept receipts for tarps, board-up, drying and temporary housing?", "Collect receipts for mitigation and additional living expenses."),
    (2, "Do you know your deductible type (flat, % wind/hail) and amount?", "Pull your declarations page and confirm every deductible that applies."),
    (1, "Is the dispute about price or scope, rather than whether damage happened at all?", "If the carrier says there’s no covered damage, talk to an attorney before demanding appraisal."),
    (1, "Do you know your suit-limitation and depreciation-recovery dates?", "Find your policy’s deadlines and put them in a calendar (try the deadline calendar tool)."),
    (1, "Are the repairs still undone, or fully documented if already done?", "If repairs are finished, collect invoices and before/after photos so the panel can see the damage."),
]
QUIZ = """
<div class="tool" data-tool="ready">
  <div class="tool-head"><span>Appraisal readiness quiz</span><i>10 questions · weighted score</i></div>
  <div class="tool-body">
    <div class="tool-in"><ol class="quiz">""" + "".join(
    f'<li data-w="{w}" data-fix="{fix}"><span>{q}</span><span class="yn"><button type="button" class="yes" aria-pressed="false">Yes</button><button type="button" class="no" aria-pressed="false">No</button></span></li>'
    for w, q, fix in _Q) + f"""</ol><button type="button" class="btn btn-line btn-sm" data-reset>Start over</button></div>
    <div class="tool-out" aria-live="polite">
      <div class="gauge"><svg width="150" height="150" viewBox="0 0 100 100" aria-hidden="true" focusable="false"><circle cx="50" cy="50" r="40" fill="none" stroke="{C_TINT}" stroke-width="10"/><circle data-o="arc" cx="50" cy="50" r="40" fill="none" stroke="{C_NAVY}" stroke-width="10" stroke-linecap="round" stroke-dasharray="251.3" stroke-dashoffset="251.3" transform="rotate(-90 50 50)"/></svg><b data-o="score">–</b><small data-o="count">0 / {len(_Q)}</small></div>
      <p class="out-msg" data-o="verdict"></p>
      <p class="mini-h">Your to-do list</p><ul class="todo" data-o="todo"></ul>
    </div>
  </div>
</div>"""

# ---------------------------------------------------------------- 7. roof snow load estimator (Montana tool)
_SNOW_TYPES = '<option value="7">Fresh, light powder (~7 lb/ft³)</option><option value="15">Settled snow (~15 lb/ft³)</option><option value="25">Wind-packed / old snow (~25 lb/ft³)</option><option value="35">Wet, heavy spring snow (~35 lb/ft³)</option><option value="57">Ice (~57 lb/ft³)</option>'
_SNOW_ROW = '<tr><td><input name="depth" inputmode="decimal" value="{0}" aria-label="Layer depth in inches"></td><td><select name="dens" aria-label="Snow type">{1}</select></td><td class="mono" data-o="row">0 psf</td><td><button type="button" class="x" aria-label="Remove layer">×</button></td></tr>'


def _row(depth, dens):
    return _SNOW_ROW.format(depth, _SNOW_TYPES.replace(f'value="{dens}"', f'value="{dens}" selected'))


SNOW = f"""
<div class="tool tool-wide" data-tool="snow">
  <div class="tool-head"><span>Roof snow load estimator</span><i>Layer by layer · pounds per square foot</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Layer depth (in)</th><th>Snow type</th><th>Load</th><th><span class="sr">Remove</span></th></tr></thead><tbody>
      {_row(14, 15)}{_row(6, 35)}{_row(1, 57)}
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn btn-line btn-sm" data-add data-run>+ Add layer</button></div>
      <div class="row2">
        <div><label for="s-area">Roof area (sq ft, optional)</label><input id="s-area" name="area" inputmode="decimal" value="1900"></div>
        <div><label for="s-design">Roof design snow load (psf)</label><input id="s-design" name="design" inputmode="decimal" value="40"><span class="hint">Illustrative default. Ask your building department or an engineer for the real figure.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated roof snow load</small><b data-o="psf">0 psf</b></div>
      <div class="meter" aria-hidden="true"><span data-o="bar"></span><i></i></div>
      <div class="out-rows">
        <div><span>Total snow depth</span><b data-o="depth">0 in</b></div>
        <div><span>Share of design load</span><b data-o="share">—</b></div>
        <div><span>Approximate weight on the roof</span><b data-o="weight">—</b></div>
        <div><span>Same weight in pickup trucks (~5,000 lb)</span><b data-o="trucks">—</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

SNOW_MINI = f"""
<div class="tool tool-mini" data-tool="snow">
  <div class="tool-head"><span>Quick roof snow check</span><i>Illustrative · runs in your browser</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="sm-depth">Snow on the roof (inches)</label><input id="sm-depth" name="depth" inputmode="decimal" value="16"></div>
      <div><label for="sm-type">What kind of snow?</label><select id="sm-type" name="dens">{_SNOW_TYPES.replace('value="25"', 'value="25" selected')}</select></div>
      <div><label for="sm-design">Roof design load (psf, illustrative)</label><input id="sm-design" name="design" inputmode="decimal" value="40"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated load</small><b data-o="psf">0 psf</b></div>
      <div class="meter" aria-hidden="true"><span data-o="bar"></span><i></i></div>
      <div class="out-rows"><div><span>Share of design load</span><b data-o="share">—</b></div></div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

# ---------------------------------------------------------------- page copy
TOOLS = [
    {
        "slug": "claim-gap-calculator", "name": "Claim Gap & Fee Calculator", "kind": "Calculator", "photo": "calculator",
        "title": "Claim Gap Calculator | Appraisal Fees & Net Gain",
        "desc": "Free claim gap calculator: compare the carrier’s estimate with yours, add appraiser and umpire fees, and find your break-even award.",
        "h1": "Claim Gap Calculator With Appraisal Fees",
        "lede": "See how big the disputed amount really is, what appraisal might cost you, and how far into the gap an award has to land before you come out ahead.",
        "short": "Disputed amount, fees and the break-even point where appraisal starts paying for itself.",
        "markup": GAP,
        "explain": """<h2>How the claim gap calculator works</h2>
<p>The gap is simply your replacement-cost estimate minus the carrier’s. Appraisal rarely awards one side’s number in full, so the slider lets you test where an award might land inside that gap. The calculator then subtracts what appraisal costs you: your own appraiser’s fee (flat, hourly or a percentage of the increase) and, if the panel needs one, half of the umpire’s fee.</p>
<h3>The break-even point</h3>
<p>The highlighted figure shows how far into the gap an award has to land just to cover your costs. If break-even sits at 15%, almost any reasonable award helps. If it sits at 70%, the dispute may be too small for formal appraisal and a documented supplement request, or an <a href="/claim-services/insurance-estimate-review/">estimate review</a>, is often the smarter first move.</p>
<h3>Reading the result</h3>
<ul><li><strong>Gap under about 10% of the carrier’s estimate:</strong> often closable with photos, measurements and a written supplement.</li><li><strong>Gap of several thousand dollars or more, with clear line-item differences:</strong> worth a conversation about appraisal.</li><li><strong>Gap driven by a coverage denial:</strong> appraisal values covered damage; it doesn’t decide coverage. Speak with a Montana attorney.</li></ul>
<p>Every figure here is illustrative. Real awards depend on the evidence, the policy and the panel.</p>""",
        "faqs": [
            ("Why compare replacement cost and not the check I received?", "Your first check is usually actual cash value minus the deductible. Appraisal sets the amount of loss, typically at both replacement cost and actual cash value, so comparing RCV totals shows the real size of the disagreement."),
            ("Do appraisers usually charge a percentage?", "Some do, some bill hourly and some charge a flat fee. The calculator handles all three. Whatever the structure, get the terms in writing before work begins."),
            ("Will I always pay half of an umpire?", "Most appraisal clauses split the umpire’s cost equally between you and the insurer. If the two appraisers agree without an umpire, there’s no umpire fee at all."),
        ],
    },
    {
        "slug": "depreciation-holdback-calculator", "name": "Depreciation & Holdback Calculator", "kind": "Calculator", "photo": "house-in-pines",
        "title": "RCV vs ACV Depreciation & Holdback Calculator",
        "desc": "Estimate depreciation, actual cash value, the first check and the recoverable holdback on a Montana property claim, item by item.",
        "h1": "Depreciation & Holdback Calculator (RCV vs. ACV)",
        "lede": "List the damaged items, their age and expected life. The calculator shows the depreciation taken, your first check and what should be released once repairs are done.",
        "short": "Item-by-item depreciation, ACV, first check and the recoverable holdback.",
        "markup": DEP,
        "explain": """<h2>Why your first check looks small</h2>
<p>Most replacement-cost policies pay in two stages. First comes actual cash value (replacement cost minus depreciation) less the deductible. The depreciation is held back and released when you finish repairs, within the window your policy allows. This calculator reproduces that math with straight-line depreciation: age divided by expected life, limited by a cap.</p>
<h3>Where depreciation disputes start</h3>
<ul><li><strong>Age:</strong> a roof replaced eight years ago is sometimes recorded as the house’s age.</li><li><strong>Life expectancy:</strong> steel siding and metal roofing last far longer than the defaults some estimates use.</li><li><strong>Labor:</strong> whether labor is depreciated depends on policy language and practice; ask how your estimate treats it.</li><li><strong>Non-recoverable roofs:</strong> some Montana policies settle older roofs on a payment schedule or ACV basis. Tick the box to see that effect.</li></ul>
<p>Depreciation is part of the amount of loss, so an appraisal panel can value it. If the figures in the carrier’s estimate look wrong, our <a href="/claim-services/insurance-estimate-review/">estimate review</a> checks them line by line. Results here are illustrative.</p>""",
        "faqs": [
            ("Is depreciation always recoverable?", "Not always. It depends on whether the policy (or a roof endorsement) settles at replacement cost or actual cash value, and whether you complete repairs within the policy’s timeframe."),
            ("What life expectancy should I use?", "Use realistic service lives for the actual material: a laminated shingle roof, steel siding and interior paint all age differently. Estimating software has defaults, but they can be challenged."),
            ("Does the deductible come out of the holdback?", "Usually the deductible is taken from the first payment, as modeled here. If the deductible is larger than the ACV, the first check may be zero."),
        ],
    },
    {
        "slug": "roof-pitch-squares-calculator", "name": "Roof Pitch & Squares Calculator", "kind": "Calculator", "photo": "roof-toolbelt",
        "title": "Roof Pitch & Squares Calculator | Free Roofing Math",
        "desc": "Free roof pitch and squares calculator: turn a footprint and pitch into true roof area, squares, bundles and a rough cost to check an estimate.",
        "h1": "Roof Pitch & Squares Calculator",
        "lede": "Convert a house footprint and roof pitch into real roof surface, squares, shingle bundles and a ballpark cost, then compare it with the quantities in the carrier’s estimate.",
        "short": "Footprint and pitch to true roof area, squares, bundles and a rough cost.",
        "markup": ROOF,
        "explain": """<h2>Why roof quantity disputes matter</h2>
<p>A roofing square is 100 square feet of roof surface. Because a pitched roof is longer than its footprint, the surface is the footprint multiplied by a pitch factor. At 6/12 that factor is about 1.118; at 10/12 it’s about 1.302. Leave the pitch out, or measure from an aerial photo without correcting for slope, and an estimate can come up several squares short.</p>
<h3>Waste, steep charges and Montana roofs</h3>
<ul><li><strong>Waste:</strong> hips, valleys and dormers need more cut material. A plain gable might need 10%; a cut-up roof can need 18% or more.</li><li><strong>Steep and high roofs:</strong> estimating software usually adds labor for pitches of roughly 7/12 and up and for multi-story eaves.</li><li><strong>Snow country details:</strong> ice-and-water membrane at eaves and valleys, snow guards on metal roofs and drip edge are common items to check.</li></ul>
<p>This is planning math, not a measurement report. For a hail claim, pair it with our guide to <a href="/field-notes/hail-claims-on-montana-roofs/">hail claims on Montana roofs</a>. Figures are illustrative.</p>""",
        "faqs": [
            ("How do I find my roof pitch?", "Count the inches the roof rises over 12 inches of horizontal run, using a level and tape from the attic or a ladder, or read it from a measurement report. Never climb a roof you aren’t equipped for."),
            ("Why does the calculator round bundles up?", "Shingles are sold in whole bundles, usually three per square, so any fraction means buying another bundle."),
            ("Does this include ridge cap and starter?", "Not separately. Those are linear items measured in feet. The waste factor covers cutting loss on the field shingles only."),
        ],
    },
    {
        "slug": "wind-hail-deductible-calculator", "name": "Wind/Hail % Deductible Calculator", "kind": "Calculator", "photo": "hail-sky",
        "title": "Wind/Hail Percentage Deductible Calculator",
        "desc": "Turn a 1%, 2% or 5% wind/hail deductible into dollars, compare it with a flat deductible and see what two storms in one season cost you.",
        "h1": "Wind & Hail Percentage Deductible Calculator",
        "lede": "Many Montana homeowner policies carry a separate wind/hail deductible set as a percentage of the dwelling limit. See it in dollars, and what a second storm in the same summer does to your out-of-pocket cost.",
        "short": "Percentage deductibles in dollars, plus the cost of a second storm in one season.",
        "markup": DEDUCT,
        "explain": """<h2>How percentage deductibles work</h2>
<p>A percentage deductible is calculated from the dwelling limit on your declarations page (Coverage A), not from the size of the loss. On a $385,000 dwelling limit, a 2% wind/hail deductible is $7,700. A loss smaller than that pays nothing, and a larger one pays only the amount above it (illustrative figures).</p>
<h3>Two storms, two deductibles</h3>
<p>Hail seasons east of the Divide can bring more than one damaging storm to the same street. Most policies apply the deductible per occurrence, so separate storms usually mean separate deductibles. A few policies or endorsements work differently, so check your wording. Tick the second-storm box to see the combined effect.</p>
<h3>Why the deductible matters in appraisal</h3>
<p>Appraisal sets the amount of loss before the deductible comes off. When the carrier’s estimate sits just above or below the deductible, a few missing line items can decide whether any payment is owed at all. That’s where a <a href="/claim-services/hail-roof-damage-appraisal/">hail damage appraisal</a> often starts. All results are illustrative.</p>""",
        "faqs": [
            ("Where do I find my wind/hail deductible?", "On the declarations page, usually listed separately from the all-peril deductible. It may be shown as a percentage, a dollar amount or both."),
            ("Does a higher dwelling limit mean a higher deductible?", "Yes. Because it’s a percentage of Coverage A, raising your dwelling limit (for example, to keep up with building costs) also raises the deductible in dollars."),
            ("Can appraisal change my deductible?", "No. The deductible is set by the policy. Appraisal determines the amount of loss, and the deductible is applied to that amount."),
        ],
    },
    {
        "slug": "claim-deadline-calendar", "name": "Claim Deadline Calendar", "kind": "Planner", "photo": "notebook",
        "title": "Claim Deadline Calendar | Export Dates to .ics",
        "desc": "Map notice, proof of loss, building-season and depreciation dates from your date of loss, then download them to any calendar app as an .ics file.",
        "h1": "Insurance Claim Deadline Calendar",
        "lede": "Enter your date of loss, adjust each window to match your policy, and download the dates to your phone or computer calendar.",
        "short": "Build a dated claim timeline and export it to your calendar as .ics.",
        "markup": DATES,
        "explain": """<h2>Deadlines that sink good claims</h2>
<p>Property policies contain time limits: prompt notice, a sworn proof of loss when requested, the window to finish repairs and recover depreciation, and a suit-limitation clause. Miss one and a strong claim can get much harder. This planner turns your date of loss into a dated list you can keep in front of you.</p>
<h3>The Montana building season</h3>
<p>We added a line most planners leave out: getting exterior work done before winter. In much of Montana, roofing and siding work slows sharply once snow arrives, and a spring hail claim that drags into November can mean a tarp over the winter. Plan the appraisal timeline with that in mind.</p>
<h3>Important limits</h3>
<ul><li>The default numbers are placeholders, not legal deadlines.</li><li>Some windows run from the carrier’s written request, not the date of loss.</li><li>Montana law can affect how some policy limits apply. If a deadline is close, talk to a licensed Montana attorney now.</li></ul>
<p>The file downloads straight from your browser; nothing is sent to us. See the <a href="/appraisal-roadmap/">appraisal roadmap</a> for where each step fits.</p>""",
        "faqs": [
            ("Is the .ics file safe to open?", "Yes. It’s a plain-text calendar file created in your browser from the dates on screen. Google Calendar, Apple Calendar and Outlook can all import it."),
            ("Why is the suit-limitation default three years?", "It’s only a placeholder. Policies differ and Montana law may affect the period. Read your policy’s ‘Suit Against Us’ condition and confirm with a Montana attorney."),
            ("Does demanding appraisal pause my deadlines?", "Don’t assume it does. Whether appraisal affects any policy deadline depends on the policy and the law. Keep tracking every date and ask an attorney if one is near."),
        ],
    },
    {
        "slug": "appraisal-readiness-quiz", "name": "Appraisal Readiness Quiz", "kind": "Checklist", "photo": "signing",
        "title": "Appraisal Readiness Quiz | Is Your Claim File Ready?",
        "desc": "Ten weighted questions that score your claim file for appraisal and build a to-do list of the documents and steps you’re still missing.",
        "h1": "Appraisal Readiness Quiz",
        "lede": "Answer ten yes-or-no questions. You’ll get a weighted readiness score and a personal to-do list before you demand appraisal.",
        "short": "Ten questions, a weighted score and a to-do list before you demand appraisal.",
        "markup": QUIZ,
        "explain": """<h2>Why readiness matters</h2>
<p>Once appraisal is demanded, the process moves on its own schedule. Appraisers inspect, compare estimates and, if needed, take open items to an umpire. A file missing the carrier’s full estimate, a competing estimate or dated photos tends to produce a weaker award, no matter how real the damage is.</p>
<h3>How the score is weighted</h3>
<p>Three questions carry the most weight because appraisal can’t really start without them: accepted coverage, the carrier’s line-item estimate and your own detailed estimate. Policy knowledge, photos, receipts and deductibles come next. Timing and repair status round it out.</p>
<h3>What to do with your score</h3>
<ul><li><strong>75 or above:</strong> your file is in good shape. The next question is whether the gap justifies the cost; try the <a href="/claim-toolkit/claim-gap-calculator/">claim gap calculator</a>.</li><li><strong>45–74:</strong> close the gaps on your list first.</li><li><strong>Under 45:</strong> hold off. Start with our guide to <a href="/field-notes/building-a-claim-file-before-appraisal/">building a claim file</a>.</li></ul>
<p>Your answers stay in your browser and disappear when you leave the page.</p>""",
        "faqs": [
            ("Is a high score a guarantee?", "No. It means your file has the pieces an appraisal panel expects. The outcome still depends on the evidence, the estimates and the policy."),
            ("What if the insurer denied the whole claim?", "Appraisal usually addresses the amount of a covered loss, not whether there is coverage. A full denial is a question for a Montana attorney."),
            ("Can I retake the quiz?", "Yes. Use ‘Start over’ any time. Nothing is saved between visits."),
        ],
    },
    {
        "slug": "roof-snow-load-estimator", "name": "Roof Snow Load Estimator", "kind": "Estimator", "photo": "snow-roof-icicles",
        "title": "Roof Snow Load Estimator | Pounds Per Square Foot",
        "desc": "Estimate roof snow load layer by layer, from powder to ice, compare it with your roof’s design load and see the total weight in plain terms.",
        "h1": "Roof Snow Load Estimator for Montana Winters",
        "lede": "Snow weight depends on what kind of snow it is. Add each layer on your roof to estimate the load in pounds per square foot and compare it with a design figure.",
        "short": "Layer-by-layer roof snow weight in psf, compared with a design load.",
        "markup": SNOW,
        "explain": """<h2>Depth isn’t weight</h2>
<p>A foot of fresh powder might weigh around 7 pounds per square foot. A foot of wet spring snow can weigh several times that, and an inch of ice adds almost 5 psf on its own. That’s why roofs in Montana mountain towns often struggle after a rain-on-snow event or a March storm rather than in the deepest part of January. This estimator multiplies each layer’s depth by a typical density and adds them up.</p>
<h3>Using the result</h3>
<ul><li><strong>Design load:</strong> buildings are designed for a roof snow load that varies with location, elevation and exposure. Your local building department or an engineer can tell you the right number; the default here is illustrative.</li><li><strong>Drifts:</strong> snow piles up against walls, in valleys and below higher roofs, so some areas carry far more than the average.</li><li><strong>Safety first:</strong> sagging, cracking sounds or doors that stick can be warning signs. Get people out and call a professional. Don’t climb onto a loaded roof.</li></ul>
<h3>When snow becomes a claim</h3>
<p>Collapse, ice dams and water damage from snow are common Montana winter claims, and how the policy treats them depends on its wording. Our <a href="/claim-services/snow-load-ice-dam-freeze-claims/">snow load and ice dam claim</a> page explains how appraisal fits. Densities are typical values, and the result is a rough, illustrative estimate, not an engineering assessment.</p>""",
        "faqs": [
            ("How accurate are the snow densities?", "They are typical ranges for each snow type. Real density varies with temperature, wind and time. For a precise number, a snow core can be weighed, but only when it’s safe to do so."),
            ("What is a normal design snow load in Montana?", "It varies widely, from moderate values on the eastern plains to much higher values in mountain communities. Ask your local building department; we don’t publish a single figure because it depends on the site."),
            ("Will insurance cover a snow load collapse?", "Many policies cover collapse caused by the weight of snow or ice, subject to their terms and exclusions. Read your policy’s collapse and roof provisions, and get the carrier’s position in writing."),
        ],
    },
]

TOOL_BY = {t["slug"]: t for t in TOOLS}
