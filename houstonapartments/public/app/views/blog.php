<?php defined('HA_ROOT') || exit; ?>
<section class="page-hero">
  <div class="page-hero-bg" aria-hidden="true"><img src="/assets/img/Houston-Skyline.webp" alt="" width="1600" height="700"></div>
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Houston Apartments</a><span>/</span><span aria-current="page">Blog</span></nav>
    <h1 class="fade-up">Houston Apartments Blog</h1>
    <p class="hero-sub fade-up d1">Community reviews, amenity round-ups and renter guides from our Houston locators.</p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="post-grid">
      <?php foreach ($posts as $i => $post): require HA_APP . '/views/partials/post-card.php'; endforeach ?>
    </div>
    <?php if ($pages > 1): ?>
      <nav class="pager static" aria-label="Blog pages">
        <?php for ($n = 1; $n <= $pages; $n++): ?>
          <a href="<?= e($base . ($n > 1 ? "page/$n/" : '')) ?>"<?= $n === $page ? ' aria-current="page"' : '' ?>><?= $n ?></a>
        <?php endfor ?>
      </nav>
    <?php endif ?>
  </div>
</section>
