<?php
defined('ERE') or exit;
header('Content-Type: application/xml; charset=utf-8');
$latest = max(array_map(fn($p) => $p['updated'], all_posts()) ?: [date('Y-m-d')]);
$urls = [['/', $latest, '1.0'], ['/blog/', $latest, '0.9'], ['/tools/', $latest, '0.9'], ['/recommended-products/', $latest, '0.6']];
foreach (all_posts() as $p) $urls[] = [$p['url'], $p['updated'], '0.8'];
foreach (cfg('categories') as $s => $c) $urls[] = ['/category/' . $s . '/', $latest, '0.6'];
foreach (tools() as $t) $urls[] = [$t['url'], $latest, '0.8'];
foreach (['about', 'contact', 'write-for-us', 'affiliate-disclosure', 'privacy-policy', 'terms'] as $s) $urls[] = ['/' . $s . '/', '2026-11-19', '0.3'];
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n" . '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
foreach ($urls as [$u, $d, $pr]) echo '  <url><loc>' . e(abs_url($u)) . '</loc><lastmod>' . e($d) . '</lastmod><priority>' . $pr . "</priority></url>\n";
echo "</urlset>\n";
