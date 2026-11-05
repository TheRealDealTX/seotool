"""Blog hub, category archive and articles. Articles live at the site root
(/slug/) to match the original WordPress permalink structure."""

from components import (BIZ, IMG, ORG_ID, callout, card, checklist, fig, faq_html, faq_schema, grid, icon,
                        related_links, section_head, steps_html, table, url)
from siteconfig import TODAY

AUTHOR = {"@type": "Organization", "@id": ORG_ID, "name": "Alabama Insurance Appraiser"}

POSTS = []


def post(slug, title, h1, desc, img, published, excerpt, body, faqs, related, read_min, modified=None):
    POSTS.append(dict(slug=slug, title=title, h1=h1, desc=desc, img=img, published=published,
                      modified=modified or published, excerpt=excerpt, body=body, faqs=faqs, related=related,
                      read_min=read_min))


# ---------------------------------------------------------------------------
post("what-does-an-insurance-appraiser-do",
     "What Does an Insurance Appraiser Do? Alabama Property Claim Guide",
     "What Does an Insurance Appraiser Do?",
     "What does an insurance appraiser do? How appraisers inspect damage, compare estimates, work with the umpire and settle the amount of loss on Alabama claims.",
     "inspect", "2026-08-11",
     "The appraiser's role on a disputed property claim: what gets inspected, how the amount of loss is decided, how the umpire fits in, and what appraisal can't do.",
     f"""
<p class="lead-p">When an insurance claim turns into a disagreement over repair costs, measurements, materials or the extent of damage, someone eventually mentions appraisal. That leads to the obvious question: <strong>what does an insurance appraiser do?</strong></p>
<p>In one sentence: an insurance appraiser evaluates the amount of a disputed property loss, builds or reviews the estimates, examines the damage and works with the other side's appraiser to arrive at a supported valuation. In practice there is a lot more to it, and knowing what to expect helps you prepare the right documents and ask the right questions.</p>
<h2>What is an insurance appraiser?</h2>
<p>An insurance appraiser is a person chosen to evaluate the <strong>amount of loss</strong> when the policyholder and insurer disagree about the value or scope of a property claim. The appraiser's authority comes from the insurance policy itself. Most property policies contain an appraisal clause that explains when appraisal can be requested, how each side picks an appraiser, how an umpire is chosen and how an award is reached.</p>
<p>An appraiser is not just another adjuster reopening the whole claim. The job is narrower: examine the disputed loss and develop a reasoned position on how much it is worth.</p>
{callout("<p>Alabama courts treat appraisal as a contractual process distinct from arbitration. The Alabama Supreme Court reaffirmed that distinction in <em>Great American Insurance Co. v. Crystal Shores Owners Association</em>, a case involving an appraisal provision covering disagreement over the amount of loss. Your policy's exact wording governs.</p>", "info", "Alabama note")}
<h2>What an insurance appraiser actually does</h2>
<p>The work starts with understanding exactly what is disputed. Suppose the carrier estimates a storm loss at $35,000 and a contractor estimates $62,000. The difference alone explains nothing. Maybe one estimate covers spot repairs and the other full replacement. Maybe quantities differ. Maybe one omits roofing accessories, interior finishes, debris removal or labor. The appraiser's job is to find those differences and evaluate each one.</p>
{checklist(["Reviewing the insurer's estimate and any contractor or policyholder estimates", "Inspecting the damaged property", "Taking or verifying measurements",
            "Reviewing photographs and claim documentation", "Identifying differences in repair scope", "Evaluating materials, quantities, labor and pricing",
            "Preparing an independent estimate", "Negotiating disputed items with the opposing appraiser"], "checklist two-col")}
<h2>When might you need an insurance appraiser?</h2>
<p>Not every claim needs appraisal. If you and the carrier agree on the amount of loss, there's nothing to appraise. Appraisal becomes relevant when a genuine valuation disagreement remains after documentation, re-inspections and supplements have been exchanged. Common disputes involve roof systems, hail and wind damage, water damage, fire repairs, interior reconstruction, siding, windows, commercial property, material quantities, labor pricing and repair-versus-replace decisions.</p>
<h2>How the appraisal process works</h2>
{steps_html([("A disagreement develops", "The policyholder and insurer disagree over the amount of loss."),
             ("The policy is reviewed", "Read the appraisal provision: how to demand appraisal, deadlines, appraiser qualifications, umpire selection and costs."),
             ("Each side selects an appraiser", "Typically one appraiser per side, each evaluating the disputed loss independently."),
             ("The appraisers compare positions", "They work through measurements, methods, quantities and pricing. Every agreed item narrows the dispute."),
             ("An umpire may become involved", "Items the appraisers can't agree on go to the umpire under the policy's procedure."),
             ("An award is reached", "The policy determines how the award is formed and what effect it has.")])}
<p>For more detail, read our full <a href="/insurance-appraisal-process/">insurance appraisal process guide</a> and <a href="/how-to-invoke-the-appraisal-clause-in-alabama/">how to invoke appraisal in Alabama</a>.</p>
<h2>What does an insurance appraiser inspect?</h2>
<p>It depends on the claim. For an exterior storm loss, an appraiser may evaluate roofing materials, measurements, ridge and hip components, flashing, vents, gutters, siding, windows and exterior finishes. For an interior loss, drywall, flooring, cabinetry, trim, paint, insulation, fixtures and ceilings. The inspection is compared with photos from right after the event, prior estimates, contractor proposals, invoices and any engineering reports.</p>
{fig("roof", "Storm water running across damaged roof shingles")}
<h2>How the amount of loss gets decided</h2>
<p>Picture two estimates $40,000 apart. The totals tell you almost nothing. An appraiser compares:</p>
<ul><li><strong>Measurements and quantities</strong> &mdash; roof squares, drywall, linear feet of trim, flashing and gutters.</li>
<li><strong>Materials</strong> &mdash; three-tab vs. architectural shingles, metal, tile, specialty flooring, custom cabinetry.</li>
<li><strong>Labor</strong> &mdash; access, height, demolition, complexity and sequencing.</li>
<li><strong>Repair scope</strong> &mdash; replacement of an assembly vs. partial repair, and the reasoning behind each.</li>
<li><strong>Related work</strong> &mdash; vents, underlayment, drip edge, disposal, insulation and paint that repairs drag along.</li></ul>
<h2>What an insurance appraiser does <em>not</em> do</h2>
<p>An appraiser can't rewrite your policy, guarantee a payment, decide every dispute with your carrier, establish coverage or replace legal advice. If the real fight is whether the policy covers the damage at all, that may fall outside appraisal.</p>
<h2>What an umpire does</h2>
<p>Say your appraiser values a roof loss at $92,000 and the carrier's appraiser at $67,000. That $25,000 may come down to five items. The appraisers agree on measurements, shingle quantity, gutters, interior ceilings and debris removal, and send only the unresolved items to the umpire. Learn more in <a href="/what-is-an-insurance-appraisal-umpire/">what is an insurance appraisal umpire</a>.</p>
<h2>A worked example</h2>
<p>An Alabama homeowner has storm damage. The carrier's estimate is <strong>$31,500</strong>; a restoration contractor's is <strong>$58,750</strong> &mdash; a $27,250 gap. Comparing the estimates shows the contractor replaced the roof where the carrier repaired it, replaced gutters the carrier repaired, and included interior water damage the carrier left out. After supplements, the gap remains. Appraisal is invoked; the appraisers inspect and agree on $49,500, leaving $5,000 of roofing items for the umpire. The point: appraisal is far more detailed than choosing between two totals.</p>
<h2>How to choose an insurance appraiser</h2>
<p>Look for real experience in property damage, construction or restoration, detailed estimating, insurance appraisal and your type of loss. Ask:</p>
<ul><li>How much appraisal experience do you have, and with losses like mine?</li><li>Will you personally inspect the property?</li><li>How do you evaluate differences between estimates?</li>
<li>What documents do you need?</li><li>How are your fees calculated?</li><li>How will you keep me updated?</li></ul>
<p>Be cautious of anyone who promises a specific award before reviewing the claim.</p>
""",
     [("Is an insurance appraiser the same as an adjuster?", "<p>No. An adjuster handles the claim for the carrier (or, in some states, for the policyholder). An appraiser is appointed under the appraisal clause specifically to value a disputed loss.</p>"),
      ("Who pays for the appraiser?", "<p>Under most policies each side pays its own appraiser and the two sides split the umpire's fee. Check your policy.</p>"),
      ("How long does appraisal take?", "<p>It varies with the size of the loss and the number of disputed items. See <a href='/how-long-does-insurance-appraisal-take/'>how long insurance appraisal takes</a>.</p>")],
     ["how-to-invoke-the-appraisal-clause-in-alabama", "what-is-an-insurance-appraisal-umpire", "insurance-appraiser-vs-public-adjuster-vs-attorney"], 11, modified=TODAY)

