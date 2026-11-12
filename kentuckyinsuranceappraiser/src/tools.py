"""Free claim tools: widget markup. Page copy lives in tool_copy.py, logic in static/assets/js/app.js.

Every widget renders usable default values without JavaScript (inputs pre-filled); results fill in
once app.js runs. Nothing is sent or stored.
"""
from tool_copy import TOOL_COPY


def _row(label, key, val="—"):
    return f'<div><dt>{label}</dt><dd data-o="{key}">{val}</dd></div>'


def _head(title, tag):
    return f'<div class="calc-bar"><h2 class="calc-t">{title}</h2><span>{tag}</span></div>'


PAYOFF = f"""
<div class="calc" data-tool="gap">
  {_head("Appraisal payoff estimator", "Private · runs in your browser")}
  <div class="calc-grid">
    <div class="calc-in">
      <div class="pair">
        <div><label for="g-ins">Insurer’s estimate (RCV, $)</label><input id="g-ins" name="insurer" inputmode="decimal" value="21600"><small>Replacement-cost total on the carrier’s estimate.</small></div>
        <div><label for="g-own">Your estimate (RCV, $)</label><input id="g-own" name="yours" inputmode="decimal" value="34900"><small>Your contractor’s or independent line-item estimate.</small></div>
      </div>
      <div><label for="g-land">Where might the award land inside the gap?</label>
        <div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div>
        <small>0% = the carrier’s number holds. 100% = your number is awarded in full.</small></div>
      <div class="pair">
        <div><label for="g-ft">Appraiser fee type</label><select id="g-ft" name="feetype"><option value="flat">Flat fee ($)</option><option value="pct">Percent of the increase (%)</option></select></div>
        <div><label for="g-fee">Fee amount</label><input id="g-fee" name="fee" inputmode="decimal" value="2800"></div>
      </div>
      <div class="pair">
        <div><label class="tick"><input type="checkbox" name="useump" checked> Add half of an umpire’s fee</label></div>
        <div><label for="g-ump">Umpire’s total fee ($)</label><input id="g-ump" name="umpire" inputmode="decimal" value="3200"></div>
      </div>
    </div>
    <div class="calc-out" aria-live="polite">
      <p class="kpi"><small>Estimated net increase to you</small><b data-o="net">—</b></p>
      <div class="stack" aria-hidden="true"><span class="s1"></span><span class="s2"></span><span class="s3"></span></div>
      <ul class="key"><li><i class="s1"></i>Carrier’s number</li><li><i class="s2"></i>Your net gain</li><li><i class="s3"></i>Appraisal costs</li></ul>
      <dl class="rows">{_row("Amount in dispute", "gap")}{_row("Gap vs. carrier estimate", "pct")}{_row("Projected award (RCV)", "award")}{_row("Gross increase", "gain")}{_row("Your appraisal costs", "cost")}{_row("Break-even landing point", "breakeven")}</dl>
      <p class="say" data-o="msg">Turn on JavaScript to see results update as you type.</p>
    </div>
  </div>
</div>"""

PAYOFF_MINI = """
<div class="calc mini" data-tool="gap">
  <div class="calc-bar"><p class="calc-t">60-second gap check</p><span>No sign-up</span></div>
  <div class="calc-grid">
    <div class="calc-in">
      <div><label for="m-ins">Insurer’s estimate ($)</label><input id="m-ins" name="insurer" inputmode="decimal" value="16800"></div>
      <div><label for="m-own">Your contractor’s estimate ($)</label><input id="m-own" name="yours" inputmode="decimal" value="29400"></div>
      <div><label for="m-land">Award lands at</label><div class="range"><input id="m-land" type="range" name="land" min="0" max="100" step="5" value="50" data-unit="%"><output>50%</output></div><small>of the disputed amount</small></div>
    </div>
    <div class="calc-out" aria-live="polite">
      <p class="kpi"><small>Amount in dispute</small><b data-o="gap">—</b></p>
      <dl class="rows"><div><dt>Gap vs. carrier estimate</dt><dd data-o="pct">—</dd></div><div><dt>Projected award</dt><dd data-o="award">—</dd></div><div><dt>Increase before fees</dt><dd data-o="gain">—</dd></div></dl>
      <p class="say" data-o="msg">Figures are illustrative. Results update as you type.</p>
    </div>
  </div>
</div>"""

