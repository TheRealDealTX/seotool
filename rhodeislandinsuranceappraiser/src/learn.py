"""Process guide, grouped FAQ, glossary and guide articles."""

PROCESS_STEPS = [
    ("Spot the disagreement", "Coverage is accepted, but your estimate and the carrier’s are far apart. Appraisal only fits a dispute about the amount of loss."),
    ("Send the written demand", "Either side demands appraisal in writing, following the policy’s appraisal paragraph."),
    ("Each side names an appraiser", "You and the insurer each choose a competent, disinterested appraiser, usually within a set number of days."),
    ("The appraisers choose an umpire", "If they can’t agree on one, many policies let either side ask a court to appoint one."),
    ("The appraisers compare estimates", "They inspect, exchange estimates and work through the differences line by line."),
    ("The umpire resolves what’s left", "Items the appraisers can’t agree on go to the umpire, who reviews both positions."),
    ("The award is signed", "When any two of the three sign, the award sets the amount of loss and payment follows under the policy."),
]

PROCESS_BODY = """
<p>Appraisal is a way to settle a disagreement about the <em>amount</em> of a covered property loss without going to court. Rhode Island law prescribes a standard fire insurance policy form, and its appraisal provision, together with similar wording in most homeowner and commercial policies, is what this guide describes. Your policy’s exact wording always controls.</p>
<h2>Before you start: is this an appraisal dispute?</h2>
<p>Appraisal works when the insurer agrees the loss is covered, at least in part, and the disagreement is about scope, pricing, repair method or value. It doesn’t decide whether a loss is covered, whether an exclusion applies or whether the insurer acted in bad faith. If your claim was denied, talk to a Rhode Island attorney first.</p>
<h2>The seven stages</h2>
<h3>1. Spot the disagreement</h3>
<p>Compare the carrier’s itemized estimate with your own. Our <a href="/policyholder-tools/settlement-gap-estimator/">settlement gap estimator</a> shows whether the difference is large enough to justify appraisal costs.</p>
<h3>2. Send the written demand</h3>
<p>The demand should identify the policy and claim, state that the parties disagree on the amount of loss and invoke the appraisal provision. Keep proof of when it was sent.</p>
<h3>3. Each side names an appraiser</h3>
<p>Policies typically give each side a set number of days, often 20, to name a competent and disinterested appraiser. “Disinterested” means the appraiser shouldn’t have a stake in the outcome beyond a normal fee.</p>
<h3>4. The appraisers choose an umpire</h3>
<p>The two appraisers try to agree on a neutral umpire. If they can’t within the time the policy allows, many policies let either party ask a court to appoint one.</p>
<h3>5. The appraisers compare estimates</h3>
<p>Each appraiser inspects and prepares a valuation. They then compare line by line. Most of the movement in appraisal happens here, and many files are resolved without the umpire.</p>
<h3>6. The umpire resolves what’s left</h3>
<p>Items still in dispute go to the umpire, who may inspect, ask for support and hear from both appraisers.</p>
<h3>7. The award is signed</h3>
<p>An award signed by any two of the three sets the amount of loss. The insurer then pays under the policy’s terms, after deductibles and any prior payments, and subject to coverage and limits.</p>
<h2>Costs</h2>
<p>Under most policies, each side pays its own appraiser and the umpire’s fee is split equally. Ask for any appraiser’s fee arrangement in writing.</p>
<h2>How long it takes</h2>
<p>Simple residential appraisals can finish in a few weeks once both appraisers are named. Large or complex claims can take months. Delays usually come from incomplete documentation, so prepare the file before you invoke.</p>
<h2>Where Rhode Island claims add complexity</h2>
<ul>
<li><strong>Hurricane deductibles.</strong> A percentage deductible can change the payment more than any single line item.</li>
<li><strong>Wind versus flood.</strong> Homeowner policies exclude flood, so coastal losses often involve two policies and two processes.</li>
<li><strong>Older homes.</strong> Plaster, slate, cedar and historic district requirements raise repair costs.</li>
</ul>
<p>Rhode Island also has a statute allowing policyholders to sue an insurer for bad-faith refusal to pay or settle a claim. That is a legal claim, separate from appraisal; an attorney can tell you whether it is relevant.</p>"""

