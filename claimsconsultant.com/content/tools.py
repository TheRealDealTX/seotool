"""Six calculators.

Each page is a working tool plus the explanation of the arithmetic behind it.
The maths lives in assets/js/site.js; the markup here just has to agree with
it on input names and data-out keys.
"""

from siteconfig import BIZ

P = BIZ["phone_display"]


def _f(label, name, value, hint="", prefix="", suffix="", kind="number", step="any", options=None):
    """One input field."""
    inner_hint = '<span class="hint">%s</span>' % hint if hint else ""
    if options:
        opts = "".join('<option value="%s"%s>%s</option>'
                       % (v, " selected" if v == value else "", t) for v, t in options)
        control = '<select name="%s" id="f-%s">%s</select>' % (name, name, opts)
    else:
        pfx = '<span class="pfx">%s</span>' % prefix if prefix else ""
        sfx = '<span class="sfx">%s</span>' % suffix if suffix else ""
        control = ('<div class="inputgroup">%s<input type="%s" inputmode="decimal" step="%s" '
                   'name="%s" id="f-%s" value="%s">%s</div>'
                   % (pfx, kind, step, name, name, value, sfx))
    return ('<div class="field"><label for="f-%s">%s%s</label>%s</div>'
            % (name, label, inner_hint, control))


def _row(label, key, cls=""):
    return ('<div class="outrow%s"><span>%s</span><span data-out="%s">&mdash;</span></div>'
            % (" " + cls if cls else "", label, key))


def _calc(name, label, fields, out_title, big_key, big_caption, rows, note, flags=()):
    flaghtml = "".join('<div class="flag" data-flag="%s" hidden></div>' % f for f in flags)
    return f"""<form class="calc" data-calc="{name}" data-label="{label}" novalidate>
  <div class="calc-in">
    <p class="kicker" style="margin-bottom:18px;">Inputs</p>
    {fields}
  </div>
  <div class="calc-out">
    <p class="outhead">{out_title}</p>
    <div class="bignum" data-out="{big_key}">&mdash;</div>
    <p class="bignum-cap">{big_caption}</p>
    <div class="outrows">{rows}</div>
    <p class="outnote">{note}</p>
    {flaghtml}
    <div class="calc-actions">
      <button class="minibtn" type="button" data-action="copy">Copy summary</button>
      <button class="minibtn" type="button" data-action="print">Print</button>
      <button class="minibtn" type="button" data-action="reset">Reset</button>
    </div>
  </div>
</form>"""


# ---------------------------------------------------------------- 1. value
CLAIM_VALUE = _calc(
    "claim-value", "commercial claim value estimator",
    (_f("Building area", "sqft", "85000", "Gross square feet of the affected structure.", suffix="sq ft")
     + '<div class="field-row field-row--2">'
     + _f("Replacement cost per sq ft", "cost", "265", "Construction class and market.", prefix="$")
     + _f("Damage severity", "damage", "35", "Share of the building affected.", suffix="%")
     + "</div>"
     + '<div class="field-row field-row--2">'
     + _f("Contents / FF&amp;E", "contents", "18", "As a share of direct damage.", suffix="%")
     + _f("Code upgrade", "code", "12", "Ordinance and law exposure.", suffix="%")
     + "</div>"
     + '<div class="field-row field-row--2">'
     + _f("Debris removal", "debris", "5", "Share of direct damage.", suffix="%")
     + _f("Building age", "age", "22", "Years since construction.", suffix="yrs")
     + "</div>"
     + '<div class="field-row field-row--2">'
     + _f("Expected service life", "life", "50", "For depreciation.", suffix="yrs")
     + _f("Deductible basis", "dedtype", "pct", "", options=[("flat", "Flat dollar amount"),
                                                             ("pct", "Percentage of insured value")])
     + "</div>"
     + _f("Deductible", "ded", "2", "Dollar amount, or the percentage if you selected percentage above.")),
    "Estimated recovery", "rcvnet",
    "Replacement cost value, net of deductible, before recoverable depreciation is withheld.",
    (_row("Insured value of structure (TIV)", "tiv")
     + _row("Direct building damage", "direct")
     + _row("Contents and FF&amp;E", "contents")
     + _row("Code and ordinance work", "code")
     + _row("Debris removal", "debris")
     + _row("Gross replacement cost of loss", "rcv")
     + _row("Depreciation applied", "dep")
     + _row("Deductible", "deductible")
     + _row("First payment (ACV basis)", "acvnet")
     + _row("Recoverable depreciation held back", "holdback")
     + _row("Total at replacement cost", "rcvnet", "outrow--total")),
    "Depreciation is straight-line against the service life you entered and capped at 75%, which "
    "is roughly where carriers stop sustaining it on maintained commercial property. This is a "
    "planning figure, not an estimate: a real scope is built line by line.",
    ("pctded", "codeflag"))

