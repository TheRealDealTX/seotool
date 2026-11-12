"""Interactive claim calculators: markup + explanatory copy. Logic lives in static/assets/js/app.js.
Tool widgets contain no headings, so they never break the page's heading order."""

C_BLUE, C_ORANGE, C_GREY = "#1550a8", "#f26a1b", "#c9d3e2"


def _head(name, note):
    return f'<div class="tool-head"><span>{name}</span><i>{note}</i></div>'


GAP_FULL = f"""
<div class="tool" data-tool="gap">
  {_head("Settlement gap &amp; fee estimator", "Runs in your browser")}
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="g-ins">Carrier’s estimate (RCV)</label><input id="g-ins" name="insurer" inputmode="decimal" value="21800"><span class="hint">Replacement cost total on the insurer’s estimate.</span></div>
        <div><label for="g-own">Your estimate (RCV)</label><input id="g-own" name="yours" inputmode="decimal" value="36400"><span class="hint">A contractor’s or independent line-item estimate.</span></div>
      </div>
      <div><label for="g-land">Where might the award land inside the gap?</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">0% = the carrier’s number holds. 100% = your full number is awarded.</span></div>
      <div class="row2">
        <div><label for="g-ft">Your appraiser’s fee</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of the increase (%)</option></select></div>
        <div><label for="g-fee">Fee amount</label><input id="g-fee" name="fee" inputmode="decimal" value="3000"></div>
      </div>
      <label class="check"><input type="checkbox" name="useump" checked> Include my half of an umpire’s fee</label>
      <div><label for="g-ump">Umpire’s total fee (split 50/50)</label><input id="g-ump" name="umpire" inputmode="decimal" value="3500"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Estimated net increase to you</small><b data-o="net">$0</b></div>
      <div class="stack" aria-hidden="true"><span style="background:{C_GREY}"></span><span style="background:{C_ORANGE}"></span><span style="background:{C_BLUE}"></span></div>
      <div class="legend"><span><i style="background:{C_GREY}"></i>Carrier’s number</span><span><i style="background:{C_ORANGE}"></i>Your net gain</span><span><i style="background:{C_BLUE}"></i>Appraisal costs</span></div>
      <div class="out-rows">
        <div><span>Amount in dispute</span><b data-o="gap">$0</b></div>
        <div><span>Gap as % of carrier estimate</span><b data-o="pct">—</b></div>
        <div><span>Projected award (RCV)</span><b data-o="award">$0</b></div>
        <div><span>Gross increase</span><b data-o="gain">$0</b></div>
        <div><span>Your appraisal costs</span><b data-o="cost">$0</b></div>
      </div>
      <table class="band"><caption>Net to you at three outcomes</caption><thead><tr><th scope="col">Award lands at</th><th scope="col">Net</th></tr></thead><tbody data-o="band"><tr><td>30%</td><td>$0</td></tr></tbody></table>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

GAP_MINI = f"""
<div class="tool tool-mini" data-tool="gap">
  {_head("Two-number gap check", "No sign-up")}
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="m-ins">Carrier’s estimate</label><input id="m-ins" name="insurer" inputmode="decimal" value="16900"></div>
      <div><label for="m-own">Your contractor’s estimate</label><input id="m-own" name="yours" inputmode="decimal" value="29300"></div>
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
  """ + _head("ACV vs. RCV holdback calculator", "Add as many line items as you need") + """
  <div class="tool-body">
    <div class="tool-in">
      <div class="table-wrap items-table"><table><thead><tr><th>Item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Asphalt shingle roof", 16800, 11, 25), ("Plaster ceiling &amp; paint", 3200, 6, 15), ("Oak strip flooring refinish", 2900, 8, 20)]) + """
      </tbody></table></div>
      <div class="btn-row"><button type="button" class="btn btn-line btn-sm" data-add data-run>+ Add line item</button></div>
      <div class="row3">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="2500"></div>
        <div><label for="d-cap">Depreciation cap</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="90">90%</option></select></div>
        <div><label for="d-pd">ACV check date</label><input id="d-pd" type="date" name="paid"></div>
      </div>
      <div class="row2">
        <div><label for="d-win">Days allowed to repair &amp; claim holdback</label><input id="d-win" name="window" inputmode="numeric" value="180"><span class="hint">Check your policy’s loss-settlement condition; it varies.</span></div>
        <div class="check-cell"><label class="check"><input type="checkbox" name="nonrec"> Policy pays actual cash value only</label></div>
      </div>
    </div>
    <div class="tool-out tool-out-3" aria-live="polite">
      <div class="out-big"><small>First check (ACV − deductible)</small><b data-o="first">$0</b></div>
      <div class="out-big"><small>Held back until repairs</small><b data-o="held">$0</b></div>
      <div class="out-big"><small>Total if fully recovered</small><b data-o="total">$0</b></div>
      <div class="out-rows span-all">
        <div><span>Replacement cost (RCV)</span><b data-o="rcv">$0</b></div>
        <div><span>Total depreciation</span><b data-o="dep">$0</b></div>
        <div><span>Depreciation as share of RCV</span><b data-o="deppct">0%</b></div>
        <div><span>Actual cash value (ACV)</span><b data-o="acv">$0</b></div>
        <div><span>Target date to claim the holdback</span><b data-o="due">Pick the check date</b></div>
      </div>
    </div>
  </div>
