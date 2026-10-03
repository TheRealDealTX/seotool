<?php
return [
    'template'    => 'storm-lookup',
    'title'       => 'Storm Event Lookup for McAllen Properties',
    'seo_title'   => 'Storm Event Lookup | Hail & Wind Reports Near McAllen ZIP Codes',
    'description' => 'Storm event lookup for McAllen and Hidalgo County: search NOAA and NWS hail, wind, and flood reports near your city or ZIP code by date and radius.',
    'lead'        => 'Search official NOAA and National Weather Service storm reports near a Hidalgo County city or ZIP code to see what was recorded around your date of loss.',
    'kicker'      => 'Interactive Tool',
    'image'       => '/assets/img/featured/page-storm-lookup.webp',
    'image_alt'   => 'Map of storm report locations around McAllen, Texas',
    'faqs' => [
        ['q' => 'Do I need to enter my street address?', 'a' => '<p>No. The storm lookup uses the center point of the city or ZIP code you enter. We do not ask for or store street addresses. Keep in mind that distances are measured from that center point, not from your property.</p>'],
        ['q' => 'What data does the storm lookup search?', 'a' => '<p>It searches verified records from the NOAA NCEI Storm Events Database for Hidalgo County and preliminary Local Storm Reports issued by the National Weather Service in Brownsville. County- and zone-wide events such as tropical storms and freezes are included when you set a date or date range.</p>'],
        ['q' => 'Why did my search return no results?', 'a' => '<p>Try a wider radius, a longer date window, or "Hail, wind &amp; more" as the event type. If there is still nothing, it may simply mean no one reported the storm. Many storms cause damage without an official report, so a missing record does not prove your property was unaffected.</p>'],
        ['q' => 'Will a matching storm report get my claim approved?', 'a' => '<p>No tool or report can guarantee a claim outcome. A nearby report is supporting evidence that a storm occurred. Your insurer will still evaluate the actual damage, the cause, and your policy terms.</p>'],
    ],
    'body' => <<<'HTML'
<h2>How the storm event lookup works</h2>
<p>This storm event lookup helps McAllen and Hidalgo County property owners find official weather reports near a location and date. Enter a city or ZIP code, choose a search radius, and optionally add the approximate date of loss. The tool then measures the distance from the <strong>center point</strong> of that city or ZIP code to each report that has coordinates and lists the ones inside your radius.</p>
<p>Results draw on two sources:</p>
<ul>
<li><strong>NOAA NCEI Storm Events Database</strong> &ndash; the verified federal record, published a few months after events occur. You can browse it in full on the <a href="/storm-history/">storm history</a> page.</li>
<li><strong>National Weather Service Local Storm Reports</strong> &ndash; preliminary reports from NWS Brownsville/Rio Grande Valley that appear within hours of a storm. The newest ones are also listed on the <a href="/weather-events/">recent weather events</a> page.</li>
</ul>
<p>Some events, such as tropical storms, hurricanes, and freezes, are recorded for a whole county or NWS forecast zone rather than a single point. Those county- and zone-wide events appear in your results when you set a date or date range that matches them.</p>

<h2>Tips for better results</h2>
<ul>
<li><strong>Start with your date of loss and a &plusmn;7-day window.</strong> People often remember the week of a storm but not the exact day, and a storm that runs late at night may be logged on the following date.</li>
<li><strong>Widen the radius in rural areas.</strong> Spotters and reports are concentrated in populated places. If your property is outside a city center, try 10 or 20 miles.</li>
<li><strong>Filter by event type</strong> once you know what you are looking for, such as hail for a dented roof or wind for missing shingles.</li>
<li><strong>Use a date range</strong> if you discovered damage later and are not sure which storm caused it. Several spring storms can hit the same area weeks apart.</li>
</ul>

<h2>Documenting what you find</h2>
<p>If you find a report that matches your date and area, save it. Open the linked NCEI record or note the NWS report details, then screenshot or print it with the date, time, location, magnitude, and source visible. Add it to your claim file together with:</p>
<ul>
<li>Dated photos and video of the damage, ideally taken before any cleanup or repairs.</li>
<li>Notes on when you noticed the damage and what you saw during the storm.</li>
<li>Your claim number, adjuster contacts, and a log of communications.</li>
<li>Repair estimates and receipts for emergency mitigation such as tarping.</li>
</ul>
<p>Our <a href="/claim-documentation-checklist/">claim documentation checklist</a> walks through this step by step, and <a href="/document-hail-damage-for-an-insurance-claim/">how to document hail damage for an insurance claim</a> covers roof photos in more detail.</p>

<h2>Limitations: nearby does not mean damaged</h2>
<p>A storm report is evidence that weather was observed at a place and time. It is <strong>not proof that your property was damaged</strong>, and it does not decide coverage. Hail and wind can vary sharply over short distances, so a report three miles away may not reflect what happened at your building. The opposite is also true: storms frequently damage properties where no one filed a report.</p>
<p>Also remember that preliminary NWS reports may contain estimated sizes, speeds, and locations that are later revised, and that distances here are measured from a city or ZIP center, not your address. Use these records as one part of your documentation alongside a physical inspection. If your insurer disputes the date or cause of storm damage, a licensed public adjuster can help review the evidence; see our <a href="/services/storm-damage-claims/">storm damage claims</a> page.</p>
HTML,
];
