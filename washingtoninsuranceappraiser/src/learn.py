"""Resources: process guide, FAQ, glossary and guide articles (original copy for Washington)."""

PROCESS_STEPS = [
    ("Put the disagreement on paper", "Appraisal starts with a claim the insurer has accepted at least in part. Before anything formal happens, write down what you think the estimate misses, attach your contractor’s figures and photos, and ask the adjuster to reconsider. Insurers in Washington are expected to respond to claim communications promptly under the state’s claims-handling rules, and many gaps close at this stage through a supplement."),
    ("Send the written demand", "If the gap remains, either side may demand appraisal in writing. A clear demand identifies the claim, says the parties disagree on the amount of loss, invokes the appraisal condition and names your appraiser or commits to naming one within the policy’s time frame. Send it in a way you can prove, such as email plus certified mail. Check first whether the policy requires a sworn proof of loss or other step."),
    ("Each side names an appraiser", "Each party picks a competent, independent appraiser, often within 20 days of the demand. Your appraiser inspects the property, studies the file and builds a line-item valuation. The insurer’s appraiser does the same. The two exchange estimates and start working through the differences."),
    ("The appraisers choose an umpire", "The two appraisers agree on a neutral umpire, ideally early so one is ready if needed. If they can’t agree within the time the policy allows, commonly 15 days, either side can ask a court of record in the county where the property is located to appoint one. In Washington, that is usually the superior court."),
    ("The appraisers work the numbers", "Most of the work happens here. The appraisers walk the property together, compare measurements and pricing, and agree on as many line items as they can. Many appraisals end at this stage with both appraisers signing an agreed award, and no umpire decision is needed."),
    ("The umpire decides what’s left", "Items the appraisers can’t settle go to the umpire. Each appraiser submits a position with supporting evidence. The umpire may inspect, ask questions or hold an informal meeting, then decides each disputed item."),
    ("The award is signed and paid", "An award signed by any two of the three sets the amount of loss. A good award separates replacement cost, depreciation and actual cash value by coverage. The insurer then pays under the policy, less the deductible and earlier payments, with recoverable depreciation paid once repairs are done."),
]

PROCESS_BODY = "".join(f'<h2 id="step-{i + 1}">Step {i + 1}: {t}</h2><p>{p}</p>' for i, (t, p) in enumerate(PROCESS_STEPS)) + """
<div class="note"><b class="h">Who pays</b>Each side pays its own appraiser. The umpire’s fee is usually split equally. Ask any appraiser, including us, to put the fee arrangement in writing before you sign anything.</div>
<h2>What appraisal won’t do</h2>
<ul>
<li>It won’t decide whether the loss is covered.</li>
<li>It won’t award interest, extra-contractual damages or attorney fees, including under the Insurance Fair Conduct Act.</li>
<li>It won’t automatically pause your policy’s suit-limitation clock.</li>
<li>It won’t produce an amount above your policy limits.</li>
</ul>
<h2>Where Washington-specific rules come in</h2>
<p>Washington regulates how insurers handle claims through the Office of the Insurance Commissioner and the claims-handling rules in chapter 284-30 of the Washington Administrative Code. The state also has a bad-faith statute, the Insurance Fair Conduct Act, that gives policyholders legal remedies in some situations. Those are legal matters for an attorney. Our role is the valuation.</p>
"""

