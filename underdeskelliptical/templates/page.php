<?php
if (!defined('ROOT')) { http_response_code(404); exit; }
/** @var array $page */
$crumbs = [['Home', '/'], [$page['h1'], CURRENT_PATH]];
page_start(['title' => $page['title'], 'description' => $page['description'], 'schema' => array_merge([schema_breadcrumbs($crumbs)], $page['schema'] ?? [])]);
?>
<section class="page-hero"><div class="wrap narrow">
  <?= breadcrumbs_html($crumbs) ?>
  <h1><?= e($page['h1']) ?></h1>
<?php if (!empty($page['lead'])): ?>  <p class="lead"><?= e($page['lead']) ?></p><?php endif; ?>
</div></section>
<div class="wrap narrow prose page-body">
<?= render_shortcodes($page['body']) ?>
</div>
<?php page_end();