FAQ = [
    ("The basics", [
        ("What is insurance appraisal?", "A process written into most property policies for settling disagreements about the amount of a covered loss. Each side names an appraiser, the appraisers choose an umpire, and any two of the three can sign a binding award on the amount."),
        ("What does a Rhode Island insurance appraiser do?", "As your appointed appraiser, we inspect, build an independent line-item valuation, work through the differences with the carrier’s appraiser and, if needed, present unresolved items to the umpire."),
        ("Is appraisal the same as mediation?", "No. Mediation is voluntary and non-binding unless you sign a settlement. An appraisal award on the amount of loss is generally binding."),
        ("Is appraisal the same as arbitration?", "They’re similar, but appraisal is narrower. It decides the amount of loss, not legal questions like coverage."),
    ]),
    ("When appraisal fits", [
        ("When should I consider appraisal?", "When coverage is accepted, you have the carrier’s itemized estimate and a credible estimate of your own, and the gap between them is meaningful."),
        ("When is appraisal the wrong tool?", "When the claim was denied, when the dispute is about coverage or causation, when the gap is too small to justify fees, or when a deadline is close and you need legal advice."),
        ("Can the insurer demand appraisal?", "Yes. Most policies let either side invoke it."),
        ("Can appraisal handle wind versus flood questions?", "Appraisal under your homeowner policy values the covered loss. Whether damage was caused by wind or flood is usually a causation and coverage question outside appraisal."),
    ]),
    ("Costs & timing", [
        ("What does appraisal cost?", "Each side pays its own appraiser, and the umpire’s fee is usually split. Fee arrangements vary; ask for one in writing."),
        ("How long does appraisal take?", "A few weeks for a straightforward residential claim once appraisers are named. Complex or commercial claims can take several months."),
        ("Is your first conversation free?", "Yes. We’ll tell you honestly whether appraisal is likely to help."),
    ]),
    ("Rhode Island specifics", [
        ("Who regulates insurance in Rhode Island?", "The Rhode Island Department of Business Regulation, through its Insurance Division. It handles consumer complaints and licenses insurers, agents and adjusters."),
        ("What is the Rhode Island FAIR Plan?", "A property insurer of last resort for owners who can’t find coverage in the regular market, often near the coast. FAIR Plan policies have their own terms, including how disputes over the amount of loss are handled."),
        ("Do Rhode Island policies have hurricane deductibles?", "Many do. They’re usually a percentage of dwelling coverage and apply when the storm meets the policy’s trigger. Check your declarations page."),
        ("Does Rhode Island have a bad-faith law?", "Yes. Rhode Island has a statute allowing an insured to bring a claim against an insurer for bad-faith refusal to pay or settle. Whether it applies is a legal question for a Rhode Island attorney; appraisal doesn’t decide it."),
        ("Do you serve the whole state?", "Yes, all 39 cities and towns across Rhode Island’s five counties, including Block Island by arrangement."),
    ]),
    ("Working with us", [
        ("Are you a public adjuster or a law firm?", "Neither. We provide appraisal, estimating and umpire services. We don’t give legal advice or negotiate claims outside the appraisal process."),
        ("Can you guarantee a result?", "No. No honest appraiser can. We can promise a thorough, documented valuation."),
        ("What should I send first?", "Your declarations page and policy, the carrier’s full estimate, any contractor estimate, photos and the carrier’s letters."),
    ]),
]

