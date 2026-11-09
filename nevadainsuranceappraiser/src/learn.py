"""Resources: appraisal roadmap (process guide), grouped FAQ, claim dictionary (glossary) and field notes (guides)."""

PROCESS_STEPS = [
    ("Pin down the disagreement", "Before appraisal, make the dispute specific. Put in writing what you believe the insurer’s estimate is missing, attach your contractor’s itemized estimate and photos, and ask for a revised estimate. A clear supplement request resolves many Nevada claims without a panel, and it creates the record a panel will use if it doesn’t."),
    ("Check the policy before you demand", "Find the appraisal paragraph in your policy conditions. Note whether it sets a time limit for naming appraisers, whether the insurer must agree to appraisal or either side can demand it, and whether a sworn proof of loss or other step comes first. Find the suit-limitation clause too, and calendar it."),
    ("Send a written demand", "The demand identifies the claim, states that you and the insurer disagree on the amount of loss, invokes the appraisal provision and names your appraiser or commits to doing so within the policy’s time frame. Send it in a way you can prove, such as email plus certified mail."),
    ("Both sides name appraisers", "Each side selects a competent and impartial appraiser. Your appraiser inspects the property, builds a line-item valuation and exchanges it with the insurer’s appraiser. The two appraisers usually agree on an umpire early, so one is ready if needed. If they can’t agree, either side can ask a Nevada district court to appoint one."),
    ("The appraisers work the differences", "Most of the work happens here. The appraisers walk the property, compare measurements, methods and prices and agree on as many items as they can. Many Nevada appraisals end at this stage with an award signed by both appraisers."),
    ("The umpire decides what’s left", "Items the appraisers can’t settle go to the umpire. Each appraiser submits a position with photos, measurements and pricing. The umpire may inspect or ask questions, then decides each disputed item."),
    ("The award and payment", "An award signed by any two of the three panel members sets the amount of loss. A clear award separates replacement cost, depreciation and actual cash value by coverage. The insurer then pays under the policy, less the deductible and prior payments, with recoverable depreciation paid once repairs are done."),
]

PROCESS_BODY = "".join(f"<h2 id=\"step-{i + 1}\">Step {i + 1}: {t}</h2><p>{p}</p>" for i, (t, p) in enumerate(PROCESS_STEPS)) + """
<div class="note"><b class="h">Who pays</b>Each side pays its own appraiser. Umpire fees are usually split equally. Get any appraiser’s fee arrangement in writing before work begins.</div>
<h2>What appraisal does not do</h2>
<ul>
<li>It doesn’t decide whether a loss is covered or whether an exclusion applies.</li>
<li>It doesn’t award interest, damages for claim handling or attorney’s fees.</li>
<li>It doesn’t necessarily pause your policy’s suit-limitation deadline.</li>
<li>It can’t produce a payment above your policy limits.</li>
</ul>
<p>Nevada law recognizes claims against insurers that unreasonably deny or delay payment, and the state’s unfair claims practices statute sets standards for claim handling. Those are legal questions for a Nevada attorney. Complaints about claim handling can also be filed with the Nevada Division of Insurance. Our role is the valuation.</p>
"""

