<?php
return [
    'template'      => 'weather',
    'title'         => 'Live San Marcos Weather',
    'seo_title'     => 'San Marcos, TX Weather Today: Live Conditions & Alerts',
    'description'   => 'Live San Marcos, TX weather from the National Weather Service: current KHYI conditions, 7-day forecast, alerts, and seasonal storm prep for Hays County.',
    'lead'          => 'Current conditions at San Marcos Regional Airport, the official 7-day forecast, and active National Weather Service alerts, plus a season-by-season storm prep guide for Hays County property owners.',
    'kicker'        => 'Live Weather',
    'image'         => '/assets/img/featured/page-weather.webp',
    'image_alt'     => 'Storm clouds building over the Texas Hill Country near San Marcos',
    'hide_hero_cta' => false,
    'faqs' => [
        ['q' => 'Where does the San Marcos weather on this page come from?', 'a' => '<p>Everything comes from the National Weather Service public data service at <a href="https://www.weather.gov/" target="_blank" rel="noopener">weather.gov</a>. Current conditions are the latest observation from the automated station at San Marcos Regional Airport (KHYI). The forecast, watches, and warnings are issued by the <a href="https://www.weather.gov/ewx/" target="_blank" rel="noopener">NWS Austin/San Antonio office</a> in New Braunfels, which covers San Marcos and the rest of Hays County.</p>'],
        ['q' => 'Why does this page sometimes disagree with my phone’s weather app?', 'a' => '<p>Many apps blend computer models or use a different station or a neighborhood sensor. This page shows the official NWS reading at the San Marcos airport and the official NWS forecast. During thunderstorms, conditions at the airport east of I-35 can be very different from conditions in a neighborhood on the west side of town or out toward Wimberley.</p>'],
        ['q' => 'What is the difference between a watch and a warning?', 'a' => '<p>A <strong>watch</strong> means conditions are favorable for a hazard such as severe storms or flash flooding to develop, so be ready. A <strong>warning</strong> means the hazard is happening, imminent, or likely in the warned area, so act now. A Flash Flood Emergency is the most serious flood warning the NWS issues.</p>'],
        ['q' => 'Does a severe weather warning mean my insurance claim will be paid?', 'a' => '<p>No. Warnings and storm reports describe what weather was expected or observed in an area. Coverage depends on your policy terms, exclusions, and deductibles, and on evidence of actual damage to your property. Weather records are useful supporting documentation, not a coverage decision.</p>'],
        ['q' => 'How often does the weather page refresh?', 'a' => '<p>Current conditions refresh about every 10 minutes, the forecast about every 30 minutes, and alerts about every 5 minutes. If the NWS service is briefly unavailable, the page shows the most recent data it received and says so.</p>'],
    ],
    'body' => <<<'HTML'
<h2>Reading the San Marcos weather data</h2>
<p>The live San Marcos weather shown above comes straight from the <a href="https://www.weather.gov/" target="_blank" rel="noopener">National Weather Service</a>. The “now” panel is the latest automated observation from <strong>San Marcos Regional Airport (KHYI)</strong> on the east side of the city. The forecast and any watches, warnings, or advisories come from <strong>NWS Austin/San Antonio</strong>, the forecast office in New Braunfels that covers San Marcos, Hays County, and most of the I-35 corridor between the two big metros.</p>
<ul>
<li><strong>One station, one spot.</strong> A thunderstorm can drop hail on a subdivision off Wonder World Drive and leave the airport dry, or the reverse. Treat the airport reading as a reference point, not a reading for your street.</li>
<li><strong>Central Time.</strong> Observation and alert times are shown in local time.</li>
<li><strong>Read the full alert.</strong> Each alert explains the hazard, the area, and when it expires. Pay special attention to flash flood warnings: San Marcos sits on the Balcones Escarpment in what is known as “Flash Flood Alley,” and water can rise fast on the Blanco River, the San Marcos River, and local creeks.</li>
</ul>

<h2>Storm preparation by season in Hays County</h2>
<p>The NOAA Storm Events record for Hays County shows clear seasonal patterns. Preparing ahead of each season can limit damage and makes any later claim easier to document.</p>
<table>
<thead><tr><th>Season</th><th>Main hazards</th><th>What the NOAA record shows</th></tr></thead>
<tbody>
<tr><td>March–June</td><td>Hail and damaging thunderstorm wind</td><td>Hail peaks in May (67 reports) and April (57); wind reports peak in May (35) and June (25)</td></tr>
<tr><td>May–June and September–November</td><td>Flash flooding and river flooding</td><td>Flood reports peak in June (28), May (24), and October (21)</td></tr>
<tr><td>December–February</td><td>Hard freezes, ice, and occasional snow</td><td>Winter Storm Uri (February 2021), the January–February 2023 ice storm, and freezing rain as recently as January 2026</td></tr>
</tbody>
</table>

<h3>Spring: hail and wind</h3>
<p>Hays County’s largest recorded hailstone, 4.5 inches, fell <a href="https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=5135628" target="_blank" rel="noopener">just north of San Marcos on March 16, 2000</a>, and on May 9, 2024 hail up to 3 inches fell west of the city while 70 mph gusts damaged roofs and downed trees. Before spring:</p>
<ul>
<li>Take dated “before” photos and video of the roof, siding, windows, skylights, gutters, fences, and HVAC units. They help separate new storm damage from older wear.</li>
<li>Trim dead or overhanging limbs, especially from large live oaks and cedar elms near the house.</li>
<li>Secure or store patio furniture, trampolines, and other items that can become projectiles.</li>
<li>Look up your wind/hail deductible on the declarations page. On many Texas policies it is a percentage of the dwelling limit.</li>
</ul>

<h3>Late spring and fall: flash floods</h3>
<p>The Memorial Day flood of May 2015 and the October 2015 flood both brought FEMA disaster declarations to Hays County, and the October 1998 flood dropped an estimated 30-plus inches over a small area south of San Marcos. When heavy rain is in the forecast:</p>
<ul>
<li>Follow NWS and local emergency instructions first. Never drive into a flooded low water crossing.</li>
<li>Clean gutters, downspouts, and yard drains, and move valuables off lower floors and out of garages.</li>
<li>Keep digital copies of your policy, a home inventory, and key phone numbers.</li>
<li>Know what your coverage does and does not include. Standard homeowners and commercial policies generally exclude flood; flood coverage comes from the National Flood Insurance Program or a private flood policy, and NFIP policies usually have a 30-day waiting period (<a href="https://www.floodsmart.gov/" target="_blank" rel="noopener">floodsmart.gov</a>). New FEMA flood maps for San Marcos took effect January 17, 2025, so it is worth checking your zone again.</li>
</ul>

<h3>Winter: freezes and ice</h3>
<p>During Winter Storm Uri in February 2021, 7.0 inches of snow fell west-northwest of San Marcos and burst pipes were widespread across the region. When a hard freeze is forecast:</p>
<ul>
<li>Insulate exposed pipes, hose bibs, and backflow devices, and disconnect garden hoses.</li>
<li>Let faucets on exterior walls drip and open sink cabinet doors to let warm air reach the pipes.</li>
<li>Find your main water shutoff before you need it, and make sure everyone in the house knows where it is.</li>
<li>If you leave town, keep the heat on and consider shutting off and draining the water supply.</li>
</ul>

<h2>What to do after a storm</h2>
<ol>
<li><strong>Stay safe.</strong> Keep away from downed lines, floodwater, and damaged structures, and report outages to your electric provider. Do not climb onto a wet or damaged roof.</li>
<li><strong>Document before cleanup.</strong> Take wide shots and close-ups of every damaged area. If you can do it safely, photograph hailstones next to a coin or ruler.</li>
<li><strong>Prevent more damage.</strong> Most policies expect reasonable protective steps, such as tarping a roof, boarding a window, or extracting water. Keep the receipts.</li>
<li><strong>Report the claim promptly.</strong> Write down the claim number and start a log of every call and email.</li>
<li><strong>Save the weather record.</strong> Note the date and time of the storm and save any alerts you received. Then check the <a href="/weather-events/">recent weather events</a> page for preliminary NWS reports, or search by city or ZIP code with the <a href="/storm-lookup/">storm lookup tool</a>.</li>
</ol>
<p>The <a href="/claim-documentation-checklist/">claim documentation checklist</a> covers what to gather for each type of loss. If an insurer disputes or underpays a storm claim, a <a href="/">San Marcos public adjuster</a> can help; see our <a href="/services/storm-damage-claims/">storm damage claims</a> page.</p>

<h2>Looking back at past storms</h2>
<p>For storms that already happened, the <a href="/storm-history/">Hays County storm history</a> page lets you filter the NOAA record by date, event type, hail size, and wind speed. Our article on <a href="/san-marcos-hail-season-storm-data/">San Marcos hail season storm data</a> explains the spring pattern in more depth. Official records support a claim, but they never prove that a particular building was damaged; a physical inspection is still needed.</p>
HTML,
];
