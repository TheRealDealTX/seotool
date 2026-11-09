"""Resources: appraisal process guide, FAQ, glossary and insights posts.

Pure data module (standard library only). Content is general information,
not legal advice.
"""

PROCESS_INTRO = """<p>Appraisal is a dispute-resolution tool written into most North Carolina property policies. It exists for one narrow problem: you and your insurer agree there is a covered loss, but you cannot agree on what it costs to make it right. Instead of arguing indefinitely or heading to court, each side names an appraiser, the two appraisers pick a neutral umpire, and an award signed by any two of the three sets the amount of loss. The stages below describe how that usually unfolds, from the first disagreement to the check. Your policy form controls the details, so read its appraisal clause alongside this guide, and talk to a North Carolina attorney about any question of coverage, deadlines or legal rights.</p>"""

PROCESS_STEPS = [
    ("The disagreement takes shape", """<p>Appraisal starts after the carrier has inspected, written an estimate and paid or offered something. The question is no longer whether there was damage, but how much it costs to repair or replace. Before invoking anything, pin down where the gap actually is.</p>
<ul>
<li>Compare the carrier’s estimate with your contractor’s line by line.</li>
<li>List missing items, wrong quantities and pricing differences separately.</li>
<li>Ask in writing for a re-inspection or supplement review if obvious items were missed.</li>
</ul>
<p>Many disputes shrink at this point once both sides see the same list. If the remaining gap is still meaningful, you have a clear, documented amount-of-loss disagreement, which is exactly what appraisal is designed to resolve. A settlement gap estimate can help you size it before you decide.</p>"""),
    ("Reading the appraisal clause", """<p>Every policy words appraisal a little differently, so the clause itself is your rulebook. North Carolina’s standard fire policy provisions in Chapter 58 of the General Statutes include an appraisal framework, and most homeowners forms follow a similar pattern: two appraisers, an umpire, and an award agreed to by any two.</p>
<h3>What to look for</h3>
<ul>
<li>Who may demand appraisal and whether the demand must be written.</li>
<li>How many days each side has to name an appraiser (20 days is common).</li>
<li>How appraiser and umpire costs are split.</li>
<li>Any requirement to submit a sworn proof of loss first.</li>
<li>The policy’s suit-limitation period, which may keep running during appraisal.</li>
</ul>
<p>If anything is unclear, ask the carrier for a certified copy of the full policy.</p>"""),
    ("Sending the written demand", """<p>Either party can usually start appraisal with a written demand. Keep it short and factual. A typical demand identifies the policyholder, property address, policy and claim numbers and date of loss; states that the parties disagree on the amount of loss; invokes the appraisal provision; and names your appraiser or commits to naming one within the policy’s time frame.</p>
<p>Send it by a method you can prove, such as certified mail plus email to the adjuster, and keep copies of everything. Avoid arguing coverage in the demand. Appraisal is about the dollar value of damage, and mixing in legal arguments can invite objections or delay. If the carrier responds that a coverage question must be resolved first, that is a point to discuss with a North Carolina attorney.</p>"""),
    ("Both sides name appraisers", """<p>Each party selects its own appraiser, and most policies require that person to be <em>competent</em> and <em>disinterested</em>. In practice that means someone who understands construction costs and estimating software and who has no financial stake that would compromise independence.</p>
<p>Once retained, your appraiser typically:</p>
<ul>
<li>Reviews the policy, the carrier’s estimate, photos and correspondence.</li>
<li>Inspects the property, measures and documents damage.</li>
<li>Builds an independent, line-item estimate of the amount of loss.</li>
<li>Contacts the carrier’s appraiser to set an exchange schedule.</li>
</ul>
<p>Choose carefully. An appraiser whose independence is questioned can give the other side grounds to challenge the eventual award. Ask any candidate to disclose relationships and fee terms in writing.</p>"""),
    ("Selecting the umpire", """<p>The two appraisers choose a neutral umpire, ideally early, before any impasse forms. A good umpire has deep estimating experience, no ties to either side and the patience to work through detailed line items.</p>
<p>Appraisers usually exchange a short list of candidates, disclose any prior dealings and agree on one name in writing. If they cannot agree within the time the policy allows, many policy forms let either party ask a court of record in the county where the property is located to appoint an umpire. That step involves a court filing, so a North Carolina attorney should handle it.</p>
<p>The umpire generally stays in the background while the appraisers negotiate. Only the items they cannot resolve are submitted, which keeps the process focused and usually reduces the umpire’s fee.</p>"""),
    ("Inspection, exchange and negotiation", """<p>This is where most of the work happens. The appraisers inspect the property, sometimes together, and exchange their estimates. Then they go line by line through the differences.</p>
<h3>Typical sticking points</h3>
<ul>
<li>Roof square counts, waste factors, pitch and steep charges.</li>
<li>Whether damaged materials can be repaired or must be replaced.</li>
<li>Unit pricing for the local market at the time of loss.</li>
<li>Overhead and profit where multiple trades are involved.</li>
<li>Matching of adjoining materials that cannot be blended.</li>
</ul>
<p>Good documentation settles most of these questions: clear photos, measurements, manufacturer specifications and contractor quotes. The appraisers agree on whatever they can and narrow the rest to a short, well-defined list for the umpire.</p>"""),
    ("Umpire review and the award", """<p>If the appraisers resolve everything, they sign an award together and the umpire may never be needed. Otherwise, each appraiser presents the disputed items to the umpire with supporting evidence. The umpire may inspect the property, ask questions and request more documentation before deciding.</p>
<p>The award usually states the amount of loss, often split into replacement cost value and actual cash value, and sometimes broken out by coverage part such as dwelling, other structures or contents. Under the typical clause, an award signed by any two of the three becomes the amount of loss.</p>
<p>Read the award carefully before anyone treats it as final. Confirm that the categories line up with your policy, that the arithmetic is right and that it is limited to amount of loss rather than coverage decisions.</p>"""),
    ("Payment and closing out the claim", """<p>After the award, the carrier applies the policy terms: it subtracts your deductible and any prior payments, applies limits, and pays the balance. Coverage questions the award did not decide may still be open, and the insurer may reserve its rights on them.</p>
<ul>
<li>Track whether payment is for actual cash value now, with recoverable depreciation released after repairs.</li>
<li>Note any deadline for completing repairs to claim the holdback.</li>
<li>Keep invoices and photos of completed work.</li>
<li>Watch the suit-limitation period if any issue remains unresolved.</li>
</ul>
<p>Knowing how replacement cost, actual cash value and holdback interact helps you anticipate each payment. If payment stalls, the North Carolina Department of Insurance accepts consumer complaints.</p>"""),
]