# ------------------------------------------------------------------- 2. BI
BI = _calc(
    "bi", "business interruption calculator",
    (_f("Annual revenue", "revenue", "14500000", "Trailing twelve months for the affected operation.", prefix="$")
     + '<div class="field-row field-row--2">'
     + _f("Gross profit margin", "margin", "38", "Revenue less non-continuing costs.", suffix="%")
     + _f("Continuing expenses", "continuing", "14", "Payroll and fixed costs that ran anyway.", suffix="%")
     + "</div>"
     + '<div class="field-row field-row--2">'
     + _f("Period of restoration", "months", "7", "Months to repair with due diligence.", suffix="mo")
     + _f("Capacity retained", "capacity", "25", "Share of operations still running.", suffix="%")
     + "</div>"
     + '<div class="field-row field-row--2">'
     + _f("Revenue trend", "trend", "4", "Year-on-year growth before the loss.", suffix="%")
     + _f("Waiting period", "waiting", "3", "Days of deductible on the time-element cover.", suffix="days")
     + "</div>"
     + '<div class="field-row field-row--2">'
     + _f("Extra expense incurred", "extra", "420000", "Costs to keep operating or speed repair.", prefix="$")
     + _f("Expenses genuinely saved", "saved", "260000", "Costs that stopped during closure.", prefix="$")
     + "</div>"),
    "Indicated time-element loss", "total",
    "Business income plus extra expense, less saved expenses and the waiting period.",
    (_row("Projected monthly revenue", "monthly")
     + _row("Revenue lost over the period", "lostrev")
     + _row("Lost gross earnings", "gross")
     + _row("Continuing expenses", "cont")
     + _row("Waiting period deduction", "wait")
     + _row("Business income loss", "bi")
     + _row("Extra expense", "extra")
     + _row("Expenses saved", "saved")
     + _row("Indicated loss per day", "perday")
     + _row("Total time-element claim", "total", "outrow--total")),
    "Carriers test the period of restoration harder than any other input here. Change seven months "
    "to five and watch what happens &mdash; that single assumption is usually where the negotiation "
    "actually is.",
    ("longtail",))

# --------------------------------------------------------- 3. coinsurance
COINS = _calc(
    "coinsurance", "coinsurance penalty calculator",
    (_f("Replacement value of the property", "value", "24000000", "What it would cost to rebuild today.", prefix="$")
     + '<div class="field-row field-row--2">'
     + _f("Limit of insurance carried", "carried", "16000000", "From the declarations page.", prefix="$")
     + _f("Coinsurance percentage", "co", "90", "Usually 80, 90 or 100.", suffix="%")
     + "</div>"
     + '<div class="field-row field-row--2">'
     + _f("Amount of the loss", "loss", "3200000", "Before any deductible.", prefix="$")
     + _f("Deductible", "ded", "100000", "Flat amount.", prefix="$")
     + "</div>"),
    "Payable after the penalty", "net",
    "What the policy actually pays once the coinsurance ratio and the deductible are applied.",
    (_row("Insurance required by the clause", "required")
     + _row("Insurance actually carried", "carried")
     + _row("Shortfall", "shortfall")
     + _row("Coinsurance ratio", "ratio")
     + _row("Loss payable before deductible", "payable")
     + _row("Coinsurance penalty", "penalty")
     + _row("Deductible", "ded")
     + _row("Net recovery", "net", "outrow--total")),
    "The formula is the standard one: limit carried divided by limit required, multiplied by the "
    "loss, less the deductible. Agreed value endorsements suspend the clause entirely &mdash; check "
    "your declarations before assuming a penalty applies.",
    ("penalized", "clean"))

# --------------------------------------------------------- 4. depreciation
DEPREC = _calc(
    "depreciation", "RCV and ACV depreciation calculator",
    (_f("Replacement cost of the item or system", "rcv", "1850000", "What it costs to replace today.", prefix="$")
     + '<div class="field-row field-row--2">'
     + _f("Age", "age", "14", "Years in service.", suffix="yrs")
     + _f("Expected service life", "life", "25", "For this system and climate.", suffix="yrs")
     + "</div>"
     + '<div class="field-row field-row--2">'
     + _f("Condition adjustment", "condition", "3", "Years credited back for good maintenance.", suffix="yrs")
     + _f("Deductible", "ded", "50000", "", prefix="$")
     + "</div>"
     + '<div class="field-row field-row--2">'
     + _f("Depreciate labor?", "labor", "yes", "", options=[("yes", "Yes — carrier is depreciating labor"),
                                                             ("no", "No — materials only")])
     + _f("Labor share of cost", "laborshare", "45", "Typical for roofing and finishes.", suffix="%")
     + "</div>"),
    "Recoverable depreciation withheld", "holdback",
    "The amount the carrier holds back until the work is completed and documented.",
    (_row("Replacement cost value", "rcv")
     + _row("Effective age after condition credit", "effage")
     + _row("Depreciation rate", "rate")
     + _row("Depreciable base", "base")
     + _row("Depreciation", "dep")
     + _row("Actual cash value", "acv")
     + _row("Deductible", "ded")
     + _row("First check (ACV)", "first")
     + _row("Held back until completion", "holdback", "outrow--total")),
    "Recoverable depreciation is real money you are owed &mdash; but only if the work is completed "
    "and claimed within the period the policy allows. Diary that deadline the day the first payment "
    "arrives.",
    ("labordep", "bigholdback"))

# ------------------------------------------------------------- 5. deadline
DEADLINE = _calc(
    "deadline", "Texas claim deadline calculator",
    (_f("Date of loss", "loss", "", "The date the damage occurred.", kind="date", step="")
     + _f("Date written notice was given", "notice", "", "Leave blank to use the date of loss.", kind="date", step="")
     + _f("Date you supplied everything the carrier requested", "items", "",
          "Starts the accept-or-reject clock. Leave blank to use the notice date.", kind="date", step="")
     + _f("Suit limitation in your policy", "suit", "2", "Years. Check the wording — some are shorter.", suffix="yrs")),
    "Days since the date of loss", "elapsed",
    "Statutory and policy deadlines calculated from the dates you entered.",
    (_row("Carrier must acknowledge the claim by", "ack")
     + _row("Carrier must accept or reject by", "decide")
     + _row("Payment due by, if accepted", "pay")
     + _row("Earliest suit date if notice given today (61 days)", "presuit")
     + _row("Policy suit limitation expires", "suit")
     + _row("Days remaining", "left", "outrow--total")),
    "Business days exclude weekends but not public holidays, so treat the accept-or-reject and "
    "payment dates as the earliest possible. Deadlines under chapter 542 apply to insurers; an "
    "interlocal risk pool may be governed by its own document instead. Confirm any limitation date "
    "with counsel before relying on it.",
    ("urgent", "expired"))

