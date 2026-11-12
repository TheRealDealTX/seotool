"""Interactive claim tools for Maine Insurance Appraiser: markup + copy. Logic lives in static/assets/js/app.js."""

GAP_FULL = """
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Settlement gap projector</span><i>Runs in your browser · nothing saved</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Carrier’s estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="21600"><span class="hint">Replacement cost total on the insurer’s estimate.</span></div>
        <div><label for="g-own">Your estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="34900"><span class="hint">Your contractor’s or independent line-item estimate.</span></div>
      </div>
      <div><label for="g-land">Where might the award land inside the gap?</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% means the carrier’s number holds; 100% means your full number is awarded.</span></div>
      <div class="row2">
        <div><label for="g-ft">Appraiser fee basis</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of the increase (%)</option></select></div>
        <div><label for="g-fee">Fee amount</label><input id="g-fee" name="fee" inputmode="decimal" value="2800"></div>
      </div>
      <label class="check"><input type="checkbox" name="useump" checked> Add my half of an umpire’s fee</label>
      <div><label for="g-ump">Umpire’s total fee (usually split 50/50)</label><input id="g-ump" name="umpire" inputmode="decimal" value="3200"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Projected net increase after costs</small><b data-o="net">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s1"></span><span class="s2"></span><span class="s3"></span></div>
      <div class="legend"><span><i class="s1"></i>Carrier’s number</span><span><i class="s2"></i>Your net gain</span><span><i class="s3"></i>Appraisal costs</span></div>
      <div class="out-rows">
        <div><span>Amount in dispute</span><b data-o="gap">$0</b></div>
        <div><span>Gap as share of carrier estimate</span><b data-o="pct">—</b></div>
        <div><span>Projected award (RCV)</span><b data-o="award">$0</b></div>
        <div><span>Your appraisal costs</span><b data-o="cost">$0</b></div>
      </div>
      <table class="scen"><caption>Net result if the award lands at…</caption><thead><tr><th scope="col">Landing</th><th scope="col">Award</th><th scope="col">Net to you</th></tr></thead><tbody data-o="scen"></tbody></table>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

GAP_MINI = """
<div class="tool tool-mini" data-tool="gap">
  <div class="tool-head"><span>Two-number gap check</span><i>No sign-up</i></div>
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
  <div class="tool-head"><span>RCV / ACV holdback calculator</span><i>Add a row for each damaged item</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Asphalt shingle roof, 28 squares", 19800, 11, 25), ("Ceiling drywall and paint, two bedrooms", 3150, 7, 15), ("Hardwood flooring refinish, hallway", 2600, 9, 25)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn ghost small" data-add data-run>+ Add item</button></div>
      <div class="row2">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="1000"></div>
        <div><label for="d-cap">Depreciation cap</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="90">90%</option></select><span class="hint">Many estimates cap depreciation per item.</span></div>
      </div>
      <label class="check"><input type="checkbox" name="nonrec"> My policy pays actual cash value only (no recoverable depreciation)</label>
    </div>
    <div class="tool-out tool-out-3" aria-live="polite">
      <div class="out-big"><small>First check (ACV minus deductible)</small><b data-o="first">$0</b></div>
      <div class="out-big"><small>Held back until repairs</small><b data-o="held">$0</b></div>
      <div class="out-big"><small>Total once recovered</small><b data-o="total">$0</b></div>
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
  <div class="tool-head"><span>Roof pitch &amp; squares converter</span><i>Includes an ice-barrier estimate</i></div>
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
      <div><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="12"></div>
      <div data-mode="area" hidden><label for="r-a">Footprint area incl. overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="1450"></div>
      <div class="row2">
        <div><label for="r-p">Roof pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 10 else "", p) for p in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16]) + """</select></div>
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="10">10%: plain gable</option><option value="13" selected>13%: gable with dormers or ell</option><option value="15">15%: hip roof</option><option value="18">18%: cut-up / multiple valleys</option></select></div>
      </div>
      <div><label for="r-pr">Installed price per square (optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 575"><span class="hint">Use a local contractor’s quote for a rough replacement figure.</span></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Roof squares (before waste)</small><b data-o="sq">0</b></div>
      <div class="out-rows">
        <div><span>Pitch multiplier</span><b data-o="mult">1.000</b></div>
        <div><span>Pitch angle</span><b data-o="deg">0°</b></div>
        <div><span>Roof surface area</span><b data-o="surface">0</b></div>
        <div><span>Squares to order (with waste)</span><b data-o="order">0</b></div>
        <div><span>Shingle bundles (3 per square)</span><b data-o="bundles">0</b></div>
        <div><span>Ice barrier courses at each eave</span><b data-o="iw">0</b></div>
        <div><span>Ice barrier area / 2-square rolls</span><b data-o="iwa">0</b></div>
        <div><span>Rough replacement cost</span><b data-o="cost">—</b></div>
      </div>
      <p class="out-msg" data-o="steep"></p>
    </div>
  </div>
</div>"""

