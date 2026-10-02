"""Free claim tool pages: /tools/ hub and one page per tool (markup wired to assets/js/tools.js)."""

CHECKLIST = [
    ("Right after the damage", [
        ("Make sure everyone is safe and call 911 for emergencies", "Safety comes before documentation."),
        ("Prevent further damage if it is safe to do so", "Tarp, shut off water, board up, and keep every receipt."),
        ("Photograph and video every affected area", "Wide shots first, then close-ups, before cleanup starts."),
        ("Write down the date, time and how you discovered the damage", ""),
        ("Save damaged items or photograph them before disposal", ""),
    ]),
    ("Reporting the claim", [
        ("Report the claim to your insurer promptly", "Follow the notice requirements in your policy."),
        ("Write down your claim number and adjuster contact details", ""),
        ("Get a full copy of your policy, including endorsements", "Your declarations page alone is not enough."),
        ("Start a claim diary for every call, email and visit", "Use our free claim diary tool."),
        ("Ask the insurer what documents it needs, in writing", ""),
    ]),
    ("Inspection", [
        ("Prepare a list of every damaged area to show the adjuster", ""),
        ("Be present for the inspection, or have a representative there", ""),
        ("Point out interior and exterior damage, including soft metals", ""),
        ("Ask which areas were inspected and note anything missed", ""),
    ]),
    ("Estimate and payment", [
        ("Get every version of the insurer's estimate in writing", ""),
        ("Compare it line by line with a contractor's scope", "Look for missing rooms, quantities and items."),
        ("Check the deductible, depreciation and payment math", "Try our claim payment calculator."),
        ("Build a contents inventory for damaged belongings", ""),
        ("Keep receipts for additional living expenses", "Hotels, meals and mileage above normal costs."),
    ]),
    ("Repairs and closing", [
        ("Keep contracts, invoices and proof of completed repairs", ""),
        ("Request recoverable depreciation after repairs, if applicable", "Check your policy's time limit."),
        ("Note any deadlines in decision letters and your policy", ""),
        ("List open questions for a free claim review", ""),
        ("Store a backup of your entire claim file", ""),
    ]),
]

LIFE_PRESETS = [
    ("Asphalt shingle roof, 3-tab (20 yrs)", 20), ("Architectural shingle roof (30 yrs)", 30), ("Metal roof (50 yrs)", 50),
    ("Carpet (10 yrs)", 10), ("Hardwood flooring (50 yrs)", 50), ("Laminate / LVP flooring (20 yrs)", 20),
    ("Interior paint (8 yrs)", 8), ("Exterior paint (10 yrs)", 10), ("Wood fence (15 yrs)", 15), ("Gutters, aluminum (25 yrs)", 25),
    ("HVAC system (15 yrs)", 15), ("Water heater (10 yrs)", 10), ("Refrigerator (13 yrs)", 13), ("Washer / dryer (11 yrs)", 11),
    ("Television (8 yrs)", 8), ("Sofa / upholstered furniture (10 yrs)", 10), ("Mattress (8 yrs)", 8), ("Clothing (5 yrs)", 5),
]


