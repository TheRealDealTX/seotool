"""Process guide, FAQ, glossary and guide articles for South Dakota policyholders."""

PROCESS_STEPS = [
    ("Pin down the disagreement", "Appraisal starts with a specific dispute about the amount of loss. Before anything else, compare the carrier’s itemized estimate with your own and list the differences: missing slopes, short quantities, pricing, matching, code items. If the dispute is really about coverage, appraisal is the wrong tool."),
    ("Send the written demand", "Either side can demand appraisal in writing under most policies. The demand should identify the claim, state that you disagree on the amount of loss and invoke the appraisal provision. Keep proof of delivery. Some policies set a time for each side to name its appraiser after the demand."),
    ("Each side names an appraiser", "You choose your appraiser and the insurer chooses its own. Most clauses require each appraiser to be competent and independent or disinterested. Your appraiser inspects the property, builds a line-item estimate and gets ready to defend it."),
    ("The appraisers select an umpire", "The two appraisers try to agree on a neutral umpire. If they cannot within the time the policy allows, either side can usually ask a court where the property is located to appoint one."),
    ("The appraisers work the numbers", "Your appraiser and the carrier’s appraiser meet, inspect together if needed and go through the estimates line by line. Every item they agree on is settled. Many claims resolve entirely at this stage."),
    ("The umpire decides what is left", "Items the appraisers cannot agree on go to the umpire with photos, measurements and pricing support. The umpire may inspect the property and will decide each open item."),
    ("Two signatures make the award", "When any two of the three panel members sign the award, it sets the amount of loss. The award should list replacement cost and actual cash value clearly. The carrier then pays according to the policy, applying the deductible, limits and any prior payments."),
]

PROCESS_BODY = """
<h2>Before you start: is appraisal the right tool?</h2>
<p>Appraisal answers one question: how much does the covered damage cost to repair or replace? It is the right tool when the insurer has accepted the claim, at least in part, and you disagree about scope, quantities or price. It is usually the wrong tool when the claim was denied, when the argument is about an exclusion, or when the gap is too small to justify the cost.</p>
<div class="note"><b class="h">South Dakota context</b>Property insurance in South Dakota is regulated by the Division of Insurance in Pierre. South Dakota has no state FAIR plan or wind pool, so most owners are insured through standard carriers or, for harder-to-place risks, the surplus lines market. Appraisal clauses appear in both, but the wording varies, so always read your own policy.</div>
<h2>The seven stages of insurance appraisal</h2>
""" + "".join(f'<h3>{i + 1}. {t}</h3><p>{p}</p>' for i, (t, p) in enumerate(PROCESS_STEPS)) + """
<h2>How long it takes</h2>
<p>A straightforward residential appraisal often finishes within two to four months after both appraisers are named. Large commercial losses, farmsteads with many buildings and panels that need an umpire hearing can take longer. Delays usually come from scheduling inspections and gathering documents, not from the panel itself.</p>
<h2>What appraisal does not do</h2>
<ul>
<li>It does not decide whether something is covered.</li>
<li>It does not award damages for bad faith or attorney’s fees.</li>
<li>It does not extend policy deadlines on its own.</li>
<li>It does not raise your policy limits.</li>
</ul>
<p>South Dakota law gives policyholders separate remedies when an insurer handles a claim unreasonably, including a recognized bad-faith claim and, in some situations, attorney fees when a refusal to pay is found to be vexatious or without reasonable cause. Those are legal questions for a South Dakota attorney, and they sit outside the appraisal process.</p>
<h2>Common mistakes to avoid</h2>
<ul>
<li><strong>Demanding appraisal too early,</strong> before hidden damage is opened up and documented.</li>
<li><strong>Naming an appraiser with a stake in the repair,</strong> which can give the other side grounds to challenge the award.</li>
<li><strong>Bringing a lump-sum bid</strong> instead of a line-item estimate.</li>
<li><strong>Signing an award that does not separate RCV and ACV,</strong> which can cause new arguments about depreciation.</li>
<li><strong>Losing track of the suit limitation date</strong> while appraisal is underway.</li>
</ul>
"""

