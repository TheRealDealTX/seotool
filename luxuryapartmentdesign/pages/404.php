<?php
page_head([
    'title' => 'Page Not Found | ' . SITE_NAME,
    'description' => 'The page you were looking for could not be found.',
    'path' => '/404/',
    'robots' => 'noindex, follow',
]);
?>
<section class="page-hero">
  <div class="container container--narrow">
    <p class="eyebrow">Error 404</p>
    <h1>This room is still empty</h1>
    <p class="page-hero__lead">The page you were looking for has moved or no longer exists. Try a search, or start with one of our most popular guides.</p>
    <form class="search-form" action="/search/" method="get">
      <label class="sr-only" for="q404">Search</label>
      <input id="q404" type="search" name="q" placeholder="Search guides and tools">
      <button class="btn btn--gold" type="submit">Search</button>
    </form>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="grid grid--3">
      <?php foreach (['luxury-apartment-interior-design', 'small-apartment-ideas', 'apartment-decorating-ideas'] as $s) if ($a = article($s)) echo article_card($a); ?>
    </div>
  </div>
</section>
<?php page_foot(); ?>
