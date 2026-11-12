"""Learn-section copy for Missouri Insurance Appraiser: process guide, FAQ, glossary and posts."""

PROCESS_INTRO = '''<p>Most Missouri homeowners and commercial property policies contain an appraisal clause: a short paragraph that gives both sides a structured way forward when they agree a loss is covered but can’t agree on what it costs to fix. Instead of trading line items for months, each side picks an appraiser, the two appraisers pick an umpire, and a written award signed by any two of the three sets the amount of loss.</p>
<p>The stages below follow the order a typical Missouri claim moves through appraisal, from the first sign of a stalled negotiation to the check clearing. Your own policy’s wording controls every detail, including deadlines, who pays for what and whether appraisal applies to your claim at all, so keep a copy of the full policy handy as you read.</p>
<div class="note"><p>We are appraisers, not attorneys or public adjusters. Appraisal settles the dollar amount of a covered loss. It does not decide coverage, and nothing on this page is legal advice. For questions about denials, bad faith or lawsuits, talk with a Missouri attorney.</p></div>'''

PROCESS_STEPS = [
    ("Pin down the disagreement", '''<p>Appraisal answers one question: how much is the covered damage worth? Before you invoke it, make sure that’s really what you and the insurer are arguing about. Line up your contractor’s estimate beside the adjuster’s and mark every place they differ.</p>
<h3>Amount disputes that fit appraisal</h3>
<ul><li>Different unit prices for the same materials or labor</li><li>How many squares of roofing, how much drywall or which rooms need paint</li><li>Repair versus replace calls on damaged components</li><li>Whether overhead and profit belongs in the estimate</li></ul>
<h3>Disputes that usually don’t fit</h3>
<p>If the insurer says the damage isn’t covered at all, blames wear and tear, or has denied the claim outright, that’s a coverage question. Appraisal panels generally don’t decide coverage, and pushing a coverage fight into appraisal can waste months. A written denial letter is a good signal to reread your policy and consider talking with a Missouri attorney before going further.</p>'''),
    ("Read the appraisal clause", '''<p>Pull the full policy, not just the declarations page, and find the section titled “Appraisal,” usually among the conditions. Read it slowly. Wording varies between insurers and even between editions of the same company’s form.</p>
<h3>What to look for</h3>
<ul><li>Who can demand appraisal: either party, or only both by agreement</li><li>How the demand must be made, usually in writing</li><li>How many days each side has to name its appraiser, and how long the appraisers have to agree on an umpire</li><li>What happens if they can’t agree on an umpire, often a request to a court in the county where the property sits</li><li>How appraisal costs are split</li><li>Whether the insurer keeps the right to deny the claim after an award</li></ul>
<p>Also check the conditions on proof of loss, duties after loss and the time limit for filing suit. Appraisal doesn’t always pause those clocks, so write the dates down now. If anything in the clause is unclear, a Missouri attorney can tell you how it’s likely to be read.</p>'''),
    ("Send the written demand", '''<p>Once you’ve confirmed the dispute is about amount, put your request for appraisal in writing. A short, plain letter works better than a long argument. Send it to the adjuster and to the claim address in your policy or claim correspondence, and keep proof of delivery.</p>
<h3>What a demand usually includes</h3>
<ul><li>Your name, the property address, the policy number and the claim number</li><li>The date of loss and the cause, such as hail or wind</li><li>A statement that you dispute the amount of loss and are invoking the appraisal provision</li><li>The name and contact details of your appraiser, if you’ve already chosen one</li><li>A copy of your estimate or a short summary of the gap</li></ul>
<p>Stay factual and polite. The demand usually starts a clock that the policy defines, so note the date it’s received. Insurers can demand appraisal too; if you receive a demand, read the clause and respond within the stated time.</p>'''),
    ("Each side names an appraiser", '''<p>Each party picks its own appraiser within the window the policy sets. Many policies say something like 20 days after the written demand is received, but yours may say something different. Missing that window can cause real problems, so treat it as a firm deadline.</p>
<h3>Choosing yours</h3>
<p>Most clauses require each appraiser to be “competent” and also “independent,” “impartial” or “disinterested.” Those words are read differently from case to case, but at a minimum your appraiser should understand construction pricing and avoid any stake in the outcome your policy prohibits. Ask candidates directly:</p>
<ul><li>How they’re paid, and whether the fee depends on the size of the award</li><li>Whether they’ve worked on this property or for your contractor</li><li>How they build estimates and which pricing data they use</li><li>Whether they’ve handled claims in your part of Missouri</li></ul>
<p>The insurer names its appraiser in the same window. That may be an outside appraiser or someone the carrier works with often.</p>'''),
    ("Choosing the umpire", '''<p>Next, the two appraisers try to agree on an umpire: a neutral third person who only steps in if the appraisers can’t settle the number between themselves. Umpires are often experienced appraisers, contractors, engineers or former adjusters.</p>
<h3>When the appraisers can’t agree</h3>
<p>Most clauses say that if the appraisers can’t agree on an umpire within a set number of days, either side may ask a court to appoint one. In Missouri that generally means the circuit court for the county where the property is located, whether that’s one of the 114 counties or the independent City of St. Louis. That request is a court filing, so many people bring in an attorney for that step.</p>
<h3>What a good umpire brings</h3>
<ul><li>No ties to either party or either appraiser</li><li>Working knowledge of local repair costs</li><li>A clear, even-handed way of receiving each side’s position</li><li>A willingness to look at the property, not just the paperwork</li></ul>'''),
    ("Inspection and competing estimates", '''<p>With the panel in place, the appraisers inspect the property, often together. On a roof that means walking the slopes, measuring and photographing damage. Inside, it can mean moisture readings, room measurements and a close look at finishes that may need to match.</p>
<h3>Building the estimates</h3>
<p>Each appraiser prepares a line-item estimate, usually in software such as Xactimate with a price list for the local market. The two estimates are then compared line by line. Expect discussion about:</p>
<ul><li>Quantities: squares, linear feet and square footage</li><li>Repair methods and whether code upgrades are triggered</li><li>Matching siding, shingles or flooring that can’t be sourced</li><li>Labor minimums, steep and high charges, and overhead and profit</li></ul>
<h3>Your role</h3>
<p>Your part is usually to give access, share receipts and photos, and answer questions about the property’s condition before the loss. Keep a copy of everything you hand to the panel.</p>'''),
    ("Negotiation and the award", '''<p>Many appraisals finish without the umpire ever weighing in. The two appraisers work through their differences, trade documentation and reach a number. When they agree, they sign a written award and send it to both parties.</p>
<h3>If the umpire is needed</h3>
<p>When the appraisers can’t agree on certain items, they submit just those differences to the umpire. The umpire reviews both positions, may visit the property, and then joins one appraiser on each disputed figure or sets a figure in between. Under most clauses, a written agreement signed by any two of the three sets the amount of loss.</p>
<h3>What the award usually shows</h3>
<ul><li>Replacement cost value and actual cash value, often split by dwelling, other structures and contents</li><li>Depreciation, where the policy allows it</li><li>Notes on any items the panel didn’t value because coverage is disputed</li></ul>
<p>An award typically doesn’t subtract the deductible or prior payments. The insurer applies those when it pays.</p>'''),
    ("Payment and what follows", '''<p>After the award, the insurer applies the policy terms: it subtracts the deductible and any earlier payments and issues payment, often with your mortgage company named on the check. The timing is usually set in the policy’s loss payment condition, so read that section and follow up in writing if payment runs late.</p>
<h3>Common next steps</h3>
<ul><li>Collect recoverable depreciation by finishing repairs and sending invoices within the policy’s time limit</li><li>Endorse and deposit lender-named checks through your mortgage company’s process</li><li>Pay your appraiser and your share of the umpire’s fee as the policy describes</li><li>File the award, estimates and photos with your permanent records</li></ul>
<h3>If problems continue</h3>
<p>An award usually settles the amount, but it may not end every issue. If the insurer won’t pay the award, raises a new coverage defense or delays without explanation, that’s a legal matter. Talk with a Missouri attorney. You can also file a complaint with the Missouri Department of Commerce and Insurance.</p>'''),
]

