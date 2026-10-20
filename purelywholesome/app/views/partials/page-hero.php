<?php /** @var array $crumbs @var string $heroTitle @var string $heroLede */ ?>
<header class="page-hero">
  <div class="page-hero__bg" aria-hidden="true"><span class="blob blob--1"></span><span class="blob blob--2"></span><span class="grain"></span></div>
  <div class="wrap">
    <?= breadcrumbs_html($crumbs) ?>
    <?php if (!empty($heroEyebrow)): ?><p class="eyebrow"><?= $heroEyebrow ?></p><?php endif ?>
    <h1><?= e($heroTitle) ?></h1>
    <?php if (!empty($heroLede)): ?><p class="page-hero__lede"><?= $heroLede ?></p><?php endif ?>
  </div>
</header>