def _tool_page(c, kw, slug, title, desc, h1, lead, body_html, faqs, how=None):
    t = c["TOOL_BY_SLUG"][slug]
    path = f"/tools/{slug}/"
    crumbs = [("Home", "/"), ("Free tools", "/tools/"), (t["name"], path)]
    others = [x for x in c["TOOLS"] if x["slug"] != slug][:3]
    how_html = ""
    if how:
        how_html = '<div class="tiles" data-stagger>' + "".join(f'<div class="tile"><span class="ico">{c["icon"](i)}</span><h3>{h}</h3><p>{p}</p></div>' for i, h, p in how) + "</div>"
    body = c["page_hero"](h1, lead, "tools", "Calculator and pencil on notepaper", crumbs, actions=False)
    body += f'''<section class="section">{body_html}</section>
{f'<section class="section tinted"><div class="wrap"><div class="section-head" data-reveal><span class="eyebrow">How it works</span><h2>Using the {t["name"].lower()}</h2></div>{how_html}</div></section>' if how else ''}
<section class="section"><div class="wrap two-col top"><div data-reveal="left"><span class="eyebrow">Questions</span><h2>{t["name"]} <em>FAQs</em></h2>
<p>These tools from {kw} help you get organized. They do not decide coverage or payment. For a closer look at your own numbers, request a free claim review.</p>
<a class="button" href="/contact/">Free claim review {c["ARROW"]}</a></div><div>{c["faq_block"](faqs)}</div></div></section>
<section class="section sand"><div class="wrap"><div class="section-head" data-reveal><span class="eyebrow">More free tools</span><h2>Keep getting organized</h2></div>{c["tool_cards"](others)}</div></section>
{c["cta_band"]()}'''
    schema = [c["breadcrumb_schema"](crumbs), c["faq_schema"](faqs),
              {"@type": "WebApplication", "name": t["name"] + " by " + kw, "url": c["SITE"]["origin"] + path,
               "applicationCategory": "FinanceApplication", "operatingSystem": "Any (web browser)",
               "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "description": desc,
               "provider": {"@id": c["SITE"]["origin"] + "/#organization"}}]
    c["write"](path, c["render"](path, title, desc, body, current="/tools/", schema=schema, scripts=("tools.js",)))


