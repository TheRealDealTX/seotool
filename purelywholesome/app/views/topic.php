<?php
/** @var string $key @var string $label @var string $blurb @var string $pillar @var array $posts @var array $toolSlugs @var array $crumbs */
$heroTitle = $label; $heroLede = e($blurb) . ' Every ' . e(strtolower($label)) . ' guide from Purely Wholesome Farm in one place.'; $heroEyebrow = count($posts) . ' guides';
include __DIR__ . '/partials/page-hero.php';
$index = posts_index();
$start = $index[$pillar] ?? null;
?>
<section class="section section--tight">
  <div class="wrap">
    <?php if ($start && $start['indexable']): ?>
      <a class="feature reveal" href="<?= post_url($start['slug']) ?>">
        <?php if ($start['image']): ?><img src="<?= e($start['image']) ?>" alt="" width="<?= (int)$start['image_w'] ?>" height="<?= (int)$start['image_h'] ?>"><?php endif ?>
        <span class="feature__text"><span class="eyebrow">Start here</span><strong><?= e($start['h1']) ?></strong><small><?= e($start['desc']) ?></small><span class="btn btn--primary">Read the guide <?= icon('arrow') ?></span></span>
      </a>
    <?php endif ?>
    <?php if ($toolSlugs): ?>
      <div class="topic-tools">
        <?php foreach ($toolSlugs as $slug): $t = tools()[$slug]; ?>
          <a class="tool-card tool-card--light reveal" href="/tools/<?= $slug ?>/"><span class="tool-card__icon tool-card__icon--<?= $t['color'] ?>"><?= icon($t['icon']) ?></span><strong><?= e($t['name']) ?></strong><small><?= e($t['short']) ?></small><span class="tool-card__go">Open tool <?= icon('arrow') ?></span></a>
        <?php endforeach ?>
      </div>
    <?php endif ?>
    <div class="cards">
      <?php foreach ($posts as $p): if ($start && $p['slug'] === $start['slug']) continue; ?><?= card($p, 'reveal') ?><?php endforeach ?>
    </div>
  </div>
</section>
