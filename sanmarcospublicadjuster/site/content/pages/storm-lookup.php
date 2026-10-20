<?php
return [
    'template'    => 'storm-lookup',
    'title'       => 'Storm Event Lookup for San Marcos-Area Properties',
    'seo_title'   => 'Storm Event Lookup | Hail & Wind Reports Near San Marcos',
    'description' => 'Storm event lookup for San Marcos and Hays County: search NOAA and NWS hail, wind, tornado, and flood reports near your city or ZIP code by date.',
    'lead'        => 'Search official NOAA and National Weather Service storm reports near a San Marcos-area city or ZIP code to see what was recorded around your date of loss.',
    'kicker'      => 'Interactive Tool',
    'image'       => '/assets/img/featured/page-storm-lookup.webp',
    'image_alt'   => 'Map of storm report locations around San Marcos and Hays County, Texas',
    'faqs' => [
        ['q' => 'Do I have to enter my street address?', 'a' => '<p>No. The lookup works from the center point of the city or ZIP code you enter, such as San Marcos or 78666. We do not ask for or store street addresses. Remember that distances are measured from that center point, not from your property.</p>'],
        ['q' => 'What records does the storm lookup search?', 'a' => '<p>Two sets: the verified NOAA NCEI Storm Events Database for Hays County, and preliminary Local Storm Reports from the National Weather Service Austin/San Antonio office. County- and zone-wide events such as winter storms and tropical storms are included when your date or date range matches them.</p>'],
        ['q' => 'My property is in Lockhart, Martindale, Seguin, or New Braunfels. Will this work?', 'a' => '<p>Partly. The verified history covers Hays County, so Hays County reports inside your radius will show up, and preliminary reports near the county line may too. Events recorded only in Caldwell, Guadalupe, or Comal County are not in this dataset. For those, search the <a href="https://www.ncdc.noaa.gov/stormevents/" target="_blank" rel="noopener">NOAA Storm Events Database</a> by county.</p>'],
        ['q' => 'Why did my search come back empty?', 'a' => '<p>Widen the radius, lengthen the date window, or switch the event type to “Hail, wind &amp; more.” If nothing appears, it may simply mean nobody reported that storm. Plenty of storms cause damage without an official report, so an empty result does not show your property was unaffected.</p>'],
        ['q' => 'Will a matching report get my claim paid?', 'a' => '<p>No report or tool can guarantee a claim outcome. A nearby report is supporting evidence that a storm happened. Your insurer still evaluates the physical damage, its cause, and your policy terms.</p>'],
    ],
    'body' => <<<'HTML'
<h2>How the storm event lookup works</h2>
<p>This storm event lookup lets San Marcos and Hays County property owners pull official weather reports for a place and a date. Type a city or ZIP code, choose a radius, and add an approximate date of loss if you have one. The tool measures from the <strong>center point</strong> of that city or ZIP code to every report that has coordinates and returns the ones that fall inside your radius, along with any county-wide events that match your dates.</p>
<p>Two sources feed the results:</p>
<ul>
<li><strong>NOAA NCEI Storm Events Database.</strong> The verified federal record, usually published a few months after a storm. For Hays County it holds about 500 events from 1953 to 2026, including 180 hail reports, 109 thunderstorm wind reports, 31 tornadoes, and 127 flash floods. Browse it in full on the <a href="/storm-history/">storm history</a> page.</li>
<li><strong>NWS Local Storm Reports.</strong> Preliminary reports from NWS Austin/San Antonio, often posted within hours. The newest ones also appear on the <a href="/weather-events/">recent weather events</a> page.</li>
</ul>

<h2>Search tips for San Marcos-area storms</h2>
<ul>
<li><strong>Use a ±7-day window first.</strong> Most people remember the week of a storm better than the exact day, and a storm that hits late at night may be logged under the next date.</li>
<li><strong>Search the whole spring if you found damage late.</strong> In the Hays County record, May (67) and April (57) account for about two-thirds of all hail reports, and busy years can log many reports (15 in 2024). A date range from March through June is a reasonable starting point.</li>
<li><strong>Widen the radius west of I-35.</strong> Reports cluster where people live and drive. For a property in the Hill Country toward Wimberley or Driftwood, or in rural areas near Redwood or Uhland, try 10 or 20 miles.</li>
<li><strong>Read the narrative, not just the place name.</strong> NOAA uses reference points such as “San Marcos Regional Airport,” “Mount Gaynor,” or “Niederwald.” The narrative usually tells you where the report actually came from, for example “near the outlet mall” or “San Marcos Academy west of the city.”</li>
<li><strong>Filter by type</strong> once you know what you are looking for: hail for dents and bruised shingles, wind for missing shingles, peeled metal roofing, or fallen trees.</li>
</ul>

<h2>Example: what a strong match looks like</h2>
<p>On May 9, 2024, NOAA logged <a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=1181388" target="_blank" rel="noopener">3-inch hail at San Marcos Academy west of the city</a>, <a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=1181409" target="_blank" rel="noopener">2.5-inch hail near the outlet mall</a>, and <a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=1181414" target="_blank" rel="noopener">70 mph gusts that damaged a church roof in San Marcos</a>. A search on San Marcos with a 5-mile radius and that date would return several reports with sizes, times, and narratives you could save to a claim file. Not every storm leaves that kind of trail, which is why the next two sections matter.</p>

<h2>Saving what you find</h2>
<p>When a report lines up with your date and area, open the NCEI link or note the NWS report details, then screenshot or print it with the date, time, location, magnitude, and source visible. File it with:</p>
<ul>
<li>Dated photos and video of the damage, ideally from before any cleanup.</li>
<li>Your notes on when the storm hit and what you saw or heard.</li>
<li>The claim number, adjuster contacts, and your communication log.</li>
<li>Estimates and receipts for emergency work such as tarping or water extraction.</li>
</ul>
<p>The <a href="/claim-documentation-checklist/">claim documentation checklist</a> walks through the rest, and our article on <a href="/san-marcos-hail-season-storm-data/">San Marcos hail season storm data</a> puts the local record in context.</p>

<h2>Limits of storm reports</h2>
<p>A report shows that weather was observed at a place and time. It is <strong>not proof that your property was damaged</strong>, and it does not decide coverage. Hail swaths can be a few blocks wide, and wind can vary sharply over short distances, so a report three miles away may not reflect conditions at your building. The reverse is just as true: many damaging storms are never reported at all.</p>
<p>Preliminary NWS sizes, speeds, and locations can be estimates that are later revised, and every distance here is measured from a city or ZIP center rather than your address. Treat these records as one piece of evidence alongside a physical inspection. If your insurer questions the date or cause of the damage, a <a href="/">San Marcos public adjuster</a> can help review the evidence; see our <a href="/services/hail-damage-claims/">hail damage claims</a> and <a href="/services/storm-damage-claims/">storm damage claims</a> pages.</p>
HTML,
];