# ---------------------------------------------------------------------------
post("how-to-invoke-the-appraisal-clause-in-alabama",
     "How to Invoke the Appraisal Clause in Alabama (Step by Step)",
     "How to Invoke the Appraisal Clause in Alabama",
     "How to invoke the appraisal clause on an Alabama property claim: reading the policy, the written demand, deadlines, choosing an appraiser and next steps.",
     "residential", TODAY,
     "Reading the clause, writing the demand, meeting deadlines and choosing your appraiser &mdash; the practical steps for Alabama policyholders.",
     f"""
<p class="lead-p">If you and your insurance company have exchanged estimates, supplements and re-inspections and you're still far apart on the amount of loss, your policy's appraisal clause may give you a way to resolve it. Invoking it correctly matters. Here's how it typically works for Alabama property owners.</p>
{callout("<p>This is general information, not legal advice. Appraisal clauses differ between policies. If coverage is disputed or a lawsuit deadline is near, talk to an Alabama attorney.</p>", "warn", "Read your own policy")}
<h2>Step 1: Confirm the dispute is about value</h2>
<p>Appraisal resolves disagreements over the <em>amount</em> of loss. If the carrier has accepted that a covered loss happened but disputes the cost of repair, appraisal may fit. If the carrier says the damage isn't covered at all, appraisal alone usually won't fix that.</p>
<h2>Step 2: Get the full policy and find the clause</h2>
<p>Request a certified copy of your complete policy with all endorsements. The appraisal provision is usually in the conditions section, often titled "Appraisal." Note:</p>
{checklist(["Who can demand appraisal (either party, or only by mutual agreement)", "Whether the demand must be in writing", "How many days each side has to name an appraiser (often 20)",
            "Required appraiser qualifications (competent, impartial or disinterested)", "How the umpire is selected, including court appointment", "How appraisal and umpire costs are split",
            "How an award is made (often by any two of the three)", "Any time limit for filing suit, which appraisal may not pause"])}
<h2>Step 3: Organize your documentation</h2>
<p>Before sending a demand, assemble estimates, photos, reports, payment letters and correspondence. Our <a href="/tools/appraisal-readiness-checklist/">appraisal readiness checklist</a> lists everything. Running the numbers through the <a href="/tools/claim-gap-calculator/">claim gap calculator</a> helps confirm the dispute is worth appraisal.</p>
<h2>Step 4: Send a written demand</h2>
<p>Send the demand to the carrier in writing, by a method that proves delivery, and keep a copy. A typical demand includes:</p>
<ul><li>Your name, the property address, policy number and claim number</li><li>A statement that you disagree with the carrier's amount of loss</li>
<li>A statement that you are demanding appraisal under the policy's appraisal provision</li><li>The name and contact details of your appraiser (if the policy asks for it at this stage)</li>
<li>A request that the carrier name its appraiser within the time the policy requires</li></ul>
<h2>Step 5: Choose your appraiser carefully</h2>
<p>Many policies require an impartial or disinterested appraiser, so the person you name should not have a financial stake in the claim beyond a reasonable fee. Look for estimating experience with your type of loss, and ask how the fee is calculated. Read <a href="/what-does-an-insurance-appraiser-do/">what does an insurance appraiser do</a> for questions to ask.</p>
<h2>Step 6: The appraisers name an umpire</h2>
<p>Once both appraisers are named, they typically select an umpire. If they can't agree within the time the policy sets, either side can usually ask a court to appoint one.</p>
<h2>Step 7: Inspection, negotiation and award</h2>
<p>The appraisers inspect, exchange estimates and work through differences. Agreed items are set; unresolved items go to the umpire. The award is signed and returned to the carrier, which then applies deductibles, prior payments and policy terms.</p>
{table(["Stage", "What happens", "Typical documents"], [
    ["Demand", "Written notice invoking appraisal", "Demand letter, proof of delivery"],
    ["Appointment", "Each side names an appraiser", "Appointment letters, engagement agreement"],
    ["Umpire", "Appraisers agree on an umpire", "Umpire agreement or court order"],
    ["Evaluation", "Inspection, estimates, negotiation", "Estimates, photos, measurements"],
    ["Award", "Signed by two of three", "Itemized appraisal award"],
])}
""",
     [("Can the insurance company refuse appraisal?", "<p>It depends on the policy. Some clauses let either party demand appraisal; others require both parties to agree. Carriers sometimes object that the dispute is about coverage rather than value.</p>"),
      ("Do I need a lawyer to invoke appraisal?", "<p>Not necessarily, but a lawyer is wise if coverage is disputed, deadlines are close or the carrier resists the demand.</p>"),
      ("What if I miss the deadline to name an appraiser?", "<p>Consequences vary by policy and circumstance. Name your appraiser promptly and keep proof of every communication.</p>")],
     ["what-does-an-insurance-appraiser-do", "what-is-an-insurance-appraisal-umpire", "how-long-does-insurance-appraisal-take"], 8)

