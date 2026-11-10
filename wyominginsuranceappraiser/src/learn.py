"""Resources: process guide, FAQ, glossary and claim guides for Wyoming."""

PROCESS_STEPS = [
    ("Pin down the disagreement", "Before anything formal happens, write down exactly what you disagree with: which items are missing, which measurements are short, which prices are low, and what your contractor’s number is. Send it to the carrier with photos. A documented supplement request closes a lot of gaps on its own, and it gives you a record if it doesn’t."),
    ("Read the appraisal condition", "Find the paragraph titled “Appraisal” in the conditions section of your policy. Note who can demand it, how many days each side has to name an appraiser, how the umpire is chosen, and whether anything else — like a sworn proof of loss — must come first. Find the “Suit Against Us” condition too."),
    ("Send a written demand", "Either side may demand appraisal. The demand should identify the policy and claim, say that you disagree on the amount of loss, invoke the appraisal provision and name your appraiser or commit to naming one within the policy’s window. Send it in a way you can prove, such as certified mail plus email."),
    ("Both appraisers are named", "Each side picks a competent, independent appraiser. Yours inspects the property, measures everything and builds a line-item estimate. The carrier’s appraiser does the same. They exchange estimates and begin comparing."),
    ("The umpire is selected", "The two appraisers agree on a neutral umpire, ideally early so one is ready if needed. If they can’t agree within the policy’s time limit, either side can usually ask a court of record in the county where the property is — in Wyoming, typically the district court — to appoint one."),
    ("The appraisers work it out", "This is where most of the money moves. The appraisers walk the property together, compare quantities and prices, and agree on every item they can. Many Wyoming appraisals end here with both appraisers signing an agreed award."),
    ("The umpire decides what’s left", "Each appraiser submits a written position on the remaining items with photos, measurements and pricing support. The umpire may visit the property or meet with both appraisers, then decides each item."),
    ("The award is signed and paid", "An award signed by any two of the three sets the amount of loss. A good award separates replacement cost, depreciation and actual cash value by coverage. The carrier then pays under the policy terms, less the deductible and prior payments, with recoverable depreciation released when repairs are done."),
]

PROCESS_BODY = "".join(f"<h2 id=\"step-{i + 1}\">Step {i + 1}: {t}</h2><p>{p}</p>" for i, (t, p) in enumerate(PROCESS_STEPS)) + """
<div class="note"><b class="h">Who pays</b>Each side pays its own appraiser, and the umpire’s fee is usually split evenly. Get every fee arrangement in writing before work begins.</div>
<h2>What appraisal can’t do</h2>
<ul>
<li>Decide whether a loss is covered — that’s a coverage question.</li>
<li>Award interest, attorney’s fees or bad-faith damages.</li>
<li>Pay more than your policy limits.</li>
<li>Automatically pause your policy’s deadline to file suit.</li>
</ul>
<h2>Wyoming context</h2>
<p>Property insurers in Wyoming are regulated by the Wyoming Department of Insurance in Cheyenne, which accepts consumer complaints about claim handling. Wyoming’s insurance code in Title 26 of the Wyoming Statutes includes rules on unfair claim settlement practices and a provision that can allow attorney’s fees and interest when an insurer unreasonably delays payment after proof of loss; Wyoming courts also recognize a common-law claim for first-party bad faith. Those are legal remedies outside appraisal, and the details matter — talk to a Wyoming-licensed attorney if you think they apply. Unlike many coastal states, Wyoming does not run a FAIR plan or state wind pool, so properties that are hard to insure are usually placed in the surplus lines market, where policy forms can differ more from standard wording.</p>
"""

