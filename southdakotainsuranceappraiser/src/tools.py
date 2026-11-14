"""Free claim tools: markup + explanatory copy. Logic lives in static/assets/js/app.js. Nothing is stored or sent."""

TB = "/policyholder-calculators/"

PAYOFF_FULL = """
<div class="tool" data-tool="gap">
  <div class="tool-head"><span>Appraisal payoff estimator</span><i>Runs in your browser · nothing saved</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Carrier’s estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="21600"><span class="hint">Replacement cost total before depreciation and deductible.</span></div>
        <div><label for="g-own">Your estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="36400"><span class="hint">Your contractor’s or independent estimate.</span></div>
      </div>
      <div><label for="g-land">Where could the award land inside the gap?</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% means the carrier’s number holds; 100% means yours is awarded in full.</span></div>
      <div class="row2">
        <div><label for="g-ft">Your appraiser’s fee basis</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of the increase (%)</option></select></div>
        <div><label for="g-fee">Fee amount</label><input id="g-fee" name="fee" inputmode="decimal" value="3000"></div>
      </div>
      <label class="check"><input type="checkbox" name="useump" checked> <span>Add my half of an umpire’s fee</span></label>
      <div><label for="g-ump">Umpire’s total fee</label><input id="g-ump" name="umpire" inputmode="decimal" value="3200"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated net increase</small><b data-o="net">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s-a"></span><span class="s-b"></span><span class="s-c"></span></div>
      <div class="legend"><span><i class="s-a"></i>Carrier’s number</span><span><i class="s-b"></i>Your net gain</span><span><i class="s-c"></i>Appraisal costs</span></div>
      <div class="out-rows">
        <div><span>Amount in dispute</span><b data-o="gap">$0</b></div>
        <div><span>Gap as % of carrier estimate</span><b data-o="pct">—</b></div>
        <div><span>Projected award (RCV)</span><b data-o="award">$0</b></div>
        <div><span>Your appraisal costs</span><b data-o="cost">$0</b></div>
        <div><span>Break-even point inside the gap</span><b data-o="be">—</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

PAYOFF_MINI = """
<div class="tool tool-mini" data-tool="gap">
  <div class="tool-head"><span>Quick gap check</span><i>Two numbers, ten seconds</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="m-ins">Carrier’s estimate</label><input id="m-ins" name="insurer" inputmode="decimal" value="17800"></div>
      <div><label for="m-own">Your contractor’s estimate</label><input id="m-own" name="yours" inputmode="decimal" value="29500"></div>
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
  <div class="tool-head"><span>Depreciation recovery calculator</span><i>Add a row for each item</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Laminated shingle roof", 16800, 11, 30), ("Steel siding — north wall", 4200, 18, 40), ("Basement carpet & pad", 3100, 7, 12)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn line small" data-add data-run>+ Add an item</button></div>
      <div class="row2">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="2500"></div>
        <div><label for="d-cap">Depreciation cap</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="100">No cap</option></select><span class="hint">Many estimates cap depreciation; check yours.</span></div>
      </div>
      <label class="check"><input type="checkbox" name="nonrec"> <span>My policy pays actual cash value only (nothing is recoverable)</span></label>
    </div>
    <div class="tool-out tool-out-3" aria-live="polite">
      <div class="out-big"><small>First check (ACV − deductible)</small><b data-o="first">$0</b></div>
      <div class="out-big"><small>Held back until repairs</small><b data-o="held">$0</b></div>
      <div class="out-big"><small>Total after full recovery</small><b data-o="total">$0</b></div>
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
  <div class="tool-head"><span>Roof squares &amp; slope factor calculator</span><i>Check the carrier’s quantities</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <fieldset class="bare"><legend class="sr-only">Measurement method</legend>
        <div class="btn-row">
          <label class="check"><input type="radio" name="mode" value="dims" checked> <span>Footprint length × width</span></label>
          <label class="check"><input type="radio" name="mode" value="area"> <span>I know the footprint area</span></label>
        </div></fieldset>
      <div class="row2" data-mode="dims">
        <div><label for="r-l">Footprint length (ft)</label><input id="r-l" name="len" inputmode="decimal" value="64"></div>
        <div><label for="r-w">Footprint width (ft)</label><input id="r-w" name="wid" inputmode="decimal" value="30"></div>
      </div>
      <div data-mode="dims"><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="16"></div>
      <div data-mode="area" hidden><label for="r-a">Footprint area incl. overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="2100"></div>
      <div class="row2">
        <div><label for="r-p">Roof pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 7 else "", p) for p in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16]) + """</select></div>
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="10">10% · plain gable</option><option value="12" selected>12% · gable with a few cuts</option><option value="15">15% · hip roof</option><option value="18">18% · cut-up or many valleys</option></select></div>
      </div>
      <div><label for="r-pr">Installed price per square (optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 560"><span class="hint">Use a local contractor’s figure for a rough replacement cost.</span></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Roof squares (before waste)</small><b data-o="sq">0</b></div>
      <div class="out-rows">
        <div><span>Slope factor</span><b data-o="mult">1.000</b></div>
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
  <div class="tool-head"><span>Hail percentage deductible calculator</span><i>Percent vs. flat, side by side</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling limit (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="340000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Wind/hail deductible</label><select id="w-p" name="pct"><option value="0.5">0.5%</option><option value="1" selected>1%</option><option value="2">2%</option><option value="3">3%</option><option value="5">5%</option></select></div>
        <div><label for="w-f">All-other-perils deductible ($)</label><input id="w-f" name="flat" inputmode="decimal" value="1500"></div>
      </div>
      <div><label for="w-l">Estimated hail or wind damage ($)</label><input id="w-l" name="loss" inputmode="decimal" value="18900"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your hail deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span class="s-c"></span><span class="s-a"></span></div>
      <div class="legend"><span><i class="s-c"></i>You pay</span><span><i class="s-a"></i>Policy pays</span></div>
      <div class="out-rows">
        <div><span>Payment with the % deductible</span><b data-o="pdpay">$0</b></div>
        <div><span>Payment if the flat deductible applied</span><b data-o="flatpay">$0</b></div>
        <div><span>Extra out of pocket from the %</span><b data-o="diff">$0</b></div>
      </div>
      <table class="mini-table"><caption>The same loss at other percentages</caption><thead><tr><th scope="col">Deductible</th><th scope="col">In dollars</th><th scope="col">Policy pays</th></tr></thead><tbody data-o="ladder"></tbody></table>
      <p class="out-msg" data-o="below"></p>
    </div>
  </div>
</div>"""

