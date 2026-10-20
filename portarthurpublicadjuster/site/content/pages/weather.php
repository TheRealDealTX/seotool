<?php
return [
    'template'      => 'weather',
    'title'         => 'Live Port Arthur Weather & 7-Day Forecast',
    'seo_title'     => 'Port Arthur Weather Today: Live Conditions, Forecast & Alerts',
    'description'   => 'Live Port Arthur weather from the National Weather Service: current conditions at KBPT, a 7-day forecast, severe and tropical alerts, and storm prep tips.',
    'lead'          => 'Real-time National Weather Service data for Port Arthur: current conditions, active alerts, and the 7-day forecast, plus practical hurricane preparation and post-storm guidance for property owners.',
    'kicker'        => 'Live Weather',
    'image'         => '/assets/img/featured/page-weather.webp',
    'image_alt'     => 'Storm clouds building over Port Arthur, Texas',
    'hide_hero_cta' => false,
    'faqs' => [
        ['q' => 'Where does the Port Arthur weather data on this page come from?', 'a' => '<p>All data comes from the National Weather Service through its public API at <a href="https://www.weather.gov/" target="_blank" rel="noopener">weather.gov</a>. Current conditions are the latest observation from the station at Jack Brooks Regional Airport (KBPT), which serves Beaumont and Port Arthur. The forecast and alerts are issued by the NWS office in Lake Charles that serves Southeast Texas.</p>'],
        ['q' => 'Why might this page differ from my phone\'s weather app?', 'a' => '<p>Many weather apps use their own models, blend several data sources, or report from a different station or neighborhood sensor. This page shows the official NWS observation at the airport and the official NWS forecast. Conditions can also vary a lot across short distances during thunderstorms and tropical rain bands, and each source updates on its own schedule.</p>'],
        ['q' => 'What is the difference between a watch and a warning?', 'a' => '<p>The National Weather Service issues a <strong>watch</strong> when conditions are favorable for hazardous weather to develop, so you should be prepared. It issues a <strong>warning</strong> when hazardous weather is occurring, imminent, or likely, so you should take action to protect yourself now. Hurricane and tropical storm watches and warnings follow the same idea for tropical systems.</p>'],
        ['q' => 'Does a severe weather or hurricane warning mean my insurance claim will be covered?', 'a' => '<p>No. A warning, watch, or storm report shows what weather was expected or observed in an area. Coverage depends on your policy terms, exclusions, and deductibles, and on evidence of actual damage to your property. Weather records are useful supporting documentation, but they do not decide a claim.</p>'],
        ['q' => 'How often does this page update?', 'a' => '<p>Current conditions refresh about every 10 minutes and the forecast about every 30 minutes, with alerts checked more frequently. If the NWS service is temporarily unavailable, the page shows the most recent data it received.</p>'],
    ],
    'body' => <<<'HTML'
<h2>How to read the Port Arthur weather data</h2>
<p>Everything above comes directly from the <a href="https://www.weather.gov/" target="_blank" rel="noopener">National Weather Service</a> (NWS). Current conditions are the latest observation from the automated station at <strong>Jack Brooks Regional Airport (KBPT)</strong>, located between Port Arthur and Beaumont. The forecast and any watches, warnings, or advisories are issued by the NWS office in Lake Charles, Louisiana, which covers Jefferson County and the rest of Southeast Texas.</p>
<p>The page refreshes on a schedule rather than second by second. Current conditions update roughly every 10 minutes and the forecast roughly every 30 minutes, with alerts checked more often. A few things to keep in mind:</p>
<ul>
<li><strong>Observations are a single point.</strong> The airport reading may not match your street, especially during a thunderstorm or tropical rain band.</li>
<li><strong>Times are local.</strong> Observation and alert times are shown in Central Time.</li>
<li><strong>Alerts are official.</strong> If an alert appears, read the full text. It explains the hazard, the affected area, and when it expires.</li>
</ul>
<p>For tropical systems still out in the Gulf or Atlantic, see the <a href="/hurricane-tracker/">hurricane tracker</a>, which pulls information from the National Hurricane Center.</p>

<h2>Storm preparation for Port Arthur properties</h2>
<p>Jefferson County faces hurricanes and tropical storms from June through November, severe thunderstorms with straight-line winds in spring and summer, extreme rainfall events, and occasional hard freezes in winter. A little preparation before each season can reduce damage and make any later insurance claim easier to document.</p>

<h3>Before hurricane season</h3>
<ul>
<li>Take dated photos and video of your roof, siding, windows, fences, and HVAC units, plus each room and its contents. "Before" photos help separate new storm damage from older wear.</li>
<li>Review your declarations pages so you know your named-storm or wind/hail deductible, which on many Texas policies is a percentage of the dwelling limit. The <a href="/hurricane-deductible-calculator/">hurricane deductible calculator</a> turns that percentage into dollars.</li>
<li>Check whether you have separate TWIA windstorm and flood policies, and keep copies of all three policies somewhere you can reach from a phone.</li>
<li>Remember that standard homeowners and TWIA policies generally exclude flood. Flood coverage comes from the National Flood Insurance Program or a private flood policy, and NFIP policies typically have a 30-day waiting period (<a href="https://www.floodsmart.gov/" target="_blank" rel="noopener">floodsmart.gov</a>), so do not wait until a storm is in the Gulf.</li>
</ul>

<h3>When a storm is approaching</h3>
<ul>
<li>Follow NWS and local emergency management instructions first, including any evacuation orders.</li>
<li>Clear gutters and drains, secure loose outdoor items, and know where water collects on your property.</li>
<li>Move important documents and valuables above likely flood levels or take them with you.</li>
</ul>

<h3>Before a freeze</h3>
<p>The February 2021 freeze showed how vulnerable local plumbing can be. When a hard freeze is forecast, insulate exposed pipes and outdoor faucets, protect plumbing in crawlspaces under pier-and-beam homes, let faucets drip, open cabinet doors under sinks on exterior walls, and know where your main water shutoff is.</p>

<h2>What to do after a storm</h2>
<ol>
<li><strong>Stay safe.</strong> Avoid downed power lines, standing water, and damaged structures. Do not climb onto a wet or damaged roof.</li>
<li><strong>Take photos and video.</strong> Document damage from several angles before cleanup, including close-ups, wide shots, and any high-water lines on walls.</li>
<li><strong>Prevent further damage.</strong> Most policies expect reasonable steps to protect the property, such as tarping a roof or extracting water. In Southeast Texas humidity, start drying quickly to limit mold. Keep receipts for materials and mitigation services.</li>
<li><strong>Notify each insurer promptly.</strong> Report the loss to your homeowners insurer, TWIA, and your flood insurer as applicable. Write down each claim number and keep a log of every call and email.</li>
<li><strong>Save the weather record.</strong> Note the date and time of the storm and save any alerts you received. Then check the <a href="/weather-events/">recent weather events</a> page for preliminary NWS storm reports and use the <a href="/storm-lookup/">storm lookup tool</a> to find reports near your city or ZIP code.</li>
</ol>
<p>Our <a href="/claim-documentation-checklist/">claim documentation checklist</a> walks through what to gather for hurricane, wind, flood, water, fire, roof, and commercial losses.</p>

<h2>Looking back: Port Arthur storm history</h2>
<p>Live weather tells you what is happening now. For past events, the <a href="/storm-history/">Port Arthur and Jefferson County storm history</a> page lets you search the NOAA Storm Events Database by date, event type, hail size, and wind speed, and highlights storms such as Rita, Ike, Harvey, Imelda, and Laura. Official records like these can support a claim, but they never prove that a particular building was damaged. A physical inspection is still needed.</p>
HTML,
];
