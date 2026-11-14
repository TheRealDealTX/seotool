"""Resources: appraisal process steps, FAQ, glossary and policy/claim guides (Pennsylvania)."""

PROCESS_INTRO = """<p>Insurance appraisal is a valuation process written into most Pennsylvania homeowner, renter, landlord and commercial property policies. It is built for one narrow situation: your insurer agrees the loss is covered, at least in part, but the two of you can’t agree on what it costs to fix. The eight steps below follow a typical Pennsylvania claim from that first disagreement through the signed award and the check. Your own policy’s wording controls every step, so keep a copy of the full policy — not just the declarations page — next to you as you read.</p>"""

PROCESS_STEPS = [
    ("Pin down the disagreement", """<p>Appraisal works best when everyone knows exactly what is in dispute. Start by laying your insurer’s estimate next to your contractor’s estimate and marking every difference: missing rooms, roof squares, pricing, code items, matching, overhead and profit, contents or additional living expense.</p>
<p>Put your position in writing to the adjuster, with photos, measurements and invoices attached. A clear supplement request sometimes closes the gap without appraisal at all. If it doesn’t, you now have a tidy list of the line items an appraisal panel will need to value — and a record showing that the dispute is about the <strong>amount</strong> of loss, not whether the loss is covered.</p>"""),
    ("Check the policy and the suit-limitation date", """<p>Read the appraisal provision itself. Note who can demand appraisal, how many days each side has to name an appraiser, how the umpire is chosen and how fees are split. Look for any requirement to submit a sworn proof of loss first.</p>
<p>Then find the suit-limitation clause. Many Pennsylvania property policies require any lawsuit to be filed within one year of the date of loss, and Pennsylvania courts have generally enforced those clauses. Appraisal may not pause that clock unless the policy or a written agreement says it does. Mark the date on your calendar now, and if it is anywhere near, talk to a Pennsylvania attorney before you go further.</p>"""),
    ("Send the written appraisal demand", """<p>Either you or the insurer can invoke appraisal. The demand should be in writing and should:</p>
<ul>
<li>identify the policy number, claim number and date of loss;</li>
<li>state that the parties disagree on the amount of loss;</li>
<li>cite the appraisal provision of the policy; and</li>
<li>name your appraiser, or confirm you will do so within the policy’s time frame.</li>
</ul>
<p>Send it in a way you can prove, such as certified mail plus email, and keep copies of everything. If the insurer responds by disputing coverage for part of the claim, note that in writing — appraisal will usually value only the items the panel is allowed to decide.</p>"""),
    ("Each side names an appraiser", """<p>Each party picks its own appraiser. Most policies call for a “competent and disinterested” or “competent and independent” appraiser, and many give each side 20 days from the demand to make the choice — your policy will say.</p>
<p>Competent means the person understands construction, estimating software, local pricing and the type of damage involved, whether that is a slate roof in Scranton or a smoke-damaged twin in Allentown. Disinterested means no financial stake in the result beyond a reasonable fee. Your appraiser reviews the file, inspects the property and builds an independent valuation. The insurer’s appraiser does the same, and the two exchange estimates before they meet.</p>"""),
    ("The appraisers pick an umpire (or a court of common pleas appoints one)", """<p>The two appraisers choose a neutral umpire, ideally early so one is ready if needed. The umpire’s job is limited: decide only the items the appraisers can’t settle between themselves.</p>
<p>If the appraisers can’t agree on an umpire within the policy’s window (often 15 days), policies typically let either party ask a court of record in the county where the property is located to appoint one. In Pennsylvania that is generally the county court of common pleas. The exact wording and timing come from your policy, so read it before filing anything, and consider having a Pennsylvania attorney handle the petition.</p>"""),
    ("Appraisers inspect and negotiate", """<p>This is where most of the work happens. The two appraisers walk the property together, confirm measurements, look at hidden damage that was opened up after the first inspection, and compare unit pricing for the local market.</p>
<p>They then go line by line. Some items fall away quickly once both sides see the same evidence; others — matching siding on a stone-and-frame farmhouse, the number of slate squares on a steep Victorian roof, whether a code upgrade is triggered — take real discussion. When the appraisers agree on every disputed item, they sign an award together and no umpire decision is needed. A good share of appraisals end right here.</p>"""),
    ("Umpire decides what’s left", """<p>Anything the appraisers can’t resolve goes to the umpire. Each appraiser presents a written position with photos, measurements, invoices, pricing data and code references. The umpire may inspect the property, ask questions of both appraisers or hold an informal meeting.</p>
<p>The umpire then decides each open item, usually by choosing one side’s figure or landing somewhere in between based on the evidence. An umpire is not there to rewrite the policy or rule on coverage; the decision is about value. Clear, well-organized submissions make the umpire’s job easier and tend to produce a cleaner award.</p>"""),
    ("Award signed and payment issued", """<p>An award signed by any two of the three panel members generally sets the amount of loss. A well-built award separates replacement cost value, depreciation and actual cash value, and breaks figures out by coverage — dwelling, other structures, contents and loss of use.</p>
<p>The insurer then pays according to the policy, subtracting the deductible and any earlier payments. Recoverable depreciation is typically released once repairs are completed and documented. Pennsylvania courts generally treat appraisal awards much like common-law arbitration, so they are hard to overturn absent fraud, misconduct, corruption or a similar irregularity. If payment stalls after the award, talk to a Pennsylvania attorney.</p>"""),
]

PROCESS_OUTRO = """<h2>What appraisal can’t decide</h2>
<ul>
<li>Whether a loss is covered, or whether an exclusion such as flood or earth movement applies.</li>
<li>Bad-faith claims, interest, punitive damages or attorney fees.</li>
<li>Whether your suit-limitation deadline has been paused or extended.</li>
<li>Any amount above your policy limits.</li>
</ul>
<div class="note"><b class="h">Fees</b>Each side normally pays its own appraiser, and umpire fees are usually split equally — check your policy. Ask any appraiser, including us, to put the fee arrangement in writing before you sign anything.</div>
<p>For coverage disputes, bad-faith questions or deadline concerns, talk to a Pennsylvania attorney who handles insurance claims. Our role is valuation: building and defending an accurate number for the loss.</p>"""

