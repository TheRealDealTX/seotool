<?php
defined('INC') || exit;
/** @var string $slug @var array $g @var array $guides */
page_start([
    'title' => $g['title'],
    'description' => $g['description'],
    'path' => "/guides/$slug/",
    'type' => 'article',
]);
add_schema([
    '@type' => 'Article',
    'headline' => $g['h1'],
    'description' => $g['description'],
    'dateModified' => $g['updated'],
    'datePublished' => $g['updated'],
    'mainEntityOfPage' => abs_url("/guides/$slug/"),
    'author' => ['@type' => 'Organization', 'name' => SITE_NAME, 'url' => SITE_URL . '/'],
    'publisher' => ['@id' => SITE_URL . '/#org'],
    'image' => SITE_URL . '/assets/img/og-image.png',
]);
$related = array_slice(array_filter($guides, fn($o, $k) => $k !== $slug && $o['category'] === $g['category'], ARRAY_FILTER_USE_BOTH), 0, 3, true);
if (count($related) < 3) {
    $related += array_slice(array_filter($guides, fn($k) => $k !== $slug && !isset($related[$k]), ARRAY_FILTER_USE_KEY), 0, 3 - count($related), true);
}
?>
<div class="wrap">
  <?= breadcrumbs([['Guides', '/guides/'], [$g['h1'], "/guides/$slug/"]]) ?>
  <div class="layout-2">
    <article class="prose prose--article">
      <header class="article-head">
        <p class="eyebrow"><?= e($g['category']) ?> · <?= (int) $g['read_minutes'] ?> min read · Updated <time datetime="<?= e($g['updated']) ?>"><?= e(date('F j, Y', strtotime($g['updated']))) ?></time></p>
        <h1><?= e($g['h1']) ?></h1>
        <p class="lede"><?= e($g['intro']) ?></p>
      </header>
      <?= $g['body'] ?>
<?php if (!empty($g['products'])): ?>
      <section class="inline-picks">
        <h2>Gear we recommend</h2>
        <?= product_grid(array_map(fn($p) => $p + ['icon' => '🛍️'], $g['products'])) ?>
        <?= disclosure() ?>
      </section>
<?php endif; ?>
      <?= faq_block($g['faq'] ?? []) ?>
    </article>
    <aside class="side">
      <div class="side-card">
        <h2>Visit Vintique Flea</h2>
        <p>Curated vintage, salvage, antiques and food trucks at Silver Street Studios.</p>
        <a class="btn btn--primary btn--block" href="/events/">Market dates</a>
      </div>
<?php if (!empty($g['shop'])): ?>
      <div class="side-card">
        <h2>Shop the guide</h2>
        <ul class="side-links">
<?php foreach ($g['shop'] as $s): if (!isset(SHOP[$s])) continue; ?>
          <li><a href="/shop/<?= $s ?>/"><?= SHOP[$s]['icon'] ?> <?= e(SHOP[$s]['name']) ?></a></li>
<?php endforeach; ?>
        </ul>
      </div>
<?php endif; ?>
      <div class="side-card">
        <h2>Keep reading</h2>
        <ul class="side-links">
<?php foreach ($related as $rs => $r): ?>
          <li><a href="/guides/<?= $rs ?>/"><?= e($r['h1']) ?></a></li>
<?php endforeach; ?>
        </ul>
      </div>
    </aside>
  </div>
</div>
<?php page_end();
