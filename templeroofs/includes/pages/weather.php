<?php
defined('TR_ROOT') || exit;
$crumbs = [['Temple Weather', '/weather/']];
$faqs = [
    ['q' => 'Where does this weather data come from?', 'a' => 'Current conditions and the seven-day forecast come from Open-Meteo, which blends national weather model data. Active watches, warnings and advisories come directly from the U.S. National Weather Service.'],
    ['q' => 'How often is the page updated?', 'a' => 'Our server refreshes forecast data about every 10 minutes and alerts about every 5 minutes. The page shows when the data was last retrieved. If a source is unavailable, the page says so clearly instead of showing old data as live.'],
    ['q' => 'Is the roof-weather risk indicator an official warning?', 'a' => 'No. It is an informational guide based on simple published rules about wind gusts, thunderstorms, rain totals and heat. Always follow official National Weather Service alerts and local emergency officials.'],
    ['q' => 'Should I schedule a roof inspection after every storm?', 'a' => 'Not necessarily. Consider one after hail, gusts above roughly 50 to 60 mph, falling limbs, or if you notice missing shingles, dented gutters or new leaks. Our storm damage self-check can help you decide.'],
];
layout_start([
    'title'       => 'Temple, TX Weather — Live Conditions & 7-Day Roofing Forecast',
    'raw_title'   => true,
    'description' => 'Live Temple, TX weather, a 7-day forecast with wind gusts and storm chances, and active NWS alerts for Bell County roofs.',
    'path'        => '/weather/',
    'crumbs'      => $crumbs,
    'schema'      => [schema_faq($faqs)],
    'scripts'     => ['js/weather.js'],
    'body_class'  => 'page-weather',
]);
?>
<section class="page-hero page-hero--weather">
  <div class="container page-hero__inner">
    <?= breadcrumbs_html($crumbs) ?>
    <p class="eyebrow eyebrow--light"><?= icon('map-pin') ?> Temple, Bell County, Texas</p>
    <h1 class="page-hero__title">Temple, TX Weather — Live Conditions &amp; 7&#8209;Day Roofing Forecast</h1>
    <p class="page-hero__lead">Current conditions, a seven-day outlook with wind gusts and storm chances, and official National Weather Service alerts — with notes on what the weather means for your roof.</p>
  </div>
</section>

<div class="weather-app" data-weather="full" aria-live="polite">
  <section class="section section--tight">
    <div class="container">
      <div class="wx-status" data-wx-status hidden></div>
      <div class="wx-alerts" data-wx-alerts>
        <div class="wx-loading"><span class="spinner" aria-hidden="true"></span> Checking National Weather Service alerts…</div>
      </div>
      <div class="wx-now-grid">
        <div class="wx-now" data-wx-current>
          <div class="wx-loading"><span class="spinner" aria-hidden="true"></span> Loading current Temple conditions…</div>
        </div>
        <div class="wx-risk" data-wx-risk></div>
      </div>
      <noscript><div class="callout">Live weather requires JavaScript. You can also view the official <a href="https://forecast.weather.gov/MapClick.php?lat=31.0982&amp;lon=-97.3428" rel="noopener">National Weather Service forecast for Temple</a>.</div></noscript>
    </div>
  </section>
  <section class="section section--tight section--alt">
    <div class="container">
      <h2 class="section-title section-title--sm">7-Day Temple Forecast</h2>
      <div class="wx-days" data-wx-days></div>
      <p class="wx-attrib">Forecast data: <a href="https://open-meteo.com/" rel="noopener">Open-Meteo.com</a> (CC BY 4.0). Alerts: <a href="https://www.weather.gov/" rel="noopener">U.S. National Weather Service</a>. Times shown in Central Time (America/Chicago). <span data-wx-updated></span></p>
    </div>
  </section>
</div>

