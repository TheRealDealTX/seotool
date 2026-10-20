<?php
return [
    'template'      => 'weather',
    'title'         => 'Live Dallas Weather',
    'seo_title'     => 'Dallas Weather Today: Live Conditions, Forecast & Alerts',
    'description'   => 'Live Dallas weather from the National Weather Service: current conditions at Dallas Love Field (KDAL), a 7-day forecast, alerts, and storm prep tips.',
    'lead'          => 'Real-time National Weather Service data for Dallas: current conditions, active alerts, and the 7-day forecast, plus practical storm preparation and post-storm guidance for property owners.',
    'kicker'        => 'Live Weather',
    'image'         => '/assets/img/featured/page-weather.webp',
    'image_alt'     => 'Storm clouds building over the Dallas skyline',
    'hide_hero_cta' => false,
    'faqs' => [
        ['q' => 'Where does the Dallas weather data on this page come from?', 'a' => '<p>All data comes from the National Weather Service through its public API at <a href="https://www.weather.gov/" target="_blank" rel="noopener">weather.gov</a>. Current conditions are the latest observation from the station at Dallas Love Field (KDAL). The forecast and alerts are issued by the NWS Fort Worth/Dallas office, which serves Dallas County and much of North Texas.</p>'],
        ['q' => 'Why might this page differ from my phone’s weather app?', 'a' => '<p>Many weather apps use their own models, blend several data sources, or report from a different station, such as DFW Airport, or a neighborhood sensor. This page shows the official NWS observation at Love Field and the official NWS forecast. Conditions can also vary a lot across short distances during thunderstorms, and each source updates on its own schedule.</p>'],
        ['q' => 'What is the difference between a watch and a warning?', 'a' => '<p>The National Weather Service issues a <strong>watch</strong> when conditions are favorable for hazardous weather to develop, so you should be prepared. It issues a <strong>warning</strong> when hazardous weather is occurring, imminent, or likely, so you should take action to protect yourself now.</p>'],
        ['q' => 'Does a severe weather warning mean my insurance claim will be covered?', 'a' => '<p>No. A warning, watch, or storm report shows what weather was expected or observed in an area. Coverage depends on your policy terms, exclusions, and deductibles, and on evidence of actual damage to your property. Weather records are useful supporting documentation, but they do not decide a claim.</p>'],
        ['q' => 'How often does this page update?', 'a' => '<p>Current conditions refresh about every 10 minutes and the forecast about every 30 minutes, with alerts checked more frequently. If the NWS service is temporarily unavailable, the page shows the most recent data it received.</p>'],
    ],
    'body' => <<<'HTML'
<h2>How to read the Dallas weather data</h2>
<p>Everything above comes directly from the <a href="https://www.weather.gov/fwd/" target="_blank" rel="noopener">National Weather Service</a> (NWS). Current conditions are the latest observation from the automated station at <strong>Dallas Love Field (KDAL)</strong>, a few miles northwest of downtown. The forecast and any watches, warnings, or advisories are issued by the <strong>NWS Fort Worth/Dallas office</strong>, which covers Dallas, Dallas County, and much of North Texas.</p>
<p>The page refreshes on a schedule rather than second by second. Current conditions update roughly every 10 minutes and the forecast roughly every 30 minutes, with alerts checked more often. A few things to keep in mind:</p>
<ul>
<li><strong>Observations are a single point.</strong> The Love Field reading may not match your street, especially during a thunderstorm. Hail can pound Richardson and miss Oak Cliff, or the reverse. On May 28, 2024, for example, the NWS measured a 75 mph gust at Love Field while its storm survey found winds up to 95 mph in Garland.</li>
<li><strong>Times are local.</strong> Observation and alert times are shown in Central Time.</li>
<li><strong>Alerts are official.</strong> If an alert appears, read the full text. It explains the hazard, the affected area, and when it expires. Pay special attention to tornado warnings and flash flood warnings; Dallas County has more than 100 tornado reports and about 300 flash flood reports in the NOAA record.</li>
</ul>

<h2>Storm preparation for Dallas properties</h2>
<p>Dallas County sees most of its hail from March through June, damaging thunderstorm winds from spring into summer, tornadoes mainly in spring with a smaller fall season, flash flooding during heavy rain events, and occasional ice storms and hard freezes in winter. A little preparation before each season can reduce damage and make any later insurance claim easier to document.</p>

<h3>Before hail and wind season</h3>
<p>In the NOAA record for Dallas County, April and May account for more than half of all hail reports, and thunderstorm wind reports peak in May and June. Before spring:</p>
<ul>
<li>Take dated photos and video of your roof, siding, windows, fences, skylights, and HVAC units in their current condition. "Before" photos help separate new storm damage from older wear.</li>
<li>Trim dead branches that overhang the roof and secure loose items such as patio furniture and trash bins. Older neighborhoods like Lakewood, Kessler Park, and the Park Cities have large mature trees, and fallen trees are a common source of wind damage.</li>
<li>Review your declarations page so you know your wind/hail deductible, which on many Texas policies is a percentage of the dwelling limit.</li>
<li>Know your safe place for a tornado warning: an interior room on the lowest floor, away from windows.</li>
</ul>

<h3>Before heavy rain and flash flooding</h3>
<ul>
<li>Follow NWS and local emergency management instructions first, and never drive into a flooded road or underpass.</li>
<li>Clear gutters, downspouts, and drains, and know where water collects on your property, especially near creeks such as White Rock Creek, Turtle Creek, or Five Mile Creek.</li>
<li>Store copies of your policy, contact numbers, and a home inventory somewhere you can reach from a phone.</li>
<li>Remember that standard homeowners and commercial policies generally exclude flood. Flood coverage comes from the National Flood Insurance Program or a private flood policy, and NFIP policies typically have a 30-day waiting period (<a href="https://www.floodsmart.gov/" target="_blank" rel="noopener">floodsmart.gov</a>).</li>
</ul>

<h3>Before a freeze or ice storm</h3>
<p>Winter Storm Uri in February 2021 brought single-digit lows to Dallas County and left many homes with burst pipes, and winter storms or ice followed in February 2022, February 2023, January 2025, and January 2026. When a hard freeze is forecast, insulate exposed pipes and outdoor faucets, protect backflow preventers, let faucets drip, open cabinet doors under sinks on exterior walls, and know where your main water shutoff is. Pier-and-beam homes with plumbing in a crawlspace need extra attention. Dallas Water Utilities customers can find water service information on <a href="https://dallascityhall.com/" target="_blank" rel="noopener">dallascityhall.com</a>.</p>

<h2>What to do after a storm</h2>
<ol>
<li><strong>Stay safe.</strong> Avoid downed power lines, floodwater, and damaged structures. Report outages and downed lines to Oncor, and report a gas smell to Atmos Energy from a safe distance. Do not climb onto a wet or damaged roof.</li>
<li><strong>Take photos and video.</strong> Document damage from several angles before cleanup, including close-ups and wide shots. Photograph hailstones next to a coin or ruler if you can do so safely.</li>
<li><strong>Prevent further damage.</strong> Most policies expect reasonable steps to protect the property, such as tarping a roof or extracting water. Keep receipts for materials and mitigation services.</li>
<li><strong>Notify your insurer promptly.</strong> Report the loss, write down the claim number, and keep a log of every call and email.</li>
<li><strong>Save the weather record.</strong> Note the date and time of the storm and save any alerts you received. Then check the <a href="/weather-events/">recent weather events</a> page for preliminary NWS storm reports and use the <a href="/storm-lookup/">storm lookup tool</a> to find reports near your city or ZIP code.</li>
</ol>
<p>Our <a href="/claim-documentation-checklist/">claim documentation checklist</a> walks through what to gather for hail, wind, water, fire, roof, and commercial losses, and our <a href="/services/storm-damage-claims/">storm damage claims</a> page explains how a public adjuster can help. After a freeze, see <a href="/freeze-damage-burst-pipe-claims-dallas/">freeze damage and burst pipe claims in Dallas</a>.</p>

<h2>Looking back: Dallas storm history</h2>
<p>Live weather tells you what is happening now. For past events, the <a href="/storm-history/">Dallas and Dallas County storm history</a> page lets you search the NOAA Storm Events Database by date, event type, hail size, and wind speed. Official records like these can support a claim, but they never prove that a particular building was damaged. A physical inspection is still needed.</p>
HTML,
];
