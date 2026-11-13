"""Resources: process guide, grouped FAQ, glossary and guide articles for Utah property owners."""

PROCESS_STEPS = [
    ("Confirm it’s an amount dispute", "Appraisal only answers one question: how much the covered damage costs. Confirm the carrier has accepted coverage for at least part of the loss and that the disagreement is about scope or price."),
    ("Document and supplement", "Gather the carrier’s full estimate, your own estimate, photos and correspondence. Submit a written supplement request explaining what’s missing. Many disputes close here."),
    ("Make the written demand", "If the gap remains, either party can demand appraisal in writing under the policy’s appraisal condition, naming or promising to name an appraiser."),
    ("Each side names an appraiser", "You and the insurer each select a competent, impartial appraiser, usually within a set number of days stated in the policy."),
    ("The appraisers pick an umpire", "The two appraisers agree on a neutral umpire. If they can’t, many policies allow a court in the county where the property sits to appoint one."),
    ("Appraisers work the differences", "The appraisers inspect, compare measurements and pricing, and agree on as many items as they can. Many files end with an agreed award."),
    ("Umpire decides what’s left", "Remaining items go to the umpire, who reviews both positions and the evidence, then joins one appraiser on each disputed item."),
    ("The award is signed and paid", "Two signatures set the amount of loss. The insurer then pays according to the policy, less deductibles and prior payments."),
]

PROCESS_BODY = """
<p>Insurance appraisal is a contract process written into most Utah property policies. It isn’t a lawsuit and it isn’t mediation. It’s a way to have the amount of a covered loss decided by a small panel when you and your insurer can’t agree. The steps below describe how it usually unfolds. Your policy’s wording controls, so read your own appraisal condition alongside this guide.</p>
""" + "".join(
    f'<h2 id="step-{i + 1}">Step {i + 1}: {t}</h2><p>{d}</p>' + extra
    for i, (t, d, extra) in enumerate([
        (*PROCESS_STEPS[0], "<p>Signs that appraisal is the wrong tool include an outright denial, a dispute over whether damage was caused by a covered peril, or an argument about an exclusion such as wear and tear. Those are coverage questions, which generally belong with an attorney.</p>"),
        (*PROCESS_STEPS[1], "<ul><li>The carrier’s complete line-item estimate, not just the summary page</li><li>Your contractor’s or independent estimate, also itemized</li><li>Dated photos, measurements and samples of damaged materials</li><li>All letters and emails in date order</li></ul>"),
        (*PROCESS_STEPS[2], "<p>Send the demand in a way you can prove, such as certified mail plus email. Keep a copy. Check whether your policy requires anything first, such as a sworn proof of loss.</p>"),
        (*PROCESS_STEPS[3], "<p>Choose someone independent of the repair. An appraiser with a financial stake in the contract can give the other side grounds to challenge the award. Get the fee arrangement in writing.</p>"),
        (*PROCESS_STEPS[4], "<p>A good umpire is experienced with the type of loss, has no conflicts and is willing to disclose prior work with either appraiser.</p>"),
        (*PROCESS_STEPS[5], "<p>This stage is where documentation pays off. Clear measurements, photos and pricing support make it easier for the other appraiser to agree.</p>"),
        (*PROCESS_STEPS[6], "<p>The umpire may inspect the property, ask for written positions or hold an informal meeting. The umpire usually decides only the items still in dispute.</p>"),
        (*PROCESS_STEPS[7], "<p>A clear award separates replacement cost, depreciation and actual cash value. Recoverable depreciation is typically paid once repairs are completed within the policy’s time limit.</p>"),
    ])
) + """
<div class="note"><b class="h">Fees</b>Each side pays its own appraiser. Umpire fees are commonly split equally. Ask for fee terms in writing before you sign anything.</div>
<h2>What appraisal doesn’t decide</h2>
<ul>
<li>Whether a loss is covered or excluded.</li>
<li>Whether the insurer handled the claim properly or owes anything beyond the policy.</li>
<li>Questions of law, such as how a policy term should be interpreted.</li>
</ul>
<p>For those questions, talk with a Utah attorney. The Utah Insurance Department also accepts consumer complaints about how claims are handled.</p>
<h2>Utah timing to keep in mind</h2>
<p>Utah law generally gives policyholders three years from the inception of a loss to bring an action on a first-party property policy (Utah Code § 31A-21-313). Policies can contain their own deadlines for notice, proof of loss and recovering depreciation. Appraisal doesn’t automatically pause those clocks, so track them separately. Our <a href="/utah-claim-calculators/claim-timeline-planner/">claim timeline planner</a> can help.</p>
"""

