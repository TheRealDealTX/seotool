<?php
// XML sitemap built from the page list + blog posts, using the host the site is served from.
$urls = [
    ['/', date('Y-m-d'), '1.0'],
    ['/tools/', '2026-10-19', '0.8'],
    ['/salary-calculator/', '2026-10-19', '0.9'],
    ['/cat-deployment-calculator/', '2026-10-19', '0.8'],
    ['/public-adjuster-fee-calculator/', '2026-10-19', '0.8'],
    ['/salary-by-state/', '2026-10-19', '0.9'],
    [BLOG_BASE, array_values(all_posts())[0]['date'] ?? '2026-10-19', '0.8'],
    ['/about/', '2026-10-19', '0.4'],
    ['/privacy-policy/', '2026-10-19', '0.2'],
    ['/terms-of-use/', '2026-10-19', '0.2'],
];
foreach (all_posts() as $p) {
    $urls[] = [post_url($p), $p['updated'] ?? $p['date'], '0.7'];
}
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
foreach ($urls as [$loc, $mod, $prio]) {
    echo '  <url><loc>' . e(base_url() . $loc) . '</loc><lastmod>' . e($mod) . '</lastmod><priority>' . $prio . "</priority></url>\n";
}
echo '</urlset>' . "\n";
