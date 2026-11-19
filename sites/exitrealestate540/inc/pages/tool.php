<?php
defined('ERE') or exit;
require ROOT . '/inc/tool-views.php';
$crumbs = [['Home', '/'], ['Free Tools', '/tools/'], [$tool['name'], $tool['url']]];
$schema = [[
    '@type' => 'WebApplication',
    'name' => $tool['name'],
    'url' => abs_url($tool['url']),
    'description' => $tool['description'],
    'applicationCategory' => 'FinanceApplication',
    'operatingSystem' => 'Any (web browser)',
    'offers' => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'],
    'publisher' => ['@id' => abs_url('/#organization')],
]];
if (!empty($tool['faq'])) $schema[] = schema_faq($tool['faq']);
page_head([
    'title' => $tool['title'] . ' | ' . cfg('short'),
    'description' => $tool['description'],
    'path' => $tool['url'],
    'crumbs' => $crumbs,
    'schema' => $schema,
    'body_class' => 'tool-page',
]);
$others = array_slice(array_values(array_filter(array_keys(tools()), fn($s) => $s !== $tool['slug'] && tools()[$s]['group'] === $tool['group'])), 0, 3);
if (count($others) < 3) $others = array_slice(array_values(array_unique(array_merge($others, array_filter(array_keys(tools()), fn($s) => $s !== $tool['slug'])))), 0, 3);
?>
<section class="page-head page-head--tool">
  <div class="wrap">
    <?php breadcrumbs($crumbs); ?>
    <h1><?= e($tool['title']) ?></h1>
    <p class="lead"><?= e($tool['intro']) ?></p>
  </div>
</section>
<section class="section section--compact">
  <div class="wrap">
    <?= tool_view($tool['slug']) ?>
    <p class="fine">Estimates only. Results depend on the inputs you provide and are not a loan offer, appraisal, tax bill or claim determination.</p>
  </div>
</section>
<section class="section section--compact">
  <div class="wrap wrap--narrow prose">
<?php foreach ($tool['how'] as [$h, $p]): ?>
    <h2><?= e($h) ?></h2>
    <p><?= $p ?></p>
<?php endforeach; ?>
<?php if (!empty($tool['faq'])): ?>
    <section class="faq">
      <h2>Frequently asked questions</h2>
<?php foreach ($tool['faq'] as [$q, $a]): ?>
      <details><summary><?= e($q) ?></summary><p><?= e($a) ?></p></details>
<?php endforeach; ?>
    </section>
<?php endif; ?>
  </div>
</section>
<?php $guides = array_filter(array_map('get_post', $tool['posts'] ?? [])); if ($guides): ?>
<section class="section section--tint">
  <div class="wrap">
    <div class="section__head"><h2>Related guides</h2></div>
    <div class="grid">
<?php foreach (array_slice($guides, 0, 3) as $p) echo post_card($p); ?>
    </div>
  </div>
</section>
<?php endif; ?>
<section class="section">
  <div class="wrap">
    <div class="section__head"><h2>More free tools</h2><a class="more" href="/tools/">All tools <?= icon('arrow') ?></a></div>
    <div class="tool-grid">
<?php foreach ($others as $s) echo tool_card($s); ?>
    </div>
  </div>
</section>
<?php page_foot(['scripts' => ['js/tools.js']]);
