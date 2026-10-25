<?php
require_once __DIR__ . '/inc/layout.php';
http_response_code(404);
page_start([
    'title' => 'Page Not Found | Monetizing Influencers',
    'description' => 'That page moved or never existed. Find influencer monetization guides, free creator tools and platform playbooks on Monetizing Influencers.',
    'path' => '/404.php',
    'noindex' => true,
]);
?>
<section class="page-hero" style="text-align:center">
  <div class="hero-grid-bg" aria-hidden="true"></div>
  <div class="wrap narrow">
    <p class="big-num" style="font-size:clamp(5rem,18vw,10rem)">404</p>
    <h1 style="margin-inline:auto">This post went viral... in another dimension</h1>
    <p class="lead" style="margin-inline:auto">The page you were looking for has moved or does not exist. Try one of these instead.</p>
    <div class="btn-row" style="justify-content:center">
      <a class="btn btn-glow" href="/"><?= icon('rocket') ?> Home</a>
      <a class="btn btn-ghost" href="/monetization/">Monetization guide</a>
      <a class="btn btn-ghost" href="/tools/">Free tools</a>
      <a class="btn btn-ghost" href="/blogs/">Blog</a>
    </div>
  </div>
</section>
<?php page_end();
