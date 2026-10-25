<?php
// Front controller for URLs that are not real files. Works on servers without
// .htaccess support (Hostinger Agency/H5G): restores WordPress's redirects, feeds
// and 404 behavior, and keeps non-production hosts out of search results.

$root = __DIR__;
$uri = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(parse_url($uri, PHP_URL_PATH) ?: '/');
$query = (string) parse_url($uri, PHP_URL_QUERY);
$host = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));

if ($host !== 'coveragestimate.com') {
    header('X-Robots-Tag: noindex, nofollow');
}

function ce_redirect(string $to, int $code = 301): void
{
    header('Location: ' . $to, true, $code);
    exit;
}

function ce_serve(string $file, string $type = 'text/html; charset=UTF-8', int $code = 200): void
{
    http_response_code($code);
    header('Content-Type: ' . $type);
    readfile($file);
    exit;
}

function ce_not_found(string $root): void
{
    ce_serve($root . '/404.html', 'text/html; charset=UTF-8', 404);
}

// HTTP -> HTTPS, as WordPress did (pages are served by this script, so it applies site-wide)
$isHttps = ($_SERVER['HTTPS'] ?? '') === 'on' || ($_SERVER['REQUEST_SCHEME'] ?? '') === 'https'
    || strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https';
if (!$isHttps && $host !== '' && !in_array($host, ['localhost', '127.0.0.1'], true)) {
    ce_redirect('https://' . $host . $uri);
}

// www -> apex, as WordPress did
if (strpos($host, 'www.') === 0) {
    ce_redirect('https://' . substr($host, 4) . $uri);
}

// Legacy WordPress query-string URLs on the home page
if ($path === '/' && $query !== '' && preg_match('/(^|&)(p|page_id|cat|s|author)=/', $query)) {
    require $root . '/ce-router.php';
    exit;
}

// Path traversal guard
if (strpos($path, '..') !== false) {
    ce_not_found($root);
}

// Fixed redirects WordPress/Yoast performed
if (preg_match('#^/home/?$#', $path) || preg_match('#^/author/[^/]+/?$#', $path)) {
    ce_redirect('/');
}
if (preg_match('#^/(sitemap|wp-sitemap)\.xml$#', $path)) {
    ce_redirect('/sitemap_index.xml');
}

// Retired WordPress endpoints and private files
if (preg_match('#^/(wp-login\.php|xmlrpc\.php|wp-cron\.php|wp-json(/.*)?|wp-admin(/.*)?|ce-private(/.*)?)$#', $path)) {
    ce_not_found($root);
}

// RSS feeds
$feeds = ['/feed/' => 'feed', '/comments/feed/' => 'comments-feed', '/category/tools/feed/' => 'category-tools-feed'];
$withSlash = rtrim($path, '/') . '/';
if (isset($feeds[$withSlash])) {
    if ($path !== $withSlash) {
        ce_redirect($withSlash . ($query !== '' ? '?' . $query : ''));
    }
    ce_serve($root . '/ce-feeds/' . $feeds[$withSlash] . '.xml', 'application/rss+xml; charset=UTF-8');
}
if (preg_match('#^/.+/feed/?$#', $path)) {
    ce_redirect('/feed/');
}

// Pages are stored under ce-pages/ (not as directory index files) so every page
// request reaches this script: /about-us/ -> ce-pages/about-us/index.html
if ($path === '/') {
    ce_serve($root . '/ce-pages/home.html');
}
$dir = $root . '/ce-pages' . rtrim($path, '/');
if (is_file($dir . '/index.html')) {
    if (substr($path, -1) !== '/') {
        ce_redirect($path . '/' . ($query !== '' ? '?' . $query : ''));
    }
    ce_serve($dir . '/index.html');
}

ce_not_found($root);