DATES = """
<div class="tool" data-tool="dates">
  <div class="tool-head"><span>Appraisal calendar builder</span><i>Download as an .ics file</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
        <div><label for="t-dm">Appraisal demand date (optional)</label><input id="t-dm" type="date" name="demand"><span class="hint">Adds a “name your appraiser” reminder.</span></div>
      </div>
      <p class="hint">Change each window to match your own policy. The defaults are common figures, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report the claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="3"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="10"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"><span class="hint">Often counted from the carrier’s request.</span></div>
        <div><label for="t-a">Name an appraiser within (days of demand)</label><input id="t-a" name="appr" inputmode="numeric" value="20"></div>
        <div><label for="t-r">Depreciation recovery (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="180"></div>
        <div><label for="t-s">Suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="730"><span class="hint">Read your policy’s “Suit Against Us” clause.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"></ol>
      <div class="btn-row"><button type="button" class="btn small" data-ics>Download .ics calendar file</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the insurer accepted coverage for at least part of the loss?", "Get written confirmation that coverage is accepted. If the claim was denied, talk with a South Dakota attorney before thinking about appraisal."),
    (3, "Do you have the carrier’s complete, line-item estimate?", "Ask in writing for the full itemized estimate, not just the summary page."),
    (3, "Do you have your own line-item estimate?", "Get an itemized estimate from a contractor or independent estimator. A one-line bid won’t carry weight with a panel."),
    (2, "Do you have dated photos taken soon after the storm or loss?", "Gather every photo, note when each was taken and add current photos."),
    (2, "Have you read the appraisal clause in your policy?", "Find the paragraph titled ‘Appraisal’ in the conditions and note any time limits."),
    (2, "Do you know your policy’s suit-limitation date?", "Find the ‘Suit Against Us’ clause and put the date on your calendar."),
    (2, "Have temporary repairs been made and receipts kept?", "Tarp, board up or dry out as needed and keep every receipt."),
    (1, "Do you have a current declarations page?", "Download or request your current declarations page."),
    (2, "Has hidden damage been opened up and documented?", "Make sure attics, wall cavities, basements and roof decking have been checked so the scope is complete."),
    (1, "Is your correspondence with the carrier organized by date?", "Collect letters, emails and claim notes in date order."),
    (2, "Is the gap between estimates more than about 10% or $5,000?", "Run the numbers in the appraisal payoff estimator. A small gap may not justify appraisal costs."),
    (1, "If a sworn proof of loss was requested, has it been sent?", "Submit any requested proof of loss before its deadline."),
]

READY = """
<div class="tool tool-wide" data-tool="ready">
  <div class="tool-head"><span>Claim file readiness grader</span><i>12 questions · about two minutes</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <ol class="quiz">""" + "".join(
    '<li data-w="%d" data-fix="%s"><span>%s</span><span class="yn"><button type="button" class="yes" aria-pressed="false">Yes</button><button type="button" class="no" aria-pressed="false">No</button></span></li>' % (w, f, q)
    for w, q, f in _QUIZ) + """
      </ol>
      <div class="btn-row"><button type="button" class="btn line small" data-reset>Clear answers</button></div>
    </div>
    <div class="tool-out grade-out" aria-live="polite">
      <div class="grade-card"><span class="grade" data-o="grade">–</span><span class="grade-pct"><span data-o="score">0</span>% ready</span><span class="hint">Answered <span data-o="count">0 / 12</span></span></div>
      <div>
        <p class="out-msg" data-o="verdict"></p>
        <p class="todo-h">Still to do</p>
        <ul class="todo" data-o="todo"></ul>
      </div>
    </div>
  </div>
