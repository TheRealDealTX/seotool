"""Resource center: appraisal process guide, grouped FAQ, glossary and articles."""

PROCESS_STEPS = [
    ("Put the disagreement on paper", "Appraisal starts with a claim that has been accepted, at least in part. The carrier has inspected and issued an estimate, and you believe it’s too low. Write down what you think is missing, attach your contractor’s or estimator’s number and the photos that support it, and send it to the adjuster. Many disputes end here, when a supplement is approved."),
    ("Make the written demand", "If the gap remains, either side can demand appraisal in writing. The demand should identify the claim, say the parties disagree on the amount of loss, invoke the appraisal provision and name your appraiser or commit to doing so on time. Send it in a way you can prove, such as certified mail plus email. Check first whether your policy requires a sworn proof of loss or another step."),
    ("Each side names an appraiser", "Under language based on New Jersey’s standard fire policy, each side commonly has 20 days from the demand to name a competent and disinterested appraiser. Your appraiser reviews the file, inspects the property and builds an independent valuation. The carrier’s appraiser does the same."),
    ("The appraisers choose an umpire", "The two appraisers pick a neutral umpire, often early so one is ready if needed. If they can’t agree within the policy’s window, commonly 15 days, either side can ask a judge to appoint one. In New Jersey that request goes to the Superior Court."),
    ("The appraisers work the differences", "This is where most of the work happens. The appraisers compare scope, measurements and pricing, often walking the property together, and agree on as many line items as they can. Many panels finish here with both appraisers signing an agreed award."),
    ("The umpire decides what’s left", "Items the appraisers can’t settle go to the umpire. Each appraiser submits a position with evidence. The umpire may inspect, ask questions or hold an informal meeting, then decides each disputed item."),
    ("The award is signed and paid", "An award signed by any two of the three sets the amount of loss. A good award separates replacement cost, depreciation and actual cash value by coverage. The insurer then pays under the policy, less the deductible and prior payments, with recoverable depreciation paid once repairs are done."),
]

PROCESS_BODY = "".join(f"<h2 id=\"step-{i + 1}\">Step {i + 1}: {t}</h2><p>{p}</p>" for i, (t, p) in enumerate(PROCESS_STEPS)) + """
<div class="note"><b class="h">Fees</b>Each side pays its own appraiser. The umpire’s fee is usually split equally. Ask any appraiser, including us, to put fee terms in writing before you sign.</div>
<h2>What appraisal won’t do</h2>
<ul>
<li>It won’t decide whether a loss is covered.</li>
<li>It won’t award interest, penalties or attorney’s fees.</li>
<li>It won’t automatically pause your policy’s suit-limitation period.</li>
<li>It won’t produce a payment higher than your policy limits.</li>
</ul>
<h2>Where New Jersey law fits in</h2>
<p>The New Jersey Department of Banking and Insurance regulates insurers and licenses public adjusters. State law and regulations on unfair claim settlement practices set standards for prompt, fair claim handling, and New Jersey courts have recognized bad-faith claims against insurers in limited circumstances. Those are legal questions. If you think your claim has been handled unfairly, talk to a New Jersey attorney or file a complaint with the Department. Our role is valuation.</p>
"""

