"""Learning content for southcarolinainsuranceappraiser.com.

Process guide (intro, steps, closing section), FAQ groups, glossary and guide posts.
Plain data only; HTML bodies are triple-quoted strings.
"""

# --------------------------------------------------------------------------- process guide

PROCESS_INTRO = """
<p>The insurance appraisal process in South Carolina is a private, policy-based way to settle one narrow question: how much a covered loss is worth. Nearly every homeowners, condo, commercial and wind-only policy sold here contains an appraisal paragraph. It lets either you or the insurer hand a pricing dispute to a small panel — one appraiser for each side and a neutral umpire — instead of trading estimates indefinitely or heading straight to court.</p>
<p>The steps below follow the order most South Carolina policies use, from the first sign of a gap between estimates to the day the check arrives. Your own policy’s wording controls the details, so keep a copy of the full policy and declarations page next to you as you read. Deadlines, notice rules and who pays the umpire can all differ from one carrier to the next.</p>
"""

PROCESS_STEPS = [
    ("Spot the gap and try a supplement", """
<p>Appraisal starts after the insurer has accepted at least part of the claim and issued an estimate you believe is too low. Before anyone demands anything, compare that estimate line by line with your contractor’s number. Look for missing rooms, roof squares counted short, absent code items, no overhead and profit, or tree removal left out entirely.</p>
<p>Send the adjuster a written supplement request that lists each missing or underpriced item and attaches photos, invoices and measurements. Many South Carolina claims close at this stage once the carrier sees the documentation. If the response is a flat no, or a revised number that still leaves a real gap, you have a genuine disagreement over the amount of loss.</p>
"""),
    ("Send a written appraisal demand", """
<p>Either side may invoke appraisal, and the demand should always be in writing. A clear demand identifies the policy and claim numbers, states that the parties disagree on the amount of loss, cites the appraisal provision, and names your appraiser or says you will do so within the policy’s time frame.</p>
<ul>
<li>Send it by a method you can prove, such as certified mail plus email to the adjuster.</li>
<li>Check whether the policy asks for a sworn proof of loss or other conditions first.</li>
<li>Keep a dated copy; many policy clocks start on the day the demand is received.</li>
</ul>
"""),
    ("Each side appoints an appraiser", """
<p>You and the insurer each choose a competent and disinterested appraiser, commonly within 20 days of the demand. “Disinterested” means your appraiser should have no financial stake in the outcome beyond a fair fee and should not be the contractor hoping to do the repair.</p>
<p>Your appraiser reviews the file, the policy, both estimates and the photo record. The insurer’s appraiser does the same for its side. From this point, the two appraisers talk directly with each other rather than through the adjuster.</p>
"""),
    ("Agree on an umpire", """
<p>The two appraisers then pick a neutral umpire, often within 15 days. Good practice is to settle on the umpire early, before positions harden, so that person is ready if the appraisers stall on a few items.</p>
<p>If the appraisers can’t agree on an umpire, most policies let either party ask a court of record in the county where the property sits to appoint one. In South Carolina, that request goes to the circuit court for that county, such as Charleston, Horry or Greenville County.</p>
"""),
    ("Inspect the property, exchange estimates", """
<p>Both appraisers inspect the damage, ideally together so they can agree on measurements and conditions on the spot. Expect roof slopes, pitches and squares to be measured, interiors to be checked with moisture meters, and attics to be examined for hidden framing damage after a wind or tree loss.</p>
<p>Each appraiser then prepares or adopts a detailed estimate, usually built in Xactimate or a similar pricing program using local South Carolina price data. The estimates are exchanged so each side can see exactly where the numbers diverge.</p>
"""),
    ("Negotiate line by line", """
<p>The appraisers work through the estimates item by item. Most lines settle quickly once both sides see the same photos and measurements. The remaining disputes tend to cluster around a familiar list:</p>
<ul>
<li>Matching of shingles, siding or flooring that can’t be blended.</li>
<li>Ordinance or law items required by the local building department.</li>
<li>Overhead and profit for a general contractor on a multi-trade job.</li>
<li>Steep and high-roof charges, waste factors and labor minimums.</li>
</ul>
<p>When the two appraisers agree on every line, they can sign an award together and the umpire never needs to rule.</p>
"""),
    ("The umpire decides open items", """
<p>Any items the appraisers can’t resolve go to the umpire. Each appraiser submits a short position on each disputed line with supporting photos, pricing and code references. Some umpires inspect the property themselves; others decide from the record.</p>
<p>The umpire picks a value for each open item, which may fall anywhere between the two positions. An agreement in writing by any two of the three panel members sets the amount of loss.</p>
"""),
    ("Award, payment and depreciation", """
<p>The signed award states the amount of loss, often split into replacement cost and actual cash value. The insurer then applies your deductible and prior payments, and issues payment within the time the policy allows.</p>
<p>If your policy pays replacement cost, the carrier may hold back recoverable depreciation until repairs are done; keep invoices and completion photos so you can claim it. If you have a mortgage, expect the lender to be named on the check under the mortgagee clause, which means coordinating endorsement and any draw schedule with your loan servicer.</p>
"""),
]

PROCESS_AFTER = """
<h2>Where appraisal stops short</h2>
<p>Appraisal is a pricing tool. It settles the amount of a covered loss, and in many South Carolina disputes that is the whole problem. It is not built to answer every question a claim can raise, and pushing the wrong question into appraisal wastes time.</p>
<ul>
<li><strong>Coverage denials.</strong> If the insurer says the loss isn’t covered at all, the panel generally can’t override that decision.</li>
<li><strong>Bad-faith or unfair claims practice concerns.</strong> Appraisal does not decide whether an insurer acted unreasonably. Those questions belong with a South Carolina attorney.</li>
<li><strong>Policy interpretation.</strong> Disputes about what a clause means — which deductible applies, or how an exclusion reads — are legal questions.</li>
<li><strong>Your suit-limitation clock.</strong> Appraisal may not pause the deadline to file suit. Confirm your dates with a South Carolina attorney before the process drags on.</li>
</ul>
<p>Causation sits in a gray zone. Some appraisal panels value damage by cause, such as wind versus flood, and courts have taken different views on how far they may go. If causation is the core of your dispute, get legal advice before you demand appraisal.</p>
<div class="note"><b class="h">How appraisal fees usually work</b>Under most South Carolina policies, each side pays its own appraiser and the two sides split the umpire’s fee. Appraisers may charge hourly, a flat fee or, in some arrangements, a percentage of the award. Ask for the fee terms in writing before you sign, and run your own numbers with our <a href="/free-claim-tools/claim-gap-fee-estimator/">claim gap and fee estimator</a>.</div>
"""

# Combined page body, for builds that render the guide as one block.
PROCESS_BODY = PROCESS_INTRO + "".join(
    f"<h2>{name}</h2>{html}" for name, html in PROCESS_STEPS
) + PROCESS_AFTER

# --------------------------------------------------------------------------- FAQ

