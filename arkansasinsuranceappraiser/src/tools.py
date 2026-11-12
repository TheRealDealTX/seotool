"""Free claim tools: markup and copy. Logic lives in static/assets/js/app.js. All math runs in the browser."""


def _bar(name, note):
    return f'<div class="calc-bar"><span>{name}</span><em>{note}</em></div>'


GAPFEE = """
<div class="calc" data-tool="gapfee">
  """ + _bar("Claim gap &amp; fee estimator", "Nothing leaves your browser") + """
  <div class="calc-grid">
    <div class="calc-in">
      <div class="pair">
        <div><label for="gf-ins">Carrier’s estimate (RCV)</label><input id="gf-ins" name="insurer" inputmode="decimal" value="21600"><small class="note">Replacement cost total before depreciation and deductible.</small></div>
        <div><label for="gf-own">Your estimate (RCV)</label><input id="gf-own" name="yours" inputmode="decimal" value="36400"><small class="note">From your contractor or an independent estimator.</small></div>
      </div>
      <div class="pair">
        <div><label for="gf-ft">Appraiser fee basis</label><select id="gf-ft" name="feetype"><option value="pct">Percent of the increase</option><option value="flat">Flat fee</option><option value="hourly">Hourly</option></select></div>
        <div><label for="gf-fee">Fee (% or $)</label><input id="gf-fee" name="fee" inputmode="decimal" value="10"></div>
      </div>
      <div class="pair" data-hourly hidden>
        <div><label for="gf-hr">Estimated hours</label><input id="gf-hr" name="hours" inputmode="decimal" value="20"></div>
        <div><label for="gf-rate">Hourly rate ($)</label><input id="gf-rate" name="rate" inputmode="decimal" value="150"></div>
      </div>
      <div><label for="gf-ump">Umpire’s total fee, if needed ($)</label><input id="gf-ump" name="umpire" inputmode="decimal" value="3200"><small class="note">You usually pay half. Enter 0 if the appraisers are likely to agree.</small></div>
      <div><label for="gf-land">Your own scenario: award lands at</label>
        <div class="slider"><input id="gf-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="% of the gap"><output>55% of the gap</output></div></div>
    </div>
    <div class="calc-out" aria-live="polite">
      <div class="readout"><small>Net increase in your scenario</small><b data-o="net">$0</b></div>
      <div class="meter" aria-hidden="true"><i class="m1"></i><i class="m2"></i><i class="m3"></i></div>
      <ul class="key"><li><i class="m1"></i>Carrier’s number</li><li><i class="m2"></i>Your net gain</li><li><i class="m3"></i>Appraisal costs</li></ul>
      <div class="table-wrap"><table class="scen"><thead><tr><th>Award lands at</th><th>Gross increase</th><th>Your costs</th><th>Net to you</th></tr></thead><tbody data-o="scen"></tbody></table></div>
      <dl class="calc-rows">
        <div><dt>Amount in dispute</dt><dd data-o="gap">$0</dd></div>
        <div><dt>Gap vs. carrier estimate</dt><dd data-o="pct">—</dd></div>
        <div><dt>Break-even award point</dt><dd data-o="breakeven">—</dd></div>
      </dl>
      <p class="verdict" data-o="msg"></p>
    </div>
  </div>
</div>"""

GAP_MINI = """
<div class="calc calc-mini" data-tool="gapfee">
  """ + _bar("Quick claim gap check", "Illustrative only") + """
  <div class="calc-grid">
    <div class="calc-in">
      <div><label for="mg-ins">Carrier’s estimate</label><input id="mg-ins" name="insurer" inputmode="decimal" value="15800"></div>
      <div><label for="mg-own">Your contractor’s estimate</label><input id="mg-own" name="yours" inputmode="decimal" value="27300"></div>
      <div><label for="mg-land">Award lands at</label><div class="slider"><input id="mg-land" type="range" name="land" min="0" max="100" step="5" value="50" data-unit="%"><output>50%</output></div></div>
    </div>
    <div class="calc-out" aria-live="polite">
      <div class="readout"><small>Amount in dispute</small><b data-o="gap">$0</b></div>
      <dl class="calc-rows">
        <div><dt>Gap vs. carrier estimate</dt><dd data-o="pct">—</dd></div>
        <div><dt>Increase before fees</dt><dd data-o="gross">$0</dd></div>
      </dl>
      <p class="verdict" data-o="msg"></p>
    </div>
  </div>
</div>"""

