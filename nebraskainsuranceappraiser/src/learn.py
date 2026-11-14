"""Process guide, FAQ, glossary and guide articles for Nebraska property owners."""

STEPS = [
    ("A covered loss and a disagreement on price", "Appraisal starts when the carrier accepts that a loss is covered but you cannot agree on what it costs. Get the coverage position and the carrier’s complete estimate in writing before anything else."),
    ("A written appraisal demand", "Either side can usually demand appraisal in writing. The demand should cite the policy’s appraisal condition, identify the claim and date of loss, and name your appraiser or state that you will name one within the policy’s time frame."),
    ("Each side names an appraiser", "You and the carrier each select a competent and impartial appraiser. Many policies give each side a set number of days to do so after the demand. Each side generally pays its own appraiser."),
    ("The appraisers choose an umpire", "The two appraisers agree on a neutral umpire. If they cannot agree, many policies allow either side to ask a court in the county where the property sits to appoint one."),
    ("Inspection and independent estimates", "Each appraiser inspects the property and prepares a valuation. Good appraisers measure, photograph and price the loss independently rather than editing the other side’s numbers."),
    ("Appraisers negotiate item by item", "The two appraisers compare estimates line by line. Agreed items are set aside, and the disagreement narrows to specific quantities, prices or repair methods. Many files settle here."),
    ("Umpire review and a signed award", "Any items still open go to the umpire, who reviews both positions and may inspect. An award signed by any two of the three sets the amount of loss. Payment then follows under the policy’s terms, less the deductible and any prior payments."),
]

PROCESS_BODY = """
<h2>Before you begin</h2>
<p>Appraisal is a process written into most property policies to resolve one question: the amount of loss. It is not a lawsuit, it is not mediation and it does not decide coverage. Used at the right time, it can turn a stalled claim into a signed award in weeks rather than years. Used too early, it can lock in a low number.</p>
<div class="note"><b class="h">Is appraisal the right tool?</b>Appraisal fits when coverage is accepted and the dispute is about scope or price. If the carrier denied the claim, raised an exclusion, or says you missed a deadline, talk to a Nebraska attorney first.</div>
<h2>The seven stages</h2>
<ol class="steps">""" + "".join(f"<li><h3>{t}</h3><p>{p}</p></li>" for t, p in STEPS) + """</ol>
<h2>What the award does and does not do</h2>
<ul>
<li>It sets the amount of loss for the items submitted.</li>
<li>It does not decide coverage, exclusions or policy conditions.</li>
<li>It does not award attorney fees, interest or bad-faith damages.</li>
<li>It is binding on the amount of loss, subject to limited challenges such as fraud, bias or the panel going beyond its authority.</li>
</ul>
<h2>Nebraska context</h2>
<p>Insurers in the state are regulated by the <strong>Nebraska Department of Insurance</strong> in Lincoln, which accepts consumer complaints and enforces the state’s unfair claims settlement practices law. Nebraska also has a statute that can allow a policyholder who wins a lawsuit on a policy to recover attorney fees, and courts recognize a bad-faith claim in some circumstances. Those are legal questions; an appraiser cannot advise on them. If you think your claim involves bad faith, speak with a Nebraska attorney.</p>
<p>Nebraska has no coastal wind pool, and as of this writing it is not among the states that operate a FAIR plan. If your coverage has been nonrenewed, the Department of Insurance can explain the market options available.</p>
<h2>Costs</h2>
<p>Each side typically pays its own appraiser and splits the umpire’s fee. Appraiser fees may be flat, hourly or a percentage of the increase. Get the arrangement in writing before work starts, and run the <a href="/claim-tools-nebraska/award-gap-fee-estimator/">award gap and fee estimator</a> to see whether your dispute justifies the expense.</p>
<h2>Timeline</h2>
<p>A straightforward residential hail claim can move from demand to award in six to ten weeks once both appraisers are named. Commercial, farm and contents-heavy files usually take longer, especially if an umpire hearing is needed.</p>
"""