FAQ = [
    ("Appraisal basics", [
        ("What is insurance appraisal?", "A process in most property policies for resolving disagreements about the amount of a covered loss. Each side picks an appraiser, the appraisers pick an umpire, and any two can sign a binding award on the amount."),
        ("Who can demand appraisal?", "Either you or the insurer, in writing, when you disagree on the amount of loss. Check your policy for any steps that must come first."),
        ("Is the award binding?", "On the amount of loss, generally yes, once two of the three panel members sign. Courts can set awards aside in limited situations, such as fraud or a lack of impartiality."),
        ("Does appraisal decide coverage?", "No. It decides how much the covered damage costs. Disputes about whether something is covered are handled separately."),
    ]),
    ("Costs and timing", [
        ("How much does an appraiser cost?", "Fee arrangements vary. Some appraisers charge hourly, some a flat fee and some a percentage of the increase. Each side pays its own appraiser and usually half of the umpire. Get terms in writing."),
        ("How long does appraisal take?", "Many residential appraisals finish within two to four months of both appraisers being named. Complex commercial claims can take longer."),
        ("Is appraisal cheaper than a lawsuit?", "Usually it’s faster and less expensive, because it focuses only on the amount of loss and avoids formal litigation. It also decides less."),
        ("When is a gap too small for appraisal?", "When fees would eat most of the expected increase. Our claim gap and fee estimator shows the math for your numbers."),
    ]),
    ("Utah-specific questions", [
        ("Who regulates insurance in Utah?", "The Utah Insurance Department, led by the insurance commissioner. It licenses insurers, adjusters and public adjusters and accepts consumer complaints."),
        ("Does Utah have a FAIR plan or wind pool?", "Utah doesn’t operate a state FAIR plan or wind pool like some coastal states. Properties that standard carriers decline are typically placed in the surplus lines market. Ask your agent about options."),
        ("How long do I have to sue my insurer in Utah?", "Utah law generally allows three years from the inception of the loss for actions on first-party property policies. Confirm with a Utah attorney, especially if a deadline is close."),
        ("What if I think my insurer acted in bad faith?", "Utah generally treats an insurer’s duty of good faith to its own policyholder as part of the insurance contract, and the Insurance Code lists unfair claim settlement practices that the Insurance Department enforces. These are legal questions for a Utah attorney; appraisal doesn’t address them."),
        ("Is earthquake damage covered in Utah?", "Not under most standard homeowners policies. Earthquake coverage is usually an endorsement or separate policy with a percentage deductible."),
    ]),
    ("Working with us", [
        ("Do you work for the insurance company?", "When we serve as your appraiser, we’re retained by you. When we serve as an umpire, we’re neutral and represent neither side."),
        ("Are you a public adjuster or law firm?", "No. We provide appraisal, estimating and umpire services. We don’t negotiate claims outside appraisal and don’t give legal advice."),
        ("What areas of Utah do you serve?", "All 29 counties, from Cache Valley to Washington County, including mountain and rural properties."),
        ("What should I send for a free review?", "The carrier’s full estimate, your declarations page, photos and any contractor estimate or correspondence."),
    ]),
]

