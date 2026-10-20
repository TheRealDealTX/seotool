<?php
return [
    'template'    => 'hurricane-deductible-calculator',
    'title'       => 'Hurricane Deductible Calculator',
    'seo_title'   => 'Hurricane Deductible Calculator for Texas Homeowners',
    'description' => 'Convert a 1%, 2%, or 5% wind/hail or named-storm deductible into dollars and see what a Port Arthur hurricane claim could pay. Free and private.',
    'lead'        => 'Percentage deductibles are figured on your dwelling limit, not your damage. See the real dollar amount before storm season — and what it means for a claim.',
    'kicker'      => 'Claim Tools',
    'image'       => '/assets/img/featured/page-hurricane-deductible-calculator.webp',
    'image_alt'   => 'Homeowners reviewing insurance policy numbers with a public adjuster',
    'hide_hero_cta' => true,
    'faqs' => [
        ['q' => 'How is a percentage hurricane deductible calculated?', 'a' => '<p>It is a percentage of the dwelling limit (Coverage A) shown on your declarations page. A 2% deductible on a home insured for $250,000 is $5,000, whether the damage is $6,000 or $60,000. Check your own policy wording, because some forms calculate it differently.</p>'],
        ['q' => 'What is the difference between a named-storm and a wind/hail deductible?', 'a' => '<p>A named-storm or hurricane deductible usually applies only to damage from a storm the National Weather Service or National Hurricane Center has named. A wind/hail deductible usually applies to any wind or hail loss, including ordinary thunderstorms. Your declarations page and endorsements say which one you have.</p>'],
        ['q' => 'Does a TWIA policy have its own deductible?', 'a' => '<p>Yes. If your homeowners policy excludes wind and you carry a separate Texas Windstorm Insurance Association policy, the TWIA deductible applies to wind and hail damage. See our <a href="/services/twia-windstorm-claims/">TWIA windstorm claims</a> page and <a href="https://www.twia.org/" target="_blank" rel="noopener">twia.org</a> for the options available.</p>'],
        ['q' => 'Should I file a claim if the damage is close to my deductible?', 'a' => '<p>Get a thorough estimate first. Hurricane damage is often larger than it looks at first&mdash;roof decking, interior moisture, and code-required items can be missed. A <a href="/free-claim-review/">Free Claim Review</a> can help you decide before you file.</p>'],
        ['q' => 'Is my flood deductible the same as my wind deductible?', 'a' => '<p>No. Flood insurance through the NFIP or a private flood carrier has separate building and contents deductibles. One hurricane can involve a wind deductible and a flood deductible on different policies.</p>'],
    ],
    'body' => <<<'HTML'
<h2>Why percentage deductibles surprise Port Arthur homeowners</h2>
<p>Many Texas homeowners policies, and TWIA windstorm policies, use a <strong>percentage deductible</strong> for wind and hail. Because it is based on the insured value of the house, the dollar amount can be several times larger than the flat deductible used for fire or plumbing leaks. A Port Arthur homeowner with a $300,000 dwelling limit and a 2% deductible pays the first $6,000 of a covered wind claim.</p>
<p>That matters most after a hurricane, when a home may have roof, siding, fence, and interior water damage at once. Knowing the number ahead of time helps you budget for repairs, decide whether a lower deductible is worth the premium, and avoid surprises when the first check arrives.</p>

<h2>Example: one storm, three deductibles</h2>
<div class="table-wrap"><table>
<thead><tr><th scope="col">Dwelling limit</th><th scope="col">1%</th><th scope="col">2%</th><th scope="col">5%</th></tr></thead>
<tbody>
<tr><td>$150,000</td><td>$1,500</td><td>$3,000</td><td>$7,500</td></tr>
<tr><td>$250,000</td><td>$2,500</td><td>$5,000</td><td>$12,500</td></tr>
<tr><td>$400,000</td><td>$4,000</td><td>$8,000</td><td>$20,000</td></tr>
</tbody></table></div>

<h2>What the calculator does not include</h2>
<p>A real claim payment also depends on depreciation, replacement cost versus actual cash value terms, roof payment schedules, sublimits, and whether a loss is covered at all. For those numbers, use the <a href="/claim-calculator/">claim settlement calculator</a>. If wind and flood both damaged your property, our guide to <a href="/wind-vs-flood-damage-port-arthur-insurance/">wind vs. flood damage</a> explains how the policies split the loss.</p>
<p>Questions about which deductible applies, or whether your insurer applied it correctly? A Port Arthur Public Adjuster can review your declarations page and the insurer's estimate at no cost through a <a href="/free-claim-review/">Free Claim Review</a>.</p>
HTML,
];
