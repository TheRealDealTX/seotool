<?php
/** @var array $page */
[$body] = render_body($page['body']);
$meta = [
    'title' => $page['title'],
    'description' => $page['description'],
    'url' => $page['url'],
    'noindex' => !empty($page['noindex']),
    'schema' => [
        ['@type' => $page['schema_type'] ?? 'WebPage', 'name' => $page['h1'], 'url' => abs_url($page['url']), 'description' => $page['description'], 'isPartOf' => ['@id' => SITE_URL . '/#website']],
        schema_breadcrumbs([['Home', '/'], [$page['h1'], $page['url']]]),
        schema_faq($page['faq'] ?? []),
    ],
];
require __DIR__ . '/header.php';
?>
<section class="page-hero">
  <canvas class="coin-canvas" data-density="0.3" aria-hidden="true"></canvas>
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><?= e($page['h1']) ?></nav>
    <?php if (!empty($page['kicker'])): ?><span class="pill"><?= e($page['kicker']) ?></span><?php endif; ?>
    <h1><?= e($page['h1']) ?></h1>
    <?php if (!empty($page['dek'])): ?><p class="dek"><?= e($page['dek']) ?></p><?php endif; ?>
  </div>
</section>
<div class="page-body article-body">
  <?= $body ?>
  <?php if (!empty($page['modified'])): ?><p class="updated-note">Last updated <?= e(nice_date($page['modified'])) ?>.</p><?php endif; ?>
</div>
<?php require __DIR__ . '/footer.php'; ?>
