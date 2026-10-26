<?php
defined('HA_ROOT') || exit;
$count = count($listings);
?>
<section class="page-hero area-hero">
  <div class="page-hero-bg" aria-hidden="true"><img src="<?= e(($page['image'] ?? '') ?: '/assets/img/Houston-Skyline.webp') ?>" alt="" width="1600" height="700"></div>
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Houston Apartments</a><span>/</span><a href="/houston-apartments-neighborhoods/">Neighborhoods</a><span>/</span><span aria-current="page"><?= e($area['name']) ?></span></nav>
    <h1 class="fade-up"><?= e($page['title'] ?? $area['name'] . ' Apartments') ?></h1>
    <p class="hero-sub fade-up d1"><?= e($area['tag']) ?></p>
    <div class="hero-actions fade-up d2">
      <a class="btn btn-grad btn-lg" href="/apartments/?area=<?= e($area['slug']) ?>">Open <?= e($area['name']) ?> map search</a>
      <button class="btn btn-ghost-light btn-lg" type="button" data-lead>Ask a local locator</button>
    </div>
  </div>
</section>

<section class="section area-listings">
  <div class="wrap">
    <div class="section-head reveal">
      <div><span class="pill"><?= $count ?: 'New' ?> <?= $count === 1 ? 'community' : 'communities' ?></span><h2><?= e($area['name']) ?> apartments for rent</h2></div>
      <a class="link-arrow" href="/apartments/?area=<?= e($area['slug']) ?>">Filter &amp; draw on map</a>
    </div>
    <?php if ($listings): ?>
      <div class="cards-grid">
        <?php foreach ($listings as $i => $c): require HA_APP . '/views/partials/card.php'; endforeach ?>
      </div>
    <?php else: ?>
      <div class="empty-state reveal">
        <p>We’re adding <?= e($area['name']) ?> communities to the map right now. A locator can send you current availability today.</p>
        <button class="btn btn-grad" type="button" data-lead>Get <?= e($area['name']) ?> listings</button>
      </div>
    <?php endif ?>
  </div>
</section>

<?php if ($page): ?>
<section class="section">
  <div class="wrap prose-grid">
    <article class="prose wp-content reveal"><?= $page['content'] ?></article>
    <aside class="side-card sticky reveal d1">
      <h3>Moving to <?= e($area['name']) ?>?</h3>
      <p>Tell us your budget and move date – we’ll send a short list of <?= e($area['name']) ?> apartments with current specials.</p>
      <button class="btn btn-grad btn-block" type="button" data-lead>Get my short list</button>
      <h4>Other areas</h4>
      <ul class="side-links">
        <?php foreach (AREAS as $k => $a): if ($k === $area['slug']) continue; ?><li><a href="/<?= $k ?>/"><?= e($a['name']) ?></a></li><?php endforeach ?>
      </ul>
    </aside>
  </div>
</section>
<?php endif ?>
