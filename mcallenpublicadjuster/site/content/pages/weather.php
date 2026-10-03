<?php
return [
    'template'      => 'weather',
    'title'         => 'Live McAllen Weather & 7-Day Forecast',
    'seo_title'     => 'McAllen Weather Today: Live Conditions, Forecast & NWS Alerts',
    'description'   => 'Live McAllen weather from the National Weather Service: current conditions at KMFE, a 7-day forecast, severe weather alerts, and storm prep tips.',
    'lead'          => 'Real-time National Weather Service data for McAllen: current conditions, active alerts, and the 7-day forecast, plus practical storm preparation and post-storm guidance for property owners.',
    'kicker'        => 'Live Weather',
    'image'         => '/assets/img/featured/page-weather.webp',
    'image_alt'     => 'Storm clouds building over McAllen, Texas',
    'hide_hero_cta' => false,
    'faqs' => [
        ['q' => 'Where does the McAllen weather data on this page come from?', 'a' => '<p>All data comes from the National Weather Service through its public API at <a href="https://www.weather.gov/" target="_blank" rel="noopener">weather.gov</a>. Current conditions are the latest observation from the station at McAllen-Miller International Airport (KMFE). The forecast and alerts are issued by the NWS office in Brownsville that serves the Rio Grande Valley.</p>'],
        ['q' => 'Why might this page differ from my phone\'s weather app?', 'a' => '<p>Many weather apps use their own models, blend several data sources, or report from a different station or neighborhood sensor. This page shows the official NWS observation at the airport and the official NWS forecast. Conditions can also vary a lot across short distances during thunderstorms, and each source updates on its own schedule.</p>'],
        ['q' => 'What is the difference between a watch and a warning?', 'a' => '<p>The National Weather Service issues a <strong>watch</strong> when conditions are favorable for hazardous weather to develop, so you should be prepared. It issues a <strong>warning</strong> when hazardous weather is occurring, imminent, or likely, so you should take action to protect yourself now.</p>'],
        ['q' => 'Does a severe weather warning mean my insurance claim will be covered?', 'a' => '<p>No. A warning, watch, or storm report shows what weather was expected or observed in an area. Coverage depends on your policy terms, exclusions, and deductibles, and on evidence of actual damage to your property. Weather records are useful supporting documentation, but they do not decide a claim.</p>'],
        ['q' => 'How often does this page update?', 'a' => '<p>Current conditions refresh about every 10 minutes and the forecast about every 30 minutes, with alerts checked more frequently. If the NWS service is temporarily unavailable, the page shows the most recent data it received.</p>'],
    ],
    'body' => <<<'HTML'
<h2>How to read the McAllen weather data</h2>
<p>Everything above comes directly from the <a href="https://www.weather.gov/" target="_blank" rel="noopener">National Weather Service</a> (NWS). Current conditions are the latest observation from the automated station at <strong>McAllen-Miller International Airport (KMFE)</strong>. The forecast and any watches, warnings, or advisories are issued by the NWS office in Brownsville, which covers McAllen and the rest of the Rio Grande Valley (RGV).</p>
<p>The page refreshes on a schedule rather than second by second. Current conditions update roughly every 10 minutes and the forecast roughly every 30 minutes, with alerts checked more often. A few things to keep in mind:</p>
<ul>
<li><strong>Observations are a single point.</strong> The airport reading may not match your street, especially during a thunderstorm. Hail and damaging wind can hit one neighborhood and miss the next.</li>
<li><strong>Times are local.</strong> Observation and alert times are shown in Central Time.</li>
<li><strong>Alerts are official.</strong> If an alert appears, read the full text. It explains the hazard, the affected area, and when it expires.</li>
</ul>

<h2>Storm preparation for McAllen properties</h2>
<p>Hidalgo County sees most of its hail and damaging thunderstorm wind in spring, tropical systems in summer and fall, and occasional hard freezes in winter. A little preparation before each season can reduce damage and make any later insurance claim easier to document.</p>

<h3>Before hail and wind season</h3>
<p>NOAA records show that most Hidalgo County hail reports fall in April and May. Before spring:</p>
<ul>
<li>Take dated photos and video of your roof, siding, windows, fences, and HVAC units in their current condition. "Before" photos help separate new storm damage from older wear.</li>
<li>Trim dead branches that overhang the roof and secure loose items such as patio furniture and trash bins.</li>
<li>Review your declarations page so you know your wind/hail deductible, which on many Texas policies is a percentage of the dwelling limit.</li>
</ul>

<h3>Before a tropical storm or hurricane</h3>
<ul>
<li>Follow NWS and local emergency management instructions first.</li>
<li>Clear gutters and drains, and know where water collects on your property.</li>
<li>Store copies of your policy, contact numbers, and a home inventory somewhere you can reach from a phone.</li>
<li>Remember that standard homeowners and commercial policies generally exclude flood. Flood coverage comes from the National Flood Insurance Program or a private flood policy, and NFIP policies typically have a 30-day waiting period (<a href="https://www.floodsmart.gov/" target="_blank" rel="noopener">floodsmart.gov</a>).</li>
</ul>

<h3>Before a freeze</h3>
<p>The February 2021 freeze showed how vulnerable local plumbing can be. When a hard freeze is forecast, insulate exposed pipes and outdoor faucets, let faucets drip, open cabinet doors under sinks on exterior walls, and know where your main water shutoff is.</p>

<h2>What to do after a storm</h2>
<ol>
<li><strong>Stay safe.</strong> Avoid downed power lines, standing water, and damaged structures. Do not climb onto a wet or damaged roof.</li>
<li><strong>Take photos and video.</strong> Document damage from several angles before cleanup, including close-ups and wide shots. Photograph hail stones next to a coin or ruler if you can do so safely.</li>
<li><strong>Prevent further damage.</strong> Most policies expect reasonable steps to protect the property, such as tarping a roof or extracting water. Keep receipts for materials and mitigation services.</li>
<li><strong>Notify your insurer promptly.</strong> Report the loss, write down the claim number, and keep a log of every call and email.</li>
<li><strong>Save the weather record.</strong> Note the date and time of the storm and save any alerts you received. Then check the <a href="/weather-events/">recent weather events</a> page for preliminary NWS storm reports and use the <a href="/storm-lookup/">storm lookup tool</a> to find reports near your city or ZIP code.</li>
</ol>
<p>Our <a href="/claim-documentation-checklist/">claim documentation checklist</a> walks through what to gather for hail, wind, water, fire, roof, and commercial losses.</p>

<h2>Looking back: McAllen storm history</h2>
<p>Live weather tells you what is happening now. For past events, the <a href="/storm-history/">McAllen and Hidalgo County storm history</a> page lets you search the NOAA Storm Events Database by date, event type, hail size, and wind speed. Official records like these can support a claim, but they never prove that a particular building was damaged. A physical inspection is still needed.</p>
HTML,
];