</div>"""

ROOF = """
<div class="tool" data-tool="roof">
  """ + _head("Roof area &amp; pitch estimator", "Compare against the carrier’s roof lines") + """
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
      <div data-mode="area" hidden><label for="r-a">Footprint area incl. overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="1600"></div>
      <div class="row2">
        <div><label for="r-p">Roof pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 8 else "", p) for p in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16]) + """</select></div>
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="10">10%: simple gable</option><option value="12" selected>12%: gable with dormers</option><option value="15">15%: hip roof</option><option value="18">18%: cut-up / complex</option></select></div>
      </div>
      <div class="row2">
        <div><label for="r-ly">Existing layers to tear off</label><select id="r-ly" name="layers"><option value="1" selected>1 layer</option><option value="2">2 layers</option><option value="3">3 layers</option></select><span class="hint">Older New York homes often carry two.</span></div>
        <div><label for="r-pr">Installed price per square (optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 650"></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Roof squares (before waste)</small><b data-o="sq">0</b></div>
      <div class="out-rows">
        <div><span>Pitch multiplier</span><b data-o="mult">1.000</b></div>
        <div><span>Roof surface area</span><b data-o="surface">0</b></div>
        <div><span>Squares to order (with waste)</span><b data-o="order">0</b></div>
        <div><span>Shingle bundles (3 per square)</span><b data-o="bundles">0</b></div>
        <div><span>Tear-off squares (all layers)</span><b data-o="tear">0</b></div>
        <div><span>Rough replacement cost</span><b data-o="cost">—</b></div>
      </div>
      <p class="out-msg" data-o="steep"></p>
    </div>
  </div>
</div>"""

DEDUCT = f"""
<div class="tool" data-tool="deduct">
  {_head("Hurricane deductible calculator", "Percentage vs. flat, side by side")}
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="w-a">Dwelling coverage (Coverage A)</label><input id="w-a" name="cova" inputmode="decimal" value="640000"><span class="hint">From your declarations page.</span></div>
      <div class="row2">
        <div><label for="w-p">Your hurricane / windstorm deductible</label><select id="w-p" name="pct"><option value="1">1%</option><option value="2" selected>2%</option><option value="3">3%</option><option value="4">4%</option><option value="5">5%</option></select></div>
        <div><label for="w-f">All-other-perils deductible ($)</label><input id="w-f" name="flat" inputmode="decimal" value="2500"></div>
      </div>
      <div><label for="w-l">Estimated storm damage ($)</label><input id="w-l" name="loss" inputmode="decimal" value="34000"></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your percentage deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="stack" aria-hidden="true"><span style="background:{C_BLUE}"></span><span style="background:{C_GREY}"></span></div>
      <div class="legend"><span><i style="background:{C_BLUE}"></i>You pay</span><span><i style="background:{C_GREY}"></i>Policy pays</span></div>
      <div class="out-rows">
        <div><span>Payment with % deductible</span><b data-o="pdpay">$0</b></div>
        <div><span>Payment if the flat deductible applied</span><b data-o="flatpay">$0</b></div>
        <div><span>Extra out-of-pocket from % deductible</span><b data-o="diff">$0</b></div>
      </div>
      <table class="band"><caption>Same loss at every common percentage</caption><thead><tr><th scope="col">Deductible</th><th scope="col">You pay</th><th scope="col">Policy pays</th></tr></thead><tbody data-o="band"><tr><td>1%</td><td>$0</td><td>$0</td></tr></tbody></table>
      <p class="out-msg" data-o="below"></p>
    </div>
  </div>
</div>"""

