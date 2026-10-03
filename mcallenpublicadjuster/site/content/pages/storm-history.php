<?php
return [
    'template'    => 'storm-history',
    'title'       => 'McAllen & Hidalgo County Storm History',
    'seo_title'   => 'McAllen Storm History | Hidalgo County Hail & Wind Records',
    'description' => 'Search McAllen and Hidalgo County storm history from NOAA: hail, wind, tornado, tropical, flood, and freeze records with notable local events.',
    'lead'        => 'A searchable record of hail, wind, tornado, tropical, flood, and freeze events in Hidalgo County from the NOAA Storm Events Database, with notable McAllen storms and tips for using the data in a claim.',
    'kicker'      => 'NOAA Storm Records',
    'image'       => '/assets/img/featured/page-storm-history.webp',
    'image_alt'   => 'Severe thunderstorm with hail core over the Rio Grande Valley',
    'faqs' => [
        ['q' => 'Where does the McAllen storm history data come from?', 'a' => '<p>It comes from the NOAA National Centers for Environmental Information (NCEI) <a href="https://www.ncdc.noaa.gov/stormevents/" target="_blank" rel="noopener">Storm Events Database</a>, the official federal record of significant weather events. We include entries for Hidalgo County and the NWS forecast zones that cover it. Each row links to the original NCEI record.</p>'],
        ['q' => 'How current is the storm history?', 'a' => '<p>NCEI typically publishes verified events a few months after they occur, and the most recent year may be partial or preliminary. For very recent storms, check the <a href="/weather-events/">recent weather events</a> page, which shows preliminary National Weather Service reports.</p>'],
        ['q' => 'When is hail season in McAllen?', 'a' => '<p>In the NOAA record for Hidalgo County, May and April have by far the most hail reports, followed by June and March. Hail can occur in other months, but spring is the peak.</p>'],
        ['q' => 'Does a hail report near my home prove my roof was damaged?', 'a' => '<p>No. A report shows that hail of a certain size was observed at a certain place and time. It does not show what happened at your address. Hail swaths can be narrow, and damage depends on stone size, wind, roof age, and materials. A physical inspection is needed to document damage.</p>'],
        ['q' => 'What if there is no report for the date my property was damaged?', 'a' => '<p>Storms often cause damage where no one filed a report, especially at night or in rural areas. The absence of a record does not prove a storm did not affect your property. Try the <a href="/storm-lookup/">storm lookup tool</a> with a wider radius and date window, and rely on photos and an inspection.</p>'],
    ],
    'body' => <<<'HTML'
<h2>About the NOAA Storm Events Database</h2>
<p>The <a href="https://www.ncdc.noaa.gov/stormevents/" target="_blank" rel="noopener">Storm Events Database</a> is maintained by NOAA's National Centers for Environmental Information (NCEI). It is the official federal record of significant weather in the United States, compiled from National Weather Service reports. For McAllen and the rest of Hidalgo County, entries are prepared by the NWS office in Brownsville that serves the Rio Grande Valley (RGV).</p>
<p>Each entry generally includes:</p>
<ul>
<li><strong>Event type</strong>, such as hail, thunderstorm wind, tornado, flash flood, tropical storm, hurricane, or frost/freeze.</li>
<li><strong>Date, time, and location.</strong> Point events like hail and wind usually list a nearby place name and, in recent decades, latitude and longitude. Widespread events like tropical storms and freezes are recorded for a <em>county</em> or an NWS <em>forecast zone</em> (for example, Northern or Southern Hidalgo County) rather than a single point.</li>
<li><strong>Magnitude</strong>, such as hail size in inches or wind speed. NCEI records wind in knots; this page converts it to miles per hour.</li>
<li><strong>Narratives</strong> describing what was observed, sometimes including NWS storm survey findings.</li>
</ul>
<p>Records begin in 1950. The early decades mostly cover tornadoes, hail, and thunderstorm wind, often with little detail. Since the mid-1990s the database includes many more event types, coordinates, and written narratives, so recent events are documented in much greater depth.</p>

<h2>Notable storms in McAllen and Hidalgo County</h2>
<p>The table below highlights several significant events in the NOAA record. Each links to an official NCEI entry. One storm often produces many separate reports, so these links point to a representative entry for each event.</p>
<table>
<thead><tr><th>Date</th><th>Event</th><th>What the NOAA record describes</th><th>Record</th></tr></thead>
<tbody>
<tr><td>July 23, 2008</td><td>Hurricane Dolly</td><td>Widespread minor to moderate structural damage across the Lower Rio Grande Valley and heavy rainfall that flooded low-lying and poorly drained areas.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=129365" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>April 20, 2012</td><td>Hail</td><td>Softball-size hail reported by the public at McAllen High School; golf ball to baseball size stones fell for more than twenty minutes across the McAllen and Mission area.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=379500" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>July 25&ndash;26, 2020</td><td>Hurricane Hanna</td><td>Category 1 landfall on Padre Island in Kenedy County; tropical-storm impacts and major rainfall flooding in Hidalgo County.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=914182" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>February 14&ndash;20, 2021</td><td>Prolonged freeze</td><td>Repeated nights below freezing; McAllen International reported a low of 21&deg;F, with lows in the lower 20s to upper teens across southern Hidalgo County.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=944581" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>April 21, 2023</td><td>Hail</td><td>Up to an hour of continuous hail across southern Hidalgo County, with reports up to baseball size (2.75 in) near Pe&ntilde;itas and McCook and tennis-ball size in Mission.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=1082244" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>April 28, 2023</td><td>Thunderstorm wind</td><td>NWS storm surveys estimated gusts near 85 mph in McAllen and found more than half the shingles off a two-story building on S 29th St; a small plane was flipped onto its roof at McAllen-Miller International Airport.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=1084452" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>May 8, 2025</td><td>Hail and microburst</td><td>A supercell produced hail up to 3 inches in north McAllen, and a microburst with estimated winds near 85 mph damaged trees near the McAllen&ndash;Edinburg line.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=1263450" target="_blank" rel="noopener">Hail</a> &middot; <a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=1257702" target="_blank" rel="noopener">Wind</a></td></tr>
</tbody>
</table>

<h2>Seasonal storm patterns in Hidalgo County</h2>
<p>The NOAA record shows a clear spring peak. Of the 163 hail reports for Hidalgo County through 2025, 64 occurred in May and 40 in April, with June and March next. Thunderstorm wind reports follow the same pattern: May and April lead, followed by June and August.</p>
<ul>
<li><strong>Spring (March&ndash;June):</strong> the main season for large hail and damaging straight-line winds. This is when many McAllen roof, siding, and window claims begin.</li>
<li><strong>Summer and fall:</strong> tropical systems such as Dolly and Hanna, plus heavy rain and flash flooding.</li>
<li><strong>Winter:</strong> occasional hard freezes, like February 2021, that can burst pipes in homes not built for prolonged cold.</li>
</ul>
<p>For a deeper look at the spring pattern, read our <a href="/mcallen-hail-season-storm-data/">McAllen hail season storm data</a> article.</p>

<h2>How to use the storm record for an insurance claim</h2>
<p>An official NOAA entry can help confirm that a storm occurred on or near your date of loss, which can be important if an insurer questions when damage happened. To use it well:</p>
<ol>
<li>Search by your approximate date of loss and the closest city name, or use the <a href="/storm-lookup/">storm lookup tool</a> to search by distance from your city or ZIP code.</li>
<li>Open the NCEI record and save or print it. Note the date, time, location, magnitude, and narrative.</li>
<li>Keep it with your photos, inspection notes, and estimates. Our <a href="/claim-documentation-checklist/">documentation checklist</a> can help organize your claim file.</li>
<li>If the storm happened recently and is not yet in the database, check the preliminary reports on the <a href="/weather-events/">recent weather events</a> page.</li>
</ol>
<p>For more on this topic, see <a href="/noaa-weather-records-document-property-damage-mcallen/">how NOAA weather records can help document property damage</a>.</p>

<h2>Why a report near you does not prove damage</h2>
<p>Storm reports describe where observers were, not where damage occurred. Hail swaths can be narrow, wind gusts vary block by block, and many storms pass through areas with no spotter at all. A report a mile away does not prove your roof was hit, and the lack of a report does not prove it was not. Damage also depends on the age and type of roofing, siding, and other materials.</p>
<p>That is why insurers and public adjusters rely on a physical inspection. If your insurer has denied or underpaid a <a href="/services/hail-damage-claims/">hail damage claim</a> or <a href="/services/wind-damage-claims/">wind damage claim</a>, a licensed public adjuster can review the evidence with you. Coverage always depends on your policy and the facts of the loss.</p>
HTML,
];