PROCESS_OUTRO = """<h2>Mistakes that weaken an appraisal</h2>
<p>Most problems in appraisal come from preparation, not from the panel itself. The ones we see most often are avoidable:</p>
<ul>
<li><strong>Invoking too early.</strong> If the carrier has not finished its estimate, there may not yet be a real disagreement to appraise.</li>
<li><strong>Thin documentation.</strong> Without dated photos, measurements and receipts, the panel has to rely on whatever the carrier recorded.</li>
<li><strong>Missing deadlines.</strong> Appraiser selection windows and suit-limitation periods can run regardless of negotiations.</li>
<li><strong>Choosing an appraiser with a conflict.</strong> A relationship or fee arrangement that looks like a stake in the outcome can be used to attack the award.</li>
<li><strong>Letting mitigation slide.</strong> Damage that grows because the property was not protected may be excluded from the amount of loss.</li>
</ul>
<h2>What appraisal can’t do</h2>
<p>Appraisal sets the amount of loss. It generally does not decide whether a policy covers a cause of loss, whether an exclusion applies, whether the claim was handled in bad faith, or how a policy should be interpreted. Those questions belong to the insurer, the North Carolina Department of Insurance or the courts, and they call for a North Carolina attorney, not an appraiser. We are an appraisal firm, not a law firm or a public adjuster, so we keep our work on valuation and refer legal questions to counsel.</p>"""

FAQ = [
    ("Appraisal basics", [
        ("What is insurance appraisal?",
         "Appraisal is a process written into most property policies for settling disagreements about the amount of a loss. Each side names an appraiser, the two appraisers choose a neutral umpire, and an award signed by any two of the three sets the value. It is usually faster and less formal than a lawsuit, but it is limited to valuation rather than coverage."),
        ("When does appraisal make sense?",
         "Appraisal fits best when the insurer has accepted that a loss is covered but you disagree on the cost of repair or replacement. Common examples are roof square counts, pricing, repair-versus-replace decisions and overhead and profit. If the carrier has denied the claim outright on coverage grounds, appraisal may not resolve the core problem."),
        ("Who can demand appraisal?",
         "Under most policy forms, either the policyholder or the insurer may demand appraisal in writing once there is a disagreement on the amount of loss. Some policies add conditions, such as submitting a proof of loss first. Your own policy’s appraisal clause controls, so read it closely or ask the carrier for a certified copy."),
        ("Is the appraisal award binding?",
         "Under the typical clause, an award signed by any two of the three panel members sets the amount of loss. Awards can sometimes be challenged on limited grounds, such as fraud, a conflict of interest or the panel deciding questions outside its authority. Whether and how an award can be challenged is a legal question for a North Carolina attorney."),
        ("Is an appraiser the same as a public adjuster?",
         "No. A public adjuster is licensed to negotiate a claim on the policyholder’s behalf. An appraiser serves on an appraisal panel under the policy’s appraisal clause and works on the amount of loss. We are an appraisal firm only. We are not public adjusters and not attorneys."),
    ]),
    ("Costs & timing", [
        ("Who pays for appraisal?",
         "Most policies say each party pays its own appraiser and the two sides split the umpire’s fee and other shared costs equally. Some forms word this differently, so check your policy. Your appraiser’s fee is a cost to weigh against the size of the gap you are trying to close."),
        ("How long does appraisal take?",
         "Timing varies with the size of the loss, how quickly appraisers are named and whether an umpire is needed. Straightforward roof or water claims may move in weeks, while large or complex losses can take several months. Delays in naming appraisers or agreeing on an umpire are the most common reason the process drags."),
        ("How do appraisers charge?",
         "Fee structures vary. Some appraisers charge a flat fee or an hourly rate, while others work on a percentage of the award. Contingency arrangements for appraisers are debated because policies often require a disinterested appraiser, and some courts and policies scrutinize them. Ask any appraiser to explain their fee in writing before you sign."),
        ("Is appraisal worth it for a small gap?",
         "It depends on the numbers. If the difference between your estimate and the carrier’s is modest, appraisal costs could absorb much of any increase. Asking for a supplement or re-inspection may be the better first step. We are happy to review the estimates and tell you plainly whether appraisal looks proportionate."),
        ("Does appraisal stop the suit-limitation clock?",
         "Do not assume it does. Many property policies set a period for filing suit, often measured from the date of loss, and appraisal may not pause it. Check your policy for the exact language and talk to a North Carolina attorney well before any deadline if a dispute might end up in court."),
    ]),
    ("North Carolina specifics", [
        ("Does North Carolina law address appraisal?",
         "Yes, in general terms. The standard fire policy provisions in Chapter 58 of the North Carolina General Statutes include an appraisal framework with two appraisers, an umpire and an award by any two. Individual homeowners policies build on that structure, so your policy’s wording is still the place to start."),
        ("Who regulates insurers in North Carolina?",
         "The North Carolina Department of Insurance regulates insurance companies doing business in the state and accepts consumer complaints about claim handling. The North Carolina Rate Bureau files homeowners rates. A complaint to the Department is separate from appraisal and can run alongside it."),
        ("What if my insurer is slow or unresponsive?",
         "Keep a dated log of every call, email and letter, and put requests in writing. North Carolina addresses unfair claim settlement practices in N.C. Gen. Stat. § 58-63-15(11), and you can file a complaint with the Department of Insurance. For questions about legal remedies, consult a North Carolina attorney."),
        ("Do coastal pool and FAIR Plan policies have appraisal?",
         "Policies issued by the North Carolina Insurance Underwriting Association and the North Carolina Joint Underwriting Association generally contain claim dispute provisions, but the wording, deadlines and procedures depend on the specific form. Read your own policy carefully or ask the association for a copy before you rely on any timeline."),
        ("Do you work anywhere in the state?",
         "We work with properties across North Carolina’s 100 counties, from the Outer Banks and coastal counties through the Piedmont to the mountains. Many reviews start remotely with documents and photos, and on-site inspections are scheduled whenever the file requires them."),
    ]),
    ("Storm claims", [
        ("Can appraisal help after a hurricane?",
         "Appraisal can resolve disagreements about how much wind damage costs to repair once wind coverage is accepted. It usually cannot decide whether damage was caused by wind or by flood if that is a coverage question under your policy. Separating the two clearly in your documentation helps either way."),
        ("How do named-storm deductibles work?",
         "Many coastal policies carry a named-storm or hurricane deductible expressed as a percentage of the dwelling limit, rather than a flat dollar amount. That can make the deductible much larger than an all-other-perils deductible. Check your declarations page, and try our named-storm deductible calculator to see the effect."),
        ("What should I document after a storm?",
         "Photograph and video every elevation of the house, the roof if safely visible, interior ceilings and walls, and damaged contents before cleanup. Record water lines, fallen trees and debris. Keep receipts for tarps, fans and emergency repairs. Dated evidence gathered early is often the strongest support in appraisal."),
        ("Can I make repairs before appraisal?",
         "You generally must take reasonable steps to prevent further damage, such as tarping a roof or drying out water. Before permanent repairs, give the carrier a chance to inspect and document conditions thoroughly. Read your policy’s duties after loss section, and ask the adjuster in writing if you are unsure."),
        ("What about hail and roof damage?",
         "Hail disputes often turn on whether shingles are functionally damaged, whether repair is feasible and how many squares need replacement. Appraisers document hits with test squares, photos and measurements. Matching and discontinued shingles are frequent sticking points that the panel may be asked to value."),
    ]),
    ("After the award", [
        ("What happens once the award is signed?",
         "The award is sent to the insurer, which applies the policy terms, subtracts the deductible and prior payments, applies limits and issues payment. Some policies require payment within a set number of days after an award. Coverage questions not decided by the panel may still be open."),
        ("How do I recover depreciation after the award?",
         "If your policy pays actual cash value first, the withheld depreciation is often released after repairs are completed and documented. Keep contracts, invoices and completion photos, and note any deadline your policy sets for finishing repairs. Our RCV, ACV and holdback calculator shows how the numbers fit together."),
        ("What if the insurer won’t pay the award?",
         "Start by asking in writing for a payment date and an explanation for any delay. Document every exchange. You can file a complaint with the North Carolina Department of Insurance. Enforcement of an award or claims about the insurer’s conduct are legal matters, so consult a North Carolina attorney."),
        ("Can I reopen a claim after appraisal?",
         "If you discover hidden damage that was not part of the original estimate, many policies allow a supplemental claim, subject to reporting and suit-limitation provisions. The award generally covers only what was before the panel. Report newly found damage promptly and in writing."),
    ]),
]

