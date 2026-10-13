<?php
// Regenerates /sitemap.xml and /sitemap_index.xml. Run from the site root after adding pages or posts:
//   php inc/build-sitemap.php
if (PHP_SAPI !== 'cli') { http_response_code(404); exit; }
require __DIR__ . '/config.php';
require __DIR__ . '/posts.php';
require __DIR__ . '/tools.php';

$root = dirname(__DIR__);
$pages = ['/' => '1.0', '/about-us/' => '0.8', '/services/' => '0.9', '/contact/' => '0.8', '/blog/' => '0.7',
    '/tools/' => '0.8', '/houston-weather/' => '0.8', '/houston-storm-history/' => '0.7', '/service-areas/' => '0.8',
    '/faq/' => '0.7', '/hurricane-preparedness-checklist/' => '0.6', '/insurance-claim-glossary/' => '0.6',
    AUTHOR['url'] => '0.6', '/category/general/' => '0.4', '/privacy-policy/' => '0.2', '/terms-of-use/' => '0.2'];
foreach (array_keys(TOOLS) as $t) $pages['/tools/' . $t . '/'] = '0.7';

$xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">'];
foreach ($pages as $path => $prio) {
    $file = $root . $path . 'index.php';
    $mod = is_file($file) ? date('c', filemtime($file)) : date('c');
    $xml[] = "  <url><loc>" . SITE_URL . $path . "</loc><lastmod>$mod</lastmod><priority>$prio</priority></url>";
}
foreach (POSTS as $slug => $p) {
    $xml[] = "  <url><loc>" . SITE_URL . "/$slug/</loc><lastmod>" . date('c', strtotime($p['modified'])) . "</lastmod><priority>0.7</priority>"
        . "<image:image><image:loc>" . SITE_URL . htmlspecialchars($p['image']) . "</image:loc></image:image></url>";
}
$xml[] = '</urlset>';
file_put_contents($root . '/sitemap.xml', implode("\n", $xml) . "\n");
file_put_contents($root . '/sitemap_index.xml', '<?xml version="1.0" encoding="UTF-8"?>' . "\n"
    . '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n"
    . '  <sitemap><loc>' . SITE_URL . '/sitemap.xml</loc><lastmod>' . date('c') . '</lastmod></sitemap>' . "\n</sitemapindex>\n");
echo count($pages) + count(POSTS), " URLs written to sitemap.xml\n";