FAQ = [
    ("Appraisal basics", [
        ("What is insurance appraisal?", "A process in most property policies for resolving disputes about the amount of loss. Each side names an appraiser, the appraisers choose an umpire, and two of the three signing an award sets the amount."),
        ("Is appraisal the same as arbitration?", "No. Appraisal is narrower. It values the loss and does not decide coverage or legal claims."),
        ("Who can demand appraisal?", "Usually either the policyholder or the insurer, by written demand, if the policy contains an appraisal clause."),
        ("Does appraisal decide whether damage is covered?", "No. Coverage is decided by the carrier and, if necessary, a court. Appraisal values covered damage."),
    ]),
    ("Costs and fees", [
        ("How much does an appraiser cost?", "Fees vary. Some appraisers charge a flat fee, some hourly and some a percentage of the increase. We put our fee in writing before work starts."),
        ("Who pays the umpire?", "Most policies split the umpire’s fee equally between you and the insurer."),
        ("Is the first conversation free?", "Yes. We review your situation at no cost and tell you whether appraisal is likely to make sense."),
        ("Can fees be more than the recovery?", "On a small gap, yes. That is why we recommend running the numbers first."),
    ]),
    ("Timing and deadlines", [
        ("How long does appraisal take?", "Often six to ten weeks for a simple residential claim once both appraisers are named. Larger claims take longer."),
        ("Is there a deadline to demand appraisal?", "Some policies set one; many tie it to other conditions. Read your policy and watch the suit-limitation period."),
        ("How soon must I report hail damage?", "Policies require prompt notice and some set a specific window for wind and hail. Report as soon as you reasonably can."),
        ("What if my policy deadline is close?", "Talk to a Nebraska attorney right away. Appraisal does not necessarily stop the clock on a lawsuit deadline."),
    ]),
    ("Nebraska specifics", [
        ("Who regulates insurers in Nebraska?", "The Nebraska Department of Insurance in Lincoln. It accepts consumer complaints and oversees claim practices."),
        ("Does Nebraska have a FAIR plan or wind pool?", "There is no coastal wind pool, and as of this writing Nebraska is not among the states with a FAIR plan. Ask the Department of Insurance about current options if you are nonrenewed."),
        ("Are percentage hail deductibles common here?", "Yes. Many Nebraska homeowners policies apply a wind/hail deductible as a percentage of the dwelling limit."),
        ("What about bad faith?", "Nebraska law addresses unfair claim practices and recognizes bad-faith claims in some circumstances. That is a legal matter for an attorney, not an appraiser."),
    ]),
    ("Working with us", [
        ("Are you public adjusters or attorneys?", "Neither. We provide appraisal, estimating and umpire services. We do not give legal advice or negotiate claims outside appraisal."),
        ("Do you serve all of Nebraska?", "Yes, all 93 counties, from Omaha and Lincoln to the Sandhills and the Panhandle."),
        ("What should I send for a review?", "Your declarations page, the carrier’s full estimate, any letters, photos and your contractor’s estimate if you have one."),
        ("Do you guarantee results?", "No honest appraiser can. We give you a candid assessment and a defensible valuation."),
    ]),
]

