"""Interactive claim tools: markup + explanatory copy. Logic lives in static/assets/js/app.js.
Widgets use no headings (labels and spans only) so page heading order stays intact."""

GAP_FULL = """
<div class="calc" data-tool="gap">
  <div class="calc-bar"><span>Appraisal gap &amp; fee estimator</span><em>Runs in your browser · nothing saved</em></div>
  <div class="calc-grid">
    <div class="calc-in">
      <div class="pair">
        <div><label for="g-ins">Insurer's estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="22600"><span class="hint">Replacement cost total on the carrier's estimate.</span></div>
        <div><label for="g-own">Your estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="38900"><span class="hint">From your contractor or an independent estimate.</span></div>
      </div>
      <div><label for="g-land">Where might the award land within the gap?</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% means the carrier's number holds; 100% means your full number is awarded.</span></div>
      <div class="pair">
        <div><label for="g-ft">Your appraiser's fee type</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of the increase (%)</option></select></div>
        <div><label for="g-fee">Fee amount</label><input id="g-fee" name="fee" inputmode="decimal" value="3000"></div>
      </div>
      <div class="pair">
        <div><label for="g-trav">Inspection travel for remote sites ($)</label><input id="g-trav" name="travel" inputmode="decimal" value="0"><span class="hint">Airfare, boat or lodging for off-road-system properties.</span></div>
        <div><label for="g-ump">Umpire's total fee ($)</label><input id="g-ump" name="umpire" inputmode="decimal" value="3500"><span class="hint">Usually split 50/50.</span></div>
      </div>
      <label class="check"><input type="checkbox" name="useump" checked> Include my half of an umpire's fee</label>
    </div>
    <div class="calc-out" aria-live="polite">
      <div class="big"><small>Estimated net increase to you</small><b data-o="net">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s1"></span><span class="s2"></span><span class="s3"></span></div>
      <div class="legend"><span><i class="s1"></i>Carrier's number</span><span><i class="s2"></i>Your net gain</span><span><i class="s3"></i>Appraisal costs</span></div>
      <dl class="rows">
        <div><dt>Amount in dispute</dt><dd data-o="gap">$0</dd></div>
        <div><dt>Gap as % of carrier estimate</dt><dd data-o="pct">—</dd></div>
        <div><dt>Projected award (RCV)</dt><dd data-o="award">$0</dd></div>
        <div><dt>Gross increase</dt><dd data-o="gain">$0</dd></div>
        <div><dt>Your appraisal costs</dt><dd data-o="cost">$0</dd></div>
      </dl>
      <p class="msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

GAP_MINI = """
<div class="calc mini" data-tool="gap">
  <div class="calc-bar"><span>Quick gap check</span><em>No sign-up</em></div>
  <div class="calc-grid">
    <div class="calc-in">
      <div><label for="m-ins">Insurer's estimate</label><input id="m-ins" name="insurer" inputmode="decimal" value="16800"></div>
      <div><label for="m-own">Your contractor's estimate</label><input id="m-own" name="yours" inputmode="decimal" value="29400"></div>
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
<div class="calc wide" data-tool="dep">
  <div class="calc-bar"><span>RCV / ACV depreciation &amp; holdback worksheet</span><em>Add as many line items as you need</em></div>
  <div class="calc-grid">
    <div class="calc-in">
      <div class="tbl items"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Metal roof panels and trim", 24800, 12, 40), ("Interior paint, upper level", 3100, 5, 10), ("Carpet and pad, family room", 2650, 7, 12), ("Baseboard heat covers", 900, 15, 30)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn ghost small" data-add data-run>+ Add item</button></div>
      <div class="pair">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="1000"></div>
        <div><label for="d-cap">Maximum depreciation</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="90">90%</option></select><span class="hint">Many estimates cap depreciation. Check yours.</span></div>
      </div>
      <label class="check"><input type="checkbox" name="nonrec"> My policy pays actual cash value only (no recoverable depreciation)</label>
    </div>
    <div class="calc-out trio" aria-live="polite">
      <div class="big"><small>First check (ACV minus deductible)</small><b data-o="first">$0</b></div>
      <div class="big"><small>Held back until repairs are done</small><b data-o="held">$0</b></div>
      <div class="big"><small>Total if fully recovered</small><b data-o="total">$0</b></div>
      <dl class="rows span">
        <div><dt>Replacement cost (RCV)</dt><dd data-o="rcv">$0</dd></div>
        <div><dt>Total depreciation</dt><dd data-o="dep">$0</dd></div>
        <div><dt>Depreciation as share of RCV</dt><dd data-o="deppct">0%</dd></div>
        <div><dt>Actual cash value (ACV)</dt><dd data-o="acv">$0</dd></div>
      </dl>
    </div>
  </div>