GLOSSARY = [
    ("Actual cash value (ACV)", "Replacement cost minus depreciation. Many policies pay ACV first and the rest after repairs."),
    ("Additional living expense (ALE)", "Coverage for extra costs of living elsewhere while your home is uninhabitable after a covered loss."),
    ("Amount of loss", "The dollar value of a covered loss. It’s what appraisal decides."),
    ("Appraisal award", "The written decision signed by two of the three panel members that sets the amount of loss."),
    ("Appraisal provision", "The policy condition that lets either side demand appraisal when they disagree on the amount of loss."),
    ("Appraiser", "A competent, disinterested person named by each side to value the loss."),
    ("Causation", "What caused the damage, such as wind versus flood. Usually a coverage question, not an appraisal question."),
    ("Coinsurance", "A commercial policy condition that can reduce payment if the property is insured below a required percentage of its value."),
    ("Coverage A", "Dwelling coverage: the limit for the house itself on a homeowner policy."),
    ("Coverage B", "Other structures coverage: detached garages, sheds, fences and similar."),
    ("Declarations page", "The summary page of your policy listing coverages, limits and deductibles."),
    ("Depreciation", "A reduction in value for age and condition, used to calculate actual cash value."),
    ("Disinterested", "Without a personal stake in the outcome. Policies require appraisers to be disinterested."),
    ("Dwelling form", "A policy form often used for rental properties, which can differ from a standard homeowner form."),
    ("Endorsement", "A form attached to the policy that adds, removes or changes coverage."),
    ("FAIR Plan", "A state-established insurer of last resort. Rhode Island’s FAIR Plan covers properties that can’t get coverage elsewhere."),
    ("Flood exclusion", "The homeowner policy provision excluding damage from flood and surface water, including storm surge."),
    ("Hurricane deductible", "A deductible, usually a percentage of Coverage A, that applies when a storm meets the policy’s hurricane trigger."),
    ("Ice dam", "A ridge of ice at the eaves that traps meltwater, which can back up under shingles and leak inside."),
    ("Line item", "A single entry on an estimate with a description, quantity, unit and price."),
    ("Loss of rents", "Coverage for rental income lost while a rented unit can’t be lived in after a covered loss."),
    ("Matching", "Whether replacement materials can reasonably match the undamaged remainder of siding, roofing or flooring."),
    ("Mitigation", "Reasonable steps to prevent further damage after a loss, such as tarping or drying."),
    ("Named storm", "A tropical storm or hurricane named by the National Hurricane Center, a common hurricane-deductible trigger."),
    ("NFIP", "The National Flood Insurance Program, which writes most residential flood policies in the U.S."),
    ("Nor’easter", "A coastal storm with strong northeast winds, common in Rhode Island from fall through spring."),
    ("Ordinance or law coverage", "Coverage for added costs of meeting current building codes during repairs."),
    ("Overhead and profit (O&P)", "A general contractor’s charges for managing a job with several trades, often 10% and 10%."),
    ("Proof of loss", "A sworn statement of the amount claimed, often due within a set time after the insurer requests it."),
    ("Recoverable depreciation", "Held-back depreciation the policy pays once repairs or replacement are completed."),
    ("Replacement cost value (RCV)", "The cost to repair or replace with materials of like kind and quality, without deducting depreciation."),
    ("Scope", "The full list of repairs needed, before pricing."),
    ("Square", "A roofing measurement equal to 100 square feet of roof surface."),
    ("Steep charge", "An estimate line adding labor for working on steep roofs."),
    ("Storm surge", "Seawater pushed ashore by a storm. Treated as flood under homeowner policies."),
    ("Suit limitation", "The policy condition limiting how long you have to sue the insurer, often counted from the date of loss."),
    ("Supplement", "A request to add missing or underpriced items to a claim after the first estimate."),
    ("Umpire", "The neutral third member of an appraisal panel who decides items the appraisers can’t agree on."),
    ("Wind-driven rain", "Rain forced through openings by wind. Coverage depends on whether wind first created an opening."),
    ("Xactimate", "Estimating software widely used by insurers and contractors to price property repairs."),
]