# ---------------------------------------------------------------------------
post("insurance-appraiser-vs-public-adjuster-vs-attorney",
     "Insurance Appraiser vs. Public Adjuster vs. Attorney in Alabama",
     "Insurance Appraiser vs. Public Adjuster vs. Attorney",
     "Who does what on a disputed Alabama property claim? Compare insurance appraisers, public adjusters and attorneys, and learn which one fits your situation.",
     "inspect", TODAY,
     "Three very different roles on a disputed claim. Here's what each does, how each is paid and when each makes sense in Alabama.",
     f"""
<p class="lead-p">When a property claim goes sideways, policyholders hear three titles thrown around: appraiser, public adjuster and attorney. They do different jobs, and in Alabama the rules for at least one of them are different from most states.</p>
<h2>The quick comparison</h2>
{table(["", "Insurance appraiser", "Public adjuster", "Attorney"], [
    ["Main job", "Value the disputed amount of loss under the appraisal clause", "Prepare and negotiate the claim for the policyholder", "Legal advice, coverage disputes, bad-faith claims and litigation"],
    ["When involved", "After a valuation disagreement, when appraisal is invoked", "Throughout the claim", "When legal rights or coverage are in dispute"],
    ["Handles coverage disputes?", "Generally no", "Limited", "Yes"],
    ["Typical fee", "Agreed fee, often hourly or flat; sometimes a percentage", "Usually a percentage of the claim", "Hourly or contingency"],
    ["Alabama note", "Appointed under the policy's terms", "Alabama does not license public adjusters the way most states do; check with ALDOI", "Licensed by the Alabama State Bar"],
])}
<h2>What an insurance appraiser does</h2>
<p>An appraiser is appointed under the policy's appraisal clause to decide one thing: the amount of loss. The appraiser inspects, measures, estimates and negotiates item by item with the other side's appraiser, with an umpire breaking ties. Appraisers generally don't argue coverage. See <a href="/what-does-an-insurance-appraiser-do/">what does an insurance appraiser do</a>.</p>
<h2>Public adjusters in Alabama</h2>
<p>In most states, licensed public adjusters represent policyholders in presenting and negotiating claims for a percentage fee. Alabama is different: it does not license public adjusters the way most states do, and negotiating someone else's insurance claim for a fee can raise legal issues. If anyone offers to negotiate your Alabama claim for a percentage, check with the <a href="https://www.aldoi.gov/" rel="noopener" target="_blank">Alabama Department of Insurance</a> first.</p>
<h2>When you need an attorney</h2>
<ul><li>The carrier has denied coverage, in whole or in part</li><li>You suspect bad faith or unreasonable delay</li><li>A suit-limitation deadline is approaching</li>
<li>The carrier refuses to participate in appraisal</li><li>There are disputes about the appraisal award itself</li></ul>
<h2>Which one do you need?</h2>
{grid([card("Value is the issue", "The carrier accepts the loss but pays too little. Consider an estimate review, then appraisal.", "/services/property-insurance-appraisal/", "scale"),
       card("Coverage is the issue", "The carrier says the damage isn't covered. Talk to an attorney.", None, "shield"),
       card("Both are issues", "Counsel handles coverage; an appraiser documents and values the loss.", "/contact/", "users")], 3)}
""",
     [("Can an appraiser and an attorney work together?", "<p>Yes. Attorneys often retain appraisers to value the loss while they handle coverage and legal issues.</p>"),
      ("Can a contractor act as my appraiser?", "<p>If your policy requires an impartial or disinterested appraiser, a contractor who stands to do the repair work may not qualify.</p>"),
      ("Who regulates insurance in Alabama?", "<p>The Alabama Department of Insurance (ALDOI) regulates insurers and licensed insurance professionals and accepts consumer complaints.</p>")],
     ["what-does-an-insurance-appraiser-do", "how-to-invoke-the-appraisal-clause-in-alabama", "what-is-an-insurance-appraisal-umpire"], 6)

