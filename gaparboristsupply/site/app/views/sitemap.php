<?php
defined('GAP') || exit;
// HTML site map: every department and category, guides, tools, brands and site pages.
$meta = ['title' => 'Site Map', 'desc' => 'Every arborist gear department, category, buying guide, tool and brand on Gap Arborist Supply, on one page.', 'canonical' => '/sitemap/'];
$tree = function (string $path) use (&$tree, $CAT): string {
    $c = $CAT['categories'][$path];
    $h = '<li><a href="' . e($path) . '">' . e($c['name']) . '</a>';
    if ($c['children']) {
        $kids = $c['children'];
        usort($kids, fn($a, $b) => strcasecmp($CAT['categories'][$a]['name'], $CAT['categories'][$b]['name']));
        $h .= '<ul>' . implode('', array_map($tree, $kids)) . '</ul>';
    }
    return $h . '</li>';
};
$brands = $CAT['brands'];
uasort($brands, fn($a, $b) => strcasecmp($a['name'], $b['name']));
$pages = ['/about/' => 'About', '/contact/' => 'Contact', '/shop-all/' => 'Shop all gear', '/brands/' => 'Brands A–Z', '/guides/' => 'Buying guides',
    '/tools/' => 'Free tools', '/shipping-returns/' => 'Shipping & returns', '/affiliate-disclosure/' => 'Affiliate disclosure',
    '/privacy-policy/' => 'Privacy policy', '/terms-of-use/' => 'Terms of use', '/image-credits/' => 'Image credits', '/sitemap.xml' => 'XML sitemap'];
?>
<section class="cat-hero"><div class="wrap">
  <?= crumbs([['Site map', '/sitemap/']]) ?>
  <h1>Site map</h1>
  <p class="lede">Every department, category, buying guide, tool and brand in the store.</p>
</div></section>
<section class="wrap sitemap-page prose">
  <h2>Departments</h2>
  <ul class="sitemap-tree"><?php foreach ($CFG['departments'] as $d) if (isset($CAT['categories'][$d])) echo $tree($d); ?></ul>
  <div class="sitemap-cols">
    <div><h2>Buying guides</h2><ul><?php foreach ($CAT['guides'] as $g): ?><li><a href="<?= e($g['path']) ?>"><?= e($g['h1']) ?></a></li><?php endforeach; ?></ul></div>
    <div><h2>Free tools</h2><ul><?php foreach (TOOLS as $slug => $t): ?><li><a href="/tools/<?= $slug ?>/"><?= e($t[0]) ?></a></li><?php endforeach; ?></ul></div>
    <div><h2>Site pages</h2><ul><?php foreach ($pages as $p => $label): ?><li><a href="<?= e($p) ?>"><?= e($label) ?></a></li><?php endforeach; ?></ul></div>
  </div>
  <h2>Brands</h2>
  <ul class="sitemap-brands"><?php foreach ($brands as $b): ?><li><a href="<?= e($b['path']) ?>"><?= e($b['name']) ?></a></li><?php endforeach; ?></ul>
</section>
