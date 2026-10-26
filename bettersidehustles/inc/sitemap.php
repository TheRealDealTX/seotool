<?php
// XML sitemaps. Keeps the Yoast URLs (sitemap_index.xml, post-sitemap.xml,
// page-sitemap.xml) that Search Console already knows about.

header('Content-Type: application/xml; charset=utf-8');
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";

$today = date('Y-m-d');

if ($path === '/sitemap.xml' || $path === '/sitemap_index.xml') {
    echo '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
    foreach (['post-sitemap.xml', 'page-sitemap.xml'] as $s) {
        echo "  <sitemap><loc>" . SITE_URL . "/$s</loc><lastmod>$today</lastmod></sitemap>\n";
    }
    echo "</sitemapindex>\n";
    return;
}

$urls = [];
if ($path === '/post-sitemap.xml') {
    $urls[] = ['/blog/', $today, null];
    foreach (all_posts() as $p) {
        $urls[] = [$p['url'], $p['modified'] ?? $p['published'], $p['image'] ?? null];
    }
} else {
    $urls[] = ['/', $today, SITE_IMAGE];
    $urls[] = ['/tools/', $today, null];
    foreach (TOOLS as $slug => $t) {
        $urls[] = ["/tools/$slug/", $today, null];
    }
    $urls[] = ['/side-hustle-gear/', $today, null];
    $urls[] = ['/contact/', $today, null];
    foreach (all_pages() as $p) {
        $urls[] = [$p['url'], $p['modified'] ?? $today, null];
    }
}

echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">' . "\n";
foreach ($urls as [$u, $mod, $img]) {
    echo '  <url><loc>' . e(SITE_URL . $u) . "</loc><lastmod>$mod</lastmod>";
    if ($img) {
        echo '<image:image><image:loc>' . e(abs_url($img)) . '</image:loc></image:image>';
    }
    echo "</url>\n";
}
echo "</urlset>\n";
