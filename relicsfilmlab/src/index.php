<?php
// Relics Film Lab — front controller. Serves pages from _p/ at their exact
// (old Shopify) URLs, 301s retired URLs, and returns a real 404 otherwise.
// The host ignores .htaccess and routes every unknown path here.
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?'));
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$canon = 'relicsfilmlab.com';
$https = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? 'https') !== 'http';
$base = ($host === $canon || $host === 'www.' . $canon) ? 'https://' . $canon : (($https ? 'https://' : 'http://') . $host);

function go($to) { global $base; header('Location: ' . (str_starts_with($to, 'http') ? $to : $base . $to), true, 301); header('Cache-Control: public, max-age=86400'); exit; }

// canonical host + scheme on the live domain
if ($host === 'www.' . $canon || ($host === $canon && !$https)) { go($path); }
// keep the temporary preview domain out of search engines
if (str_contains($host, 'hostingersite.com')) { header('X-Robots-Tag: noindex, nofollow'); }

// trailing slash / case normalisation
if ($path !== '/' && str_ends_with($path, '/')) { go(rtrim($path, '/')); }
if ($path === '/index.php' || $path === '/home') { go('/'); }
if ($path !== strtolower($path) && is_file(__DIR__ . '/_p' . strtolower($path) . '.html')) { go(strtolower($path)); }

$file = $path === '/' ? 'home' : substr($path, 1);
if (preg_match('#^[a-z0-9][a-z0-9/_\-.]*$#', $file) && !str_contains($file, '..') && is_file(__DIR__ . "/_p/$file.html")) {
    header('Content-Type: text/html; charset=utf-8');
    header('Cache-Control: public, max-age=600');
    readfile(__DIR__ . "/_p/$file.html");
    exit;
}

// Old Shopify market prefixes: /en-ca/..., /en-us/..., /fr-ca/... -> same path without the prefix
if (preg_match('#^/(?:[a-z]{2}-[a-z]{2})(/.*)?$#', $path, $m)) { go(($m[1] ?? '') === '' ? '/' : $m[1]); }
// Old Shopify CDN media that no longer exists -> a real image (keeps image links from 404ing)
if (preg_match('#^/cdn/shop/.+\.(jpe?g|png|webp|gif)$#i', $path) && !is_file(__DIR__ . $path)) { go('/assets/img/site/hero.webp'); }
$R = require __DIR__ . '/_redirects.php';
if (isset($R[$path])) { go($R[$path]); }
// Shopify nested product URLs: /collections/<c>/products/<p>
if (preg_match('#^/collections/[^/]+/products/([^/]+)$#', $path, $m)) {
    $t = '/products/' . strtolower($m[1]);
    if (isset($R[$t])) { go($R[$t]); }
    if (is_file(__DIR__ . '/_p' . $t . '.html')) { go($t); }
}
// Shopify collection filters/tags: /collections/<c>/<tag>
if (preg_match('#^/collections/([a-z0-9\-]+)/[^/]+$#', $path, $m) && is_file(__DIR__ . '/_p/collections/' . $m[1] . '.html')) { go('/collections/' . $m[1]); }
// Shopify blog tags / old article variants
if (preg_match('#^/blogs/guides/tagged/#', $path)) { go('/blogs/guides'); }
// Shopify product .json/.js/.oembed endpoints
if (preg_match('#^(/products/[a-z0-9\-]+)\.(json|js|oembed|xml)$#', $path, $m) && is_file(__DIR__ . '/_p' . $m[1] . '.html')) { go($m[1]); }
if ($path === '/sitemap_index.xml' || preg_match('#^/sitemap_[a-z_0-9]+\.xml$#', $path)) { go('/sitemap.xml'); }

http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
