"""Interactive claim worksheets: markup + explanatory copy. Logic lives in static/assets/js/app.js."""

GAP_FULL = """
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Claim gap &amp; fee estimator</span><i>Runs in your browser</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Carrier’s estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="22600"><span class="hint">Replacement cost total on the insurer’s estimate.</span></div>
        <div><label for="g-own">Your estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="38900"><span class="hint">Your contractor’s or independent estimate.</span></div>
      </div>
      <div><label for="g-land">Where might the award land inside the gap?</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% means the carrier’s figure holds; 100% means your full figure is awarded. Panels often land in between.</span></div>
      <div class="row2">
        <div><label for="g-ft">Your appraiser’s fee basis</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of the increase (%)</option></select></div>
        <div><label for="g-fee">Fee amount</label><input id="g-fee" name="fee" inputmode="decimal" value="2800"></div>
      </div>
      <label class="check"><input type="checkbox" name="useump" checked> Include my half of an umpire’s fee</label>
      <div><label for="g-ump">Umpire’s total fee (split 50/50)</label><input id="g-ump" name="umpire" inputmode="decimal" value="3200"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated net increase to you</small><b data-o="net">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s-a"></span><span class="s-b"></span><span class="s-c"></span></div>
      <div class="legend"><span><i class="s-a"></i>Carrier’s figure</span><span><i class="s-b"></i>Your net gain</span><span><i class="s-c"></i>Appraisal costs</span></div>
      <div class="out-rows">
        <div><span>Amount in dispute</span><b data-o="gap">$0</b></div>
        <div><span>Gap as % of carrier estimate</span><b data-o="pct">—</b></div>
        <div><span>Projected award (RCV)</span><b data-o="award">$0</b></div>
        <div><span>Gross increase</span><b data-o="gain">$0</b></div>
        <div><span>Your appraisal costs</span><b data-o="cost">$0</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

GAP_MINI = """
<div class="tool" data-tool="gap" style="margin:0">
  <div class="tool-head"><span>60-second gap check</span><i>Nothing is stored</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="m-ins">Carrier’s estimate</label><input id="m-ins" name="insurer" inputmode="decimal" value="17800"></div>
      <div><label for="m-own">Your contractor’s estimate</label><input id="m-own" name="yours" inputmode="decimal" value="31400"></div>
      <div><label for="m-land">Award lands at</label><div class="range"><input id="m-land" type="range" name="land" min="0" max="100" step="5" value="50" data-unit="%"><output>50%</output></div><span class="hint">of the disputed amount (illustrative)</span></div>
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
  <div class="tool-head"><span>RCV / ACV &amp; holdback calculator</span><i>Add as many lines as you need</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Architectural shingle roof", 21400, 11, 30), ("Vinyl siding — two elevations", 6300, 14, 40), ("Hardwood floor — first level", 9800, 8, 50)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn ghost small" data-add data-run>+ Add a line</button></div>
      <div class="row2">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="1500"></div>
        <div><label for="d-cap">Depreciation cap</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="90">90%</option></select><span class="hint">Many estimates cap depreciation; check yours.</span></div>
      </div>
      <label class="check"><input type="checkbox" name="nonrec"> My policy pays actual cash value only (no recoverable depreciation)</label>
    </div>
    <div class="tool-out" aria-live="polite" style="grid-template-columns:repeat(auto-fit,minmax(190px,1fr))">
      <div class="out-big"><small>First payment (ACV − deductible)</small><b data-o="first">$0</b></div>
      <div class="out-big"><small>Held back until repairs</small><b data-o="held">$0</b></div>
      <div class="out-big"><small>Total if fully recovered</small><b data-o="total">$0</b></div>
      <div class="out-rows" style="grid-column:1/-1">
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
  <div class="tool-head"><span>Roof pitch &amp; squares calculator</span><i>Check the carrier’s square count</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <fieldset class="plain-fs"><legend class="sr-only">Measurement method</legend>
        <div class="btn-row">
          <label class="check"><input type="radio" name="mode" value="dims" checked> Footprint length × width</label>
          <label class="check"><input type="radio" name="mode" value="area"> I know the footprint area</label>
        </div></fieldset>
      <div class="row2" data-mode="dims">
        <div><label for="r-l">Footprint length (ft)</label><input id="r-l" name="len" inputmode="decimal" value="52"></div>
        <div><label for="r-w">Footprint width (ft)</label><input id="r-w" name="wid" inputmode="decimal" value="30"></div>
      </div>
      <div data-mode="dims"><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="12"></div>
      <div data-mode="area" hidden><label for="r-a">Footprint area incl. overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="1900"></div>
      <div class="row2">
        <div><label for="r-p">Roof pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 8 else "", p) for p in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16]) + """</select></div>
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="10">10% — plain gable</option><option value="12">12% — gable with dormers</option><option value="15" selected>15% — hip roof</option><option value="18">18% — cut-up / complex</option></select></div>
      </div>
      <div><label for="r-pr">Installed price per square (optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 560"><span class="hint">Use a local contractor’s quote for a rough figure.</span></div>
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
  <div class="tool-head"><span>Hurricane deductible calculator</span><i>Percentage vs. flat</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling coverage (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="525000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Hurricane / named-storm deductible</label><select id="w-p" name="pct"><option value="1">1%</option><option value="2" selected>2%</option><option value="3">3%</option><option value="5">5%</option><option value="10">10%</option></select></div>
        <div><label for="w-f">All-other-perils flat deductible</label><input id="w-f" name="flat" inputmode="decimal" value="1000"></div>
      </div>
      <div><label for="w-l">Estimated storm damage</label><input id="w-l" name="loss" inputmode="decimal" value="27500"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your percentage deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s-c"></span><span class="s-a"></span></div>
      <div class="legend"><span><i class="s-c"></i>You pay</span><span><i class="s-a"></i>Policy pays</span></div>
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
  <div class="tool-head"><span>Claim deadline calendar</span><i>Export to your calendar</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="t-dol">Date of loss</label><input id="t-dol" name="dol" type="date"></div>
      <div class="row2">
        <div><label for="t-n">Report the claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="3"></div>
        <div><label for="t-m">Finish temporary repairs (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="10"></div>
      </div>
      <div class="row2">
        <div><label for="t-p">Proof of loss window (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Usually counted from the insurer’s request.</span></div>
        <div><label for="t-r">Depreciation recovery window (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="180"></div>
      </div>
      <div><label for="t-s">Policy suit-limitation period (days)</label><input id="t-s" name="suit" inputmode="numeric" value="365"><span class="hint">Enter the period in your policy. Ask a Delaware attorney how it applies.</span></div>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download .ics calendar</button></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"><li><b>Pick your date of loss</b><span>Milestones will appear here.</span></li></ol>
    </div>
  </div>
</div>"""

