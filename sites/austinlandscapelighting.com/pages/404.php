<?php
declare(strict_types=1);
if (!defined('ALL_SITE')) { http_response_code(404); exit; }

$page = [
    'title' => 'Page Not Found | Austin Landscape Lighting',
    'description' => 'The page you were looking for is not here. Find Austin Landscape Lighting services, service areas, tools and articles from the links below.',
    'path' => '/404/',
    'robots' => 'noindex, follow',
    'schema' => [],
];
ob_start(); ?>
<section class="error-page spotlight" data-spotlight>
  <div class="stars" data-stars></div>
  <div class="container" data-reveal>
    <p class="eyebrow">Lights out</p>
    <p class="display">404</p>
    <h1 class="display" style="font-size:clamp(1.6rem,3vw,2.4rem)">This page has gone dark</h1>
    <p class="lede" style="margin:0 auto 28px">The address may have changed when we rebuilt austinlandscapelighting.com. Try one of these instead, or head home.</p>
    <div class="cta-band__actions">
      <a class="btn btn--primary" href="/">Back to the homepage <?= icon('arrow') ?></a>
      <a class="btn btn--ghost" href="/services/">Services</a>
      <a class="btn btn--ghost" href="/blog/">Blog</a>
      <a class="btn btn--ghost" href="/contact/">Contact</a>
    </div>
  </div>
</section>
<?php
render_page($page, ob_get_clean());