# ---------------------------------------------------------------------------
post("what-is-an-insurance-appraisal-umpire",
     "What Is an Insurance Appraisal Umpire? Role, Selection &amp; Fees",
     "What Is an Insurance Appraisal Umpire?",
     "What an insurance appraisal umpire does, how umpires are selected in Alabama, how umpire fees are split and how to prepare items for umpire review.",
     "commercial", TODAY,
     "The umpire breaks ties between the two appraisers. Here's how umpires are chosen, what they decide and how to present items to them.",
     f"""
<p class="lead-p">Most appraisal clauses build in a tiebreaker: the umpire. When the two appraisers can't agree on part of the loss, the umpire decides between them. Understanding the umpire's role helps you see why item-by-item documentation matters so much.</p>
<h2>What does an umpire do?</h2>
<p>The umpire reviews only the items the appraisers couldn't resolve. The umpire considers each side's position and evidence, may inspect the property, and joins with one appraiser (or decides independently, depending on the policy) to form the award. Under many clauses, an award signed by any two of the three is binding as to the amount of loss.</p>
<h2>How umpires are selected</h2>
{steps_html([("Appraisers confer", "After both appraisers are named, they try to agree on a competent, impartial umpire."),
             ("Time limit", "Many policies give them a set period, often 15 days, to agree."),
             ("Court appointment", "If they can't agree, either party can usually ask a court in the county where the property is located to appoint one.")])}
<h2>Who makes a good umpire?</h2>
<p>Good umpires are experienced in construction, estimating and the appraisal process, have no stake in the claim and are trusted by both sides. Many are former contractors, adjusters, engineers or appraisers.</p>
<h2>Umpire fees</h2>
<p>Most appraisal clauses split the umpire's fee equally between the policyholder and the insurer. Fees are usually hourly or a set fee agreed in advance.</p>
<h2>Presenting items to the umpire</h2>
{checklist(["Narrow the dispute: agree on everything you reasonably can first", "Present each disputed item separately with its quantity, unit price and reasoning",
            "Support each item with photos, measurements, manufacturer specs or code references", "Explain the repair method and why the other position falls short",
            "Keep it organized; a matrix of disputed items helps everyone"])}
{fig("commercial", "Commercial building where an umpire may inspect disputed items")}
""",
     [("Can the umpire decide coverage?", "<p>Generally no. Like the appraisers, the umpire decides the amount of loss, not whether the policy covers it.</p>"),
      ("Does the umpire have to inspect the property?", "<p>Not always. Many umpires inspect when the disputed items require it; others decide on the documentation.</p>"),
      ("Can an umpire's award be challenged?", "<p>Courts can set aside awards in limited circumstances, such as fraud, partiality or decisions outside the appraisers' authority. Talk to an attorney if you have concerns.</p>")],
     ["what-does-an-insurance-appraiser-do", "how-to-invoke-the-appraisal-clause-in-alabama", "how-long-does-insurance-appraisal-take"], 5)

