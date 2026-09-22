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
     + _f("Expenses saved", "saved", "260000", "Costs that stopped during closure.", prefix="$")
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
    "to five and watch what happens. That single assumption is usually where the negotiation "
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
    "What the policy pays once the coinsurance ratio and the deductible are applied.",
    (_row("Insurance required by the clause", "required")
     + _row("Insurance carried", "carried")
     + _row("Shortfall", "shortfall")
     + _row("Coinsurance ratio", "ratio")
     + _row("Loss payable before deductible", "payable")
     + _row("Coinsurance penalty", "penalty")
     + _row("Deductible", "ded")
     + _row("Net recovery", "net", "outrow--total")),
    "The formula is the standard one: limit carried divided by limit required, multiplied by the "
    "loss, less the deductible. Agreed value endorsements suspend the clause &mdash; check "
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
    "Recoverable depreciation is real money you are owed, but only if the work is completed "
    "and claimed within the period the policy allows. Diary that deadline the day the first payment "
    "arrives.",
    ("labordep", "bigholdback"))

# -------------------------------------------------------------- 5. cabinets
CABINET = _calc(
    "cabinet", "cabinet repair versus replace calculator",
    (_f("Cabinet boxes in the run", "total", "34", "Total boxes in the continuous installation.", suffix="boxes")
     + '<div class="field-row field-row--2">'
     + _f("Boxes affected", "damaged", "19", "Showing moisture, swelling or finish damage.", suffix="boxes")
     + _f("Assessed repairable", "repairable", "8", "Sound substrate, intact joints.", suffix="boxes")
     + "</div>"
     + '<div class="field-row field-row--2">'
     + _f("Refinish cost per box", "refinish", "185", "Clean, seal and refinish in place.", prefix="$")
     + _f("Replacement cost per box", "replace", "640", "Installed, including demolition.", prefix="$")
     + "</div>"
     + '<div class="field-row field-row--2">'
     + _f("Countertop replacement", "tops", "4200", "Tops rarely survive box removal.", prefix="$")
     + _f("Door profile still available?", "matching", "no", "",
          options=[("yes", "Yes — matching boxes can be sourced"),
                   ("no", "No — line or profile discontinued")])
     + "</div>"),
    "Indicated scope cost", "partial",
    "The partial-repair path: refinishing what is sound, replacing what is not.",
    (_row("Boxes affected", "damaged")
     + _row("Repairable", "repairable")
     + _row("Actually refinished", "refinished")
     + _row("Not repairable", "notrepairable")
     + _row("Boxes in the replacement scope", "partialboxes")
     + _row("Refinishing", "partialrefinish")
     + _row("Replacement boxes", "partialreplace")
     + _row("Countertops", "partialtops")
     + _row("Partial path total", "partial")
     + _row("Full replacement", "full")
     + _row("Partial as a share of full", "ratio")
     + _row("Saving against full replacement", "saving", "outrow--total")),
    "Repairability is a substrate and moisture finding, not a visual one: particleboard and MDF "
    "do not recover from sustained wetting, and plywood boxes with solid face frames often do. "
    "Enter the repairable count from an actual assessment rather than an impression.",
    ("nomatch", "threshold", "worthit"))

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
    "a roof survey, a specified assembly and local bids. Energy code often requires added "
    "insulation on a full tear-off, which is ordinance and law exposure instead of betterment.",
    ("op",))