FAQ = [
    ("Appraisal basics", [
        ("What is insurance appraisal?", "A process written into most property policies for settling disagreements about the amount of a covered loss. Each side names an appraiser, the appraisers choose an umpire, and an agreement signed by any two of the three sets the amount."),
        ("Is appraisal the same as arbitration?", "They are similar but not identical. Appraisal is narrower: it decides the amount of loss, not legal questions such as coverage or bad faith, and it is usually less formal than arbitration."),
        ("Who can demand appraisal?", "Under most policy wording, either you or the insurance company can demand it in writing once you disagree on the amount of loss."),
        ("Does my policy have an appraisal clause?", "Most Wyoming homeowners, farm and commercial property policies do. Look for a paragraph titled “Appraisal” in the conditions section. Surplus lines and specialty policies sometimes use different wording or replace it with arbitration."),
    ]),
    ("Cost and timing", [
        ("How much does appraisal cost?", "You pay your own appraiser and usually half of the umpire’s fee. Appraiser fees may be flat, hourly or tied to the claim; ask for the arrangement in writing. Our award net-gain projector helps you see whether the cost makes sense."),
        ("How long does appraisal take?", "Many residential appraisals finish within two to three months after both appraisers are named. Winter access in the mountains, large commercial losses and umpire hearings can extend it."),
        ("Does appraisal stop the clock on my deadline to sue?", "Not automatically. Unless your policy or a written agreement says otherwise, the suit-limitation period may keep running. Protect it separately."),
    ]),
    ("Wyoming specifics", [
        ("Who regulates insurance companies in Wyoming?", "The Wyoming Department of Insurance, based in Cheyenne. It licenses insurers and adjusters and accepts consumer complaints."),
        ("Does Wyoming have a FAIR plan or wind pool?", "No. Wyoming does not operate a FAIR plan or a state wind pool. Hard-to-insure properties are usually written in the surplus lines market."),
        ("Does Wyoming have a bad-faith law?", "Wyoming recognizes a common-law claim for first-party bad faith, and its insurance code includes unfair claim practices rules and a provision on attorney’s fees and interest for unreasonable delays. Those are legal questions; ask a Wyoming attorney. Appraisal does not decide them."),
        ("How many counties do you cover?", "All 23 Wyoming counties, from Laramie County in the southeast to Teton and Park counties in the northwest."),
    ]),
    ("Working with us", [
        ("Are you a public adjuster or a law firm?", "Neither. We provide appraisal, estimate review and umpire services. We don’t negotiate claims outside appraisal and we don’t give legal advice."),
        ("Can you tell me if my claim is worth appraising?", "Yes. The first conversation is free. We’ll look at both estimates and your photos and give you a straight answer — including when appraisal isn’t the right tool."),
        ("Do you guarantee a result?", "No honest appraiser can. We guarantee a careful, well-documented valuation and clear communication."),
    ]),
]

