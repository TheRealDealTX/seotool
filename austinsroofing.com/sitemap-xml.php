<?php
// XML sitemaps at the URLs Yoast used: /sitemap_index.xml, /page-sitemap.xml,
// /post-sitemap.xml, /category-sitemap.xml (rewritten here by .htaccess).
require __DIR__ . '/includes/config.php';

header('Content-Type: application/xml; charset=utf-8');
header('X-Robots-Tag: noindex, follow');
$type = $_GET['type'] ?? 'index';
$o = BIZ['origin'];
$x = fn($s) => htmlspecialchars($s, ENT_XML1 | ENT_QUOTES, 'UTF-8');

echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";

if ($type === 'index' || !in_array($type, ['page', 'post', 'category'], true)) {
    echo '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
    foreach (['page', 'post', 'category'] as $t) {
        echo "  <sitemap><loc>{$o}/{$t}-sitemap.xml</loc><lastmod>" . SITE_UPDATED . "</lastmod></sitemap>\n";
    }
    echo '</sitemapindex>';
    exit;
}

echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">' . "\n";
$url = function (string $path, string $mod, ?string $img = null) use ($o, $x) {
    echo "  <url><loc>{$x($o . $path)}</loc><lastmod>{$mod}</lastmod>";
    if ($img) echo "<image:image><image:loc>{$x($o . $img)}</image:loc></image:image>";
    echo "</url>\n";
};

if ($type === 'page') {
    foreach (CORE_PAGES as $path => $p) {
        if ($path === '/blog/') continue;
        $url($path, SITE_UPDATED, $path === '/' ? BIZ['logo'] : null);
    }
    foreach (SERVICES as $slug => $s) $url("/services/{$slug}/", SITE_UPDATED);
    foreach (AREAS as $slug => $a) $url("/service-areas/{$slug}/", SITE_UPDATED);
    foreach (TOOLS as $slug => $t) $url("/roofing-tools/{$slug}/", SITE_UPDATED);
} elseif ($type === 'post') {
    $url('/blog/', SITE_UPDATED);
    $posts = POSTS;
    uasort($posts, fn($a, $b) => strcmp($b['date'], $a['date']));
    foreach ($posts as $slug => $p) $url("/blog/{$slug}/", $p['modified'], $p['img']);
} else {
    $url('/category/general/', SITE_UPDATED);
}
echo '</urlset>';
