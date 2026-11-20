<?php defined('APP') || exit;

/**
 * URLs from the previous WordPress install of thesublet.com (crawled 2026-11-20).
 * Relevant ones are 301'd to their closest new page; the rest return 410 Gone.
 */
function legacy_route(string $path): void
{
    $map = [
        '/post-a-sublet' => '/post-a-sublet/',
        '/corporaterentals/' => '/sublets/tx/houston/',
        '/corporaterentals' => '/sublets/tx/houston/',
        // old sample "sublet" posts → the matching city / filter pages
        '/sublets/sunny-1br-in-brooklyn-heights/' => '/sublets/ny/new-york/',
        '/sublets/cozy-studio-near-university/' => '/sublets/',
        '/sublets/spacious-2br-in-capitol-hill/' => '/sublets/wa/seattle/',
        '/sublets/modern-condo-downtown-chicago/' => '/sublets/il/chicago/',
        '/sublets/private-room-in-shared-house/' => '/sublets/',
        '/sublets/charming-3br-townhouse-in-austin/' => '/sublets/tx/austin/',
        '/wp-sitemap.xml' => '/sitemap.xml',
        '/sitemap_index.xml' => '/sitemap.xml',
        '/feed/' => '/blog/',
    ];
    if (isset($map[$path])) redirect($map[$path], 301);
    if (preg_match('#^/sublets/[a-z0-9-]{3,}/?$#', $path)) redirect('/sublets/', 301);

    $goneRe = [
        '#^/hello-world/?$#', '#^/sample-page/?$#', '#^/category/#', '#^/author/#', '#^/tag/#',
        '#^/comments/feed/?$#', '#^/feed/.+#', '#^/wp-#', '#^/xmlrpc\.php#', '#^/wp-sitemap#', '#^/\?p=#',
        '#^/sublet/?$#', '#^/sublet_category/#', '#^/[0-9]{4}/[0-9]{2}/#',
    ];
    foreach ($goneRe as $re) if (preg_match($re, $path)) gone();
}