GLOSSARY = [
    ("Actual cash value (ACV)", "The value of damaged property at the time of loss, usually replacement cost minus depreciation."),
    ("Additional living expense (ALE)", "Coverage for extra costs of living elsewhere while your home is uninhabitable after a covered loss."),
    ("Appraisal clause", "The policy condition that lets either party demand appraisal when they disagree on the amount of loss."),
    ("Appraisal award", "The written decision, signed by any two of the three panel members, that sets the amount of loss."),
    ("Appraiser", "The person each side names to value the loss on an appraisal panel; usually required to be competent and independent."),
    ("Bad faith", "A legal claim that an insurer unreasonably handled or denied a claim. Decided by courts, not appraisal panels."),
    ("Class 4 shingle", "A shingle rated for the highest impact resistance under the UL 2218 test; common in hail-prone Wyoming towns."),
    ("Collapse", "A coverage term, defined in each policy, for the sudden falling in of a building or part of one, such as from snow weight."),
    ("Cosmetic damage exclusion", "An endorsement that excludes damage that changes appearance but not function, often applied to dented metal roofing."),
    ("Coverage A", "Dwelling coverage — the limit for the house itself and attached structures."),
    ("Coverage B", "Other structures coverage for detached garages, shops, barns and fences."),
    ("Coverage C", "Personal property, or contents, coverage."),
    ("Creased shingle", "A shingle bent back by wind so that it has lost its seal and much of its wind resistance."),
    ("Declarations page", "The summary page of a policy listing limits, deductibles, endorsements and the insured property."),
    ("Depreciation", "The reduction in value for age, wear and condition, subtracted from replacement cost to reach actual cash value."),
    ("Disinterested", "Having no financial stake in the outcome; a requirement many policies place on appraisers."),
    ("Endorsement", "A form that adds to, removes or changes the terms of a base policy."),
    ("Estimate review", "A line-by-line check of an insurance estimate for missing items, measurement errors and pricing issues."),
    ("Ground snow load", "The design weight of snow on the ground at a location, used by building codes to set roof load requirements."),
    ("Holdback", "Recoverable depreciation withheld from the first payment until repairs are completed."),
    ("Ice dam", "A ridge of ice at the eaves that traps meltwater, which can back up under shingles and leak inside."),
    ("Ice and water shield", "A self-adhering waterproof underlayment installed at eaves and valleys, often required by code in snowy areas."),
    ("Line item", "A single priced entry in an estimate, such as a quantity of shingles or a square foot of drywall."),
    ("Matching", "The question of whether replacement materials must reasonably match undamaged materials in color and style."),
    ("Mitigation", "Reasonable steps to prevent further damage after a loss, like tarping a roof or extracting water."),
    ("Ordinance or law coverage", "Coverage for extra costs to bring repaired portions of a building up to current code."),
    ("Overhead and profit (O&P)", "A general contractor’s charge, often 10% plus 10%, for coordinating multiple trades on a repair."),
    ("Percentage deductible", "A deductible calculated as a percentage of Coverage A rather than a flat dollar amount; common for wind and hail."),
    ("Pitch", "The steepness of a roof, expressed as inches of rise per 12 inches of run, such as 6/12."),
    ("Proof of loss", "A sworn statement of the amount claimed, which an insurer may require within a set time after requesting it."),
    ("Recoverable depreciation", "Depreciation that can be collected after repairs are completed under a replacement cost policy."),
    ("Replacement cost value (RCV)", "The cost to repair or replace damaged property with materials of like kind and quality, without deduction for depreciation."),
    ("Reservation of rights", "A letter in which an insurer continues to handle a claim while reserving the right to deny coverage later."),
    ("Scope of loss", "The full list of damaged items and the work needed to repair them."),
    ("Square", "A roofing unit equal to 100 square feet of roof surface."),
    ("Steep charge", "An estimate line adding labor cost for roofs too steep to walk safely, usually 7/12 pitch and above."),
    ("Suit limitation", "The policy condition setting how long you have to file a lawsuit against the insurer."),
    ("Supplement", "A request to add missing or underpriced items to an existing insurance estimate."),
    ("Surplus lines", "Coverage placed with insurers not licensed as admitted carriers in a state, used for risks standard insurers won’t write."),
    ("Test square", "A 10-by-10-foot area marked on a roof slope where hail hits are counted."),
    ("Umpire", "The neutral third member of an appraisal panel who decides items the two appraisers can’t agree on."),
    ("Wind-driven hail", "Hail carried at an angle by strong wind, which damages siding, windows and windward roof slopes."),
    ("Xactimate", "Estimating software widely used by insurers, adjusters and contractors to price property repairs."),
]

