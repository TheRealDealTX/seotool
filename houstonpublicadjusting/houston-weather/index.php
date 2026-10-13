<?php
require dirname(__DIR__) . '/inc/layout.php';

$crumbs = [['Home', '/'], ['Live Houston Weather', '/houston-weather/']];
$faqs = [
    ['Where does this weather data come from?', 'Everything on this page is pulled live from the National Weather Service (api.weather.gov), the NWS Houston/Galveston radar (KHGX), the National Hurricane Center and the Storm Prediction Center. Nothing is delayed or edited by us.'],
    ['What should I do right after a storm damages my Houston property?', 'Make sure everyone is safe, photograph and video all damage before anything is moved, make temporary repairs to prevent further damage (tarp the roof, extract water), keep every receipt, and report the claim to your insurer promptly. Then call Houston Public Adjusters at ' . PHONE_DISPLAY . ' for a free review before the carrier inspects.'],
    ['Does my insurance cover hurricane damage in Houston?', 'Most Texas homeowners policies cover wind damage from a hurricane, usually subject to a separate named-storm or windstorm deductible of 1%–5% of the dwelling limit. Rising water is excluded and needs separate flood insurance (NFIP or private). Our hurricane deductible calculator shows what that deductible means in dollars.'],
];

page_start([
    'title' => 'Live Houston Weather Tracker: Radar, Alerts & Hurricane Outlook',
    'desc' => 'Live Houston weather tracker: current conditions, National Weather Service alerts, 7-day forecast, KHGX radar loop, hurricane outlook and severe storm reports — from Houston Public Adjusters.',
    'path' => '/houston-weather/',
    'crumbs' => $crumbs,
    'body_class' => 'weather-page',
    'schema' => [faq_schema($faqs)],
    'scripts' => ['/assets/js/weather.js'],
]);
echo page_hero('Live Houston Weather Tracker', 'Real-time conditions, National Weather Service watches and warnings, the 7-day forecast, live radar and the tropical outlook for Houston and surrounding cities. When the weather turns into a claim, Houston Public Adjusters are a call away.', $crumbs, 'Updated automatically every 10 minutes');
?>
<section class="section" id="wx-app">
  <div class="wrap">
    <div class="wx-controls">
      <label>Choose your area
        <select id="wx-area">
<?php foreach (AREAS as $a): ?>
          <option value="<?= e(slugify_area($a[0])) ?>" data-lat="<?= $a[1] ?>" data-lng="<?= $a[2] ?>"><?= e($a[0]) ?></option>
<?php endforeach; ?>
        </select>
      </label>
      <button class="btn btn-dark" type="button" id="wx-refresh">Refresh now</button>
      <span id="wx-updated" class="kw-note"></span>
    </div>
    <div class="wx-grid">
      <div class="wx-now" id="wx-now"><p class="skel">Loading&hellip;</p></div>
      <div>
        <h2 style="font-size:1.4rem">Active watches &amp; warnings</h2>
        <div class="wx-alerts" id="wx-alerts"><p class="skel">Loading&hellip;</p></div>
      </div>
    </div>
    <h2 style="font-size:1.4rem;margin-top:40px">7-day forecast</h2>
    <div class="wx-forecast" id="wx-forecast"><p class="skel">Loading&hellip;</p></div>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    <h2 class="section-title">Radar, Hurricane &amp; Severe Storm Outlook</h2>
    <p class="section-lede">Live imagery from NOAA. The radar loop covers Harris, Fort Bend, Montgomery, Brazoria and Galveston counties.</p>
    <div class="wx-maps">
      <figure><img src="https://radar.weather.gov/ridge/standard/KHGX_loop.gif" data-refresh="https://radar.weather.gov/ridge/standard/KHGX_loop.gif" alt="Live NWS Houston/Galveston (KHGX) radar loop" width="600" height="550" loading="lazy">
        <figcaption><strong>Houston radar loop (KHGX)</strong> &mdash; National Weather Service Houston/Galveston.</figcaption></figure>
      <figure><img src="https://www.nhc.noaa.gov/xgtwo/two_atl_7d0.png" data-refresh="https://www.nhc.noaa.gov/xgtwo/two_atl_7d0.png" alt="National Hurricane Center 7-day Atlantic tropical weather outlook" width="600" height="500" loading="lazy">
        <figcaption><strong>7-day tropical outlook</strong> &mdash; National Hurricane Center. Atlantic hurricane season runs June 1 &ndash; November 30.</figcaption></figure>
      <figure><img src="https://www.spc.noaa.gov/products/outlook/day1otlk.png" data-refresh="https://www.spc.noaa.gov/products/outlook/day1otlk.png" alt="Storm Prediction Center day 1 severe thunderstorm outlook" width="600" height="450" loading="lazy">
        <figcaption><strong>Today&rsquo;s severe storm outlook</strong> &mdash; Storm Prediction Center risk of hail, damaging wind and tornadoes.</figcaption></figure>
      <figure><img src="https://www.spc.noaa.gov/climo/reports/today.gif" data-refresh="https://www.spc.noaa.gov/climo/reports/today.gif" alt="Storm Prediction Center map of today's hail, wind and tornado reports" width="600" height="450" loading="lazy">
        <figcaption><strong>Today&rsquo;s storm reports</strong> &mdash; preliminary hail (green), wind (blue) and tornado (red) reports.</figcaption></figure>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap two-col">
    <div class="prose">
      <h2>After the storm: protect your claim</h2>
      <p>The hours after a hurricane, hailstorm or flood decide how much of your loss gets paid. Insurers expect you to document and mitigate; Houston public adjusters make sure that work is turned into a claim the carrier cannot shortchange.</p>
      <ul class="checklist">
        <li>Photograph and video every room, the roof line, fences, gutters and vehicles before cleanup</li>
        <li>Note the date and time of the storm &mdash; your claim is tied to a date of loss</li>
        <li>Prevent further damage: tarp openings, shut off water, start drying within 24&ndash;48 hours</li>
        <li>Keep damaged materials (shingle samples, flooring, drywall) until the adjuster sees them</li>
        <li>Save receipts for tarps, fans, hotel stays and meals &mdash; they may be reimbursable</li>
        <li>Report the claim promptly and write down the claim number and every conversation</li>
        <li>Get a free claim review before you accept the insurer&rsquo;s first estimate</li>
      </ul>
      <p><a href="/hurricane-preparedness-checklist/">Use the interactive hurricane checklist &rarr;</a> &nbsp; <a href="/houston-storm-history/">Houston storm history &rarr;</a></p>
    </div>
    <div>
      <div class="side-card">
        <?= lead_form('lead-weather', 'Storm damage? Get a free claim review', 'Licensed Houston public adjusters &mdash; no upfront fees.') ?>
      </div>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="wrap" style="max-width:860px">
    <h2 class="section-title">Weather &amp; storm claim questions</h2>
    <?= faq_html($faqs) ?>
    <p class="tool-note">Weather data courtesy of the National Weather Service, National Hurricane Center and Storm Prediction Center (NOAA). For life-safety decisions always follow official guidance from <a href="https://www.weather.gov/hgx/" target="_blank" rel="noopener">NWS Houston/Galveston</a> and <a href="https://www.readyharris.org/" target="_blank" rel="noopener">ReadyHarris</a>.</p>
  </div>
</section>
<?php
function slugify_area(string $s): string { return trim(preg_replace('/[^a-z0-9]+/', '-', strtolower($s)), '-'); }
page_end();
