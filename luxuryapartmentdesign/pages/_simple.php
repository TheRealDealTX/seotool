<?php
// Shared shell for text pages. Expects $sp = [path, crumb, title, description, h1, lead, html, schema_type].
$crumbs = [['Home', '/'], [$sp['crumb'], $sp['path']]];
page_head([
    'title' => $sp['title'],
    'description' => $sp['description'],
    'path' => $sp['path'],
    'schema' => [['@type' => $sp['schema_type'] ?? 'WebPage', '@id' => url($sp['path']), 'name' => $sp['h1'], 'isPartOf' => ['@id' => url('/#website')]], schema_breadcrumbs($crumbs)],
]);
?>
<section class="page-hero">
  <div class="container container--narrow">
    <?= breadcrumbs_html($crumbs) ?>
    <h1><?= e($sp['h1']) ?></h1>
    <?php if (!empty($sp['lead'])): ?><p class="page-hero__lead"><?= e($sp['lead']) ?></p><?php endif; ?>
  </div>
</section>
<section class="section">
  <div class="container container--narrow prose"><?= $sp['html'] ?></div>
</section>
<?php page_foot(); ?>