def build(c, kw):
    icon, A = c["icon"], c["ARROW"]

    # ---------------- hub
    body = c["page_hero"]("A little preparation. <em>A lot more clarity.</em>",
                          f"Seven free claim tools from {kw}. Calculate a deductible, estimate a payment, map Texas claim deadlines and organize your file. Everything stays in your browser.",
                          "tools", "Calculator and pencil on notepaper", [("Home", "/"), ("Free tools", "/tools/")], actions=False)
    body += f'''<section class="section"><div class="wrap"><div class="section-head" data-reveal><span class="eyebrow">Calculators &amp; organizers</span><h2>Free tools from {kw}</h2>
<p>Use them before your first claim conversation, while your claim is under review, or when an estimate arrives. No sign-up, and nothing you enter is sent to us.</p></div>
{c["tool_cards"]()}</div></section>
<section class="section tinted"><div class="wrap two-col"><div data-reveal="left"><span class="eyebrow">Private by design</span><h2>Your numbers <em>stay with you.</em></h2>
<p>The calculators run entirely in your browser. The checklist, inventory, diary and depreciation worksheet save to local storage on your own device so you can come back later. Export to CSV or print whenever you are ready to share with your adjuster.</p>
<ul class="check-list"><li>No account or email required</li><li>Works on phones, tablets and desktops</li><li>Printable and exportable results</li></ul></div>
<div class="frame wide" data-reveal="zoom">{c["img"]("estimate", "Reviewing claim numbers with a calculator", parallax=".08")}</div></div></section>
{c["cta_band"]("Numbers are a start. A review gives you the full picture.")}'''
    c["write"]("/tools/", c["render"]("/tools/", "Free Claim Tools & Calculators | The Colony Public Adjuster",
                                      "Free claim tools from The Colony Public Adjuster: deductible, payment and depreciation calculators, Texas claim deadlines, checklist, inventory and diary.",
                                      body, current="/tools/", scripts=("tools.js",),
                                      schema=[c["breadcrumb_schema"]([("Home", "/"), ("Free tools", "/tools/")]),
                                              {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i, "name": t["name"], "url": c["SITE"]["origin"] + f"/tools/{t['slug']}/"} for i, t in enumerate(c["TOOLS"], 1)]}]))

    # ---------------- 1 deductible
    html1 = f'''<div class="wrap tool-shell" id="tool-deductible">
<form class="panel" data-reveal="left" novalidate><h2 style="font-size:1.9rem">Your policy numbers</h2>
<div class="seg" role="group" aria-label="Deductible type"><button type="button" data-mode="percent" aria-pressed="true">Percentage</button><button type="button" data-mode="flat" aria-pressed="false">Flat dollar</button></div>
<div class="form-grid">
<div class="field full" data-mode-show="percent"><label for="coverage">Dwelling coverage limit (Coverage A, $)</label><input id="coverage" name="coverage" inputmode="decimal" value="400000"><span class="hint">Find it on your declarations page.</span></div>
<div class="field full" data-mode-show="percent"><label for="rate">Wind/hail or all-peril deductible (%)</label><div class="range-row"><input id="rate" name="rate" type="range" min="0.5" max="10" step="0.5" value="2"><output id="rate-out">2%</output></div></div>
<div class="field full" data-mode-show="flat" hidden><label for="flat">Flat deductible ($)</label><input id="flat" name="flat" inputmode="decimal" value="2500"></div>
<div class="field full"><label for="estimate">Repair estimate (optional, $)</label><input id="estimate" name="estimate" inputmode="decimal" placeholder="e.g. 18500"><span class="hint">From your insurer or contractor, to compare with the deductible.</span></div>
</div>
<div data-mode-show="percent"><h3 style="margin-top:26px">Common percentages at this limit</h3><div class="table-wrap"><table class="data-table"><thead><tr><th>Deductible</th><th class="num">Amount</th></tr></thead><tbody id="ded-table"></tbody></table></div></div>
</form>
<div class="result-card" data-reveal="right" aria-live="polite"><span class="eyebrow on-dark" style="color:var(--gold-2)">Your deductible</span><div class="big-num" id="ded-out">$8,000.00</div><p id="ded-desc"></p>
<div class="bar-viz" id="ded-bar"></div><div class="bar-legend"></div>
<div class="rows"><div><span>Repair estimate</span><strong id="ded-est">—</strong></div><div class="total"><span>Amount above deductible</span><strong id="ded-above">—</strong></div></div>
<p id="ded-verdict"></p><p class="notice">Illustration only. Your policy may use a different deductible for different perils, and a percentage deductible is usually based on Coverage A, not the claim amount. This is not a payment estimate.</p></div>
</div>'''
    _tool_page(c, kw, "deductible-calculator", "Deductible Calculator | The Colony Public Adjuster",
               "Free deductible calculator from The Colony Public Adjuster. Convert a 1%, 2% or 5% wind/hail deductible into dollars and compare it with your repair estimate.",
               "What does that <em>percentage deductible</em> really cost?", "Many Texas policies use a percentage deductible for wind and hail. Enter your dwelling coverage and see the dollar amount, then compare it with a repair estimate.",
               html1,
               [("How is a percentage deductible calculated?", "It is usually a percentage of your dwelling coverage limit (Coverage A), not of the damage. A 2% deductible on a $400,000 dwelling limit is $8,000."),
                ("Can I have different deductibles for different perils?", "Yes. Many Texas policies have a separate wind/hail deductible and an all-other-perils deductible. Check your declarations page."),
                ("Should I file a claim if the damage is close to my deductible?", "That is your decision. Hidden damage often appears during inspection, so an estimate that seems close may grow. A free review can help you weigh it.")],
               [("percent", "Pick the deductible type", "Choose percentage or flat dollar, matching your declarations page."),
                ("calculator", "Enter your numbers", "Add your Coverage A limit and percentage. The result updates as you type."),
                ("scale", "Compare an estimate", "Add a repair estimate to see how much of it sits above the deductible.")])

    # ---------------- 2 payment
    html2 = f'''<div class="wrap tool-shell" id="tool-payment">
<form class="panel" data-reveal="left" novalidate><h2 style="font-size:1.9rem">Your estimate</h2>
<div class="form-grid">
<div class="field full"><label for="rcv">Replacement cost value (RCV) of repairs ($)</label><input id="rcv" name="rcv" inputmode="decimal" value="24000"><span class="hint">The total before depreciation, from the estimate.</span></div>
<div class="field full"><label>Depreciation</label><div class="seg" role="group" aria-label="Depreciation entry"><button type="button" data-mode="amount" aria-pressed="true">Dollar amount</button><button type="button" data-mode="pct" aria-pressed="false">Percentage</button></div>
<div data-mode-show="amount"><label class="sr" for="dep">Depreciation amount</label><input id="dep" name="dep" inputmode="decimal" value="6000"></div>
<div data-mode-show="pct" hidden><div class="range-row"><label class="sr" for="deppct">Depreciation percent</label><input id="deppct" name="deppct" type="range" min="0" max="80" step="1" value="25"><output id="dep-out">25%</output></div></div></div>
<div class="field"><label for="deductible">Deductible ($)</label><input id="deductible" name="deductible" inputmode="decimal" value="4000"></div>
<div class="field"><label for="prior">Prior payments ($)</label><input id="prior" name="prior" inputmode="decimal" value="0"></div>
<div class="field full"><label for="policy">Policy valuation</label><select id="policy" name="policy"><option value="rcv">Replacement cost (RCV), depreciation recoverable</option><option value="acv">Actual cash value (ACV) only</option></select></div>
</div></form>
<div class="result-card" data-reveal="right" aria-live="polite"><span class="eyebrow on-dark" style="color:var(--gold-2)">Estimated first payment</span><div class="big-num" id="pay-first">$0</div><p id="pay-note"></p>
<div class="bar-viz" id="pay-bar"></div><div class="bar-legend"></div>
<div class="rows"><div><span>Replacement cost (RCV)</span><strong id="pay-rcv"></strong></div><div><span>Depreciation</span><strong id="pay-dep"></strong></div>
<div><span>Actual cash value (ACV)</span><strong id="pay-acv"></strong></div><div><span>Deductible</span><strong id="pay-ded"></strong></div><div><span>Prior payments</span><strong id="pay-prior"></strong></div>
<div><span>Recoverable after repairs</span><strong id="pay-hold"></strong></div><div class="total"><span>Potential total</span><strong id="pay-total"></strong></div></div>
<p class="notice">Simplified illustration. Policy limits, sublimits, code coverage, overhead and profit, and other terms can change the result. This is not a settlement offer or a guarantee.</p></div></div>'''
    _tool_page(c, kw, "claim-payment-calculator", "Claim Payment Calculator | The Colony Public Adjuster",
               "See how RCV, depreciation, your deductible and prior payments shape your insurance claim check. Free calculator from The Colony Public Adjuster.",
               "How your claim payment <em>is actually calculated.</em>", "Your first check is rarely the full estimate. This calculator shows how depreciation, your deductible and prior payments combine, and how much may be recoverable after repairs.",
               html2,
               [("Why is my first insurance check less than the estimate?", "Most replacement cost policies first pay actual cash value: the estimate minus depreciation and your deductible. The withheld depreciation may be paid after repairs are completed."),
                ("How do I recover depreciation?", "Typically by completing repairs and sending proof, such as the final invoice, within the time your policy allows. Check your policy for the deadline."),
                ("Is depreciation applied to labor?", "Practices vary by insurer and policy. Ask the insurer how depreciation was calculated on your estimate.")],
               [("calculator", "Enter the RCV", "Use the replacement cost total from the estimate, before depreciation."),
                ("trend", "Add depreciation", "Enter the dollar amount from the estimate, or try a percentage."),
                ("eye", "Read the breakdown", "See the first payment, what may be recoverable later and the potential total.")])

    # ---------------- 3 depreciation
    opts = "".join(f'<option value="{l}" data-life="{y}">{l}</option>' for l, y in LIFE_PRESETS)
    html3 = f'''<div class="wrap tool-shell" id="tool-depreciation">
<form class="panel" data-reveal="left" novalidate><h2 style="font-size:1.9rem">Add an item</h2>
<div class="form-grid">
<div class="field full"><label for="preset">Quick pick (optional)</label><select id="preset" name="preset"><option value="">Choose a typical item…</option>{opts}</select><span class="hint">Life expectancies are common industry estimates, not your insurer's tables.</span></div>
<div class="field full"><label for="itemname">Item or component *</label><input id="itemname" name="itemname" maxlength="80" required placeholder="e.g. Living room carpet"></div>
<div class="field"><label for="cost">Replacement cost ($) *</label><input id="cost" name="cost" inputmode="decimal" required placeholder="3200"></div>
<div class="field"><label for="age">Age (years)</label><input id="age" name="age" inputmode="decimal" placeholder="4"></div>
<div class="field"><label for="life">Life expectancy (years) *</label><input id="life" name="life" inputmode="decimal" required value="10"></div>
<div class="field"><label for="cap">Max depreciation</label><div class="range-row"><input id="cap" name="cap" type="range" min="20" max="100" step="5" value="80"><output id="cap-out">80%</output></div></div>
</div>
<p class="small" style="margin-top:14px">Preview: <strong id="depr-preview"></strong></p>
<button class="button" type="submit" style="margin-top:8px">Add to worksheet {A}</button></form>
<div class="result-card" data-reveal="right" aria-live="polite"><span class="eyebrow on-dark" style="color:var(--gold-2)">Worksheet total</span><div class="big-num" id="depr-acv">$0</div><p>Actual cash value of <span id="depr-count">0 items</span></p>
<div class="bar-viz" id="depr-bar"></div><div class="bar-legend"></div>
<div class="rows"><div><span>Replacement cost</span><strong id="depr-rcv">$0</strong></div><div><span>Depreciation</span><strong id="depr-dep">$0</strong></div></div>
<p class="notice">Straight-line illustration: age ÷ life expectancy, capped at the maximum you set. Insurers may use different tables, condition adjustments or no depreciation on some items.</p></div>
<div class="tool-shell wide" style="grid-column:1/-1"><div class="toolbar no-print"><button class="button small ghost" type="button" id="depr-csv">Export CSV</button><button class="button small ghost" type="button" id="depr-print">Print</button><button class="button small ghost" type="button" id="depr-clear">Clear all</button></div>
<div class="table-wrap"><table class="data-table"><thead><tr><th>Item</th><th class="num">Replacement cost</th><th class="num">Age / life</th><th class="num">Depreciated</th><th class="num">ACV</th><th><span class="sr">Remove</span></th></tr></thead><tbody id="depr-rows"></tbody></table></div></div>
</div>'''
    _tool_page(c, kw, "depreciation-calculator", "Depreciation Calculator | The Colony Public Adjuster",
               "Free depreciation calculator from The Colony Public Adjuster. Estimate actual cash value item by item for roofs, flooring, appliances and contents.",
               "Estimate depreciation <em>item by item.</em>", "Depreciation is often the largest gap between an estimate and your first check. Build a worksheet that shows how age and life expectancy affect actual cash value.",
               html3,
               [("How do insurance companies calculate depreciation?", "Commonly by comparing an item's age with its expected useful life, sometimes adjusted for condition. Ask the insurer which method and life expectancy were used on your estimate."),
                ("Is there a maximum on depreciation?", "Many estimating tools cap depreciation, often somewhere between 50% and 80%, but caps vary. This tool lets you set the cap you want to test."),
                ("Where is my worksheet saved?", "Only in this browser, on this device, using local storage. Nothing is sent to us. Export to CSV to keep a copy.")],
               [("list", "Pick an item", "Use a quick pick or type your own item and replacement cost."),
                ("clock", "Add age and life", "Age divided by life expectancy gives the straight-line depreciation."),
                ("box", "Build the worksheet", "Add as many items as you need, then export or print.")])

    # ---------------- 4 deadlines
    html4 = f'''<div class="wrap tool-shell" id="tool-timeline">
<form class="panel" data-reveal="left" novalidate><h2 style="font-size:1.9rem">Your claim dates</h2>
<div class="form-grid">
<div class="field full"><label for="notice">Date the insurer received notice of your claim</label><input id="notice" name="notice" type="date"></div>
<div class="field full"><label for="items">Date the insurer received all items it requested (optional)</label><input id="items" name="items" type="date"><span class="hint">Statements, documents and forms the insurer asked for.</span></div>
<div class="field full"><label for="accepted">Date the insurer said it would pay (optional)</label><input id="accepted" name="accepted" type="date"></div>
<label class="check-label field full"><input type="checkbox" name="cat" id="cat"><span>Claim arises from a weather-related catastrophe or major natural disaster declared by the Texas insurance commissioner (adds 15 days).</span></label>
<label class="check-label field full"><input type="checkbox" name="surplus" id="surplus"><span>My insurer is an eligible surplus lines insurer (30 business days to acknowledge).</span></label>
</div>
<div class="callout"><p><strong>Why this matters.</strong> Texas Insurance Code Chapter 542, Subchapter B (the Prompt Payment of Claims Act) sets deadlines for insurers to acknowledge, decide and pay claims. Knowing the dates helps you follow up at the right time.</p></div></form>
<div class="result-card" data-reveal="right" aria-live="polite"><span class="eyebrow on-dark" style="color:var(--gold-2)">Key insurer deadlines</span><ul class="deadline-list" id="tl-list"></ul>
<button class="button small outline-light no-print" type="button" id="tl-print">Print timeline</button>
<p class="notice">Educational summary, not legal advice. Business days exclude weekends and federal holidays as an approximation. Some policies, insurers and claim types follow different rules, and other exceptions may apply. Confirm deadlines with the statute, your insurer or an attorney.</p></div></div>'''
    _tool_page(c, kw, "texas-claim-deadlines", "Texas Claim Deadline Calculator | The Colony Public Adjuster",
               "Map Texas Prompt Payment Act deadlines for your claim: acknowledgment, decision and payment dates. Free tool from The Colony Public Adjuster.",
               "Texas claim deadlines, <em>mapped to your dates.</em>", "Texas law gives insurers set windows to acknowledge, decide and pay property claims. Enter your dates to see when each response is generally due.",
               html4,
               [("How long does an insurance company have to acknowledge a claim in Texas?", "Generally 15 days after receiving notice of the claim, during which it must also begin investigating and request the items it needs (Tex. Ins. Code §542.055). Eligible surplus lines insurers generally have 30 business days."),
                ("How long does the insurer have to accept or deny?", "Generally 15 business days after receiving all requested items, extendable up to 45 days if the insurer notifies you that it needs more time and explains why (§542.056)."),
                ("When must the insurer pay once it accepts the claim?", "Generally within 5 business days after notifying you that it will pay (§542.057). Weather catastrophes can add 15 days to these deadlines.")],
               [("calendar", "Enter the notice date", "The date the insurer received notice of your claim."),
                ("clipboard", "Add later dates", "When the insurer received requested items, and when it agreed to pay."),
                ("clock", "See the deadlines", "Each date is calculated and labeled with the statute section it comes from.")])

    # ---------------- 5 checklist
    total = sum(len(i) for _s, i in CHECKLIST)
    stages = ""
    n = 0
    for stage, items in CHECKLIST:
        rows = ""
        for label, note in items:
            n += 1
            rows += f'<label class="check-item"><input type="checkbox" id="c{n}" data-label="{label}"><span>{label}{f"<small>{note}</small>" if note else ""}</span></label>'
        stages += f'<div class="checklist-stage"><h3>{stage} <small>0 / {len(items)}</small></h3>{rows}</div>'
    html5 = f'''<div class="wrap tool-shell" id="tool-checklist">
<div class="panel" data-reveal="left"><h2 style="font-size:1.9rem">Your claim checklist</h2><p class="small">Your progress saves in this browser. Nothing is sent to us.</p>{stages}</div>
<div class="result-card" data-reveal="right" aria-live="polite"><span class="eyebrow on-dark" style="color:var(--gold-2)">Progress</span>
<div style="display:flex;gap:22px;align-items:center;margin:14px 0"><div class="ring" id="check-ring" data-label="0%"></div><div><strong id="check-status" style="font-size:1.1rem">0 of {total} steps complete</strong><p style="margin:6px 0 0">Next up: <span id="check-next"></span></p></div></div>
<div class="toolbar no-print"><button class="button small light" type="button" id="check-print">Print checklist</button><button class="button small outline-light" type="button" id="check-reset">Reset</button></div>
<p class="notice">An organizational aid, not a complete list of policy duties or legal requirements. Always follow the specific requirements in your policy and insurer correspondence.</p></div></div>'''
    _tool_page(c, kw, "claim-checklist", "Insurance Claim Checklist | The Colony Public Adjuster",
               f"A free {total}-step property insurance claim checklist from The Colony Public Adjuster, from the day of the damage to final repairs. Saves progress and prints.",
               "A claim checklist <em>for every stage.</em>", f"{total} practical steps in five stages, from the moment damage happens to the final repair invoice. Check them off as you go.",
               html5,
               [("What is the first thing to do after property damage?", "Make sure everyone is safe, then take reasonable steps to prevent further damage and document conditions with photos and video before cleanup."),
                ("Do I need to keep damaged items?", "Keep them, or photograph them thoroughly, until the insurer has had a chance to document them, unless they pose a health or safety risk."),
                ("Will my checklist be saved?", "Yes, in this browser on this device. Clearing your browser data or using a private window will reset it.")])

    # ---------------- 6 inventory
    html6 = f'''<div class="wrap tool-shell" id="tool-inventory">
<form class="panel" data-reveal="left" novalidate><h2 style="font-size:1.9rem">Add an item</h2>
<div class="form-grid">
<div class="field"><label for="room">Room</label><input id="room" name="room" list="rooms" maxlength="40" value="Living room"><datalist id="rooms"><option>Living room</option><option>Kitchen</option><option>Primary bedroom</option><option>Bedroom 2</option><option>Bathroom</option><option>Garage</option><option>Office</option><option>Dining room</option><option>Closet / storage</option><option>Patio / outdoor</option></datalist></div>
<div class="field"><label for="inv-item">Item *</label><input id="inv-item" name="itemname" maxlength="100" required placeholder="e.g. 65-inch TV"></div>
<div class="field"><label for="qty">Quantity</label><input id="qty" name="qty" type="number" min="1" value="1"></div>
<div class="field"><label for="year">Purchase year</label><input id="year" name="year" inputmode="numeric" maxlength="4" placeholder="2022"></div>
<div class="field"><label for="value">Estimated replacement value each ($)</label><input id="value" name="value" inputmode="decimal" placeholder="899"></div>
<div class="field"><label for="notes">Brand / model / serial</label><input id="notes" name="notes" maxlength="140"></div>
</div><button class="button" type="submit" style="margin-top:18px">Add item {A}</button></form>
<div class="result-card" data-reveal="right" aria-live="polite"><span class="eyebrow on-dark" style="color:var(--gold-2)">Inventory total</span><div class="big-num" id="inv-total">$0</div><p id="inv-count">0 items</p>
<div class="rows" id="inv-rooms"></div><p class="notice">Saved only in this browser. Export a CSV copy and store it somewhere safe outside your home.</p></div>
<div class="tool-shell wide" style="grid-column:1/-1"><div class="toolbar no-print"><button class="button small ghost" type="button" id="inv-csv">Export CSV</button><button class="button small ghost" type="button" id="inv-print">Print</button><button class="button small ghost" type="button" id="inv-clear">Clear all</button></div>
<div class="table-wrap"><table class="data-table"><thead><tr><th>Room</th><th>Item</th><th class="num">Qty</th><th class="num">Year</th><th class="num">Value</th><th><span class="sr">Remove</span></th></tr></thead><tbody id="inv-rows"></tbody></table></div></div></div>'''
    _tool_page(c, kw, "home-inventory", "Home Inventory Tool | The Colony Public Adjuster",
               "Build a room-by-room home inventory for insurance with values, purchase years and serial numbers, then export to CSV. Free tool from The Colony Public Adjuster.",
               "Build your home inventory <em>room by room.</em>", "A contents inventory makes a fire, water or theft claim far easier. Add items as you walk through each room, then export a copy.",
               html6,
               [("Why do I need a home inventory?", "After a major loss it is hard to remember everything you owned. An inventory with values, ages and photos makes a contents claim faster and more complete."),
                ("What should I include?", "Furniture, electronics, appliances, clothing, jewelry, tools, sports equipment and anything of value. Note brand, model, serial number and purchase year where possible."),
                ("Is my inventory private?", "Yes. It is saved only in your browser. We never see it unless you choose to share the exported file.")])

    # ---------------- 7 diary
    html7 = f'''<div class="wrap tool-shell" id="tool-diary">
<form class="panel" data-reveal="left" novalidate><h2 style="font-size:1.9rem">Log an entry</h2>
<div class="form-grid">
<div class="field"><label for="date">Date</label><input id="date" name="date" type="date" required></div>
<div class="field"><label for="type">Type</label><select id="type" name="type"><option>Phone call</option><option>Email</option><option>Letter</option><option>Inspection / visit</option><option>Document sent</option><option>Payment received</option><option>Other</option></select></div>
<div class="field full"><label for="who">Spoke with / from</label><input id="who" name="who" maxlength="80" placeholder="e.g. Desk adjuster J. Smith"></div>
<div class="field full"><label for="summary">Summary *</label><textarea id="summary" name="summary" required maxlength="600" placeholder="What was discussed, requested or promised"></textarea></div>
<div class="field full"><label for="follow">Follow-up date</label><input id="follow" name="follow" type="date"></div>
</div><button class="button" type="submit" style="margin-top:18px">Save entry {A}</button></form>
<div class="result-card" data-reveal="right" aria-live="polite"><span class="eyebrow on-dark" style="color:var(--gold-2)">Claim diary</span><div class="big-num" id="diary-count">0</div><p>entries logged</p>
<div class="rows"><div><span>Next follow-up</span><strong id="diary-next">None scheduled</strong></div><div><span>Overdue follow-ups</span><strong id="diary-overdue">0</strong></div></div>
<p class="notice">Saved only in this browser. Export a CSV copy to share with your public adjuster or attorney.</p></div>
<div class="tool-shell wide" style="grid-column:1/-1"><div class="toolbar no-print"><button class="button small ghost" type="button" id="diary-csv">Export CSV</button><button class="button small ghost" type="button" id="diary-print">Print</button><button class="button small ghost" type="button" id="diary-clear">Clear all</button></div>
<div class="table-wrap"><table class="data-table"><thead><tr><th>Date</th><th>Type</th><th>With / from</th><th>Summary</th><th>Follow-up</th><th><span class="sr">Remove</span></th></tr></thead><tbody id="diary-rows"></tbody></table></div></div></div>'''
    _tool_page(c, kw, "claim-diary", "Claim Diary & Call Log | The Colony Public Adjuster",
               "Keep a dated log of every insurance claim call, email, inspection and payment with follow-up reminders. Free claim diary from The Colony Public Adjuster.",
               "A claim diary that <em>keeps everyone accountable.</em>", "Every call, email, inspection and payment in one dated log, with follow-up reminders so nothing slips through the cracks.",
               html7,
               [("Why keep a claim diary?", "A dated record of who said what, and when, helps you follow up on promises, track deadlines and explain the history of your claim to anyone who reviews it."),
                ("What should each entry include?", "The date, how you communicated, who you spoke with, what was discussed or requested, and when to follow up."),
                ("Can I share the diary?", "Yes. Export it as a CSV file or print it to share with your public adjuster, contractor or attorney.")])
