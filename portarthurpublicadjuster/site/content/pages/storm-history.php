<?php
return [
    'template'    => 'storm-history',
    'title'       => 'Port Arthur & Jefferson County Storm History',
    'seo_title'   => 'Port Arthur Storm History | Jefferson County NOAA Records',
    'description' => 'Search Port Arthur and Jefferson County storm history from NOAA: hurricane, tropical, flood, wind, hail, tornado, and freeze records with notable local storms.',
    'lead'        => 'A searchable record of hurricane, tropical storm, flood, wind, hail, tornado, and freeze events in Jefferson County from the NOAA Storm Events Database, with notable Port Arthur storms and tips for using the data in a claim.',
    'kicker'      => 'NOAA Storm Records',
    'image'       => '/assets/img/featured/page-storm-history.webp',
    'image_alt'   => 'Hurricane rain bands over the Southeast Texas coast near Port Arthur',
    'faqs' => [
        ['q' => 'Where does the Port Arthur storm history data come from?', 'a' => '<p>It comes from the NOAA National Centers for Environmental Information (NCEI) <a href="https://www.ncdc.noaa.gov/stormevents/" target="_blank" rel="noopener">Storm Events Database</a>, the official federal record of significant weather events. We include entries for Jefferson County and the NWS forecast zones that cover it. Each row links to the original NCEI record.</p>'],
        ['q' => 'How current is the storm history?', 'a' => '<p>NCEI typically publishes verified events a few months after they occur, and the most recent year may be partial or preliminary. For very recent storms, check the <a href="/weather-events/">recent weather events</a> page, which shows preliminary National Weather Service reports.</p>'],
        ['q' => 'When is hurricane season in Port Arthur?', 'a' => '<p>The Atlantic hurricane season runs June 1 through November 30, according to the National Hurricane Center, with peak activity from mid-August through September. Rita, Ike, Harvey, Imelda, and Laura all affected Southeast Texas between late August and late September.</p>'],
        ['q' => 'Does a storm report near my home prove my property was damaged?', 'a' => '<p>No. A report shows that weather of a certain type and strength was observed at a certain place and time. It does not show what happened at your address. Wind, hail, and rainfall can vary sharply over short distances, and damage depends on the building\'s age, materials, and condition. A physical inspection is needed to document damage.</p>'],
        ['q' => 'What if there is no report for the date my property was damaged?', 'a' => '<p>Storms often cause damage where no one filed a report, especially at night or during a hurricane when spotters are sheltering. Widespread tropical events are often logged for a whole county or forecast zone rather than a point. Try the <a href="/storm-lookup/">storm lookup tool</a> with a wider radius and date window, and rely on photos and an inspection.</p>'],
    ],
    'body' => <<<'HTML'
<h2>About the NOAA Storm Events Database</h2>
<p>The <a href="https://www.ncdc.noaa.gov/stormevents/" target="_blank" rel="noopener">Storm Events Database</a> is maintained by NOAA's National Centers for Environmental Information (NCEI). It is the official federal record of significant weather in the United States, compiled from National Weather Service reports. For Port Arthur and the rest of Jefferson County, entries are prepared by the NWS office in Lake Charles, Louisiana, which serves Southeast Texas and Southwest Louisiana.</p>
<p>Each entry generally includes:</p>
<ul>
<li><strong>Event type</strong>, such as hurricane, tropical storm, storm surge, flash flood, flood, heavy rain, thunderstorm wind, hail, tornado, or frost/freeze.</li>
<li><strong>Date, time, and location.</strong> Point events like hail and wind usually list a nearby place name and, in recent decades, latitude and longitude. Widespread events like hurricanes, tropical storms, and freezes are recorded for a <em>county</em> or an NWS <em>forecast zone</em> rather than a single point.</li>
<li><strong>Magnitude</strong>, such as hail size in inches or wind speed. NCEI records wind in knots; this page converts it to miles per hour.</li>
<li><strong>Narratives</strong> describing what was observed, sometimes including NWS storm survey findings.</li>
</ul>
<p>Records begin in 1950. The early decades mostly cover tornadoes, hail, and thunderstorm wind, often with little detail. Since the mid-1990s the database includes many more event types, coordinates, and written narratives, so recent events are documented in much greater depth.</p>

<h2>Notable storms in Port Arthur and Jefferson County</h2>
<p>The table below highlights several significant tropical events that affected Port Arthur and Southeast Texas, with links to official National Hurricane Center and National Weather Service summaries. You can find the related county and zone entries in the searchable record above.</p>
<table>
<thead><tr><th>Date</th><th>Event</th><th>What the official record describes</th><th>Source</th></tr></thead>
<tbody>
<tr><td>September 24, 2005</td><td>Hurricane Rita</td><td>Category 3 landfall near the Texas&ndash;Louisiana border in the Sabine Pass / Johnson's Bayou area, with widespread wind damage across Southeast Texas, including Port Arthur.</td><td><a href="https://www.nhc.noaa.gov/data/tcr/AL182005_Rita.pdf" target="_blank" rel="noopener">NHC report</a></td></tr>
<tr><td>September 13, 2007</td><td>Hurricane Humberto</td><td>Landfall near High Island; wind damage in the Port Arthur and Beaumont area.</td><td><a href="https://www.nhc.noaa.gov/data/tcr/AL092007_Humberto.pdf" target="_blank" rel="noopener">NHC report</a></td></tr>
<tr><td>September 13, 2008</td><td>Hurricane Ike</td><td>Category 2 landfall at Galveston; large storm surge along the upper Texas coast, including Sabine Pass and low-lying parts of Jefferson County, plus wind damage across the region.</td><td><a href="https://www.nhc.noaa.gov/data/tcr/AL092008_Ike.pdf" target="_blank" rel="noopener">NHC report</a></td></tr>
<tr><td>August 24&ndash;31, 2017</td><td>Hurricane Harvey</td><td>Widespread storm totals over 40 inches in Jefferson County; 60.58 inches near Nederland, a U.S. tropical cyclone rainfall record at the time; more than 64,000 homes flooded in the county; Port Arthur, Groves, and northeast Beaumont among the hardest hit.</td><td><a href="https://www.weather.gov/lch/2017Harvey" target="_blank" rel="noopener">NWS Lake Charles</a></td></tr>
<tr><td>September 17&ndash;19, 2019</td><td>Tropical Storm Imelda</td><td>Extreme rainfall, preliminarily more than 40 inches in parts of Jefferson County, and widespread flash flooding across Southeast Texas, including the Port Arthur and Beaumont areas.</td><td><a href="https://www.nhc.noaa.gov/data/tcr/AL112019_Imelda.pdf" target="_blank" rel="noopener">NHC report</a></td></tr>
<tr><td>August 27, 2020</td><td>Hurricane Laura</td><td>Category 4 landfall near Cameron, Louisiana, about 30 miles east of the Texas border; damaging winds in eastern Jefferson and Orange counties, with numerous trees and power lines down.</td><td><a href="https://www.weather.gov/lch/2020Laura" target="_blank" rel="noopener">NWS Lake Charles</a></td></tr>
<tr><td>October 9, 2020</td><td>Hurricane Delta</td><td>Landfall near Creole, Louisiana, six weeks after Laura, affecting the same region again.</td><td><a href="https://www.nhc.noaa.gov/data/tcr/AL262020_Delta.pdf" target="_blank" rel="noopener">NHC report</a></td></tr>
<tr><td>February 2021</td><td>Winter storm</td><td>A prolonged freeze across Texas that caused burst pipes and interior water damage statewide.</td><td>See freeze entries in the record above</td></tr>
</tbody>
</table>

<h2>Seasonal storm patterns in Jefferson County</h2>
<p>Port Arthur's weather risks follow the calendar. Use the filters above to see how the record breaks down by month for each event type.</p>
<ul>
<li><strong>Hurricane season (June 1&ndash;November 30):</strong> the main source of large wind, surge, and rainfall losses, peaking from mid-August through September.</li>
<li><strong>Spring and summer thunderstorms:</strong> straight-line winds, occasional hail, and brief tornadoes, including tornadoes embedded in tropical rain bands.</li>
<li><strong>Heavy rain events year-round:</strong> slow-moving systems like Harvey and Imelda showed that extreme rainfall flooding can happen far from the shoreline, inside the levee system.</li>
<li><strong>Winter:</strong> occasional hard freezes, like February 2021, that can burst pipes in homes not built for prolonged cold.</li>
</ul>
<p>For a deeper look at past storms, read <a href="/port-arthur-hurricane-history-insurance-lessons/">Port Arthur hurricane history and insurance lessons</a>.</p>

<h2>How to use the storm record for an insurance claim</h2>
<p>An official NOAA entry can help confirm that a storm occurred on or near your date of loss, which can be important if an insurer questions when damage happened or whether it was caused by wind or water. To use it well:</p>
<ol>
<li>Search by your approximate date of loss and the closest city name, or use the <a href="/storm-lookup/">storm lookup tool</a> to search by distance from your city or ZIP code.</li>
<li>Open the NCEI record and save or print it. Note the date, time, location, magnitude, and narrative.</li>
<li>Keep it with your photos, inspection notes, and estimates. Our <a href="/claim-documentation-checklist/">documentation checklist</a> can help organize your claim file.</li>
<li>If the storm happened recently and is not yet in the database, check the preliminary reports on the <a href="/weather-events/">recent weather events</a> page.</li>
</ol>
<p>See also <a href="/how-to-document-storm-damage-port-arthur/">how to document storm damage in Port Arthur</a>.</p>

<h2>Why a report near you does not prove damage</h2>
<p>Storm reports describe where observers were, not where damage occurred. Wind gusts vary block by block, rainfall totals can differ by many inches across the county, and many storms pass through areas with no spotter at all. A report a mile away does not prove your roof was hit, and the lack of a report does not prove it was not. Damage also depends on the age and type of roofing, siding, and other materials.</p>
<p>That is why insurers and public adjusters rely on a physical inspection. If your insurer has denied or underpaid a <a href="/services/hurricane-damage-claims/">hurricane damage claim</a> or <a href="/services/wind-damage-claims/">wind damage claim</a>, a licensed public adjuster can review the evidence with you. Coverage always depends on your policy and the facts of the loss.</p>
HTML,
];
