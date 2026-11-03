<?php
/** /sitemap.xml generated from the route registry. */
defined('SCC') || exit;
header('Content-Type: application/xml; charset=utf-8');
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">' . "\n";
foreach (routes() as $path => [$kind, $src, $sec]) {
    $lastmod = BUILD_DATE; $img = null;
    if ($kind === 'article') { $a = article($src); $lastmod = $a['updated'] ?? BUILD_DATE; $img = $a['image'] ?? null; }
    if ($kind === 'tool') { $a = article("tool-$src"); $lastmod = $a['updated'] ?? BUILD_DATE; }
    $pri = $path === '/' ? '1.0' : ($sec === 'pillar' || $path === '/tools/' ? '0.9' : ($kind === 'page' && !in_array($path, ['/solar-camera-guides/', '/tools/'], true) ? '0.3' : '0.7'));
    echo "  <url><loc>" . e(abs_url($path)) . "</loc><lastmod>$lastmod</lastmod><priority>$pri</priority>";
    if ($img) echo '<image:image><image:loc>' . e(img_url($img)) . '</image:loc></image:image>';
    echo "</url>\n";
}
echo "</urlset>\n";