_DEP_ROW = """<tr><td><input name="item" value="{0}" aria-label="Item"></td><td><input name="rcv" inputmode="decimal" value="{1}" aria-label="Replacement cost in dollars"></td><td><input name="age" inputmode="decimal" value="{2}" aria-label="Age in years"></td><td><input name="life" inputmode="decimal" value="{3}" aria-label="Expected life in years"></td><td class="num" data-o="row">—</td><td><button type="button" class="x" aria-label="Remove row">×</button></td></tr>"""

HOLDBACK = f"""
<div class="calc wide" data-tool="dep">
  {_head("RCV &amp; ACV holdback calculator", "Add as many line items as you need")}
  <div class="calc-grid">
    <div class="calc-in">
      <div class="scroll-x"><table class="items"><thead><tr><th scope="col">Item</th><th scope="col">Replacement cost ($)</th><th scope="col">Age (yrs)</th><th scope="col">Life (yrs)</th><th scope="col">ACV</th><th scope="col"><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_DEP_ROW.format(*r) for r in [("Laminated shingle roof", 19800, 11, 30), ("Vinyl siding — north and west walls", 7400, 14, 30), ("Interior paint — first floor", 2600, 5, 10), ("Carpet — family room", 2100, 7, 12)]) + f"""
      </tbody></table></div>
      <p><button type="button" class="btn line sm" data-add>+ Add a line item</button></p>
      <div class="pair">
        <div><label for="d-ded">Deductible ($)</label><input id="d-ded" name="deduct" inputmode="decimal" value="1500"></div>
        <div><label for="d-cap">Depreciation cap</label><select id="d-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="100">No cap</option></select><small>Many estimates cap depreciation; check yours.</small></div>
      </div>
      <label class="tick"><input type="checkbox" name="nonrec"> My policy pays actual cash value only (no recoverable depreciation)</label>
      <label class="tick"><input type="checkbox" name="done"> Repairs are finished and invoiced</label>
    </div>
    <div class="calc-out" aria-live="polite">
      <div class="kpis"><p class="kpi"><small>First check (ACV − deductible)</small><b data-o="first">—</b></p><p class="kpi"><small data-o="heldlabel">Held back until repairs</small><b data-o="held">—</b></p><p class="kpi"><small>Total if fully recovered</small><b data-o="total">—</b></p></div>
      <dl class="rows">{_row("Replacement cost (RCV)", "rcv")}{_row("Total depreciation", "dep")}{_row("Depreciation share of RCV", "deppct")}{_row("Actual cash value (ACV)", "acv")}</dl>
      <p class="say" data-o="msg">Straight-line depreciation, illustrative only.</p>
    </div>
  </div>
</div>"""

ROOF = f"""
<div class="calc" data-tool="roof">
  {_head("Roof measurement calculator", "Check the squares on your estimate")}
  <div class="calc-grid">
    <div class="calc-in">
      <fieldset class="seg"><legend>How will you measure?</legend>
        <label class="tick"><input type="radio" name="mode" value="dims" checked> Footprint length × width</label>
        <label class="tick"><input type="radio" name="mode" value="area"> I know the footprint area</label>
      </fieldset>
      <div class="pair" data-mode="dims">
        <div><label for="r-l">Footprint length (ft)</label><input id="r-l" name="len" inputmode="decimal" value="54"></div>
        <div><label for="r-w">Footprint width (ft)</label><input id="r-w" name="wid" inputmode="decimal" value="32"></div>
      </div>
      <div data-mode="dims"><label for="r-oh">Eave overhang (inches)</label><input id="r-oh" name="oh" inputmode="decimal" value="12"></div>
      <div data-mode="area" hidden><label for="r-a">Footprint area incl. overhangs (sq ft)</label><input id="r-a" name="area" inputmode="decimal" value="2000"></div>
      <div class="pair">
        <div><label for="r-p">Roof pitch (rise per 12)</label><select id="r-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 7 else "", p) for p in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16]) + """</select></div>
        <div><label for="r-wst">Waste factor</label><select id="r-wst" name="waste"><option value="10">10% — plain gable</option><option value="13" selected>13% — gable with valleys</option><option value="15">15% — hip roof</option><option value="18">18% — cut-up / dormers</option></select></div>
      </div>
      <div class="pair">
        <div><label for="r-pr">Installed price per square ($, optional)</label><input id="r-pr" name="price" inputmode="decimal" placeholder="e.g. 540"></div>
        <div><label for="r-c">Squares on the carrier’s estimate (optional)</label><input id="r-c" name="carrier" inputmode="decimal" placeholder="e.g. 19.5"></div>
      </div>
    </div>
    <div class="calc-out" aria-live="polite">
      <p class="kpi"><small>Roof squares (before waste)</small><b data-o="sq">—</b></p>
      <dl class="rows">""" + _row("Pitch multiplier", "mult") + _row("Roof surface area", "surface") + _row("Squares with waste", "order") + _row("Shingle bundles (3 per square)", "bundles") + _row("Rough replacement cost", "cost") + _row("Versus the carrier’s squares", "vs") + """</dl>
      <p class="say" data-o="steep">Results update as you type.</p>
    </div>
  </div>