_Q = [
    (3, "I have the insurer’s full, itemized estimate (not just the payment letter).", "Request the complete line-item estimate from your adjuster."),
    (3, "I have my own contractor or independent estimate covering the same scope.", "Get a detailed, itemized estimate from a licensed contractor or independent estimator."),
    (2, "The insurer has accepted that the loss is covered.", "Confirm coverage in writing. Appraisal resolves amount, not coverage."),
    (2, "I have dated photos of the damage taken before repairs or cleanup.", "Gather every photo and video you have and note the dates."),
    (2, "I’ve read the appraisal clause in my policy.", "Find the “Appraisal” paragraph in your policy form and read it closely."),
    (2, "I know my policy deadlines (proof of loss, depreciation recovery, suit limitation).", "Use the claim deadline calendar and confirm dates with your policy."),
    (1, "I’ve kept receipts for temporary repairs and mitigation.", "Collect receipts for tarps, drying, board-up and other emergency work."),
    (1, "The gap between the two estimates is more than a few thousand dollars.", "Run the claim gap and fee estimator to see if the gap justifies appraisal."),
    (1, "I’ve separated wind damage from any flood damage (coastal properties).", "Use the wind vs. flood split estimator and document water lines."),
    (1, "I have the declarations page showing my limits and deductibles.", "Download or request your current declarations page."),
]

READY = """
<div class="tool" data-tool="ready">
  <div class="tool-head"><span>Appraisal readiness check</span><i>10 quick questions</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <ul class="quiz">""" + "".join(
    f'<li data-w="{w}" data-fix="{fix}"><span>{q}</span><span class="yn"><button type="button" class="yes" aria-pressed="false">Yes</button><button type="button" class="no" aria-pressed="false">No</button></span></li>'
    for w, q, fix in _Q) + """</ul>
      <div class="btn-row"><button type="button" class="btn ghost small" data-reset>Reset answers</button></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="gauge"><svg viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="40" class="g-bg"/><circle cx="50" cy="50" r="40" class="g-arc" data-o="arc"/></svg><div><b data-o="score">–</b><small>Score</small></div></div>
      <p class="out-msg" data-o="verdict"></p>
      <div class="out-rows"><div><span>Answered</span><b data-o="count">0 / 10</b></div></div>
      <p class="todo-h">Still to do</p>
      <ul class="todo" data-o="todo"></ul>
    </div>
  </div>
</div>"""

