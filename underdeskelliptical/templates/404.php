<?php
if (!defined('ROOT')) { http_response_code(404); exit; }
page_start(['title' => 'Page Not Found | ' . SITE_NAME, 'description' => 'That page could not be found.', 'noindex' => true]);
?>
<section class="page-hero"><div class="wrap narrow">
  <h1>Sorry, that page is not here</h1>
  <p class="lead">Try a search, or start with one of our most popular under desk elliptical guides.</p>
  <form action="/" method="get" class="big-search" role="search"><input type="search" name="s" aria-label="Search" placeholder="Search guides…"><button class="btn">Search</button></form>
</div></section>
<div class="wrap"><div class="grid grid-3"><?php foreach (array_slice(all_posts(), 0, 6) as $p) echo post_card($p); ?></div></div>
<?php page_end();
