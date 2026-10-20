<?php
return [
    'template'    => 'storm-history',
    'title'       => 'San Marcos & Hays County Storm History',
    'seo_title'   => 'San Marcos Storm History | Hays County Hail & Wind Records',
    'description' => 'Search San Marcos and Hays County storm history from NOAA: hail, wind, tornado, flood, and winter storm records, notable local events, and claim tips.',
    'lead'        => 'A searchable record of hail, wind, tornado, flood, and winter weather in Hays County from the NOAA Storm Events Database, with the storms that shaped San Marcos and tips for using the data in an insurance claim.',
    'kicker'      => 'NOAA Storm Records',
    'image'       => '/assets/img/featured/page-storm-history.webp',
    'image_alt'   => 'Severe thunderstorm with a hail shaft over the Central Texas Hill Country',
    'faqs' => [
        ['q' => 'Where does this San Marcos storm history come from?', 'a' => '<p>From the NOAA National Centers for Environmental Information (NCEI) <a href="https://www.ncdc.noaa.gov/stormevents/" target="_blank" rel="noopener">Storm Events Database</a>, the official federal record of significant weather. We include entries filed for Hays County and the NWS forecast zone that covers it. Every row links to the original NCEI record.</p>'],
        ['q' => 'How up to date is the record?', 'a' => '<p>NCEI usually publishes verified events a few months after they happen, and the newest months can be partial or preliminary. For a storm in the last few weeks, check the <a href="/weather-events/">recent weather events</a> page, which lists preliminary National Weather Service reports.</p>'],
        ['q' => 'When is hail season in San Marcos?', 'a' => '<p>In the Hays County NOAA record, May has the most hail reports (67 of 180), followed by April (57) and March (23). Hail has been reported in every month except July, but March through May is the main season.</p>'],
        ['q' => 'Does a hail report near my house prove my roof was damaged?', 'a' => '<p>No. A report shows that hail of a certain size was observed at a certain place and time. It does not show what happened at your address. Hail swaths can be narrow, and damage depends on stone size, wind, and the age and type of roofing. A physical inspection is needed to document damage.</p>'],
        ['q' => 'There is no report for the day my property was damaged. Is my claim weaker?', 'a' => '<p>Not necessarily. Many storms cause damage where nobody filed a report, especially at night or in rural parts of the county. The absence of a record does not prove a storm missed your property. Try the <a href="/storm-lookup/">storm lookup tool</a> with a wider radius and date window, and lean on photos and an inspection.</p>'],
    ],
    'body' => <<<'HTML'
<h2>About the NOAA Storm Events Database</h2>
<p>The <a href="https://www.ncdc.noaa.gov/stormevents/" target="_blank" rel="noopener">Storm Events Database</a> is the official record of significant weather in the United States, maintained by NOAA’s National Centers for Environmental Information. Entries for San Marcos and the rest of Hays County are prepared by the National Weather Service Austin/San Antonio office in New Braunfels. The record on this page holds 502 Hays County events from 1953 through 2026:</p>
<table>
<thead><tr><th>Event type</th><th>Reports</th><th>Notes</th></tr></thead>
<tbody>
<tr><td>Hail</td><td>180</td><td>58 at golf-ball size (1.75") or larger; 8 at baseball size (2.75") or larger</td></tr>
<tr><td>Flash flood</td><td>127</td><td>Plus 12 river or areal flood entries</td></tr>
<tr><td>Thunderstorm wind</td><td>109</td><td>Several estimated at 75–80 mph</td></tr>
<tr><td>Tornado</td><td>31</td><td>Mostly brief EF0/EF1 or older F-scale reports</td></tr>
<tr><td>Winter storm, winter weather, ice storm</td><td>29</td><td>Recorded for the county or forecast zone, not a single point</td></tr>
<tr><td>Tropical storm and lightning</td><td>6</td><td>Including Hurricane Harvey’s remnants in August 2017</td></tr>
</tbody>
</table>
<p>Each entry lists an event type, a date and time, and a location. Point events such as hail and wind use a nearby reference name, which in Hays County is often “San Marcos Regional Airport,” “Mount Gaynor,” “Niederwald,” “Henly,” or “Fitzhugh,” even when the report came from a neighborhood several miles away. The written narrative usually names the actual spot. NCEI stores wind in knots; this page converts it to miles per hour. Older entries from the 1950s through the early 1990s are sparse, often with no narrative and no coordinates.</p>

<h2>Notable storms in San Marcos and Hays County</h2>
<p>These events stand out in the official record. One storm often produces many separate reports, so each link points to a representative entry.</p>
<table>
<thead><tr><th>Date</th><th>Event</th><th>What the record describes</th><th>Source</th></tr></thead>
<tbody>
<tr><td>Oct 17–18, 1998</td><td>Flood</td><td>NWS estimated more than 30 inches of rain over a small area south of San Marcos in 36 hours; FEMA DR-1257 included Hays County.</td><td><a href="https://www.weather.gov/ewx/wxevent-1998flood" target="_blank" rel="noopener">NWS</a></td></tr>
<tr><td>Mar 16, 2000</td><td>Giant hail</td><td>4.5-inch hail, the largest in the county record, caused widespread damage to roofs, windows, and vehicles just north of San Marcos.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=5135628" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>Apr 20, 2006</td><td>Hail and wind</td><td>4.25-inch hail with 40–50 mph gusts along I-35 from Center Point Road north to the San Marcos outlet malls.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=5496762" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>Jan 13, 2007</td><td>Thunderstorm wind</td><td>Winds estimated at 70–80 mph along I-35 in San Marcos tore metal roofs off several buildings.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=12001" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>Oct 30–31, 2013</td><td>Halloween flood</td><td>12–14 inches of rain from Wimberley to Driftwood flooded the Blanco River and Onion Creek watersheds (FEMA DR-4159).</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=481045" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>May 23–24, 2015</td><td>Memorial Day flood</td><td>The Blanco River at Wimberley rose from about 5 feet to about 41 feet in roughly four hours; the San Marcos River crested at 43.08 feet. NWS issued Flash Flood Emergencies for Wimberley and San Marcos (FEMA DR-4223).</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=581658" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>Oct 30, 2015</td><td>Flood and EF1 tornado</td><td>18.46 inches of rain in two days near Buda and 15.63 inches north of San Marcos (FEMA DR-4245); an EF1 tornado crossed into Hays County near Centerpoint Road.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=605510" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>Feb 19, 2017</td><td>EF1 tornado</td><td>A tornado beginning near RR 12 and Hugo Road in Wimberley caused considerable structural damage to a small business.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=674534" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>Apr 11, 2017</td><td>Flash flood</td><td>Up to 8 inches of rain in San Marcos closed I-35 frontage roads and led to dozens of water rescues.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=686439" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>Jun 9, 2019</td><td>Thunderstorm wind</td><td>A 75 mph gust partly peeled the metal roof off a house in San Marcos; an 80 mph gust blew a large section of roof off a house in Niederwald.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=835457" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>Jan 10, 2020</td><td>Thunderstorm wind</td><td>75 mph gusts in Kyle blew siding off a house; multiple houses had shingle damage.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=869349" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>Feb 2021</td><td>Winter Storm Uri</td><td>Ice and snow across the county, with 7.0 inches of snow west-northwest of San Marcos and widespread burst pipes (FEMA DR-4586).</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=943766" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>Jan 30–Feb 2, 2023</td><td>Ice storm</td><td>Up to half an inch of ice in Dripping Springs and about 0.38 inch in Wimberley and Driftwood (FEMA DR-4705).</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=1078570" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>May 9, 2024</td><td>Hail and wind</td><td>3-inch hail at San Marcos Academy, 2.5-inch hail near the outlet mall and near Wimberley, and 70 mph gusts that damaged roofs and downed trees in San Marcos.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=1181388" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>May 22, 2025</td><td>Hail</td><td>Baseball-size (2.75-inch) hail in Uhland and tennis-ball-size hail near Simon Middle School in Kyle.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=1264433" target="_blank" rel="noopener">NCEI</a></td></tr>
</tbody>
</table>

<h2>Seasonal storm patterns in Hays County</h2>
<table>
<thead><tr><th>Hazard</th><th>Peak months in the NOAA record</th><th>Typical property claims</th></tr></thead>
<tbody>
<tr><td>Hail (180 reports)</td><td>May (67), April (57), March (23)</td><td>Shingle and metal roofs, skylights, siding, windows, gutters, AC units</td></tr>
<tr><td>Thunderstorm wind (109)</td><td>May (35), June (25), April (13)</td><td>Lifted or missing shingles, peeled metal roofing, fallen trees, fences, carports</td></tr>
<tr><td>Flash flood and flood (139)</td><td>June (28), May (24), October (21)</td><td>Flooded homes and garages (usually a flood-policy matter), plus roof leaks from wind-driven rain</td></tr>
<tr><td>Winter storms and ice</td><td>December–February</td><td>Burst pipes, ice-loaded trees on roofs, interior water damage</td></tr>
</tbody>
</table>
<p>Hail activity swings from year to year. Hays County logged 15 hail reports in 2024, 10 in 2017, and 9 each in 2013, 2023, and 2025, while some years have only one or two. For a closer look at the spring pattern, read our <a href="/san-marcos-hail-season-storm-data/">San Marcos hail season storm data</a> article. For flooding and coverage, see <a href="/flood-damage-insurance-claims-san-marcos/">flood damage insurance claims in San Marcos</a>.</p>

<h2>Using the storm record in an insurance claim</h2>
<p>An official NOAA entry can help confirm that a storm happened on or near your date of loss, which matters when an insurer questions when the damage occurred. To put it to work:</p>
<ol>
<li>Filter the tool above by your approximate date and event type, or use the <a href="/storm-lookup/">storm lookup tool</a> to search by distance from your city or ZIP code.</li>
<li>Open the NCEI record and save or print it, keeping the date, time, location, magnitude, and narrative visible.</li>
<li>Store it with your photos, inspection notes, and estimates. The <a href="/claim-documentation-checklist/">claim documentation checklist</a> helps organize the file.</li>
<li>If the storm is too recent to appear here, check the preliminary reports on the <a href="/weather-events/">recent weather events</a> page.</li>
</ol>

<h2>Why a nearby report does not prove damage</h2>
<p>Storm reports show where observers happened to be, not where damage occurred. Hail swaths can be narrow, wind gusts vary from block to block, and many storms cross rural parts of Hays County with nobody watching. A report a mile away does not prove your roof was hit, and the lack of one does not prove it was missed. Roof age, material, and condition also affect what a given storm does to a building.</p>
<p>That is why insurers and public adjusters rely on a physical inspection. If your insurer denied or underpaid a <a href="/services/hail-damage-claims/">hail damage claim</a> or <a href="/services/wind-damage-claims/">wind damage claim</a>, a <a href="/">San Marcos public adjuster</a> can review the evidence with you. Coverage always depends on your policy and the facts of the loss.</p>
HTML,
];