GLOSSARY = [
    ("Actual cash value (ACV)", "Replacement cost minus depreciation. Often the first payment on a replacement cost policy."),
    ("Additional living expense (ALE)", "Extra costs of living elsewhere while a home is uninhabitable after a covered loss."),
    ("Amount of loss", "The dollar value of a covered loss. The only question an appraisal panel decides."),
    ("Appraisal clause", "The policy condition that lets either side demand appraisal when they disagree on the amount of loss."),
    ("Appraisal award", "The written decision signed by two of the three panel members that sets the amount of loss."),
    ("Appraiser", "The person each side selects to value the loss. Policies often require that they be competent and impartial."),
    ("Bad faith", "A legal claim that an insurer unreasonably handled or denied a claim. Not decided in appraisal."),
    ("Coinsurance", "A commercial policy clause that can reduce payment if a building is insured for less than a set share of its value."),
    ("Collapse", "A named coverage, often limited to specific causes such as the weight of ice or snow."),
    ("Cosmetic damage exclusion", "Policy language, common on metal roofs, that excludes dents that do not affect function."),
    ("Coverage A", "Dwelling coverage on a homeowners policy. Percentage deductibles are often based on this limit."),
    ("Coverage B", "Other structures coverage, such as detached garages, sheds and fences."),
    ("Declarations page", "The summary page of a policy listing coverages, limits, deductibles and endorsements."),
    ("Depreciation", "The reduction in value due to age, wear and obsolescence."),
    ("Derecho", "A widespread, long-lived windstorm with straight-line winds, often causing damage across hundreds of miles."),
    ("Drip edge", "Metal flashing along roof edges. Often required by code when a roof is replaced."),
    ("Endorsement", "A form that adds, removes or changes coverage in a policy."),
    ("Functional damage", "Damage that affects how a material performs, such as a fractured shingle mat."),
    ("Holdback", "Depreciation withheld until repairs are complete. Also called recoverable depreciation."),
    ("Ice and water shield", "A self-adhering underlayment used at eaves and valleys to resist ice dam leaks."),
    ("Ice dam", "A ridge of ice at the roof edge that traps meltwater, which can back up under shingles."),
    ("Line item", "A single entry in an estimate for a specific task, quantity and price."),
    ("Matching", "Whether repaired areas can reasonably match undamaged areas in color and appearance."),
    ("Mitigation", "Steps taken to prevent further damage after a loss, such as tarping or drying."),
    ("Nebraska Department of Insurance", "The state agency that regulates insurers and accepts consumer complaints."),
    ("Ordinance or law coverage", "Coverage for added costs to meet current building codes during repair."),
    ("Overhead and profit (O&P)", "A general contractor’s markup, often 10% and 10%, when multiple trades are involved."),
    ("Percentage deductible", "A deductible equal to a percentage of a coverage limit rather than a flat dollar amount."),
    ("Pitch", "Roof slope, expressed as inches of rise per 12 inches of run, such as 6/12."),
    ("Proof of loss", "A sworn statement of the amount claimed, often required within a set time after the insurer requests it."),
    ("Recoverable depreciation", "Depreciation that can be paid once repairs are completed under a replacement cost policy."),
    ("Replacement cost value (RCV)", "The cost to repair or replace with materials of like kind and quality, without depreciation."),
    ("Scope of loss", "The list of damaged items and repairs included in an estimate."),
    ("Soft metals", "Vents, flashing, gutters and similar components that show hail dents clearly."),
    ("Square", "100 square feet of roof surface."),
    ("Steep charge", "Extra labor added for working on roofs above a certain pitch."),
    ("Supplement", "A request to add missed or underpriced items to an estimate."),
    ("Suit limitation", "The policy period within which a lawsuit against the insurer must be filed."),
    ("Umpire", "The neutral third panel member who resolves items the two appraisers cannot agree on."),
    ("Wind/hail deductible", "A separate deductible for windstorm and hail losses, often a percentage of Coverage A."),
    ("Xactimate", "Estimating software widely used by insurers and contractors to price property repairs."),
]

