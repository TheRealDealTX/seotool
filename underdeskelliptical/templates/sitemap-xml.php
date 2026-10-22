<?php
if (!defined('ROOT')) { http_response_code(404); exit; }
/** @var array $m */
header('Content-Type: application/xml; charset=utf-8');
header('X-Robots-Tag: noindex, follow');
$file = $m[1];
$latest = max(array_column(all_posts(), 'updated'));
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";

if (in_array($file, ['sitemap.xml', 'sitemap_index.xml', 'wp-sitemap.xml'])) {
    echo '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
    foreach (['post', 'page', 'category', 'post_tag'] as $s) {
        echo "  <sitemap><loc>" . SITE_URL . "/$s-sitemap.xml</loc><lastmod>{$latest}</lastmod></sitemap>\n";
    }
    echo "</sitemapindex>\n";
    return;
}

$urls = [];
if ($file === 'post-sitemap.xml') {
    $urls[] = ['/blog/', $latest];
    foreach (all_posts() as $p) {
        $urls[] = [$p['url'], $p['updated'], $p['image'] ?? null];
    }
} elseif ($file === 'page-sitemap.xml') {
    $urls[] = ['/', $latest];
    foreach (['about-us', 'contact', 'affiliate-disclosure', 'privacy-policy', 'terms-of-use', 'sitemap'] as $s) {
        $urls[] = ["/$s/", SITE_UPDATED];
    }
    $urls[] = ['/tools/', SITE_UPDATED];
    foreach (TOOLS as $s => $t) {
        $urls[] = ["/tools/$s/", SITE_UPDATED];
    }
} elseif ($file === 'category-sitemap.xml') {
    foreach (CATEGORIES as $s => $c) {
        if (array_filter(all_posts(), fn($p) => $p['category'] === $s || in_array($s, $p['also'] ?? []))) {
            $urls[] = ["/topic/$s/", $latest];
        }
    }
} else {
    foreach (TAGS as $s => $t) {
        if (count(array_filter(all_posts(), fn($p) => in_array($s, $p['tags']))) >= 3) {
            $urls[] = ["/tag/$s/", $latest];
        }
    }
}
echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">' . "\n";
foreach ($urls as $u) {
    echo '  <url><loc>' . e(SITE_URL . $u[0]) . '</loc><lastmod>' . e($u[1]) . '</lastmod>';
    if (!empty($u[2])) {
        echo '<image:image><image:loc>' . e(abs_url($u[2])) . '</image:loc></image:image>';
    }
    echo "</url>\n";
}
echo "</urlset>\n";