PROCESS_BODY = (
    PROCESS_INTRO
    + "".join(f"\n<h2>Step {i} — {name}</h2>\n{html}" for i, (name, html) in enumerate(PROCESS_STEPS, 1))
    + "\n" + PROCESS_OUTRO
)

FAQ = [
    ("Getting started", [
        ("What is insurance appraisal?", "It’s a process in most property policies for settling disagreements about the amount of a covered loss. Each side names an appraiser, the appraisers pick an umpire, and an award signed by any two of the three sets the amount."),
        ("When does appraisal make sense?", "When the insurer accepts that the loss is covered but its estimate is well below what repairs actually cost. It is a poor fit when the claim has been denied outright or when the gap is small compared with the fees."),
        ("Who can demand appraisal?", "Either you or the insurance company, as long as the policy contains an appraisal provision. The demand should be in writing and should cite that provision."),
        ("Is an insurance appraiser the same as a real estate appraiser?", "No. A real estate appraiser estimates what a property would sell for. An insurance appraiser values the cost to repair or replace damaged property under the terms of the policy."),
        ("What’s the difference between a public adjuster, an appraiser and an attorney?", "A public adjuster is licensed by the Pennsylvania Insurance Department to prepare and negotiate your claim with the insurer. An appraiser serves on an appraisal panel to value a disputed loss, and an attorney gives legal advice and handles coverage, bad-faith and litigation issues."),
    ]),
    ("Costs and fees", [
        ("How much does an insurance appraiser cost?", "Arrangements vary and can include flat fees, hourly rates or other structures. Each side pays its own appraiser and usually half of the umpire’s fee, so get the terms in writing before you sign."),
        ("Who pays the umpire?", "Most policies split the umpire’s fee equally between you and the insurer. Your policy’s appraisal clause will spell out the split."),
        ("Is appraisal worth it for a small difference?", "Often not. If the gap is only a few thousand dollars, fees can absorb most of any increase, so run the numbers with our claim gap fee projector before deciding."),
        ("Can I get my appraisal costs back from the insurer?", "Usually not through the appraisal itself, since the panel decides the amount of loss rather than fees or damages. Ask a Pennsylvania attorney whether any other route applies to your situation."),
    ]),
    ("Timing and deadlines", [
        ("How long does appraisal take?", "Many residential appraisals wrap up within a couple of months once both appraisers are named. Large commercial losses, heavy contents claims or disputes that need an umpire can take longer."),
        ("Does appraisal stop the one-year suit clause?", "Not necessarily. Many Pennsylvania policies require a lawsuit within one year of the date of loss, courts have generally enforced that, and appraisal may not pause the clock unless the policy or a written agreement says so — talk to a Pennsylvania attorney early."),
        ("How long do I have to name my appraiser?", "Many policies allow 20 days from the written demand, but the number varies. Check your policy on the day you send or receive a demand."),
        ("Is there a deadline to demand appraisal?", "Some policies set one and many don’t, but waiting can still hurt you because the suit-limitation clause keeps running. Document the dispute and decide promptly."),
        ("What happens if the appraisers can’t agree on an umpire?", "Policies typically let either party ask a court of record in the county where the property sits to appoint one, which in Pennsylvania is generally the county court of common pleas. Your policy will say how and when."),
    ]),
    ("Pennsylvania rules and agencies", [
        ("Who regulates insurance companies in Pennsylvania?", "The Pennsylvania Insurance Department, led by the Insurance Commissioner. It accepts consumer complaints about insurers and licenses public adjusters."),
        ("What is the Pennsylvania FAIR Plan?", "It’s the state’s insurer of last resort for property owners who can’t find coverage in the regular market. FAIR Plan policies have their own terms, so read the appraisal and suit-limitation language carefully."),
        ("Does Pennsylvania have a bad-faith law?", "Yes. Pennsylvania’s bad-faith statute (42 Pa.C.S. § 8371) lets a court award interest, punitive damages, court costs and attorney fees if it finds an insurer acted in bad faith toward its insured, but appraisal does not decide bad faith."),
        ("Does my homeowner policy cover flood or mine subsidence?", "Standard homeowner policies exclude flood, which requires an NFIP or private flood policy, and usually exclude earth movement. The Mine Subsidence Insurance program run by the Pennsylvania Department of Environmental Protection offers separate coverage for damage from underground coal mine collapse."),
        ("Are there rules about how fast insurers must handle claims?", "Pennsylvania’s Unfair Insurance Practices Act and related claim-handling regulations set general standards for prompt, fair handling. If you believe an insurer is ignoring them, you can file a complaint with the Pennsylvania Insurance Department."),
    ]),
    ("Working with your insurer and contractor", [
        ("Will demanding appraisal upset my insurer?", "Appraisal is a normal part of the policy and insurers use it too. Keeping communication professional and well documented helps the process run smoothly."),
        ("Can my roofer or contractor be my appraiser?", "Usually not a good idea, because most policies require a disinterested appraiser and a contractor who will do the work has a stake in the result. Your contractor can still supply estimates, photos and testimony to your appraiser."),
        ("Should I keep talking to the adjuster during appraisal?", "Yes, stay responsive and keep everything in writing. Your appraiser handles the valuation discussions with the other appraiser, but the insurer may still need documents or access."),
        ("Can I start repairs before the appraisal is finished?", "You generally must take reasonable steps to prevent further damage, and that mitigation should be documented with photos and receipts. Before major permanent repairs, make sure both appraisers have seen or recorded the damage."),
    ]),
]

