<?php
defined('SCC') || exit;
page_head([
    'title' => 'About Solar CCTV Camera: Who We Are & How We Work',
    'description' => 'Solar CCTV Camera is an independent, research-based resource for solar security cameras. Learn how we research, how we choose picks and how we make money.',
    'path' => '/about-us/',
    'schema' => [breadcrumb_schema([['Home', '/'], ['About Us', '/about-us/']]), ['@type' => 'AboutPage', 'name' => 'About Solar CCTV Camera', 'url' => abs_url('/about-us/')]],
]);
?>
<section class="page-hero"><div class="hero-sky" aria-hidden="true"><span class="hero-sun"></span></div><div class="wrap" style="position:relative">
  <?= breadcrumbs_html([['Home', '/'], ['About Us', '/about-us/']]) ?>
  <h1>About Solar CCTV Camera</h1>
  <p class="lede">We help people secure the places power cables don’t reach. SolarCCTVCamera.com covers one topic, solar-powered security cameras, in more depth than general tech sites can.</p>
</div></section>
<div class="legal prose wrap">
  <h2>Why this site exists</h2>
  <p>Solar cameras look simple: a camera, a battery and a small panel. In practice, whether one works for you comes down to details most reviews skip: how many peak sun hours your location gets in December, whether your Wi‑Fi reaches the gate, how much 4G data a busy driveway burns, and how cold mornings stop lithium batteries from charging. Those details are what we write about.</p>
  <h2>How we research</h2>
  <p>We are a research publication, not a test lab, and we say so plainly. Our guides are built from:</p>
  <ul>
    <li>Manufacturer specifications and manuals (battery capacity, panel wattage, radio type, operating temperatures).</li>
    <li>Public solar resource data, such as NREL’s PVWatts and NOAA solar position calculations, for sun-hour and panel-angle guidance.</li>
    <li>Installer documentation, electrical codes and carrier documentation for cellular cameras.</li>
    <li>Patterns in owner reports, support forums and returns feedback, which we treat as signals to check rather than as proof.</li>
    <li>Plain energy math, shown openly in our <a href="/tools/">calculators</a> so you can check it.</li>
  </ul>
  <p>When a recommendation depends on an assumption, we state the assumption. When a spec is a manufacturer claim we can’t verify, we say that too.</p>
  <h2>How we choose products</h2>
  <p>Product picks are organised by situation (no Wi‑Fi, no subscription, multi-camera) rather than by a single “best” score, because the right solar camera depends on your sun, signal and property. We don’t publish star ratings for products we haven’t evaluated hands-on.</p>
  <h2>How we make money</h2>
  <p>Some product links are affiliate links (for example Amazon Associates). If you buy through them we may earn a commission at no extra cost to you. Commissions never decide which products we include, and we never accept payment for placement. Details are in our <a href="/affiliate-disclosure/">affiliate disclosure</a>.</p>
  <h2>Corrections and contact</h2>
  <p>Spotted an error, a spec change or a model that has been discontinued? Tell us through the <a href="/contact/">contact page</a> or email <a href="mailto:<?= SITE_EMAIL ?>"><?= SITE_EMAIL ?></a>. We update guides when the facts change and show the last-updated date on every page.</p>
</div>
<?php require_once ROOT . '/inc/article.php'; cta_band(); page_foot();
