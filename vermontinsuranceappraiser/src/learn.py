"""Process guide, FAQ, glossary and field guides."""

PROCESS_STEPS = [
    ("Pin down the disagreement", "Appraisal is for one kind of dispute: the carrier accepts that the loss is covered but you disagree on how much it costs. Get the carrier’s full estimate and any letters explaining its position. Compare it with your contractor’s estimate so you know exactly where the numbers differ."),
    ("Read the appraisal condition", "Find the Appraisal paragraph in the conditions section of your policy. Note who can demand appraisal, how the demand must be made, the time to name an appraiser (often 20 days) and how the umpire is chosen. Look for any endorsement that changes the standard wording."),
    ("Send a written demand", "Either side can usually invoke appraisal in writing. A clear demand identifies the claim, states that you disagree on the amount of loss, invokes the appraisal provision and names your appraiser or says you will within the policy deadline. Keep proof of delivery."),
    ("Each side names an appraiser", "You choose a competent and impartial appraiser, and so does the carrier. Each side pays its own. Your appraiser inspects the property, builds an independent estimate and gathers the photos and measurements to support it."),
    ("The appraisers select an umpire", "The two appraisers try to agree on a neutral umpire, often within 15 days. If they cannot, either side may usually ask a court in the county where the property is located to appoint one. The umpire’s fee is normally split."),
    ("The appraisers work the differences", "The appraisers compare estimates line by line. Most items are resolved here, sometimes on site. Anything they agree on is set; only disputed items move on."),
    ("The umpire decides what is left", "The umpire reviews the remaining items, sometimes with an inspection and written submissions from each appraiser, then joins one appraiser or the other on each item."),
    ("The award is signed and paid", "An award signed by any two of the three sets the amount of loss. The carrier then pays according to the policy: the award, less the deductible, prior payments and any depreciation not yet recoverable."),
]

PROCESS_BODY = """
<p>The appraisal condition in most Vermont property policies follows a familiar pattern, but the details vary. Use this guide to understand the steps, then read your own policy’s wording, which controls.</p>
<div class="callout"><b>Before you start.</b> Appraisal decides the amount of loss. It is not designed to settle coverage disputes, claims of delay or bad faith. Vermont’s insurance trade practices law (Title 8) lists unfair claim settlement practices, and Vermont courts have recognized bad-faith claims against insurers in some circumstances. Those are questions for the Department of Financial Regulation or a Vermont attorney.</div>
""" + "".join(f'<h2 id="step-{i + 1}">Step {i + 1}: {t}</h2><p>{p}</p>' for i, (t, p) in enumerate(PROCESS_STEPS)) + """
<h2>How long it takes</h2>
<p>A straightforward residential appraisal often resolves in one to three months after the demand. Larger or more technical claims, winter access problems and umpire scheduling can stretch that. Preparing your file before the demand is the best way to keep it moving.</p>
<h2>What it costs</h2>
<p>Each side pays its own appraiser and usually half of the umpire. Fee arrangements include flat fees, hourly rates and, sometimes, a percentage of the increase. Our <a href="/vermont-claim-tools/claim-gap-fee-estimator/">claim gap &amp; fee estimator</a> shows how fees affect your net result. Example figures on this site are illustrative.</p>
<h2>Where claims go wrong</h2>
<ul>
<li>Demanding appraisal before getting a complete, itemized estimate of your own.</li>
<li>Letting the deadline to name an appraiser pass.</li>
<li>Mixing excluded flood damage into a homeowners appraisal.</li>
<li>Choosing an appraiser who cannot meet the policy’s impartiality standard.</li>
<li>Forgetting that the suit-limitation clock may keep running during appraisal.</li>
</ul>
"""

