<?php
declare(strict_types=1);
if (!defined('ALL_SITE')) { http_response_code(404); exit; }

$crumbs = [['Home', '/'], ['Reviews', '/reviews/']];
$page = [
    'title' => 'Austin Landscape Lighting Reviews | 4.9 Stars on Google',
    'description' => 'What Austin homeowners and business owners say about Austin Landscape Lighting: design quality, clean installs, honest pricing and 4.9 stars on Google.',
    'path' => '/reviews/',
    'active' => '/reviews/',
    'image' => 'landscape-lighting-austin-3',
    'schema' => [schema_webpage(['title' => 'Reviews', 'description' => 'Austin Landscape Lighting reviews.', 'path' => '/reviews/']), schema_breadcrumb($crumbs)],
];
ob_start();
echo sub_hero(['eyebrow' => 'Reviews', 'h1' => 'Austin Homeowners Love What They See', 'intro' => 'Austin Landscape Lighting holds a 4.9-star rating across 127 Google reviews. Here is a sample of what clients in Tarrytown, Westlake Hills, Rollingwood, Cedar Park and East Austin have said.', 'image' => 'landscape-lighting-austin-3', 'image_alt' => 'Austin home lit at night by Austin Landscape Lighting', 'crumbs' => $crumbs, 'meta' => '<p class="rating-badge" style="margin-top:14px"><span class="stars">' . str_repeat(icon('star', 'ico ico--star'), 5) . '</span> 4.9 · 127 Google reviews</p>']);
?>
<section class="section">
  <div class="container">
    <div class="reviews-grid"><?php foreach (REVIEWS as $i => $r) echo review_card($r, $i); ?></div>
  </div>
</section>
<section class="section section--alt">
  <div class="container feature-split">
    <div class="feature-split__media" data-reveal="left"><?= picture('custom-landscape-lighting-austin-1', 'Custom landscape lighting in Austin', ['width' => 1600, 'height' => 1200]) ?></div>
    <div data-reveal="right">
      <p class="eyebrow">Why the ratings</p>
      <h2 class="display">What clients mention most</h2>
      <ul class="checks">
        <li><?= icon('pencil') ?><div><strong>The design conversation</strong><span>Clients consistently say we were the only company that asked what they wanted the house to feel like, not just where to put lights.</span></div></li>
        <li><?= icon('dollar') ?><div><strong>Quoted price, final price</strong><span>Written estimates with no change orders. The number you sign is the number you pay.</span></div></li>
        <li><?= icon('clock') ?><div><strong>Fast, tidy installs</strong><span>Most systems in a day, wire buried, beds restored, and a night aiming visit so every fixture is right.</span></div></li>
        <li><?= icon('warranty') ?><div><strong>We come back</strong><span>Two-year workmanship warranty and seasonal tune-ups keep systems looking like opening night.</span></div></li>
      </ul>
    </div>
  </div>
</section>
<?= cta_band('Add your name to the list', 'A free dusk consultation with Austin Landscape Lighting is the first step. No pressure, no obligation.') ?>
<?php
render_page($page, ob_get_clean());