FAQ = [
    ("The basics", [
        ("What does an insurance appraiser actually do?",
         "An insurance appraiser values the cost to repair or replace damaged property under the terms of a policy. When you and your insurer agree a loss is covered but disagree on the price, each side names an appraiser, and those two try to agree on the amount of loss, with an umpire breaking any deadlock."),
        ("Is appraisal the same as going to court?",
         "No. Appraisal is a private process written into your policy, and it normally decides only the amount of loss. A lawsuit can address coverage, contract interpretation and other legal claims. For anything beyond price, talk with a South Carolina attorney."),
        ("Who can invoke appraisal?",
         "Either party: you or the insurance company. The demand should be in writing, cite the appraisal provision in your policy and state that the parties disagree on the amount of loss."),
        ("Is the appraisal award binding?",
         "On the amount of loss, generally yes, once any two of the three panel members sign. Courts can set awards aside in limited situations, such as fraud, a biased panel member or a panel deciding questions outside its authority."),
        ("Does appraisal work for commercial and HOA claims?",
         "Yes. Commercial, condominium association and HOA master policies usually carry an appraisal clause that works the same way. Those claims often involve more buildings, more trades and contents or business income, so they tend to take longer."),
    ]),
    ("Costs & fees", [
        ("How are insurance appraisers paid?",
         "Arrangements vary. Some appraisers bill hourly, some charge a flat fee and some work for a percentage of the award or of the increase over the insurer’s number. Whatever the structure, get it in writing before you sign."),
        ("Who pays the umpire?",
         "Under most policy wording, each side pays its own appraiser and the two sides share the umpire’s fee equally. Check your policy, because some carriers use different language."),
        ("Is appraisal worth it for a small gap?",
         "Often not. If the difference between estimates is only a few thousand dollars, appraisal fees can eat most of the gain. A well-documented supplement request or a call to the adjuster’s supervisor may be the better first step."),
        ("Can I recover appraisal costs from the insurer?",
         "Usually the policy says each side bears its own appraisal costs. Whether any fees can be shifted in a later dispute is a legal question that depends on the facts, so ask a South Carolina attorney rather than assuming either way."),
    ]),
    ("Timing & deadlines", [
        ("How long does appraisal take in South Carolina?",
         "Many residential appraisals wrap up within two to four months of the demand, depending on how fast both appraisers are named and whether an umpire is needed. Large commercial, condo or contents claims, and periods right after a major hurricane, can stretch that timeline."),
        ("Is there a deadline to demand appraisal?",
         "Some policies set one and many don’t, but waiting too long can create arguments about waiver. Separately, your policy may set a deadline to file suit, and South Carolina contract claims generally carry a three-year limitation period. Confirm with a South Carolina attorney how those rules apply to your claim."),
        ("How quickly must each side name its appraiser?",
         "Many policies give each side 20 days from the demand to name an appraiser and give the appraisers 15 days to agree on an umpire. Calendar those dates the day the demand goes out or arrives."),
        ("Does appraisal pause my deadline to sue?",
         "Not automatically. Depending on the policy wording and the facts, the suit-limitation clock may keep running during appraisal. If your deadline is getting close, speak with a South Carolina attorney before relying on appraisal alone."),
        ("When does the insurer have to pay after an award?",
         "The policy usually sets a payment window after the award is signed, often measured in days. Expect the deductible and prior payments to come off, recoverable depreciation to be held until repairs are complete, and your mortgage lender to be named on the check."),
    ]),
    ("South Carolina specifics", [
        ("How do hurricane deductibles work in South Carolina?",
         "Many coastal policies use a hurricane or named-storm deductible set as a percentage of the dwelling limit, often 1% to 5% or more, instead of a flat dollar amount. Whether it applies depends on the trigger wording in your policy, such as a watch or warning being issued. Check the declarations page, where the deductible must be disclosed."),
        ("Does a wind pool policy from SCWHUA include appraisal?",
         "The South Carolina Wind and Hail Underwriting Association insures wind and hail in designated coastal areas, and its policies, like most property forms, generally contain an appraisal provision. Read your current SCWHUA policy for the exact wording, and remember that your homeowners and flood policies are handled separately."),
        ("Can flood damage go to appraisal?",
         "Flood is excluded from standard homeowners policies and is covered by a separate NFIP or private flood policy. The NFIP’s standard flood policy has its own appraisal provision and strict proof-of-loss rules set by federal regulation. Private flood policies follow their own wording."),
        ("Where can I complain about how my claim was handled?",
         "The South Carolina Department of Insurance (SCDOI) accepts consumer complaints and licenses adjusters. A complaint can prompt a response from the carrier, but SCDOI doesn’t set the value of your loss. Questions about bad faith or unfair claims practices are for a South Carolina attorney."),
        ("What happens if the appraisers can’t agree on an umpire?",
         "Most policies let either side ask a court of record in the county where the property is located to appoint one. In South Carolina, that is the circuit court for the county, and the request is a short filing that an attorney typically handles."),
    ]),
    ("Working with us", [
        ("What do you need to review my claim?",
         "Send the full policy and declarations page, the insurer’s estimate, any contractor estimates, correspondence with the adjuster and your photos. With those, we can tell you whether the gap looks like an amount dispute that suits appraisal."),
        ("Are you a public adjuster or a law firm?",
         "Neither. We are an independent insurance appraisal practice. We serve as appraiser, estimate reviewer or umpire on disputed property claims. We don’t negotiate the claim as a public adjuster would, and we don’t give legal advice."),
        ("Do you serve my part of South Carolina?",
         "We work on claims statewide, from the Upstate and Midlands to the Pee Dee, the Grand Strand and the Lowcountry. Inspections are scheduled around the claim, and much of the estimate work can be done from your documents."),
        ("Can you act as an umpire?",
         "Yes, when both appraisers agree to appoint us or a court does. As an umpire, we stay neutral and decide only the items the two appraisers can’t resolve."),
        ("Will you tell me if appraisal isn’t a good fit?",
         "Yes. If the gap is small, the dispute is really about coverage, or a legal deadline is close, we’ll say so plainly and suggest other routes, including speaking with a South Carolina attorney."),
    ]),
]

# --------------------------------------------------------------------------- glossary