FAQ = [
    ("How appraisal works", [
        ("What is insurance appraisal?", "A process written into most property policies for settling disagreements about the amount of a covered loss. Each side names an appraiser, the appraisers choose an umpire, and an agreement signed by any two of the three sets the amount."),
        ("Who can demand appraisal?", "Under most policies, either you or the insurer can demand appraisal in writing when you disagree on the amount of loss."),
        ("Is the appraisal award binding?", "On the amount of loss, generally yes, once two of the three panel members sign. Coverage questions are separate."),
        ("Does appraisal decide coverage?", "No. Appraisal values the loss. Whether the policy covers it is decided by the policy, the parties and, if necessary, the courts."),
        ("Do I need a lawyer for appraisal?", "Not necessarily. Many appraisals happen without lawyers. If there is a coverage denial, a bad-faith concern or an approaching deadline, talk to a South Dakota attorney."),
    ]),
    ("Costs and fees", [
        ("Who pays for appraisal?", "Usually each side pays its own appraiser and the two sides split the umpire’s fee and other shared costs. Your policy controls."),
        ("How do appraisers charge?", "Arrangements vary: flat fees, hourly rates or a percentage of the increase. We put our fee in writing before any work begins."),
        ("Is appraisal worth it for a small claim?", "Often not. When the gap is small, a documented supplement request is usually faster and cheaper. Our appraisal payoff estimator helps you check."),
    ]),
    ("Timing and deadlines", [
        ("How long does appraisal take?", "Simple residential claims often resolve within a few months of both appraisers being named. Complex claims take longer."),
        ("Is there a deadline to demand appraisal?", "Some policies set time limits around appraisal and all policies have a suit limitation clause. Read your policy and do not assume appraisal pauses any deadline."),
        ("When do I get paid after an award?", "Policies usually set a period for payment after an award or agreement. The carrier applies the deductible, limits and prior payments."),
    ]),
    ("South Dakota specifics", [
        ("Who regulates insurers in South Dakota?", "The South Dakota Division of Insurance, part of the Department of Labor and Regulation, based in Pierre. It accepts consumer complaints about claim handling."),
        ("Does South Dakota have a FAIR plan or wind pool?", "No. South Dakota does not have a state FAIR plan or wind pool. Properties that standard carriers decline are typically placed in the surplus lines market."),
        ("What are the most common claims here?", "Hail and wind lead by a wide margin, followed by winter damage, water losses, fire and, in the Black Hills, wildfire."),
        ("What if my insurer acted in bad faith?", "South Dakota recognizes legal remedies when an insurer handles a claim unreasonably. Those are legal claims for an attorney. Appraisal deals only with the amount of loss."),
    ]),
    ("Working with us", [
        ("Do you work statewide?", "Yes. We serve all 66 South Dakota counties, from the Sioux Empire to the Black Hills."),
        ("Are you a public adjuster or a law firm?", "Neither. We provide appraisal, estimating and umpire services. We do not negotiate claims outside appraisal and we do not give legal advice."),
        ("What should I send for a first review?", "The carrier’s full estimate, your declarations page, carrier letters, photos and your contractor’s estimate if you have one."),
    ]),
]