FAQ = [
    ("The basics", [
        ("What is insurance appraisal?", "A process written into most property policies for resolving disagreements over the amount of a covered loss. Each side names an appraiser, the appraisers choose an umpire, and an award signed by two of the three sets the amount."),
        ("Who can demand appraisal?", "Most policies let either you or the insurer demand appraisal in writing. Some policies add conditions, so read the wording."),
        ("Is appraisal the same as arbitration?", "They are related but not identical. Appraisal is usually limited to the amount of loss, while arbitration can address broader issues. Vermont courts look at the policy language."),
        ("Does appraisal decide coverage?", "Generally no. If the carrier denies that the loss is covered at all, that is a coverage dispute, usually handled through a complaint to the Department of Financial Regulation or with an attorney."),
    ]),
    ("Costs and timing", [
        ("How much does appraisal cost?", "Each side pays its own appraiser and usually half the umpire. Costs depend on the size and complexity of the claim. We quote fees in writing before starting."),
        ("How long does it take?", "Many residential appraisals finish within one to three months of the demand. Larger claims and scheduling can take longer."),
        ("Is there a deadline to demand appraisal?", "Some policies set a time limit, and the suit-limitation clause can also affect timing. Check your policy and talk to a professional if dates are close."),
        ("What if the gap is small?", "If the difference is small, appraisal fees may eat the recovery. A documented supplement request to the carrier is often a better first step."),
    ]),
    ("Vermont specifics", [
        ("Who regulates insurance in Vermont?", "The Vermont Department of Financial Regulation, through its Insurance Division. It licenses insurers, agents and public adjusters and handles consumer complaints."),
        ("Does Vermont have a FAIR plan or wind pool?", "Vermont does not operate a coastal wind pool. Hard-to-place risks are often written by surplus lines carriers. Check with the Department of Financial Regulation for current options."),
        ("Is flood covered by a homeowners policy?", "Usually not. Flood from rising water is generally excluded and covered under a separate flood policy, such as the National Flood Insurance Program."),
        ("Are ice dams covered?", "Many policies cover sudden interior water damage caused by ice dams. Some limit roof repairs or ice removal. Read the water, roof and freezing wording together."),
        ("What about bad faith?", "Vermont recognizes claims against insurers for bad-faith handling in some circumstances, and Title 8 lists unfair claim settlement practices. We do not give legal advice; consult a Vermont attorney."),
    ]),
    ("Working with us", [
        ("Are you a public adjuster?", "No. We work as appraisers, estimators and umpires. A public adjuster handles the whole claim; we focus on the amount of loss."),
        ("Are you lawyers?", "No. We do not give legal advice. When a claim needs a lawyer, we say so."),
        ("Do you work outside the big towns?", "Yes. We work in all 14 Vermont counties, including the Northeast Kingdom and rural southern Vermont."),
        ("Can you guarantee a result?", "No honest appraiser can. We can promise a thorough, defensible valuation and a candid opinion about whether appraisal makes sense."),
    ]),
]

