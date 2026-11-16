"""Seven free claim tools for Mississippi property owners: markup + explanatory copy.
All math runs in static/assets/js/app.js. Nothing is stored or sent."""

B = "/claim-calculator-suite/"


def _f(fid, name, label, value="", hint="", mode="decimal", extra=""):
    h = f'<small class="hint">{hint}</small>' if hint else ""
    v = f' value="{value}"' if value != "" else ""
    return f'<div class="fld"><label for="{fid}">{label}</label><input id="{fid}" name="{name}" inputmode="{mode}"{v}{extra}>{h}</div>'


def _sel(fid, name, label, opts, sel, hint=""):
    o = "".join(f'<option value="{v}"{" selected" if v == sel else ""}>{t}</option>' for v, t in opts)
    h = f'<small class="hint">{hint}</small>' if hint else ""
    return f'<div class="fld"><label for="{fid}">{label}</label><select id="{fid}" name="{name}">{o}</select>{h}</div>'


def _head(title, tag):
    return f'<div class="calc-head"><p class="calc-title">{title}</p><span class="calc-tag">{tag}</span></div>'


# 1 -------------------------------------------------------------- payoff estimator
PAYOFF = f"""
<div class="calc" data-tool="gap">
{_head("Appraisal payoff estimator", "Private · runs in your browser")}
<div class="calc-grid">
<div class="calc-in">
<div class="two">{_f("g-ins", "insurer", "Carrier’s estimate (RCV, $)", "21600", "Replacement cost total before depreciation.")}{_f("g-own", "yours", "Your estimate (RCV, $)", "36400", "Contractor or independent line-item estimate.")}</div>
<div class="fld"><label for="g-land">Where could the award land inside the gap?</label><div class="range"><input id="g-land" type="range" name="land" min="0" max="100" step="5" value="55" data-unit="%"><output>55%</output></div><small class="hint">0% = carrier’s number holds · 100% = your full number is awarded.</small></div>
<div class="two">{_sel("g-ft", "feetype", "Your appraiser’s fee", [("flat", "Flat fee ($)"), ("pct", "Percent of the increase (%)"), ("hourly", "Hourly (hours × rate)")], "flat")}{_f("g-fee", "fee", "Fee amount / percent / hours", "2800")}</div>
<div class="two">{_f("g-rate", "rate", "Hourly rate ($, if hourly)", "175")}{_f("g-ump", "umpire", "Umpire’s total fee ($)", "3200", "Usually split 50/50.")}</div>
<label class="chk"><input type="checkbox" name="useump" checked> Assume an umpire is needed</label>
</div>
<div class="calc-out" aria-live="polite">
<div class="kpi"><small>Estimated net gain to you</small><b data-o="net">$0</b></div>
<div class="bar" aria-hidden="true"><span class="b1"></span><span class="b2"></span><span class="b3"></span></div>
<ul class="key"><li><i class="b1"></i>Carrier’s number</li><li><i class="b2"></i>Your net gain</li><li><i class="b3"></i>Appraisal costs</li></ul>
<dl class="rows">
<div><dt>Amount in dispute</dt><dd data-o="gap">$0</dd></div>
<div><dt>Gap vs. carrier estimate</dt><dd data-o="pct">—</dd></div>
<div><dt>Projected award (RCV)</dt><dd data-o="award">$0</dd></div>
<div><dt>Gross increase</dt><dd data-o="gain">$0</dd></div>
<div><dt>Your share of costs</dt><dd data-o="cost">$0</dd></div>
<div><dt>Break-even landing point</dt><dd data-o="breakeven">—</dd></div>
</dl>
<p class="verdict" data-o="msg"></p>
</div></div></div>"""

PAYOFF_MINI = f"""
<div class="calc calc-mini" data-tool="gap">
{_head("60-second gap check", "Illustrative figures")}
<div class="calc-grid">
<div class="calc-in">
{_f("m-ins", "insurer", "Carrier’s estimate ($)", "15800")}
{_f("m-own", "yours", "Your contractor’s estimate ($)", "27300")}
<div class="fld"><label for="m-land">Award lands at</label><div class="range"><input id="m-land" type="range" name="land" min="0" max="100" step="5" value="50" data-unit="%"><output>50%</output></div><small class="hint">of the disputed amount</small></div>
</div>
<div class="calc-out" aria-live="polite">
<div class="kpi"><small>Amount in dispute</small><b data-o="gap">$0</b></div>
<dl class="rows">
<div><dt>Gap vs. carrier estimate</dt><dd data-o="pct">—</dd></div>
<div><dt>Projected award</dt><dd data-o="award">$0</dd></div>
<div><dt>Increase before fees</dt><dd data-o="gain">$0</dd></div>
</dl>
<p class="verdict" data-o="msg"></p>
</div></div></div>"""

