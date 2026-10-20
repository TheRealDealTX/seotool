<?php
// Yoast-compatible sitemap set, so the URLs submitted to Search Console keep working.
/** @var string $path */
header('Content-Type: application/xml; charset=utf-8');
echo '<?xml version="1.0" encoding="UTF-8"?>', "\n";
$posts = live_posts();
$latest = max(array_column($posts, 'modified'));
if ($path === '/sitemap_index.xml' || $path === '/sitemap.xml') {
    echo '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">', "\n";
    foreach (['post', 'page', 'category'] as $s) {
        echo '<sitemap><loc>', SITE_ORIGIN, '/', $s, '-sitemap.xml</loc><lastmod>', $latest, '</lastmod></sitemap>', "\n";
    }
    echo '</sitemapindex>';
    exit;
}
echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">', "\n";
$url = function (string $path, string $lastmod = '', string $image = '') {
    echo '<url><loc>', e(canonical($path)), '</loc>', $lastmod ? '<lastmod>' . $lastmod . '</lastmod>' : '';
    echo $image ? '<image:image><image:loc>' . e(canonical($image)) . '</image:loc></image:image>' : '', '</url>', "\n";
};
if ($path === '/post-sitemap.xml') {
    foreach ($posts as $p) $url(post_url($p['slug']), $p['modified'], $p['image']);
} elseif ($path === '/page-sitemap.xml') {
    foreach (['/', '/blog/', '/tools/', '/about-us/', '/contact-us/', '/editorial-policy/', '/privacy-policy/', '/terms-of-use/'] as $p) $url($p, $latest);
    foreach (array_keys(tools()) as $t) $url('/tools/' . $t . '/', $latest);
} else {
    foreach (array_keys(TOPICS) as $t) $url('/topics/' . $t . '/', $latest);
    foreach (array_keys(CATEGORIES) as $c) $url('/category/' . $c . '/', $latest);
}
echo '</urlset>';
