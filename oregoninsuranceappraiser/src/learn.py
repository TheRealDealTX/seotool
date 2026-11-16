"""Process guide, grouped FAQ, glossary and guide articles for Oregon Insurance Appraiser."""

TB = "/oregon-claim-calculators/"
SB = "/property-appraisals/"

PROCESS_STEPS = [
    ("A disagreement on the number", "The insurer accepts the claim but its estimate is lower than yours. You have asked for a re-inspection or sent a supplement, and the gap remains."),
    ("The written demand", "Either side sends a written demand for appraisal that identifies the claim, the disagreement and the clause being invoked."),
    ("Each side names an appraiser", "Within the time the policy sets, often 20 days, each side names a competent, disinterested appraiser and tells the other."),
    ("The appraisers pick an umpire", "The two appraisers agree on a neutral umpire. If they can’t, the policy usually lets either side ask a court to appoint one."),
    ("Inspection and estimates", "Your appraiser inspects, measures and writes an independent, line-item estimate. The other appraiser does the same."),
    ("Working the differences", "The appraisers compare estimates item by item and agree what they can. Most of the gap usually closes here."),
    ("Umpire review", "Items still open go to the umpire, who reviews both appraisers’ support and decides each one."),
    ("The signed award", "An award signed by any two of the three sets the amount of loss. The insurer then pays under the policy’s terms."),
]

PROCESS_BODY = f"""
<h2>Before anyone demands appraisal</h2>
<p>Appraisal is a tool for one kind of disagreement: the insurer agrees the loss is covered, but you disagree on what it costs. Before you invoke it, make sure you have the insurer’s full line-item estimate, your own itemized estimate, dated photos and a copy of your policy, including the declarations page. Run our <a href="{TB}appraisal-readiness-checkup/">appraisal readiness checkup</a> to see what’s missing.</p>
<div class="note"><b class="h">Where the clause comes from</b>Most Oregon property policies contain an appraisal clause in their conditions section. Oregon’s insurance code (ORS chapter 742) also sets standard fire-policy provisions that include an appraisal process. Your policy’s wording controls the details, so read it first.</div>
<h2>Stage 1: A disagreement on the number</h2>
<p>Ask for a re-inspection, send a documented supplement and get the insurer’s position in writing. Many disputes close here. If the gap is still meaningful, use the <a href="{TB}appraisal-payoff-estimator/">appraisal payoff estimator</a> to see whether appraisal is likely to be worth the cost.</p>
<h2>Stage 2: The written demand</h2>
<p>The demand should be in writing, name the claim number and the date of loss, state that you disagree with the amount of loss, and invoke the appraisal provision. Keep proof of when it was sent and received.</p>
<h2>Stage 3: Each side names an appraiser</h2>
<p>Most clauses require each side to name a “competent and disinterested” appraiser within a set number of days, often 20. Disinterested generally means no financial stake in the outcome beyond a fee, so your contractor is usually a poor choice. Put the deadline on your calendar with the <a href="{TB}claim-calendar-builder/">claim calendar builder</a>.</p>
<h2>Stage 4: The appraisers pick an umpire</h2>
<p>The two appraisers exchange names and agree on a neutral umpire. If they can’t agree within the time the policy allows, either side can usually ask a court to appoint one. Umpire fees are commonly split equally.</p>
<h2>Stage 5: Inspection and estimates</h2>
<p>Your appraiser inspects the property, measures it and writes an independent estimate. The insurer’s appraiser does the same. Good estimates tie every line to a photo, a measurement or a pricing source.</p>
<h2>Stage 6: Working the differences</h2>
<p>The appraisers meet, compare estimates and agree what they can, item by item. This is where most of the gap usually closes. If they agree on everything, they sign an award together and the umpire isn’t needed.</p>
<h2>Stage 7: Umpire review</h2>
<p>Open items go to the umpire, who reviews both appraisers’ support, may inspect the property, and decides each item.</p>
<h2>Stage 8: The signed award</h2>
<p>An award signed by any two of the three sets the amount of loss. A clear award shows replacement cost, actual cash value and depreciation by coverage. The insurer then pays under the policy, applying the deductible, limits and any holdback.</p>
<h2>What appraisal won’t decide</h2>
<ul><li>Whether a loss is covered or excluded</li><li>Claim-handling conduct or unfair claim practices</li><li>Attorney fees or penalties</li></ul>
<p>Those questions belong with the Oregon Division of Financial Regulation, which accepts consumer complaints, or with an Oregon attorney. Oregon’s unfair claim settlement practices statute (ORS 746.230) lists conduct insurers must avoid, and ORS 742.061 can allow a policyholder to recover attorney fees in some lawsuits. Ask an attorney how those rules apply to you.</p>
"""