<section class="section">
  <div class="container">
    <?= section_head('Roofing weather advisory', 'What the Forecast Means for Your Roof', 'How each type of Central Texas weather affects roofing — and what to watch for.') ?>
    <div class="factor-grid factor-grid--3">
      <article class="factor reveal"><span class="factor__icon"><?= icon('wind') ?></span><h3>Strong wind forecasts</h3><p>Gusts of 40 mph and up can lift shingles whose seal strips have weakened with age. The National Weather Service treats gusts of 58 mph or more as severe. After a windy day, look from the ground for missing tabs along ridges, rakes and corners.</p></article>
      <article class="factor reveal"><span class="factor__icon"><?= icon('cloud-lightning') ?></span><h3>Severe thunderstorms</h3><p>Central Texas thunderstorms can produce damaging winds, hail and torrential rain together. Secure patio furniture and trampolines, trim limbs that overhang the roof before storm season and park vehicles under cover.</p></article>
      <article class="factor reveal"><span class="factor__icon"><?= icon('cloud-hail') ?></span><h3>Hail alerts</h3><p>Hail one inch or larger (quarter-size) meets the National Weather Service severe threshold and can bruise asphalt shingles. Dented gutters, vents and AC fins after a storm are good reasons to request an inspection.</p></article>
      <article class="factor reveal"><span class="factor__icon"><?= icon('cloud-rain') ?></span><h3>Heavy rain</h3><p>Downpours expose weak flashing, cracked pipe boots and clogged gutters. Clear gutters before a big rain event and check ceilings and the attic (if safe) afterward for new stains.</p></article>
      <article class="factor reveal"><span class="factor__icon"><?= icon('thermometer') ?></span><h3>Extreme heat</h3><p>Triple-digit days push dark shingle temperatures far higher than the air. Good attic ventilation reduces heat stress on shingles. Heat also makes shingles soft, so roofs should not be walked on casually in midday sun.</p></article>
      <article class="factor reveal"><span class="factor__icon"><?= icon('snowflake') ?></span><h3>Winter freezes</h3><p>Occasional hard freezes can crack brittle shingles and burst attic plumbing. Ice is rare but dangerous; never go on a frosted or icy roof.</p></article>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container split split--top">
    <div class="split__copy reveal">
      <h2 class="section-title">Preparing Your Roof for Severe Weather</h2>
      <ul class="check-list">
        <li><?= icon('check') ?><span>Clean gutters and downspouts so heavy rain drains away from the roof edge and foundation.</span></li>
        <li><?= icon('check') ?><span>Have overhanging limbs trimmed back by a tree professional.</span></li>
        <li><?= icon('check') ?><span>Fix known problems — loose shingles, cracked pipe boots, lifted flashing — before storm season.</span></li>
        <li><?= icon('check') ?><span>Take dated photos of your roof and home exterior now, so you have a "before" record.</span></li>
        <li><?= icon('check') ?><span>Know your insurance policy's wind/hail deductible and claim-reporting requirements.</span></li>
      </ul>
    </div>
    <div class="split__copy reveal">
      <h2 class="section-title">Inspecting Safely After a Storm</h2>
      <ul class="check-list">
        <li><?= icon('check') ?><span>Wait until the storm has fully passed and lightning has stopped.</span></li>
        <li><?= icon('check') ?><span>Stay clear of downed power lines and hanging limbs; report lines to the utility.</span></li>
        <li><?= icon('check') ?><span>Look from the ground: missing shingles, debris, dented gutters, granules at downspouts.</span></li>
        <li><?= icon('check') ?><span>Check ceilings and, if safely accessible, the attic for water.</span></li>
        <li><?= icon('check') ?><span>Never climb onto the roof — use our <a href="/tools/storm-damage-checklist/">storm damage self-check</a> and call a professional.</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="section">
  <div class="container container--narrow">
    <?= faq_html($faqs, 'Temple Weather Page FAQs') ?>
  </div>
</section>
<?php final_cta('Storm Coming or Just Passed? Schedule a Free Roof Inspection.', 'If wind, hail or heavy rain has hit your part of Temple, we will check your roof for free and document what we find with photos.', '/weather/'); ?>
<?php layout_end();
