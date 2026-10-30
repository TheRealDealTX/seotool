<?php page_start(['robots' => 'noindex,follow']); ?>
<section class="page-hero"><div class="wrap narrow">
  <p class="eyebrow">Error 404</p>
  <h1>That page is not on the blueprint</h1>
  <p class="lead">The page you were looking for has moved or never existed. Most of the old store pages now live under our new plan and style guides.</p>
  <p><a class="btn" href="/tiny-house-plans/">Browse tiny house plans</a> <a class="btn btn-outline" href="/tools/">Try the free tools</a></p>
</div></section>
<section class="section"><div class="wrap">
  <h2>Popular pages</h2>
  <?php route_cards('style', '', 6); ?>
</div></section>
<?php page_end(); ?>