GLOSSARY = [
    ("Actual cash value (ACV)", "The value of damaged property at the time of loss, usually replacement cost minus depreciation. Many policies pay ACV first and the rest after repairs."),
    ("Additional living expense (ALE)", "Coverage, often Coverage D, for reasonable extra costs of living elsewhere while a home is uninhabitable after a covered loss, such as rent, meals and mileage above normal."),
    ("Anti-concurrent causation", "Policy language stating that if an excluded cause, such as flood, combines with a covered cause, the loss may be excluded regardless of the sequence of events."),
    ("Appraisal clause", "The policy provision allowing either party to demand appraisal when they disagree on the amount of loss, using two appraisers and an umpire."),
    ("Award", "The written decision of an appraisal panel stating the amount of loss. Under the typical clause it is effective when signed by any two of the three panel members."),
    ("Code upgrade", "Work required by current building codes when damaged property is repaired, such as new underlayment or electrical updates, often covered under ordinance or law coverage."),
    ("Competent appraiser", "An appraiser with the construction, pricing and estimating knowledge needed to value the specific loss accurately, as most appraisal clauses require."),
    ("Contents inventory", "A room-by-room list of damaged or destroyed personal property, with descriptions, ages, quantities and replacement prices, used to support a Coverage C claim."),
    ("Coverage A (Dwelling)", "The part of a homeowners policy covering the house itself and attached structures, such as an attached garage or deck."),
    ("Coverage B (Other structures)", "Coverage for detached structures on the property, such as fences, sheds and detached garages, typically a percentage of the dwelling limit."),
    ("Coverage C (Personal property)", "Coverage for belongings such as furniture, clothing and electronics, subject to limits and special sub-limits for certain categories."),
    ("Coverage D (Loss of use)", "Coverage for additional living expense or fair rental value when a covered loss makes the home unfit to live in."),
    ("Debris removal", "Coverage for removing damaged property and certain storm debris, often included within limits or subject to a separate sub-limit such as for fallen trees."),
    ("Declarations page", "The summary page of a policy listing the insured, property, coverage limits, deductibles, endorsements and policy period."),
    ("Depreciation", "The reduction in value of property due to age, wear and condition, subtracted from replacement cost to arrive at actual cash value."),
    ("Disinterested appraiser", "An appraiser without a personal or financial stake that would compromise independence. What qualifies is judged by the policy wording and applicable law."),
    ("Holdback", "The portion of a claim payment, usually recoverable depreciation, that the insurer withholds until repairs or replacement are completed and documented."),
    ("Ice dam", "A ridge of ice at a roof edge that traps melting snow, allowing water to back up under shingles and leak into the home."),
    ("Line item", "A single entry in an estimate describing a task or material with a quantity, unit and price, such as removing and replacing a square of shingles."),
    ("Matching", "The question of whether undamaged materials must be replaced so repairs are reasonably uniform in appearance with adjoining areas, as policy wording allows."),
    ("Mitigation", "Reasonable steps a policyholder takes after a loss to prevent further damage, such as tarping a roof, shutting off water or drying wet materials."),
    ("Mold remediation", "The process of containing, removing and cleaning mold growth, often subject to policy exclusions or sub-limits depending on the cause and wording."),
    ("Named-storm deductible", "A deductible that applies to damage from a named tropical storm or hurricane, often a percentage of the dwelling limit rather than a flat amount."),
    ("NCIUA (Coastal Property Insurance Pool)", "The North Carolina Insurance Underwriting Association, which offers wind and other property coverage in beach and coastal areas of 18 eastern counties."),
    ("NCJUA (FAIR Plan)", "The North Carolina Joint Underwriting Association, the state’s FAIR Plan, which offers basic property coverage to owners unable to obtain it in the regular market."),
    ("NFIP", "The National Flood Insurance Program, a federal program that provides flood coverage, which standard homeowners policies typically exclude. It has its own claim rules and deadlines."),
    ("Ordinance or law coverage", "Coverage for added costs of complying with building codes or ordinances when repairing or rebuilding after a covered loss, usually limited to a percentage of the dwelling limit."),
    ("Overhead and profit (O&P)", "A general contractor’s charge for coordinating a job and earning a margin, often figured as a percentage added when several trades are involved."),
    ("Percentage deductible", "A deductible calculated as a percentage of the dwelling coverage limit rather than a fixed dollar amount, common for named-storm and wind or hail perils."),
    ("Pitch", "The steepness of a roof, expressed as rise over twelve inches of run. Steeper roofs often carry additional labor charges in estimates."),
    ("Proof of loss", "A formal statement from the policyholder of the amount claimed, often required by the policy within a set time after the insurer requests it."),
    ("Recoverable depreciation", "Depreciation withheld from an initial payment that can be recovered once repairs or replacement are completed, under replacement cost policies."),
    ("Replacement cost value (RCV)", "The cost to repair or replace damaged property with materials of like kind and quality at current prices, without deducting depreciation."),
    ("Reservation of rights", "A letter in which the insurer continues handling a claim while reserving the right to deny or limit coverage later based on stated reasons."),
    ("Scope of loss", "The full description of damaged areas and the repairs needed, before pricing. Many estimate disputes start with differences in scope rather than price."),
    ("Square (roofing)", "A unit of roof area equal to 100 square feet, used to measure and price shingles, underlayment and related roofing work."),
    ("Suit limitation", "A policy provision setting the time within which a lawsuit must be filed against the insurer. Check your policy and consult an attorney about how it applies."),
    ("Supplement", "A request to add items or costs to an existing estimate, often because hidden damage is found or the original scope missed necessary work."),
    ("Sworn statement", "A signed and notarized statement, such as a sworn proof of loss, that the policyholder attests is true under penalty of law."),
    ("Umpire", "The neutral third member of an appraisal panel, chosen by the two appraisers, who decides items they cannot agree on."),
    ("Umpire selection", "The process by which the two appraisers agree on an umpire. Many policies allow a court to appoint one if the appraisers cannot agree in time."),
    ("Wind/hail deductible", "A separate deductible that applies to wind or hail damage, which may be a flat amount or a percentage of the dwelling limit."),
    ("Xactimate", "Widely used estimating software with regional price lists that insurers, contractors and appraisers use to build line-item repair estimates."),
]

