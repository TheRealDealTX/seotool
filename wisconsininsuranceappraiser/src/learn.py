"""Learning content: appraisal process steps, FAQ, claims dictionary and learning-center guides."""

# ---------------------------------------------------------------------------
# Appraisal process guide: eight steps (the builder adds an h2 per step)
# ---------------------------------------------------------------------------
PROCESS_STEPS = [
    ("Pin down the disagreement", """
<p>Appraisal settles one kind of argument: how much a covered loss is worth. Before anyone sends a demand, get specific about where you and the carrier part ways. Is the gap in roof squares, in the price of siding, in whether drywall gets patched or replaced, or in overhead and profit?</p>
<ul>
<li>Lay your contractor’s estimate next to the carrier’s and mark every line that differs.</li>
<li>Ask the adjuster in writing to reconsider the items you can document. A supplement sometimes closes the gap without appraisal.</li>
<li>Note anything the carrier calls a coverage question rather than a pricing question, because that part may not belong in appraisal at all.</li>
</ul>
<p>A short, written list of disputed items becomes the backbone of everything that follows.</p>
"""),
    ("Read the appraisal provision", """
<p>Find the policy itself, not just the declarations page, and locate the paragraph usually titled “Appraisal” in the conditions section. Policies vary, so read your own wording rather than relying on a summary. Look for:</p>
<ul>
<li>Who may demand appraisal and whether the demand must be in writing.</li>
<li>How many days each side has to name its appraiser.</li>
<li>How the umpire is chosen and what happens if the appraisers can’t agree on one.</li>
<li>How appraiser and umpire costs are split.</li>
<li>Any requirement that appraisers be “competent,” “independent,” “impartial” or “disinterested.”</li>
</ul>
<p>Also check for related duties, such as a sworn proof of loss or a suit-limitation period, that run on their own clocks while appraisal is underway.</p>
"""),
    ("Send a written demand", """
<p>Once the gap is clear and the clause is understood, the demand itself is usually short. A typical demand letter:</p>
<ul>
<li>Identifies the policyholder, property address, policy number and claim number.</li>
<li>States that the parties disagree on the amount of loss.</li>
<li>Invokes the appraisal provision by name.</li>
<li>Names your appraiser, or commits to naming one within the policy’s time limit.</li>
</ul>
<p>Send it in a way you can prove later, such as email plus certified mail, and keep copies of everything. Stay factual and calm; the letter isn’t the place to argue the estimate. If the carrier responds that some items are coverage disputes, note that in your file and keep the appraisal moving on the amounts.</p>
"""),
    ("Choose your appraiser", """
<p>Your appraiser builds and defends your valuation, so choose someone who understands construction pricing, the type of damage involved and the appraisal procedure itself. Ask any candidate:</p>
<ul>
<li>How they’re paid, and whether the fee structure could be challenged under an impartiality requirement in your policy.</li>
<li>Whether they have any relationship with your contractor, your carrier or the property.</li>
<li>Which estimating platform they use and how they handle local pricing.</li>
<li>How they communicate progress and what they need from you.</li>
</ul>
<p>The carrier names its own appraiser on the same timeline. Each appraiser works for the side that hired them, but each should also be able to sign an award they can stand behind.</p>
"""),
    ("Select the umpire", """
<p>The two appraisers try to agree on a neutral umpire, ideally early, so one is in place before any impasse. A good umpire understands estimating and construction, has no ties to either side and is willing to look at evidence rather than split the difference by habit.</p>
<p>If the appraisers can’t agree within the time the policy allows, many clauses let either party ask a court to appoint one. In Wisconsin that request typically goes to the circuit court for the county where the property is located, though policies vary in how they describe the court and the procedure. Our <a href="/appraisal-solutions/umpire-selection-services/">umpire selection</a> page explains what a strong candidate list looks like.</p>
"""),
    ("Inspect and build estimates", """
<p>Each appraiser inspects the property, ideally with the other appraiser present, and documents what they see. For a roof that might mean measuring every slope, counting hail hits in test areas and noting the shingle line. For a water loss it might mean moisture readings, cut lines and contents lists.</p>
<p>From that inspection each side prepares or refines a line-item estimate. Good estimates are specific: quantities, unit prices, labor, materials, tear-off, disposal, code items and access costs. Photos and measurements should support each disputed line, because the strongest number in appraisal is the one with evidence behind it. If you want an outside look at the carrier’s figures first, see our <a href="/appraisal-solutions/carrier-estimate-review/">carrier estimate review</a>.</p>
"""),
    ("Negotiate line by line", """
<p>With both estimates in hand, the appraisers compare them line by line. Many items settle quickly once measurements are reconciled or a missing component is spotted. The harder items, such as matching, repair versus replacement, or overhead and profit, take documentation and discussion.</p>
<ul>
<li>Agreed lines are recorded so they don’t get reopened.</li>
<li>Disputed lines are narrowed to a specific quantity or price difference.</li>
<li>Each appraiser prepares a short written position for anything still open.</li>
</ul>
<p>When the two appraisers reach full agreement, they sign an award and the umpire never needs to decide anything. When they don’t, only the remaining disputed items go to the umpire, which keeps the decision focused and the cost contained.</p>
"""),
    ("Sign the award and get paid", """
<p>An award signed by the two appraisers, or by one appraiser and the umpire, generally sets the amount of loss. A clear award separates replacement cost from actual cash value and lists categories such as dwelling, other structures and contents, so payment can be calculated without new arguments.</p>
<p>After the award, the carrier applies the deductible, prior payments and any depreciation holdback under the policy terms. Recoverable depreciation is often released once repairs are completed and documented, so keep invoices and photos. Our <a href="/insurance-claim-calculators/rcv-acv-holdback-calculator/">RCV, ACV and holdback calculator</a> can help you see how the numbers usually flow. If payment stalls or coverage is disputed after the award, talk to a Wisconsin attorney.</p>
"""),
]