GLOSSARY = [
    ("Actual cash value (ACV)", "The replacement cost of damaged property minus depreciation for age and wear. Many policies pay ACV first and the balance after repairs are finished."),
    ("Additional living expense (ALE)", "The increase in your normal living costs, such as a rental or hotel and extra meals, while a covered loss leaves your home unlivable. It is usually paid under Coverage D."),
    ("Anti-concurrent causation", "Policy wording that excludes a loss caused by an excluded peril, such as flood, even if a covered peril, such as wind, contributed at the same time. Courts read these clauses differently, so legal advice matters when one is in play."),
    ("Appraisal award", "The written decision that sets the amount of loss, signed by at least two of the three panel members. It is generally binding on the amount but not on coverage questions."),
    ("Appraisal clause", "The policy provision that lets either party demand appraisal when they agree a loss is covered but disagree on its amount. It sets out how appraisers and the umpire are chosen."),
    ("Appraiser", "The person each side chooses to value the loss during appraisal. Most policies require the appraiser to be competent and disinterested."),
    ("Catastrophe savings account", "A tax-advantaged savings account created by South Carolina’s 2007 coastal insurance reforms. Homeowners can use it to set money aside for a hurricane deductible or other uninsured storm losses."),
    ("Coinsurance", "A clause, common in commercial policies, that reduces a claim payment if the property was insured for less than a required percentage of its value. The shortfall is shared by the policyholder."),
    ("Coverage A (dwelling)", "The part of a homeowners policy that covers the house itself and attached structures. Its limit is often the base for percentage hurricane deductibles."),
    ("Coverage B (other structures)", "Coverage for detached structures on the property, such as fences, sheds and detached garages. Its limit is usually a percentage of Coverage A."),
    ("Coverage C (personal property)", "Coverage for belongings such as furniture, clothing and electronics. It may pay actual cash value or replacement cost depending on the policy."),
    ("Coverage D (loss of use)", "Coverage for additional living expense or lost rental income when a covered loss makes the home unlivable. It is often limited by dollars or time."),
    ("Declarations page", "The summary page of a policy listing the insured, the property, coverage limits, deductibles and endorsements. In South Carolina, hurricane deductibles must be clearly disclosed on it."),
    ("Deductible", "The portion of a covered loss the policyholder pays before the insurer pays. It may be a flat dollar amount or a percentage of the dwelling limit."),
    ("Depreciation", "The reduction in value of property due to age, wear and condition. It is the difference between replacement cost and actual cash value."),
    ("Earthquake endorsement", "An add-on that brings earthquake damage into a policy that otherwise excludes it. It usually carries its own, often large, percentage deductible."),
    ("Endorsement", "A written change to a policy that adds, removes or modifies coverage. Endorsements control over the base policy wording where they conflict."),
    ("Hurricane deductible", "A separate deductible that applies to losses from a hurricane, often a percentage of the dwelling limit. The policy’s trigger wording defines when it applies instead of the standard deductible."),
    ("Matching", "The question of whether undamaged materials must be replaced so repairs match in color, texture and appearance. Policy wording and the availability of materials drive these disputes."),
    ("Mitigation", "Reasonable steps to protect property from further damage after a loss, such as tarping a roof or drying a wet room. Most policies require it and pay reasonable mitigation costs."),
    ("Mortgagee clause", "A policy provision that protects the mortgage lender’s interest in the property. It is why lenders are often named on claim checks."),
    ("Named storm", "A tropical storm or hurricane that has been given a name by the National Hurricane Center. Some policies use a named-storm deductible triggered by any such storm, not only hurricanes."),
    ("National Flood Insurance Program (NFIP)", "The federal program that writes most flood insurance in the United States. Its standard flood policy has its own rules, deadlines and appraisal provision."),
    ("Ordinance or law coverage", "Coverage for the extra cost of meeting current building codes when damaged property is repaired or rebuilt. It is often limited to a percentage of the dwelling limit."),
    ("Overhead and profit", "The general contractor’s charge for managing and coordinating a job, often estimated at 10% overhead plus 10% profit. It is a frequent dispute when a repair involves several trades."),
    ("Peril", "A cause of loss, such as wind, hail, fire, lightning or theft. Policies either list covered perils or cover all perils except those excluded."),
    ("Proof of loss", "A sworn statement of the amount claimed and supporting details. Some policies, including the NFIP flood policy, require it within a set time."),
    ("Recoverable depreciation", "Depreciation held back from an initial replacement cost claim payment that can be recovered once repairs or replacement are completed. Time limits often apply."),
    ("Replacement cost value (RCV)", "The cost to repair or replace damaged property with materials of like kind and quality, without deducting depreciation."),
    ("Reservation of rights", "A letter in which the insurer says it is handling a claim while reserving the right to deny coverage later. It signals a possible coverage issue worth reviewing carefully."),
    ("SC Safe Home", "A South Carolina grant program, created under the 2007 coastal insurance reforms, that helps eligible homeowners pay for wind-resistance upgrades such as roof-to-wall connections and opening protection."),
    ("Scope of loss", "The list of damaged items and the repair work each one needs. Most appraisal disputes start with differences in scope rather than in unit prices."),
    ("South Carolina Department of Insurance (SCDOI)", "The state agency that regulates insurers, licenses adjusters and handles consumer complaints. It does not decide the value of individual claims."),
    ("South Carolina Wind and Hail Underwriting Association (SCWHUA)", "The insurer of last resort for wind and hail coverage in designated coastal areas of South Carolina. Its wind-only policies are often paired with a homeowners policy that excludes wind."),
    ("Square (roofing)", "A unit of roof area equal to 100 square feet. Roofing estimates are priced per square, plus a waste factor."),
    ("Steep charge", "An added labor charge for working on steep roof slopes, commonly applied at about a 7/12 pitch and steeper. It is a frequent line-item dispute in roof estimates."),
    ("Storm surge", "Seawater pushed ashore by a hurricane or tropical storm. Damage from surge is treated as flood and is excluded from standard homeowners and wind policies."),
    ("Subrogation", "The insurer’s right, after paying a claim, to pursue a third party who caused the loss. Policyholders must not waive that right without the insurer’s consent."),
    ("Suit limitation", "The time limit for filing a lawsuit over a claim, set by the policy, by statute or both. Confirm the deadline that applies with a South Carolina attorney."),
    ("Supplement", "A request to add items or costs to an insurer’s estimate, often after hidden damage is found during repairs. Many disputes resolve through supplements without appraisal."),
    ("Umpire", "The neutral third member of an appraisal panel who decides only the items the two appraisers cannot resolve. Agreement by any two panel members sets the award."),
    ("Wind-driven rain", "Rain forced into a building by high wind. Many policies cover interior water damage only if wind first creates an opening in the roof or walls."),
    ("Xactimate", "Estimating software widely used by insurers, adjusters and contractors to price repairs with regional cost data. Appraisers often build or compare estimates in it."),
]

# --------------------------------------------------------------------------- guide posts

