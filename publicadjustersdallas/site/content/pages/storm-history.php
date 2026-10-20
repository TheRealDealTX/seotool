<?php
return [
    'template'    => 'storm-history',
    'title'       => 'Dallas & Dallas County Storm History',
    'seo_title'   => 'Dallas Storm History | Dallas County Hail, Wind & Tornado Records',
    'description' => 'Search Dallas and Dallas County storm history from NOAA: hail, wind, tornado, flash flood, and winter storm records with notable North Texas events.',
    'lead'        => 'A searchable record of hail, wind, tornado, flood, and winter weather events in Dallas County from the NOAA Storm Events Database, with notable Dallas storms and tips for using the data in a claim.',
    'kicker'      => 'NOAA Storm Records',
    'image'       => '/assets/img/featured/page-storm-history.webp',
    'image_alt'   => 'Severe thunderstorm with a hail core over the Dallas skyline',
    'faqs' => [
        ['q' => 'Where does the Dallas storm history data come from?', 'a' => '<p>It comes from the NOAA National Centers for Environmental Information (NCEI) <a href="https://www.ncdc.noaa.gov/stormevents/" target="_blank" rel="noopener">Storm Events Database</a>, the official federal record of significant weather events. We include entries for Dallas County and the NWS forecast zone that covers it. Each row links to the original NCEI record.</p>'],
        ['q' => 'How current is the storm history?', 'a' => '<p>NCEI typically publishes verified events a few months after they occur, so the most recent months may be missing or preliminary. For very recent storms, check the <a href="/weather-events/">recent weather events</a> page, which shows preliminary National Weather Service reports for Dallas County.</p>'],
        ['q' => 'When is hail season in Dallas?', 'a' => '<p>In the NOAA record for Dallas County, April has the most hail reports (241 of 841), followed by May (197) and June (123), with March close behind (105). The main season runs March through June, and there is a smaller secondary bump in October (61 reports).</p>'],
        ['q' => 'Does a hail report near my home prove my roof was damaged?', 'a' => '<p>No. A report shows that hail of a certain size was observed at a certain place and time. It does not show what happened at your address. Hail swaths can be narrow, and damage depends on stone size, wind, roof age, and materials. A physical inspection is needed to document damage.</p>'],
        ['q' => 'What if there is no report for the date my property was damaged?', 'a' => '<p>Storms often cause damage where no one filed a report, especially at night. The absence of a record does not prove a storm missed your property. Try the <a href="/storm-lookup/">storm lookup tool</a> with a wider radius and date window, and rely on dated photos and an inspection.</p>'],
    ],
    'body' => <<<'HTML'
<h2>About the NOAA Storm Events Database</h2>
<p>The <a href="https://www.ncdc.noaa.gov/stormevents/" target="_blank" rel="noopener">Storm Events Database</a> is maintained by NOAA's National Centers for Environmental Information (NCEI). It is the official federal record of significant weather in the United States, compiled from National Weather Service reports. For Dallas and the rest of Dallas County, entries are prepared by the NWS Fort Worth/Dallas office.</p>
<p>Each entry generally includes:</p>
<ul>
<li><strong>Event type</strong>, such as hail, thunderstorm wind, tornado, flash flood, flood, winter storm, ice storm, or extreme cold.</li>
<li><strong>Date, time, and location.</strong> Point events like hail and wind list a nearby reference place (for example "Gribble," "Sowers," or "Bouchard") and, in recent decades, latitude and longitude. The narrative usually names the actual city or streets. Widespread events like winter storms are recorded for the county or its NWS forecast <em>zone</em> rather than a single point.</li>
<li><strong>Magnitude</strong>, such as hail size in inches, wind speed, or a tornado's EF rating. NCEI records wind in knots; this page converts it to miles per hour.</li>
<li><strong>Narratives</strong> describing what was observed, often including NWS storm survey findings.</li>
</ul>
<p>The Dallas County record on this page holds about 2,140 events from 1952 to 2026: 841 hail reports, 708 thunderstorm wind reports, 305 flash floods, 109 tornadoes, 42 lightning events, 22 floods, and a smaller number of winter storm, ice, snow, and extreme cold entries. The early decades mostly cover tornadoes, hail, and wind, often with little detail. Since the mid-1990s the database includes many more event types, coordinates, and written narratives.</p>

<h2>Notable storms in Dallas and Dallas County</h2>
<p>The table below highlights significant events in the NOAA record. Each links to an official NCEI entry. One storm often produces many separate reports, so these links point to a representative entry for each event.</p>
<table>
<thead><tr><th>Date</th><th>Event</th><th>What the NOAA record describes</th><th>Record</th></tr></thead>
<tbody>
<tr><td>April 25, 1994</td><td>F4 tornado</td><td>The Lancaster tornado was on the ground about six miles and half a mile wide, producing upper F3 to lower F4 damage; 223 homes were destroyed.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=10351936" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>June 14, 1996</td><td>Thunderstorm wind</td><td>A 115 mph gust measured at Addison Airport, the highest measured wind in the Dallas County record.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=5556565" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>May 24, 2011</td><td>Giant hail</td><td>Grapefruit-size hail up to 4.25 inches around Irving broke windows and damaged the TPC Four Seasons Las Colinas during the Byron Nelson; the same storms dropped baseball hail in Dallas near Skillman St. and Southwestern Blvd.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=306259" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>April 3, 2012</td><td>Tornado outbreak and hail</td><td>Seventeen Dallas County reports in one day, including tornadoes in Mesquite, Coppell, west Irving, and an EF2 crossing from Ellis County into Lancaster and DeSoto, plus hail up to 3 inches in Coppell.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=377596" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>December 26, 2015</td><td>EF4 tornado</td><td>The Garland and Rowlett tornado traveled a little over 13 miles, nearly 10 of them in Dallas County, crossing I-30 near the President George Bush Turnpike. An EF3 tornado struck Glenn Heights and DeSoto the same night.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=606471" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>October 20, 2019</td><td>EF3 tornado</td><td>A tornado formed in northwest Dallas near SH-348 and Luna Rd. and tracked east-northeast across I-35E and Harry Hines Blvd. through north Dallas; EF2 and EF1 tornadoes hit Garland and Rowlett the same night.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=856409" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>February 13&ndash;19, 2021</td><td>Winter Storm Uri</td><td>Extreme cold, freezing drizzle, and two rounds of snow, ice, and sleet, with low temperatures in the single digits on February 15&ndash;16.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=944869" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>May 16, 2021</td><td>Tornadoes</td><td>An EF0 tornado formed at Williams Park in Highland Park, and an EF1 tornado was recorded in the University Park area.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=961151" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>August 21&ndash;22, 2022</td><td>Flash flooding</td><td>Upwards of 15 inches of rain fell in parts of Dallas; roads, vehicles, homes, and buildings flooded, with water rescues in Balch Springs and I-635 at Scyene closed in Mesquite.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=1053557" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>February 1, 2023</td><td>Ice storm</td><td>Freezing rain with ice totals up to half an inch, highest in the southern part of the county.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=1083186" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>June 12, 2023</td><td>Giant hail</td><td>Hail up to 4 inches in diameter near Cedar Hill.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=1105878" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>May 28, 2024</td><td>Damaging straight-line winds</td><td>An NWS storm survey found winds up to 95 mph in Garland and up to 90 mph in Richardson, with a 75 mph gust at Dallas Love Field and a roof torn from a commercial building in Carrollton.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=1186742" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>January 24, 2026</td><td>Winter storm and extreme cold</td><td>Sleet and snow totals of 0.5 to 3 inches with light freezing rain, followed by wind chills as low as &minus;6&deg;F.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=1313571" target="_blank" rel="noopener">NCEI</a></td></tr>
</tbody>
</table>

<h2>Seasonal storm patterns in Dallas County</h2>
<p>The NOAA record shows a spring peak for hail and tornadoes, a late-spring to early-summer peak for damaging wind, and winter cold events that drive burst-pipe claims:</p>
<table>
<thead><tr><th>Hazard</th><th>Peak months in the NOAA record</th><th>Typical property claims</th></tr></thead>
<tbody>
<tr><td>Hail (841 reports)</td><td>April (241), May (197), June (123), March (105); secondary bump in October (61)</td><td>Roofs, skylights, siding, windows, gutters, HVAC units</td></tr>
<tr><td>Thunderstorm wind (708)</td><td>June (154), May (122), April (96)</td><td>Missing shingles, fallen trees, fences, commercial roof membranes</td></tr>
<tr><td>Tornado (109)</td><td>May (25), April (23), October (14)</td><td>Structural damage, roof decking, trees through roofs, total losses</td></tr>
<tr><td>Flash flood (305)</td><td>May (60), June (57), August (33)</td><td>Flooded slabs, garages, and vehicles (usually a flood-policy matter); roof leaks from wind-driven rain</td></tr>
<tr><td>Winter storms and cold</td><td>January&ndash;February</td><td>Burst pipes, ice-damaged trees and roofs, interior water damage</td></tr>
</tbody>
</table>
<p>Hail activity also varies widely from year to year: Dallas County logged 53 hail reports in 2012, 52 in 2011, and 51 in 2023, and 2026 already had 28 by mid-year, compared with single digits in some quieter years. For a deeper look at the spring pattern, read our <a href="/dallas-hail-season-storm-data/">Dallas hail season storm data</a> article. For tornadoes, see <a href="/tornado-damage-insurance-claims-dallas/">tornado damage insurance claims in Dallas</a>, and for flooding, <a href="/flash-flood-damage-insurance-dallas/">flash flood damage and insurance in Dallas</a>.</p>

<h2>How to use the storm record for an insurance claim</h2>
<p>An official NOAA entry can help confirm that a storm occurred on or near your date of loss, which can matter if an insurer questions when damage happened. That question comes up often in Dallas, where several hailstorms can cross the same neighborhood in one spring. To use the record well:</p>
<ol>
<li>Search by your approximate date of loss and the closest city, or use the <a href="/storm-lookup/">storm lookup tool</a> to search by distance from your city or ZIP code.</li>
<li>Open the NCEI record and save or print it. Note the date, time, location, magnitude, and narrative.</li>
<li>Keep it with your photos, inspection notes, and estimates. Our <a href="/claim-documentation-checklist/">documentation checklist</a> can help organize your claim file.</li>
<li>If the storm happened recently and is not yet in the database, check the preliminary reports on the <a href="/weather-events/">recent weather events</a> page.</li>
</ol>

<h2>Why a report near you does not prove damage</h2>
<p>Storm reports describe where observers were, not where damage occurred. Hail swaths can be narrow, wind gusts vary block by block, and many storms pass through at night with no spotter reporting. A report a mile away does not prove your roof was hit, and the lack of a report does not prove it was not. Damage also depends on the age and type of roofing, siding, and other materials.</p>
<p>That is why insurers and public adjusters rely on a physical inspection. If your insurer has denied or underpaid a <a href="/services/hail-damage-claims/">hail damage claim</a>, <a href="/services/wind-damage-claims/">wind damage claim</a>, or <a href="/services/tornado-damage-claims/">tornado damage claim</a>, a Dallas Public Adjuster can review the evidence with you. Coverage always depends on your policy and the facts of the loss.</p>
HTML,
];
