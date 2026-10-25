<?php
page_start(['breadcrumbs' => [['Home', '/'], ['Sitemap', null]]]);
$groups = ['Tiny house plans' => ['catalog', 'plan'], 'Styles' => ['style'], 'Free tools' => ['hub-tools', 'tool'], 'Guides' => ['hub-blog', 'guide'], 'Company' => ['home', 'company', 'legal']];
?>
<section class="page-hero"><div class="wrap"><h1>Sitemap</h1><p class="lead">Every page on Tiny Homes Blueprint.</p></div></section>
<section class="section" style="padding-top:0"><div class="wrap card-grid">
<?php foreach ($groups as $label => $types): ?>
  <div class="aside-box"><h2 style="font-size:1.2rem"><?= e($label) ?></h2><ul>
  <?php foreach ($ROUTES as $p => $r):
      $t = $r['type'] === 'hub' ? ($p === '/tools/' ? 'hub-tools' : 'hub-blog') : $r['type'];
      if (!in_array($t, $types, true)) continue;
      $name = $r['nav'] ?? preg_replace('/\s*\|.*$/', '', $r['title']); ?>
    <li><a href="<?= e($p) ?>"><?= e($name) ?></a></li>
  <?php endforeach; ?>
  </ul></div>
<?php endforeach; ?>
</div></section>
<?php page_end(); ?>
