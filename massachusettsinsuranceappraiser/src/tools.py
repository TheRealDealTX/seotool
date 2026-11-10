"""Free claim estimators: markup + explanatory copy. Logic lives in static/assets/js/app.js (data-tool hooks)."""

B = "/estimators/"

GAP_FULL = """
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Award gap &amp; fee estimator</span><i>Private · runs in your browser</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Carrier’s estimate (RCV total)</label><input id="g-ins" name="insurer" inputmode="decimal" value="23600"><span class="hint">Replacement cost before depreciation and deductible.</span></div>
        <div><label for="g-own">Your estimate (RCV total)</label><input id="g-own" name="yours" inputmode="decimal" value="38900"><span class="hint">Contractor or independent line-item estimate.</span></div>
      </div>
      <div><label for="g-land">Where in the gap might the award settle?</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% means the carrier’s number stands; 100% means your full number is awarded. Test several points.</span></div>
      <div class="row2">
        <div><label for="g-ft">Appraiser fee structure</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of the increase (%)</option></select></div>
        <div><label for="g-fee">Fee amount</label><input id="g-fee" name="fee" inputmode="decimal" value="3000"></div>
      </div>
      <label class="check"><input type="checkbox" name="useump" checked> Add my half of an umpire’s fee</label>
      <div><label for="g-ump">Umpire’s total fee (split evenly)</label><input id="g-ump" name="umpire" inputmode="decimal" value="3500"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated net increase after costs</small><b data-o="net">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s-a"></span><span class="s-b"></span><span class="s-c"></span></div>
      <div class="legend"><span><i class="s-a"></i>Carrier’s number</span><span><i class="s-b"></i>Net gain to you</span><span><i class="s-c"></i>Appraisal costs</span></div>
      <div class="out-rows">
        <div><span>Disputed amount</span><b data-o="gap">$0</b></div>
        <div><span>Gap vs. carrier estimate</span><b data-o="pct">—</b></div>
        <div><span>Projected award (RCV)</span><b data-o="award">$0</b></div>
        <div><span>Increase before costs</span><b data-o="gain">$0</b></div>
        <div><span>Your share of costs</span><b data-o="cost">$0</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

GAP_MINI = """
<div class="tool tool-mini" data-tool="gap">
  <div class="tool-head"><span>60-second gap check</span><i>Nothing is stored</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="m-ins">Carrier’s estimate</label><input id="m-ins" name="insurer" inputmode="decimal" value="17800"></div>
      <div><label for="m-own">Your contractor’s estimate</label><input id="m-own" name="yours" inputmode="decimal" value="31200"></div>
      <div><label for="m-land">Award settles at</label><div class="range"><input id="m-land" type="range" name="land" min="0" max="100" step="5" value="50" data-unit="%"><output>50%</output></div><span class="hint">of the disputed amount</span></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Disputed amount</small><b data-o="gap">$0</b></div>
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
  <div class="tool-head"><span>RCV / ACV holdback calculator</span><i>Add a row for each damaged item</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Asphalt shingle roof, ice & water shield", 21400, 12, 30), ("Kitchen ceiling drywall & paint", 3100, 7, 15), ("Hardwood floor refinish — dining room", 2650, 10, 25), ("Cedar shingle siding — north wall", 4800, 18, 35)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn ghost small" data-add data-run>+ Add item</button></div>
      <div class="row2">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="1000"></div>
        <div><label for="d-cap">Depreciation cap</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="90">90%</option></select><span class="hint">Estimates usually stop depreciating at a ceiling — check yours.</span></div>
      </div>
      <label class="check"><input type="checkbox" name="nonrec"> My policy pays actual cash value only (depreciation is not recoverable)</label>
    </div>
    <div class="tool-out tool-out-grid" aria-live="polite">
      <div class="out-big"><small>First payment (ACV − deductible)</small><b data-o="first">$0</b></div>
      <div class="out-big"><small>Holdback released after repairs</small><b data-o="held">$0</b></div>
      <div class="out-big"><small>Total once fully recovered</small><b data-o="total">$0</b></div>
      <div class="out-rows span-all">
        <div><span>Replacement cost (RCV)</span><b data-o="rcv">$0</b></div>
        <div><span>Total depreciation</span><b data-o="dep">$0</b></div>
        <div><span>Depreciation share of RCV</span><b data-o="deppct">0%</b></div>
        <div><span>Actual cash value (ACV)</span><b data-o="acv">$0</b></div>
      </div>
    </div>
  </div>
