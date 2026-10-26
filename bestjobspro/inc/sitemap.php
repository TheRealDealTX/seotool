<?php
// /sitemap.xml - every indexable URL. The old Yoast sitemap URLs 301 here.
header('Content-Type: application/xml; charset=utf-8');
$lastmod = '2026-10-26';
$urls = [];
foreach (PAGES as $p => $file) {
    if ($p !== '/category/job-articles/') {
        $urls[$p] = $lastmod;
    }
}
foreach (TOOLS as $slug => $t) {
    $urls['/career-tools/' . $slug . '/'] = $lastmod;
}
foreach (all_posts() as $post) {
    $urls[$post['path']] = $post['updated'];
}
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
foreach ($urls as $p => $d) {
    echo '  <url><loc>' . e(url($p)) . '</loc><lastmod>' . $d . '</lastmod></url>' . "\n";
}
echo '</urlset>' . "\n";
