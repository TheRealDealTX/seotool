"""Process guide, FAQ, glossary and guide articles for Indiana Insurance Appraiser."""

PROCESS_STEPS = [
    ("Confirm it is an amount dispute", "Appraisal resolves how much a covered loss costs. Before anything else, confirm the carrier has accepted coverage for at least part of the loss and that the disagreement is about scope or price, not whether the policy applies."),
    ("Read the clause and the calendar", "Find the appraisal condition in your policy, note how long each side has to name an appraiser, and calendar the suit-limitation date. Appraisal may not stop that clock."),
    ("Send the written demand", "Either side can demand appraisal in writing. The demand identifies the claim, states that the parties disagree on the amount of loss and names your appraiser or commits to naming one within the policy window."),
    ("Both appraisers inspect and estimate", "Each appraiser inspects the property and builds or refines a line-item estimate. Good appraisers document measurements, photos and pricing sources for every disputed line."),
    ("Appraisers negotiate line by line", "The two appraisers compare estimates item by item. Many disputes narrow sharply here, and an agreed award signed by both appraisers ends the process."),
    ("The umpire decides what is left", "Items the appraisers can’t agree on go to the umpire they selected, or one appointed by a court if they couldn’t agree. The umpire reviews submissions, may inspect, and decides each item."),
    ("Sign the award and get paid", "An award signed by any two of the three panel members sets the amount of loss. The carrier then applies the deductible, depreciation and limits and issues payment under the policy."),
]

PROCESS_BODY = """
<p>Indiana does not have a statute that writes the appraisal process for homeowners and commercial property policies. Your rights come from the appraisal condition in your own policy, read together with Indiana contract law. The wording varies by carrier, so treat this guide as a map of how appraisal commonly runs, then check each step against your policy.</p>
""" + "".join(f"<h2>{i + 1}. {t}</h2><p>{p}</p>" for i, (t, p) in enumerate(PROCESS_STEPS)) + """
<h2>How long it takes</h2>
<p>A residential file with a clear scope often wraps up in two to three months after both appraisers are named. Large commercial losses, contents-heavy claims and files that need an umpire hearing can take longer. Delays most often come from incomplete documentation, so the work you do before the demand pays off later.</p>
<h2>What it costs</h2>
<p>Each side pays its own appraiser, and most policies split the umpire’s fee equally. Appraiser fees may be a flat amount, hourly or a percentage of the increase. Get the arrangement in writing before anyone starts, and run your numbers through the <a href="/claim-gap-tools/claim-gap-net-recovery-estimator/">claim gap and net recovery estimator</a>.</p>
<h2>Where appraisal stops</h2>
<p>An appraisal panel values the loss. It doesn’t decide coverage, interpret disputed policy language beyond what valuation requires, or award damages for bad faith. Indiana courts recognize that insurers owe policyholders a duty of good faith and fair dealing, and the state’s unfair claim settlement practices law is enforced by the Indiana Department of Insurance. Whether a particular claim was mishandled is a legal question for an Indiana attorney.</p>
<div class="note"><b class="h">Before you demand</b>Run through the <a href="/claim-gap-tools/appraisal-readiness-checkup/">appraisal readiness checkup</a>. A complete file is the single biggest factor in a good award.</div>
"""

