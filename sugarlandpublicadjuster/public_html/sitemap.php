<?php
/** Yoast-compatible XML sitemaps: /sitemap_index.xml, /page-sitemap.xml, /post-sitemap.xml, /category-sitemap.xml */
require __DIR__ . '/inc/config.php';
require __DIR__ . '/inc/posts.php';
require __DIR__ . '/inc/pages.php';

$map = $_GET['map'] ?? 'sitemap_index';
$o = SITE['origin'];
$latestPost = max(array_map(fn($p) => $p['modified'], POSTS));
header('Content-Type: application/xml; charset=UTF-8');
header('X-Robots-Tag: noindex, follow');
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";

function iso(string $d): string { return date('c', strtotime($d)); }

if ($map === 'sitemap_index') {
    echo '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
    foreach (['post-sitemap' => $latestPost, 'page-sitemap' => max(array_column(PAGES, 2)), 'category-sitemap' => $latestPost] as $name => $mod) {
        echo "  <sitemap><loc>$o/$name.xml</loc><lastmod>" . iso($mod) . "</lastmod></sitemap>\n";
    }
    echo "</sitemapindex>\n";
    exit;
}

echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">' . "\n";
if ($map === 'post-sitemap') {
    foreach (POSTS as $p) {
        echo "  <url><loc>$o/{$p['slug']}/</loc><lastmod>" . iso($p['modified']) . "</lastmod>"
           . "<image:image><image:loc>" . htmlspecialchars($o . $p['image']) . "</image:loc></image:image></url>\n";
    }
} elseif ($map === 'page-sitemap') {
    foreach (PAGES as [$path, , $mod]) {
        echo "  <url><loc>$o$path</loc><lastmod>" . iso($mod) . "</lastmod></url>\n";
    }
} elseif ($map === 'category-sitemap') {
    echo "  <url><loc>$o/category/general/</loc><lastmod>" . iso($latestPost) . "</lastmod></url>\n";
}
echo "</urlset>\n";
