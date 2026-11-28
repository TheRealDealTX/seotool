<?php
header('Content-Type: application/xml; charset=utf-8');
$latest = max(array_map(fn($a) => $a['updated'] ?? $a['date'], articles()) ?: [date('Y-m-d')]);
$urls = [['/', $latest, '1.0'], ['/tools', $latest, '0.9'], ['/blog', $latest, '0.8']];
foreach (tools() as $s => $t) $urls[] = ['/' . $s, '2026-11-28', '0.9'];
foreach (articles() as $a) $urls[] = ['/blog/' . $a['slug'], $a['updated'] ?? $a['date'], '0.7'];
foreach (['/study-supplies', '/about-us', '/contact', '/privacy-policy', '/terms-of-use', '/disclaimer', '/affiliate-disclosure', '/sitemap'] as $p) $urls[] = [$p, '2026-11-28', '0.3'];
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n" . '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
foreach ($urls as [$p, $d, $pr]) echo '  <url><loc>' . e(abs_url($p)) . '</loc><lastmod>' . e($d) . '</lastmod><priority>' . $pr . "</priority></url>\n";
echo '</urlset>';