FAQ = [
    ("The basics", [
        ("What is insurance appraisal?", "A process written into most property policies for settling disagreements about the amount of a covered loss. Each side names an appraiser, the appraisers choose an umpire, and an award signed by any two of the three sets the amount."),
        ("Is appraisal the same as arbitration?", "No. Appraisal is narrower. It decides the amount of loss, not legal questions such as coverage or bad faith, and it’s usually less formal than arbitration."),
        ("Does every New Jersey policy have an appraisal clause?", "Most homeowners, condo, landlord and commercial property policies do. Flood policies under the National Flood Insurance Program follow federal rules and handle appraisal differently. Check the conditions section of your policy."),
        ("Can appraisal decide whether my damage is covered?", "Generally no. Coverage questions are for the insurer, an attorney and, if needed, a court. Appraisal values the loss."),
    ]),
    ("Timing and deadlines", [
        ("How long does appraisal take?", "Many residential claims resolve within two to four months after both appraisers are named. Large commercial losses and claims that need an umpire decision can take longer."),
        ("How long do I have to demand appraisal?", "Policies rarely set a deadline to demand appraisal itself, but other deadlines keep running, including the suit-limitation period, which is often 12 months in New Jersey. Don’t wait to protect those dates."),
        ("Does demanding appraisal stop the suit deadline?", "Not automatically. New Jersey courts have allowed the suit period to pause while a claim is under review, but how that applies to you is a question for an attorney."),
    ]),
    ("Costs", [
        ("How are appraisers paid?", "Each side pays its own appraiser. Fees may be flat, hourly or a percentage of the increase. The umpire is usually split equally. Get the terms in writing."),
        ("Is appraisal worth it for a small gap?", "Often not. When the gap is a few thousand dollars, fees can eat most of the gain. Our claim gap estimator shows the net at different outcomes."),
        ("Is your first consultation free?", "Yes. We review your situation and tell you honestly whether appraisal is likely to help."),
    ]),
    ("New Jersey specifics", [
        ("Who regulates insurance in New Jersey?", "The New Jersey Department of Banking and Insurance. It handles consumer complaints, licenses insurance professionals including public adjusters, and oversees insurers doing business in the state."),
        ("What is the New Jersey FAIR Plan?", "The New Jersey Insurance Underwriting Association offers basic property coverage to owners who can’t find it in the regular market, including some shore properties. Its policies include appraisal language."),
        ("Do hurricane deductibles apply to nor’easters?", "Usually not. Hurricane deductibles apply only when the policy’s trigger is met. After Sandy, the state said they shouldn’t apply because Sandy wasn’t a hurricane at landfall. Read your endorsement."),
        ("Are you public adjusters?", "No. Public adjusters are licensed by the state to handle and negotiate claims. We work as appraisers within the appraisal clause, as estimators and as umpires."),
    ]),
    ("Working with us", [
        ("What should I send for a first review?", "The declarations page, the carrier’s full estimate, any letters from the carrier, your photos and your contractor’s estimate if you have one."),
        ("Do you travel to the property?", "Yes. We inspect throughout New Jersey, from Sussex County to Cape May."),
        ("Will you tell me if appraisal isn’t right?", "Yes. If an attorney, a public adjuster or a simple supplement request would serve you better, we’ll say so."),
    ]),
]

GLOSSARY = [
    ("Actual cash value (ACV)", "Replacement cost minus depreciation. Many policies pay ACV first and the rest after repairs."),
    ("Additional living expense (ALE)", "Coverage for extra costs of living elsewhere while your home is being repaired."),
    ("Amount of loss", "The dollar value of covered damage. It’s the question an appraisal panel decides."),
    ("Appraisal clause", "The policy provision that lets either side demand appraisal when they disagree on the amount of loss."),
    ("Appraisal award", "The written decision that sets the amount of loss, binding when signed by any two of the three panel members."),
    ("Appraiser", "The person each side names to value the loss. Policies usually require a competent and disinterested appraiser."),
    ("Coverage A", "Dwelling coverage for the house itself and attached structures."),
    ("Coverage B", "Other-structures coverage for detached garages, sheds and fences."),
    ("Coverage C", "Personal property coverage for contents."),
    ("Coverage D", "Loss-of-use coverage, including additional living expenses."),
    ("Debris removal", "Coverage for removing debris after a covered loss, often with separate limits for trees."),
    ("Declarations page", "The summary page of your policy listing limits, deductibles and endorsements."),
    ("Deductible", "The part of a covered loss you pay before the policy pays."),
    ("Depreciation", "The reduction in value for age and wear. Recoverable depreciation is paid after repairs under a replacement cost policy."),
    ("DOBI", "The New Jersey Department of Banking and Insurance, the state’s insurance regulator."),
    ("Endorsement", "A policy amendment that adds, removes or changes coverage."),
    ("FAIR Plan", "A state-backed insurer of last resort. In New Jersey it’s the New Jersey Insurance Underwriting Association."),
    ("Flood exclusion", "The homeowners policy provision that excludes surface water, storm surge and related flooding."),
    ("Holdback", "Recoverable depreciation the insurer holds until repairs are completed."),
    ("Hurricane deductible", "A separate deductible, often a percentage of Coverage A, that applies when the policy’s hurricane trigger is met."),
    ("Ice dam", "A ridge of ice at the eaves that traps meltwater, which can back up under shingles into the home."),
    ("Line item", "A single priced entry in an estimate, such as one square of shingles."),
    ("Matching", "Whether repaired areas must reasonably match undamaged areas in color, texture and style."),
    ("Mitigation", "Steps taken to prevent further damage after a loss, such as tarping or drying."),
    ("NFIP", "The National Flood Insurance Program, the federal program that writes most flood insurance."),
    ("Nor’easter", "A coastal storm with northeast winds, common in New Jersey in fall and winter."),
    ("Ordinance or law coverage", "Coverage for added costs of meeting building codes during repairs."),
    ("Overhead and profit (O&P)", "A general contractor’s charge for coordinating a repair, often 10% plus 10%."),
    ("Proof of loss", "A sworn statement of the amount claimed, sometimes required by the insurer."),
    ("Public adjuster", "A state-licensed professional who represents policyholders in handling and negotiating claims."),
    ("Replacement cost value (RCV)", "The cost to repair or replace damaged property with similar materials, without depreciation."),
    ("Reservation of rights", "A letter in which the insurer investigates while reserving the right to deny coverage."),
    ("Scope", "The list of damaged items and repairs included in an estimate."),
    ("Square", "100 square feet of roof surface."),
    ("Supplement", "A request to add items or costs to an existing estimate."),
    ("Suit limitation", "The policy deadline for filing a lawsuit against the insurer, often 12 months in New Jersey."),
    ("Umpire", "The neutral third panel member who decides items the appraisers can’t agree on."),
    ("Uniform Construction Code (UCC)", "New Jersey’s statewide building code, which governs permits and repairs."),
    ("Windstorm deductible", "A deductible that applies to wind losses generally, broader than a hurricane deductible."),
    ("Xactimate", "Estimating software widely used by insurers and contractors to price repairs."),
]