</div>"""

ROOF = """
<div class="calc" data-tool="roof">
  <div class="calc-bar"><span>Roof area &amp; pitch calculator</span><em>Check the squares on your estimate</em></div>
  <div class="calc-grid">
    <div class="calc-in">
      <fieldset class="plain"><legend class="sr-only">Measurement method</legend>
        <div class="btn-row">
          <label class="check"><input type="radio" name="mode" value="dims" checked> Footprint length × width</label>
          <label class="check"><input type="radio" name="mode" value="area"> I know the footprint area</label>
        </div></fieldset>
      <div class="pair" data-mode="dims">
        <div><label for="r-l">Footprint length (ft)</label><input id="r-l" name="len" inputmode="decimal" value="52"></div>
        <div><label for="r-w">Footprint width (ft)</label><input id="r-w" name="wid" inputmode="decimal" value="30"></div>
      </div>
      <div data-mode="dims"><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="18"></div>
      <div data-mode="area" hidden><label for="r-a">Footprint area including overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="1900"></div>
      <div class="pair">
        <div><label for="r-p">Roof pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 8 else "", p) for p in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16]) + """</select></div>
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="10">10% simple gable</option><option value="12" selected>12% gable with dormers</option><option value="15">15% hip roof</option><option value="18">18% complex roof</option></select></div>
      </div>
      <div class="pair">
        <div><label for="r-eave">Total eave length (ft)</label><input id="r-eave" name="eave" inputmode="decimal" value="104"><span class="hint">For ice and water shield along the eaves.</span></div>
        <div><label for="r-pr">Installed price per square (optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 650"></div>
      </div>
    </div>
    <div class="calc-out" aria-live="polite">
      <div class="big"><small>Roof squares (before waste)</small><b data-o="sq">0</b></div>
      <dl class="rows">
        <div><dt>Pitch multiplier</dt><dd data-o="mult">1.000</dd></div>
        <div><dt>Roof surface area</dt><dd data-o="surface">0</dd></div>
        <div><dt>Squares to order (with waste)</dt><dd data-o="order">0</dd></div>
        <div><dt>Shingle bundles (3 per square)</dt><dd data-o="bundles">0</dd></div>
        <div><dt>Ice &amp; water shield at eaves</dt><dd data-o="iws">0</dd></div>
        <div><dt>Rough replacement cost</dt><dd data-o="cost">—</dd></div>
      </dl>
      <p class="msg" data-o="steep"></p>
    </div>
  </div>
</div>"""

DEDUCT = """
<div class="calc" data-tool="deduct">
  <div class="calc-bar"><span>Deductible impact calculator</span><em>Earthquake or wind % vs. flat</em></div>
  <div class="calc-grid">
    <div class="calc-in">
      <div><label for="w-a">Dwelling coverage (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="420000"><span class="hint">From your declarations page.</span></div>
      <div class="pair">
        <div><label for="w-p">Percentage deductible</label><select id="w-p" name="pct"><option value="1">1% (wind, some policies)</option><option value="2">2%</option><option value="5">5%</option><option value="10" selected>10% (earthquake, common)</option><option value="15">15%</option><option value="20">20%</option><option value="25">25%</option></select></div>
        <div><label for="w-f">Regular flat deductible</label><input id="w-f" name="flat" inputmode="decimal" value="1000"></div>
      </div>
      <div><label for="w-l">Estimated covered damage</label><input id="w-l" name="loss" inputmode="decimal" value="58000"></div>
    </div>
    <div class="calc-out" aria-live="polite">
      <div class="big"><small>Your percentage deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack two" aria-hidden="true"><span class="s3"></span><span class="s1"></span></div>
      <div class="legend"><span><i class="s3"></i>You pay</span><span><i class="s1"></i>Policy pays</span></div>
      <dl class="rows">
        <div><dt>Payment with the % deductible</dt><dd data-o="pdpay">$0</dd></div>
        <div><dt>Payment if the flat deductible applied</dt><dd data-o="flatpay">$0</dd></div>
        <div><dt>Extra out of pocket from the % deductible</dt><dd data-o="diff">$0</dd></div>
      </dl>
      <p class="msg" data-o="below"></p>
    </div>
  </div>
</div>"""

