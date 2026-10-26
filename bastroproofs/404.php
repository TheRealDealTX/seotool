<?php
require_once __DIR__ . '/includes/bootstrap.php';
http_response_code(404);
page_start([
    'title'       => 'Page Not Found | Bastrop Roofing',
    'description' => 'The page you were looking for could not be found. Explore Bastrop Roofing services, tools and service areas.',
    'path'        => '/404/',
    'robots'      => 'noindex, follow',
]);
?>
<section class="page-hero">
  <canvas class="weather-canvas" data-weather="rain" aria-hidden="true"></canvas>
  <div class="container page-hero-inner center">
    <span class="eyebrow eyebrow-light">Error 404</span>
    <h1>Looks Like This Page Blew Off the Roof</h1>
    <p class="page-hero-lead">The page you were looking for has moved or does not exist. Try one of these instead.</p>
    <div class="hero-actions center">
      <a class="btn btn-primary" href="/">Bastrop Roofing Home</a>
      <a class="btn btn-outline" href="/services/">Roofing Services</a>
      <a class="btn btn-outline" href="/contact/">Contact Us</a>
    </div>
  </div>
  <div class="hero-shingles" aria-hidden="true"></div>
</section>
<section class="section"><div class="container"><div class="card-grid"><?php service_cards(); ?></div></div></section>
<?php page_end();
