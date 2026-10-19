<?php
// kotric.com - front controller for every page.
//
// The host serves existing files directly (and ignores .htaccess), so the HTML pages
// live in _pages/ under paths no page links to, and every page URL reaches this
// script instead. That lets us 301 http:// and www. to https://kotric.com and return
// real 404s. robots.txt blocks /_pages/. Assets (CSS, JS, images, icons) are served directly.
$home  = 'https://kotric.com';
$uri   = $_SERVER['REQUEST_URI'] ?? '/';
$path  = rawurldecode(strtok($uri, '?'));
$host  = strtolower($_SERVER['HTTP_HOST'] ?? '');
$pages = __DIR__ . '/_pages';

function send_redirect($to) {
    header('Location: ' . $to, true, 301);
    header('Cache-Control: public, max-age=86400');
    exit;
}

// Canonical scheme and host (TLS terminates upstream, so check X-Forwarded-Proto).
$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
if ($host === 'www.kotric.com' || ($insecure && $host === 'kotric.com')) {
    send_redirect($home . $uri);
}

// Old WordPress-era URLs.
$redirects = [
    '/index.php/' => '/',
    '/home.html/' => '/',
    '/blog/page/2/' => '/blog/',
    '/category/no-sew/' => '/no-sew-fabric-craft-projects/',
    '/no-sew-fabric-projects/' => '/no-sew-fabric-craft-projects/',
    '/41-no-sew-fabric-projects/' => '/no-sew-fabric-craft-projects/',
    '/contact-us/' => '/contact/',
    '/about-us/' => '/about/',
    '/privacy/' => '/privacy-policy/',
    '/terms/' => '/terms-of-use/',
    '/terms-and-conditions/' => '/terms-of-use/',
    '/comments/feed/' => '/feed/',
];
$key = rtrim($path, '/') . '/';
if (isset($redirects[$key])) {
    send_redirect($home . $redirects[$key]);
}
if (preg_match('#^/(wp-admin|wp-includes|wp-content|wp-json|wp-login\.php|xmlrpc\.php)(/|$)#', $path)) {
    send_redirect($home . '/');
}
if (preg_match('#^/(page|author|tag)/#', $path) || preg_match('#^/category/[^/]+/page/#', $path)
    || preg_match('#^/[^/]+/(feed|amp)/?$#', $path)) {
    send_redirect($home . '/blog/');
}

function serve($file, $type) {
    $mtime = filemtime($file);
    $etag  = '"' . md5($mtime . filesize($file)) . '"';
    header('Content-Type: ' . $type);
    header('Cache-Control: public, max-age=600');
    header('Last-Modified: ' . gmdate('D, d M Y H:i:s', $mtime) . ' GMT');
    header('ETag: ' . $etag);
    if (($_SERVER['HTTP_IF_NONE_MATCH'] ?? '') === $etag) {
        http_response_code(304);
        exit;
    }
    if (($_SERVER['REQUEST_METHOD'] ?? 'GET') !== 'HEAD') {
        readfile($file);
    }
    exit;
}

if ($key === '/feed/' && is_file($pages . '/feed.xml')) {
    if (substr($path, -1) !== '/') send_redirect($home . '/feed/');
    serve($pages . '/feed.xml', 'application/rss+xml; charset=utf-8');
}

// Only plain slug paths map to pages; anything with dots or traversal is a 404.
if (preg_match('#^/([a-z0-9-]+/)*$#', $key)) {
    $file = $pages . ($key === '/' ? '/index.html' : $key . 'index.html');
    if (is_file($file)) {
        if (substr($path, -1) !== '/') send_redirect($home . $key);
        serve($file, 'text/html; charset=utf-8');
    }
}

http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
header('Cache-Control: no-cache');
readfile(is_file($pages . '/404.html') ? $pages . '/404.html' : __DIR__ . '/404.html');