DATES = """
<div class="calc" data-tool="dates">
  <div class="calc-bar"><span>Alaska claim timeline planner</span><em>Exports to your calendar</em></div>
  <div class="calc-grid">
    <div class="calc-in">
      <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
      <p class="hint">Change each window to match your policy. Defaults are common figures, not legal advice.</p>
      <div class="days">
        <div><label for="t-n">Report the claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="3"></div>
        <div><label for="t-m">Protect the property within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="7"><span class="hint">Tarps, heat, snow removal, drying.</span></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Often counted from the carrier's request.</span></div>
        <div><label for="t-r">Depreciation recovery (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="365"><span class="hint">Remote and winter repairs can take longer.</span></div>
        <div><label for="t-s">Suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="730"><span class="hint">Use the period stated in your policy.</span></div>
      </div>
    </div>
    <div class="calc-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download .ics calendar file</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the insurer accepted coverage for at least part of the loss?", "Get written confirmation that coverage is accepted. If the claim was denied, talk to an Alaska attorney before considering appraisal."),
    (3, "Do you have the carrier's complete, itemized estimate?", "Ask in writing for the full line-item estimate, not just the summary page."),
    (3, "Do you have your own itemized estimate?", "Get a line-item estimate from a contractor or estimator. A lump-sum bid is hard to defend before a panel."),
    (2, "Do you have dated photos from soon after the loss?", "Collect every photo and note when each was taken. If snow or ice was involved, include photos showing depth and conditions."),
    (2, "Have you read the appraisal clause in your policy?", "Find the Appraisal paragraph in the policy conditions and note any deadlines for naming an appraiser."),
    (2, "Do you know your policy's suit-limitation date?", "Find the Suit Against Us clause and put the date on your calendar. The timeline planner can help."),
    (2, "Did you protect the property and keep receipts?", "Keep every receipt for tarps, heaters, snow removal, drying equipment and board-up."),
    (2, "Has hidden damage been opened up and documented?", "Make sure attics, wet walls, crawlspaces and framing have been checked so the scope is complete."),
    (2, "If the property is remote, do you have freight or travel quotes?", "Get written quotes for barge or air freight and crew travel. These costs are often left out."),
    (1, "Do you have your current declarations page?", "Download or request your declarations page, including any endorsements such as earthquake coverage."),
    (1, "Is your correspondence with the carrier organized by date?", "Gather letters, emails and claim notes in date order."),
    (2, "Is the gap more than roughly 10% or $5,000?", "Run the numbers in the gap and fee estimator. A small gap may not justify appraisal costs."),
]

READY = """
<div class="calc wide" data-tool="ready">
  <div class="calc-bar"><span>Appraisal file checkup</span><em>12 questions · about two minutes</em></div>
  <div class="calc-grid">
    <div class="calc-in">
      <ol class="quiz">""" + "".join(
    '<li data-w="%d" data-fix="%s"><span>%s</span><span class="yn"><button type="button" class="yes" aria-pressed="false">Yes</button><button type="button" class="no" aria-pressed="false">No</button></span></li>' % (w, f, q)
    for w, q, f in _QUIZ) + """
      </ol>
      <div class="btn-row"><button type="button" class="btn ghost small" data-reset>Reset answers</button></div>
    </div>
    <div class="calc-out score" aria-live="polite">
      <div class="meter"><div class="meter-ring" data-o="ring"><span data-o="score">–</span></div><p class="hint">Answered <span data-o="count">0 / 12</span></p></div>
      <div>
        <p class="msg" data-o="verdict"></p>
        <p class="todo-h">Your to-do list</p>
        <ul class="todo" data-o="todo"></ul>
      </div>
    </div>
  </div>
