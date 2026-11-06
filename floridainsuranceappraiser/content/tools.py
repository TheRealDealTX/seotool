"""Free claim tools. `ui` is the interactive markup; assets/js/tools.js wires it up by data-tool."""

def _money(id_, label, value="", hint=""):
    h = f'<small class="hint">{hint}</small>' if hint else ""
    return (f'<div class="field"><label for="{id_}">{label}</label><div class="money">'
            f'<input id="{id_}" name="{id_}" inputmode="decimal" value="{value}" autocomplete="off"></div>{h}</div>')


def _num(id_, label, value="", step="1", hint=""):
    h = f'<small class="hint">{hint}</small>' if hint else ""
    return (f'<div class="field"><label for="{id_}">{label}</label>'
            f'<input id="{id_}" name="{id_}" type="number" step="{step}" min="0" value="{value}">{h}</div>')


def _sel(id_, label, opts):
    o = "".join(f'<option value="{v}"{" selected" if s else ""}>{t}</option>' for v, t, s in opts)
    return f'<div class="field"><label for="{id_}">{label}</label><select id="{id_}" name="{id_}">{o}</select></div>'


def _date(id_, label):
    return f'<div class="field"><label for="{id_}">{label}</label><input id="{id_}" name="{id_}" type="date"></div>'


