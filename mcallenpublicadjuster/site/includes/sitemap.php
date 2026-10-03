<?php
/**
 * XML sitemap and RSS feed, generated from the content files so they never go stale.
 */

declare(strict_types=1);

function sitemap_items(): array
{
    $items = [];
    foreach (['pages', 'services', 'posts'] as $type) {
        foreach (all_content($type) as $c) {
            if (!empty($c['noindex'])) {
                continue;
            }
            $file = MPA_ROOT . '/content/' . $type . '/' . $c['_name'] . '.php';
            $lastmod = $c['updated'] ?? $c['date'] ?? date('Y-m-d', (int) filemtime($file));
            // Live-data pages change constantly.
            if (in_array($c['template'] ?? '', ['weather', 'weather-events'], true)) {
                $lastmod = date('Y-m-d');
            }
            $items[] = ['loc' => url($c['path']), 'lastmod' => $lastmod, 'image' => $c['image'] ?? null, 'title' => $c['title']];
        }
    }
    usort($items, fn($a, $b) => strcmp($a['loc'], $b['loc']));
    return $items;
}

function output_sitemap(): void
{
    header('Content-Type: application/xml; charset=utf-8');
    header('X-Robots-Tag: noindex, follow');
    echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
    echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">' . "\n";
    foreach (sitemap_items() as $it) {
        echo "  <url>\n    <loc>" . e($it['loc']) . "</loc>\n    <lastmod>" . e(date('Y-m-d', strtotime($it['lastmod']))) . "</lastmod>\n";
        if ($it['image']) {
            echo '    <image:image><image:loc>' . e(url($it['image'])) . "</image:loc></image:image>\n";
        }
        echo "  </url>\n";
    }
    echo "</urlset>\n";
}

function output_feed(): void
{
    header('Content-Type: application/rss+xml; charset=utf-8');
    $posts = array_slice(all_content('posts'), 0, 20);
    echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
    echo '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/">' . "\n<channel>\n";
    echo '<title>' . e(cfg('site_name')) . "</title>\n";
    echo '<atom:link href="' . e(url('/feed/')) . '" rel="self" type="application/rss+xml"/>' . "\n";
    echo '<link>' . e(url('/')) . "</link>\n";
    echo "<description>Property insurance claim guidance for McAllen and the Rio Grande Valley.</description>\n<language>en-US</language>\n";
    if ($posts) {
        echo '<lastBuildDate>' . date(DATE_RSS, strtotime($posts[0]['updated'] ?? $posts[0]['date'])) . "</lastBuildDate>\n";
    }
    foreach ($posts as $p) {
        echo "<item>\n<title>" . e($p['title']) . "</title>\n<link>" . e(url($p['path'])) . "</link>\n<guid isPermaLink=\"true\">" . e(url($p['path'])) . "</guid>\n";
        echo '<pubDate>' . date(DATE_RSS, strtotime($p['date'])) . "</pubDate>\n<dc:creator>Joseph Dittman</dc:creator>\n";
        echo '<category>' . e($p['category'] ?? 'Insurance Claims') . "</category>\n";
        echo '<description>' . e($p['excerpt'] ?? $p['description'] ?? '') . "</description>\n</item>\n";
    }
    echo "</channel>\n</rss>\n";
}