_HB_ROW = ('<tr><td><input name="item" value="{0}" aria-label="Item"></td><td><input name="rcv" inputmode="decimal" value="{1}" aria-label="Replacement cost"></td>'
           '<td><input name="labor" inputmode="decimal" value="{2}" aria-label="Labor share percent"></td><td><input name="age" inputmode="decimal" value="{3}" aria-label="Age in years"></td>'
           '<td><input name="life" inputmode="decimal" value="{4}" aria-label="Expected life in years"></td><td class="num" data-o="row">$0</td><td><button type="button" class="rm" aria-label="Remove row">×</button></td></tr>')

HOLDBACK = """
<div class="calc calc-wide" data-tool="holdback">
  """ + _bar("RCV vs. ACV holdback calculator", "Add as many line items as you need") + """
  <div class="calc-grid">
    <div class="calc-in">
      <div class="table-wrap items"><table><thead><tr><th>Item</th><th>RCV ($)</th><th>Labor %</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
      """ + "".join(_HB_ROW.format(*r) for r in [("Laminated shingle roof", 19800, 45, 8, 30), ("Gutters &amp; downspouts", 2300, 40, 12, 25), ("Interior paint, two rooms", 1900, 70, 5, 10), ("LVP flooring, living area", 4600, 35, 4, 20)]) + """
      </tbody></table></div>
      <p><button type="button" class="btn btn-line btn-sm" data-add data-run>+ Add a line item</button></p>
      <div class="pair">
        <div><label for="hb-ded">Deductible ($)</label><input id="hb-ded" name="deduct" inputmode="decimal" value="2000"></div>
        <div><label for="hb-cap">Depreciation cap</label><select id="hb-cap" name="cap"><option value="50">50%</option><option value="70">70%</option><option value="80" selected>80%</option><option value="100">No cap</option></select></div>
      </div>
      <label class="tick"><input type="checkbox" name="matonly" checked> Depreciate materials only (leave the labor share undepreciated)</label>
      <label class="tick"><input type="checkbox" name="acvonly"> My policy pays actual cash value only</label>
    </div>
    <div class="calc-out" aria-live="polite">
      <div class="readouts">
        <div class="readout"><small>First check (ACV − deductible)</small><b data-o="first">$0</b></div>
        <div class="readout"><small>Held back until repairs</small><b data-o="held">$0</b></div>
        <div class="readout"><small>Total if fully recovered</small><b data-o="total">$0</b></div>
      </div>
      <dl class="calc-rows">
        <div><dt>Replacement cost (RCV)</dt><dd data-o="rcv">$0</dd></div>
        <div><dt>Depreciation applied</dt><dd data-o="dep">$0</dd></div>
        <div><dt>Depreciation if labor were depreciated too</dt><dd data-o="depall">$0</dd></div>
        <div><dt>Difference on the first check</dt><dd data-o="labordiff">$0</dd></div>
      </dl>
      <p class="verdict" data-o="msg"></p>
    </div>
  </div>
</div>"""

