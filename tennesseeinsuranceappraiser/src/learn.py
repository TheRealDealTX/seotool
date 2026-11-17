"""Resources: process guide, FAQ, glossary and guide articles for Tennessee property owners."""

_T = "/tennessee-claim-tools/"
_S = "/tn-claim-appraisals/"

PROCESS_STEPS = [
    ("Pin down the disagreement", "Get the carrier’s full, itemized estimate in writing and compare it line by line with an independent estimate. Appraisal works only when the dispute is about the amount of a covered loss."),
    ("Check the policy and the calendar", "Find the appraisal condition, the suit-limitation clause and any proof-of-loss request. Note every deadline before you act."),
    ("Send a written demand", "Either side can demand appraisal in writing. Reference the policy and claim numbers, state that you disagree on the amount of loss, and name your appraiser or say you will within the policy’s window."),
    ("Both sides name appraisers", "Each party selects a competent, impartial appraiser — commonly within 20 days of the demand. The carrier’s appraiser is often an independent firm it hires."),
    ("Agree on an umpire", "The two appraisers select a neutral umpire. If they can’t agree within the policy’s window, either side can usually ask a court of record in the county where the property sits to appoint one."),
    ("Inspect, price and negotiate", "The appraisers inspect, exchange estimates and work through disputed line items. Most of the gap usually narrows at this stage."),
    ("Umpire review if needed", "Items still in dispute go to the umpire with photos, measurements and pricing support from each appraiser."),
    ("Signed award and payment", "A written award signed by any two of the three sets the amount of loss. The carrier then pays under the policy’s terms, less the deductible and any prior payments."),
]

PROCESS_BODY = f"""
<p>Appraisal is a short paragraph in most Tennessee property policies, but it sets up a complete dispute-resolution process. Here is how it usually unfolds, step by step, and where claims tend to stall. Policy wording differs, so read your own form alongside this guide.</p>
<h2>Before you start: is this an amount dispute?</h2>
<p>Appraisal settles <strong>how much</strong> a covered loss costs. It isn’t designed to decide <strong>whether</strong> the loss is covered. If the carrier says “we’ll pay for six squares” and you say the roof needs twenty-eight, that’s an amount dispute. If the carrier says “wear and tear isn’t covered,” that’s a coverage dispute, and appraisal alone usually won’t solve it.</p>
<div class="note"><b class="h">Get legal advice for denials</b>Tennessee law gives policyholders a statutory bad-faith remedy in certain circumstances, along with other contract remedies. Those are pursued through the courts, not through appraisal. For outright denials or approaching deadlines, consult a Tennessee attorney.</div>
<h2>The eight stages of a Tennessee appraisal</h2>
<ol class="steps">{"".join(f"<li><h3>{t}</h3><p>{d}</p></li>" for t, d in PROCESS_STEPS)}</ol>
<h2>What a well-prepared file contains</h2>
<ul>
<li>The complete policy, including declarations and endorsements.</li>
<li>The carrier’s itemized estimate and all correspondence, in date order.</li>
<li>An independent, line-item estimate — not a lump-sum bid.</li>
<li>Dated photos and video taken soon after the loss, plus current photos.</li>
<li>Mitigation invoices, drying logs and receipts for temporary repairs.</li>
<li>Any engineer, roofer or restoration reports.</li>
</ul>
<p>Our <a href="{_T}appraisal-readiness-check/">appraisal readiness check</a> scores your file in about two minutes.</p>
<h2>How long does it take?</h2>
<p>A simple residential appraisal often resolves within two to three months after both appraisers are named. Commercial losses, contents-heavy claims and panels that need a formal umpire hearing take longer. Delays usually come from missing documents, slow appraiser selection or disagreement over the umpire.</p>
<h2>What it costs</h2>
<p>Each side pays its own appraiser, and the umpire’s fee is usually split evenly. Appraiser fees may be flat, hourly or a percentage of the increase. Use the <a href="{_T}claim-gap-calculator/">claim gap &amp; fee estimator</a> to see whether the math works before you start.</p>
<h2>After the award</h2>
<p>The award typically states replacement cost and actual cash value, and sometimes breaks the loss out by category. The carrier applies the deductible, subtracts prior payments and pays the balance. Recoverable depreciation follows the policy’s normal rules, usually after repairs are completed.</p>
"""

