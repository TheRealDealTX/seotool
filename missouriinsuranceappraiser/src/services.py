"""Service pages for Missouri Insurance Appraiser (missouriinsuranceappraiser.com).

Each entry renders at /appraisal-help/<slug>/. Bodies are HTML fragments that sit under the page H1.
"""

SERVICES = [
    # 1 ------------------------------------------------------------------
    {
        "slug": "appraisal-demand-representation",
        "name": "Appraisal Demand Representation",
        "kw": "appraisal clause representation in Missouri",
        "short": "Your own appraiser under the policy’s appraisal clause, from the demand letter to a signed award.",
        "h1": "Appraisal Clause Representation in Missouri, From Demand to Award",
        "lede": "When you and your insurer agree there’s a covered loss but can’t agree on what it costs to fix, the appraisal clause gives you a way to settle the number. We serve as your appraiser and build the case for the full amount of loss.",
        "facts": [
            ("Best stage", "After the carrier estimate"),
            ("Decides", "Amount of loss only"),
            ("Serving", "All of Missouri"),
        ],
        "title": "Appraisal Clause Representation in Missouri Claims",
        "desc": "Need an appraiser under your policy’s appraisal clause? We represent Missouri homeowners and businesses from the written demand to a signed award.",
        "body": """<p>Most Missouri homeowners and commercial property policies contain an appraisal clause. It’s a short paragraph, usually under the conditions section, that says if you and the insurance company disagree on the <strong>amount of loss</strong>, either side can demand appraisal in writing. Each side then picks its own appraiser, the two appraisers pick an umpire, and an agreement signed by any two of the three sets the amount. It’s a private, practical process built for exactly one question: what does it cost to put this property back?</p>

<h2>What appraisal can and can’t settle</h2>
<p>Appraisal is about dollars, not coverage. If the carrier has denied the claim outright, says the damage is from wear and tear, or says a whole category of loss isn’t covered, that’s a coverage dispute. Appraisers don’t rule on it. If the carrier has accepted the claim but its estimate is thin, appraisal is often the right tool.</p>
<ul>
<li><strong>Good fit:</strong> the adjuster priced a roof repair when the slope needs replacing, left out interior trades, or used unit prices that don’t match what Missouri contractors actually charge.</li>
<li><strong>Usually not a fit:</strong> a full denial, a late-notice argument, or a dispute about whether a peril is excluded. Those are questions for a Missouri attorney.</li>
<li><strong>Gray area:</strong> disputes about how much of the damage came from a covered event. Some policies and courts treat that as part of the amount of loss; others don’t. The policy wording controls.</li>
</ul>

<h2>How we handle an appraisal demand</h2>
<h3>Reading the clause first</h3>
<p>Appraisal clauses aren’t identical. Some give each side 20 days to name an appraiser; some require the appraisers to be “competent and impartial” or “disinterested”; some spell out who pays the umpire. We read your declarations page, the clause, and the loss settlement provisions before anything is sent, so the demand fits your policy.</p>
<h3>Building the number</h3>
<p>We inspect the property, document the damage with photos and measurements, and write a line-item estimate in the same estimating format carriers use. Then we compare it against the insurer’s estimate line by line so every disagreement is visible and supported. Our <a href="/appraisal-roadmap/">appraisal roadmap</a> lays out each step in order.</p>
<h3>Working with the other appraiser</h3>
<p>Most appraisals settle between the two appraisers without an umpire. That happens when the supporting documents are clear enough that the other side can’t reasonably argue with them. If we can’t agree, the disputed items go to the umpire, and we present our side.</p>

<h2>What it looks like on paper</h2>
<div class="table-wrap"><table>
<thead><tr><th>Stage</th><th>What happens</th><th>Who acts</th></tr></thead>
<tbody>
<tr><td>Demand</td><td>Written notice invoking appraisal</td><td>You or the carrier</td></tr>
<tr><td>Selection</td><td>Each side names its appraiser</td><td>Both sides</td></tr>
<tr><td>Umpire</td><td>Appraisers agree on a neutral</td><td>The two appraisers</td></tr>
<tr><td>Review</td><td>Inspection, estimates, negotiation</td><td>Appraisers</td></tr>
<tr><td>Award</td><td>Signed by any two of three</td><td>Appraisers and umpire</td></tr>
</tbody></table></div>

<h2>Missouri context worth knowing</h2>
<p>Property insurance in Missouri is regulated by the Missouri Department of Commerce and Insurance (DCI), which takes consumer complaints about claim handling. Missouri also has unfair claims settlement practices rules that set general expectations for how insurers acknowledge, investigate and pay claims. Separately, Missouri’s vexatious refusal to pay statutes may allow added penalties and attorney fees when an insurer refuses to pay without reasonable cause. Whether any of that applies to your claim is a legal question for a Missouri attorney, and we don’t give legal advice.</p>
<div class="note"><p>Appraisal is not a lawsuit and we are not a law firm or a public adjuster. We serve as your appraiser on the amount of loss. Deadlines in your policy and under Missouri law can be short, so don’t sit on a disputed claim.</p></div>

<h2>Before you send a demand</h2>
<ol>
<li>Get the carrier’s full estimate in writing, not just the payment letter.</li>
<li>Pull a certified copy of your policy, including endorsements.</li>
<li>Gather your own contractor bids, photos, receipts and any engineer reports.</li>
<li>Note every date: loss date, notice date, inspection, payments.</li>
</ol>
<p>If you’re not sure appraisal fits, <a href="/get-in-touch/">tell us about the claim</a> and we’ll give you a straight answer.</p>""",
        "faqs": [
            ("Who can demand appraisal in Missouri?", "Under most policies either you or the insurer can demand appraisal in writing once there’s a disagreement over the amount of loss. Check your policy’s appraisal clause, because the steps and timelines vary."),
            ("Is the appraisal award binding?", "Most clauses say an award signed by two of the three panel members sets the amount of loss. The carrier can still raise coverage issues, and questions about enforcing or challenging an award belong with a Missouri attorney."),
            ("Do I pay for the umpire?", "Many policies split the umpire’s fee equally between you and the insurer, while each side pays its own appraiser. Your policy wording controls."),
        ],
    },
    # 2 ------------------------------------------------------------------
    {
        "slug": "homeowner-claim-appraisal",
        "name": "Homeowner Claim Appraisal",
        "kw": "homeowners insurance appraisal Missouri",
        "short": "Help for Missouri homeowners whose claim payment won’t cover the actual cost of repairs.",
        "h1": "Homeowners Insurance Appraisal for Missouri Families",
        "lede": "Your house is probably the biggest thing you own, and the adjuster may have spent an hour on it. We take the time to document the full loss and stand in as your appraiser when the numbers don’t add up.",
        "facts": [
            ("Policy types", "HO-3, HO-5, HO-6, DP-3"),
            ("Typical fight", "Scope and unit pricing"),
            ("Areas", "Statewide, 114 counties"),
        ],
        "title": "Homeowners Insurance Appraisal Missouri | Fair Claim Values",
        "desc": "Homeowners insurance appraisal for Missouri families whose claim check falls short. We document the loss and serve as your appraiser on the amount.",
        "body": """<p>A homeowners claim usually starts well. The adjuster comes out, takes photos, and a few weeks later an estimate arrives. Then your contractor reads it and tells you it won’t cover the job. The roof is priced as a repair, the paint stops at one wall, the drywall line is short, or the pricing looks like it came from a different market. That’s the moment many Missouri homeowners start looking at the appraisal clause in their policy.</p>

<h2>Where homeowner claims come up short</h2>
<p>From St. Joseph to Cape Girardeau, the same patterns show up in residential estimates:</p>
<ul>
<li><strong>Partial scope.</strong> Repairs priced only where damage is obvious, leaving out adjacent materials that have to be removed or replaced to do the job right.</li>
<li><strong>Matching.</strong> New siding, shingles or flooring that won’t match what’s left. How your policy handles that depends on its wording.</li>
<li><strong>Depreciation.</strong> On actual cash value policies or before recoverable depreciation is released, heavy depreciation on labor or materials can make the check look small.</li>
<li><strong>Overhead and profit.</strong> When a job needs a general contractor to coordinate three or more trades, contractor overhead and profit is often a reasonable line item.</li>
<li><strong>Code items.</strong> Local building departments may require upgrades. Whether they’re paid often turns on an ordinance-or-law coverage limit.</li>
</ul>

<h2>Know your policy form</h2>
<h3>HO-3 and HO-5</h3>
<p>The most common Missouri homeowners forms. The dwelling is usually written on an open-perils basis subject to exclusions, with replacement cost loss settlement. Many pay actual cash value first and the rest once repairs are done.</p>
<h3>HO-6 condo unit policies</h3>
<p>Condo owners have to sort out what the association’s master policy covers versus their own unit policy. That split comes from the declarations and bylaws, and it matters before anyone argues about price.</p>
<h3>DP-3 and rental homes</h3>
<p>Landlord policies often settle differently and may include lost rental income. We read the form before we estimate.</p>
<p>Not sure which you have? Our <a href="/appraisal-dictionary/">appraisal dictionary</a> explains the terms on your declarations page.</p>

<h2>How residential appraisal works with us</h2>
<ol>
<li><strong>Free first look.</strong> Send the carrier estimate and photos. We’ll tell you whether the gap looks like an amount-of-loss dispute.</li>
<li><strong>Inspection.</strong> We walk the house top to bottom: roof, attic, exterior elevations, every affected room.</li>
<li><strong>Our estimate.</strong> Line items, measurements and pricing that reflects your part of Missouri.</li>
<li><strong>Demand and panel.</strong> Once appraisal is invoked, we work with the carrier’s appraiser and, if needed, an umpire.</li>
<li><strong>Award.</strong> The signed award sets the amount of loss under the policy terms.</li>
</ol>

<div class="note"><p>For example, an illustrative claim might have a carrier estimate of $14,000 against a contractor bid of $31,000. Appraisal doesn’t guarantee you’ll get the higher figure. It gives both numbers a fair hearing on documented scope and pricing.</p></div>

<h2>Missouri homeowner realities</h2>
<p>Missouri sits in the path of spring hail, tornado outbreaks, summer derechos and winter ice. In rural counties a homeowner may wait weeks for a contractor after a big storm, and prices can climb as crews get booked. Older housing stock in places like Kansas City’s historic neighborhoods and St. Louis city brick homes can raise questions about plaster, old-growth trim and materials no longer sold. If your carrier won’t renew you, the Missouri FAIR Plan, formally the Missouri Property Insurance Placement Facility, is a fallback market, and its policies have appraisal provisions too.</p>
<p>If you have a complaint about how a claim is being handled, the Missouri Department of Commerce and Insurance accepts consumer complaints. For legal questions, talk to a Missouri attorney.</p>

<h2>When to call</h2>
<p>The best time is after you have the carrier’s written estimate and before you’ve cashed out and moved on. Use our <a href="/toolkit/">claim toolkit</a> to organize what you have, then reach out.</p>""",
        "faqs": [
            ("Can I use appraisal if my insurer already paid part of the claim?", "Usually yes. Accepting a partial payment doesn’t typically waive appraisal, but read any release carefully and ask a Missouri attorney if you’re unsure before signing."),
            ("Does appraisal cover my contents too?", "It can. If the disagreement includes personal property values, those items can be part of the appraisal as long as coverage for them isn’t in dispute."),
            ("How long does a homeowner appraisal take?", "Many residential appraisals wrap up in a few months, though it depends on how quickly appraisers are named, how complex the loss is and whether an umpire is needed."),
        ],
    },
    # 3 ------------------------------------------------------------------
    {
        "slug": "commercial-hoa-appraisal",
        "name": "Commercial & HOA Claim Appraisal",
        "kw": "commercial property claim appraisal Missouri",
        "short": "Appraisal for offices, retail, warehouses, churches, apartments and condo or HOA associations.",
        "h1": "Commercial Property Claim Appraisal Across Missouri",
        "lede": "Bigger buildings mean bigger estimates and more room for disagreement. We handle appraisal for Missouri businesses, congregations and associations whose carrier estimate doesn’t match the real scope.",
        "facts": [
            ("Property types", "Retail, office, apartments"),
            ("Common issue", "Roof systems and code"),
            ("Also covers", "Condo and HOA boards"),
        ],
        "title": "Commercial & HOA Claim Appraisal in Missouri",
        "desc": "Commercial and HOA property claim appraisal in Missouri for offices, retail, warehouses, churches and associations disputing the insurer’s estimate.",
        "body": """<p>Commercial claims in Missouri often involve large flat or low-slope roofs, multiple buildings, specialized systems and a policy with endorsements stacked several pages deep. When an insurer’s estimate for a strip center in Springfield, a warehouse in the Riverside area, or a church in Jefferson County lands far below what contractors are bidding, appraisal may be the cleanest way to settle the amount of loss without a lawsuit.</p>

<h2>Properties we handle</h2>
<ul>
<li><strong>Offices and retail:</strong> strip centers, standalone stores, medical offices, mixed-use buildings.</li>
<li><strong>Industrial:</strong> warehouses, light manufacturing, metal buildings, agricultural outbuildings with commercial coverage.</li>
<li><strong>Churches and nonprofits:</strong> sanctuaries with steep roofs, stained glass, fellowship halls and gyms.</li>
<li><strong>Apartments:</strong> garden-style complexes with many identical buildings and shared roof and siding systems.</li>
<li><strong>Condo and HOA associations:</strong> master policies covering roofs, exteriors and common elements.</li>
</ul>

<h2>Where commercial estimates diverge</h2>
<h3>Roof systems</h3>
<p>TPO, EPDM, modified bitumen, built-up and standing-seam metal roofs each have their own failure patterns. Hail can bruise insulation board under a membrane without obvious surface marks. Core samples and moisture surveys may be needed to establish the scope.</p>
<h3>Building code and ordinance-or-law</h3>
<p>Re-roofing a large commercial building can trigger insulation, drainage and parapet requirements under the local building code. Whether those costs are paid usually depends on an ordinance-or-law endorsement and its limits.</p>
<h3>Multiple buildings, one claim</h3>
<p>Apartment and HOA claims can involve dozens of structures. A carrier may sample a few and extrapolate. We push for a scope based on what’s actually on each building.</p>
<h3>Business income</h3>
<p>Lost income and extra expense often run alongside the property claim. Those figures can be part of an appraisal when coverage isn’t in dispute, though they usually need an accountant’s input.</p>

<h2>Working with HOA boards</h2>
<p>Association boards have duties to every owner, and they rarely have a construction professional on the board. We give boards a clear written comparison of the carrier estimate and ours, explain the appraisal process in plain terms, and keep management companies in the loop. The board decides whether to invoke appraisal; we don’t push it.</p>
<p>One common question: who covers what between the master policy and individual unit-owner policies. That split comes from the declaration, bylaws and policy language, and it should be settled before arguing about price.</p>

<div class="table-wrap"><table>
<thead><tr><th>Issue</th><th>What we look at</th></tr></thead>
<tbody>
<tr><td>Roof scope</td><td>Membrane, insulation, flashings, drains</td></tr>
<tr><td>Pricing</td><td>Commercial labor rates in your market</td></tr>
<tr><td>Code upgrades</td><td>Ordinance-or-law limits and triggers</td></tr>
<tr><td>Coinsurance</td><td>Insured value vs. replacement cost</td></tr>
</tbody></table></div>

<h2>Coinsurance and valuation</h2>
<p>Many commercial policies have a coinsurance clause. If the building was insured for less than the required percentage of its value, the payment can be reduced. Appraisal sets the amount of loss, but valuation questions like this may come up alongside it, and they can affect the final check. Some coinsurance and valuation disputes cross into coverage, which is a question for a Missouri attorney.</p>
<div class="note"><p>Illustrative example only: a 40-unit HOA might see a carrier estimate covering roof repairs on six buildings while contractors bid full replacement on all of them. Appraisal lets both sides put documented scope in front of a neutral panel.</p></div>

<h2>Getting started</h2>
<p>Send us the policy, the carrier’s estimate and any engineer or roofing consultant reports. We’ll review the scope at no charge and tell you whether appraisal looks like a fit. Start on the <a href="/get-in-touch/">contact page</a>, or see the <a href="/appraisal-roadmap/">appraisal roadmap</a> for the full sequence.</p>""",
        "faqs": [
            ("Can an HOA board invoke appraisal without a vote of all owners?", "That depends on the association’s governing documents. Many boards have authority to manage insurance claims, but check the bylaws and ask the association’s attorney if it’s unclear."),
            ("Does appraisal work on business income claims?", "It can, when the dispute is about the amount of lost income or extra expense rather than whether coverage applies. These claims usually need financial records and an accountant’s input."),
            ("What if the carrier only inspected a few buildings?", "We document each building separately. Sampling can miss damage, and the appraisal panel can consider building-by-building evidence."),
        ],
    },
    # 4 ------------------------------------------------------------------
    {
        "slug": "hail-roof-damage-appraisal",
        "name": "Hail & Roof Damage Appraisal",
        "kw": "hail damage appraisal Missouri",
        "short": "Appraisal for hail-damaged roofs, siding, gutters and metal when the carrier’s scope comes up short.",
        "h1": "Hail Damage Appraisal in Missouri for Roofs, Siding & Metal",
        "lede": "Missouri gets hit by hail almost every spring, and roof claims are where most scope disputes start. We document the damage shingle by shingle and argue the full amount of loss.",
        "facts": [
            ("Peak season", "March through June"),
            ("Key issues", "Matching, soft metals"),
            ("Watch for", "Cosmetic damage clauses"),
        ],
        "title": "Hail Damage Appraisal in Missouri | Roof & Siding Claims",
        "desc": "Hail damage appraisal in Missouri for roof, siding and gutter claims. We address matching, discontinued shingles and cosmetic damage wording.",
        "body": """<p>Missouri is one of the busier hail states in the country. Storms build along the I-70 and I-44 corridors every spring, and a single afternoon cell can mark thousands of roofs from Columbia to the St. Louis suburbs. The April 10, 2001 hailstorm along the I-70 corridor in the St. Louis area was one of the costliest hail events of its time, and big hail days have kept coming since. When the claim comes back as “a few shingles and a gutter,” appraisal is often how homeowners and building owners get the full roof looked at fairly.</p>

<h2>What a hail roof dispute usually looks like</h2>
<p>The insurer agrees hail hit the property. The disagreement is how much damage there is and what fixing it requires.</p>
<ul>
<li><strong>Repair vs. replace.</strong> The adjuster counts hits on a test square and decides the slope can be patched. Your roofer says the shingles are brittle and can’t be repaired without breaking more.</li>
<li><strong>Discontinued shingles.</strong> If your shingle line is no longer made, a repair may leave a visible patch. How that’s handled depends on your policy and the facts.</li>
<li><strong>Matching.</strong> Some policies address matching directly; some limit it; some are silent. The wording controls.</li>
<li><strong>Soft metals.</strong> Dents in gutters, downspouts, vents, flashing and AC fins are evidence of hail size and direction, and they’re often damaged in their own right.</li>
</ul>

<h2>Functional vs. cosmetic damage</h2>
<p>A growing number of policies sold in Missouri include a cosmetic damage exclusion or limitation, most often for metal roofs and siding. Under that language, dents that don’t affect the roof’s ability to shed water may not be covered. Whether a given dent is “cosmetic” or “functional” is often argued hard.</p>
<h3>What appraisal can address</h3>
<p>If coverage is accepted and the fight is about how many panels or squares need replacing, that’s generally an amount-of-loss question. Appraisers measure, count and price.</p>
<h3>What appraisal can’t address</h3>
<p>If the carrier says all of the damage is cosmetic and excluded, that’s a coverage position. An appraiser doesn’t decide coverage. A Missouri attorney can advise on that.</p>

<h2>How we document a hail loss</h2>
<ol>
<li>Confirm the storm date with weather data and match it to your notice date.</li>
<li>Inspect every slope, marking and photographing hits on shingles, ridge caps and vents.</li>
<li>Check soft metals, window wraps, siding, screens and outdoor units on all sides.</li>
<li>Identify the shingle manufacturer and line, and check whether it’s still available.</li>
<li>Write a full estimate including tear-off, underlayment, drip edge, ice-and-water shield where code calls for it, and code-required items.</li>
</ol>

<div class="table-wrap"><table>
<thead><tr><th>Component</th><th>Common carrier position</th><th>What we check</th></tr></thead>
<tbody>
<tr><td>Shingles</td><td>Spot repair</td><td>Hit count, brittleness, availability</td></tr>
<tr><td>Metal roof</td><td>Cosmetic only</td><td>Seams, fasteners, policy wording</td></tr>
<tr><td>Gutters</td><td>Not damaged</td><td>Dent pattern, sizing, matching</td></tr>
<tr><td>Siding</td><td>Replace one wall</td><td>Profile availability, color match</td></tr>
</tbody></table></div>

<h2>Timing matters with hail</h2>
<p>Hail damage isn’t always visible from the ground, and many people don’t learn about it until a roofer knocks on the door weeks later. Most policies require prompt notice, and some have shorter windows for wind and hail claims. Report it, get it inspected, and keep records of the storm date. Our <a href="/toolkit/">toolkit</a> has a storm-date checklist.</p>
<div class="note"><p>Be careful with door-knockers after a hail storm. A legitimate roofer won’t pressure you to sign on the spot. Appraisal is a separate process from choosing a contractor, and we don’t sell roofs.</p></div>

<h2>After the award</h2>
<p>The appraisal award sets the amount of loss. Depreciation holdback and deductibles still apply according to your policy, and many carriers release recoverable depreciation once you show the work is done. If you’re also facing interior water stains from a damaged roof, see <a href="/appraisal-help/burst-pipe-water-damage-appraisal/">water damage appraisal</a> for how those claims are handled.</p>""",
        "faqs": [
            ("Will the appraisal panel order a full roof replacement?", "The panel sets the dollar amount of loss, not a construction order. If the evidence shows the roof can’t be properly repaired, the award can reflect a replacement cost, but nothing is guaranteed."),
            ("My metal roof has dents but doesn’t leak. Is that covered?", "It depends on your policy. Some Missouri policies exclude or limit cosmetic damage to metal; others don’t. Coverage is a question for the policy wording and, if disputed, a Missouri attorney."),
            ("How long after a hail storm can I file a claim?", "Policies vary, and some set specific windows for wind and hail claims. Read your policy and report the damage as soon as you know about it."),
            ("Do dented gutters prove hail damage to my roof?", "Not by themselves, but they’re useful evidence of hail size and direction. Appraisers look at soft metals alongside the roof covering itself."),
        ],
    },
    # 5 ------------------------------------------------------------------
    {
        "slug": "tornado-straight-line-wind-appraisal",
        "name": "Tornado & Derecho Wind Appraisal",
        "kw": "tornado damage appraisal Missouri",
        "short": "Appraisal for tornado, derecho and straight-line wind losses, from torn shingles to total losses.",
        "h1": "Tornado Damage Appraisal in Missouri, Including Derecho Winds",
        "lede": "Wind claims range from a few missing shingles to a slab where a house used to be. We help Missouri owners settle the amount of loss when the carrier’s number misses the real cost to rebuild.",
        "facts": [
            ("Perils", "Tornado, derecho, wind"),
            ("Big issues", "Code upgrades, total loss"),
            ("Also check", "Debris and ALE limits"),
        ],
        "title": "Tornado Damage Appraisal Missouri | Wind & Derecho Claims",
        "desc": "Tornado and derecho wind damage appraisal across Missouri, covering partial losses, total losses, debris removal and ordinance-or-law code upgrades.",
        "body": """<p>Missouri knows wind. The May 22, 2011 Joplin EF5 tornado was one of the deadliest and most destructive in modern U.S. history. A month earlier, the April 22, 2011 Good Friday tornado tore through north St. Louis County and struck Lambert airport. The May 22, 2019 Jefferson City EF3 tornado hit the capital overnight, and the December 10, 2021 outbreak brought a tornado through St. Charles County near Defiance. Add the summer derechos and straight-line wind storms, like the July 2006 storms that left much of the St. Louis area without power, and wind claims become a regular part of life here.</p>

<h2>Partial wind losses</h2>
<p>Most wind claims aren’t total losses. They’re missing shingles, lifted ridge caps, torn siding, broken windows, damaged fences and a tree on the garage. Disputes usually come down to scope:</p>
<ul>
<li>Whether a roof with scattered creased and missing shingles can be repaired or needs a slope or full replacement.</li>
<li>Whether siding can be patched with matching material or needs a full elevation.</li>
<li>Whether interior damage from rain getting in through wind openings is fully included.</li>
<li>Whether tree removal and debris haul-off are priced correctly and within policy limits.</li>
</ul>

<h2>Total and near-total losses</h2>
<h3>Rebuild cost vs. policy limits</h3>
<p>When a home is destroyed, the question becomes what it costs to rebuild a comparable house today. After a large event, labor and materials can spike as every contractor in the region gets booked. An estimate written from a pricing database the week after the storm may not reflect what rebuilding actually costs months later.</p>
<h3>Ordinance or law</h3>
<p>Rebuilding means meeting the current building code. That can add costs for things like updated electrical service, egress windows, energy code insulation or foundation requirements. Many policies cover those costs only up to an ordinance-or-law limit, often a percentage of the dwelling limit. The limit is a coverage term; the cost of complying is something appraisal can help value.</p>
<h3>Debris removal and demolition</h3>
<p>Clearing a site after a tornado isn’t cheap. Policies usually treat debris removal as part of the dwelling limit with some additional amount on top. Read that section carefully.</p>

<h2>Wind vs. other causes</h2>
<p>Carriers sometimes attribute roof or siding damage to age, installation defects or wear rather than wind. When causation is the core of the dispute, appraisal may not resolve it, because appraisers don’t decide coverage. When the carrier accepts wind damage but disputes how much, appraisal fits well. If a tornado brought heavy rain with it, keep in mind that flood and surface water are usually excluded from homeowners policies and need separate flood insurance.</p>

<div class="note"><p>For example, an illustrative total-loss claim might show a carrier rebuild figure of $260,000 while local builders quote $340,000 for a comparable home under current code. Appraisal looks at documented rebuild costs; it doesn’t raise your policy limits.</p></div>

<h2>Living expenses while you rebuild</h2>
<p>Additional living expense (ALE) or loss of use pays for temporary housing and the extra costs of being displaced. After a big tornado, rental housing gets scarce fast. ALE disputes can sometimes be part of an appraisal when the question is the amount rather than coverage. Keep every receipt.</p>

<h2>What to do in the first weeks</h2>
<ol>
<li>Make the property safe and prevent further damage; keep receipts for tarps and board-up.</li>
<li>Photograph everything before cleanup, including debris piles and contents.</li>
<li>Get a certified copy of your policy and note your dwelling, other structures, contents, ALE and ordinance-or-law limits.</li>
<li>Get the carrier’s estimate in writing and compare it to local contractor bids.</li>
</ol>
<p>Our <a href="/appraisal-roadmap/">appraisal roadmap</a> explains what happens after a demand. For a line-by-line look at the carrier’s numbers first, see <a href="/appraisal-help/insurer-estimate-review/">insurer estimate review</a>.</p>""",
        "faqs": [
            ("Is a derecho covered the same as a tornado?", "Generally both fall under windstorm coverage in most homeowners and commercial policies. Your policy may have a separate wind or hail deductible, so check the declarations page."),
            ("Can appraisal increase my policy limits?", "No. Appraisal sets the amount of loss. Payment is still capped by your policy limits, including any ordinance-or-law and debris removal limits."),
            ("What if the insurer says the damage is old wear rather than wind?", "That’s a causation dispute, and appraisers don’t decide coverage. Depending on the policy wording, a Missouri attorney may need to weigh in before appraisal makes sense."),
        ],
    },
    # 6 ------------------------------------------------------------------
    {
        "slug": "burst-pipe-water-damage-appraisal",
        "name": "Burst Pipe & Water Damage Appraisal",
        "kw": "water damage claim appraisal Missouri",
        "short": "Appraisal for burst pipes and sudden water losses when drying, tear-out or rebuild is underpaid.",
        "h1": "Water Damage Claim Appraisal in Missouri for Burst Pipes",
        "lede": "A burst pipe can soak floors, walls and cabinets in minutes. When the carrier accepts the claim but underpays the drying, tear-out or rebuild, we help settle the full amount of loss.",
        "facts": [
            ("Covered type", "Sudden and accidental"),
            ("Excluded", "Flood, surface water"),
            ("Often separate", "Sewer and drain backup"),
        ],
        "title": "Water Damage Claim Appraisal in Missouri | Burst Pipes",
        "desc": "Water damage claim appraisal in Missouri for burst pipes and sudden leaks, covering drying, tear-out, cabinets, flooring and policy mold limits.",
        "body": """<p>Water claims are among the most common property claims in Missouri, and they can be some of the most frustrating. A supply line lets go under the kitchen sink, a water heater fails in the basement, or a pipe freezes in an exterior wall during a January cold snap. The carrier agrees it’s covered, but the estimate dries two rooms, replaces a strip of flooring and calls it done. Meanwhile the cabinets are swelling and the flooring runs continuous through half the house.</p>

<h2>What’s usually covered and what usually isn’t</h2>
<p>Most Missouri homeowners policies cover sudden and accidental discharge of water from plumbing, heating or appliance systems. That’s the core of a burst-pipe claim. Several related situations are handled very differently:</p>
<ul>
<li><strong>Flood and surface water:</strong> usually excluded. Rising water from rivers, creeks or heavy rain running across the ground needs separate flood insurance. Missouri learned that the hard way in the Great Flood of 1993 and again in the 2019 Missouri River flooding.</li>
<li><strong>Sewer and drain backup:</strong> often excluded unless you bought a specific water backup endorsement, which commonly carries its own lower limit.</li>
<li><strong>Long-term leaks:</strong> slow seepage over weeks or months is often excluded as continuous or repeated leakage.</li>
<li><strong>Mold:</strong> many policies cap mold remediation at a set dollar amount, even when the underlying water loss is covered.</li>
</ul>
<p>These are coverage terms. Appraisal doesn’t change them. It values the covered loss once coverage is accepted.</p>

<h2>Where water estimates fall short</h2>
<h3>Drying and mitigation</h3>
<p>Proper drying follows industry standards for water category and class, moisture readings and equipment days. Carriers sometimes cut equipment counts or days. Moisture logs from the mitigation company are the best evidence here.</p>
<h3>Tear-out and rebuild</h3>
<p>Wet drywall usually needs cutting well above the water line. Insulation behind it is often ruined. Baseboards, door casing and paint follow. Estimates that replace only the visibly stained areas often miss these.</p>
<h3>Continuous flooring</h3>
<p>Hardwood, laminate and luxury vinyl plank often run through several rooms without a break. If the damaged section can’t be matched or isolated, there’s a strong argument to replace the continuous area. Your policy wording governs.</p>
<h3>Cabinets and countertops</h3>
<p>Swollen particleboard cabinets rarely recover. Replacing lower cabinets can mean removing countertops, plumbing and backsplash, all of which belong in the estimate.</p>

<h2>Frozen pipes in Missouri winters</h2>
<p>Missouri isn’t Minnesota, but a hard freeze can split pipes in crawlspaces, exterior walls and unheated garages. Many policies cover freeze damage as long as you took reasonable steps to maintain heat or drain the system, especially in a vacant home. Read that condition carefully if the house was empty. For more on winter claims, see <a href="/appraisal-help/winter-storm-ice-damage-appraisal/">ice storm and freeze damage appraisal</a>.</p>

<div class="table-wrap"><table>
<thead><tr><th>Item</th><th>Carrier shortfall we often see</th></tr></thead>
<tbody>
<tr><td>Drying</td><td>Fewer equipment days than logs show</td></tr>
<tr><td>Drywall</td><td>Cut height too low, no insulation</td></tr>
<tr><td>Flooring</td><td>Partial room, no continuous area</td></tr>
<tr><td>Cabinets</td><td>Doors only, boxes left in place</td></tr>
<tr><td>Contents</td><td>Low values, missed items</td></tr>
</tbody></table></div>

<div class="note"><p>Illustrative example: a carrier estimate of $9,500 for a burst supply line might leave out cabinet replacement and continuous flooring that push a contractor’s bid to $27,000. Appraisal weighs the documented scope; it doesn’t override a mold cap or an excluded peril.</p></div>

<h2>Protect your claim from day one</h2>
<ol>
<li>Shut off the water and call a mitigation company quickly. Policies require you to prevent further damage.</li>
<li>Keep the failed part, whether it’s a supply line, fitting or water heater.</li>
<li>Photograph wet areas and ask for moisture maps and drying logs.</li>
<li>Don’t throw away damaged contents until they’re documented.</li>
</ol>
<p>Questions about the terms on your estimate? Our <a href="/questions-answered/">questions answered</a> page covers the common ones.</p>""",
        "faqs": [
            ("Does homeowners insurance cover a sewer backup in Missouri?", "Often only if you added a water backup endorsement, and that coverage typically has its own limit. Check your declarations page for the endorsement and its limit."),
            ("Will appraisal get my mold cleanup paid in full?", "Appraisal can value the mold work, but the payment is still limited by any mold sublimit in your policy. The cap is a coverage term."),
            ("Is a slow leak under my sink covered?", "Many policies exclude damage from continuous or repeated leakage over time. Whether your loss counts as sudden or long-term is a coverage question that appraisal doesn’t decide."),
        ],
    },
    # 7 ------------------------------------------------------------------
    {
        "slug": "fire-smoke-damage-appraisal",
        "name": "Fire & Smoke Damage Appraisal",
        "kw": "fire damage appraisal Missouri",
        "short": "Appraisal for fire, smoke and soot losses to the structure and contents, including ALE questions.",
        "h1": "Fire Damage Appraisal in Missouri for Structure, Smoke & Contents",
        "lede": "After a fire, the argument is rarely whether there’s a loss. It’s how far the smoke went, what can be cleaned and what has to be replaced. We help Missouri owners settle that number.",
        "facts": [
            ("Main disputes", "Clean vs. replace"),
            ("Also valued", "Contents and ALE"),
            ("Key evidence", "Soot testing, inventories"),
        ],
        "title": "Fire Damage Appraisal in Missouri | Smoke & Soot Claims",
        "desc": "Fire and smoke damage appraisal in Missouri when the insurer’s estimate misses smoke spread, soot cleaning, contents values or the true rebuild cost.",
        "body": """<p>A house fire changes everything in an afternoon. Whether it started in a kitchen in Independence, from an electrical fault in an older St. Louis brick two-family, or from a wood stove in a farmhouse outside Rolla, the claim that follows is one of the most complicated in property insurance. Fire claims involve structural repair, smoke and soot cleaning, contents, and often months of temporary housing. Each piece can be underestimated.</p>

<h2>Structure: what burned and what the smoke touched</h2>
<p>The burned area is easy to see. The harder question is how far heat and smoke damage extends beyond it.</p>
<ul>
<li><strong>Heat damage:</strong> framing, wiring and plumbing near the fire may be compromised even if they look intact.</li>
<li><strong>Smoke migration:</strong> smoke travels through HVAC ducts, wall cavities and attic spaces, depositing residue rooms away from the origin.</li>
<li><strong>Odor:</strong> lingering odor often signals residue in insulation or porous materials that cleaning won’t reach.</li>
<li><strong>Water from firefighting:</strong> thousands of gallons of water can soak floors, drywall and the basement.</li>
</ul>

<h2>Clean or replace?</h2>
<p>This is the heart of most fire appraisals. Carriers frequently estimate cleaning and sealing where owners and contractors believe replacement is needed.</p>
<h3>Hard surfaces</h3>
<p>Non-porous surfaces like sealed countertops, tile and metal fixtures often clean well. Light residue on painted walls may be cleanable followed by sealing and repainting.</p>
<h3>Porous materials</h3>
<p>Carpet, pad, insulation, unsealed wood and upholstered furniture absorb smoke. Cleaning may reduce odor but not eliminate it. Testing for soot and char particles can help show how deep the contamination goes.</p>
<h3>HVAC systems</h3>
<p>Ductwork that carried smoke may need cleaning or replacement. Flexible duct and duct board are hard to clean thoroughly.</p>

<h2>Contents</h2>
<p>A fire contents claim can include thousands of items. Carriers often apply depreciation and pricing that don’t match what replacement costs. Appraisal can cover contents value disputes when coverage isn’t in question.</p>
<ol>
<li>Build a room-by-room inventory with photos, videos and any receipts you can find.</li>
<li>Look for replacement prices for comparable items, not bargain-bin substitutes.</li>
<li>Separate items that can be cleaned from items that can’t.</li>
<li>Watch the special limits on jewelry, firearms, collectibles and cash.</li>
</ol>

<div class="table-wrap"><table>
<thead><tr><th>Area</th><th>Carrier tendency</th><th>What we document</th></tr></thead>
<tbody>
<tr><td>Walls and ceilings</td><td>Clean and seal</td><td>Residue depth, odor, test results</td></tr>
<tr><td>Framing</td><td>Leave in place</td><td>Char depth, heat exposure</td></tr>
<tr><td>Ductwork</td><td>Clean only</td><td>Duct type, contamination</td></tr>
<tr><td>Contents</td><td>Heavy depreciation</td><td>Inventory, comparable pricing</td></tr>
</tbody></table></div>

<h2>Additional living expense</h2>
<p>ALE, also called loss of use, covers the extra cost of living elsewhere while your home is repaired. That can mean rent, utilities at the temporary place, added mileage and meals above your normal cost. ALE is usually limited by time, dollar amount or both. A slow rebuild can push you toward the limit, which is one reason prompt resolution of the amount of loss matters. Keep every receipt and a simple log.</p>
<div class="note"><p>Illustrative example only: a kitchen fire estimate might clean every room outside the kitchen while soot testing shows residue throughout the attic insulation and ductwork. The appraisal panel can weigh that evidence when it sets the amount of loss.</p></div>

<h2>Practical notes for Missouri fire claims</h2>
<p>If the fire department, insurer or a private investigator is looking into cause and origin, let that run its course. Appraisal isn’t meant to resolve questions about how the fire started or whether the claim is covered. Once the carrier accepts the loss and the dispute is about scope and price, appraisal is often a good fit. Ordinance-or-law coverage may matter if rebuilding triggers current code requirements, especially in older homes. For more on that, see <a href="/appraisal-help/tornado-straight-line-wind-appraisal/">tornado and wind appraisal</a>, where code upgrades come up constantly.</p>
<p>Have the carrier’s estimate in hand? Start with an <a href="/appraisal-help/insurer-estimate-review/">insurer estimate review</a> before deciding on appraisal.</p>""",
        "faqs": [
            ("Can appraisal decide whether smoke-damaged items need replacing?", "Yes, when coverage is accepted, the appraisal panel can decide the amount of loss, including whether the evidence supports cleaning or replacement costs."),
            ("Is additional living expense part of an appraisal?", "It can be when the dispute is about the amount owed rather than whether ALE coverage applies. Your policy’s ALE limits still cap the payment."),
            ("Should I throw out smoke-damaged belongings?", "Not until they’ve been documented and, ideally, inspected by the adjuster. Photograph everything and keep a written inventory first."),
        ],
    },
    # 8 ------------------------------------------------------------------
    {
        "slug": "sinkhole-ground-collapse-appraisal",
        "name": "Sinkhole & Ground Collapse Appraisal",
        "kw": "sinkhole claim appraisal Missouri",
        "short": "Appraisal for accepted sinkhole and collapse claims in Missouri’s karst country, valued carefully.",
        "h1": "Sinkhole Claim Appraisal in Missouri’s Karst Country",
        "lede": "Missouri’s limestone bedrock dissolves slowly, and sometimes the ground gives way. When a sinkhole or collapse claim is accepted but the repair figure is disputed, we help value the loss.",
        "facts": [
            ("Hot spots", "Ozarks, Greene County"),
            ("Coverage key", "Collapse wording, riders"),
            ("Also note", "Earthquake is separate"),
        ],
        "title": "Sinkhole Claim Appraisal in Missouri | Karst & Collapse",
        "desc": "Sinkhole claim appraisal in Missouri’s karst areas. Once coverage is accepted, we help value foundation, structural and repair costs for the loss.",
        "body": """<p>Much of Missouri sits on limestone and dolomite that slowly dissolve as groundwater moves through them. Geologists call that karst. It’s why the state is known for caves and springs, and it’s why Missouri has thousands of mapped sinkholes. The Missouri Geological Survey, part of the Missouri Department of Natural Resources, maps known sinkholes across the state. They’re most common in the Ozarks and southern Missouri, around Springfield and Greene County, and in parts of eastern Missouri, including limestone areas of the St. Louis metro.</p>

<h2>Coverage comes first, and it’s often the hard part</h2>
<p>This is the most important point on this page. Most standard homeowners policies <strong>exclude earth movement</strong>, and that exclusion is commonly written broadly enough to include sinkholes, settling and subsidence. Whether a sinkhole loss is covered often depends on:</p>
<ul>
<li>Specific collapse coverage in the policy and how it’s worded.</li>
<li>Any endorsement you added for sinkhole or ground collapse.</li>
<li>How the policy defines collapse and what causes it lists.</li>
<li>Whether the damage is ongoing settling or a sudden event.</li>
</ul>
<p>An appraiser doesn’t decide any of that. Appraisal values the <strong>amount of loss once coverage is accepted</strong>. If the carrier has denied the claim based on an earth movement exclusion, that’s a coverage dispute for a Missouri attorney, not an appraisal question.</p>

<h2>When appraisal does fit a sinkhole claim</h2>
<p>Sometimes the insurer accepts that a covered collapse or sinkhole event occurred, under a collapse provision or endorsement, and then offers a repair figure the owner can’t make work. That’s where appraisal can help.</p>
<h3>Foundation and ground stabilization</h3>
<p>Repairs can range from compaction grouting or underpinning to piers and slab replacement. An engineer’s report usually drives the scope. Appraisers compare competing repair methods and their costs, while staying within whatever the policy and endorsement actually cover.</p>
<h3>Structural and finish damage</h3>
<p>Cracked walls, racked door frames, separated brick veneer, broken plumbing and uneven floors all follow foundation movement. These finish repairs often add up to more than people expect.</p>
<h3>Endorsement limits</h3>
<p>Sinkhole or collapse endorsements may carry their own limits or deductibles. The award values the loss; the endorsement terms decide what’s paid.</p>

<div class="table-wrap"><table>
<thead><tr><th>Question</th><th>Who decides</th></tr></thead>
<tbody>
<tr><td>Is earth movement excluded?</td><td>Policy wording; attorney if disputed</td></tr>
<tr><td>Did a covered collapse occur?</td><td>Carrier; courts if disputed</td></tr>
<tr><td>What causes the damage?</td><td>Engineers, carrier, courts</td></tr>
<tr><td>How much does repair cost?</td><td>Appraisal panel, once covered</td></tr>
</tbody></table></div>

<h2>Practical steps if the ground opens up</h2>
<ol>
<li>Keep people away and call local authorities if the hole is near a structure, road or utility line.</li>
<li>Report it to your insurer promptly and in writing.</li>
<li>Photograph the hole, cracks and any changes over days or weeks.</li>
<li>Check the Missouri Geological Survey’s sinkhole information for your area.</li>
<li>Get a structural or geotechnical engineer involved early; their report will shape everything.</li>
</ol>
<div class="note"><p>Not every crack or sunken patch is a sinkhole. Settling from poor compaction, drought-shrunk clay soils or leaking pipes can look similar. Cause matters for coverage, and appraisers don’t decide cause or coverage.</p></div>

<h2>Earthquake is a different policy question</h2>
<p>Southeast Missouri sits in the New Madrid seismic zone, and earthquake damage is generally excluded from standard homeowners policies. Earthquake coverage is usually a separate endorsement you have to choose and pay for, and it often comes with a percentage deductible. If you live in the Bootheel, Cape Girardeau or the St. Louis region and haven’t looked at this, it’s worth a call to your agent. Sinkhole and earthquake damage are separate perils, and one doesn’t stand in for the other.</p>
<p>For definitions of collapse, subsidence and related terms, see our <a href="/appraisal-dictionary/">appraisal dictionary</a>. Unsure whether your claim is at the appraisal stage? <a href="/get-in-touch/">Reach out</a> and we’ll tell you honestly.</p>""",
        "faqs": [
            ("Does Missouri homeowners insurance cover sinkholes?", "Usually not under a standard policy, because most exclude earth movement. Coverage may exist through specific collapse wording or an endorsement, so read your policy and ask your agent."),
            ("Can an appraiser decide whether my sinkhole damage is covered?", "No. Appraisal only sets the amount of loss once coverage is accepted. Coverage and causation disputes belong with your insurer and, if needed, a Missouri attorney."),
            ("Where can I check whether sinkholes are mapped near my home?", "The Missouri Geological Survey, part of the Missouri Department of Natural Resources, maintains sinkhole mapping for the state."),
            ("Is earthquake damage covered with sinkhole coverage?", "No. Earthquake coverage is usually a separate endorsement you have to choose, and it’s distinct from any sinkhole or collapse coverage."),
        ],
    },
    # 9 ------------------------------------------------------------------
    {
        "slug": "winter-storm-ice-damage-appraisal",
        "name": "Ice Storm & Freeze Damage Appraisal",
        "kw": "ice storm damage appraisal Missouri",
        "short": "Appraisal for ice storm, ice dam, fallen limb and frozen pipe claims across Missouri.",
        "h1": "Ice Storm Damage Appraisal in Missouri for Roofs, Trees & Pipes",
        "lede": "Missouri ice storms snap limbs, crush gutters and freeze pipes in a single night. When the carrier accepts the loss but underpays it, we help put a fair number on the damage.",
        "facts": [
            ("Common damage", "Limbs, gutters, ice dams"),
            ("Season", "December through March"),
            ("Watch for", "Tree removal limits"),
        ],
        "title": "Ice Storm Damage Appraisal Missouri | Freeze & Ice Dams",
        "desc": "Ice storm damage appraisal in Missouri for fallen limbs, crushed gutters, ice dams and frozen pipes when the insurer’s estimate leaves out repairs.",
        "body": """<p>Missouri winters swing hard. A week of mild weather can turn into freezing rain overnight, coating every branch and power line in ice. The January 2007 ice storm in southwest Missouri left Springfield and surrounding counties with widespread tree damage and long power outages. Storms like that leave behind a particular set of claims: limbs through roofs, collapsed gutters, ice dams leaking into ceilings and pipes that froze when the heat went out.</p>

<h2>Typical ice storm and freeze claims</h2>
<ul>
<li><strong>Falling limbs and trees:</strong> roof punctures, crushed decking, broken trusses, damaged siding and fences.</li>
<li><strong>Gutters and downspouts:</strong> torn off or bent under ice weight, often taking fascia and soffit with them.</li>
<li><strong>Ice dams:</strong> meltwater backing up under shingles at the eaves and leaking into attics, walls and ceilings.</li>
<li><strong>Frozen pipes:</strong> splits in supply lines during extended outages, often discovered when the thaw comes.</li>
<li><strong>Weight of ice:</strong> sagging or collapsed carports, porch roofs and outbuildings.</li>
</ul>

<h2>Where these estimates come up short</h2>
<h3>Roof damage under the limb</h3>
<p>A limb through a roof is obvious. What’s less obvious is cracked decking and damaged trusses around the impact, or shingles broken when crews removed the limb. A proper scope looks at the whole area, often from the attic too.</p>
<h3>Tree removal limits</h3>
<p>Policies usually pay to remove a tree that fell on a covered structure, often with a per-tree and per-event cap. Trees that fell in the yard without hitting anything may not be covered at all. These limits are coverage terms; appraisal values the work within them.</p>
<h3>Ice dam interior damage</h3>
<p>Ice dam claims often involve stained ceilings, wet insulation and damp wall cavities. Carriers sometimes pay to paint over a stain without addressing wet insulation or drywall. Some policies treat ice dam leakage differently from other water damage, so read the wording.</p>
<h3>Gutters and matching</h3>
<p>Replacing one run of seamless gutter in a color that’s no longer made can leave the house mismatched. How matching is handled depends on your policy.</p>

<div class="table-wrap"><table>
<thead><tr><th>Damage</th><th>Common carrier scope</th><th>What may be missing</th></tr></thead>
<tbody>
<tr><td>Limb on roof</td><td>Patch shingles</td><td>Decking, trusses, gutters</td></tr>
<tr><td>Ice dam leak</td><td>Paint ceiling</td><td>Insulation, drywall, drying</td></tr>
<tr><td>Frozen pipe</td><td>Pipe repair only</td><td>Access, tear-out, flooring</td></tr>
<tr><td>Gutters</td><td>Single run</td><td>Fascia, matching runs</td></tr>
</tbody></table></div>

<h2>Frozen pipes and the heat requirement</h2>
<p>Most policies cover freeze damage if you used reasonable care to maintain heat or shut off and drain the water. During a regional power outage, that care may look different, and the facts matter. Vacant homes are a frequent sticking point. Once coverage is accepted, the tear-out, drying and rebuild are standard appraisal territory. For more on water losses, see <a href="/appraisal-help/burst-pipe-water-damage-appraisal/">burst pipe and water damage appraisal</a>.</p>

<div class="note"><p>Illustrative example: a carrier might pay $3,200 to patch a roof and remove a limb, while an inspection finds cracked decking, a broken truss and wet attic insulation that bring the repair closer to $11,000. Appraisal weighs documented scope, not guesses.</p></div>

<h2>What to do after an ice storm</h2>
<ol>
<li>Stay clear of downed power lines and report them to the utility.</li>
<li>Photograph limbs on structures before removal, and keep tree service invoices.</li>
<li>Tarp roof openings and keep receipts; preventing further damage is your duty under the policy.</li>
<li>If the power is out for days, take steps to protect plumbing, and document what you did.</li>
<li>Check the attic for wet insulation once things thaw.</li>
</ol>
<p>Winter storm damage sometimes doesn’t show until spring. If you find late leaks, report them promptly and note when you first noticed. Our <a href="/toolkit/">claim toolkit</a> includes a winter damage checklist.</p>""",
        "faqs": [
            ("Does insurance pay to remove a tree that fell in my yard but didn’t hit anything?", "Often not, or only in limited situations. Many policies pay for tree removal only when the tree damages a covered structure, usually with a per-tree cap."),
            ("Are ice dam leaks covered by homeowners insurance?", "Many Missouri policies cover interior damage from ice dams, but wording varies. Check the policy’s water damage and ice dam language before assuming either way."),
            ("My pipes froze during a power outage. Is that covered?", "Freeze damage is commonly covered if you took reasonable steps to maintain heat or drain the system. Whether those steps were reasonable during an outage is a fact question for the carrier and, if disputed, an attorney."),
        ],
    },
    # 10 -----------------------------------------------------------------
    {
        "slug": "insurer-estimate-review",
        "name": "Insurer Estimate Review",
        "kw": "insurance estimate review Missouri",
        "short": "A line-by-line review of the carrier’s Xactimate or Symbility estimate before you decide next steps.",
        "h1": "Insurance Estimate Review for Missouri Property Owners",
        "lede": "Before you invoke appraisal, it pays to know exactly where the carrier’s estimate falls short. We read it line by line and show you what’s missing, mispriced or misapplied.",
        "facts": [
            ("Formats", "Xactimate, Symbility"),
            ("We check", "Scope, pricing, O&P, code"),
            ("Deliverable", "Written comparison"),
        ],
        "title": "Insurance Estimate Review Missouri | Line-by-Line Check",
        "desc": "Insurance estimate review for Missouri property owners. We check the carrier’s Xactimate or Symbility estimate for missing items, pricing and O&P.",
        "body": """<p>Insurance estimates look official. Pages of line items, unit costs, quantities and codes make it hard to argue with them. But an estimate is only as good as the inspection and assumptions behind it. A line-by-line review tells you, in plain language, whether the carrier’s number holds up and where it doesn’t. For many Missouri property owners, it’s the right first step before deciding whether appraisal is worth it.</p>

<h2>What we review</h2>
<p>Most carriers write estimates in Xactimate or Symbility, two of the most widely used estimating platforms. Both price items using regional pricing databases. We read the estimate the way an appraiser would.</p>
<h3>Scope: what’s included</h3>
<ul>
<li>Every damaged room, elevation and roof slope accounted for.</li>
<li>Removal and replacement of adjacent materials needed to complete repairs.</li>
<li>Prep items like floor protection, content manipulation and cleanup.</li>
<li>Permits, dumpster fees and temporary repairs already performed.</li>
</ul>
<h3>Quantities</h3>
<p>Wrong measurements are common. A roof measured short by a few squares, a wall height that ignores a vaulted ceiling, or a room left off altogether can add up quickly.</p>
<h3>Pricing</h3>
<p>Database pricing may not match what Missouri contractors charge, especially after a big storm when labor is scarce. We compare unit prices to the local market and to the price list date used in the estimate.</p>
<h3>Overhead and profit</h3>
<p>General contractor overhead and profit (O&amp;P) is commonly included when a job needs coordination across multiple trades. Carriers sometimes omit it. Whether it belongs depends on the complexity of the job and the policy.</p>
<h3>Code items</h3>
<p>Repairs may need to meet the current local building code, such as drip edge, ice-and-water shield, upgraded electrical or egress requirements. Whether those are paid often depends on an ordinance-or-law coverage limit.</p>

<h2>What you get from a review</h2>
<ol>
<li>A plain-language summary of where the estimate falls short.</li>
<li>A list of missing line items and incorrect quantities.</li>
<li>Pricing comparisons for the biggest-ticket items.</li>
<li>An honest opinion on whether the dispute looks like an amount-of-loss issue suited to appraisal, or something else.</li>
</ol>

<div class="table-wrap"><table>
<thead><tr><th>Category</th><th>Common problem</th></tr></thead>
<tbody>
<tr><td>Scope</td><td>Missing rooms, trades or adjacent work</td></tr>
<tr><td>Quantities</td><td>Short measurements, wrong pitch</td></tr>
<tr><td>Pricing</td><td>Outdated price list or wrong region</td></tr>
<tr><td>O&amp;P</td><td>Omitted on a multi-trade job</td></tr>
<tr><td>Depreciation</td><td>Applied to labor or too heavily</td></tr>
</tbody></table></div>

<h2>Depreciation: read it carefully</h2>
<p>On replacement cost policies, carriers often withhold depreciation until repairs are completed. On actual cash value policies, depreciation is a permanent reduction. How depreciation is calculated, and whether it’s applied to labor, can make a real difference. We flag depreciation that looks excessive or inconsistent so you can ask the right questions. Some depreciation questions are legal ones; for those, talk to a Missouri attorney.</p>

<div class="note"><p>For example, an illustrative review might find a roof estimate missing starter course, drip edge and two squares of measurement, plus O&amp;P left off a multi-trade job. Small items like these can add up to thousands of dollars on a single claim.</p></div>

<h2>What happens next</h2>
<p>Sometimes the review shows the carrier’s estimate is fair, and we’ll tell you that. Other times you can send our findings to the adjuster and get a supplement without formal appraisal. When the gap is large and the carrier won’t move, the review becomes the foundation for an <a href="/appraisal-help/appraisal-demand-representation/">appraisal demand</a>. If you have questions about claim handling, the Missouri Department of Commerce and Insurance accepts consumer complaints, and its website explains how to file one. Common estimate terms are explained on our <a href="/questions-answered/">questions answered</a> page.</p>""",
        "faqs": [
            ("Do I need an estimate review before demanding appraisal?", "It isn’t required, but it’s smart. A review shows whether the dispute is about the amount of loss and gives you a clear picture of what you’d be arguing for."),
            ("Can a review get my claim reopened without appraisal?", "Sometimes. Many carriers will consider a documented supplement request. If they won’t, the review can support an appraisal demand."),
            ("What do I need to send for a review?", "The carrier’s full estimate, not just the summary page, plus your policy declarations, photos and any contractor bids you’ve received."),
        ],
    },
    # 11 -----------------------------------------------------------------
    {
        "slug": "appraisal-umpire-services",
        "name": "Appraisal Umpire Services",
        "kw": "appraisal umpire Missouri",
        "short": "Neutral umpire services for Missouri property appraisals when the two appraisers can’t agree.",
        "h1": "Appraisal Umpire Services for Missouri Property Claims",
        "lede": "When the two appraisers can’t agree on the amount of loss, a neutral umpire breaks the tie. We serve as umpire on Missouri residential and commercial appraisals.",
        "facts": [
            ("Role", "Neutral tiebreaker"),
            ("Chosen by", "Both appraisers"),
            ("Fallback", "Court appointment"),
        ],
        "title": "Appraisal Umpire in Missouri | Neutral Tiebreaker Service",
        "desc": "Neutral appraisal umpire services for Missouri property claims. We help resolve disputed items when the two appraisers can’t agree on the loss amount.",
        "body": """<p>Every appraisal clause has a built-in way to break a deadlock. Each side picks an appraiser, and the two appraisers choose a neutral umpire. If the appraisers agree on the amount of loss, the umpire may never be needed. If they don’t, the umpire reviews the disputed items, and an award signed by any two of the three sets the amount. We serve as umpire on Missouri property appraisals, and when we do, we work for neither side.</p>

<h2>What an umpire does</h2>
<p>An umpire’s job is narrow and important: resolve the specific items the appraisers couldn’t agree on, based on the evidence.</p>
<ul>
<li>Review both appraisers’ estimates and supporting documents.</li>
<li>Inspect the property, usually with both appraisers present.</li>
<li>Hear each appraiser’s position on the disputed items.</li>
<li>Decide the disputed items and sign an award with at least one appraiser.</li>
</ul>
<p>An umpire doesn’t decide coverage, interpret disputed policy language in a binding way, or rule on legal issues. Those stay with the parties and, if needed, the courts.</p>

<h2>How umpires are chosen</h2>
<h3>Agreement between the appraisers</h3>
<p>Most policies direct the two appraisers to select an umpire within a set period, often 15 days. They typically exchange names, check for conflicts and settle on someone both find acceptable.</p>
<h3>Court appointment</h3>
<p>If the appraisers can’t agree on an umpire within the time the policy allows, most appraisal clauses let either party ask a court to appoint one. In Missouri, that request is generally made to a court in the county where the property is located. The procedure and timing are legal matters, so the party seeking appointment usually works with a Missouri attorney.</p>
<h3>Conflict checks</h3>
<p>Before accepting an umpire role, we check for relationships with either party, either appraiser and the carrier. If there’s a conflict that would undermine neutrality, we decline.</p>

<div class="table-wrap"><table>
<thead><tr><th>Step</th><th>What happens</th></tr></thead>
<tbody>
<tr><td>Appointment</td><td>Selected by appraisers or a court</td></tr>
<tr><td>Disclosure</td><td>Conflicts reviewed and disclosed</td></tr>
<tr><td>Submissions</td><td>Both estimates and evidence received</td></tr>
<tr><td>Inspection</td><td>Property visit with both appraisers</td></tr>
<tr><td>Award</td><td>Disputed items decided, award signed</td></tr>
</tbody></table></div>

<h2>How we handle the umpire role</h2>
<ol>
<li><strong>Clear ground rules.</strong> We confirm the disputed items in writing and how submissions will be shared, so nobody is surprised.</li>
<li><strong>Equal access.</strong> Both appraisers get the same information and the same chance to make their case. We avoid one-sided conversations.</li>
<li><strong>Itemized awards.</strong> Where the panel agrees to it, we prefer awards that break out the amounts by category, which can help the parties apply policy terms afterward.</li>
<li><strong>Plain reasoning.</strong> We explain the basis for decisions on disputed items so the appraisers understand the outcome and the parties can see how the award was reached.</li>
</ol>

<div class="note"><p>Umpire fees are commonly split equally between the insured and the insurer under most appraisal clauses, but your policy controls. We disclose our fee arrangement to both appraisers before accepting the role.</p></div>

<h2>Umpiring in Missouri</h2>
<p>Missouri appraisals cover everything from a hail-damaged ranch house in Lee’s Summit to a tornado-hit warehouse or an apartment complex in Springfield. Disputed items often involve roof scope, matching, code upgrades and pricing in markets stretched thin after a major storm. An umpire who understands both residential and commercial estimating, and how Missouri contractors actually price work, can resolve those items efficiently.</p>
<p>Appraisers looking for an umpire can reach us through the <a href="/get-in-touch/">contact page</a>. Property owners who want to understand the full process can start with the <a href="/appraisal-roadmap/">appraisal roadmap</a>.</p>""",
        "faqs": [
            ("Can the umpire side with my insurer?", "On any disputed item, the umpire decides based on the evidence and may agree with either appraiser. An award needs the signatures of any two of the three panel members."),
            ("What happens if the appraisers can’t agree on an umpire?", "Most appraisal clauses let either side ask a court to appoint one, usually in the county where the property is located. That step usually involves a Missouri attorney."),
            ("Can you serve as umpire if you’ve worked as an appraiser on other claims?", "Yes, as long as there’s no conflict with the parties, the appraisers or the carrier on this claim. We disclose relevant relationships before accepting."),
        ],
    },
]
