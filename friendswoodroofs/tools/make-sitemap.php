<?php
// Writes public_html/sitemap.xml from the app's route list (same output as the
// dynamic /sitemap.xml). Re-run after adding pages or changing launch_date:
//   php tools/make-sitemap.php
define('FR_PUBLIC', dirname(__DIR__) . '/public_html');
define('FR_APP', dirname(__DIR__) . '/app');
$GLOBALS['FR_CONFIG'] = require FR_APP . '/config/site.php';
date_default_timezone_set((string) $GLOBALS['FR_CONFIG']['timezone']);
foreach (['helpers', 'content', 'seo', 'security', 'mailer', 'estimate', 'router'] as $f) {
    require FR_APP . "/src/$f.php";
}
$xml = '<?xml version="1.0" encoding="UTF-8"?>' . "\n"
     . '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
foreach (sitemap_entries() as $path => $lastmod) {
    $xml .= '  <url><loc>' . e(abs_url($path)) . '</loc><lastmod>' . e($lastmod) . "</lastmod></url>\n";
}
$xml .= "</urlset>\n";
file_put_contents(FR_PUBLIC . '/sitemap.xml', $xml);
echo 'Wrote public_html/sitemap.xml (' . substr_count($xml, '<url>') . " URLs)\n";
