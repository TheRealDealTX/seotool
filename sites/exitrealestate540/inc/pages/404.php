<?php
defined('ERE') or exit;
page_head([
    'title' => 'Page not found | Exit Real Estate 540',
    'description' => 'The page you were looking for could not be found.',
    'path' => strtok($_SERVER['REQUEST_URI'] ?? '/', '?'),
    'robots' => 'noindex, follow',
]);
?>
<section class="page-head">
  <div class="wrap wrap--narrow">
    <h1>We could not find that page</h1>
    <p class="lead">It may have moved when we rebuilt the site. Try one of these instead:</p>
    <div class="hero__cta"><a class="btn btn--primary" href="/blog/">Browse all guides</a> <a class="btn btn--ghost" href="/tools/">Free calculators</a></div>
  </div>
</section>
<section class="section"><div class="wrap grid">
<?php foreach (array_slice(array_values(all_posts()), 0, 3) as $p) echo post_card($p); ?>
</div></section>
<?php page_foot();