GLOSSARY = [
    ("Actual cash value (ACV)", "Replacement cost minus depreciation. Often the first payment under a replacement cost policy."),
    ("Additional living expense (ALE)", "Coverage for extra costs of living elsewhere while a damaged home is repaired, sometimes called loss of use."),
    ("Amount of loss", "The dollar value of covered damage. This is the only question an appraisal panel decides."),
    ("Appraisal clause", "The policy condition allowing either party to demand appraisal when they disagree on the amount of loss."),
    ("Appraisal award", "The written decision signed by at least two of the three panel members setting the amount of loss."),
    ("Appraiser", "The person each side selects to value the loss and work with the other appraiser and umpire."),
    ("Bad faith", "A general term for an insurer’s unreasonable handling of a claim. In Utah it is usually analyzed under the implied covenant of good faith in the policy; a legal question for an attorney."),
    ("Coinsurance", "A commercial policy condition that can reduce a claim payment if the property is insured for less than a required percentage of its value."),
    ("Coverage A", "Dwelling coverage on a homeowners policy, the limit used to calculate percentage deductibles."),
    ("Coverage B", "Other structures coverage, such as detached garages, sheds and fences."),
    ("Coverage C", "Personal property, or contents, coverage."),
    ("Declarations page", "The summary page of a policy listing limits, deductibles, endorsements and the policy period."),
    ("Depreciation", "The reduction in value due to age, wear and condition, subtracted from replacement cost to find ACV."),
    ("Debris removal", "Coverage for the cost of removing damaged property and debris after a covered loss, often subject to limits."),
    ("Earthquake endorsement", "An addition to a property policy that covers earthquake damage, typically with a percentage deductible."),
    ("Endorsement", "A written change to a policy that adds, removes or modifies coverage."),
    ("Estimate review", "A line-by-line audit of an insurance estimate to identify missing items and pricing gaps."),
    ("Extended replacement cost", "An endorsement that pays above the dwelling limit, by a set percentage, if rebuilding costs more than expected."),
    ("Fair rental value", "Coverage for lost rent when a rental property can’t be occupied because of a covered loss."),
    ("First-party claim", "A claim you make under your own insurance policy, as opposed to a claim against someone else’s policy."),
    ("Holdback", "Recoverable depreciation withheld until repairs are completed, also called recoverable depreciation."),
    ("Ice dam", "A ridge of ice at a roof’s edge that prevents melting snow from draining and can force water under shingles."),
    ("Impartial", "Without bias toward either side. Many appraisal clauses require appraisers and umpires to be impartial or disinterested."),
    ("Line item", "A single entry in an estimate describing a task or material, its quantity and its price."),
    ("Matching", "The question of whether undamaged materials must be replaced so repairs match in color, texture and appearance."),
    ("Mitigation", "Steps taken to prevent further damage after a loss, such as tarping or water extraction. Policies generally require it."),
    ("Ordinance or law coverage", "Coverage for added costs of meeting current building codes when repairing or rebuilding."),
    ("Overhead and profit (O&P)", "A general contractor’s charge, often 10% and 10%, for coordinating multiple trades on a repair."),
    ("Percentage deductible", "A deductible calculated as a percentage of the dwelling limit rather than a flat dollar amount."),
    ("Proof of loss", "A sworn statement of the amount claimed, which an insurer may require within a set time after requesting it."),
    ("Public adjuster", "A licensed professional who represents a policyholder in presenting and negotiating a claim for a fee."),
    ("Recoverable depreciation", "Depreciation that can be recovered after repairs are completed under a replacement cost policy."),
    ("Replacement cost value (RCV)", "The cost to repair or replace damaged property with materials of like kind and quality, without deduction for depreciation."),
    ("Scope of loss", "The full list of damaged items and repairs needed, before pricing."),
    ("Snow load", "The weight of snow and ice on a roof, measured in pounds per square foot."),
    ("Square (roofing)", "100 square feet of roof surface, the standard unit for roofing estimates."),
    ("Steep charge", "An added labor charge for working on roofs above a certain pitch, often 7/12 or 8/12."),
    ("Supplement", "A request to add missing items or costs to an insurance estimate after the initial settlement."),
    ("Surplus lines", "Insurance written by carriers not licensed as standard insurers in a state, often for hard-to-place risks."),
    ("Umpire", "The neutral third member of an appraisal panel who decides items the two appraisers can’t agree on."),
    ("Wildland-urban interface (WUI)", "Areas where homes meet or mix with undeveloped wildland vegetation, raising wildfire risk."),
]

