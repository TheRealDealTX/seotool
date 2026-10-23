<?php defined('SS_APP') || exit;
echo page_hero($GLOBALS['ss_route'], 'Every page on Saffron Supplement, grouped by section. Search engines can use the <a href="/sitemap.xml">XML sitemap</a>.');
$groups = [
    'Reviews & Home' => ['/', '/best-saffron-supplements/', '/faq/'],
    'Benefits' => [], 'Guides' => [], 'Blog' => [], 'Free Tools' => [],
    'Company & Legal' => ['/about/', '/contact/', '/affiliate-disclosure/', '/medical-disclaimer/', '/privacy-policy/', '/terms/'],
];
foreach (ROUTES as $p => $r) {
    if ($p === '/saffron-benefits/' || ($r['parent'] ?? null) === '/saffron-benefits/') $groups['Benefits'][] = $p;
    elseif ($p === '/guides/' || ($r['parent'] ?? null) === '/guides/') $groups['Guides'][] = $p;
    elseif ($p === '/blog/' || ($r['parent'] ?? null) === '/blog/') $groups['Blog'][] = $p;
    elseif ($p === '/tools/' || ($r['parent'] ?? null) === '/tools/') $groups['Free Tools'][] = $p;
}
?>
<div class="wrap section">
  <div class="grid g3">
  <?php foreach ($groups as $label => $paths): ?>
    <div class="side-box">
      <h2><?= e($label) ?></h2>
      <ul><?php foreach ($paths as $p): ?><li><a href="<?= e($p) ?>"><?= e($p === '/' ? SITE_NAME . ' Home' : ROUTES[$p]['h1']) ?></a></li><?php endforeach; ?></ul>
    </div>
  <?php endforeach; ?>
  </div>
</div>