# 2 -------------------------------------------------------------- holdback
_ROW = ('<tr><td><input name="item" value="{0}" aria-label="Item"></td><td><input name="rcv" inputmode="decimal" value="{1}" aria-label="Replacement cost"></td>'
        '<td><input name="age" inputmode="decimal" value="{2}" aria-label="Age in years"></td><td><input name="life" inputmode="decimal" value="{3}" aria-label="Expected life in years"></td>'
        '<td class="num" data-o="row">$0</td><td><button type="button" class="del" aria-label="Remove row">×</button></td></tr>')

HOLDBACK = """
<div class="calc calc-wide" data-tool="dep">
""" + _head("RCV / ACV holdback calculator", "Add as many lines as you need") + """
<div class="calc-grid">
<div class="calc-in">
<div class="tbl"><table><thead><tr><th>Damaged item</th><th>Replacement cost ($)</th><th>Age (yrs)</th><th>Life (yrs)</th><th>ACV</th><th><span class="sr-only">Remove</span></th></tr></thead><tbody>
""" + "".join(_ROW.format(*r) for r in [("Architectural shingle roof", 19800, 8, 30), ("Gutters & downspouts", 2100, 12, 25), ("Interior paint — two rooms", 2600, 5, 10), ("Laminate flooring — den", 3400, 7, 20)]) + """
</tbody></table></div>
<p><button type="button" class="btn btn-line btn-sm" data-add data-run>+ Add a line</button></p>
<div class="two">""" + _f("d-ded", "deduct", "Deductible ($)", "1500") + _sel("d-cap", "cap", "Depreciation cap", [("50", "50%"), ("60", "60%"), ("70", "70%"), ("80", "80%"), ("90", "90%")], "80", "Most estimates cap depreciation; check yours.") + """</div>
<div class="two">""" + _f("d-lab", "labor", "Labor share of each line (%)", "0", "Optional: share you believe shouldn’t be depreciated.") + _f("d-paid", "paid", "Already paid by the carrier ($)", "0") + """</div>
<label class="chk"><input type="checkbox" name="nonrec"> My policy pays actual cash value only (no recoverable depreciation)</label>
</div>
<div class="calc-out calc-out-row" aria-live="polite">
<div class="kpi"><small>First check (ACV − deductible − paid)</small><b data-o="first">$0</b></div>
<div class="kpi"><small>Held back until repairs</small><b data-o="held">$0</b></div>
<div class="kpi"><small>Total if fully recovered</small><b data-o="total">$0</b></div>
<dl class="rows wide">
<div><dt>Replacement cost (RCV)</dt><dd data-o="rcv">$0</dd></div>
<div><dt>Total depreciation</dt><dd data-o="dep">$0</dd></div>
<div><dt>Depreciation as share of RCV</dt><dd data-o="deppct">0%</dd></div>
<div><dt>Actual cash value (ACV)</dt><dd data-o="acv">$0</dd></div>
</dl>
</div></div></div>"""

# 3 -------------------------------------------------------------- roof
ROOF = f"""
<div class="calc" data-tool="roof">
{_head("Roof pitch & squares calculator", "Check the carrier’s measurements")}
<div class="calc-grid">
<div class="calc-in">
<fieldset class="seg"><legend>How will you measure?</legend>
<label><input type="radio" name="mode" value="dims" checked> <span>Length × width</span></label>
<label><input type="radio" name="mode" value="area"> <span>Known footprint area</span></label></fieldset>
<div class="two" data-mode="dims">{_f("r-l", "len", "Footprint length (ft)", "62")}{_f("r-w", "wid", "Footprint width (ft)", "36")}</div>
<div data-mode="dims">{_f("r-oh", "oh", "Eave overhang (inches)", "16")}</div>
<div data-mode="area" hidden>{_f("r-a", "area", "Footprint incl. overhangs (sq ft)", "2400")}</div>
<div class="two">{_sel("r-p", "pitch", "Roof pitch (rise per 12)", [(str(p), f"{p}/12") for p in [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14]], "7")}{_sel("r-wst", "waste", "Roof shape / waste", [("10", "Simple gable — 10%"), ("13", "Gable with dormers — 13%"), ("15", "Hip roof — 15%"), ("19", "Cut-up / complex — 19%")], "15")}</div>
{_f("r-pr", "price", "Installed price per square (optional, $)", "", "Use a local contractor’s quote for a rough figure.", extra=' placeholder="e.g. 540"')}
</div>
<div class="calc-out" aria-live="polite">
<div class="kpi"><small>Roof squares before waste</small><b data-o="sq">0</b></div>
<dl class="rows">
<div><dt>Pitch multiplier</dt><dd data-o="mult">1.000</dd></div>
<div><dt>Roof surface area</dt><dd data-o="surface">0</dd></div>
<div><dt>Squares to order (with waste)</dt><dd data-o="order">0</dd></div>
<div><dt>Shingle bundles (3 per square)</dt><dd data-o="bundles">0</dd></div>
<div><dt>Eave perimeter (drip edge / starter)</dt><dd data-o="perim">—</dd></div>
<div><dt>Rough replacement cost</dt><dd data-o="cost">—</dd></div>
</dl>
<p class="verdict" data-o="steep"></p>
</div></div></div>"""