POSTS = [
    {
        "slug": "rhode-island-appraisal-provision-explained", "date": "2026-11-02", "read": "7 min",
        "title": "The Rhode Island Appraisal Provision, Explained",
        "seo": "The Rhode Island Appraisal Provision, Explained",
        "summary": "What the appraisal paragraph in a Rhode Island property policy says, what it can decide and the steps that matter most.",
        "desc": "A plain guide to the appraisal provision in Rhode Island property policies: who can invoke it, what it decides and the steps and costs involved.",
        "body": """
<p>Most homeowners never read the appraisal paragraph in their policy until they need it. In Rhode Island, the standard fire policy form set out in state law includes an appraisal provision, and most homeowner and commercial policies carry similar wording. Here is what it usually says and what it means in practice.</p>
<h2>The core of the provision</h2>
<p>If you and the insurer fail to agree on the amount of loss, either side can make a written demand for appraisal. Each side then selects a competent and disinterested appraiser, usually within 20 days. The two appraisers select an umpire. If they can’t agree within a set time, either side can usually ask a court to select one. The appraisers then set the amount of loss, and any disagreement goes to the umpire. A written award agreed by any two sets the amount of loss.</p>
<h2>What it doesn’t do</h2>
<p>Appraisal is about value. It doesn’t decide whether a loss is covered, and the insurer usually keeps its right to deny coverage even after an award. If coverage is disputed, that’s a matter for the insurer, the Rhode Island Department of Business Regulation’s complaint process or an attorney.</p>
<h2>Three things to check in your policy</h2>
<ul>
<li><strong>Time limits</strong> for naming your appraiser after a demand</li>
<li><strong>Cost sharing</strong> for the umpire and appraisal expenses</li>
<li><strong>Any added conditions</strong>, such as requirements to submit a proof of loss first</li>
</ul>
<h2>Practical advice</h2>
<p>Don’t invoke appraisal until you have the carrier’s itemized estimate, an itemized estimate of your own and good photos. The award is hard to undo, so the file should be ready before the process starts. Our <a href="/policyholder-tools/appraisal-readiness-checkup/">readiness checkup</a> walks through the essentials.</p>""",
    },
    {
        "slug": "hurricane-deductibles-in-rhode-island", "date": "2026-10-21", "read": "6 min",
        "title": "Hurricane Deductibles in Rhode Island: How the Math Works",
        "seo": "Hurricane Deductibles in Rhode Island: The Math",
        "summary": "Why a 2% deductible can mean $10,000 or more, what usually triggers it and why the full wind scope matters even more.",
        "desc": "How hurricane deductibles work on Rhode Island policies: percentage math, common triggers and why a complete wind estimate matters even more.",
        "body": """
<p>If you own a home near Rhode Island’s coast, and often even if you don’t, your policy probably has a hurricane or named-storm deductible. It’s one of the most misunderstood parts of a property claim.</p>
<h2>A percentage of coverage, not of the loss</h2>
<p>A hurricane deductible is typically 1% to 5% of your dwelling coverage (Coverage A). On a home insured for $450,000, a 2% deductible is $9,000. If wind damage totals $14,000, the policy pays $5,000. If the damage totals $8,500, the policy pays nothing.</p>
<h2>What triggers it</h2>
<p>The policy spells out the trigger. Common versions refer to a hurricane or named storm declared by the National Hurricane Center or National Weather Service, sometimes with a window of hours before and after the storm. A strong nor’easter normally isn’t a named storm, so the standard deductible usually applies.</p>
<h2>Why the full scope matters even more</h2>
<p>With a fixed deductible of several thousand dollars, every missed slope, siding wall or interior ceiling comes straight out of what you’re paid. That’s why a careful estimate review matters most when a hurricane deductible is in play.</p>
<h3>Try your numbers</h3>
<p>Our <a href="/policyholder-tools/hurricane-deductible-calculator/">hurricane deductible calculator</a> converts the percentage into dollars and compares it with your standard deductible. All figures in this article are illustrative.</p>""",
    },
    {
        "slug": "documenting-ice-dam-and-nor-easter-damage", "date": "2026-10-08", "read": "6 min",
        "title": "Documenting Ice Dam and Nor’easter Damage for a Claim",
        "seo": "Documenting Ice Dam & Nor’easter Damage",
        "summary": "A winter checklist for photos, receipts and notes that make an ice-dam or nor’easter claim easier to value.",
        "desc": "How to document ice dam, snow and nor’easter damage in Rhode Island: photos, receipts, timelines and the details appraisers look for.",
        "body": """
<p>Winter claims in Rhode Island have a documentation problem: the evidence melts. Ice dams disappear in a thaw, snow slides off and stains dry. Good records made in the moment are what keep the claim intact.</p>
<h2>Outside</h2>
<ul>
<li>Photograph ice ridges along the eaves and icicles from the ground, with something for scale.</li>
<li>Photograph every side of the house after the storm, including damaged gutters, shingles and siding.</li>
<li>Note the storm’s date and name if it had one, and keep weather reports.</li>
</ul>
<h2>Inside</h2>
<ul>
<li>Photograph stains, drips and wet insulation as soon as you see them, then again as they spread.</li>
<li>Use a moisture meter if you have one, or ask the mitigation company for readings.</li>
<li>Photograph the thermostat setting if pipes froze.</li>
</ul>
<h2>Receipts and invoices</h2>
<p>Keep invoices for roof raking, ice-dam steaming, snow removal, tarping and water extraction. Reasonable mitigation costs are often part of the claim.</p>
<h2>Write a short timeline</h2>
<p>When did the storm hit, when did you notice the leak, what did you do and when did you report it? A one-page timeline written while it’s fresh is worth more than memories months later.</p>""",
    },
    {
        "slug": "wind-versus-flood-after-a-coastal-storm", "date": "2026-09-24", "read": "8 min",
        "title": "Wind Versus Flood After a Coastal Storm",
        "seo": "Wind Versus Flood After a Rhode Island Coastal Storm",
        "summary": "How homeowner and flood policies divide a coastal loss, what each covers and how to organize a mixed claim.",
        "desc": "How wind and flood damage are separated after a Rhode Island coastal storm, what each policy covers and how to organize a mixed claim.",
        "body": """
<p>When a hurricane or strong nor’easter hits Rhode Island’s coast, many homes take damage from both wind and water. Two policies, two adjusters and two sets of rules can follow. Understanding the split early prevents gaps.</p>
<h2>The basic division</h2>
<ul>
<li><strong>Homeowner policy:</strong> wind damage, and rain that enters through an opening created by wind. Flood and storm surge are excluded.</li>
<li><strong>Flood policy</strong> (NFIP or private): damage from rising water, including surge, subject to its own limits, deductible and rules, which can be narrow for basements.</li>
</ul>
<h2>Where disputes start</h2>
<p>A first-floor wall can be soaked by surge, by rain through a damaged roof or by both. Each insurer may attribute more of the damage to the other peril. Water lines, debris lines, photos of the roof damage and the order of events all help show what caused what.</p>
<h2>Organize before the adjusters arrive</h2>
<p>List each damaged area, the likely cause and your evidence. Our <a href="/policyholder-tools/wind-flood-damage-splitter/">wind vs. flood damage splitter</a> lets you tag items and see how deductibles apply to each portion.</p>
<h2>Where appraisal fits</h2>
<p>Appraisal under the homeowner policy can resolve the amount of the wind-related loss once coverage is accepted. Causation disputes between the two policies often sit outside appraisal, and a Rhode Island attorney may be the right call for those.</p>""",
    },
    {
        "slug": "matching-materials-on-older-rhode-island-homes", "date": "2026-09-10", "read": "6 min",
        "title": "Matching Materials on Older Rhode Island Homes",
        "seo": "Matching Materials on Older Rhode Island Homes",
        "summary": "Slate, cedar, clapboard and plaster: why matching is a frequent dispute on Rhode Island’s older houses, and how it’s documented.",
        "desc": "Why matching slate, cedar shingle, clapboard and plaster is a frequent claim dispute on older Rhode Island homes, and how it is documented.",
        "body": """
<p>Rhode Island has some of the oldest housing in the country. When a storm damages part of a slate roof in Providence, a cedar-shingled wall in Westerly or plaster ceilings in Pawtucket, the question isn’t only what was damaged. It’s whether a repair can match what’s left.</p>
<h2>Why matching comes up so often here</h2>
<ul>
<li>Older materials weather and fade, so new pieces stand out.</li>
<li>Many products used decades ago are discontinued.</li>
<li>Historic district rules in places like Newport, Providence, Bristol and Wickford may require specific materials.</li>
</ul>
<h2>What policies say</h2>
<p>Policy language on matching varies. Some forms address it directly; others say only that repairs use materials of “like kind and quality.” Some states have regulations on matching; the policy and any applicable rules control. We value the cost of a reasonable repair and document the matching question with photos, samples and product research.</p>
<h2>How we document it</h2>
<ol>
<li>Identify the existing material: type, size, profile, color and age.</li>
<li>Research whether a reasonable match is available.</li>
<li>Show, with photos or samples, how a partial repair would look.</li>
<li>Price the repair that achieves a reasonable, uniform appearance.</li>
</ol>""",
    },
    {
        "slug": "choosing-claim-help-in-rhode-island", "date": "2026-08-27", "read": "5 min",
        "title": "Appraiser, Public Adjuster or Attorney: Choosing Claim Help",
        "seo": "Appraiser, Adjuster or Attorney? Choosing Claim Help",
        "summary": "Three kinds of help for a property claim, what each one does and how to tell which you need first.",
        "desc": "Appraiser, public adjuster or attorney? What each one does on a Rhode Island property claim and how to decide which kind of help you need first.",
        "body": """
<p>When a property claim stalls, owners hear about three kinds of help. They do different jobs, and starting with the right one saves time and money.</p>
<h2>Insurance appraiser</h2>
<p>An appraiser values the loss. Within the appraisal process, each side’s appraiser works out the amount of loss, and an umpire resolves differences. Appraisal fits when coverage is accepted and the dispute is about money.</p>
<h2>Public adjuster</h2>
<p>A public adjuster is licensed to represent policyholders in preparing and negotiating claims, often from the start of the claim. In Rhode Island, public adjusters are licensed through the Department of Business Regulation.</p>
<h2>Attorney</h2>
<p>An attorney handles legal questions: denials, coverage disputes, bad-faith claims, deadlines and lawsuits. If a suit-limitation date is close or your claim was denied, start here.</p>
<h2>A quick way to decide</h2>
<ul>
<li>Claim denied, or a deadline is close: attorney.</li>
<li>Claim just starting and you want someone to manage it: public adjuster.</li>
<li>Coverage accepted, number disputed: appraiser.</li>
</ul>
<p>We’ll tell you on the first call if your claim needs someone other than us.</p>""",
    },
]