FAQ = [
    ("Appraisal basics", [
        ("What is insurance appraisal?", "A process in most property policies for settling disagreements about the amount of a covered loss. Each side names an appraiser, the appraisers choose an umpire, and an agreement signed by two of the three sets the amount."),
        ("Is appraisal the same as arbitration?", "Not exactly. Appraisal is limited to the amount of loss and is usually less formal. It doesn’t decide coverage or legal claims."),
        ("Can I demand appraisal if my claim was denied?", "Appraisal is designed for disputes about the amount of a covered loss. If the claim was denied outright, you will generally need to resolve coverage first, usually with an attorney."),
        ("Does my Oregon policy have an appraisal clause?", "Most homeowner and commercial property policies do. Look in the conditions section for a paragraph titled “Appraisal.” Oregon’s standard fire-policy provisions also include an appraisal process."),
    ]),
    ("Costs and fees", [
        ("Who pays for appraisal?", "Each side usually pays its own appraiser, and the umpire’s fee is usually split equally. Check your policy’s wording."),
        ("How do appraisers charge?", "Flat fees, hourly rates or a percentage of the increase are all common. We put our fee in writing before any work starts."),
        ("Is the first conversation free?", "Yes. We will look at what you have and tell you honestly whether appraisal is likely to help."),
    ]),
    ("Timing and deadlines", [
        ("How long does appraisal take?", "Simple residential claims often finish within two to three months of both appraisers being named. Large or complex claims take longer."),
        ("Is there a deadline to demand appraisal?", "Some policies set one; many don’t. But the policy’s deadline to file a lawsuit, commonly two years from the loss in Oregon, keeps running. Talk to an attorney if it is near."),
        ("Do I have to name my appraiser quickly?", "Many clauses give each side about 20 days after a written demand to name an appraiser. Check yours."),
    ]),
    ("Oregon rules and resources", [
        ("Who regulates insurers in Oregon?", "The Division of Financial Regulation, part of the Oregon Department of Consumer and Business Services. It licenses insurers, agents and public adjusters and accepts consumer complaints."),
        ("Can I file a complaint and use appraisal?", "Yes. A complaint with the Division of Financial Regulation addresses claim handling; appraisal addresses the amount of loss. They can run side by side."),
        ("What is the Oregon FAIR Plan?", "The Oregon FAIR Plan Association offers basic property coverage to owners who can’t find it in the regular market. Its policies have their own terms, including appraisal provisions."),
        ("Does Oregon have special wildfire rules?", "After the 2020 Labor Day fires, Oregon adopted additional protections for wildfire policyholders in some situations, such as more time to collect replacement cost after a total loss in a declared emergency. Confirm current rules with the Division of Financial Regulation."),
        ("Is earthquake damage covered?", "Not by a standard homeowner policy. Earthquake coverage is usually an endorsement or separate policy with a percentage deductible."),
    ]),
    ("Working with us", [
        ("Are you a public adjuster or a law firm?", "Neither. We provide appraisal, estimating and umpire services. We don’t negotiate claims outside appraisal and don’t give legal advice."),
        ("Do you work outside the Portland area?", "Yes. We work statewide across all 36 counties."),
        ("What should I send for a first review?", "The insurer’s estimate, your contractor’s estimate, photos, the declarations page and any letters from the insurer."),
    ]),
]

