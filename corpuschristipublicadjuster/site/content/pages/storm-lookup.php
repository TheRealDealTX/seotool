<?php
return [
    'template'    => 'storm-lookup',
    'title'       => 'Storm Event Lookup for Coastal Bend Properties',
    'seo_title'   => 'Storm Event Lookup | Hail & Wind Reports Near Corpus Christi',
    'description' => 'Storm event lookup for Corpus Christi and the Coastal Bend: search NOAA and NWS hail, wind, flood, and tropical reports near your city or ZIP code by date.',
    'lead'        => 'Search official NOAA and National Weather Service storm reports near a Coastal Bend city or ZIP code to see what was recorded around your date of loss.',
    'kicker'      => 'Interactive Tool',
    'image'       => '/assets/img/featured/page-storm-lookup.webp',
    'image_alt'   => 'Map of storm report locations around Corpus Christi, Texas',
    'faqs' => [
        ['q' => 'Do I need to enter my street address?', 'a' => '<p>No. The storm lookup uses the center point of the city, community, or ZIP code you enter. We do not ask for or store street addresses. Distances are measured from that center point, not from your property.</p>'],
        ['q' => 'Which areas can I search?', 'a' => '<p>The lookup covers Nueces, San Patricio, Aransas, and Kleberg counties. You can enter places such as Corpus Christi, Calallen, Flour Bluff, North Padre Island, Port Aransas, Portland, Ingleside, Aransas Pass, Rockport, Robstown, or Kingsville, or a local ZIP code.</p>'],
        ['q' => 'What data does the storm lookup search?', 'a' => '<p>It searches verified records from the NOAA NCEI Storm Events Database for the four counties and preliminary Local Storm Reports issued by the National Weather Service in Corpus Christi. County- and zone-wide events such as hurricanes, tropical storms, storm surge, and freezes are included when you set a date or date range.</p>'],
        ['q' => 'Why did my search return no results?', 'a' => '<p>Try a wider radius, a longer date window, or a broader event type. If there is still nothing, it may simply mean no one reported the storm. Many storms cause damage without an official report, so a missing record does not prove your property was unaffected.</p>'],
        ['q' => 'Will a matching storm report get my claim approved?', 'a' => '<p>No tool or report can guarantee a claim outcome. A nearby report is supporting evidence that a storm occurred. Your insurer will still evaluate the actual damage, the cause, and your policy terms.</p>'],
    ],
    'body' => <<<'HTML'
<h2>How the storm event lookup works</h2>
<p>This storm event lookup helps property owners in Corpus Christi, Nueces County, and the surrounding Coastal Bend find official weather reports near a location and date. Enter a city, community, or ZIP code, choose a search radius, and add the approximate date of loss if you know it. The tool measures the distance from the <strong>center point</strong> of that place to each report with coordinates and lists the ones inside your radius. Place and ZIP code center points come from U.S. Census Bureau gazetteer files; a few neighborhood centers, such as Calallen and Flour Bluff, are approximate.</p>
<p>Results draw on two sources covering <strong>Nueces, San Patricio, Aransas, and Kleberg counties</strong>:</p>
<ul>
<li><strong>NOAA NCEI Storm Events Database</strong> &ndash; the verified federal record, published a few months after events occur. You can browse it on the <a href="/storm-history/">storm history</a> page.</li>
<li><strong>National Weather Service Local Storm Reports</strong> &ndash; preliminary reports from NWS Corpus Christi that appear within hours of a storm. The newest are also listed on the <a href="/weather-events/">recent weather events</a> page.</li>
</ul>
<p>Hurricanes, tropical storms, storm surge, and freezes are recorded for a whole county or NWS forecast zone (for example, Nueces County Islands or Coastal San Patricio County) rather than a single point. Those events appear in your results when your date or date range matches them.</p>

<h2>Tips for better results</h2>
<ul>
<li><strong>Start with your date of loss and a &plusmn;7-day window.</strong> People often remember the week of a storm but not the exact day, and a storm late at night may be logged on the following date.</li>
<li><strong>Widen the radius outside the city.</strong> Reports cluster where people live. For property near Banquete, Agua Dulce, or rural San Patricio County, try 10 or 20 miles.</li>
<li><strong>Filter by event type</strong> once you know what you are looking for, such as hail for a dented metal roof or wind for missing shingles.</li>
<li><strong>Use a date range</strong> if you found damage later and are not sure which storm caused it. Several spring storms can cross the same area weeks apart.</li>
<li><strong>For hurricanes, search by date.</strong> Zone-wide tropical and surge entries are matched by date, not distance.</li>
</ul>

<h2>Documenting what you find</h2>
<p>If you find a report that matches your date and area, save it. Open the linked NCEI record or note the NWS report details, then screenshot or print it with the date, time, location, magnitude, and source visible. Add it to your claim file along with:</p>
<ul>
<li>Dated photos and video of the damage, ideally taken before cleanup or repairs</li>
<li>Notes on when you noticed the damage and what you saw during the storm</li>
<li>Your claim number, adjuster contacts, and a log of communications</li>
<li>Repair estimates and receipts for emergency work such as tarping</li>
</ul>
<p>Our <a href="/claim-documentation-checklist/">claim documentation checklist</a> walks through this step by step, and <a href="/document-hail-damage-for-an-insurance-claim/">how to document hail damage for an insurance claim</a> covers roof photos in more detail.</p>

<h2>Limitations: nearby does not mean damaged</h2>
<p>A storm report is evidence that weather was observed at a place and time. It is <strong>not proof that your property was damaged</strong>, and it does not decide coverage. Hail and wind can vary sharply over short distances, so a report three miles away may not reflect what happened at your building. Storms also damage properties where no one filed a report.</p>
<p>Preliminary NWS reports may contain estimated sizes, speeds, and locations that are later revised, and distances here are measured from a place or ZIP center, not your address. Use these records as one part of your documentation alongside a physical inspection. If your insurer disputes the date or cause of storm damage, a licensed public adjuster can help review the evidence; see our <a href="/services/storm-damage-claims/">storm damage claims</a> page.</p>
HTML,
];
