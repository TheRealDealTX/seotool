<?php
// RSS feed, XML sitemaps (WordPress-compatible URLs) and robots.txt.
defined('LLT') or die(http_response_code(404));

function xml_header(): void {
    header('Content-Type: application/xml; charset=utf-8');
    header('X-Robots-Tag: noindex, follow');
    echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
}

function render_rss(): void {
    header('Content-Type: application/rss+xml; charset=utf-8');
    echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
    echo '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>';
    echo '<title>' . e(SITE_NAME) . '</title><link>' . SITE_ORIGIN . '/</link>';
    echo '<atom:link href="' . SITE_ORIGIN . '/feed/" rel="self" type="application/rss+xml"/>';
    echo '<description>Landscape lighting guides and ideas for Texas homes</description><language>en-US</language>';
    foreach (posts() as $p) {
        echo '<item><title>' . e($p['h1']) . '</title><link>' . abs_url($p['path']) . '</link><guid>' . abs_url($p['path']) . '</guid>'
           . '<pubDate>' . date(DATE_RSS, strtotime($p['date'] . ' 12:00:00 UTC')) . '</pubDate><category>General</category>'
           . '<description>' . e($p['description']) . '</description></item>';
    }
    echo '</channel></rss>';
}

function sitemap_groups(): array {
    global $PAGES;
    $pages = array_filter($PAGES, fn($p) => $p['type'] !== 'post' && $p['path'] !== '/category/general/');
    return ['page' => $pages, 'post' => posts(), 'category' => ['/category/general/' => $PAGES['/category/general/']]];
}

function render_sitemap_index(): void {
    xml_header();
    echo '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">';
    foreach (sitemap_groups() as $kind => $items) {
        $last = max(array_map(fn($p) => $p['modified'], $items));
        echo '<sitemap><loc>' . SITE_ORIGIN . '/' . $kind . '-sitemap.xml</loc><lastmod>' . $last . '</lastmod></sitemap>';
    }
    echo '</sitemapindex>';
}

function render_sitemap(string $kind): void {
    $items = sitemap_groups()[$kind] ?? [];
    xml_header();
    echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">';
    foreach ($items as $path => $p) {
        echo '<url><loc>' . abs_url($path) . '</loc><lastmod>' . $p['modified'] . '</lastmod>';
        if ($p['image']) echo '<image:image><image:loc>' . abs_url(img_url($p['image'])) . '</image:loc></image:image>';
        echo '</url>';
    }
    echo '</urlset>';
}

function render_robots(): void {
    header('Content-Type: text/plain; charset=utf-8');
    echo "User-agent: *\nDisallow: /inc/\nDisallow: /pages/\nDisallow: /posts/\nDisallow: /storage/\nDisallow: /tests/\nAllow: /\n\nSitemap: " . SITE_ORIGIN . "/sitemap_index.xml\n";
}