FAQ = [
    ("Appraisal basics", [
        ("What is insurance appraisal?", "A process written into most property policies for resolving disagreements over the amount of a covered loss. Each side names an appraiser, the appraisers choose an umpire, and a written agreement by any two sets the amount."),
        ("Who can demand appraisal?", "Either you or the insurance company, as long as the policy contains an appraisal clause and the dispute is about the amount of loss."),
        ("Is appraisal the same as mediation?", "No. Mediation is a negotiation with a neutral facilitator and isn’t binding unless both sides sign a settlement. An appraisal award signed by two of the three panel members is binding on the amount of loss."),
        ("Does appraisal decide coverage?", "No. It decides the amount of loss. Coverage questions — whether a peril or item is covered at all — remain for the parties and, if necessary, the courts."),
    ]),
    ("Tennessee specifics", [
        ("Who regulates insurance in Tennessee?", "The Tennessee Department of Commerce and Insurance. It licenses insurers and adjusters and accepts consumer complaints about claim handling."),
        ("Does Tennessee have a FAIR plan or wind pool?", "No. Unlike many states, Tennessee doesn’t operate a FAIR plan or wind pool. Owners who can’t find standard coverage often turn to surplus-lines insurers, whose policies can contain different appraisal and settlement terms."),
        ("What is Tennessee’s bad-faith statute?", "Tennessee law (Tenn. Code Ann. § 56-7-105) allows a penalty of up to 25% of the loss in limited circumstances when an insurer’s refusal to pay is found to be in bad faith. It has specific requirements, including a formal demand and a waiting period. It’s a legal remedy, so talk to a Tennessee attorney about it."),
        ("Are earthquakes covered in Tennessee?", "Not under standard homeowner policies. Earthquake coverage, most often purchased in West Tennessee near the New Madrid Seismic Zone, is added by endorsement and usually carries a percentage deductible."),
        ("How many counties do you serve?", "All 95 Tennessee counties, across East, Middle and West Tennessee."),
    ]),
    ("Cost and timing", [
        ("How much does appraisal cost?", "You pay your own appraiser and usually half of the umpire’s fee. We put our fee in writing before any work begins, and the first conversation is free."),
        ("How long does appraisal take?", "Many residential claims resolve within two to three months after both appraisers are named. Larger or more complex claims can take longer."),
        ("Is it worth it for a small gap?", "Often not. When the difference is small, a documented supplement request is usually faster and cheaper. Our claim gap estimator helps you check."),
    ]),
    ("Working with us", [
        ("Are you a public adjuster or a law firm?", "Neither. We provide appraisal, estimating and umpire services. We don’t give legal advice or negotiate claims outside the appraisal process."),
        ("Do you work for insurance companies?", "When we serve as an umpire, we represent neither side. When you appoint us as your appraiser, we serve in that role only and disclose any prior relationships."),
        ("What should I send you first?", "Your declarations page, the carrier’s full estimate, any letters from the carrier, your photos and any contractor estimate you have."),
        ("Can contractors or attorneys refer clients?", "Yes. We regularly work alongside contractors, attorneys and public adjusters who need an independent valuation."),
    ]),
]

