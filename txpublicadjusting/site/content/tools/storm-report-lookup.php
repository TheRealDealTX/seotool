<?php
return [
    'title'       => 'Texas Hail & Wind Storm Report Lookup by Date',
    'description' => 'Search National Weather Service hail, wind and tornado reports near any Texas city for a date or range. Find your date of loss for an insurance claim.',
    'h1'          => 'Storm report lookup',
    'lead'        => 'Insurers want a specific date of loss. Search National Weather Service storm reports (hail size, wind gusts, damage and tornadoes) near your property for a single day or a whole season.',
    'updated'     => '2026-10-13',
    'script'      => '/assets/js/tools/storms.js',
    'app'         => <<<'HTML'
<div data-storm>
  <div class="tcols">
    <div>
      <label class="tf">City or town in Texas<input list="tx-places" data-in="city" placeholder="Start typing, e.g. Belton" autocomplete="off"><small data-out="cityhint">Distances are measured from the town center.</small></label>
      <datalist id="tx-places"></datalist>
      <div class="tf-row">
        <label class="tf">Search radius<select data-in="radius"><option value="5">5 miles</option><option value="10" selected>10 miles</option><option value="25">25 miles</option><option value="50">50 miles</option></select></label>
        <label class="tf">Report types<select data-in="types"><option value="hail" selected>Hail and wind</option><option value="hailonly">Hail only</option><option value="all">Hail, wind and tornado</option></select></label>
      </div>
    </div>
    <div>
      <p class="tlabel">When?</p>
      <div class="seg" data-seg="range">
        <button type="button" class="is-on" data-v="day">A specific date</button>
        <button type="button" data-v="span">Date range</button>
        <button type="button" data-v="year">Last 12 months</button>
      </div>
      <div class="tf-row">
        <label class="tf" data-r="day span">From<input type="date" data-in="d1"></label>
        <label class="tf" data-r="span" hidden>To<input type="date" data-in="d2"></label>
      </div>
      <button type="button" class="btn btn--primary btn--block" data-act="go">Search storm reports</button>
    </div>
  </div>
  <div data-out="status" class="muted" style="margin-top:1rem" aria-live="polite"></div>
  <div data-out="summary"></div>
  <div class="table-wrap" data-out="tablewrap" hidden>
    <table><thead><tr><th>Date &amp; time (CT)</th><th>Report</th><th>Size / speed</th><th>Location</th><th>Distance</th><th>Source</th></tr></thead><tbody data-out="rows"></tbody></table>
  </div>
  <div class="storm-links" data-out="links"></div>
  <p class="muted" style="font-size:.8rem;margin-top:1rem">Storm reports: National Weather Service Local Storm Reports via the Iowa Environmental Mesonet. Place coordinates: GeoNames (CC BY 4.0). Reports are preliminary, and a storm can damage properties where nobody filed a report.</p>
</div>
HTML,
    'body'        => <<<'HTML'
<h2>Why the date of loss matters</h2>
<p>A property claim attaches to a specific event. If the insurer can't tie your damage to a storm on a specific date, within your policy period and inside any reporting window, it may deny the claim as "wear and tear" or "prior damage." This is especially common in hail-prone parts of Texas, where a roof may have been hit by several storms. Our guide to <a href="/post/how-long-do-you-have-to-file-a-hail-claim-in-texas/">hail claim filing deadlines</a> explains why old damage is harder to claim.</p>
<h2>How to read the results</h2>
<ul class="checklist">
  <li><strong>Hail size</strong> is reported in inches. One inch (quarter size) and larger is often where shingle damage starts to be argued, but damage depends on the roof, the wind and the hail density, not size alone.</li>
  <li><strong>Distance</strong> is from the center of the town you picked. Storms are wider than the points on a map; a report three miles away can still mean hail at your address.</li>
  <li><strong>No report doesn't mean no storm.</strong> Reports come from spotters, the public and weather stations. Rural areas have fewer of them.</li>
  <li>For a claim, pair the report with your own evidence: dated photos, soft-metal dents, neighbors' claims.</li>
</ul>
<div class="callout callout--tip"><p><strong>Tip:</strong> save or print the results page for your claim file, along with the NOAA daily report linked above. Engineers and adjusters often check the same sources.</p></div>
[[tool:claim-documentation-checklist]]
HTML,
    'faqs' => [
        ['q' => 'Where does this storm data come from?', 'a' => 'Local Storm Reports issued by National Weather Service offices, accessed through the Iowa Environmental Mesonet at Iowa State University. The tool also links to NOAA\'s Storm Prediction Center daily reports and the NCEI Storm Events Database, which publishes verified records after a delay of a few months.'],
        ['q' => 'Can I use this report as proof for my insurance claim?', 'a' => 'It\'s supporting evidence of a storm on a date near your property. Insurers and their engineers use similar sources, often with commercial hail-mapping products. Combine it with photos and physical evidence.'],
        ['q' => 'Why can\'t I find the storm that hit my house?', 'a' => 'Try a wider radius, the day before or after (storms that arrive after midnight are dated the next day), and "Hail, wind and tornado" report types. Some storms simply go unreported.'],
    ],
    'related' => ['/post/hail-damage-insurance-claim/', '/post/how-insurance-companies-evaluate-hail-damage/', '/services/roof-hail-damage-claims/'],
];
