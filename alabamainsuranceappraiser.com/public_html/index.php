<?php
// alabamainsuranceappraiser.com front controller.
// The host serves existing files directly and sends "/" and every unknown
// path here (it ignores .htaccess). So this file: serves the homepage,
// enforces https + apex host, 301s legacy WordPress URLs, adds missing
// trailing slashes, and returns a real 404 for everything else.

$home  = 'https://alabamainsuranceappraiser.com';
$uri   = $_SERVER['REQUEST_URI'] ?? '/';
$path  = rawurldecode(strtok($uri, '?'));
$query = $_GET;

function go($to, $code = 301) {
    header('Location: ' . $to, true, $code);
    header('Cache-Control: public, max-age=3600');
    exit;
}

// 1. Canonical scheme + host (TLS terminates upstream, so trust X-Forwarded-Proto).
$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
if ($insecure || $host === 'www.alabamainsuranceappraiser.com') {
    go($home . $uri);
}

// 2. Legacy WordPress query URLs (?p=83, ?page_id=, ?s=, ?cat=).
if ($path === '/' || $path === '/index.php') {
    if (isset($query['p']) && (int)$query['p'] === 83) go($home . '/what-does-an-insurance-appraiser-do/');
    if (isset($query['page_id'])) {
        // IDs from the WordPress REST export (backup/wordpress-2026-11-05/api/pages.json).
        $pages = [3 => '/privacy-policy/', 10 => '/', 13 => '/about-us/', 15 => '/services/', 17 => '/contact/', 28 => '/blog/', 48 => '/terms-of-use/'];
        go($home . ($pages[(int)$query['page_id']] ?? '/'));
    }
    if (isset($query['p']) || isset($query['s']) || isset($query['cat'])) go($home . '/blog/');
    header('Content-Type: text/html; charset=utf-8');
    header('Cache-Control: public, max-age=600');
    readfile(__DIR__ . '/home.html');
    exit;
}

// 3. Legacy WordPress paths -> nearest new page.
$map = [
    '#^/(sitemap_index|page-sitemap|post-sitemap|category-sitemap|wp-sitemap|sitemap-index)\.xml$#' => '/sitemap.xml',
    '#^/main-sitemap\.xsl$#'                       => '/sitemap.xml',
    '#^/(feed|comments/feed|rss|atom)/?$#'         => '/blog/',
    '#^/blog/(feed|page/\d+)/?$#'                  => '/blog/',
    '#^/category/general/(feed|page/\d+)/?$#'      => '/category/general/',
    '#^/category/[^/]+/?$#'                        => '/category/general/',
    '#^/(tag|author)/.*$#'                         => '/blog/',
    '#^/20\d\d(/\d\d){0,2}/?$#'                    => '/blog/',
    '#^/what-does-an-insurance-appraiser-do/(feed|amp|embed)/?$#' => '/what-does-an-insurance-appraiser-do/',
    '#^/(home|homepage)/?$#'                       => '/',
    '#^/about/?$#'                                 => '/about-us/',
    '#^/contact-us/?$#'                            => '/contact/',
    '#^/service/?$#'                               => '/services/',
    '#^/(privacy|privacy-policy-2)/?$#'            => '/privacy-policy/',
    '#^/(terms|terms-and-conditions|terms-of-service)/?$#' => '/terms-of-use/',
    '#^/(tools|calculators?)/?$#'                  => '/tools/',
    '#^/(wp-admin|wp-includes|wp-json|wp-login\.php|xmlrpc\.php|wp-signup\.php|wp-cron\.php)(/.*)?$#' => '/',
];
foreach ($map as $re => $to) {
    if (preg_match($re, $path)) go($home . $to);
}

// 4. Old pages for /<slug>/feed/ or /<slug>/amp/ on any existing page.
if (preg_match('#^(/.+?)/(feed|amp|embed)/?$#', $path, $m) && is_file(__DIR__ . $m[1] . '/index.html')) {
    go($home . $m[1] . '/');
}

// 5. Directory without trailing slash, or index.html / .php variants.
$clean = rtrim($path, '/');
if (preg_match('#^(.*)/index\.(html|php)$#', $path, $m) && $m[1] !== '' && is_file(__DIR__ . $m[1] . '/index.html')) {
    go($home . $m[1] . '/');
}
if ($clean !== '' && substr($path, -1) !== '/' && is_file(__DIR__ . $clean . '/index.html')) {
    go($home . $clean . '/' . (isset($_SERVER['QUERY_STRING']) && $_SERVER['QUERY_STRING'] !== '' ? '?' . $_SERVER['QUERY_STRING'] : ''));
}
// Paths with different case (e.g. /About-Us/).
$lower = strtolower($path);
if ($lower !== $path && is_file(__DIR__ . rtrim($lower, '/') . '/index.html')) {
    go($home . rtrim($lower, '/') . '/');
}

// 6. Everything else: real 404.
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
header('Cache-Control: no-cache');
readfile(__DIR__ . '/404.html');