DATES = """
<div class="tool" data-tool="dates">
  """ + _head("New York claim calendar builder", "Exports an .ics file") + """
  <div class="tool-body">
    <div class="tool-in">
      <div class="row2">
        <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
        <div><label for="t-q">Proof-of-loss request received (optional)</label><input id="t-q" type="date" name="req"><span class="hint">Proof-of-loss timing usually runs from the request.</span></div>
      </div>
      <p class="hint">Adjust each window to match your policy. Defaults are common figures, not legal advice.</p>
      <div class="days-grid">
        <div><label for="t-n">Report claim within (days)</label><input id="t-n" name="notice" inputmode="numeric" value="3"></div>
        <div><label for="t-m">Temporary repairs within (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="10"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"></div>
        <div><label for="t-r">Holdback recovery (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="180"></div>
        <div><label for="t-s">Suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="730"><span class="hint">Two years = 730 days.</span></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <ol class="timeline" data-o="timeline"><li><b>Pick your date of loss</b><span>Milestones will appear here.</span></li></ol>
      <div class="btn-row"><button type="button" class="btn btn-blue btn-sm" data-ics>Download .ics calendar file</button></div>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the insurer accepted coverage for at least part of the loss?", "Get written confirmation that coverage is accepted. If the claim was denied, talk to a New York attorney before considering appraisal."),
    (3, "Do you have the carrier’s complete, itemized estimate?", "Ask in writing for the full line-item estimate, not just the summary page."),
    (3, "Do you have your own line-item estimate?", "Get an independent, itemized estimate. A one-line contractor bid won’t carry weight with a panel."),
    (2, "Do you have dated photos taken soon after the loss?", "Collect every photo and note when each was taken. Add photos of current conditions."),
    (2, "Have you read your policy’s appraisal condition?", "Find the ‘Appraisal’ paragraph in the policy conditions and note any timing language."),
    (2, "Do you know your policy’s suit-limitation date?", "Find the ‘Suit Against Us’ condition and calendar the date with the claim calendar builder."),
    (2, "Were temporary repairs made, with receipts saved?", "Make reasonable temporary repairs (tarps, extraction, board-up) and keep every receipt."),
    (1, "Do you have your current declarations page?", "Download or request your declarations page and any endorsements."),
    (2, "Has hidden damage been opened up and documented?", "Make sure wet walls, attics, ceilings and roof decking were inspected so the scope is complete."),
    (2, "For a co-op or condo: do you know which policy covers which part?", "Read the proprietary lease or bylaws repair section and compare it with the master policy and your HO-6."),
    (2, "Is the gap more than about 10% or several thousand dollars?", "Run the settlement gap & fee estimator. A small gap may not justify appraisal costs."),
    (1, "If the carrier asked for a sworn proof of loss, was it filed on time?", "If a proof of loss was requested, file it on time and keep a copy."),
]

READY = """
<div class="tool tool-wide" data-tool="ready">
  """ + _head("Appraisal readiness checkup", "12 questions · about two minutes") + """
  <div class="tool-body">
    <div class="tool-in">
      <ol class="quiz">""" + "".join(
    '<li data-w="%d" data-fix="%s"><span>%s</span><span class="yn"><button type="button" class="yes" aria-pressed="false">Yes</button><button type="button" class="no" aria-pressed="false">No</button></span></li>' % (w, f, q)
    for w, q, f in _QUIZ) + """
      </ol>
      <div class="btn-row"><button type="button" class="btn btn-line btn-sm" data-reset>Reset answers</button></div>
    </div>
    <div class="tool-out tool-out-score" aria-live="polite">
      <div>
        <svg class="gauge" viewBox="0 0 200 110" aria-hidden="true"><path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#e4eaf3" stroke-width="18"/><path data-o="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#f26a1b" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="251.3"/></svg>
        <div class="gauge-num"><span data-o="score">–</span></div>
        <p class="hint center">Answered <span data-o="count">0 / 12</span></p>
      </div>
      <div>
        <p class="out-msg" data-o="verdict"></p>
        <p class="todo-h">Your to-do list</p>
        <ul class="todo" data-o="todo"></ul>
      </div>
    </div>
  </div>