# ----------------------------------------------------------------- 7. O&P
OANDP = _calc(
    "oandp", "overhead, profit and general conditions calculator",
    (_f("Direct trade cost", "direct", "2400000",
        "The line-item repair cost before markups.", prefix="$")
     + '<div class="field-row field-row--2">'
     + _f("Trades on the scope", "trades", "6", "Roofing, framing, MEP, finishes, and so on.", suffix="trades")
     + _f("Construction duration", "months", "9", "For the general conditions test.", suffix="mo")
     + "</div>"
     + '<div class="field-row field-row--2">'
     + _f("Occupied-building premium", "occupancy", "8",
          "Night work, phasing, protection, noise and dust control.", suffix="%")
     + _f("Building occupied during work?", "occupied", "yes", "",
          options=[("yes", "Yes — apply the premium"), ("no", "No — vacant")])
     + "</div>"
     + '<div class="field-row field-row--2">'
     + _f("General conditions", "gc", "9", "Supervision, temporary utilities, logistics.", suffix="%")
     + _f("Payment &amp; performance bond", "bond", "1.2", "Common on public work.", suffix="%")
     + "</div>"
     + '<div class="field-row field-row--2">'
     + _f("Contractor overhead", "overhead", "10", "Conventionally 10%.", suffix="%")
     + _f("Contractor profit", "profit", "10", "Conventionally 10%.", suffix="%")
     + "</div>"),
    "Total with markups", "total",
    "Direct cost plus access premium, general conditions, overhead, profit and bond.",
    (_row("Direct trade cost", "direct")
     + _row("Occupied-building premium", "access")
     + _row("Adjusted direct cost", "base")
     + _row("General conditions", "gc")
     + _row("General conditions per month", "gcmo")
     + _row("Subtotal before O&amp;P", "subtotal")
     + _row("Overhead", "overhead")
     + _row("Profit", "profit")
     + _row("Combined O&amp;P rate", "combined")
     + _row("Bond", "bond")
     + _row("Total", "total", "outrow--total")),
    "Ten and ten is a convention, not a rule, and general conditions are a schedule-driven cost "
    "instead of a percentage anyone should accept without testing. This models the standard "
    "treatment so both the figure and the assumptions behind it are visible.",
    ("trades", "fewtrades", "gcflag"))


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
                 "deductible and the depreciation holdback shown separately, because the "
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
                          "will offer. That depends on how the scope is documented, "
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
                        "<strong>Replacement cost per square foot.</strong> Using an outdated figure understates everything downstream, including the coinsurance test. Current Texas commercial construction costs vary enormously by occupancy, a warehouse shell and a hospital wing are not comparable.",
                        "<strong>Deductible basis.</strong> A flat $50,000 and a 2% of values deductible look similar in a conversation and are wildly different in a claim. Switch the selector and watch the bottom line move.",
                        "<strong>Code upgrade percentage.</strong> On any building older than about twenty years, this is real and often substantial. It is also capped by your ordinance and law limit, which is often far lower than the exposure.",
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
                        ("p", "Money spent to keep operating, temporary premises, expedited "
                              "freight, overtime, rented equipment, accelerated construction"
                              ", is generally recoverable where it reduces the overall loss. "
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
                        ["Saved expenses", "More was saved than you have credited.", "Departmental accounts showing what stopped and what did not"],
                    ]),
                ],
            },
        ],
        "faqs": [
            ("What margin should we use?",
             "<p>Gross profit as your accounts define it is a reasonable starting point, but the "
             "policy&rsquo;s own definition governs. Some forms use a gross earnings definition "
             "that deducts only specified costs; others use net profit plus continuing expenses. "
             "Read the definition before you build the model. It is usually on the first "
             "page of the time-element form.</p>"),
            ("Does this work for a nonprofit or a public entity?",
             "<p>Yes, with a translation. Substitute the interrupted income stream &mdash; tuition, "
             "program fees, rentals, dining, tithes and offerings, event income, for "
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
        "card_blurb": ("Find out whether your limit satisfies the coinsurance clause, and "
                       "what the shortfall costs on every claim, not just a total loss."),
        "title": "Coinsurance Penalty Calculator | Commercial Property",
        "description": "Calculate the coinsurance penalty on a commercial property claim. Enter your limit, the property value, the coinsurance percentage and the loss.",
        "eyebrow": "Tool &middot; Underinsurance",
        "h1": "Coinsurance<br>penalty <em>calculator</em>",
        "h1_plain": "Coinsurance penalty calculator",
        "lede": ("The most expensive clause in commercial property insurance is one that almost "
                 "nobody reads. It reduces every covered loss by the ratio of the limit you bought "
                 "to the limit you should have bought, and it applies to a small claim just "
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
                    ("p", "Two things make it dangerous in practice. Values drift, "
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
                         "usually cheaper than people expect. Check your declarations. "
                         "You may already have it and not know.</p>"),
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
             "the clause is live. If the schedule says agreed value, it is suspended for the term"
             ", but check that the signed statement of values is current, because that is "
             "the condition.</p>"),
            ("Our broker says we are fine. Should we check anyway?",
             "<p>Yes, with numbers instead of reassurance. Construction costs in Texas have moved "
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
                       "depreciation, and whether labor is being depreciated."),
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
                        ["Recoverable depreciation", "The withheld difference, released once the work is completed and documented within the policy&rsquo;s time limit."],
                        ["Non-recoverable depreciation", "Depreciation you never get back, the position on an ACV-only policy, or on roof surfacing under an actual cash value roof endorsement."],
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
                        "The policy&rsquo;s valuation wording, whether it permits depreciation of labor at all is a wording question, not a software setting.",
                        "The deadline for claiming recoverable depreciation, diarised from the date of the first payment.",
                    ]),
                ],
            },
        ],
        "faqs": [
            ("Can insurers depreciate labor in Texas?",
             "<p>It is contested and it turns on the policy language. Estimating software will "
             "depreciate labor by default, and many adjusters never change the setting. The "
             "argument against is straightforward, labor is consumed when performed and "
             "does not deteriorate, and on a large claim the sums involved justify making "
             "it. Where the wording is ambiguous, that ambiguity is generally construed against "
             "the insurer, which is a question for counsel instead of for us.</p>"),
            ("How long do we have to claim recoverable depreciation?",
             "<p>Whatever the policy says, commonly 180 days or two years from the date of loss, "
             "and sometimes measured from the ACV payment instead. It is one of the most "
             "often missed deadlines in commercial property insurance. Find the provision, "
             "write the date in a calendar, and ask for an extension in writing if the rebuild is "
             "going to run past it &mdash; carriers regularly grant them and rarely volunteer them.</p>"),
            ("Is a condition adjustment a real thing or are we inventing it?",
             "<p>It is real and standard practice. Adjusters assess effective age rather than "
             "chronological age precisely because maintenance matters. What makes it persuasive is "
             "evidence: service records, photographs, inspection reports. Asserting good condition "
             "without documentation rarely moves a number.</p>"),
        ],
    },
    {
        "slug": "cabinet-repair-vs-replace-calculator",
        "nav_label": "Cabinet Repair vs Replace",
        "card_title": "Cabinet repair vs replace calculator",
        "card_blurb": ("Compare refinishing against replacement across a run, including what a "
                       "discontinued door profile does to the scope."),
        "title": "Cabinet Repair vs Replace Calculator | Casework Scope",
        "description": ("Compare partial cabinet repair against full replacement: refinishing, "
                        "replacement boxes, countertops, and the effect of a discontinued door "
                        "profile on the scope."),
        "eyebrow": "Tool &middot; Casework",
        "h1": "Cabinet repair<br>versus <em>replace</em>",
        "h1_plain": "Cabinet repair vs replace calculator",
        "lede": ("The argument is rarely about the unit costs. It is about how many boxes are "
                 "repairable and whether the ones that are not can be matched, "
                 "and those two inputs move the answer far more than any price does."),
        "calc": CABINET,
        "sections": [
            {
                "eyebrow": "The two inputs that matter",
                "h2": "Repairable count and profile availability.",
                "blocks": [
                    ("p", "Everything else in this calculation is arithmetic. The repairable "
                          "count is a physical finding: substrate identified at a cut edge, "
                          "moisture measured at the toe kick and base, swelling measured rather "
                          "than described, joint integrity tested. Particleboard and MDF that "
                          "have swollen do not come back; plywood boxes with solid face frames "
                          "commonly do."),
                    ("p", "Profile availability is a documentary finding. If the line has been "
                          "discontinued, new boxes cannot be blended into a run that has to read "
                          "as one installation, and the replacement scope extends to the whole "
                          "run rather than to the failed boxes. That is the matching argument, "
                          "and it turns on manufacturer correspondence and supplier quotes "
                          "rather than on anyone&rsquo;s opinion."),
                    ("html", '<a class="tlink" href="/services/cabinet-repairability-reports/">'
                             'How a repairability report is built <span class="arw">&rarr;</span></a>'),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "The threshold",
                "h2": "When partial repair stops making sense.",
                "blocks": [
                    ("p", "There is a point where a partial scope costs so close to full "
                          "replacement that it is the worse outcome for both parties. One "
                          "mobilization instead of two, a uniform finish across the whole run, "
                          "and a warranty on all of it, against a marginal saving and a visible "
                          "line between old and new casework."),
                    ("p", "Around 70% of replacement cost is a reasonable place to have that "
                          "conversation. It is a rule of thumb rather than a standard, and it is "
                          "a great deal more productive than arguing box by box."),
                    ("table", "What moves the answer",
                     ["Input", "Effect"], [
                        ["Substrate type", "Decides the repairable count, which is the dominant variable"],
                        ["Profile availability", "Binary. Discontinued converts a partial scope into a full one"],
                        ["Countertop reuse", "Tops rarely survive box removal; assume replacement wherever boxes come out"],
                        ["Finish uniformity", "Refinished and new boxes age differently, which is a real defect in a single run"],
                        ["Run definition", "What counts as one continuous installation is often the actual dispute"],
                     ]),
                ],
            },
        ],
        "faqs": [
            ("Does this apply to vanities and commercial millwork?",
             "<p>Yes, with the same logic. Reception and nurse-station millwork, laboratory "
             "casework, library shelving and church built-ins all turn on substrate, matching "
             "and run definition. Laboratory and healthcare casework adds a chemical-resistance "
             "or cleanability specification that constrains what a repair is allowed to be.</p>"),
            ("How do we establish the repairable count?",
             "<p>From an assessment instead of a walkthrough: substrate identified at a cut "
             "edge, moisture readings recorded by location with the meter and scale noted, "
             "swelling measured at affected and unaffected points, joints and hardware tested. "
             "A number entered from an impression is exactly the input the other side will "
             "attack, and correctly.</p>"),
            ("What if the run has already been demolished?",
             "<p>Then the assessment works from photographs, retained components and the "
             "contractor&rsquo;s documentation, and the resulting opinion is qualified "
             "accordingly. This is a one-day exercise before demolition that becomes very hard "
             "a week later.</p>"),
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
                          "in the access line instead of hiding it in the unit price."),
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
             "system, and manufacturers will often say so in writing, which is the "
             "document that settles the argument.</p>"),
            ("Why does overhead and profit matter so much on a roof claim?",
             "<p>Because it is 20% of a large number and it is removed silently. The usual carrier "
             "position is that O&amp;P is owed only when a general contractor is engaged. "
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
        "slug": "overhead-profit-general-conditions-calculator",
        "nav_label": "O&amp;P and General Conditions",
        "card_title": "Overhead, profit &amp; general conditions",
        "card_blurb": ("Model the markups that get argued over on every commercial repair "
                       "&mdash; O&amp;P, general conditions, access premium and bond."),
        "title": "Overhead &amp; Profit Calculator | General Conditions",
        "description": ("Calculate overhead, profit, general conditions, occupied-building "
                        "premium and bond on a commercial repair, and test the three-trade "
                        "threshold for whether O&amp;P is owed."),
        "eyebrow": "Tool &middot; Markups",
        "h1": "Overhead, profit and<br>general <em>conditions</em>",
        "h1_plain": "Overhead, profit and general conditions calculator",
        "lede": ("After scope, markups are the single most disputed part of a commercial repair "
                 "estimate. This lays out the conventional treatment line by line so the "
                 "argument is about the assumptions instead of about the total."),
        "calc": OANDP,
        "sections": [
            {
                "eyebrow": "The three-trade test",
                "h2": "When is a general contractor reasonably required?",
                "blocks": [
                    ("p", "Overhead and profit compensate a general contractor for running a job: "
                          "coordinating subcontractors, carrying risk, supervising a schedule. "
                          "The question is not whether a GC was hired, it is whether one "
                          "was reasonably required by the nature of the work."),
                    ("p", "The convention that has grown up around that question is the "
                          "three-trade threshold: where a repair involves three or more trades "
                          "needing coordination, a general contractor is normally considered "
                          "reasonably necessary, and O&amp;P follows. It is a rule of thumb "
                          "instead of a legal standard, and it is a reasonable place for both "
                          "sides to start."),
                    ("p", "What makes the argument tractable is counting the trades honestly on "
                          "the actual scope and saying so. A commercial re-roof that involves "
                          "roofing, sheet metal, mechanical disconnect and reset, electrical and "
                          "structural repair is plainly a coordinated job. A single-trade "
                          "flooring replacement plainly is not. Most disputes live between those "
                          "two, and they are resolved by the scope document, not by assertion."),
                    ("table", "How the markups differ",
                     ["Markup", "What it pays for", "How it should be tested"], [
                        ["General conditions",
                         "Project-specific, time-dependent costs: supervision, temporary utilities and protection, dumpsters, permits, logistics, site facilities.",
                         "Built up from the schedule and the site, not taken as a flat percentage"],
                        ["Overhead",
                         "The contractor&rsquo;s cost of being in business: office, estimating, insurance, administration.",
                         "Conventionally 10%; genuinely varies with market and job type"],
                        ["Profit",
                         "Return for carrying the risk of the work.",
                         "Conventionally 10%; a matter of market rather than entitlement"],
                        ["Bond",
                         "Payment and performance security, common and often mandatory on public work.",
                         "A real, quotable cost, obtain the rate instead of estimating it"],
                     ]),
                ],
            },
            {
                "band": "paper2",
                "eyebrow": "General conditions",
                "h2": "The line that moves with the schedule.",
                "blocks": [
                    ("p", "General conditions are usually entered as a flat percentage and "
                          "then defended as though the percentage were the cost. They are not. "
                          "Supervision, temporary power, weather protection, site security and "
                          "logistics accrue per week, which means a disputed construction "
                          "schedule moves this line and the business-interruption claim at the "
                          "same time and in the same direction."),
                    ("p", "That connection is worth making explicit on any large file. If one "
                          "party argues the rebuild should have taken five months instead of "
                          "nine, they are arguing down the time-element loss and the general "
                          "conditions together, and a schedule that documents the cause "
                          "of each delay answers both at once."),
                    ("checks", [
                        "Build general conditions from a staffing and duration schedule, not from a percentage, on any job over a few months.",
                        "Identify which costs are time-dependent and which are fixed, so a change in duration can be priced rather than argued.",
                        "Price occupied-building constraints explicitly (phasing, night work, protection, infection control) instead of burying them in unit costs.",
                        "Obtain an actual bond rate where bonding is required; it is quotable and it is not a percentage guess.",
                        "State the trade count on the face of the estimate. It is the fact the O&amp;P argument turns on.",
                    ]),
                ],
            },
        ],
        "faqs": [
            ("Is 10 and 10 a rule?",
             "<p>No. It is a long-standing convention that both sides of the industry use as a "
             "starting point, and it is neither a statutory entitlement nor a ceiling. Markets, "
             "job types and risk profiles differ. What matters far more than the percentage is "
             "whether a general contractor is reasonably required at all, and whether general "
             "conditions have been built up properly or assumed.</p>"),
            ("Should O&amp;P be paid if the owner self-performs or acts as their own GC?",
             "<p>It is a genuine question instead of an obvious one, and it turns on the policy "
             "wording and on what the work actually required. The common position is that the "
             "measure is the reasonable cost to repair, which contemplates the contractor a "
             "prudent owner would engage, not a discount for the owner&rsquo;s own "
             "labor. The opposing position is that unincurred cost is not a loss. Both are "
             "arguable; the scope and the wording decide it.</p>"),
            ("Does the occupied-building premium belong in the claim?",
             "<p>Where the building has to stay in use during the repair, and that constraint "
             "increases the cost of the work, yes. It is part of the reasonable "
             "cost to repair that property. What it needs is documentation: the phasing plan, "
             "the hours restriction, the protection and containment required. Entered "
             "as a bare percentage it invites a bare percentage in reply.</p>"),
        ],
    },
]

for _t in TOOLS:
    _t["path"] = "/tools/%s/" % _t["slug"]