DEDUCT = """
<div class="tool" data-tool="deduct">
  <div class="tool-head"><span>Percentage deductible checker</span><i>Percent vs. flat, side by side</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling coverage (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="410000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Wind, hurricane or named-storm deductible</label><select id="w-p" name="pct"><option value="1">1%</option><option value="2" selected>2%</option><option value="3">3%</option><option value="5">5%</option><option value="10">10%</option></select></div>
        <div><label for="w-f">All-other-perils flat deductible</label><input id="w-f" name="flat" inputmode="decimal" value="1000"></div>
      </div>
      <div><label for="w-l">Estimated storm damage</label><input id="w-l" name="loss" inputmode="decimal" value="17900"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your percentage deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s3"></span><span class="s1"></span></div>
      <div class="legend"><span><i class="s3"></i>You pay</span><span><i class="s1"></i>Policy pays</span></div>
      <div class="out-rows">
        <div><span>Payment with the % deductible</span><b data-o="pdpay">$0</b></div>
        <div><span>Payment if the flat deductible applied</span><b data-o="flatpay">$0</b></div>
        <div><span>Extra out of pocket from the % deductible</span><b data-o="diff">$0</b></div>
        <div><span>Damage needed before the policy pays</span><b data-o="need">$0</b></div>
      </div>
      <p class="out-msg" data-o="below"></p>
    </div>
  </div>
</div>"""

DATES = """
<div class="tool" data-tool="dates">
  <div class="tool-head"><span>Claim date tracker</span><i>Exports to your calendar (.ics)</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
      <p class="hint">Set each window to match your policy and the carrier’s letters. Defaults are common figures, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report the claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="2"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="10"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Often counted from the carrier’s written request.</span></div>
        <div><label for="t-a">Name your appraiser (days after demand)</label><input id="t-a" name="appr" inputmode="numeric" value="20"><span class="hint">Counted from today, as if appraisal were demanded now.</span></div>
        <div><label for="t-r">Depreciation recovery (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="180"></div>
        <div><label for="t-s">Suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="730"><span class="hint">Read the “Suit Against Us” condition in your policy.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download .ics calendar file</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the carrier accepted coverage for at least part of the loss, in writing?", "Get written confirmation that coverage is accepted. If the claim was denied outright, talk with a Maine attorney before considering appraisal."),
    (3, "Do you have the carrier’s complete line-item estimate, not just a summary page?", "Ask the adjuster for the full itemized estimate, including the price list date and any photo report."),
    (3, "Do you have your own line-item estimate from a contractor or estimator?", "Get an itemized estimate. A one-line contractor bid rarely holds up in front of an appraisal panel."),
    (2, "Do you have dated photos taken soon after the loss, before snow, cleanup or repairs?", "Pull every photo and video you have, note the dates, and photograph current conditions now."),
    (2, "Has hidden damage been opened up: attic, wall cavities, subfloor, decking?", "Make sure wet insulation, sheathing and framing have been inspected so the scope is complete."),
    (2, "Have you read the Appraisal paragraph in your policy’s conditions?", "Find the Appraisal condition, note any deadlines for naming an appraiser, and check how umpire costs are shared."),
    (2, "Do you know your policy’s suit-limitation date?", "Locate the “Suit Against Us” condition and put the date on your calendar with the claim date tracker."),
    (2, "Were temporary repairs made and receipts saved (tarps, water extraction, heat)?", "Finish reasonable mitigation and keep every receipt, invoice and fuel or rental bill."),
    (1, "Is your declarations page in hand?", "Download or request the current declarations page showing limits and deductibles."),
    (1, "Is your correspondence with the carrier organized by date?", "Collect emails, letters and adjuster notes in date order in one folder."),
    (2, "Is the gap between estimates more than about 10% or $5,000?", "Run both numbers through the settlement gap projector; a narrow gap may be cheaper to close with a documented supplement."),
    (1, "If the carrier asked for a sworn proof of loss, was it submitted on time?", "If a proof of loss was requested, complete and return it before the stated deadline."),
]

READY = """
<div class="tool tool-wide" data-tool="ready">
  <div class="tool-head"><span>Appraisal file strength test</span><i>12 questions · about two minutes</i></div>
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
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#e3e9f0" stroke-width="18"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#e2683c" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3"/></svg>
        <div class="gauge-num"><span data-o="score">–</span></div>
        <p class="hint center">Answered <span data-o="count">0 / 12</span></p>
      </div>
      <div>
        <p class="out-msg" data-o="verdict"></p>
        <p class="todo-h">Close these gaps first</p>
        <ul class="todo" data-o="todo"><li>Nothing flagged yet.</li></ul>
      </div>
    </div>
  </div>
