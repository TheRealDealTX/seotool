<?php
view('head', ['meta' => ['title' => 'Page not found - ' . SITE_NAME, 'description' => '', 'canonical' => '/', 'robots' => 'noindex, follow', 'bodyClass' => 'error404']]);
?>
<section class="page-hero">
  <div class="wrap-narrow center">
    <p class="script-title big404">Lost in thought?</p>
    <h1 class="page-title">That page wandered off.</h1>
    <p class="page-lede">The link may be old or mistyped. Try a search, or start with one of our most-read reflections below.</p>
    <form class="sbox js-suggest" role="search" action="/" method="get" autocomplete="off">
      <label class="sr-only" for="s404">Search articles</label>
      <svg class="sbox-icon" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M10 2a8 8 0 0 1 6.32 12.9l5.39 5.4-1.41 1.4-5.4-5.39A8 8 0 1 1 10 2Zm0 2a6 6 0 1 0 0 12 6 6 0 0 0 0-12Z"/></svg>
      <input id="s404" type="search" name="s" placeholder="Search articles" aria-autocomplete="list" aria-controls="s404-list" aria-expanded="false">
      <button type="submit" class="btn btn-accent">Search</button>
      <div class="suggest" id="s404-list" role="listbox" hidden></div>
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