POSTS = [
    {
        "slug": "invoking-appraisal-north-carolina-policy",
        "title": "How to Invoke Appraisal Under a North Carolina Homeowners Policy",
        "seo": "How to Invoke Appraisal in North Carolina",
        "desc": "A step-by-step look at invoking appraisal under a NC homeowners policy: the written demand, naming an appraiser, typical timelines and mistakes.",
        "summary": "What a written appraisal demand should include, the timelines common in North Carolina policy forms, and the mistakes that slow the process down.",
        "read": "7 min",
        "date": "2026-09-15",
        "body": """<p>Most North Carolina homeowners policies contain an appraisal clause, but few people read it until a claim stalls. When the carrier’s estimate and your contractor’s number are far apart and the adjuster will not move, appraisal offers a structured way to settle the amount of loss without going straight to court. Invoking it well, though, takes more than a quick email. This guide walks through the steps we see work, the timelines that often appear in policy forms, and the mistakes that cost time.</p>
<h2>Confirm that you have an amount-of-loss dispute</h2>
<p>Appraisal is built for one kind of disagreement: how much it costs to repair or replace covered damage. If the insurer has accepted the claim and paid something, and you believe the estimate is too low, you likely have that kind of dispute. If the insurer has denied the claim entirely, or says a particular cause of loss is excluded, the disagreement is about coverage, and appraisal may not resolve it. Coverage questions belong with a North Carolina attorney.</p>
<p>Before invoking, make sure the carrier has actually finished its estimate. Demanding appraisal while the adjuster is still reviewing a supplement can look premature and invite an objection.</p>
<h2>Read your appraisal clause line by line</h2>
<p>The standard fire policy provisions in Chapter 58 of the North Carolina General Statutes include an appraisal framework, and most homeowners forms track it: each side picks an appraiser, the appraisers choose an umpire, and an award signed by any two sets the amount of loss. Within that framework, policy forms vary. Look for:</p>
<ul>
<li><strong>Who may demand.</strong> Usually either party, in writing.</li>
<li><strong>Time to name an appraiser.</strong> Many forms give each side 20 days after the demand.</li>
<li><strong>Umpire selection.</strong> Often a set period for the appraisers to agree, with a court in the county where the property sits able to appoint one if they cannot.</li>
<li><strong>Costs.</strong> Typically each party pays its own appraiser and splits the umpire.</li>
<li><strong>Conditions.</strong> Some policies expect a sworn proof of loss or other duties to be met first.</li>
</ul>
<p>If you do not have the complete policy, ask the carrier in writing for a certified copy, including endorsements. Endorsements can change deductibles and loss settlement terms that matter to the valuation.</p>
<h2>Write a clear, short demand</h2>
<p>A demand letter does not need to be long. It needs to be unmistakable. We suggest including:</p>
<ol>
<li>Your name, the property address, policy number, claim number and date of loss.</li>
<li>A plain statement that you and the insurer disagree on the amount of loss.</li>
<li>A statement that you are invoking the policy’s appraisal provision.</li>
<li>The name and contact information of your appraiser, or a commitment to name one within the policy’s time frame.</li>
<li>A request that the insurer name its appraiser within the period the policy allows.</li>
</ol>
<p>Keep it factual. Do not argue coverage, accuse the adjuster of bad faith or attach a lengthy narrative. Those arguments do not help the panel and can give the other side a reason to resist appraisal.</p>
<h2>Send it so you can prove it</h2>
<p>Use a delivery method that creates a record. Certified mail with return receipt, combined with email to the adjuster and any claims mailbox listed in your correspondence, is common. Save the delivery confirmation and calendar the dates that follow from it: the deadline for each side to name an appraiser and, later, the window for agreeing on an umpire. Our <a href="/calculators/claim-timeline-planner/">claim timeline planner</a> can help you map those dates.</p>
<h2>Assemble the file your appraiser will need</h2>
<p>An appraiser can only be as effective as the documentation behind the claim. Before or right after the demand, gather:</p>
<ul>
<li>The full policy and declarations page.</li>
<li>Every estimate from the carrier, including revisions.</li>
<li>Your contractor’s estimate and any supporting quotes.</li>
<li>Dated photos and video from before and after cleanup.</li>
<li>Receipts for emergency repairs, tarps, drying equipment and hotel stays.</li>
<li>All letters and emails with the insurer.</li>
</ul>
<p>Our <a href="/calculators/appraisal-preparedness-checkup/">appraisal preparedness checkup</a> walks through this list and flags gaps.</p>
<h2>Mistakes that slow things down</h2>
<h3>Missing the appraiser deadline</h3>
<p>If your policy gives 20 days to name an appraiser and you take 45, you hand the other side an argument. Line up your appraiser before you send the demand when you can.</p>
<h3>Choosing someone with a stake in the outcome</h3>
<p>Most policies call for a disinterested appraiser. Your roofing contractor, a relative or anyone whose pay depends heavily on the result may draw an objection that delays the process or threatens the award.</p>
<h3>Forgetting the suit-limitation clock</h3>
<p>Many property policies set a period for filing suit, often measured from the date of loss. Do not assume appraisal pauses it. Check your policy and speak with a North Carolina attorney well before any deadline if court is a possibility.</p>
<h3>Stopping mitigation</h3>
<p>Invoking appraisal does not suspend your duty to protect the property from further damage. Keep the roof tarped and the moisture under control, and keep receipts.</p>
<h2>What comes next</h2>
<p>Once both appraisers are named, they inspect, exchange estimates and work through differences line by line, bringing in the umpire only for what they cannot settle. Our <a href="/appraisal-process-guide/">appraisal process guide</a> covers those stages in detail. If you would like us to look at your estimates before you decide whether to invoke, we are glad to review the file and give you a straight answer about whether appraisal looks proportionate to the gap.</p>""",
    },
    {
        "slug": "wind-vs-flood-hurricane-claims-nc",
        "title": "Wind vs. Flood: Sorting Hurricane Damage on North Carolina Claims",
        "seo": "Wind vs. Flood Damage on NC Hurricane Claims",
        "desc": "How wind and flood damage get separated after storms like Florence and Helene, how homeowners and NFIP policies split, and where appraisal fits.",
        "summary": "After a hurricane, the line between wind and water decides which policy pays. Here is how that line gets drawn, documented and, sometimes, appraised.",
        "read": "8 min",
        "date": "2026-09-29",
        "body": """<p>North Carolina has a long memory for hurricanes: Hazel in 1954, Hugo in 1989, Fran in 1996, Floyd in 1999, and more recently Matthew in 2016, Florence in 2018 and Helene in 2024. Each storm brought a different mix of wind and water. Florence stalled and dumped extraordinary rain across the coastal plain. Helene tore through the mountains with flooding and landslides far from any coastline. In both cases, many homeowners discovered that the question of whether damage came from wind or flood decided which policy, if any, would pay.</p>
<h2>Why the distinction matters so much</h2>
<p>A standard homeowners policy typically covers windstorm damage, subject to any wind or named-storm deductible, but excludes flood. Flood coverage usually comes from a separate policy, most often through the National Flood Insurance Program, with its own limits, deductibles, claim procedures and deadlines. Some homes have both policies; many inland homes affected by Helene had neither flood policy nor any reason to expect they would need one.</p>
<p>When a single house shows a torn roof, wet ceilings, a waterline on the walls and a ruined crawlspace, each piece of damage has to be attributed to a cause. The answer determines whether the homeowners carrier, the flood insurer or neither is responsible for each line of the repair.</p>
<h2>Anti-concurrent causation in general terms</h2>
<p>Many homeowners policies include what is often called anti-concurrent causation language. In general terms, it says that if an excluded cause, such as flood, contributes to a loss together with a covered cause, the loss may be excluded regardless of which happened first. How that language applies to a particular set of facts is a legal and coverage question, and courts have not always treated it the same way. We do not interpret policies; if anti-concurrent language is part of your dispute, a North Carolina attorney should review it.</p>
<p>What we can say is that clear evidence about which damage came from which force makes every one of those conversations easier, and it is the foundation of any later valuation.</p>
<h2>Reading the house for evidence</h2>
<p>Wind and water leave different signatures. Experienced estimators look for patterns such as:</p>
<ul>
<li><strong>Wind indicators.</strong> Missing or creased shingles, lifted flashing, damaged ridge caps, displaced siding, broken windows from debris, and interior water staining that starts at the ceiling and spreads downward.</li>
<li><strong>Flood indicators.</strong> A consistent horizontal waterline on walls, silt and mud deposits, saturated insulation from the bottom up, buckled floors and damage concentrated at lower levels.</li>
<li><strong>Mixed areas.</strong> Rooms with both ceiling stains and floor-level water need careful separation, often wall by wall and material by material.</li>
</ul>
<p>Our <a href="/calculators/wind-flood-damage-splitter/">wind and flood damage splitter</a> lets you organize line items by likely cause before you talk to either carrier.</p>
<h2>Documentation that holds up</h2>
<p>The most useful evidence is gathered before cleanup starts, which is hard when you are worried about mold and your family needs a place to stay. Even so, a few minutes of documentation can matter for the life of the claim:</p>
<ol>
<li>Photograph the waterline in every affected room, with a tape measure showing its height.</li>
<li>Capture the roof and exterior from every side, including any fallen trees or debris.</li>
<li>Photograph ceilings and upper walls separately from floors and lower walls.</li>
<li>Keep samples or photos of removed drywall, flooring and insulation before disposal.</li>
<li>Save receipts for tarps, pumps, fans, dehumidifiers and remediation services.</li>
<li>Write down what you observed during the storm, such as when leaks started and when water entered.</li>
</ol>
<p>Report the claim to each potentially responsible insurer promptly. Flood and homeowners policies have separate notice and proof-of-loss requirements, and NFIP proof-of-loss timing in particular is strict, so read each policy and follow its instructions closely.</p>
<h2>Where appraisal fits, and where it doesn’t</h2>
<p>Appraisal is built to resolve disagreements about the amount of loss. Suppose your homeowners carrier accepts that wind tore off part of the roof and let rain into the upstairs bedrooms, but its estimate for that work seems far too low. That is a classic appraisal dispute: square counts, pitch charges, underlayment, interior drywall, paint and the cost of matching materials.</p>
<p>Appraisal is a weaker fit when the core disagreement is whether a cause of loss is covered at all, for example when the carrier says the entire loss was flood and excluded. Some policies and courts allow appraisers to allocate damage between causes as part of measuring the loss; others treat causation as a coverage question beyond the panel’s authority. That boundary depends on your policy wording and the law, so get legal advice before assuming appraisal can resolve a causation dispute.</p>
<p>NFIP flood policies have their own appraisal provisions and dispute procedures that differ from homeowners policies. Review the flood policy’s language separately and follow its timelines.</p>
<h2>Deductibles add another layer</h2>
<p>Coastal homeowners policies often carry named-storm or hurricane deductibles expressed as a percentage of the dwelling limit. Illustrative example: on a dwelling limit of $300,000, a 2 percent named-storm deductible would be $6,000, while a 5 percent deductible would be $15,000. That can make a modest wind claim fall below the deductible entirely. Our <a href="/calculators/named-storm-deductible-calculator/">named-storm deductible calculator</a> shows how your own percentage plays out.</p>
<h2>How we approach storm files</h2>
<p>On hurricane claims, we focus on building a clear, line-item record of the damage and its likely source so that each carrier’s responsibility is visible. When the dispute is about value, we can serve as your appraiser on the panel. When it is about coverage, we will tell you so and suggest you speak with a North Carolina attorney. Our <a href="/claim-appraisal/hurricane-tropical-storm-claims/">hurricane and tropical storm claims</a> page explains that work in more detail.</p>""",
    },
    {
        "slug": "ice-storm-claims-north-carolina",
        "title": "Ice Storm and Hard Freeze Claims in North Carolina: What to Expect",
        "seo": "Ice Storm and Freeze Claims in North Carolina",
        "desc": "Ice storms and hard freezes bring falling limbs, burst pipes and ice dams. How NC homeowners can document these claims and handle value disputes.",
        "summary": "Falling limbs, burst pipes and ice dams each raise different claim questions. How to protect the property, document the loss and handle estimate disputes.",
        "read": "7 min",
        "date": "2026-10-08",
        "body": """<p>Winter weather in North Carolina tends to arrive as ice rather than deep snow, and ice is hard on houses. The December 2002 ice storm coated the Piedmont, brought down trees and power lines across a wide area and left many households without power for days. The January 2000 snowstorm buried the Triangle. More recently, the Christmas 2022 cold snap sent temperatures plunging and burst pipes in homes that rarely see a sustained hard freeze. These events produce a familiar set of claims, and each comes with its own valuation questions.</p>
<h2>Tree limbs on roofs</h2>
<p>Ice loading can bring down limbs and whole trees onto roofs, porches, fences and vehicles. On the house itself, the typical claim includes roof decking and framing repair, shingles, gutters, interior ceiling damage from leaks, and tree removal from the structure.</p>
<p>Disputes tend to center on:</p>
<ul>
<li>Whether rafters or trusses were damaged and need engineered repair.</li>
<li>How much of the roof surface must be replaced, versus a localized patch.</li>
<li>Whether replacement shingles can reasonably match the rest of the roof.</li>
<li>Interior work such as drywall, insulation and paint after water intrusion.</li>
</ul>
<h3>Debris removal limits</h3>
<p>Many homeowners policies treat tree removal and debris removal with care. Removing a tree that struck a covered structure is commonly covered, while removing a tree that fell in the yard without hitting anything may be limited or excluded. Policies often set a separate sub-limit for tree debris, sometimes per tree and per occurrence. Check the debris removal and trees, shrubs and plants sections of your policy before assuming a full removal invoice will be paid.</p>
<h2>Burst pipes and frozen plumbing</h2>
<p>When temperatures stay well below freezing, pipes in crawlspaces, exterior walls and unheated attics can freeze and split. The real damage often appears when the pipe thaws and water runs until someone finds it.</p>
<p>Policies commonly cover sudden and accidental water discharge, but many also contain freezing-related conditions. A frequent example requires the policyholder to have used reasonable care to maintain heat in the building, or to have shut off the water and drained the system, particularly if the home was vacant or unoccupied. Read that condition closely, because it is often where coverage disputes begin. Questions about whether the condition was met are coverage questions for a North Carolina attorney, not an appraisal panel.</p>
<p>When coverage is accepted, the amount-of-loss questions are familiar: how far water traveled, which materials can be dried and which must be replaced, flooring continuity across rooms, cabinet replacement and whether mold remediation is needed.</p>
<h2>Ice dams</h2>
<p>Ice dams form when heat escaping through the roof melts snow, and the water refreezes at the colder eaves. Water then backs up under shingles and into walls and ceilings. Interior damage from ice dams is commonly covered, but the cost of removing ice from the roof and fixing attic ventilation or insulation issues may be treated differently. Document interior staining carefully and photograph the ice formation at the eaves before it melts.</p>
<h2>Mitigation duties come first</h2>
<p>After any winter loss, most policies require reasonable steps to prevent further damage. In practical terms:</p>
<ol>
<li>Shut off the main water supply as soon as you discover a leak.</li>
<li>Tarp roof openings once it is safe to do so.</li>
<li>Remove standing water and start drying with fans and dehumidifiers.</li>
<li>Move undamaged belongings out of harm’s way.</li>
<li>Keep receipts for every mitigation expense and photograph the work.</li>
</ol>
<p>Damage that worsens because mitigation was delayed may be excluded from the amount of loss. If you cannot reach a contractor quickly during a widespread freeze, write down your efforts and when they happened.</p>
<h2>Documenting a winter loss</h2>
<p>Winter claims are often reported in waves, with adjusters stretched thin. Strong documentation helps your claim stand on its own:</p>
<ul>
<li>Photos of the fallen tree or limb in place before removal, including where it struck.</li>
<li>Photos of the split pipe section, and keep the pipe if you can.</li>
<li>Moisture readings from your mitigation contractor, with dates.</li>
<li>Thermostat settings and any utility outage records.</li>
<li>Invoices for tree removal, drying and emergency plumbing.</li>
</ul>
<h2>When estimates fall short</h2>
<p>Winter claims sometimes come back with estimates that cover the visible damage but miss what is behind it: wet insulation in walls, subfloor swelling, cabinets that delaminate weeks later, or ceiling framing hit by a limb. A supplement request supported by photos and moisture readings often resolves this. When it does not, and the dispute is about value rather than coverage, appraisal can be the next step.</p>
<p>Illustrative example: if the carrier’s estimate for a burst-pipe loss covers drying and drywall in one room, but water also reached the hallway and the flooring runs continuously through both spaces, the difference in scope can be significant. That is a valuation dispute an appraisal panel is designed to resolve. Our <a href="/calculators/settlement-gap-estimator/">settlement gap estimator</a> can help you size the difference first.</p>
<h2>How we help</h2>
<p>For ice and freeze losses, we review the carrier’s estimate against the damage, identify missed scope and pricing gaps, and, when appraisal is invoked, serve as your appraiser. Learn more on our <a href="/claim-appraisal/ice-storm-freeze-damage/">ice storm and freeze damage</a> page, or <a href="/contact-us/">contact us</a> to talk through your file.</p>""",
    },
    {
        "slug": "coastal-pool-fair-plan-claims",
        "title": "Claims with the NC Coastal Pool and FAIR Plan: A Practical Guide",
        "seo": "NC Coastal Pool and FAIR Plan Claims Guide",
        "desc": "An overview of claims with the NC Insurance Underwriting Association and FAIR Plan, and why your own policy form controls appraisal and deadlines.",
        "summary": "Many coastal and hard-to-insure properties carry policies from the state’s residual market associations. What that means when a claim turns into a dispute.",
        "read": "7 min",
        "date": "2026-10-16",
        "body": """<p>Not every North Carolina property is insured by a traditional private carrier. Many homes along the coast, and some properties elsewhere that are hard to place in the regular market, are insured through one of two residual market associations: the North Carolina Insurance Underwriting Association, which operates the Coastal Property Insurance Pool, and the North Carolina Joint Underwriting Association, which operates the state’s FAIR Plan. Claims under these policies follow many of the same principles as other property claims, but the specific forms, procedures and deadlines deserve close attention.</p>
<h2>What the two associations are</h2>
<h3>NCIUA and the Coastal Property Insurance Pool</h3>
<p>The North Carolina Insurance Underwriting Association was created to make property coverage available in the beach and coastal areas of 18 eastern counties, where wind and hurricane exposure can make private coverage hard to find. Depending on the property and the policy, coverage may be written for wind and hail only, with other perils insured elsewhere, or on a broader basis. Many homeowners in coastal areas carry a private homeowners policy that excludes wind, paired with a wind policy from the association.</p>
<h3>NCJUA and the FAIR Plan</h3>
<p>The North Carolina Joint Underwriting Association administers the FAIR Plan, which offers basic property coverage to owners who cannot obtain it in the voluntary market. FAIR Plan policies are often narrower than a full homeowners policy, and the forms and endorsements available vary by property type.</p>
<p>These descriptions are general. Eligibility rules, territories, coverage options and procedures can change, so the association’s current information and your own policy documents are the authority, not this article.</p>
<h2>Why two policies can mean two claims</h2>
<p>If your coastal home has a private homeowners policy that excludes wind and a separate wind policy from the association, a hurricane can produce two claims: one under the wind policy and possibly another under the homeowners or flood policy for other damage. Each claim has its own deductible, adjuster, estimate and timelines. Damage has to be attributed carefully, much as it is between wind and flood. Our <a href="/calculators/wind-flood-damage-splitter/">wind and flood damage splitter</a> can help you organize line items by policy.</p>
<h2>Deductibles on coastal policies</h2>
<p>Coastal wind policies often carry named-storm or hurricane deductibles expressed as a percentage of the dwelling limit. That deductible can be several times larger than a flat all-other-perils deductible. Illustrative example: a 3 percent deductible on a $250,000 dwelling limit would be $7,500 before any payment. Check your declarations page for the exact percentage and the event that triggers it, and use our <a href="/calculators/named-storm-deductible-calculator/">named-storm deductible calculator</a> to see the effect.</p>
<h2>Read your own policy form for dispute language</h2>
<p>This is the most important point in this guide. Policies issued by the associations generally contain claim dispute provisions, and many include appraisal language, but the exact wording, conditions and deadlines depend on the specific form and edition you hold. Before relying on any timeline, check:</p>
<ul>
<li>Whether the policy contains an appraisal clause and how it is triggered.</li>
<li>How many days each side has to name an appraiser.</li>
<li>How the umpire is chosen and what happens if the appraisers cannot agree.</li>
<li>How appraisal and umpire costs are divided.</li>
<li>Any proof-of-loss requirement and its due date.</li>
<li>The period the policy allows for filing suit, and when it starts.</li>
</ul>
<p>If you do not have the full policy, request a complete copy, including endorsements, from the association or your agent. Do not assume the language matches your previous policy or a neighbor’s.</p>
<h2>Practical steps after a coastal loss</h2>
<ol>
<li>Report the claim promptly to every insurer that may be responsible.</li>
<li>Photograph all elevations, the roof, interior damage and any waterlines before cleanup.</li>
<li>Protect the property from further damage and keep every receipt.</li>
<li>Keep a log of calls, inspections and correspondence with dates and names.</li>
<li>Get a detailed, line-item estimate from a qualified contractor.</li>
<li>Compare that estimate with the adjuster’s, line by line.</li>
</ol>
<h2>When the estimate seems too low</h2>
<p>Coastal claims often involve exposure-specific costs that a generic estimate may underweight: wind-rated shingles and fasteners, elevated structures with difficult access, corrosion-resistant hardware, stairs and decks exposed to surge, and building code requirements in coastal jurisdictions. If the adjuster’s estimate leaves these out, start with a written supplement request supported by photos and contractor pricing.</p>
<p>If the gap remains and your policy provides for appraisal, the process generally works as it does for other property policies: each side names an appraiser, the appraisers select an umpire, and an award signed by two sets the amount of loss. Appraisal resolves amount of loss, not coverage. If the association has denied coverage for part of the claim, or questions arise about the policy terms, a North Carolina attorney is the right resource.</p>
<h2>Complaints and help</h2>
<p>The North Carolina Department of Insurance accepts consumer complaints and can be a useful resource if communication breaks down. A complaint is separate from appraisal and can proceed alongside it.</p>
<h2>How we can help</h2>
<p>We review coastal pool and FAIR Plan estimates against the documented damage, flag missing scope and pricing gaps, and, when appraisal is invoked under the policy, serve as your appraiser. Start with our <a href="/claim-appraisal/carrier-estimate-audit/">carrier estimate audit</a> if you want a second look before deciding on next steps.</p>""",
    },
    {
        "slug": "matching-disputes-roof-siding",
        "title": "Matching Disputes on Roofs, Siding and Flooring: How They Get Valued",
        "seo": "Matching Disputes: Roofs, Siding and Flooring",
        "desc": "Why matching disputes arise on roofs, siding and floors, how discontinued shingles complicate claims, and how appraisers document a uniform look.",
        "summary": "When replacement materials cannot match what is left, the dispute is often over how far repairs must extend. How matching is documented and where coverage limits apply.",
        "read": "7 min",
        "date": "2026-10-22",
        "body": """<p>Few claim disagreements are as visible as a matching dispute. A hailstorm damages one slope of a roof, a fallen limb tears a section of vinyl siding, or a burst pipe ruins flooring in one room of an open floor plan. The carrier offers to replace only the damaged pieces. The homeowner points out that the new materials will not match what remains, leaving the house looking patched. Who is right depends partly on the policy and partly on the facts, and it helps to separate those two questions early.</p>
<h2>Coverage questions versus amount-of-loss questions</h2>
<p>Matching disputes often mix two different issues:</p>
<ul>
<li><strong>A coverage question:</strong> does the policy require the insurer to pay for replacing undamaged materials to achieve a reasonably uniform appearance? The answer depends on the policy wording, any matching endorsement or limitation, and North Carolina law. That is a question for the insurer and, if disputed, a North Carolina attorney.</li>
<li><strong>An amount-of-loss question:</strong> given the policy terms, what does it actually cost to repair the damage properly? Can a match be found? How far must repairs extend to reach a natural break? What does that work cost?</li>
</ul>
<p>Appraisal panels deal with the second category. Some policies and courts allow appraisers to address the extent of repair needed to restore the property, including matching; others treat matching as a coverage issue for the courts. Your policy wording matters, so read it and get legal advice if coverage is contested.</p>
<h2>Roofs and discontinued shingles</h2>
<p>Roofing is where matching comes up most. Shingle lines are reformulated and discontinued over time, colors change with production runs, and even the same product weathers differently after years of sun. A small repair with new shingles can stand out sharply against an older roof.</p>
<p>Disputes typically turn on:</p>
<ul>
<li>Whether the existing shingle is still manufactured in the same size, profile and color.</li>
<li>Whether a different product can blend acceptably with the existing roof.</li>
<li>Whether repair is feasible without damaging surrounding shingles, especially on brittle older roofs.</li>
<li>Whether a full slope, or the whole roof, must be replaced to achieve a reasonable match.</li>
</ul>
<h3>How appraisers document a roof match</h3>
<p>We document shingle identification carefully: measuring exposure and dimensions, noting markings on the back of a removed shingle when one is available, photographing color and granule pattern in good light, and checking manufacturer and supplier information on whether the product is still made. Where a repair test is appropriate, a brittleness or lift test can show whether shingles crack when handled. Our <a href="/claim-appraisal/roof-hail-loss-appraisal/">roof and hail loss appraisal</a> page explains more.</p>
<h2>Siding</h2>
<p>Vinyl, fiber cement and wood siding all fade and weather. Profiles change, and a manufacturer may no longer make the exact pattern, reveal or color. When only a portion of a wall is damaged, the question is how far replacement must run to avoid an obvious mismatch. Natural breaks such as inside and outside corners, windows and doors often define a reasonable repair boundary.</p>
<p>Appraisers document the existing profile, measure the reveal, photograph faded and protected areas side by side, and gather supplier confirmation about availability. Clear photos of the damaged wall alongside the adjoining elevations help a panel judge whether a repair will stand out.</p>
<h2>Flooring</h2>
<p>Hardwood, laminate, luxury vinyl plank and tile frequently run continuously from room to room without thresholds. Replacing flooring in one room can leave a visible line where new meets old, or may be physically impossible if the product is discontinued and planks lock together. Appraisers note where the flooring is continuous, where natural breaks such as doorways with transitions exist, and whether matching material is available.</p>
<p>Illustrative example: if water damages flooring in a kitchen that flows without a transition into a dining room and hallway, an estimate that replaces only the kitchen may not reflect a workable repair. Documenting the continuous run and product availability gives the panel a basis to value the realistic scope.</p>
<h2>Building a matching file</h2>
<p>Whether you are negotiating with the adjuster or heading into appraisal, a strong matching file includes:</p>
<ol>
<li>Photos of the damaged area and the adjoining undamaged areas, taken in consistent light.</li>
<li>Product identification: brand, line, color, size and profile if known.</li>
<li>Written confirmation from suppliers or manufacturers on availability.</li>
<li>Contractor opinion on repair feasibility and the natural break points.</li>
<li>A copy of the policy language on loss settlement and any matching endorsement.</li>
</ol>
<h2>Where matching fits in the estimate</h2>
<p>On the estimate, matching shows up as additional line items: removing and replacing undamaged sections, extra squares of roofing, more siding or flooring, plus related labor such as trim, underlayment or baseboards. Because these items can be large, they often account for a big share of the gap between estimates. Our <a href="/calculators/settlement-gap-estimator/">settlement gap estimator</a> can help you see how much of your dispute turns on matching.</p>
<h2>How we approach matching</h2>
<p>We keep our analysis on the facts and costs: what the damaged material is, whether it can be matched, and what a realistic repair costs. When a carrier says its policy does not pay for matching at all, we will tell you that is a coverage issue and suggest you consult a North Carolina attorney. When the dispute is about how far repairs must go and what they cost, that is squarely the kind of work an appraisal panel does, and we can serve as your appraiser. See our <a href="/insurance-terms/">insurance terms</a> page for related definitions.</p>""",
    },
    {
        "slug": "choosing-an-independent-appraiser",
        "title": "Choosing an Independent Appraiser: Questions to Ask and Red Flags",
        "seo": "Choosing an Independent Insurance Appraiser",
        "desc": "What competent and disinterested mean in practice, how appraisers charge, the questions to ask before hiring one, and the red flags worth noticing.",
        "summary": "The appraiser you pick shapes the panel and the award. What competent and disinterested mean, how fees work, and what to ask before you sign anything.",
        "read": "7 min",
        "date": "2026-11-02",
        "body": """<p>When you invoke appraisal, the person you name as your appraiser becomes one of three people who will decide the amount of your loss. That choice matters more than many homeowners realize. A capable appraiser can document a claim thoroughly, negotiate efficiently with the other side and present disputed items to the umpire clearly. A poor choice can lead to delays, a weak record or even a challenge to the award. Here is how to think about the decision.</p>
<h2>What “competent and disinterested” means in practice</h2>
<p>Most appraisal clauses, including those modeled on North Carolina’s standard fire policy provisions, require each appraiser to be competent and disinterested. Policies rarely define those words, so it helps to think about them practically.</p>
<h3>Competent</h3>
<p>A competent appraiser understands how buildings are constructed and repaired, and how repair costs are estimated. In practice, look for:</p>
<ul>
<li>Fluency with line-item estimating, including Xactimate or similar software.</li>
<li>Knowledge of local pricing and building code requirements.</li>
<li>Experience with the type of loss involved, such as roofing, water, fire or storm.</li>
<li>The ability to explain an estimate clearly to another appraiser and an umpire.</li>
</ul>
<h3>Disinterested</h3>
<p>Disinterested generally means the appraiser has no personal or financial stake that would compromise independent judgment. An appraiser can advocate for a well-supported number, but should not be so tied to the outcome that independence is in doubt. Situations that commonly raise questions include a family relationship with the policyholder, an ownership interest in the property, or being the contractor who will perform and profit from the repairs. How a court would view a specific relationship depends on the policy and North Carolina law, so if the issue comes up, ask a North Carolina attorney.</p>
<h2>How appraisers charge</h2>
<p>Fee arrangements vary, and it is worth understanding them before you sign.</p>
<ul>
<li><strong>Flat fee.</strong> A fixed price for the engagement, sometimes tied to the size or complexity of the loss. Predictable, though it may be adjusted if the scope changes significantly.</li>
<li><strong>Hourly.</strong> You pay for time spent on inspection, estimating, negotiation and umpire hearings. Transparent, but the total depends on how the process unfolds.</li>
<li><strong>Contingency.</strong> The fee is a percentage of the award or of the increase over the carrier’s estimate.</li>
</ul>
<p>Contingency fees for appraisers are a debated topic. Some argue they align the appraiser with the policyholder and make appraisal accessible to homeowners who cannot pay upfront. Others argue that a stake in the size of the award is in tension with the disinterested requirement, and some courts and some policy forms scrutinize or restrict those arrangements. We do not take a position for you here; read your policy, ask any appraiser how their fee arrangement is likely to be viewed under it, and get legal advice if you are unsure.</p>
<p>Remember also that under most policies you pay your own appraiser and split the umpire’s fee. Illustrative example: if an umpire charges $3,000 for a file, each side would typically pay $1,500 of that, on top of its own appraiser’s fee.</p>
<h2>Questions to ask before hiring</h2>
<ol>
<li>What types and sizes of property claims do you typically handle?</li>
<li>How will you document the damage, and will you inspect in person?</li>
<li>What estimating tools and price data do you use?</li>
<li>Do you have any relationship with me, my contractor, the carrier or its appraiser?</li>
<li>How do you charge, and what costs could be added later?</li>
<li>How will you handle umpire selection if the other appraiser proposes someone?</li>
<li>How often will you update me, and in what form?</li>
<li>Will you put the engagement terms in writing?</li>
</ol>
<p>Clear, specific answers are a good sign. Vague answers, or reluctance to put terms in writing, are not.</p>
<h2>Red flags</h2>
<ul>
<li><strong>Guaranteed results.</strong> No honest appraiser can promise a particular award. The umpire and the other appraiser have a say.</li>
<li><strong>Legal advice.</strong> An appraiser who tells you how a coverage exclusion will be interpreted or whether you have a bad-faith claim is outside the appraisal role. That is attorney territory.</li>
<li><strong>Pressure to sign immediately.</strong> Especially after a major storm, take the time to read an engagement agreement.</li>
<li><strong>Undisclosed relationships.</strong> Ties to your contractor or to other parties should be disclosed up front.</li>
<li><strong>Taking over the claim.</strong> An appraiser’s role is the appraisal panel. Negotiating the broader claim on your behalf is the work of a licensed public adjuster or an attorney.</li>
<li><strong>No written estimate.</strong> Your appraiser should produce a detailed, line-item valuation, not just a number.</li>
</ul>
<h2>Thinking about the umpire, too</h2>
<p>Your appraiser will help pick the umpire, so ask how they approach that step. A good umpire is experienced, impartial and willing to dig into details. Candidates should disclose prior dealings with either appraiser or carrier. If you want to understand that role in more depth, see our <a href="/claim-appraisal/neutral-umpire-services/">neutral umpire services</a> page.</p>
<h2>How we work</h2>
<p>We are an independent appraisal firm. We serve as a party’s appraiser under the policy’s appraisal clause, review carrier estimates, and serve as neutral umpires. We are not a law firm and not public adjusters, so we stay focused on valuation and refer legal questions to counsel. If you are considering appraisal, our <a href="/common-questions/">common questions</a> page covers the basics, and you can <a href="/contact-us/">contact us</a> to discuss your file and our fee terms before you decide anything.</p>""",
    },
]