</div>"""

CAMP = """
<div class="tool" data-tool="camp">
  <div class="tool-head"><span>Seasonal camp vacancy check</span><i>For camps, cottages and second homes</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="c-last">Last night someone stayed there</label><input id="c-last" type="date" name="last"></div>
        <div><label for="c-found">Date the damage was found</label><input id="c-found" type="date" name="found"></div>
      </div>
      <div class="row2">
        <div><label for="c-th">Policy’s vacancy / unoccupancy window</label><select id="c-th" name="thresh"><option value="30">30 days</option><option value="60" selected>60 consecutive days</option><option value="90">90 days</option></select><span class="hint">Check the conditions and any seasonal-dwelling endorsement.</span></div>
        <div><label for="c-chk">Someone checked the property every (days)</label><input id="c-chk" name="check" inputmode="numeric" value="14"></div>
      </div>
      <fieldset class="bare"><legend class="lbl">Freeze protection while you were away</legend>
        <label class="check"><input type="checkbox" name="heat" checked> Heat was kept on (thermostat set, fuel delivered)</label>
        <label class="check"><input type="checkbox" name="drain"> Water was shut off at the main and the lines drained</label>
        <label class="check"><input type="checkbox" name="alarm"> A low-temperature or water alarm was installed</label>
      </fieldset>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Days unoccupied when the damage was found</small><b data-o="days">–</b></div>
      <div class="out-rows">
        <div><span>Date the vacancy window was passed</span><b data-o="cross">—</b></div>
        <div><span>Days past (or left in) the window</span><b data-o="margin">—</b></div>
        <div><span>Longest likely gap between checks</span><b data-o="gapchk">—</b></div>
        <div><span>Freeze-protection steps documented</span><b data-o="steps">—</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
      <p class="todo-h">Gather for the claim file</p>
      <ul class="todo" data-o="todo"></ul>
    </div>
  </div>
</div>"""


def _faq(*qa):
    return list(qa)


TOOLS = [
    {
        "slug": "settlement-gap-projector", "name": "Settlement Gap Projector", "icon": "$", "kind": "Estimator",
        "short": "Compare two estimates, add appraiser and umpire fees, and see the net at three award landings.",
        "title": "Settlement Gap Projector | Appraisal Fees & Net",
        "desc": "Free settlement gap projector: compare the carrier’s estimate with yours, add appraiser and umpire fees, and see the likely net from appraisal.",
        "h1": "Settlement Gap Projector: Is Appraisal Worth It?",
        "lede": "Enter the carrier’s number and yours. The projector shows the disputed amount, what appraisal might cost, and the net result if the award lands low, in the middle or high.",
        "markup": GAP_FULL,
        "explain": """<h2>How the projector works</h2>
