<?php
// dogwooddiy.com - static site front controller.
// The host routes "/" and unknown paths here; every real page is a static file.
$path = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
$home = 'https://dogwooddiy.com';

// Canonical host and scheme (TLS ends upstream, so check the forwarded proto).
$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
if ($insecure || ($_SERVER['HTTP_HOST'] ?? '') === 'www.dogwooddiy.com') {
    header('Location: ' . $home . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}

if ($path === '/' || $path === '/index.php') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}

// Old WordPress URLs.
$moved = [
    '/about' => '/about/',
    '/blog' => '/blog/',
    '/contact' => '/contact/',
    '/disclosure/' => '/disclaimer/',
    '/privacy/' => '/privacy-policy/',
    '/category/home-improvement/' => '/category/home-renovation/',
    '/category/diy/' => '/category/home-renovation/',
    '/category/garden/' => '/category/garden-outdoor/',
    '/category/gardening/' => '/category/garden-outdoor/',
    '/category/outdoor/' => '/category/garden-outdoor/',
    '/category/decor/' => '/category/decor-design/',
    '/category/uncategorized/' => '/blog/',
];
if (isset($moved[$path])) {
    header('Location: ' . $home . $moved[$path], true, 301);
    exit;
}
if (preg_match('#^/(feed|comments/feed)/?$#', $path) || preg_match('#^/page/\d+/?$#', $path)) {
    header('Location: ' . $home . '/blog/', true, 301);
    exit;
}
if (preg_match('#^/([a-z0-9-]+)/(feed|amp|comment-page-\d+)/?$#', $path, $m) && is_dir(__DIR__ . '/' . $m[1])) {
    header('Location: ' . $home . '/' . $m[1] . '/', true, 301);
    exit;
}
if (preg_match('#^/(wp-admin|wp-includes|wp-json|wp-login\.php|xmlrpc\.php)(/|$)#', $path)) {
    header('Location: ' . $home . '/', true, 301);
    exit;
}
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path)) {
    header('Location: ' . $home . $path . '/', true, 301);
    exit;
}
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
