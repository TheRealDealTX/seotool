<?php
// XML sitemaps: an index plus one sitemap per version and book.

const SITEMAP_LASTMOD = '2026-10-13';

function xml_out(string $body): void {
    header('Content-Type: application/xml; charset=utf-8');
    header('Cache-Control: public, max-age=86400');
    echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n" . $body;
}

function sitemap_index(): void {
    $x = '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">';
    $x .= '<sitemap><loc>' . SITE_URL . '/sitemap-pages.xml</loc><lastmod>' . SITEMAP_LASTMOD . '</lastmod></sitemap>';
    foreach (versions() as $ver => $_) {
        foreach (books() as $slug => $b) {
            if ($b['available'][$ver] === 0) continue;
            $x .= '<sitemap><loc>' . SITE_URL . "/sitemap-$ver-$slug.xml</loc><lastmod>" . SITEMAP_LASTMOD . '</lastmod></sitemap>';
        }
    }
    xml_out($x . '</sitemapindex>');
}

function sitemap_urls(array $paths): void {
    $x = '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">';
    foreach ($paths as $p) $x .= '<url><loc>' . SITE_URL . e($p) . '</loc></url>';
    xml_out($x . '</urlset>');
}

/** Returns false when the name isn't one of ours. */
function sitemap(string $name): bool {
    if ($name === 'sitemap_index.xml' || $name === 'sitemap.xml') { sitemap_index(); return true; }
    if ($name === 'sitemap-pages.xml') {
        $paths = ['/', '/verse-of-the-day/', '/plan/', '/search/', '/app/', '/blog/', '/privacy-policy/'];
        foreach (versions() as $v => $_) $paths[] = "/$v/";
        foreach (blog_posts() as $p) $paths[] = '/blog/' . $p['slug'] . '/';
        sitemap_urls($paths);
        return true;
    }
    if (preg_match('/^sitemap-([a-z]+)-([a-z0-9]+)\.xml$/', $name, $m) && isset(versions()[$m[1]], books()[$m[2]])) {
        [$_, $ver, $slug] = $m;
        $paths = [url_for($ver, $slug)];
        foreach (books()[$slug]['verses'] as $i => $n) {
            $c = $i + 1;
            if (chapter_available($ver, $slug, $c) === 0) continue;
            $paths[] = url_for($ver, $slug, $c);
            foreach (chapter_text($ver, $slug, $c) as $j => $t) if ($t) $paths[] = url_for($ver, $slug, $c, $j + 1);
        }
        sitemap_urls($paths);
        return true;
    }
    return false;
}
