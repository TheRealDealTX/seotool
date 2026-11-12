"""Learn-section content for Montana Insurance Appraiser.

Defines the appraisal roadmap (intro, eight stages, outro), the grouped FAQ,
the claim glossary and the field-notes posts. All text is general information
about the appraisal process, not legal advice.
"""

# ---------------------------------------------------------------------------
# Appraisal roadmap
# ---------------------------------------------------------------------------

PROCESS_INTRO = """
<p>Appraisal is a policy-based way to settle one narrow question: how much a covered loss is worth. It isn’t a lawsuit, and it isn’t another round of phone calls with the adjuster. Two appraisers and, when needed, a neutral umpire work through the numbers and sign a written award.</p>
<p>The eight stages below follow a typical Montana property claim from the first disagreement to the check. Your policy’s wording controls the details, so read each stage alongside your own appraisal clause and declarations page.</p>
"""

PROCESS_STEPS = [
    ("Pin down the disagreement", """
<p>Appraisal only works when the dispute is about <strong>how much</strong>, not <strong>whether</strong>. Before anything else, compare the carrier’s estimate with your contractor’s bid line by line and write down exactly where they differ.</p>
<ul>
<li><strong>Scope gaps:</strong> items the adjuster left out, such as the north slope of a hail-hit roof, gutters, window wraps or a pole barn.</li>
<li><strong>Pricing gaps:</strong> unit costs that don’t reflect what contractors actually charge in Billings, Kalispell or a rural county after a big storm year.</li>
<li><strong>Depreciation gaps:</strong> age or condition assumptions you believe are wrong.</li>
</ul>
<p>If the carrier has denied the whole claim, or says a peril isn’t covered, that is a coverage question, and appraisal generally can’t answer it. Many disputes also end at this stage when a well-documented supplement is accepted, so send one with photos and a revised estimate before you escalate.</p>
"""),
    ("Read the appraisal clause", """
<p>Find the appraisal clause in your policy. It usually sits in the conditions section of a homeowners form, or in the loss conditions of a commercial or farm form. Read it twice and note:</p>
<ul>
<li>Who can demand appraisal (usually either party) and whether the demand must be in writing.</li>
<li>How many days each side has to name an appraiser after a demand.</li>
<li>How the umpire is chosen and what happens if the appraisers can’t agree on one.</li>
<li>How costs are split. Most forms have each side pay its own appraiser and share the umpire.</li>
<li>Whether anything must happen first, such as a sworn proof of loss.</li>
</ul>
<p>Check your endorsements too. Some carriers amend the clause, and policies written in the surplus-lines market can use wording that differs from standard forms. If the clause is missing or unclear, ask the carrier in writing for a certified copy of the full policy.</p>
"""),
    ("Send a written demand", """
<p>Once you decide to proceed, put the demand in writing. Keep it short and factual:</p>
<ul>
<li>Your name, the property address, the policy number and the claim number.</li>
<li>A statement that you and the carrier disagree on the <strong>amount of loss</strong> and that you are invoking the appraisal provision.</li>
<li>The name and contact details of your appraiser, or a note that you will name one within the policy’s time frame.</li>
<li>A brief summary of the disputed amounts, with your estimate attached if you have one.</li>
</ul>
<p>Send it in a way you can prove, such as certified mail plus email to the adjuster, and keep a dated copy. The carrier may respond by naming its own appraiser, asking for more information or objecting that some items are coverage issues. Answer objections in writing and keep the tone businesslike; the record you build now often matters later.</p>
"""),
    ("Choose a competent appraiser", """
<p>Most clauses require each appraiser to be <strong>competent and disinterested</strong>; some say “independent” or “impartial.” Competent means the person can actually price your loss, whether that is a roofing system, water mitigation, smoke cleaning or log construction. Disinterested generally means no financial or personal stake in the outcome beyond a normal fee.</p>
<p>Questions worth asking any candidate:</p>
<ul>
<li>Have you handled appraisals on this type of loss and this type of building?</li>
<li>Do you have any relationship with my contractor, a public adjuster or the carrier?</li>
<li>How is your fee set? Some fee arrangements can invite challenges to impartiality, so ask how that is handled.</li>
<li>Will you inspect in person, and when?</li>
</ul>
<p>The carrier names its own appraiser under the same standard. If you have doubts about the other side’s choice, raise them early and in writing rather than after an award is signed.</p>
"""),
    ("Select a neutral umpire", """
<p>The two appraisers try to agree on a neutral umpire, usually soon after they are named and before serious disagreement sets in. A good umpire understands construction pricing and the policy’s valuation terms and has no ties to either side. Appraisers often trade short lists and disclose any past dealings with each candidate.</p>
<p>If the appraisers can’t agree within the time the policy allows, most clauses let either party ask a court of record in the state where the property sits to choose one. In Montana that generally means a short filing asking a district court to appoint an umpire. Procedures vary, so many people have an attorney handle that request.</p>
<ul>
<li>Agree on the umpire’s fee arrangement up front.</li>
<li>Put the selection and any disclosures in a short written agreement.</li>
<li>Keep the umpire out of the details until the appraisers actually need a decision.</li>
</ul>
"""),
    ("Inspect and build estimates", """
<p>Each appraiser inspects the property, ideally with the other present so both are looking at the same damage. On a hail claim that may mean walking every slope, checking soft metals and vents, and counting impacts in test squares. On a winter water loss it can mean moisture readings, inspection holes and a review of mitigation logs.</p>
<p>Each appraiser then builds an estimate, usually in Xactimate or Symbility, with pricing that fits the property’s location and when the work can realistically be done. A useful estimate shows:</p>
<ul>
<li>A clear scope, room by room or slope by slope.</li>
<li>Quantities anyone can check: roofing squares, linear feet, square feet of drywall.</li>
<li>Unit pricing and any overhead and profit.</li>
<li>Replacement cost, depreciation and actual cash value, if the policy pays them separately.</li>
</ul>
<p>The appraisers exchange estimates and supporting documents before they sit down to negotiate.</p>
"""),
    ("Panel talks and umpire hearing", """
<h3>Appraiser negotiation</h3>
<p>Most appraisals settle between the two appraisers. They go through the competing estimates line by line, agree on what they can and mark the rest as disputed. Photos, measurements, manufacturer data and local contractor pricing tend to move numbers more than argument does. When both appraisers agree and sign, that award is generally binding on the amount of loss.</p>
<h3>Taking it to the umpire</h3>
<p>If gaps remain, the appraisers submit only the disputed items to the umpire. Some umpires work from written submissions; others hold an informal meeting, sometimes at the property. Each appraiser explains a position and the evidence behind it. The umpire then decides each disputed item, and an award signed by the umpire and either appraiser usually settles the amount.</p>
<p>Ask your appraiser to walk you through the umpire’s process before it begins so nothing about the format surprises you.</p>
"""),
    ("The award and payment", """
<p>The award is a written statement of the amount of loss, often itemized by coverage: dwelling, other structures, contents and loss of use. Many awards show both replacement cost and actual cash value so recoverable depreciation is clear.</p>
<ul>
<li><strong>Holdback:</strong> under many replacement cost policies, the carrier pays actual cash value first and releases withheld depreciation after repairs are completed and documented.</li>
<li><strong>Mortgagee on the check:</strong> if you have a mortgage, expect the lender’s name on dwelling payments. Lenders often run repair funds through a loss draft process.</li>
<li><strong>Deductible and prior payments:</strong> these come off the award total.</li>
</ul>
<p>An award decides the amount of loss. It generally does not decide coverage, whether a policy condition was met, or questions about how the carrier handled the claim. If those issues exist, they belong with a licensed Montana attorney.</p>
"""),
]