GLOSSARY = [
    ("Actual cash value (ACV)", "Replacement cost minus depreciation. Many policies pay ACV first and the balance after repairs are done."),
    ("Additional living expense (ALE)", "Coverage for the extra cost of living elsewhere while your home is unlivable after a covered loss, often part of Coverage D."),
    ("Amount of loss", "The dollar value of a covered loss — the question an appraisal panel is normally limited to deciding."),
    ("Appraisal award", "The written decision signed by at least two of the three panel members that sets the amount of loss."),
    ("Appraisal clause", "The policy provision that lets either party demand appraisal when they disagree on the amount of a covered loss."),
    ("Bad faith", "Unreasonable conduct by an insurer toward its insured. Pennsylvania’s bad-faith statute lets a court award certain remedies; appraisal does not decide it."),
    ("Building code upgrade (ordinance or law)", "Coverage for extra costs needed to bring repaired work up to current building codes, often subject to its own limit."),
    ("Coverage A", "Dwelling coverage for the house itself and attached structures."),
    ("Coverage B", "Other structures coverage for detached garages, fences, sheds and similar buildings."),
    ("Coverage C", "Personal property coverage for furniture, clothing, electronics and other belongings."),
    ("Coverage D", "Loss of use coverage, including additional living expense or fair rental value."),
    ("Declarations page", "The summary page of a policy showing the insured, property, coverages, limits, deductibles and policy period."),
    ("Deductible", "The portion of a covered loss you pay before the insurer pays, subtracted from the claim payment."),
    ("Depreciation", "A reduction in value for age, wear and condition, used to calculate actual cash value."),
    ("Disinterested appraiser", "An appraiser with no financial stake in the outcome beyond a reasonable fee, as most appraisal clauses require."),
    ("Earth movement exclusion", "Policy language that excludes damage from earthquakes, landslides, subsidence, sinkholes and similar ground movement, with limited exceptions."),
    ("FAIR Plan", "The Pennsylvania FAIR Plan, the state’s insurer of last resort for property owners who can’t get coverage in the regular market."),
    ("Flood exclusion", "Standard homeowner policy language excluding damage from surface water and rising water; flood coverage comes from NFIP or private flood policies."),
    ("Holdback", "The recoverable depreciation an insurer withholds until repairs are completed and documented."),
    ("Ice dam", "A ridge of ice at the roof edge that traps melting snow, which can back up under shingles and leak into the home."),
    ("Line item", "A single entry in an estimate, such as a quantity of drywall or roofing, with its unit price and total."),
    ("Matching", "The question of whether undamaged materials must be replaced so repairs reasonably match in color, texture or style."),
    ("Mine Subsidence Insurance (MSI)", "A program run by the Pennsylvania Department of Environmental Protection that covers damage from the collapse of underground coal mines."),
    ("Mitigation", "Reasonable steps to prevent further damage after a loss, such as tarping a roof or drying out a wet basement."),
    ("NFIP", "The National Flood Insurance Program, the federal program that writes most flood insurance policies."),
    ("Overhead and profit (O&P)", "A general contractor’s charges for overhead and profit, commonly added when a repair needs coordination of several trades."),
    ("Party wall", "A shared wall between two attached homes, common in rowhomes and twins, which can complicate repair scope and responsibility."),
    ("Pennsylvania Insurance Department", "The state agency, led by the Insurance Commissioner, that regulates insurers, takes consumer complaints and licenses public adjusters."),
    ("Proof of loss", "A sworn statement of the amount claimed, which some policies require within a set time after the insurer asks."),
    ("Public adjuster", "A professional licensed by the Pennsylvania Insurance Department to prepare and negotiate a claim on the policyholder’s behalf for a fee."),
    ("Recoverable depreciation", "Depreciation that can be paid back once repairs or replacement are completed under a replacement cost policy."),
    ("Replacement cost value (RCV)", "The cost to repair or replace damaged property with materials of like kind and quality, without a deduction for depreciation."),
    ("Reservation of rights", "A letter in which an insurer handles a claim while reserving the right to deny coverage later."),
    ("Roof square", "A roofing unit equal to 100 square feet of roof surface."),
    ("Scope of loss", "The full description of damaged areas and the repairs needed, separate from pricing."),
    ("Statement of loss", "The insurer’s summary of the claim showing RCV, depreciation, deductible, prior payments and the net amount paid."),
    ("Suit-limitation clause", "Policy language limiting the time to sue the insurer, commonly one year from the date of loss in Pennsylvania property policies."),
    ("Supplement", "A request to add items or costs to an estimate after hidden damage is found or pricing changes."),
    ("Umpire", "The neutral third member of an appraisal panel who decides items the two appraisers can’t agree on."),
    ("Unfair claims practices", "Claim-handling conduct the Unfair Insurance Practices Act and related regulations prohibit, such as failing to respond or investigate promptly."),
    ("Wind-driven rain", "Rain forced into a building by wind; coverage often depends on whether the wind first created an opening."),
    ("Xactimate", "Estimating software widely used by insurers, adjusters and contractors to price property repairs."),
]