</div>"""

COINS = """
<div class="tool" data-tool="coins">
  <div class="tool-head"><span>Coinsurance penalty calculator</span><i>Farm, commercial &amp; HOA policies</i></div>
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="c-v">Replacement cost of the building today ($)</label><input id="c-v" name="value" inputmode="decimal" value="420000"><span class="hint">What it would cost to rebuild now, not what you paid.</span></div>
      <div class="row2">
        <div><label for="c-p">Coinsurance requirement</label><select id="c-p" name="pct"><option value="80" selected>80%</option><option value="90">90%</option><option value="100">100%</option></select></div>
        <div><label for="c-l">Limit you carry ($)</label><input id="c-l" name="limit" inputmode="decimal" value="280000"></div>
      </div>
      <div class="row2">
        <div><label for="c-loss">Amount of loss ($)</label><input id="c-loss" name="loss" inputmode="decimal" value="96000"></div>
        <div><label for="c-d">Deductible ($)</label><input id="c-d" name="deduct" inputmode="decimal" value="5000"></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated payment after coinsurance</small><b data-o="pay">$0</b></div>
      <div class="meter" aria-hidden="true"><span data-o="bar"></span></div>
      <div class="out-rows">
        <div><span>Insurance required</span><b data-o="req">$0</b></div>
        <div><span>Your insurance-to-value ratio</span><b data-o="ratio">—</b></div>
        <div><span>Payment with no penalty</span><b data-o="full">$0</b></div>
        <div><span>Coinsurance penalty</span><b data-o="pen">$0</b></div>
        <div><span>Limit needed to avoid a penalty</span><b data-o="need">$0</b></div>
      </div>
      <p class="out-msg" data-o="cmsg"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "appraisal-payoff-estimator", "name": "Appraisal Payoff Estimator", "icon": "Δ", "kind": "Calculator",
        "short": "Size the dispute, test where an award might land and subtract realistic fees to see your net.",
        "title": "Appraisal Payoff Estimator | Is Appraisal Worth It?",
        "desc": "Free appraisal payoff estimator: compare two estimates, test award outcomes and subtract appraiser and umpire fees to see your likely net gain.",
        "h1": "Appraisal Payoff Estimator: Will Appraisal Pay for Itself?",
        "lede": "Enter the carrier’s estimate and yours, choose where an award might land, and add fees. The appraisal payoff estimator shows your net and the break-even point inside the gap.",
        "markup": PAYOFF_FULL,
        "explain": """
<h2>How to use the appraisal payoff estimator</h2>
<ol><li><strong>Enter both totals at replacement cost.</strong> Use the RCV line on the carrier’s estimate and the matching total on yours.</li>
<li><strong>Test several outcomes.</strong> Slide to 30%, 50% and 80% rather than trusting a single answer.</li>
<li><strong>Add the fees you would actually pay.</strong> Flat or percentage, plus your half of the umpire if one is needed.</li>
<li><strong>Read the break-even point.</strong> It tells you how much of the gap a panel would need to award before appraisal pays for itself.</li></ol>
<h2>Reading the break-even point</h2>
<p>If the break-even point is 15%, even a modest award leaves you ahead. If it is 85%, the case only works if almost everything goes your way, which rarely happens. A low break-even point and a well-documented estimate are the two signs that appraisal is worth a conversation.</p>
<h2>What this estimator leaves out</h2>
<p>It does not handle depreciation timing, policy limits or deductibles. Those change what you are paid, not the size of the dispute. For payment timing, use the <a href="/policyholder-calculators/depreciation-recovery-calculator/">depreciation recovery calculator</a>.</p>
<p class="small-note">Example figures are illustrative only and are not results from any real claim.</p>
""",
        "faqs": [("Is the projected award a prediction?", "No. It is a planning scenario. Real awards depend on documentation, the panel and the policy."), ("What does an umpire usually charge?", "It varies with the size and complexity of the claim. Ask the appraisers for a quote once an umpire is proposed."), ("Why use replacement cost instead of actual cash value?", "Appraisal awards usually state both. Comparing at RCV keeps both estimates on the same basis.")],
    },
    {
        "slug": "depreciation-recovery-calculator", "name": "Depreciation Recovery Calculator", "icon": "ACV", "kind": "Calculator",
        "short": "Estimate the first ACV check, the depreciation held back and the total after repairs.",
        "title": "Depreciation Recovery Calculator | RCV, ACV & Holdback",
        "desc": "Free depreciation recovery calculator: estimate your first ACV check, the depreciation held back and your total once repairs are finished.",
        "h1": "Depreciation Recovery Calculator for RCV and ACV Claims",
        "lede": "Most replacement cost policies pay in two parts. The depreciation recovery calculator shows the first check, how much is held back and what you should receive once the work is finished.",
        "markup": DEP,
        "explain": """
<h2>How depreciation and holdback work</h2>
<p>On a replacement cost policy, the carrier usually pays actual cash value first: replacement cost minus depreciation, minus your deductible. The depreciation it withheld is called <em>recoverable depreciation</em> or <em>holdback</em>. You typically recover it after repairs are completed and documented, within the time your policy allows.</p>
<h2>Using the depreciation recovery calculator</h2>
<ol><li>Add a row for each major item: roof, siding, flooring and so on.</li>
<li>Enter its replacement cost, its age and a reasonable expected life.</li>
<li>Set your deductible and the depreciation cap your estimate uses, if any.</li>
<li>Check the box if your policy pays actual cash value only.</li></ol>
<h2>Where depreciation gets argued</h2>
<p>Carriers sometimes depreciate labor, apply short life expectancies or depreciate items well beyond their actual wear. Each of those choices can be questioned. Depreciation also matters in appraisal, because many award forms list replacement cost and actual cash value separately.</p>
<p class="small-note">The calculator uses straight-line depreciation for illustration. Your carrier’s method may differ.</p>
""",
        "faqs": [("How long do I have to recover depreciation?", "Your policy sets the window, and it varies. Check the loss settlement section and ask the carrier in writing if anything is unclear."), ("Can labor be depreciated?", "Practices and rules vary. If your estimate depreciates labor, it is worth asking how and why."), ("What if my policy pays ACV only?", "Then the depreciation is not recoverable, and the ACV figure is the main payment. Tick the ACV-only box to see that result.")],
    },
    {
        "slug": "roof-slope-factor-calculator", "name": "Roof Squares & Slope Factor Calculator", "icon": "◭", "kind": "Calculator",
        "short": "Turn a footprint and pitch into roof squares, order quantities and a rough replacement figure.",
        "title": "Roof Squares & Slope Factor Calculator | Free Tool",
        "desc": "Free roof squares and slope factor calculator: turn a footprint and pitch into squares, waste, bundles and a rough cost to check an estimate.",
        "h1": "Roof Squares and Slope Factor Calculator",
        "lede": "Hail estimates live and die on quantities. Use the roof squares and slope factor calculator to sanity-check the carrier’s squares, waste and steep-roof treatment before you argue about price.",
        "markup": ROOF,
        "explain": """
<h2>How the slope factor works</h2>
<p>A roof is bigger than the footprint it covers. The steeper the pitch, the more surface area there is. The slope factor is the multiplier that converts flat footprint area into actual roof area. A 7/12 roof, for example, has about 15% more surface than its footprint.</p>
<h2>Using the roof squares and slope factor calculator</h2>
<ol><li>Enter the footprint length and width, or the total footprint area if you know it.</li>
<li>Add the eave overhang. It adds more area than people expect.</li>
<li>Choose the pitch and a waste factor that fits the roof’s complexity.</li>
<li>Optionally add a local installed price per square for a rough total.</li></ol>
<h2>Comparing with the carrier’s estimate</h2>
<p>Look for the total squares, the waste percentage and any steep or high-roof charges in the carrier’s estimate. If their squares are well below yours, ask how the roof was measured. If steep charges are missing on a roof of 8/12 or more, ask why.</p>
<p class="small-note">Results are estimates for planning only. Hips, valleys, dormers and multiple pitches change the answer.</p>
""",
        "faqs": [("What is a roofing square?", "One square equals 100 square feet of roof surface."), ("Why is waste added?", "Shingles are cut at hips, valleys and edges. Waste covers material that cannot be used, and complex roofs need more."), ("Does this work for steel roofs?", "The area math is the same, but steel is ordered by panel length and coverage width, so final quantities differ.")],
    },
    {
        "slug": "hail-percentage-deductible-calculator", "name": "Hail Percentage Deductible Calculator", "icon": "%", "kind": "Calculator",
        "short": "Convert a wind/hail percentage deductible into dollars and compare it with a flat deductible.",
        "title": "Hail Percentage Deductible Calculator | Wind & Hail",
        "desc": "Free hail percentage deductible calculator: turn a wind/hail deductible into dollars, compare it with a flat one and see what the policy pays.",
        "h1": "Hail Percentage Deductible Calculator",
        "lede": "A 1% or 2% wind and hail deductible sounds small until you do the math on your dwelling limit. The hail percentage deductible calculator converts it to dollars and compares it with a flat deductible.",
        "markup": DEDUCT,
        "explain": """
<h2>Why percentage deductibles are common here</h2>
<p>Hail and wind cause a large share of property claims in South Dakota. To manage that risk, many carriers use a separate wind and hail deductible set as a percentage of the dwelling limit, rather than a flat dollar amount. On a $340,000 house, a 2% deductible is $6,800.</p>
<h2>Using the hail percentage deductible calculator</h2>
<ol><li>Enter your Coverage A dwelling limit from the declarations page.</li>
<li>Pick your wind and hail percentage and enter your regular flat deductible.</li>
<li>Enter an estimated damage amount to compare payouts.</li>
<li>Check the ladder table to see the same loss at other percentages.</li></ol>
<h2>What it means for appraisal</h2>
<p>The deductible comes off the award, not the dispute. If the carrier’s estimate is close to your deductible, a modest increase in appraisal can turn a near-zero payment into a meaningful one. If the whole loss falls inside the deductible, appraisal will not change what you receive.</p>
<p class="small-note">Some policies calculate the deductible differently. Your declarations page and endorsements control.</p>
""",
        "faqs": [("Is the percentage based on the loss or the dwelling limit?", "Usually the dwelling limit (Coverage A), not the amount of the loss. Check your policy wording."), ("Does the wind and hail deductible apply to every claim?", "Normally only to losses caused by windstorm or hail. Other perils use the regular deductible."), ("Can I change my deductible?", "You can ask your agent at renewal. A lower deductible usually means a higher premium.")],
    },
    {
        "slug": "appraisal-calendar-builder", "name": "Appraisal Calendar Builder", "icon": "◷", "kind": "Planner",
        "short": "Build a claim and appraisal timeline from your date of loss and export it to your calendar.",
        "title": "Appraisal Calendar Builder | Claim Deadlines to .ics",
        "desc": "Free appraisal calendar builder: map claim and appraisal deadlines from your date of loss and download them to your calendar as an .ics file.",
        "h1": "Appraisal Calendar Builder for Claim Deadlines",
        "lede": "Missing a policy deadline can hurt a claim more than any estimate. The appraisal calendar builder turns your date of loss and policy windows into a dated timeline you can download.",
        "markup": DATES,
        "explain": """
<h2>How the appraisal calendar builder works</h2>
<p>Enter your date of loss and, if appraisal has been demanded, the date of that demand. Then adjust each window to match your policy. The builder sorts the milestones by date, flags anything within 30 days and lets you download every date as a calendar file that works with Google Calendar, Outlook and Apple Calendar.</p>
<h2>Where to find your real deadlines</h2>
<ul><li><strong>Notice and duties after loss</strong> are in the conditions section, often under “Duties After Loss.”</li>
<li><strong>Proof of loss</strong> timing is usually measured from the carrier’s request.</li>
<li><strong>Appraisal</strong> time limits, if any, are in the appraisal paragraph.</li>
<li><strong>Depreciation recovery</strong> windows are in the loss settlement section.</li>
<li><strong>Suit limitation</strong> is in the “Suit Against Us” or “Legal Action Against Us” clause.</li></ul>
<div class="note"><b class="h">Not legal advice</b>Deadlines depend on your policy and South Dakota law. If a suit limitation date is close, talk with a South Dakota attorney promptly.</div>
""",
        "faqs": [("Is anything I enter saved?", "No. The calendar is built in your browser and the file is created on your device."), ("Does appraisal pause the suit limitation clock?", "Not necessarily. Do not assume appraisal extends any deadline. Ask an attorney if the date is close."), ("Which calendar apps can open the file?", "Any app that reads .ics files, including Google Calendar, Outlook and Apple Calendar.")],
    },
    {
        "slug": "claim-file-readiness-grader", "name": "Claim File Readiness Grader", "icon": "A+", "kind": "Checklist",
        "short": "Answer twelve questions and get a letter grade plus a to-do list before you demand appraisal.",
        "title": "Claim File Readiness Grader | Before You Demand",
        "desc": "Free claim file readiness grader: answer 12 questions, get a letter grade and a to-do list showing what to gather before you demand appraisal.",
        "h1": "Claim File Readiness Grader",
        "lede": "Appraisal rewards preparation. The claim file readiness grader scores your documentation, gives it a letter grade and lists what to fix before you demand appraisal.",
        "markup": READY,
        "explain": """
<h2>Why readiness matters</h2>
<p>An appraisal award is binding on the amount of loss once two of three panel members sign. If key documents are missing when the panel meets, those gaps can lower the award, and you may not get a second chance. Grading your file first helps you avoid that.</p>
<h2>How the claim file readiness grader scores you</h2>
<p>Questions are weighted. Coverage acceptance, the carrier’s itemized estimate and your own itemized estimate count most, because a panel cannot work without them. Photos, policy knowledge and repair records come next. The grade is A for 90% and up, B for 75%, C for 60%, D for 45% and F below that.</p>
<h2>After you grade your file</h2>
<p>Work through the to-do list, then run the <a href="/policyholder-calculators/appraisal-payoff-estimator/">appraisal payoff estimator</a> to see whether the gap justifies appraisal. If both look good, an <a href="/appraiser-services/insurance-estimate-second-opinion/">insurance estimate review</a> is a sensible next step.</p>
""",
        "faqs": [("Is a low grade a bad sign?", "Not on its own. It means your file needs work before appraisal, which is fixable."), ("Do I need every item to start appraisal?", "No, but the most heavily weighted items, such as both itemized estimates, matter a great deal."), ("Is my information stored?", "No. Your answers stay in your browser.")],
    },
    {
        "slug": "coinsurance-penalty-calculator", "name": "Coinsurance Penalty Calculator", "icon": "÷", "kind": "Calculator",
        "short": "See whether underinsurance could shrink a farm, commercial or HOA payment, and by how much.",
        "title": "Coinsurance Penalty Calculator | Farm & Commercial",
        "desc": "Free coinsurance penalty calculator for farm, commercial and HOA policies: see if underinsurance could cut your claim payment, and by how much.",
        "h1": "Coinsurance Penalty Calculator for Farm and Commercial Policies",
        "lede": "A strong appraisal award can still shrink if a building was underinsured. The coinsurance penalty calculator shows how a coinsurance clause could reduce your payment and what limit would avoid it.",
        "markup": COINS,
        "explain": """
<h2>What coinsurance means</h2>
<p>Many commercial, farm and association policies include a coinsurance clause. It requires you to insure a building for at least a set percentage of its value, often 80%, 90% or 100%. If you carry less, the policy may pay only a proportion of the loss. The common formula is: limit carried ÷ limit required × loss − deductible, capped at the limit.</p>
<h2>Why it matters in South Dakota</h2>
<p>Construction costs have climbed in recent years, and many farm buildings, shops and older commercial properties are still insured at values set long ago. After a big hail or wind loss, the coinsurance clause can catch owners by surprise. Rural buildings scheduled one by one on a farm policy deserve a close look.</p>
<h2>Using the coinsurance penalty calculator</h2>
<ol><li>Enter what it would cost to rebuild the building today.</li>
<li>Choose the coinsurance percentage from your policy and enter the limit you carry.</li>
<li>Enter the amount of loss and your deductible.</li>
<li>Compare the payment with and without the penalty, and note the limit needed to avoid one.</li></ol>
<p class="small-note">Some policies use agreed value or waive coinsurance. Your policy wording controls. Figures are illustrative.</p>
""",
        "faqs": [("Does coinsurance apply to homeowner policies?", "Homeowner policies usually handle underinsurance through replacement cost conditions instead, which work differently. Coinsurance is more common on commercial and farm forms."), ("Can appraisal fix a coinsurance problem?", "Appraisal can value the loss and sometimes the property, but it cannot change the limit you carried."), ("What is an agreed value endorsement?", "An endorsement in which the insurer and owner agree on a value in advance, which typically suspends the coinsurance clause for that period.")],
    },
]
