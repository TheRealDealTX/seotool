<?php
// yasminsblog.com front controller.
// Hostinger's plain php-fpm websites ignore .htaccess and send every path that
// isn't an existing file here. The old Squarespace URLs had no trailing slash
// (/mamablog/2018/1/20/slug), so each page is stored as <path>/index.html and
// served from this script at its original URL with a 200.
$canonHost = 'www.yasminsblog.com';
$host = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?'));
$qs   = $_SERVER['QUERY_STRING'] ?? '';
$live = in_array($host, ['yasminsblog.com', 'www.yasminsblog.com'], true);

function go($to) { header('Location: ' . $to, true, 301); exit; }
function serve($file) {
    header('Content-Type: text/html; charset=utf-8');
    header('Cache-Control: public, max-age=600');
    readfile($file);
    exit;
}

if ($live) {
    // TLS terminates upstream, so trust X-Forwarded-Proto.
    $insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? 'https') === 'http';
    if ($insecure || $host !== $canonHost) go('https://' . $canonHost . $uri);
} else {
    // Temporary/staging domain: keep it out of search results.
    header('X-Robots-Tag: noindex, nofollow');
}

if (strpos($path, '..') !== false || strpos($path, "\0") !== false) $path = '/404';
$path = str_replace(' ', '+', $path);            // "porto rico" -> "porto+rico" tag slugs

// Squarespace RSS: /mamablog?format=rss
if (preg_match('/(^|&)format=rss(&|$)/', $qs)) {
    header('Content-Type: application/rss+xml; charset=utf-8');
    readfile(__DIR__ . '/_pages/mamablog/feed.xml');
    exit;
}

if ($path === '/' || $path === '/index.php' || $path === '/home.html') serve(__DIR__ . '/home.html');

// Old Squarespace and common aliases.
$aliases = [
    '/home' => '/', '/blog' => '/mamablog', '/journal' => '/mamablog',
    '/about-me' => '/about', '/about-1' => '/about', '/contact-me' => '/contact',
    '/privacy' => '/privacy-policy', '/mamablog/category/photography' => '/mamablog/category/Photography',
    '/mamablog/category/food' => '/mamablog/category/Food', '/mamablog/category/culture' => '/mamablog/category/Culture',
    '/mamablog/category/travel' => '/mamablog/category/Travel', '/feed' => '/mamablog/feed.xml',
    '/mamablog/rss' => '/mamablog/feed.xml',
];
$trim = rtrim($path, '/');
if (isset($aliases[$trim])) go($aliases[$trim]);

if ($trim === '/mamablog/feed.xml') {
    header('Content-Type: application/rss+xml; charset=utf-8');
    readfile(__DIR__ . '/_pages/mamablog/feed.xml');
    exit;
}

// Canonical form has no trailing slash.
$pages = __DIR__ . '/_pages';
if ($path !== $trim && is_file($pages . $trim . '.html')) go($trim);
if (is_file($pages . $path . '.html')) serve($pages . $path . '.html');

// Case-insensitive match (/mamablog/Tag/New+York, /About etc.).
$want = strtolower($trim);
$it = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($pages, FilesystemIterator::SKIP_DOTS));
foreach ($it as $f) {
    $rel = substr($f->getPathname(), strlen($pages), -5);
    if (substr($f->getPathname(), -5) === '.html' && strtolower($rel) === $want) go($rel);
}

// /mamablog/2018/1/20/slug/extra or a wrong date -> the post with that slug.
if (preg_match('#^/mamablog/\d{4}/\d{1,2}/\d{1,2}/([^/]+)#', $path, $m)) {
    foreach (glob($pages . '/mamablog/*/*/*/' . $m[1] . '.html') ?: [] as $f) {
        go(substr($f, strlen($pages), -5));
    }
}

http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
