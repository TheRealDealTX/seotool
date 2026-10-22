<?php
if (!defined('ROOT')) { http_response_code(404); exit; }
$crumbs = [['Home', '/'], ['Tools', '/tools/']];
page_start(['title' => 'Free Under Desk Elliptical Tools: Calculators, Quiz & Comparison', 'description' => 'Free interactive tools from ' . SITE_NAME . ': calorie calculator, steps converter, desk clearance checker, pedal timer, product quiz and comparison table.', 'schema' => [schema_breadcrumbs($crumbs)]]);
?>
<section class="page-hero"><div class="wrap">
  <?= breadcrumbs_html($crumbs) ?>
  <h1>Free Under Desk Elliptical Tools</h1>
  <p class="lead">Calculators and checkers that answer the questions people ask most before and after buying an under desk elliptical. Free, no sign-up, and they work on your phone.</p>
</div></section>
<div class="wrap">
  <div class="tool-grid big">
<?php foreach (TOOLS as $s => $o): ?>
    <a class="tool-tile" href="/tools/<?= e($s) ?>/"><strong><?= e($o['short']) ?></strong><span><?= e($o['description']) ?></span><em>Open tool &rarr;</em></a>
<?php endforeach; ?>
  </div>
</div>
<?php page_end();
