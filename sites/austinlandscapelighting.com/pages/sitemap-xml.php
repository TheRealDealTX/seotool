<?php
declare(strict_types=1);
if (!defined('ALL_SITE')) { http_response_code(404); exit; }

$today = date('Y-m-d');
$urls = [
    ['/', $today, '1.0'],
    ['/services/', $today, '0.9'],
    ['/service-areas/', $today, '0.8'],
    ['/tools/', $today, '0.8'],
    ['/gallery/', $today, '0.6'],
    ['/blog/', $today, '0.7'],
    ['/about-us/', $today, '0.6'],
    ['/reviews/', $today, '0.6'],
    ['/faq/', $today, '0.6'],
    ['/contact/', $today, '0.8'],
    ['/sitemap/', $today, '0.2'],
];
foreach (services() as $s) $urls[] = [$s['path'], $today, '0.9'];
foreach (areas() as $a) $urls[] = [$a['path'], $today, '0.8'];
foreach (tools() as $t) $urls[] = [$t['path'], $today, '0.7'];
foreach (posts() as $p) $urls[] = [$p['path'], $p['modified'] ?? $p['published'], '0.7'];

header('Content-Type: application/xml; charset=utf-8');
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
foreach ($urls as [$path, $mod, $pri]) {
    echo "  <url><loc>" . e(url($path)) . "</loc><lastmod>" . e($mod) . "</lastmod><priority>{$pri}</priority></url>\n";
}
echo "</urlset>\n";