POSTS = [
    {
        "slug": "pennsylvania-appraisal-clause-guide",
        "title": "The Pennsylvania Appraisal Clause: A Plain-English Guide",
        "seo": "Pennsylvania Appraisal Clause: Plain-English Guide",
        "desc": "Read the Pennsylvania appraisal clause line by line: who can demand it, how appraisers and umpires are picked, and what the award can decide.",
        "keyword": "Pennsylvania appraisal clause",
        "summary": "The appraisal paragraph is short, but every phrase shapes how your dispute will run. Here’s what each part usually means in practice.",
        "date": "2026-08-06", "read": "7 min",
        "body": """
<p>Most Pennsylvania homeowners read the appraisal clause for the first time after the adjuster’s estimate arrives and the number looks wrong. The paragraph is usually short — a few sentences buried near the end of the conditions section — but it controls how a valuation dispute will be resolved. This guide walks through the pieces that appear in most policies. Wording varies by insurer and form, so treat this as a map, and read your own policy for the actual route.</p>
<h2>The trigger: a disagreement about the amount of loss</h2>
<p>Nearly every clause opens with some version of “if you and we fail to agree on the amount of loss.” That phrase defines the job. Appraisal is for disputes about <strong>how much</strong> a covered loss costs to repair or replace. It isn’t designed to decide whether the loss is covered in the first place.</p>
<p>In real claims, the line between amount and coverage can blur. Consider a hailstorm in south-central Pennsylvania: if the insurer agrees hail damaged the roof but pays for two slopes instead of four, that sounds like an amount question. If it says the remaining slopes show wear rather than hail, it may call that a causation or coverage issue. Expect some back-and-forth, and keep your evidence focused on scope and cost.</p>
<h2>Either party may demand appraisal</h2>
<p>Most clauses let either side start the process with a written demand. That means you can invoke appraisal, and so can your insurer. A good demand names the policy and claim numbers, states that you disagree on the amount of loss, cites the appraisal provision and names your appraiser or confirms you will.</p>
<p>Some policies list conditions that come first, such as a sworn proof of loss or an examination under oath when requested. Check for those before you send anything, because skipping a required step can give the other side something to argue about.</p>
<h2>Competent and disinterested appraisers</h2>
<p>Each side then picks its own appraiser, often within 20 days of the demand. Two words do most of the work here.</p>
<h3>Competent</h3>
<p>The appraiser should understand the kind of property and damage involved. A flat modified-bitumen roof on a Philadelphia rowhome, a slate roof in an older Scranton neighborhood and a smoke-damaged commercial building in Harrisburg all call for different knowledge. Ask a prospective appraiser about relevant experience, but be wary of anyone who promises a result.</p>
<h3>Disinterested</h3>
<p>The appraiser shouldn’t have a financial stake in the outcome beyond a reasonable fee. That’s why the contractor who will do the work is usually a poor choice, even though their estimate and photos can be very useful to your appraiser.</p>
<h2>The umpire and the court of common pleas</h2>
<p>The two appraisers choose a neutral umpire. If they can’t agree within the policy’s window — often 15 days — policies typically let either party ask a court of record in the county where the property is located to appoint one. In Pennsylvania that generally means the county court of common pleas. Your policy will say exactly how this works, and many people have a Pennsylvania attorney handle that petition.</p>
<p>The umpire only steps in on items the two appraisers can’t settle. In many claims the appraisers resolve everything themselves and sign an agreed award.</p>
<h2>The award and what it binds</h2>
<p>Most clauses say an award in writing signed by any two of the three sets the amount of loss. Pennsylvania courts generally treat appraisal awards much like common-law arbitration, so they are hard to overturn absent fraud, misconduct, corruption or a similar irregularity. That makes preparation important: a panel decision is usually the final word on value.</p>
<p>The award typically doesn’t decide coverage, bad faith, interest or fees. Pennsylvania’s bad-faith statute (42 Pa.C.S. § 8371) lets a court award interest, punitive damages, court costs and attorney fees if it finds an insurer acted in bad faith toward its insured. Appraisal does not decide bad faith, so those questions belong with a Pennsylvania attorney.</p>
<div class="note"><b class="h">Watch the clock</b>Many Pennsylvania property policies require any lawsuit to be filed within one year of the date of loss, and appraisal may not pause that deadline unless the policy or a written agreement says so. Read our guide to the <a href="/policy-and-claim-guides/one-year-suit-limitation-and-appraisal/">one-year suit limitation</a> and talk to an attorney early.</div>
<h2>Fees and costs</h2>
<p>Most clauses say each side pays its own appraiser and the umpire’s fee is split equally. Some add that other appraisal expenses are shared the same way. Before you hire anyone, get the fee terms in writing and compare them against the size of the gap you’re trying to close. Our <a href="/claim-calculators/claim-gap-fee-projector/">claim gap fee projector</a> can help you test whether appraisal makes financial sense.</p>
<h2>Putting it to work</h2>
<p>Before demanding appraisal, gather the full policy, every estimate and payment letter, photos from before and after any mitigation, and your contractor’s scope. Write down each disputed line item. When those pieces are organized, the process tends to move faster and the panel has what it needs. If you’d like an independent look at your file, our <a href="/property-appraisal-services/appraisal-demand-representation/">appraisal demand representation</a> page explains how we work as your appointed appraiser.</p>
""",
    },
    {
        "slug": "one-year-suit-limitation-and-appraisal",
        "title": "The One-Year Suit Clause and Appraisal in Pennsylvania",
        "seo": "One-Year Suit Limitation and Appraisal in PA",
        "desc": "Many Pennsylvania policies set a one-year suit limitation. See how it interacts with appraisal and why to call an attorney well before it.",
        "keyword": "one-year suit limitation",
        "summary": "A clause many owners never notice can end their right to sue a year after the loss. Here’s how it overlaps with an appraisal timeline.",
        "date": "2026-08-27", "read": "7 min",
        "body": """
<p>Ask a homeowner how long they have to resolve an insurance claim and you’ll hear guesses ranging from a few months to several years. The real answer is in the policy. Many Pennsylvania property policies contain a suit-limitation clause that requires any lawsuit against the insurer to be filed within one year of the date of loss, and Pennsylvania courts have generally enforced those clauses. For anyone heading into appraisal, that single sentence can matter more than any line item.</p>
<p>We are appraisers, not lawyers. This article explains how the deadline and appraisal fit together in practical terms so you know when to bring in a Pennsylvania attorney. It is not legal advice.</p>
<h2>What a suit-limitation clause says</h2>
<p>The language often appears in the conditions section under a heading such as “Suit Against Us.” A typical version says no action can be brought unless the policy’s terms have been followed and the action is started within one year after the date of loss. Some forms use a different period; commercial policies and FAIR Plan policies have their own wording. The only reliable source is your own complete policy.</p>
<h3>The date of loss</h3>
<p>The clock usually runs from the date of loss — the day of the storm, freeze, fire or pipe break — not from the date you filed the claim or received the estimate. For a burst pipe that wasn’t discovered right away, or a slow roof leak, the date of loss itself can be disputed. Write down what you know and how you know it.</p>
<h2>Why appraisal doesn’t automatically stop the clock</h2>
<p>Appraisal can take weeks or months, especially after a regional storm when appraisers, umpires and contractors are busy. Meanwhile, the suit-limitation period keeps running unless something stops it. Appraisal may not pause that clock unless the policy or a written agreement says so.</p>
<p>That matters because appraisal resolves only the amount of loss. If a coverage dispute remains — the insurer says part of the damage is excluded, or the award is not paid — you may need to file suit to protect your rights. If the year has passed, that option may be gone.</p>
<div class="note"><b class="h">Practical rule</b>The moment you see a real disagreement with your insurer, find the suit-limitation clause, write the deadline on your calendar and talk to a Pennsylvania attorney about whether a written tolling agreement or other step makes sense. Do this before the appraisal starts, not near the end of it.</div>
<h2>A timeline that shows the squeeze</h2>
<p>Here is an illustrative claim. A windstorm damages a roof and siding in early spring. The first inspection takes three weeks, the estimate arrives a month later, and the supplement discussion drags on for two more months. By early summer, the owner demands appraisal. Each side names an appraiser within the policy’s 20 days, the appraisers spend six weeks scheduling a joint inspection, and the umpire selection stalls. By the end of autumn, roughly eight or nine months have passed and the panel still hasn’t signed an award.</p>
<p>Nothing unusual happened in that example. It simply shows how a year can disappear. Our <a href="/claim-calculators/claim-deadline-calendar/">claim deadline calendar</a> lets you map your own dates and see how much room remains.</p>
<h2>Steps that help protect your position</h2>
<ul>
<li><strong>Get the full policy.</strong> Request a certified copy from your insurer if you don’t have one. The declarations page alone won’t show the suit clause or appraisal provision.</li>
<li><strong>Keep a dated file.</strong> Save every letter, email, estimate and payment notice, along with notes of phone calls.</li>
<li><strong>Move promptly.</strong> Delay rarely helps a policyholder. Decide on appraisal when the dispute is clear.</li>
<li><strong>Put agreements in writing.</strong> If an adjuster suggests the deadline is flexible, ask for that in a signed writing — and have an attorney review it.</li>
<li><strong>Call counsel early.</strong> A Pennsylvania attorney can explain whether any exception, tolling agreement or filing strategy fits your situation.</li>
</ul>
<h2>Where appraisal still helps</h2>
<p>None of this means appraisal is a bad idea. For a covered loss where the only real dispute is price and scope, it is often faster and less expensive than litigation, and the award is generally hard to overturn absent fraud, misconduct, corruption or a similar irregularity. The point is to run appraisal with the deadline in view, so that if something goes sideways you still have options.</p>
<p>Bad-faith questions also sit outside appraisal. Pennsylvania’s bad-faith statute (42 Pa.C.S. § 8371) lets a court award interest, punitive damages, court costs and attorney fees if it finds an insurer acted in bad faith toward its insured. Appraisal does not decide bad faith, and those claims have their own timing rules an attorney can explain.</p>
<h2>Next steps</h2>
<p>If you are early in a dispute, our <a href="/claim-calculators/appraisal-readiness-checkup/">appraisal readiness checkup</a> walks through the documents and decisions to gather first. For a closer look at the policy language itself, see our <a href="/policy-and-claim-guides/pennsylvania-appraisal-clause-guide/">Pennsylvania appraisal clause guide</a>. And if the calendar is already tight, call an attorney today — then call us about the valuation.</p>
""",
    },
    {
        "slug": "flood-or-water-damage-after-tropical-remnants",
        "title": "Flood or Water Damage? Claims After Tropical Remnants",
        "seo": "Flood vs Water Damage After Tropical Remnants",
        "desc": "Is it flood or water damage? After tropical remnants, Pennsylvania policies split the two. See which pays and where appraisal helps on value.",
        "keyword": "flood or water damage",
        "summary": "When remnants of a tropical storm stall over Pennsylvania, the cause of the water decides which policy pays. Here’s how to sort it out.",
        "date": "2026-09-17", "read": "8 min",
        "body": """
<p>Pennsylvania doesn’t take many direct hurricane hits, but the remnants of tropical systems have shaped the state’s claim history for generations. Agnes in June 1972 sent the Susquehanna through Wilkes-Barre and Harrisburg. The remnants of Ivan flooded the Pittsburgh area in September 2004. Tropical Storm Lee soaked Bloomsburg in 2011. On September 1, 2021, the remnants of Ida pushed the Schuylkill into Manayunk and neighboring river towns while an EF2 tornado tore through Upper Dublin in Montgomery County. In August 2024, the remnants of Debby caused flash flooding in Tioga County.</p>
<p>Those storms share a pattern: they deliver more rain than wind, and the resulting claims turn on one question — where did the water come from?</p>
<h2>Why the source of water matters</h2>
<p>A standard homeowner policy excludes flood. Flood coverage comes from a separate policy, usually through the NFIP or a private flood insurer. So when water ends up in your basement or living room after tropical remnants, the insurer’s first step is to classify the water.</p>
<h3>Usually treated as flood</h3>
<ul>
<li>Rising rivers and creeks that overflow onto your property.</li>
<li>Surface water flowing across the ground and entering through doors, windows or basement walls.</li>
<li>Mudflow carried by floodwater.</li>
</ul>
<h3>Often treated as water damage under a homeowner policy</h3>
<ul>
<li>Rain entering through an opening created by wind, such as a torn roof or broken window.</li>
<li>Water from a burst pipe or failed appliance.</li>
<li>Sewer or drain backup, if you bought that endorsement.</li>
</ul>
<p>The exact wording differs between policies, and many forms limit wind-driven rain unless wind first created an opening. Read the definitions and exclusions carefully.</p>
<div class="note"><b class="h">Coverage is not appraisal’s job</b>Whether water counts as flood is a coverage question. Appraisal values the amount of a covered loss; it doesn’t decide which policy applies. If your insurer has denied part of a claim as flood, talk to a Pennsylvania attorney about the coverage question.</div>
<h2>When one storm creates two claims</h2>
<p>Tropical remnants often produce both kinds of damage at once. Wind can lift shingles and drive rain into an upstairs bedroom, while a nearby creek fills the basement. If you carry both homeowner and flood coverage, you may have two claims with two adjusters, two estimates and two sets of rules.</p>
<p>That overlap creates real valuation problems. Each insurer may try to assign shared damage — drywall, flooring, electrical work — to the other policy. Careful documentation helps: photos showing water lines, the path of roof leaks, and the order in which areas got wet. A clean record makes it easier for everyone to separate the damage.</p>
<h3>Does flood insurance have appraisal?</h3>
<p>NFIP policies contain their own appraisal provision, and private flood policies vary. The rules, deadlines and limits are not the same as your homeowner policy, so read each policy separately. Proof-of-loss timing under flood policies can be especially strict.</p>
<h2>Common valuation disputes after tropical remnants</h2>
<p>Once coverage is settled, the disagreement is usually about the amount. Typical issues include:</p>
<ul>
<li><strong>Drying and mitigation charges.</strong> The number of days, equipment counts and whether antimicrobial treatment was reasonable.</li>
<li><strong>Height of drywall removal.</strong> Whether a flood cut at two feet is enough or wicking moisture required more.</li>
<li><strong>Finished basements.</strong> Many policies limit what they pay for basement finishes and contents; the scope still has to be priced correctly.</li>
<li><strong>Matching flooring.</strong> When water damages part of a continuous floor, whether adjoining areas must be replaced for a reasonable match.</li>
<li><strong>Interior roof leak damage.</strong> Ceilings, insulation and framing in older homes where wet plaster and lath are involved.</li>
</ul>
<h2>Steps to take after the water recedes</h2>
<ol>
<li>Make the property safe and prevent further damage. Document every mitigation step with photos and receipts.</li>
<li>Photograph water lines, damaged materials and contents before they are removed.</li>
<li>Report the claim to every insurer that might apply — homeowner and flood — promptly.</li>
<li>Get copies of every policy and note the suit-limitation and proof-of-loss deadlines.</li>
<li>Keep samples of flooring, cabinets or trim where possible, for later matching discussions.</li>
</ol>
<p>Then compare each estimate to your contractor’s scope. If the coverage is accepted but the number is low, our <a href="/property-appraisal-services/tropical-storm-remnant-appraisal/">tropical storm remnant appraisal</a> service and our <a href="/property-appraisal-services/water-damage-claim-appraisal/">water damage claim appraisal</a> work focus on that valuation gap.</p>
<h2>Deadlines still apply</h2>
<p>After a regional storm, contractors and adjusters are stretched thin and weeks can pass quickly. Many Pennsylvania property policies require a lawsuit within one year of the date of loss, and appraisal may not pause that clock unless the policy or a written agreement says so. Flood policies carry their own deadlines. Read our guide to the <a href="/policy-and-claim-guides/one-year-suit-limitation-and-appraisal/">one-year suit limitation</a> and keep a calendar from the start.</p>
""",
    },
    {
        "slug": "ice-dam-and-frozen-pipe-claims",
        "title": "Ice Dam and Frozen Pipe Claims: A Pennsylvania Guide",
        "seo": "Ice Dam and Frozen Pipe Claims in Pennsylvania",
        "desc": "Ice dam and frozen pipe claims spike every Pennsylvania winter. Learn what policies cover, where estimates fall short and how to document.",
        "keyword": "ice dam and frozen pipe claims",
        "summary": "Freeze-thaw cycles hit Pennsylvania homes hard. Here’s how ice dam and burst pipe claims usually work and where the numbers get disputed.",
        "date": "2026-10-08", "read": "7 min",
        "body": """
<p>Pennsylvania winters are rarely gentle on houses. Heavy snow followed by a thaw and another hard freeze is a recipe for ice dams on the roof and split pipes in the walls. The Blizzard of 1993, the January 1996 storm, the Valentine’s Day 2007 ice storm, the back-to-back snowstorms of February 2010 and Erie’s Christmas 2017 lake-effect snow — more than 60 inches in about two days — all produced waves of winter claims. Every cold snap since has added more.</p>
<p>These claims are often accepted but underpaid. Here is how they typically work and where the valuation fights tend to happen.</p>
<h2>How ice dams cause damage</h2>
<p>Heat escaping from the living space warms the roof deck and melts snow on the upper roof. The meltwater runs down to the colder eaves and refreezes, building a ridge of ice. More meltwater pools behind that ridge, works under the shingles and leaks into soffits, walls and ceilings.</p>
<p>Older Pennsylvania housing is especially prone: Victorian homes in Scranton and Erie with complex rooflines, Cape Cods with little attic ventilation, and rowhomes with flat or low-slope roofs where water has nowhere to go.</p>
<h3>Coverage questions</h3>
<p>Many homeowner policies cover sudden water damage from an ice dam, though some limit or exclude damage to the roof itself or to gutters. Insurers may also argue the damage is long-term leakage or a maintenance issue. Those are coverage arguments; if you face one, talk to a Pennsylvania attorney. When the insurer accepts the claim, the dispute shifts to scope and cost.</p>
<h2>How frozen pipes cause damage</h2>
<p>Water expands as it freezes. A pipe in an exterior wall, crawlspace or unheated garage can split, and the leak often doesn’t show until the ice thaws. By then water may have run for hours inside walls, under floors or into a finished basement.</p>
<p>Policies commonly cover sudden and accidental discharge from plumbing but may exclude freezing damage if the home was vacant or unheated and the owner didn’t take reasonable steps such as keeping heat on or draining the system. Read that condition closely if you own a second home, a rental near State College or a property between tenants.</p>
<div class="note"><b class="h">Document before you dry</b>Shut off the water, call a mitigation company and photograph everything before materials are removed: wet ceilings, buckled floors, stained walls and the failed pipe section itself. Keep the broken pipe if you can. Those details often decide later scope arguments.</div>
<h2>Where estimates usually fall short</h2>
<ul>
<li><strong>Hidden moisture.</strong> Water travels farther than it looks. Moisture readings and thermal images help prove how much drywall, insulation and subfloor got wet.</li>
<li><strong>Plaster and lath.</strong> Many older Pennsylvania homes have plaster walls, which cost more to repair than drywall and are often priced as if they were drywall.</li>
<li><strong>Hardwood floors.</strong> Cupping can show weeks after drying. Whether to refinish, replace a section or replace the full run is a frequent dispute.</li>
<li><strong>Roof edge repairs.</strong> After an ice dam, the question may be whether to replace damaged shingles, add ice-and-water shield to meet current code, or replace slopes for a reasonable match.</li>
<li><strong>Access and tear-out.</strong> Opening walls and ceilings to reach a pipe, then closing and finishing them, adds up quickly.</li>
<li><strong>Overhead and profit.</strong> A winter water loss can involve plumbers, mitigation crews, drywall finishers, painters and flooring installers — the kind of multi-trade project where a general contractor is reasonable.</li>
</ul>
<h2>Snow load and roof collapse</h2>
<p>February 2010 showed what heavy, wet snow can do to flat and low-slope roofs, porches and older outbuildings such as bank barns. Collapse claims bring structural engineering, temporary shoring and sometimes code upgrades into the estimate. If you’re worried about a roof before the next storm, our <a href="/claim-calculators/roof-snow-load-estimator/">roof snow load estimator</a> gives a rough sense of the weight involved.</p>
<h2>Working the claim</h2>
<ol>
<li>Report the loss promptly and keep a log of every call and visit.</li>
<li>Get a written scope from a contractor who will walk the whole house, not just the visible stain.</li>
<li>Compare that scope to the insurer’s estimate line by line.</li>
<li>Ask for a supplement with photos and moisture data.</li>
<li>If the gap remains and coverage is accepted, consider appraisal.</li>
</ol>
<p>Keep your deadlines in view. Many Pennsylvania property policies require a lawsuit within one year of the date of loss, and appraisal may not pause that clock unless the policy or a written agreement says so. If you’re close, call an attorney.</p>
<p>Our <a href="/property-appraisal-services/ice-dam-frozen-pipe-appraisal/">ice dam and frozen pipe appraisal</a> service focuses on exactly these winter losses, and our <a href="/property-appraisal-services/insurance-estimate-audit/">insurance estimate audit</a> can show where an existing estimate is thin before you decide on appraisal.</p>
""",
    },
    {
        "slug": "rowhome-flat-roof-claims",
        "title": "Rowhome Flat Roof Claims: Party Walls, Leaks and Scope",
        "seo": "Rowhome Flat Roof Claims: Party Walls and Leaks",
        "desc": "Rowhome flat roof claims raise party-wall, matching and drainage issues. Learn where insurer estimates fall short and how to document damage.",
        "keyword": "rowhome flat roof claims",
        "summary": "Flat roofs and shared walls make rowhome claims unlike any other. Here’s what usually goes wrong in the estimate and how to fix it.",
        "date": "2026-10-22", "read": "7 min",
        "body": """
<p>Rowhomes define the streetscape in Philadelphia, Reading, York and Harrisburg. Most have low-slope roofs covered in modified bitumen, built-up layers or a newer membrane, and they share party walls with the neighbors on one or both sides. When a summer thunderstorm, a nor’easter or a winter freeze damages one of these roofs, the claim brings problems a detached house simply doesn’t have.</p>
<h2>How rowhome roofs fail</h2>
<p>Flat roofs aren’t really flat; they’re pitched gently toward a drain, scupper or gutter at the rear. Damage usually comes from a few sources:</p>
<ul>
<li><strong>Wind.</strong> Gusts lift seams and edges, peel back flashing at parapets and tear membrane at the front cornice.</li>
<li><strong>Hail and falling debris.</strong> Branches, chimney caps and neighbors’ rooftop equipment can puncture the surface.</li>
<li><strong>Ponding and ice.</strong> Clogged drains let water sit; freeze-thaw cycles open cracks and seams.</li>
<li><strong>Fire.</strong> Rooftop fires or fire next door can scorch membrane and damage the deck.</li>
</ul>
<p>Leaks often show up far from the actual opening, because water travels along the deck and joists before dripping through a ceiling. That makes careful inspection more important than on a sloped roof.</p>
<h2>The party wall problem</h2>
<p>On a row of attached homes, the roof membrane often runs continuously across property lines, and flashing laps onto the parapet or the neighbor’s roof. When one section is damaged, the repair may need to tie into adjoining roofs.</p>
<h3>Questions that come up</h3>
<ul>
<li>Does the scope include cutting back and properly tying into the neighbor’s roof, with new flashing at the joint?</li>
<li>Is the parapet or party wall itself damaged, and if so, whose policy responds?</li>
<li>Are there access charges for working across adjacent roofs?</li>
<li>Does interior damage extend into a shared wall cavity?</li>
</ul>
<p>Responsibility for shared structures can involve neighbors, their insurers and sometimes local rules. Those can become legal questions; a Pennsylvania attorney is the right person for them.</p>
<div class="note"><b class="h">Photograph the whole row</b>Take wide shots showing your roof and both neighbors’ roofs, plus close-ups of seams, flashing and drains. Photos that show where your membrane meets theirs help an adjuster or appraiser understand what a proper repair requires.</div>
<h2>Where the estimate usually falls short</h2>
<p>Insurer estimates for rowhome roofs often price a patch when a larger repair is needed. Common gaps include:</p>
<ul>
<li><strong>Patch versus replacement.</strong> Modified bitumen ages and shrinks. A patch on brittle, multi-layer roofing may not hold, and many roofers won’t warranty one.</li>
<li><strong>Tear-off layers.</strong> Older rowhomes may have several layers of roofing. Removing them, and disposing of them, costs more than the estimate assumes.</li>
<li><strong>Deck repair.</strong> Wet or rotted decking under the membrane must be replaced before new roofing goes on.</li>
<li><strong>Code items.</strong> Re-roofing may trigger insulation or edge requirements. Building code upgrade coverage — often called ordinance or law — may pay for some of this, subject to its own limit.</li>
<li><strong>Interior finishes.</strong> Plaster ceilings, crown moulding and older trim in rowhomes cost more to restore than the generic drywall line items often used.</li>
<li><strong>Access.</strong> Narrow streets, no rear alley and limited staging areas add labor and equipment costs, including hoisting and permits for dumpsters.</li>
</ul>
<h2>Measuring and pricing low-slope roofs</h2>
<p>Low-slope roofing is priced by the roof square, like any other roof, but parapet walls, curbs, skylights and drains add flashing and labor that a simple area measurement misses. Make sure the estimate captures the perimeter, every penetration and the transitions to neighbors. Our <a href="/claim-calculators/roof-pitch-squares-estimator/">roof pitch and squares estimator</a> helps sanity-check area figures.</p>
<h2>When appraisal fits</h2>
<p>If the insurer agrees the roof was damaged by a covered peril but the estimate covers only a patch, that is a classic amount-of-loss dispute. Appraisal can resolve the scope and price. If the insurer says the damage is wear and tear, that’s closer to a coverage or causation question, and you may need a Pennsylvania attorney.</p>
<p>Before you decide, gather your contractor’s written scope, photos of the whole roof and interior, the insurer’s estimate and any engineer’s report. Then compare them line by line. Our <a href="/property-appraisal-services/roof-hail-damage-appraisal/">roof and hail damage appraisal</a> service handles low-slope and rowhome roofs, and our <a href="/where-we-work/philadelphia/">Philadelphia</a> page covers the city’s housing in more detail.</p>
<p>As always, keep the suit-limitation date in view. Many Pennsylvania property policies require a lawsuit within one year of the date of loss, and appraisal may not pause that clock.</p>
""",
    },
    {
        "slug": "mine-subsidence-sinkholes-and-your-policy",
        "title": "Mine Subsidence, Sinkholes and Your Pennsylvania Policy",
        "seo": "Mine Subsidence, Sinkholes and Your Policy",
        "desc": "Mine subsidence and sinkholes are usually excluded from home policies. See how Pennsylvania’s MSI program works and when appraisal applies.",
        "keyword": "mine subsidence and sinkholes",
        "summary": "Ground movement is excluded from most homeowner policies. Here’s how mine subsidence insurance and sinkhole limits work in Pennsylvania.",
        "date": "2026-11-05", "read": "8 min",
        "body": """
<p>Pennsylvania’s geology creates two ground-movement risks that many homeowners don’t think about until cracks appear. In the coal regions of the northeast and west, old underground mines can collapse decades after they closed. In the limestone (karst) areas of the Lehigh Valley and the Lancaster, Berks and Cumberland Valley region, water can dissolve bedrock and open sinkholes. Both can crack foundations, tilt floors and split walls — and neither is usually covered by a standard homeowner policy.</p>
<h2>The earth movement exclusion</h2>
<p>Most homeowner policies contain an earth movement exclusion. It typically lists earthquakes, landslides, mudflow, subsidence and sinkholes, along with soil shifting, expansion and settling. Some policies carve out exceptions, such as fire or explosion that follows earth movement. The details vary, so read your own policy’s definitions and any endorsements.</p>
<p>Because of this exclusion, a crack in a foundation may set off a coverage dispute rather than a valuation dispute. That distinction matters for appraisal, which values the amount of a covered loss but doesn’t decide whether a loss is covered.</p>
<div class="note"><b class="h">Coverage first</b>If your insurer denies a claim under the earth movement exclusion, the question is about coverage, not price. Appraisal usually isn’t the right tool for that; talk to a Pennsylvania attorney about the denial.</div>
<h2>Mine Subsidence Insurance (MSI)</h2>
<p>Pennsylvania offers a separate safety net for coal mine collapse. The Mine Subsidence Insurance program, run by the Pennsylvania Department of Environmental Protection, offers coverage for damage caused by the collapse of underground coal mines. It is separate from your homeowner policy and has its own application, terms, limits and claim process.</p>
<h3>Who should look into it</h3>
<p>Owners in areas with a history of underground coal mining — much of the region around Scranton and Wilkes-Barre, parts of the Pittsburgh area and Johnstown, and many smaller towns in between — often find that their property sits above or near old workings. DEP provides information about mined areas and how to apply. Because MSI is a distinct program, check its current terms directly rather than relying on what a neighbor bought years ago.</p>
<h3>Making an MSI claim</h3>
<p>If you see new cracks in foundation walls, doors and windows that suddenly stick, sloping floors or separation between walls and chimneys, document the damage and contact the program promptly. Claims typically involve an investigation to determine whether mine subsidence caused the damage. The program’s rules control how disputes are resolved, so read the policy you receive.</p>
<h2>Sinkholes in karst country</h2>
<p>Limestone bedrock runs under a large swath of south-central and southeastern Pennsylvania. As water moves through cracks in the rock, it slowly dissolves it. Heavy rain, broken water or sewer lines, and poorly managed stormwater can speed the process and cause the ground above to drop.</p>
<p>Sinkhole damage is often excluded or limited under homeowner policies. Some insurers sell endorsements; many don’t. Read the policy before the ground moves, not after.</p>
<h3>When water causes the hole</h3>
<p>Sometimes a covered event — a sudden pipe break, for example — contributes to ground collapse. Whether any resulting damage is covered depends on the policy’s wording about water damage, earth movement and how the two interact. That’s a coverage question for a Pennsylvania attorney, not an appraisal panel.</p>
<h2>Where appraisal fits</h2>
<p>Appraisal becomes relevant once coverage is accepted and the disagreement is about the amount of loss. Examples include:</p>
<ul>
<li>An insurer accepts a fire or explosion loss that followed ground movement but undervalues the repair.</li>
<li>A water-related collapse is accepted under a homeowner policy but the scope of foundation and interior work is disputed.</li>
<li>Any policy, including a separate program policy, contains an appraisal provision and the parties disagree only on value.</li>
</ul>
<p>In those cases, foundation repair, underpinning, structural engineering, interior crack repair and finishes all need careful pricing. Structural work is expensive and estimates can differ widely, so detailed engineering reports and contractor bids make a real difference.</p>
<h2>Documenting ground-movement damage</h2>
<ol>
<li>Photograph cracks with a ruler or tape measure for scale, and date each photo.</li>
<li>Mark the ends of cracks with a pencil and recheck them over time to show movement.</li>
<li>Note doors and windows that bind and floors that slope, with simple level readings.</li>
<li>Keep records of water bills, plumbing repairs and any recent excavation nearby.</li>
<li>Consider a structural engineer’s inspection before major repairs.</li>
</ol>
<h2>Deadlines and next steps</h2>
<p>Ground-movement damage can develop slowly, which makes the date of loss harder to pin down. Many Pennsylvania property policies require a lawsuit within one year of the date of loss, and appraisal may not pause that clock unless the policy or a written agreement says so. Read our <a href="/policy-and-claim-guides/one-year-suit-limitation-and-appraisal/">one-year suit limitation</a> guide, and talk to an attorney early.</p>
<p>If coverage has been accepted and the dispute is over value, our <a href="/property-appraisal-services/home-insurance-claim-appraisal/">home insurance claim appraisal</a> service can help. For background on terms like earth movement and recoverable depreciation, see our <a href="/claim-terms-glossary/">claim terms glossary</a>.</p>
""",
    },
]