SPLIT = """
<div class="tool" data-tool="split">
  <div class="tool-head"><span>Wind vs. flood split estimator</span><i>For coastal and creekside homes</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="s-t">Total building damage (repair cost)</label><input id="s-t" name="total" inputmode="decimal" value="84000"></div>
      <div><label for="s-w">Share caused by wind &amp; wind-driven rain</label>
        <div class="range"><input id="s-w" type="range" name="wind" min="0" max="100" step="5" value="45" data-unit="%"><output>45%</output></div>
        <span class="hint">The rest is treated as flood (rising water). The split is the real dispute — try several.</span></div>
      <div class="row2">
        <div><label for="s-a">Coverage A (homeowners)</label><input id="s-a" name="cova" inputmode="decimal" value="610000"></div>
        <div><label for="s-hp">Hurricane deductible</label><select id="s-hp" name="hpct"><option value="0">Flat (not a %)</option><option value="1">1%</option><option value="2">2%</option><option value="3" selected>3%</option><option value="5">5%</option></select></div>
      </div>
      <div class="row2">
        <div><label for="s-hf">Flat homeowners deductible</label><input id="s-hf" name="hflat" inputmode="decimal" value="2500"><span class="hint">Used when the deductible is flat.</span></div>
        <div><label for="s-fd">Flood policy deductible</label><input id="s-fd" name="fded" inputmode="decimal" value="5000"></div>
      </div>
      <div><label for="s-fl">Flood building coverage limit</label><input id="s-fl" name="flim" inputmode="decimal" value="250000"><span class="hint">Enter 0 if you have no flood policy.</span></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Combined payment from both policies</small><b data-o="paid">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s-a"></span><span class="s-b"></span><span class="s-c"></span></div>
      <div class="legend"><span><i class="s-a"></i>Homeowners pays</span><span><i class="s-b"></i>Flood pays</span><span><i class="s-c"></i>You pay</span></div>
      <div class="out-rows">
        <div><span>Wind portion of damage</span><b data-o="wamt">$0</b></div>
        <div><span>Homeowners deductible</span><b data-o="hded">$0</b></div>
        <div><span>Homeowners payment</span><b data-o="hpay">$0</b></div>
        <div><span>Flood portion of damage</span><b data-o="famt">$0</b></div>
        <div><span>Flood payment</span><b data-o="fpay">$0</b></div>
        <div><span>Left for you to cover</span><b data-o="oop">$0</b></div>
      </div>
      <p class="out-msg" data-o="smsg"></p>
    </div>
  </div>
</div>"""


def _faq(*qa):
    return list(qa)


