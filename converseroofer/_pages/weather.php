<?php defined('ROUTER') or exit; ?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Converse, TX Weather, Hail Risk &amp; NWS Alerts | Converse Roofer</title>
<meta name="description" content="Live weather for Converse, TX: current conditions, 7-day forecast, hail and severe storm risk, and active NWS alerts. Updated automatically.">
<link rel="canonical" href="https://converseroofer.com/weather">
<meta property="og:title" content="Converse, TX Weather, Hail Risk &amp; NWS Alerts | Converse Roofer">
<meta property="og:description" content="Live weather for Converse, TX: current conditions, 7-day forecast, hail and severe storm risk, and active NWS alerts. Updated automatically.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://converseroofer.com/weather">
<meta property="og:image" content="https://converseroofer.com/assets/img/og-image.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon.png" type="image/png" sizes="64x64">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta name="theme-color" content="#0f1f33">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "RoofingContractor",
  "name": "Converse Roofer",
  "url": "https://converseroofer.com/",
  "telephone": "+1-956-465-6045",
  "image": "https://converseroofer.com/assets/img/logo.svg",
  "priceRange": "Free inspections",
  "address": {"@type": "PostalAddress", "addressLocality": "Converse", "addressRegion": "TX", "addressCountry": "US"},
  "areaServed": ["Converse TX","Kirby TX","Windcrest TX","Universal City TX","Live Oak TX","Schertz TX","Cibolo TX","Selma TX","St. Hedwig TX","San Antonio TX"],
  "description": "Live weather for Converse, TX: current conditions, 7-day forecast, hail and severe storm risk, and active NWS alerts. Updated automatically."
}
</script>
<script type="application/ld+json">{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://converseroofer.com/"}, {"@type": "ListItem", "position": 2, "name": "Weather", "item": "https://converseroofer.com/weather"}]}</script>
</head>
<body>
<div class="storm-bar">⚠️ Hit by the <a href="hail-storm-september-11-2026">September 11 hail storm</a>? Golf-ball hail fell on Converse &amp; Kirby. <a href="contact">Free inspection</a> · <a href="tel:+19564656045">956-465-6045</a></div>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="./"><img src="assets/img/logo.svg" alt="" width="40" height="40"><span>Converse Roofer<small>Hail &amp; storm roofing · Converse, TX</small></span></a>
    <button class="nav-toggle" aria-label="Menu" aria-expanded="false" aria-controls="nav">☰</button>
    <nav class="nav" id="nav"><a href="./">Home</a><a href="hail-storm-september-11-2026">Hail Storm</a><a href="areas/">Areas</a><a href="weather" class="active">Weather</a><a href="gallery">Photos</a><a href="blog/">Blog</a><a href="about">About</a><a href="contact">Contact</a><a class="btn primary" href="tel:+19564656045">📞 956-465-6045</a></nav>
  </div>
</header>
<main>
<section class="hero small"><img class="bg" src="https://images.unsplash.com/photo-1500674425229-f692875b0ab7?auto=format&fit=crop&w=1800&q=60" alt="" onerror="this.onerror=null;this.src='assets/img/scene-bg.svg'"><div class="shade"></div>
<div class="wrap"><div><div class="crumbs"><a href="./">Home</a> › Weather</div><h1>Converse, TX Live Weather &amp; Storm Alerts</h1><p class="lead">Current conditions, 7-day forecast, hail and severe-storm risk, and active National Weather Service alerts for Converse and the northeast side of San Antonio.</p></div></div></section>
<section class="section"><div class="wrap">
  <span class="eyebrow">Active alerts</span>
  <h2>NWS alerts for Converse</h2>
  <div id="wx-alerts"><div class="alert info"><h4>Checking for alerts…</h4><p>Pulling active alerts from the National Weather Service.</p></div></div>
</div></section>

<section class="section alt"><div class="wrap">
  <div class="wx-now">
    <div class="wx-card">
      <span class="eyebrow">Right now · Converse, TX</span>
      <div class="wx-big"><span class="ic" id="wx-icon">🌡️</span><div><div class="t"><span id="wx-temp">—</span></div><div id="wx-desc">Loading…</div></div></div>
      <div class="wx-kv">
        <div><span>Feels like</span><b id="wx-feels">—</b></div>
        <div><span>Humidity</span><b id="wx-hum">—</b></div>
        <div><span>Wind</span><b id="wx-wind">—</b></div>
        <div><span>Gusts</span><b id="wx-gust">—</b></div>
        <div><span>Precip (last hr)</span><b id="wx-precip">—</b></div>
        <div><span>Updated</span><b id="wx-updated">—</b></div>
      </div>
    </div>
    <div class="wx-card">
      <span class="eyebrow">Hail &amp; severe storm risk · next 48 hours</span>
      <p><span class="risk-pill low" id="wx-risk">Calculating…</span></p>
      <p>Risk is estimated from the forecast weather code, rain probability and peak gusts. It's a homeowner's heads-up, not an official outlook. For official severe weather outlooks see the <a href="https://www.spc.noaa.gov/products/outlook/" target="_blank" rel="noopener">Storm Prediction Center</a> and <a href="https://www.weather.gov/ewx/" target="_blank" rel="noopener">NWS Austin/San Antonio</a>.</p>
      <h3 style="margin-top:14px">If hail is in the forecast</h3>
      <ul class="checks" style="font-size:.95rem">
        <li>Move vehicles into the garage or under cover.</li>
        <li>Bring in patio cushions and cover the AC condenser if you can do it safely.</li>
        <li>Close blinds and stay away from windows during the storm.</li>
        <li>Afterward, photograph hail on the ground next to a coin or ruler before it melts.</li>
      </ul>
    </div>
  </div>
  <h3 style="margin-top:32px">7-day forecast</h3>
  <p class="wx-note">Days with thunderstorm or strong-gust potential are highlighted.</p>
  <div class="wx-days" id="wx-days"><div class="wx-day">Loading…</div></div>
  <p class="wx-note" style="margin-top:10px">Weather data from <a href="https://open-meteo.com/" target="_blank" rel="noopener">Open-Meteo</a>. Alerts from the <a href="https://www.weather.gov/" target="_blank" rel="noopener">National Weather Service</a>. Coordinates: 29.518, -98.316 (Converse, TX). Times are Central.</p>
</div></section>

<section class="section"><div class="wrap"><div class="gallery" style="grid-template-columns:repeat(3,1fr)"><figure><img src="https://images.unsplash.com/photo-1500674425229-f692875b0ab7?auto=format&fit=crop&w=800&q=70" alt="Dark storm clouds rolling in over a neighborhood" loading="lazy"   onerror="this.onerror=null;this.src='assets/img/scene-storm.svg'"><figcaption>Storm clouds over FM 78</figcaption></figure><figure><img src="https://images.unsplash.com/photo-1534088568595-a066f410bcda?auto=format&fit=crop&w=800&q=70" alt="Supercell thunderstorm building at dusk" loading="lazy"   onerror="this.onerror=null;this.src='assets/img/scene-storm.svg'"><figcaption>Cell building west of Converse</figcaption></figure><figure><img src="https://images.unsplash.com/photo-1428592953211-077101b2021b?auto=format&fit=crop&w=800&q=70" alt="Rain streaming down a window during a storm" loading="lazy"   onerror="this.onerror=null;this.src='assets/img/scene-storm.svg'"><figcaption>Heavy rain on the 11th</figcaption></figure></div></div></section>
<section class="section" style="padding-top:0"><div class="wrap"><article class="article">
<h2>Hail season on the northeast side</h2>
<p>Bexar County sits on the southern edge of Texas hail alley. Our biggest hail months are April through June, but as the <a href="hail-storm-september-11-2026">September 11, 2026 storm</a> proved, a single front in early fall can drop golf-ball stones with no warning beyond a few minutes. The northeast side of San Antonio, from Windcrest out through Converse, Kirby, Universal City and Schertz, takes a disproportionate share of those storms because of how cells track off the Hill Country and along I-35 and I-10.</p>
<h3>Recent severe weather affecting Converse and Kirby</h3>
<table class="data">
<tr><th>Date</th><th>Event</th><th>Roof impact</th></tr>
<tr><td>Sept 11, 2026</td><td>Severe thunderstorm, golf-ball hail (2–2.5" photographed), 60 mph gusts, 8,000+ outages</td><td>Widespread shingle bruising, dented metal, screen damage across Converse and Kirby</td></tr>
<tr><td>Late May 2026</td><td>Damaging wind storm in Kirby: downed trees, a truck pushed several houses down the street</td><td>Lifted and missing shingles, ridge cap damage, tree impacts</td></tr>
</table>
<figure class="fig"><img src="assets/img/storm-track-map.svg" alt="Schematic map of the September 11, 2026 hail track over Kirby, Converse and northeast San Antonio" loading="lazy" style="width:100%;height:auto;aspect-ratio:auto;object-fit:contain;box-shadow:none;border-radius:14px"><figcaption>The September 11 hail core over Kirby and Converse.</figcaption></figure>
<p><a class="btn dark" href="storms/">All storm reports</a></p>
<p class="small">Want your street checked against a specific storm date? <a href="contact">Send us the address</a> and we'll pull the radar and warning history for that day.</p>
</article></div></section>
<script src="assets/js/weather.js" defer></script>
</main>
<section class="cta-band">
  <div class="wrap">
    <div><h2>Think your roof took hail on 9/11?</h2><p>Free inspection, photo report, and straight answers. Serving Converse, Kirby, Windcrest, Universal City &amp; NE San Antonio.</p></div>
    <div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn dark lg" href="tel:+19564656045">Call 956-465-6045</a><a class="btn ghost lg" href="contact" style="border-color:#fff">Request Online</a></div>
  </div>
</section>
<footer class="site-footer">
  <div class="wrap">
    <div class="cols">
      <div>
        <a class="brand" href="./" style="margin-bottom:12px"><img src="assets/img/logo.svg" alt="" width="40" height="40"><span>Converse Roofer</span></a>
        <p>Local storm-damage roofing for Converse and the northeast side of San Antonio. Free hail inspections, written estimates, repairs and full replacements.</p>
        <a class="phone" href="tel:+19564656045">956-465-6045</a><br><small>Call or text · 7 days a week</small>
      </div>
      <div><h4>Pages</h4><ul><li><a href="./">Home</a></li><li><a href="hail-storm-september-11-2026">Hail Storm</a></li><li><a href="areas/">Areas</a></li><li><a href="weather">Weather</a></li><li><a href="gallery">Photos</a></li><li><a href="blog/">Blog</a></li><li><a href="about">About</a></li><li><a href="contact">Contact</a></li><li><a href="storms/">Storm Reports</a></li></ul></div>
      <div><h4>Services</h4><ul><li><a href="contact">Free hail inspections</a></li><li><a href="contact">Storm damage documentation</a></li><li><a href="contact">Roof replacement</a></li><li><a href="contact">Roof repair &amp; leaks</a></li><li><a href="contact">Gutters &amp; emergency tarping</a></li></ul></div>
      <div><h4>Service area</h4><ul><li><a href="areas/converse">Converse</a></li><li><a href="areas/kirby-windcrest">Kirby &amp; Windcrest</a></li><li><a href="areas/universal-city-live-oak">Universal City &amp; Live Oak</a></li><li><a href="areas/schertz-cibolo-selma">Schertz, Cibolo &amp; Selma</a></li><li><a href="areas/st-hedwig">St. Hedwig</a></li><li><a href="areas/ne-san-antonio">NE San Antonio</a></li></ul></div>
    </div>
    <div class="bottom"><span>© <span data-year></span> Converse Roofer · converseroofer.com</span><span>Texas law prohibits roofers from paying or waiving insurance deductibles (Tex. Bus. &amp; Com. Code §27.02). We never do.</span></div>
  </div>
</footer>
<div class="call-bar"><a href="tel:+19564656045">📞 Tap to call 956-465-6045 — free inspection</a></div>
<script src="assets/js/config.js"></script>
<script src="assets/js/analytics.js"></script>
<script src="assets/js/main.js"></script>
</body>
</html>