# 4 -------------------------------------------------------------- named storm deductible
DEDUCT = f"""
<div class="calc" data-tool="deduct">
{_head("Named-storm deductible calculator", "Percentage vs. flat")}
<div class="calc-grid">
<div class="calc-in">
{_f("w-a", "cova", "Dwelling coverage — Coverage A ($)", "310000", "From your declarations page (homeowners or MWUA wind policy).")}
<div class="two">{_sel("w-p", "pct", "Hurricane / named-storm deductible", [("1", "1%"), ("2", "2%"), ("3", "3%"), ("5", "5%"), ("10", "10%")], "2")}{_f("w-f", "flat", "All-other-perils deductible ($)", "1000")}</div>
{_f("w-l", "loss", "Estimated storm damage ($)", "24500")}
</div>
<div class="calc-out" aria-live="polite">
<div class="kpi"><small>Your percentage deductible in dollars</small><b data-o="pd">$0</b></div>
<div class="bar" aria-hidden="true"><span class="b3"></span><span class="b1"></span></div>
<ul class="key"><li><i class="b3"></i>You absorb</li><li><i class="b1"></i>Policy pays</li></ul>
<dl class="rows">
<div><dt>Payment with % deductible</dt><dd data-o="pdpay">$0</dd></div>
<div><dt>Payment if the flat deductible applied</dt><dd data-o="flatpay">$0</dd></div>
<div><dt>Extra out of pocket from the % deductible</dt><dd data-o="diff">$0</dd></div>
</dl>
<div class="tbl mini"><table><thead><tr><th>Deductible</th><th>In dollars</th><th>Policy pays</th></tr></thead><tbody data-o="ladder"></tbody></table></div>
<p class="verdict" data-o="below"></p>
</div></div></div>"""

# 5 -------------------------------------------------------------- calendar
DATES = f"""
<div class="calc" data-tool="dates">
{_head("Mississippi claim calendar builder", "Exports an .ics file")}
<div class="calc-grid">
<div class="calc-in">
<div class="two"><div class="fld"><label for="t-d">Date of loss</label><input id="t-d" type="date" name="dol"></div><div class="fld"><label for="t-ad">Appraisal demand date (optional)</label><input id="t-ad" type="date" name="demand"></div></div>
<p class="hint">Change each window to match your policy. Defaults are common figures, not legal advice.</p>
<div class="three">
{_f("t-n", "notice", "Report the claim within (days)", "3", mode="numeric")}
{_f("t-m", "mitig", "Temporary repairs within (days)", "10", mode="numeric")}
{_f("t-p", "pol", "Proof of loss (days)", "60", "Often 60 days from the carrier’s request.", mode="numeric")}
{_f("t-r", "rcd", "Depreciation recovery (days)", "365", mode="numeric")}
{_f("t-a", "appoint", "Name your appraiser within (days of demand)", "20", mode="numeric")}
{_f("t-s", "suit", "Lawsuit deadline to confirm (years)", "3", "Mississippi’s general contract period is three years. Confirm with an attorney.", mode="numeric")}
</div>
</div>
<div class="calc-out" aria-live="polite">
<ol class="tline" data-o="timeline"></ol>
<p><button type="button" class="btn btn-sm" data-ics>Download calendar (.ics)</button></p>
</div></div></div>"""