FAQ = [
    ("Understanding appraisal", [
        ("What is insurance appraisal?", "A process written into most property policies for resolving disagreements over the amount of a covered loss. Each side names an appraiser, the appraisers choose an umpire, and a written award signed by two of the three sets the amount."),
        ("Is appraisal the same as arbitration?", "They’re similar but not identical. Appraisal is limited to the amount of loss and is usually less formal, with no discovery or testimony under oath in the typical case."),
        ("Does Indiana law require appraisal?", "Indiana doesn’t impose a statutory appraisal process on homeowners policies. Appraisal rights come from the policy itself, so your form’s wording controls."),
        ("Can appraisal decide whether something is covered?", "Generally no. Appraisal values the loss. Coverage disputes, such as whether an exclusion applies, are decided by the carrier and, if contested, by a court."),
    ]),
    ("Costs and fees", [
        ("Who pays for appraisal?", "Each side pays its own appraiser. Most policies split the umpire’s fees and expenses equally."),
        ("How do appraisers charge?", "Flat fees, hourly rates and percentages of the increase are all common. Ask for the arrangement in writing before work begins."),
        ("Is the first conversation free?", "Yes. We review your situation at no charge and tell you honestly whether appraisal is likely to help."),
    ]),
    ("Timing and deadlines", [
        ("How long does an Indiana appraisal take?", "Many residential appraisals finish in two to three months after both appraisers are named. Complex claims can take longer."),
        ("Is there a deadline to demand appraisal?", "Some policies set one, and others are silent. Courts may also consider whether a demand came within a reasonable time. Act promptly once a dispute is clear."),
        ("Does appraisal stop the suit-limitation clock?", "Not automatically. Many Indiana policies require suits within two years of the loss. Protect that date separately and talk to an attorney if it is approaching."),
    ]),
    ("Indiana specifics", [
        ("Who regulates insurance companies in Indiana?", "The Indiana Department of Insurance licenses insurers, adjusters and agents and accepts consumer complaints about claim handling."),
        ("What is the Indiana FAIR Plan?", "A residual market that offers basic property coverage to owners who can’t obtain it in the regular market. FAIR Plan policies have their own conditions, so read the appraisal and claim provisions in yours."),
        ("Is there a wind pool in Indiana?", "No. Indiana is an inland state without a coastal wind pool. Wind and hail are covered under ordinary homeowners, farm and commercial policies."),
        ("What counties do you serve?", "All 92 Indiana counties, from Lake County on Lake Michigan to Posey County on the Ohio River."),
    ]),
    ("Working with us", [
        ("Are you a public adjuster or a law firm?", "Neither. We provide appraisal, estimating and umpire services. We don’t negotiate claims outside appraisal and we don’t give legal advice."),
        ("Can you work with my contractor or attorney?", "Yes. We regularly coordinate with contractors for scope details and with attorneys when a claim involves both valuation and legal issues."),
        ("What should I send you first?", "The carrier’s full estimate, your declarations page, any letters from the carrier, your photos and your contractor’s estimate if you have one."),
    ]),
]