POSTS = [
    {
        "slug": "utah-appraisal-clause-guide",
        "title": "How the Appraisal Clause Works in a Utah Homeowners Policy",
        "seo": "How the Appraisal Clause Works in a Utah Policy",
        "desc": "A plain-English walk through the appraisal clause in a Utah homeowners policy: who can demand it, how the panel works and what the award decides.",
        "summary": "Who can demand appraisal, how appraisers and umpires are chosen, and what the award does and doesn’t decide.",
        "date": "2026-10-20", "read": "7 min",
        "body": """
<p>Somewhere in the conditions section of your Utah homeowners policy, usually after the loss-payment and before the suit provisions, there’s a paragraph titled “Appraisal.” Most people never read it until a claim goes sideways. Here’s what it typically says and how it plays out.</p>
<h2>The trigger: a disagreement on the amount</h2>
<p>The clause applies when you and the insurer “fail to agree on the amount of loss.” That phrase matters. Appraisal resolves disputes about cost and scope. It doesn’t resolve whether a loss is covered. If the insurer says hail damage is just wear and tear, that’s often a causation or coverage question, though appraisers may be asked to address how much damage a storm caused, depending on the policy and the facts.</p>
<h2>The demand</h2>
<p>Either side can demand appraisal in writing. A good demand identifies the claim number, states the disagreement, invokes the appraisal condition and names your appraiser. Keep proof of delivery.</p>
<h2>The panel</h2>
<p>Each party chooses a competent and impartial appraiser, typically within a set number of days. The two appraisers then select an umpire. If they can’t agree, many policies let either party ask a court of record in the county where the property is located to appoint one.</p>
<h2>The process</h2>
<p>The appraisers each value the loss, then compare numbers line by line. Items they agree on are settled. Items they don’t agree on go to the umpire. An award signed by any two of the three sets the amount of loss.</p>
<h2>What it costs</h2>
<p>Each side pays its own appraiser. Umpire costs are usually shared equally. Ask for fee terms in writing before you hire anyone.</p>
<h2>What the award doesn’t do</h2>
<ul><li>It doesn’t decide coverage.</li><li>It doesn’t address how the claim was handled.</li><li>It doesn’t change policy limits or deductibles.</li></ul>
<div class="note"><b class="h">Deadlines still run</b>Utah generally allows three years from the inception of a loss to bring an action on a first-party policy, but your policy has its own notice, proof-of-loss and depreciation deadlines. Track them independently.</div>
""",
    },
    {
        "slug": "snow-load-ice-dam-claims",
        "title": "Snow Load and Ice Dam Claims After a Heavy Utah Winter",
        "seo": "Snow Load & Ice Dam Claims After a Heavy Utah Winter",
        "desc": "What Utah homeowners should know about snow-load roof damage and ice-dam leaks: documenting the loss, hidden damage and common estimate gaps.",
        "summary": "How to document snow-load and ice-dam damage, what estimates commonly miss and where coverage gets tricky.",
        "date": "2026-10-06", "read": "6 min",
        "body": """
<p>Utah winters can deliver months of snow on the same roof. The 2022–23 season set records across northern Utah, and claims for collapsed carports, sagging roofs and ice-dam leaks followed. Here’s how to approach those claims.</p>
<h2>Snow load: what to look for</h2>
<ul><li>Sagging ridgelines or rooflines</li><li>New cracks in drywall, especially near ceilings and door frames</li><li>Doors and windows that suddenly stick</li><li>Cracked or bowed rafters and trusses visible in the attic</li><li>Damaged carports, patio covers, decks and outbuildings</li></ul>
<p>If you suspect structural damage, stay safe and get the roof evaluated before anyone climbs on it. An engineer’s report can become an important part of the claim.</p>
<h2>Ice dams: where the water goes</h2>
<p>When warm attic air melts snow on the roof, water runs down to the cold eaves and refreezes, creating a dam. Meltwater then backs up under shingles and into walls, ceilings and insulation. The visible stain is usually a fraction of the damage.</p>
<h2>What estimates commonly miss</h2>
<ul><li>Wet insulation and vapor barriers in attics and exterior walls</li><li>Drying and mold prevention inside wall cavities</li><li>Ice-and-water shield along eaves when roofing is replaced</li><li>Structural repair and engineering costs for snow load</li><li>Interior finishes removed to dry the structure</li></ul>
<h2>Coverage wrinkles</h2>
<p>Many policies cover sudden water damage from ice dams and collapse from the weight of snow and ice, but they may exclude the ice dam itself, gradual leaks or maintenance issues. Read your policy’s collapse and water damage provisions.</p>
<p>To estimate what a roof was carrying, try our <a href="/utah-claim-calculators/roof-snow-load-estimator/">roof snow load estimator</a>. Example figures it produces are illustrative, not engineering conclusions.</p>
""",
    },
    {
        "slug": "canyon-windstorm-claim-checklist",
        "title": "After a Canyon Windstorm: A Claim Checklist for Wasatch Front Homes",
        "seo": "Canyon Windstorm Claim Checklist for Wasatch Front Homes",
        "desc": "A checklist for Davis, Weber and Salt Lake County homeowners after a canyon windstorm: safety, documentation, trees, fences and estimate gaps.",
        "summary": "A step-by-step list for the days after a downslope windstorm, from tree removal to fence and siding scope.",
        "date": "2026-09-22", "read": "5 min",
        "body": """
<p>The east winds that roared through Davis County in December 2011 and again in September 2020 left neighborhoods covered in branches, shingles and fence panels. If your home is in the windstorm corridor, here’s a checklist for the days that follow.</p>
<h2>First 48 hours</h2>
<ol><li>Stay clear of downed power lines and call the utility.</li><li>Photograph everything before cleanup: trees, debris, roof, siding, fences, vehicles.</li><li>Make temporary repairs such as tarps and board-ups. Keep receipts.</li><li>Report the claim to your insurer as soon as you can.</li></ol>
<h2>Trees</h2>
<p>Note where each tree fell and what it hit. Policies often treat trees that strike a covered structure differently from trees that fall in open yard. Keep invoices for removal and photograph stumps and root balls.</p>
<h2>Roof and siding</h2>
<p>Look for missing, creased or lifted shingles, damaged ridge caps and loose flashing. Check every elevation for cracked or missing siding. Matching is a frequent issue with older vinyl and aluminum siding.</p>
<h2>Fences and outbuildings</h2>
<p>Wind claims often include long fence runs, sheds, pergolas and play sets. Measure fence lengths and photograph every damaged panel and post.</p>
<h2>Interior</h2>
<p>Wind-driven rain and snow can enter through damaged roofs and windows. Check attics and ceilings for moisture in the days after the storm.</p>
<h2>When the estimate arrives</h2>
<p>Compare it with your own list. Missing elevations, partial fence runs and limited tree removal are common gaps. A <a href="/utah-appraisal-services/insurance-estimate-audit/">line-by-line estimate review</a> can show what’s been left out.</p>
""",
    },
    {
        "slug": "earthquake-coverage-deductibles",
        "title": "Earthquake Coverage in Utah: Endorsements, Deductibles and Appraisal",
        "seo": "Utah Earthquake Coverage: Deductibles & Appraisal",
        "desc": "How earthquake coverage typically works for Utah homeowners: endorsements, percentage deductibles, documenting cracks and when appraisal makes sense.",
        "summary": "Why most Utah homeowners policies exclude earthquakes, how percentage deductibles work and how appraisal fits in.",
        "date": "2026-09-08", "read": "6 min",
        "body": """
<p>The magnitude 5.7 Magna earthquake on March 18, 2020 reminded the Wasatch Front that it sits on an active fault system. Many homeowners learned afterward that their policies didn’t cover the damage. Here’s how earthquake coverage generally works.</p>
<h2>The standard exclusion</h2>
<p>Most homeowners policies exclude earth movement, including earthquakes. Coverage is typically added through an endorsement or a separate policy.</p>
<h2>Percentage deductibles</h2>
<p>Earthquake deductibles are usually a percentage of the dwelling limit, commonly 10% to 20% or more. As an illustrative example, a home insured for $450,000 with a 15% deductible would carry a $67,500 deductible. Many smaller claims never exceed it.</p>
<h2>Documenting earthquake damage</h2>
<ul><li>Photograph cracks with a ruler or tape for scale.</li><li>Compare with any earlier photos of the same areas.</li><li>Note fresh, clean crack edges versus older, dirty or painted-over cracks.</li><li>Check chimneys, masonry, foundations and plaster.</li><li>Consider an engineer’s evaluation for structural issues.</li></ul>
<h2>When appraisal makes sense</h2>
<p>If the insurer accepts coverage but disputes the amount, appraisal can resolve it. Because of high deductibles, the key question is whether the disputed amount moves the payment meaningfully. Our <a href="/utah-claim-calculators/percentage-deductible-calculator/">percentage deductible calculator</a> makes that comparison easy.</p>
<div class="note"><b class="h">Coverage questions</b>Disputes about whether cracking was caused by an earthquake or by settling can involve coverage and causation. Some may be addressed in appraisal, others may need an attorney.</div>
""",
    },
    {
        "slug": "wildfire-smoke-documentation",
        "title": "Wildfire Smoke Claims: What Utah Homeowners Should Document",
        "seo": "Wildfire Smoke Claims: What Utah Owners Should Document",
        "desc": "Wildfire smoke and ash can damage Utah homes that never burned. Learn what to document, when to test and how smoke claims are commonly underpaid.",
        "summary": "Smoke and ash can damage homes miles from the flames. Here’s how to document it and what estimates often miss.",
        "date": "2026-08-25", "read": "5 min",
        "body": """
<p>When a wildfire burns near a Utah neighborhood, the homes that didn’t burn can still be damaged. Smoke, soot and ash work their way into HVAC systems, insulation, carpet and furniture. These claims are common and frequently underpaid.</p>
<h2>Signs of smoke damage</h2>
<ul><li>Persistent smoke odor inside the home</li><li>Soot or discoloration around vents, outlets and windows</li><li>Ash on roofs, decks, gutters and in landscaping</li><li>Dirty HVAC filters and ductwork</li><li>Residue on soft goods such as curtains, bedding and clothing</li></ul>
<h2>What to document</h2>
<p>Photograph soot and ash, save air filters and keep records of evacuation orders and fire perimeters. Professional testing by an industrial hygienist or environmental lab can identify smoke particles and support the cleaning scope.</p>
<h2>Where estimates fall short</h2>
<ul><li>Cleaning limited to a few rooms instead of the whole home</li><li>No HVAC cleaning or filter replacement</li><li>Soft goods and contents left out</li><li>No sealing or deodorization of framing and attic spaces</li><li>Exterior cleaning of siding, decks and roofs ignored</li></ul>
<h2>Next steps</h2>
<p>Report the claim promptly, document thoroughly and request the carrier’s full estimate. If it falls short, an estimate review or <a href="/utah-appraisal-services/wildfire-claim-appraisal/">wildfire claim appraisal</a> can help close the gap.</p>
""",
    },
    {
        "slug": "choosing-claim-help",
        "title": "Appraiser, Public Adjuster or Attorney: Choosing Help for a Utah Claim",
        "seo": "Appraiser, Public Adjuster or Attorney? Utah Claim Help",
        "desc": "How an appraiser, a public adjuster and an attorney differ on a Utah property claim, and how to decide which one fits your situation and stage.",
        "summary": "Each professional solves a different problem. Here’s how to match the help to the dispute.",
        "date": "2026-08-11", "read": "6 min",
        "body": """
<p>When a claim goes wrong, the hardest part can be deciding who to call. An appraiser, a public adjuster and an attorney each handle different problems. Here’s a simple way to sort it out.</p>
<h2>Start with the question you need answered</h2>
<div class="table-wrap"><table><thead><tr><th>Your situation</th><th>Usually a fit for</th></tr></thead><tbody>
<tr><th>Coverage accepted, amount disputed</th><td>Appraiser</td></tr>
<tr><th>Early in a complex claim, need help presenting it</th><td>Public adjuster</td></tr>
<tr><th>Claim denied, coverage dispute or deadline near</th><td>Attorney</td></tr>
<tr><th>Need to know if the estimate is low</th><td>Estimate review</td></tr>
</tbody></table></div>
<h2>Appraisers</h2>
<p>An appraiser works within the policy’s appraisal clause on the amount of loss. The result is a binding award on the amount. Appraisers don’t decide coverage or give legal advice.</p>
<h2>Public adjusters</h2>
<p>Public adjusters in Utah are licensed by the Utah Insurance Department. They prepare and negotiate claims on the policyholder’s behalf, usually for a percentage fee. They can be involved from the start of a claim.</p>
<h2>Attorneys</h2>
<p>Attorneys handle legal disputes: denials, coverage interpretation, claims-handling issues and lawsuits. If a deadline is approaching or the insurer has denied coverage, talk with a Utah attorney promptly.</p>
<h2>Using more than one</h2>
<p>These roles can work together. An attorney may recommend appraisal for the amount while handling coverage separately. A public adjuster may bring in an appraiser once appraisal is demanded. What matters is that each role is clear.</p>
""",
    },
]
