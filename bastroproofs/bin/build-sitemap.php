<?php
/**
 * Regenerate /sitemap.xml from the content data. Run after adding pages:
 *   php bin/build-sitemap.php
 */
require dirname(__DIR__) . '/includes/bootstrap.php';
$today = date('Y-m-d');
$urls = [['/', '1.0'], ['/services/', '0.9'], ['/service-areas/', '0.8'], ['/roofing-tools/', '0.8'], ['/blog/', '0.7'],
         ['/about/', '0.6'], ['/contact/', '0.7'], ['/faq/', '0.6']];
foreach ($SERVICES as $k => $_) $urls[] = ["/services/$k/", $k === 'metal-roofing-bastrop-tx' ? '0.9' : '0.8'];
foreach ($AREAS as $k => $_)    $urls[] = ["/service-areas/$k/", '0.7'];
foreach ($TOOLS as $k => $_)    $urls[] = ["/roofing-tools/$k/", '0.7'];
foreach ($POSTS as $k => $p)    $urls[] = ["/blog/$k/", '0.6', $p['date']];
foreach (['/privacy-policy/', '/terms-of-use/', '/sitemap/'] as $u) $urls[] = [$u, '0.2'];

$xml = '<?xml version="1.0" encoding="UTF-8"?>' . "\n" . '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
foreach ($urls as $u) {
    $xml .= '  <url><loc>' . abs_url($u[0]) . '</loc><lastmod>' . ($u[2] ?? $today) . '</lastmod><priority>' . $u[1] . "</priority></url>\n";
}
$xml .= "</urlset>\n";
file_put_contents(ROOT . '/sitemap.xml', $xml);
echo count($urls) . " URLs written to sitemap.xml\n";