PROCESS_OUTRO = '''<h2>When appraisal is the wrong tool</h2>
<p>Appraisal is good at one job, and forcing it into others usually costs time and money. Think twice before demanding it when:</p>
<ul><li>The claim has been denied outright, or the insurer says the cause of loss is excluded</li><li>The insurer is alleging misrepresentation or fraud</li><li>The gap between estimates is small enough that appraisal fees would eat most of it</li><li>A suit limitation deadline is close and your policy doesn’t clearly pause it</li><li>The insurer hasn’t yet had a fair chance to see the damage or your documentation</li></ul>
<p>In those situations, a Missouri attorney or a simple reinspection request is often the better first move. If you’re not sure which kind of dispute you have, an independent estimate review can help separate amount questions from coverage questions before you commit to anything.</p>'''

FAQ = [
    ("Appraisal basics", [
        ("What is insurance appraisal?",
         "It’s a process written into most property policies for resolving disagreements over the amount of a covered loss. Each side names an appraiser, the appraisers choose an umpire, and a written award signed by any two of the three sets the amount."),
        ("Is an appraiser the same as a public adjuster?",
         "No. A public adjuster is licensed to represent a policyholder in handling the whole claim, while an appraiser serves within the appraisal process to help determine the amount of loss. We are appraisers, not public adjusters or attorneys."),
        ("Does appraisal decide whether my damage is covered?",
         "Generally no. Appraisal sets the dollar amount of the loss, while coverage questions are left to the insurer and, if disputed, the courts. Your policy wording and Missouri law control where that line falls."),
        ("Can my insurer refuse to go to appraisal?",
         "It depends on the policy. Some clauses let either party demand appraisal, while others require both sides to agree. If an insurer refuses a demand under a clause that reads as mandatory, a Missouri attorney can explain your options."),
        ("Is the appraisal award binding?",
         "Most clauses say an award signed by two of the three panel members is binding on the amount of loss. Awards can sometimes be challenged in court on narrow grounds, which is a question for an attorney."),
    ]),
    ("Costs and timing", [
        ("Who pays for appraisal?",
         "Most policies say each side pays its own appraiser and the two sides split the umpire’s fee and other appraisal expenses equally. Wording varies, so check your policy."),
        ("How are appraisers usually paid?",
         "Common arrangements include hourly rates and flat fees, and some appraisers charge a percentage of the award. Some policies and courts view contingency fees as a concern for impartiality, so ask about fees up front and compare them with your policy’s requirements."),
        ("How long does appraisal take in Missouri?",
         "A straightforward roof claim can wrap up in a few weeks, while a large or complicated loss can take several months. After a major hail or tornado event, busy schedules can slow inspections and umpire selection."),
        ("Is there a deadline to demand appraisal?",
         "Some policies set one and some don’t, but never assume time is unlimited. Policies also commonly include a suit limitation clause that appraisal may not pause, so track every date and talk with an attorney if one is close."),
        ("Is appraisal worth it when the gap is small?",
         "Sometimes not. If the difference between estimates is only a little more than the expected fees, a reinspection request or direct negotiation may make more sense."),
    ]),
    ("Missouri rules and agencies", [
        ("Who regulates insurance companies in Missouri?",
         "The Missouri Department of Commerce and Insurance (DCI) licenses insurers and adjusters, handles consumer complaints and enforces the state’s insurance laws, including its rules on unfair claims practices."),
        ("How do I file a complaint against my insurer in Missouri?",
         "You can file a consumer complaint with the DCI, which typically contacts the insurer and asks for a response. A complaint doesn’t decide your claim, but it creates an official record and can prompt a closer look."),
        ("What is vexatious refusal?",
         "It refers to Missouri statutes, including RSMo 375.296 and 375.420, that may allow added penalties and attorney fees when an insurer refuses to pay a claim without reasonable cause. Whether they apply to a situation is a legal question for a Missouri attorney."),
        ("Does Missouri have a wind pool for homeowners?",
         "No. Missouri has no coastal wind pool. The Missouri FAIR Plan, formally the Missouri Property Insurance Placement Facility, offers basic property coverage to owners who can’t get it in the standard market."),
        ("Does my homeowners policy cover flooding?",
         "Standard homeowners policies typically exclude flood and surface water. Flood coverage usually requires a separate flood insurance policy, which is worth considering near the Missouri and Mississippi rivers and in other low-lying areas."),
    ]),
    ("Storm and peril questions", [
        ("When is hail season in Missouri?",
         "Hail can fall in nearly any month, but the most active stretch generally runs from spring into early summer. Damage often isn’t noticed until a later inspection or leak, so check your policy’s reporting requirements."),
        ("What is a percentage wind/hail deductible?",
         "It’s a deductible figured as a percentage of your dwelling limit rather than a flat dollar amount. On an illustrative $300,000 dwelling limit, a 2% deductible would be $6,000."),
        ("Are tornado and straight-line wind damage treated differently?",
         "Most homeowners policies cover windstorm generally, so tornado and straight-line wind damage are usually handled the same way. Disputes tend to center on scope, matching and cost rather than the kind of wind."),
        ("Is sinkhole damage covered?",
         "Many policies exclude earth movement, which can include sinkholes, though some provide limited collapse or sinkhole coverage or offer an endorsement. Appraisal can only value damage the insurer has accepted as covered."),
        ("Do I need separate earthquake coverage in Missouri?",
         "Usually, yes. Standard homeowners policies typically exclude earthquake, and coverage is commonly added by endorsement, which many owners consider given the New Madrid seismic zone in southeast Missouri."),
        ("Is ice storm damage covered?",
         "Weight of ice and falling trees are commonly covered causes of loss, though details vary by policy. Ice dams that push water under shingles can raise separate questions about how the policy treats water damage."),
    ]),
    ("After the award", [
        ("How soon will I be paid after the award?",
         "Many policies say payment is due within a set number of days after an award or agreement. Check the loss payment condition in your policy and follow up in writing if payment is late."),
        ("Why is my mortgage company on the check?",
         "Most policies include a mortgagee clause that protects the lender’s interest in the property. Larger checks may go into a lender-controlled account and be released as repairs progress."),
        ("How do I collect recoverable depreciation?",
         "Under many replacement cost policies, the insurer pays actual cash value first and releases the withheld depreciation after repairs are complete. Send final invoices and photos within the time your policy allows."),
        ("Can the insurer still deny the claim after an award?",
         "Some policies reserve the insurer’s right to deny coverage even after appraisal. If that happens, the issue is coverage rather than amount, and a Missouri attorney is the right person to ask."),
        ("What if more damage turns up after the award?",
         "Hidden damage found during repairs may be handled as a supplement or a separate claim, depending on the policy and what the award covered. Report it promptly and photograph it before it’s covered up."),
    ]),
]

