<?php
return [
    'template'    => 'claim-calculator',
    'title'       => 'Insurance Claim Settlement Calculator',
    'seo_title'   => 'Insurance Claim Settlement Calculator | RCV, ACV & Deductible',
    'description' => 'Free insurance claim settlement calculator for San Marcos and Hays County: see how RCV, depreciation, ACV, deductibles, and limits shape your payment.',
    'lead'        => 'Plug in the figures from your estimate and declarations page to see how a Texas property insurance payment is likely to break down. The math runs in your browser and nothing is sent to us.',
    'kicker'      => 'Interactive Tool',
    'image'       => '/assets/img/featured/page-claim-calculator.webp',
    'image_alt'   => 'Calculator beside a printed property insurance estimate',
    'faqs' => [
        ['q' => 'How accurate is this insurance claim settlement calculator?', 'a' => '<p>It uses the same basic structure insurers use for replacement cost and actual cash value settlements, so it is a good way to see how the pieces fit. It is still an educational estimate. Your real payment depends on your policy forms, endorsements, sublimits, how depreciation is applied, and the facts of the loss.</p>'],
        ['q' => 'What do RCV and ACV mean on my estimate?', 'a' => '<p>Replacement cost value (RCV) is today’s cost to repair or replace the damaged property with materials of like kind and quality. Actual cash value (ACV) is generally RCV minus depreciation. Our article on <a href="/replacement-cost-vs-actual-cash-value-texas/">replacement cost vs. actual cash value in Texas</a> explains both in more detail.</p>'],
        ['q' => 'When do I get the depreciation that was held back?', 'a' => '<p>On many replacement-cost policies, recoverable depreciation is released after the repairs are finished and documented, often within a time limit stated in the policy. Ask your insurer what proof it needs, such as a final invoice or completion photos, and note the deadline.</p>'],
        ['q' => 'Why is my wind/hail deductible so much higher than my other deductible?', 'a' => '<p>Many Texas policies set a separate wind/hail deductible as a percentage of the dwelling (Coverage A) limit. A 2% wind/hail deductible on a $350,000 dwelling limit is $7,000. Because hail and thunderstorm wind are the most common severe weather in Hays County’s NOAA record, that deductible applies to a large share of San Marcos roof claims. Your declarations page shows the exact figure.</p>'],
        ['q' => 'What should I do if the insurer’s estimate looks low?', 'a' => '<p>Compare it line by line with what the repair actually requires, including permit and code items, and ask the insurer to explain differences in writing. A public adjuster can go through it with you through our <a href="/services/insurance-estimate-review/">insurance estimate review</a> service. No one can promise a different outcome, but a careful review often finds missing or underpriced items.</p>'],
    ],
    'body' => <<<'HTML'
<h2>The building blocks of a property insurance settlement</h2>
<p>Most homeowners only see the bottom line on an insurer’s estimate: the net claim amount. This insurance claim settlement calculator works backward from the pieces that produce that number so San Marcos and Hays County property owners can see where the money goes, why the first check is often smaller than a contractor’s bid, and how much may still come later. Below is what each input means and where to find it.</p>

<table>
<thead><tr><th>Term</th><th>What it means</th><th>Where to find it</th></tr></thead>
<tbody>
<tr><td>Replacement cost value (RCV)</td><td>Today’s price to repair or replace with like kind and quality</td><td>Summary page of the insurer’s estimate, or your contractor’s total</td></tr>
<tr><td>Depreciation</td><td>A reduction for age, wear, and condition, often applied line by line</td><td>Insurer’s estimate (sometimes split into recoverable and non-recoverable)</td></tr>
<tr><td>Actual cash value (ACV)</td><td>Generally RCV minus depreciation</td><td>Insurer’s estimate summary</td></tr>
<tr><td>Deductible</td><td>The share of a covered loss you pay; wind/hail is often a percentage</td><td>Declarations page</td></tr>
<tr><td>Policy limit</td><td>The most the policy pays for that coverage</td><td>Declarations page (Coverage A for the dwelling)</td></tr>
<tr><td>Prior payments</td><td>Checks already issued on this claim</td><td>Payment letters or your bank records</td></tr>
</tbody>
</table>

<h3>Recoverable and non-recoverable depreciation</h3>
<p>Depreciation is where most of the confusion lives. Under a replacement-cost policy, depreciation is usually <strong>recoverable</strong>: the insurer holds it back until the work is done, then pays it once you show the repairs were completed, often within a deadline in the policy. Under an actual cash value policy, or coverage settled at ACV, depreciation is <strong>non-recoverable</strong> and never comes back. Some Texas policies treat roofs differently from the rest of the house, either settling them at ACV or using a roof payment schedule based on age, so read the roof provisions in your policy carefully.</p>

<h3>Percentage deductibles</h3>
<p>Hays County is outside the Texas Windstorm Insurance Association (TWIA) area, so wind and hail coverage for San Marcos properties normally comes from the regular homeowners or commercial insurer and follows that policy’s deductible. A percentage wind/hail deductible can be several thousand dollars, which is why some modest hail claims end up with little or no payment. Check the deductible before deciding how to proceed.</p>

<h2>Worked example</h2>
<p>Press <strong>Load example</strong> in the calculator to fill in these figures: a replacement-cost policy, $24,000 RCV, $7,200 depreciation, a $5,000 deductible, no prior payments, no non-covered costs, and no limit entered.</p>
<table>
<thead><tr><th>Step</th><th>How it is figured</th><th>Result</th></tr></thead>
<tbody>
<tr><td>Covered RCV</td><td>$24,000 RCV minus $0 non-covered</td><td>$24,000</td></tr>
<tr><td>ACV</td><td>$24,000 minus $7,200 depreciation</td><td>$16,800</td></tr>
<tr><td>First (ACV) payment</td><td>$16,800 minus $5,000 deductible minus $0 already paid</td><td>$11,800</td></tr>
<tr><td>Recoverable depreciation</td><td>($24,000 minus $5,000) minus $11,800</td><td>$7,200</td></tr>
<tr><td>Total estimated proceeds</td><td>$11,800 plus $7,200</td><td>$19,000</td></tr>
<tr><td>Your out-of-pocket</td><td>$24,000 minus $19,000</td><td>$5,000 (the deductible)</td></tr>
</tbody>
</table>
<p>Now uncheck the replacement-cost box. On an ACV basis the $7,200 of depreciation is not paid later, total proceeds stay at $11,800, and your share of the project rises to $12,200. That single checkbox shows why it matters so much to know how your policy settles roofs and other items.</p>

<h2>Why the totals may not match the real repair cost</h2>
<ul>
<li><strong>Items left off the estimate.</strong> Drip edge, starter course, ridge cap, flashing, gutter and downspout work, detach-and-reset of solar panels or satellite dishes, and interior ceiling or insulation damage are common omissions.</li>
<li><strong>Code and permit requirements.</strong> The City of San Marcos enforces the 2021 International Codes. Upgrades that the code requires may fall under ordinance or law coverage, up to its limit, rather than the main dwelling coverage. Our <a href="/local-building-codes/">San Marcos building codes guide</a> explains the local rules.</li>
<li><strong>Depreciation choices.</strong> The age and condition assigned to a roof or flooring can swing the ACV by thousands of dollars.</li>
<li><strong>Pricing after a big storm.</strong> After a widespread hail event along the I-35 corridor, labor and material costs can rise as many properties need work at once.</li>
<li><strong>Hidden damage.</strong> Water that has wicked into walls or insulation, or hail damage to soft metals and HVAC fins, may not show up until a closer inspection.</li>
</ul>
<p>For roof claims specifically, see <a href="/how-to-review-underpaid-roof-insurance-estimate/">how to review an underpaid roof insurance estimate</a>, and if new damage is found during repairs, read about <a href="/services/insurance-claim-supplements/">insurance claim supplements</a>. If the numbers still do not add up, a <a href="/">San Marcos public adjuster</a> can compare the estimate with the actual scope of work. Coverage and payment always depend on your policy and the facts of your claim.</p>
HTML,
];