GLOSSARY = [
    ("Actual cash value (ACV)", "Replacement cost minus depreciation. The first payment under most replacement cost policies."),
    ("Additional living expense (ALE)", "Coverage for extra costs of living elsewhere while a home is repaired, such as rent and meals above normal."),
    ("Amount of loss", "The dollar value of the damage. The only question an appraisal panel decides."),
    ("Appraisal clause", "The policy condition that lets either side demand appraisal when they disagree on the amount of loss."),
    ("Appraisal award", "The written decision signed by two of the three panel members that sets the amount of loss."),
    ("Atmospheric river", "A long band of moisture that brings heavy rain and sometimes strong wind to the Pacific Northwest."),
    ("Coinsurance", "A commercial policy condition that can reduce payment if the property was insured for less than a required percentage of its value."),
    ("Contents (Coverage C)", "Coverage for personal belongings."),
    ("Declarations page", "The summary page of a policy listing limits, deductibles, coverages and the policy period."),
    ("Deductible", "The part of a covered loss the policyholder pays before the insurer pays."),
    ("Depreciation", "The reduction in value for age and condition. Often recoverable after repairs under replacement cost policies."),
    ("Disinterested appraiser", "An appraiser without a financial stake in the outcome beyond a fee, as most appraisal clauses require."),
    ("Division of Financial Regulation (DFR)", "The Oregon agency, within the Department of Consumer and Business Services, that regulates insurance and handles consumer complaints."),
    ("Dwelling (Coverage A)", "Coverage for the house itself and attached structures."),
    ("Earthquake endorsement", "Optional coverage added to a property policy for earthquake damage, usually with a percentage deductible."),
    ("Estimate", "An itemized list of repair work with quantities and prices."),
    ("Extended replacement cost", "An endorsement that pays above the dwelling limit, often by 20% to 50%, if rebuilding costs more than expected."),
    ("FAIR Plan", "A state-established insurer of last resort. In Oregon, the Oregon FAIR Plan Association."),
    ("Holdback", "Recoverable depreciation withheld until repairs are complete."),
    ("Line item", "A single entry in an estimate, such as a quantity of shingles or square feet of drywall."),
    ("Matching", "Whether new materials can reasonably match undamaged ones in color, texture and style."),
    ("Mitigation", "Steps taken to prevent further damage after a loss, such as tarping or water extraction."),
    ("Ordinance or law coverage", "Coverage for added costs of meeting building codes when repairing or rebuilding."),
    ("Other structures (Coverage B)", "Coverage for detached structures such as garages, fences and sheds."),
    ("Overhead and profit (O&amp;P)", "A general contractor’s charge for coordinating a multi-trade repair, commonly 10% plus 10%."),
    ("Percentage deductible", "A deductible calculated as a percentage of the dwelling limit rather than a flat dollar amount."),
    ("Pitch", "The steepness of a roof, written as inches of rise per 12 inches of run."),
    ("Policy limit", "The maximum the insurer will pay under a coverage."),
    ("Proof of loss", "A sworn statement of the amount claimed, often required within a set time after the insurer requests it."),
    ("Public adjuster", "A licensed professional who represents policyholders in handling and negotiating a claim for a fee."),
    ("Recoverable depreciation", "Depreciation paid once repairs or replacement are completed."),
    ("Replacement cost value (RCV)", "The cost to repair or replace damaged property with materials of like kind and quality, without deducting depreciation."),
    ("Reservation of rights", "A letter in which the insurer says it is handling the claim while reserving the right to deny coverage later."),
    ("Scope of loss", "The description of what is damaged and what work is needed to repair it."),
    ("Smoke infiltration", "Smoke and soot entering a structure from a nearby fire, including wildfire."),
    ("Square", "100 square feet of roof surface."),
    ("Steep charge", "An added labor charge for working on steep roofs, usually 7/12 pitch and above."),
    ("Subrogation", "The insurer’s right to recover what it paid from a third party who caused the loss."),
    ("Suit limitation", "The policy’s deadline to file a lawsuit, commonly two years from the loss in Oregon."),
    ("Supplement", "A request for additional payment for items missed or underpriced in the original estimate."),
    ("Umpire", "The neutral third member of an appraisal panel who decides items the appraisers can’t agree on."),
    ("Unfair claim settlement practices", "Insurer conduct prohibited by statute; in Oregon, listed in ORS 746.230."),
    ("Wildland-urban interface (WUI)", "Areas where homes meet or mix with undeveloped wildland vegetation and face higher wildfire risk."),
    ("Xactimate", "Widely used estimating software for property insurance claims."),
]