</div>"""

DEDUCT = f"""
<div class="calc" data-tool="deduct">
  {_head("Percentage deductible calculator", "Wind/hail % vs. flat")}
  <div class="calc-grid">
    <div class="calc-in">
      <div><label for="w-a">Dwelling coverage — Coverage A ($)</label><input id="w-a" name="cova" inputmode="decimal" value="312000"><small>From your declarations page.</small></div>
      <div class="pair">
        <div><label for="w-p">Wind/hail deductible</label><select id="w-p" name="pct"><option value="1" selected>1%</option><option value="2">2%</option><option value="3">3%</option><option value="5">5%</option></select></div>
        <div><label for="w-f">All-other-perils deductible ($)</label><input id="w-f" name="flat" inputmode="decimal" value="1000"></div>
      </div>
      <div><label for="w-l">Estimated storm damage ($)</label><input id="w-l" name="loss" inputmode="decimal" value="14800"></div>
    </div>
    <div class="calc-out" aria-live="polite">
      <p class="kpi"><small>Your percentage deductible in dollars</small><b data-o="pd">—</b></p>
      <div class="stack two" aria-hidden="true"><span class="s3"></span><span class="s1"></span></div>
      <ul class="key"><li><i class="s3"></i>You pay</li><li><i class="s1"></i>Policy pays</li></ul>
      <dl class="rows">{_row("Payment with the % deductible", "pdpay")}{_row("Payment if the flat deductible applied", "flatpay")}{_row("Extra out of pocket", "diff")}{_row("Deductible as a share of this loss", "share")}{_row("Break-even loss size", "breakeven")}</dl>
      <p class="say" data-o="below">Results update as you type.</p>
    </div>
  </div>
</div>"""

DATES = f"""
<div class="calc" data-tool="dates">
  {_head("Claim timeline builder", "Exports to your calendar")}
  <div class="calc-grid">
    <div class="calc-in">
      <div class="pair">
        <div><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div>
        <div><label for="t-dm">Appraisal demanded on (optional)</label><input id="t-dm" type="date" name="demand"></div>
      </div>
      <p><small>Every window is an editable default, not legal advice. Match each one to your policy.</small></p>
      <div class="days">
        <div><label for="t-n">Report claim (days)</label><input id="t-n" name="notice" inputmode="numeric" value="3"></div>
        <div><label for="t-m">Temporary repairs (days)</label><input id="t-m" name="mitig" inputmode="numeric" value="10"></div>
        <div><label for="t-p">Proof of loss (days)</label><input id="t-p" name="pol" inputmode="numeric" value="60"></div>
        <div><label for="t-r">RC holdback notice (days)</label><input id="t-r" name="rcd" inputmode="numeric" value="180"></div>
        <div><label for="t-s">Suit limitation (days)</label><input id="t-s" name="suit" inputmode="numeric" value="365"><small>Read your policy’s “Suit Against Us” clause.</small></div>
        <div><label for="t-a">Name appraiser after demand (days)</label><input id="t-a" name="appr" inputmode="numeric" value="20"></div>
      </div>
    </div>
    <div class="calc-out" aria-live="polite">
      <ol class="tl" data-o="timeline"><li><b>Pick your date of loss</b><span>Milestones appear here.</span></li></ol>
      <p><button type="button" class="btn sm" data-ics>Download .ics calendar file</button></p>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the insurer accepted coverage for at least part of the loss?", "Get coverage confirmed in writing. If the claim was denied outright, talk with a Kentucky attorney before thinking about appraisal."),
    (3, "Do you have the carrier’s full, itemized estimate — not just a summary page?", "Ask the adjuster for the complete line-item estimate in writing."),
    (3, "Do you have your own itemized estimate from a contractor or estimator?", "Get a line-item estimate. A one-line bid is hard to compare and easy to discount."),
    (2, "Do you have dated photos taken soon after the loss?", "Collect every photo, note the dates, and add photos of current conditions."),
    (2, "Have you found and read the policy’s Appraisal paragraph?", "Look in the Conditions section of the policy and note any time limits."),
    (2, "Do you know your policy’s suit-limitation date?", "Find the “Suit Against Us” clause and put the date on a calendar."),
    (2, "Were temporary repairs made, with receipts kept?", "Make reasonable temporary repairs and keep every receipt and invoice."),
    (2, "Has hidden damage (attic, decking, wall cavities) been opened up and documented?", "Make sure the full scope is visible before anyone prices it."),
    (1, "Is your correspondence with the carrier saved in date order?", "Gather letters, emails and claim notes into one dated file."),
    (2, "Is the gap more than about 10% of the carrier’s number or several thousand dollars?", "Run the appraisal payoff estimator. A small gap may not cover appraisal costs."),
]