FAQ = [
    ("Appraisal basics", [
        ("What is insurance appraisal?", "A process written into most property policies for resolving disagreements about the amount of a covered loss. Each side names an appraiser, the appraisers pick an umpire, and an award signed by two of the three sets the amount."),
        ("Is appraisal the same as arbitration?", "They are similar in that a panel reaches a decision, but appraisal is narrower. It is limited to the amount of loss and is usually less formal, with no discovery or witnesses in the courtroom sense."),
        ("Can I demand appraisal, or only the insurer?", "Most policies let either side demand it. Some older or specialty forms require both sides to agree. Read your policy’s appraisal paragraph."),
        ("Does appraisal decide coverage?", "Generally no. The panel values the loss. Whether a loss or part of it is covered is a separate question for the insurer and, if disputed, the courts."),
    ]),
    ("Costs and fees", [
        ("How much does an appraiser cost?", "Fee arrangements vary: flat fees, hourly rates or a percentage of the increase. Get the arrangement in writing before any work starts. Our first conversation is free."),
        ("Who pays the umpire?", "Most policies split the umpire’s fee equally between you and the insurer."),
        ("Is appraisal worth it on a small claim?", "Sometimes not. If the gap is small, fees can absorb most of the gain. Our claim gap & fee estimator shows the break-even point."),
        ("Will the insurer pay my appraiser’s fee?", "Typically not. Each side pays its own appraiser unless the policy or an agreement says otherwise."),
    ]),
    ("Timing and deadlines", [
        ("How long does appraisal take in Nevada?", "Simple residential claims often resolve within two to three months after both appraisers are named. Commercial, smoke-heavy or contents-heavy claims can take longer, especially if an umpire is needed."),
        ("Is there a deadline to demand appraisal?", "Some policies set one; many don’t. But your policy’s suit-limitation clause still runs. Watch it closely and ask a Nevada attorney if it is near."),
        ("What if the insurer doesn’t name its appraiser?", "Many policies set a time limit for naming appraisers. If the insurer misses it, talk to a Nevada attorney about your options."),
        ("Can I still repair my home during appraisal?", "Often yes, after documentation is complete. Protect the evidence first: photos, measurements and samples where relevant. Tell the insurer before you remove damaged materials."),
    ]),
    ("Nevada specifics", [
        ("Who regulates insurance in Nevada?", "The Nevada Division of Insurance, part of the Department of Business and Industry, with offices in Carson City and Las Vegas. It licenses insurers and adjusters and accepts consumer complaints."),
        ("Does Nevada have a FAIR plan?", "As of this writing, Nevada does not operate a state FAIR plan. Homeowners who can’t find standard coverage often turn to surplus lines insurers. Check with the Division of Insurance for current options."),
        ("Is earthquake damage covered by my homeowners policy?", "Usually not. Earthquake coverage is generally a separate policy or endorsement with a percentage deductible."),
        ("What protections exist if my insurer handles the claim unfairly?", "Nevada’s unfair claims practices statute sets standards insurers must follow, and Nevada courts recognize bad-faith claims against insurers in some circumstances. These are legal matters for a Nevada attorney."),
        ("Do you cover rural Nevada?", "Yes. We work in all 16 counties and Carson City, from Clark County to Elko, Humboldt and White Pine counties."),
    ]),
    ("Working with us", [
        ("Are you a public adjuster or a lawyer?", "Neither. We are appraisers and estimators. We don’t negotiate claims outside appraisal and we don’t give legal advice."),
        ("Can you work with my contractor or attorney?", "Yes. We often coordinate with contractors and attorneys, but on an appraisal panel we act independently."),
        ("What should I send for a first review?", "The insurer’s full estimate, your declarations page, any letters from the insurer, your photos and your contractor’s estimate if you have one."),
    ]),
]