# 6 -------------------------------------------------------------- readiness
_QUIZ = [
    (3, "Has the carrier accepted coverage for at least part of the loss?", "Get written confirmation of what the carrier accepts. If the claim was denied outright, speak with a Mississippi attorney before thinking about appraisal."),
    (3, "Do you have the carrier’s full line-item estimate, not just a summary?", "Ask the adjuster in writing for the complete itemized estimate, including the price list date."),
    (3, "Do you have your own line-item estimate (not a lump-sum bid)?", "Get an independent estimate with quantities and unit prices — a one-line bid won’t carry weight with a panel."),
    (2, "Are there dated photos taken soon after the storm or event?", "Pull every photo and video you have, note when each was taken, and add current-condition photos."),
    (2, "If you’re in a coastal county, have you separated wind damage from flood damage?", "Document water lines, debris direction and which damage came from wind or rain entry — and keep wind and flood claims organized separately."),
    (2, "Do you know which deductible applies (named-storm, wind/hail or all-other-perils)?", "Check your declarations page and the deductible endorsement, then run the named-storm deductible calculator."),
    (2, "Have you read the appraisal clause and noted its deadlines?", "Find the ‘Appraisal’ condition in your policy (or MWUA policy) and calendar any appointment windows."),
    (2, "Have temporary repairs been made, with receipts saved?", "Tarp, dry out and secure the property, and keep every receipt — mitigation costs are usually part of the claim."),
    (2, "Has hidden damage (attic, decking, wall cavities) been opened up and documented?", "Make sure the full scope is visible before a panel values it; a partial scope locks in a partial award."),
    (1, "Do you have your current declarations page?", "Download it from your carrier’s portal or ask your agent for a copy."),
    (1, "Are letters, emails and claim notes organized by date?", "Put all correspondence in one folder in date order — panels move faster with a clean file."),
    (2, "Is the gap between estimates more than roughly 10% or $5,000?", "Test the gap in the appraisal payoff estimator; a small gap may not justify appraisal costs."),
]

READY = """
<div class="calc calc-wide" data-tool="ready">
""" + _head("Appraisal readiness checkup", "12 questions · about two minutes") + """
<div class="calc-grid">
<div class="calc-in">
<ol class="quiz">""" + "".join(
    f'<li data-w="{w}" data-fix="{f}"><span class="q">{q}</span><span class="yn"><button type="button" class="yes" aria-pressed="false">Yes</button><button type="button" class="no" aria-pressed="false">No</button></span></li>'
    for w, q, f in _QUIZ) + """
</ol>
<p><button type="button" class="btn btn-line btn-sm" data-reset>Reset answers</button></p>
</div>
<div class="calc-out" aria-live="polite">
<div class="meter"><div class="meter-top"><span>Readiness</span><b><span data-o="score">–</span><small>/100</small></b></div><div class="meter-track"><span data-o="fill"></span></div><small class="hint">Answered <span data-o="count">0 / 12</span></small></div>
<p class="verdict" data-o="verdict"></p>
<p class="todo-h">Your to-do list</p>
<ul class="todo" data-o="todo"></ul>
</div></div></div>"""

# 7 -------------------------------------------------------------- wind vs water
SPLIT = f"""
<div class="calc" data-tool="split">
{_head("Wind vs. water split estimator", "Coastal claims · illustrative")}
<div class="calc-grid">
<div class="calc-in">
{_f("s-t", "total", "Total building damage, all causes ($)", "184000", "Full repair cost of the structure at replacement cost.")}
<div class="fld"><label for="s-w">Share caused by wind (and wind-driven rain)</label><div class="range"><input id="s-w" type="range" name="windpct" min="0" max="100" step="5" value="45" data-unit="%"><output>45%</output></div><small class="hint">The rest is treated as flood or storm-surge damage.</small></div>
<div class="two">{_f("s-a", "cova", "Wind policy Coverage A ($)", "260000", "Homeowners or MWUA wind policy.")}{_sel("s-p", "wded", "Named-storm deductible", [("1", "1%"), ("2", "2%"), ("3", "3%"), ("5", "5%")], "2")}</div>
<div class="two">{_f("s-fl", "flimit", "Flood building limit ($)", "250000", "NFIP building coverage tops out at $250,000.")}{_f("s-fd", "fded", "Flood deductible ($)", "2000")}</div>
<label class="chk"><input type="checkbox" name="noflood"> No flood policy on this building</label>
</div>
<div class="calc-out" aria-live="polite">
<div class="kpi"><small>Estimated total from both policies</small><b data-o="both">$0</b></div>
<div class="bar" aria-hidden="true"><span class="b1"></span><span class="b2"></span><span class="b3"></span></div>
<ul class="key"><li><i class="b1"></i>Wind policy pays</li><li><i class="b2"></i>Flood policy pays</li><li><i class="b3"></i>Not paid (deductibles, limits, uninsured)</li></ul>
<dl class="rows">
<div><dt>Wind portion of the damage</dt><dd data-o="windamt">$0</dd></div>
<div><dt>Named-storm deductible</dt><dd data-o="wdedamt">$0</dd></div>
<div><dt>Wind policy payment</dt><dd data-o="windpay">$0</dd></div>
<div><dt>Flood portion of the damage</dt><dd data-o="floodamt">$0</dd></div>
<div><dt>Flood policy payment</dt><dd data-o="floodpay">$0</dd></div>
<div><dt>Left unpaid</dt><dd data-o="gap">$0</dd></div>
<div><dt>Moved between policies by a 10% shift</dt><dd data-o="moved">$0</dd></div>
<div><dt>Net change in total from +10% wind</dt><dd data-o="swing">$0</dd></div>
</dl>
<p class="verdict" data-o="msg"></p>
</div></div></div>"""