PROCESS_EXTRA = """
<h2>What appraisal costs</h2>
<p>Most appraisal clauses say each side pays its own appraiser and the two sides split the umpire’s fee and other shared expenses equally. Read your policy, because the split isn’t universal.</p>
<h3>How appraisers are paid</h3>
<p>Appraisers commonly charge a flat fee, an hourly rate, or a combination. Some offer a percentage of the award. Where a policy requires a “disinterested” or “impartial” appraiser, a fee tied to the outcome can invite a challenge to the award, so ask any appraiser to explain their arrangement in writing before you sign. We quote our fee up front and explain what it covers.</p>
<h3>When appraisal may not pay off</h3>
<p>If the gap between estimates is small compared with the likely appraiser and umpire costs, a documented supplement or a second conversation with the adjuster may make more sense. Our <a href="/insurance-claim-calculators/settlement-gap-calculator/">settlement gap calculator</a> helps you weigh that.</p>

<h2>What appraisal won’t decide</h2>
<p>An appraisal panel values the loss. It generally does not decide legal questions, including:</p>
<ul>
<li><strong>Coverage.</strong> Whether a peril, a part of the building or an item is covered under the policy is usually for the carrier, and ultimately a court, to decide.</li>
<li><strong>Bad faith.</strong> Whether a carrier handled a claim unreasonably is a legal claim, not an appraisal issue.</li>
<li><strong>Interest and penalties.</strong> Questions about late payment and what is owed for delay sit outside the panel’s job.</li>
</ul>
<p>The panel can, however, value disputed items separately so that a later coverage decision can be applied to the numbers without starting over.</p>

<h2>Wisconsin specifics</h2>
<p>Insurance in Wisconsin is regulated by the Office of the Commissioner of Insurance (OCI), which licenses insurers and agents and accepts consumer complaints. A complaint to OCI is separate from appraisal and doesn’t replace it.</p>
<p>If the two appraisers can’t agree on an umpire, many policies allow either side to ask a court to appoint one. In practice that is usually the circuit court in the county where the property sits, but policies vary in their wording.</p>
<p>Wisconsin courts recognize bad-faith claims against insurers, and a Wisconsin statute addresses timely payment of claims and interest on overdue amounts. How those rules apply depends on the facts and the policy. We are appraisers, not lawyers, and we don’t give legal advice; for legal questions, consult a Wisconsin attorney.</p>
<div class="note"><b class="h">Watch your deadlines</b>Appraisal does not automatically pause other policy deadlines, such as a suit-limitation period. Track every date in your policy, and use our <a href="/insurance-claim-calculators/claim-timeline-planner/">claim timeline planner</a> to keep them in one place.</div>

<h2>Documents to gather</h2>
<ul>
<li>The full policy, including the declarations page and all endorsements.</li>
<li>Every carrier estimate, letter and payment record on the claim.</li>
<li>Your contractor’s estimate, invoices and any bids.</li>
<li>Dated photos and video of the damage, before and after any mitigation.</li>
<li>Mitigation invoices, moisture logs and receipts for emergency repairs.</li>
<li>A log of calls, emails and inspections with names and dates.</li>
</ul>
<p>Not sure you’re ready? Try the <a href="/insurance-claim-calculators/appraisal-readiness-quiz/">appraisal readiness quiz</a>, or <a href="/contact-us/">contact us</a> to talk through your file.</p>
"""

# ---------------------------------------------------------------------------
# FAQ
# ---------------------------------------------------------------------------
FAQ = [
    ("Starting appraisal", [
        ("When does appraisal make sense?", "Appraisal fits when the carrier accepts that at least part of the loss is covered but you disagree on what it will cost to repair or replace. It is generally not the tool for a full denial of coverage."),
        ("Who can demand appraisal?", "Under most policies either side can, you or the insurance company. The demand is usually made in writing and should refer to the appraisal provision in your policy."),
        ("Do I need my contractor’s estimate before I start?", "It helps a great deal. A detailed estimate shows where you and the carrier disagree and gives your appraiser a starting point, though an appraiser can also build an estimate from an inspection."),
        ("Can I ask for a supplement instead?", "Yes, and it is often worth trying first. If the carrier accepts a documented supplement, you may not need appraisal at all."),
        ("Is appraisal the same as arbitration or a lawsuit?", "No. Appraisal is a narrower process set out in your policy that normally decides only the amount of loss, while legal and coverage questions are left to the parties and, if needed, the courts."),
    ]),
    ("Costs & fees", [
        ("Who pays for appraisal?", "Most clauses say each side pays its own appraiser and the umpire’s costs are split equally. Your policy’s wording controls, so check it."),
        ("How do appraisers charge?", "Common structures are a flat fee, an hourly rate or a combination. Ask any appraiser to explain their fee in writing before you hire them."),
        ("Are percentage fees a problem?", "They can be. If your policy requires a disinterested or impartial appraiser, a fee tied to the size of the award may be raised as a challenge, so ask how any appraiser handles that."),
        ("Is appraisal worth it for a small gap?", "Sometimes not. If the difference between estimates is small compared with the likely fees, a supplement or further negotiation may be the better route; our settlement gap calculator can help you compare."),
    ]),
    ("Timing & deadlines", [
        ("How long does appraisal take?", "Many residential appraisals wrap up in a few weeks to a few months, depending on the size of the loss, how quickly the umpire is chosen and how many items are disputed. Larger commercial losses can take longer."),
        ("How long do I have to name an appraiser?", "Many policies give each side a set number of days after the written demand, often around 20. Your policy states the exact period."),
        ("Does appraisal stop other deadlines?", "Not automatically. Suit-limitation periods and proof-of-loss deadlines may keep running, so track them separately and ask a Wisconsin attorney if you are unsure."),
        ("Should I make repairs before appraisal?", "Protect the property from further damage right away, and keep records and receipts. For permanent repairs, document the damage thoroughly first, because the panel will need to see or verify what was there."),
    ]),
    ("Wisconsin rules & coverage", [
        ("Who regulates insurance in Wisconsin?", "The Office of the Commissioner of Insurance (OCI). It licenses insurers and agents and accepts consumer complaints, which is a separate process from appraisal."),
        ("What happens if the appraisers can’t agree on an umpire?", "Many policies allow either party to ask a court to appoint one, which in Wisconsin is usually the circuit court in the county where the property is located. Policies vary in their exact wording."),
        ("Can the panel decide whether my damage is covered?", "Generally no. Appraisal sets the amount of loss, while coverage questions are for the carrier and, if disputed, the courts."),
        ("What is the Wisconsin Insurance Plan?", "It is the state’s FAIR plan, which offers basic property coverage to owners who have trouble getting it in the regular market. Plan policies have their own terms, so read the appraisal and loss-settlement provisions in yours."),
        ("Does appraisal affect a bad-faith claim?", "Appraisal doesn’t decide bad faith, which is a legal question. Wisconsin courts recognize bad-faith claims against insurers, and a Wisconsin attorney can tell you how that might apply to your situation."),
    ]),
    ("Working with us", [
        ("Are you a public adjuster or a law firm?", "Neither. We are independent insurance appraisers who serve as party appraisers, umpires and estimate reviewers, and we don’t give legal advice."),
        ("What do you need to review my claim?", "The policy with endorsements, the carrier’s estimates and letters, your contractor’s estimate, and dated photos are the core of most files. The documents list in our process guide covers the rest."),
        ("Do you work outside the Milwaukee and Madison areas?", "Yes. We work with property owners throughout Wisconsin, from the Fox Valley to the Driftless Area and the Northwoods; see our local appraisers page for areas we cover."),
        ("Can you serve as an umpire?", "Yes, when both appraisers agree to appoint us or a court does, provided we have no conflict with either side or the property."),
    ]),
]