ROOF = """
<div class="calc" data-tool="roof">
  """ + _bar("Roof pitch &amp; squares calculator", "Check the quantities in your estimate") + """
  <div class="calc-grid">
    <div class="calc-in">
      <div class="pair">
        <div><label for="rf-l">Footprint length (ft)</label><input id="rf-l" name="len" inputmode="decimal" value="62"></div>
        <div><label for="rf-w">Footprint width (ft)</label><input id="rf-w" name="wid" inputmode="decimal" value="36"></div>
      </div>
      <div class="pair">
        <div><label for="rf-oh">Eave overhang (in)</label><input id="rf-oh" name="oh" inputmode="decimal" value="16"></div>
        <div><label for="rf-p">Pitch (rise per 12)</label><select id="rf-p" name="pitch">""" + "".join('<option value="%d"%s>%d/12</option>' % (p, " selected" if p == 7 else "", p) for p in [3, 4, 5, 6, 7, 8, 9, 10, 12, 14]) + """</select></div>
      </div>
      <div class="pair">
        <div><label for="rf-s">Roof style</label><select id="rf-s" name="style"><option value="gable" data-waste="10">Gable</option><option value="hip" data-waste="15" selected>Hip</option><option value="complex" data-waste="20">Cut-up / complex</option></select></div>
        <div><label for="rf-pr">Installed price per square ($, optional)</label><input id="rf-pr" name="price" inputmode="decimal" placeholder="e.g. 560"></div>
      </div>
    </div>
    <div class="calc-out" aria-live="polite">
      <div class="readout"><small>Roof squares (before waste)</small><b data-o="sq">0</b></div>
      <dl class="calc-rows">
        <div><dt>Pitch angle / multiplier</dt><dd data-o="mult">—</dd></div>
        <div><dt>Roof surface area</dt><dd data-o="surface">0</dd></div>
        <div><dt>Waste for this style</dt><dd data-o="waste">—</dd></div>
        <div><dt>Squares to order</dt><dd data-o="order">0</dd></div>
        <div><dt>Shingle bundles (3 per square)</dt><dd data-o="bundles">0</dd></div>
        <div><dt>Drip edge (eaves + rakes, approx.)</dt><dd data-o="drip">0</dd></div>
        <div><dt>Ridge (+ hips, approx.)</dt><dd data-o="ridge">0</dd></div>
        <div><dt>Rough replacement cost</dt><dd data-o="cost">—</dd></div>
      </dl>
      <p class="verdict" data-o="steep"></p>
    </div>
  </div>
</div>"""

DEDUCT = """
<div class="calc" data-tool="pctded">
  """ + _bar("Percentage deductible calculator", "Wind/hail vs. all other perils") + """
  <div class="calc-grid">
    <div class="calc-in">
      <div><label for="pd-a">Dwelling limit (Coverage A, $)</label><input id="pd-a" name="cova" inputmode="decimal" value="310000"><small class="note">From your declarations page.</small></div>
      <div class="pair">
        <div><label for="pd-p">Wind/hail deductible</label><select id="pd-p" name="pct"><option value="1">1%</option><option value="2" selected>2%</option><option value="3">3%</option><option value="5">5%</option></select></div>
        <div><label for="pd-f">All-other-perils deductible ($)</label><input id="pd-f" name="flat" inputmode="decimal" value="1500"></div>
      </div>
      <div><label for="pd-l">Estimated storm damage ($)</label><input id="pd-l" name="loss" inputmode="decimal" value="17800"></div>
    </div>
    <div class="calc-out" aria-live="polite">
      <div class="readout"><small>Your wind/hail deductible in dollars</small><b data-o="pd">$0</b></div>
      <div class="meter two" aria-hidden="true"><i class="m3"></i><i class="m1"></i></div>
      <ul class="key"><li><i class="m3"></i>You pay</li><li><i class="m1"></i>Policy pays</li></ul>
      <dl class="calc-rows">
        <div><dt>Policy pays with this deductible</dt><dd data-o="pdpay">$0</dd></div>
        <div><dt>Policy would pay with the flat deductible</dt><dd data-o="flatpay">$0</dd></div>
        <div><dt>Extra out of pocket</dt><dd data-o="diff">$0</dd></div>
      </dl>
      <div class="table-wrap"><table class="scen"><thead><tr><th>If your deductible were</th><th>In dollars</th><th>Policy pays</th></tr></thead><tbody data-o="cmp"></tbody></table></div>
      <p class="verdict" data-o="below"></p>
    </div>
  </div>
</div>"""

