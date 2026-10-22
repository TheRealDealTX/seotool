<?php
defined('CCPA_ROOT') || exit;
return [
    'title'       => 'Replacement Cost vs. Actual Cash Value in Texas Property Claims',
    'seo_title'   => 'Replacement Cost vs. Actual Cash Value in Texas Claims',
    'description' => 'Replacement cost vs. actual cash value in Texas: how depreciation, holdback, and roof schedules shape what Corpus Christi owners are paid on a claim.',
    'kicker'      => 'Claim Process',
    'image'       => '/assets/img/featured/replacement-cost-vs-actual-cash-value-texas.webp',
    'image_alt'   => 'Homeowner reviewing an insurance estimate that shows replacement cost, depreciation, and actual cash value columns',
    'date'        => '2026-09-15',
    'updated'     => '2026-10-22',
    'category'    => 'Claim Process',
    'excerpt'     => 'Why your first insurance check is often smaller than the estimate total, how recoverable depreciation works, and what Corpus Christi owners should check before repairs begin.',
    'related'     => [
        '/how-to-review-underpaid-roof-insurance-estimate/',
        '/named-storm-hurricane-deductibles-texas/',
        '/why-property-insurance-claims-are-delayed-texas/',
    ],
    'sources'     => [
        ['Texas Insurance Code Chapter 4102 — Public Adjusters', 'https://tcss.legis.texas.gov/resources/IN/htm/IN.4102.htm'],
        ['Texas Windstorm Insurance Association — Coverage and eligibility', 'https://www.twia.org/coverage-eligibility/'],
        ['City of Corpus Christi — Residential remodels and repairs', 'https://www.corpuschristitx.gov/department-directory/development-services/applications-permits-and-guidance/residential-remodels-and-repairs/'],
    ],
    'faqs' => [
        ['q' => 'Why is my first insurance check less than the estimate total?', 'a' => '<p>Under many replacement cost policies, the insurer first pays the actual cash value: the replacement cost minus depreciation and minus your deductible. The withheld amount, often called recoverable depreciation, may be released after the repairs are completed and documented, subject to the policy’s conditions and time limits.</p>'],
        ['q' => 'How long do I have to recover depreciation in Texas?', 'a' => '<p>There is no single answer for every claim. The deadline is set by the replacement cost provision in your policy, and it varies by insurer and form. Read that section of your policy as soon as you receive the first payment, and if repairs will take longer, ask the insurer in writing how to protect your right to the holdback.</p>'],
        ['q' => 'Can I dispute the amount of depreciation the insurer applied?', 'a' => '<p>Often, yes. Depreciation is an estimate based on age, condition, and expected life, and it can be applied too heavily or to items that should not be depreciated at all. Ask for the depreciation breakdown by line item. If you still disagree on the amount of loss, the policy’s appraisal clause may be available.</p>'],
        ['q' => 'Does a roof payment schedule mean I only get actual cash value for my roof?', 'a' => '<p>Some Texas policies settle roof surfaces on a payment schedule based on roof age rather than full replacement cost. The effect is similar to non-recoverable depreciation: the reduction is not paid back after repairs. Check your declarations page and endorsements to see whether your roof is covered at replacement cost, actual cash value, or a schedule.</p>'],
        ['q' => 'Are building code upgrades included in replacement cost?', 'a' => '<p>Not automatically. Replacement cost generally means like kind and quality. The extra cost to meet current code is usually handled by ordinance or law coverage, which pays up to its own limit. In Corpus Christi, permit and windstorm certification requirements for re-roofing make this coverage worth checking.</p>'],
        ['q' => 'Does it matter whether I hire a contractor before the claim is settled?', 'a' => '<p>It can. Recovering depreciation usually requires proof that the work was done, such as a final invoice and photos. If the contractor’s price is higher than the insurer’s estimate, document why before or during the work, not months later. A public adjuster or estimate review can help you compare the scopes first.</p>'],
    ],
    'body' => <<<'HTML'
<div class="key-takeaways"><h2>Key takeaways</h2><ul>
<li>Actual cash value (ACV) is replacement cost minus depreciation. Replacement cost value (RCV) is what it costs to repair or replace with like kind and quality today.</li>
<li>On many RCV policies, the insurer pays ACV first and holds back recoverable depreciation until repairs are finished and documented.</li>
<li>The deadline to collect that holdback is set by your policy, not by a single Texas rule. Find it early.</li>
<li>Some Texas policies pay roofs on an ACV basis or a roof-age payment schedule, which can sharply reduce a roof claim.</li>
<li>Depreciation is an estimate. It can be questioned line by line, and disputes over the amount may go to appraisal.</li>
</ul></div>

<p>Few things confuse Texas property owners more than <strong>replacement cost vs. actual cash value</strong>. You read an insurance estimate that totals one number, then a check arrives for a noticeably smaller one. Nothing has been denied, yet money seems to be missing. In most cases the gap is depreciation, and how your policy treats depreciation decides whether you ever see that money again.</p>

<p>This guide explains the two valuation methods in plain English, shows how the math works on a typical Corpus Christi storm claim, and lists what to check before you sign a repair contract. It is general information, not legal advice. Your policy language controls, and coverage depends on the facts of your loss.</p>

<h2>Replacement cost vs. actual cash value: the basic definitions</h2>

<p><strong>Replacement cost value (RCV)</strong> is the cost to repair or replace damaged property with materials of like kind and quality at today's prices, without a deduction for age or wear. If a 12-year-old composition shingle roof is destroyed by wind, RCV is roughly what a roofer would charge to tear it off and install a comparable new roof now.</p>

<p><strong>Actual cash value (ACV)</strong> is generally replacement cost minus depreciation. Depreciation reflects the portion of the item's useful life that has already been used up. That same 12-year-old roof might be valued at a fraction of its RCV, depending on how the insurer estimates its life expectancy and condition.</p>

<p>Your declarations page and policy form tell you which method applies to which property. It is common for a single policy to use more than one method: replacement cost for the dwelling, actual cash value for certain contents, and a separate schedule or ACV basis for the roof.</p>

<table>
<thead><tr><th>Feature</th><th>Replacement cost (RCV)</th><th>Actual cash value (ACV)</th></tr></thead>
<tbody>
<tr><td>What it measures</td><td>Cost to repair or replace with like kind and quality today</td><td>Replacement cost minus depreciation</td></tr>
<tr><td>Depreciation</td><td>Withheld at first, often recoverable after repairs</td><td>Deducted and generally not paid back</td></tr>
<tr><td>First payment</td><td>Often ACV minus deductible</td><td>ACV minus deductible</td></tr>
<tr><td>Proof of repair needed?</td><td>Usually, to release the holdback</td><td>Usually not</td></tr>
<tr><td>Premium</td><td>Typically higher</td><td>Typically lower</td></tr>
<tr><td>Who it suits</td><td>Owners who plan to repair or rebuild</td><td>Owners willing to absorb the age-related gap</td></tr>
</tbody>
</table>

<h2>How depreciation works on an insurance estimate</h2>

<p>Most carrier estimates in Texas are written in Xactimate or similar software. Each line item, such as "remove and replace laminated composition shingles" or "drywall, hang, tape, and finish," shows a replacement cost, then a depreciation amount, then an ACV. At the bottom of the estimate you will usually see a summary that looks something like this:</p>

<table>
<thead><tr><th>Estimate summary line</th><th>Illustrative amount</th><th>What it means</th></tr></thead>
<tbody>
<tr><td>Replacement cost value</td><td>$24,000</td><td>Total cost of the repairs at today's prices</td></tr>
<tr><td>Less recoverable depreciation</td><td>($7,000)</td><td>Withheld now; may be paid after repairs</td></tr>
<tr><td>Less non-recoverable depreciation</td><td>($1,500)</td><td>Deducted permanently under the policy terms</td></tr>
<tr><td>Actual cash value</td><td>$15,500</td><td>RCV minus all depreciation</td></tr>
<tr><td>Less deductible</td><td>($4,000)</td><td>Your share of the loss</td></tr>
<tr><td>Net claim (first payment)</td><td>$11,500</td><td>What the first check is based on</td></tr>
</tbody>
</table>

<p><em>The numbers above are a made-up example to show the math, not a typical or expected result.</em> Notice that the owner's first check is less than half of the replacement cost, even though nothing was denied. If repairs are completed on time and the holdback is released, the owner may receive the $7,000 in recoverable depreciation later. The $1,500 in non-recoverable depreciation and the deductible stay with the owner.</p>

<p>You can run your own numbers with our <a href="/claim-calculator/">claim calculator</a>, and if you have a percentage wind or named-storm deductible, the <a href="/hurricane-deductible-calculator/">hurricane deductible calculator</a> shows how that deductible changes the net payment.</p>

<h3>Recoverable vs. non-recoverable depreciation</h3>

<p>Recoverable depreciation is the part an RCV policy promises to pay back once you actually repair or replace the property. Non-recoverable depreciation is not paid back. Some items may be valued at ACV only, either because the policy says so or because an endorsement changed the settlement terms. Ask the adjuster which category each depreciation amount falls into. The estimate summary usually shows both, but they are easy to miss.</p>

<h3>What drives the depreciation number</h3>

<p>Depreciation is not a fixed table that applies the same way to everyone. Adjusters typically consider the item's age, its expected life, and its condition before the loss. Two homes on the same street with roofs installed the same year can be depreciated differently if one roof was well maintained and the other was already failing. That judgment call is where disagreements start.</p>

<p>Common problems we see in depreciation include:</p>
<ul>
<li>Depreciating labor as well as materials, where the policy or practice in that situation does not support it.</li>
<li>Applying an age that is wrong because the adjuster guessed rather than checked a permit, invoice, or closing record.</li>
<li>Depreciating items that were new or nearly new, such as recently replaced flooring or a newer water heater.</li>
<li>Treating salt-air wear on coastal properties as if it erased most of an item's remaining value, without a condition inspection to support it.</li>
</ul>

<p>If you think depreciation is off, ask in writing for the age, life expectancy, and condition assumptions the adjuster used. Proof of age, such as a roofing permit or a receipt, can change the result.</p>

<h2>Collecting recoverable depreciation after repairs</h2>

<p>On an RCV policy, the holdback is usually released when you show the work was done. Insurers often want a final invoice from the contractor, sometimes with photos of the completed work, and they may reinspect. A few practical points help:</p>

<ol>
<li><strong>Find the deadline now.</strong> Your policy sets how long you have to complete repairs and claim replacement cost. The window differs between insurers and forms. Put the date on your calendar the day the first check arrives.</li>
<li><strong>Ask about extensions in writing.</strong> After a hurricane or major hail event, contractors in Corpus Christi, Portland, and Rockport can be booked for months. If repairs will run late, ask the insurer in writing how to preserve the claim.</li>
<li><strong>Match the scope.</strong> If your contractor's invoice covers the same work as the insurer's estimate, release is usually straightforward. If the invoice includes items the carrier did not include, you may need a supplement first.</li>
<li><strong>Keep the mortgage company in the loop.</strong> If your lender is named on the check, it may control how funds are released. Ask the lender's loss draft department about its process early.</li>
</ol>

<p>Whether depreciation is recoverable at all, and how much, depends on your policy. The <a href="/claim-deadline-calculator/">claim deadline calculator</a> can help you track the key dates you already know, but the policy itself is the final word on replacement cost timing.</p>

[[cta]]

<h2>Roofs, payment schedules, and ACV endorsements</h2>

<p>Roof claims are where the replacement cost vs. actual cash value question hits hardest in Texas. Some policies cover the roof at full replacement cost. Others cover roof surfaces at actual cash value, or use a payment schedule that pays a decreasing percentage of the roof's replacement cost as it ages. Under those terms, the reduction is generally not paid back after you replace the roof.</p>

<p>Before a storm, check your declarations page and endorsements for words like "roof surface," "payment schedule," or "actual cash value roof." After a storm, those terms decide the math. A roof claim that looks large on the RCV line can shrink substantially once a schedule or ACV basis is applied. That does not mean the claim is wrong, but it does mean you should understand the numbers before you sign a contract with a roofer. Our <a href="/services/roof-damage-insurance-claims/">roof damage claim service</a> starts with exactly that review.</p>

<h3>Coastal properties with more than one policy</h3>

<p>Many homes and businesses in Nueces, San Patricio, Aransas, and Kleberg counties carry a homeowners or commercial policy that excludes wind and hail, a separate TWIA windstorm policy for wind and hail, and a flood policy. Each policy has its own valuation terms, deductibles, and conditions. A wind-damaged roof may be valued under the TWIA policy while the interior water damage from the same event is handled differently. Read each policy on its own terms. Our page on <a href="/services/twia-windstorm-claims/">TWIA windstorm claims</a> explains how those policies interact.</p>

<h2>Code upgrades and permit costs are a separate question</h2>

<p>Replacement cost usually means like kind and quality, not "whatever the current code requires." In Corpus Christi, that distinction matters. The city has adopted the 2021 International Residential Code with local amendments, effective August 1, 2023, and its local design criteria list a 140/150 mph design wind speed and a windborne debris zone. Re-roofing requires a permit, and the city's roofing submission includes a completed TDI WPI-1 form from the windstorm engineer or inspector responsible for windstorm compliance.</p>

<p>Those requirements can add work and cost that the original roof never had. Whether your insurer pays for them depends largely on <strong>ordinance or law coverage</strong>, which pays up to its own limit for the increased cost of complying with codes. Code requirements by themselves do not create coverage. See our summary of <a href="/local-building-codes/">local building codes</a> for the permit and windstorm details that commonly come up on claims.</p>

<h2>When you disagree with the valuation</h2>

<p>Disagreements over depreciation, roof age, or the price of repairs are disagreements about the <em>amount</em> of loss. That matters because most property policies include an appraisal clause for exactly this kind of dispute. Each side picks an appraiser, the appraisers pick an umpire, and an award agreed to by any two is generally binding on the amount, subject to the policy's wording. Appraisal does not decide whether something is covered.</p>

<p>Before you get there, try these steps:</p>
<ul>
<li>Request the full estimate with line-item depreciation, not just the summary page.</li>
<li>Send proof of age and condition, such as permits, invoices, and dated photos.</li>
<li>Get a detailed contractor estimate written in the same format so the two can be compared line by line.</li>
<li>Put your questions in writing and keep copies of every response.</li>
</ul>

<p>An independent <a href="/services/insurance-estimate-review/">insurance estimate review</a> can show whether the depreciation and the replacement cost lines are reasonable. If the gap is significant, our <a href="/services/underpaid-insurance-claims/">underpaid claim help</a> and <a href="/services/insurance-appraisal/">appraisal support</a> pages describe the next steps.</p>

<h2>How a public adjuster can help</h2>

<p>A licensed public adjuster represents the policyholder, not the insurance company. At Corpus Christi Public Adjuster, that work typically includes reading your declarations and endorsements to confirm how each part of the property is valued, inspecting and documenting the damage, preparing a detailed estimate, and presenting the claim and any depreciation disputes to the insurer. We cannot promise a particular result, and coverage always depends on the policy and the facts.</p>

<p>Fees are disclosed in a written contract before any work begins; Texas law caps public adjuster compensation at 10% of the insurance settlement. Texas also gives you 72 hours after signing to rescind a public adjuster contract by written notice.</p>

<p>If you have a first payment in hand and the numbers do not make sense, a <a href="/free-claim-review/">free claim review</a> from Corpus Christi Public Adjuster is a simple way to find out where the gap comes from and whether it is worth pursuing.</p>
HTML,
];
