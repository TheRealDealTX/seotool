<?php
return [
    'template'    => 'deductible-calculator',
    'title'       => 'Hurricane Deductible Calculator',
    'seo_title'   => 'Hurricane Deductible Calculator | Texas Coast Wind & Hail',
    'description' => 'Hurricane deductible calculator for Corpus Christi homeowners: turn a 1%, 2%, 5%, or 10% named-storm or wind/hail deductible into dollars before a storm hits.',
    'lead'        => 'See what a percentage named-storm or wind/hail deductible means in real dollars for your home, and how much of a storm loss you would pay before the policy responds.',
    'kicker'      => 'Interactive Tool',
    'image'       => '/assets/img/featured/page-hurricane-deductible-calculator.webp',
    'image_alt'   => 'Homeowner reviewing a declarations page with a calculator before hurricane season',
    'faqs' => [
        ['q' => 'How is a percentage hurricane deductible calculated?', 'a' => '<p>A percentage deductible is calculated on the dwelling (Coverage A) limit shown on your declarations page, not on the amount of damage. A 2% deductible on a $300,000 dwelling limit is $6,000, whether the storm causes $8,000 or $80,000 of covered damage. Policy wording controls, so check how your policy defines the deductible.</p>'],
        ['q' => 'Is a named-storm deductible the same as a wind/hail deductible?', 'a' => '<p>Not always. A wind/hail deductible usually applies to any wind or hail loss. A named-storm or hurricane deductible typically applies only when the damage is caused by a storm that the National Weather Service or National Hurricane Center has named or declared, sometimes within a set time window. Some policies have both. Your declarations page and endorsements explain which applies.</p>'],
        ['q' => 'Does my TWIA policy have a separate deductible from my homeowners policy?', 'a' => '<p>Yes. TWIA covers wind and hail for eligible coastal properties, and its deductible is set on the TWIA policy. Your homeowners policy, which on the coast often excludes wind and hail, has its own deductible for other covered perils. A flood policy has a separate deductible too. After a hurricane, more than one deductible may apply.</p>'],
        ['q' => 'What if my storm damage is less than the deductible?', 'a' => '<p>Then the policy would likely pay nothing for that loss, though it is still worth documenting the damage and reporting it if your policy requires notice. Hidden damage sometimes turns up later, and a reported claim preserves your timeline. TWIA claims must generally be filed within one year of the date of loss.</p>'],
        ['q' => 'Can I lower my hurricane deductible?', 'a' => '<p>Deductible options depend on your insurer and policy, and changes usually take effect at renewal, not after a storm is in the Gulf. A lower deductible generally means a higher premium. Ask your agent or insurer what options are available well before hurricane season.</p>'],
    ],
    'body' => <<<'HTML'
<h2>Why a hurricane deductible calculator matters on the Texas coast</h2>
<p>Many Corpus Christi and Coastal Bend homeowners are surprised after a storm to learn that their deductible is thousands of dollars higher than they expected. The reason is usually a <strong>percentage deductible</strong>. Instead of a flat $1,000 or $2,500, many Texas policies set the wind/hail or named-storm deductible as a percentage of the dwelling (Coverage A) limit. This hurricane deductible calculator converts that percentage into dollars, so you know your number before hurricane season rather than after.</p>

<h2>Types of storm deductibles you may see</h2>
<table>
<thead><tr><th>Deductible</th><th>When it usually applies</th><th>Where to look</th></tr></thead>
<tbody>
<tr><td>All other perils (AOP)</td><td>Most covered losses other than wind and hail, such as fire or a burst pipe</td><td>Declarations page</td></tr>
<tr><td>Wind/hail</td><td>Any wind or hail damage, whether or not the storm had a name</td><td>Declarations page and wind/hail endorsement</td></tr>
<tr><td>Named storm or hurricane</td><td>Damage from a storm named or declared by the NWS or NHC, as defined in the policy</td><td>Declarations page and named-storm endorsement</td></tr>
<tr><td>TWIA windstorm</td><td>Wind and hail damage covered by a TWIA policy</td><td>TWIA declarations page</td></tr>
<tr><td>Flood</td><td>Flood and surge damage covered by an NFIP or private flood policy</td><td>Flood policy declarations</td></tr>
</tbody>
</table>
<p>On the coast, wind and hail coverage for many homes comes from the Texas Windstorm Insurance Association, because the homeowners policy excludes it. Nueces, San Patricio, Aransas, and Kleberg counties are all in TWIA's designated catastrophe area. Read more in <a href="/named-storm-hurricane-deductibles-texas/">named storm and hurricane deductibles in Texas</a>.</p>

<h2>A worked example</h2>
<p>Click <strong>Load example</strong> in the calculator. It uses a $300,000 dwelling limit, a 2% deductible, and $18,000 of covered wind damage.</p>
<table>
<thead><tr><th>Deductible</th><th>Dollar amount on $300,000</th><th>You pay on $18,000 of damage</th><th>Policy could pay*</th></tr></thead>
<tbody>
<tr><td>1%</td><td>$3,000</td><td>$3,000</td><td>$15,000</td></tr>
<tr><td>2%</td><td>$6,000</td><td>$6,000</td><td>$12,000</td></tr>
<tr><td>5%</td><td>$15,000</td><td>$15,000</td><td>$3,000</td></tr>
<tr><td>10%</td><td>$30,000</td><td>$18,000</td><td>$0</td></tr>
</tbody>
</table>
<p>*Before depreciation, sublimits, roof payment schedules, and other policy terms. On a replacement cost policy, the first payment is usually based on actual cash value, with recoverable depreciation paid after repairs. Use the <a href="/claim-calculator/">claim settlement calculator</a> to model that step.</p>

<h2>How to use your result</h2>
<ul>
<li><strong>Before the season.</strong> Know your number, and decide whether you can cover it. Some owners set aside an emergency fund equal to the deductible.</li>
<li><strong>After a storm.</strong> Compare a contractor's estimate with your deductible. A loss just above the deductible may still be worth a claim, and damage is often larger than it first looks once the roof and attic are inspected.</li>
<li><strong>When more than one policy applies.</strong> Hurricane damage can involve a TWIA wind claim and a flood claim at the same time, each with its own deductible. Read <a href="/wind-vs-storm-surge-damage-claims-texas-coast/">wind vs. storm surge damage claims</a>.</li>
<li><strong>When the insurer's estimate is close to the deductible.</strong> Missing line items can make the difference. An <a href="/services/insurance-estimate-review/">estimate review</a> may help.</li>
</ul>
<p>This calculator runs in your browser; nothing you enter is sent to us. It is an educational estimate, not a coverage decision. For help with a <a href="/services/hurricane-damage-claims/">hurricane damage claim</a> or a <a href="/services/twia-windstorm-claims/">TWIA windstorm claim</a>, request a Free Claim Review.</p>
HTML,
];