# ---------------------------------------------------------------------------
# Claims dictionary (alphabetical)
# ---------------------------------------------------------------------------
GLOSSARY = [
    ("Actual cash value", "The value of damaged property at the time of loss, usually figured as replacement cost minus depreciation. Some policies define it differently."),
    ("Additional living expense", "Coverage for the extra cost of living elsewhere while a home can’t be lived in after a covered loss, subject to policy limits."),
    ("Amount of loss", "The dollar value of a covered loss. It is the question an appraisal panel is normally asked to decide."),
    ("Appraisal award", "The written decision that sets the amount of loss, generally binding once signed by two of the three panel members."),
    ("Appraisal clause", "The policy provision that lets either party demand appraisal when they disagree on the amount of loss and sets out how the process works."),
    ("Appraisal demand", "The written notice from one party invoking the appraisal clause, usually naming that party’s appraiser."),
    ("Coinsurance", "A policy condition that can reduce a claim payment if the property was insured for less than a required percentage of its value. More common on commercial policies."),
    ("Declarations page", "The summary page of a policy listing the insured, property, coverages, limits, deductibles and endorsements."),
    ("Deductible", "The portion of a covered loss the policyholder pays before the insurer’s payment begins."),
    ("Depreciation", "A reduction in value for age, wear and condition, subtracted from replacement cost to reach actual cash value."),
    ("Derecho", "A long-lived, widespread windstorm produced by a line of thunderstorms, capable of straight-line wind damage across a very large area."),
    ("Disinterested appraiser", "An appraiser with no financial or personal stake in the outcome. Many policies require appraisers to be disinterested, impartial or independent."),
    ("Endorsement", "A written change to a policy that adds, removes or modifies coverage, such as a sewer backup endorsement."),
    ("Estimate review", "A line-by-line check of an insurance estimate for missing items, incorrect quantities and pricing that doesn’t reflect local costs."),
    ("Exclusion", "Policy language that removes a cause of loss or type of property from coverage, such as flood or wear and tear."),
    ("Hail bruising", "Damage to a shingle from hail impact that may not be obvious at first glance but can loosen granules and weaken the mat."),
    ("Holdback", "The portion of a replacement cost claim, usually recoverable depreciation, that the insurer withholds until repairs are completed."),
    ("Ice and water shield", "A self-adhering underlayment installed at eaves, valleys and other vulnerable areas to resist leaks from ice dams and wind-driven rain."),
    ("Ice dam", "A ridge of ice that forms at a roof’s edge when melting snow refreezes, which can force water under shingles and into the home."),
    ("Line item", "A single entry in an estimate describing one task or material with its quantity, unit and price."),
    ("Matching", "The question of whether repaired areas must reasonably match undamaged areas in color, texture or style, and what happens when matching materials aren’t available."),
    ("Mitigation", "Reasonable steps to prevent further damage after a loss, such as tarping a roof or drying out a basement. Most policies require it."),
    ("National Flood Insurance Program", "The federal program that provides most flood insurance, which is separate from a standard homeowners policy."),
    ("Office of the Commissioner of Insurance", "Wisconsin’s insurance regulator, known as OCI, which licenses insurers and agents and handles consumer complaints."),
    ("Ordinance or law coverage", "Coverage for added costs to bring repaired portions of a building up to current building codes, subject to a limit."),
    ("Overhead and profit", "A general contractor’s charge for business overhead and profit, often a disputed item when several trades are involved."),
    ("Percentage deductible", "A deductible set as a percentage of the dwelling coverage limit rather than a flat dollar amount, often applied to wind or hail losses."),
    ("Proof of loss", "A sworn statement of the amount claimed that some policies require within a set time after a loss or after the insurer’s request."),
    ("Recoverable depreciation", "Depreciation the insurer will pay back once repairs or replacement are completed, under a replacement cost policy."),
    ("Replacement cost value", "The cost to repair or replace damaged property with materials of like kind and quality, without a deduction for depreciation."),
    ("Reservation of rights", "A letter in which the insurer continues handling a claim while reserving the right to deny coverage later."),
    ("Roof square", "A unit of roofing measure equal to 100 square feet of roof surface."),
    ("Scope of loss", "The description of what was damaged and what work is needed to repair it, before pricing is applied."),
    ("Sewer backup endorsement", "An optional addition to a homeowners policy that covers water backing up through sewers or drains, or overflowing from a sump, usually up to a separate limit."),
    ("Snow load", "The weight of accumulated snow and ice on a roof, which can cause sagging, cracking or collapse when it exceeds what the structure can carry."),
    ("Supplement", "A request to add or revise items in an insurance estimate after hidden damage is found or omissions are identified."),
    ("Test square", "A marked 10-by-10-foot area on a roof slope used to count hail hits and assess damage."),
    ("Umpire", "The neutral third member of an appraisal panel who decides items the two appraisers can’t agree on."),
    ("Wisconsin Insurance Plan", "Wisconsin’s FAIR plan, offering basic property insurance to owners who can’t obtain it in the regular market."),
    ("Xactimate", "A widely used estimating software platform for property insurance claims, with regional price lists for labor and materials."),
]

