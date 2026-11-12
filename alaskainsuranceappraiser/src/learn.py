"""Process guide, FAQ, glossary and guide articles for Alaska Insurance Appraiser."""

PROCESS_STEPS = [
    ("Pin down the disagreement", "Appraisal resolves the amount of loss. Before anything else, confirm that coverage is accepted and that the dispute is about scope or price. Get the carrier's full itemized estimate in writing."),
    ("Build your own number", "Get an independent, line-item estimate that reflects current costs where the property is, including freight, travel and seasonal access when they apply."),
    ("Send a written demand", "Follow your policy's appraisal clause. Most require a written demand. Keep a copy and proof of delivery."),
    ("Name the appraisers", "Each side appoints its own appraiser, often within a set number of days of the demand. Your appraiser should meet the policy's independence requirement."),
    ("Select an umpire", "The two appraisers try to agree on a neutral umpire. If they cannot, many policies let either side ask a court in the state where the property is located to appoint one."),
    ("Appraisers work the differences", "The appraisers inspect, exchange estimates and go line by line. Most items are usually resolved at this stage."),
    ("Umpire decides what is left", "Remaining items go to the umpire with supporting photos, measurements and pricing. The umpire may inspect the property."),
    ("Signed award and payment", "An award signed by any two of the three sets the amount of loss. Payment then follows under the policy terms, subject to deductibles, limits and depreciation."),
]

PROCESS_BODY = """
<p>The appraisal clause turns an open-ended disagreement over the value of a claim into a defined process with a binding result on the amount. Here is how it typically works in Alaska, step by step. Your policy's wording always controls, so read your own appraisal clause alongside this guide.</p>
<h2>Before you start: is appraisal the right tool?</h2>
<p>Appraisal is designed for disputes over how much a covered loss is worth. It is generally not the place to resolve whether the loss is covered at all, whether an exclusion applies, or how the insurer handled the claim. Those questions may need an Alaska attorney. If coverage is accepted and the gap is about scope or price, appraisal may fit well.</p>
<ol class="steps">{steps}</ol>
<h2>How long it takes</h2>
<p>A straightforward residential appraisal often resolves within two to three months after both appraisers are named. Larger commercial claims, contents-heavy files, umpire hearings and properties that are hard to reach in winter can take longer.</p>
<h2>What it costs</h2>
<p>Each side typically pays its own appraiser, and the umpire's fee is usually split evenly. Fees vary by claim size and complexity. Get your appraiser's fee in writing before work begins.</p>
<h2>Common mistakes</h2>
<ul>
<li>Invoking appraisal before the full scope of damage is known</li>
<li>Appointing an appraiser who has a financial interest in the repair</li>
<li>Missing a deadline in the appraisal clause or the suit-limitation clause</li>
<li>Signing an award without checking how replacement cost, actual cash value and depreciation are stated</li>
<li>Expecting appraisal to resolve a coverage denial</li>
</ul>
<div class="note"><b class="h">About Alaska law</b>Alaska's insurance code includes a section on unfair claim settlement practices, and Alaska courts have recognized bad-faith claims against insurers in some circumstances. Whether either applies to a particular claim is a legal question for an Alaska attorney. Appraisers value losses; they do not give legal advice.</div>
"""