TIMELINE = """
<div class="calc" data-tool="timeline">
  """ + _bar("Claim timeline builder", "Export to Google, Apple or Outlook calendar") + """
  <div class="calc-grid">
    <div class="calc-in">
      <div class="pair">
        <div><label for="tl-d">Date of loss</label><input id="tl-d" type="date" name="dol"></div>
        <div><label for="tl-r">Date carrier requested proof of loss (optional)</label><input id="tl-r" type="date" name="req"></div>
      </div>
      <p class="note">Set each window to match your own policy. The defaults are placeholders, not legal advice.</p>
      <div class="days">
        <div><label for="tl-n">Report the claim (days)</label><input id="tl-n" name="notice" inputmode="numeric" value="2"></div>
        <div><label for="tl-m">Temporary repairs (days)</label><input id="tl-m" name="mitig" inputmode="numeric" value="10"></div>
        <div><label for="tl-e">Get your own estimate (days)</label><input id="tl-e" name="est" inputmode="numeric" value="30"></div>
        <div><label for="tl-p">Proof of loss after request (days)</label><input id="tl-p" name="pol" inputmode="numeric" value="60"></div>
        <div><label for="tl-a">Name appraiser after demand (days)</label><input id="tl-a" name="appr" inputmode="numeric" value="20"></div>
        <div><label for="tl-c">Replacement-cost recovery (days)</label><input id="tl-c" name="rcd" inputmode="numeric" value="365"></div>
        <div><label for="tl-s">Suit limitation in your policy (days)</label><input id="tl-s" name="suit" inputmode="numeric" value="730"></div>
      </div>
    </div>
    <div class="calc-out" aria-live="polite">
      <ol class="tline" data-o="list"></ol>
      <p><button type="button" class="btn btn-sm" data-ics>Download .ics calendar file</button></p>
    </div>
  </div>
</div>"""

_QUIZ = [
    (3, "Has the carrier accepted coverage for at least part of the loss?", "Get written confirmation of what was accepted. If the claim was denied outright, talk with an Arkansas attorney first."),
    (3, "Do you have the carrier’s complete, line-item estimate?", "Ask in writing for the full itemized estimate, not just the payment summary."),
    (3, "Do you have your own itemized estimate?", "Get a line-item estimate from a contractor or estimator. A lump-sum bid carries little weight with a panel."),
    (2, "Do you have dated photos taken soon after the loss?", "Collect every photo and note when each was taken. Add photos of current conditions."),
    (2, "Have you read your policy’s appraisal paragraph?", "Find the appraisal condition and note the deadline to name an appraiser."),
    (2, "Do you know your replacement-cost and suit-limitation deadlines?", "Find both dates in your policy and add them to a calendar. Our timeline builder can help."),
    (2, "Has all hidden damage been opened up and documented?", "Make sure attics, wall cavities, decking and crawl spaces were checked so the scope is complete."),
    (2, "Are temporary repairs done and receipts saved?", "Complete reasonable temporary repairs and keep every receipt."),
    (1, "Do you have your current declarations page?", "Download it from your insurer’s portal or ask your agent."),
    (1, "Is your carrier correspondence organized by date?", "Gather letters, emails and adjuster notes in date order."),
    (2, "Is the gap more than about 10% or $5,000?", "Run the claim gap and fee estimator. A small gap may not justify appraisal costs."),
    (1, "Did you submit proof of loss if one was requested?", "If a sworn proof of loss was requested, submit it on time."),
]

READY = """
<div class="calc calc-wide" data-tool="ready">
  """ + _bar("Appraisal readiness checkup", "12 questions · about two minutes") + """
  <div class="calc-grid">
    <div class="calc-in">
      <ol class="quiz">""" + "".join(
    '<li data-w="%d" data-fix="%s"><span>%s</span><span class="yn"><button type="button" class="yes" aria-pressed="false">Yes</button><button type="button" class="no" aria-pressed="false">No</button></span></li>' % (w, f, q)
    for w, q, f in _QUIZ) + """
      </ol>
      <p><button type="button" class="btn btn-line btn-sm" data-reset>Clear answers</button></p>
    </div>
    <div class="calc-out" aria-live="polite">
      <div class="ring-wrap"><svg class="ring" viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="50" fill="none" stroke="#efe4e2" stroke-width="12"/><circle data-o="arc" cx="60" cy="60" r="50" fill="none" stroke="#8f1d24" stroke-width="12" stroke-linecap="round" stroke-dasharray="314.2" stroke-dashoffset="314.2" transform="rotate(-90 60 60)"/></svg><span class="ring-num" data-o="score">–</span></div>
      <p class="note" style="text-align:center">Answered <span data-o="count">0 / 12</span></p>
      <p class="verdict" data-o="verdict"></p>
      <p class="todo-h">Your to-do list</p>
      <ul data-o="todo" class="todo"></ul>
    </div>
  </div>
</div>"""