GLOSSARY = [
    ("Actual cash value (ACV)", "Replacement cost minus depreciation. Often the first payment on a replacement cost policy, and the full payment on an ACV policy."),
    ("Additional living expense (ALE)", "Coverage for extra costs of living elsewhere while your home is being repaired. Also called loss of use or Coverage D."),
    ("Agreed value", "An endorsement in which the insurer and the owner agree on a property’s value in advance, usually suspending coinsurance."),
    ("All-risk policy", "A policy that covers physical loss from any cause not specifically excluded. Also called open perils."),
    ("Amount of loss", "The dollar value of the damage. This is what an appraisal panel decides."),
    ("Appraisal award", "The written decision signed by two of the three panel members that sets the amount of loss."),
    ("Appraisal clause", "The policy provision that lets either side demand appraisal when they disagree on the amount of loss."),
    ("Appraiser", "The person each side names to value the loss and work with the other appraiser and the umpire."),
    ("Coinsurance", "A clause requiring you to insure property for a set percentage of its value. Falling short can reduce a claim payment."),
    ("Collateral damage", "Damage to soft metals, screens, vents and other items that helps show hail size, direction and date."),
    ("Cosmetic damage exclusion", "An endorsement, common on metal roofs, that excludes dents or marks that do not affect function."),
    ("Coverage A", "Dwelling coverage for the house itself and attached structures."),
    ("Coverage B", "Other structures coverage for detached garages, sheds, fences and similar buildings."),
    ("Coverage C", "Personal property coverage for contents."),
    ("Declarations page", "The summary page of your policy listing limits, deductibles, endorsements and the policy period."),
    ("Deductible", "The portion of a covered loss you pay before the policy pays."),
    ("Depreciation", "A reduction in value for age, wear and obsolescence."),
    ("Derecho", "A long-lived, widespread windstorm produced by a line of thunderstorms. Eastern South Dakota was hit by one on May 12, 2022."),
    ("Disinterested", "Having no financial or personal stake in the outcome. Many appraisal clauses require appraisers to be disinterested or independent."),
    ("Endorsement", "A written change to a policy that adds, removes or modifies coverage."),
    ("Estimate", "An itemized list of repairs with quantities and prices. Appraisal panels work from line-item estimates."),
    ("Ice dam", "A ridge of ice at the roof edge that traps meltwater, which can then back up under shingles and into the house."),
    ("Ingress", "Water or debris entering a building through an opening, such as one created by wind or hail."),
    ("Line item", "A single entry in an estimate for one task or material, with a quantity and unit price."),
    ("Matching", "The question of whether repairs must reasonably match undamaged areas in color, texture and appearance."),
    ("Mitigation", "Reasonable steps to prevent further damage after a loss, such as tarping a roof or drying a basement."),
    ("Named peril", "A policy that covers only the causes of loss listed in it, common for some farm buildings."),
    ("Ordinance or law coverage", "Coverage for extra costs to meet current building codes during repair or rebuilding."),
    ("Overhead and profit (O&P)", "A contractor’s general costs and margin, often 10% and 10%, added when a project requires coordination of several trades."),
    ("Pitch", "The steepness of a roof, written as rise over 12 inches of run, such as 7/12."),
    ("Proof of loss", "A sworn statement of the amount claimed, which carriers may request within a set time."),
    ("Recoverable depreciation", "Depreciation withheld from the first payment that you can recover after repairs are completed."),
    ("Replacement cost value (RCV)", "The cost to repair or replace damaged property with materials of like kind and quality, without deducting depreciation."),
    ("Reservation of rights", "A letter in which the insurer says it is handling a claim while reserving the right to deny coverage later."),
    ("Scope", "The list of damaged items and the work needed to repair them."),
    ("Square", "A roofing unit equal to 100 square feet of roof surface."),
    ("Sub-limit", "A lower limit within a policy for a specific type of loss, such as mold, trees or sewer backup."),
    ("Supplement", "A request to add items or increase amounts in the carrier’s estimate, supported by documentation."),
    ("Surplus lines", "Insurance written by carriers not licensed as standard insurers in the state, often used for hard-to-place risks."),
    ("Suit limitation", "The policy clause setting how long you have to file a lawsuit against the insurer."),
    ("Test square", "A marked area of roof, often 10 feet by 10 feet, where hail hits are counted."),
    ("Umpire", "The neutral third member of an appraisal panel who decides items the two appraisers cannot agree on."),
    ("Wind and hail deductible", "A separate deductible for windstorm or hail losses, often a percentage of the dwelling limit."),
]