<p>Appraisal settles how much a covered loss costs. It doesn’t guarantee you’ll get your number. Panels often land somewhere between the two estimates, depending on which line items each side can support. The slider lets you test that range. The scenario table then shows the net at 25%, 50% and 75% of the gap after your appraiser’s fee and your half of an umpire.</p>
<ul><li><strong>Amount in dispute</strong> is your estimate minus the carrier’s, using replacement cost (RCV) on both sides.</li>
<li><strong>Projected award</strong> is the carrier’s number plus the share of the gap you choose.</li>
<li><strong>Costs</strong> are either a flat fee or a percentage of the increase, plus half the umpire’s fee if you tick the box.</li></ul>
<h2>Reading the result</h2>
<p>If the net stays positive at a 25% landing, the dispute is usually large enough to talk through with a Maine Insurance Appraiser. If it only works at 75% or more, start with a <a href="/appraisal-work/carrier-estimate-line-review/">line-item estimate review</a> or a documented supplement request. Those are cheaper and often close smaller gaps.</p>
<div class="note"><b class="h">Illustrative figures only</b><p>The default numbers are an example, not a result from any real claim. Fees vary by appraiser and by claim size, so put the real quote in writing before you decide.</p></div>""",
        "faqs": _faq(("Why compare replacement cost and not actual cash value?", "Appraisal panels usually value both, but the dispute is easiest to see at replacement cost. Depreciation is applied afterward and can be checked with the holdback calculator."),
                     ("Is a 55% landing typical?", "There is no typical figure. Results depend on documentation, pricing and how many items are genuinely disputed, which is why the tool shows a range."),
                     ("Does the carrier pay my appraiser?", "Under most appraisal clauses each side pays its own appraiser and the two sides split the umpire. Read your policy’s Appraisal condition to confirm.")),
    },
    {
        "slug": "rcv-acv-holdback-calculator", "name": "RCV / ACV Holdback Calculator", "icon": "%", "kind": "Calculator",
        "short": "Itemize depreciation, see the first check and what’s held back until repairs are done.",
        "title": "RCV vs ACV Holdback Calculator | Depreciation",
        "desc": "Work out depreciation item by item, the first actual cash value check, and the holdback you can recover after repairs. Free and private.",
        "h1": "RCV / ACV Holdback Calculator",
        "lede": "Most replacement cost policies pay in two steps: actual cash value first, then the depreciation held back once repairs are finished. Itemize the damage and see both checks.",
        "markup": DEP,
        "explain": """<h2>Two checks, not one</h2>
<p>On a replacement cost policy, the first payment is usually actual cash value (ACV): replacement cost minus depreciation, minus your deductible. The depreciation is held back and released when you complete the repairs and send proof, within the time your policy allows. On an ACV-only policy, the first check is all there is.</p>
<h2>Where depreciation goes wrong</h2>
<ul><li><strong>Labor depreciated along with materials.</strong> Whether labor can be depreciated depends on policy language and is a common sticking point.</li>
<li><strong>Ages and lifespans that don’t fit.</strong> A 9-year-old architectural shingle roof shouldn’t be treated like one at the end of its life.</li>
<li><strong>Depreciation on items that don’t wear out</strong>, such as permits, debris removal and code upgrades.</li></ul>
<p>If the depreciation on the carrier’s estimate looks heavy, an <a href="/appraisal-work/carrier-estimate-line-review/">estimate review</a> will show which lines drive it. Then put the recovery deadline on your calendar with the <a href="/claim-math/claim-date-tracker/">claim date tracker</a>.</p>""",
        "faqs": _faq(("What is a depreciation cap?", "Many estimates limit depreciation on any single item to a maximum share of its replacement cost, often 50% to 80%. The calculator lets you pick the cap."),
                     ("How long do I have to recover the holdback?", "It depends on the policy. Some allow 180 days and some a year or more, and some let you ask for more time. Read the Loss Settlement condition."),
                     ("Can appraisal decide depreciation?", "Many appraisal awards state both replacement cost and actual cash value, so the panel can resolve disputed depreciation along with price and scope.")),
    },
    {
        "slug": "roof-pitch-squares-converter", "name": "Roof Pitch & Squares Converter", "icon": "▲", "kind": "Calculator",
        "short": "Footprint to roof squares, waste, bundles and the ice-barrier courses a Maine eave needs.",
        "title": "Roof Pitch & Squares Converter | Ice Barrier Too",
        "desc": "Convert a footprint and pitch into roof squares, waste, shingle bundles and ice-barrier courses, then check the totals on your insurance estimate.",
        "h1": "Roof Pitch & Squares Converter",
        "lede": "Turn a house footprint and pitch into roof squares, order quantities and the ice-barrier membrane needed at the eaves, so you can check the roof lines on the carrier’s estimate.",
        "markup": ROOF,
        "explain": """<h2>From footprint to squares</h2>