GLOSSARY = [
    ("Actual cash value (ACV)", "The value of damaged property at the time of loss, usually replacement cost minus depreciation."),
    ("Additional living expense (ALE)", "Coverage for increased living costs, such as temporary housing, while a home is uninhabitable after a covered loss."),
    ("Amount of loss", "The dollar value of a covered loss. It’s the question an appraisal panel decides."),
    ("Appraisal award", "The written decision signed by two of the three panel members that sets the amount of loss."),
    ("Appraisal clause", "The policy condition allowing either party to demand appraisal when they disagree on the amount of loss."),
    ("Bad faith", "A legal claim that an insurer breached its duty of good faith and fair dealing. It’s decided by courts, not appraisal panels."),
    ("Collapse", "A coverage provision, often narrow, for the abrupt falling down of a building or part of it from specified causes such as the weight of ice or snow."),
    ("Coinsurance", "A commercial policy provision that reduces payment if the property was insured below a required percentage of its value."),
    ("Coverage A", "Dwelling coverage on a homeowners policy, for the house itself."),
    ("Coverage B", "Other structures coverage, for detached garages, sheds, fences and similar structures."),
    ("Coverage C", "Personal property, or contents, coverage."),
    ("Declarations page", "The summary page of a policy listing the insured, property, limits, deductibles and endorsements."),
    ("Deductible", "The portion of a covered loss the policyholder pays before the policy pays."),
    ("Depreciation", "The reduction in value due to age, wear and obsolescence, used to calculate actual cash value."),
    ("Derecho", "A long-lived, widespread windstorm with damaging straight-line winds, such as the June 2012 event that crossed Indiana."),
    ("Drip edge", "Metal flashing installed along roof edges to direct water into gutters; often missing from roof estimates."),
    ("Endorsement", "A written change to a policy that adds, removes or modifies coverage."),
    ("Estimate review", "A professional line-by-line comparison of the carrier’s estimate with the actual damage and current pricing."),
    ("Ice and water shield", "A self-adhering underlayment applied at eaves and valleys to resist leaks from ice dams and wind-driven rain."),
    ("Ice dam", "A ridge of ice at a roof’s edge that traps meltwater, which can back up under shingles and into the home."),
    ("Indiana Department of Insurance", "The state agency that regulates insurers, agents and adjusters in Indiana and handles consumer complaints."),
    ("Indiana FAIR Plan", "The residual market association that provides basic property insurance to owners unable to obtain it in the regular market."),
    ("Like kind and quality", "The standard for replacement materials that are similar in type and quality to the damaged property."),
    ("Matching", "Whether replacement materials must reasonably match undamaged areas, a frequent issue with discontinued shingles and siding."),
    ("Mitigation", "Reasonable steps taken after a loss to prevent further damage, such as tarping a roof or drying a wet basement."),
    ("Ordinance or law coverage", "Coverage for added repair costs required by building codes or ordinances in effect at the time of repair."),
    ("Overhead and profit (O&P)", "A general contractor’s charges for coordinating and supervising repairs, often 10% and 10%."),
    ("Proof of loss", "A sworn statement of the amount claimed, which the insurer may request within a time set by the policy."),
    ("Recoverable depreciation", "The depreciation held back from an initial payment that a replacement cost policy pays after repairs are completed."),
    ("Replacement cost value (RCV)", "The cost to repair or replace damaged property with like kind and quality, without deduction for depreciation."),
    ("Scope of loss", "The full list of damaged items and repairs needed, before pricing."),
    ("Square (roofing)", "One hundred square feet of roof surface."),
    ("Steep charge", "An estimate line item that compensates for slower work on steep roofs, commonly starting around 7/12 pitch."),
    ("Suit limitation", "The policy provision setting how long the insured has to file a lawsuit, commonly two years in Indiana property policies."),
    ("Supplement", "A request to add items or costs to an existing claim estimate, usually supported by documentation."),
    ("Test square", "A marked 10-by-10-foot area on a roof slope used to count hail impacts."),
    ("Umpire", "The neutral third member of an appraisal panel who decides items the two appraisers can’t agree on."),
    ("Unfair claim settlement practices", "Claim-handling conduct prohibited by Indiana insurance law and enforced by the Department of Insurance."),
    ("Water backup endorsement", "Optional coverage for water that backs up through sewers or drains or overflows from a sump, usually with its own limit."),
    ("Xactimate", "Estimating software widely used by insurers and contractors to price property repairs by ZIP code."),
]