GLOSSARY = [
    ("Actual cash value (ACV)", "The value of damaged property at the time of loss, usually replacement cost minus depreciation. Some policies pay only ACV."),
    ("Additional living expense (ALE)", "Coverage for extra costs of living elsewhere while a home is repaired, often called Coverage D or loss of use."),
    ("Amount of loss", "The dollar value of the damage. Appraisal is designed to decide this, not coverage."),
    ("Appraisal clause", "The policy condition that lets either party demand appraisal when they disagree on the amount of loss."),
    ("Appraisal award", "The written decision signed by two of the three panel members that sets the amount of loss."),
    ("Appraiser", "A person each side names to value the loss. Policies usually require a competent and impartial appraiser."),
    ("Collapse", "An additional coverage in many policies. Some define it narrowly as an abrupt falling down."),
    ("Coverage A", "Dwelling coverage for the house itself and attached structures."),
    ("Coverage B", "Other structures coverage for detached garages, barns, sheds and fences."),
    ("Coverage C", "Personal property, or contents, coverage."),
    ("Declarations page", "The summary page of a policy listing limits, deductibles, the insured property and endorsements."),
    ("Deductible", "The part of a covered loss you pay before the policy pays."),
    ("Depreciation", "A reduction in value for age, wear and obsolescence used to calculate ACV."),
    ("Endorsement", "A form that adds to, removes or changes coverage in the base policy."),
    ("Exclusion", "Policy language removing certain causes or types of damage from coverage, such as flood."),
    ("Flood", "Generally, rising surface water from rivers, rain or melting snow. Usually excluded from homeowners policies and covered by separate flood insurance."),
    ("Holdback", "Recoverable depreciation withheld from the first payment until repairs are completed."),
    ("Ice dam", "A ridge of ice at the eaves that traps meltwater, which can back up under roofing and leak inside."),
    ("Impartial", "Without bias toward either side. Many appraisal clauses require impartial or disinterested appraisers."),
    ("Like kind and quality", "Materials and workmanship equal to what existed before the loss."),
    ("Line item", "One entry in an estimate, such as a quantity of shingles or a coat of paint, with a unit price."),
    ("Matching", "Whether new materials must match undamaged ones so the repair is uniform. Policy wording and state rules vary."),
    ("Mitigation", "Reasonable steps after a loss to prevent further damage, such as tarping or water extraction."),
    ("NFIP", "The National Flood Insurance Program, which writes most residential flood policies through participating carriers."),
    ("Ordinance or law", "Coverage for added costs to meet building codes during repair. Often a percentage of Coverage A."),
    ("Overhead and profit (O&P)", "A general contractor’s charge for managing a job, often 10% overhead plus 10% profit."),
    ("Peril", "A cause of loss, such as fire, wind, hail or the weight of ice and snow."),
    ("Proof of loss", "A sworn statement of the amount claimed, required by many policies when the insurer requests it."),
    ("Public adjuster", "A licensed professional hired by the policyholder to prepare and negotiate the whole claim."),
    ("Recoverable depreciation", "Depreciation the insurer pays after repairs are completed under a replacement cost policy."),
    ("Replacement cost value (RCV)", "The cost to repair or replace damaged property with like kind and quality, without deducting depreciation."),
    ("Scope of loss", "The list of damaged items and the repairs needed, the foundation of any estimate."),
    ("Snow load", "The weight of snow and ice on a roof, measured in pounds per square foot."),
    ("Square", "A roofing unit equal to 100 square feet of roof surface."),
    ("Sub-limit", "A lower limit within a policy for a certain kind of property or loss, such as mold or trees."),
    ("Suit limitation", "A policy condition setting how long you have to sue the insurer. Vermont law may affect how it applies."),
    ("Supplement", "A request for additional payment for items missed or under-priced in the original estimate."),
    ("Umpire", "The neutral third panel member who decides the items the two appraisers cannot agree on."),
    ("Vacancy", "A condition in many policies that limits coverage when a building has been empty for a set period."),
    ("Xactimate", "Estimating software widely used by insurers and contractors, with regional price lists."),
]