<p>A roofing square is 100 square feet of roof surface. Because a pitched roof is longer than the footprint it covers, the footprint is multiplied by a pitch factor: about 1.118 at 6/12, 1.302 at 10/12 and 1.414 at 12/12. Waste is then added for cuts at hips, valleys, dormers and the connected ells common on older Maine farmhouses.</p>
<h2>Why the ice-barrier line matters here</h2>
<p>Building codes in cold climates call for an ice barrier at the eaves that runs from the edge to at least 24 inches inside the exterior wall. On a steep roof with a deep overhang that can take two or three courses of membrane, not one. When a roof is replaced after an ice dam or wind loss, check that the estimate prices the full ice-barrier area, drip edge and any required underlayment. Those lines are easy to leave short.</p>
<ul><li>Compare the squares here with the roof report on the estimate; a gap of more than a few squares is worth asking about.</li>
<li>At 8/12 and steeper, look for steep-roof labor charges. At two stories, look for high-roof charges.</li></ul>
<p>More on winter roof claims: <a href="/appraisal-work/ice-dam-snow-load-appraisal/">ice dam and snow load appraisal</a> and <a href="/appraisal-work/roof-hail-loss-appraisal/">roof and hail claims</a>.</p>""",
        "faqs": _faq(("Is this as accurate as a measurement report?", "No. Aerial or field measurements capture every facet, valley and dormer. This converter is a reasonableness check against the estimate."),
                     ("Why does the tool assume two eaves?", "It treats the footprint as a simple gable with eaves on the two long sides. Hip roofs have eaves on all sides, so add the extra length when you compare."),
                     ("What waste factor should I use?", "Plain gables run around 10%. Roofs with dormers, ells and valleys often need 13% to 18%. Your estimate should state the waste it used.")),
    },
    {
        "slug": "percent-deductible-checker", "name": "Percentage Deductible Checker", "icon": "÷", "kind": "Calculator",
        "short": "Turn a 1–10% wind or named-storm deductible into dollars and compare it with a flat one.",
        "title": "Percentage Deductible Checker | Wind & Storm",
        "desc": "Convert a percentage wind, hurricane or named-storm deductible into dollars and see how much storm damage it takes before your policy pays.",
        "h1": "Percentage Deductible Checker",
        "lede": "A 2% deductible sounds small until it’s 2% of your dwelling limit. Convert it to dollars and see what the policy pays on a storm loss compared with a flat deductible.",
        "markup": DEDUCT,
        "explain": """<h2>How percentage deductibles work</h2>
