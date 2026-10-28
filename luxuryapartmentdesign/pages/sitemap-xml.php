<?php
header('Content-Type: application/xml; charset=utf-8');
$urls = [['/', date('Y-m-d'), '1.0'], ['/blogs/', date('Y-m-d'), '0.8'], ['/tools/', date('Y-m-d'), '0.9']];
foreach (TOOLS as $s => $_) $urls[] = ['/tools/' . $s . '/', '2026-10-28', '0.8'];
foreach (CATEGORIES as $s => $_) $urls[] = ['/category/' . $s . '/', date('Y-m-d'), '0.7'];
foreach (articles() as $a) $urls[] = ['/' . $a['slug'] . '/', $a['updated'] ?? $a['published'], '0.8'];
foreach (['/about-us/', '/editorial-policy/', '/contact/', '/privacy-policy/', '/terms-of-use/', '/sitemap/'] as $p) $urls[] = [$p, '2026-10-28', '0.3'];
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">' . "\n";
foreach ($urls as [$p, $mod, $pri]) {
    echo '  <url><loc>' . e(url($p)) . '</loc><lastmod>' . e($mod) . '</lastmod><priority>' . $pri . '</priority>';
    $slug = trim($p, '/');
    if (($a = article($slug))) {
        echo '<image:image><image:loc>' . e(url(img_url($a['image']))) . '</image:loc></image:image>';
    }
    echo "</url>\n";
}
echo '</urlset>';