PROCESS_OUTRO = """
<h2>A word on deadlines and attorneys</h2>
<p>Policies set their own time limits for things like reporting a loss, submitting a proof of loss, naming an appraiser, completing repairs to collect holdback and filing suit. Montana law may also affect how some of those limits apply. We don’t give legal advice, so we can’t tell you which deadline governs your claim. Read your policy, write down every date and put it on a calendar.</p>
<p>If the carrier denies coverage, raises a policy-condition defense or you believe the claim has been handled unfairly, talk to a licensed Montana attorney before any deadline passes. Appraisal and legal advice can run side by side; one doesn’t replace the other.</p>
"""

# ---------------------------------------------------------------------------
# FAQ
# ---------------------------------------------------------------------------

FAQ = [
    ("Appraisal basics", [
        ("What is insurance appraisal?",
         "Appraisal is a process written into most property policies for resolving a disagreement over the amount of a covered loss. Each side names an appraiser, the two appraisers pick a neutral umpire, and an award signed by any two of the three generally sets the amount. It is not a lawsuit, and it does not decide whether the loss is covered."),
        ("When does appraisal make sense?",
         "Appraisal fits best when the carrier accepts that a loss is covered but you disagree on price, the scope of repairs or depreciation. Common examples are hail-damaged roofs paid as repairs instead of replacement, unit pricing that is too low for your area, or missing interior items after a water or smoke loss. If the gap is small or the dispute is about coverage, another route may be better."),
        ("Does appraisal decide coverage?",
         "Generally, no. Appraisal decides the amount of loss. Whether a peril is covered, whether an exclusion applies or whether a policy condition was met are coverage questions, and courts usually treat them as outside the appraisers’ role. Some awards list disputed items separately so a later coverage decision can be applied. A licensed Montana attorney can explain how that works for your claim."),
        ("Who can demand appraisal?",
         "Under most policy forms, either you or the insurer can demand appraisal in writing once there is a genuine disagreement over the amount of loss. Some policies list steps that must come first, such as submitting a sworn proof of loss. Read your appraisal clause and every endorsement to see exactly what your own policy requires before you send a demand."),
        ("Is an appraisal award binding?",
         "An award signed by two of the three panel members, either both appraisers or one appraiser and the umpire, is generally binding on the amount of loss. Awards can be challenged in limited circumstances, such as fraud, a lack of impartiality or a panel deciding matters outside its authority. Whether a challenge is possible is a legal question for a licensed Montana attorney."),
    ]),
    ("Costs & timing", [
        ("Who pays for appraisal?",
         "Most policies say each side pays its own appraiser and the two sides split the umpire’s fee and other shared costs equally. The insurer does not usually reimburse your appraiser’s fee, even when the award comes in higher than its estimate. Check your own appraisal clause, since some forms word the cost split differently."),
        ("How are appraiser fees structured?",
         "Appraisers may charge hourly, a flat fee or a fee tied to the size of the claim. Each approach has trade-offs. Some contingency-style arrangements can draw challenges to an appraiser’s impartiality, so ask any candidate how the fee works and whether it could be an issue under your policy wording. Get the arrangement in writing before work starts."),
        ("How long does appraisal take in Montana?",
         "Many residential appraisals wrap up within a few months of the demand, but timing depends on how quickly both sides name appraisers, how fast an umpire is chosen and how far apart the estimates are. Big hail years, winter access to mountain properties and contractor backlogs can all stretch the timeline."),
        ("Is appraisal worth it for a small gap?",
         "Sometimes not. Because you pay your own appraiser and half the umpire, a small difference can be eaten up by costs. Illustrative example: if the gap is only a few thousand dollars, a well-documented supplement or a reinspection request may be the better first step. Run your numbers with our claim gap calculator before deciding."),
        ("Does demanding appraisal delay my payment?",
         "It shouldn’t stop payment of amounts that are not in dispute. Many carriers pay their own estimate first, less the deductible, and the award later sets any additional amount owed. If undisputed money is being held back, ask the adjuster in writing why. The Montana CSI publishes consumer guidance if you have concerns about claim handling."),
    ]),
    ("Montana specifics", [
        ("Who regulates insurance in Montana?",
         "The Office of the Montana Commissioner of Securities and Insurance, known as the CSI, regulates insurers doing business in the state. It is part of the State Auditor’s office, and the elected State Auditor serves as Commissioner. The CSI takes consumer complaints about claim handling and publishes guidance for policyholders."),
        ("Does Montana have a FAIR plan or wind pool?",
         "No. Montana does not have a state FAIR plan or a wind pool. Homes that standard carriers decline, including some in the wildland-urban interface, may be placed with a surplus-lines insurer instead. Surplus-lines policy forms can vary more than standard forms, so read the appraisal clause, deductibles and exclusions closely."),
        ("What does Montana law say about unfair claim handling?",
         "Montana’s Unfair Trade Practices Act, found in Title 33, Chapter 18 of the Montana Code Annotated, lists unfair claim settlement practices insurers must avoid. Montana law also allows an insured to bring a claim against their own insurer for certain of those practices. Whether any of that applies to your claim is a legal question, so talk to a licensed Montana attorney. We don’t give legal advice."),
        ("How do percentage wind and hail deductibles work?",
         "Some Montana policies set the wind or hail deductible as a percentage of the dwelling coverage limit instead of a flat dollar amount. Illustrative example: a 2 percent deductible on a $400,000 dwelling limit equals $8,000 (illustrative figures). Check your declarations page, since this deductible can be much larger than your all-peril deductible."),
        ("Are matching rules and roof payment schedules common in Montana?",
         "Both come up. Matching questions arise when discontinued shingles or siding can’t be blended with undamaged areas, and how that is handled depends on policy wording and the facts. Some carriers also use roof payment schedules that pay a declining share of roof replacement as the roof ages. Read your endorsements and ask your agent which apply."),
    ]),
    ("Hail, wind, wildfire & winter", [
        ("Can appraisal help with a hail-damaged roof?",
         "Yes, when the carrier accepts some hail damage but you disagree on repair versus replacement, the number of slopes, pricing or accessories. Montana roofs see repeated hail east of the Divide and along the Hi-Line, so appraisers often look at test squares, soft-metal marks, prior damage and whether patching is practical with the existing material."),
        ("What about metal roofs and cosmetic damage?",
         "Some policies include a cosmetic damage exclusion or endorsement for metal roofs, which can limit payment for dents that don’t affect function. Whether a dent is cosmetic or functional may be partly a coverage question and partly an amount question. Read the exact endorsement wording before demanding appraisal, and ask your appraiser how a panel might handle it."),
        ("How are wind claims from Chinook winds handled?",
         "Downslope winds along the Rocky Mountain Front and around Livingston can lift shingles, peel metal panels and damage siding and outbuildings. The carrier may point to wear or prior damage. Once coverage is accepted, appraisal can settle the scope and price of wind repairs. Photograph damage promptly, since repeated wind events can blur what happened when."),
        ("Is wildfire smoke damage covered and appraisable?",
         "Many policies cover smoke and ash from a nearby wildfire even when flames never reach the house, but terms vary. Disputes often involve cleaning versus replacement, HVAC work, contents and how far odor reaches. Once smoke damage is accepted, appraisal can address the cost of cleaning and repairs. Testing and careful documentation help on both sides."),
        ("Are ice dam and frozen pipe losses appraisable?",
         "Interior water damage from an ice dam or a burst pipe is often covered when it is sudden, though some policies limit long-term leaks or freezing in a home where heat wasn’t maintained. When the carrier accepts the loss but underpays drying, drywall or flooring, appraisal can resolve the amount. Snowmelt flooding is different and usually needs NFIP or private flood coverage."),
    ]),
    ("After the award", [
        ("When will I get paid after an award?",
         "Your policy usually sets a payment period after an award is signed and submitted, and the carrier then pays the award less the deductible and earlier payments. The exact time frame depends on your policy wording. If payment seems slow, follow up in writing. The CSI publishes consumer guidance if you have concerns."),
        ("Why is my mortgage company on the check?",
         "If your policy lists a mortgagee, the carrier is generally required to include the lender as a payee on dwelling payments. Many lenders deposit large checks into a loss draft account and release money in stages as repairs progress. Contact your lender’s loss draft department early to learn its paperwork and inspection rules."),
        ("How do I collect recoverable depreciation?",
         "Under many replacement cost policies, the carrier pays actual cash value first and holds back depreciation until repairs are complete. To collect it, you usually submit proof of completion, such as a final invoice, photos or a contractor’s completion certificate. Check your policy for any time limit on finishing repairs and making that request."),
        ("Can I still pursue other claims after an appraisal award?",
         "An award generally settles the amount of loss, but it usually doesn’t resolve coverage disputes or concerns about how the insurer handled the claim. Whether you have other claims, and what deadlines apply, is a legal question. Talk with a licensed Montana attorney. We don’t give legal advice or represent anyone in court."),
        ("What if repairs cost more than the award?",
         "Hidden damage found during repairs, such as rotted decking under a hail-damaged roof, may support a supplemental claim if it wasn’t part of what the panel considered. Code upgrades may fall under ordinance or law coverage if your policy includes it. Photograph new findings before they are covered up and notify the carrier promptly in writing."),
    ]),
]

