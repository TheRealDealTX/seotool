"""Process guide, FAQ, glossary and guide articles for Kansas property owners."""

G = "/kansas-appraisal-guides/"
TL = "/claim-calculators-kansas/"

PROCESS_BODY = """
<h2>Step 1: Confirm the dispute is about money</h2>
<p>Appraisal is built for one kind of disagreement: the insurer has accepted the claim, at least in part, and the two sides disagree on what the loss costs. Before anything else, read the carrier’s letters. If they deny coverage, cite an exclusion or say the damage is “wear and tear,” the dispute may be about coverage, which appraisal generally does not decide.</p>
<h2>Step 2: Put the gap on paper</h2>
<p>Gather the carrier’s full line-item estimate, your contractor’s or estimator’s line-item estimate, dated photos and your declarations page. Write a short supplement request listing what is missing and why. A surprising number of Kansas hail claims close at this stage when a missed slope, gutter run or steep charge is pointed out with proof.</p>
<h2>Step 3: Send the written demand</h2>
<p>If the gap remains, either side can demand appraisal in writing. A demand typically identifies the policy and claim number, states that the parties disagree on the amount of loss, invokes the appraisal condition and names your appraiser or commits to naming one within the policy’s time frame. Send it in a way you can prove, such as certified mail plus email.</p>
<h2>Step 4: Each side names an appraiser</h2>
<p>Many forms give each side 20 days after the demand to name a competent and impartial appraiser. Your appraiser reviews the file, inspects the property and builds an independent valuation. The insurer’s appraiser does the same.</p>
<h2>Step 5: The appraisers select an umpire</h2>
<p>The two appraisers choose a neutral umpire, ideally early. If they can’t agree within the time the policy allows, many policies let either party ask a court of record in the county where the property is located to appoint one. In Kansas that is typically the district court.</p>
<h2>Step 6: The appraisers work the differences</h2>
<p>This is where most of the value is decided. The appraisers inspect together, compare measurements and pricing, and agree on as many items as they can. Many appraisals end right here with an award signed by both appraisers.</p>
<h2>Step 7: The umpire decides what remains</h2>
<p>Unresolved items go to the umpire. Each appraiser submits a position with photos, measurements and pricing support. The umpire may inspect or hold an informal meeting, then decides each open item.</p>
<h2>Step 8: The award and payment</h2>
<p>An award signed by any two of the three sets the amount of loss. A clear award separates replacement cost, depreciation and actual cash value by coverage. The insurer then pays according to the policy, less the deductible and prior payments, with any recoverable depreciation paid after repairs. Roof payment schedules and cosmetic exclusions, where they apply, are applied to the award.</p>
<div class="note"><b class="h">Who pays</b>Each side pays its own appraiser, and umpire fees are usually split equally. Get any appraiser’s fee arrangement, including ours, in writing before you sign.</div>
<h2>What appraisal doesn’t do</h2>
<ul>
<li>It doesn’t decide coverage or exclusions.</li>
<li>It doesn’t award attorney fees, interest or damages for claim handling. Kansas statutes such as K.S.A. 40-256 and 40-908 can allow fee awards in some lawsuits; that is a question for a Kansas attorney.</li>
<li>It doesn’t automatically pause policy deadlines, including the suit-limitation period.</li>
</ul>
<h2>Where to get outside help</h2>
<p>The Kansas Insurance Department in Topeka offers consumer assistance and accepts complaints about insurers. Property owners who can’t find coverage in the standard market may be eligible for the Kansas FAIR Plan, the state’s residual market for basic property insurance. Neither replaces your own appraiser or attorney, but both are useful to know about.</p>
"""