# ---------------------------------------------------------------------------
post("how-long-does-insurance-appraisal-take",
     "How Long Does Insurance Appraisal Take in Alabama?",
     "How Long Does Insurance Appraisal Take?",
     "How long insurance appraisal takes on an Alabama property claim, what affects the timeline, and how to keep appraisal moving from demand to award.",
     "storm", TODAY,
     "A realistic look at appraisal timelines &mdash; and the factors you can control to keep things moving.",
     f"""
<p class="lead-p">There's no universal timeline for appraisal. A well-documented residential roof dispute can wrap up in weeks; a multi-building commercial loss can take months. What you can control is how prepared you are and how quickly the early steps happen.</p>
<h2>A typical timeline</h2>
{table(["Stage", "Typical timing*", "What drives it"], [
    ["Written demand to appraisers named", "Often about 20 days", "Policy deadlines"],
    ["Umpire selection", "Often about 15 days, longer if a court must appoint", "Appraisers' cooperation"],
    ["Inspection and estimates", "1&ndash;6 weeks", "Scheduling, size of loss, documentation"],
    ["Negotiation between appraisers", "1&ndash;8 weeks", "Number and complexity of disputed items"],
    ["Umpire review (if needed)", "2&ndash;8 weeks", "Umpire's availability, inspection needs"],
    ["Award and payment", "Policy-dependent", "Carrier's payment terms after award"],
])}
<p class="muted">*General planning ranges only; your policy and the facts control.</p>
<h2>What slows appraisal down</h2>
<ul><li>Missing or disorganized documentation</li><li>Delays in naming appraisers or agreeing on an umpire</li><li>Access problems at the property</li>
<li>Large numbers of disputed line items</li><li>Disputes about whether an issue is coverage or value</li></ul>
<h2>How to keep it moving</h2>
{checklist(["Have the full policy and all estimates before sending the demand", "Name your appraiser in the demand when the policy allows",
            "Use our <a href='/tools/appraisal-readiness-checklist/'>readiness checklist</a> to organize records", "Keep a log of every deadline and communication",
            "Respond quickly to scheduling requests"])}
""",
     [("Does appraisal stop the suit-limitation clock?", "<p>Not necessarily. Many policies have a deadline for filing suit that appraisal may not pause. Calendar it and ask an attorney if it's close.</p>"),
      ("Is appraisal faster than a lawsuit?", "<p>Usually, yes. That's one of its main advantages for pure valuation disputes.</p>"),
      ("When is payment made after the award?", "<p>Payment timing depends on the policy terms and the carrier. Many policies set a deadline for payment after an award is filed.</p>")],
     ["how-to-invoke-the-appraisal-clause-in-alabama", "what-is-an-insurance-appraisal-umpire", "what-does-an-insurance-appraiser-do"], 4)