# ---------------------------------------------------------------------------
# Glossary
# ---------------------------------------------------------------------------

GLOSSARY = [
    ("Actual cash value (ACV)", "The value of damaged property at the time of loss, usually figured as replacement cost minus depreciation. Some policies define it differently, so check your own policy’s wording."),
    ("Additional living expense (ALE)", "Coverage for the increased cost of living away from home, such as lodging, extra mileage and restaurant meals, while a covered loss makes the home uninhabitable."),
    ("Amount of loss", "The dollar value of a covered loss. Appraisal decides this figure; it generally does not decide whether the loss is covered in the first place."),
    ("Appraisal clause", "The policy provision that lets either party demand appraisal when they disagree on the amount of loss. It sets out how appraisers and the umpire are chosen and how the award works."),
    ("Award", "The written decision of an appraisal panel stating the amount of loss. An award signed by any two of the three panel members is generally binding on the amount."),
    ("Class 4 shingle", "A shingle that earned the highest impact-resistance rating under the UL 2218 test. Some insurers offer premium discounts for Class 4 roofs, though the shingles are not hail-proof."),
    ("Collapse", "A policy term for a building, or part of one, falling down or, under some policies, being in imminent danger of falling. Definitions vary widely, so read the exact wording."),
    ("Competent and disinterested", "The standard many appraisal clauses set for appraisers: able to evaluate and price the loss, and without a financial or personal stake in the outcome beyond a reasonable fee."),
    ("Contents (personal property)", "Belongings such as furniture, clothing, tools and electronics, usually insured under Coverage C. Some categories, like jewelry or firearms, carry special lower limits for theft."),
    ("Cosmetic damage exclusion", "An endorsement in some policies that limits or excludes payment for damage that affects only appearance, such as hail dents on metal roofing, without affecting how the roof performs."),
    ("Debris removal", "Coverage for the cost of removing debris from damaged property after a covered loss. Some policies pay it within the coverage limit and add a modest extra amount."),
    ("Declarations page", "The summary page of a policy listing the named insured, the property, coverage limits, deductibles, the policy period and attached endorsements. Often called the dec page."),
    ("Deductible", "The amount you bear toward a covered loss before the insurer pays. It is subtracted from the claim payment rather than paid to the carrier separately."),
    ("Dwelling (Coverage A)", "The coverage for the house itself and structures attached to it, such as an attached garage, porch or deck, along with built-in fixtures."),
    ("Endorsement", "A form attached to a policy that adds, removes or changes coverage. Endorsements can change deductibles, valuation, roof coverage or even the appraisal clause itself."),
    ("Holdback", "The amount a carrier withholds, usually recoverable depreciation, until repairs are finished. It is released once you document completion, subject to any time limit in the policy."),
    ("Ice dam", "A ridge of ice that forms at a roof’s edge and traps melting snow behind it. The water backs up under roofing and can leak into ceilings, walls and insulation."),
    ("Line of sight", "A concept used in matching disputes: whether repaired and undamaged areas can be seen together. Areas in a continuous line of sight are more likely to raise matching issues."),
    ("Loss of use", "The coverage section, often Coverage D, that includes additional living expense and fair rental value when a covered loss makes the property unusable."),
    ("Matching", "The question of whether replacement materials must reasonably match undamaged areas in color, texture and size. How it is handled depends on policy wording and the facts."),
    ("Mitigation", "Reasonable steps taken to prevent further damage after a loss, such as tarping a roof, shutting off water or drying out a building. Most policies require it."),
    ("Montana CSI", "The Office of the Montana Commissioner of Securities and Insurance, part of the State Auditor’s office. It regulates insurers, takes consumer complaints and publishes consumer guidance."),
    ("Mortgagee clause", "A policy provision protecting the lender’s interest in the property. It usually means the lender is named as a payee on dwelling claim payments."),
    ("NFIP", "The National Flood Insurance Program, a federal program that offers flood insurance. Most homeowners policies exclude flood, so flood coverage usually requires a separate NFIP or private policy."),
    ("Ordinance or law coverage", "Coverage for the added cost of meeting current building codes when repairing or rebuilding, such as required ice and water shield or structural upgrades. Limits are often a percentage of dwelling coverage."),
    ("Other structures (Coverage B)", "Coverage for detached structures on the property, such as fences, sheds, detached garages, pole barns and corrals, usually limited to a percentage of the dwelling limit."),
    ("Overhead and profit (O&P)", "A contractor’s charges for business overhead and profit, often figured as a percentage added to an estimate. Disputes often center on whether a general contractor is reasonably needed."),
    ("Percentage deductible", "A deductible figured as a percentage of a coverage limit, usually the dwelling limit, instead of a flat dollar amount. It grows as the coverage limit grows."),
    ("Pitch", "The slope of a roof, expressed as inches of rise per 12 inches of horizontal run, such as 6/12. Steeper pitches add labor, safety and equipment costs."),
    ("Proof of loss", "A sworn statement of the amount claimed and the facts of the loss. Some policies require one within a set time or when the carrier asks for it."),
    ("Recoverable depreciation", "The portion of depreciation a replacement cost policy will pay once repairs or replacement are completed, usually after you submit proof of the finished work."),
    ("Replacement cost value (RCV)", "The cost to repair or replace damaged property with materials of like kind and quality, without any deduction for depreciation."),
    ("Reservation of rights", "A letter in which an insurer says it is investigating or paying a claim while reserving the right to deny coverage later, often citing specific policy provisions."),
    ("Roof payment schedule", "An endorsement that pays a declining percentage of roof replacement cost based on the roof’s age and material, regardless of its condition before the loss."),
    ("Scope of loss", "The list of damaged items and the repairs needed to restore them. Many appraisal disputes turn on scope rather than on unit pricing."),
    ("Snow load", "The weight of accumulated snow and ice on a roof. Local building codes set design snow loads, which are considerably higher in many Montana mountain towns."),
    ("Square (roofing)", "A unit of roof area equal to 100 square feet. Roofing estimates are priced per square, with an added allowance for cutting waste."),
    ("Supplement", "A request for additional payment for items missed in the original estimate or found during repairs, supported by photos, invoices or a revised estimate."),
    ("Surplus lines insurer", "A non-admitted insurer allowed to write hard-to-place risks in Montana through licensed surplus-lines brokers. Its policy forms can differ more from standard forms."),
    ("Symbility", "Property claims estimating software used by some insurers and adjusters as an alternative to Xactimate, with its own pricing data and report format."),
    ("Umpire", "A neutral third person chosen by the two appraisers, or appointed by a court if they can’t agree, who decides the items the appraisers can’t resolve."),
    ("Unfair claim settlement practices", "Claim-handling conduct that Montana’s Unfair Trade Practices Act, in Title 33, Chapter 18 of the Montana Code Annotated, lists as prohibited. Talk to a licensed Montana attorney about specific situations."),
    ("Wildland-urban interface (WUI)", "Areas where homes and other development meet or mix with forest, grassland or other wildland fuels. Many western Montana homes sit in the WUI."),
    ("Wind/hail deductible", "A separate deductible that applies only to wind or hail losses. On some Montana policies it is a percentage of the dwelling limit and can exceed the all-peril deductible."),
    ("Xactimate", "Estimating software widely used by insurers, adjusters, appraisers and contractors to price property repairs from regional price lists for labor and materials."),
]

