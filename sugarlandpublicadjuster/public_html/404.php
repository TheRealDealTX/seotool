<?php
require_once __DIR__ . '/inc/layout.php';
http_response_code(404);
page_start([
    'title' => 'Page Not Found | Sugar Land Public Adjuster',
    'description' => 'The page you were looking for could not be found. Find claim help from Sugar Land Public Adjuster.',
    'path' => current_path(),
    'robots' => 'noindex, follow',
]);
page_hero('Page not found', 'Sorry—that page doesn’t exist or has moved. These links will get you where you need to go.', [['Home', '/'], ['Page not found', current_path()]]);
?>
<section class="section">
  <div class="container">
    <div class="grid-3">
      <div class="card linked"><h3><a href="/">Home</a></h3><p>Start at the Sugar Land Public Adjuster homepage.</p></div>
      <div class="card linked"><h3><a href="/services/">Claim Services</a></h3><p>Hurricane, hail, water, fire, flood and commercial claims.</p></div>
      <div class="card linked"><h3><a href="/tools/">Tools &amp; Calculators</a></h3><p>Settlement, depreciation, fee and deadline calculators.</p></div>
      <div class="card linked"><h3><a href="/blog/">Blog</a></h3><p>Claim guides from Joseph Dittman, public adjuster.</p></div>
      <div class="card linked"><h3><a href="/sugar-land-weather/">Live Weather</a></h3><p>Current conditions, radar and NWS alerts for Sugar Land.</p></div>
      <div class="card linked"><h3><a href="/contact/">Contact</a></h3><p>Call or text <?= e(SITE['phone_display']) ?> for a free review.</p></div>
    </div>
  </div>
</section>
<?php page_end(); ?>