</div>"""

SNOW = """
<div class="calc" data-tool="snow">
  <div class="calc-bar"><span>Roof snow load calculator</span><em>Weight of snow and ice on your roof</em></div>
  <div class="calc-grid">
    <div class="calc-in">
      <div class="pair">
        <div><label for="s-d1">Top layer depth (inches)</label><input id="s-d1" name="d1" inputmode="decimal" value="20"></div>
        <div><label for="s-t1">Top layer type</label><select id="s-t1" name="t1"><option value="7">Fresh powder (~7 lb/ft³)</option><option value="18" selected>Settled snow (~18 lb/ft³)</option><option value="25">Wind-packed (~25 lb/ft³)</option><option value="30">Wet / rain-soaked (~30 lb/ft³)</option></select></div>
      </div>
      <div class="pair">
        <div><label for="s-d2">Lower layer depth (inches)</label><input id="s-d2" name="d2" inputmode="decimal" value="3"><span class="hint">Use 0 if there is only one layer.</span></div>
        <div><label for="s-t2">Lower layer type</label><select id="s-t2" name="t2"><option value="18">Settled snow</option><option value="30">Wet snow</option><option value="57" selected>Ice (~57 lb/ft³)</option></select></div>
      </div>
      <div class="pair">
        <div><label for="s-a">Roof area, measured flat (sq ft)</label><input id="s-a" name="area" inputmode="decimal" value="1800"><span class="hint">The footprint the roof covers, not the sloped surface.</span></div>
        <div><label for="s-dl">Roof snow load the structure was designed for (lb/ft²)</label><input id="s-dl" name="design" inputmode="decimal" value="40"><span class="hint">Illustrative default. Ask your building official or an engineer for your actual figure.</span></div>
      </div>
    </div>
    <div class="calc-out" aria-live="polite">
      <div class="big"><small>Current load on the roof</small><b data-o="psf">0 lb/ft²</b></div>
      <div class="gaugebar" aria-hidden="true"><span data-o="bar"></span></div>
      <dl class="rows">
        <div><dt>Share of design load</dt><dd data-o="share">0%</dd></div>
        <div><dt>Total weight on the roof</dt><dd data-o="lbs">0 lb</dd></div>
        <div><dt>In tons</dt><dd data-o="tons">0</dd></div>
        <div><dt>About the weight of</dt><dd data-o="trucks">0 pickups</dd></div>
      </dl>
      <p class="msg" data-o="snowmsg"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "appraisal-gap-fee-estimator", "name": "Appraisal Gap & Fee Estimator", "icon": "scale", "kind": "Calculator", "photo": "calculator-documents",
        "kw": "appraisal cost calculator",
        "short": "Size the disputed amount, test where an award might land, and subtract appraiser, umpire and travel costs.",
        "title": "Appraisal Cost Calculator | Claim Gap & Fees",
        "desc": "Free appraisal cost calculator: compare your estimate with the insurer's, project an award and subtract appraiser, umpire and remote travel fees.",
        "h1": "Appraisal Cost Calculator: Claim Gap and Fee Estimator",
        "lede": "Enter both estimates, choose where an award might land and add realistic costs, including travel for remote Alaska properties. The estimator shows whether appraisal is likely to leave you ahead.",
        "markup": GAP_FULL,
        "explain": """
<h2>How to use the estimator</h2>
<ol><li><strong>Enter the insurer's RCV total</strong>, the replacement cost figure before depreciation and deductible.</li>
<li><strong>Enter your own estimate</strong> at RCV from a contractor or independent estimator.</li>
<li><strong>Move the slider</strong> to test outcomes. Try 30%, 50% and 80% to see a range, not a single answer.</li>
<li><strong>Add costs.</strong> Use your appraiser's quoted fee, a realistic umpire fee and any travel needed to reach the property.</li></ol>
<h2>The Alaska twist: travel</h2>
<p>For a home in Anchorage or Fairbanks, travel is a minor cost. For a lodge on a fly-in lake or a home in a western Alaska village, getting an appraiser on site can mean airfare, charter time and lodging. Including it here shows whether the gap still justifies appraisal once those costs are counted.</p>
<h2>Reading the result</h2>
<p>If the net increase only looks good at 90% or 100%, the case is fragile. If it still makes sense at 40%, appraisal is more likely to be worth discussing. All figures are illustrative and depend on what you enter.</p>
""",
        "faqs": [("Is the projected award a prediction?", "No. It is a planning scenario. Real awards depend on documentation, the panel and the policy."), ("What does an umpire usually charge?", "It varies with the size and complexity of the claim. Ask for a quote once an umpire is proposed. The cost is usually split evenly.")],
    },
    {
        "slug": "depreciation-holdback-worksheet", "name": "RCV/ACV Depreciation Worksheet", "icon": "file", "kind": "Worksheet", "photo": "calculator-desk",
        "kw": "depreciation calculator",
        "short": "Work out the first ACV check, the recoverable depreciation held back and the total once repairs are done.",
        "title": "Insurance Depreciation Calculator | RCV vs ACV",
        "desc": "Free insurance depreciation calculator: estimate the first ACV payment, the recoverable depreciation held back and your total after repairs.",
        "h1": "Insurance Depreciation Calculator: RCV, ACV and Holdback",
        "lede": "Replacement cost policies usually pay in two stages. Add your line items to see how much arrives in the first check and how much is held back until repairs are finished.",
        "markup": DEP,
        "explain": """
<h2>How depreciation works on a claim</h2>
<p>Replacement cost value (RCV) is what it costs to repair or replace the damaged item new. Actual cash value (ACV) is RCV minus depreciation for age and condition. Many policies pay ACV first and release the depreciation, often called holdback or recoverable depreciation, after the repair is completed.</p>
<h2>Using the worksheet</h2>
<ol><li>Enter each item's replacement cost, its age and its expected life.</li><li>Choose the maximum depreciation your estimate applies.</li><li>Enter your deductible.</li><li>Check the ACV-only box if your policy does not pay recoverable depreciation.</li></ol>
<h2>Alaska timing</h2>
<p>Policies usually set a deadline to complete repairs and claim the holdback. In Alaska, short building seasons, barge schedules and contractor backlogs after big storms can make those deadlines tight. If you are running short on time, ask the carrier in writing about an extension before the deadline passes.</p>
""",
        "faqs": [("Is depreciation applied to labor?", "Practices vary by carrier and policy, and the question has been litigated in some states. Ask how labor depreciation is handled on your estimate."), ("Why is my depreciation so high?", "Age, expected life and the maximum depreciation cap drive the number. Small changes in assumed life can make a large difference.")],
    },
    {
        "slug": "roof-area-pitch-calculator", "name": "Roof Area & Pitch Calculator", "icon": "home", "kind": "Calculator", "photo": "roof-aerial",
        "kw": "roof square calculator",
        "short": "Convert a footprint and pitch into roof squares, bundles, waste and ice-and-water shield at the eaves.",
        "title": "Roof Square Calculator with Pitch & Waste",
        "desc": "Free roof square calculator: turn a footprint and pitch into squares, bundles and waste, plus eave ice and water shield, to check a roof estimate.",
        "h1": "Roof Square Calculator: Area, Pitch and Waste",
        "lede": "Most roof disputes start with measurement. Convert a footprint and pitch into squares, waste and ice-and-water shield to see whether the estimate's quantities are in the right range.",
        "markup": ROOF,
        "explain": """
<h2>Why measurements matter</h2>
<p>A square is 100 square feet of roof surface. Because a sloped roof covers more area than the footprint beneath it, the pitch multiplier converts flat area to surface area. A steeper roof, a more complex shape and a larger overhang all add squares. Small errors in each compound quickly.</p>
<h2>Ice and water shield</h2>
<p>In cold climates, a self-adhering membrane is commonly installed along the eaves to help resist ice dam leaks. Local codes and manufacturers set how far up the roof it should extend. The calculator estimates two courses at the eaves; your roofer may recommend more, including valleys and penetrations.</p>
<h2>Steep roofs</h2>
<p>Snow-country roofs are often steep. Estimating software typically adds steep charges above certain pitches, and high roofs may add more. Check whether your estimate includes them.</p>
""",
        "faqs": [("Should I use the calculator instead of measuring?", "No. It is a cross-check. An on-site measurement or aerial report is more accurate."), ("Why does waste change by roof type?", "Hips, valleys and dormers require more cutting, so more material is wasted.")],
    },
    {
        "slug": "deductible-impact-calculator", "name": "Deductible Impact Calculator", "icon": "shield", "kind": "Calculator", "photo": "quake-damage",
        "kw": "percentage deductible calculator",
        "short": "Turn an earthquake or wind percentage deductible into dollars and compare it with a flat deductible.",
        "title": "Earthquake & Percentage Deductible Calculator",
        "desc": "Free percentage deductible calculator for Alaska: convert an earthquake or wind deductible into dollars and compare what the policy pays on a loss.",
        "h1": "Percentage Deductible Calculator for Earthquake and Wind",
        "lede": "Earthquake coverage in Alaska usually comes with a percentage deductible, and some policies use one for wind. This calculator shows what that percentage means in dollars.",
        "markup": DEDUCT,
        "explain": """
<h2>How percentage deductibles work</h2>
<p>A percentage deductible is calculated from your coverage limit, not the size of the loss. A 10% earthquake deductible on a $420,000 dwelling limit is $42,000. On a $58,000 loss, the policy would pay $16,000. Figures here are illustrative.</p>
<h2>Why it matters for appraisal</h2>
<p>When the deductible is high, the difference between estimates decides whether any payment is owed. A carrier estimate just under the deductible means no payment. An accurate estimate that exceeds it can change the outcome entirely, which is why earthquake disputes are often worth reviewing closely.</p>
<h2>Check your declarations page</h2>
<p>Your declarations page or endorsement shows the deductible type, the percentage and what it is calculated from. Some earthquake endorsements apply separate deductibles to dwelling and contents.</p>
""",
        "faqs": [("Does the percentage apply to the loss or the limit?", "Usually the limit, such as Coverage A. Read your endorsement to confirm."), ("Can there be more than one deductible?", "Depending on the policy, separate deductibles may apply to different coverages or to separate events.")],
    },
    {
        "slug": "claim-timeline-planner", "name": "Claim Timeline Planner", "icon": "clock", "kind": "Planner", "photo": "clipboard-notes",
        "kw": "insurance claim deadline calculator",
        "short": "Turn your date of loss into a dated checklist of claim milestones and download it to your calendar.",
        "title": "Insurance Claim Deadline Calculator | .ics Export",
        "desc": "Free insurance claim deadline calculator: enter your date of loss to build a dated timeline of claim milestones and export it to your calendar.",
        "h1": "Insurance Claim Deadline Calculator and Timeline",
        "lede": "Deadlines are easy to miss when you are dealing with damage. Enter your date of loss, adjust each window to your policy, and download the dates to your calendar.",
        "markup": DATES,
        "explain": """
<h2>The deadlines that matter</h2>
<ul><li><strong>Notice.</strong> Policies require prompt notice of loss. Report as soon as you reasonably can.</li>
<li><strong>Protecting the property.</strong> You are generally expected to take reasonable steps to prevent further damage, such as tarping, keeping heat on or removing snow.</li>
<li><strong>Proof of loss.</strong> If the carrier requests a sworn proof of loss, the policy sets a time to provide it.</li>
<li><strong>Depreciation recovery.</strong> Policies often set a window to complete repairs and claim the holdback.</li>
<li><strong>Suit limitation.</strong> Policies usually limit how long you have to sue. Talk to an Alaska attorney well before that date.</li></ul>
<h2>Using the calendar file</h2>
<p>The .ics file works with Google Calendar, Apple Calendar and Outlook. It is created in your browser and never sent to us.</p>
<div class="note"><b class="h">Not legal advice</b>Your policy and Alaska law control the actual deadlines. If a date is close, consult an attorney promptly.</div>
""",
        "faqs": [("Are these default deadlines correct for my policy?", "They are placeholders. Replace each one with the period in your policy."), ("Is my data saved?", "No. Everything runs in your browser and nothing is stored or sent.")],
    },
    {
        "slug": "appraisal-file-checkup", "name": "Appraisal File Checkup", "icon": "doc", "kind": "Checklist", "photo": "clipboard",
        "kw": "appraisal readiness checklist",
        "short": "Answer 12 questions to score how ready your claim file is for appraisal and get a to-do list.",
        "title": "Appraisal Readiness Checklist | File Checkup",
        "desc": "Free appraisal readiness checklist: answer 12 questions to score your claim file and get a to-do list before you invoke the appraisal clause.",
        "h1": "Appraisal Readiness Checklist: Score Your Claim File",
        "lede": "A strong file makes a stronger appraisal. Answer twelve questions to see how ready you are and what to gather before invoking the appraisal clause.",
        "markup": READY,
        "explain": """
<h2>Why preparation matters</h2>
<p>An appraisal award is binding on the amount of loss. Anything missing from your documentation when the panel decides may be gone for good. Preparing first means the panel sees the full scope.</p>
<h2>What the score means</h2>
<p>Each question is weighted by how much it typically affects an appraisal. A high score means you have the core pieces. A low score means appraisal now could lock in a low number. The to-do list shows what to work on first.</p>
<h2>Alaska-specific items</h2>
<p>Two questions reflect Alaska conditions: documenting snow and ice when weather was involved, and getting freight and travel quotes for remote properties. Both are commonly missing from carrier estimates.</p>
""",
        "faqs": [("Do I need a perfect score?", "No. It is a guide. Some items may not apply to your claim."), ("Is anything I enter saved?", "No. Answers stay in your browser.")],
    },
    {
        "slug": "roof-snow-load-calculator", "name": "Roof Snow Load Calculator", "icon": "snow", "kind": "Calculator", "photo": "snow-roof-house",
        "kw": "roof snow load calculator",
        "short": "Estimate how much your roof's snow and ice weigh per square foot and in total, compared with a design load.",
        "title": "Roof Snow Load Calculator | Weight of Snow & Ice",
        "desc": "Free roof snow load calculator: estimate the weight of snow and ice on your roof per square foot and in total, and compare it with a design load.",
        "h1": "Roof Snow Load Calculator: How Much Does Your Snow Weigh?",
        "lede": "Fresh powder is light. Settled snow, rain-soaked snow and ice are not. Enter depth and snow type to estimate the load on your roof, then compare it with the load the structure was designed for.",
        "markup": SNOW,
        "explain": """
<h2>How the calculation works</h2>
<p>Snow load is depth times density. A foot of fresh powder may weigh around 7 pounds per square foot, while a foot of wet, settled snow can weigh 30 or more. A layer of ice weighs far more per inch than any snow. The calculator adds two layers, multiplies by the roof's horizontal area and compares the result with a design load you enter.</p>
<h2>Design loads</h2>
<p>Buildings are designed for a roof snow load set by local building codes and the engineer's calculations, which vary across Alaska and with roof shape, exposure and drifting. The default here is illustrative only. Your local building department or an engineer can tell you the right figure.</p>
<h2>Using it for a claim</h2>
<p>If a roof, carport or outbuilding was damaged by snow, record the depth and type of snow with photos and a ruler before removal. That record helps show the weight involved. This calculator is not a structural assessment.</p>
<div class="note"><b class="h">Safety first</b>If you see sagging, cracking or doors that suddenly stick, get people out and call a professional. Do not climb onto an overloaded roof.</div>
""",
        "faqs": [("Is roof shape accounted for?", "No. Drifts, valleys and sliding snow concentrate load in places. This is a simple average."), ("Is snow load damage covered?", "Many homeowner policies cover weight of ice, snow or sleet, sometimes with limits for certain structures. Read your policy.")],
    },
]