POSTS = [
    {
        "slug": "how-the-appraisal-clause-works-in-south-dakota",
        "title": "How the Appraisal Clause Works on a South Dakota Policy",
        "seo": "How the Appraisal Clause Works in South Dakota",
        "desc": "A plain-English guide to how the appraisal clause works on South Dakota property policies: the demand, the panel, the umpire and the award.",
        "summary": "What the appraisal clause says, what it covers, when to use it and the mistakes that cost policyholders money.",
        "date": "2026-10-06", "read": "7 min",
        "body": """
<p>Most South Dakota property owners never read the appraisal clause until they need it. That is understandable. It is a short paragraph buried in the conditions section. But when a claim stalls over money, it may be the most useful paragraph in the policy.</p>
<h2>What the clause usually says</h2>
<p>Wording varies by carrier, but most appraisal clauses follow the same pattern. If you and the insurer fail to agree on the amount of loss, either party may demand appraisal in writing. Each side selects a competent and independent appraiser. The two appraisers select an umpire. If they cannot agree on one, either side can ask a court to choose. The appraisers state the amount of loss separately, and any disagreements go to the umpire. A written agreement by any two of the three sets the amount.</p>
<h2>The key phrase: amount of loss</h2>
<p>Appraisal is about money, not coverage. A panel can decide how many roof squares were damaged, what siding costs, whether a basement carpet can be dried or must be replaced, and what a pole barn costs to rebuild. It generally cannot decide whether a peril is excluded, whether you gave late notice or whether the damage is wear and tear. Some disputes mix both, and how courts treat those mixed questions can vary.</p>
<h2>When appraisal makes sense</h2>
<ul>
<li>The carrier accepted the claim, at least in part.</li>
<li>You have the carrier’s itemized estimate and your own.</li>
<li>The gap is large enough to justify appraisal costs.</li>
<li>The disagreement is about scope, quantities or price.</li>
</ul>
<h2>When it does not</h2>
<ul>
<li>The claim was denied entirely.</li>
<li>The real dispute is about an exclusion or a policy condition.</li>
<li>The gap is small enough to close with a documented supplement.</li>
<li>A suit limitation date is close and you have not spoken to an attorney.</li>
</ul>
<h2>Mistakes that cost money</h2>
<p>The most expensive mistake is demanding appraisal before the claim is fully documented. Hidden damage that was never opened up, rooms nobody inspected and a lump-sum contractor bid all weaken your position. The second is naming an appraiser who stands to earn the repair contract, which can invite a challenge to the award. The third is signing an award that does not separate replacement cost and actual cash value.</p>
<h2>Where South Dakota fits in</h2>
<p>South Dakota insurers are regulated by the Division of Insurance in Pierre. The state recognizes legal remedies when an insurer handles a claim unreasonably, but those are separate from appraisal and belong with an attorney. Appraisal stays focused on the number.</p>
<p>Before demanding appraisal, grade your file with our <a href="/policyholder-calculators/claim-file-readiness-grader/">claim file readiness grader</a>.</p>
""",
    },
    {
        "slug": "documenting-hail-damage-after-a-prairie-storm",
        "title": "Documenting Hail Damage After a Prairie Storm",
        "seo": "Documenting Hail Damage After a Prairie Storm",
        "desc": "How to document hail damage after a South Dakota storm: photos, storm dates, collateral damage and roof details that hold up in a claim.",
        "summary": "A practical checklist for photographing and recording hail damage so the claim, and any appraisal, rests on solid evidence.",
        "date": "2026-09-15", "read": "6 min",
        "body": """
<p>Hail claims are won and lost on documentation. The storm passes in minutes, but the arguments about what it did can last months. Here is how to build a record that holds up.</p>
<h2>Right after the storm</h2>
<ul>
<li><strong>Note the date and time.</strong> Write down when hail started and stopped and how large the stones looked.</li>
<li><strong>Photograph hailstones</strong> next to a coin, ruler or tape measure, if it is safe to go out.</li>
<li><strong>Photograph soft metals:</strong> gutters, downspouts, window wraps, roof vents, mailboxes, grills and air conditioner fins. These show hail size and direction.</li>
<li><strong>Photograph vehicles, fences and outdoor furniture</strong> that were hit. They help tie damage to this storm.</li>
</ul>
<h2>On the roof (or from a ladder)</h2>
<p>Only climb if it is safe, or hire a roofer to document it. Photograph each slope from a distance, then close up with chalk circles around hits and a scale in the frame. Note the shingle brand if you can find it, its age and any discontinued products. On steel roofs, photograph dents with a straightedge and raking light so depth shows.</p>
<h2>Siding, windows and outbuildings</h2>
<p>Walk each side of the house and every outbuilding. Hail driven by wind often damages one or two elevations far more than the others. Photograph cracked vinyl, chipped paint, dented steel and broken window seals. On farms, document every steel building separately.</p>
<h2>Keep a running file</h2>
<ul>
<li>A folder of photos, labeled by date and location.</li>
<li>Copies of every letter and email with the carrier.</li>
<li>Contractor estimates and invoices for temporary repairs.</li>
<li>Your declarations page and policy.</li>
</ul>
<h2>Why storm history matters here</h2>
<p>South Dakota roofs often see more than one hailstorm over their lives. Carriers may argue that some damage came from an earlier storm. Clear dates, collateral damage and photos taken right after the event help separate this storm’s damage from older wear.</p>
<p>Use the <a href="/policyholder-calculators/roof-slope-factor-calculator/">roof squares and slope factor calculator</a> to check the carrier’s quantities once you have their estimate.</p>
""",
    },
    {
        "slug": "derecho-claims-straight-line-wind-versus-tornado",
        "title": "Derecho Claims: Straight-Line Wind Versus Tornado Damage",
        "seo": "Derecho Claims: Straight-Line Wind vs. Tornado",
        "desc": "What South Dakota owners should know about derecho claims: how straight-line wind damage differs from tornadoes and what estimates often miss.",
        "summary": "The May 2022 derecho showed how much damage straight-line wind can do. Here is how those claims work and where they go wrong.",
        "date": "2026-08-25", "read": "6 min",
        "body": """
<p>On May 12, 2022, a derecho raced across eastern South Dakota, bringing hurricane-force gusts to towns that rarely see that kind of wind outside a tornado. Many owners learned for the first time that straight-line wind can do as much damage as a twister.</p>
<h2>What a derecho is</h2>
<p>A derecho is a widespread, long-lived windstorm produced by a fast-moving line of thunderstorms. Unlike a tornado’s narrow, rotating path, derecho winds blow in one general direction over a wide area. Damage can stretch for hundreds of miles.</p>
<h2>Does the label matter for insurance?</h2>
<p>For most property policies, no. Windstorm is usually a covered peril whether the weather service calls it a derecho, a downburst or a tornado. What matters is the policy wording, your deductible, and how well the damage is documented.</p>
<h2>What derecho estimates often miss</h2>
<ul>
<li><strong>Creased shingles</strong> that lifted and fell back in place but lost their seal.</li>
<li><strong>Siding damage</strong> on the windward side, including loose panels and cracks.</li>
<li><strong>Racked outbuildings</strong> whose framing shifted out of square.</li>
<li><strong>Tree damage</strong> and the real cost of removal near structures.</li>
<li><strong>Interior water</strong> from rain driven through wind openings.</li>
</ul>
<h2>Straight-line versus tornado: what the damage shows</h2>
<p>Straight-line damage tends to show debris and fallen trees pointing in one direction. Tornado damage often shows debris thrown in several directions and a narrower, more intense path. Neither pattern changes coverage on its own, but understanding it helps an appraiser explain why damage is where it is.</p>
<h2>After a big wind event</h2>
<p>Report the claim promptly, document every elevation and outbuilding, make temporary repairs and keep receipts. If the carrier’s estimate covers only what is lying on the ground, ask for a closer inspection or a second opinion.</p>
<p>Our <a href="/appraiser-services/tornado-straight-line-wind-appraiser/">wind, tornado and derecho damage appraisal</a> page explains how we value these losses.</p>
""",
    },
    {
        "slug": "black-hills-wildfire-smoke-claim-checklist",
        "title": "A Black Hills Wildfire and Smoke Claim Checklist",
        "seo": "Black Hills Wildfire & Smoke Claim Checklist",
        "desc": "A Black Hills wildfire and smoke claim checklist: documenting smoke, ash and heat damage, contents, trees and living expenses after a fire.",
        "summary": "Whether a fire reached your property or only its smoke did, this checklist helps you document the claim fully.",
        "date": "2026-07-28", "read": "7 min",
        "body": """
<p>Fires like Jasper, Grizzly Gulch, Legion Lake and Schroeder have shown that wildfire is a real risk across the Black Hills. Many homeowners are lucky enough to be spared the flames but still face smoke, ash and heat damage. These partial losses are where claims are most often underpaid.</p>
<h2>First steps</h2>
<ul>
<li>Return only when authorities say it is safe.</li>
<li>Report the claim promptly and ask for the claim number in writing.</li>
<li>Photograph every room, the exterior and the property before cleaning anything.</li>
<li>Ask the carrier whether it wants to inspect before cleaning or testing begins.</li>
</ul>
<h2>Smoke and ash</h2>
<ul>
<li>Note odors room by room, including closets, attics and basements.</li>
<li>Photograph soot on window sills, light fixtures, vents and air filters.</li>
<li>Keep a used HVAC filter as evidence.</li>
<li>Ask whether testing was done and request copies of results.</li>
</ul>
<h2>Heat and ember damage</h2>
<ul>
<li>Check vinyl siding, window frames, skylights and gutters on the side facing the fire for warping or melting.</li>
<li>Look for ember burns on decks, roofs, outdoor furniture and vents.</li>
<li>Photograph any cracked or fogged window glass.</li>
</ul>
<h2>Contents</h2>
<p>Smoke settles into fabrics, mattresses, upholstery and electronics. Make an inventory with item, age, condition and replacement price. Where the carrier proposes cleaning, ask how it will confirm items are restored to pre-loss condition.</p>
<h2>Trees, landscaping and outbuildings</h2>
<p>Many policies have separate limits for trees and landscaping, and outbuildings have their own coverage. Document each burned or scorched tree and every damaged shed, fence and garage.</p>
<h2>Living expenses</h2>
<p>If you cannot live in the home during cleanup or repair, keep every receipt for lodging, meals above your normal costs and mileage. Additional living expense coverage has limits and time frames, so track them.</p>
<p>See our <a href="/appraiser-services/black-hills-wildfire-claim-appraiser/">Black Hills wildfire claim appraisal</a> service for more.</p>
""",
    },
    {
        "slug": "who-to-call-appraiser-adjuster-or-attorney",
        "title": "Who to Call: Appraiser, Public Adjuster or Attorney?",
        "seo": "Appraiser, Public Adjuster or Attorney: Who to Call",
        "desc": "Appraiser, public adjuster or attorney? A guide for South Dakota property owners on which professional fits which claim problem, and when.",
        "summary": "Each professional solves a different problem. Picking the right one first saves time and fees.",
        "date": "2026-06-30", "read": "5 min",
        "body": """
<p>When a claim goes sideways, property owners often call the first professional they hear about. But appraisers, public adjusters and attorneys do very different jobs. Here is how to tell which one fits.</p>
<h2>Call an appraiser when the dispute is about money</h2>
<p>If the insurer has accepted your claim but you disagree about the amount, an appraiser can value the loss and represent you in the appraisal process. The result is a binding award on the amount of loss once two of three panel members sign. Appraisers do not decide coverage and do not give legal advice.</p>
<h2>Call a public adjuster when you need help managing the whole claim</h2>
<p>A licensed public adjuster represents you through the claim process, preparing the claim and negotiating with the insurer. Public adjusters are licensed by the state and are often hired early, sometimes right after a loss, and are typically paid a percentage of the settlement.</p>
<h2>Call an attorney when the problem is legal</h2>
<p>If your claim was denied, the insurer is relying on an exclusion, a deadline is close, or you believe the insurer acted in bad faith, a South Dakota attorney is the right call. Only an attorney can give legal advice and file suit.</p>
<h2>A quick comparison</h2>
<div class="table-wrap"><table><thead><tr><th scope="col">Situation</th><th scope="col">Usually the best first call</th></tr></thead><tbody>
<tr><td>Claim accepted, amount disputed</td><td>Appraiser</td></tr>
<tr><td>Need help preparing and presenting the whole claim</td><td>Public adjuster</td></tr>
<tr><td>Claim denied or coverage disputed</td><td>Attorney</td></tr>
<tr><td>Suit limitation date approaching</td><td>Attorney</td></tr>
<tr><td>Want to know if the carrier’s estimate is fair</td><td>Appraiser for an estimate review</td></tr>
</tbody></table></div>
<h2>Can they work together?</h2>
<p>Yes. Attorneys and public adjusters often bring in appraisers when a claim reaches appraisal. The key is that each professional stays in their own lane.</p>
<p>Not sure where your claim stands? <a href="/get-a-claim-review/">Send us the details</a> and we will tell you honestly whether appraisal fits.</p>
""",
    },
    {
        "slug": "coinsurance-and-farm-building-claims",
        "title": "Coinsurance and Farm Building Claims: What Owners Miss",
        "seo": "Coinsurance and Farm Building Claims Explained",
        "desc": "How coinsurance and scheduled limits affect South Dakota farm building claims, and how to avoid a surprise penalty after a hail or wind loss.",
        "summary": "Farm and commercial policies can reduce a payment when buildings are underinsured. Here is how that works and how to check.",
        "date": "2026-05-26", "read": "6 min",
        "body": """
<p>A July hailstorm can damage every steel building on a farmstead in ten minutes. When the claim is settled, some owners discover their payment is lower than the damage because of a clause they never noticed: coinsurance.</p>
<h2>How coinsurance works</h2>
<p>A coinsurance clause requires you to insure a building for at least a set percentage of its value, often 80% or 90%. If you carry less, the policy may pay only a proportion of the loss. The common formula is the limit you carry divided by the limit you should carry, times the loss, minus the deductible.</p>
<p><em>Illustrative example:</em> a machine shed would cost $250,000 to replace. With an 80% clause, you need $200,000 of coverage. If you carry $150,000, you have 75% of what is required. On a $60,000 loss with a $2,500 deductible, the payment would be about $42,500 instead of $57,500.</p>
<h2>Why farm buildings are vulnerable</h2>
<ul>
<li>Limits are often set when the building was new and never updated.</li>
<li>Steel and construction costs have risen sharply in recent years.</li>
<li>Each building may be scheduled separately with its own limit.</li>
<li>Some older buildings are covered at actual cash value.</li>
</ul>
<h2>What to do now, before a loss</h2>
<ul>
<li>Review each scheduled building’s limit with your agent.</li>
<li>Ask whether coinsurance applies and at what percentage.</li>
<li>Ask about agreed value options, which can suspend coinsurance.</li>
<li>Keep photos and measurements of every building on file.</li>
</ul>
<h2>What to do after a loss</h2>
<p>If the carrier applies a coinsurance penalty, ask for the valuation it used. The building’s value at the time of loss is part of the calculation, and that figure can be questioned. Appraisal can value the loss, and some policies allow it to address value as well, but it cannot change the limit you carried.</p>
<p>Check your numbers with the <a href="/policyholder-calculators/coinsurance-penalty-calculator/">coinsurance penalty calculator</a>.</p>
""",
    },
]