POSTS = [
    {
        "slug": "oregon-appraisal-clause-basics",
        "title": "Oregon’s Appraisal Clause: What It Says and How It Works",
        "seo": "Oregon Appraisal Clause: What It Says and How It Works",
        "desc": "Oregon appraisal clause guide: what the policy language says, how ORS 742 fire-policy provisions fit in, and what a panel can and can’t decide.",
        "summary": "A plain-language walk through the appraisal clause in Oregon property policies: the demand, the panel, the umpire and the award.",
        "date": "2026-10-20", "read": "7 min",
        "body": f"""
<h2>The short version</h2>
<p>If you and your insurer agree that a loss is covered but can’t agree on the amount, either of you can usually demand appraisal. Each side names an appraiser, the appraisers pick an umpire, and an agreement signed by any two of the three sets the amount of loss.</p>
<h2>Where the clause lives</h2>
<p>In most Oregon homeowner and commercial policies, the appraisal clause sits in the “Conditions” section, near clauses about duties after loss, suit against the insurer and loss payment. Oregon’s insurance code (ORS chapter 742) also sets standard fire-policy provisions that include an appraisal process. Policies may use different words, so your own form controls the details.</p>
<h2>Reading it phrase by phrase</h2>
<h3>“If you and we fail to agree on the amount of loss”</h3>
<p>This is the trigger. The disagreement has to be about value or scope, not coverage. If the insurer has denied the claim, appraisal generally isn’t the first step.</p>
<h3>“Either may demand appraisal in writing”</h3>
<p>Either you or the insurer can start the process. The demand should be in writing and identify the claim and the disagreement.</p>
<h3>“Each party will choose a competent and disinterested appraiser”</h3>
<p>Many clauses set a time to do this, commonly 20 days. “Disinterested” generally means no stake in the outcome beyond a fee, which is why a contractor who wants the job is a risky choice.</p>
<h3>“The two appraisers will choose an umpire”</h3>
<p>If they can’t agree, most clauses let either side ask a court to appoint one.</p>
<h3>“A decision agreed to by any two will be binding”</h3>
<p>This is what gives appraisal its force. Two signatures set the amount of loss.</p>
<h3>“Each party will pay its own appraiser”</h3>
<p>And usually half the umpire’s fee and other shared costs.</p>
<h2>What the panel can’t decide</h2>
<p>Appraisal doesn’t decide coverage, exclusions, claim-handling conduct, penalties or attorney fees. Oregon’s unfair claim settlement practices statute (ORS 746.230) and the attorney fee statute (ORS 742.061) are matters for the Division of Financial Regulation or the courts, not an appraisal panel.</p>
<div class="note"><b class="h">Not legal advice</b>This guide describes how appraisal commonly works. Read your own policy, and talk to an Oregon attorney about legal questions or approaching deadlines.</div>
<h2>Next steps</h2>
<p>Check whether your file is ready with the <a href="{TB}appraisal-readiness-checkup/">readiness checkup</a>, then read the full <a href="/oregon-appraisal-roadmap/">appraisal process guide</a>.</p>
""",
    },
    {
        "slug": "documenting-a-wildfire-total-loss",
        "title": "Documenting a Wildfire Total Loss in Oregon",
        "seo": "How to Document a Wildfire Total Loss in Oregon",
        "desc": "How to document a wildfire total loss in Oregon: rebuild estimates, debris removal, contents inventories, living costs and key deadlines.",
        "summary": "What Oregon wildfire survivors can do to document the dwelling, contents and living expenses after a total loss, and where claims are often disputed.",
        "date": "2026-10-06", "read": "8 min",
        "body": f"""
<h2>Start with the policy</h2>
<p>Get a complete copy of your policy, including the declarations page and all endorsements. Note your dwelling, other structures, contents and living-expense limits, and whether you have extended replacement cost or ordinance-or-law coverage. Those limits shape everything that follows.</p>
<h2>The dwelling</h2>
<ul><li><strong>Get a real rebuild estimate.</strong> After a regional fire, construction costs rise. Estimates based on normal pricing or a per-square-foot shortcut often fall short.</li>
<li><strong>Gather what the house was.</strong> Old photos, real estate listings, permits, plans and appraisals help show size, finishes and features.</li>
<li><strong>Include site work.</strong> Debris and ash removal, hazardous materials, foundation evaluation, utility reconnection, retaining walls and driveways.</li>
<li><strong>Ask about code upgrades.</strong> Rebuilding under current codes can add cost that ordinance-or-law coverage may pay.</li></ul>
<h2>Contents</h2>
<p>A total-loss inventory is the hardest part of most wildfire claims. Work room by room, and use photos and videos from phones and social media, bank and card statements, and online order histories. List brand, age and quantity where you can. Our <a href="{TB}wildfire-contents-estimator/">wildfire contents estimator</a> gives an early sense of scale.</p>
<p>After 2020, Oregon adopted additional protections for wildfire policyholders in some situations, which may affect how detailed an inventory must be or how much time you have. Check the current rules with the Division of Financial Regulation.</p>
<h2>Living expenses</h2>
<p>Keep receipts for rent, mileage, meals above normal and other added costs. Rebuilds after wildfires often take much longer than first projected, and living-expense disputes are common.</p>
<h2>Where disputes arise</h2>
<ul><li>Rebuild pricing that doesn’t reflect post-disaster costs</li><li>Depreciation on contents</li><li>Debris removal limits</li><li>Smoke damage to surviving structures</li><li>How long living expenses continue</li></ul>
<p>When the insurer accepts the loss but undervalues it, appraisal can resolve the amount. See our <a href="{SB}wildfire-loss-appraisal/">wildfire loss appraisal</a> page.</p>
<div class="note"><b class="h">Deadlines</b>Track proof-of-loss, depreciation recovery and suit deadlines with the <a href="{TB}claim-calendar-builder/">claim calendar builder</a>, and confirm wildfire-specific timelines with an attorney.</div>
""",
    },
    {
        "slug": "after-an-ice-storm-claim-checklist",
        "title": "After an Oregon Ice Storm: A Claim Checklist",
        "seo": "Oregon Ice Storm Insurance Claim Checklist",
        "desc": "Oregon ice storm claim checklist: photographing fallen limbs, tree removal, frozen pipes, power-outage losses and what estimates often miss.",
        "summary": "Practical steps after a Willamette Valley ice storm, from photographing fallen limbs to documenting burst pipes and outage losses.",
        "date": "2026-09-22", "read": "6 min",
        "body": f"""
<h2>Why ice storm claims are tricky</h2>
<p>The February 2021 and January 2024 ice storms brought down trees and power lines across the Portland and Salem areas. Claims that followed combined roof damage, tree removal, burst pipes, spoiled food and long stays away from home. Each piece has its own coverage rules.</p>
<h2>Right after the storm</h2>
<ol><li><strong>Stay safe.</strong> Stay away from downed lines and don’t climb onto icy roofs.</li>
<li><strong>Photograph before anything moves.</strong> Limbs on the roof, impact points, the tree’s base and any visible rot.</li>
<li><strong>Prevent further damage.</strong> Tarp openings and shut off water if pipes freeze or burst. Keep every receipt.</li>
<li><strong>Report the claim promptly.</strong></li></ol>
<h2>What estimates often miss</h2>
<ul><li>Cracked rafters, broken trusses and damaged roof decking under a fallen limb</li>
<li>Gutters, fascia and soffits pulled down by ice weight</li>
<li>Water damage from ice dams and rain that entered before tarping</li>
<li>Drying, demolition and rebuilding after a burst pipe, not just the plumbing repair</li>
<li>Crane and emergency removal costs for large trees</li></ul>
<h2>Outage losses</h2>
<p>Some policies limit coverage for damage caused by an off-premises power failure. Food spoilage coverage, if any, may be capped. Read the wording before assuming these are covered.</p>
<h2>Trees and limits</h2>
<p>Many policies pay a limited amount to remove a tree that damaged a covered structure. Trees that fall without hitting anything are often not covered. See our <a href="{SB}fallen-tree-appraisal/">fallen tree damage appraisal</a> and <a href="{SB}ice-storm-snow-appraisal/">ice storm appraisal</a> pages.</p>
""",
    },
    {
        "slug": "earthquake-coverage-and-appraisal",
        "title": "Earthquake Coverage, Deductibles and Appraisal in Oregon",
        "seo": "Oregon Earthquake Coverage, Deductibles and Appraisal",
        "desc": "Oregon earthquake coverage explained: why standard policies exclude it, how percentage deductibles work and when appraisal can help.",
        "summary": "Why most Oregon homeowner policies exclude earthquake, how endorsement deductibles work, and how appraisal fits if a quake claim is underpaid.",
        "date": "2026-09-08", "read": "6 min",
        "body": f"""
<h2>The Cascadia question</h2>
<p>Oregon sits near the Cascadia Subduction Zone, capable of a very large earthquake, and crustal faults also run under parts of the state. Yet most Oregon homeowners don’t carry earthquake coverage, because standard homeowner policies exclude it.</p>
<h2>How earthquake coverage is added</h2>
<p>Earthquake coverage is usually added by endorsement or bought as a separate policy. It typically has:</p>
<ul><li><strong>A percentage deductible</strong>, often 10% or more of the dwelling limit</li>
<li><strong>Separate limits or deductibles</strong> for contents and other structures in some forms</li>
<li><strong>Exclusions</strong> for things like masonry veneer, unless added back</li></ul>
<p>Use our <a href="{TB}percentage-deductible-checker/">percentage deductible checker</a> to see your deductible in dollars.</p>
<h2>Fire following earthquake</h2>
<p>Many policies that exclude earthquake still cover fire that follows an earthquake. After a major quake, that distinction can be very large.</p>
<h2>Where appraisal fits</h2>
<p>If you have earthquake coverage and the insurer accepts the claim but disputes the amount, appraisal can resolve the value. Disputes about whether damage was caused by the earthquake or by settling, age or construction are often coverage questions.</p>
<div class="note"><b class="h">Plan ahead</b>Photograph your home inside and out now. Pre-loss photos are the best evidence of condition if you ever need to make an earthquake claim.</div>
""",
    },
    {
        "slug": "reading-an-insurance-estimate",
        "title": "How to Read the Insurer’s Estimate, Line by Line",
        "seo": "How to Read an Insurance Estimate, Line by Line",
        "desc": "How to read an insurance estimate line by line: summary page, quantities, depreciation, overhead and profit, and the items most often left out.",
        "summary": "A guided tour of a typical property claim estimate: the summary, line items, depreciation, O&P and what to look for when something seems missing.",
        "date": "2026-08-25", "read": "7 min",
        "body": f"""
<h2>Start with the summary page</h2>
<p>The summary shows replacement cost (RCV), depreciation, actual cash value (ACV), deductible and net payment, usually by coverage. Check that the deductible matches your declarations page and that depreciation is marked recoverable if you have replacement cost coverage.</p>
<h2>Then the line items</h2>
<p>Each line has a description, quantity, unit, unit price and total. Look at:</p>
<ul><li><strong>Quantities.</strong> Do roof squares, wall areas and flooring match the real dimensions? Use our <a href="{TB}roof-pitch-squares-converter/">roof pitch and squares converter</a> for roofs.</li>
<li><strong>Remove and replace.</strong> Is there a line to tear out and dispose of damaged material, not just install new?</li>
<li><strong>Prep and protection.</strong> Masking, floor protection, content manipulation and cleanup.</li>
<li><strong>Trades.</strong> Is every trade needed listed, such as electrician, plumber and painter?</li></ul>
<h2>Depreciation</h2>
<p>Look for how depreciation was calculated, whether labor was depreciated, and whether any items were treated as non-recoverable. The <a href="{TB}depreciation-holdback-tracker/">depreciation and holdback tracker</a> shows the effect.</p>
<h2>Overhead and profit</h2>
<p>When a repair needs several trades coordinated by a general contractor, estimates often include overhead and profit. If yours doesn’t, ask why.</p>
<h2>Commonly missing items</h2>
<ul><li>Matching of adjacent finishes</li><li>Code-required items</li><li>Steep and high roof charges</li><li>Minimum charges for small trades</li><li>Permits and dumpsters</li></ul>
<p>If you find a meaningful gap, a <a href="{SB}carrier-estimate-review/">professional estimate review</a> can confirm it before you supplement or demand appraisal.</p>
""",
    },
    {
        "slug": "appraisal-dfr-complaint-or-attorney",
        "title": "Appraisal, a DFR Complaint or an Attorney: Choosing a Path",
        "seo": "Appraisal, DFR Complaint or Attorney? Picking a Path",
        "desc": "Appraisal, a complaint to Oregon’s Division of Financial Regulation or an attorney? How to choose the right path for an underpaid claim.",
        "summary": "Three different tools for three different problems. How to decide whether your Oregon claim needs appraisal, a regulator complaint or legal help.",
        "date": "2026-08-11", "read": "6 min",
        "body": f"""
<h2>Match the tool to the problem</h2>
<p>An underpaid claim can stem from different problems. Picking the right path first saves time and money.</p>
<h2>Appraisal: the amount is wrong</h2>
<p>Use appraisal when the insurer accepts coverage but you disagree on the cost to repair or replace. It is focused, usually faster than litigation, and ends in a binding amount. It doesn’t decide coverage or conduct.</p>
<h2>A DFR complaint: the handling is wrong</h2>
<p>The Oregon Division of Financial Regulation accepts consumer complaints about insurers, such as unexplained delays, unanswered communications or claim handling that seems unfair. Oregon’s unfair claim settlement practices statute (ORS 746.230) lists conduct insurers must avoid. A complaint can prompt a response from the insurer, but the Division doesn’t act as your lawyer or set the value of your claim.</p>
<h2>An attorney: the claim was denied or the stakes are legal</h2>
<p>Talk to an Oregon attorney when the claim is denied, coverage is disputed, a deadline to sue is approaching, or you believe the insurer acted in bad faith. Oregon law can allow a policyholder to recover attorney fees in some lawsuits (ORS 742.061), and an attorney can explain whether that applies.</p>
<h2>Using more than one</h2>
<p>These paths aren’t exclusive. Many policyholders file a complaint about handling while using appraisal to settle the amount, or consult an attorney before demanding appraisal to protect deadlines.</p>
<div class="note"><b class="h">We’ll tell you</b>If your situation calls for a complaint or an attorney rather than appraisal, we will say so on the first call.</div>
""",
    },
]
