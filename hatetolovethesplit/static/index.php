<?php
// hatetolovethesplit.com front controller.
// The Hostinger platform serves existing files directly and routes "/" and
// unknown paths here, so the homepage lives in home.html and everything that
// isn't a real file gets a proper 404 (or a 301 for old WordPress URLs).
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = strtok($uri, '?');
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$canonicalHost = 'hatetolovethesplit.com';

// Once the real domain is attached: force https and drop www.
$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
if ($host === 'www.' . $canonicalHost || ($insecure && $host === $canonicalHost)) {
    header('Location: https://' . $canonicalHost . $uri, true, 301);
    exit;
}

if ($path === '/' || $path === '/index.php') {
    // Old WordPress query-string URLs (?p=123, ?cat=4, ?s=...) land on the homepage.
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}
if (preg_match('#^/(feed|rss|comments/feed)/?$#', $path) || preg_match('#^/.+/feed/?$#', $path)) {
    header('Content-Type: application/rss+xml; charset=utf-8');
    readfile(__DIR__ . '/feed.xml');
    exit;
}
if (preg_match('#^/(wp-admin|wp-includes|wp-json|wp-login\.php|xmlrpc\.php|wp-content)(/|$)#', $path)) {
    header('Location: /', true, 301);
    exit;
}
// Old WordPress "page/N" on the homepage -> archive
if (preg_match('#^/page/\d+/?$#', $path)) {
    header('Location: /archives/', true, 301);
    exit;
}
// Missing trailing slash on a real directory
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path) && strpos($path, '..') === false) {
    header('Location: ' . $path . '/' . (strpos($uri, '?') !== false ? substr($uri, strpos($uri, '?')) : ''), true, 301);
    exit;
}
// Paginated tag/date URLs that don't exist any more -> their first page
if (preg_match('#^(/(?:tag|category|\d{4}(?:/\d{2})?)/[^?]*?)page/\d+/?$#', $path, $m) && is_dir(__DIR__ . $m[1])) {
    header('Location: ' . $m[1], true, 301);
    exit;
}
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
