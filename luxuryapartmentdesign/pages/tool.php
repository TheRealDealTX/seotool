<?php
/** @var array $tool */
$slug = $tool['slug'];
$path = '/tools/' . $slug . '/';
$crumbs = [['Home', '/'], ['Design Tools', '/tools/'], [$tool['name'], $path]];
[$guide] = add_heading_ids(tool_body($slug));
$schema = [
    [
        '@type' => 'WebApplication',
        '@id' => url($path) . '#app',
        'name' => $tool['name'],
        'url' => url($path),
        'description' => $tool['description'],
        'applicationCategory' => 'DesignApplication',
        'operatingSystem' => 'Any (web browser)',
        'offers' => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'],
        'publisher' => ['@id' => url('/#organization')],
    ],
    schema_breadcrumbs($crumbs),
    schema_faq($tool['faq']),
];
if ($tool['how_to']) {
    $schema[] = [
        '@type' => 'HowTo',
        'name' => 'How to use the ' . $tool['name'],
        'step' => array_map(fn($s, $i) => ['@type' => 'HowToStep', 'position' => $i + 1, 'text' => $s], $tool['how_to'], array_keys($tool['how_to'])),
    ];
}
page_head([
    'title' => $tool['title'],
    'description' => $tool['description'],
    'path' => $path,
    'schema' => $schema,
    'scripts' => ['tools/' . $slug . '.js'],
    'body_class' => 'is-tool',
]);
?>
<section class="page-hero page-hero--tool">
  <div class="container">
    <?= breadcrumbs_html($crumbs) ?>
    <p class="eyebrow">Free design tool</p>
    <h1><?= e($tool['h1']) ?></h1>
    <?php if ($tool['intro']): ?><p class="page-hero__lead"><?= e($tool['intro']) ?></p><?php endif; ?>
  </div>
</section>
<section class="section section--tool">
  <div class="container">
    <div class="tool-app" id="tool-app" data-tool="<?= e($slug) ?>">
      <?php require dirname(__DIR__) . '/templates/tools/' . $slug . '.php'; ?>
    </div>
    <p class="tool-note">Results are planning guidelines based on standard interior design rules of thumb. Always measure twice and check product dimensions before you buy.</p>
  </div>
</section>
<?php if ($tool['how_to']): ?>
<section class="section section--tint">
  <div class="container container--narrow">
    <h2 class="section__title">How to use the <?= e($tool['name']) ?></h2>
    <ol class="steps">
      <?php foreach ($tool['how_to'] as $s): ?><li><?= e($s) ?></li><?php endforeach; ?>
    </ol>
  </div>
</section>
<?php endif; ?>
<section class="section">
  <div class="container container--narrow">
    <div class="prose"><?= $guide ?></div>
    <?= faq_block($tool['faq']) ?>
  </div>
</section>
<?php
$rel = array_filter(array_map('article', $tool['related']));
if ($rel): ?>
<section class="section section--tint">
  <div class="container">
    <h2 class="section__title">Related guides</h2>
    <div class="grid grid--3"><?php foreach ($rel as $r) echo article_card($r); ?></div>
  </div>
</section>
<?php endif; ?>
<section class="section">
  <div class="container">
    <h2 class="section__title">More free design tools</h2>
    <div class="grid grid--4 tools-grid">
      <?php foreach (array_keys(TOOLS) as $t) if ($t !== $slug) echo tool_card($t); ?>
    </div>
  </div>
</section>
<?php page_foot(['scripts' => ['tools/' . $slug . '.js']]); ?>
