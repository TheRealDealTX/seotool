<?php
require $_SERVER['DOCUMENT_ROOT'] . '/inc/layout.php';

$path = '/sugar-land-weather/';
$crumbs = [['Home', '/'], ['Storm Center', $path]];
$faqs = [
    ['What is the difference between a watch and a warning?',
     '<p>A <strong>watch</strong> means conditions are favorable for the hazard—get ready. A <strong>warning</strong> means the hazard is happening or imminent in your area—act now. Hurricane, tornado, severe thunderstorm and flash flood watches and warnings all follow this rule.</p>'],
    ['Where does this weather data come from?',
     '<p>Directly from the National Weather Service (Houston/Galveston office and the Sugar Land Regional Airport station), NOAA’s National Hurricane Center and Storm Prediction Center, and the NOAA river gauge on the Brazos River at Richmond. The page refreshes automatically every 10 minutes.</p>'],
    ['Why should I save weather records after a storm?',
     '<p>Insurers often question whether damage came from a specific storm. Screenshots of alerts, radar and observed wind speeds for your date of loss help tie the damage to that event. Save them the day of the storm.</p>'],
    ['When is hurricane season in Sugar Land?',
     '<p>The Atlantic hurricane season runs from June 1 through November 30, with the peak from mid-August through September. Severe thunderstorms with hail and damaging winds are most common in spring.</p>'],
];
page_start([
    'title' => 'Sugar Land Weather Today: Live Radar, Alerts & Storm Tracker',
    'description' => 'Live Sugar Land, TX weather: current conditions, NWS watches and warnings, 7-day forecast, Houston radar, tropical outlook and the Brazos River at Richmond gauge.',
    'path' => $path,
    'breadcrumbs' => $crumbs,
    'schema' => [faq_schema($faqs, $path)],
]);
page_hero('Live Sugar Land Weather &amp; Storm Tracker', 'Real-time conditions, National Weather Service alerts, radar, the tropics and the Brazos River—everything Sugar Land and Fort Bend County property owners watch when a storm is coming.', $crumbs, 'Storm Center');
?>
<section class="section-sm">
  <div class="container" id="wx" data-lat="<?= SITE['lat'] ?>" data-lng="<?= SITE['lng'] ?>">
    <div class="wx-grid">
      <div class="wx-now">
        <p class="eyebrow" style="color:var(--lavender)">Sugar Land now · Sugar Land Regional Airport (KSGR)</p>
        <div class="wx-temp" data-wx="temp">--°</div>
        <div class="wx-cond" data-wx="cond">Loading current conditions…</div>
        <div class="wx-meta">
          <div><span>Feels like</span><strong data-wx="feels">--</strong></div>
          <div><span>Humidity</span><strong data-wx="hum">--</strong></div>
          <div><span>Wind</span><strong data-wx="wind">--</strong></div>
          <div><span>Gusts</span><strong data-wx="gust">--</strong></div>
          <div><span>Pressure</span><strong data-wx="pres">--</strong></div>
          <div><span>Dew point</span><strong data-wx="dew">--</strong></div>
        </div>
        <p class="wx-updated" data-wx="updated">Data: National Weather Service</p>
      </div>
      <div>
        <h2 class="h3">Active NWS alerts for Sugar Land</h2>
        <div class="wx-alerts" data-wx="alerts"><div class="wx-ok">Checking the National Weather Service…</div></div>
        <p class="small muted mt-2">Alerts for the Sugar Land area from the NWS Houston/Galveston office. Always follow official instructions from Fort Bend County and the City of Sugar Land.</p>
      </div>
    </div>
  </div>
</section>

<section class="section-sm">
  <div class="container">
    <h2>7-day Sugar Land forecast</h2>
    <div class="wx-forecast" data-wx="forecast"><div class="wx-day">Loading…</div></div>
    <p class="small muted" data-wx="fcupdated"></p>
  </div>
</section>

