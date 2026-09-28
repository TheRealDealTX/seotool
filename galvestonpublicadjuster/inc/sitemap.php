<?php
// Dynamic sitemap: static routes plus every published blog post.
header('Content-Type: application/xml; charset=utf-8');
$urls = [];
foreach (ROUTES as $p => $page) {
    if (in_array($page, ['thank-you'], true)) continue;
    $urls[] = [$p, date('Y-m-d', filemtime(ROOT . '/pages/' . $page . '.php'))];
}
foreach (blog_posts() as $post) $urls[] = ['/blog/' . $post['slug'] . '/', $post['date']];
echo '<?xml version="1.0" encoding="UTF-8"?>', "\n", '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">', "\n";
foreach ($urls as [$p, $d]) echo '  <url><loc>', SITE_URL, e($p), '</loc><lastmod>', e($d), "</lastmod></url>\n";
echo "</urlset>\n";