GLOSSARY = [
    ("Actual cash value (ACV)", "The value of damaged property at the time of loss, usually replacement cost minus depreciation."),
    ("Additional living expense (ALE)", "Coverage for extra costs of living elsewhere while your home is being repaired."),
    ("Amount of loss", "The cost to repair or replace covered damage — the question an appraisal panel decides."),
    ("Appraisal award", "The written decision signed by two of the three panel members that sets the amount of loss."),
    ("Appraisal clause", "The policy condition that lets either party demand appraisal when they disagree on the amount of loss."),
    ("Bad-faith penalty", "A statutory remedy in Tennessee, available in limited circumstances, when an insurer’s refusal to pay is found to lack good faith."),
    ("Causation", "Whether a covered peril caused the damage. Often argued as a coverage issue rather than an amount issue."),
    ("Coinsurance", "A commercial-policy provision that can reduce payment if a building is insured below a required percentage of its value."),
    ("Collateral damage", "Dents and marks on gutters, vents and other soft metals that help confirm and date a hailstorm."),
    ("Coverage A", "The dwelling coverage limit on a homeowner policy."),
    ("Debris removal", "Coverage for removing debris of covered property, often with additional limited coverage beyond the dwelling limit."),
    ("Declarations page", "The summary page listing your coverages, limits, deductibles and endorsements."),
    ("Depreciation", "Reduction in value due to age, wear and condition, used to calculate actual cash value."),
    ("Derecho", "A long-lived, widespread windstorm with damaging straight-line winds, such as the July 2003 Memphis storm."),
    ("Disinterested appraiser", "An appraiser with no financial stake in the outcome of the claim."),
    ("Dwelling-fire policy", "A policy form often used for rental homes, with settlement terms that can differ from homeowner forms."),
    ("Earthquake endorsement", "Optional coverage added to a property policy for earthquake damage, usually with a percentage deductible."),
    ("Endorsement", "A written change to the policy that adds, removes or modifies coverage."),
    ("Estimate review", "A line-by-line audit of an insurance estimate to identify missing items and pricing errors."),
    ("Functional damage", "Damage that affects how a material performs, such as hail fractures that shorten a shingle’s life."),
    ("HO-3", "The most common homeowner policy form, covering the dwelling on an open-perils basis."),
    ("HO-6", "A condominium unit-owner policy covering interior improvements and personal property."),
    ("Holdback", "Recoverable depreciation withheld until repairs are completed."),
    ("Like kind and quality", "The standard for replacement materials of similar type and quality to what was damaged."),
    ("Line item", "An individual entry in an estimate, such as a quantity of shingles or a square foot of drywall."),
    ("Matching", "The question of whether undamaged materials must be replaced so repairs reasonably match."),
    ("Mitigation", "Steps taken to prevent further damage after a loss, such as tarping or drying."),
    ("New Madrid Seismic Zone", "An active fault zone affecting West Tennessee, relevant to earthquake coverage decisions."),
    ("Ordinance or law", "Coverage for added costs to meet current building codes during repairs."),
    ("Overhead and profit (O&P)", "A general contractor’s charge for coordinating multiple trades, often 10% plus 10%."),
    ("Percentage deductible", "A deductible calculated as a percentage of the dwelling limit rather than a flat dollar amount."),
    ("Proof of loss", "A sworn statement of the amount claimed, which an insurer may request within a stated period."),
    ("Recoverable depreciation", "Depreciation that can be collected after repairs are completed under a replacement cost policy."),
    ("Replacement cost value (RCV)", "The cost to repair or replace damaged property with new materials of like kind and quality."),
    ("Scope of loss", "The list of damaged items and the repairs needed."),
    ("Square", "100 square feet of roof surface."),
    ("Steep charge", "An added labor cost for working on roofs with a high pitch."),
    ("Suit limitation", "A policy clause limiting the time to file a lawsuit against the insurer."),
    ("Supplement", "A request for additional payment for items missed in the original estimate."),
    ("Surplus lines", "Insurance from non-admitted carriers, often used when standard coverage isn’t available."),
    ("TDCI", "The Tennessee Department of Commerce and Insurance, the state’s insurance regulator."),
    ("Umpire", "The neutral third panel member who decides items the two appraisers can’t agree on."),
    ("Waste factor", "Extra material added to an estimate for cutting and fitting, especially on roofs."),
]