READY = f"""
<div class="calc wide" data-tool="ready">
  {_head("Appraisal readiness checkup", "10 questions · about two minutes")}
  <div class="calc-grid">
    <div class="calc-in">
      <ol class="quiz">""" + "".join(
    '<li data-w="%d" data-fix="%s"><span>%s</span><span class="yn"><button type="button" class="yes" aria-pressed="false">Yes</button><button type="button" class="no" aria-pressed="false">No</button></span></li>' % (w, f, q)
    for w, q, f in _QUIZ) + """
      </ol>
      <p><button type="button" class="btn line sm" data-reset>Reset answers</button></p>
    </div>
    <div class="calc-out" aria-live="polite">
      <p class="kpi"><small>Readiness score</small><b><span data-o="score">–</span><em>/100</em></b></p>
      <div class="meter" aria-hidden="true"><span data-o="bar"></span><i style="left:45%"></i><i style="left:75%"></i></div>
      <p class="meter-k"><span>Not ready</span><span>Getting there</span><span>Strong</span></p>
      <p class="say" data-o="verdict">Answer the questions to see your score.</p>
      <p class="fix-t">Answered: <b data-o="count">0 / 10</b></p>
      <ul class="fix" data-o="todo"><li>Nothing flagged yet.</li></ul>
    </div>
  </div>
</div>"""

TREE = f"""
<div class="calc" data-tool="tree">
  {_head("Storm tree removal coverage calculator", "Ice storms &amp; windstorms")}
  <div class="calc-grid">
    <div class="calc-in">
      <div class="pair">
        <div><label for="x-n">Trees down</label><input id="x-n" name="trees" inputmode="numeric" value="3"></div>
        <div><label for="x-c">Removal cost per tree ($)</label><input id="x-c" name="cost" inputmode="decimal" value="850"></div>
      </div>
      <fieldset class="seg"><legend>Did a tree hit a covered structure or block a driveway or ramp?</legend>
        <label class="tick"><input type="radio" name="hit" value="yes" checked> Yes</label>
        <label class="tick"><input type="radio" name="hit" value="no"> No — it just fell in the yard</label>
      </fieldset>
      <div class="pair">
        <div><label for="x-pt">Per-tree limit ($)</label><input id="x-pt" name="pertree" inputmode="decimal" value="500"></div>
        <div><label for="x-po">Per-occurrence limit ($)</label><input id="x-po" name="perocc" inputmode="decimal" value="1000"></div>
      </div>
      <small>Defaults reflect limits common on many homeowners forms. Check your policy’s debris-removal wording.</small>
    </div>
    <div class="calc-out" aria-live="polite">
      <p class="kpi"><small>Estimated covered tree removal</small><b data-o="covered">—</b></p>
      <div class="stack two" aria-hidden="true"><span class="s1"></span><span class="s3"></span></div>
      <ul class="key"><li><i class="s1"></i>Policy may pay</li><li><i class="s3"></i>Out of pocket</li></ul>
      <dl class="rows">{_row("Total removal cost", "total")}{_row("Capped per tree", "capped")}{_row("Out of pocket (before deductible)", "oop")}</dl>
      <p class="say" data-o="msg">Results update as you type.</p>
    </div>
  </div>
</div>"""

_ICONS = {"Calculator": "÷", "Estimator": "≈", "Planner": "▦", "Checkup": "✓"}
_MARKUP = {
    "appraisal-payoff-estimator": PAYOFF, "rcv-acv-holdback-calculator": HOLDBACK, "roof-measurement-calculator": ROOF,
    "percentage-deductible-calculator": DEDUCT, "claim-timeline-builder": DATES, "appraisal-readiness-checkup": READY,
    "tree-removal-coverage-calculator": TREE,
}

TOOLS = []
for slug, markup in _MARKUP.items():
    c = dict(TOOL_COPY[slug])
    c.update(slug=slug, markup=markup, icon=_ICONS.get(c.get("kind"), "÷"))
    TOOLS.append(c)