GLOSSARY = [
    ("Actual cash value (ACV)", "The value of damaged property at the time of loss, usually replacement cost minus depreciation."),
    ("Additional living expense (ALE)", "Coverage for extra costs of living elsewhere while your home is uninhabitable after a covered loss."),
    ("Amount of loss", "The dollar value of a covered loss. Appraisal resolves disagreements about this figure."),
    ("Appraisal award", "The written decision signed by two of the three panel members setting the amount of loss."),
    ("Appraisal clause", "The policy provision that allows either party, or both, to resolve a disagreement over the amount of loss through appraisal."),
    ("Bad faith", "A legal claim that an insurer unreasonably denied, delayed or underpaid a claim. Decided by courts, not appraisal panels."),
    ("Caliche", "A hard, cemented soil layer common in Southern Nevada that can complicate excavation and foundation work."),
    ("Concrete tile", "A roof covering of molded concrete tiles, very common in Southern Nevada, laid over underlayment on battens or deck."),
    ("Contents", "Personal property such as furniture, clothing and electronics, usually Coverage C on a homeowners policy."),
    ("Coverage A", "Dwelling coverage on a homeowners policy: the house and attached structures."),
    ("Coverage B", "Other structures coverage: detached garages, block walls, fences, sheds and similar."),
    ("Declarations page", "The summary page of your policy listing coverages, limits, deductibles and the policy period."),
    ("Deductible", "The portion of a covered loss you pay before the insurer pays."),
    ("Depreciation", "A reduction in value for age, wear and condition."),
    ("Detach and reset", "Removing an item, such as solar panels or a satellite dish, to allow repairs and reinstalling it afterward."),
    ("Earth movement exclusion", "A common policy exclusion for earthquake, landslide and similar ground movement."),
    ("Ember intrusion", "Wildfire embers entering a building through vents, gaps or openings and igniting material inside."),
    ("Estimate", "An itemized list of repair tasks, quantities and prices used to value a loss."),
    ("Flood", "Surface water from outside rising onto normally dry land. Usually excluded from homeowners policies and covered by separate flood insurance."),
    ("Ice dam", "A ridge of ice at the eaves that traps meltwater, which can back up under roofing and leak inside."),
    ("Impartial appraiser", "An appraiser without a financial interest in the outcome. Many policies require appraisers to be competent and impartial."),
    ("Line item", "A single task or material in an estimate, with quantity, unit and price."),
    ("Matching", "The question of whether repaired areas must reasonably match undamaged areas in color, texture and appearance."),
    ("Microburst", "A sudden, localized thunderstorm downdraft producing damaging straight-line winds."),
    ("Mitigation", "Reasonable steps to prevent further damage after a loss, such as tarping or drying."),
    ("Monsoon", "Southern Nevada’s summer thunderstorm season, usually July through September."),
    ("Nevada Division of Insurance", "The state agency that regulates insurers, licenses adjusters and handles consumer complaints."),
    ("Ordinance or law coverage", "Coverage for added costs of meeting current building codes during repairs."),
    ("Overhead and profit (O&P)", "A general contractor’s charge for coordinating multiple trades, often 10% and 10%."),
    ("Percentage deductible", "A deductible calculated as a percentage of the dwelling limit rather than a fixed dollar amount."),
    ("Proof of loss", "A sworn statement of the claimed loss, often required within a set time after the insurer requests it."),
    ("Recoverable depreciation", "Depreciation held back from the first payment and paid after repairs are completed."),
    ("Replacement cost value (RCV)", "The cost to repair or replace damaged property with like kind and quality, without deduction for depreciation."),
    ("Scope of loss", "The full list of damage and the repairs needed to restore the property."),
    ("Slab leak", "A leak in water lines beneath or within a concrete slab foundation."),
    ("Square", "One hundred square feet of roof surface."),
    ("Stucco", "A cement-based exterior wall finish common in Nevada, applied over lath and building paper."),
    ("Suit limitation", "The policy’s deadline for filing a lawsuit against the insurer."),
    ("Supplement", "A request to add missed items or revise an estimate after the first inspection."),
    ("Surplus lines insurer", "An insurer not licensed as an admitted carrier in the state, allowed to write coverage that admitted carriers won’t."),
    ("Umpire", "The neutral third member of an appraisal panel who decides items the appraisers can’t agree on."),
    ("Underlayment", "The waterproof layer beneath roof tiles or shingles."),
    ("Washoe Zephyr", "A strong afternoon westerly wind common in the Reno area."),
]