FAQ = [
    ("The basics", [
        ("What is insurance appraisal?", "A process in most property policies for resolving disagreements about the amount of a covered loss. Each side appoints an appraiser, the appraisers choose an umpire, and an award signed by two of the three sets the amount."),
        ("Is appraisal the same as arbitration?", "They are similar in that a neutral decides, but appraisal is usually limited to the amount of loss and tends to be less formal. Alaska courts and policy language determine how it works in a given case."),
        ("Who can invoke appraisal?", "Either the policyholder or the insurer, under the terms of the policy. A written demand is usually required."),
        ("Does my Alaska policy have an appraisal clause?", "Most homeowner, condo, landlord and commercial property policies do. Look in the conditions section for a paragraph titled Appraisal."),
    ]),
    ("Costs and timing", [
        ("How much does appraisal cost?", "Each side pays its own appraiser, and the umpire's fee is usually split. Total cost depends on the size and complexity of the claim and, in Alaska, on travel to the property."),
        ("How long does it take?", "Often two to three months for a simple residential claim after appraisers are named. Larger, remote or umpire-heavy claims can take longer."),
        ("When is the gap too small for appraisal?", "If the costs would absorb most of the expected increase, a documented supplement request is often better. Our gap and fee estimator helps you check."),
        ("Can I invoke appraisal after accepting a payment?", "Often yes, depending on the policy and deadlines. Accepting a partial payment does not necessarily close a claim, but read any release carefully."),
    ]),
    ("Alaska-specific questions", [
        ("Who regulates insurance in Alaska?", "The Alaska Division of Insurance, part of the Department of Commerce, Community, and Economic Development. It handles consumer complaints and licenses insurers and adjusters."),
        ("Does Alaska have a FAIR plan or a state wind pool?", "No. Alaska does not operate a FAIR plan or a wind pool. Owners who cannot find standard coverage may turn to the surplus lines market."),
        ("Does my homeowner policy cover earthquakes?", "Usually not. Earthquake coverage is generally added by endorsement or separate policy and often carries a percentage deductible."),
        ("Is flood covered?", "Surface flooding, storm surge and glacial outburst flooding are typically excluded from homeowner policies and insured separately, for example through the National Flood Insurance Program."),
        ("Can you work on properties off the road system?", "Yes. Remote properties need travel planning, and repair estimates should account for freight, travel and seasonal access."),
    ]),
    ("Working with us", [
        ("Are you a public adjuster or a law firm?", "No. We provide appraisal, estimating and umpire services. We do not negotiate claims outside appraisal and we do not give legal advice."),
        ("Can you be my appraiser and the umpire?", "No. We serve in one role per claim and disclose any prior involvement."),
        ("What should I send for a free review?", "Your declarations page, the carrier's full estimate, photos and any contractor estimates."),
    ]),
]

GLOSSARY = [
    ("Actual cash value (ACV)", "Replacement cost minus depreciation. Often the first payment on a replacement cost policy."),
    ("Additional living expense (ALE)", "Coverage for extra costs of living elsewhere while your home is being repaired after a covered loss."),
    ("Appraisal award", "The written decision signed by two of the three panel members that sets the amount of loss."),
    ("Appraisal clause", "The policy condition that lets either side demand appraisal when they disagree on the amount of loss."),
    ("Appraiser", "The person each side appoints to value the loss. Policies often require appraisers to be competent and independent."),
    ("Arctic entry", "An enclosed entry vestibule common in Alaska homes that limits heat loss. It is part of the dwelling for claim purposes."),
    ("Barge freight", "Shipping materials by barge to coastal or river communities, often on a seasonal schedule. A real cost in remote repairs."),
    ("Borough", "Alaska's equivalent of a county. The state has 19 organized boroughs plus the Unorganized Borough."),
    ("Census area", "One of 11 statistical divisions of Alaska's Unorganized Borough, used where no borough government exists."),
    ("Coverage A", "Dwelling coverage for the house itself and attached structures."),
    ("Coverage B", "Other structures coverage for detached garages, shops, sheds and fences."),
    ("Coverage C", "Personal property coverage for contents."),
    ("Declarations page", "The summary page of your policy listing coverages, limits, deductibles and endorsements."),
    ("Deductible", "The part of a covered loss you pay before the policy pays."),
    ("Depreciation", "A reduction in value for age, wear and condition, used to calculate actual cash value."),
    ("Earth movement exclusion", "A common exclusion for earthquake, landslide, settlement and similar ground movement."),
    ("Earthquake endorsement", "An addition to a policy that provides earthquake coverage, usually with a percentage deductible."),
    ("Endorsement", "A written change to a policy that adds, removes or modifies coverage."),
    ("Estimate", "An itemized list of the work and materials needed to repair a loss, with quantities and prices."),
    ("Glacial outburst flood", "A sudden release of water dammed by or beside a glacier, such as the floods on Juneau's Mendenhall River."),
    ("Holdback", "Recoverable depreciation withheld until repairs are complete."),
    ("Ice dam", "A ridge of ice at the eaves that traps meltwater, which can then leak into the home."),
    ("Ice and water shield", "A self-adhering roof membrane installed in vulnerable areas such as eaves and valleys to resist leaks."),
    ("Line item", "A single entry on an estimate, such as a quantity of drywall or roofing at a unit price."),
    ("Matching", "The question of whether repaired areas must reasonably match undamaged areas, which can expand the scope."),
    ("Mitigation", "Steps taken to prevent further damage, such as tarping, drying, heating or snow removal."),
    ("Named peril", "A cause of loss specifically listed as covered in a policy."),
    ("Ordinance or law coverage", "Coverage for added costs of meeting current building codes when repairing a damaged building."),
    ("Overhead and profit (O&P)", "A general contractor's charges for managing a project, often expressed as percentages."),
    ("Percentage deductible", "A deductible calculated as a percentage of a coverage limit rather than a flat dollar amount."),
    ("Permafrost", "Ground that stays frozen for two or more years. Thaw-related settlement is usually excluded from coverage."),
    ("Proof of loss", "A sworn statement of the amount claimed, which the insurer may request within a set time."),
    ("Public adjuster", "A licensed professional who represents a policyholder in presenting and negotiating a claim."),
    ("Recoverable depreciation", "Depreciation the policy will pay once repairs or replacement are completed."),
    ("Replacement cost value (RCV)", "The cost to repair or replace with new materials of like kind and quality, without deduction for depreciation."),
    ("Scope of loss", "The full description of the damaged areas and items, and the work needed to repair them."),
    ("Snow load", "The weight of accumulated snow and ice on a roof, measured in pounds per square foot."),
    ("Steep charge", "An additional cost for working on steep roofs, typically above a certain pitch."),
    ("Suit limitation clause", "The policy condition limiting how long you have to file a lawsuit against the insurer."),
    ("Supplement", "A request for additional payment for items missed or underpaid in the original estimate."),
    ("Surplus lines", "Insurance written by insurers not licensed in the state, used for risks the standard market does not cover."),
    ("Umpire", "The neutral third member of an appraisal panel who decides items the two appraisers cannot agree on."),
    ("Unorganized Borough", "The large part of Alaska not within an organized borough, divided into census areas for statistics."),
    ("Weight of ice, snow or sleet", "A named peril in many homeowner policies covering damage caused by the weight of accumulated snow and ice."),
]