# ---------------------------------------------------------------------------
post("hail-damage-roof-insurance-claims-alabama",
     "Hail Damage Roof Insurance Claims in Alabama: A Homeowner Guide",
     "Hail Damage Roof Insurance Claims in Alabama",
     "Hail damage roof claims in Alabama: spotting and documenting damage, repair vs. replacement and matching disputes, and what to do when the estimate is low.",
     "roof", TODAY,
     "From spotting hail damage to fighting a low roof estimate &mdash; what Alabama homeowners should know.",
     f"""
<p class="lead-p">Hail is one of the most common causes of roof claims in Alabama, especially across the Tennessee Valley and the Birmingham metro. Here's how to handle a hail claim from the first storm to a fair settlement.</p>
<h2>Signs of hail damage</h2>
{checklist(["Dents in gutters, downspouts, vents and flashing", "Dark spots on shingles where granules were knocked off", "Cracked or split shingles",
            "Damaged window screens, siding and HVAC fins", "Granules collecting at downspout outlets"], "checklist two-col")}
<h2>Document it right away</h2>
<p>Photograph soft metals and the roof (from the ground or a ladder only if safe), note the date and time of the storm, and save weather reports for your address. Report the claim promptly &mdash; delay makes it harder to tie damage to a specific storm.</p>
<h2>Common hail-claim disputes</h2>
<h3>Repair vs. replacement</h3>
<p>Carriers often approve a few shingles. But older or brittle shingles may crack when lifted, and discontinued products can make a repair impossible to match.</p>
<h3>Matching</h3>
<p>If new shingles won't reasonably match the old, whether more of the roof should be replaced depends on the policy and the facts.</p>
<h3>Missing items</h3>
<p>Starter strip, drip edge, ridge cap, ice-and-water shield, vents, pipe jacks, steep and high charges, and a realistic waste factor are often missing. Check your roof size with our <a href="/tools/roof-square-calculator/">roof square calculator</a>.</p>
{fig("roof", "Close-up of storm-damaged shingles after a hail event")}
<h2>If the estimate is too low</h2>
{steps_html([("Request the full estimate", "Get the line-item estimate, not just the summary."),
             ("Compare with a contractor estimate", "Look for missing items, quantities and pricing differences."),
             ("Submit a supplement", "Send photos and documentation for missing items."),
             ("Consider appraisal", "If a large, supported gap remains, appraisal may resolve it.")])}
<p>Learn more on our <a href="/services/hail-damage-appraisal/">hail damage appraisal</a> page.</p>
""",
     [("Can I get a new roof if only some shingles are damaged?", "<p>It depends on repairability, matching and your policy. These are common appraisal issues.</p>"),
      ("Will my roof's age affect the payment?", "<p>Yes. Depreciation is based on age and condition, and some policies settle roofs at actual cash value. Try our <a href='/tools/depreciation-calculator/'>depreciation calculator</a>.</p>"),
      ("What about cosmetic damage on metal roofs?", "<p>Some policies exclude cosmetic hail damage on metal roofing. Read the endorsement carefully.</p>")],
     ["alabama-hurricane-deductibles-explained", "what-does-an-insurance-appraiser-do", "how-to-invoke-the-appraisal-clause-in-alabama"], 5)