POSTS = [
    {
        "slug": "nebraska-hail-claim-documentation",
        "title": "How to Document a Nebraska Hail Claim Slope by Slope",
        "seo": "How to Document a Nebraska Hail Claim, Slope by Slope",
        "desc": "A practical guide to documenting Nebraska hail damage slope by slope, from soft metals and test areas to photos that hold up in appraisal.",
        "summary": "The photos and notes that make the difference when a carrier approves only part of your roof.",
        "date": "2026-10-06", "read": "7 min",
        "body": """
<h2>Start the day of the storm</h2>
<p>Note the date and time, and if it is safe, photograph hail on the ground next to a coin or ruler. Local news reports and weather service storm reports for your county help pin down the event later, especially if your area has seen more than one storm.</p>
<h2>Soft metals tell the story</h2>
<p>Dents in gutters, downspouts, roof vents, flashing, window screens and air conditioner fins show hail size and direction. Photograph each with a wide shot for location and a close shot for detail.</p>
<h2>Go slope by slope</h2>
<p>Carriers often approve slopes facing the storm and deny the rest. Label each slope by direction, then photograph representative hits on every one. Chalk circles around hits help them show in photos. A roofer or appraiser can count hits in a marked test area on each slope.</p>
<h2>Don’t forget the rest of the property</h2>
<ul>
<li>Siding and window wraps on every elevation</li>
<li>Fences, decks and painted surfaces</li>
<li>Detached garages, sheds and farm buildings</li>
<li>Skylights, satellite dishes and solar equipment</li>
</ul>
<h2>Keep records of prior repairs</h2>
<p>If your roof was replaced or repaired after an earlier storm, keep the invoice and photos. They are your best answer to a prior-damage argument.</p>
""",
    },
    {
        "slug": "percentage-deductible-explained",
        "title": "Percentage Hail Deductibles Explained for Nebraska Homeowners",
        "seo": "Percentage Hail Deductibles Explained for Homeowners",
        "desc": "What a percentage wind and hail deductible means in dollars, how it affects your claim payment and when appraisal is still worth considering.",
        "summary": "Why a 1% deductible can cost more than you think, and how it changes the math on a disputed claim.",
        "date": "2026-09-22", "read": "5 min",
        "body": """
<h2>The basic idea</h2>
<p>A percentage deductible is calculated from your dwelling limit, not from the loss. On a home insured for $300,000, a 1% wind/hail deductible is $3,000 and a 2% deductible is $6,000. Your other claims may still use a flat deductible.</p>
<h2>Why insurers use them</h2>
<p>In hail-prone states, frequent storms make roof claims a large share of losses. Percentage deductibles shift part of that cost to the policyholder in exchange for a lower premium.</p>
<h2>How it affects a dispute</h2>
<p>The deductible comes off the final amount of loss, not the gap. If your claim is barely above the deductible, even a successful appraisal may produce a modest payment. If the claim is well above it, every dollar recovered in appraisal goes to you.</p>
<h2>Illustrative example</h2>
<p>These figures are illustrative only. A $20,000 hail loss with a 2% deductible on a $340,000 home leaves $13,200 after the $6,800 deductible. If appraisal raises the loss to $26,000, the payment rises to $19,200.</p>
<h2>Check before the next storm</h2>
<p>Review your declarations page at renewal. Our <a href="/claim-tools-nebraska/hail-deductible-calculator/">hail deductible calculator</a> converts any percentage into dollars.</p>
""",
    },
    {
        "slug": "appraiser-adjuster-or-attorney",
        "title": "Appraiser, Public Adjuster or Attorney: Who Should You Call?",
        "seo": "Appraiser, Public Adjuster or Attorney: Who to Call",
        "desc": "How an insurance appraiser, a public adjuster and an attorney differ, and which one fits your Nebraska property claim at each stage.",
        "summary": "Three different jobs, three different stages. Picking the right help first saves time and fees.",
        "date": "2026-09-08", "read": "6 min",
        "body": """
<h2>Three roles</h2>
<ul>
<li><strong>Appraiser:</strong> values the amount of loss inside the policy’s appraisal process.</li>
<li><strong>Public adjuster:</strong> represents the policyholder in presenting and negotiating the whole claim, usually for a percentage fee. Public adjusters are licensed by the Nebraska Department of Insurance.</li>
<li><strong>Attorney:</strong> handles coverage disputes, denials, bad-faith questions and litigation.</li>
</ul>
<h2>When an appraiser fits</h2>
<p>Coverage is accepted, you have the carrier’s estimate and the disagreement is about scope or price.</p>
<h2>When a public adjuster fits</h2>
<p>Early in a complex claim when you need someone to prepare and present the claim, especially if you do not have time to manage it yourself.</p>
<h2>When an attorney fits</h2>
<p>The claim was denied, an exclusion is being applied, a deadline is close or you believe the carrier acted in bad faith. Nebraska law addresses unfair claim practices and fee recovery in some lawsuits, which are legal questions only an attorney should advise on.</p>
<h2>Our approach</h2>
<p>If your claim needs an attorney or a public adjuster instead of an appraiser, we will tell you on the first call.</p>
""",
    },
    {
        "slug": "farm-building-claims-after-storms",
        "title": "Farm Building Claims After a Nebraska Storm",
        "seo": "Farm Building Insurance Claims After a Nebraska Storm",
        "desc": "How Nebraska farm building claims work after hail or wind: scheduled limits, valuation methods, grain bins, pole barns and documenting damage.",
        "summary": "Machine sheds, pole barns and grain bins are valued differently from houses. Here is what to check.",
        "date": "2026-08-25", "read": "6 min",
        "body": """
<h2>Start with the schedule</h2>
<p>Farm policies often list each building separately with its own limit and valuation basis. Some buildings are insured at replacement cost, others at actual cash value or a stated amount. Find your schedule before the adjuster arrives.</p>
<h2>Common farm losses</h2>
<ul>
<li>Hail-dented steel roofs and walls</li>
<li>Wind-racked pole barns and collapsed doors</li>
<li>Grain bins torn from foundations</li>
<li>Snow load damage to older buildings</li>
</ul>
<h2>Document the whole building</h2>
<p>Photograph every wall and roof panel, door tracks, trusses and purlins. Note any stored grain, equipment or livestock that complicated repairs.</p>
<h2>Price it like a farm repair</h2>
<p>Post-frame and steel buildings need specialty panels, lifts and sometimes cranes. Make sure the estimate reflects those costs, not residential line items.</p>
<h2>Cosmetic damage clauses</h2>
<p>Some farm and commercial policies exclude dents in metal that do not affect function. Read the wording carefully before deciding how to proceed.</p>
""",
    },
    {
        "slug": "when-appraisal-is-the-wrong-move",
        "title": "When Appraisal Is the Wrong Move",
        "seo": "When Insurance Appraisal Is the Wrong Move for a Claim",
        "desc": "Insurance appraisal is not always the answer. Learn the situations where a supplement, a public adjuster or an attorney fits your claim better.",
        "summary": "Appraisal is powerful, but it can lock in a bad number if you use it at the wrong time.",
        "date": "2026-08-11", "read": "5 min",
        "body": """
<h2>The claim was denied</h2>
<p>Appraisal values covered losses. If the carrier denied coverage, appraisal will not fix that. Talk to an attorney.</p>
<h2>The gap is small</h2>
<p>If the disagreement is a few thousand dollars, appraiser and umpire fees may consume most of it. A documented supplement request is often better.</p>
<h2>You don’t have the full estimate</h2>
<p>Without the carrier’s itemized estimate, you cannot know where the disagreement lies. Get it first.</p>
<h2>A deadline is close</h2>
<p>Appraisal may not stop a suit-limitation period. If a deadline is near, speak with a Nebraska attorney before anything else.</p>
<h2>Your documentation is thin</h2>
<p>The award is binding. If you have few photos and no independent estimate, build your file before demanding appraisal. The <a href="/claim-tools-nebraska/appraisal-readiness-check/">appraisal readiness check</a> helps.</p>
""",
    },
    {
        "slug": "winter-water-damage-claims",
        "title": "Winter Water Damage Claims: Ice Dams and Frozen Pipes",
        "seo": "Winter Water Damage Claims: Ice Dams and Frozen Pipes",
        "desc": "How Nebraska ice dam and frozen pipe claims work: what policies usually cover, heat-maintenance conditions and the documentation that helps.",
        "summary": "Long cold snaps cause some of the most expensive water claims of the year. Here is how to protect yours.",
        "date": "2026-07-28", "read": "6 min",
        "body": """
<h2>Two winter culprits</h2>
<p>Frozen pipes split and release water when they thaw. Ice dams trap meltwater at the eaves and push it under shingles. Both can soak insulation, drywall and flooring before anyone notices.</p>
<h2>Coverage conditions to know</h2>
<ul>
<li>Many policies limit freezing coverage if heat was not maintained or the building was vacant.</li>
<li>Interior damage from ice dams is commonly covered, but removing the ice may not be.</li>
<li>Collapse from snow or ice weight is often a named coverage with its own conditions.</li>
</ul>
<h2>Document as you go</h2>
<p>Photograph icicles and ice dams before they melt, note outdoor temperatures and save utility bills that show heat was on. Keep moisture readings and drying logs from the mitigation company.</p>
<h2>Where claims fall short</h2>
<p>Drying times are longer in cold weather, finished basements are expensive to restore and hidden insulation damage is easy to miss. Make sure the estimate covers all of it.</p>
""",
    },
]