TOOLS = [
    {
        "slug": "appraisal-worth-it-calculator",
        "name": "Appraisal Worth-It Calculator",
        "icon": "scale",
        "short": "Compare the disputed amount against what appraisal is likely to cost you, across low, middle and full-recovery scenarios.",
        "title": "Is Insurance Appraisal Worth It? Free Florida Calculator",
        "description": "Free calculator from Florida Insurance Appraiser: weigh your claim gap against appraiser and umpire costs to see whether invoking appraisal makes sense.",
        "h1": "Appraisal Worth-It Calculator",
        "kicker": "Gap vs. cost, in seconds",
        "lead": "Enter the insurance company’s number, your contractor’s number and the likely cost of appraisal. The calculator shows the disputed amount and what you could net under three realistic award scenarios.",
        "ui": f"""<form class="tool" data-tool="worth" onsubmit="return false">
<div class="tool-grid">
{_money('w_ins', 'Insurance company’s estimate (RCV)', '18500')}
{_money('w_con', 'Your contractor / independent estimate', '41200')}
{_sel('w_feetype', 'Your appraiser’s fee structure', [('flat', 'Flat or hourly fee', True), ('pct', 'Percentage of the award', False)])}
{_num('w_fee', 'Fee ($ if flat, % if percentage)', '3000', '0.5')}
{_money('w_ump', 'Estimated umpire fee (total)', '2500', 'Only needed if the appraisers cannot agree. You usually pay half.')}
{_sel('w_umpchance', 'Will an umpire be needed?', [('0.5', 'Unsure — weight it 50%', True), ('1', 'Plan for it', False), ('0', 'Unlikely', False)])}
</div></form>
<div class="out" id="worth-out">
<div class="hl"><span>Disputed amount</span><b data-o="gap">—</b></div>
<div><span>Your estimated appraisal cost</span><b data-o="cost">—</b></div>
<div><span>Break-even award (share of gap)</span><b data-o="be">—</b></div>
</div>
<div class="table-wrap" style="margin-top:18px"><table class="cmp"><thead><tr><th>If the award lands at…</th><th>Added recovery</th><th>Net after appraisal costs</th></tr></thead><tbody id="worth-rows"></tbody></table></div>
<p class="verdict" id="worth-verdict">Enter your numbers above.</p>""",
        "sections": [
            ("How the calculator works", "<p>Appraisal resolves a disagreement over the <em>amount</em> of a covered loss. The calculator subtracts the insurer’s estimate from your estimate to find the disputed amount, then estimates your cost: your own appraiser’s fee plus your typical half-share of the umpire’s fee, weighted by how likely an umpire is to be needed.</p><p>Because awards usually land somewhere between the two estimates, the table models three outcomes — a quarter, half and three-quarters of the gap — and shows what you would net after appraisal costs in each case. The break-even figure tells you how much of the gap the award must recover just to cover the process.</p>"),
            ("Reading the result", "<ul><li><strong>Break-even under 20%:</strong> appraisal is usually economical if your estimate is well documented.</li><li><strong>Break-even between 20% and 50%:</strong> worth it only if your line items are strong — get an <a href=\"/appraisal-services/xactimate-estimate-review/\">estimate review</a> first.</li><li><strong>Break-even over 50%:</strong> a documented supplement, re-inspection request or <a href=\"/appraisal-process/\">DFS mediation</a> may be the better first step.</li></ul>"),
            ("What the calculator can’t tell you", "<p>It cannot judge whether your estimate is accurate, whether a disputed item is a coverage question (which appraisal does not decide), or what your specific policy says about fees and deadlines. Read your policy’s appraisal provision and talk with Florida Insurance Appraiser before you send a demand.</p>"),
        ],
        "faqs": [
            ("Who pays for insurance appraisal in Florida?", "Most Florida policies say each side pays its own appraiser and the two sides split the umpire’s fee and other shared appraisal expenses equally. Check the appraisal provision in your policy for the exact wording."),
            ("Is a percentage fee or a flat fee better?", "A flat or hourly fee keeps costs predictable on large losses; a percentage fee shifts more risk to the appraiser on uncertain claims. The calculator lets you compare both."),
            ("What gap is too small for appraisal?", "There is no fixed threshold, but when your expected appraisal cost is a large share of the disputed amount, a well-documented supplement or mediation is often the smarter first move."),
        ],
    },
    {
        "slug": "hurricane-deductible-calculator",
        "name": "Hurricane Deductible Calculator",
        "icon": "hurricane",
        "short": "Turn a 2%, 5% or 10% hurricane deductible into dollars, track what you’ve already absorbed this year, and estimate your payout.",
        "title": "Florida Hurricane Deductible Calculator (2%, 5%, 10%)",
        "description": "Convert your Florida hurricane deductible percentage into dollars, account for earlier storms in the same calendar year, and estimate your net claim payment.",
        "h1": "Florida Hurricane Deductible Calculator",
        "kicker": "Percent to dollars",
        "lead": "Florida hurricane deductibles are usually a percentage of your dwelling limit (Coverage A), not a flat amount — and they generally run per calendar year rather than per storm. See what that means in real dollars.",
        "ui": f"""<form class="tool" data-tool="hurdeduct" onsubmit="return false">
<div class="tool-grid">
{_money('h_cova', 'Dwelling limit (Coverage A)', '425000')}
{_sel('h_pct', 'Hurricane deductible', [('0.02', '2% of Coverage A', True), ('0.05', '5% of Coverage A', False), ('0.10', '10% of Coverage A', False), ('flat', 'Flat dollar amount', False)])}
{_money('h_flat', 'Flat hurricane deductible (if flat)', '500')}
{_money('h_aop', 'All-other-perils (AOP) deductible', '2500')}
{_money('h_loss', 'Estimated covered hurricane damage', '38000')}
{_money('h_used', 'Hurricane deductible already absorbed this calendar year', '0', 'From an earlier hurricane claim this year, if any.')}
</div></form>
<div class="out">
<div><span>Full hurricane deductible</span><b data-o="ded">—</b></div>
<div><span>Deductible applied to this claim</span><b data-o="applied">—</b></div>
<div class="hl"><span>Estimated claim payment</span><b data-o="pay">—</b></div>
</div>
<p class="verdict" id="hur-verdict"></p>""",
        "sections": [
            ("How Florida hurricane deductibles work", "<p>Most Florida homeowners policies carry a separate hurricane deductible expressed as a percentage of the Coverage A dwelling limit — commonly 2%, 5% or 10% — with flat options such as $500 available on some policies. On a $425,000 dwelling limit, a 2% deductible is $8,500 and a 5% deductible is $21,250.</p><p>Florida law generally applies the hurricane deductible once per calendar year. If a second hurricane damages your home in the same year, the insurer applies whatever remains of the hurricane deductible or your all-other-perils deductible, whichever is greater. This calculator models that rule when you enter the amount already absorbed.</p>"),
            ("Why the deductible matters in an appraisal", "<p>An appraisal award sets the amount of loss; the deductible and prior payments are subtracted afterward. When an insurer’s estimate lands just above or below a large percentage deductible, a few missed line items can be the difference between a check and a denial letter. That is a common reason property owners call Florida Insurance Appraiser after a <a href=\"/appraisal-services/hurricane-claim-appraisal/\">hurricane claim</a>.</p>"),
            ("Wind is not flood", "<p>Your homeowners hurricane deductible applies to wind and wind-driven damage. Storm surge and rising water fall under flood insurance — usually an NFIP or private flood policy with its own deductible. Read more in our <a href=\"/blog/florida-hurricane-deductible-explained/\">hurricane deductible guide</a>.</p>"),
        ],
        "faqs": [
            ("Is the hurricane deductible per storm or per year in Florida?", "For most Florida residential policies it applies per calendar year. Later hurricanes in the same year use the remaining hurricane deductible or the AOP deductible, whichever is greater."),
            ("Does the hurricane deductible apply to tropical storms?", "It depends on your policy’s definition. Many Florida policies tie the hurricane deductible to a hurricane watch or warning issued by the National Hurricane Center and a set window afterward. Check your declarations and definitions."),
            ("Can appraisal change my deductible?", "No. Appraisal decides the amount of loss. The deductible stays as written in the policy, but a higher award means more is left after the deductible is subtracted."),
        ],
    },
    {
        "slug": "acv-depreciation-calculator",
        "name": "ACV & Depreciation Calculator",
        "icon": "chart",
        "short": "Estimate depreciation and actual cash value for roofs, flooring, HVAC and contents using age and expected service life.",
        "title": "ACV & Depreciation Calculator for Florida Claims",
        "description": "Estimate depreciation, actual cash value and recoverable depreciation for roofing, flooring, HVAC and contents on a Florida property insurance claim. Free tool.",
        "h1": "ACV & Depreciation Calculator",
        "kicker": "RCV, ACV & holdback",
        "lead": "Insurers often pay actual cash value first and hold back depreciation until repairs are done. Estimate how much is being withheld — and whether the depreciation rate looks reasonable.",
        "ui": f"""<form class="tool" data-tool="acv" onsubmit="return false">
<div class="tool-grid">
{_sel('a_item', 'Item or component', [('25', 'Architectural shingle roof (≈25 yrs)', True), ('20', '3-tab shingle roof (≈20 yrs)', False), ('50', 'Concrete / clay tile roof (≈50 yrs)', False), ('40', 'Metal roof (≈40 yrs)', False), ('18', 'Modified bitumen flat roof (≈18 yrs)', False), ('15', 'HVAC system (≈15 yrs)', False), ('12', 'Water heater (≈12 yrs)', False), ('10', 'Carpet (≈10 yrs)', False), ('25', 'Vinyl plank / laminate (≈25 yrs)', False), ('8', 'Interior paint (≈8 yrs)', False), ('custom', 'Custom life expectancy', False)])}
{_num('a_life', 'Life expectancy (years)', '25')}
{_money('a_rcv', 'Replacement cost value (RCV)', '24000')}
{_num('a_age', 'Age (years)', '9', '0.5')}
{_sel('a_cond', 'Condition before the loss', [('0', 'Average', True), ('-0.1', 'Well maintained (−10%)', False), ('0.1', 'Below average (+10%)', False)])}
{_sel('a_cap', 'Maximum depreciation', [('1', 'No cap', False), ('0.8', '80% cap', True), ('0.5', '50% cap', False)])}
</div></form>
<div class="out">
<div><span>Depreciation rate</span><b data-o="rate">—</b></div>
<div><span>Depreciation (holdback)</span><b data-o="dep">—</b></div>
<div class="hl"><span>Actual cash value (ACV)</span><b data-o="acv">—</b></div>
</div>
<p class="verdict" id="acv-verdict"></p>""",
        "sections": [
            ("Straight-line depreciation, explained", "<p>Most estimating platforms depreciate a component in a straight line across its expected life: a 25-year roof that is 10 years old is 40% depreciated. Condition adjustments and caps change the result, and Florida policies differ in whether labor is depreciated and whether depreciation is recoverable.</p><p>Actual cash value (ACV) is replacement cost minus depreciation. On a replacement cost policy, the withheld depreciation is usually <strong>recoverable</strong> once repairs are complete and documented.</p>"),
            ("When depreciation becomes the dispute", "<p>Depreciation is one of the most common line-item disagreements we see. Typical problems include a life expectancy that is too short for the material, an age taken from a permit date that doesn’t match a later re-roof, or depreciation applied to items that shouldn’t carry it. In appraisal, depreciation is part of the amount of loss and can be argued line by line. See <a href=\"/appraisal-services/roof-claim-appraisal/\">roof claim appraisal</a>.</p>"),
            ("Roof payment schedules", "<p>Some Florida policies use a roof surface payment schedule or ACV-only roof endorsement that pays a set percentage based on roof age, regardless of the usual RCV terms. If your declarations page shows one, this calculator will overstate what you can recover on the roof — the schedule controls.</p>"),
        ],
        "faqs": [
            ("Is depreciation recoverable in Florida?", "On replacement cost policies it usually is, once repairs are completed and documented within the policy’s time limits. ACV-only policies and roof payment schedules work differently."),
            ("Can labor be depreciated?", "It depends on the policy language and the estimating method. Ask for the insurer’s estimate with depreciation shown by line so you can see exactly what was withheld."),
            ("What life expectancy should I use?", "Use the manufacturer’s rated life or a commonly accepted service life for the material in Florida’s climate. The presets here are general planning figures, not industry rulings."),
        ],
    },
    {
        "slug": "claim-deadline-calculator",
        "name": "Claim Deadline Calculator",
        "icon": "calendar",
        "short": "Plug in your date of loss to map Florida’s key claim-notice windows and the insurer’s typical response timelines.",
        "title": "Florida Property Claim Deadline Calculator",
        "description": "Map the key Florida property claim timelines from your date of loss: notice windows for new, reopened and supplemental claims and insurer response deadlines.",
        "h1": "Florida Claim Deadline Calculator",
        "kicker": "Know your windows",
        "lead": "Florida shortened several property-claim timelines in recent reforms. Enter your dates to see the common statutory windows and how many days remain. Your policy may set additional or shorter deadlines — including for appraisal.",
        "ui": f"""<form class="tool" data-tool="deadline" onsubmit="return false">
<div class="tool-grid">
{_date('d_loss', 'Date of loss')}
{_date('d_notice', 'Date you reported the claim (optional)')}
</div></form>
<ul class="dl" id="dl-out"><li><span>Enter your date of loss to build the timeline.</span></li></ul>
<p class="note">Timelines reflect our general reading of ss. 627.70131 and 627.70132, Florida Statutes, as amended through recent reforms. Laws change and exceptions apply — confirm current deadlines with your policy, your insurer or a Florida attorney. This is not legal advice.</p>""",
        "sections": [
            ("The windows that matter most", "<p>Under current Florida law, notice of a new or reopened property claim generally must be given within <strong>one year</strong> of the date of loss, and a supplemental claim within <strong>18 months</strong>. Insurers generally must acknowledge a claim within days of notice and pay or deny within a set period, commonly <strong>60 days</strong> after notice, absent factors beyond their control.</p><p>Appraisal has its own clock: many policies require a written demand, set a short window for each side to name its appraiser and expect the appraisers to select an umpire within a stated period. Those deadlines live in your policy, not the statute.</p>"),
            ("Why it helps to start early", "<p>Building a documented estimate, gathering photos and pulling the insurer’s file takes time. Owners who wait until the last month of a notice window often end up rushing the evidence that wins appraisals. Our <a href=\"/claim-tools/appraisal-readiness-quiz/\">readiness quiz</a> shows what to collect first.</p>"),
        ],
        "faqs": [
            ("How long do I have to file a property claim in Florida?", "For new or reopened claims, Florida law generally requires notice within one year of the date of loss; supplemental claims generally within 18 months. Your policy may impose additional conditions."),
            ("Does invoking appraisal stop the claim clock?", "Not automatically. Appraisal deadlines are set by your policy, and statutory notice and lawsuit deadlines may keep running. Get legal advice if a deadline is close."),
            ("What if my insurer misses its deadline?", "Missed statutory timelines can matter, but the remedies are a legal question. Florida Insurance Appraiser handles the amount of loss; talk with a Florida attorney about remedies."),
        ],
    },
    {
        "slug": "roof-measurement-calculator",
        "name": "Roof Measurement Calculator",
        "icon": "roof",
        "short": "Convert a home’s footprint and pitch into roof squares, waste, shingle bundles and underlayment — then compare against the insurer’s estimate.",
        "title": "Roof Squares Calculator: Pitch, Waste & Bundles",
        "description": "Calculate roof area, squares, waste factor, shingle bundles and underlayment from footprint and pitch, then check the measurements in your insurance estimate.",
        "h1": "Roof Measurement Calculator",
        "kicker": "Squares, pitch & waste",
        "lead": "Measurement errors are a quiet source of underpaid roof claims. Estimate your roof’s true surface area from the footprint and pitch, then compare it to the squares in the insurer’s estimate.",
        "ui": f"""<form class="tool" data-tool="roof" onsubmit="return false">
<div class="tool-grid">
{_num('r_len', 'Footprint length (ft)', '62', '0.5')}
{_num('r_wid', 'Footprint width (ft)', '38', '0.5')}
{_num('r_oh', 'Eave overhang (inches)', '18', '1')}
{_sel('r_pitch', 'Roof pitch', [(str(p), f'{p}/12', p == 6) for p in [2, 3, 4, 5, 6, 7, 8, 9, 10, 12]])}
{_sel('r_style', 'Roof style (sets waste factor)', [('0.10', 'Gable — 10% waste', False), ('0.15', 'Hip — 15% waste', True), ('0.20', 'Complex / cut-up — 20% waste', False)])}
{_num('r_ins', 'Squares in insurer’s estimate (optional)', '', '0.01')}
</div></form>
<div class="out">
<div><span>Roof surface area</span><b data-o="area">—</b></div>
<div class="hl"><span>Squares incl. waste</span><b data-o="sq">—</b></div>
<div><span>Shingle bundles (3 per sq)</span><b data-o="bund">—</b></div>
</div>
<p class="verdict" id="roof-verdict"></p>""",
        "sections": [
            ("The math behind it", "<p>A roofing square is 100 square feet. The calculator adds the overhang to each side of the footprint, multiplies by the pitch factor — √(1 + (rise ÷ 12)²) — to convert flat area into sloped surface area, then applies a waste factor that reflects how many cuts the roof shape requires.</p><p>Pitch factors to remember: 4/12 is about 1.054, 6/12 about 1.118, 8/12 about 1.202 and 12/12 about 1.414.</p>"),
            ("Common measurement problems in estimates", "<ul><li>Waste factor omitted or set too low for a hip or cut-up roof.</li><li>Pitch under-measured, which also hides steep-slope labor charges.</li><li>Detached garages, porches or additions left off the diagram.</li><li>Starter, ridge cap, drip edge and underlayment quantities that don’t match the measured area.</li></ul><p>If the gap is large, our <a href=\"/appraisal-services/roof-claim-appraisal/\">roof claim appraisal</a> service starts with an independent measurement.</p>"),
        ],
        "faqs": [
            ("Is this as accurate as aerial measurement?", "No — it is a planning estimate from a simple rectangular footprint. Aerial reports or a field measurement are more precise, especially on complex roofs."),
            ("What waste factor do insurers use?", "It varies by roof shape and estimator. Simple gable roofs often get around 10%, hip roofs around 15%, and complex roofs more. The suggested waste is often listed separately in the estimate."),
            ("Does Florida tile roof math differ?", "Tile is also measured in squares, but material is priced per square differently and often needs separate underlayment and hip/ridge line items."),
        ],
    },
    {
        "slug": "contents-inventory-builder",
        "name": "Contents Inventory Builder",
        "icon": "list",
        "short": "Build a room-by-room list of damaged belongings with replacement cost and estimated ACV. Saves in your browser and exports to CSV.",
        "title": "Home Contents Inventory Builder for Insurance Claims",
        "description": "Free contents inventory builder for Florida property claims: list damaged items by room, estimate replacement cost and ACV, save in your browser and export CSV.",
        "h1": "Contents Inventory Builder",
        "kicker": "Personal property list",
        "lead": "Contents (Coverage C) claims are won with a complete, organized list. Add each damaged item, and the builder totals replacement cost and estimated actual cash value. Your list stays in this browser — nothing is uploaded.",
        "ui": """<div class="tool" data-tool="inventory">
<div class="table-wrap"><table class="inv"><thead><tr><th style="min-width:170px">Item</th><th style="min-width:120px">Room</th><th style="width:70px">Qty</th><th style="width:80px">Age (yrs)</th><th style="min-width:150px">Category</th><th style="min-width:120px">Unit cost ($)</th><th style="width:40px"><span class="sr">Remove</span></th></tr></thead><tbody id="inv-body"></tbody></table></div>
<div class="actions" style="margin-top:14px"><button type="button" class="btn btn-ink" id="inv-add">+ Add item</button><button type="button" class="btn btn-ghost" id="inv-csv">Export CSV</button><button type="button" class="btn btn-ghost" id="inv-print">Print</button><button type="button" class="btn btn-ghost" id="inv-clear">Clear list</button></div>
<div class="out">
<div><span>Items</span><b data-o="count">0</b></div>
<div class="hl"><span>Replacement cost (RCV)</span><b data-o="rcv">$0</b></div>
<div><span>Estimated ACV</span><b data-o="acv">$0</b></div>
</div></div>""",
        "sections": [
            ("Tips for a contents list that holds up", "<ul><li>Go room by room, including closets, the garage, attic and outdoor areas.</li><li>Record brand, model and size where you can — “55-inch Samsung QLED” prices more accurately than “TV”.</li><li>Use current like-kind-and-quality replacement prices, not what you paid years ago.</li><li>Keep photos or video of damaged items before disposal, and note anything a mitigation company removed.</li><li>Separate items with special limits (jewelry, firearms, collectibles, business property) and check your policy’s sub-limits.</li></ul>"),
            ("How the ACV estimate is calculated", "<p>Each category carries a typical service life, and the builder applies straight-line depreciation with a 20% floor (no item drops below 20% of its replacement cost). Real insurer depreciation tables vary, so treat ACV as a ballpark. Replacement cost policies generally pay the withheld depreciation after items are replaced — see the <a href=\"/claim-tools/acv-depreciation-calculator/\">ACV calculator</a>.</p>"),
        ],
        "faqs": [
            ("Is my inventory stored online?", "No. It is saved only in your browser’s local storage on this device. Export a CSV to keep a copy or share it with your adjuster or appraiser."),
            ("Can contents be included in an appraisal?", "Yes. If you and the insurer disagree on the value of covered personal property, that amount can be part of the appraisal, subject to your policy terms."),
            ("Do I need receipts?", "Receipts help but aren’t always required. Photos, bank or card statements, product manuals and online order history are all useful proof of ownership and value."),
        ],
    },
    {
        "slug": "appraisal-readiness-quiz",
        "name": "Appraisal Readiness Quiz",
        "icon": "check",
        "short": "Twelve quick questions that score how prepared your claim is for appraisal, with a personalized to-do list for any gaps.",
        "title": "Appraisal Readiness Quiz for Florida Property Claims",
        "description": "Twelve quick questions from Florida Insurance Appraiser score how ready your property claim is for appraisal and build a to-do list for whatever is missing.",
        "h1": "Appraisal Readiness Quiz",
        "kicker": "Score your claim file",
        "lead": "Appraisal rewards preparation. Check every statement that is true for your claim to get a readiness score and a short list of what to tackle next.",
        "ui": """<div class="tool quiz" data-tool="quiz"><ol id="quiz-list"></ol>
<div class="result"><small>Your readiness score</small><div class="big" data-o="score">0 / 100</div><div class="meter"><i></i></div><small data-o="label">Check the items that apply.</small></div>
<div id="quiz-todo"></div></div>""",
        "sections": [
            ("Why preparation decides appraisals", "<p>In appraisal, two appraisers compare estimates line by line and an umpire settles what they can’t agree on. The side with clear measurements, dated photos and a complete estimate usually controls that conversation. The quiz focuses on the documents that carry the most weight. If you score low, start with a certified copy of the policy and the insurer’s full estimate.</p>"),
            ("What to do with your score", "<p>Above 75, you’re in good shape to talk about invoking appraisal. Between 40 and 75, close the gaps listed under your score first. Below 40, focus on documentation — our <a href=\"/appraisal-services/homeowners-claim-appraisal/\">homeowners claim appraisal</a> team can help build the file.</p>"),
        ],
        "faqs": [
            ("Do I need a contractor estimate before appraisal?", "It helps a great deal. A detailed, line-item estimate — ideally in Xactimate or Symbility format — gives the appraisers something concrete to compare."),
            ("What is a certified policy?", "A complete copy of your policy, including declarations, forms and endorsements, certified by the insurer as in force on the date of loss. You can request one in writing."),
            ("Is my answer data saved?", "No. The quiz runs entirely in your browser."),
        ],
    },
]
