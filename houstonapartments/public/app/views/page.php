<?php defined('HA_ROOT') || exit; ?>
<section class="page-hero">
  <div class="page-hero-bg" aria-hidden="true"></div>
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Houston Apartments</a><span>/</span><span aria-current="page"><?= e($page['title']) ?></span></nav>
    <h1 class="fade-up"><?= e($page['title']) ?></h1>
  </div>
</section>
<?php if ($page['slug'] === 'about-houston-apartments'): ?>
<div class="wrap about-founder"><?php $founderVariant = 'full'; require HA_APP . '/views/partials/founder.php'; ?></div>
<?php endif ?>
<section class="section">
  <div class="wrap prose-grid">
    <article class="prose wp-content"><?= $page['content'] ?></article>
    <aside class="side-card sticky reveal d1">
      <h3>Start your search</h3>
      <p>Search every community on our live map, or let a locator build your short list for free.</p>
      <a class="btn btn-grad btn-block" href="/apartments/">Open map search</a>
      <button class="btn btn-outline btn-block" type="button" data-lead>Talk to a locator</button>
    </aside>
  </div>
</section>
