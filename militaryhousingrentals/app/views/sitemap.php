<?php
header('Content-Type: application/xml; charset=UTF-8');
header('X-Robots-Tag: noindex, follow');
$maps = ['post', 'page', 'properties', 'bases'];
$lastmod = function ($items, $key = 'date') { $d = array_map(fn($i) => $i['modified'] ?? $i[$key] ?? '', $items); rsort($d); return $d[0] ?? date('Y-m-d'); };
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
if ($sitemap === 'index') {
    echo '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
    $mods = ['post' => $lastmod(posts()), 'page' => $lastmod(posts()), 'properties' => $lastmod(listings()), 'bases' => $lastmod(listings())];
    foreach ($maps as $m) echo "<sitemap><loc>" . e(abs_url("/$m-sitemap.xml")) . "</loc><lastmod>{$mods[$m]}</lastmod></sitemap>\n";
    echo '</sitemapindex>';
    exit;
}
$urls = [];
switch ($sitemap) {
    case 'post':
        $urls[] = ['/blog/', $lastmod(posts())];
        foreach (posts() as $p) $urls[] = ['/' . $p['slug'] . '/', $p['modified'], $p['image']['src'] ?? null];
        break;
    case 'page':
        $urls[] = ['/', $lastmod(listings())];
        foreach (['/properties/', '/marine-bases/', '/contact-us/', '/submit-property/', '/privacy-policy/', '/terms-of-use/'] as $u) $urls[] = [$u, $lastmod(listings())];
        break;
    case 'properties':
        foreach (listings() as $l) $urls[] = ['/properties/' . $l['slug'] . '/', $l['modified'] ?? $l['date'], listing_image($l)['src']];
        break;
    case 'bases':
        $urls[] = ['/bases/featured/', $lastmod(listings())];
        foreach (bases() as $b) $urls[] = ['/bases/' . $b['slug'] . '/', $lastmod(listings_for_base($b['slug']) ?: listings())];
        break;
    case 'category':
        $urls[] = ['/blog/', $lastmod(posts())];
        break;
}
echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">' . "\n";
foreach ($urls as $u) {
    echo '<url><loc>' . e(abs_url($u[0])) . '</loc><lastmod>' . e(substr($u[1], 0, 10)) . '</lastmod>';
    if (!empty($u[2])) echo '<image:image><image:loc>' . e(abs_url($u[2])) . '</image:loc></image:image>';
    echo "</url>\n";
}
echo '</urlset>';