# ---------------------------------------------------------------------------
post("alabama-hurricane-deductibles-explained",
     "Alabama Hurricane Deductibles Explained (With Examples)",
     "Alabama Hurricane Deductibles Explained",
     "How hurricane and named-storm deductibles work in Alabama, how to calculate yours in dollars, when they apply and how FORTIFIED roofs can help coastal homeowners.",
     "flood", TODAY,
     "Percentage deductibles can mean thousands out of pocket. Here's how they work and how to calculate yours.",
     f"""
<p class="lead-p">If you live near the Alabama coast &mdash; or even well inland &mdash; your policy may have a separate hurricane or named-storm deductible. Unlike a flat $1,000 deductible, it's a percentage of your dwelling coverage, and it can be the biggest number on your claim.</p>
<h2>How percentage deductibles work</h2>
<p>The deductible is calculated on Coverage A (dwelling), not on the amount of damage.</p>
{table(["Coverage A", "1%", "2%", "5%"], [
    ["$200,000", "$2,000", "$4,000", "$10,000"],
    ["$350,000", "$3,500", "$7,000", "$17,500"],
    ["$500,000", "$5,000", "$10,000", "$25,000"],
])}
<p>Calculate yours with our <a href="/tools/hurricane-deductible-calculator/">hurricane deductible calculator</a>.</p>
<h2>When does it apply?</h2>
<p>That depends on how the policy defines the triggering event. Some trigger when the National Hurricane Center names a storm; others when a hurricane watch or warning is issued for any part of the state; some apply to all wind and hail. Read the definition in your policy.</p>
<h2>Coastal wind coverage</h2>
<p>Some properties in Mobile and Baldwin counties get wind coverage through the Alabama Insurance Underwriting Association (AIUA), the state's coastal wind pool, with other perils covered by a separate homeowner policy. Two policies can mean two deductibles and two claims.</p>
<h2>FORTIFIED roofs</h2>
<p>Alabama law requires insurers to offer premium discounts for homes built or retrofitted to IBHS FORTIFIED standards, and the Strengthen Alabama Homes program has offered grants toward FORTIFIED roofs. If you have a FORTIFIED roof, make sure repairs maintain the designation.</p>
{callout("<p>Appraisal can resolve the amount of loss, but it doesn't change the deductible. Knowing your deductible helps you judge whether a disputed gap is worth pursuing.</p>", "tip", "Appraisal and deductibles")}
""",
     [("Is flood covered by my hurricane deductible?", "<p>No. Flood is excluded from standard homeowner policies and handled under a separate flood policy with its own deductible.</p>"),
      ("Can I choose a lower hurricane deductible?", "<p>Sometimes, for a higher premium. Ask your agent about options.</p>"),
      ("Does the hurricane deductible apply inland?", "<p>It can. The policy's trigger definition decides, not your distance from the coast.</p>")],
     ["hail-damage-roof-insurance-claims-alabama", "how-to-invoke-the-appraisal-clause-in-alabama", "what-does-an-insurance-appraiser-do"], 5)


POST_BY = {p["slug"]: p for p in POSTS}


def post_card(p):
    f, w, h = IMG[p["img"]]
    small = f.replace(".webp", "-720.webp")
    return (f'<a class="card post-card spot tilt reveal" href="/{p["slug"]}/"><div class="post-img">'
            f'<img src="/assets/img/{small}" width="720" height="{round(720 * h / w)}" alt="{p["h1"]}" loading="lazy"></div>'
            f'<div class="post-body"><span class="post-meta">{p["read_min"]} min read</span><h3>{p["h1"]}</h3>'
            f'<p>{p["excerpt"]}</p><span class="card-link">Read article {icon("arrow", "ico ico-sm")}</span></div></a>')


