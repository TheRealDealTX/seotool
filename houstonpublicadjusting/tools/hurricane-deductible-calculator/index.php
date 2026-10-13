<?php
require dirname(__DIR__, 2) . '/inc/tools.php';
tool_page([
    'slug' => 'hurricane-deductible-calculator',
    'title' => 'Hurricane Deductible Calculator for Houston & Texas Homeowners',
    'desc' => 'Hurricane and named-storm deductible calculator. See what a 1%, 2% or 5% windstorm deductible means in dollars for your Houston home — and what the insurer should pay.',
    'h1' => 'Hurricane Deductible Calculator',
    'lede' => 'Texas coastal policies often carry a percentage deductible for hurricanes and named storms. Turn that percentage into dollars and see how it changes your payout.',
    'form' => '
<form data-tool="deductible" data-out="out-deductible" class="tool-grid">
  <label>Dwelling coverage &mdash; Coverage A ($)<input name="coverage_a" inputmode="decimal" value="350000"><span class="hint">On your declarations page</span></label>
  <label>Hurricane / windstorm deductible (%)
    <select name="pct"><option>1</option><option selected>2</option><option>3</option><option>5</option><option>10</option></select></label>
  <label>Standard all-peril deductible ($)<input name="standard" inputmode="decimal" value="2500"></label>
  <label>Estimated storm damage ($)<input name="damage" inputmode="decimal" value="28000"></label>
</form>
<div class="tool-result" id="out-deductible" aria-live="polite"></div>',
    'prose' => '
<h2>How hurricane deductibles work</h2>
<p>A hurricane (or &ldquo;named storm&rdquo; or &ldquo;windstorm and hail&rdquo;) deductible is a percentage of your <strong>dwelling coverage limit</strong>, not of the damage. On a home insured for $350,000, a 2% deductible is $7,000 &mdash; the first $7,000 of hurricane damage is yours. Many Houston-area policies carry 1% to 2%; homes closer to the coast and policies through the Texas Windstorm Insurance Association (TWIA) can be higher.</p>
<p>What triggers the deductible matters. Most policies apply it only when the National Weather Service has named the storm, and only for a defined window around it. Damage from a derecho like May 2024, a spring hailstorm or an unnamed tropical system usually falls under the standard deductible instead. We have seen carriers apply the larger deductible to the wrong event, and that alone can cost a homeowner thousands.</p>
<h2>Ways to reduce what you pay out of pocket</h2>
<ul class="checklist">
  <li>Make sure the carrier&rsquo;s estimate is complete; low scopes are the most common reason a claim &ldquo;doesn&rsquo;t meet the deductible&rdquo;</li>
  <li>Include all wind damage: roof, fences, siding, gutters, screens, interior water from wind openings</li>
  <li>Confirm the deductible actually applies to the storm and dates in question</li>
  <li>Check whether separate structures, contents and ALE are affected by the same deductible</li>
</ul>',
    'faqs' => [
        ['Does a hurricane deductible apply to flood damage?', 'No. Flood damage (rising water) is excluded from homeowners policies and is covered only by a separate flood policy with its own deductible.'],
        ['Is a hurricane deductible applied per storm or per year?', 'Most Texas policies apply it per named-storm event. Read the endorsement on your policy; a few use a calendar-year approach.'],
        ['My damage is less than the deductible. Should I still file?', 'Get a full inspection first. Carrier estimates are frequently low, and hidden roof or interior damage can push a claim over the deductible. A free review costs nothing.'],
    ],
]);