FAQ = [
    ("Appraisal basics", [
        ("What is insurance appraisal?", "A process written into most property policies for settling disagreements about the amount of a covered loss. Each side names an appraiser, the appraisers pick an umpire, and two of the three signatures set the amount."),
        ("Is appraisal the same as arbitration?", "Not quite. Appraisal is limited to the amount of loss and is usually less formal. Arbitration can address broader issues, depending on the agreement."),
        ("Who can demand appraisal?", "Either you or the insurer, if the policy contains an appraisal clause and the parties disagree on the amount of loss."),
        ("Does appraisal decide coverage?", "Generally no. If the insurer says something isn’t covered, that is a coverage question for the insurer, the Kansas Insurance Department or an attorney."),
    ]),
    ("Kansas specifics", [
        ("Who regulates insurers in Kansas?", "The Kansas Insurance Department, led by the elected Commissioner of Insurance. It offers consumer assistance and takes complaints about insurers."),
        ("Does Kansas have a FAIR Plan?", "Yes. The Kansas FAIR Plan provides basic property insurance to owners who can’t get coverage in the voluntary market. Eligibility rules apply, including prior declinations."),
        ("What happens if my insurer handles a claim unfairly?", "Kansas has an unfair claim settlement practices law enforced by the Insurance Department, and statutes such as K.S.A. 40-256 and 40-908 can allow attorney fees in some lawsuits against insurers. A Kansas attorney can tell you whether any of that fits your situation."),
        ("Are percentage hail deductibles common in Kansas?", "Yes. Many Kansas homeowner policies carry a wind/hail deductible set as a percentage of the dwelling limit. Check your declarations page."),
        ("What is a roof payment schedule?", "An endorsement that pays a percentage of a roof’s replacement cost based on its age. It is increasingly common on policies sold in hail-prone states."),
    ]),
    ("Cost and timing", [
        ("What does appraisal cost?", "You pay your appraiser and usually half the umpire’s fee. Arrangements vary, so get the fee in writing before work starts."),
        ("How long does it take?", "Simple residential claims often resolve in six to ten weeks after both appraisers are named. Complex or commercial claims take longer."),
        ("Is it worth it for a small claim?", "Often not. If the gap is small relative to fees, a documented supplement request is usually better. Our appraisal payoff projector helps you check."),
        ("Do I have to repair before appraisal?", "No. But temporary repairs to prevent further damage are usually required, and recoverable depreciation is generally paid after repairs."),
    ]),
    ("After the award", [
        ("Is the award binding?", "On the amount of loss, an award signed by two of the three panel members is generally binding, subject to limited challenges."),
        ("When will I be paid?", "The policy sets the payment timing after an award. Deductibles, prior payments and recoverable depreciation rules still apply."),
        ("What if the insurer won’t pay the award?", "That is a matter for a Kansas attorney. The award is strong evidence of the amount owed."),
        ("Does the roof schedule still apply after an award?", "Usually yes. The award sets the roof’s full replacement cost; the schedule then determines what percentage is paid."),
    ]),
]

GLOSSARY = [
    ("Actual cash value (ACV)", "Replacement cost minus depreciation. The first payment under most replacement cost policies."),
    ("Additional living expense (ALE)", "Coverage for extra costs of living elsewhere while a home is repaired after a covered loss."),
    ("Appraisal clause", "The policy condition that lets either party demand appraisal when they disagree on the amount of loss."),
    ("Appraisal award", "The written decision, signed by two of the three panel members, that sets the amount of loss."),
    ("Appraiser", "A competent, impartial person chosen by each side to value the loss in appraisal."),
    ("Coinsurance", "A commercial policy condition that can reduce payment if a building is insured for less than a required percentage of its value."),
    ("Cosmetic damage exclusion", "An endorsement that excludes hail dents or marks that don’t affect a roof’s function, common on metal roofs."),
    ("Coverage A", "Dwelling coverage for the house itself. Percentage deductibles are often based on this limit."),
    ("Coverage B", "Other structures coverage, such as detached garages, sheds and fences."),
    ("Coverage C", "Personal property, or contents, coverage."),
    ("Declarations page", "The summary page of a policy listing coverages, limits, deductibles and endorsements."),
    ("Debris removal", "Coverage for removing debris from covered damage, often subject to a separate limit."),
    ("Demand for appraisal", "The written notice that invokes the appraisal clause."),
    ("Depreciation", "The reduction in value for age and condition. Recoverable depreciation can be paid after repairs."),
    ("Derecho", "A long-lived, widespread windstorm with damaging straight-line winds."),
    ("Drip edge", "Metal flashing along roof edges, often required by code and frequently missed in estimates."),
    ("Endorsement", "A form that adds to or changes the terms of a policy."),
    ("Estimate", "A line-item list of repair quantities and prices, usually prepared in estimating software."),
    ("FAIR Plan", "A state residual market for basic property insurance. Kansas has the Kansas FAIR Plan."),
    ("Functional damage", "Damage that affects how a roof or component performs, as opposed to appearance only."),
    ("Hail strike", "An impact mark from hail, counted in test squares to assess roof damage."),
    ("Holdback", "Recoverable depreciation withheld until repairs are complete."),
    ("Ice-and-water shield", "A self-adhering roof underlayment used at eaves and valleys to resist ice dams."),
    ("Kansas Insurance Department", "The state agency in Topeka that regulates insurers and helps consumers."),
    ("Line item", "A single entry in an estimate, such as a roofing square of shingles or a linear foot of gutter."),
    ("Matching", "The issue of whether repaired areas can reasonably match undamaged areas in color, texture or profile."),
    ("Mitigation", "Reasonable steps to prevent further damage after a loss, such as tarping or drying."),
    ("Ordinance or law", "Coverage for added costs to meet current building codes during repairs."),
    ("Overhead and profit (O&P)", "A general contractor’s charges for overhead and profit, often 10% and 10%."),
    ("Payment schedule (roof)", "An endorsement that pays a percentage of roof replacement cost based on roof age."),
    ("Percentage deductible", "A deductible calculated as a percentage of the dwelling limit, common for wind and hail."),
    ("Pitch", "Roof slope expressed as rise per 12 inches of run, such as 6/12."),
    ("Proof of loss", "A sworn statement of the amount claimed, sometimes requested by the insurer."),
    ("Replacement cost value (RCV)", "The cost to repair or replace with materials of like kind and quality, without depreciation."),
    ("Roofing square", "One hundred square feet of roof surface."),
    ("Scope", "The list of damaged items and the repairs needed."),
    ("Steep charge", "An added labor charge for roofs with steeper pitches, often 7/12 and above."),
    ("Suit limitation", "The policy clause that sets a time limit for suing the insurer."),
    ("Supplement", "A request for additional payment for items missed or under-priced in the original estimate."),
    ("Test square", "A 10-by-10-foot area on a roof slope used to count hail strikes."),
    ("Umpire", "The neutral third member of an appraisal panel who decides items the appraisers can’t agree on."),
    ("Wind/hail deductible", "A separate deductible that applies to wind and hail losses, often a percentage."),
]