ICE = """
<div class="calc" data-tool="ice">
  """ + _bar("Ice load limb calculator", "Glaze ice on a single limb") + """
  <div class="calc-grid">
    <div class="calc-in">
      <div class="pair">
        <div><label for="ic-d">Limb diameter (in)</label><input id="ic-d" name="dia" inputmode="decimal" value="4"></div>
        <div><label for="ic-l">Limb length (ft)</label><input id="ic-l" name="len" inputmode="decimal" value="20"></div>
      </div>
      <div><label for="ic-t">Radial ice thickness</label><div class="slider"><input id="ic-t" type="range" name="ice" min="0.25" max="1.5" step="0.25" value="0.5" data-unit=" in"><output>0.5 in</output></div><small class="note">The January 2009 storm left roughly an inch or more in parts of north Arkansas.</small></div>
      <div class="pair">
        <div><label for="ic-tw">Twig factor</label><select id="ic-tw" name="twig"><option value="1">Bare limb only</option><option value="2" selected>Some side branches (×2)</option><option value="4">Dense twigs (×4)</option></select><small class="note">Small twigs collect far more ice than their size suggests.</small></div>
        <div><label for="ic-n">Similar limbs over the roof</label><input id="ic-n" name="count" inputmode="numeric" value="6"></div>
      </div>
    </div>
    <div class="calc-out" aria-live="polite">
      <div class="readout"><small>Ice weight added to one limb</small><b data-o="ice1">0 lb</b></div>
      <dl class="calc-rows">
        <div><dt>Green wood weight of the limb</dt><dd data-o="wood">0 lb</dd></div>
        <div><dt>Load increase from ice</dt><dd data-o="inc">0%</dd></div>
        <div><dt>Ice on all similar limbs</dt><dd data-o="all">0 lb</dd></div>
      </dl>
      <p class="verdict" data-o="msg"></p>
    </div>
  </div>
</div>"""