</div>"""

ROOF = """
<div class="tool" data-tool="roof">
  <div class="tool-head"><span>Roof area &amp; pitch converter</span><i>Check the carrier’s squares</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <fieldset class="plain"><legend class="sr-only">Measurement method</legend>
        <div class="btn-row">
          <label class="check"><input type="radio" name="mode" value="dims" checked> Length × width of the house</label>
          <label class="check"><input type="radio" name="mode" value="area"> I already know the footprint area</label>
        </div></fieldset>
      <div class="row2" data-mode="dims">
        <div><label for="r-l">Footprint length (ft)</label><input id="r-l" name="len" inputmode="decimal" value="44"></div>
        <div><label for="r-w">Footprint width (ft)</label><input id="r-w" name="wid" inputmode="decimal" value="28"></div>
      </div>
      <div data-mode="dims"><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="10"></div>
      <div data-mode="area" hidden><label for="r-a">Footprint area incl. overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="1450"></div>
      <div class="row2">
        <div><label for="r-p">Roof pitch (rise per 12 in)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 9 else "", p) for p in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 18]) + """</select></div>
        <div><label for="r-wst">Waste allowance</label><select id="r-wst" name="waste"><option value="10">10% — plain gable (Cape)</option><option value="12" selected>12% — gable with dormers</option><option value="15">15% — hip roof</option><option value="18">18% — Victorian / cut-up</option></select></div>
      </div>
      <div><label for="r-pr">Installed price per square (optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 650"><span class="hint">Use a local contractor’s quote for a rough replacement figure.</span></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Roof squares before waste</small><b data-o="sq">0</b></div>
      <div class="out-rows">
        <div><span>Pitch multiplier</span><b data-o="mult">1.000</b></div>
        <div><span>Sloped roof surface</span><b data-o="surface">0</b></div>
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
  <div class="tool-head"><span>Hurricane deductible calculator</span><i>Percentage vs. flat</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling limit (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="640000"><span class="hint">Printed on your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Hurricane / named-storm deductible</label><select id="w-p" name="pct"><option value="1">1%</option><option value="2" selected>2%</option><option value="3">3%</option><option value="5">5%</option></select></div>
        <div><label for="w-f">All-other-perils deductible</label><input id="w-f" name="flat" inputmode="decimal" value="1000"></div>
      </div>
      <div><label for="w-l">Estimated wind damage</label><input id="w-l" name="loss" inputmode="decimal" value="27500"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your percentage deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s-c"></span><span class="s-a"></span></div>
      <div class="legend"><span><i class="s-c"></i>Paid by you</span><span><i class="s-a"></i>Paid by the policy</span></div>
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
  <div class="tool-head"><span>Claim calendar builder</span><i>Download as .ics</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
      <p class="hint flush">Change each window to match your policy and letters. Defaults are common figures, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report the claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="2"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="10"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Often counted from the carrier’s request.</span></div>
        <div><label for="t-r">Depreciation recovery (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="180"></div>
        <div><label for="t-s">Suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="730"><span class="hint">Two years = 730 days. Check your policy.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download calendar (.ics)</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the carrier accepted coverage for at least part of the loss?", "Get coverage acceptance in writing. If the claim was denied, speak with a Massachusetts attorney before thinking about appraisal."),
    (3, "Do you have the carrier’s full line-item estimate, not just a payment letter?", "Ask the adjuster in writing for the complete itemized estimate, including the price list date."),
    (3, "Do you have an independent line-item estimate of your own?", "Get an itemized estimate from a contractor or estimator — a one-line bid carries little weight with a panel."),
    (2, "Were photos taken soon after the loss, with dates?", "Collect every photo and video, note the date each was taken, and add photos of current conditions."),
    (2, "Have you found the appraisal or “reference” wording in your policy?", "Read the conditions section for the appraisal or reference paragraph and note any time limits."),
    (2, "Do you know the date your policy’s lawsuit window closes?", "Find the suit-limitation wording and put the date in a calendar — our claim calendar builder can help."),
    (2, "Were temporary repairs (tarps, water removal, heat) done and receipts kept?", "Finish reasonable temporary repairs and keep every receipt and invoice."),
    (1, "Do you have the current declarations page?", "Download or request the declarations page that was in force on the date of loss."),
    (2, "Has hidden damage (attic, wall cavities, subfloor) been opened and documented?", "Make sure wet insulation, sheathing and framing have been inspected so the scope is complete."),
    (1, "Are your emails and letters with the carrier in date order?", "Organize correspondence and claim notes chronologically."),
    (2, "Is the gap between estimates more than about 10% or $5,000?", "Run both numbers through the award gap estimator — a small gap may not justify appraisal costs."),
    (1, "If the carrier asked for a sworn proof of loss, was it sent on time?", "If a proof of loss was requested, return it before the deadline in the request letter."),
]

READY = """
<div class="tool tool-wide" data-tool="ready">
  <div class="tool-head"><span>Appraisal file checkup</span><i>12 questions · two minutes</i></div>
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
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#e3e7ee" stroke-width="18"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#e07a4f" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3" style="transition:stroke-dashoffset .5s,stroke .3s"/></svg>
        <div class="gauge-num"><span data-o="score">–</span></div>
        <p class="hint center">Answered <span data-o="count">0 / 12</span></p>
      </div>
      <div>
        <p class="out-msg" data-o="verdict"></p>
        <p class="todo-h">Still to do</p>
        <ul data-o="todo" class="todo"></ul>
      </div>
    </div>
  </div>