FAQ = [
    ("Appraisal basics", [
        ("What is insurance appraisal?", "It is a process written into most property policies for settling disagreements about the amount of a covered loss. Each side names an appraiser, the appraisers choose an umpire, and an award signed by two of the three sets the amount."),
        ("Is appraisal the same as arbitration?", "They’re similar but not the same. Appraisal is narrower: it decides the amount of loss, not legal questions or coverage. It’s usually less formal and faster."),
        ("Who can demand appraisal?", "Either you or the insurer, as long as the policy has an appraisal clause and the disagreement is about the amount of loss."),
        ("Is the award binding?", "On the amount of loss, yes, once two of the three panel members sign. Courts can set awards aside in limited circumstances, such as fraud or a panel exceeding its authority."),
        ("Does appraisal decide coverage?", "No. If the insurer says something isn’t covered, that is a coverage dispute. Appraisal can value the damage, but whether it is payable may still be argued."),
    ]),
    ("Costs and timing", [
        ("How much does appraisal cost?", "Each side pays its own appraiser and usually half the umpire’s fee. Appraiser fees may be flat, hourly or a percentage of the increase. Get any arrangement in writing before work starts."),
        ("How long does it take?", "Straightforward home claims often finish in six to twelve weeks after both appraisers are named. Commercial and total-loss claims take longer."),
        ("When is a gap too small for appraisal?", "As a rough guide, if the difference is under about 10% of the insurer’s estimate or a few thousand dollars, a documented supplement request may be more cost-effective. Our appraisal payoff calculator can help you check."),
        ("Does appraisal stop the suit-limitation deadline?", "Not automatically. Washington law does not let policies shorten the time to sue to less than one year from the loss, and many homeowner policies use exactly one year. Protect that deadline separately and talk to an attorney if it’s close."),
    ]),
    ("Washington rules", [
        ("Who regulates insurers in Washington?", "The Office of the Insurance Commissioner (OIC), based in Tumwater. It licenses insurers and adjusters, enforces claims-handling rules and takes consumer complaints."),
        ("What is the Insurance Fair Conduct Act?", "IFCA is a Washington law that gives policyholders a legal remedy when an insurer unreasonably denies coverage or payment of benefits. It has notice requirements before suit. It is a legal claim, separate from appraisal, so ask a Washington attorney about it."),
        ("Does Washington have a FAIR plan or wind pool?", "Washington does not currently operate a state FAIR plan or windstorm pool like some coastal states. Homeowners who can’t find standard coverage often turn to the surplus lines market. Lawmakers and the OIC have discussed options as wildfire risk grows."),
        ("Is earthquake covered?", "Not under standard homeowner policies. Earthquake coverage is sold separately or by endorsement, usually with a percentage deductible such as 10% to 20% of the dwelling limit."),
        ("Is flood covered?", "Not under standard homeowner policies. Flood from rising water requires separate flood insurance, such as through the National Flood Insurance Program."),
    ]),
    ("Working with us", [
        ("Are you a public adjuster or a law firm?", "Neither. We provide appraisal, estimate review and umpire services. We don’t negotiate claims outside the appraisal process and we don’t give legal advice."),
        ("Do you serve the whole state?", "Yes. We work in all 39 Washington counties, from Puget Sound and the coast to the Columbia Basin and the Inland Northwest."),
        ("What should I send for a first review?", "The insurer’s full estimate, your declarations page, any contractor estimate, photos and the most important letters or emails from the insurer."),
        ("Can I hire you after the insurer has already demanded appraisal?", "Yes. We can step in as your appraiser at any point after a demand, as long as the policy’s deadlines are met."),
    ]),
]