# ---------------------------------------------------------------------------
# Field notes (posts)
# ---------------------------------------------------------------------------

POSTS = [
    {
        "slug": "montana-appraisal-clause-explained",
        "title": "Montana Appraisal Clause Explained: How the Process Works",
        "seo": "Montana Appraisal Clause Explained | Policy Guide",
        "kw": "Montana appraisal clause",
        "desc": "Montana appraisal clause guide: who can demand it, how appraisers and umpires are chosen, and what an award decides or leaves alone.",
        "summary": "A plain-language walk through the appraisal clause in Montana property policies, phrase by phrase. Learn what it can decide, what it can’t and when it’s the wrong tool.",
        "date": "2026-09-03",
        "read": "7 min",
        "body": """
<h2>What the appraisal clause is for</h2>
<p>Almost every homeowners, farm and commercial property policy sold in Montana contains a short paragraph titled “Appraisal.” It gives you and your insurer a way to settle one specific kind of dispute: a disagreement over the <strong>amount of loss</strong>. It doesn’t replace the claim process, and it isn’t a lawsuit. It is a private, policy-based valuation panel that both sides agreed to when the policy was issued.</p>
<p>The Montana appraisal clause in most standard forms reads much like the clause used across the country, but the details matter. Carriers amend it by endorsement, and policies written by surplus-lines insurers can use their own wording. Because Montana has no state FAIR plan, some homes in the wildland-urban interface end up in that market. Read your clause, not a summary of it.</p>
<h2>The typical language, piece by piece</h2>
<p>A common version says that if you and the insurer fail to agree on the amount of loss, either may demand an appraisal in writing. Each party then chooses a competent and disinterested appraiser within a set number of days. The two appraisers choose an umpire, and if they can’t agree, either side may ask a court of record in the state where the property is located to select one. The appraisers state separately the amount of loss, and any differences go to the umpire. A written award agreed to by any two sets the amount of loss.</p>
<p>Each of those phrases does real work:</p>
<ul>
<li><strong>“Fail to agree on the amount of loss.”</strong> There must be a genuine disagreement about price or scope. A flat denial is usually a coverage dispute, not an appraisal issue.</li>
<li><strong>“Either may demand.”</strong> You and the carrier hold the same right. Some carriers invoke appraisal themselves when a contractor’s bid is far above their estimate.</li>
<li><strong>“Competent and disinterested.”</strong> Each appraiser must be able to price the loss and must not have a stake in the outcome beyond a fee.</li>
<li><strong>“Court of record.”</strong> If the appraisers deadlock over the umpire, a Montana district court can usually be asked to appoint one.</li>
<li><strong>“Any two.”</strong> Two signatures out of three make the award. The umpire only weighs in when the appraisers can’t agree.</li>
</ul>
<h2>What appraisal can and can’t decide</h2>
<p>Appraisal answers <em>how much</em>. It generally doesn’t answer <em>whether</em>. In practice, the panel can usually decide:</p>
<ul>
<li>Whether a hail-damaged roof needs full replacement or a repair, once hail damage is accepted.</li>
<li>Unit pricing for labor and materials in your part of Montana, from Miles City to Whitefish.</li>
<li>Quantities, such as roofing squares, drywall square footage or linear feet of fence.</li>
<li>Depreciation and actual cash value, if the policy pays them separately.</li>
</ul>
<p>It usually can’t decide whether a peril is excluded, whether you met a policy condition, or whether the insurer handled the claim properly. Those questions belong with a licensed Montana attorney. A careful award sometimes lists contested items separately so a later coverage decision can be applied without redoing the appraisal.</p>
<h2>Timelines inside the clause</h2>
<p>Many clauses give each side a fixed window, often around 20 days, to name an appraiser after a written demand. Some set a similar window for agreeing on an umpire. Policies differ, and Montana law may affect how some time limits apply, so never assume. Write down the dates in your own policy and track them. Our <a href="/appraisal-roadmap/">appraisal roadmap</a> walks through each stage in order.</p>
<h2>Costs under a standard clause</h2>
<p>The usual rule is that each side pays its own appraiser and the two sides share the umpire and other joint costs equally. That split is why appraisal suits meaningful gaps better than small ones.</p>
<div class="note"><p>Illustrative example: if the carrier’s estimate is $18,000 and your contractor’s bid is $41,000, a $23,000 gap may justify the cost of appraisal. A $2,500 gap often doesn’t. These figures are illustrative only.</p></div>
<h2>Conditions that can come first</h2>
<p>Some policies require a sworn proof of loss, an examination under oath or access to records before an appraisal demand moves forward. Others are silent. If the carrier says a condition hasn’t been met, answer in writing and consider asking a Montana attorney whether the objection holds up. Don’t let the clock run while you argue about it.</p>
<h2>Choosing who sits on your side</h2>
<p>Your appraiser is the most important choice you make. Look for someone who prices the type of loss you have, inspects in person and documents every number. On a ranch claim, that might mean someone comfortable with pole barns and machine sheds. In Big Sky or Whitefish, it might mean high-end finishes and resort-area labor costs. We provide <a href="/claim-services/appraisal-clause-representation/">appraisal clause representation</a> for policyholders and also serve as a neutral <a href="/claim-services/umpire-services/">umpire</a> when both sides agree to it.</p>
<h2>When the clause isn’t the right tool</h2>
<p>The Montana appraisal clause is not the best move when the carrier has denied the claim outright, when the real dispute is about an exclusion, or when the gap is too small to justify the cost. In those situations, a supplement with better documentation, a reinspection request, a complaint to the Montana Commissioner of Securities and Insurance or a conversation with an attorney may make more sense. If terms in your policy are confusing, our <a href="/claim-dictionary/">claim dictionary</a> defines the words that come up most often in appraisal disputes.</p>
""",
    },
    {
        "slug": "hail-claims-on-montana-roofs",
        "title": "Montana Hail Claims on Roofs: Scope, Matching and Appraisal",
        "seo": "Montana Hail Claim Guide: Roofs, Deductibles, Appraisal",
        "kw": "Montana hail claim",
        "desc": "A Montana hail claim guide for roofs: repair vs. replacement, matching, metal roofs, percentage deductibles and when appraisal fits.",
        "summary": "Why hail roof disputes are so common in Montana and what decides them. Covers test squares, matching, metal roofs, deductibles, payment schedules and missed items.",
        "date": "2026-09-17",
        "read": "8 min",
        "body": """
<h2>Why hail drives so many Montana roofing disputes</h2>
<p>Montana is one of the most hail-prone states in the country. Convective storms that build over the plains in late spring and summer can drop large stones across Yellowstone, Cascade, Hill and Gallatin counties in a single afternoon, and Billings, Great Falls and towns along the Hi-Line see repeat events. That history shapes almost every Montana hail claim: roofs may carry old damage, adjusters may be stretched thin after a big storm, and roofers can be booked months out.</p>
<p>Most disputes fall into a few predictable patterns. Knowing them helps you document the right things before appraisal.</p>
<h2>Repair versus replacement</h2>
<p>The most common gap is a carrier estimate that pays to replace a handful of shingles while your roofer says the whole roof needs to come off. The questions that usually decide it:</p>
<ul>
<li>How many hail hits are there per test square on each slope?</li>
<li>Will repaired shingles reseal and lie flat, or does lifting them cause more damage? Older and brittle shingles often crack when handled.</li>
<li>Is the product still made? If not, can a repair match in color, size and profile?</li>
<li>Does the local building department require more than a patch once a certain portion of the roof is replaced?</li>
</ul>
<p>Appraisers on both sides should look at the same slopes, ideally together, and record test-square counts with photos.</p>
<h2>Matching discontinued shingles and siding</h2>
<p>Many Montana homes have roofing or siding that is no longer manufactured. When a repair can’t blend with undamaged areas, a matching dispute follows. How matching is handled depends on your policy wording and the facts; some policies address it directly, and some limit it by endorsement. Get a written statement from a supplier if a product is discontinued, and keep a sample.</p>
<h2>Metal roofs and cosmetic damage</h2>
<p>Metal roofing is common on rural homes, cabins and ag buildings, and stone-coated steel has become popular in hail country. Some policies include a cosmetic damage exclusion or endorsement that limits payment for dents that don’t affect how the roof sheds water. Whether a particular dent is cosmetic or functional can be partly a coverage question, so read the exact wording before you demand appraisal. If coverage is accepted, appraisers can still disagree on panel replacement, trim and fasteners.</p>
<h2>Class 4 shingles</h2>
<p>Many owners install Class 4 impact-resistant shingles, sometimes for a premium discount. Those shingles resist hail better, but they aren’t hail-proof. Look for fractured mats, granule loss and damage to vents, flashing and gutters. Ask whether your policy has any special terms tied to the discount.</p>
<h2>Deductibles and payment schedules</h2>
<p>Two policy features can change the math on a Montana hail claim before anyone argues about scope.</p>
<h3>Percentage wind and hail deductibles</h3>
<p>Some policies set a separate wind and hail deductible as a percentage of dwelling coverage. Illustrative example: a 1 percent deductible on a $350,000 dwelling limit is $3,500, while 2 percent would be $7,000 (illustrative figures). Our <a href="/claim-toolkit/wind-hail-deductible-calculator/">wind and hail deductible calculator</a> shows how yours works.</p>
<h3>Roof payment schedules</h3>
<p>Some carriers use a roof payment schedule that pays a declining percentage of replacement cost as the roof ages, regardless of condition. If your policy has one, appraisal can still settle the full replacement cost figure, and the schedule then applies to it. Check your declarations page and endorsements so you know what to expect.</p>
<h2>Measuring the roof correctly</h2>
<p>Small measurement errors become big dollar gaps. Steep pitches, multiple facets, dormers, starter and ridge materials all affect the number of squares and the labor charges, and steep-roof and high-roof charges are easy to leave off. Check pitch and square counts with our <a href="/claim-toolkit/roof-pitch-squares-calculator/">roof pitch and squares calculator</a>, and compare them against any aerial measurement report in the file.</p>
<h2>Items adjusters often leave out</h2>
<ul>
<li>Gutters, downspouts and gutter guards with hail dents.</li>
<li>Window screens, wraps and siding on the storm-facing side.</li>
<li>Roof vents, turbines, skylights and a satellite dish reset.</li>
<li>Ice and water shield where local code calls for it.</li>
<li>Drip edge, permits, dumpsters and haul-off on long rural drives.</li>
<li>Detached garages, sheds and pole barns under other structures coverage.</li>
</ul>
<h2>Old damage and the date of loss</h2>
<p>Because Montana roofs can be hit several times over the years, carriers sometimes attribute damage to an earlier storm. Weather data for your address, dated photos and prior inspection reports help tie damage to a specific event. If you had an earlier claim on the same roof, keep that file handy, since the panel may need to separate what was paid before from what is new.</p>
<h2>Contractor availability after a big year</h2>
<p>After a widespread storm, crews from out of state arrive, local roofers get backlogged and prices can climb. A fair estimate reflects what it actually costs to get the work done in your area within a reasonable time, including travel to rural properties. Keep any bids that show local pricing.</p>
<h2>Where appraisal fits</h2>
<p>Once your carrier accepts hail damage but disagrees on scope or price, appraisal can settle the amount of your Montana hail claim. Billings-area owners can read more on our <a href="/montana-cities/billings/">Billings page</a>, and our <a href="/claim-services/hail-roof-damage-appraisal/">hail and roof damage appraisal</a> service explains how we document roofs for the panel.</p>
""",
    },
    {
        "slug": "wildfire-and-smoke-claims-montana",
        "title": "Montana Wildfire Smoke Claims: Total Losses, Soot, Ash and Appraisal",
        "seo": "Montana Wildfire Smoke Claim Guide: Damage and Appraisal",
        "kw": "Montana wildfire smoke claim",
        "desc": "How a Montana wildfire smoke claim works: total losses, soot and ash cleaning, HVAC, contents, living expenses and where appraisal fits.",
        "summary": "Wildfire claims in Montana range from total losses to smoke damage in homes the fire never touched. Here’s what drives disputes and how to document them.",
        "date": "2026-09-30",
        "read": "8 min",
        "body": """
<h2>Fire seasons that shape Montana claims</h2>
<p>Montana has a long wildfire record: the 1988 fires in and around Yellowstone, the 2000 Bitterroot fires in Ravalli County, and the 2017 season with the Lolo Peak Fire near Missoula, the Rice Ridge Fire near Seeley Lake and the Lodgepole Complex in Garfield County. Eastern Montana isn’t immune; the 2012 Dahl Fire near Roundup destroyed dozens of homes, and the 2021 Richard Spring Fire burned across Rosebud County. Smoke from big fires can settle over western valleys for weeks.</p>
<p>A Montana wildfire smoke claim usually falls into one of three groups: a total loss, partial burn damage, or smoke, soot and ash damage to a home the fire never reached. Each raises different valuation questions.</p>
<h2>Total losses</h2>
<p>When a home burns, the questions center on the dwelling limit, debris removal, code upgrades and contents. Rebuilding in a remote county can cost more than the carrier’s pricing assumes because of contractor travel, short building seasons and material delivery. If your policy includes ordinance or law coverage, it may help with code items. Check whether you have extended replacement cost or similar endorsements.</p>
<p>Contents inventories are a major part of a total loss. Build them room by room using photos, videos, bank and card statements and online order histories. Many policies pay actual cash value first and release depreciation after items are replaced.</p>
<h2>Smoke, soot and ash without flames</h2>
<p>This is where most disputes happen. Many policies cover smoke damage from a nearby wildfire, but terms vary, and carriers sometimes treat the damage as temporary or limit it to light cleaning. Common points of disagreement:</p>
<ul>
<li><strong>Cleaning versus replacement:</strong> whether soft goods, insulation, carpet and porous finishes can be cleaned or must be replaced.</li>
<li><strong>HVAC systems:</strong> duct cleaning, filter replacement and whether ash has entered the air handler.</li>
<li><strong>Odor:</strong> how far smoke odor reaches into wall cavities, attics and crawl spaces, and whether sealing and deodorizing are needed.</li>
<li><strong>Exterior:</strong> ash etching on glass, staining on siding and damage to log home finishes, which may need blasting and refinishing.</li>
<li><strong>Contents:</strong> cleaning costs, pack-out and storage, and items that can’t be restored.</li>
</ul>
<h3>Testing and documentation</h3>
<p>Lab sampling for soot, char and ash can help show where wildfire residue is present. Testing isn’t always necessary, and either side may question methods, but objective data often narrows the dispute. Photograph surfaces before cleaning, keep sampling reports and save receipts for any emergency work.</p>
<h2>Living expenses during evacuation and repairs</h2>
<p>Evacuation orders, smoke levels and repair work can keep you out of your home. Many policies pay additional living expense when the home is uninhabitable, and some include coverage tied to a civil authority order. Keep hotel bills, mileage and meal receipts, and note the dates on any evacuation notice. These amounts can be part of an appraisal if the carrier disputes them and the policy allows it.</p>
<h2>Insurance in the wildland-urban interface</h2>
<p>Montana has no state FAIR plan. Some homes in the wildland-urban interface, from the Bitterroot to the Flathead, end up with a surplus-lines insurer when standard carriers decline. Surplus-lines policies can use different appraisal language, sublimits for smoke or debris and different exclusions. Read the full policy, not just the declarations page. If a provision is unclear, the Montana Commissioner of Securities and Insurance publishes consumer guidance, and a licensed Montana attorney can explain your rights.</p>
<h2>Trees, landscaping and outbuildings</h2>
<p>Many policies cover trees and landscaping with low per-item limits and only for certain perils, so read that section closely. Fences, sheds, barns and corrals usually fall under other structures coverage. On ranch properties those structures add up quickly, and their replacement cost is often underestimated. Document each one’s size, materials and condition.</p>
<h2>Working with cleaning and restoration crews</h2>
<p>After a big fire, restoration companies get busy fast. Before any crew starts, ask for a written scope of what it will clean and how, and keep copies. If the carrier hires its own vendor, you can still document conditions yourself before and after. Cleaning that leaves odor or residue behind is a common reason claims reopen, so do a walkthrough with the crew before signing off.</p>
<h2>When to consider appraisal</h2>
<p>Once your carrier accepts that smoke or fire damage occurred but you disagree on the scope or cost of cleaning, repair or replacement, appraisal can settle the amount. It won’t decide whether a smoke exclusion applies. For more on how we approach these claims, see our <a href="/claim-services/wildfire-claim-appraisal/">wildfire claim appraisal</a> and <a href="/claim-services/fire-smoke-claim-appraisal/">fire and smoke claim appraisal</a> pages. Owners in Missoula County can also visit our <a href="/montana-cities/missoula/">Missoula page</a>.</p>
<div class="note"><p>A Montana wildfire smoke claim often turns on early documentation. Photograph everything before cleaning crews arrive, and keep a dated log of what was done.</p></div>
""",
    },
    {
        "slug": "snow-load-and-ice-dam-claims",
        "title": "Snow Load and Ice Dam Claims: A Montana Winter Guide",
        "seo": "Snow Load and Ice Dam Claims in Montana Homes",
        "kw": "snow load and ice dam claims",
        "desc": "Snow load and ice dam claims in Montana: collapse wording, outbuildings, frozen pipes, mitigation, flood exclusions and where appraisal fits.",
        "summary": "Winter damage in Montana raises more coverage questions than most claims. Here’s how carriers look at collapse, ice dams and frozen pipes, and how to document them.",
        "date": "2026-10-14",
        "read": "8 min",
        "body": """
<h2>Winter is its own claim season in Montana</h2>
<p>Montana winters bring heavy snow in the mountains, long cold snaps on the plains and fast swings when a Chinook arrives or an arctic front drops in. Those conditions produce a steady run of snow load and ice dam claims, along with frozen and burst pipes. The damage often shows up weeks after a storm, when snow melts and water finds its way inside.</p>
<p>These claims tend to involve more coverage arguments than hail claims. Before you think about appraisal, it helps to understand how carriers look at winter damage.</p>
<h2>Snow load and collapse</h2>
<p>Many homeowners policies cover collapse caused by the weight of ice, snow or sleet, often under a separate collapse provision with its own definitions. The meaning of collapse varies by policy. Some require an abrupt falling down; others also cover parts of a building in imminent danger of falling. Sagging rafters, cracked trusses and bowed walls may or may not qualify depending on the wording.</p>
<p>Mountain towns such as Bozeman, Big Sky, Whitefish and Red Lodge typically have higher design snow loads than the eastern plains, and local building departments set the requirements. An older cabin or a pole barn built before current codes may not meet them. If repairs trigger code upgrades, ordinance or law coverage, if you have it, may help pay for them.</p>
<h3>Outbuildings and ag structures</h3>
<p>Pole barns, machine sheds, hay barns and loafing sheds are vulnerable because of their long clear spans. They usually fall under other structures coverage on a homeowners policy, or under a separate farm or ranch schedule. Check the limit and the valuation basis, since some structures are covered at actual cash value only.</p>
<h2>Ice dams</h2>
<p>An ice dam forms when heat escaping through the roof melts snow and the water refreezes at the colder eaves. Water backs up under shingles and leaks into ceilings, walls and insulation. Carriers often accept the interior water damage but argue about:</p>
<ul>
<li>Whether the roof itself was damaged or just needs snow and ice removal.</li>
<li>How much drywall, insulation and paint must be replaced.</li>
<li>Whether ice and water shield must be added to meet code when the roof is repaired.</li>
<li>Whether the leak was sudden or a long-term condition, which some policies exclude.</li>
</ul>
<p>Keep invoices for roof snow removal and ice steaming. Those costs may be covered as reasonable steps to protect the property.</p>
<h2>Frozen and burst pipes</h2>
<p>During a cold snap, pipes in exterior walls, crawl spaces and unheated garages can freeze and split, and the water can do serious damage fast. Many policies cover sudden water damage from a burst pipe, but some exclude or limit freezing losses if the home was vacant or heat wasn’t maintained, unless the water supply was shut off and the system drained. Cabins and seasonal homes deserve a close read of the vacancy and freezing language.</p>
<h2>Mitigation comes first</h2>
<p>Most policies require reasonable steps to prevent further damage. In winter that means stopping water, getting heat back on, calling a mitigation company and documenting what you find. Mitigation estimates and drying logs often become exhibits in appraisal, so keep moisture readings, photos and equipment logs. Disputes over the number of drying days or how much material was removed are common, and they can be appraised once the loss is accepted.</p>
<h2>Flood is different</h2>
<p>Snowmelt flooding, ice jams and rain-on-snow events, like the June 2022 Yellowstone River flooding that hit Gardiner, Red Lodge and the Paradise Valley, are usually excluded from homeowners policies. Flood coverage typically comes from the National Flood Insurance Program or a private flood policy. Water that comes through the roof from an ice dam is treated differently from surface water rising into a basement, and that distinction matters.</p>
<h2>Estimating winter claims</h2>
<p>Snow load and ice dam claims can involve structural engineering, temporary shoring and repairs that must wait for spring. Good estimates account for:</p>
<ul>
<li>Engineering reports and stamped repair designs where required.</li>
<li>Shoring and snow removal before repairs can start.</li>
<li>Winter conditions, such as heating and protecting the work area.</li>
<li>Contractor travel to remote properties and short building seasons.</li>
</ul>
<p>Our <a href="/claim-toolkit/roof-snow-load-estimator/">roof snow load estimator</a> gives a rough sense of the weight on a roof, though it doesn’t replace an engineer.</p>
<h2>Documenting a winter loss</h2>
<p>Snow covers evidence and melt changes it. Photograph rooflines, eaves and icicles before anyone clears the roof, and take interior photos as stains spread. Note outdoor temperatures and the date heat was lost if a furnace failed. If you shut off water at a cabin, keep a record of when and how it was drained.</p>
<h2>Where appraisal helps</h2>
<p>Once your carrier accepts that snow load, ice dam or freezing damage is covered but disagrees on scope or price, appraisal can settle the amount. It won’t decide whether a collapse definition or freezing exclusion applies. See our <a href="/claim-services/snow-load-ice-dam-freeze-claims/">snow load, ice dam and freeze claims</a> service, and if you live in Gallatin County, our <a href="/montana-cities/bozeman/">Bozeman page</a>.</p>
""",
    },
    {
        "slug": "montana-unfair-claim-practices-overview",
        "title": "Montana Unfair Claim Practices: A General Overview",
        "seo": "Montana Unfair Claim Practices: A Plain Overview",
        "kw": "Montana unfair claim practices",
        "desc": "A cautious overview of Montana unfair claim practices rules, the CSI complaint process and when to talk to a licensed Montana attorney.",
        "summary": "A general, plain-language look at how Montana regulates claim handling, how to use the CSI complaint process and when to call an attorney. Not legal advice.",
        "date": "2026-10-22",
        "read": "7 min",
        "body": """
<h2>A general overview, not legal advice</h2>
<p>This article gives a plain-language overview of Montana unfair claim practices rules and how they relate to property claims. It is general information only. It is not legal advice, and we are not a law firm. If you think your claim has been handled unfairly, talk to a licensed Montana attorney about your situation.</p>
<h2>Where the rules come from</h2>
<p>Montana’s Unfair Trade Practices Act sits in Title 33, Chapter 18 of the Montana Code Annotated. Among other things, it lists unfair claim settlement practices that insurers doing business in Montana are expected to avoid. Montana law also allows an insured to bring a claim against their own insurer for certain of those practices. When and how that works, including what must be shown and what time limits apply, are legal questions for an attorney.</p>
<p>The regulator is the Office of the Montana Commissioner of Securities and Insurance, or CSI. The CSI is part of the State Auditor’s office, and the State Auditor serves as Commissioner. It licenses insurers and agents, takes consumer complaints and publishes consumer guidance.</p>
<h2>The kinds of conduct these laws address</h2>
<p>Without quoting or interpreting the statute, unfair claim practices laws like Montana’s generally address conduct such as:</p>
<ul>
<li>Misrepresenting facts or policy provisions about coverage.</li>
<li>Failing to acknowledge and act reasonably promptly on communications about a claim.</li>
<li>Failing to follow reasonable standards for investigating claims.</li>
<li>Refusing to pay a claim without conducting a reasonable investigation.</li>
<li>Not affirming or denying coverage within a reasonable time after proof of loss is completed.</li>
<li>Not attempting in good faith to settle promptly and fairly once liability is reasonably clear.</li>
<li>Failing to promptly explain the basis for a denial or a compromise offer.</li>
</ul>
<p>Read the statute itself, or ask an attorney, for the exact wording and how it has been applied. We don’t summarize court decisions here.</p>
<h2>A disagreement isn’t automatically unfair</h2>
<p>Many claim disputes are honest differences over price or scope. A carrier’s estimate coming in lower than your contractor’s bid doesn’t, by itself, mean the carrier acted unfairly. That kind of disagreement is exactly what the appraisal clause is designed to resolve. Concerns about Montana unfair claim practices tend to involve how a claim was handled: long delays, unexplained denials, ignored documentation or misstatements about the policy.</p>
<h2>How appraisal and claim-handling concerns fit together</h2>
<p>Appraisal decides the amount of loss. It generally doesn’t decide whether the insurer handled the claim properly. The two can exist side by side. Some policyholders go through appraisal and later talk to an attorney about claim handling; others consult an attorney first. Taking part in appraisal can affect other rights in ways that depend on the facts, which is one more reason to get legal advice early if you have concerns.</p>
<h2>Keep a record of claim handling</h2>
<p>Whatever path you choose, a clean record helps. Keep:</p>
<ul>
<li>A dated log of every call, email, letter and inspection, with names.</li>
<li>Copies of every estimate, reinspection report and payment letter.</li>
<li>Your written requests for explanations, and the carrier’s responses or lack of them.</li>
<li>Your policy, all endorsements and any certified copy you requested.</li>
</ul>
<p>Our <a href="/claim-toolkit/claim-deadline-calendar/">claim deadline calendar</a> helps you track dates from your own policy. It can’t tell you which legal deadlines apply; only an attorney can do that.</p>
<h2>Using the CSI complaint process</h2>
<p>If you believe an insurer isn’t handling your claim properly, you can file a complaint with the CSI. The office generally reviews the complaint, asks the insurer for a response and can help clarify what is expected of the company. A complaint isn’t a lawsuit and doesn’t replace legal advice, but it creates a record and sometimes gets a stalled claim moving. Check the CSI’s current website for its complaint form and instructions.</p>
<p>When you file, keep it factual: the claim number, the dates, what you asked for, what the carrier did and copies of key documents. Avoid speculation about motives and stick to what happened.</p>
<h2>When to call a licensed Montana attorney</h2>
<p>Consider talking to a licensed Montana attorney if:</p>
<ul>
<li>The carrier denies coverage or cites an exclusion you don’t understand.</li>
<li>You’ve gone a long time without a decision or a meaningful response.</li>
<li>The carrier raises a policy-condition defense, such as late notice or a missing proof of loss.</li>
<li>You believe the carrier misrepresented your policy.</li>
<li>Time limits in your policy or under Montana law may be approaching.</li>
</ul>
<p>Many attorneys offer an initial consultation. Bring your claim file, your policy and your log so the conversation can be specific.</p>
<h2>Where we fit, and where we don’t</h2>
<p>Our role is narrow. We value disputed property losses and work through the appraisal process as your appraiser or as a neutral umpire. We don’t evaluate whether an insurer broke the law, and we don’t pursue claims against insurers. If those questions come up during an appraisal, we’ll tell you it’s time to talk to a lawyer.</p>
<div class="note"><p>We are appraisers, not attorneys, and nothing here is legal advice. Learn more <a href="/about-our-firm/">about our firm</a>, or browse our <a href="/appraisal-questions/">appraisal questions</a>.</p></div>
""",
    },
    {
        "slug": "building-a-claim-file-before-appraisal",
        "title": "Building a Claim File Before Appraisal: A Montana Checklist",
        "seo": "Claim File Before Appraisal: A Montana Checklist",
        "kw": "claim file before appraisal",
        "desc": "Build a strong claim file before appraisal: policy documents, photos, a claim timeline, a marked-up estimate, bids and the numbers that matter.",
        "summary": "Appraisal panels decide numbers based on evidence. This checklist shows Montana policyholders what to gather before an appraisal starts and why each piece matters.",
        "date": "2026-11-04",
        "read": "7 min",
        "body": """
<h2>Why the file matters more than the argument</h2>
<p>Appraisal panels decide numbers based on evidence. An appraiser who arrives with dated photos, clean measurements, contractor pricing and a clear timeline usually moves the panel further than one who arrives with frustration. Building a claim file before appraisal is the most useful thing a Montana policyholder can do, and most of it costs nothing but time.</p>
<p>Here’s a practical checklist, organized the way an appraisal panel tends to look at a claim.</p>
<h2>1. The policy itself</h2>
<ul>
<li>The full policy, including every form and endorsement, not just the declarations page. If you don’t have it, ask the carrier in writing for a certified copy.</li>
<li>The appraisal clause, highlighted.</li>
<li>Deductibles, especially any percentage wind and hail deductible.</li>
<li>Endorsements that change valuation, such as roof payment schedules, cosmetic damage exclusions, ordinance or law coverage and extended replacement cost.</li>
</ul>
<h2>2. Proof of the loss and the date</h2>
<ul>
<li>Photos and video from right after the event, with dates. Wide shots first, then close-ups.</li>
<li>Weather information for your address: storm reports, hail size and wind data, or local news coverage.</li>
<li>Earlier photos of the property, such as real estate listing photos or inspection reports, that show its condition before the loss.</li>
<li>Records of any prior claims on the same part of the property.</li>
</ul>
<h2>3. The claim history</h2>
<p>Create a single timeline, starting with the date of loss and the date you reported it. Add every inspection, phone call, email, estimate, reinspection and payment, and note who you spoke with and what they said. Keep copies of every letter, especially any reservation of rights letter or partial denial. A clean timeline helps the panel understand where the numbers came from, and it also helps if questions about claim handling come up later.</p>
<h2>4. The carrier’s estimate, marked up</h2>
<p>Print the carrier’s estimate and go through it line by line. Mark items that are missing, quantities that look low and prices that seem out of line for your area. Common issues on Montana claims include:</p>
<ul>
<li>Missing roof slopes, elevations or rooms.</li>
<li>Low square counts or missing steep and high-roof charges.</li>
<li>Pricing that ignores contractor travel to rural properties or resort-area labor rates in places like Big Sky and Whitefish.</li>
<li>Missing overhead and profit when several trades are involved.</li>
<li>Depreciation that seems high for the age and condition of materials.</li>
</ul>
<p>An independent <a href="/claim-services/insurance-estimate-review/">insurance estimate review</a> can help you find gaps you might otherwise miss.</p>
<h2>5. Your own pricing</h2>
<p>Get at least one detailed contractor bid, itemized as far as possible. Lump-sum bids are hard to compare with a line-item estimate. If your contractor can produce an estimate in Xactimate or Symbility format, side-by-side comparison gets much easier. For discontinued materials, get a written statement from a supplier. For specialty work, such as log home restoration, standing-seam metal roofing or smoke remediation, a specialist’s bid carries more weight than a general one.</p>
<h2>6. Mitigation and emergency work</h2>
<p>Keep invoices, drying logs, moisture maps and photos from any mitigation company. Keep receipts for tarps, board-up, roof snow removal and your own emergency repairs. Many policies cover reasonable costs to prevent further damage, and these records show what was done and why.</p>
<h2>7. Contents and living expenses</h2>
<p>For contents, build an inventory with item descriptions, ages, quantities and replacement prices. For additional living expense, keep hotel and rental receipts, extra mileage and higher food costs, all with dates. A spreadsheet with one row per item is easier for a panel to work with than a stack of receipts.</p>
<h2>8. Know your numbers</h2>
<p>Before appraisal, calculate the gap between the carrier’s estimate and your documented number, and how much of that gap is depreciation you may recover later anyway.</p>
<div class="note"><p>Illustrative example: if the carrier’s replacement cost estimate is $30,000 and your contractor’s is $48,000, the gap is $18,000. If $6,000 of the carrier’s depreciation is recoverable after repairs, that changes the picture of what you would actually collect. All figures are illustrative.</p></div>
<p>Our <a href="/claim-toolkit/depreciation-holdback-calculator/">depreciation and holdback calculator</a> helps you sort out replacement cost, actual cash value and holdback.</p>
<h2>9. Check whether you’re ready</h2>
<p>Take our <a href="/claim-toolkit/appraisal-readiness-quiz/">appraisal readiness quiz</a> to see whether appraisal looks like a good fit or whether the claim needs more documentation or a different approach first. A claim file before appraisal doesn’t have to be perfect, but it should let a stranger understand what happened, what was paid and what’s still in dispute.</p>
<h2>Keep it organized</h2>
<p>Use one folder, paper or digital, with numbered sections that match this list. Name photos by date and location, such as “north slope” or “kitchen ceiling.” Send copies, never originals, and keep a record of what you sent and when.</p>
<h2>How we use your file</h2>
<p>When we act as your appraiser, we start with your file, inspect the property and build an estimate that can be defended line by line. A complete file saves time and often narrows the dispute before an umpire is ever involved. If you have questions about your claim, <a href="/get-in-touch/">get in touch</a>.</p>
""",
    },
]