<p>Some Maine policies, especially on coastal property, apply a separate deductible to windstorm, hurricane or named-storm losses. It’s figured as a percentage of Coverage A (the dwelling limit), not of the loss. On a $410,000 dwelling limit, 2% is $8,200 before the policy pays anything for that storm.</p>
<h2>What triggers it</h2>
<p>The trigger is set by your policy wording: a named storm, a hurricane watch or warning, or any windstorm. A nor’easter isn’t a named storm, so a named-storm deductible may not apply to it, while a broader windstorm deductible might. Read the deductible endorsement on your declarations page carefully.</p>
<div class="note"><b class="h">Deductibles and appraisal</b><p>Appraisal decides the amount of loss before the deductible comes off. A higher award can lift a loss above the deductible threshold, which is why accurate pricing matters even on mid-size storm claims.</p></div>
<p>See also <a href="/appraisal-work/noreaster-hurricane-appraisal/">nor’easter and hurricane appraisal</a>.</p>""",
        "faqs": _faq(("Is the deductible a percentage of my loss?", "No. Percentage deductibles are a share of the dwelling coverage limit on your declarations page."),
                     ("Does a named-storm deductible apply to a nor’easter?", "Usually not, because nor’easters aren’t named by the National Hurricane Center, but the trigger language varies. Read your endorsement."),
                     ("Can I change my deductible after a storm?", "Changes apply going forward, not to a loss that has already happened. Ask your agent about options at renewal.")),
    },
    {
        "slug": "claim-date-tracker", "name": "Claim Date Tracker", "icon": "◷", "kind": "Planner",
        "short": "Lay out notice, proof of loss, appraiser and suit dates, then export them to your calendar.",
        "title": "Claim Date Tracker | Deadlines to Your Calendar",
        "desc": "Build a timeline of property claim dates from your date of loss: notice, proof of loss, appraiser, holdback and suit limits, with .ics export.",
        "h1": "Claim Date Tracker with Calendar Export",
        "lede": "Pick your date of loss, set each window to match your policy, and download a calendar file so notice, proof-of-loss, holdback and suit dates don’t slip past during a long claim.",
        "markup": DATES,
        "explain": """<h2>Why dates matter more than people expect</h2>
<p>Property claims in Maine often stretch across a season. A January ice dam may not be fully scoped until April, and contractors are booked solid after a big storm. Meanwhile the policy’s clocks keep running. The tracker turns each window into a date, flags anything within 30 days, and exports everything as an .ics file for Google Calendar, Outlook or Apple Calendar.</p>
<h2>The windows to check in your policy</h2>
<ul><li><strong>Notice:</strong> policies require prompt notice. Report as soon as you reasonably can.</li>
<li><strong>Proof of loss:</strong> often due within a set number of days after the carrier asks for it in writing.</li>
<li><strong>Naming an appraiser:</strong> many appraisal clauses give each side about 20 days after a written demand.</li>
<li><strong>Depreciation recovery:</strong> the time allowed to finish repairs and claim the holdback.</li>
<li><strong>Suit limitation:</strong> the “Suit Against Us” condition. Talk with a Maine attorney well before it arrives.</li></ul>
<div class="note"><b class="h">Not legal advice</b><p>Default values are common figures, not Maine law. Your policy and the carrier’s letters control. If a date is close, call a Maine attorney.</p></div>""",
        "faqs": _faq(("Does appraisal pause the suit-limitation clock?", "Don’t assume it does. Whether any deadline is tolled is a legal question, so ask a Maine attorney if the date is approaching."),
                     ("What does the .ics file contain?", "One all-day calendar event per milestone, with a short note. The file is created in your browser and never sent to us."),
                     ("Why is the appraiser date counted from today?", "The demand date is when you or the carrier invoke appraisal in writing. The tool assumes today so you can see how quickly you’d need to act.")),
    },
    {
        "slug": "appraisal-file-strength-test", "name": "Appraisal File Strength Test", "icon": "✓", "kind": "Checklist",
        "short": "Twelve yes-or-no questions that score your claim file and list what to fix before a demand.",
        "title": "Appraisal File Strength Test | Ready to Demand?",
        "desc": "Twelve quick questions score how ready your property claim file is for appraisal and build a to-do list of the documents still missing.",
        "h1": "Appraisal File Strength Test",
        "lede": "Answer twelve questions about your claim file. The score is weighted toward what appraisal panels rely on most, and every “no” becomes an item on your to-do list.",
        "markup": READY,
        "explain": """<h2>Why preparation comes first</h2>