POSTS = [
    {
        "slug": "reading-the-appraisal-clause-in-a-tennessee-policy",
        "title": "Reading the Appraisal Clause in a Tennessee Policy",
        "seo": "Reading the Appraisal Clause in a Tennessee Policy",
        "desc": "A plain-English guide to the appraisal clause in Tennessee property policies: the trigger, deadlines, umpire selection and binding award.",
        "date": "2026-10-14", "read": "7 min",
        "summary": "The appraisal paragraph is short, but every phrase does work. Here’s how to read it before you send or answer a demand.",
        "body": f"""
<p>Most Tennessee homeowners have never read the appraisal paragraph in their policy. It sits in the conditions section, usually between “Loss Payment” and “Suit Against Us,” and runs a hundred-odd words. Here is what the typical pieces mean in practice. Your carrier’s exact wording controls.</p>
<h2>The trigger: “if you and we fail to agree on the amount of loss”</h2>
<p>Appraisal is for amount disputes. It isn’t designed to decide whether something is covered. The line can blur — a disagreement about how many slopes hail damaged sounds like amount, while “hail didn’t cause this” sounds like coverage — and courts in different jurisdictions treat causation questions differently. Expect the carrier to label some issues as coverage.</p>
<h2>The demand: “either may demand appraisal”</h2>
<p>Either side can start the process. Put the demand in writing, cite the policy and claim numbers, state the disagreement and reference the appraisal condition. Keep proof of when it was sent.</p>
<h2>The appraisers: “competent and impartial”</h2>
<p>Some forms say “disinterested.” Either way, the person you name should know how to value your type of loss and have no stake in the repair contract. Many forms set a 20-day window to name your appraiser after the demand.</p>
<h2>The umpire</h2>
<p>The two appraisers choose an umpire. If they can’t agree within the policy’s window, either side can typically ask a court of record in the county where the property is located to appoint one.</p>
<h2>The award: “agreement by any two”</h2>
<p>This is what gives appraisal force. A written award signed by two of the three panel members sets the amount of loss. That’s why preparation matters before you demand — see our <a href="{_T}appraisal-readiness-check/">readiness check</a>.</p>
<h2>Costs</h2>
<p>Each side pays its own appraiser and usually half the umpire. Some policies also split other appraisal expenses.</p>
""",
    },
    {
        "slug": "after-a-tennessee-tornado-first-30-days",
        "title": "After a Tennessee Tornado: Your First 30 Days of the Claim",
        "seo": "After a Tennessee Tornado: First 30 Days of the Claim",
        "desc": "A practical 30-day checklist for Tennessee tornado claims: safety, documentation, mitigation, estimates and deadlines that protect you.",
        "date": "2026-10-21", "read": "8 min",
        "summary": "What you do in the first month after a tornado shapes the whole claim. A practical checklist built from Tennessee storm seasons.",
        "body": f"""
<p>Tennessee tornadoes often strike at night and often in clusters, as Nashville, Cookeville, Clarksville and countless smaller towns have learned. Once everyone is safe, the claim begins. These steps protect your recovery.</p>
<h2>Days 1–3: safety and notice</h2>
<ul><li>Stay out of damaged structures until utilities are safe and the building is stable.</li>
<li>Report the claim to your insurer and write down the claim number, adjuster name and every call.</li>
<li>Photograph and video everything before anything is moved — exterior, roof from the ground, every room and damaged contents.</li></ul>
<h2>Days 3–10: stop further damage</h2>
<ul><li>Tarp roofs and board up openings. Keep invoices; reasonable mitigation is usually reimbursable.</li>
<li>Remove standing water and start drying wet materials.</li>
<li>Save samples of damaged siding, shingles or flooring for matching later.</li></ul>
<h2>Days 10–20: build your own scope</h2>
<p>Before the adjuster’s estimate becomes the only number in the file, get an independent, itemized estimate. After big outbreaks, contractor pricing rises quickly, so make sure the estimate reflects current local rates.</p>
<h2>Days 20–30: compare and decide</h2>
<p>When the carrier’s estimate arrives, compare it line by line. Use the <a href="{_T}claim-gap-calculator/">claim gap estimator</a> and the <a href="{_T}rcv-acv-holdback-calculator/">holdback calculator</a> to understand what you’ll be paid and when. If the gap is large, appraisal may be appropriate.</p>
<h2>Don’t forget the calendar</h2>
<p>Proof-of-loss requests, depreciation recovery windows and suit-limitation clauses all run in the background. Our <a href="{_T}claim-deadline-calendar/">deadline calendar</a> puts them on your phone.</p>
""",
    },
    {
        "slug": "burst-pipes-after-a-hard-freeze",
        "title": "Burst Pipes After a Hard Freeze: How Tennessee Claims Play Out",
        "seo": "Burst Pipes After a Freeze: Tennessee Claim Guide",
        "desc": "How burst-pipe claims play out after a Tennessee freeze: heat and vacancy wording, documentation, drying records and valuing the loss.",
        "date": "2026-10-28", "read": "6 min",
        "summary": "Hard freezes catch Tennessee homes off guard. Here’s how freeze claims are handled, where they stall and how to document them.",
        "body": f"""
<p>Tennessee winters are usually mild, which is exactly why a hard freeze does so much damage. Pipes run through exterior walls, attics and crawlspaces that were never built for single digits. The Christmas 2022 cold snap and the January 2024 freeze left thousands of water claims across the state.</p>
<h2>The coverage question comes first</h2>
<p>Many homeowner policies cover freezing of plumbing only if you used reasonable care to maintain heat, or shut off and drained the water. Vacant homes, seasonal cabins and rentals between tenants are the most exposed to a denial on this basis. That’s a coverage issue to sort out before valuation.</p>
<h2>Document like you’ll need to prove it</h2>
<ul><li>Note the thermostat setting and keep utility bills that show the heat was on.</li>
<li>Photograph the split pipe and keep it if the plumber removes it.</li>
<li>Get the plumber’s invoice describing the cause and location.</li>
<li>Keep moisture readings and drying logs from the restoration company.</li></ul>
<h2>Where freeze estimates come up short</h2>
<p>Pipe bursts often affect multiple rooms or floors, and water travels inside walls. Estimates frequently miss insulation, subfloor, cabinetry and continuous flooring. After a statewide freeze, plumbers and restoration crews are stretched thin, and prices reflect it.</p>
<h2>When appraisal fits</h2>
<p>If coverage is accepted and the dispute is about the scope or price of repairs, appraisal can resolve it. See our <a href="{_S}ice-storm-freeze-appraisal/">ice storm &amp; freeze appraisal</a> service.</p>
""",
    },
    {
        "slug": "matching-siding-and-shingles-after-a-storm",
        "title": "Matching Siding and Shingles After a Storm",
        "seo": "Matching Siding and Shingles After a Storm Claim",
        "desc": "Why matching disputes cause so many underpaid storm claims, how to document discontinued siding and shingles, and when appraisal helps.",
        "date": "2026-11-03", "read": "6 min",
        "summary": "One damaged wall, three good ones and a siding color that no longer exists. Matching is one of the most common storm-claim disputes.",
        "body": f"""
<p>Storms rarely damage every side of a house equally. Hail may hit only the west elevation; a tornado may peel siding off one corner. The carrier offers to replace what’s damaged. The problem: the replacement doesn’t match.</p>
<h2>Why matching disputes happen</h2>
<p>Siding colors fade and profiles get discontinued. Shingle lines change every few years. Brick blends vary by batch. A patch that technically restores the damaged area can leave a home visibly mismatched.</p>
<h2>What policies and rules say</h2>
<p>Policies usually promise repair or replacement with materials of like kind and quality. How that applies to undamaged areas varies by policy language and jurisdiction, and carriers take different positions. The facts — whether a reasonable match is available — usually drive the outcome.</p>
<h2>How to document a matching problem</h2>
<ul><li>Identify the product, manufacturer and color where possible.</li>
<li>Get written confirmation from suppliers that the product is discontinued.</li>
<li>Photograph test pieces held against the existing material.</li>
<li>Note continuous runs: siding that wraps corners, flooring that flows between rooms.</li></ul>
<h2>When appraisal helps</h2>
<p>If coverage is accepted and the dispute is how much of the material must be replaced for a reasonable repair, appraisal panels often address it as part of the amount of loss. A strong record makes the difference.</p>
""",
    },
    {
        "slug": "estimate-red-flags-tennessee-roof-claims",
        "title": "Ten Red Flags in a Tennessee Roof Estimate",
        "seo": "Ten Red Flags in a Tennessee Roof Claim Estimate",
        "desc": "Ten common red flags in Tennessee roof insurance estimates, from undercounted squares and missing steep charges to absent code items.",
        "date": "2026-11-07", "read": "7 min",
        "summary": "Roof estimates follow patterns. These ten red flags show up again and again in underpaid Tennessee roof claims.",
        "body": f"""
<p>Roof claims are the most common property claims in Tennessee, and many estimates share the same omissions. Check yours for these red flags.</p>
<ol>
<li><strong>Squares don’t match reality.</strong> Compare against a measurement or our <a href="{_T}roof-area-pitch-calculator/">roof area &amp; pitch calculator</a>.</li>
<li><strong>Low waste factor.</strong> A hip roof with valleys needs more waste than a simple gable.</li>
<li><strong>No steep charges</strong> on roofs pitched around 7/12 and above.</li>
<li><strong>No high-roof charges</strong> on two-story sections.</li>
<li><strong>Missing starter and ridge cap</strong> as separate lines.</li>
<li><strong>No drip edge or underlayment upgrades</strong> where code or manufacturer specs require them.</li>
<li><strong>Gutters and downspouts ignored</strong> despite visible hail or wind damage.</li>
<li><strong>Detach-and-reset items missing</strong> — satellite dishes, solar panels, skylights.</li>
<li><strong>Repair instead of replacement</strong> on a discontinued or brittle roof.</li>
<li><strong>No overhead and profit</strong> when multiple trades are needed.</li>
</ol>
<p>Finding two or three of these doesn’t guarantee an underpayment, but it’s a strong signal to get a professional <a href="{_S}insurance-estimate-audit/">estimate review</a>.</p>
""",
    },
    {
        "slug": "appraisal-or-attorney-choosing-the-right-help",
        "title": "Appraisal or Attorney? Choosing the Right Help in Tennessee",
        "seo": "Appraisal or Attorney? Choosing Help in Tennessee",
        "desc": "When a Tennessee property claim calls for an appraiser, a public adjuster or an attorney, and why picking the right help first matters.",
        "date": "2026-11-12", "read": "6 min",
        "summary": "Appraisers, public adjusters and attorneys solve different problems. Choosing the right one first saves time and money.",
        "body": f"""
<p>When a claim stalls, it’s tempting to call the first professional you find. But each type of help fits a different problem.</p>
<h2>An appraiser fits amount disputes</h2>
<p>If the insurer accepts coverage and the dispute is about price or scope, an appraiser working under the policy’s appraisal clause is often the most direct path to a binding number.</p>
<h2>A public adjuster manages the whole claim</h2>
<p>Licensed public adjusters represent policyholders throughout the claim process — documenting, presenting and negotiating. They’re often brought in early, especially on large or complex losses.</p>
<h2>An attorney handles legal disputes</h2>
<p>Denials, coverage disputes, bad-faith conduct and approaching suit deadlines call for a Tennessee attorney. Tennessee’s statutory bad-faith remedy and contract claims are pursued through the courts.</p>
<h2>A quick decision guide</h2>
<div class="table-wrap"><table><thead><tr><th>Situation</th><th>Usually start with</th></tr></thead><tbody>
<tr><th>Coverage accepted, number too low</th><td>Appraiser / estimate review</td></tr>
<tr><th>Early in a large, complex claim</th><td>Public adjuster</td></tr>
<tr><th>Claim denied or deadline close</th><td>Attorney</td></tr>
<tr><th>Not sure</th><td>A free conversation to triage</td></tr>
</tbody></table></div>
<p>We’ll tell you honestly if appraisal isn’t the right fit. Start with our <a href="/get-a-claim-review/">free claim review</a>.</p>
""",
    },
]