TOOLS = [
    {
        "slug": "appraisal-payoff-estimator", "name": "Appraisal Payoff Estimator", "kind": "Calculator", "kw": "appraisal payoff estimator",
        "short": "Size the disputed amount, test where an award might land and subtract realistic appraiser and umpire fees.",
        "title": "Appraisal Payoff Estimator | Net Gain After Fees",
        "desc": "Free appraisal payoff estimator: compare your estimate with the carrier’s, test award outcomes and subtract fees to see your likely net gain.",
        "h1": "Appraisal Payoff Estimator: What Would You Actually Net?",
        "lede": "Appraisal only makes sense if the likely increase beats the cost. Enter both estimates, slide the landing point and add fees — the estimator shows your net and the break-even point.",
        "markup": PAYOFF,
        "explain": f"""
<h2>Reading the result honestly</h2>
<p>Panels rarely award either side’s opening number. Line items backed by measurements, photos and local pricing usually hold; padding usually falls. That’s why the estimator asks where the award might land rather than assuming you win everything. Try three scenarios — 30%, 55% and 80% — and look at the spread.</p>
<p>The <strong>break-even landing point</strong> is the share of the gap the panel must award just to cover your appraisal costs. If it’s above about 50%, your file needs to be very strong. If it’s under 20%, appraisal is probably worth a serious conversation.</p>
<h2>Fee structures you may see</h2>
<ul><li><strong>Flat fee:</strong> a set price agreed in writing up front.</li><li><strong>Percentage of the increase:</strong> paid only on money above the carrier’s number.</li><li><strong>Hourly:</strong> common for umpires and for large commercial losses.</li></ul>
<p>Whichever arrangement you choose, get it in writing before work starts. Each side normally pays its own appraiser and splits the umpire’s fee.</p>
<h2>What this tool leaves out</h2>
<p>It sizes the dispute at replacement cost. Deductibles, depreciation timing and sub-limits change what reaches your bank account — use the <a href="{B}holdback-recovery-calculator/">holdback recovery calculator</a> and the <a href="{B}named-storm-deductible-calculator/">named-storm deductible calculator</a> for those.</p>
""",
        "faqs": [("Is the projected award a prediction?", "No. It is a planning scenario based on the numbers you enter. Real awards depend on documentation, policy wording and the panel."),
                 ("How big should the gap be before I consider appraisal?", "As a rough rule of thumb, gaps under about 10% of the carrier’s estimate or a few thousand dollars are often better handled with a documented supplement request."),
                 ("Are my numbers saved?", "No. The estimator runs entirely in your browser and nothing is stored or sent.")],
    },
    {
        "slug": "holdback-recovery-calculator", "name": "Holdback Recovery Calculator", "kind": "Calculator", "kw": "rcv acv holdback calculator",
        "short": "Split a replacement-cost claim into the first ACV check, the depreciation held back and the total after repairs.",
        "title": "RCV vs ACV Holdback Calculator | Recoverable Depreciation",
        "desc": "Use this free RCV vs ACV holdback calculator to estimate your first check, the recoverable depreciation held back and the total after repairs.",
        "h1": "RCV / ACV Holdback Calculator for Mississippi Claims",
        "lede": "Most replacement-cost policies pay twice: an actual-cash-value check now and the held-back depreciation after you repair. List the damaged items to see how the money splits.",
        "markup": HOLDBACK,
        "explain": f"""
<h2>How the math works</h2>
<p>Each line is depreciated straight-line — age divided by expected life — up to the cap you choose. Subtract depreciation from replacement cost and you get actual cash value (ACV). The first check is usually ACV minus the deductible and anything already paid. The depreciation is “held back” until repairs are complete.</p>
<p>The optional labor field lets you see the effect of not depreciating labor. Whether labor may be depreciated depends on policy language and the law that applies; treat that field as a what-if, not a statement of your rights.</p>
<h2>Life expectancies you’ll often see</h2>
<div class="tbl"><table><thead><tr><th>Item</th><th>Common range in estimates</th></tr></thead><tbody>
<tr><td>Architectural shingles</td><td>25–30 years</td></tr><tr><td>3-tab shingles</td><td>20–25 years</td></tr><tr><td>Metal roofing panels</td><td>40–50 years</td></tr><tr><td>Interior paint</td><td>8–12 years</td></tr><tr><td>Carpet</td><td>8–12 years</td></tr><tr><td>Vinyl siding</td><td>30–40 years</td></tr></tbody></table></div>
<h2>Getting the holdback released</h2>
<p>Send invoices and photos of the completed work, and watch the policy’s time limit for claiming replacement cost. The <a href="{B}claim-calendar-builder/">claim calendar builder</a> can put that date on your phone.</p>
""",
        "faqs": [("What happens if I don’t repair?", "Under most replacement-cost policies you keep the actual-cash-value payment, but the held-back depreciation may not be paid."),
                 ("Why does the carrier’s depreciation look higher than mine?", "Estimates may use shorter life expectancies, condition adjustments or depreciate items you wouldn’t expect. Ask for the depreciation detail line by line.")],
    },
    {
        "slug": "roof-pitch-squares-calculator", "name": "Roof Pitch & Squares Calculator", "kind": "Calculator", "kw": "roof squares calculator",
        "short": "Turn a footprint into true roof squares, bundles and eave footage — then compare against the carrier’s roof section.",
        "title": "Roof Squares Calculator with Pitch, Waste & Eave Length",
        "desc": "Free roof squares calculator: turn footprint and pitch into true surface area, squares, bundles and eave footage to check a roof estimate.",
        "h1": "Roof Pitch & Squares Calculator for Storm Claims",
        "lede": "Short measurements are one of the most common reasons roof claims come up light. Enter the footprint and pitch to estimate real surface area, squares, bundles and drip-edge footage.",
        "markup": ROOF,
        "explain": f"""
<h2>The pitch multiplier</h2>
<p>A sloped roof has more surface than the ground it covers. The multiplier is √(1 + (rise ÷ 12)²): a 6/12 roof is about 11.8% larger than its footprint, an 8/12 roof about 20.2% larger, and a 12/12 roof about 41.4% larger. Leave that out and a 30-square roof can be written as 25.</p>
<h2>What to compare in the carrier’s estimate</h2>
<ul><li>Total squares and the waste percentage on the shingle line.</li><li>Steep charges (often starting at 7/12) and high-roof charges for two-story sections.</li><li>Separate lines for starter, ridge cap, drip edge, valley metal and ice-and-water shield.</li><li>Removal, felt or synthetic underlayment, and decking replacement where boards are damaged.</li></ul>
<p>Differences of more than 5–10% in squares deserve a closer look. Hail and wind claims in North Mississippi and the Pine Belt often turn on exactly these lines — see our <a href="/our-appraisal-services/roof-hail-claim-appraisal/">roof and hail claim appraisal</a> page.</p>
<h2>Limits of a footprint method</h2>
<p>Roofs with several pitches, dormers and valleys should be measured plane by plane, from an aerial report or in the field. Use this calculator as a sanity check, not a replacement for measurement.</p>
""",
        "faqs": [("What is a roofing square?", "One hundred square feet of roof surface. Many single-story Mississippi homes fall between 20 and 35 squares."),
                 ("Why does the waste factor change with roof shape?", "Hips, valleys and dormers need more cutting, so more material ends up as scrap. Simple gables waste the least.")],
    },
    {
        "slug": "named-storm-deductible-calculator", "name": "Named-Storm Deductible Calculator", "kind": "Calculator", "kw": "hurricane deductible calculator",
        "short": "See a 1%–10% hurricane or named-storm deductible in real dollars and what a storm claim would actually pay.",
        "title": "Hurricane Deductible Calculator | Named-Storm % in Dollars",
        "desc": "Free hurricane deductible calculator: turn a percentage named-storm deductible into dollars and compare payouts from 1% up to 10%.",
        "h1": "Named-Storm & Hurricane Deductible Calculator",
        "lede": "On the Coast, a “2% deductible” is two percent of your dwelling limit, not of the damage. See what yours means in dollars and how much of a storm loss your policy would actually pay.",
        "markup": DEDUCT,
        "explain": f"""
<h2>Why percentage deductibles catch people off guard</h2>
<p>Policies in Hancock, Harrison and Jackson counties — and many farther inland — use a hurricane, named-storm or wind deductible calculated from Coverage A. Illustrative example: on a $310,000 dwelling limit, a 2% deductible is $6,200 and a 5% deductible is $15,500, compared with a typical $1,000 all-other-perils deductible.</p>
<h2>Where to find yours</h2>
<p>Look on the declarations page for “hurricane,” “named storm,” “windstorm” or “wind/hail.” If wind is excluded from your homeowners policy and written through the Mississippi Windstorm Underwriting Association (MWUA), the deductible is on the MWUA declarations instead. The endorsement defines when it applies — often tied to a storm named by the National Hurricane Center.</p>
<h2>How it affects an appraisal decision</h2>
<p>The deductible doesn’t change the amount of loss a panel decides, but it changes what you receive. A loss barely above the deductible rarely justifies a dispute; one far above it may. Read more in our guide to <a href="/claim-advice/coast-hurricane-deductibles-explained/">Coast hurricane deductibles</a>.</p>
""",
        "faqs": [("Does the percentage come off each part of the claim?", "Usually the dollar amount is calculated from Coverage A and then applied once to the whole covered wind loss for that storm. Check your endorsement’s wording."),
                 ("Can I lower my named-storm deductible?", "Sometimes, at renewal and for a higher premium. Ask your agent what options your carrier or MWUA offers.")],
    },
    {
        "slug": "claim-calendar-builder", "name": "Claim Calendar Builder", "kind": "Planner", "kw": "insurance claim deadline calendar",
        "short": "Turn your date of loss into dated milestones — notice, proof of loss, holdback, appraisal windows — and export them.",
        "title": "Insurance Claim Deadline Calendar | Free .ics Planner",
        "desc": "Build an insurance claim deadline calendar from your date of loss, add appraisal windows and download every milestone as an .ics file.",
        "h1": "Insurance Claim Deadline Calendar Builder",
        "lede": "Policy deadlines keep running while you argue about a number. Enter your date of loss — and your appraisal demand date if there is one — to build a timeline you can drop into any calendar app.",
        "markup": DATES,
        "explain": f"""
<h2>The dates worth protecting</h2>
<ul><li><strong>Prompt notice.</strong> Policies require you to report a loss promptly; late notice is a common defense.</li>
<li><strong>Proof of loss.</strong> If the carrier asks for a sworn proof of loss, many policies give 60 days to return it.</li>
<li><strong>Replacement-cost recovery.</strong> Most policies set a period to finish repairs and claim held-back depreciation.</li>
<li><strong>Appraisal windows.</strong> Many clauses give each side about 20 days after a written demand to name an appraiser.</li>
<li><strong>Lawsuit deadline.</strong> Mississippi’s general limitation period for many contract claims is three years, and state law generally restricts contracts from shortening it. Your situation may differ — confirm the date with a Mississippi attorney.</li></ul>
<div class="callout"><b class="callout-t">Important</b><p>The planner only uses the numbers you type in. It isn’t legal advice, and nothing here extends or changes a deadline. If a date is close, talk to an attorney promptly.</p></div>
<h2>Using the .ics file</h2>
<p>The download works with Google Calendar, Apple Calendar and Outlook. Each milestone imports as an all-day event with a short note. Nothing you enter leaves your browser. Next, check whether your file is ready with the <a href="{B}appraisal-readiness-checkup/">appraisal readiness checkup</a>.</p>
""",
        "faqs": [("Is my date of loss the day I noticed the damage?", "Usually it is the date the storm or event happened. Weather records for your address can help pin it down."),
                 ("Does demanding appraisal pause the lawsuit deadline?", "Not automatically. Some policies or agreements address it and many don’t, so protect the deadline separately.")],
    },
    {
        "slug": "appraisal-readiness-checkup", "name": "Appraisal Readiness Checkup", "kind": "Checklist", "kw": "appraisal readiness checklist",
        "short": "Twelve yes/no questions that score your claim file and build a to-do list before anyone demands appraisal.",
        "title": "Appraisal Readiness Checklist | Score Your Claim File",
        "desc": "A free appraisal readiness checklist: answer twelve questions to score your claim file and get a to-do list before you demand appraisal.",
        "h1": "Appraisal Readiness Checkup: Is Your File Ready?",
        "lede": "The strongest appraisals are prepared before the demand letter goes out. Answer twelve quick questions to see where your file stands and what to fix first.",
        "markup": READY,
        "explain": f"""
<h2>How the score is weighted</h2>
<p>Coverage, estimates and evidence carry the most weight because they decide whether appraisal is the right tool at all and how well your number will hold up. Coastal questions — separating wind from flood and knowing which deductible applies — come next, because they change what a Mississippi award is actually worth. Paperwork items matter too, but they’re the easiest to fix.</p>
<h2>What to do with your score</h2>
<ul><li><strong>75 or higher:</strong> your file is in good shape; a professional look at the dollar gap is the logical next step.</li><li><strong>45 to 74:</strong> close the open items first — each one strengthens your number.</li><li><strong>Below 45:</strong> demanding appraisal now risks locking in a low award. Build the file first.</li></ul>
<p>When you’re ready, our <a href="/our-appraisal-services/carrier-estimate-review/">carrier estimate review</a> is a low-cost way to find out where the carrier’s number falls short.</p>
""",
        "faqs": [("Is anything I answer stored?", "No. The checkup runs entirely in your browser and nothing is saved or sent."),
                 ("Can I bring my result to a consultation?", "Yes. A screenshot of your score and to-do list is a helpful starting point for a first call.")],
    },
    {
        "slug": "wind-water-split-estimator", "name": "Wind vs. Water Split Estimator", "kind": "Estimator", "kw": "wind vs flood damage calculator",
        "short": "See how splitting coastal storm damage between wind and flood changes what each policy pays — and what’s left over.",
        "title": "Wind vs Flood Damage Calculator | Coastal Claim Split",
        "desc": "This wind vs flood damage calculator shows how splitting storm damage between a wind policy and a flood policy changes what each one may pay.",
        "h1": "Wind vs. Water Split Estimator for Coastal Claims",
        "lede": "After a hurricane, the biggest dollar question on the Coast is often how much damage came from wind and how much from water. Move the slider to see how the split changes what each policy pays.",
        "markup": SPLIT,
        "explain": f"""
<h2>Why the split matters so much in Mississippi</h2>
<p>Hurricane Katrina pushed storm surge miles inland across Hancock, Harrison and Jackson counties while also tearing roofs apart with wind. Homeowners and wind policies generally cover wind and wind-driven rain, while flood and surge are excluded and handled — if at all — by a separate flood policy. Many claims after 2005 turned on that allocation, and the same question returns with every Gulf storm.</p>
<h2>How the estimator works</h2>
<ul><li>The wind share of the damage, minus the named-storm deductible, is paid by the wind policy up to Coverage A.</li><li>The flood share, minus the flood deductible, is paid by the flood policy up to its building limit.</li><li>Anything above limits or inside deductibles — or flood damage with no flood policy — is left unpaid.</li></ul>
<p>Illustrative figures only. Real allocations depend on evidence, policy wording (including any anti-concurrent causation clause) and the law that applies.</p>
<div class="callout"><b class="callout-t">Coverage vs. amount</b><p>Appraisal can value the wind damage once coverage for it is accepted. It doesn’t decide whether damage was caused by wind or flood when that is a coverage dispute — that question may need an attorney. Read <a href="/claim-advice/wind-vs-water-after-katrina/">wind vs. water after Katrina</a> for more.</p></div>
<h2>Evidence that moves the split</h2>
<p>Interior water lines, debris direction, missing roof coverings, wind-blown openings and a timeline of when water arrived all matter. Our <a href="/our-appraisal-services/hurricane-named-storm-appraisal/">hurricane and named-storm appraisal</a> work starts with that evidence.</p>
""",
        "faqs": [("Does this tool tell me the right split for my house?", "No. It shows how sensitive your recovery is to the split. The actual allocation depends on evidence and policy terms."),
                 ("What if I don’t have flood insurance?", "Tick the box and the flood share shows as unpaid. That makes clear how much depends on documenting wind damage thoroughly."),
                 ("Is the NFIP limit really $250,000?", "Standard NFIP building coverage for a single-family home is capped at $250,000; some owners buy excess flood coverage privately.")],
    },
]
