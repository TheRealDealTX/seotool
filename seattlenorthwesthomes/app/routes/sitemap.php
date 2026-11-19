<?php defined('SNW') || (http_response_code(404) && exit);
header('Content-Type: application/xml; charset=utf-8');
$latest = array_values(posts())[0]['date'] ?? date('Y-m-d');
$urls = [['/', $latest, '1.0'], ['/homes-for-sale/', date('Y-m-d', max(array_map(fn($l) => strtotime($l['listed']), listings()))), '0.9'],
         ['/neighborhoods/', null, '0.8'], ['/blog/', $latest, '0.8'],
         ['/buy-a-home-in-seattle/', null, '0.8'], ['/sell-your-home-seattle/', null, '0.8'],
         ['/about-seattle-northwest-homes/', null, '0.5'], ['/contact-seattle-real-estate-agents/', null, '0.5'],
         ['/privacy-policy/', null, '0.2'], ['/terms-of-use/', null, '0.2']];
foreach (listings() as $l) $urls[] = ['/homes-for-sale/' . $l['slug'] . '/', $l['listed'], $l['status'] === 'Sold' ? '0.4' : '0.8'];
foreach (neighborhoods() as $s => $h) $urls[] = ['/neighborhoods/' . $s . '/', null, '0.7'];
foreach (categories() as $s => $c) $urls[] = ['/blog/category/' . $s . '/', null, '0.4'];
foreach (posts() as $po) $urls[] = ['/blog/' . $po['slug'] . '/', $po['modified'], '0.6'];
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n" . '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
foreach ($urls as [$u, $mod, $pri]) {
    echo '  <url><loc>' . e(abs_url($u)) . '</loc>' . ($mod ? '<lastmod>' . $mod . '</lastmod>' : '') . '<priority>' . $pri . '</priority></url>' . "\n";
}
echo '</urlset>' . "\n";