POSTS = [
    {
        "slug": "reading-an-alaska-appraisal-clause",
        "title": "Reading the Appraisal Clause in Your Alaska Policy",
        "seo": "How to Read the Appraisal Clause in Your Policy",
        "desc": "A plain-English walk through the appraisal clause in an Alaska homeowners or commercial policy: demands, deadlines, umpires and the award.",
        "summary": "The appraisal clause is a short paragraph with big consequences. Here is what each sentence usually means.",
        "date": "2026-11-02", "read": "7 min", "photo": "consultation",
        "body": """
<p>Most Alaska property policies contain a paragraph titled <em>Appraisal</em>, usually in the conditions section. It is only a few sentences long, but it sets out a process that can bind you and the insurer to a dollar amount. Here is how to read it.</p>
<h2>1. The trigger</h2>
<p>The clause usually begins with something like: "If you and we fail to agree on the amount of loss, either may demand an appraisal of the loss." The key words are <strong>amount of loss</strong>. Appraisal is about value, not whether the loss is covered.</p>
<h2>2. The demand</h2>
<p>Most clauses require a written demand. Some say nothing about format. Send the demand in a way you can prove it was received, and keep a copy.</p>
<h2>3. Naming appraisers</h2>
<p>Each side chooses its own appraiser, often within a set period such as 20 days after the demand. Many policies require the appraiser to be "competent and independent" or "disinterested." That generally rules out someone with a financial stake in the repair.</p>
<h2>4. The umpire</h2>
<p>The two appraisers choose an umpire. If they cannot agree within a set time, either side can usually ask a court of record in the state where the property is located to appoint one.</p>
<h2>5. The award</h2>
<p>The appraisers separately state the amount of loss. If they agree, that amount is set. If not, they submit their differences to the umpire. A written decision signed by any two sets the amount of loss.</p>
<h2>6. Costs</h2>
<p>Each side pays its own appraiser. Umpire costs are usually shared equally.</p>
<h2>What the clause usually does not say</h2>
<ul><li>It typically does not let the panel decide coverage.</li><li>It does not usually change deadlines in other parts of the policy, such as the suit-limitation clause.</li><li>It does not create a right to attorney's fees.</li></ul>
<div class="note"><b class="h">Not legal advice</b>This article describes common policy language. Your policy controls, and legal questions should go to an Alaska attorney.</div>
""",
    },
    {
        "slug": "earthquake-claims-after-an-alaska-quake",
        "title": "Earthquake Claims After an Alaska Quake: What Owners Learned in 2018",
        "seo": "Alaska Earthquake Insurance Claims: A Practical Guide",
        "desc": "What Alaska owners learned from the 2018 Anchorage earthquake: endorsements, percentage deductibles, documenting cracks and when appraisal helps.",
        "summary": "Earthquake coverage, high deductibles and cracked drywall: practical lessons from the 2018 Anchorage earthquake.",
        "date": "2026-10-20", "read": "8 min", "photo": "quake-damage",
        "body": """
<p>On November 30, 2018, a magnitude 7.1 earthquake struck just north of Anchorage. Damage spread across the Municipality of Anchorage and the Mat-Su. For owners who carried earthquake coverage, the claims that followed raised several recurring issues.</p>
<h2>Earthquake coverage is separate</h2>
<p>Standard homeowner policies typically exclude earth movement. Coverage usually comes from an endorsement or separate policy. If you are not sure whether you have it, check your declarations page for an earthquake endorsement and deductible.</p>
<h2>Percentage deductibles</h2>
<p>Earthquake deductibles are usually a percentage of the coverage limit. On a home insured for $400,000, a 15% deductible is $60,000. That means small differences in the estimate can decide whether anything is paid. These figures are illustrative.</p>
<h2>Cracks: quake, settlement or age?</h2>
<p>Many homes had cracks before the quake. Carriers often attribute cracks to settlement, frost heave or age. Pre-quake photos, real estate listing photos and inspection reports can help show what changed. Engineers may be needed for foundation questions.</p>
<h2>Drywall scope</h2>
<p>Earthquake drywall damage is often scattered across many rooms. Estimates that repair isolated cracks without accounting for continuous wall and ceiling planes, texture matching and paint can fall short.</p>
<h2>When appraisal helps</h2>
<p>If coverage is accepted and the dispute is about the extent and cost of repairs, appraisal may help. If the carrier says the damage was not caused by the quake, that may involve coverage questions that an attorney should review.</p>
<h2>Preparing for the next one</h2>
<ul><li>Photograph your home's interior and foundation now, and save the files off-site.</li><li>Review your earthquake coverage and deductible.</li><li>Know where your gas, water and electrical shutoffs are.</li></ul>
""",
    },
    {
        "slug": "snow-load-and-ice-dam-claims-before-the-thaw",
        "title": "Snow Load and Ice Dam Claims: Document Before the Thaw",
        "seo": "Snow Load & Ice Dam Insurance Claims: What to Document",
        "desc": "How to document snow load and ice dam damage for an insurance claim in Alaska: snow depth, photos, attic checks and the costs that get missed.",
        "summary": "Snow and ice disappear. The evidence you need for a strong claim disappears with them unless you record it first.",
        "date": "2026-10-06", "read": "6 min", "photo": "snow-roof-house",
        "body": """
<p>Snow load and ice dam claims have a timing problem. By the time damage is obvious, the snow that caused it may be gone. Here is what to record while it is still there.</p>
<h2>Record the snow</h2>
<ul><li>Photograph the roof from several angles, including drifts and valleys.</li><li>Measure depth in a few places with a ruler or yardstick in the photo.</li><li>Note the type of snow: powder, settled, wet or ice layers.</li><li>Record the date and recent weather, such as rain on snow.</li></ul>
<p>Our <a href="/appraisal-tools/roof-snow-load-calculator/">roof snow load calculator</a> turns those measurements into an estimated load.</p>
<h2>Check inside</h2>
<ul><li>Look for new cracks in drywall, especially near the ceiling.</li><li>Check doors and windows that suddenly stick.</li><li>Look in the attic for wet insulation, frost or bent framing.</li><li>Photograph stains and leaks as they appear.</li></ul>
<h2>Keep receipts</h2>
<p>Snow removal, shoring, heat tape, temporary tarps and drying equipment may be reimbursable as reasonable steps to protect the property. Keep receipts and photos of the work.</p>
<h2>Costs that are often missed</h2>
<ul><li>Removal and replacement of wet insulation and vapor barrier</li><li>Framing repairs found only after opening ceilings</li><li>Code-required upgrades during structural repair</li><li>Winter conditions: heat, enclosure and protection</li></ul>
<h2>Maintenance arguments</h2>
<p>Insurers sometimes argue that ice dams result from poor ventilation or insulation. Whether that affects coverage depends on the policy. Once coverage is accepted, appraisal can help resolve the amount.</p>
""",
    },
    {
        "slug": "pricing-repairs-off-the-road-system",
        "title": "Pricing Repairs Off the Road System: Freight, Barges and Travel",
        "seo": "Remote Alaska Repair Costs in Insurance Estimates",
        "desc": "Why remote Alaska repairs cost more and how freight, barge schedules, crew travel and short seasons should appear in an insurance estimate.",
        "summary": "Most Alaska communities are not on the road system. Here is how freight, barges and travel should show up in a claim estimate.",
        "date": "2026-09-22", "read": "6 min", "photo": "storm-response",
        "body": """
<p>Standard estimating software prices labor and materials for a city. For a home in a western Alaska village, a lodge on a fly-in lake or a cabin across Kachemak Bay, those prices are only the beginning.</p>
<h2>Freight</h2>
<p>Materials may travel by barge, air freight or seasonal ice road. Each has costs: freight charges by weight or volume, handling at each transfer, and minimums. Barge schedules may mean materials must be ordered months ahead.</p>
<h2>Crew travel</h2>
<p>When local labor is not available, crews travel in. That means airfare, lodging, per diem and travel time. Projects may be scheduled around flight availability and weather.</p>
<h2>Equipment</h2>
<p>Lifts, dumpsters and specialty tools may need to be shipped in and out. Debris may need to be backhauled.</p>
<h2>Seasons</h2>
<p>Building seasons can be short. If repairs cannot start until summer, temporary protection may be needed for months.</p>
<h2>How to document it</h2>
<ul><li>Get written freight quotes from carriers serving the community.</li><li>Get travel quotes for crews.</li><li>Ask contractors who work in the area for estimates that list remote costs separately.</li><li>Keep receipts for temporary protection.</li></ul>
<p>When these costs are listed separately and supported, they are easier for an insurer or appraisal panel to evaluate than a single unexplained markup.</p>
""",
    },
    {
        "slug": "appraiser-public-adjuster-or-attorney-in-alaska",
        "title": "Appraiser, Public Adjuster or Attorney: Who to Call in Alaska",
        "seo": "Appraiser vs Public Adjuster vs Attorney in Alaska",
        "desc": "When to call an insurance appraiser, a public adjuster or an attorney for an Alaska property claim, and how their roles and costs differ.",
        "summary": "Each solves a different problem. Picking the right help first saves time and money.",
        "date": "2026-09-08", "read": "5 min", "photo": "consultation-laptop",
        "body": """
<p>Property owners with a disputed claim often wonder who to call. Here is how the three main options differ.</p>
<h2>Insurance appraiser</h2>
<p>An appraiser values the loss within the policy's appraisal process. Best when coverage is accepted and the dispute is about scope or price. Result: a binding award on the amount of loss once two of three panel members sign.</p>
<h2>Public adjuster</h2>
<p>A public adjuster, licensed through the Alaska Division of Insurance, represents the policyholder in preparing and negotiating the claim. Often involved early, from first notice. Usually paid a percentage of the settlement, subject to state rules.</p>
<h2>Attorney</h2>
<p>An attorney handles legal disputes: denials, coverage questions, bad-faith concerns and lawsuits. If the claim was denied, a deadline is close, or you believe the claim was handled improperly, an Alaska attorney is often the right first call.</p>
<h2>Quick guide</h2>
<ul><li><strong>Coverage accepted, number disputed:</strong> appraiser, often after an estimate review.</li><li><strong>Large, complex claim from the start:</strong> public adjuster.</li><li><strong>Denial, coverage dispute or deadline:</strong> attorney.</li></ul>
<p>We will tell you honestly if your situation calls for someone else.</p>
""",
    },
]
