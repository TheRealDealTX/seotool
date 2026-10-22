<?php
return [
    'template'    => 'storm-history',
    'title'       => 'Corpus Christi & Coastal Bend Storm History',
    'seo_title'   => 'Corpus Christi Storm History | Hurricane, Hail & Wind Records',
    'description' => 'Corpus Christi storm history from NOAA: hurricane, hail, wind, tornado, flood, surge, and freeze records for Nueces, San Patricio, Aransas, and Kleberg.',
    'lead'        => 'A searchable record of hurricanes, hail, wind, tornadoes, flooding, storm surge, and freezes in Nueces, San Patricio, Aransas, and Kleberg counties from the NOAA Storm Events Database, with notable local storms.',
    'kicker'      => 'NOAA Storm Records',
    'image'       => '/assets/img/featured/page-storm-history.webp',
    'image_alt'   => 'Hurricane clouds over the Corpus Christi bayfront',
    'faqs' => [
        ['q' => 'Where does the Corpus Christi storm history data come from?', 'a' => '<p>It comes from the NOAA National Centers for Environmental Information (NCEI) <a href="https://www.ncdc.noaa.gov/stormevents/" target="_blank" rel="noopener">Storm Events Database</a>, the official federal record of significant weather. We include entries for Nueces, San Patricio, Aransas, and Kleberg counties and the NWS forecast zones that cover them. Each row links to the original NCEI record.</p>'],
        ['q' => 'How current is the storm history?', 'a' => '<p>NCEI typically publishes verified events a few months after they occur, and the most recent year may be partial or preliminary. For very recent storms, check the <a href="/weather-events/">recent weather events</a> page, which shows preliminary National Weather Service reports.</p>'],
        ['q' => 'When is hail season in Corpus Christi?', 'a' => '<p>In the NOAA record for Nueces County, May has by far the most hail reports, followed by April and March. Hail can fall in other months, including the fall, but spring is the peak.</p>'],
        ['q' => 'Why are hurricanes listed by county or zone instead of an exact location?', 'a' => '<p>Widespread events such as hurricanes, tropical storms, storm surge, and freezes are recorded for a county or an NWS forecast zone, such as Coastal Nueces County or Nueces County Islands, rather than a single point. Use a date or date range to find them.</p>'],
        ['q' => 'Does a hail report near my home prove my roof was damaged?', 'a' => '<p>No. A report shows that hail of a certain size was observed at a certain place and time. It does not show what happened at your address. Hail swaths can be narrow, and damage depends on stone size, wind, roof age, and materials. A physical inspection is needed to document damage.</p>'],
        ['q' => 'What if there is no report for the date my property was damaged?', 'a' => '<p>Storms often cause damage where no one filed a report, especially at night or in rural areas. The absence of a record does not prove a storm did not affect your property. Try the <a href="/storm-lookup/">storm lookup tool</a> with a wider radius and date window, and rely on photos and an inspection.</p>'],
    ],
    'body' => <<<'HTML'
<h2>About the NOAA Storm Events Database</h2>
<p>The <a href="https://www.ncdc.noaa.gov/stormevents/" target="_blank" rel="noopener">Storm Events Database</a> is maintained by NOAA's National Centers for Environmental Information (NCEI). It is the official federal record of significant weather in the United States, compiled from National Weather Service reports. For Corpus Christi and the Coastal Bend, entries are prepared by the <a href="https://www.weather.gov/crp" target="_blank" rel="noopener">NWS Corpus Christi office</a>. This page covers <strong>Nueces, San Patricio, Aransas, and Kleberg counties</strong>.</p>
<p>Each entry generally includes:</p>
<ul>
<li><strong>Event type</strong>, such as hail, thunderstorm wind, tornado, flash flood, storm surge/tide, tropical storm, hurricane, or frost/freeze.</li>
<li><strong>Date, time, and location.</strong> Point events like hail and wind usually list a nearby place name and, in recent decades, coordinates. Widespread events are recorded for a county or an NWS forecast zone, such as Coastal Nueces County or Nueces County Islands.</li>
<li><strong>Magnitude</strong>, such as hail size in inches or wind speed. NCEI records wind in knots; this page converts it to miles per hour.</li>
<li><strong>Narratives</strong> describing what was observed, sometimes including NWS storm survey findings.</li>
</ul>
<p>Records begin in the 1950s. The early decades mostly cover tornadoes, hail, and thunderstorm wind, often with little detail. Since the mid-1990s the database includes many more event types, coordinates, and written narratives.</p>

<h2>Notable storms in Corpus Christi and the Coastal Bend</h2>
<p>The table below highlights significant events. One storm often produces many separate reports, so the links point to a representative entry for each event.</p>
<table>
<thead><tr><th>Date</th><th>Event</th><th>What the record describes</th><th>Source</th></tr></thead>
<tbody>
<tr><td>Aug. 3, 1970</td><td>Hurricane Celia</td><td>Category 4 landfall near Aransas Pass; the NWS reports 140 mph sustained winds measured at Corpus Christi International Airport.</td><td><a href="https://www.weather.gov/crp/hurricanecelia" target="_blank" rel="noopener">NWS</a></td></tr>
<tr><td>Aug. 25, 2017</td><td>Hurricane Harvey</td><td>Category 4 landfall near Rockport. The Nueces County entry describes widespread major damage in Port Aransas, mostly major roof damage, with storm tides of 6 to 8 feet there.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=720925" target="_blank" rel="noopener">Nueces</a> &middot; <a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=718519" target="_blank" rel="noopener">Aransas</a></td></tr>
<tr><td>July 25, 2020</td><td>Hurricane Hanna</td><td>Category 1 landfall on Padre Island. Surge of 2 to 4 feet above ground in coastal Nueces County damaged parts of the Corpus Christi Marina and piers along the bay and inundated North Beach.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=912741" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>Feb. 14&ndash;16, 2021</td><td>Winter storm</td><td>Corpus Christi International Airport set daily record lows three days in a row, including 17&deg;F on February 15, and stayed below freezing all day.</td><td><a href="https://www.weather.gov/crp/stormhistory" target="_blank" rel="noopener">NWS</a></td></tr>
<tr><td>Aug. 22, 2023</td><td>Tropical Storm Harold</td><td>Tropical-storm-force gusts across the Coastal Bend, up to 62 mph at Corpus Christi International Airport, with elevated tides on the bays and barrier islands.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=1133839" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>Apr. 24, 2016</td><td>Hail</td><td>Spotter photos of baseball-size hail (2.75 in) west of Calallen near County Road 75 and FM 624.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=632317" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>May 8, 2025</td><td>Thunderstorm wind</td><td>NWS storm surveys estimated gusts of 105 to 115 mph around Petronila, Driscoll, and Agua Dulce, with snapped power poles and roof damage.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=1247377" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>Nov. 1, 2025</td><td>Hail</td><td>Hail estimated at 3 inches near the Port Aransas airport, the largest Nueces County hail size in the record.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=1297578" target="_blank" rel="noopener">NCEI</a></td></tr>
</tbody>
</table>
<p>For a longer narrative, read <a href="/corpus-christi-storm-history-hail-wind-hurricanes/">Corpus Christi storm history: hail, wind, and hurricanes</a>.</p>

<h2>Seasonal storm patterns in Nueces County</h2>
<p>The NOAA record shows a clear spring peak for hail and thunderstorm wind, and a summer-to-fall season for tropical systems. Of the 134 hail reports for Nueces County in the record, 58 occurred in May, 28 in April, and 18 in March. Thunderstorm wind reports follow a similar pattern, with May far ahead of March, June, and April. The Nueces County record also includes 256 flash flood reports and 17 storm surge/tide entries.</p>
<ul>
<li><strong>Spring (March&ndash;June):</strong> the main season for large hail and damaging straight-line winds, when many Corpus Christi roof, siding, and window claims begin.</li>
<li><strong>Summer and fall:</strong> tropical storms and hurricanes, storm surge, and heavy rain. The Atlantic season runs June 1 through November 30.</li>
<li><strong>Winter:</strong> occasional hard freezes, like February 2021, that can burst pipes in homes not built for prolonged cold.</li>
</ul>
<p>Counts are individual reports, not storm days, and the current year is partial.</p>

<h2>How to use the storm record for an insurance claim</h2>
<p>An official NOAA entry can help confirm that a storm occurred on or near your date of loss, which matters if an insurer questions when damage happened. To use it well:</p>
<ol>
<li>Search by your approximate date of loss and the closest place name, or use the <a href="/storm-lookup/">storm lookup tool</a> to search by distance from your city or ZIP code.</li>
<li>Open the NCEI record and save or print it. Note the date, time, location, magnitude, and narrative.</li>
<li>Keep it with your photos, inspection notes, and estimates. Our <a href="/claim-documentation-checklist/">documentation checklist</a> can help organize your file.</li>
<li>If the storm was recent and is not yet in the database, check the preliminary reports on the <a href="/weather-events/">recent weather events</a> page.</li>
</ol>

<h2>Why a report near you does not prove damage</h2>
<p>Storm reports describe where observers were, not where damage occurred. Hail swaths can be narrow, wind gusts vary block by block, and many storms pass through areas with no spotter at all. A report a mile away does not prove your roof was hit, and the lack of a report does not prove it was not. After a hurricane, the record also cannot tell you whether a given room was damaged by wind or by surge.</p>
<p>That is why insurers and public adjusters rely on a physical inspection. If your insurer has denied or underpaid a <a href="/services/hurricane-damage-claims/">hurricane damage claim</a>, <a href="/services/hail-damage-claims/">hail damage claim</a>, or <a href="/services/wind-damage-claims/">wind damage claim</a>, a licensed public adjuster can review the evidence with you. Coverage always depends on your policy and the facts of the loss.</p>
HTML,
];
