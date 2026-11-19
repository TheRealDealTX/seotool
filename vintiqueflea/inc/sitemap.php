<?php
defined('INC') || exit;
/** Dynamic XML sitemap. */
header('Content-Type: application/xml; charset=UTF-8');
$today = date('Y-m-d');
$urls = [['/', '1.0'], ['/events/', '0.9'], ['/shop/', '0.9'], ['/play/', '0.8'], ['/guides/', '0.8'], ['/food-trucks/', '0.7'], ['/vendors/', '0.7'], ['/about/', '0.6'], ['/contact/', '0.5'], ['/affiliate-disclosure/', '0.2'], ['/privacy-policy/', '0.2']];
foreach (SHOP as $s => $_) $urls[] = ["/shop/$s/", '0.8'];
foreach (EDITIONS as $s => $_) $urls[] = ["/events/$s/", '0.7'];
foreach (GAMES as $s => $_) $urls[] = ["/play/$s/", '0.7'];
$guides = load_guides();
foreach ($guides as $s => $_) $urls[] = ["/guides/$s/", '0.7'];
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
foreach ($urls as [$u, $p]) {
    $lm = str_starts_with($u, '/guides/') && isset($guides[trim(substr($u, 8), '/')]) ? $guides[trim(substr($u, 8), '/')]['updated'] : $today;
    echo '  <url><loc>' . e(abs_url($u)) . '</loc><lastmod>' . $lm . '</lastmod><priority>' . $p . "</priority></url>\n";
}
echo "</urlset>\n";
