<?php
layout_start(['title' => 'Page not found', 'description' => 'The page you were looking for could not be found.', 'path' => $_SERVER['REQUEST_URI'] ?? '/', 'robots' => 'noindex, follow']);
?>
<section class="section notfound">
  <div class="wrap narrow center">
    <p class="big-404">404</p>
    <h1>We couldn't find that page</h1>
    <p class="lead">It may have moved. Try searching, or start from one of these pages.</p>
    <form class="inline-search" action="/" method="get" role="search"><input type="search" name="s" placeholder="Search listings and guides" aria-label="Search"><button class="btn btn-primary" type="submit"><?= icon('search') ?> Search</button></form>
    <p class="btn-row"><a class="btn btn-outline" href="/properties/">Browse listings</a><a class="btn btn-outline" href="/marine-bases/">Military bases</a><a class="btn btn-outline" href="/blog/">Blog</a></p>
  </div>
</section>
<?php layout_end();
