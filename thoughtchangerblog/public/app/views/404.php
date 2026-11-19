<?php
view('head', ['meta' => ['title' => 'Page not found - ' . SITE_NAME, 'description' => '', 'canonical' => '/', 'robots' => 'noindex, follow', 'bodyClass' => 'error404']]);
?>
<section class="page-hero">
  <div class="wrap-narrow center">
    <p class="script-title big404">Lost in thought?</p>
    <h1 class="page-title">That page wandered off.</h1>
    <p class="page-lede">The link may be old or mistyped. Try a search, or start with one of our most-read reflections below.</p>
    <form class="search search-lg" role="search" action="/" method="get">
      <label class="sr-only" for="s404">Search</label>
      <input id="s404" type="search" name="s" placeholder="Search articles">
      <button type="submit" class="btn btn-accent">Search</button>
    </form>
  </div>
</section>
<section class="band">
  <div class="wrap">
    <div class="grid grid-3">
      <?php foreach (array_filter(array_map('post_by_slug', ['life-is-fleeting-5-ways-to-slow-it-down', 'heres-what-it-means-to-level-up', 'stick-to-your-lane'])) as $p) view('card', ['p' => $p]); ?>
    </div>
  </div>
</section>
<?php view('foot'); ?>