<section class="section-sm">
  <div class="container wx-grid">
    <div>
      <h2>Houston/Galveston radar</h2>
      <img class="wx-img" data-refresh src="https://radar.weather.gov/ridge/standard/KHGX_loop.gif" alt="Animated NWS radar loop for the Houston–Galveston area including Sugar Land" width="600" height="550" loading="lazy">
      <p class="small muted">NWS KHGX radar loop. <a href="https://radar.weather.gov/station/khgx/standard" target="_blank" rel="noopener">Open full radar</a></p>
    </div>
    <div>
      <h2>Tropical outlook (next 7 days)</h2>
      <img class="wx-img" data-refresh src="https://www.nhc.noaa.gov/xgtwo/two_atl_7d0.png" alt="National Hurricane Center 7-day Atlantic tropical weather outlook" width="600" height="440" loading="lazy" style="background:#fff">
      <p class="small muted">National Hurricane Center. <a href="https://www.nhc.noaa.gov/" target="_blank" rel="noopener">Active storms &amp; advisories</a> · <span data-wx="season"></span></p>
    </div>
  </div>
</section>

<section class="section-sm">
  <div class="container wx-grid">
    <div class="gauge">
      <h2 class="h3">Brazos River at Richmond (RMOT2)</h2>
      <p class="mb-0"><strong data-wx="rstage" style="font-size:1.6rem;font-family:var(--font-slab);color:var(--ink)">-- ft</strong> <span data-wx="rcat" class="muted"></span></p>
      <div class="gauge-bar"><span class="gauge-marker" data-wx="rmarker" style="left:0"></span></div>
      <div class="gauge-legend"><span>0 ft</span><span>Action 20</span><span>Minor 45</span><span>Major 50</span><span>60</span></div>
      <p class="small muted mt-2" data-wx="rmeta">The Brazos runs along Sugar Land’s southern and western edge. Record crest: 55.19 ft during Hurricane Harvey (Sept. 1, 2017).</p>
      <a class="small" href="https://water.noaa.gov/gauges/rmot2" target="_blank" rel="noopener">NOAA gauge page &amp; forecast hydrograph</a>
    </div>
    <div>
      <h2 class="h3">Severe weather outlook (today)</h2>
      <img class="wx-img" data-refresh src="https://www.spc.noaa.gov/products/outlook/day1otlk.png" alt="Storm Prediction Center day 1 convective outlook map" width="600" height="420" loading="lazy" style="background:#fff">
      <p class="small muted">NOAA Storm Prediction Center day-1 outlook for severe thunderstorms, hail and tornadoes.</p>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container content-layout" style="padding:0">
    <div class="prose">
      <h2>Weather risks for Sugar Land property owners</h2>
      <p>Sugar Land sits about 20 miles southwest of downtown Houston and roughly 50 miles inland from the Gulf of Mexico. That location brings four recurring threats to homes and businesses:</p>
      <ul class="checklist purple">
        <li><strong>Hurricanes and tropical storms</strong> (June–November): wind damage, falling trees and long power outages, as with Ike in 2008 and Beryl in 2024.</li>
        <li><strong>Severe thunderstorms</strong> (mostly spring): hail, straight-line winds and isolated tornadoes.</li>
        <li><strong>Flooding</strong>: heavy rain on flat terrain, plus Brazos River and Oyster Creek flooding during major events like Harvey in 2017.</li>
        <li><strong>Hard freezes</strong>: rare but costly—Winter Storm Uri in February 2021 burst pipes across the city.</li>
      </ul>
      <h2>Had storm damage? Save the evidence today</h2>
      <p>The day of the storm is the easiest time to prove what happened. Take screenshots of the alerts and radar on this page, note the time the damage occurred, and photograph everything before cleanup. Then use our <a href="/hurricane-preparedness-checklist/">after-the-storm checklist</a>, check your <a href="/tools/hurricane-deductible-calculator/">deductible</a>, and call a Sugar Land public adjuster for a free review before the insurer’s inspection.</p>
      <p>Looking back instead of ahead? See <a href="/sugar-land-storm-history/">Sugar Land’s storm history</a>.</p>
      <h2>Storm center FAQ</h2>
      <?php faq_list($faqs); ?>
    </div>
    <?php sidebar_cta(); ?>
  </div>
</section>
<?php page_end(['scripts' => '<script src="/assets/js/weather.js?v=' . ASSET_VER . '" defer></script>']); ?>