POSTS = [
    {
        "slug": "ice-dams-and-indiana-homeowners-policies",
        "title": "Ice Dams and Your Indiana Homeowners Policy",
        "seo": "Ice Dams and Indiana Homeowners Insurance Claims",
        "desc": "How ice dams form on Indiana roofs, what homeowners policies commonly cover, and how to document an ice dam water claim for appraisal.",
        "summary": "Why ice dams form, what a typical policy covers, and how to document the water damage they cause.",
        "date": "2026-11-02", "read": "6 min",
        "body": """
<p>Every winter, ice dams turn small amounts of melting snow into ceiling stains, wet insulation and peeling paint in homes across northern Indiana. They are just as possible further south whenever heavy snow is followed by a stretch of freezing nights. Here is how they work and how to approach the claim.</p>
<h2>How an ice dam forms</h2>
<p>Heat escaping into the attic warms the roof deck and melts snow from below. The meltwater runs down to the eaves, which sit over the unheated overhang and stay cold, and it refreezes. Over days, a ridge of ice builds at the edge. Meltwater pools behind it, works under shingles and drips into the wall cavity or ceiling.</p>
<h2>What homeowners policies commonly cover</h2>
<p>Many Indiana homeowners forms cover sudden interior water damage caused by ice dams. The cost of removing the ice itself, or of improving insulation and ventilation, is generally treated as maintenance. Some forms contain specific language about ice dams, so read the water damage and exclusions sections of your own policy.</p>
<h2>Documenting the claim</h2>
<ul>
<li>Photograph the ice at the eaves from the ground, including icicles and the thickness of the ridge.</li>
<li>Photograph interior stains, wet insulation and any damage to finishes as soon as they appear.</li>
<li>Note the dates of snowfall and the cold snap that followed.</li>
<li>Keep receipts for emergency steaming or ice removal and any temporary repairs.</li>
</ul>
<h2>Where the disputes come from</h2>
<p>Carriers sometimes argue that ice dam leaks are long-term seepage or the result of poor ventilation. Clear dates, photos of the ice and fresh interior damage help show a sudden event. When coverage is accepted but the repair scope is too narrow, for example a patch of drywall when insulation and multiple ceiling areas are wet, appraisal can resolve the amount.</p>
<p>For more on winter claims, see our <a href="/indiana-claim-appraisal/ice-dam-freeze-snow-load-appraisal/">ice dam, freeze and snow-load appraisal</a> service page.</p>
""",
    },
    {
        "slug": "documenting-tornado-and-derecho-damage",
        "title": "Tornado or Derecho? Documenting Indiana Wind Damage",
        "seo": "Documenting Tornado and Derecho Damage in Indiana",
        "desc": "How to document tornado and derecho wind damage in Indiana, from storm reports to hidden structural damage, so the claim reflects the loss.",
        "summary": "Narrow tornado paths and broad derecho swaths leave different evidence. Here is how to capture both.",
        "date": "2026-10-20", "read": "7 min",
        "body": """
<p>Indiana sees both tornadoes and derechos, and both are windstorms under most property policies. The difference shows up in the evidence. A tornado leaves a concentrated path, often with debris thrown in many directions. A derecho leaves damage spread over a wide area, usually blown in one direction.</p>
<h2>Start with the storm record</h2>
<p>The National Weather Service surveys significant tornadoes and publishes ratings and paths, and storm reports document hail and damaging winds. Those public records help tie your damage to a date within the policy period. Save the relevant report or a screenshot with your claim file.</p>
<h2>What to photograph</h2>
<ul>
<li>Every elevation of the house, plus the roof from the ground, before any cleanup.</li>
<li>Missing, creased or lifted shingles. Creases across the tab show the shingle was folded back by wind.</li>
<li>Siding, soffit and fascia pulled loose, and trim that has shifted.</li>
<li>Fallen trees and limbs where they lie, along with their stumps or break points.</li>
<li>Outbuildings, fences and other structures.</li>
</ul>
<h2>Look for what’s hidden</h2>
<p>Strong winds can rack framing, crack trusses and loosen roof decking. Signs include doors that suddenly stick, new drywall cracks, nail pops and sagging rooflines. Ask for an attic inspection and document what it shows. Hidden structural damage is a common reason wind estimates come up short.</p>
<h2>Wind and water together</h2>
<p>When wind opens the roof or walls, rain follows. Interior damage from rain entering through a wind-created opening is commonly covered, while flooding from rising water usually is not. Photograph the opening and the interior damage together so the cause is clear.</p>
<p>Our <a href="/indiana-claim-appraisal/tornado-wind-damage-appraisal/">tornado and wind damage appraisal</a> page explains how we value these losses.</p>
""",
    },
    {
        "slug": "matching-discontinued-shingles-after-hail",
        "title": "Matching and Discontinued Shingles After Indiana Hail",
        "seo": "Matching Discontinued Shingles After Indiana Hail",
        "desc": "What Indiana homeowners should know about matching discontinued shingles and siding after hail, and how to document a matching dispute.",
        "summary": "When the original product is gone, a spot repair can leave a patchwork roof. What to know and what to document.",
        "date": "2026-10-06", "read": "6 min",
        "body": """
<p>Builders in Indiana’s fast-growing suburbs often used one shingle line and one siding profile across an entire neighborhood. A decade later, those products may be discontinued. After a hailstorm, that raises a hard question: what happens when only part of the roof or siding is approved for replacement?</p>
<h2>Why matching matters</h2>
<p>New shingles rarely match weathered ones exactly, even within the same line. When the line has been discontinued, the color, size and profile can differ noticeably. Siding is similar: a different profile or exposure can be obvious from the street, and some panels won’t lock into older ones.</p>
<h2>What your policy says</h2>
<p>Policy language on matching varies. Some forms say nothing specific, some promise like kind and quality, and some include endorsements that limit matching obligations. Indiana does not have a broad statute on matching for residential property claims comparable to some other states’ rules, so your policy wording and the facts carry most of the weight.</p>
<h2>How to document a matching issue</h2>
<ul>
<li>Identify the product. Shingle wrappers left in the attic or garage, or a sample taken by a roofer, can identify the line.</li>
<li>Get a written statement from a supplier or manufacturer confirming whether the product is still available.</li>
<li>Photograph the transition between new and old materials if any repair has been made.</li>
<li>Note brittle older shingles that tear when lifted, which can make a spot repair impractical.</li>
</ul>
<h2>Where appraisal fits</h2>
<p>When coverage is accepted and the dispute is whether a repair can actually restore the roof or siding to a reasonable, uniform condition, the cost of the repair method is often part of the amount of loss. That makes it the kind of question an appraisal panel regularly considers.</p>
""",
    },
    {
        "slug": "indiana-department-of-insurance-and-your-claim",
        "title": "What the Indiana Department of Insurance Can Do for Your Claim",
        "seo": "The Indiana Department of Insurance and Your Claim",
        "desc": "What the Indiana Department of Insurance can and cannot do about a property claim dispute, from consumer complaints to the FAIR Plan.",
        "summary": "A regulator’s role, how complaints work, and why a complaint isn’t a substitute for appraisal or legal advice.",
        "date": "2026-09-22", "read": "5 min",
        "body": """
<p>When a claim stalls, many policyholders wonder whether the state can step in. The Indiana Department of Insurance plays an important role, but it is a regulator, not a judge of how much your claim is worth.</p>
<h2>What the Department does</h2>
<p>The Department licenses and regulates insurers, agents and adjusters doing business in Indiana. It accepts consumer complaints, asks insurers to respond, and enforces Indiana’s laws on unfair claim settlement practices, which address conduct such as unreasonable delays or failing to explain a claim decision.</p>
<h2>What a complaint can do</h2>
<p>A complaint can prompt a written response from the carrier, bring attention to delays and correct clear procedural errors. Patterns of complaints can also inform regulatory action against a company.</p>
<h2>What it usually can’t do</h2>
<p>The Department generally doesn’t decide the dollar value of a disputed claim or order a specific payment amount in an individual valuation dispute. That is what appraisal is for. And it can’t give you legal advice about bad faith or other claims, which is a question for an Indiana attorney.</p>
<h2>The Indiana FAIR Plan</h2>
<p>If you have struggled to find coverage, the Indiana FAIR Plan offers basic property insurance to owners who can’t obtain it in the voluntary market. FAIR Plan policies have their own claim conditions. Read the appraisal provision in your policy if you have a dispute over amount.</p>
<h2>Using the tools together</h2>
<p>For a dispute about how much a covered loss is worth, appraisal is usually the most direct path. A complaint can run alongside it when claim handling has been slow or unclear.</p>
""",
    },
    {
        "slug": "releases-final-payments-and-holdback",
        "title": "Before You Sign: Releases, Final Checks and Holdback",
        "seo": "Before You Sign: Claim Releases and Holdback",
        "desc": "Before cashing a final insurance check or signing a release, Indiana homeowners should check scope, recoverable depreciation and deadlines.",
        "summary": "A final payment or release can close doors. Five checks to make before you sign anything.",
        "date": "2026-09-08", "read": "5 min",
        "body": """
<p>A check marked “final” or a release form in the mail can feel like the end of a long process. Before you sign or deposit anything described as a full and final settlement, take a few minutes to make sure you aren’t giving up more than you intend.</p>
<h2>1. Read every word on the check and the letter</h2>
<p>Language such as “full and final settlement” or an attached release can affect your ability to pursue more money later. If you don’t understand the effect of what you’re signing, ask an Indiana attorney before you sign.</p>
<h2>2. Compare the scope with the damage</h2>
<p>Does the estimate include every room, slope and trade that was damaged? Missing items are much harder to add after a release.</p>
<h2>3. Track recoverable depreciation</h2>
<p>On a replacement cost policy, the first payment is often actual cash value. The held-back depreciation is paid after repairs, within a deadline. Use our <a href="/claim-gap-tools/rcv-acv-holdback-calculator/">holdback calculator</a> and calendar the deadline.</p>
<h2>4. Check the deadlines</h2>
<p>Suit limitation, depreciation recovery and any appraisal demand windows keep running. Our <a href="/claim-gap-tools/claim-timeline-builder/">timeline builder</a> can lay them out.</p>
<h2>5. Get a second look if the gap is large</h2>
<p>If the payment is well below your contractor’s estimate, an <a href="/indiana-claim-appraisal/carrier-estimate-review/">estimate review</a> before you sign can show whether a supplement or appraisal makes sense.</p>
""",
    },
    {
        "slug": "appraisal-or-litigation-indiana",
        "title": "Appraisal or a Lawsuit? Choosing a Path for an Underpaid Claim",
        "seo": "Appraisal or Lawsuit for an Underpaid Indiana Claim?",
        "desc": "Appraisal or a lawsuit for an underpaid Indiana claim? Compare the two by issue, cost and timing, and see when an attorney should come first.",
        "summary": "Appraisal fixes amount disputes; courts handle coverage and conduct. How to tell which problem you have.",
        "date": "2026-08-25", "read": "7 min",
        "body": """
<p>An underpaid claim can be a valuation problem, a coverage problem, a conduct problem or all three. The right path depends on which one you actually have.</p>
<h2>When appraisal fits</h2>
<p>Appraisal is designed for disagreements over the amount of a covered loss: scope, measurements, pricing, matching and repair methods. It is usually faster and less expensive than litigation, and the award is binding on the amount.</p>
<h2>When you need an attorney</h2>
<ul>
<li>The claim has been denied outright.</li>
<li>The carrier relies on an exclusion or a late-notice defense.</li>
<li>A suit-limitation deadline is close.</li>
<li>You believe the claim was handled in bad faith.</li>
</ul>
<p>Indiana courts recognize a duty of good faith and fair dealing that insurers owe their policyholders. Whether conduct in a particular claim breached that duty, and what remedies may be available, are legal questions for an Indiana attorney.</p>
<h2>Can you do both?</h2>
<p>Sometimes. A claim might go to appraisal to set the amount while an attorney addresses coverage or conduct issues separately. The order matters, and an attorney can advise on how one affects the other.</p>
<h2>Comparing the paths</h2>
<div class="table-wrap"><table><thead><tr><th></th><th>Appraisal</th><th>Litigation</th></tr></thead><tbody>
<tr><th>Decides</th><td>Amount of loss</td><td>Coverage, conduct, damages</td></tr>
<tr><th>Typical timeline</th><td>Weeks to months</td><td>Months to years</td></tr>
<tr><th>Who decides</th><td>Two appraisers and an umpire</td><td>Judge or jury</td></tr>
<tr><th>Costs</th><td>Your appraiser plus half the umpire</td><td>Attorney fees and litigation costs</td></tr>
</tbody></table></div>
<p>If you’re unsure which path fits, start with a free conversation. We will tell you honestly if your claim needs a lawyer instead of an appraiser.</p>
""",
    },
]
