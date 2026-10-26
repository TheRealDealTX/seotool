<?php defined('HA_ROOT') || exit; ?>
<section class="page-hero">
  <div class="page-hero-bg" aria-hidden="true"><img src="/assets/img/Houston-Skyline.webp" alt="" width="1600" height="700"></div>
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Houston Apartments</a><span>/</span><span aria-current="page">Neighborhoods</span></nav>
    <h1 class="fade-up">Houston Apartments by Neighborhood</h1>
    <p class="hero-sub fade-up d1">From Inner Loop high-rises to master-planned suburbs – pick an area to see the map, local guide and every community we work with.</p>
  </div>
</section>
<section class="section">
  <div class="wrap hood-grid all">
    <?php $i = 0; foreach (AREAS as $k => $a): $c = $counts[$k]; ?>
      <a class="hood-tile reveal d<?= $i++ % 4 ?>" href="/<?= $k ?>/" style="--h: <?= (crc32($k) % 360) ?>">
        <span class="hood-name"><?= e($a['name']) ?></span>
        <span class="hood-tag"><?= e($a['tag']) ?></span>
        <span class="hood-meta"><?= $c['count'] ? $c['count'] . ' communit' . ($c['count'] === 1 ? 'y' : 'ies') : 'Coming soon' ?><?= $c['min'] ? ' · from ' . money($c['min']) : '' ?></span>
        <span class="hood-arrow" aria-hidden="true">→</span>
      </a>
    <?php endforeach ?>
  </div>
</section>