POSTS = [
    {
        "slug": "wyoming-appraisal-clause-plain-english",
        "kw": "Wyoming appraisal clause",
        "title": "The Wyoming Appraisal Clause in Plain English",
        "seo": "The Wyoming Appraisal Clause in Plain English",
        "desc": "What the appraisal clause in a typical Wyoming property policy says, phrase by phrase, and where disputes usually start when a claim is underpaid.",
        "date": "2026-10-14", "read": "7 min",
        "summary": "A phrase-by-phrase reading of the paragraph most policyholders never notice until a claim comes up short.",
        "body": """
<p>The appraisal paragraph in a Wyoming homeowners or commercial policy is short — often under 200 words — and it rarely gets read until a claim goes sideways. Below is a reading of language that appears in many policies, phrase by phrase. Your form may be worded differently, especially if it is a surplus lines or farm policy, so put your own policy next to this guide.</p>
<h2>“If you and we fail to agree on the amount of loss…”</h2>
<p>This is the trigger, and the key word is <strong>amount</strong>. Appraisal decides what a covered loss costs to repair. It isn’t built to decide whether the loss is covered at all. When an adjuster says a slope wasn’t damaged by hail, is that a dispute about amount or about cause? Courts around the country have answered that differently, and it is one of the most argued points in appraisal.</p>
<h2>“…either may demand appraisal of the loss.”</h2>
<p>You or the insurer can start it, in writing. A good demand names the policy and claim number, says the parties disagree on the amount of loss, cites the appraisal provision and names your appraiser or says you will within the policy window.</p>
<h2>“Each party will choose a competent and independent appraiser…”</h2>
<p>Competent means qualified to value this kind of loss. Independent — or, in older forms, disinterested — means no stake in the outcome. That is why a contractor who will do the work, or an appraiser paid a share of the increase, can create problems for the award.</p>
<h2>“…within 20 days after receiving a written request from the other.”</h2>
<p>Twenty days is common but not universal. Calendar it the day the demand is sent or received. Our <a href="/free-calculators/claim-timeline-builder/">claim timeline builder</a> can help.</p>
<h2>“The two appraisers will choose an umpire.”</h2>
<p>If they can’t agree within the policy window — frequently 15 days — either side can usually ask a court of record in the county where the property is to appoint one. In Wyoming, that is typically the district court.</p>
<h2>“A decision agreed to by any two will set the amount of loss.”</h2>
<p>This is what gives appraisal force. Once two of three sign, the amount is set. A weak, poorly documented valuation from your appraiser makes it easy for the umpire to sign with the other side.</p>
<h2>“Each party will pay its own appraiser and bear the other expenses of the appraisal and umpire equally.”</h2>
<p>Budget for both. On a small dispute, fees can swallow the increase, which is why we built the <a href="/free-calculators/award-net-gain-projector/">award net-gain projector</a>.</p>
<h2>What the clause usually doesn’t say</h2>
<p>Most clauses are silent on how long appraisal can take, what happens to the deadline to sue while it is pending, and how depreciation should appear in the award. Those gaps are where experience matters. If coverage, delay or bad-faith issues are part of your situation, talk with a Wyoming-licensed attorney; appraisal won’t resolve them.</p>
""",
    },
    {
        "slug": "wind-driven-hail-siding-claims",
        "kw": "wind-driven hail siding damage",
        "title": "Wind-Driven Hail: Why Siding and Windows Get Missed",
        "seo": "Wind-Driven Hail Siding Damage: What Gets Missed",
        "desc": "Why wind-driven hail on Wyoming’s high plains damages siding, windows and screens on one side of a house, and how to document it before it’s missed.",
        "date": "2026-10-21", "read": "6 min",
        "summary": "When hail rides a 50 mph west wind, the roof is only part of the story. Here’s what to check on every elevation.",
        "body": """
<p>Picture a summer storm coming off the Laramie Range toward Cheyenne. The hail isn’t falling straight down; it’s being thrown sideways by a strong west or northwest wind. The roof takes hits, but so do the siding, windows, screens, gutters, fences and anything else facing the storm. A claim that only looks up can leave thousands of dollars on the ground.</p>
<h2>Elevation by elevation</h2>
<ul>
<li><strong>Vinyl siding</strong> cracks and punctures, especially in cold weather when it is brittle.</li>
<li><strong>Fiber-cement and wood siding</strong> chips and dents; paint may be knocked off in spots.</li>
<li><strong>Aluminum and steel siding</strong> dents, raising cosmetic-versus-functional questions.</li>
<li><strong>Window screens</strong> tear or stretch; aluminum frames and wraps dent; glass can crack.</li>
<li><strong>Gutters and downspouts</strong> show dents that can help confirm hail size and direction.</li>
<li><strong>HVAC condensers</strong> on the windward side often have flattened fins.</li>
</ul>
<h2>Why it gets missed</h2>
<p>Field adjusters working a busy storm have limited time per house. Roofs get the attention because roofs are expensive. Siding damage on one elevation may be noted but valued as a few replacement pieces, even when the profile is discontinued and the wall can’t be repaired without looking patched.</p>
<h2>How to document it</h2>
<ol>
<li>Photograph each elevation straight on, then close-ups of individual hits with a coin or tape for scale.</li>
<li>Use side lighting — early morning or evening — to make dents visible on metal.</li>
<li>Note the direction the storm came from and compare damage by side.</li>
<li>Look for the manufacturer and profile of your siding; a label or a spare piece in the garage helps.</li>
<li>Keep any broken pieces.</li>
</ol>
<h2>Matching and uniform appearance</h2>
<p>If damaged siding can’t be matched, the question becomes whether your policy requires a reasonable match. Policies and court decisions vary on how far that obligation extends. A panel can value the cost of reasonable matching where it is owed; whether it is owed may depend on policy language. The <a href="/free-calculators/hail-test-square-scorer/">hail test-square scorer</a> helps with the roof side of the same storm.</p>
""",
    },
    {
        "slug": "roof-collapse-from-snow-what-to-document",
        "kw": "snow roof collapse insurance claim",
        "title": "Roof Damage From Snow: What to Document Before You Shovel",
        "seo": "Snow Roof Collapse Insurance Claim: What to Document",
        "desc": "A Wyoming checklist for a snow roof collapse insurance claim: safety, photos, engineers, temporary shoring and the coverage questions to expect.",
        "date": "2026-10-28", "read": "6 min",
        "summary": "Sagging ridges, cracked rafters and porches pulled loose after a heavy snow year: a checklist for protecting the claim.",
        "body": """
<p>Big snow years in Jackson, Pinedale, Afton, Cody and the mountain cabin areas push roofs hard. Most snow-load damage isn’t a dramatic cave-in; it’s a ridge that starts to sag, a rafter that cracks, a porch or carport that pulls away from the house, or a door that suddenly won’t close. What you do in the first days shapes the claim.</p>
<h2>1. Safety first</h2>
<p>If framing is cracking or a roof is visibly deflecting, get people out of the area below it. Don’t climb on a loaded roof. Call a contractor experienced with snow removal and shoring.</p>
<h2>2. Photograph before anything changes</h2>
<ul>
<li>The roofline from several angles, showing any sag.</li>
<li>Snow depth on the roof and on the ground, with a measuring stick if you can do it safely.</li>
<li>Interior ceilings, cracks, doors that stick and any water stains.</li>
<li>Attic framing, if you can see it safely.</li>
</ul>
<h2>3. Protect the building and keep receipts</h2>
<p>Snow removal, temporary shoring and tarps are usually reasonable mitigation. Keep every invoice and take photos of the work being done.</p>
<h2>4. Get an engineer involved</h2>
<p>Structural damage needs an engineer’s assessment. That report becomes the backbone of the repair scope and is valuable evidence for a panel if appraisal is needed.</p>
<h2>5. Expect coverage questions</h2>
<p>Policies define collapse in specific ways, and some limit coverage for certain structures like awnings, fences, patios or pools when snow or ice is the cause. Some exclude long-term deterioration. Those are coverage questions. Once coverage is accepted, the cost of framing, decking, roofing, interiors and contents is a valuation question.</p>
<h2>6. Watch the scope</h2>
<p>Snow claims are often underscoped because hidden framing damage isn’t opened up. If the carrier’s estimate replaces the roof covering but not the cracked rafters underneath, that is a gap worth closing. Our <a href="/what-we-appraise/snow-load-ice-dam-claims/">snow load and ice dam</a> page has more detail.</p>
""",
    },
    {
        "slug": "choosing-appraiser-adjuster-or-attorney",
        "kw": "appraiser vs public adjuster vs attorney",
        "title": "Appraiser, Public Adjuster or Attorney? Picking the Right Help",
        "seo": "Appraiser vs Public Adjuster vs Attorney in Wyoming",
        "desc": "How an insurance appraiser, a public adjuster and an attorney differ for a Wyoming property claim, and how to tell which one your situation needs.",
        "date": "2026-11-03", "read": "5 min",
        "summary": "Three kinds of help solve three different problems. Here’s how to tell which one fits your claim right now.",
        "body": """
<p>When a claim goes wrong, you’ll hear all three suggested. They are not interchangeable. Picking the right one first saves time and fees.</p>
<h2>An insurance appraiser</h2>
<p>An appraiser works within the policy’s appraisal clause on one question: the amount of a covered loss. If coverage is accepted and the dispute is about how much the repair costs, an appraiser is the specialist. The result is a binding award on the amount once two of three panel members sign.</p>
<h2>A public adjuster</h2>
<p>A public adjuster is licensed to represent the policyholder in presenting and negotiating the whole claim, usually for a percentage of the recovery. Public adjusters are licensed through the Wyoming Department of Insurance. They can be helpful early, when a claim is complex and you don’t have time to manage it.</p>
<h2>An attorney</h2>
<p>An attorney handles legal problems: coverage denials, disputes about policy interpretation, deadlines to sue, and claims of bad faith. If your claim was denied outright, or the carrier is raising coverage defenses, a Wyoming-licensed attorney should be your first call.</p>
<h2>A quick guide</h2>
<div class="table-wrap"><table><thead><tr><th>Your situation</th><th>Usually start with</th></tr></thead><tbody>
<tr><th>Covered, but the estimate is too low</th><td>Estimate review, then appraisal</td></tr>
<tr><th>Just filed, complex claim, no time to manage it</th><td>Public adjuster</td></tr>
<tr><th>Denied, or coverage disputed</th><td>Attorney</td></tr>
<tr><th>Suit deadline approaching</th><td>Attorney, right away</td></tr>
</tbody></table></div>
<p>We will always tell you if your situation calls for one of the others instead of us.</p>
""",
    },
    {
        "slug": "matching-and-discontinued-materials",
        "kw": "discontinued shingles insurance claim",
        "title": "Discontinued Shingles and Siding: The Matching Problem",
        "seo": "Discontinued Shingles Insurance Claim: Matching Guide",
        "desc": "How matching disputes work when shingles or siding are discontinued on a Wyoming home, what evidence helps, and how appraisal panels approach it.",
        "date": "2026-11-07", "read": "6 min",
        "summary": "A partial repair that leaves a two-tone roof or wall is one of the most common disputes we see. Here’s how it gets resolved.",
        "body": """
<p>Much of Wyoming was built in bursts — oil, gas, coal, trona — and many homes were sided and roofed with whatever was available that decade. Twenty or thirty years later, after a hail or windstorm, the exact color or profile is often gone. The carrier approves a repair to the damaged area; the owner is left with a wall or roof that obviously doesn’t match.</p>
<h2>What policies say</h2>
<p>Many policies promise repair or replacement with materials of “like kind and quality.” Some include language about uniform appearance; others expressly limit matching. Approaches vary by state and by policy, and courts have not all agreed on how far the obligation goes. Read your policy and any endorsements, and ask the carrier to explain its position in writing.</p>
<h2>Evidence that helps</h2>
<ul>
<li><strong>Product identification.</strong> A sample sent to a matching service, or a label from leftover materials.</li>
<li><strong>Manufacturer statements</strong> that a color or profile has been discontinued.</li>
<li><strong>Side-by-side photos</strong> of the closest available product against the existing material.</li>
<li><strong>Repairability testing</strong> for older shingles that may break when lifted.</li>
</ul>
<h2>How appraisal panels approach it</h2>
<p>Where matching is owed, a panel can value what a reasonable match costs — which may mean an entire elevation or roof plane, not a handful of pieces. Where matching is a coverage dispute, that question may need to be resolved first. Our <a href="/what-we-appraise/carrier-estimate-second-look/">estimate review</a> can tell you which situation you’re in.</p>
""",
    },
]