# ----------------------------------------------------------------- 6. roof
ROOF = _calc(
    "roof", "commercial roof replacement cost estimator",
    (_f("Roof area", "area", "62000", "Square feet, including parapets and overhangs.", suffix="sq ft")
     + '<div class="field-row field-row--2">'
     + _f("Roof system", "system", "11.5", "Installed cost per square foot.",
          options=[("7.5", "Modified bitumen — $7.50/sf"),
                   ("9.0", "Built-up (BUR), 4-ply — $9.00/sf"),
                   ("10.5", "TPO, 60 mil, mechanically attached — $10.50/sf"),
                   ("11.5", "TPO/PVC, 80 mil, fully adhered — $11.50/sf"),
                   ("14.0", "PVC with enhanced warranty — $14.00/sf"),
                   ("19.0", "Standing seam metal — $19.00/sf")])
     + _f("Existing layers to tear off", "layers", "2", "At roughly $1.35/sf per layer.", suffix="layers")
     + "</div>"
     + '<div class="field-row field-row--2">'
     + _f("Insulation upgrade", "insul", "3.2", "Per sq ft, to meet current energy code.", prefix="$")
     + _f("Deck repair", "deck", "8", "Share of deck needing replacement.", suffix="%")
     + "</div>"
     + '<div class="field-row field-row--2">'
     + _f("Perimeter flashing and coping", "flashing", "1400", "Linear feet, at about $28/lf.", suffix="lf")
     + _f("Mechanical curbs and penetrations", "curbs", "34", "Count, at about $850 each.", suffix="each")
     + "</div>"
     + '<div class="field-row field-row--2">'
     + _f("Access and logistics", "access", "8", "Crane, occupied building, night work.", suffix="%")
     + _f("Market adjustment", "market", "6", "Post-catastrophe demand surge.", suffix="%")
     + "</div>"),
    "Estimated replacement cost", "total",
    "Full tear-off and replacement, including overhead and profit at 20%.",
    (_row("Roof area in squares", "squares")
     + _row("Roof system, installed", "field")
     + _row("Tear-off and disposal", "tearoff")
     + _row("Insulation", "insul")
     + _row("Deck repair", "deck")
     + _row("Flashing and coping", "flashing")
     + _row("Curbs and penetrations", "curbs")
     + _row("Access and logistics", "access")
     + _row("Overhead and profit", "oandp")
     + _row("Cost per square foot", "persf")
     + _row("Total estimated cost", "total", "outrow--total")),
    "Unit costs are broad Texas commercial ranges for planning only; a real estimate is built from "
    "a roof survey, a specified assembly and local bids. Energy code frequently requires added "
    "insulation on a full tear-off, which is ordinance and law exposure rather than betterment.",
    ("op",))


# ------------------------------------------------------------------ 7. fee
FEE = _calc(
    "fee", "public adjuster fee and net recovery calculator",
    (_f("Carrier&rsquo;s current offer", "offer", "480000",
        "What is on the table today. Enter 0 if nothing has been offered.", prefix="$")
     + _f("Realistic settlement with representation", "projected", "1150000",
          "Your own estimate, or ours after a scope review.", prefix="$")
     + '<div class="field-row field-row--2">'
     + _f("Fee rate", "rate", "10", "Capped at 10% in Texas.", suffix="%")
     + _f("Prior offer carved out of the fee base?", "carve", "yes", "",
          options=[("yes", "Yes — fee on the improvement only"),
                   ("no", "No — fee on the whole settlement")])
     + "</div>"
     + _f("Third-party costs you pay directly", "costs", "35000",
          "Engineers, forensic accountants, surveys. Not our fee.", prefix="$")),
    "Net in your hands", "net",
    "Settlement less the adjusting fee and any third-party costs you pay directly.",
    (_row("Offer on the table today", "offer")
     + _row("Projected settlement", "projected")
     + _row("Improvement", "uplift")
     + _row("Fee base", "base")
     + _row("Adjusting fee", "fee")
     + _row("Third-party costs", "costs")
     + _row("Net recovery", "net")
     + _row("Break-even settlement", "breakeven")
     + _row("Fee as a share of the improvement", "effective")
     + _row("Net gain versus taking the offer", "gain", "outrow--total")),
    "Texas caps a public adjuster&rsquo;s fee at 10% of the claim settlement under "
    "Tex. Ins. Code &sect;4102.104. Whether an offer already made is carved out of the fee base is "
    "a matter of negotiation, not statute &mdash; which is exactly why it belongs in the "
    "engagement letter.",
    ("carveout", "thin", "worth"))


