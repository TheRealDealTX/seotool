<?php
// XML sitemap built from the route registry.
header('Content-Type: application/xml; charset=utf-8');
$default = ['home' => '1.0', 'catalog' => '0.9', 'style' => '0.8', 'tool' => '0.8', 'guide' => '0.7', 'hub' => '0.8', 'plan' => '0.8', 'company' => '0.5', 'legal' => '0.2'];
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
foreach ($ROUTES as $path => $r) {
    $mod = $r['modified'] ?? $r['date'] ?? '2026-10-25';
    printf("  <url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>\n",
        e(SITE_URL . $path), e($mod), $r['priority'] ?? $default[$r['type']] ?? '0.5');
}
echo "</urlset>\n";