GLOSSARY = [
    ("Actual cash value (ACV)", "The value of damaged property at the time of loss, usually figured as replacement cost minus depreciation. Some policies define it differently, so check yours."),
    ("Replacement cost value (RCV)", "The cost to repair or replace damaged property with materials of like kind and quality, without subtracting depreciation."),
    ("Recoverable depreciation", "Depreciation withheld from the first payment under a replacement cost policy that can be collected once repairs or replacement are finished, within the policy’s time limit."),
    ("Holdback", "A common name for the recoverable depreciation an insurer keeps back until repairs are complete."),
    ("Appraisal clause", "The policy provision that lets the parties resolve a disagreement over the amount of loss through two appraisers and an umpire instead of in court."),
    ("Umpire", "A neutral third person chosen by the two appraisers, or appointed by a court, who decides the items the appraisers can’t agree on."),
    ("Amount of loss", "The dollar value of covered damage. It’s the question appraisal is designed to answer."),
    ("Appraisal award", "The written decision signed by at least two of the three panel members that sets the amount of loss."),
    ("Proof of loss", "A sworn statement of the amount claimed and the details of the loss, which many policies require within a set time after the insurer asks for it."),
    ("Declarations page", "The summary page of a policy listing the insured, the property, coverages, limits, deductibles and endorsements."),
    ("Deductible", "The part of a covered loss the policyholder bears, subtracted after the loss has been valued."),
    ("Percentage deductible", "A deductible calculated as a percentage of a coverage limit, usually the dwelling limit, rather than a flat dollar amount."),
    ("Wind/hail deductible", "A separate deductible for wind or hail losses, often written as a percentage of the dwelling limit in Missouri policies."),
    ("Overhead and profit (O&P)", "Allowances for a general contractor’s business costs and profit, often figured as percentages of an estimate, when a repair needs several trades coordinated."),
    ("Line-item estimate", "An estimate that lists each repair task separately with its quantity, unit price and total, so two estimates can be compared item by item."),
    ("Xactimate", "Estimating software widely used by insurers, adjusters and contractors that applies regional price lists to line-item repair estimates."),
    ("Square (roofing)", "A unit of roof area equal to 100 square feet."),
    ("Pitch", "The steepness of a roof, written as inches of rise per 12 inches of horizontal run, such as 6/12. Steeper roofs usually cost more to repair."),
    ("Matching", "The question of whether replacement materials must reasonably match undamaged areas in color, texture or style, and what happens when they can’t. Policy wording controls."),
    ("Ordinance or law coverage", "Coverage for added costs to bring repaired or rebuilt property up to current building codes, often limited to a percentage of the dwelling limit."),
    ("Loss of use / ALE", "Coverage for additional living expenses, such as temporary housing and extra meal costs, when a covered loss makes the home unlivable."),
    ("Coinsurance", "A clause, common in commercial policies, that can reduce payment when property is insured for less than a required percentage of its value."),
    ("Collapse coverage", "A narrow additional coverage for abrupt collapse caused by listed perils, such as hidden decay or the weight of ice and snow. Settling and cracking are typically excluded."),
    ("Earth movement exclusion", "A standard exclusion for losses caused by earthquake, landslide, subsidence, sinkholes and other shifting of the ground, subject to any exceptions the policy lists."),
    ("Sinkhole", "A depression or opening that forms when soil or rock drops into a void below, often where bedrock has dissolved."),
    ("Karst", "A landscape shaped by dissolving bedrock such as limestone and dolomite, marked by caves, springs and sinkholes. Large parts of Missouri, especially the Ozarks, are karst."),
    ("Mine subsidence", "Sinking of the ground caused by the failure of old underground mine workings. Standard policies generally exclude it unless specific coverage is added."),
    ("Surface water", "Water on the ground from rain or snowmelt that hasn’t entered a defined channel. Homeowners policies commonly exclude it along with flood."),
    ("Sewer/drain backup endorsement", "An add-on that covers damage from water backing up through sewers or drains, which standard policies usually exclude."),
    ("Mitigation", "Reasonable steps taken after a loss to prevent further damage, such as tarping a roof or drying out wet rooms. Most policies require it."),
    ("Supplement", "A request for additional payment for damage or costs found after the original estimate, often once repairs begin."),
    ("Scope of loss", "The description of what was damaged and what work is needed to repair it, before any pricing is applied."),
    ("Reservation of rights", "A letter in which the insurer keeps handling a claim while reserving the right to deny coverage later for stated reasons."),
    ("Suit limitation clause", "A policy provision setting how long you have to file a lawsuit against the insurer. Deadlines vary, and appraisal may not pause them."),
    ("Vexatious refusal", "A Missouri legal claim under statutes such as RSMo 375.296 and 375.420 that may allow added penalties and attorney fees when an insurer refuses to pay without reasonable cause. Whether it applies is a question for a Missouri attorney."),
    ("Missouri Department of Commerce and Insurance (DCI)", "The state agency that regulates insurers and adjusters doing business in Missouri and accepts consumer complaints."),
    ("Missouri FAIR Plan", "The common name for the Missouri Property Insurance Placement Facility, which provides basic property coverage to owners who can’t obtain it in the standard market."),
    ("Derecho", "A widespread, long-lived windstorm driven by a fast-moving line of thunderstorms, such as the July 2006 derecho that caused widespread damage and outages in the St. Louis area."),
    ("Straight-line wind", "Damaging thunderstorm winds that blow in one general direction, unlike the rotating winds of a tornado. Policies usually treat both as windstorm."),
    ("Functional vs. cosmetic damage", "Functional damage affects a component’s ability to do its job, such as shedding water, while cosmetic damage affects appearance only. Some policies exclude cosmetic damage to roofs or siding."),
    ("Ice dam", "A ridge of ice along a roof’s edge that traps melting snow, which can back up under shingles and leak into the home."),
    ("Contents inventory", "A room-by-room list of damaged or destroyed personal property, with descriptions, ages, quantities and values."),
    ("Independent appraiser", "An appraiser hired by one party under the appraisal clause who must still meet the policy’s standard of independence or impartiality."),
    ("Disinterested and competent", "Common policy wording for appraiser qualifications: competent means able to value the loss, and disinterested generally means having no improper stake in the outcome. How these words are applied can vary."),
    ("Mortgagee clause", "A policy provision protecting the lender’s interest in the insured property, which is why lenders are often named on claim checks."),
    ("Depreciation", "The reduction in value of property due to age, wear and condition, used to figure actual cash value."),
    ("Named-peril policy", "A policy that covers only the causes of loss it specifically lists, as opposed to an open-peril policy that covers everything not excluded."),
]