</div>"""

SNOW = """
<div class="tool" data-tool="snow">
  <div class="tool-head"><span>Roof snow load estimator</span><i>Rule-of-thumb weights</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row3">
        <div><label for="s-f">Fresh, fluffy snow (in)</label><input id="s-f" name="fresh" inputmode="decimal" value="14"></div>
        <div><label for="s-p">Packed / wet snow (in)</label><input id="s-p" name="packed" inputmode="decimal" value="8"></div>
        <div><label for="s-i">Ice layer (in)</label><input id="s-i" name="ice" inputmode="decimal" value="1"></div>
      </div>
      <div class="row2">
        <div><label for="s-a">Roof area (sq ft)</label><input id="s-a" name="area" inputmode="decimal" value="1600"><span class="hint">The roof area converter can give you this.</span></div>
        <div><label for="s-d">Reference capacity (lb per sq ft)</label><input id="s-d" name="design" inputmode="decimal" value="30"><span class="hint">Illustrative default. Your building’s real capacity can be higher or lower — ask an engineer.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated load on the roof</small><b data-o="psf">0 psf</b></div>
      <div class="meter" aria-hidden="true"><span data-o="bar"></span></div>
      <div class="out-rows">
        <div><span>Total weight on the roof</span><b data-o="lbs">0 lb</b></div>
        <div><span>Share of reference capacity</span><b data-o="share">0%</b></div>
        <div><span>Equivalent in compact cars (~3,000 lb)</span><b data-o="cars">0</b></div>
      </div>
      <p class="out-msg" data-o="snowmsg"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "appraisal-award-gap-estimator", "name": "Award Gap & Fee Estimator", "icon": "Δ", "kind": "Estimator", "kw": "appraisal award estimator",
        "short": "Size the dispute, test where an award could settle and subtract appraiser and umpire costs.",
        "title": "Appraisal Award Estimator | Net Gain After Fees (MA)",
        "desc": "Free appraisal award estimator for Massachusetts claims: compare both estimates, test award outcomes and subtract appraiser and umpire fees.",
        "h1": "Appraisal Award Estimator: What Would You Net After Fees?",
        "lede": "Enter the carrier’s number and yours, slide the award between them, and add realistic costs. You’ll see whether appraisal is likely to leave you ahead.",
        "markup": GAP_FULL,
        "explain": """
<h2>Read the result as a range, not a promise</h2>
<p>Panels rarely adopt either side’s opening figure. Line items backed by measurements, photos and local pricing tend to survive; padded or unsupported items tend to fall away. Run the slider at 30%, 50% and 75%. If appraisal only pays off near 100%, the file is fragile. If it still pays at 40%, it is worth a conversation.</p>
<h2>Fee structures you may be quoted</h2>
<ul><li><strong>Flat fee</strong> — a fixed amount for the engagement, sometimes with a separate inspection charge.</li>
<li><strong>Percentage of the increase</strong> — a share of the amount the award adds over the carrier’s estimate. Some policies and courts look closely at whether a contingent arrangement is consistent with an appraiser being “disinterested,” so ask how the fee is set before you sign.</li>
<li><strong>Umpire</strong> — usually split evenly between you and the carrier, and only needed if the two appraisers can’t agree.</li></ul>
<div class="note"><b class="h">Illustrative only</b>The default figures are examples, not typical results. Your numbers depend on your policy, your documentation and the panel.</div>
<h2>What isn’t in the math</h2>
<p>Deductibles, depreciation timing, policy limits and sub-limits change what you are <em>paid</em>, not the size of the dispute. For holdback timing, use the <a href="/estimators/rcv-acv-holdback-calculator/">RCV / ACV holdback calculator</a>; for coastal wind claims, try the <a href="/estimators/hurricane-deductible-calculator/">hurricane deductible calculator</a>.</p>
""",
        "faqs": [("Does a higher slider setting mean a stronger case?", "No. The slider is a what-if. Strength comes from documentation, accurate scope and current local pricing."), ("Who pays the umpire?", "Most policies split the umpire’s fee evenly between you and the insurer. Each side pays its own appraiser."), ("Is this an appraisal of my claim?", "No. It’s a planning calculator. An appraisal requires an inspection and a line-item estimate.")],
    },
    {
        "slug": "rcv-acv-holdback-calculator", "name": "RCV / ACV Holdback Calculator", "icon": "ACV", "kind": "Calculator", "kw": "RCV ACV depreciation calculator",
        "short": "Split replacement cost into the first ACV check and the depreciation released after repairs.",
        "title": "RCV vs ACV Depreciation & Holdback Calculator",
        "desc": "List damaged items with age and expected life to estimate your first ACV payment, the recoverable depreciation held back and your total.",
        "h1": "RCV vs. ACV Depreciation and Holdback Calculator",
        "lede": "Replacement cost policies usually pay twice: an actual cash value check now and the held-back depreciation once repairs are finished. Add your items to see the split.",
        "markup": DEP,
        "explain": """
<h2>The method behind the numbers</h2>
<p>Each row uses straight-line depreciation — age divided by expected life — limited by the cap you choose. Carrier estimates may instead apply condition-based percentages, treat some items as non-depreciable (permits, debris removal) or depreciate labor differently, so expect differences of a few points either way.</p>
<h2>Life expectancies that come up in New England estimates</h2>
<div class="table-wrap"><table><thead><tr><th>Item</th><th>Range often used</th></tr></thead><tbody>
<tr><th>Architectural asphalt shingles</th><td>25–30 years</td></tr><tr><th>Natural slate</th><td>60–100+ years</td></tr><tr><th>Red or white cedar shingle siding</th><td>25–40 years</td></tr><tr><th>Interior paint</th><td>8–12 years</td></tr><tr><th>Oil or gas boiler</th><td>20–30 years</td></tr><tr><th>Wall-to-wall carpet</th><td>8–12 years</td></tr>
</tbody></table></div>
<h2>Getting the holdback released</h2>
<p>Policies typically release recoverable depreciation after repairs are complete, often within a set number of days. Send final invoices and photos of finished work, and put the date in the <a href="/estimators/claim-calendar-builder/">claim calendar builder</a> so it doesn’t slip past.</p>
""",
        "faqs": [("Is depreciation on labor allowed?", "It depends on the policy wording and evolving case law. Ask the carrier to explain in writing how labor was treated in your estimate."), ("What happens if I don’t rebuild?", "Under most replacement cost policies you keep the ACV payment but may give up the held-back depreciation."), ("Why does slate depreciate so little?", "Natural slate can last a century or more, so a few decades of age is a small share of its expected life.")],
    },
    {
        "slug": "roof-area-pitch-converter", "name": "Roof Area & Pitch Converter", "icon": "▲", "kind": "Converter", "kw": "roof squares calculator",
        "short": "Turn a house footprint into sloped roof squares with pitch and waste, then compare to the estimate.",
        "title": "Roof Squares Calculator with Pitch & Waste | MA Claims",
        "desc": "Convert a footprint into roof squares using pitch and waste factors, then compare your result with the squares on a carrier’s roof estimate.",
        "h1": "Roof Squares Calculator: Convert Footprint, Pitch and Waste",
        "lede": "Steep Capes, Colonials and Victorians carry far more roof than their footprint suggests. Convert the footprint to true squares and check the carrier’s measurement.",
        "markup": ROOF,
        "explain": """
<h2>Why pitch changes everything</h2>
<p>A roof square is 100 square feet of sloped surface. A 9/12 roof — common on older Massachusetts Colonials — has about 25% more surface than its flat footprint, and a 12/12 Cape roof about 41% more. If an estimate seems to price the footprint rather than the slope, the shortfall can be large.</p>
<h2>Waste and accessories</h2>
<p>Waste covers cutting at hips, valleys, dormers and rakes. A plain gable might need 10%; a cut-up Victorian with turrets and dormers can run 18% or more. Separate line items usually cover starter, ridge cap, drip edge and — important in this climate — ice and water shield along the eaves and in valleys.</p>
<h2>Steep and high roofs</h2>
<p>Estimating programs typically add steep charges from about 7/12 or 8/12 and high-roof charges for two stories and up. Triple-deckers and tall Victorians often qualify for both. Compare your result with the carrier’s numbers, then see our <a href="/what-we-appraise/roof-hail-damage-appraisal/">roof and hail claim appraisal</a> page if the gap is significant.</p>
""",
        "faqs": [("Is the carrier’s satellite measurement reliable?", "Aerial reports are usually close, but they can miss dormers, low-slope sections or overhangs hidden by trees. A field measurement settles disagreements."), ("Why are bundles rounded up?", "Shingles come in bundles, typically three per square, so you can’t buy a fraction."), ("Does this work for slate?", "The squares math is the same, but slate is priced very differently. Use a slate contractor’s per-square price.")],
    },
    {
        "slug": "hurricane-deductible-calculator", "name": "Hurricane Deductible Calculator", "icon": "%", "kind": "Calculator", "kw": "hurricane deductible calculator",
        "short": "See what a 1%–5% named-storm deductible means in dollars for a coastal Massachusetts home.",
        "title": "Hurricane Deductible Calculator | Coastal MA Homes",
        "desc": "Convert a percentage hurricane or named-storm deductible into dollars and compare the payout with a flat deductible for coastal Massachusetts.",
        "h1": "Hurricane Deductible Calculator for Coastal Massachusetts",
        "lede": "On Cape Cod, the Islands and much of the coast, wind losses from a named storm may carry a percentage deductible. See what yours costs in real dollars.",
        "markup": DEDUCT,
        "explain": """
<h2>How percentage deductibles work</h2>
<p>A hurricane or named-storm deductible is a percentage of the dwelling limit (Coverage A), not of the damage. On a home insured for $640,000, a 2% deductible is $12,800 before the policy pays anything for that storm. Policies define exactly which storms trigger it and for how long, so read the endorsement.</p>
<h2>Where you’re likely to see one</h2>
<ul><li>Cape Cod and the Islands, where both private carriers and the FAIR Plan (MPIUA) commonly use them.</li>
<li>South Shore and South Coast towns close to open water.</li>
<li>Some North Shore and Boston Harbor neighborhoods, depending on the carrier and distance to the shore.</li></ul>
<div class="note"><b class="h">Nor’easters are different</b>A nor’easter is usually not a named storm, so the all-other-perils deductible may apply instead. The trigger wording in your policy decides.</div>
<h2>Why the deductible matters in appraisal</h2>
<p>Appraisal sets the amount of loss; the deductible is applied afterward. When a percentage deductible is large, a few missed line items can decide whether any payment is owed at all. See <a href="/what-we-appraise/hurricane-noreaster-appraisal/">hurricane and nor’easter claim appraisal</a> for how we approach coastal wind losses.</p>
""",
        "faqs": [("Is the percentage based on my damage?", "No. It’s based on the dwelling coverage limit shown on your declarations page."), ("Does it apply to flood damage?", "Flood is excluded from standard homeowner policies and is covered, if at all, by a separate flood policy with its own deductible."), ("Can I lower it?", "Some carriers offer lower percentages for a higher premium or after mitigation such as storm shutters. Ask your agent.")],
    },
    {
        "slug": "claim-calendar-builder", "name": "Claim Calendar Builder", "icon": "◷", "kind": "Planner", "kw": "insurance claim deadline calendar",
        "short": "Turn your date of loss into dated claim milestones and download them to your calendar.",
        "title": "Insurance Claim Deadline Calendar (.ics) | Massachusetts",
        "desc": "Enter your date of loss to build a dated list of claim milestones — notice, repairs, proof of loss, holdback and suit date — then export .ics.",
        "h1": "Insurance Claim Deadline Calendar Builder",
        "lede": "Claims are lost on dates as often as on dollars. Build a dated checklist from your date of loss and drop it straight into your phone’s calendar.",
        "markup": DATES,
        "explain": """
<h2>Milestones worth tracking</h2>
<ol><li><strong>Notice</strong> — policies ask for prompt notice. Report as soon as you can; the target here is your own.</li>
<li><strong>Temporary repairs</strong> — tarps, water extraction and heat to prevent freezing protect the property and the claim.</li>
<li><strong>Proof of loss</strong> — if the carrier requests a sworn proof of loss, the clock often runs from that request.</li>
<li><strong>Depreciation recovery</strong> — replacement cost policies commonly require repairs within a set time to release holdback.</li>
<li><strong>Suit limitation</strong> — many Massachusetts policies limit lawsuits to two years. Confirm your wording and talk to an attorney well before it arrives.</li></ol>
<div class="note"><b class="h">Not legal advice</b>Deadlines depend on your policy, your letters and the law. Appraisal does not automatically pause a suit-limitation clock.</div>
<h2>How the export works</h2>
<p>The download is a standard .ics file built in your browser. Open it on a phone or computer and each milestone becomes an all-day event. Nothing is sent to us. Next, check whether your file is ready with the <a href="/estimators/appraisal-file-checkup/">appraisal file checkup</a>.</p>
""",
        "faqs": [("Is my date of loss saved anywhere?", "No. The calendar is created entirely in your browser and nothing is transmitted."), ("Which date should I use after a multi-day nor’easter?", "Use the date the damage occurred if you know it; otherwise use the date in the carrier’s claim file and note the storm dates."), ("Can I change the windows later?", "Yes. Edit any number and the list and download update immediately.")],
    },
    {
        "slug": "appraisal-file-checkup", "name": "Appraisal File Checkup", "icon": "✓", "kind": "Scorecard", "kw": "appraisal readiness checklist",
        "short": "Twelve yes/no questions that score your documentation and list what to fix before appraisal.",
        "title": "Appraisal Readiness Checklist & Score | Free Checkup",
        "desc": "Answer 12 yes-or-no questions to score how ready your property claim file is for appraisal and get a to-do list of the documentation gaps.",
        "h1": "Appraisal Readiness Checklist: Score Your Claim File",
        "lede": "A panel can only value what you can show. Score your file in two minutes and get a short list of what to gather before anyone invokes appraisal.",
        "markup": READY,
        "explain": """
<h2>How the score is weighted</h2>
<p>Questions about coverage, the carrier’s itemized estimate and your own itemized estimate count most, because without them there is nothing for a panel to compare. Photos, policy wording and deadlines come next. Organization items count least but still save time and fees.</p>
<h2>What a strong file looks like</h2>
<ul><li>Coverage accepted in writing, with the carrier’s full line-item estimate.</li>
<li>An independent estimate with measurements, photos and current local pricing.</li>
<li>Dated photos from right after the loss, plus current conditions.</li>
<li>The policy, declarations page and a dated timeline of letters and calls.</li></ul>
<h2>Next steps</h2>
<p>Scored under 45? Work the to-do list first. Scored 75 or more? Size the dispute with the <a href="/estimators/appraisal-award-gap-estimator/">award gap estimator</a> and read the <a href="/appraisal-roadmap/">appraisal roadmap</a>.</p>
""",
        "faqs": [("Is a high score a guarantee?", "No. It means your paperwork is in order. The outcome still depends on the facts and the panel."), ("Why does coverage acceptance matter so much?", "Appraisal resolves the amount of a covered loss. If coverage is denied, appraisal usually isn’t the right tool."), ("Are my answers saved?", "No. Everything stays in your browser and resets when you leave the page.")],
    },
    {
        "slug": "roof-snow-load-estimator", "name": "Roof Snow Load Estimator", "icon": "❄", "kind": "Estimator", "kw": "roof snow load calculator",
        "short": "Estimate the weight of fresh snow, packed snow and ice on your roof after a Massachusetts storm.",
        "title": "Roof Snow Load Calculator | Massachusetts Winters",
        "desc": "Estimate pounds per square foot and total weight of snow and ice on your roof using common rules of thumb, then compare with a reference load.",
        "h1": "Roof Snow Load Calculator for Massachusetts Homes",
        "lede": "After back-to-back storms, the weight on a roof can climb fast — especially once rain soaks the snowpack. Get a rough read using common rules of thumb.",
        "markup": SNOW,
        "explain": """
<h2>The rules of thumb used</h2>
<p>Snow weight varies with density, so public-safety guidance often uses approximations: roughly 10–12 inches of fresh snow, 3–5 inches of old packed snow, or about 1 inch of ice each weigh around 5 pounds per square foot. This estimator uses 0.5 psf per inch of fresh snow, 1.25 psf per inch of packed or wet snow and 5 psf per inch of ice.</p>
<div class="table-wrap"><table><thead><tr><th>Layer</th><th>Approximate weight</th></tr></thead><tbody>
<tr><th>Fresh, dry snow</th><td>~0.5 lb per sq ft per inch</td></tr><tr><th>Packed or rain-soaked snow</th><td>~1.25 lb per sq ft per inch</td></tr><tr><th>Ice</th><td>~5 lb per sq ft per inch</td></tr>
</tbody></table></div>
<h2>Why the reference capacity is only a placeholder</h2>
<p>Real capacity depends on framing, span, age, condition, drifting and the code in force when the building was built. The 30 psf default is illustrative. Flat and low-slope commercial roofs, drifts beside parapets and older barns deserve a professional look. Never climb onto a loaded roof; snow removal is a job for insured professionals.</p>
<h2>When snow becomes a claim</h2>
<p>Sagging ceilings, doors that suddenly stick, cracking sounds and new leaks can signal stress. If damage occurs, photograph it, mitigate safely and see <a href="/what-we-appraise/ice-dam-snow-load-appraisal/">ice dam and snow load claim appraisal</a> for how collapse and ice dam losses are valued.</p>
""",
        "faqs": [("Is this an engineering assessment?", "No. It’s a rough estimate based on public rules of thumb. Only a qualified engineer can assess a roof’s capacity."), ("Why does rain on snow matter so much?", "Snow acts like a sponge. Rain adds weight without melting much of the pack, which is why loads spike after a rain-on-snow event."), ("Does insurance cover roof collapse from snow?", "Many policies cover collapse caused by the weight of ice or snow, subject to the policy’s terms. Check your collapse wording.")],
    },
]
