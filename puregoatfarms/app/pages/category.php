<?php
defined('PGF') || exit;

$c = CATEGORIES[$slug];
$posts = posts_in($slug);
$crumbs = [['Home', '/'], ['Blog', '/blog/'], [$c['name'], "/category/$slug/"]];
$page = [
    'path'   => "/category/$slug/",
    'title'  => $c['name'] . ' — Goat Guides | Pure Goat Farms',
    'desc'   => $c['intro'],
    'crumbs' => $crumbs,
    'schema' => [
        ['@type' => 'CollectionPage', '@id' => SITE_URL . "/category/$slug/#webpage", 'url' => SITE_URL . "/category/$slug/", 'name' => $c['name'], 'isPartOf' => ['@id' => SITE_URL . '/#website']],
    ],
];
// Tools that fit this category.
$related = [
    'milking-dairy' => ['goat-milk-yield-calculator', 'goat-milk-production-estimator', 'goat-cheese-herd-calculator'],
    'farm-life'     => ['goat-feed-calculator', 'goat-gestation-calculator', 'goat-milk-converter'],
    'goat-breeds'   => ['dairy-goat-breed-finder', 'goat-milk-production-estimator', 'goat-feed-calculator'],
    'health-care'   => ['goat-gestation-calculator', 'goat-feed-calculator', 'goat-milk-yield-calculator'],
][$slug];
ob_start();
?>
<section class="page-hero">
  <div class="page-hero__bg" aria-hidden="true"><span class="blob blob--1"></span><span class="blob blob--2"></span></div>
  <div class="container">
    <?= breadcrumbs_html($crumbs) ?>
    <p class="eyebrow reveal"><span class="cat-num"><?= $c['num'] ?></span> Category</p>
    <h1 class="reveal"><?= e($c['name']) ?></h1>
    <p class="page-hero__lead reveal"><?= e($c['intro']) ?></p>
    <nav class="filter-bar reveal" aria-label="Categories">
      <a class="chip" href="/blog/">All</a>
<?php foreach (CATEGORIES as $s => $cc): ?>
      <a class="chip<?= $s === $slug ? ' is-on' : '' ?>" href="/category/<?= $s ?>/"<?= $s === $slug ? ' aria-current="page"' : '' ?>><?= e($cc['name']) ?></a>
<?php endforeach; ?>
    </nav>
  </div>
</section>
<section class="section section--tight">
  <div class="container">
<?php if ($posts): ?>
    <div class="post-grid">
<?php foreach ($posts as $s => $p): ?>
      <?= post_card($s, $p) ?>
<?php endforeach; ?>
    </div>
<?php else: ?>
    <p class="empty-state">New <?= e($c['name']) ?> guides are on the way.</p>
<?php endif; ?>
  </div>
</section>
<section class="section section--sand">
  <div class="container">
    <div class="section-head reveal"><p class="eyebrow">Put it to work</p><h2>Tools for <?= e(strtolower($c['name'])) ?></h2></div>
    <div class="tool-grid tool-grid--3">
<?php foreach ($related as $t): ?>
      <?= tool_card($t, TOOLS[$t]) ?>
<?php endforeach; ?>
    </div>
  </div>
</section>
<?php
render_page($page, ob_get_clean());