GLOSSARY = [
    ("Actual cash value (ACV)", "Replacement cost minus depreciation. Many policies pay ACV first, then pay the depreciation once repairs are made."),
    ("Additional living expense (ALE)", "Coverage for the extra cost of living elsewhere while a home is being repaired after a covered loss. Often called Coverage D or loss of use."),
    ("Amount of loss", "The dollar value of covered damage. This is what an appraisal panel decides."),
    ("Appraisal award", "The written decision of an appraisal panel setting the amount of loss, signed by at least two of the three panel members."),
    ("Appraisal clause", "The policy condition that lets either party demand appraisal when they disagree on the amount of loss."),
    ("Atmospheric river", "A long, narrow band of moisture that brings heavy, sustained rain. Western Washington sees several each winter."),
    ("Bomb cyclone", "A storm whose pressure drops very quickly, producing strong winds. The November 2024 storm that hit Puget Sound was one."),
    ("Code upgrade", "Work needed to bring repairs up to current building codes. Usually paid under ordinance or law coverage."),
    ("Collapse", "A sudden falling down of a building or part of it. Policies define it narrowly and cover it only in certain situations."),
    ("Contents", "Personal belongings, covered under Coverage C in most homeowner policies."),
    ("Coverage A", "Dwelling coverage for the house itself and attached structures."),
    ("Coverage B", "Other structures coverage for detached garages, sheds, fences and similar."),
    ("Declarations page", "The summary page of your policy showing coverages, limits, deductibles and the policy period."),
    ("Debris removal", "Coverage for removing damaged property and debris after a covered loss, often with a separate limit."),
    ("Depreciation", "The reduction in value because of age, wear or obsolescence. Subtracted from replacement cost to get ACV."),
    ("Earthquake deductible", "A separate deductible for earthquake coverage, usually a percentage of the dwelling limit."),
    ("Extended replacement cost", "An endorsement that pays above the dwelling limit, such as 25% or 50% more, if rebuilding costs exceed it."),
    ("Flood exclusion", "The standard policy exclusion for damage from surface water, rising rivers and similar. Flood needs separate coverage."),
    ("HO-3", "The most common homeowner policy form, covering the dwelling on an open-perils basis and contents on a named-perils basis."),
    ("HO-6", "A policy for condominium unit owners covering unit improvements, contents and liability."),
    ("Holdback", "Recoverable depreciation the insurer withholds until repairs are completed."),
    ("Ice dam", "A ridge of ice at the roof edge that traps melting snow, which can back up under shingles and leak inside."),
    ("IFCA", "Washington’s Insurance Fair Conduct Act, which provides legal remedies for unreasonable denial of coverage or benefits."),
    ("Independent appraiser", "An appraiser with no financial interest in the outcome or the repair contract, as most appraisal clauses require."),
    ("Line item", "A single entry in an estimate, such as removing and replacing a square of shingles."),
    ("Master policy", "The insurance policy a condominium or homeowners association buys to cover common areas and building elements."),
    ("Matching", "Whether replacement materials must match undamaged ones so the repair looks uniform. A common source of dispute."),
    ("Mitigation", "Steps taken to prevent further damage after a loss, such as tarping or water extraction. Policies require it."),
    ("OIC", "The Washington Office of the Insurance Commissioner, the state regulator of insurance companies and agents."),
    ("Ordinance or law coverage", "Coverage for extra costs caused by building codes or laws when repairing or rebuilding."),
    ("Overhead and profit (O&P)", "A general contractor’s charge for coordinating multiple trades, often 10% overhead plus 10% profit."),
    ("Proof of loss", "A sworn statement of the amount claimed, which the insurer may request within a set time."),
    ("Recoverable depreciation", "Depreciation you can collect after completing repairs under a replacement cost policy."),
    ("Replacement cost value (RCV)", "The cost to repair or replace damaged property with materials of like kind and quality, without deducting depreciation."),
    ("Scope of loss", "The list of everything that is damaged and how it must be repaired. The foundation of any estimate."),
    ("Steep charge", "Extra labor cost for working on roofs with a steep pitch, often 7/12 and above."),
    ("Suit limitation", "The policy clause setting how long you have to file a lawsuit. Washington law sets a one-year minimum."),
    ("Supplement", "A request to the insurer to add items or money to an estimate, supported by documentation."),
    ("Surplus lines", "Insurance from carriers not licensed in the state but allowed to write coverage that the standard market won’t."),
    ("Umpire", "The neutral third member of an appraisal panel who decides items the two appraisers can’t agree on."),
    ("Xactimate", "Estimating software used by most insurers and contractors, with regional price lists."),
]

