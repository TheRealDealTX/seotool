<?php
/*
 * newhomestudent2019.com — front controller.
 * The Hostinger php-fpm website serves real files directly, ignores .htaccess and
 * sends every other request here, so all routing (and every redirect) lives in this file.
 */
declare(strict_types=1);
const NHS = true;
define('APP_ROOT', __DIR__);
date_default_timezone_set('America/Chicago');

require APP_ROOT . '/inc/config.php';
require APP_ROOT . '/inc/functions.php';
require APP_ROOT . '/inc/products.php';
require APP_ROOT . '/inc/mailer.php';
require APP_ROOT . '/inc/layout.php';
require APP_ROOT . '/inc/views.php';
require APP_ROOT . '/inc/views-special.php';

$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?') ?: '/');
$qs   = (string) parse_url($uri, PHP_URL_QUERY);

// Canonical scheme + host. TLS terminates upstream, so trust X-Forwarded-Proto.
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$canonHost = parse_url(SITE['origin'], PHP_URL_HOST);
if (PHP_SAPI !== 'cli-server' && (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http' || $host === 'www.' . $canonHost)) {
    $base = ($host === $canonHost || $host === 'www.' . $canonHost) ? SITE['origin'] : 'https://' . $host;
    header('Location: ' . $base . $uri, true, 301);
    exit;
}
// Keep preview/staging hostnames out of search results.
if ($host !== $canonHost) header('X-Robots-Tag: noindex, nofollow');

// WordPress query-string permalinks (?p=123, ?page_id=5) and search -> blog.
if ($path === '/' && preg_match('/(^|&)(p|page_id|s|cat|m)=/', $qs)) redirect('/blog/');

// Legacy one-to-one redirects.
if (isset(LEGACY_REDIRECTS[$path])) redirect(LEGACY_REDIRECTS[$path]);

// Old WordPress plumbing.
if (preg_match('#^/(wp-admin|wp-includes|wp-json|wp-login\.php|xmlrpc\.php|wp-cron\.php)(/|$)#', $path)) redirect('/');
if (preg_match('#^/(?:[a-z0-9-]+/)?feed/?$#', $path) && $path !== '/feed/') redirect('/feed/');
if (preg_match('#^/wp-sitemap-.*\.xml$#', $path)) redirect('/sitemap.xml');

// Old media library URLs -> the new optimized featured image (or the post itself for HTML requests).
if (str_starts_with($path, '/wp-content/uploads/')) {
    $key = preg_replace('/(-\d+x\d+|-scaled)?\.(jpe?g|png|webp|gif)$/i', '', $path);
    $map = require APP_ROOT . '/data/legacy-images.php';
    if (isset($map[$key])) redirect('/assets/img/posts/' . $map[$key] . '.webp');
    view_404();
}

// Every page URL ends with a slash (except files).
if ($path !== '/' && !str_ends_with($path, '/') && !preg_match('/\.[a-z0-9]+$/i', $path)) redirect($path . '/' . ($qs !== '' ? '?' . $qs : ''));

// Pagination helper: /foo/page/2/
$page = 1;
if (preg_match('#^(.*/)page/(\d+)/$#', $path, $m)) {
    $page = (int) $m[2];
    if ($page === 1) redirect($m[1]);
    $path = $m[1];
}

switch (true) {
    case $path === '/' && $page === 1:
        view_home();
    case $path === '/' && $page > 1:
        redirect('/blog/page/' . $page . '/');
    case $path === '/blog/':
        view_blog($page);
    case $path === '/sitemap.xml':
        view_sitemap();
    case $path === '/feed/':
        view_feed();
    case $path === '/site.webmanifest':
        // Served from PHP so it gets the right MIME type (the host sends .webmanifest files as octet-stream).
        header('Content-Type: application/manifest+json; charset=utf-8');
        header('Cache-Control: public, max-age=86400');
        readfile(APP_ROOT . '/data/site.webmanifest.json');
        exit;
    case $path === '/free-training/':
        view_free_training();
    case $path === '/our-products/':
        view_products_hub();
    case $path === '/author/jonathon/':
        view_author($page);
    case (bool) preg_match('#^/author/[^/]+/$#', $path):
        redirect('/author/jonathon/');
    case (bool) preg_match('#^/category/([a-z0-9-]+)/$#', $path, $m):
        if (isset(CATEGORIES[$m[1]])) view_category($m[1], $page);
        view_404();
    case (bool) preg_match('#^/tag/[^/]+/$#', $path):
        redirect('/blog/');
}

// Single-segment slugs: content pages first, then posts.
if ($page === 1 && preg_match('#^/([a-z0-9-]+)/$#', $path, $m)) {
    if ($pg = get_page($m[1])) view_page($m[1], $pg);
    if ($post = get_post($m[1])) view_post($post);
    // WordPress date permalinks or stray prefixes: /2023/08/slug/
}
if (preg_match('#^/(?:\d{4}/\d{2}/(?:\d{2}/)?)([a-z0-9-]+)/$#', $path, $m) && get_post($m[1])) redirect('/' . $m[1] . '/');

view_404();
