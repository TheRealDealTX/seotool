<?php
return [
    'template'    => 'storm-history',
    'title'       => 'San Antonio & Bexar County Storm History',
    'seo_title'   => 'San Antonio Storm History | Bexar County Hail & Wind Records',
    'description' => 'Search San Antonio and Bexar County storm history from NOAA: hail, wind, tornado, flash flood, and winter storm records with notable local events.',
    'lead'        => 'A searchable record of hail, wind, tornado, flood, and winter weather events in Bexar County from the NOAA Storm Events Database, with notable San Antonio storms and tips for using the data in a claim.',
    'kicker'      => 'NOAA Storm Records',
    'image'       => '/assets/img/featured/page-storm-history.webp',
    'image_alt'   => 'Severe thunderstorm with a hail core over San Antonio',
    'faqs' => [
        ['q' => 'Where does the San Antonio storm history data come from?', 'a' => '<p>It comes from the NOAA National Centers for Environmental Information (NCEI) <a href="https://www.ncdc.noaa.gov/stormevents/" target="_blank" rel="noopener">Storm Events Database</a>, the official federal record of significant weather events. We include entries for Bexar County and the NWS forecast zone that covers it. Each row links to the original NCEI record.</p>'],
        ['q' => 'How current is the storm history?', 'a' => '<p>NCEI typically publishes verified events a few months after they occur, and the most recent months may be partial or preliminary. For very recent storms, check the <a href="/weather-events/">recent weather events</a> page, which shows preliminary National Weather Service reports.</p>'],
        ['q' => 'When is hail season in San Antonio?', 'a' => '<p>In the NOAA record for Bexar County, April has the most hail reports (225 of 618), followed by May (160) and March (117). Hail can fall in any month, but March through May is the main season.</p>'],
        ['q' => 'Does a hail report near my home prove my roof was damaged?', 'a' => '<p>No. A report shows that hail of a certain size was observed at a certain place and time. It does not show what happened at your address. Hail swaths can be narrow, and damage depends on stone size, wind, roof age, and materials. A physical inspection is needed to document damage.</p>'],
        ['q' => 'What if there is no report for the date my property was damaged?', 'a' => '<p>Storms often cause damage where no one filed a report, especially at night or in less populated parts of the county. The absence of a record does not prove a storm did not affect your property. Try the <a href="/storm-lookup/">storm lookup tool</a> with a wider radius and date window, and rely on photos and an inspection.</p>'],
    ],
    'body' => <<<'HTML'
<h2>About the NOAA Storm Events Database</h2>
<p>The <a href="https://www.ncdc.noaa.gov/stormevents/" target="_blank" rel="noopener">Storm Events Database</a> is maintained by NOAA's National Centers for Environmental Information (NCEI). It is the official federal record of significant weather in the United States, compiled from National Weather Service reports. For San Antonio and the rest of Bexar County, entries are prepared by the NWS Austin/San Antonio office in New Braunfels.</p>
<p>Each entry generally includes:</p>
<ul>
<li><strong>Event type</strong>, such as hail, thunderstorm wind, tornado, flash flood, flood, winter storm, or extreme cold.</li>
<li><strong>Date, time, and location.</strong> Point events like hail and wind list a nearby reference place (for example "Leon Vly," "Grey Forest," or "Kirby") and, in recent decades, latitude and longitude. The narrative often names the actual streets. Widespread events like winter storms are recorded for the county or its NWS forecast <em>zone</em> rather than a single point.</li>
<li><strong>Magnitude</strong>, such as hail size in inches or wind speed. NCEI records wind in knots; this page converts it to miles per hour.</li>
<li><strong>Narratives</strong> describing what was observed, sometimes including NWS storm survey findings.</li>
</ul>
<p>The Bexar County record on this page holds about 1,525 events from the 1950s to 2026: 618 hail reports, 420 flash floods, 309 thunderstorm wind reports, 71 tornadoes, 45 floods, and a smaller number of winter storm, ice, and extreme cold entries. The early decades mostly cover tornadoes, hail, and thunderstorm wind, often with little detail. Since the mid-1990s the database includes many more event types, coordinates, and written narratives.</p>

<h2>Notable storms in San Antonio and Bexar County</h2>
<p>The table below highlights significant events in the NOAA record. Each links to an official NCEI entry. One storm often produces many separate reports, so these links point to a representative entry for each event.</p>
<table>
<thead><tr><th>Date</th><th>Event</th><th>What the NOAA record describes</th><th>Record</th></tr></thead>
<tbody>
<tr><td>May 27, 1997</td><td>Downburst</td><td>Severe downburst winds estimated in excess of 100 mph across much of southwest San Antonio near Kelly AFB, damaging roofs, outbuildings, windows, signs, and trees; power was out for over 100,000 people.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=5599060" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>October 17, 1998</td><td>River flooding</td><td>Major flooding on the San Antonio River, Medina River, and Olmos, Leon, Helotes, Salado, and Cibolo creeks; several homes below Loop 410 had 10 feet of water over the slabs.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=5672611" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>May 6, 2001</td><td>Hail and wind</td><td>Described as one of the most devastating hail-and-wind storms in Bexar County history: hail up to 4 inches with winds over 60 mph destroyed roofs of hundreds of homes, worst in northwest San Antonio.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=5243267" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>March 19, 2002</td><td>Tornadoes</td><td>Six tornadoes in southern Bexar County near Von Ormy and Somerset; the strongest, a minimal F2, destroyed four mobile homes.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=5285553" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>May 25, 2013</td><td>Flash flood</td><td>Record rainfall: San Antonio International Airport recorded 9.87 inches, most of it in about six hours, with widespread flash flooding.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=453032" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>April 12, 2016</td><td>Giant hail</td><td>Hail to 4.5 inches near Tezel Rd. and Bandera Rd., tied at the time for the largest hailstone reported in Bexar County; the storm crossed the northern half of San Antonio and is widely reported as one of the costliest hailstorms in Texas history.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=623870" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>February 19, 2017</td><td>EF2 tornado</td><td>A tornado formed near San Pedro Ave. and strengthened to EF2 along Linda Dr. and Sharon Dr. with peak winds near 120 mph; a few homes had their roofs completely removed.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=674529" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>August 26, 2017</td><td>Hurricane Harvey remnants</td><td>Harvey weakened to a tropical storm as it moved inland east of Bexar County; the county is recorded under a tropical storm entry.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=720275" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>February 13&ndash;18, 2021</td><td>Winter Storm Uri</td><td>Ice, snow, and extreme cold, with wind chills of -5 to -10&deg;F across Bexar County.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=943791" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>May 3, 2021</td><td>Record hail</td><td>5.5-inch hail near Sayers and the China Grove area on the east side of San Antonio, the largest in the county record, and 4.5-inch hail near I-410 and Paula Dr.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=961040" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>May 28, 2021</td><td>Thunderstorm wind</td><td>A 77 mph gust measured at San Antonio International Airport; estimated 80 mph winds knocked a large tree through a home in Alamo Heights.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=961392" target="_blank" rel="noopener">NCEI</a></td></tr>
<tr><td>January 24, 2026</td><td>Ice storm</td><td>Freezing rain left 0.14 inch of ice at San Antonio International Airport, followed by wind chills down to 9&deg;F.</td><td><a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=1314172" target="_blank" rel="noopener">NCEI</a></td></tr>
</tbody>
</table>

<h2>Seasonal storm patterns in Bexar County</h2>
<p>The NOAA record shows a clear spring peak for hail and a broader season for wind and flooding:</p>
<table>
<thead><tr><th>Hazard</th><th>Peak months in the NOAA record</th><th>Typical property claims</th></tr></thead>
<tbody>
<tr><td>Hail (618 reports)</td><td>April (225), May (160), March (117)</td><td>Roofs, skylights, siding, windows, gutters, HVAC units</td></tr>
<tr><td>Thunderstorm wind (309)</td><td>May (92), June (41), April (40)</td><td>Missing shingles, fallen trees, fences, carports, metal buildings</td></tr>
<tr><td>Flash flood (420)</td><td>June (93), May (72), September (48), October (46)</td><td>Flooded slabs and garages (usually a flood-policy matter), roof leaks from wind-driven rain</td></tr>
<tr><td>Winter storms and cold</td><td>January&ndash;February</td><td>Burst pipes, ice-damaged trees and roofs, interior water damage</td></tr>
</tbody>
</table>
<p>Hail activity also varies a lot from year to year: Bexar County logged 63 hail reports in 2016, 45 in both 2021 and 2023, and 34 in 2025, compared with single digits in some quieter years. For a deeper look at the spring pattern, read our <a href="/san-antonio-hail-season-storm-data/">San Antonio hail season storm data</a> article. For flooding, see <a href="/flash-flood-damage-insurance-san-antonio/">flash flood damage and insurance in San Antonio</a>.</p>

<h2>How to use the storm record for an insurance claim</h2>
<p>An official NOAA entry can help confirm that a storm occurred on or near your date of loss, which can be important if an insurer questions when damage happened. To use it well:</p>
<ol>
<li>Search by your approximate date of loss and the closest place name, or use the <a href="/storm-lookup/">storm lookup tool</a> to search by distance from your city or ZIP code.</li>
<li>Open the NCEI record and save or print it. Note the date, time, location, magnitude, and narrative.</li>
<li>Keep it with your photos, inspection notes, and estimates. Our <a href="/claim-documentation-checklist/">documentation checklist</a> can help organize your claim file.</li>
<li>If the storm happened recently and is not yet in the database, check the preliminary reports on the <a href="/weather-events/">recent weather events</a> page.</li>
</ol>

<h2>Why a report near you does not prove damage</h2>
<p>Storm reports describe where observers were, not where damage occurred. Hail swaths can be narrow, wind gusts vary block by block, and many storms pass through areas with no spotter at all. A report a mile away does not prove your roof was hit, and the lack of a report does not prove it was not. Damage also depends on the age and type of roofing, siding, and other materials.</p>
<p>That is why insurers and public adjusters rely on a physical inspection. If your insurer has denied or underpaid a <a href="/services/hail-damage-claims/">hail damage claim</a> or <a href="/services/wind-damage-claims/">wind damage claim</a>, a licensed public adjuster can review the evidence with you. Coverage always depends on your policy and the facts of the loss.</p>
HTML,
];