# ---------------------------------------------------------------------------
# Learning center guides
# ---------------------------------------------------------------------------
POSTS = [
    {
        "slug": "wisconsin-appraisal-clause-guide",
        "title": "Reading the Appraisal Clause in Your Wisconsin Property Policy",
        "seo": "Wisconsin Appraisal Clause: How to Read It",
        "desc": "How to find and read the appraisal clause in a Wisconsin homeowners or commercial policy, from the demand to the umpire and the award.",
        "date": "2026-08-11", "read": "7 min",
        "summary": "The appraisal clause is short, but each phrase shapes how a dispute plays out. Here’s how to read the version in your Wisconsin policy.",
        "body": """
<p>Most Wisconsin property owners first look for the appraisal clause after a claim has stalled. The adjuster’s estimate is lower than the contractor’s, the back-and-forth has stopped producing results, and someone mentions “appraisal.” This guide walks through how to find the clause in your policy and what each part usually means. Policies vary, so treat this as a reading companion, not a substitute for your own wording.</p>

<h2>Where to find it</h2>
<p>The declarations page won’t include it. You need the full policy form. In most homeowners policies the appraisal provision sits in the “Conditions” section, often near “Loss Payment,” “Suit Against Us” and “Duties After Loss.” Commercial property forms usually place it among the loss conditions. Endorsements can modify it, so read every page that came with your policy, including any state-specific amendment.</p>
<p>If you can’t find your policy, ask your agent or the carrier for a certified copy. You are entitled to see the terms that govern your claim.</p>

<h2>The parts of a typical appraisal clause</h2>
<h3>The trigger</h3>
<p>Most clauses begin with language like “If you and we fail to agree on the amount of loss.” That phrase matters. The <strong>Wisconsin appraisal clause</strong> in most standard forms is aimed at disputes about value, not disputes about whether something is covered. If the carrier has denied the claim outright, appraisal usually isn’t the right tool.</p>
<h3>The demand</h3>
<p>Many clauses say either party “may demand” appraisal and that the demand must be in writing. Some older forms require both parties to agree. Read carefully: if the clause says “either party,” you don’t need the carrier’s permission to start.</p>
<h3>The appraisers</h3>
<p>Each side typically chooses “a competent and impartial appraiser” or similar within a set number of days, commonly 20, after receiving the written demand. Words like <em>impartial</em>, <em>independent</em> or <em>disinterested</em> set a standard your appraiser should meet. Ask how a candidate is paid and whether they have any ties to your contractor.</p>
<h3>The umpire</h3>
<p>The two appraisers then choose an umpire. If they can’t agree within the stated time, often 15 days, the clause usually lets either party ask a court of record to appoint one. In Wisconsin that request typically goes to the circuit court in the county where the property is located, though the exact language differs from policy to policy. Our <a href="/appraisal-solutions/umpire-selection-services/">umpire selection services</a> page covers what makes a good candidate.</p>
<h3>The decision</h3>
<p>The appraisers try to agree on the amount of loss. If they do, their written agreement sets the amount. If they don’t, they submit their differences to the umpire, and a decision agreed to by any two of the three generally sets the amount of loss.</p>
<h3>The costs</h3>
<p>Most clauses say each party pays its own appraiser and the two share the umpire’s fee and other appraisal expenses equally. A few policies handle costs differently, so check yours.</p>
<h3>The reservation</h3>
<p>Many clauses end with a sentence saying that if there is an appraisal, the insurer still retains its right to deny the claim. In plain terms, the award sets a number, but coverage questions can still be raised.</p>

<h2>What the clause usually doesn’t say</h2>
<p>Appraisal clauses tend to be brief, which leaves practical questions open:</p>
<ul>
<li><strong>Timing of the award.</strong> Few clauses set a deadline for the panel to finish.</li>
<li><strong>Format of the award.</strong> Many don’t say whether the award must separate replacement cost from actual cash value, or itemize categories. A well-drafted award does both.</li>
<li><strong>Inspections.</strong> Most clauses don’t spell out who attends inspections or how evidence is exchanged. Appraisers usually agree on that among themselves.</li>
<li><strong>Other deadlines.</strong> The clause rarely mentions whether suit-limitation periods pause during appraisal. Don’t assume they do.</li>
</ul>

<h2>Related provisions to read alongside it</h2>
<p>The appraisal clause doesn’t operate in isolation. Read these sections too:</p>
<ol>
<li><strong>Duties after loss.</strong> These may require prompt notice, mitigation, an inventory of damaged items and a sworn proof of loss on request.</li>
<li><strong>Loss settlement.</strong> This explains whether you are paid replacement cost or actual cash value, and when depreciation holdback is released.</li>
<li><strong>Suit against us.</strong> This sets the time limit to file a lawsuit, which may keep running during appraisal.</li>
<li><strong>Deductibles and endorsements.</strong> A percentage wind or hail deductible, or a sewer backup endorsement with its own limit, changes the math on any award.</li>
</ol>

<h2>Before you send a demand</h2>
<p>Make sure the gap is real and documented. Compare your contractor’s estimate with the carrier’s line by line, and ask for a supplement on the items you can support. If the gap remains, our <a href="/insurance-claim-calculators/appraisal-readiness-quiz/">appraisal readiness quiz</a> is a quick way to check whether your file is ready, and the <a href="/appraisal-process-guide/">appraisal process guide</a> walks through each step from demand to award.</p>
<p>When you’re ready to move forward, our <a href="/appraisal-solutions/appraisal-demand-representation/">appraisal demand and representation</a> service can help you prepare the demand and serve as your appraiser. If your questions turn to coverage, bad faith or deadlines to sue, those are legal questions, and a Wisconsin attorney is the right person to ask.</p>
""",
    },
    {
        "slug": "ice-dam-insurance-claims",
        "title": "Ice Dam Insurance Claims in Wisconsin: What’s Usually Covered and How to Document It",
        "seo": "Ice Dam Insurance Claims in Wisconsin",
        "desc": "What Wisconsin homeowners policies typically cover after an ice dam, what they usually exclude, and how to document and estimate the damage.",
        "date": "2026-08-27", "read": "7 min",
        "summary": "Ice dams are a fact of Wisconsin winters. Here’s how coverage typically works, where claims get disputed and how to build a strong file.",
        "body": """
<p>Every Wisconsin winter brings the same pattern: heavy snow, a sunny afternoon, a hard freeze overnight. Snow melts over the warm part of the roof, runs down to the cold eaves and refreezes into a ridge of ice. Water backs up behind that ridge, works under the shingles and shows up as a brown stain on a bedroom ceiling. An <strong>ice dam insurance claim</strong> usually starts there.</p>
<p>Coverage depends on your policy, and policies vary. What follows is how these claims commonly play out under standard homeowners forms.</p>

<h2>What is typically covered</h2>
<p>Many homeowners policies cover sudden and accidental water damage to the interior that results from an ice dam. That often includes:</p>
<ul>
<li>Wet or stained drywall and plaster on ceilings and walls.</li>
<li>Saturated insulation in the attic or exterior walls.</li>
<li>Damaged flooring, trim, cabinets and paint.</li>
<li>Personal property soaked by the leak, under contents coverage.</li>
<li>Reasonable costs to dry the structure and prevent mold.</li>
</ul>
<p>Some policies also cover physical damage to the roof itself caused by the weight of ice and snow, such as bent gutters or torn fascia. That varies, so read the wording on weight of ice, snow or sleet.</p>

<h2>What is usually not covered</h2>
<ul>
<li><strong>The ice itself.</strong> Removing an ice dam is usually treated as maintenance, though some policies pay for reasonable removal as a step to prevent further damage. Ask before you assume either way.</li>
<li><strong>Wear and tear.</strong> Old shingles, failed flashing or deteriorated underlayment are generally excluded as maintenance issues.</li>
<li><strong>Long-term seepage.</strong> Many policies exclude damage from water that leaked repeatedly over weeks or months. Prompt reporting matters.</li>
<li><strong>Upgrades.</strong> Adding insulation or ventilation to prevent future dams is usually your cost, unless code or ordinance coverage applies to required work.</li>
</ul>

<h2>Why ice dam claims get disputed</h2>
<h3>Cause and timing</h3>
<p>Carriers sometimes argue the damage is long-term seepage or the result of poor attic ventilation rather than a covered event. Dated photos, weather records and a prompt report help answer that.</p>
<h3>Hidden damage</h3>
<p>Water travels. It can soak insulation and wall cavities far from the visible stain. An adjuster who looks only at the ceiling may scope a small patch when the wall cavity below is wet too. Moisture readings settle that question.</p>
<h3>Repair method</h3>
<p>Patch-and-paint versus replace is a frequent gap. If several rooms share continuous ceilings, or the drywall is stained in multiple places, a patch may not produce a reasonable repair.</p>

<h2>How to document ice dam damage</h2>
<ol>
<li><strong>Photograph the outside first.</strong> Capture the ice ridge, icicles, gutters and snow depth from the ground with a timestamp. Don’t climb on an icy roof.</li>
<li><strong>Photograph every interior stain.</strong> Take wide shots of each room and close-ups of each stain, drip and bubble in the paint.</li>
<li><strong>Get moisture readings.</strong> A mitigation company’s moisture map and drying log are strong evidence of how far the water went.</li>
<li><strong>Keep removed materials if you can.</strong> Or at least photograph them before disposal.</li>
<li><strong>Save every receipt.</strong> Emergency removal, tarping, fans and dehumidifiers all belong in the file.</li>
<li><strong>Write a short timeline.</strong> When you noticed the leak, when you called the carrier, and what was done.</li>
</ol>

<h2>Estimating ice dam repairs</h2>
<p>A complete estimate for an ice dam loss usually includes more than drywall. Look for:</p>
<ul>
<li>Drywall removal and replacement, tape, texture and paint, often to a natural break such as a corner.</li>
<li>Insulation removal and replacement in affected bays.</li>
<li>Drying equipment, antimicrobial treatment and monitoring.</li>
<li>Flooring, trim and contents handling where water reached them.</li>
<li>Exterior items such as gutters, fascia, soffit and any roof damage the policy covers.</li>
<li>Code items, such as ice and water shield at the eaves when roof repairs trigger current requirements, which may fall under ordinance or law coverage.</li>
</ul>
<p>If you have both an ice dam leak and a frozen pipe, keep them separate in the file. Each may be a different event with its own deductible, depending on the policy.</p>

<h2>Illustrative example</h2>
<p>An illustrative example only: a carrier scopes a 4-by-6-foot ceiling patch and repainting of one room. A moisture map later shows wet insulation across three attic bays and a damp exterior wall in the room below. The documented scope now includes insulation, a wall section and two adjoining ceilings. That kind of difference is what a supplement or an appraisal is built on.</p>

<h2>When appraisal fits</h2>
<p>If the carrier accepts that the interior damage is covered but you disagree on the scope or price, appraisal may be the right tool. If the carrier says the loss isn’t covered at all, that’s a coverage question and a conversation for a Wisconsin attorney.</p>
<p>Our <a href="/appraisal-solutions/ice-dam-frozen-pipe-appraisal/">ice dam and frozen pipe appraisal</a> page explains how we approach these files. For heavy-snow seasons, the <a href="/insurance-claim-calculators/roof-snow-load-calculator/">roof snow load calculator</a> offers a rough sense of the weight on your roof, and our <a href="/appraisal-solutions/snow-load-roof-collapse-appraisal/">snow load appraisal</a> page covers structural damage from the weight itself. Unfamiliar terms are defined in the <a href="/claims-dictionary/">claims dictionary</a>.</p>
""",
    },
    {
        "slug": "hail-claim-photo-checklist",
        "title": "Hail Claim Photo Checklist: Documenting Damage After a Wisconsin Storm",
        "seo": "Hail Claim Photo Checklist for Wisconsin Homes",
        "desc": "A step-by-step hail claim photo checklist for Wisconsin homeowners, covering the roof, siding, gutters, windows and soft metals after a storm.",
        "date": "2026-09-15", "read": "6 min",
        "summary": "Good photos taken soon after a storm are the backbone of a hail claim. Use this checklist to document what an adjuster or appraiser will need.",
        "body": """
<p>Hail moves through Wisconsin quickly. A storm can leave one side of a street untouched and the other with dented gutters and bruised shingles. Days later, the evidence starts to fade: hailstones melt, leaves cover spatter marks and fresh granule loss washes away. A disciplined <strong>hail claim photo checklist</strong> preserves what you’ll need when the adjuster arrives and, if it comes to that, during appraisal.</p>
<p>Safety comes first. Don’t climb onto a roof yourself. A roofer or inspector with proper equipment can document the roof surface; you can capture everything at ground level.</p>

<h2>Right after the storm</h2>
<ul>
<li><strong>Hailstones.</strong> If it’s safe, photograph a handful of stones beside a coin or ruler. Freezing a few in a bag and photographing them later also works.</li>
<li><strong>Time and place.</strong> Take a photo of the street and your house with the date visible on your phone. Screenshot a local weather report or radar image if one is available.</li>
<li><strong>Debris and spatter.</strong> Shredded leaves, broken branches and spatter marks on decks, fences or mailboxes show the direction and size of the hail.</li>
</ul>

<h2>The roof</h2>
<p>Your roofer or inspector should capture:</p>
<ol>
<li><strong>Overview shots of every slope,</strong> labeled by direction, so damage can be tied to a specific face of the roof.</li>
<li><strong>Test squares.</strong> A marked 10-by-10-foot area on each slope with hits circled in chalk, photographed wide and close.</li>
<li><strong>Close-ups of individual hits</strong> showing bruising, exposed mat or fractured edges, with a scale reference.</li>
<li><strong>Soft metals on the roof:</strong> vents, flashing, ridge caps, skylight frames and chimney caps. Dents in these parts are often the clearest proof of hail size.</li>
<li><strong>The shingle itself.</strong> A label, bundle wrapper or an exposed back of a shingle can help identify the product line, which matters if matching becomes an issue.</li>
<li><strong>Prior repairs or wear,</strong> so the file honestly separates old conditions from storm damage.</li>
</ol>
<p>Our <a href="/insurance-claim-calculators/roof-pitch-squares-calculator/">roof pitch and squares calculator</a> can help you check whether the carrier’s roof measurements look reasonable.</p>

<h2>Siding, windows and trim</h2>
<ul>
<li>Every elevation of the house, wide enough to show the whole wall.</li>
<li>Close-ups of cracked, holed or chipped vinyl, fiber cement or wood siding.</li>
<li>Dents in aluminum siding, trim coil and window wraps, shot at an angle with raking light so they show.</li>
<li>Window screens, glazing beads, cracked glass and damaged frames.</li>
<li>Paint chips on wood trim, doors and decks.</li>
</ul>

<h2>Gutters, downspouts and other soft metals</h2>
<p>Gutters and downspouts take a beating in a hailstorm and are easy to photograph from the ground. Shoot each run, then close up on dents. Also document:</p>
<ul>
<li>Air conditioning condenser fins, which can flatten from hail.</li>
<li>Garage doors, especially steel panels.</li>
<li>Light fixtures, mailboxes, meter boxes and vent hoods.</li>
<li>Outdoor furniture, grills and play equipment, if you plan to claim them.</li>
</ul>

<h2>Other structures</h2>
<p>Detached garages, sheds, fences and, in rural Wisconsin, barns and machine sheds often fall under separate coverage. Photograph them the same way: every elevation, every roof slope that can be reached safely, and close-ups of damage. Our <a href="/appraisal-solutions/farm-barn-outbuilding-appraisal/">farm, barn and outbuilding appraisal</a> page explains how those structures are typically valued.</p>

<h2>Interior damage</h2>
<p>Hail can break skylights and windows, letting water in. If that happens, photograph stains, wet carpet and damaged contents before cleanup, and keep receipts for any emergency tarping or drying.</p>

<h2>How to organize the photos</h2>
<ul>
<li>Create one folder per area: roof by slope, each elevation, gutters, other structures, interior.</li>
<li>Keep the original files with their date and location data. Don’t edit or filter them.</li>
<li>Add a short log noting who took the photos and when.</li>
<li>Back everything up somewhere other than your phone.</li>
</ul>

<h2>Common gaps between estimates</h2>
<p>Even with good photos, hail estimates often differ on a few predictable items:</p>
<ul>
<li>Number of slopes approved for replacement versus repair.</li>
<li>Roof measurements, waste factor and steep or high charges.</li>
<li>Soft metals, flashing, drip edge and ice and water shield.</li>
<li>Matching of siding or shingles that can’t be replaced in kind.</li>
<li>Overhead and profit when several trades are involved.</li>
</ul>
<p>A percentage wind or hail deductible changes what you actually receive, so run the numbers in our <a href="/insurance-claim-calculators/percentage-deductible-calculator/">percentage deductible calculator</a>.</p>

<h2>Next steps</h2>
<p>Share your photos with your contractor and ask for a detailed, line-item estimate. If the carrier’s number still falls short, a <a href="/appraisal-solutions/carrier-estimate-review/">carrier estimate review</a> can pinpoint the differences, and our <a href="/appraisal-solutions/hail-roof-damage-appraisal/">hail and roof damage appraisal</a> page explains how a disputed hail claim moves through appraisal. If the storm also left matching problems, read our guide to <a href="/learning-center/matching-siding-and-shingles/">matching siding and shingles</a>.</p>
""",
    },
    {
        "slug": "sewer-backup-vs-flood-coverage",
        "title": "Sewer Backup vs. Flood Coverage: How Wisconsin Basement Water Claims Differ",
        "seo": "Sewer Backup vs. Flood Coverage in Wisconsin",
        "desc": "How sewer backup endorsements, NFIP flood policies and sudden water coverage differ for Wisconsin basement water claims, and where limits apply.",
        "date": "2026-10-02", "read": "8 min",
        "summary": "A wet basement can fall under three very different coverages, or none. Here’s a cautious overview of how they usually differ.",
        "body": """
<p>Wisconsin has seen its share of basements filling with water: the June 2008 floods that drained Lake Delton, the July 2010 Milwaukee flash flood that left many basements backed up, and the August 2018 flash flooding around Dane County. After events like these, the first question homeowners ask is whether insurance will pay. The honest answer is that it depends on where the water came from and what coverage you bought. Understanding <strong>sewer backup vs. flood coverage</strong> is the starting point.</p>
<p>This is a general overview. Policies vary widely, and the exact wording of your policy and endorsements controls. For questions about how coverage applies to your loss, talk to your agent or a Wisconsin attorney.</p>

<h2>Three different sources, three different coverages</h2>
<h3>Water that backs up through drains or overflows a sump</h3>
<p>Standard homeowners policies commonly exclude water that backs up through sewers or drains, or overflows from a sump pump. Many carriers sell a <em>water backup</em> or <em>sewer backup</em> endorsement that adds this coverage back, usually with its own limit.</p>
<h3>Surface water and flood</h3>
<p>Water that rises from outside, such as overland flooding, a river overtopping its banks or heavy rain pooling and flowing into a basement window well, is generally excluded from homeowners policies. Flood coverage usually comes from a separate policy, most often through the National Flood Insurance Program (NFIP) or a private flood insurer.</p>
<h3>Sudden and accidental discharge</h3>
<p>Water that escapes suddenly from a plumbing system, appliance or water heater inside the home is often covered under a standard homeowners policy, subject to exclusions for long-term leaks and wear and tear. A pipe that bursts during a cold snap, like the late-January 2019 polar vortex, is a classic example.</p>

<h2>The sewer backup endorsement</h2>
<p>If you have a backup endorsement, check these points on your declarations page and in the endorsement form:</p>
<ul>
<li><strong>The limit.</strong> Backup endorsements often carry modest limits. Illustrative figures such as $5,000, $10,000 or $25,000 are typical of the options carriers offer, but yours may differ. A finished basement can exceed a low limit quickly.</li>
<li><strong>The deductible.</strong> Some endorsements have their own deductible.</li>
<li><strong>What’s included.</strong> Some endorsements cover the building and contents together under one limit; others split them.</li>
<li><strong>Exclusions.</strong> Many endorsements exclude backup caused by flooding in the area, or water that enters through foundation walls. Read the language closely.</li>
</ul>
<p>When the endorsement limit is lower than the damage, appraisal won’t raise the limit. It can, however, establish the full amount of loss, which matters if other coverage may also apply or if the limit is in dispute.</p>

<h2>NFIP flood insurance</h2>
<p>NFIP policies have their own rules, and many differ from homeowners policies in ways that surprise owners:</p>
<ul>
<li>A waiting period, commonly 30 days, generally applies before a new policy takes effect, with some exceptions.</li>
<li>Coverage for basements is limited. Many finishes and contents in a basement are not covered under the standard flood policy.</li>
<li>Building and contents are separate coverages with separate limits.</li>
<li>Claim procedures and deadlines are set by federal rules and the policy form, and NFIP disputes follow their own process.</li>
</ul>
<p>Because NFIP rules are distinct, read your flood policy separately and ask your agent or a Wisconsin attorney about deadlines.</p>

<h2>When more than one source is involved</h2>
<p>In a heavy storm, a basement can take water from more than one direction at once: a backed-up floor drain, seepage through the walls and overland water through a window well. The carrier may attribute damage to an excluded source, while the owner points to a covered one. These cause disputes are largely coverage questions, which appraisal generally doesn’t resolve.</p>
<p>What helps either way is evidence gathered early:</p>
<ol>
<li>Photos and video of where the water entered, while it’s still visible.</li>
<li>The water line on walls and the depth of standing water.</li>
<li>Whether the floor drain or sump was overflowing, and whether the sump pump was running.</li>
<li>Any municipal notices about sewer surcharging in your neighborhood.</li>
<li>Mitigation reports, moisture readings and photos of removed materials.</li>
</ol>

<h2>Contaminated water</h2>
<p>Sewer backup water is usually treated as contaminated. That affects the scope: porous materials such as carpet, pad, drywall near the floor and some contents are often removed rather than dried. Estimates that treat a sewage backup like a clean-water leak tend to fall short on demolition, antimicrobial treatment, disposal and protective equipment.</p>

<h2>Where appraisal fits</h2>
<p>Appraisal is useful when the carrier accepts that the loss is covered under a particular coverage but disagrees on the amount. Common pricing gaps include:</p>
<ul>
<li>How much drywall, insulation and flooring needs to be removed.</li>
<li>Drying equipment days and mitigation charges.</li>
<li>Contents values and whether items can be cleaned.</li>
<li>Furnace, water heater and electrical components damaged by water.</li>
</ul>
<p>If the question is which coverage applies, or whether any does, that is a coverage dispute and a matter for a Wisconsin attorney.</p>

<h2>Planning ahead</h2>
<p>Pull out your declarations page before the next storm season. Check whether you have a backup endorsement, what its limit is and whether flood coverage makes sense for your property. Our <a href="/appraisal-solutions/water-sewer-backup-appraisal/">water and sewer backup appraisal</a> page explains how we approach basement claims, and the <a href="/insurance-appraisal-faq/">insurance appraisal FAQ</a> answers common questions about the process. If your loss involves frozen pipes rather than backup, see our <a href="/learning-center/ice-dam-insurance-claims/">ice dam claims guide</a> for related documentation tips.</p>
""",
    },
    {
        "slug": "derecho-straight-line-wind-claims",
        "title": "Derecho and Straight-Line Wind Claims: Why They Get Disputed and How to Scope Them",
        "seo": "Derecho & Straight-Line Wind Claims in Wisconsin",
        "desc": "What a derecho is, why straight-line wind claims in Wisconsin are often disputed, and how to scope roof, siding and tree damage thoroughly.",
        "date": "2026-10-20", "read": "7 min",
        "summary": "Derechos can damage thousands of properties in a single day. Here’s why wind claims get contested and how a thorough scope helps.",
        "body": """
<p>Wisconsin residents know tornadoes, from Barneveld in June 1984 and Oakfield in July 1996 to the August 18, 2005 outbreak that hit Stoughton and the May 2011 tornado in La Crosse. But some of the widest wind damage in the state comes from storms that never produce a funnel. The July 2019 derecho that tore through northern Wisconsin flattened forests, damaged homes and cabins, and left many owners with complicated <strong>derecho insurance claims</strong>.</p>

<h2>What a derecho is</h2>
<p>A derecho is a long-lived, widespread windstorm produced by a line or cluster of fast-moving thunderstorms. Instead of the rotating winds of a tornado, a derecho pushes damaging straight-line winds across a broad swath, often hundreds of miles long. Damage tends to be laid out in one direction, with trees and debris falling the same way across large areas.</p>
<p>For insurance purposes, the label matters less than the cause: most homeowners and commercial policies cover direct physical loss from windstorm, subject to the policy’s deductibles, exclusions and conditions. Policies vary, so read yours.</p>

<h2>Why wind claims get disputed</h2>
<h3>Wind versus wear</h3>
<p>The most common argument is whether missing or creased shingles were caused by the storm or by age and prior wear. Adjusters may approve a handful of shingle repairs while the owner sees a roof that can’t be reasonably repaired.</p>
<h3>Repairability</h3>
<p>Older or brittle shingles may not survive a repair. If lifting adjacent shingles to replace damaged ones breaks them, a spot repair may not be practical. That question often decides whether a slope or the whole roof is replaced.</p>
<h3>Hidden damage</h3>
<p>Wind can break the seal strip on shingles without tearing them off. It can loosen siding fasteners, rack fences and shift outbuildings. These problems are easy to miss on a quick inspection after a widespread storm.</p>
<h3>Trees</h3>
<p>Coverage for fallen trees varies. Many policies cover removal of a tree that falls on a covered structure, up to a limit, and the damage it caused. Trees that fall without striking anything are often treated differently. Check your policy’s debris removal and trees provisions.</p>
<h3>Volume</h3>
<p>After a large event, carriers bring in adjusters from elsewhere. Inspections can be rushed, and local pricing may not be reflected if labor and materials are in short supply.</p>

<h2>How to scope a wind claim</h2>
<p>A thorough scope addresses every part of the property that faced the wind. Use this as a checklist:</p>
<ol>
<li><strong>Roof.</strong> Missing, creased or unsealed shingles on every slope; ridge cap; starter course; flashing; vents and pipe boots; and any decking exposed or damaged.</li>
<li><strong>Siding and trim.</strong> Loose, cracked or missing panels; bent corners; soffit and fascia; window wraps.</li>
<li><strong>Gutters and downspouts.</strong> Pulled away, bent or detached sections.</li>
<li><strong>Windows and doors.</strong> Broken glass, damaged frames, garage doors pushed in or off track.</li>
<li><strong>Other structures.</strong> Detached garages, sheds, fences, decks, docks and, on farms, barns, pole buildings and grain bins.</li>
<li><strong>Interior.</strong> Water entry through damaged roofs or windows, with stains, wet insulation and contents.</li>
<li><strong>Trees and debris.</strong> Removal from structures, haul-off and any landscape coverage the policy provides.</li>
</ol>
<p>Document the direction of damage. Photos showing debris and trees laid out the same way support a wind event and help tie specific elevations to the storm.</p>

<h2>Estimating details that often get missed</h2>
<ul>
<li>Shingle seal-strip failure across a slope, not just the tabs that blew off.</li>
<li>Code-required items such as drip edge or ice and water shield, which may fall under ordinance or law coverage.</li>
<li>Matching where replacement shingles or siding can’t be found in the same line or color.</li>
<li>Steep, high or multi-story access charges.</li>
<li>Temporary repairs, tarping and board-up costs.</li>
<li>Overhead and profit when multiple trades are coordinated.</li>
</ul>

<h2>Deductibles after a wind event</h2>
<p>Some policies carry a separate wind or hail deductible, sometimes set as a percentage of the dwelling limit. As an illustrative example only, a 2 percent deductible on a $300,000 dwelling limit is $6,000. Run your own numbers with the <a href="/insurance-claim-calculators/percentage-deductible-calculator/">percentage deductible calculator</a>.</p>

<h2>When appraisal fits</h2>
<p>If the carrier agrees the storm caused covered damage but limits the repair to a few shingles or one elevation, the dispute is often about the amount and scope of loss, which is the kind of disagreement appraisal is designed for. Whether a particular item was caused by wind at all can blur into a coverage question; panels and courts handle that line differently, so document causation carefully.</p>
<p>Our <a href="/appraisal-solutions/tornado-straight-line-wind-appraisal/">tornado and straight-line wind appraisal</a> page explains how we approach these claims. For HOA, condo and commercial properties, see <a href="/appraisal-solutions/commercial-hoa-appraisal/">commercial and HOA appraisal</a>. Track deadlines in the <a href="/insurance-claim-calculators/claim-timeline-planner/">claim timeline planner</a>, and if a hailstorm came with the wind, our <a href="/learning-center/hail-claim-photo-checklist/">hail claim photo checklist</a> covers documentation. Legal questions about coverage or claim handling belong with a Wisconsin attorney.</p>
""",
    },
    {
        "slug": "matching-siding-and-shingles",
        "title": "Matching Siding and Shingles After a Claim: Discontinued Materials and Uniform Appearance",
        "seo": "Matching Siding and Shingles in Insurance Claims",
        "desc": "How matching disputes over discontinued siding and shingles usually arise in insurance claims, what policy wording says, and how to document them.",
        "date": "2026-11-05", "read": "7 min",
        "summary": "When replacement siding or shingles don’t match, a small repair can leave a patchwork. Here’s how matching disputes typically unfold.",
        "body": """
<p>A hailstorm dents the siding on two sides of a house. The carrier agrees to replace those two walls. But the siding line was discontinued years ago, and the closest product available is a different profile and a slightly different color. The repaired house now looks like two houses stitched together. That is the heart of a <strong>matching siding and shingles</strong> dispute.</p>
<p>How matching is handled depends on your policy language, the facts and, sometimes, the carrier’s own practices. Policies vary, and there is no single answer that applies to every Wisconsin claim.</p>

<h2>Why matching comes up so often</h2>
<ul>
<li><strong>Product lines change.</strong> Siding and shingle manufacturers discontinue colors, profiles and entire lines regularly.</li>
<li><strong>Weathering.</strong> Even the same product fades. New panels next to ten-year-old panels can look noticeably different.</li>
<li><strong>Partial damage.</strong> Hail and wind often damage one or two elevations or a few roof slopes, not the whole building.</li>
<li><strong>Continuous surfaces.</strong> Siding wraps around corners and roofs share ridgelines, so a visible line between old and new can be hard to avoid.</li>
</ul>

<h2>What policies typically say</h2>
<p>Many homeowners policies don’t mention matching by name. Instead, the question turns on how the loss settlement provision is worded, often a promise to pay to repair or replace damaged property with material of “like kind and quality.” Owners argue that a repair which leaves an obvious mismatch isn’t like kind and quality. Carriers may argue they only owe for the physically damaged portion.</p>
<p>Some policies and endorsements address matching directly. Certain endorsements limit payment to the damaged area only, or exclude cosmetic mismatch. Others provide some coverage for undamaged adjoining areas to achieve a reasonably uniform appearance. Read your declarations page and every endorsement, because this wording can decide the outcome.</p>

<h2>Common matching scenarios</h2>
<h3>Discontinued shingles</h3>
<p>If a few shingles on one slope are damaged and the product is no longer made, replacement shingles may differ in size, exposure or color. Mismatched dimensions can make a proper repair impossible, which supports replacing more of the roof. A shingle identification report, or a sample sent for analysis, helps show what was originally installed.</p>
<h3>Discontinued siding</h3>
<p>Siding profiles, such as the width of the lap and the texture, change between lines. Even a close color in a different profile is often visible. Owners frequently argue for replacing all elevations visible together, or the full wall to a natural break such as a corner.</p>
<h3>Weathered but available</h3>
<p>When the same product is still available but new material looks different next to weathered material, the dispute is usually about how far the replacement must extend to look reasonable.</p>
<h3>Interior finishes</h3>
<p>Matching issues also arise inside: flooring that runs continuously through several rooms, cabinets, countertops and tile. The same documentation principles apply.</p>

<h2>How to document a matching issue</h2>
<ol>
<li><strong>Identify the product.</strong> Find labels, leftover materials, original invoices or builder records. A siding or shingle identification service can help.</li>
<li><strong>Prove availability.</strong> Get written confirmation from suppliers or the manufacturer that the product is discontinued or not available in your color.</li>
<li><strong>Show the visual.</strong> Photograph the closest available material held against the existing siding or shingles in daylight.</li>
<li><strong>Map sightlines.</strong> Photograph each elevation to show which walls or slopes are visible together.</li>
<li><strong>Get a contractor’s opinion in writing.</strong> Explain why a partial repair can’t be done properly or won’t produce a reasonable appearance.</li>
</ol>

<h2>Where appraisal fits</h2>
<p>Whether an appraisal panel can decide a matching question depends on how the dispute is framed and on the policy. If the carrier says matching is never covered under your policy, that’s a coverage position, and a Wisconsin attorney can advise you on it. If the carrier accepts that some extended replacement is owed but disagrees on how far it must extend or what it costs, the panel can often value it.</p>
<p>A practical approach many panels use is to value the disputed matching items separately in the award. That way, if coverage for those items is later resolved one way or the other, the numbers are already set.</p>

<h2>Illustrative example</h2>
<p>An illustrative example only: a carrier’s estimate replaces siding on the north and west walls. The owner’s appraiser documents that the siding line is discontinued and that the east wall is visible from the same corner. The award lists the north and west walls as agreed, and the east and south walls as a separate line so that a later coverage decision can be applied directly.</p>

<h2>Next steps</h2>
<p>Start by reading your loss settlement provision and any endorsements on matching or cosmetic damage. Then gather product identification and availability evidence before the adjuster’s next visit. If storm photos are still on your to-do list, our <a href="/learning-center/hail-claim-photo-checklist/">hail claim photo checklist</a> covers what to capture. For an outside look at the carrier’s numbers, see <a href="/appraisal-solutions/carrier-estimate-review/">carrier estimate review</a>, and for the process as a whole, the <a href="/appraisal-solutions/home-insurance-appraisal/">home insurance appraisal</a> page explains how we help. Questions? <a href="/contact-us/">Contact us</a>.</p>
""",
    },
]