def article_page(p):
    path = f"/{p['slug']}/"
    from datetime import date
    pub = date.fromisoformat(p["published"]).strftime("%B %-d, %Y")
    pg = {
        "path": path, "title": p["title"], "description": p["desc"], "h1": p["h1"], "lead": p["excerpt"],
        "kicker": "Guide", "hero_img": p["img"], "nav_active": "/blog/", "is_post": True,
        "published": p["published"], "modified": p["modified"],
        "crumbs": [("Home", "/"), ("Blog", "/blog/"), (p["h1"], path)],
        "hero_meta": f'<div class="hero-meta"><span>{icon("clock", "ico ico-xs")} {p["read_min"]} min read</span><span>Published {pub}</span><span>By Alabama Insurance Appraiser</span></div>',
        "hero_actions": "", "sidebar_title": "More guides",
        "sidebar_links": [(q["h1"], f"/{q['slug']}/") for q in POSTS if q["slug"] != p["slug"]][:6],
        "schema_type": "WebPage", "priority": "0.7",
    }
    rel = related_links("Keep reading", [(POST_BY[s]["h1"], f"/{s}/") for s in p["related"]])
    pg["body"] = p["body"] + f'<h2>Frequently asked questions</h2>{faq_html(p["faqs"])}' + rel
    f, w, h = IMG[p["img"]]
    pg["schema"] = [{
        "@type": "BlogPosting", "@id": url(path) + "#article", "headline": p["h1"], "description": p["desc"],
        "datePublished": p["published"], "dateModified": p["modified"], "author": AUTHOR, "publisher": {"@id": ORG_ID},
        "mainEntityOfPage": {"@id": url(path) + "#webpage"}, "inLanguage": "en-US",
        "image": {"@type": "ImageObject", "url": url("/assets/img/" + f), "width": w, "height": h},
        "articleSection": "General", "isPartOf": {"@id": url("/blog/#blog")},
    }, faq_schema(pg, p["faqs"])]
    return pg


def listing(path, title, desc, h1, lead, crumbs, schema_type):
    pg = {
        "path": path, "title": title, "description": desc, "h1": h1, "lead": lead, "kicker": "Tips &amp; resources",
        "hero_img": "inspect", "nav_active": "/blog/", "crumbs": crumbs, "layout": "wide", "hero_actions": "",
        "schema_type": schema_type, "priority": "0.7" if path != "/blog/" else "0.8", "changefreq": "weekly",
    }
    cards = [post_card(p) for p in POSTS]
    pg["body"] = f'''<section class="section section-white"><div class="container">
  {grid(cards, 3)}
</div></section>
<section class="section section-aqua"><div class="container">
  {section_head("More resources", "Go deeper", "", True)}
  {grid([card("Appraisal process", "How Alabama insurance appraisal works, step by step.", "/insurance-appraisal-process/", "list"),
         card("FAQ", "Answers to common appraisal questions.", "/faq/", "help"),
         card("Claim glossary", "Plain-English insurance claim terms.", "/glossary/", "book"),
         card("Free tools", "Calculators and checklists for your claim.", "/tools/", "calculator")], 4)}
</div></section>'''
    return pg


def pages():
    blog = listing("/blog/", "Insurance Appraisal Blog &amp; Guides | Alabama Insurance Appraiser",
                   "Guides for Alabama property owners on insurance appraisal, umpires, hail and hurricane claims, deductibles and choosing the right help for a disputed claim.",
                   "Insurance Appraisal Blog &amp; Guides", "Practical, plain-English guides for Alabama property owners dealing with a disputed insurance claim.",
                   [("Home", "/"), ("Blog", "/blog/")], "CollectionPage")
    blog["schema"] = [{"@type": "Blog", "@id": url("/blog/#blog"), "name": "Alabama Insurance Appraiser Blog", "url": url("/blog/"),
                       "publisher": {"@id": ORG_ID},
                       "blogPost": [{"@type": "BlogPosting", "@id": url(f"/{p['slug']}/#article"), "headline": p["h1"],
                                     "url": url(f"/{p['slug']}/"), "datePublished": p["published"]} for p in POSTS]}]
    cat = listing("/category/general/", "General Insurance Appraisal Articles | Alabama Insurance Appraiser",
                  "All general articles from Alabama Insurance Appraiser on property insurance appraisal, claim disputes, umpires and deductibles in Alabama.",
                  "General Articles", "Every guide in our General category.",
                  [("Home", "/"), ("Blog", "/blog/"), ("General", "/category/general/")], "CollectionPage")
    cat["priority"] = "0.4"
    return [blog, cat] + [article_page(p) for p in POSTS]
