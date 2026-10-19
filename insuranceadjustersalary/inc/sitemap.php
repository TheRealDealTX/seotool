<?php
// XML sitemap (pages + blog posts, with image entries) on the canonical domain.
$posts = all_posts();
$latest = max(array_map(fn($p) => $p['updated'] ?? $p['date'], $posts) ?: ['2026-10-19']);
$siteUpdated = '2026-10-19';

$urls = [
    ['/', max($latest, $siteUpdated), '1.0', 'hero-roof-inspection.webp'],
    ['/salary-calculator/', $siteUpdated, '0.9', 'analytics-laptop.webp'],
    ['/salary-by-state/', $siteUpdated, '0.9', 'miami-skyline.webp'],
    ['/cat-deployment-calculator/', $siteUpdated, '0.8', 'tornado-storm.webp'],
    ['/public-adjuster-fee-calculator/', $siteUpdated, '0.8', 'signing-documents.webp'],
    ['/tools/', $siteUpdated, '0.7', 'women-laptop.webp'],
    [BLOG_BASE, $latest, '0.8', 'office-team.webp'],
    ['/about/', $siteUpdated, '0.4', 'handshake.webp'],
    ['/privacy-policy/', $siteUpdated, '0.2', null],
    ['/terms-of-use/', $siteUpdated, '0.2', null],
];
foreach ($posts as $p) {
    $urls[] = [post_url($p), $p['updated'] ?? $p['date'], '0.7', $p['image']];
}

echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">' . "\n";
foreach ($urls as [$loc, $mod, $prio, $img]) {
    echo '  <url>' . "\n";
    echo '    <loc>' . e(base_url() . $loc) . "</loc>\n";
    echo '    <lastmod>' . e($mod) . "</lastmod>\n";
    echo '    <priority>' . $prio . "</priority>\n";
    if ($img) {
        echo '    <image:image><image:loc>' . e(base_url() . '/assets/img/' . $img) . "</image:loc></image:image>\n";
    }
    echo "  </url>\n";
}
echo '</urlset>' . "\n";