<p>The award is binding on the amount of loss once two of the three panel members sign it. If a damaged area was never opened up, or your estimate is a single lump sum, it’s hard to add later. The strongest files have three things: accepted coverage, two itemized estimates, and dated proof of the damage.</p>
<h2>How the score is weighted</h2>
<p>Coverage, both itemized estimates and the carrier’s full estimate count most. Photos, hidden-damage inspection, policy reading and mitigation come next, then the paperwork that keeps a file organized.</p>
<ul><li><strong>75 or above:</strong> ready for a professional look at the dollar gap.</li>
<li><strong>45 to 74:</strong> close the flagged items first.</li>
<li><strong>Below 45:</strong> demanding appraisal now risks a low award.</li></ul>
<p>Next steps: <a href="/the-appraisal-path/">the appraisal path, step by step</a>, or the <a href="/claim-math/settlement-gap-projector/">settlement gap projector</a>.</p>""",
        "faqs": _faq(("Is a high score a prediction of the award?", "No. It measures how complete your file is, not the outcome. Pricing, policy terms and the facts of the loss decide the award."),
                     ("Why does coverage count so heavily?", "Appraisal resolves the amount of a covered loss. If coverage itself is denied, the dispute usually belongs with an attorney."),
                     ("Are my answers saved?", "No. Everything stays in your browser and clears when you close or reload the page.")),
    },
    {
        "slug": "seasonal-camp-vacancy-check", "name": "Seasonal Camp Vacancy Check", "icon": "⌂", "kind": "Checker",
        "short": "Count unoccupied days at a camp or second home and check the freeze-protection proof you’ll need.",
        "title": "Seasonal Camp Vacancy Check | Freeze Claims",
        "desc": "For Maine camps and second homes: count unoccupied days against your policy’s vacancy window and list the freeze-protection proof a claim needs.",
        "h1": "Seasonal Camp Vacancy & Freeze Check",
        "lede": "Burst pipes at a closed-up camp are one of Maine’s most common winter claims, and one of the most disputed. Count the unoccupied days, test them against your policy window and see what proof to gather.",
        "markup": CAMP,
        "explain": """<h2>Why camps get extra scrutiny</h2>
<p>Thousands of Maine lake camps, coastal cottages and ski condos sit empty for weeks at a time in winter. Homeowners policies commonly limit coverage for freezing unless the owner kept heat on or shut off and drained the water, and many restrict certain losses once a building has been vacant or unoccupied beyond a set period, often 60 consecutive days. Seasonal-dwelling endorsements can change those rules.</p>
<h2>How the check works</h2>
<p>The tool counts the days between the last overnight stay and the day damage was found, compares that with the window you choose, and lists the documents that show reasonable care: fuel delivery slips, thermostat or alarm logs, a caretaker’s visit notes and plumber invoices for winterizing.</p>
<div class="note"><b class="h">Vacant and unoccupied aren’t the same</b><p>Policies define them differently. A furnished camp you visit now and then may be unoccupied without being vacant. The exact wording in your policy decides which limits apply, and coverage questions belong with your agent or a Maine attorney.</p></div>
<p>Read the full guide: <a href="/owner-guides/seasonal-camp-vacancy-freeze-claims/">seasonal camps, vacancy clauses and freeze claims</a>. If coverage is accepted and the dispute is over cost, see <a href="/appraisal-work/water-damage-loss-appraisal/">water damage appraisal</a>.</p>""",
        "faqs": _faq(("Does passing the vacancy window mean no coverage?", "Not automatically. It depends on the policy definitions and on which peril caused the loss, so the result is a prompt to read your policy, not a coverage decision."),
                     ("What proof of heat helps most?", "Fuel delivery records, utility bills showing normal use, smart thermostat or temperature-alarm logs, and dated notes from whoever checked the property."),
                     ("Can appraisal decide whether the freeze exclusion applies?", "No. Appraisal sets the amount of a covered loss. Whether an exclusion applies is a coverage question for the carrier, and possibly a court.")),
    },
]