TOOLS = [
    {
        "slug": "claim-gap-fee-estimator", "kw": "claim gap estimator",
        "name": "Claim Gap & Fee Estimator", "kind": "Estimator", "icon": "gap",
        "short": "Compare estimates, test three award scenarios and see your net after appraiser and umpire fees.",
        "title": "Claim Gap Estimator with Appraisal Fees | Free",
        "desc": "Free claim gap estimator: compare your estimate with the carrier’s, test award scenarios and subtract appraiser and umpire fees to see your net.",
        "h1": "Claim Gap Estimator: Will Appraisal Pay Off After Fees?",
        "lede": "Enter the two estimates you already have, choose how your appraiser charges, and see three illustrative award scenarios side by side with your break-even point.",
        "markup": GAPFEE,
        "explain": """
<h2>How the estimator works</h2>
<p>The <strong>amount in dispute</strong> is your estimate minus the carrier’s. An appraisal award often lands somewhere inside that gap, so the tool shows three illustrative outcomes (25%, 50% and 75% of the gap) plus a scenario you set with the slider.</p>
<p>For each outcome it subtracts your likely costs: your appraiser’s fee (percentage, flat or hourly) and half of the umpire’s fee. The <strong>break-even point</strong> is the share of the gap the award must reach before you come out ahead.</p>
<h2>Reading the results</h2>
<ul><li>If even the 75% scenario nets little, a documented supplement request is usually a better first step.</li>
<li>If the 25% scenario is already clearly positive, appraisal may be worth a serious look.</li>
<li>All figures are illustrative. Real awards depend on the evidence and the panel.</li></ul>""",
        "faqs": [
            ("Why doesn’t the tool assume I get my full number?", "Panels often land between the two estimates. Planning on a range is more realistic than planning on a best case."),
            ("Should I include the umpire fee?", "Include it if the appraisers may not agree on everything. Many residential panels settle without an umpire decision."),
            ("Does this include my deductible?", "No. The deductible applies either way, so it doesn’t change the gap between estimates."),
        ],
    },
    {
        "slug": "rcv-acv-holdback-calculator", "kw": "RCV ACV calculator",
        "name": "RCV vs. ACV Holdback Calculator", "kind": "Calculator", "icon": "dep",
        "short": "Line-item depreciation with a labor-share toggle, showing your first check and the holdback.",
        "title": "RCV vs. ACV Calculator | Depreciation & Holdback",
        "desc": "Free RCV vs. ACV calculator: depreciate each line item, compare materials-only and full depreciation, and see your first check and holdback.",
        "h1": "RCV vs. ACV Calculator: Depreciation and Holdback by Line Item",
        "lede": "See how depreciation turns replacement cost into your first check, and how much is held back until repairs are done. A labor-share column shows how depreciating labor changes the numbers.",
        "markup": HOLDBACK,
        "explain": """
<h2>How depreciation is estimated here</h2>
<p>Each line uses straight-line depreciation: age divided by expected life, up to the cap you choose. With <em>Depreciate materials only</em> checked, the labor share you enter is left undepreciated. Uncheck it to see what the first check would look like if the whole line were depreciated.</p>
<h2>Why the labor column is there</h2>
<p>Arkansas courts have addressed whether labor can be depreciated when calculating actual cash value, in decisions including <em>Adams v. Cameron Mutual</em> (2013) and <em>Shelter Mutual v. Goodner</em> (2015). The law can change, so treat the comparison as illustrative and talk to an Arkansas attorney if the question matters to your claim. Our guide on <a href="/appraisal-guides/labor-depreciation-arkansas-acv/">labor depreciation in Arkansas</a> explains more.</p>
<h2>First check and holdback</h2>
<p>The first check is ACV minus the deductible. The holdback is recoverable depreciation, paid after repairs are completed within the policy’s time limit. ACV-only policies don’t pay the holdback.</p>""",
        "faqs": [
            ("What expected life should I use?", "Common figures are 25–30 years for laminated shingles, 10 years for interior paint and 15–25 years for many floor coverings. Your carrier’s estimate may list its own."),
            ("Why is there a depreciation cap?", "Many estimates cap depreciation so an item never drops to zero value. Check what your estimate used."),
            ("Is this how my carrier calculated it?", "Not necessarily. Carriers use their own methods and condition adjustments. Use this to ask informed questions."),
        ],
    },
    {
        "slug": "roof-pitch-squares-calculator", "kw": "roof squares calculator",
        "name": "Roof Pitch & Squares Calculator", "kind": "Calculator", "icon": "roof",
        "short": "Footprint, overhang, pitch and roof style into squares, bundles, drip edge and ridge lengths.",
        "title": "Roof Squares Calculator | Pitch, Waste & Bundles",
        "desc": "Free roof squares calculator: turn footprint, overhang, pitch and roof style into squares, bundles, drip edge and ridge lengths to check an estimate.",
        "h1": "Roof Squares Calculator with Pitch, Waste and Accessories",
        "lede": "Roof measurements drive the biggest line items on a hail or wind estimate. Check whether the squares, waste and accessory lengths in your estimate are in the right range.",
        "markup": ROOF,
        "explain": """
<h2>The math</h2>
<p>The footprint plus overhangs is multiplied by the pitch factor, √(1 + (rise ÷ 12)²), to get roof surface area. Divide by 100 for squares. Waste depends on style: about 10% for a simple gable, 15% for a hip and 20% for a cut-up roof with valleys and dormers.</p>
<p>Drip edge is approximated from the perimeter. Ridge length is the long dimension for a gable; for a hip, hip lengths are added using the pitch. These are rough checks; a measured report or field measurement is more precise.</p>
<h2>What to compare</h2>
<ul><li>If the estimate’s squares are much lower than this result, ask how the roof was measured.</li>
<li>Check that steep charges appear when the pitch is 7/12 or steeper, and high-roof charges for two-story eaves.</li>
<li>Look for starter strip, drip edge, ridge cap and flashing as separate lines.</li></ul>""",
        "faqs": [
            ("Why is my result different from a measurement report?", "Footprint math assumes one pitch and a simple shape. Reports measure each facet separately."),
            ("Does waste get paid on a claim?", "Estimates normally include a waste factor on shingles because material is cut and lost during installation."),
            ("What price per square should I use?", "Use a local contractor’s quote. Prices vary by shingle type, tear-off layers and access."),
        ],
    },
    {
        "slug": "wind-hail-percentage-deductible", "kw": "percentage deductible calculator",
        "name": "Percentage Deductible Calculator", "kind": "Calculator", "icon": "pct",
        "short": "Turn a 1%, 2% or 5% wind/hail deductible into dollars and see what the policy actually pays.",
        "title": "Percentage Deductible Calculator | Wind & Hail",
        "desc": "Free percentage deductible calculator: convert a 1%, 2% or 5% wind and hail deductible into dollars and compare what the policy pays on a storm loss.",
        "h1": "Percentage Deductible Calculator for Wind and Hail Claims",
        "lede": "Many Arkansas policies use a wind/hail deductible set as a percentage of the dwelling limit. On a large home, that percentage can be thousands of dollars more than a flat deductible.",
        "markup": DEDUCT,
        "explain": """
<h2>How percentage deductibles work</h2>
<p>A 2% deductible on a $310,000 dwelling limit is $6,200, applied to each covered wind or hail loss. It’s based on the dwelling limit, not the size of the claim, so a modest roof claim can fall mostly or entirely within it.</p>
<h2>Why it matters for appraisal</h2>
<p>The deductible comes off the final amount of loss. If an appraisal raises the award from $9,000 to $14,000 on a policy with a $6,200 deductible, the payment rises from $2,800 to $7,800. Always look at the net, not the gross.</p>
<h2>Two storms in one season</h2>
<p>Each separate storm is usually a separate occurrence with its own deductible. Northwest Arkansas owners sometimes face two hail events in one spring, so keep the dates and damage of each storm distinct.</p>""",
        "faqs": [
            ("Where do I find my wind/hail deductible?", "On your declarations page, usually listed separately from the all-other-perils deductible."),
            ("Can I change my deductible?", "Often at renewal. A lower percentage costs more in premium; ask your agent for options."),
            ("Does the deductible apply to contents too?", "Usually it applies once per occurrence to the whole claim. Check your policy wording."),
        ],
    },
    {
        "slug": "claim-timeline-builder", "kw": "claim deadline calendar",
        "name": "Claim Timeline Builder", "kind": "Planner", "icon": "cal",
        "short": "Build a dated timeline of claim milestones and export it as a calendar file.",
        "title": "Claim Deadline Calendar Builder | .ics Export",
        "desc": "Build a claim deadline calendar from your date of loss: notice, repairs, proof of loss, appraiser naming, recovery and suit dates, with .ics export.",
        "h1": "Claim Deadline Calendar: Build and Export Your Timeline",
        "lede": "Enter your date of loss, adjust each window to match your policy, and download every milestone to your phone’s calendar so nothing slips while the claim is open.",
        "markup": TIMELINE,
        "explain": """
<h2>Why a timeline matters</h2>
<p>Property claims carry several clocks at once. Some come from the policy, such as proof of loss, the window to name an appraiser and the replacement-cost recovery period. Others, like the suit-limitation period, can end your options if they pass unnoticed.</p>
<h2>Setting the windows</h2>
<ul><li><strong>Proof of loss:</strong> if the carrier requested one, enter the request date. The deadline is counted from that date.</li>
<li><strong>Appraiser naming:</strong> counted here from the date of loss as a planning placeholder. Once a demand is sent, count from the demand date.</li>
<li><strong>Suit limitation:</strong> read your policy’s “Suit Against Us” condition and ask an Arkansas attorney how it applies.</li></ul>
<p>The .ics file works with Google Calendar, Apple Calendar and Outlook. It’s generated in your browser; nothing is uploaded.</p>""",
        "faqs": [
            ("Are the default numbers Arkansas law?", "No. They are placeholders. Your policy and Arkansas law control, and an attorney can confirm deadlines."),
            ("Does invoking appraisal stop the suit clock?", "Don’t assume so. Ask an attorney about your specific situation if a deadline is approaching."),
            ("Is my date stored anywhere?", "No. Everything runs in your browser and disappears when you close the page."),
        ],
    },
    {
        "slug": "appraisal-readiness-checkup", "kw": "appraisal readiness checklist",
        "name": "Appraisal Readiness Checkup", "kind": "Checklist", "icon": "check",
        "short": "Twelve weighted questions that score your file and build a to-do list before you invoke appraisal.",
        "title": "Appraisal Readiness Checklist | Free Score",
        "desc": "Free appraisal readiness checklist: answer 12 questions to score your claim file and get a to-do list before you demand appraisal on your claim.",
        "h1": "Appraisal Readiness Checklist: Is Your File Ready?",
        "lede": "Invoking appraisal before your file is ready can lock in a low award. Answer twelve questions and get a weighted score plus a personal to-do list.",
        "markup": READY,
        "explain": """
<h2>How the score works</h2>
<p>Each question carries a weight from 1 to 3 based on how much it affects an appraisal. Coverage acceptance and having both itemized estimates weigh most, because without them a panel has nothing to compare.</p>
<h2>What the bands mean</h2>
<ul><li><strong>75 and up:</strong> your file has what a panel expects. The next step is a professional look at the dollar gap.</li>
<li><strong>45–74:</strong> close the gaps on your to-do list before you invoke appraisal.</li>
<li><strong>Below 45:</strong> appraisal now risks an incomplete award. Work through the list first.</li></ul>""",
        "faqs": [
            ("Is a high score a guarantee?", "No. It means your documentation is in good shape, not that the award will match your number."),
            ("What if the claim was denied?", "Then appraisal usually isn’t the right tool. Talk to an Arkansas attorney about the denial."),
            ("Can I retake the checkup?", "Yes. Clear your answers and run it again as you complete items."),
        ],
    },
    {
        "slug": "ice-load-limb-calculator", "kw": "ice load calculator",
        "name": "Ice Load Limb Calculator", "kind": "Arkansas tool", "icon": "ice",
        "short": "See how much weight glaze ice adds to a tree limb, and why healthy trees fail in Arkansas ice storms.",
        "title": "Ice Load Calculator for Tree Limbs | Ice Storms",
        "desc": "Free ice load calculator: estimate the weight glaze ice adds to a tree limb and why healthy trees fail on roofs during Arkansas ice storms.",
        "h1": "Ice Load Calculator: How Much Weight Ice Adds to a Limb",
        "lede": "Freezing rain coats every limb in clear ice. This calculator estimates the added weight on a single limb and across the limbs hanging over your roof.",
        "markup": ICE,
        "explain": """
<h2>The physics</h2>
<p>Glaze ice weighs about 57 pounds per cubic foot. The tool treats the limb as a cylinder and adds a uniform shell of ice around it: ice volume = π × length × ((r + t)² − r²), where r is the limb radius and t is the ice thickness. A twig factor accounts for side branches, which collect ice out of proportion to their size. Green hardwood is estimated at about 55 pounds per cubic foot.</p>
<h2>Why it matters for a claim</h2>
<p>Insurers sometimes argue that a limb failed because the tree was dead or decayed. Showing the load the ice imposed helps explain why healthy limbs failed during storms like December 2000 and January 2009. Photos of the break, showing sound wood, are strong evidence.</p>
<h2>Limits of the estimate</h2>
<p>Real ice accretion is uneven, wind adds dynamic load, and wood density varies by species and moisture. Treat the results as illustrative, not an engineering analysis.</p>""",
        "faqs": [
            ("Is a tree falling on my house covered if the tree was healthy?", "Generally the damage to the covered structure is covered, with limited coverage for removal. Policy wording controls."),
            ("What if the tree was dead?", "Carriers may argue maintenance issues, but the damage to your home may still be covered. Coverage disputes like this may need legal advice."),
            ("Should I photograph the broken limb?", "Yes. Close-ups of the break showing sound or decayed wood help establish why it failed."),
        ],
    },
]
