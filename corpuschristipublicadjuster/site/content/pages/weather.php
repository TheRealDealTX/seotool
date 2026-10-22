<?php
defined('CCPA_ROOT') || exit;
return [
    'template'      => 'weather',
    'title'         => 'Live Corpus Christi Weather, Radar & Tides',
    'seo_title'     => 'Corpus Christi Weather Today: Radar, Tides, Forecast & Alerts',
    'description'   => 'Live Corpus Christi weather from the NWS: KCRP conditions, hourly and 7-day forecast, radar loop, NOAA tides, hurricane tracking, and storm prep tips.',
    'lead'          => 'Official National Weather Service, NOAA, and National Hurricane Center data for Corpus Christi in one place: current conditions, alerts, forecasts, radar, tides, and the tropics, plus storm preparation guidance for property owners.',
    'kicker'        => 'Live Weather',
    'image'         => '/assets/img/featured/page-weather.webp',
    'image_alt'     => 'Storm clouds building over Corpus Christi Bay',
    'hide_hero_cta' => false,
    'faqs' => [
        ['q' => 'Where does the Corpus Christi weather data on this page come from?', 'a' => '<p>Current conditions are the latest observation from the National Weather Service station at Corpus Christi International Airport (KCRP). The hourly and 7-day forecasts and all alerts come from the NWS Corpus Christi office (CRP) through <a href="https://www.weather.gov/crp" target="_blank" rel="noopener">weather.gov</a>. Radar comes from NEXRAD via the Iowa Environmental Mesonet, tides from <a href="https://tidesandcurrents.noaa.gov/" target="_blank" rel="noopener">NOAA Tides and Currents</a>, and tropical storm information from the <a href="https://www.nhc.noaa.gov/" target="_blank" rel="noopener">National Hurricane Center</a>.</p>'],
        ['q' => 'Why might this page differ from my phone\'s weather app?', 'a' => '<p>Many apps use their own models, blend several data sources, or report from a different station or neighborhood sensor. This page shows the official NWS observation at the airport and the official NWS forecast. Conditions on the Island or in Portland can differ from the airport, especially during thunderstorms, and each source updates on its own schedule.</p>'],
        ['q' => 'What does "observed vs. predicted" mean on the tide chart?', 'a' => '<p>The predicted line is the astronomical tide NOAA expects from the moon and sun alone. The observed line is the water level the station actually measured. When observed water runs above the prediction, wind, a front, or a tropical system is pushing extra water into the bays. That difference is a useful early sign of coastal flooding risk.</p>'],
        ['q' => 'What is the difference between a watch and a warning?', 'a' => '<p>The National Weather Service issues a <strong>watch</strong> when conditions are favorable for hazardous weather, so you should be prepared. It issues a <strong>warning</strong> when hazardous weather is occurring, imminent, or likely, so you should act now to protect yourself. For hurricanes and storm surge, follow evacuation orders from local officials.</p>'],
        ['q' => 'Does a severe weather warning mean my insurance claim will be covered?', 'a' => '<p>No. A warning, watch, or storm report shows what weather was expected or observed in an area. Coverage depends on your policy terms, exclusions, and deductibles, and on evidence of actual damage to your property. Weather records are useful supporting documentation, but they do not decide a claim.</p>'],
        ['q' => 'How often does this page update?', 'a' => '<p>Current conditions refresh about every 10 minutes, forecasts about every 30 minutes, and alerts about every 5 minutes. Tide and tropical data refresh about every 30 minutes, and the radar loop shows recent frames updated every few minutes. If a source is temporarily unavailable, the page shows the most recent data it received.</p>'],
    ],
    'body' => <<<'HTML'
<h2>How to read the Corpus Christi weather data</h2>
<p>Everything above comes from official government sources. Current conditions are the latest observation from the automated station at <strong>Corpus Christi International Airport (KCRP)</strong>. The hourly forecast for the next 48 hours, the 7-day forecast, and any watches, warnings, or advisories are issued by the <a href="https://www.weather.gov/crp" target="_blank" rel="noopener">National Weather Service office in Corpus Christi (CRP)</a>, which covers the city, Nueces County, and the rest of the Coastal Bend.</p>
<ul>
<li><strong>Observations are a single point.</strong> The airport reading may not match your street. Hail and damaging wind can hit Calallen and miss Flour Bluff, and the barrier islands often run windier than inland neighborhoods.</li>
<li><strong>Times are local.</strong> Observation, forecast, and alert times are shown in Central Time.</li>
<li><strong>Alerts are official.</strong> If an alert appears, read the full text. It explains the hazard, the area, and when it expires.</li>
</ul>

<h3>Radar loop</h3>
<p>The radar loop shows NEXRAD base reflectivity from the <a href="https://mesonet.agron.iastate.edu/" target="_blank" rel="noopener">Iowa Environmental Mesonet</a> over an Esri dark-gray base map (built with OpenStreetMap data). Brighter colors mean heavier rain and, in strong storms, possible hail. Use the slider to step through recent frames and see which way storms are moving.</p>

<h3>Tides and water levels</h3>
<p>The tide panel uses NOAA CO-OPS stations at <strong>USS Lexington in Corpus Christi Bay (8775296)</strong>, <strong>Packery Channel on Padre Island (8775792)</strong>, and <strong>Port Aransas (8775237)</strong>. Each chart compares the predicted astronomical tide with the observed water level. When the observed line runs well above the prediction, wind or a tropical system is piling water into the bays, which matters for North Beach, the Island, Port Aransas, and low-lying bayfront property. Levels are in feet above mean lower low water (MLLW), and recent observations are preliminary.</p>

<h3>Tropics watch</h3>
<p>The tropics panel lists active storms from the <a href="https://www.nhc.noaa.gov/" target="_blank" rel="noopener">National Hurricane Center</a> with straight-line distance from downtown Corpus Christi. Distance is not a forecast. For track, cone, and surge information, always read the NHC advisory itself. The Atlantic hurricane season runs June 1 through November 30, with the peak around September 10.</p>

<h2>Storm preparation for Corpus Christi properties</h2>
<p>NOAA records for Nueces County show most hail and damaging thunderstorm wind reports in spring, especially April and May, tropical systems from June into the fall, and occasional hard freezes in winter. A little preparation before each season can reduce damage and make any later claim easier to document. Our <a href="/hurricane-season-guide/">hurricane season guide</a> covers this in more detail.</p>

<h3>Before hail and wind season</h3>
<ul>
<li>Take dated photos and video of your roof, siding, windows, fences, and HVAC units in their current condition. "Before" photos help separate new storm damage from older wear and salt-air corrosion.</li>
<li>Trim dead branches over the roof and secure loose items such as patio furniture and trash bins.</li>
<li>Check your declarations page for the wind/hail deductible, which on many Texas policies is a percentage of the dwelling limit.</li>
</ul>

<h3>Before a tropical storm or hurricane</h3>
<ul>
<li>Follow NWS, NHC, and local emergency management instructions first, including evacuation orders.</li>
<li>Know which policies you have: a homeowners or commercial policy, a TWIA windstorm policy for wind and hail, and a flood policy for surge and rising water. NFIP flood policies usually have a 30-day waiting period (<a href="https://www.floodsmart.gov/" target="_blank" rel="noopener">floodsmart.gov</a>).</li>
<li>Run the numbers on your named-storm deductible with the <a href="/hurricane-deductible-calculator/">hurricane deductible calculator</a>.</li>
<li>Store copies of your policies, contact numbers, and a home inventory where you can reach them from a phone.</li>
</ul>

<h3>Before a freeze</h3>
<p>During the February 2021 winter storm, Corpus Christi International Airport recorded a low of 17&deg;F on February 15 and stayed below freezing all day. When a hard freeze is forecast, insulate exposed pipes and outdoor faucets, let faucets drip, open cabinet doors on exterior walls, and know where your main water shutoff is.</p>

<h2>What to do after a storm</h2>
<ol>
<li><strong>Stay safe.</strong> Avoid downed power lines, floodwater, and damaged structures. Do not climb onto a wet or damaged roof.</li>
<li><strong>Take photos and video.</strong> Document damage from several angles before cleanup. After a hurricane, photograph water lines on walls, since the wind-versus-water question often decides which policy pays.</li>
<li><strong>Prevent further damage.</strong> Most policies expect reasonable steps such as tarping a roof or extracting water. Keep receipts.</li>
<li><strong>Notify each insurer promptly.</strong> TWIA claims must generally be filed within one year of the date of loss. Write down claim numbers and keep a log of every call and email.</li>
<li><strong>Save the weather record.</strong> Note the date and time and save any alerts you received. Then check <a href="/weather-events/">recent weather events</a> for preliminary NWS storm reports and use the <a href="/storm-lookup/">storm lookup tool</a> to search near your city or ZIP code.</li>
</ol>
<p>Our <a href="/claim-documentation-checklist/">claim documentation checklist</a> lists what to gather for each type of damage.</p>

<h2>Looking back: Corpus Christi storm history</h2>
<p>Live weather shows what is happening now. For past events, the <a href="/storm-history/">Coastal Bend storm history</a> page lets you search the NOAA Storm Events Database by date, event type, hail size, and wind speed. Official records support a claim, but they never prove that a particular building was damaged; a physical inspection is still needed.</p>
HTML,
];