POSTS = [
    {
        "slug": "washington-appraisal-clause-guide",
        "title": "The Appraisal Clause in Washington Policies: A Plain-English Guide",
        "seo": "Washington Appraisal Clause Explained | Plain-English Guide",
        "desc": "What the appraisal clause in a Washington home or business policy says, how a demand works, and what an appraisal panel can and can’t decide.",
        "summary": "What the clause says, how a demand works and the limits of what a panel can decide.",
        "read": "7 min", "date": "2026-10-06",
        "body": """
<p>Most people never read the conditions section of their property policy until something goes wrong. Buried there, usually after “Loss Payment” and before “Suit Against Us,” is a short paragraph called <strong>Appraisal</strong>. If you live in Washington and your claim is stuck on a number, it may be the most useful paragraph in the policy.</p>
<h2>What a typical clause says</h2>
<p>Wording varies, but most clauses follow the same pattern:</p>
<ul>
<li>If you and the insurer fail to agree on the amount of loss, either may demand appraisal in writing.</li>
<li>Each party selects a competent and independent appraiser within a set time, often 20 days.</li>
<li>The two appraisers select an umpire. If they can’t agree, either may ask a court of record where the property is located to choose one.</li>
<li>The appraisers set the amount of loss. If they don’t agree, they submit their differences to the umpire.</li>
<li>A decision agreed to by any two will set the amount of loss.</li>
<li>Each party pays its own appraiser and shares the umpire’s costs equally.</li>
</ul>
<h2>Amount of loss, not coverage</h2>
<p>The key phrase is “amount of loss.” Appraisal answers how much covered damage costs. It doesn’t decide whether damage is covered at all, whether an exclusion applies, or whether the insurer handled the claim properly. Those questions belong to the insurer, the Office of the Insurance Commissioner or a court.</p>
<p>In practice, the line can blur. Is a cracked shingle storm damage or old wear? Is wet drywall from the windstorm or a long-term leak? Panels often have to decide what damage was caused by the event in order to value it. Well-written awards make clear what the panel decided.</p>
<h2>When it makes sense in Washington</h2>
<p>Appraisal works best when coverage is accepted and the gap is meaningful. Typical examples include a windstorm roof claim where the insurer approved two slopes and your roofer says the whole roof, a fir through the garage where structural framing was left out, or a smoke claim where only a few rooms were scheduled for cleaning.</p>
<h2>When it doesn’t</h2>
<p>If the insurer denied the claim, delayed it without reason or you believe it acted in bad faith, appraisal won’t solve that. Washington’s Insurance Fair Conduct Act and the state’s claims-handling rules may give you other options. Those are legal questions, so speak with a Washington attorney.</p>
<div class="note"><b class="h">Practical tip</b>Before demanding appraisal, find your policy’s suit-limitation clause and calendar the date. Many Washington homeowner policies allow one year from the loss, which is the minimum state law permits.</div>
""",
    },
    {
        "slug": "appraisal-oic-complaint-or-ifca",
        "title": "Appraisal, an OIC Complaint or an IFCA Claim: Which Path Fits?",
        "seo": "Appraisal vs. OIC Complaint vs. IFCA Claim in Washington",
        "desc": "Three ways Washington policyholders push back on a claim: appraisal, an OIC complaint or an IFCA claim. Here is when each path tends to fit.",
        "summary": "Three ways to push back on a claim in Washington, and the problem each one is built to solve.",
        "read": "6 min", "date": "2026-10-13",
        "body": """
<p>When a property claim stalls in Washington, owners usually have three main paths. Each solves a different problem. Picking the right one first saves time, money and frustration.</p>
<h2>1. Appraisal: when the dispute is the number</h2>
<p>Appraisal is a contract right in most property policies. It fits when the insurer accepts that the loss is covered but you disagree on what it costs to repair. Each side names an appraiser, the appraisers pick an umpire, and two signatures set the amount of loss.</p>
<ul>
<li><strong>Best for:</strong> scope and price disputes on accepted claims.</li>
<li><strong>Result:</strong> a binding award on the amount of loss.</li>
<li><strong>Cost:</strong> your appraiser’s fee plus half the umpire’s.</li>
</ul>
<h2>2. An OIC complaint: when the handling is the problem</h2>
<p>The Washington Office of the Insurance Commissioner regulates insurers and takes consumer complaints. If the insurer isn’t responding, isn’t explaining its decisions or seems to be ignoring the rules, a complaint asks the OIC to look into it. The OIC’s consumer advocates contact the insurer and ask for a response.</p>
<ul>
<li><strong>Best for:</strong> delays, lack of communication, unexplained decisions.</li>
<li><strong>Result:</strong> the insurer must respond to the regulator. The OIC can’t act as your lawyer or order a specific payment in most cases.</li>
<li><strong>Cost:</strong> free.</li>
</ul>
<h2>3. An IFCA claim: when you believe the insurer acted unreasonably</h2>
<p>Washington’s Insurance Fair Conduct Act gives policyholders a legal remedy if an insurer unreasonably denies a claim for coverage or payment of benefits. The law includes a requirement to give written notice to the insurer and the OIC before filing suit. It is a legal claim, and only an attorney can advise you on whether you have one.</p>
<ul>
<li><strong>Best for:</strong> denials or conduct you believe was unreasonable.</li>
<li><strong>Result:</strong> potentially damages beyond the policy amount, decided by a court or settlement.</li>
<li><strong>Cost:</strong> attorney fees, often on contingency. The statute may allow recovery of fees.</li>
</ul>
<h2>Can you use more than one?</h2>
<p>Often, yes. A claim can go to appraisal to settle the amount while an attorney evaluates handling issues. An OIC complaint can run alongside either. The order matters, though, and deadlines apply. If legal questions are involved, talk to an attorney before you invoke appraisal.</p>
<div class="note"><b class="h">Our role</b>We are appraisers, not attorneys. We can tell you whether your dispute looks like a valuation problem, and we’ll say so plainly when it doesn’t.</div>
""",
    },
    {
        "slug": "documenting-windstorm-tree-damage",
        "title": "How to Document Windstorm and Fallen Tree Damage",
        "seo": "How to Document Windstorm & Fallen Tree Damage in WA",
        "desc": "A practical checklist for documenting windstorm and fallen tree damage in Washington, from first photos to structural reports and receipts.",
        "summary": "A practical checklist for the first days after a Pacific windstorm or a tree through the roof.",
        "read": "6 min", "date": "2026-10-20",
        "body": """
<p>When a winter windstorm sweeps through western Washington, the first hours are about safety: downed lines, blocked roads, no power. Once everyone is safe, good documentation is the single biggest thing you can do to protect your claim.</p>
<h2>Before anything is moved</h2>
<ul>
<li><strong>Photograph wide, then close.</strong> Start with each side of the house from the street, then move closer. Get the tree where it lies, the root ball or break point, and every point of contact.</li>
<li><strong>Take video.</strong> A slow walk-around video with narration captures context photos miss.</li>
<li><strong>Note the date and time.</strong> Write down when the storm hit and when you found the damage.</li>
<li><strong>Save weather records.</strong> National Weather Service reports and local news coverage tie damage to the event.</li>
</ul>
<h2>Protecting the property</h2>
<p>Your policy requires reasonable steps to prevent further damage. Tarp openings, shut off water if pipes are broken and move belongings away from leaks. Keep every receipt, and photograph temporary repairs before and after.</p>
<p>If a tree must be removed before the adjuster arrives, document it thoroughly first, tell the insurer and keep the arborist’s or tree service’s invoice. Ask whether cut sections should be kept.</p>
<h2>Inside the house</h2>
<p>Damage from a fallen tree or wind-driven rain often shows up indoors over days: stains on ceilings, cracked drywall, sticking doors and windows. Photograph each room and recheck after a week.</p>
<h2>Structural questions</h2>
<p>A heavy fir can crack rafters, trusses and walls even when the roof looks repairable. If doors stick, floors slope or walls crack after an impact, ask for a structural engineer’s evaluation. Its findings give everyone a clear basis for the repair scope.</p>
<h2>Roof and siding</h2>
<p>Wind damage is directional. Note which slopes and walls faced the wind. Look for creased or missing shingles, lifted tabs, broken seals and siding pulled from its fasteners. Photograph with a tape measure or coin for scale.</p>
<h2>Keep a claim log</h2>
<p>Record every call, email and visit: date, name, what was said. Organized records make supplements, complaints or appraisal much easier later.</p>
""",
    },
    {
        "slug": "wildfire-total-loss-claim-checklist",
        "title": "Wildfire Total Loss: A Claim Checklist for Washington Homeowners",
        "seo": "Wildfire Total Loss Claim Checklist for Washington Homes",
        "desc": "A checklist for Washington homeowners after a wildfire total loss: dwelling limits, contents, living costs, debris removal and rebuild costs.",
        "summary": "Limits, contents, living expenses and rebuild costs after a home is lost to wildfire.",
        "read": "8 min", "date": "2026-10-27",
        "body": """
<p>Losing a home to wildfire is overwhelming. In the weeks after the 2023 Gray and Oregon Road fires near Spokane, and after the Carlton Complex and Malden fires before them, families had to make insurance decisions while dealing with displacement and grief. This checklist is meant to make the claim side a little more manageable.</p>
<h2>First steps</h2>
<ul>
<li>Report the claim and get a claim number and adjuster contact.</li>
<li>Ask for a complete copy of your policy, including all endorsements and the declarations page.</li>
<li>Ask about an advance on additional living expenses and contents.</li>
<li>Start a claim log of every call, email and payment.</li>
</ul>
<h2>Coverage A: is the limit enough?</h2>
<p>Compare your dwelling limit with real rebuild costs. Post-fire demand for contractors and current code requirements can push costs up. Check whether you have extended replacement cost, which pays a set percentage above the limit, and ordinance or law coverage for code upgrades. Our <a href="/free-claim-calculators/wildfire-total-loss-coverage-check/">wildfire total-loss coverage check</a> helps you test the numbers.</p>
<h2>Contents</h2>
<p>A full inventory after a total loss is a huge task. Ask the insurer whether it will accept a partial inventory or pay part of the contents limit without one. Use photos, videos, bank and credit card records and online order histories to rebuild your list room by room.</p>
<h2>Additional living expenses</h2>
<p>ALE covers the extra cost of living elsewhere: rent, increased food costs, mileage and more. Keep every receipt, and ask how long ALE lasts and whether it has a dollar limit.</p>
<h2>Debris removal and site work</h2>
<p>Ash, burned materials and hazardous debris must be removed before rebuilding. Policies often have a separate or limited debris removal amount. Ask how your policy handles it, and whether government cleanup programs apply.</p>
<h2>Rebuild or buy elsewhere?</h2>
<p>Some policies let you rebuild on another lot or buy an existing home and still collect replacement cost, sometimes with limits. Get the insurer’s position in writing before you decide.</p>
<h2>When numbers don’t match</h2>
<p>If the insurer’s rebuild estimate is well below contractor bids, an estimate review or appraisal may help with the amount. If the dispute is about limits, policy terms or how the claim is being handled, contact the OIC’s consumer advocates or a Washington attorney.</p>
""",
    },
    {
        "slug": "frozen-pipes-ice-dams-coverage",
        "title": "Frozen Pipes and Ice Dams: What Washington Policies Usually Say",
        "seo": "Frozen Pipe & Ice Dam Claims in Washington: Policy Basics",
        "desc": "How Washington homeowner policies usually treat frozen pipe and ice dam claims, the conditions insurers raise and how to document the damage.",
        "summary": "How policies usually treat winter water damage, and the conditions insurers tend to raise.",
        "read": "5 min", "date": "2026-11-03",
        "body": """
<p>Western Washington isn’t built for long freezes. When an arctic blast arrives, as it did in December 2008, February 2019 and January 2024, pipes in crawl spaces, garages and exterior walls split. East of the mountains, Spokane and Wenatchee winters bring snow, ice dams and cold snaps every year.</p>
<h2>Frozen pipes</h2>
<p>Most homeowner policies cover sudden water damage from a pipe that freezes and bursts. The pipe itself may not be covered, but tearing out walls or floors to reach it and repairing the water damage usually is.</p>
<p>Policies commonly include a condition: if the home is vacant, unoccupied or under construction, you must use reasonable care to maintain heat or shut off and drain the water. Second homes and cabins are where this condition comes up most.</p>
<h2>Ice dams</h2>
<p>An ice dam forms when heat from the house melts snow on the roof and the water refreezes at the cold eaves. Water backs up under the shingles and leaks into walls and ceilings. Many policies cover the resulting water damage. Insurers sometimes argue poor insulation or ventilation caused it, raising maintenance questions.</p>
<h2>Snow load and collapse</h2>
<p>Heavy snow can collapse carports, patio covers, barns and older roofs. Policies define collapse narrowly, and some limit coverage for certain structures. Read the collapse section carefully.</p>
<h2>Documenting winter damage</h2>
<ul>
<li>Photograph ice dams, icicles and snow depth on the roof before it melts.</li>
<li>Photograph the burst pipe and keep the failed section.</li>
<li>Record indoor temperatures and thermostat settings if you can.</li>
<li>Keep plumber, mitigation and utility records.</li>
</ul>
<p>Once coverage is accepted, the remaining question is the amount of loss. That’s where an estimate review or appraisal can help.</p>
""",
    },
    {
        "slug": "reading-your-insurer-estimate",
        "title": "How to Read Your Insurer’s Estimate Line by Line",
        "seo": "How to Read an Insurance Estimate Line by Line",
        "desc": "How to read an insurer’s property estimate: line items, quantities, depreciation, overhead and profit, and where the gaps usually hide.",
        "summary": "Line items, quantities, depreciation and O&P, and where the gaps usually hide.",
        "read": "7 min", "date": "2026-11-10",
        "body": """
<p>Insurance estimates can run dozens of pages of codes and abbreviations. You don’t need to be an estimator to find the most common problems, though. Here’s how to read one.</p>
<h2>Start with the summary</h2>
<p>The summary page shows replacement cost (RCV), depreciation, actual cash value (ACV), the deductible and the net payment. Check that the deductible matches your declarations page and that prior payments are listed correctly.</p>
<h2>Check the rooms and areas</h2>
<p>Estimates are organized by room or area: roof, elevations, kitchen, living room. Make a list of every damaged area and confirm each appears. Missing rooms are one of the simplest gaps to find.</p>
<h2>Read each line item</h2>
<p>Each line has a description, quantity, unit and unit price. Look for:</p>
<ul>
<li><strong>Quantities:</strong> does the square footage of drywall or flooring match the room’s size?</li>
<li><strong>Remove and replace:</strong> does the line include removing old material, or only installing new?</li>
<li><strong>Related trades:</strong> painting after drywall, baseboards after flooring, detach and reset of fixtures.</li>
<li><strong>Roof extras:</strong> starter, ridge cap, drip edge, underlayment, steep and high charges.</li>
</ul>
<h2>Depreciation</h2>
<p>Depreciation should reflect age and condition. Look for very high percentages on newer items, depreciation on labor where the policy may not allow it, and whether the depreciation is recoverable.</p>
<h2>Overhead and profit</h2>
<p>When a repair needs several trades coordinated by a general contractor, O&amp;P is often appropriate. Check whether it’s included and, if not, why.</p>
<h2>Compare with your contractor</h2>
<p>Put the two estimates side by side by room. Mark the lines that differ and the reason: missing item, different quantity or different price. That comparison is the foundation for a supplement request or an appraisal.</p>
<p>If the gap is large, our <a href="/free-claim-calculators/appraisal-payoff-calculator/">appraisal payoff calculator</a> shows whether appraisal is likely to be worth the cost.</p>
""",
    },
]