POSTS = [
    {
        "slug": "new-jersey-appraisal-clause-explained", "date": "2026-10-06", "read": "7 min",
        "title": "The New Jersey Appraisal Clause, Explained in Plain English",
        "seo": "New Jersey Appraisal Clause Explained | Plain English",
        "desc": "What the appraisal clause in a New Jersey property policy says, how the 20-day and 15-day windows work and what the panel can and can’t decide.",
        "summary": "Where the clause comes from, what each sentence means and the deadlines hidden inside it.",
        "body": """
<p>Most New Jersey property owners never read the appraisal paragraph until they need it. It’s short, but every sentence matters.</p>
<h2>Where it comes from</h2>
<p>New Jersey adopted a standard fire policy by statute. Its appraisal provision became the model for the appraisal clauses in homeowners, landlord and commercial forms sold in the state. Insurers can and do change the wording, so treat the description below as typical, not as your policy.</p>
<h2>What a typical clause says, sentence by sentence</h2>
<p>The quoted wording below follows common homeowners forms. Your policy may phrase it differently.</p>
<ul>
<li><strong>“If you and we fail to agree on the amount of loss…”</strong> The trigger is a disagreement about money, not coverage.</li>
<li><strong>“…either may demand an appraisal.”</strong> You or the insurer can start it. The demand should be in writing.</li>
<li><strong>“Each party will choose a competent and disinterested appraiser within 20 days…”</strong> Your appraiser must be independent and named on time.</li>
<li><strong>“The two appraisers will choose an umpire. If they cannot agree within 15 days…”</strong> A judge can be asked to appoint one.</li>
<li><strong>“A decision agreed to by any two will set the amount of loss.”</strong> This is what makes the award binding.</li>
<li><strong>“Each party will pay its own appraiser and bear the other expenses equally.”</strong> The usual fee split.</li>
</ul>
<h2>What the panel can’t decide</h2>
<p>Coverage, exclusions, late notice and bad-faith questions sit outside appraisal. A panel can value damage, but if the insurer says the damage isn’t covered at all, you may need an attorney.</p>
<h2>Practical takeaways</h2>
<ul><li>Calendar the 20-day window the day a demand is made, by either side.</li><li>Choose an appraiser with no stake in the repair contract.</li><li>Protect the suit-limitation date separately.</li></ul>
""",
    },
    {
        "slug": "wind-versus-flood-lessons-from-sandy", "date": "2026-09-22", "read": "8 min",
        "title": "Wind Versus Flood: What Sandy Taught New Jersey Homeowners",
        "seo": "Wind vs. Flood Claims in New Jersey: Lessons From Sandy",
        "desc": "How New Jersey homeowners can separate wind damage from flood damage on the same house, with lessons from Superstorm Sandy for future storms.",
        "summary": "Two policies, one house. How to document a coastal storm so each policy pays its share.",
        "body": """
<p>When Sandy came ashore in October 2012, thousands of New Jersey homes were damaged by wind and by surge in the same night. Many owners found that the hardest part of the claim was deciding which policy paid for what.</p>
<h2>Two policies, two sets of rules</h2>
<p>Homeowners policies cover wind but exclude flood. Flood insurance, usually through the National Flood Insurance Program, covers flood but not wind. Each has its own deductibles, limits, deadlines and claim process.</p>
<h2>How to document a mixed loss</h2>
<ul>
<li><strong>Mark the water line</strong> inside and outside, with photos and measurements.</li>
<li><strong>Photograph the roof, windows and siding</strong> before any repairs or tarping.</li>
<li><strong>Note the order of damage.</strong> Was the roof open before the surge arrived? Neighbors, weather records and timestamps can help.</li>
<li><strong>Keep the two claims separate</strong> on paper, room by room and item by item.</li>
</ul>
<h2>Where disputes start</h2>
<p>Interior damage above the water line, elevated-home stairs and decks, and mold that grew after the storm are the items most often pushed from one policy to the other. Careful documentation is the best protection.</p>
<h2>Where appraisal fits</h2>
<p>A homeowners appraisal panel values the covered wind damage. It doesn’t decide the flood claim, and causation disputes may need legal advice.</p>
""",
    },
    {
        "slug": "hurricane-deductibles-in-new-jersey", "date": "2026-09-08", "read": "6 min",
        "title": "Hurricane Deductibles in New Jersey: When They Apply and When They Don’t",
        "seo": "Hurricane Deductibles in New Jersey: When They Apply",
        "desc": "How hurricane and windstorm deductibles work in New Jersey, why Sandy didn’t trigger them and how to read the trigger language in your policy.",
        "summary": "A percentage deductible can cost thousands. Here’s how to read the trigger in your policy.",
        "body": """
<p>Many New Jersey homeowners policies carry a hurricane deductible, usually 1% to 5% of the dwelling limit. On a $500,000 home, a 2% deductible is $10,000.</p>
<h2>What triggers it</h2>
<p>The trigger is in the endorsement, not the declarations page. Common triggers include a hurricane warning issued for New Jersey by the National Weather Service or a storm officially classed as a hurricane. Some policies instead use a broader windstorm deductible that applies to any wind loss.</p>
<h2>The Sandy example</h2>
<p>Sandy was classed as a post-tropical cyclone when it made landfall near Brigantine in 2012. The state told insurers that hurricane deductibles shouldn’t apply, and homeowners paid their ordinary deductibles instead. Future storms will depend on the exact wording in each policy.</p>
<h2>Nor’easters</h2>
<p>Most nor’easters don’t trigger a hurricane deductible. If your policy has a windstorm deductible, though, it may apply.</p>
<h2>Check your numbers</h2>
<p>Our hurricane deductible calculator shows your deductible in dollars and what a claim would pay with and without the trigger.</p>
""",
    },
    {
        "slug": "documenting-ice-dam-and-frozen-pipe-claims", "date": "2026-08-25", "read": "6 min",
        "title": "Documenting an Ice Dam or Frozen Pipe Claim in New Jersey",
        "seo": "Ice Dam & Frozen Pipe Claims in NJ: How to Document",
        "desc": "A step-by-step guide to documenting ice dam and frozen pipe water damage in New Jersey homes, from the first drip to a complete claim file.",
        "summary": "Winter water losses grow fast. Here’s what to photograph, measure and keep.",
        "body": """
<p>New Jersey winters freeze and thaw over and over, which is ideal for ice dams and burst pipes. Water claims move fast, and the evidence disappears once drying starts.</p>
<h2>The first hour</h2>
<ul><li>Shut off the water at the main if a pipe has burst.</li><li>Photograph the source, the ice on the roof and every wet area before anything is moved.</li><li>Call your insurer and a mitigation company.</li></ul>
<h2>The first week</h2>
<ul><li>Keep the mitigation company’s moisture readings, drying logs and photos.</li><li>Save damaged materials or samples until the adjuster has seen them, if you can.</li><li>Keep receipts for every expense.</li></ul>
<h2>Coverage questions to expect</h2>
<p>Insurers will ask whether heat was maintained, whether the leak was sudden or long-term, and whether the home was vacant. Thermostat records, utility bills and service records help answer those questions.</p>
<h2>Where estimates fall short</h2>
<p>Drying days, demolition height, continuous flooring and access costs are the most common gaps. A complete file makes those items easier to support.</p>
""",
    },
    {
        "slug": "reading-a-carrier-estimate-line-by-line", "date": "2026-08-11", "read": "9 min",
        "title": "How to Read an Insurance Estimate Line by Line",
        "seo": "How to Read an Insurance Estimate Line by Line",
        "desc": "A practical guide to reading an insurance company’s property estimate: scope, quantities, unit prices, depreciation, O&P and sales tax.",
        "summary": "Scope, quantities, unit prices, depreciation and O&P: what to check on every page.",
        "body": """
<p>An insurance estimate can run dozens of pages. You don’t need to be an estimator to find the most common problems.</p>
<h2>1. Scope</h2>
<p>Check that every damaged room, roof slope and exterior wall appears. Missing areas are the most common and most expensive gap.</p>
<h2>2. Quantities</h2>
<p>Compare square footage, linear feet and roof squares with your own measurements. Our roof pitch and squares calculator can help with roofs.</p>
<h2>3. Unit prices</h2>
<p>Prices should reflect your area and the current market. Ask your contractor to flag prices that look low.</p>
<h2>4. Depreciation</h2>
<p>Look at the age and life expectancy behind each depreciation figure, and whether labor was depreciated.</p>
<h2>5. Overhead and profit</h2>
<p>If the repair needs a general contractor to coordinate several trades, O&P may be appropriate.</p>
<h2>6. Code items and tax</h2>
<p>Check for permits, Uniform Construction Code items and New Jersey sales tax on materials.</p>
<h2>What to do next</h2>
<p>List the differences, attach your evidence and send a supplement request. If the gap stays large, an estimate review or appraisal may help.</p>
""",
    },
    {
        "slug": "appraiser-public-adjuster-or-attorney-in-nj", "date": "2026-07-28", "read": "7 min",
        "title": "Appraiser, Public Adjuster or Attorney? Choosing Help in New Jersey",
        "seo": "Appraiser vs. Public Adjuster vs. Attorney in New Jersey",
        "desc": "When a New Jersey property owner needs an appraiser, a public adjuster or an attorney, and how each one is paid, licensed and limited.",
        "summary": "Three kinds of help, three different jobs. How to choose the right one first.",
        "body": """
<p>Picking the right help early saves time and money. Here’s how the three roles differ in New Jersey.</p>
<h2>Appraiser</h2>
<p>Works inside the policy’s appraisal clause to value the amount of loss. Best when coverage is accepted and the dispute is about money. Paid by the side that names them.</p>
<h2>Public adjuster</h2>
<p>Licensed by the New Jersey Department of Banking and Insurance to represent policyholders in preparing and negotiating claims. Often involved from the start of a claim. Usually paid a percentage of the settlement, under terms set by state rules.</p>
<h2>Attorney</h2>
<p>Handles coverage denials, bad-faith claims, lawsuits and deadline problems. If your claim was denied or a suit deadline is close, start here.</p>
<h2>Quick guide</h2>
<div class="table-wrap"><table><thead><tr><th>Situation</th><th>Usually best first call</th></tr></thead><tbody>
<tr><th>Coverage accepted, number disputed</th><td>Appraiser</td></tr>
<tr><th>Large, complex claim from day one</th><td>Public adjuster</td></tr>
<tr><th>Claim denied or deadline near</th><td>Attorney</td></tr>
</tbody></table></div>
""",
    },
]
