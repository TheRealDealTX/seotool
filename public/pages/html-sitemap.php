<?php
defined('SCC') || (http_response_code(404) && exit);
page_head(['title' => 'Sitemap | Solar CCTV Camera', 'description' => 'Every page on SolarCCTVCamera.com: solar security camera guides, buying guides, use cases and free calculators.', 'path' => '/sitemap/',
    'schema' => [breadcrumb_schema([['Home', '/'], ['Sitemap', '/sitemap/']])]]);
?>
<section class="page-hero"><div class="wrap"><?= breadcrumbs_html([['Home', '/'], ['Sitemap', '/sitemap/']]) ?><h1>Sitemap</h1></div></section>
<div class="legal prose wrap">
  <h2>Guides</h2>
  <ul class="sitemap-list">
<?php foreach (articles() as $p => $a): ?>
    <li><a href="<?= e($p) ?>"><?= e($a['h1']) ?></a></li>
<?php endforeach; ?>
  </ul>
  <h2>Tools</h2>
  <ul class="sitemap-list">
<?php foreach (tools_meta() as $t): ?>
    <li><a href="<?= e($t['path']) ?>"><?= e($t['name']) ?></a></li>
<?php endforeach; ?>
  </ul>
  <h2>Site</h2>
  <ul class="sitemap-list">
<?php foreach (['/', '/solar-camera-guides/', '/tools/', '/about-us/', '/contact/', '/affiliate-disclosure/', '/privacy-policy/', '/terms-of-use/'] as $p): ?>
    <li><a href="<?= e($p) ?>"><?= e(route_title($p)) ?></a></li>
<?php endforeach; ?>
  </ul>
</div>
<?php page_foot();