POSTS = [
    {
        "slug": "kansas-hail-claim-roof-schedules",
        "title": "Kansas Hail Claims, Roof Schedules and Cosmetic Exclusions",
        "seo": "Kansas Hail Claims: Roof Schedules & Exclusions",
        "desc": "How roof payment schedules, cosmetic damage exclusions and wind/hail deductibles shape what a Kansas hail claim actually pays.",
        "summary": "Three policy features now decide many Kansas hail payouts. Here is how each works and how appraisal fits around them.",
        "date": "2026-11-03", "read": "7 min",
        "body": """
<h2>Hail is the Kansas claim</h2>
<p>Kansas regularly ranks among the states with the most hail claims. Insurers have responded with three policy features that change how much a hail claim pays: roof payment schedules, cosmetic damage exclusions and percentage wind/hail deductibles. None of them changes how much damage the storm did. All of them change the check.</p>
<h2>1. Roof payment schedules</h2>
<p>A roof schedule pays a set percentage of roof replacement cost based on age. A five-year-old roof may be paid at most or all of its replacement cost; a fifteen-year-old roof may be paid at well under half. Unlike ordinary depreciation, the reduction usually isn’t recoverable after repairs.</p>
<p>Two practical points: confirm the roof age the insurer used, and make sure the replacement cost the schedule is applied to is complete. A higher, accurate roof valuation still raises the scheduled payment. Try the <a href=\"""" + TL + """roof-age-payment-schedule-calculator/">roof age payment schedule calculator</a> to see the effect.</p>
<h2>2. Cosmetic damage exclusions</h2>
<p>Often attached to metal roofing, these exclusions remove coverage for dents that don’t affect function, meaning the roof still sheds water. Whether specific damage is cosmetic or functional can be contested, and that question often turns on coverage rather than cost.</p>
<h2>3. Percentage wind/hail deductibles</h2>
<p>A 1% or 2% deductible on a $300,000 dwelling limit is $3,000 or $6,000. On a modest hail claim, that can absorb most of the payment. Use the <a href=\"""" + TL + """percentage-deductible-converter/">percentage deductible converter</a> to see yours in dollars.</p>
<h2>Where appraisal fits</h2>
<p>Appraisal sets the amount of loss: the full replacement cost of the damaged roof, siding, gutters and other items. The policy’s schedule, exclusions and deductible are then applied to that number. If the insurer under-measured the roof or approved only some slopes, appraisal can correct the base number even when a schedule applies.</p>
<div class="note"><b class="h">Illustrative example</b>Suppose a roof’s replacement cost is $17,500 and a schedule pays 55% at its age. If an accurate valuation raises the roof to $21,000, the scheduled payment rises from $9,625 to $11,550. Figures are hypothetical.</div>
""",
    },
    {
        "slug": "appraisal-attorneys-and-kansas-fee-statutes",
        "title": "Appraisal, Attorneys and Kansas Fee Statutes: A Plain Overview",
        "seo": "Appraisal, Attorneys & Kansas Fee Statutes",
        "desc": "A plain overview of where appraisal ends and legal help begins in Kansas, including K.S.A. 40-256 and 40-908, without legal advice.",
        "summary": "Appraisal handles the amount of loss. Some disputes need a lawyer. Here is a careful, general look at the line between them in Kansas.",
        "date": "2026-10-27", "read": "6 min",
        "body": """
<h2>Different tools for different problems</h2>
<p>An appraiser values the loss. A public adjuster manages and negotiates a claim on the policyholder’s behalf. An attorney handles legal disputes: coverage denials, claim-handling problems, deadlines and lawsuits. Choosing the right help first saves time and money.</p>
<h2>When appraisal is the right tool</h2>
<ul><li>The insurer accepts the loss, at least in part.</li><li>The disagreement is about scope, quantities or prices.</li><li>You have documentation, including your own line-item estimate.</li><li>Deadlines aren’t close.</li></ul>
<h2>When to talk to a Kansas attorney</h2>
<ul><li>The claim is denied, or a major part is excluded.</li><li>The insurer isn’t responding or keeps delaying.</li><li>A suit-limitation date is approaching.</li><li>You’re asked to sign a release or examination under oath.</li></ul>
<h2>Kansas fee statutes, described generally</h2>
<p>Kansas has two statutes that can allow a court to award attorney fees to a policyholder who wins a lawsuit against an insurer. K.S.A. 40-256 addresses refusals to pay without just cause or excuse. K.S.A. 40-908 applies to actions on policies insuring property against fire, tornado, lightning or hail, subject to conditions such as tender. Kansas courts have generally not recognized a separate first-party bad-faith tort in the way some states do. How these rules apply depends on facts and current case law, so treat this as background, not advice.</p>
<h2>How we fit in</h2>
<p>We are appraisers, not lawyers. If your claim needs legal help, we will tell you so on the first call. If appraisal is the right step, we can work alongside your attorney when you have one.</p>
""",
    },
    {
        "slug": "documenting-tornado-damage-kansas",
        "title": "After a Kansas Tornado: Documenting Partial and Total Losses",
        "seo": "After a Kansas Tornado: Documenting Your Loss",
        "desc": "A practical guide to documenting tornado and straight-line wind damage in Kansas, from missing shingles to total losses and debris.",
        "summary": "What to photograph, measure and save after a tornado or derecho so the amount of loss can be valued fully.",
        "date": "2026-10-14", "read": "7 min",
        "body": """
<h2>Safety and mitigation first</h2>
<p>Stay out of damaged structures until they are safe. Then take reasonable steps to prevent further damage: tarp openings, board windows, shut off water if pipes are broken. Keep receipts. Most policies require mitigation, and the costs are generally reimbursable.</p>
<h2>Photograph before anything moves</h2>
<ul><li>Wide shots of every side of each building, then close-ups.</li><li>The roof from the ground and, if safe, from a ladder or drone.</li><li>Interior rooms, ceilings and attic, including any light coming through.</li><li>Fences, sheds, outbuildings, trees and vehicles.</li><li>Debris on the property, including items that blew in from elsewhere.</li></ul>
<h2>Look for hidden structural damage</h2>
<p>Tornadoes and strong straight-line winds can rack framing, shift walls on foundations and crack slabs without obvious exterior signs. Doors that stick, cracked drywall at corners and gaps at the sill plate are clues. A structural engineer may be needed.</p>
<h2>Total losses</h2>
<p>For total losses, the key questions become the rebuild cost, debris removal, code upgrades and contents. After big events like the Greensburg tornado, demand for contractors and materials rises. Estimates written in the first days may not reflect real rebuild costs.</p>
<h2>Keep a claim journal</h2>
<p>Log every call, email and visit with dates and names. Store photos with dates. Use our <a href=\"""" + TL + """claim-timeline-builder/">claim timeline builder</a> to track deadlines.</p>
""",
    },
    {
        "slug": "grass-fire-claims-kansas-farms",
        "title": "Grass Fire Claims on Kansas Farms, Ranches and Acreages",
        "seo": "Grass Fire Claims on Kansas Farms & Ranches",
        "desc": "How grass fire and wildfire claims work on Kansas farms and acreages: fencing, outbuildings, smoke damage and coverage questions.",
        "summary": "Prairie fires burn more than homes. Here is how fence, outbuildings and smoke damage are handled, and where disputes arise.",
        "date": "2026-09-30", "read": "6 min",
        "body": """
<h2>Fast fires, wide losses</h2>
<p>When dry grass meets strong wind, Kansas fires can travel for miles. The 2016 Anderson Creek fire, the 2017 Starbuck fire and the 2021 Four County Fire each burned homes, barns, fence and pasture over huge areas. Claims after fires like these involve many kinds of property at once.</p>
<h2>Sort your coverages first</h2>
<p>Farm and ranch policies often schedule buildings, fence and equipment separately with their own limits and valuation. A homeowner policy may cover fence only under Other Structures. Start by matching each damaged item to the coverage that applies.</p>
<h2>Fence</h2>
<p>Fence is priced per linear foot, but the real cost depends on post type, wire, terrain, access and how much old fence must be removed. Document lengths, types and conditions with photos and maps.</p>
<h2>Outbuildings and equipment</h2>
<p>Pole barns, sheds and bins may be insured at actual cash value. Equipment may need specialist valuation. Keep purchase records and photos.</p>
<h2>Smoke damage</h2>
<p>Homes that didn’t burn can still have smoke and soot in HVAC systems, attics and contents. Cleaning protocols and replacement decisions are a frequent source of disagreement.</p>
<h2>Where appraisal helps</h2>
<p>When coverage is accepted and the dispute is cost, appraisal can resolve fence, building and smoke-cleaning values with documentation that reflects rural realities.</p>
""",
    },
    {
        "slug": "choosing-an-appraisal-umpire",
        "title": "How an Appraisal Umpire Is Chosen, and Why It Matters",
        "seo": "How an Appraisal Umpire Is Chosen in Kansas",
        "desc": "How appraisal umpires are chosen in Kansas, what they decide, what they cost and what to do if the appraisers cannot agree on one.",
        "summary": "The umpire decides the items the appraisers can’t settle. Here is how one is selected and what makes a good choice.",
        "date": "2026-09-16", "read": "5 min",
        "body": """
<h2>The umpire’s role</h2>
<p>The umpire is the neutral third member of an appraisal panel. The umpire doesn’t revisit items the appraisers agreed on; they decide the remaining disputed items, and their signature with one appraiser makes the award binding on the amount of loss.</p>
<h2>How umpires are selected</h2>
<p>Most policies direct the two appraisers to choose the umpire. If they can’t agree within the time allowed, either party can usually ask a court of record in the county where the property is located to appoint one. In Kansas, that is generally the district court.</p>
<h2>What makes a good umpire</h2>
<ul><li>Real estimating and construction knowledge.</li><li>No conflicts with either side, and full disclosure.</li><li>A clear process for submissions and inspections.</li><li>Willingness to explain decisions item by item.</li></ul>
<h2>Cost</h2>
<p>Umpire fees vary with complexity and are usually split equally. Ask for the fee arrangement in writing before the umpire starts.</p>
<h2>Our umpire work</h2>
<p>We serve as umpire on Kansas panels where we represent neither side. See our <a href="/what-we-handle/appraisal-umpire-services/">umpire services</a> page.</p>
""",
    },
    {
        "slug": "matching-siding-shingles-after-hail",
        "title": "Matching Siding and Shingles After Hail in Kansas",
        "seo": "Matching Siding & Shingles After Hail in Kansas",
        "desc": "Why matching discontinued siding and shingles is a frequent Kansas hail claim dispute, and how documentation helps an appraisal panel.",
        "summary": "When the old siding or shingle is no longer made, a partial repair can leave a patchwork. Here is how matching disputes are handled.",
        "date": "2026-09-02", "read": "6 min",
        "body": """
<h2>The matching problem</h2>
<p>Hail often damages one or two sides of a house or a few roof slopes. If the existing siding profile or shingle color is discontinued, a partial repair may not match. Owners argue the whole elevation or roof should be replaced; insurers may argue only damaged pieces are owed.</p>
<h2>What policies and regulations say</h2>
<p>Policy language varies, and so do state rules and court decisions on matching. Some policies address it directly; many don’t. Because this is partly a coverage question, the policy wording matters a great deal.</p>
<h2>Documenting a matching issue</h2>
<ul><li>Identify the product: brand, profile, color and exposure.</li><li>Get written confirmation from suppliers if it’s discontinued.</li><li>Photograph sample pieces against the existing material in daylight.</li><li>Show how the elevations or slopes connect visually.</li></ul>
<h2>How appraisal handles it</h2>
<p>Where the insurer agrees matching is owed but disputes the cost, or where the policy clearly supports it, appraisal can value the full repair. Where the insurer denies that matching is covered at all, a legal opinion may be needed first.</p>
""",
    },
]