TOOLS = [
    {
        "slug": "claim-gap-and-fee-estimator", "name": "Claim Gap & Fee Estimator", "kind": "Estimator", "icon": "scale", "photo": "calculator-paperwork",
        "short": "See the disputed amount, a projected award and what you keep after appraiser and umpire fees.",
        "title": "Claim Gap & Appraisal Fee Estimator | Free Tool",
        "desc": "Free claim gap estimator for Delaware property owners: compare estimates, project an award and see your net after appraiser and umpire fees.",
        "h1": "Claim Gap & Appraisal Fee Estimator",
        "lede": "Compare the carrier’s estimate with yours, choose where an award might land, and see what’s left after your appraiser and half an umpire are paid. Figures are illustrative.",
        "markup": GAP_FULL,
        "explain": """
<h2>How the estimator works</h2>
<p>The disputed amount is simply your estimate minus the carrier’s. Appraisal panels rarely award either side’s full number, so the slider lets you test outcomes anywhere in between. The tool then subtracts your appraiser’s fee (flat or percentage) and, if you tick the box, half of the umpire’s fee.</p>
<h2>Reading the result</h2>
<ul>
<li><strong>Net increase:</strong> the projected award minus the carrier’s estimate, minus your costs.</li>
<li><strong>Gap as a percentage:</strong> a quick sense of how far apart the two estimates are.</li>
<li><strong>The message:</strong> a rule-of-thumb read on whether appraisal, a supplement or a review is the logical next step.</li>
</ul>
<h2>Keep in mind</h2>
<p>These figures are illustrative only. Real awards depend on the evidence, the panel and your policy. Deductibles, depreciation and prior payments also affect what you actually receive — try the <a href="/claim-worksheets/depreciation-holdback-worksheet/">RCV/ACV holdback calculator</a> for that part.</p>
""",
        "faqs": _faq(("Where should I set the slider?", "Try several positions. A well-documented claim may land closer to your number; a weak one closer to the carrier’s. The point is to see whether appraisal still makes sense at a cautious setting."),
                     ("Are appraiser fees really that much?", "Fees vary by claim size and complexity. Enter the actual quote you receive; any appraiser should give you the fee in writing before work starts."),
                     ("Does the estimator account for my deductible?", "No. It compares estimate totals. Use the holdback calculator to see how deductibles and depreciation affect payment.")),
    },
    {
        "slug": "depreciation-holdback-worksheet", "name": "RCV / ACV Holdback Calculator", "kind": "Calculator", "icon": "file", "photo": "laptop-spreadsheet",
        "short": "Work out depreciation line by line, your first payment and the holdback you can recover after repairs.",
        "title": "RCV vs. ACV Depreciation & Holdback Calculator",
        "desc": "Free RCV vs. ACV calculator: depreciate items line by line, apply your deductible and see the first payment and the holdback recoverable later.",
        "h1": "RCV / ACV Depreciation & Holdback Calculator",
        "lede": "Most replacement cost policies pay in two stages: actual cash value first, then the depreciation holdback after repairs. Enter each item’s cost, age and expected life to see both.",
        "markup": DEP,
        "explain": """
<h2>The two-check system</h2>
<p>Replacement cost value (RCV) is what it costs to repair or replace with like kind and quality today. Actual cash value (ACV) is RCV minus depreciation. Many policies pay ACV minus the deductible first, then pay the withheld depreciation once you complete repairs within the policy’s time limit.</p>
<h2>How depreciation is estimated here</h2>
<p>The tool uses straight-line depreciation: age divided by expected life, applied to the replacement cost and capped at the percentage you choose. Real estimates may use different life tables, condition adjustments or non-depreciable items such as labor in some cases. Use the result to understand the carrier’s math, not to replace it.</p>
<h2>What to check on your own estimate</h2>
<ul>
<li>Is depreciation applied to labor, and does your policy allow it?</li>
<li>Are the ages and life expectancies reasonable for your materials?</li>
<li>Is the depreciation marked recoverable or non-recoverable?</li>
<li>How many days do you have to complete repairs and claim the holdback?</li>
</ul>
""",
        "faqs": _faq(("What is recoverable depreciation?", "It’s the depreciation withheld from your first payment that you can collect after completing repairs, if your policy pays replacement cost."),
                     ("Why does the tool cap depreciation?", "Estimates rarely depreciate items to zero. Many cap at a percentage. Choose the cap that matches your estimate."),
                     ("What if my policy is ACV only?", "Tick the box. The tool will show that no holdback is recoverable and the total equals ACV minus the deductible.")),
    },
    {
        "slug": "roof-pitch-and-squares-calculator", "name": "Roof Pitch & Squares Calculator", "kind": "Calculator", "icon": "home", "photo": "roofer-at-work",
        "short": "Convert a footprint and pitch into roof squares, waste, bundles and a rough replacement cost.",
        "title": "Roof Pitch & Squares Calculator | Free Claim Tool",
        "desc": "Free roof pitch and squares calculator: turn a footprint and pitch into roof area, squares with waste, bundles and a rough replacement figure.",
        "h1": "Roof Pitch & Squares Calculator",
        "lede": "Roof estimates are priced by the square (100 square feet). Check whether the carrier’s square count, pitch and waste factor are in the right range before you accept a roof estimate.",
        "markup": ROOF,
        "explain": """
<h2>From footprint to squares</h2>
<p>The calculator adds your eave overhang to the footprint, then multiplies by a pitch factor: the square root of 1 + (rise ÷ 12)². A 6/12 roof has a factor of about 1.118, an 8/12 about 1.202 and a 12/12 about 1.414. Divide the surface area by 100 to get squares, then add waste for cuts, hips and valleys.</p>
<h2>Why waste matters</h2>
<p>Hip roofs and cut-up roofs need more material than simple gables because of all the angled cuts. Estimates that use a low waste factor on a complex roof can understate material by several squares. Compare the waste factor in your estimate with the roof’s actual shape.</p>
<h2>Steep and high charges</h2>
<p>Estimating software typically adds labor charges for steep slopes and for roofs more than one story high. If your roof is 7/12 or steeper, look for those charges in the carrier’s estimate.</p>
<p>This tool gives a ballpark. Dormers, multiple pitches and complex geometry need real measurements or an aerial report.</p>
""",
        "faqs": _faq(("How do I find my roof pitch?", "A roofer, inspection report or aerial measurement report will list it. You can also measure the rise over a 12-inch level on the rafter or roof surface."),
                     ("Why are my squares different from the carrier’s?", "Differences in measurement, overhang, pitch or waste factor add up. Ask for the carrier’s measurement report and compare."),
                     ("Does the cost estimate include tear-off?", "Only if your price per square includes it. Use an installed price from a local contractor for the best rough figure.")),
    },
    {
        "slug": "named-storm-deductible-worksheet", "name": "Hurricane Deductible Calculator", "kind": "Calculator", "icon": "storm", "photo": "storm-clouds-shore",
        "short": "Turn a percentage hurricane or named-storm deductible into dollars and compare it with a flat deductible.",
        "title": "Hurricane Deductible Calculator | Percent to Dollars",
        "desc": "Free hurricane deductible calculator: turn a percentage named-storm deductible into dollars and compare your payout with a flat deductible.",
        "h1": "Hurricane & Named-Storm Deductible Calculator",
        "lede": "Coastal Delaware policies often carry a hurricane or named-storm deductible based on a percentage of dwelling coverage. See what that means in dollars on a real loss.",
        "markup": DEDUCT,
        "explain": """
<h2>Percentage deductibles in plain numbers</h2>
<p>A 2% hurricane deductible on a home insured for $525,000 is $10,500 — ten times a typical $1,000 flat deductible. On beach homes in Rehoboth, Bethany or Fenwick with higher dwelling limits, the dollar figure climbs quickly.</p>
<h2>When does the hurricane deductible apply?</h2>
<p>That depends entirely on your policy’s definition. Some apply when the National Weather Service names a storm or issues a hurricane watch or warning for any part of the state, and remain in effect for a set period afterward. Others apply only to damage from a hurricane itself. A tornado or nor’easter may fall under the regular deductible. Read your endorsement carefully.</p>
<h2>Why it matters for disputes</h2>
<p>When a large deductible applies, every dollar of under-scoped damage comes straight out of your pocket. A thorough estimate is the only way to recover the amount above the deductible that you’re actually owed.</p>
""",
        "faqs": _faq(("Is the deductible based on the loss or the coverage amount?", "Percentage deductibles are usually calculated on the Coverage A (dwelling) limit, not the size of the loss."),
                     ("Can I lower my hurricane deductible?", "Sometimes, at renewal, for a higher premium. Talk with your agent; it can’t be changed after a loss."),
                     ("Does the hurricane deductible apply to nor’easters?", "Usually not, unless the policy definition is broad enough to include them. Check the wording.")),
    },
    {
        "slug": "policy-deadline-calendar", "name": "Claim Deadline Calendar", "kind": "Planner", "icon": "clock", "photo": "inspector-clipboard",
        "short": "Map notice, mitigation, proof of loss, holdback and suit dates from your date of loss, then export to .ics.",
        "title": "Insurance Claim Deadline Calendar with .ics Export",
        "desc": "Free claim deadline calendar: map notice, repairs, proof of loss, depreciation and suit-limitation dates from your date of loss and export to .ics.",
        "h1": "Insurance Claim Deadline Calendar",
        "lede": "Policies are full of time limits. Enter your date of loss and the periods from your own policy, then download the milestones to your phone or computer calendar.",
        "markup": DATES,
        "explain": """
<h2>The deadlines that matter</h2>
<ul>
<li><strong>Notice:</strong> most policies require prompt notice. Report damage as soon as you can.</li>
<li><strong>Mitigation:</strong> take reasonable steps to prevent further damage and keep receipts.</li>
<li><strong>Proof of loss:</strong> many policies require a sworn proof of loss within a set number of days after the insurer’s request.</li>
<li><strong>Depreciation recovery:</strong> replacement cost policies often set a deadline for completing repairs to collect the holdback.</li>
<li><strong>Suit limitation:</strong> policies often shorten the time to file a lawsuit. Delaware law has its own limitations periods, and how they interact with policy language is a legal question for a Delaware attorney.</li>
</ul>
<h2>Using the calendar</h2>
<p>The default values are examples, not legal deadlines. Replace them with the periods in your policy and in any letters from your insurer. The .ics file works with Google Calendar, Apple Calendar and Outlook. Nothing you enter leaves your browser.</p>
""",
        "faqs": _faq(("Are the default periods legal deadlines?", "No. They’re examples. Use the periods stated in your policy and correspondence."),
                     ("Does invoking appraisal pause the suit deadline?", "Not necessarily. Ask a Delaware attorney how your policy’s suit-limitation clause applies while appraisal is underway."),
                     ("What does the .ics file contain?", "One all-day event per milestone with a short description. It’s created in your browser and downloaded directly.")),
    },
    {
        "slug": "appraisal-readiness-check", "name": "Appraisal Readiness Check", "kind": "Checklist", "icon": "doc", "photo": "consultation",
        "short": "Ten yes-or-no questions that score how prepared your claim file is for an appraisal panel.",
        "title": "Appraisal Readiness Check | 10-Question Score",
        "desc": "Free appraisal readiness check: answer 10 yes-or-no questions to score your claim file and get a to-do list before you invoke appraisal.",
        "h1": "Appraisal Readiness Check",
        "lede": "Appraisal rewards preparation. Answer ten questions to see how ready your file is and what to gather before you invoke the clause.",
        "markup": READY,
        "explain": """
<h2>What the score means</h2>
<p>Each question is weighted by how much it affects an appraisal outcome. The itemized estimates and coverage acceptance carry the most weight, because without them appraisal can’t really work. A high score means you have what a panel expects to see; a low score gives you a to-do list.</p>
<h2>Why preparation matters</h2>
<p>An appraisal award is binding on the amount of loss once two of three panel members sign. If key evidence is missing, the award may lock in a lower number than the damage deserves. It’s much easier to gather documents before appraisal than to argue about them after.</p>
<p>Your answers are not saved or sent anywhere.</p>
""",
        "faqs": _faq(("Do I need a perfect score to invoke appraisal?", "No. But each “no” answer is a gap a panel may notice. Close the important ones first."),
                     ("Why is coverage acceptance on the list?", "Appraisal decides the amount of loss, not coverage. If coverage is denied, you may need an attorney instead."),
                     ("Is my information stored?", "No. The checklist runs entirely in your browser.")),
    },
    {
        "slug": "wind-vs-flood-split-estimator", "name": "Wind vs. Flood Split Estimator", "kind": "Estimator", "icon": "drop", "photo": "flood-street",
        "short": "See how the wind-versus-flood allocation changes what your homeowners and flood policies each pay.",
        "title": "Wind vs. Flood Damage Split Estimator | Coastal",
        "desc": "Free wind vs. flood split estimator for coastal Delaware homes: see how damage allocation changes homeowners and flood payments and your share.",
        "h1": "Wind vs. Flood Damage Split Estimator",
        "lede": "When a coastal storm brings both wind and rising water, the homeowners policy and the flood policy each cover part of the damage. This tool shows how the split changes what each one pays — and what’s left for you.",
        "markup": SPLIT,
        "explain": """
<h2>Why the split matters in Delaware</h2>
<p>Coastal storms along the Delaware Bay, the Atlantic and the inland bays often bring wind damage and flood damage at the same time. Homeowners policies generally cover wind and wind-driven rain through storm-created openings and exclude flood. Flood policies cover rising water but have their own limits and deductibles. When each insurer argues the other should pay, the allocation decides your recovery.</p>
<h2>How the estimator calculates</h2>
<ul>
<li>The wind share of the total damage goes to the homeowners policy, minus the hurricane deductible (percentage of Coverage A) or a flat deductible.</li>
<li>The rest goes to the flood policy, minus its deductible and capped at its building limit.</li>
<li>Anything not paid by either policy is shown as your share.</li>
</ul>
<h2>Try different splits</h2>
<p>Move the slider and watch the payments shift. With a large hurricane deductible, a wind-heavy split may still leave you paying a lot; with no flood policy, every dollar allocated to flood is yours. That’s why documenting water lines and wind-created openings carefully is so important. All figures are illustrative.</p>
""",
        "faqs": _faq(("Can appraisal decide the wind vs. flood split?", "Sometimes appraisers value damage by cause, but whether an appraisal panel can decide causation depends on the policy and the law. Coverage disputes may need an attorney."),
                     ("Do NFIP flood policies cover contents?", "Only if you bought contents coverage. This tool looks at building damage only."),
                     ("Why does my homeowners policy pay nothing at some splits?", "If the wind portion is smaller than the hurricane deductible, the homeowners policy has nothing to pay.")),
    },
]
