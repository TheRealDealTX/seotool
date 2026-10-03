<?php
return [
    'template'    => 'claim-calculator',
    'title'       => 'Insurance Claim Settlement Calculator',
    'seo_title'   => 'Insurance Claim Settlement Calculator (RCV, ACV, Depreciation)',
    'description' => 'Free insurance claim settlement calculator: estimate RCV, ACV, depreciation, deductible, and out-of-pocket cost for a Texas property claim.',
    'lead'        => 'Estimate how replacement cost, depreciation, your deductible, and policy limits may affect a property insurance payment. Everything runs in your browser.',
    'kicker'      => 'Interactive Tool',
    'image'       => '/assets/img/featured/page-claim-calculator.webp',
    'image_alt'   => 'Calculator and insurance estimate on a desk',
    'faqs' => [
        ['q' => 'Is this insurance claim settlement calculator accurate?', 'a' => '<p>It applies standard math for replacement cost and actual cash value settlements, so it is useful for understanding how the numbers fit together. It is an educational estimate only. Your actual payment depends on your policy language, endorsements, sublimits, depreciation methods, and the facts of the claim.</p>'],
        ['q' => 'What is the difference between RCV and ACV?', 'a' => '<p>Replacement cost value (RCV) is the cost to repair or replace damaged property with materials of like kind and quality at today\'s prices. Actual cash value (ACV) is generally RCV minus depreciation. Read more in our guide to <a href="/replacement-cost-vs-actual-cash-value-texas/">replacement cost vs. actual cash value in Texas</a>.</p>'],
        ['q' => 'How do I get my recoverable depreciation?', 'a' => '<p>Under many replacement-cost policies, the insurer pays ACV first and releases recoverable depreciation after repairs are completed and documented, often within a deadline stated in the policy. Check your policy for the time limit and ask your insurer what proof it needs, such as a final invoice.</p>'],
        ['q' => 'Why is my wind/hail deductible so high?', 'a' => '<p>Many Texas policies carry a separate wind/hail deductible calculated as a percentage of the dwelling (Coverage A) limit, rather than a flat dollar amount. For example, a 2% deductible on a $250,000 dwelling limit is $5,000. Check your declarations page for the exact figure.</p>'],
        ['q' => 'What if the insurer\'s estimate seems too low?', 'a' => '<p>Compare the estimate line by line with what the repairs actually require, including code-required items, and ask the insurer to explain any differences. A public adjuster can review the estimate with you; see our <a href="/services/insurance-estimate-review/">insurance estimate review</a> service. We cannot promise a different result, but a careful review can identify missing items.</p>'],
    ],
    'body' => <<<'HTML'
<h2>How an insurance claim settlement is calculated</h2>
<p>Property insurance payments follow a fairly standard structure, even though every policy is different. This insurance claim settlement calculator walks through that structure so you can see why the first check is often smaller than the repair estimate, and how much more may be available later. Here are the key terms.</p>

<h3>Replacement cost value (RCV)</h3>
<p>RCV is what it would cost today to repair or replace the damaged property with materials of like kind and quality. On a roof claim, for example, that includes tear-off, new shingles or panels, underlayment, flashing, labor, and related items. The insurer's estimate and your contractor's estimate should both show an RCV total.</p>

<h3>Depreciation</h3>
<p>Depreciation is a reduction in value based on age, wear, and condition. Insurers often apply it line by line in the estimate. There are two kinds that matter:</p>
<ul>
<li><strong>Recoverable depreciation</strong> &ndash; under a replacement-cost policy, the withheld amount can typically be recovered after repairs are completed, often within a deadline stated in the policy.</li>
<li><strong>Non-recoverable depreciation</strong> &ndash; on an actual cash value policy, or on coverage that is settled at ACV (some Texas roof coverage works this way), depreciation is not paid back.</li>
</ul>

<h3>Actual cash value (ACV)</h3>
<p>ACV is generally RCV minus depreciation. Under a typical replacement-cost policy, the insurer pays ACV first, minus your deductible, and then releases recoverable depreciation once repairs are done.</p>

<h3>Deductibles</h3>
<p>Your deductible is the portion of a covered loss you pay. Many Texas policies have a separate <strong>wind/hail deductible</strong> calculated as a percentage of the dwelling (Coverage A) limit. A 2% deductible on a $250,000 dwelling limit, for example, is $5,000. Named-storm or hurricane deductibles may also apply. Check your declarations page.</p>

<h3>Policy limits and prior payments</h3>
<p>The insurer will not pay more than the applicable limit, such as your Coverage A dwelling limit or a sublimit for a specific type of damage. If you have already received checks on the claim, they are subtracted to show what may still be owed.</p>

<h3>Where to find your numbers</h3>
<p>The insurer's estimate usually lists the RCV, depreciation, ACV, deductible, and net claim amount on its summary page. Your declarations page shows your coverage limits and deductibles. If you have a contractor's estimate, you can enter its total as the RCV to compare it with the insurer's figures. Enter any payments already issued so the calculator can show what may remain.</p>

<h2>Worked example</h2>
<p>Click <strong>Load example</strong> in the calculator to see these numbers. The example assumes a replacement-cost policy, an RCV of $24,000, depreciation of $7,200, a $5,000 deductible, no prior payments, no non-covered costs, and no policy limit entered.</p>
<table>
<thead><tr><th>Step</th><th>Calculation</th><th>Amount</th></tr></thead>
<tbody>
<tr><td>Covered RCV</td><td>$24,000 RCV &minus; $0 non-covered</td><td>$24,000</td></tr>
<tr><td>Actual cash value (ACV)</td><td>$24,000 &minus; $7,200 depreciation</td><td>$16,800</td></tr>
<tr><td>Initial (ACV) payment</td><td>$16,800 &minus; $5,000 deductible &minus; $0 prior payments</td><td>$11,800</td></tr>
<tr><td>Recoverable depreciation</td><td>($24,000 &minus; $5,000) &minus; $11,800</td><td>$7,200</td></tr>
<tr><td>Total estimated proceeds</td><td>$11,800 + $7,200</td><td>$19,000</td></tr>
<tr><td>Out-of-pocket cost</td><td>$24,000 &minus; $19,000 (the deductible)</td><td>$5,000</td></tr>
</tbody>
</table>
<p>If you uncheck the replacement-cost box to model an ACV policy, the recoverable depreciation drops to $0, total proceeds fall to $11,800, and the $7,200 of depreciation becomes part of your out-of-pocket cost.</p>

<h2>Common reasons the numbers do not match your repair cost</h2>
<ul>
<li><strong>Missing line items.</strong> Estimates sometimes leave out items like drip edge, starter strip, ridge vents, gutters, or interior damage.</li>
<li><strong>Code-required work.</strong> Upgrades required by current building codes may be covered only under ordinance or law coverage, up to its limit. See our <a href="/local-building-codes/">McAllen building codes</a> page.</li>
<li><strong>Depreciation choices.</strong> The age and condition assigned to materials can change the ACV significantly.</li>
<li><strong>Pricing.</strong> Unit prices may not reflect local labor and material costs at the time of repair.</li>
</ul>
<p>For a full explanation of settlement types, read <a href="/replacement-cost-vs-actual-cash-value-texas/">replacement cost vs. actual cash value in Texas</a>. If the insurer's estimate looks low, our <a href="/services/insurance-estimate-review/">insurance estimate review</a> service can help you compare it with the actual scope of repairs. Coverage and payment always depend on your policy and the facts of your claim.</p>
HTML,
];
