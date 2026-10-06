<?php
defined('SLT') || exit;

function xml_head(): void {
    header('Content-Type: application/xml; charset=utf-8');
    header('X-Robots-Tag: noindex, follow');
    echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
}

function latest_post_date(): string {
    $d = '2026-07-21';
    foreach (POSTS as $p) $d = max($d, $p['updated'] ?? $p['date']);
    return $d;
}

function sitemap_index(): void {
    xml_head();
    $lm = latest_post_date();
    echo '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
    foreach (['page', 'post', 'category'] as $s) {
        echo "  <sitemap><loc>" . SITE_URL . "/$s-sitemap.xml</loc><lastmod>{$lm}T08:00:00-05:00</lastmod></sitemap>\n";
    }
    echo '</sitemapindex>';
}

function url_entry(string $path, string $lastmod, ?string $img = null): void {
    echo '  <url><loc>' . e(abs_url($path)) . '</loc><lastmod>' . $lastmod . '</lastmod>';
    if ($img) echo '<image:image><image:loc>' . e(abs_url('/assets/img/' . $img)) . '</image:loc></image:image>';
    echo "</url>\n";
}

function sitemap_pages(): void {
    xml_head();
    $d = '2026-10-06';
    echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">' . "\n";
    foreach (PAGES as $path => $p) { if (!empty($p[3]['noindex'])) continue; url_entry($path, $d, $path === '/' ? 'Spring-Landscape-Lighting-BG-1.webp' : null); }
    foreach (SERVICES as $k => $s) url_entry("/services/$k/", $d);
    foreach (AREAS as $k => $a) url_entry("/service-areas/$k/", $d);
    foreach (TOOLS as $k => $t) url_entry("/tools/$k/", $d);
    echo '</urlset>';
}

function sitemap_posts(): void {
    xml_head();
    echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">' . "\n";
    url_entry('/blog/', latest_post_date());
    foreach (POSTS as $k => $p) url_entry("/$k/", $p['updated'] ?? $p['date'], $p['img']);
    echo '</urlset>';
}

function sitemap_categories(): void {
    xml_head();
    echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
    foreach (CATEGORIES as $k => $c) {
        $d = '2026-07-21';
        foreach (POSTS as $p) if ($p['cat'] === $k) $d = max($d, $p['updated'] ?? $p['date']);
        url_entry("/category/$k/", $d);
    }
    echo '</urlset>';
}

function rss_feed(): void {
    header('Content-Type: application/rss+xml; charset=utf-8');
    echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
    echo '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>';
    echo '<title>' . e(BRAND) . '</title><link>' . SITE_URL . '/blog/</link><description>Landscape lighting ideas and guides for Spring, TX homes.</description><language>en-US</language>';
    echo '<atom:link href="' . SITE_URL . '/feed/" rel="self" type="application/rss+xml"/>';
    $posts = POSTS; uasort($posts, fn($a, $b) => strcmp($b['date'], $a['date']));
    foreach ($posts as $k => $p) {
        echo '<item><title>' . e($p['title']) . '</title><link>' . SITE_URL . "/$k/</link><guid>" . SITE_URL . "/$k/</guid>";
        echo '<pubDate>' . date(DATE_RSS, strtotime($p['date'] . ' 08:00:00 -0500')) . '</pubDate><description>' . e($p['excerpt']) . '</description></item>';
    }
    echo '</channel></rss>';
}