</div>"""

SPLIT = f"""
<div class="tool" data-tool="split">
  {_head("Co-op &amp; condo claim splitter", "Master policy vs. your HO-6")}
  <div class="tool-body">
    <div class="tool-in">
      <div><label for="s-t">Total cost to repair the unit ($)</label><input id="s-t" name="total" inputmode="decimal" value="48000"></div>
      <div><label for="s-b">Share that is building property</label>
        <div class="range"><input id="s-b" type="range" name="bshare" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <span class="hint">Original walls, pipes and fixtures the building insures. Your lease or bylaws decide this; the rest is your improvements.</span></div>
      <div class="row2">
        <div><label for="s-md">Master policy deductible ($)</label><input id="s-md" name="mded" inputmode="decimal" value="25000"></div>
        <div><label for="s-ms">Deductible charged back to you</label><select id="s-ms" name="charge"><option value="0">None (building absorbs it)</option><option value="0.05">Your share by shares/interest (5%)</option><option value="1" selected>All of it (unit-caused loss)</option></select></div>
      </div>
      <div class="row2">
        <div><label for="s-hd">Your HO-6 deductible ($)</label><input id="s-hd" name="hded" inputmode="decimal" value="1000"></div>
        <div><label for="s-la">HO-6 loss assessment limit ($)</label><input id="s-la" name="lalim" inputmode="decimal" value="10000"></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="out-big"><small>Your estimated out-of-pocket</small><b data-o="oop">$0</b></div>
      <div class="stack" aria-hidden="true"><span style="background:{C_GREY}"></span><span style="background:{C_BLUE}"></span><span style="background:{C_ORANGE}"></span></div>
      <div class="legend"><span><i style="background:{C_GREY}"></i>Building / master policy</span><span><i style="background:{C_BLUE}"></i>Your HO-6 pays</span><span><i style="background:{C_ORANGE}"></i>You pay</span></div>
      <div class="out-rows">
        <div><span>Building portion</span><b data-o="bpart">$0</b></div>
        <div><span>Master policy pays (after its deductible)</span><b data-o="mpay">$0</b></div>
        <div><span>Deductible charged back to you</span><b data-o="cb">$0</b></div>
        <div><span>Your improvements portion</span><b data-o="upart">$0</b></div>
        <div><span>HO-6 pays (improvements + assessment)</span><b data-o="hpay">$0</b></div>
      </div>
      <p class="out-msg" data-o="msg"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "settlement-gap-fee-estimator", "name": "Settlement Gap & Fee Estimator", "kind": "Calculator",
        "short": "See the disputed amount, a projected award and what you’d net after appraiser and umpire fees.",
        "title": "Settlement Gap & Fee Estimator | Is Appraisal Worth It?",
        "desc": "Free calculator: compare your estimate with the insurer’s, project an appraisal award and subtract appraiser and umpire fees to see your net.",
        "h1": "Settlement Gap & Fee Estimator for Disputed Claims",
        "lede": "Enter the carrier’s estimate and yours, choose where an award might land, and add realistic fees. The estimator shows whether appraisal is likely to leave more money in your pocket, at three different outcomes.",
        "markup": GAP_FULL,
        "explain": """
<h2>How to use the estimator</h2>
<ol><li><strong>Enter the carrier’s replacement cost total</strong>, the figure before depreciation and deductible.</li>
<li><strong>Enter your estimate</strong> from a contractor or independent estimator, also at replacement cost.</li>
<li><strong>Move the slider</strong> to test a likely outcome. The table underneath always shows 30%, 55% and 80% so you see a range, not one answer.</li>
<li><strong>Add fees</strong> using your appraiser’s quoted arrangement and a realistic umpire fee.</li></ol>
<h2>Reading the three-outcome table</h2>
<p>Awards rarely match either side’s opening number. Well-documented line items tend to hold; inflated or unsupported ones tend to fall. If appraisal only pays at 80%, the case is fragile. If it still nets something at 30%, it’s more likely to be worth the effort.</p>
<div class="note"><b class="h">Illustrative example</b>With the default figures, a $14,600 gap and an award at 55% of it yields about $8,030 more before fees. After a $3,000 flat fee and half of a $3,500 umpire fee, the net is about $3,280. These are made-up numbers for illustration only.</div>
<h2>What the estimator leaves out</h2>
<p>It doesn’t model depreciation timing, policy limits, sub-limits or deductibles. Those change what you’re paid, not the size of the dispute. For holdback math use the <a href="/appraisal-calculators/acv-rcv-holdback-calculator/">ACV vs. RCV holdback calculator</a>, and for coastal policies check the <a href="/appraisal-calculators/hurricane-deductible-calculator/">hurricane deductible calculator</a>.</p>
""",
        "faqs": [("Is a projected award a guarantee?", "No. It’s a planning scenario. Real awards depend on documentation, the panel and the policy wording."), ("What’s a typical umpire fee?", "It varies with the size and complexity of the claim. Ask for a quote once an umpire is proposed; the cost is usually split evenly between the two sides."), ("Should I use a flat fee or a percentage?", "Use whatever your appraiser actually quoted. Try both settings to see how each arrangement changes your net.")],
    },
    {
        "slug": "acv-rcv-holdback-calculator", "name": "ACV vs. RCV Holdback Calculator", "kind": "Calculator",
        "short": "Estimate the first actual cash value check, the depreciation held back, and the date to claim it.",
        "title": "ACV vs RCV Holdback Calculator | Recoverable Depreciation",
        "desc": "Line-item calculator for actual cash value, recoverable depreciation and the deductible, plus a target date to claim the holdback after repairs.",
        "h1": "ACV vs. RCV Holdback Calculator",
        "lede": "Replacement cost policies usually pay in two steps: actual cash value now, and the depreciation held back once repairs are done. Add your line items to see both checks and the date to calendar.",
        "markup": DEP,
        "explain": """
<h2>How the two checks work</h2>
<p>Most New York homeowners policies settle buildings at replacement cost, but many pay the actual cash value first. The difference, recoverable depreciation, is released after you repair or replace within the time the policy allows. This calculator applies straight-line depreciation (age ÷ expected life) to each line, capped at the percentage you choose.</p>
<h2>Why the cap and the life matter</h2>
<p>Depreciation is one of the most argued numbers in an appraisal. A 25-year life on a roof that’s 11 years old yields 44% depreciation; call it a 20-year roof and the figure jumps to 55%. Plaster ceilings, oak floors and slate are often depreciated as if they were drywall, carpet and asphalt. Change the inputs to see how much each assumption is worth.</p>
<ul><li><strong>Labor:</strong> some carriers depreciate labor as well as materials. Ask how yours handled it.</li><li><strong>Non-depreciable items:</strong> permits, debris removal and many code items usually aren’t depreciated.</li><li><strong>The deadline:</strong> the holdback date shown is only a target. Your policy’s loss-settlement condition controls.</li></ul>
<div class="note"><b class="h">Worth knowing</b>An appraisal award form can list replacement cost and actual cash value separately. Asking for both protects your later holdback claim.</div>
<p>To check the roof line itself, try the <a href="/appraisal-calculators/roof-area-pitch-estimator/">roof area &amp; pitch estimator</a>.</p>
""",
        "faqs": [("Does every policy pay recoverable depreciation?", "No. Actual cash value policies don’t. Tick the ACV-only box to see that result."), ("What if I can’t finish repairs in time?", "Ask the carrier in writing for an extension before the window closes and keep proof of the request. If the date is near, talk to a New York attorney."), ("Is depreciation negotiable in appraisal?", "The amount of depreciation is part of the loss valuation, so it is commonly addressed by the panel. How it applies depends on your policy.")],
    },
    {
        "slug": "roof-area-pitch-estimator", "name": "Roof Area & Pitch Estimator", "kind": "Calculator",
        "short": "Turn a footprint and pitch into roof squares, waste, bundles and tear-off for multiple layers.",
        "title": "Roof Squares & Pitch Estimator | Check Your Claim’s Roof",
        "desc": "Convert a roof footprint and pitch into squares, waste, shingle bundles and multi-layer tear-off, then compare them with your insurance estimate.",
        "h1": "Roof Area & Pitch Estimator",
        "lede": "Roof claims are often won or lost on measurements. Use the footprint and pitch to estimate squares, waste and tear-off, then compare them with the lines in the carrier’s estimate.",
        "markup": ROOF,
        "explain": """
<h2>From footprint to squares</h2>
<p>A roofing square is 100 square feet of roof surface. The calculator adds your eave overhang to the footprint, multiplies by the pitch factor (the slope’s true length per foot of run) and divides by 100. Waste covers cutting at hips, valleys and dormers.</p>
<h2>New York details to check in the estimate</h2>
<ul><li><strong>Multiple layers.</strong> Many older homes from Queens to Buffalo carry two layers of shingles. Each layer should be removed and priced.</li><li><strong>Steep and high charges.</strong> Pitches of 7/12 and above, and roofs above two stories, typically add labor.</li><li><strong>Ice and water shield.</strong> Code-required eave protection in snow country is an easy line to miss.</li><li><strong>Drip edge, starter and ridge.</strong> Small lines that add up.</li></ul>
<div class="note"><b class="h">Worth knowing</b>Footprint math is an approximation. Aerial measurement reports or a field measurement are what a panel will rely on. Use this to spot a large gap, then verify.</div>
<p>Hail or wind on the roof? See <a href="/claim-appraisals/roof-hail-damage-appraisal/">roof &amp; hail damage appraisal</a> and <a href="/claim-appraisals/snow-load-ice-dam-appraisal/">snow load &amp; ice dam appraisal</a>.</p>
""",
        "faqs": [("Why is my result different from the carrier’s squares?", "Differences usually come from pitch, overhangs, waste or missed sections such as porch roofs and dormers. Compare section by section."), ("What waste factor should I use?", "Simple gables often run around 10%; hips and cut-up roofs run higher. Your estimate should explain the waste it applied."), ("Does the calculator handle flat roofs?", "Choose 2/12 for a near-flat roof. Membrane roofs are priced differently from shingles, so treat the cost line with care.")],
    },
    {
        "slug": "hurricane-deductible-calculator", "name": "Hurricane Deductible Calculator", "kind": "Calculator",
        "short": "Convert a 1–5% hurricane deductible into dollars and compare it with your flat deductible.",
        "title": "Hurricane Deductible Calculator for New York Policies",
        "desc": "See what a 1% to 5% hurricane or windstorm deductible costs in dollars, how much a storm claim pays, and how it compares with a flat deductible.",
        "h1": "Hurricane Deductible Calculator for New York Homes",
        "lede": "Coastal New York policies often carry a percentage hurricane or windstorm deductible. Enter your dwelling limit and damage to see the deductible in dollars and the payment at every common percentage.",
        "markup": DEDUCT,
        "explain": """
<h2>How a percentage deductible works</h2>
<p>A 2% hurricane deductible on a home insured for $640,000 is $12,800, not $2,500. It’s calculated on the dwelling limit (Coverage A) shown on your declarations page, not on the size of the loss. That’s why owners on Long Island, in the boroughs and along the Westchester shore are often surprised after a storm.</p>
<h2>When it applies</h2>
<p>The percentage deductible applies only when the event your policy defines has happened. Wording varies: some forms tie it to a hurricane watch or warning issued by the National Weather Service for part of New York, with a set period before and after. Other wind losses fall under your regular deductible. Read the endorsement itself.</p>
<ul><li>Check whether the trigger is “hurricane,” “named storm” or “windstorm.”</li><li>Check the time window around the event.</li><li>Remember surge and flooding are usually excluded entirely and handled by a flood policy.</li></ul>
<div class="note"><b class="h">Illustrative example</b>A $34,000 wind loss with a 2% deductible on $640,000 of dwelling coverage pays $21,200. Under a $2,500 flat deductible, it would pay $31,500. Figures are illustrative.</div>
<p>More on the topic: <a href="/policyholder-guides/hurricane-deductibles-long-island-nyc/">hurricane deductibles on Long Island and in NYC</a> and <a href="/claim-appraisals/hurricane-noreaster-appraisal/">hurricane &amp; nor’easter appraisal</a>.</p>
""",
        "faqs": [("Can appraisal change my deductible?", "No. Appraisal values the loss. Which deductible applies is a policy question. A higher valuation can still increase the payment above the deductible."), ("Does a nor’easter trigger a hurricane deductible?", "Usually not, unless your policy uses a broader windstorm trigger. Check the endorsement wording."), ("Why does the table show several percentages?", "So you can see what a different deductible choice would mean before renewal, or check the carrier applied the right one.")],
    },
    {
        "slug": "claim-calendar-builder", "name": "Claim Calendar Builder", "kind": "Planner",
        "short": "Turn your date of loss into dated claim milestones and download them as a calendar file.",
        "title": "Claim Calendar Builder | Insurance Deadlines to .ics",
        "desc": "Free planner: enter your date of loss to map notice, mitigation, proof of loss, holdback and suit-limitation dates, then download an .ics calendar.",
        "h1": "Claim Calendar Builder: Your Policy Deadlines, Dated",
        "lede": "Claims stall quietly and deadlines don’t. Enter your date of loss (and the proof-of-loss request date, if you have one) to see every milestone and save them to your calendar.",
        "markup": DATES,
        "explain": """
<h2>The milestones it maps</h2>
<ul><li><strong>Notice.</strong> Policies require prompt notice. The target here is self-imposed; report as soon as you can.</li><li><strong>Temporary repairs.</strong> Mitigation protects the property and the claim. Keep every receipt.</li><li><strong>Proof of loss.</strong> If the carrier asks for a sworn proof of loss, many New York policies set a deadline counted from that request. Enter the request date and the calendar counts from it.</li><li><strong>Holdback recovery.</strong> The window to finish repairs and claim recoverable depreciation.</li><li><strong>Suit limitation.</strong> Many New York property policies limit lawsuits to two years from the loss. Treat this as a hard stop and speak with an attorney well before it.</li></ul>
<h2>Importing the calendar file</h2>
<p>The .ics download works with Google Calendar, Apple Calendar and Outlook. Each milestone is an all-day event with a short description. Nothing is uploaded; the file is created in your browser.</p>
<div class="note"><b class="h">Worth knowing</b>Appraisal doesn’t pause every policy deadline automatically. If a suit-limitation date is approaching during appraisal, get legal advice about protecting it.</div>
<p>Next, check whether the file is ready with the <a href="/appraisal-calculators/appraisal-readiness-checkup/">appraisal readiness checkup</a>.</p>
""",
        "faqs": [("Are the default days correct for my policy?", "They’re common figures, not your policy’s terms. Replace each with the number in your own policy."), ("Why does proof of loss use a separate date?", "Because the deadline in many policies runs from the carrier’s written request, not from the date of loss."), ("Can I edit the events after importing?", "Yes. Once imported they’re ordinary calendar events you can move, edit or set reminders on.")],
    },
    {
        "slug": "appraisal-readiness-checkup", "name": "Appraisal Readiness Checkup", "kind": "Checklist",
        "short": "Twelve yes-or-no questions that score your file and build a to-do list before you demand appraisal.",
        "title": "Appraisal Readiness Checkup | Is Your Claim File Ready?",
        "desc": "Answer 12 yes-or-no questions to score how ready your property claim is for appraisal and get a personal to-do list of gaps to close first.",
        "h1": "Appraisal Readiness Checkup",
        "lede": "Appraisal locks in a number. Before you demand it, make sure your file can support the number you want. Twelve questions, a weighted score and a to-do list.",
        "markup": READY,
        "explain": """
<h2>How the score is weighted</h2>
<p>Questions about accepted coverage and the two itemized estimates carry the most weight, because without them appraisal either can’t start or can’t succeed. Photos, policy deadlines and complete scoping come next. Paperwork items carry the least weight but still matter.</p>
<h2>What a strong file looks like</h2>
<ul><li>Written acceptance of coverage, even partial.</li><li>The carrier’s full line-item estimate and your own.</li><li>Dated photos from right after the loss and of current conditions.</li><li>For co-ops and condos, the lease or bylaws section on who repairs what.</li><li>A calendar of every deadline.</li></ul>
<div class="note"><b class="h">Worth knowing</b>A low score isn’t a dead end. It’s a list. Most gaps can be closed in a week or two, and closing them often moves the carrier before appraisal is even needed.</div>
<p>Then test the economics with the <a href="/appraisal-calculators/settlement-gap-fee-estimator/">settlement gap &amp; fee estimator</a>, or read the <a href="/appraisal-walkthrough/">appraisal walkthrough</a>.</p>
""",
        "faqs": [("Is my answer data saved?", "No. Answers stay in your browser and disappear when you leave the page."), ("What score should I aim for?", "Roughly 75 or higher means your documentation is in good shape. Below that, work through the to-do list first."), ("Does a high score mean appraisal will work?", "No. It means your file is organized. The economics and the facts of the loss still decide whether appraisal makes sense.")],
    },
    {
        "slug": "co-op-condo-claim-splitter", "name": "Co-op & Condo Claim Splitter", "kind": "Calculator",
        "short": "Split a unit loss between the building’s master policy, your HO-6 and your own pocket.",
        "title": "Co-op & Condo Claim Splitter | Master Policy vs HO-6",
        "desc": "Split a co-op or condo unit loss between the building’s master policy and your HO-6, including deductible chargebacks and loss assessment coverage.",
        "h1": "Co-op & Condo Claim Splitter: Master Policy vs. HO-6",
        "lede": "In a New York co-op or condo, one leak can involve the building’s master policy, a deductible charged back to you and your own HO-6. Enter the numbers to see who likely pays what.",
        "markup": SPLIT,
        "explain": """
<h2>Why unit claims get complicated</h2>
<p>Your proprietary lease (co-op) or bylaws and declaration (condo) decide which parts of the apartment belong to the building and which belong to you. The board’s master policy insures the building’s share, subject to its own deductible, which is often large. Your unit-owners (HO-6) policy covers your improvements, belongings and, through loss assessment coverage, some charges the board passes on to you.</p>
<h2>How the splitter calculates</h2>
<ol><li>The building portion is the total times the building share you set.</li><li>The master policy pays the building portion above its deductible.</li><li>Any deductible charged back to you, plus the unpaid building portion if you’re made responsible for it, becomes an assessment. Your HO-6 loss assessment coverage pays up to its limit.</li><li>Your improvements portion is paid by your HO-6 after its deductible.</li></ol>
<div class="note"><b class="h">Worth knowing</b>Boards and leases handle chargebacks differently, and some HO-6 policies limit how loss assessment coverage responds to a master deductible. Treat the result as a starting point and confirm with your managing agent and policy.</div>
<p>More detail: <a href="/policyholder-guides/co-op-condo-master-policy-vs-ho6/">master policy vs. HO-6</a> and <a href="/claim-appraisals/co-op-condo-commercial-appraisal/">co-op, condo &amp; commercial appraisal</a>.</p>
""",
        "faqs": [("Who decides the building share?", "Your governing documents, applied to the facts of the loss. If the board and you disagree, that’s a question about responsibility, not just valuation."), ("Does the HO-6 deductible apply to loss assessment?", "Often it does, but forms vary. Check your policy’s loss assessment section."), ("Can appraisal resolve a unit-versus-building dispute?", "Appraisal sets the amount of loss under one policy. It doesn’t decide which policy responds. Valuation and responsibility are separate questions.")],
    },
]