POSTS = [
    {
        "slug": "appraisal-clause-nevada-policies", "photo": "signing-papers", "date": "2026-10-14", "read": "7 min",
        "title": "Reading the Appraisal Clause in a Nevada Property Policy",
        "seo": "The Appraisal Clause in Nevada Policies | Field Notes",
        "desc": "How the appraisal clause in a Nevada property policy works: who can demand it, naming appraisers, umpire selection, awards and what it can’t decide.",
        "summary": "A plain-English walk through the paragraph that turns a stalled claim into a three-person panel.",
        "body": """
<p>Almost every Nevada homeowners and commercial property policy contains an appraisal paragraph. Most people never read it until a claim stalls. Here is what it typically says and how each sentence plays out in practice.</p>
<h2>“If we and you fail to agree on the amount of loss…”</h2>
<p>This opening limits appraisal to disagreements about amount. If the insurer has denied the claim entirely or says a specific item isn’t covered, appraisal generally won’t resolve that part. Many claims involve both: the insurer accepts the roof but denies the interior, for example. The panel can value the covered part.</p>
<h2>“…either may demand an appraisal of the loss.”</h2>
<p>Most forms let either side start appraisal with a written demand. A few require both sides to agree. The demand should be clear and provable: identify the claim, state that you disagree on the amount and invoke the provision.</p>
<h2>“Each party will choose a competent and impartial appraiser…”</h2>
<p>Your appraiser should be qualified to value the loss and should not have a financial stake in the repair. Policies often give each side a set number of days, frequently 20, to name its appraiser.</p>
<h2>“The two appraisers will choose an umpire.”</h2>
<p>If the appraisers can’t agree on an umpire, most policies allow either side to ask a court to appoint one. In Nevada, that is typically the district court in the county where the property sits.</p>
<h2>“A decision agreed to by any two will set the amount of loss.”</h2>
<p>This is the binding part. Once two of the three sign, the amount is set. Payment then follows under the policy, less the deductible and prior payments.</p>
<h2>What to do before you demand</h2>
<ol><li>Get the insurer’s full line-item estimate.</li><li>Get your own itemized estimate.</li><li>Organize photos and correspondence by date.</li><li>Find and calendar your policy’s suit-limitation date.</li><li>Run the numbers with the <a href="/toolkit/claim-gap-estimator/">claim gap &amp; fee estimator</a>.</li></ol>
<div class="note"><b class="h">Not legal advice</b>Policy wording varies, and courts interpret it. For questions about your rights or deadlines, talk to a Nevada attorney.</div>
""",
    },
    {
        "slug": "tile-roof-claims-southern-nevada", "photo": "clay-tile-rows", "date": "2026-10-21", "read": "8 min",
        "title": "Tile Roof Claims in Southern Nevada: Breakage, Underlayment and Matching",
        "seo": "Tile Roof Insurance Claims in Southern Nevada",
        "desc": "Why tile roof claims in Las Vegas and Henderson get disputed: broken tile, aged underlayment, discontinued profiles and repair-or-replace math.",
        "summary": "Concrete tile is everywhere in the Las Vegas Valley. Here is why tile roof claims are disputed so often, and what to document.",
        "body": """
<p>Concrete tile covers a large share of the homes built in the Las Vegas Valley since the 1980s. It handles heat well and can last decades. But tile roof claims are among the most disputed we see, for reasons that have little to do with the tile itself.</p>
<h2>The tile isn’t the waterproofing</h2>
<p>On most tile roofs, the underlayment beneath the tile keeps water out. Tile sheds most water and protects the underlayment from sun. After 15 or 20 Southern Nevada summers, older felt underlayment can be brittle and torn. When wind or hail damages tile, the repair often exposes underlayment that can’t be patched cleanly.</p>
<h2>Breakage multiplies</h2>
<p>To replace one broken tile, roofers often lift surrounding courses. Old tile cracks when it is walked on and handled. A repair estimated at 40 tiles can turn into 120. Estimates that price only the visibly broken pieces usually come up short.</p>
<h2>Discontinued profiles and colors</h2>
<p>Many tile profiles and colors from the 1990s and 2000s are no longer made. Salvaged tile may be available; sometimes it isn’t. When replacement tile doesn’t reasonably match, the scope can grow to a full slope or full roof, depending on your policy wording and the facts.</p>
<h2>What to document</h2>
<ul><li>Count broken, cracked and displaced tiles by slope.</li><li>Photograph underlayment wherever tile is missing.</li><li>Note tile manufacturer and profile markings if visible.</li><li>Get a roofer’s written opinion on repairability.</li><li>Record pitch, stories and access issues.</li></ul>
<p>Our <a href="/toolkit/roof-squares-tile-calculator/">roof squares &amp; tile calculator</a> shows what share of the roof your broken tiles represent.</p>
<h2>Wear vs. storm damage</h2>
<p>Insurers often attribute breakage to foot traffic or age. Fresh fractures, impact marks, the pattern of displacement and recent weather data help show cause. That scope question is a good fit for appraisal.</p>
""",
    },
    {
        "slug": "wildfire-smoke-claims-northern-nevada", "photo": "wildfire-night-ridge", "date": "2026-10-28", "read": "7 min",
        "title": "Smoke and Ash Claims After a Northern Nevada Wildfire",
        "seo": "Wildfire Smoke & Ash Claims in Northern Nevada",
        "desc": "What to document and expect after wildfire smoke or ash reaches your home near Reno, Carson City or Lake Tahoe, and why cleaning scopes get disputed.",
        "summary": "Your home didn’t burn, but it smells like it. What to document and why the cleaning scope is usually the fight.",
        "body": """
<p>Northern Nevada lives with wildfire. The Caughlin, Washoe Drive, Waterfall, Little Valley and Davis fires all burned homes, and smoke from fires across the Sierra settles over Reno, Carson City and Lake Tahoe most summers. Many smoke claims come from homes the fire never reached.</p>
<h2>Document early</h2>
<ul><li>Photograph ash on window sills, decks, patio furniture and vehicles.</li><li>Wipe a few surfaces with a white cloth and photograph the residue.</li><li>Check HVAC filters and supply registers.</li><li>Note odor in closets, cabinets and soft furnishings.</li><li>Keep records of evacuation dates and air-quality alerts.</li></ul>
<h2>Why cleaning scopes are disputed</h2>
<p>Insurers often offer a light cleaning and a filter change. A complete scope may include HEPA vacuuming and wet cleaning of all surfaces, duct cleaning or replacement, attic insulation removal, carpet and upholstery cleaning, contents cleaning and odor treatment. The difference can be large, and it is a disagreement about scope and cost, which is what appraisal addresses.</p>
<h2>Testing</h2>
<p>Residue testing by a qualified professional can help define the scope. It is not always necessary, but it can be persuasive when the insurer doubts smoke reached the interior.</p>
<h2>Build an illustrative scope</h2>
<p>Our <a href="/toolkit/smoke-ash-cleaning-estimator/">smoke &amp; ash cleaning estimator</a> shows how a fuller scope adds up, using unit prices you can edit.</p>
""",
    },
    {
        "slug": "earthquake-damage-nevada-coverage", "photo": "aspen-creek", "date": "2026-11-02", "read": "6 min",
        "title": "Earthquake Damage in Nevada: Coverage, Deductibles and Appraisal",
        "seo": "Earthquake Damage Claims in Nevada | Coverage Basics",
        "desc": "Nevada earthquake claims: why homeowners policies usually exclude earth movement, how percentage deductibles work and where appraisal fits.",
        "summary": "Nevada shakes more than most people realize. What a homeowners policy usually covers, what it doesn’t, and how deductibles change the math.",
        "body": """
<p>Nevada is among the most seismically active states in the country. The February 2008 Wells earthquake damaged older masonry buildings in Elko County, and the May 2020 Monte Cristo Range earthquake, centered in remote west-central Nevada, was the state’s largest in decades. Western Nevada, including Reno and Carson City, sits along active fault zones.</p>
<h2>What a homeowners policy usually says</h2>
<p>Most homeowners policies exclude earth movement, including earthquake. Some cover ensuing fire or water damage caused by an earthquake, such as a gas-line fire or a burst pipe. Earthquake damage to the structure itself generally requires a separate earthquake policy or endorsement.</p>
<h2>Percentage deductibles</h2>
<p>Earthquake coverage usually carries a deductible stated as a percentage of the dwelling limit, commonly 5% to 25%. On a $400,000 home, a 15% deductible is $60,000. Use our <a href="/toolkit/percentage-deductible-calculator/">percentage deductible calculator</a> to see your figure.</p>
<h2>Where appraisal fits</h2>
<p>Earthquake policies often contain their own appraisal provision. Disputes tend to involve cracking in stucco, drywall and foundations, and whether cracks are new or pre-existing. Documentation of the home’s condition before an event helps a great deal.</p>
<div class="note"><b class="h">Coverage questions</b>Whether a particular crack or ensuing loss is covered is a coverage question. Talk to your agent or a Nevada attorney.</div>
""",
    },
    {
        "slug": "monsoon-water-claims-rain-vs-flood", "photo": "monsoon-rain-shaft", "date": "2026-09-30", "read": "6 min",
        "title": "Monsoon Water Claims: Wind-Driven Rain vs. Flood",
        "seo": "Monsoon Water Claims in Nevada: Rain vs. Flood",
        "desc": "How Nevada monsoon storms create both covered rain damage and excluded flood damage at the same home, and how to document the difference room by room.",
        "summary": "One storm, two kinds of water, very different coverage. How to document monsoon damage so the covered part gets paid.",
        "body": """
<p>Southern Nevada’s monsoon storms can drop more than an inch of rain in under an hour. In 1999, 2022 and again during Tropical Storm Hilary’s remnants in 2023, water moved through streets and into homes across the Las Vegas Valley. Often a single home has two kinds of water damage.</p>
<h2>Rain through the roof or walls</h2>
<p>When wind lifts tile, tears flashing or drives rain past windows and stucco, water that enters through those openings is typically covered under a homeowners policy, subject to its terms.</p>
<h2>Water from outside, at ground level</h2>
<p>Water flowing across the yard and under doors is usually treated as flood and excluded from homeowners policies. Flood insurance through the National Flood Insurance Program or a private flood policy covers it if you have one.</p>
<h2>Documenting the difference</h2>
<ul><li>Photograph roof and wall openings and ceiling stains from above.</li><li>Mark water lines on walls with tape and photograph them.</li><li>Note which rooms were wet from above and which from the floor.</li><li>Keep mitigation logs that show moisture readings by room.</li></ul>
<p>That room-by-room record lets an appraisal panel value the covered portion clearly, while coverage questions stay with the insurer and, if needed, the courts.</p>
""",
    },
    {
        "slug": "appraiser-public-adjuster-or-attorney-nevada", "photo": "handshake-table", "date": "2026-09-16", "read": "6 min",
        "title": "Appraiser, Public Adjuster or Attorney? Choosing Help in Nevada",
        "seo": "Appraiser vs. Public Adjuster vs. Attorney in Nevada",
        "desc": "Disputed Nevada property claim? What an appraiser, a licensed public adjuster and an insurance attorney each do, and when to call which one.",
        "summary": "Three kinds of help for a disputed claim, each built for a different problem. Picking the right one first saves time and money.",
        "body": """
<p>Property owners with a disputed claim often hear three suggestions: hire an appraiser, hire a public adjuster or hire a lawyer. Each solves a different problem.</p>
<h2>Appraiser</h2>
<p>An appraiser works within the policy’s appraisal clause on one question: the amount of loss. Best when coverage is accepted and the dispute is about scope or price. The result is a binding award on the amount.</p>
<h2>Public adjuster</h2>
<p>A public adjuster is licensed by the Nevada Division of Insurance to represent policyholders in preparing, presenting and negotiating claims. Best early in a claim, especially large or complex ones, when you want someone to manage the whole process.</p>
<h2>Attorney</h2>
<p>An insurance attorney handles legal disputes: denials, coverage arguments, bad-faith claims and approaching lawsuit deadlines. Best when the problem isn’t the number but whether the insurer has to pay at all, or how it handled the claim.</p>
<h2>Quick comparison</h2>
<div class="table-wrap"><table><thead><tr><th>Question</th><th>Appraiser</th><th>Public adjuster</th><th>Attorney</th></tr></thead><tbody>
<tr><th>Main job</th><td>Value the loss</td><td>Manage and negotiate the claim</td><td>Legal disputes</td></tr>
<tr><th>Best timing</th><td>Coverage accepted, amount disputed</td><td>From the start</td><td>Denials, deadlines, bad faith</td></tr>
<tr><th>Result</th><td>Binding award on amount</td><td>Negotiated settlement</td><td>Settlement or judgment</td></tr>
</tbody></table></div>
<p>If you’re not sure which you need, call us. If appraisal isn’t the right tool, we’ll say so.</p>
""",
    },
]