POSTS = [
    {
        "slug": "ice-dam-claims-in-vermont", "date": "2026-10-28", "read": "7 min",
        "title": "Ice Dam Claims in Vermont: What Policies Usually Cover",
        "seo": "Ice Dam Claims in Vermont: What Is Usually Covered",
        "desc": "How ice dam claims in Vermont usually work: interior water damage, roof repairs, ice removal and what to photograph before the ice melts.",
        "summary": "Why ice dams form, what homeowners policies typically pay for, and how to document a winter leak before the evidence melts.",
        "body": """
<p>If you own an older home in Vermont, you have probably seen it: thick icicles along the eaves, a brown stain spreading across a bedroom ceiling, water dripping from a window header in February. Ice dam claims in Vermont are among the most common winter losses, and among the most misunderstood.</p>
<h2>Why ice dams form</h2>
<p>Warm air leaks from the living space into the attic and heats the underside of the roof. Snow on the upper roof melts, runs down to the colder overhang and freezes again. Over days and weeks, that ice builds into a dam. Meltwater pools behind it, works under the shingles and leaks into the attic, wall cavities and ceilings. Long winters, frequent thaws and older homes with little insulation make the problem especially common here.</p>
<h2>What policies usually cover</h2>
<ul>
<li><strong>Interior damage.</strong> Most homeowners policies cover sudden water damage to ceilings, walls, insulation and floors caused by ice dam leakage, subject to the deductible.</li>
<li><strong>The roof itself.</strong> Some policies cover roof repairs needed because of the ice dam. Others exclude damage to the roof from freezing or treat it as maintenance.</li>
<li><strong>Ice removal.</strong> Steaming or removing ice to stop further damage may be covered as a reasonable repair to protect the property, or it may be excluded. Keep receipts either way.</li>
<li><strong>Mold.</strong> If water sat for weeks before it was found, mold may be limited by a sub-limit.</li>
</ul>
<h2>What to document</h2>
<ol>
<li>Photograph the ice at the eaves and any icicles, from the ground, with a date stamp.</li>
<li>Photograph interior stains as soon as they appear and again as they spread.</li>
<li>Check the attic with a flashlight and photograph wet insulation or frost on the sheathing.</li>
<li>Keep a short written log: when you first saw water, what the weather was doing and what you did.</li>
<li>Save receipts for ice removal, tarps, fans and dehumidifiers.</li>
</ol>
<h2>Where estimates fall short</h2>
<p>Ice dam estimates often patch a ceiling stain and paint. But water usually travels farther than the stain shows. Wet insulation should usually be removed, plaster ceilings can delaminate, and wall cavities behind finished surfaces may be soaked. A thorough scope follows the water from the roof edge to wherever it stopped.</p>
<h2>Fixing the cause</h2>
<p>Insurance generally does not pay to improve attic insulation or ventilation, which is the long-term fix. But if you do not address the cause, the carrier may push back on a second claim next winter. Keep records of any improvements you make.</p>
<h2>When appraisal fits</h2>
<p>If the carrier accepts the ice dam loss but its estimate leaves out the insulation, the wall cavities or proper plaster repair, that is an amount-of-loss dispute. An <a href="/vt-claim-appraisal/insurance-estimate-review/">estimate review</a> is the usual first step.</p>
""",
    },
    {
        "slug": "flood-or-water-damage-after-a-vermont-storm", "date": "2026-10-14", "read": "8 min",
        "title": "Flood or Water Damage? Sorting Claims After a Vermont Storm",
        "seo": "Flood or Water Damage After a Vermont Storm?",
        "desc": "After a Vermont storm, flood and water damage are usually separate claims. Here is how wind, rain, sewer backup and rising water differ.",
        "summary": "The 2023 and 2024 summer floods left many owners with two claims on one building. How to tell which damage belongs to which policy.",
        "body": """
<p>Vermont learned hard lessons about water in 2011, 2023 and 2024. After Tropical Storm Irene, and again after the July floods of 2023 and the remnants of Hurricane Beryl in 2024, thousands of owners discovered that the word “water” covers several very different kinds of insurance claims.</p>
<h2>Four kinds of water</h2>
<ul>
<li><strong>Rain through a storm opening.</strong> Wind tears off shingles or a tree punctures the roof, and rain pours in. Usually covered by a homeowners or commercial policy.</li>
<li><strong>Plumbing and appliance water.</strong> A burst pipe or failed fitting. Usually covered as sudden and accidental discharge.</li>
<li><strong>Sewer or drain backup.</strong> Water pushed up through floor drains or toilets. Often covered only by an endorsement, with a separate limit.</li>
<li><strong>Flood.</strong> Rising surface water from a river, brook or overland flow. Generally excluded from homeowners policies and covered by a separate flood policy.</li>
</ul>
<h2>Why the distinction matters</h2>
<p>When a storm brings wind and floodwater together, carriers may argue over which caused what. A wall that was wet from both rising water and a roof leak can end up in a gap between two policies. Clear evidence of the high-water mark, the roof openings and the timing protects the covered part of the claim.</p>
<h2>What to document</h2>
<ol>
<li>Photograph and measure the high-water line inside and outside.</li>
<li>Photograph roof, siding and window damage separately, from outside and inside.</li>
<li>Note which rooms were wet from above and which from below.</li>
<li>Keep receipts for pumping, extraction and drying for each area.</li>
</ol>
<h2>Flood policies run on their own clock</h2>
<p>National Flood Insurance Program policies have strict proof-of-loss deadlines, usually measured from the date of loss, and their own appraisal provision for disputes over the value of covered damage. They also limit coverage in basements. Read the flood policy separately from your homeowners policy.</p>
<h2>Where appraisal fits</h2>
<p>If the carrier accepts the wind or plumbing damage but undervalues it, appraisal can address the amount. If the dispute is whether the water was flood or covered water, that is a coverage question. Our <a href="/vt-claim-appraisal/tropical-storm-claim-appraisal/">tropical storm claim appraisal</a> page explains how we handle mixed losses.</p>
""",
    },
    {
        "slug": "documenting-a-winter-claim", "date": "2026-09-30", "read": "6 min",
        "title": "Documenting a Property Claim in the Middle of a Vermont Winter",
        "seo": "Documenting a Winter Property Claim in Vermont",
        "desc": "Documenting a winter property claim in Vermont: photos before snow covers damage, heat records for freeze losses and safe roof checks.",
        "summary": "Snow hides damage and melts evidence. A practical list for photographing, recording and protecting a claim between December and March.",
        "body": """
<p>Winter makes every part of a claim harder. Snow covers roof damage, ice hides gutters, inspections get postponed and evidence melts. Here is how to document a winter property claim so it holds up months later.</p>
<h2>Photograph early and often</h2>
<ul>
<li>Take wide shots first, then close-ups, with the date visible in the file data.</li>
<li>Photograph the outside of the building from every side, even if snow covers the roof.</li>
<li>Capture ice dams and icicles before they melt or are removed.</li>
<li>Photograph interior damage as soon as it appears and again each week.</li>
</ul>
<h2>Keep heat records for freeze losses</h2>
<p>If pipes froze, the carrier will likely ask whether heat was maintained. Gather fuel delivery receipts, thermostat history from smart devices, monitoring alerts, utility bills and notes from anyone who checked the property. If the building was vacant, find out what your policy requires and whether the water was shut off and drained.</p>
<h2>Do not climb icy roofs</h2>
<p>No claim is worth a fall. Use binoculars, a camera zoom or a drone if you are comfortable, and leave roof access to professionals with proper equipment.</p>
<h2>Protect the property</h2>
<p>Make reasonable temporary repairs: shut off water, call a mitigation company, tarp openings when it is safe. Keep every receipt. Policies generally require you to protect the property from further damage.</p>
<h2>Write it down</h2>
<p>A short log helps more than people expect. Record when you discovered the damage, what the weather was, who you called and what they did. Memories fade by spring.</p>
<h2>Ask for a spring re-inspection</h2>
<p>If snow prevented a full roof inspection, ask the carrier in writing to re-inspect once the roof is clear. Damage found later can be added to the claim if it relates to the same loss.</p>
""",
    },
    {
        "slug": "reading-a-carrier-estimate", "date": "2026-09-16", "read": "8 min",
        "title": "Reading a Carrier’s Estimate Line by Line",
        "seo": "Reading an Insurance Estimate Line by Line",
        "desc": "A guide to reading an insurance estimate line by line: measurements, missing items, pricing, depreciation and overhead and profit explained.",
        "summary": "What each part of a typical claim estimate means and the five places Vermont estimates most often come up short.",
        "body": """
<p>An insurance estimate can run dozens of pages of codes and abbreviations. Reading it line by line is the most useful thing you can do before deciding whether to dispute a claim.</p>
<h2>The parts of an estimate</h2>
<ul>
<li><strong>Summary page:</strong> the totals for replacement cost, depreciation, deductible and net claim.</li>
<li><strong>Room or area sections:</strong> each room, roof slope or elevation with its own line items.</li>
<li><strong>Line items:</strong> a description, quantity, unit price, tax and depreciation for each task.</li>
<li><strong>Diagrams:</strong> sketches with measurements that drive the quantities.</li>
<li><strong>Price list:</strong> usually named on the first page, with a region and month.</li>
</ul>
<h2>Five places estimates come up short</h2>
<ol>
<li><strong>Measurements.</strong> Compare room sizes and roof squares with your own measurements.</li>
<li><strong>Missing items.</strong> Demolition, debris removal, content manipulation, protection and cleanup are often left out.</li>
<li><strong>Materials.</strong> Plaster priced as drywall, slate priced as asphalt, wide-plank priced as standard flooring.</li>
<li><strong>Depreciation.</strong> Check the rates and whether labor was depreciated.</li>
<li><strong>Overhead and profit.</strong> If the job needs several trades coordinated, a general contractor’s overhead and profit may be appropriate.</li>
</ol>
<h2>Check the price list date</h2>
<p>Price lists are updated regularly. An estimate written on an older list, or one for a different region, may not match current Vermont costs, especially after a large storm drives up demand.</p>
<h2>Make a comparison list</h2>
<p>Create a simple table: the item, the carrier’s quantity and price, your contractor’s quantity and price, and the difference. That list becomes your supplement request, or the starting point for appraisal.</p>
<p>If you would like a professional to do it, our <a href="/vt-claim-appraisal/insurance-estimate-review/">estimate review</a> produces exactly that comparison.</p>
""",
    },
    {
        "slug": "lessons-from-irene-and-the-july-floods", "date": "2026-09-02", "read": "7 min",
        "title": "What Irene and the July Floods Taught Vermont Policyholders",
        "seo": "What Irene and the July Floods Taught Vermonters",
        "desc": "Lessons from Irene and the 2023 and 2024 July floods for Vermont policyholders: coverage gaps, flood insurance and claim documentation.",
        "summary": "Three major floods in thirteen years exposed the same coverage gaps again and again. The practical lessons for owners today.",
        "body": """
<p>Tropical Storm Irene in August 2011, the July 2023 floods and the July 2024 floods from the remnants of Hurricane Beryl reshaped how many Vermonters think about property insurance. The same lessons came up after each one.</p>
<h2>Lesson 1: Flood is usually a separate policy</h2>
<p>Many owners outside mapped flood zones did not carry flood insurance and learned after the fact that their homeowners policy excluded rising water. Flood can reach properties far from mapped floodplains, especially along small mountain streams that rise quickly.</p>
<h2>Lesson 2: Check basement and sewer backup coverage</h2>
<p>Sewer and drain backup is often an optional endorsement with a modest limit. Flood policies also restrict what they cover in basements. Knowing both limits before a storm avoids surprises after it.</p>
<h2>Lesson 3: Mixed losses need careful documentation</h2>
<p>Storms that bring flooding also bring wind, falling trees and roof leaks. Owners who photographed high-water marks and roof damage separately had an easier time getting the covered parts paid.</p>
<h2>Lesson 4: Repair costs rise after a disaster</h2>
<p>After a widespread flood, contractors are booked and material costs climb. Estimates written on pre-storm pricing may not reflect what repairs actually cost months later.</p>
<h2>Lesson 5: Deadlines do not pause for disasters</h2>
<p>Proof-of-loss and suit-limitation deadlines can run while owners are still cleaning up. Federal and state agencies sometimes extend flood deadlines after declared disasters, but never assume an extension applies. Write down every deadline early.</p>
<h2>Lesson 6: Help exists</h2>
<p>The Department of Financial Regulation publishes consumer guidance after major storms and takes complaints. FEMA assistance, community groups and legal aid organizations have all helped Vermonters through recovery.</p>
""",
    },
    {
        "slug": "choosing-an-appraiser-and-umpire", "date": "2026-08-19", "read": "6 min",
        "title": "Choosing an Appraiser and an Umpire in a Small State",
        "seo": "Choosing an Appraiser and Umpire in Vermont",
        "desc": "How to choose an appraiser and umpire in Vermont: impartiality, experience, fee terms and conflicts in a state where people know each other.",
        "summary": "Vermont is small, and everyone in the claims world seems to know each other. What to ask before you name an appraiser or agree on an umpire.",
        "body": """
<p>Vermont is a small state. Contractors, adjusters and appraisers often cross paths again and again. That familiarity can help a panel work smoothly, but it also makes it important to ask the right questions before you name an appraiser or agree on an umpire.</p>
<h2>What to look for in an appraiser</h2>
<ul>
<li><strong>Estimating skill.</strong> Can they build a complete line-item estimate on their own, not just mark up yours?</li>
<li><strong>Relevant experience.</strong> Roofs, water, fire, historic homes, commercial buildings, farm structures. Ask what they have handled.</li>
<li><strong>Impartiality.</strong> Many policies require a competent and impartial or disinterested appraiser. Ask about prior relationships with the carrier, the other appraiser and your contractor.</li>
<li><strong>Clear fees.</strong> Get the fee arrangement in writing before work starts.</li>
<li><strong>Honesty about fit.</strong> A good appraiser will tell you if your claim needs a lawyer or a supplement instead.</li>
</ul>
<h2>What to look for in an umpire</h2>
<p>The umpire should be neutral, experienced in construction costs and willing to disclose any connections to either side. Many umpires are experienced appraisers, contractors, engineers or retired judges. Ask both appraisers to share candidates’ backgrounds and fee quotes.</p>
<h2>Questions to ask</h2>
<ol>
<li>Have you worked with or against this carrier or appraiser before? How often?</li>
<li>Have you ever been challenged as not impartial?</li>
<li>How do you charge, and what is included?</li>
<li>Will you inspect in person?</li>
<li>How long do your appraisals usually take?</li>
</ol>
<h2>If the appraisers cannot agree on an umpire</h2>
<p>Most policies let either side ask a court in the county where the property is located to appoint one. That adds time and cost, so it is usually a last resort.</p>
""",
    },
]
