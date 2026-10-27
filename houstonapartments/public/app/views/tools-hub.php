<?php defined('HA_ROOT') || exit; ?>
<section class="page-hero">
  <div class="page-hero-bg" aria-hidden="true"></div>
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Houston Apartments</a><span>/</span><span aria-current="page">Renter Tools</span></nav>
    <h1 class="fade-up">Free Tools for Houston Renters</h1>
    <p class="hero-sub fade-up d1">Budget, compare, plan and tour smarter – free calculators and checklists from the Houston Apartments team.</p>
  </div>
</section>
<section class="section">
  <div class="wrap tool-grid">
    <?php $i = 0; foreach (TOOLS as $slug => $t): ?>
      <a class="tool-card reveal d<?= $i++ % 3 ?>" href="<?= TOOLS_BASE . $slug ?>/">
        <span class="tool-ico" aria-hidden="true"><?= $t['icon'] ?></span>
        <h2><?= e($t['name']) ?></h2>
        <p><?= e($t['short']) ?></p>
        <span class="link-arrow">Open tool</span>
      </a>
    <?php endforeach ?>
  </div>
</section>