POSTS = [
    {
        "slug": "hurricane-deductibles-explained",
        "title": "Hurricane Deductible in South Carolina: Triggers, Math and Disputes",
        "kw": "hurricane deductible in South Carolina",
        "seo": "Hurricane Deductible in South Carolina, Explained",
        "desc": "How a hurricane deductible in South Carolina is triggered and calculated, with illustrative math and where appraisal can and can’t help.",
        "summary": "Percentage deductibles can swallow a coastal claim. Here’s how triggers work, how the math runs and where disputes really start.",
        "date": "2026-09-03",
        "read": "7 min",
        "body": """
<h2>Why this deductible catches people off guard</h2>
<p>For many homeowners, the hurricane deductible in South Carolina policies is the single largest number on the declarations page, and it is easy to miss until a storm arrives. A standard deductible might be $1,000 or $2,500. A hurricane deductible is often a percentage of the dwelling limit, and on a coastal home that can mean five figures before the insurer pays anything.</p>
<p>That gap shapes almost every storm claim along the coast, from Hilton Head Island and Beaufort to Charleston, Georgetown and the Grand Strand. It also matters inland. Hugo pushed damaging winds through Sumter and the Midlands in 1989, and Helene brought widespread tree fall to the Upstate and Aiken County in 2024. Whether a hurricane deductible applied to those inland losses came down to each policy’s wording.</p>

<h2>What triggers it</h2>
<p>There is no single statewide trigger. Each policy defines when its hurricane or named-storm deductible replaces the standard one. Common approaches include:</p>
<ul>
<li><strong>Watch or warning triggers.</strong> The deductible applies to losses during a window that starts when the National Weather Service issues a hurricane watch or warning for any part of South Carolina and ends a set number of hours after it is lifted.</li>
<li><strong>Named-storm triggers.</strong> The deductible applies to any storm named by the National Hurricane Center, including tropical storms that never reach hurricane strength.</li>
<li><strong>Peril limits.</strong> Many forms apply the deductible only to wind and hail during the storm window. Fire from a lightning strike during the same storm may fall under the standard deductible.</li>
</ul>
<p>Read the trigger language word for word. A storm like Matthew in 2016, which made landfall near McClellanville as a Category 1, or Ian in 2022, which came ashore near Georgetown, can produce very different deductible outcomes under two policies on the same street.</p>

<h2>How the math works</h2>
<p>A percentage deductible is calculated on the Coverage A dwelling limit, not on the amount of damage. That is the part most people get wrong.</p>
<p>Here are illustrative figures only. Say a Mount Pleasant home is insured for $450,000 under Coverage A with a 2% hurricane deductible. The deductible is $9,000. If the insurer values the wind damage at $11,500, the payment is $2,500. If your contractor’s estimate is $24,000, the payment would be $15,000. Same deductible, but the gap between the two estimates is now the whole claim.</p>
<p>The same arithmetic explains why small underpricing hurts so much on a coastal claim. A missing ridge vent, a short count on roof squares or no overhead and profit can push a claim from barely above the deductible to below it. You can test your own numbers with our <a href="/free-claim-tools/hurricane-deductible-calculator/">hurricane deductible calculator</a>.</p>
<h3>Stacked deductibles</h3>
<p>Homes in coastal areas that pair a South Carolina Wind and Hail Underwriting Association wind policy with a homeowners policy and a flood policy can face more than one deductible from one storm. Wind damage carries the wind policy’s hurricane deductible, water from storm surge carries the flood deductible, and an unrelated covered loss carries the homeowners deductible.</p>

<h2>Disputes appraisal can help with</h2>
<p>Appraisal decides the amount of a covered loss. It does not usually decide which deductible applies, because that is a question of policy interpretation. But the amount is often the real fight. Disputes that fit appraisal include:</p>
<ul>
<li>Whether the full roof slope or only a few shingles need replacement.</li>
<li>Matching of siding, shingles or flooring that can’t be blended with existing materials.</li>
<li>Steep and high-roof charges on the multi-story homes common in the Lowcountry.</li>
<li>Code upgrades required by the local building department, such as drip edge, underlayment or roof-to-wall connections.</li>
<li>Interior water damage from wind-driven rain after the roof was opened up.</li>
</ul>
<p>When the insurer’s number sits just under the deductible, a careful line-by-line valuation can make the difference between no payment and a meaningful one. Our <a href="/claim-dispute-services/hurricane-claim-appraisal/">hurricane claim appraisal</a> page explains how we approach those reviews.</p>
<div class="note"><b class="h">Coverage questions go elsewhere</b>If you believe the hurricane deductible was applied when it shouldn’t have been — for example, the loss happened outside the trigger window — that is a coverage dispute. Raise it in writing with the insurer, consider a complaint to the South Carolina Department of Insurance, and talk with a South Carolina attorney.</div>

<h2>Ways to soften the blow before the next storm</h2>
<p>South Carolina’s 2007 coastal insurance reforms added a few tools worth knowing about. None of them is legal or tax advice, so confirm details with the program or a professional.</p>
<ul>
<li><strong>Clear disclosure.</strong> Insurers must clearly disclose a hurricane deductible, so you should find the dollar or percentage amount on your declarations page. If it isn’t clear, ask your agent to state it in dollars.</li>
<li><strong>Catastrophe savings accounts.</strong> These tax-advantaged accounts let you set money aside for a hurricane deductible or other uninsured storm losses.</li>
<li><strong>SC Safe Home grants.</strong> Eligible homeowners can apply for help paying for wind-resistance upgrades, which may also qualify for insurance discounts.</li>
</ul>
<p>It also pays to review your deductible choice at each renewal. A lower percentage costs more in premium, but on an older roof in Beaufort County it may be cheaper over time than absorbing a large share of the next storm yourself.</p>

<h2>What to do after the storm</h2>
<p>Photograph the damage before any cleanup, keep receipts for tarps and emergency repairs, and get a detailed written estimate from a contractor who itemizes quantities rather than giving a single lump sum. When the insurer’s estimate arrives, compare it with yours line by line, subtract the deductible from both, and look at what is actually in dispute. If the gap is large and the disagreement is about price and scope rather than coverage, appraisal may be the right next step.</p>
""",
    },
    {
        "slug": "when-a-tree-falls-on-your-house",
        "title": "When a Tree Falls on Your House: A Tree Fall Insurance Claim Guide",
        "kw": "tree fall insurance claim",
        "seo": "Tree Fall Insurance Claim Guide for SC Homeowners",
        "desc": "A South Carolina tree fall insurance claim guide: removal limits, hidden framing damage, Helene lessons and when appraisal fits the dispute.",
        "summary": "Helene dropped trees on thousands of Upstate and Aiken County homes. What policies usually pay for, what gets missed and when appraisal helps.",
        "date": "2026-09-17",
        "read": "8 min",
        "body": """
<h2>Helene changed how South Carolina thinks about trees</h2>
<p>Hurricane Helene crossed the state on September 26–27, 2024, and the damage that followed was less about storm surge than about trees. Across the Upstate and Aiken County, tall pines and hardwoods came down on roofs, cars and power lines, and outages lasted for days or weeks. For many owners it was their first tree fall insurance claim, and many found that the first estimate missed a good deal of what the tree actually broke.</p>
<p>Trees fall for many reasons here: hurricanes and tropical storms, spring thunderstorms and tornadoes, and ice storms like the one that coated Aiken, the Midlands and the Pee Dee in February 2014. The claim process is similar in each case, and so are the disputes.</p>

<h2>The first 48 hours</h2>
<p>Safety comes first. Stay away from downed lines and call the utility. Once the area is safe, your policy almost certainly requires you to take reasonable steps to prevent further damage. Those steps are usually covered, and they also create the evidence your claim will rely on.</p>
<ul>
<li>Photograph the tree on the house from every side before anything is moved, including the root ball or broken trunk.</li>
<li>Take wide shots showing the tree’s path and close-ups of where it struck the roof, walls, gutters and fences.</li>
<li>Hire a tree service with a crane if needed, and ask for an itemized invoice listing crane time, crew hours and haul-off.</li>
<li>Tarp the roof and board openings, and keep every receipt.</li>
<li>Photograph the attic and interior ceilings right after removal, before drywall is torn out.</li>
</ul>
<p>For a fuller room-by-room list, see our <a href="/appraisal-guides/storm-damage-photo-checklist/">storm damage photo checklist</a>.</p>

<h2>What policies usually cover</h2>
<p>Most South Carolina homeowners policies follow a similar pattern, though your wording controls.</p>
<h3>Damage to the house and other structures</h3>
<p>If a tree falls because of wind, ice or another covered peril and strikes your house, the damage to the dwelling is generally covered under Coverage A, subject to your deductible. Fences, sheds and detached garages fall under Coverage B. It usually doesn’t matter whose tree it was. If a neighbor’s healthy tree lands on your roof, your own policy typically responds. The picture can change if the tree was obviously dead or diseased and the owner ignored it, but that is a liability question for the insurers involved.</p>
<h3>Removing the tree</h3>
<p>Removing the part of the tree that is on or in the house is normally treated as part of the repair. Removing trees that fell without hitting a covered structure is a different matter. Many forms offer only a modest debris removal allowance — often around $500 per tree and $1,000 per loss in common forms — and only when a tree blocks a driveway or similar access. Check your policy for the exact figure.</p>
<h3>Living elsewhere</h3>
<p>If the house can’t be lived in, Coverage D may pay additional living expense. Keep hotel and meal receipts and a simple log of extra miles driven.</p>

<h2>Where estimates fall short</h2>
<p>The first adjuster estimate on a tree claim is often written from the ground or from photos, sometimes weeks after the storm when adjusters are stretched thin. Common gaps include:</p>
<ul>
<li><strong>Hidden framing damage.</strong> A tree that cracks a rafter or truss can leave the roof deck looking intact from below. Broken framing needs repair, and an engineer’s letter may be warranted.</li>
<li><strong>Interior water damage.</strong> Rain through a puncture can soak insulation, drywall and flooring. Moisture readings taken early matter.</li>
<li><strong>Roof scope.</strong> A carrier may price a patch where the damaged area, shingle availability or local code calls for replacing whole slopes.</li>
<li><strong>Crane and access costs.</strong> On a tight lot in a Greenville mill village or a wooded Aiken subdivision, the crane can cost more than the carpentry.</li>
<li><strong>Matching.</strong> Siding, gutters and shingles that can’t be matched may need wider replacement.</li>
<li><strong>Overhead and profit.</strong> Tree claims typically involve roofing, framing, drywall, paint and electrical, which is the classic case for a general contractor.</li>
</ul>
<div class="note"><b class="h">Illustrative example</b>For example, a carrier might estimate $14,000 for roof patching and tree removal on a Spartanburg home. After the attic is opened, the contractor finds three broken trusses and wet insulation and prices the job at $31,000. Those are illustrative figures, but a gap of that shape is a classic amount-of-loss dispute.</div>

<h2>When appraisal fits — and when it doesn’t</h2>
<p>Start with a supplement. Send the adjuster the attic photos, the engineer’s letter if you have one, the tree service invoice and your contractor’s itemized estimate. Many tree claims are corrected at this stage.</p>
<p>If the carrier still won’t move, appraisal is well suited to tree claims because the disputes are usually about scope and price: how much framing is broken, whether slopes need full replacement, what a crane costs, and whether O&amp;P applies. Our <a href="/claim-dispute-services/tree-fall-ice-storm-appraisal/">tree fall and ice storm appraisal</a> service handles exactly these questions.</p>
<p>Appraisal is the wrong tool if the insurer says a tree removal limit doesn’t apply at all, or denies the claim on the ground that the tree fell from rot rather than wind. Those are coverage questions. A written request for the basis of the denial is a sensible first step, and a South Carolina attorney can advise on what comes next.</p>

<h2>A short checklist before you call anyone</h2>
<ul>
<li>Find the full policy, not just the declarations page, and note your deductible and any tree or debris limits.</li>
<li>Gather every photo, invoice and receipt in one folder with dates.</li>
<li>Get at least one itemized contractor estimate that includes framing, interior and access costs.</li>
<li>Write down the claim number, adjuster name and each conversation.</li>
</ul>
<p>Good records do not guarantee a higher payment, but they make every later step, from a supplement to an umpire’s decision, faster and fairer.</p>
""",
    },
    {
        "slug": "wind-pool-claims-and-appraisal",
        "title": "Wind Pool Claims and Appraisal: SCWHUA, Homeowners and Flood",
        "kw": "wind pool claims",
        "seo": "Wind Pool Claims and Appraisal in South Carolina",
        "desc": "How wind pool claims work on the South Carolina coast when SCWHUA, homeowners and flood policies stack, and where appraisal fits each one.",
        "summary": "Many coastal homes carry three policies for one storm. How SCWHUA, homeowners and flood claims interact, and where appraisal helps.",
        "date": "2026-10-01",
        "read": "8 min",
        "body": """
<h2>Three policies, one storm</h2>
<p>On much of the South Carolina coast, a single hurricane can produce three separate claims. Wind pool claims go to the South Carolina Wind and Hail Underwriting Association (SCWHUA), the insurer of last resort for wind and hail in designated coastal areas. Fire, theft and other non-wind losses go to a homeowners policy that excludes wind. Water from storm surge or rising rivers goes to a flood policy through the National Flood Insurance Program or a private carrier.</p>
<p>The arrangement is common from Hilton Head Island and Bluffton through Charleston, Mount Pleasant and Georgetown up to North Myrtle Beach. Each policy has its own adjuster, deductible, deadlines and, usually, its own appraisal provision. Treating them as one claim is the most common mistake owners make after a storm.</p>

<h2>Why the wind and water split matters</h2>
<p>After a hurricane, the central question on a coastal home is often what wind did and what water did. Storm surge is flood. Wind-driven rain through a damaged roof is usually wind. A ground floor wrecked by surge and a second floor soaked through a torn roof may belong to two different carriers.</p>
<p>South Carolina has seen this play out repeatedly. Hugo in 1989 brought both catastrophic surge and violent wind around Charleston and Sullivan’s Island. Matthew in 2016 caused heavy tree loss on Hilton Head and Beaufort alongside flooding. Ian’s landfall near Georgetown in 2022 again mixed wind and water. In each case, owners who carried separate wind, home and flood policies had to show which damage belonged where.</p>
<h3>Anti-concurrent causation</h3>
<p>Many policies contain anti-concurrent causation language, which says a loss caused by an excluded peril such as flood is excluded even if wind contributed at the same time. How these clauses apply depends on the exact wording and the facts, and courts in different places have reached different conclusions. If an insurer relies on this language to deny part of a claim, that is a coverage question to raise with a South Carolina attorney, not something an appraisal panel can settle on its own.</p>

<h2>Evidence that separates wind from water</h2>
<p>The better the record, the easier it is to assign each item to the right policy. Useful evidence includes:</p>
<ul>
<li>Photos of the water line inside and outside, with a tape measure in frame.</li>
<li>Photos of the roof, soffits and windows showing openings created by wind.</li>
<li>Water stains that run down from ceilings, which point to rain intrusion rather than rising water.</li>
<li>Debris lines, sand and marsh wrack showing how far surge reached.</li>
<li>Weather data and any engineer’s report on wind speeds and surge height at your address.</li>
</ul>
<p>Our <a href="/free-claim-tools/wind-flood-damage-splitter/">wind and flood damage splitter</a> can help you organize damage room by room before you talk with adjusters.</p>

<h2>How appraisal applies to each policy</h2>
<p>Appraisal works one policy at a time. A dispute with SCWHUA over the amount of wind damage is resolved under the SCWHUA policy’s appraisal provision, with appraisers and an umpire chosen for that claim. Check your current wind policy for the exact wording, timelines and any conditions that must be met first.</p>
<p>Your homeowners policy will have its own provision, and so will a private flood policy. The NFIP’s standard flood policy also includes an appraisal provision, but it is governed by federal rules, including a strict proof-of-loss deadline that is typically 60 days from the date of loss unless FEMA extends it. Missing that deadline can be costly, so treat the flood claim as its own project with its own calendar.</p>
<div class="note"><b class="h">Same storm, separate deductibles</b>Illustrative figures only: a Surfside Beach home with a $300,000 wind limit and a 5% hurricane deductible faces a $15,000 wind deductible. Its flood policy may carry a separate $2,000 deductible, and the homeowners policy another for any non-wind loss. Before deciding whether appraisal is worth it, compare the gap on each policy after its own deductible.</div>

<h2>Common disputes in wind pool claims</h2>
<p>Once causation is sorted out, wind pool claims tend to involve the same pricing questions as any wind claim, magnified by coastal construction:</p>
<ul>
<li>Full roof replacement versus repairs on metal or tile roofs where matching parts are scarce.</li>
<li>Steep and high-roof charges on elevated homes with tall pilings.</li>
<li>Code requirements for coastal wind zones when roofs or windows are replaced.</li>
<li>Interior water damage from wind-driven rain and its effect on insulation and drywall.</li>
<li>Siding, trim and screened porches facing the ocean, where exposure is greatest.</li>
</ul>
<p>Those are amount disputes, and appraisal is designed for them. On high-rise and mid-rise condos on the Grand Strand, the association’s master policy may carry the building claim while individual owners carry their own interior coverage, adding yet another layer. Our <a href="/locations-served/myrtle-beach/">Myrtle Beach</a> page covers what we see most often along that stretch.</p>

<h2>Keeping the claims organized</h2>
<p>Practical habits make a three-policy claim manageable:</p>
<ul>
<li>Open a separate folder, log and calendar for each claim.</li>
<li>Give each adjuster the full photo set, but list which items you are claiming under their policy.</li>
<li>Ask each carrier for its estimate in writing, and compare them side by side so nothing falls between policies.</li>
<li>Track every deadline: proof of loss, appraisal timelines and any suit-limitation period. Confirm the suit deadlines with a South Carolina attorney.</li>
</ul>
<p>When the split between wind and water is settled and the remaining disagreement is about price and scope, appraisal under the right policy can bring a stalled coastal claim to a decision.</p>
""",
    },
    {
        "slug": "appraisal-versus-lawsuit",
        "title": "Appraisal vs Lawsuit: Two Paths for a South Carolina Claim Dispute",
        "kw": "appraisal vs lawsuit",
        "seo": "Appraisal vs Lawsuit for a South Carolina Claim",
        "desc": "Appraisal vs lawsuit for a South Carolina property claim: what each decides, typical cost and time, and when to call a South Carolina attorney.",
        "summary": "Appraisal settles price; a lawsuit can address much more. A plain comparison of the two paths, without legal advice.",
        "date": "2026-10-14",
        "read": "8 min",
        "body": """
<h2>Two tools for different problems</h2>
<p>When an insurance claim stalls, owners often frame the choice as appraisal vs lawsuit. In practice, the two answer different questions. Appraisal is a private process in your policy that decides how much a covered loss is worth. A lawsuit asks a court to decide legal disputes, which can include coverage, the meaning of the policy and how the insurer handled the claim.</p>
<p>This guide explains the differences in general terms. It is not legal advice, and we are not a law firm. If you are weighing a lawsuit, speak with a South Carolina attorney who handles insurance disputes.</p>

<h2>What appraisal decides</h2>
<p>Appraisal starts when either side makes a written demand under the policy. Each side names an appraiser, the appraisers choose an umpire, and agreement by any two of the three sets the amount of loss. The process is built for disputes such as:</p>
<ul>
<li>How many roof squares were damaged and whether slopes need full replacement.</li>
<li>Whether matching requires replacing undamaged siding or flooring.</li>
<li>Code upgrade costs, overhead and profit, and local labor and material prices.</li>
<li>The value of contents, or the cost to repair a commercial building or condo association property.</li>
</ul>
<p>Appraisal is usually faster and less formal than litigation. There is no discovery, no depositions and no trial. Each side pays its own appraiser and typically shares the umpire’s fee, so the cost is usually far below the cost of a lawsuit, though it is not free. An award on the amount of loss is generally binding, with limited grounds to challenge it.</p>
<p>Appraisal has firm limits. It generally does not decide whether a loss is covered, what a disputed clause means, or whether the insurer acted unreasonably. Our <a href="/claim-dispute-services/appraisal-demand-representation/">appraisal demand representation</a> page describes what an appraiser does within those limits.</p>

<h2>What a lawsuit can address</h2>
<p>A lawsuit is a formal proceeding in court. It can address the questions appraisal cannot, such as:</p>
<ul>
<li>An outright denial of coverage, including disputes about exclusions or anti-concurrent causation wording.</li>
<li>Disputes about policy conditions, notice, or whether the insurer waived a requirement.</li>
<li>Claims that the insurer handled the claim unreasonably.</li>
</ul>
<p>Lawsuits take longer and cost more, and outcomes are uncertain. They involve pleadings, discovery, expert witnesses and possibly a trial or mediation. A South Carolina attorney can explain how fees would work, whether any fees might be recoverable, and what a realistic timeline looks like for your case.</p>
<h3>Bad faith, in general terms</h3>
<p>South Carolina courts recognize a claim against an insurer that unreasonably refuses to pay benefits owed under its policy. A provision of Title 38 of the state insurance code can also allow attorney’s fees in some cases where an insurer refuses to pay without reasonable cause, and the state has rules on unfair claims practices. Whether any of this applies depends entirely on the facts. Appraisal does not decide bad faith, and only a South Carolina attorney can tell you whether you have such a claim.</p>

<h2>Can you use both?</h2>
<p>Sometimes. Appraisal and litigation are not always either-or. A few general points are worth knowing, all of which you should confirm with an attorney:</p>
<ul>
<li>Courts in many places have allowed appraisal to proceed on the amount of loss while legal issues are handled separately.</li>
<li>An appraisal award may resolve the price question and leave coverage or claims-handling issues for a court.</li>
<li>Appraisal may not pause the deadline to file suit. South Carolina contract actions generally carry a three-year limitation period, but policy wording and other rules matter, so confirm with a South Carolina attorney.</li>
</ul>
<div class="note"><b class="h">Watch the calendar</b>The biggest practical risk in choosing appraisal is letting a suit-limitation deadline pass while the panel is still working. If your loss is more than a year or two old, or the insurer has denied any part of it, talk with a South Carolina attorney before you send an appraisal demand.</div>

<h2>A simple way to frame the decision</h2>
<p>These questions won’t make the decision for you, but they help sort the dispute:</p>
<ul>
<li><strong>Has the insurer accepted the claim and paid something?</strong> If yes, and the fight is over price, appraisal is often a good fit.</li>
<li><strong>Is the insurer saying the loss isn’t covered at all?</strong> That is a legal question for an attorney.</li>
<li><strong>Is the main concern how the claim was handled?</strong> Delays, unexplained denials or ignored documentation raise questions an appraisal panel cannot answer.</li>
<li><strong>How big is the gap?</strong> For example, a $6,000 difference may not justify either path, while a $60,000 gap on a hurricane claim in Beaufort or Charleston may justify careful review. Those figures are illustrative.</li>
<li><strong>How close is any deadline?</strong> If a deadline is near, get legal advice first.</li>
</ul>
<p>You can also contact the South Carolina Department of Insurance with a complaint about claim handling. A complaint can prompt a response from the carrier, but it does not set the value of a loss or replace legal advice.</p>

<h2>Where we fit</h2>
<p>We are an independent appraisal practice. We can review estimates, serve as your appraiser, or act as a neutral umpire. When a dispute is really about coverage or claims handling, we will say so and suggest you speak with a South Carolina attorney. If you are unsure which path fits your claim, <a href="/contact-an-appraiser/">contact an appraiser</a> for an initial look at the estimates and the gap between them.</p>
""",
    },
    {
        "slug": "storm-damage-photo-checklist",
        "title": "Storm Damage Photo Checklist for South Carolina Homeowners",
        "kw": "storm damage photo checklist",
        "seo": "Storm Damage Photo Checklist for SC Homeowners",
        "desc": "A storm damage photo checklist for South Carolina homes: what to shoot before and after a storm, how to organize it and how appraisers use it.",
        "summary": "Photos are the evidence every adjuster, appraiser and umpire relies on. A room-by-room list of what to capture and how to keep it organized.",
        "date": "2026-10-23",
        "read": "7 min",
        "body": """
<h2>Why photos carry so much weight</h2>
<p>Every storm claim is decided, at some level, from pictures. Adjusters arrive days or weeks after a hurricane, contractors tear out wet materials fast, and appraisers and umpires often see the property only after repairs have started. A thorough storm damage photo checklist turns those gaps into a record no one can argue with.</p>
<p>South Carolina gives owners plenty of reasons to keep one handy: hurricanes and tropical storms on the coast, spring hail in the Upstate and Midlands, tornadoes like the April 2020 outbreak that hit Seneca and Hampton County, and ice storms that bring down limbs across the Pee Dee. The list below works for all of them.</p>

<h2>Before the storm: a baseline</h2>
<p>A ten-minute walk-around before hurricane season can save weeks of argument later. Take a short video of each room and each side of the house, and photograph:</p>
<ul>
<li>Each roof slope from the ground or a window, plus any skylights, vents and chimneys.</li>
<li>Siding, trim, gutters, fences, screened porches and outbuildings.</li>
<li>Flooring, cabinets and appliances, with model labels where easy.</li>
<li>Electronics, furniture and valuables, opening closets and drawers on the video.</li>
</ul>
<p>Store the files in cloud storage, not only on your phone. A baseline makes it much harder for anyone to say damage was pre-existing.</p>

<h2>After the storm: outside the house</h2>
<p>Wait until it is safe. Stay off the roof and away from downed lines. Then work from wide to close:</p>
<ul>
<li><strong>Wide shots</strong> of each elevation, with the street or a neighbor’s house in frame for location.</li>
<li><strong>Roof</strong> from the ground or a drone: missing shingles, lifted tabs, exposed decking, displaced metal panels or tile.</li>
<li><strong>Hail evidence</strong>: dents on gutters, downspouts, AC fins and soft metals, with a coin or ruler for scale.</li>
<li><strong>Trees and limbs</strong> where they struck the structure, before removal.</li>
<li><strong>Windows, doors, soffits and siding</strong>, especially on the side that faced the strongest wind.</li>
<li><strong>Fences, sheds and detached garages</strong>, which fall under a different coverage section.</li>
</ul>
<h3>If water came in from outside</h3>
<p>On coastal and riverside homes, record the high-water mark inside and outside with a tape measure in frame. Photograph debris lines, sand and mud. Storm surge and rising water are flood, usually covered under a separate policy, so these pictures help the adjusters split wind damage from water damage.</p>

<h2>After the storm: inside the house</h2>
<p>Go room by room in the same order every time. For each room, take one wide shot from the doorway, then close-ups of:</p>
<ul>
<li>Ceiling stains, sagging drywall and wet insulation, ideally with a moisture meter reading visible.</li>
<li>Wall stains, peeling paint and swollen baseboards.</li>
<li>Flooring that is cupped, buckled or stained.</li>
<li>Damaged contents, with labels, serial numbers and receipts photographed where possible.</li>
<li>The attic, especially decking, rafters and trusses near any roof damage.</li>
</ul>
<p>Photograph mitigation work as it happens: tarps going on, fans and dehumidifiers running, materials removed. Keep a sample of discontinued flooring or siding if you can, since matching disputes depend on it.</p>
<p>Video helps too. A slow, narrated walk-through of each room, saying the room name and date out loud, gives an adjuster or appraiser context that still photos can miss. For damaged contents you plan to throw away, photograph each item with its brand label before it goes to the curb, and ask the adjuster whether they want anything kept for inspection.</p>
<div class="note"><b class="h">Don’t delay mitigation for photos</b>Your policy expects you to protect the property from further damage. Take quick photos first, then tarp, dry and remove soaked materials. A fast, documented mitigation effort is far better than perfect photos of a home that grew mold while you waited.</div>

<h2>Organizing the record</h2>
<p>A thousand unsorted photos are hard for anyone to use. A little structure helps:</p>
<ul>
<li>Keep the original files; editing can strip the date and location data.</li>
<li>Make folders by area: roof, each exterior side, each room, contents, mitigation.</li>
<li>Add a simple index listing what each folder shows and when it was taken.</li>
<li>Save receipts, invoices and estimates in the same place.</li>
</ul>
<p>Our <a href="/free-claim-tools/appraisal-readiness-checkup/">appraisal readiness checkup</a> walks through the documents that help most if a dispute goes further.</p>

<h2>How appraisers and umpires use your photos</h2>
<p>In appraisal, photos do most of the heavy lifting. An appraiser uses them to support quantities, such as the number of damaged roof squares or the linear feet of siding. An umpire deciding a disputed line item will look for proof that damage existed, that it was caused by the storm and that the repair proposed is the one needed.</p>
<p>Photos are especially important on roofs, where hail and wind damage can be hard to see once repairs begin. Our <a href="/claim-dispute-services/roof-hail-damage-appraisal/">roof and hail damage appraisal</a> page explains how roof disputes are typically valued. For example, a clear set of ground and drone shots showing creased shingles on all four slopes is far more persuasive than a single photo of one damaged tab.</p>
<p>Good photos won’t guarantee any result, but they make every step clearer, from the first adjuster visit through a supplement and, if it comes to that, an appraisal award.</p>
""",
    },
    {
        "slug": "how-umpires-decide-line-items",
        "title": "How an Appraisal Umpire Decides Disputed Line Items",
        "kw": "appraisal umpire",
        "seo": "How an Appraisal Umpire Decides Line Items",
        "desc": "How an appraisal umpire weighs disputed line items such as matching, O&P, steep charges and code upgrades, and how to present your side.",
        "summary": "The umpire only rules on what the appraisers can’t settle. What that looks like item by item, and what makes a position persuasive.",
        "date": "2026-11-05",
        "read": "8 min",
        "body": """
<h2>The umpire’s narrow job</h2>
<p>An appraisal umpire is the neutral third member of the panel. Under most South Carolina policies, the umpire is chosen by the two appraisers, or appointed by the circuit court in the county where the property sits if they can’t agree. The umpire does not redo the whole estimate. The job is to decide only the items the two appraisers could not resolve, then join one of them in signing an award.</p>
<p>That narrow role shapes everything. A well-run appraisal often reaches the umpire with dozens of items already agreed and a short list still open. The quality of that short list, and the evidence behind each item, usually decides how the award comes out.</p>

<h2>What the umpire receives</h2>
<p>Practices vary, but umpires typically receive:</p>
<ul>
<li>Both appraisers’ estimates, often in Xactimate format, with agreed items marked.</li>
<li>A dispute list showing each open item and each side’s value.</li>
<li>Photos, measurements, moisture readings and any engineer or contractor reports.</li>
<li>Code references, manufacturer documents and pricing support.</li>
<li>The relevant parts of the policy, such as the loss settlement and matching wording.</li>
</ul>
<p>Some umpires inspect the property; others decide from the record or hold a short meeting with both appraisers. In all cases, the umpire works within the policy and does not decide coverage questions.</p>

<h2>Common items and how they are weighed</h2>
<h3>Quantities</h3>
<p>Disputes over roof squares, siding square footage or the number of rooms affected usually turn on measurements. An umpire tends to favor measured diagrams, aerial measurement reports and photos tied to specific slopes or walls over estimates by eye. Waste factors are weighed against the roof’s complexity: a cut-up hip roof on a Charleston single house needs more waste than a simple gable.</p>
<h3>Matching</h3>
<p>When undamaged materials can’t be matched, the question is how far replacement must extend. Umpires look at the policy wording, whether the material is discontinued, and whether a repair would leave an obvious mismatch on a continuous surface. Samples, supplier letters and clear photos of color and profile help.</p>
<h3>Overhead and profit</h3>
<p>Overhead and profit for a general contractor is often disputed. Umpires typically consider how many trades are involved, whether coordination and supervision are genuinely needed, and how the policy and local practice treat it. A tree claim involving roofing, framing, drywall, paint and electrical presents a stronger case than a single-trade fence repair.</p>
<h3>Steep, high and access charges</h3>
<p>Steep charges are commonly applied on slopes of about 7/12 and steeper, and high-roof charges on roofs two or more stories up. Umpires weigh measured pitch, photos showing roof height and access limits such as tight lots or elevated coastal homes.</p>
<h3>Code upgrades</h3>
<p>If the local building department requires work beyond like-kind repair, the umpire looks for the code section, the permit requirements and the ordinance or law limit in the policy. Whether the item is covered at all may be a coverage question; the umpire’s job is the cost.</p>

<h2>An illustrative decision</h2>
<p>Here is an example with illustrative figures only. On a Columbia bungalow with wind damage, two appraisers agree on 42 of 50 line items. Eight remain, worth $18,400 in total under one appraiser’s estimate and $6,900 under the other’s.</p>
<div class="table-wrap"><table>
<thead><tr><th>Disputed item</th><th>Appraiser A</th><th>Appraiser B</th><th>Umpire</th></tr></thead>
<tbody>
<tr><td>Roof replacement, rear slope</td><td>$5,200</td><td>$1,100 (repair)</td><td>$5,200</td></tr>
<tr><td>Steep charge</td><td>$900</td><td>$0</td><td>$900</td></tr>
<tr><td>Matching siding, north wall</td><td>$4,300</td><td>$1,600</td><td>$2,700</td></tr>
<tr><td>Overhead and profit</td><td>$4,100</td><td>$2,400</td><td>$3,300</td></tr>
<tr><td>Four other items</td><td>$3,900</td><td>$1,800</td><td>$2,500</td></tr>
</tbody>
</table></div>
<p>The umpire sided fully with one appraiser on the roof slope and steep charge because measurements and photos supported them, and chose middle values where the evidence was mixed. The umpire then signed with whichever appraiser agreed to the final figures. Real outcomes depend entirely on the evidence and policy.</p>
<p>Once two panel members sign, the award sets the amount of loss. The insurer then applies the deductible and prior payments, and any recoverable depreciation is usually released after repairs are finished. If one side believes the umpire strayed into coverage questions or decided items outside the dispute, that challenge is a legal matter for a South Carolina attorney rather than another round of appraisal.</p>
<div class="note"><b class="h">The umpire isn’t a tiebreaker on everything</b>An umpire picks a supported value for each item. That value may match one side, the other, or fall in between. Splitting every difference down the middle is not the goal, and a strong record on one item doesn’t carry over to a weak one.</div>

<h2>How to present a disputed item well</h2>
<p>Your appraiser prepares the presentation, but owners can help by supplying the raw material early. The most persuasive submissions share a few traits:</p>
<ul>
<li>One page per item, stating the dispute, the value proposed and the reason.</li>
<li>Photos labeled by location and date, not a folder of unlabeled images.</li>
<li>Measurements or reports that tie directly to the quantity claimed.</li>
<li>Pricing support from local South Carolina sources, not national averages.</li>
<li>Policy wording quoted where it matters, such as matching or loss settlement language.</li>
</ul>
<p>If you are an appraiser or a party looking for a neutral, our <a href="/claim-dispute-services/umpire-neutral-appraiser/">umpire and neutral appraiser</a> page explains how we take on umpire roles. For the full sequence from demand to award, see <a href="/appraisal-process-explained/">the appraisal process explained</a>.</p>
""",
    },
]