POSTS = [
    {
        "slug": "missouri-appraisal-clause-walkthrough",
        "title": "How the Appraisal Clause Works in a Typical Missouri Homeowners Policy",
        "seo": "Missouri Appraisal Clause: How It Works",
        "desc": "A plain walkthrough of the appraisal clause in a typical Missouri homeowners policy: the demand, deadlines, umpire, award and what it won’t decide.",
        "summary": "Follow a typical appraisal clause from the written demand to the signed award, and learn which questions the panel can’t answer.",
        "date": "2026-09-03",
        "read": "8 min",
        "body": '''<p>Most Missouri homeowners never read the appraisal clause until a claim stalls. Then it suddenly matters a great deal. This walkthrough follows a typical clause from the demand to the award, explains what each step means in practice, and flags the places where your own policy may say something different.</p>
<h2>Where the clause lives and what it says</h2>
<p>In a typical homeowners policy, appraisal appears in the conditions section, often near “Loss Settlement” and “Suit Against Us.” The language usually runs only a paragraph or two, but every sentence does work. A common version says that if you and the insurer fail to agree on the amount of loss, either may demand appraisal in writing; each party then chooses a competent, impartial appraiser within a set period; the appraisers choose an umpire; and an award agreed to by any two sets the amount of loss.</p>
<p>That’s the typical shape, not a promise about your policy. Some forms require both parties to agree before appraisal can begin. Some describe the appraisers as “disinterested” or “independent.” Some add language preserving the insurer’s right to deny the claim afterward. Read the exact words in your policy before relying on any summary, including this one.</p>
<h2>Step one: a real disagreement over amount</h2>
<p>The clause is triggered by a failure to agree on the amount of loss. That usually means the insurer has accepted at least part of the claim and issued an estimate, and you have a competing estimate showing a higher cost. If the insurer hasn’t finished investigating, or has denied the claim entirely, there may not yet be an amount dispute to appraise.</p>
<p>Before you demand appraisal, it helps to have:</p>
<ul><li>The insurer’s estimate and any payment letters</li><li>Your contractor’s or appraiser’s line-item estimate</li><li>Photos, measurements and any engineering or inspection reports</li><li>A short list of the main differences, such as roof quantities, matching or overhead and profit</li></ul>
<p>An <a href="/appraisal-help/insurer-estimate-review/">independent review of the insurer’s estimate</a> can show whether the gap is big enough to justify the cost of appraisal.</p>
<h2>Step two: the written demand and the clock it starts</h2>
<p>The demand should be in writing and sent in a way you can prove. It identifies the claim, states that you dispute the amount of loss and invokes the appraisal provision. Many people name their appraiser in the same letter.</p>
<p>The demand typically starts the first deadline. Policy language often gives each side 20 days to name an appraiser, though some policies use a different number, and many measure it from when the other side receives the demand rather than when it was sent. Standard wording then commonly gives the appraisers another set period to agree on an umpire. Put these dates on a calendar the day the demand goes out. Our <a href="/toolkit/claim-calendar-builder/">claim calendar builder</a> can help you lay them out next to proof-of-loss and suit deadlines.</p>
<div class="note"><p>Appraisal doesn’t necessarily stop other policy deadlines from running, including the time limit for filing suit. If a deadline is close, talk with a Missouri attorney before relying on appraisal.</p></div>
<h2>Step three: appraisers, the umpire and the inspection</h2>
<p>Each appraiser should meet the clause’s standard, usually “competent” plus “impartial,” “independent” or “disinterested.” Ask any candidate how they’re paid and whether they have ties to you, your contractor or the insurer. Those questions matter if the award is ever challenged.</p>
<p>The two appraisers then pick an umpire. If they can’t agree in time, the clause usually lets either party ask a court of record in the state where the property is located to appoint one. In Missouri that generally means the circuit court for the county where the home sits, or the City of St. Louis if the property is there.</p>
<p>Next comes the inspection. The appraisers measure, photograph and test, then build line-item estimates. Expect them to exchange those estimates and talk through the differences item by item, with each side supplying receipts, photos and contractor input as needed.</p>
<h2>Step four: the award and what “binding” means</h2>
<p>If the two appraisers agree, they sign an award. If they can’t, they send their differences to the umpire, and agreement by any two of the three sets the amount. The award often lists replacement cost and actual cash value separately, and it may break the numbers out by coverage, such as dwelling, other structures and contents.</p>
<p>Most clauses describe the award as binding on the amount of loss. In practice, that means neither side can simply reopen the numbers because it dislikes them. Awards can sometimes be challenged on narrow grounds, such as a panel member who wasn’t impartial or a panel that stepped outside its role. Those are legal questions for a Missouri attorney.</p>
<p>The award usually doesn’t subtract your deductible or prior payments. The insurer applies those when it pays. Our <a href="/toolkit/award-net-payout-estimator/">award net payout estimator</a> shows how those deductions typically work.</p>
<h2>What the clause does not decide</h2>
<p>Appraisal is about amount. In general, it doesn’t decide:</p>
<ul><li>Whether a cause of loss is covered or excluded</li><li>Whether you met your duties after loss, such as prompt notice</li><li>Whether the insurer acted in bad faith or refused to pay without reasonable cause</li><li>How policy language should be read when the two sides interpret it differently</li></ul>
<p>Some disputes blur the line, such as whether damage came from the storm or from age. Panels and courts handle those mixed questions in different ways, and policy wording matters. When coverage is the main fight, appraisal may be the wrong first step.</p>
<h2>A practical checklist</h2>
<ol><li>Read the full appraisal clause and the suit limitation clause.</li><li>Confirm the insurer has accepted coverage for at least part of the loss.</li><li>Gather competing estimates and supporting photos.</li><li>Send a dated written demand and keep proof of delivery.</li><li>Name a qualified, impartial appraiser within the policy’s window.</li><li>Track the umpire deadline and every other policy date.</li><li>Keep copies of everything you give the panel.</li></ol>
<p>Nothing here is legal advice, and your policy controls. If you’d like help with the demand or want an appraiser on your side, see our <a href="/appraisal-help/appraisal-demand-representation/">appraisal demand representation</a> page.</p>''',
    },
    {
        "slug": "hail-claims-missouri-roofs",
        "title": "Documenting Hail Damage on Missouri Roofs: Evidence, Matching and Deductibles",
        "seo": "Hail Damage on Missouri Roofs: What to Document",
        "desc": "How to document hail damage on a Missouri roof: soft-metal evidence, test squares, matching, cosmetic damage exclusions and percentage deductibles.",
        "summary": "What to photograph after a Missouri hailstorm, why matching and cosmetic exclusions cause fights, and how percentage deductibles change the math.",
        "date": "2026-09-17",
        "read": "8 min",
        "body": '''<p>Hail is one of the most common reasons Missouri homeowners file property claims, and roof damage is one of the most common reasons those claims end up in dispute. The trouble is rarely whether hail fell. It’s usually how much damage it did, whether that damage counts under your policy and what a proper repair costs. Good documentation, gathered early, answers most of those questions before they turn into arguments.</p>
<h2>Missouri’s hail season and why timing matters</h2>
<p>Hail can fall in Missouri in almost any month, but the busiest stretch generally runs from spring into early summer, when strong thunderstorms track across the state. The St. Louis area has seen some memorable events. The April 10, 2001 hailstorm along the I-70 corridor is often cited as one of the costliest hail events in the region’s history, battering roofs, siding and vehicles across a wide swath of the metro.</p>
<p>Timing matters for two reasons. First, many policies require prompt notice of a loss, and some set a specific window for reporting wind or hail claims. Second, Missouri roofs often take more than one hit over a few years. The longer you wait, the harder it becomes to show which storm caused which damage. Note the date of the storm, save local weather reports and photograph your roof and yard as soon as it’s safe.</p>
<h2>What to document on the roof and around the house</h2>
<p>Adjusters and appraisers look for a consistent pattern of damage that fits a specific storm. Help them see it.</p>
<h3>Soft metals and collateral damage</h3>
<p>Dents in soft metals are some of the clearest evidence of hail size and direction. Photograph:</p>
<ul><li>Gutters, downspouts and roof vents</li><li>Ridge vents, flashing and chimney caps</li><li>Window wraps, air-conditioner fins and metal mailboxes</li><li>Spatter marks on painted surfaces, decks and fences</li></ul>
<p>Put a coin or tape measure in the frame for scale, and note which side of the house each photo comes from.</p>
<h3>Test squares and shingle hits</h3>
<p>Many inspectors mark a 10-by-10-foot test square on each slope and count the hail hits inside it. On asphalt shingles, look for bruises that feel soft when pressed, granule loss that exposes the mat and fractures in the fiberglass. On wood shakes, look for fresh splits with sharp, unweathered edges. Take close-up and wide shots of each test square, and write down the count for each slope. Only climb a roof if you can do it safely; otherwise let a qualified contractor or appraiser handle it.</p>
<h2>Matching and discontinued shingles</h2>
<p>A common fight on Missouri roofs is what happens when damaged shingles can’t be matched. The color may have faded, the product may be discontinued or the profile may have changed. Insurers sometimes propose repairing only the damaged slopes, while homeowners often argue that a patchwork roof isn’t a reasonable repair.</p>
<p>How this plays out depends on your policy wording and the facts. Helpful evidence includes the shingle brand and product line (sometimes printed on a wrapper left in the attic), a supplier’s written statement that the product is discontinued and photos showing the visible difference between old and new. In appraisal, the panel can consider what repair is needed to restore the roof, but matching questions sometimes overlap with coverage, so read the policy closely.</p>
<h2>Functional versus cosmetic damage</h2>
<p>Some Missouri policies, especially newer ones, include a cosmetic damage exclusion or endorsement for roofs. These provisions generally exclude damage that changes how a roof looks without affecting its ability to keep water out, such as small dents in metal roofing or certain marks on shingles.</p>
<p>If your policy has this language, focus your documentation on function: fractured mats, punctures, broken seals, granule loss that exposes the asphalt and any active leaks. Whether a particular dent or mark is cosmetic can be a coverage question rather than an amount question. If the insurer is relying on a cosmetic exclusion to deny the roof, that dispute may need a different path than appraisal, and a Missouri attorney can help you understand it.</p>
<h2>Percentage wind/hail deductibles</h2>
<p>Many Missouri policies use a separate wind/hail deductible written as a percentage of your dwelling limit instead of a flat dollar amount. That can make a big difference in what you actually receive.</p>
<div class="table-wrap"><table><thead><tr><th>Illustrative dwelling limit</th><th>1% deductible</th><th>2% deductible</th></tr></thead><tbody><tr><td>$200,000</td><td>$2,000</td><td>$4,000</td></tr><tr><td>$300,000</td><td>$3,000</td><td>$6,000</td></tr><tr><td>$400,000</td><td>$4,000</td><td>$8,000</td></tr></tbody></table></div>
<p>These figures are illustrative only. Check your declarations page for your actual deductible, or plug your own numbers into our <a href="/toolkit/hail-deductible-calculator/">hail deductible calculator</a>.</p>
<p>The deductible doesn’t change the amount of loss. It’s subtracted after the loss is valued, so it matters most when you’re deciding whether a modest gap between estimates is worth pursuing.</p>
<h2>When a hail claim belongs in appraisal</h2>
<p>Appraisal fits best when the insurer agrees there’s hail damage but disputes how much. Common examples include disagreements over the number of squares, whether the whole roof or only some slopes need replacement, waste factors, steep-roof charges, and overhead and profit. If the insurer says there’s no hail damage at all, or relies on an exclusion, coverage may need to be resolved first.</p>
<p>To see how we approach these disputes, visit our <a href="/appraisal-help/hail-roof-damage-appraisal/">hail and roof damage appraisal</a> page. Nothing here is legal advice, and your policy wording controls.</p>''',
    },
    {
        "slug": "vexatious-refusal-vs-appraisal",
        "title": "Appraisal vs. a Vexatious Refusal Claim in Missouri: What Each One Is For",
        "seo": "Vexatious Refusal vs. Appraisal in Missouri",
        "desc": "Appraisal settles the amount of a covered loss; a Missouri vexatious refusal claim is a legal matter. Learn the difference and when to call a lawyer.",
        "summary": "Appraisal answers “how much?” Missouri’s vexatious refusal statutes raise a different, legal question. Here’s how to tell which one you’re facing.",
        "date": "2026-10-01",
        "read": "7 min",
        "body": '''<p>When a Missouri property claim goes sideways, homeowners often hear two very different terms: appraisal and vexatious refusal. They sometimes come up in the same conversation, but they do different jobs. One is a policy process for settling the dollar amount of a covered loss. The other is a legal claim under Missouri statutes. Knowing which one fits your situation can save time and help you call the right professional first.</p>
<div class="note"><p>We are insurance appraisers, not attorneys. This article describes general concepts only and isn’t legal advice. Whether a vexatious refusal claim exists in your situation is a legal question for a licensed Missouri attorney.</p></div>
<h2>What appraisal is for</h2>
<p>Appraisal is a contract provision found in most Missouri homeowners and commercial property policies. When you and the insurer agree the loss is covered, at least in part, but disagree on the amount, either side can typically demand appraisal. Each side names an appraiser, the appraisers choose an umpire and an award signed by any two sets the amount of loss.</p>
<p>Appraisal is useful for disputes such as:</p>
<ul><li>How many squares of roofing need replacement</li><li>Whether damaged siding or flooring can be matched</li><li>Unit prices for labor and materials</li><li>Whether overhead and profit belongs in the estimate</li></ul>
<p>What appraisal generally doesn’t do is decide whether the loss is covered, whether the insurer acted reasonably or whether any penalties are owed. Those questions sit outside the panel’s role. Our <a href="/appraisal-roadmap/">appraisal roadmap</a> walks through the process step by step.</p>
<h2>What a vexatious refusal claim is</h2>
<p>Missouri has statutes, including RSMo 375.296 and 375.420, that address an insurer’s refusal to pay a loss without reasonable cause or excuse. In general terms, where those statutes apply, a court may allow damages beyond the policy benefits, including a percentage-based penalty set by statute and a reasonable attorney fee.</p>
<p>These claims are brought in court, not in appraisal. They typically turn on questions such as whether the insurer’s refusal was willful and without reasonable cause, what the insurer knew and when, and whether there was a genuine dispute over the facts or the law. Courts look closely at the specific circumstances, and the outcome depends heavily on evidence and procedure. That’s attorney territory.</p>
<p>It’s also worth knowing that a disagreement isn’t automatically vexatious. Insurers are generally allowed to contest claims where there’s an honest, reasonable dispute. Whether a particular refusal crosses the line is exactly the kind of judgment a Missouri attorney should make.</p>
<h2>How the two can interact</h2>
<p>Appraisal and a vexatious refusal claim aren’t necessarily either-or, but neither replaces the other. A few general points:</p>
<ul><li>An appraisal award settles the amount of loss under the policy. It doesn’t, by itself, decide whether the insurer’s conduct was reasonable.</li><li>How an insurer behaves around appraisal, such as long delays in naming an appraiser or paying an award, can sometimes become part of the factual picture in a later dispute. How a court would view it is a legal question.</li><li>Starting appraisal may affect timing, strategy or other legal rights. That’s one reason to get legal advice first if you think a statutory claim might be in play.</li></ul>
<p>In short, appraisal answers “how much?” A vexatious refusal claim asks whether the insurer refused to pay without reasonable cause, and what follows from that.</p>
<h2>When to call a lawyer before an appraiser</h2>
<p>Consider talking with a Missouri attorney first if:</p>
<ul><li>The insurer denied the claim entirely or says the damage is excluded</li><li>The insurer has stopped responding, or keeps asking for the same documents without explanation</li><li>You’ve been accused of misrepresentation or fraud</li><li>The insurer has sent a reservation of rights letter</li><li>The insurer won’t pay an appraisal award that has already been signed</li><li>A suit limitation deadline in your policy is approaching</li></ul>
<p>In these situations, the main fight probably isn’t about line items. An attorney can explain your rights under Missouri law and whether appraisal is still a useful step.</p>
<h2>When appraisal is the sensible next step</h2>
<p>Appraisal tends to make sense when the insurer has accepted coverage, has paid or offered something and has stayed reasonably responsive, but the numbers are far apart. In those cases, a panel of appraisers who understand construction pricing is often a faster, less expensive way to close the gap than litigation.</p>
<p>Before you demand appraisal, an <a href="/appraisal-help/insurer-estimate-review/">independent estimate review</a> can confirm the dispute is really about amount and show where the gaps are.</p>
<h2>The Department of Commerce and Insurance complaint process</h2>
<p>Separately from appraisal or any lawsuit, you can file a consumer complaint with the Missouri Department of Commerce and Insurance (DCI). The department regulates insurers doing business in Missouri and enforces the state’s unfair claims practices rules, which generally deal with things like prompt communication, reasonable investigation and fair settlement conduct.</p>
<p>In general, the DCI forwards a complaint to the insurer, asks for a written response and reviews it. A complaint doesn’t decide the amount of your claim and isn’t a substitute for legal advice, but it creates an official record and can encourage an insurer to take a closer look. Keep copies of your letters, emails, estimates and claim notes; a clear timeline helps whichever path you choose.</p>
<p>If you’d like to talk through whether your dispute is about amount, you can <a href="/get-in-touch/">get in touch</a>. If it turns out to be a legal problem, we’ll say so.</p>''',
    },
    {
        "slug": "tornado-rebuild-total-loss",
        "title": "Rebuilding After a Missouri Tornado: Total Losses, Code Upgrades and Valuation Disputes",
        "seo": "Rebuilding After a Missouri Tornado Total Loss",
        "desc": "What Missouri homeowners should know when a tornado causes a total loss: debris removal, code upgrades, contents, ALE and why valuations get disputed.",
        "summary": "A practical look at total-loss tornado claims in Missouri, from debris removal and code upgrades to contents, living expenses and appraisal.",
        "date": "2026-10-15",
        "read": "8 min",
        "body": '''<p>Tornadoes are a fact of life across Missouri, and the state has seen some of the most destructive storms in modern memory. The Joplin tornado of May 22, 2011 leveled large parts of that city, and the Jefferson City tornado of May 22, 2019 damaged homes and businesses across the capital. For owners whose homes are destroyed or heavily damaged, the insurance claim becomes a long project of its own. Knowing where valuation disputes tend to arise can help you prepare.</p>
<h2>What a total loss means under your policy</h2>
<p>“Total loss” sounds simple, but it can mean different things. A home may be physically destroyed, or it may still be standing but damaged so badly that repair would cost more than rebuilding. Either way, the policy’s loss settlement provisions decide how the claim is paid.</p>
<p>Key items to check on your declarations page and in the policy include:</p>
<ul><li>The dwelling limit and whether it was kept up to date</li><li>Whether the dwelling is insured for replacement cost or actual cash value</li><li>Any extended replacement cost endorsement</li><li>Whether you must rebuild, and where, to receive full replacement cost</li></ul>
<p>Many replacement cost policies pay actual cash value first and release the rest, often called recoverable depreciation or holdback, after you rebuild. Some limit how long you have to finish. Note those deadlines early, because a full rebuild can take a long time.</p>
<h2>Debris removal and site costs</h2>
<p>After a tornado, cleanup can be a major expense: hauling away what remains of the house, removing fallen trees and clearing the foundation. Many policies include debris removal within the dwelling limit, with a modest additional amount available if the limit is exhausted. Some treat tree removal separately, with its own lower limit.</p>
<p>Disputes often arise over what debris removal costs, whether removing a damaged foundation is included and how much of the cleanup relates to covered property rather than a neighbor’s. Keep invoices, photos of the debris and the contractor’s load tickets.</p>
<h2>Ordinance or law and code upgrades</h2>
<p>When a home is rebuilt, it generally must meet the building codes in effect when the work is permitted, not the codes from when it was first built. Upgrades can include stronger roof-to-wall connections, electrical changes, energy code requirements and other items, depending on the local jurisdiction.</p>
<p>Standard policies often provide limited ordinance or law coverage, frequently expressed as a percentage of the dwelling limit, and some owners have bought more. Disputes arise over which items are true code requirements, whether the local authority actually enforces them and how they should be priced. A letter from your local building department or a code review from your contractor can help settle those questions.</p>
<h2>Contents and additional living expenses</h2>
<h3>Contents</h3>
<p>After a total loss, rebuilding a contents inventory from memory is one of the hardest parts of the claim. Use photos and videos from phones and social media, bank and credit card statements, and online order histories. Go room by room, including closets, the garage, the basement and any outbuildings. Many policies pay actual cash value first and the remainder after you replace items.</p>
<h3>Additional living expense</h3>
<p>Loss of use or additional living expense (ALE) coverage typically pays the increase in your normal living costs while the home is unlivable, such as rent, extra mileage and higher food costs. It often has a dollar limit, a time limit or both. Keep receipts and track your usual expenses so you can show the difference.</p>
<h2>Why valuation disputes arise after tornadoes</h2>
<p>After a major tornado, demand for contractors and materials can surge, and estimates written from standard price lists may not reflect what it actually costs to rebuild in that market at that moment. Other common sources of disagreement include:</p>
<ul><li>Whether the home is a total loss or can be repaired</li><li>The quality and features of the original home, especially when it was destroyed and few photos survive</li><li>Reusing versus replacing the foundation</li><li>Depreciation on a home that was well maintained</li><li>Overhead and profit for a general contractor coordinating many trades</li></ul>
<p>Tornado claims can also involve straight-line wind damage in surrounding areas, which is usually covered under the same windstorm peril. Either way, the argument is often about numbers rather than coverage.</p>
<h2>Where appraisal fits in a rebuild</h2>
<p>If you and the insurer agree the tornado damage is covered but can’t agree on the cost to rebuild, appraisal may be an option under your policy. Depending on the wording, it can address the dwelling, other structures, contents and sometimes ALE. It won’t resolve whether you were underinsured or whether a particular exclusion applies; those are coverage or legal questions for a Missouri attorney.</p>
<p>For more, see our <a href="/appraisal-help/tornado-straight-line-wind-appraisal/">tornado and straight-line wind appraisal</a> page. Our <a href="/toolkit/">claim toolkit</a> includes calculators and a calendar to help you keep track of rebuild deadlines. Nothing here is legal advice, and your policy controls.</p>''',
    },
    {
        "slug": "sinkholes-earth-movement-new-madrid",
        "title": "Sinkholes, Earth Movement and Earthquake Coverage in Missouri",
        "seo": "Missouri Sinkholes, Earth Movement and Quakes",
        "desc": "How Missouri policies treat sinkholes, mine subsidence and New Madrid earthquake risk, and where appraisal fits once the insurer accepts coverage.",
        "summary": "Karst, mines and the New Madrid seismic zone make ground movement a real Missouri risk. Here’s how coverage usually works and where appraisal fits.",
        "date": "2026-10-27",
        "read": "8 min",
        "body": '''<p>Missouri’s ground can be unpredictable. Much of the state sits on limestone and dolomite that slowly dissolve, creating caves, springs and sinkholes. Old mine workings lie beneath parts of several regions. And southeast Missouri sits atop the New Madrid seismic zone, which produced a series of major earthquakes in 1811 and 1812. When the ground moves and a home cracks, settles or drops, the first question usually isn’t how much the damage costs. It’s whether the policy covers it at all.</p>
<h2>Karst geology and Missouri sinkholes</h2>
<p>Karst is a landscape formed when water dissolves soluble bedrock. Missouri has extensive karst, especially across the Ozarks, around Springfield and Greene County, and in parts of the St. Louis region. Sinkholes can form slowly, as soil gradually washes into openings below, or suddenly, when the roof of an underground void gives way.</p>
<p>The Missouri Geological Survey, part of the Missouri Department of Natural Resources, maintains maps of known sinkholes and other karst features. Checking those maps can tell you whether your property sits in an area with documented sinkholes. That won’t decide a claim, but it’s useful context for you, your engineer and the insurer.</p>
<h2>The earth movement exclusion</h2>
<p>Most standard homeowners policies exclude earth movement. The exclusion typically lists things like earthquake, landslide, mudflow, subsidence and the sinking, rising or shifting of the ground. Depending on the wording, it may apply whether the movement was caused by natural forces or by human activity.</p>
<p>That exclusion is often why sinkhole and settlement claims are denied. Wording varies, though, and some policies carve out exceptions, such as ensuing fire or explosion, or provide specific sinkhole or collapse coverage. Read the exclusion and every endorsement closely. If the insurer has denied a claim under the earth movement exclusion, that’s a coverage dispute, and a Missouri attorney is the right person to evaluate it.</p>
<h2>Collapse coverage</h2>
<p>Many policies include an additional coverage for collapse, and it’s usually narrow. Typical language covers the abrupt collapse of a building or part of a building caused by specific perils, such as hidden decay, hidden insect damage, the weight of ice or snow, or defective materials used during construction. Many forms define collapse to exclude settling, cracking, shrinking, bulging and expansion.</p>
<p>Whether a particular event counts as collapse can be a close question that turns on the policy’s definition and the engineering facts. An engineer’s report that explains what happened, why and roughly when is usually the most important piece of evidence.</p>
<h2>Mine subsidence</h2>
<p>Missouri has a long mining history, including lead, zinc, coal and other materials, and old underground workings exist in several parts of the state. When those workings fail, the ground above can sink. Standard policies generally treat this as earth movement and exclude it unless specific coverage has been added. If you live in an area with a known mining history, ask your agent whether any mine subsidence coverage is available for your property, and review what your policy actually says.</p>
<p>If cracks, sticking doors or sloping floors appear in a home above old workings, document them with dated photos and measurements, and note when you first noticed each change. Ground movement often unfolds slowly, and a clear timeline helps an engineer judge the cause and helps everyone see how the damage progressed.</p>
<h2>The New Madrid seismic zone and earthquake coverage</h2>
<p>The New Madrid seismic zone runs through southeast Missouri, including the Bootheel, and into neighboring states along the Mississippi River. The 1811–1812 earthquakes were among the strongest ever recorded in the central United States, and smaller quakes still occur in the region. A strong event could affect much of eastern Missouri, including the St. Louis area.</p>
<p>Standard homeowners policies almost always exclude earthquake. Coverage is usually available as a separate endorsement or policy, often with its own percentage deductible that can be much larger than your regular deductible. Before anything happens, check your declarations page to see whether earthquake coverage is listed, what the deductible is and whether it applies to the dwelling, other structures and contents.</p>
<h2>Where appraisal fits</h2>
<p>Appraisal values covered damage. It isn’t a tool for deciding whether earth movement, sinkhole, collapse or earthquake damage is covered. In ground-movement claims, the order usually looks like this:</p>
<ol><li>The insurer investigates, often with an engineer, and makes a coverage decision.</li><li>If coverage is denied, the dispute is about coverage, and you may want a Missouri attorney and your own engineer.</li><li>If coverage is accepted, in whole or in part, but you disagree on the repair scope or cost, appraisal may be available under your policy.</li></ol>
<p>Repair scope in these claims can be complicated. Foundation stabilization, piering, grout injection and structural repairs need careful engineering, and estimates can vary widely. Our <a href="/appraisal-help/sinkhole-ground-collapse-appraisal/">sinkhole and ground collapse appraisal</a> page explains how we approach those cases. For terms like karst, collapse and subsidence, see the <a href="/appraisal-dictionary/">appraisal dictionary</a>.</p>
<p>Nothing here is legal advice. Your policy controls, and coverage questions belong with a Missouri attorney.</p>''',
    },
    {
        "slug": "missouri-fair-plan-claims",
        "title": "Claims Under the Missouri FAIR Plan: Coverage Basics and Amount-of-Loss Disputes",
        "seo": "Missouri FAIR Plan Claims and Appraisal",
        "desc": "A guide to Missouri FAIR Plan claims: who the plan serves, typical coverage limits, reading the declarations and taking amount disputes to appraisal.",
        "summary": "The Missouri Property Insurance Placement Facility covers properties the standard market won’t. Here’s how its claims work and when appraisal may apply.",
        "date": "2026-11-05",
        "read": "7 min",
        "body": '''<p>Not every Missouri property can get coverage from a standard insurance company. Older homes, vacant buildings, properties in certain urban neighborhoods and properties with past losses sometimes struggle to find a standard policy. For many of those owners, the Missouri FAIR Plan, formally the Missouri Property Insurance Placement Facility, is the market of last resort. FAIR Plan claims work much like other property claims, but the coverage is often more limited, so reading the policy matters even more.</p>
<h2>Who the Missouri FAIR Plan serves</h2>
<p>The FAIR Plan exists so property owners who can’t find coverage in the voluntary market still have access to basic property insurance. It operates as an association of insurers licensed in Missouri under state law. Typical policyholders include owners of:</p>
<ul><li>Older homes or buildings that standard carriers decline</li><li>Rental and investment properties</li><li>Properties in neighborhoods where standard coverage is hard to obtain</li><li>Buildings with past claims or conditions insurers consider higher risk</li></ul>
<p>Eligibility rules, inspections and available coverages can change, so check with an agent or the plan itself for current details.</p>
<h2>What FAIR Plan coverage typically looks like</h2>
<p>FAIR Plan policies are often more basic than a standard homeowners policy. Depending on the form, coverage may be:</p>
<ul><li>Named-peril rather than open-peril, covering only the listed perils, such as fire, lightning, windstorm, hail and vandalism</li><li>Written on an actual cash value basis, or offering replacement cost only in limited situations</li><li>Limited or missing for liability, theft or loss of use, which may need separate coverage</li><li>Subject to specific conditions about vacancy or the condition of the building</li></ul>
<p>None of that is universal. The point is to read your own policy instead of assuming it works like a neighbor’s standard homeowners policy.</p>
<h2>Reading your declarations page</h2>
<p>The declarations page summarizes your coverage. For a FAIR Plan policy, pay close attention to:</p>
<ul><li>The form name or number, which tells you which policy wording applies</li><li>The covered perils, especially whether wind and hail are included</li><li>Limits for the building, other structures and contents</li><li>The valuation basis: actual cash value or replacement cost</li><li>The deductible, and whether a separate wind/hail deductible applies</li><li>Any mortgagee or loss payee listed</li></ul>
<p>Keep a copy of the full policy, not just the declarations. The conditions section holds the claim procedures, deadlines and any appraisal provision.</p>
<h2>Filing and handling a FAIR Plan claim</h2>
<p>The claim process looks familiar. Report the loss promptly, protect the property from further damage and keep receipts for emergency repairs. Expect an adjuster inspection, requests for documentation and possibly a sworn proof of loss.</p>
<p>Because many FAIR Plan policies pay actual cash value, depreciation often becomes the central issue. Ask for the adjuster’s estimate in writing, line by line, and look at how depreciation was calculated for each item. Age, condition and the expected life of materials all affect the number, and reasonable people can disagree about each of them.</p>
<h3>Rental and vacant properties</h3>
<p>If the property is a rental or was empty at the time of loss, check the policy for vacancy or occupancy conditions. Some forms limit or exclude certain perils when a building has been vacant for a stated period. Those are coverage questions, not amount questions.</p>
<h3>Mortgage companies and loss payees</h3>
<p>Many FAIR Plan properties carry a mortgage, and some investment properties list a contract seller or other loss payee. Those parties are often named on claim checks, which can slow payment while everyone endorses. Ask your lender early how it handles insurance proceeds so repair money isn’t stuck waiting on paperwork.</p>
<h2>Disputes over the amount of loss</h2>
<p>If the FAIR Plan accepts the claim but you disagree on the amount, look for an appraisal provision in the conditions section. Many property policies include one, but check your policy rather than assuming yours does. If it’s there, it usually works the same way as in other policies: a written demand, an appraiser for each side, an umpire chosen by the appraisers and an award signed by any two.</p>
<p>Appraisal can help with disputes over repair scope, unit costs and depreciation. It doesn’t decide whether a peril is covered or whether a vacancy condition applies. For those issues, talk with a Missouri attorney. You can also contact the Missouri Department of Commerce and Insurance with questions or complaints about how a claim is being handled.</p>
<h2>Practical next steps</h2>
<ol><li>Get a full copy of your FAIR Plan policy, including every form and endorsement.</li><li>Request the adjuster’s estimate in writing.</li><li>Get an independent estimate from a contractor or appraiser.</li><li>Compare the two line by line, focusing on scope and depreciation.</li><li>Check for an appraisal provision and write down every deadline.</li></ol>
<p>Our <a href="/questions-answered/">questions answered</a> page covers common concerns about cost and timing, and an <a href="/appraisal-help/insurer-estimate-review/">insurer estimate review</a> can show whether appraisal is worth pursuing. If a panel needs a neutral third member, see our <a href="/appraisal-help/appraisal-umpire-services/">umpire services</a>.</p>''',
    },
]