TOOLS = [
    {
        "slug": "commercial-claim-value-estimator",
        "nav_label": "Claim Value Estimator",
        "card_title": "Commercial claim value estimator",
        "card_blurb": ("Build a planning figure for a large property loss: direct damage, contents, "
                       "code work, depreciation and the deductible."),
        "title": "Commercial Claim Value Estimator | Free Calculator",
        "description": "Estimate a large commercial property claim: replacement cost, contents, code upgrades, depreciation, deductible and recoverable depreciation. Free.",
        "eyebrow": "Tool &middot; Valuation",
        "h1": "Commercial claim<br><em>value</em> estimator",
        "h1_plain": "Commercial claim value estimator",
        "lede": ("A first-order estimate of what a large property loss should be worth, with the "
                 "deductible and the depreciation holdback shown separately &mdash; because the "
                 "check that arrives first is never the whole number."),
        "calc": CLAIM_VALUE,
        "sections": [
            {
                "eyebrow": "Reading the output",
                "h2": "Three numbers, and the gap between them.",
                "blocks": [
                    ("p", "Every replacement cost policy pays a large loss in at least two "
                          "instalments. The first is actual cash value: the cost to repair, less "
                          "depreciation, less the deductible. The second is the recoverable "
                          "depreciation, released after the work is finished and documented. "
                          "Institutions get into trouble when they budget from the first check "
                          "and discover the rebuild costs the full amount."),
                    ("p", "The third number, the one this tool cannot compute, is what the carrier "
                          "will actually offer. That depends on how the scope is documented, "
                          "whether overhead and profit are included, how code upgrades are "
                          "treated and whether anyone has argued for the parts of the building "
                          "the adjuster did not inspect."),
                    ("table", "Where the three numbers diverge", ["Figure", "What it is", "Typical distance from the truth"], [
                        ["Carrier&rsquo;s first estimate", "A template scope produced from a single site visit.", "Usually the lowest number in the file"],
                        ["ACV first payment", "Replacement cost less depreciation less deductible.", "Correct arithmetic on a possibly incorrect scope"],
                        ["Full replacement cost", "What it actually costs to put the building back.", "What the claim should settle at, with documentation"],
                    ]),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "Inputs that matter most",
                "h2": "Two fields move the answer more than the rest combined.",
                "blocks": [
                    ("checks", [
                        "<strong>Replacement cost per square foot.</strong> Using an outdated figure understates everything downstream, including the coinsurance test. Current Texas commercial construction costs vary enormously by occupancy &mdash; a warehouse shell and a hospital wing are not comparable.",
                        "<strong>Deductible basis.</strong> A flat $50,000 and a 2% of values deductible look similar in a conversation and are wildly different in a claim. Switch the selector and watch the bottom line move.",
                        "<strong>Code upgrade percentage.</strong> On any building older than about twenty years, this is real and frequently substantial. It is also capped by your ordinance and law limit, which is often far lower than the exposure.",
                        "<strong>Service life.</strong> Depreciation is straight-line here. Real adjusters argue effective age against condition, and a well-maintained system deserves credit for it.",
                    ]),
                ],
            },
        ],
        "faqs": [
            ("Is this an appraisal?",
             "<p>No. It is arithmetic applied to assumptions you supplied. A real estimate is built "
             "from a measured survey, a line-item scope, current local unit costs and the specific "
             "wording of your policy. Use this to work out whether the number on your desk is "
             "plausible, then have the loss scoped properly.</p>"),
            ("Why is recoverable depreciation shown separately?",
             "<p>Because it is the part people forget. On a replacement cost policy the carrier "
             "pays actual cash value first and releases the remainder once repairs are complete "
             "and invoiced. That release is time-limited under most policies. If you never "
             "complete the work, or you miss the deadline, that money stays with the insurer.</p>"),
            ("Does this store anything we enter?",
             "<p>No. It runs entirely in your browser. Nothing is transmitted, logged or saved, "
             "and closing the tab discards it. Use the copy or print button if you want a record.</p>"),
        ],
    },
    {
        "slug": "business-interruption-calculator",
        "nav_label": "Business Interruption Calculator",
        "card_title": "Business interruption calculator",
        "card_blurb": ("Model lost gross earnings, continuing expenses, extra expense and the "
                       "waiting period over a period of restoration."),
        "title": "Business Interruption Calculator | Commercial BI Loss",
        "description": "Free business interruption calculator for commercial claims. Model lost gross earnings, continuing expenses, extra expense and the waiting period.",
        "eyebrow": "Tool &middot; Time element",
        "h1": "Business interruption<br>loss <em>calculator</em>",
        "h1_plain": "Business interruption calculator",
        "lede": ("Time-element losses are argued in six variables. Change any one of them and the "
                 "answer moves substantially, which is exactly why carriers spend so much effort "
                 "on the period of restoration."),
        "calc": BI,
        "sections": [
            {
                "eyebrow": "The formula",
                "h2": "What a business income claim is, arithmetically.",
                "blocks": [
                    ("p", "Business income coverage pays the net profit the operation would have "
                          "earned plus the continuing normal operating expenses it had to keep "
                          "paying. It does not pay lost turnover, which is the mistake most "
                          "first-draft claims make, and it does not pay expenses that stopped."),
                    ("p", "Expressed plainly: project the revenue, apply the margin, add back what "
                          "kept running, subtract what stopped, add the extra expense you incurred "
                          "to limit the damage, and deduct the waiting period. Every one of those "
                          "steps is contestable and every one has a documentary answer."),
                    ("callout", "Extra expense is the lever", [
                        ("p", "Money spent to keep operating &mdash; temporary premises, expedited "
                              "freight, overtime, rented equipment, accelerated construction "
                              "&mdash; is generally recoverable where it reduces the overall loss. "
                              "It also demonstrates mitigation, which strengthens the rest of the "
                              "claim. Spend deliberately, and document as you go."),
                    ]),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "Pitfalls",
                "h2": "Four assumptions that get attacked.",
                "blocks": [
                    ("table", "Where the carrier&rsquo;s accountant will push", ["Assumption", "Their argument", "Your answer"], [
                        ["Revenue trend", "The growth you projected would not have continued.", "Multi-year trend, booked orders, market or competitive-set benchmark data"],
                        ["Period of restoration", "The rebuild should have taken less time.", "Dated construction schedule with the cause of every variance recorded"],
                        ["Continuing expenses", "You should have furloughed or cut.", "Contractual obligations, retention rationale, and the cost of losing trained staff"],
                        ["Saved expenses", "More was saved than you have credited.", "Departmental accounts showing what actually stopped and what did not"],
                    ]),
                ],
            },
        ],
        "faqs": [
            ("What margin should we use?",
             "<p>Gross profit as your accounts define it is a reasonable starting point, but the "
             "policy&rsquo;s own definition governs. Some forms use a gross earnings definition "
             "that deducts only specified costs; others use net profit plus continuing expenses. "
             "Read the definition before you build the model &mdash; it is usually on the first "
             "page of the time-element form.</p>"),
            ("Does this work for a nonprofit or a public entity?",
             "<p>Yes, with a translation. Substitute the interrupted income stream &mdash; tuition, "
             "program fees, rentals, dining, tithes and offerings, event income &mdash; for "
             "revenue, and use the contribution margin for that activity. The arithmetic is "
             "identical; the vocabulary in the policy is what changes.</p>"),
            ("Our operation never fully closed. Is there still a claim?",
             "<p>Usually. Partial interruption is the normal case, not the exception. Set the "
             "capacity retained field to the share of operations that kept running and the model "
             "will scale the loss accordingly. Proving the partial figure takes more documentation "
             "than proving a total closure, not less.</p>"),
        ],
    },
    {
        "slug": "coinsurance-penalty-calculator",
        "nav_label": "Coinsurance Penalty Calculator",
        "card_title": "Coinsurance penalty calculator",
        "card_blurb": ("Find out whether your limit satisfies the coinsurance clause &mdash; and "
                       "what the shortfall costs on every claim, not just a total loss."),
        "title": "Coinsurance Penalty Calculator | Commercial Property",
        "description": "Calculate the coinsurance penalty on a commercial property claim. Enter your limit, the property value, the coinsurance percentage and the loss.",
        "eyebrow": "Tool &middot; Underinsurance",
        "h1": "Coinsurance<br>penalty <em>calculator</em>",
        "h1_plain": "Coinsurance penalty calculator",
        "lede": ("The most expensive clause in commercial property insurance is one that almost "
                 "nobody reads. It reduces every covered loss by the ratio of the limit you bought "
                 "to the limit you should have bought &mdash; and it applies to a small claim just "
                 "as ruthlessly as to a large one."),
        "calc": COINS,
        "sections": [
            {
                "eyebrow": "The mechanism",
                "h2": "It is a penalty for under-reporting, not for under-claiming.",
                "blocks": [
                    ("p", "Insurers price property cover on the values you report. If everybody "
                          "reported half their value and bought half the limit, the premium pool "
                          "would collapse, because most losses are partial. The coinsurance clause "
                          "exists to prevent that: carry at least the stated percentage of "
                          "replacement value, or every claim is reduced proportionally."),
                    ("p", "Two things make it dangerous in practice. Values drift &mdash; "
                          "construction costs in Texas have moved sharply since most statements of "
                          "value were assembled, and few institutions revalue annually. And the "
                          "test is applied at the time of loss, using the value then, not the "
                          "value when the policy was written."),
                    ("html", '<a class="tlink" href="/services/policy-review-and-pre-loss-consulting/">'
                             'Have the schedule reviewed before renewal <span class="arw">&rarr;</span></a>'),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "The fix",
                "h2": "Three ways out, in order of preference.",
                "blocks": [
                    ("steps", [
                        ("Agreed value endorsement",
                         "<p>Suspends the coinsurance clause for the policy term in exchange for "
                         "a signed statement of values. The cleanest solution available and "
                         "frequently cheaper than people expect. Check your declarations &mdash; "
                         "you may already have it and not know.</p>"),
                        ("Revalue the schedule",
                         "<p>A professional valuation, or at minimum a current cost-per-square-foot "
                         "review by occupancy and construction class. Then raise the limits to "
                         "match. Uncomfortable at renewal; considerably less uncomfortable than "
                         "the alternative.</p>"),
                        ("Argue the value at claim time",
                         "<p>The last resort, and a real one. The required amount depends on the "
                         "property&rsquo;s value at the date of loss, and that figure is a matter "
                         "of evidence rather than the carrier&rsquo;s assertion. Where a penalty "
                         "is being applied on an inflated valuation, it is contestable.</p>"),
                    ]),
                ],
            },
        ],
        "faqs": [
            ("Does the penalty apply to total losses?",
             "<p>Generally no, in effect: coinsurance limits recovery to the ratio applied to the "
             "loss, but recovery is also capped at the policy limit, and on a total loss the limit "
             "usually bites first. The clause hurts most on partial losses, which is the "
             "overwhelming majority of claims.</p>"),
            ("How do we know if we have a coinsurance clause?",
             "<p>Look at the declarations page next to each building&rsquo;s limit. You will "
             "normally see 80%, 90% or 100%, or the words agreed value. If a percentage is shown, "
             "the clause is live. If the schedule says agreed value, it is suspended for the term "
             "&mdash; but check that the signed statement of values is current, because that is "
             "the condition.</p>"),
            ("Our broker says we are fine. Should we check anyway?",
             "<p>Yes, with numbers rather than reassurance. Construction costs in Texas have moved "
             "substantially, and a schedule that satisfied a 90% requirement four years ago may not "
             "now. The test costs ten minutes on this page and a current cost-per-square-foot "
             "figure for your construction class.</p>"),
        ],
    },
    {
        "slug": "rcv-acv-depreciation-calculator",
        "nav_label": "RCV / ACV Depreciation Calculator",
        "card_title": "RCV vs ACV depreciation calculator",
        "card_blurb": ("See exactly how much of your claim is being held back as recoverable "
                       "depreciation &mdash; and whether labor is being depreciated."),
        "title": "RCV vs ACV Calculator | Recoverable Depreciation",
        "description": "Calculate actual cash value, depreciation and recoverable depreciation on a commercial insurance claim, including whether labor is being depreciated.",
        "eyebrow": "Tool &middot; Valuation",
        "h1": "RCV, ACV and the<br><em>holdback</em>",
        "h1_plain": "RCV vs ACV depreciation calculator",
        "lede": ("The difference between replacement cost and actual cash value is depreciation, "
                 "and on a replacement cost policy most of it is yours &mdash; later, conditionally, "
                 "and only if somebody tracks the deadline."),
        "calc": DEPREC,
        "sections": [
            {
                "eyebrow": "Definitions",
                "h2": "Four terms that decide the size of the first check.",
                "blocks": [
                    ("table", "The vocabulary", ["Term", "What it means"], [
                        ["Replacement cost value (RCV)", "What it costs today to repair or replace with materials of like kind and quality, without deduction for depreciation."],
                        ["Actual cash value (ACV)", "Replacement cost less depreciation. In Texas this is commonly computed as replacement cost less depreciation, though some wording contemplates a fair-market or broad-evidence approach."],
                        ["Recoverable depreciation", "The withheld difference, released once the work is actually completed and documented within the policy&rsquo;s time limit."],
                        ["Non-recoverable depreciation", "Depreciation you never get back &mdash; the position on an ACV-only policy, or on roof surfacing under an actual cash value roof endorsement."],
                    ]),
                    ("callout", "Check for an ACV roof endorsement", [
                        ("p", "A growing number of Texas commercial policies pay roof surfacing on "
                              "an actual cash value basis regardless of the rest of the building. "
                              "On a 20-year-old roof that endorsement can remove most of the "
                              "claim, and it is easy to miss on a declarations page. Look for "
                              "wording about roof surfacing, cosmetic damage or a roof schedule."),
                    ]),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "Arguing it",
                "h2": "Depreciation is an opinion presented as a calculation.",
                "blocks": [
                    ("p", "The software produces a number, which makes it look objective. It is "
                          "not. Effective age, remaining service life and condition are judgment "
                          "calls, and a roof that has been maintained, inspected and kept under "
                          "warranty is not in the same condition as one of identical age that has "
                          "never been touched. Documentation shifts that judgment."),
                    ("checks", [
                        "Maintenance records, inspection reports and warranty status for the affected system.",
                        "Manufacturer statements on expected service life for that specific assembly in this climate.",
                        "Evidence of recent partial replacement or refurbishment, which resets effective age for those sections.",
                        "The policy&rsquo;s valuation wording &mdash; whether it permits depreciation of labor at all is a wording question, not a software setting.",
                        "The deadline for claiming recoverable depreciation, diarised from the date of the first payment.",
                    ]),
                ],
            },
        ],
        "faqs": [
            ("Can insurers depreciate labor in Texas?",
             "<p>It is contested and it turns on the policy language. Estimating software will "
             "depreciate labor by default, and many adjusters never change the setting. The "
             "argument against is straightforward &mdash; labor is consumed when performed and "
             "does not deteriorate &mdash; and on a large claim the sums involved justify making "
             "it. Where the wording is ambiguous, that ambiguity is generally construed against "
             "the insurer, which is a question for counsel rather than for us.</p>"),
            ("How long do we have to claim recoverable depreciation?",
             "<p>Whatever the policy says, commonly 180 days or two years from the date of loss, "
             "and sometimes measured from the ACV payment instead. It is one of the most "
             "frequently missed deadlines in commercial property insurance. Find the provision, "
             "write the date in a calendar, and ask for an extension in writing if the rebuild is "
             "going to run past it &mdash; carriers routinely grant them and rarely volunteer them.</p>"),
            ("Is a condition adjustment a real thing or are we inventing it?",
             "<p>It is real and standard practice. Adjusters assess effective age rather than "
             "chronological age precisely because maintenance matters. What makes it persuasive is "
             "evidence: service records, photographs, inspection reports. Asserting good condition "
             "without documentation rarely moves a number.</p>"),
        ],
    },
    {
        "slug": "texas-claim-deadline-calculator",
        "nav_label": "Texas Claim Deadline Calculator",
        "card_title": "Texas claim deadline calculator",
        "card_blurb": ("Date the statutory clock on a Texas claim: acknowledgement, "
                       "accept-or-reject, payment, pre-suit notice and the limitation period."),
        "title": "Texas Claim Deadline Calculator | Chapter 542",
        "description": "Calculate Texas insurance claim deadlines: the 15-day acknowledgement, 15 business day accept-or-reject, 5 business day payment and the suit limitation.",
        "eyebrow": "Tool &middot; Statutory clock",
        "h1": "Texas claim<br><em>deadline</em> calculator",
        "h1_plain": "Texas claim deadline calculator",
        "lede": ("Chapter 542 of the Texas Insurance Code puts deadlines on insurers, and chapter "
                 "542A puts a notice requirement on you. Enter three dates and see where your "
                 "claim actually sits."),
        "calc": DEADLINE,
        "sections": [
            {
                "eyebrow": "The statute",
                "h2": "What the prompt payment provisions require.",
                "blocks": [
                    ("p", "Subchapter B of chapter 542 &mdash; the Prompt Payment of Claims Act "
                          "&mdash; sets out a sequence. On receiving written notice of a claim the "
                          "insurer must acknowledge it, commence an investigation and request the "
                          "items it reasonably requires, generally within 15 days. Once it has "
                          "what it asked for, it must notify you in writing whether the claim is "
                          "accepted or rejected, generally within 15 business days. If accepted, "
                          "payment is due within 5 business days of that notice."),
                    ("p", "Missing those deadlines exposes an insurer to statutory interest on the "
                          "amount of the claim plus reasonable attorney&rsquo;s fees. The rate and "
                          "its calculation differ depending on when the claim arose and whether it "
                          "falls under chapter 542A, which covers claims arising from forces of "
                          "nature such as wind, hail and rain. That is a question for a lawyer, "
                          "and it is one worth asking."),
                    ("callout", "Chapter 542A pre-suit notice", [
                        ("p", "For most weather-related claims, a claimant must give the insurer "
                              "written notice at least 61 days before filing suit, stating the "
                              "acts complained of, the amount alleged to be owed and the "
                              "attorney&rsquo;s fees incurred. The insurer may then demand an "
                              "inspection. Get this wrong and the consequences reach attorney&rsquo;s "
                              "fees and, in some circumstances, abatement of the suit."),
                    ]),
                ],
            },
            {
                "band": "ink",
                "eyebrow": "Caveats",
                "h2": "Three reasons not to rely on this page alone.",
                "blocks": [
                    ("checks", [
                        "<strong>Business days are approximated.</strong> The calculator excludes weekends but not public holidays, so treat the accept-or-reject and payment dates as the earliest possible.",
                        "<strong>Risk pools may not be covered.</strong> If your coverage is through an interlocal risk pool rather than an insurer, chapter 542 may not apply in the same way. The coverage document&rsquo;s own procedures govern.",
                        "<strong>Limitation periods are legal questions.</strong> Policy wording, when the cause of action accrued, tolling and chapter 542A all affect the real deadline. Confirm it with counsel before relying on any date shown here.",
                    ]),
                ],
            },
        ],
        "faqs": [
            ("When does the clock actually start?",
             "<p>On written notice of the claim, not on the date of the damage. That is why the "
             "calculator asks for both. Giving clear written notice, keeping proof of when it was "
             "sent, and responding promptly to the carrier&rsquo;s requests for information are "
             "the three things that keep the statutory timeline working for you rather than "
             "against you.</p>"),
            ("The carrier keeps asking for more documents. Does that reset the deadline?",
             "<p>It can extend the practical timeline, because the accept-or-reject clock runs from "
             "when the insurer receives all items it reasonably requested. Repeated, escalating or "
             "unreasonable requests are a recognized delay tactic. The answer is to respond fully "
             "and in writing, log every request and every response with dates, and create a record "
             "that shows when the carrier actually had everything it needed.</p>"),
            ("We are past a deadline. Is the claim dead?",
             "<p>Not necessarily, and do not assume it is. Notice requirements, limitation periods "
             "and prejudice all interact, and the outcome depends on facts. What is certain is that "
             "delay never improves the position. If a date on this page has passed, that is a "
             "reason to speak to a lawyer this week.</p>"),
        ],
    },
    {
        "slug": "commercial-roof-replacement-cost-estimator",
        "nav_label": "Roof Replacement Cost Estimator",
        "card_title": "Commercial roof replacement estimator",
        "card_blurb": ("Price a full commercial tear-off and re-roof by system, including "
                       "insulation, deck, flashing, curbs and overhead and profit."),
        "title": "Commercial Roof Replacement Cost Estimator | Texas",
        "description": "Estimate the cost to replace a commercial roof in Texas: TPO, PVC, modified bitumen, built-up and standing seam metal, with tear-off and insulation.",
        "eyebrow": "Tool &middot; Roofing",
        "h1": "Commercial roof<br>replacement <em>estimator</em>",
        "h1_plain": "Commercial roof replacement cost estimator",
        "lede": ("Before you can argue about whether a hail-damaged roof is repairable, you need a "
                 "credible replacement number. This prices a full tear-off by system, with the "
                 "line items carriers most often leave out shown separately."),
        "calc": ROOF,
        "sections": [
            {
                "eyebrow": "Systems",
                "h2": "What each assembly costs, and how each one fails.",
                "blocks": [
                    ("table", "Commercial roof systems in Texas", ["System", "Indicative installed cost", "Typical service life", "How hail shows up"], [
                        ["Modified bitumen", "~$7&ndash;9/sf", "~15&ndash;20 yrs", "Granule loss, bruising and fracture of the cap sheet; damage often only visible in a test cut"],
                        ["Built-up (BUR)", "~$8&ndash;11/sf", "~20&ndash;25 yrs", "Displaced gravel, fractured felts, bruised membrane beneath the aggregate"],
                        ["TPO, mechanically attached", "~$9&ndash;12/sf", "~18&ndash;25 yrs", "Punctures over fastener plates, membrane bruising, seam stress"],
                        ["PVC / TPO fully adhered", "~$11&ndash;15/sf", "~20&ndash;30 yrs", "Impact fracture of the insulation board beneath an intact membrane"],
                        ["Standing seam metal", "~$16&ndash;22/sf", "~30&ndash;45 yrs", "Denting and coating damage; the cosmetic-versus-functional argument lives here"],
                    ]),
                    ("p", "Costs move with steel and resin prices, with labor availability after a "
                          "catastrophe, and with how difficult the building is to work on. An "
                          "occupied hospital roof with limited crane access and night-only work is "
                          "not the same job as an empty warehouse, and the estimate should say so "
                          "in the access line rather than hiding it in the unit price."),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "Disputes",
                "h2": "Four line items the carrier will try to remove.",
                "blocks": [
                    ("checks", [
                        "<strong>Overhead and profit.</strong> A commercial re-roof involves roofing, sheet metal, mechanical disconnect and reconnect, electrical, and often structural work. That is the multi-trade test for a general contractor, and it is worth 20% of the job.",
                        "<strong>Insulation to current code.</strong> A full tear-off usually triggers current energy code R-values, which can mean thicker insulation than what was there. That is ordinance and law exposure, not an upgrade you chose.",
                        "<strong>Tapered and crickets.</strong> Where drainage does not meet current requirements, the replacement has to fix it. Carriers price a flat replacement of what existed.",
                        "<strong>Mechanical curbs and raising units.</strong> Thicker insulation means curbs must be extended and units lifted and reset. It is a real cost and almost never in the first estimate.",
                    ]),
                ],
            },
        ],
        "faqs": [
            ("Should a damaged commercial roof be repaired or replaced?",
             "<p>The test is whether repair restores the roof to its pre-loss condition and service "
             "life. Scattered punctures on a young membrane can be repaired. Widespread impact "
             "damage to insulation beneath a membrane cannot be patched back to a warrantable "
             "system, and manufacturers will frequently say so in writing &mdash; which is the "
             "document that settles the argument.</p>"),
            ("Why does overhead and profit matter so much on a roof claim?",
             "<p>Because it is 20% of a large number and it is removed silently. The usual carrier "
             "position is that O&amp;P is owed only when a general contractor is actually engaged. "
             "The more common standard is whether one is reasonably likely to be needed, and the "
             "rule of thumb is three or more trades. A commercial re-roof almost always clears "
             "that.</p>"),
            ("Our roof has two layers already. Does that change anything?",
             "<p>Yes, in two ways. Tear-off cost roughly doubles, and most jurisdictions will not "
             "permit a third layer, so a recover is off the table. Both points strengthen a "
             "replacement argument and both should be priced explicitly rather than absorbed.</p>"),
        ],
    },
    {
        "slug": "public-adjuster-fee-calculator",
        "nav_label": "Fee &amp; Net Recovery Calculator",
        "card_title": "Public adjuster fee &amp; net recovery",
        "card_blurb": ("Work out whether representation actually pays &mdash; net gain, break-even "
                       "settlement, and the fee as a share of the improvement."),
        "title": "Public Adjuster Fee Calculator | Net Recovery",
        "description": "Calculate what a public adjuster costs and whether it pays: net recovery after the fee, break-even settlement and the fee as a share of the improvement.",
        "eyebrow": "Tool &middot; Engagement economics",
        "h1": "Does representation<br>actually <em>pay</em>?",
        "h1_plain": "Public adjuster fee and net recovery calculator",
        "lede": ("It is the first question every board, council and finance committee asks, and it "
                 "deserves a number rather than a reassurance. Put your figures in and see the "
                 "break-even point &mdash; including the cases where the answer is no."),
        "calc": FEE,
        "sections": [
            {
                "eyebrow": "The economics",
                "h2": "The only question that matters is the net, not the fee.",
                "blocks": [
                    ("p", "A 10% fee on a settlement that doubles is a bargain. The same fee on a "
                          "claim that was already correctly adjusted is a straight loss. Both "
                          "happen, and an honest firm will tell you which one you are looking at "
                          "before you sign anything rather than afterwards."),
                    ("p", "Two structural details decide most of it. The first is whether an offer "
                          "already made is carved out of the fee base &mdash; if the carrier has "
                          "put $480,000 on the table before we are engaged, charging a percentage "
                          "of that is charging for work nobody did. The second is who pays for "
                          "engineers, forensic accountants and specialist surveys, which on a "
                          "large institutional file can run into real money and are usually the "
                          "client&rsquo;s direct cost."),
                    ("p", "Both belong in the engagement letter in plain language. If a firm will "
                          "not put the carve-out in writing, that tells you something useful at no "
                          "cost."),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "What the law says",
                "h2": "Texas caps the fee, and regulates the contract.",
                "blocks": [
                    ("table", "Fee rules under chapter 4102", ["Provision", "What it requires"], [
                        ["Fee cap", "A public insurance adjuster&rsquo;s compensation may not exceed 10% of the amount of the claim settlement (Tex. Ins. Code &sect;4102.104)."],
                        ["Written contract", "The engagement must be in writing, signed, and must state the services and the compensation."],
                        ["Licensing", "Public adjusters must be licensed by the Texas Department of Insurance and may not act as a contractor on the same loss."],
                        ["No conflicted interest", "A public adjuster may not participate directly or indirectly in the reconstruction or repair of the damaged property they adjusted."],
                        ["Cancellation", "Statute and the contract provide a period in which the insured may cancel the engagement. Read that clause before you sign."],
                    ]),
                    ("callout", "The conflict rule is a feature", [
                        ("p", "The prohibition on adjusting and repairing the same loss is the "
                              "reason to use a licensed public adjuster rather than a contractor "
                              "who offers to handle your claim. A roofer whose fee is the roof has "
                              "an interest in the scope. We have an interest in the number, and "
                              "you pick the contractor."),
                    ]),
                ],
            },
        ],
        "faqs": [
            ("Is the 10% cap per claim or per payment?",
             "<p>The statutory limit is expressed against the amount of the claim settlement. The "
             "practical questions &mdash; whether the base includes an offer already made, how "
             "supplements are treated, and what happens if you settle part of the claim without us "
             "&mdash; are matters for the engagement letter. Get them written down before work "
             "starts.</p>"),
            ("What if you recover nothing?",
             "<p>Then there is no fee. Third-party costs you authorised directly &mdash; an "
             "engineer, a forensic accountant &mdash; are a separate matter and are normally your "
             "cost regardless, which is why we discuss each one before it is incurred rather than "
             "presenting a bill at the end.</p>"),
            ("Would you ever tell us not to hire you?",
             "<p>Regularly. If the carrier&rsquo;s estimate is broadly right, if the loss will not "
             "clear the deductible, or if the real problem is a coverage denial that needs a lawyer "
             "rather than an adjuster, the honest answer is that we would be taking a fee for very "
             "little. Run the numbers on this page. If the net gain is thin, say so when you call "
             "and we will tell you plainly what we think.</p>"),
        ],
    },
]

for _t in TOOLS:
    _t["path"] = "/tools/%s/" % _t["slug"]
