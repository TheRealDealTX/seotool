<?php
// zibetti.co - static site front controller.
// The host serves existing files directly and routes "/" plus unknown paths here.
$path = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
// Local preview with `php -S`: let the built-in server hand out real files.
if (PHP_SAPI === 'cli-server' && $path !== '/' && is_file(__DIR__ . $path)) {
    return false;
}
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$home = 'https://zibetti.co';

// Canonical host and scheme once the real domain is connected (preview domains are left alone).
$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
if ($host === 'www.zibetti.co' || ($host === 'zibetti.co' && $insecure)) {
    header('Location: ' . $home . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}

if ($path === '/' || $path === '/index.php') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}

// Old-site URLs -> their new homes.
$map = [
    '#^/home/?$#' => '/',
    '#^/index\.html?$#' => '/',
    '#^/shop/?$#' => '/',
    '#^/(feed|comments/feed)/?$#' => '/blog/',
    '#^/\d{4}/\d{2}/\d{2}/[^/]+/?$#' => '/blog/',
    '#^/\d{4}(/\d{2})?/?$#' => '/blog/',
    '#^/(category|tag|author)/.*$#' => '/blog/',
    '#^/blog/page/\d+/?$#' => '/blog/',
    '#^/(contact|inquire)/?$#' => '/contact-us/',
    '#^/(about)/?$#' => '/about-us/',
    '#^/(investment|prices)/?$#' => '/pricing/',
    '#^/(films?|videos)/?$#' => '/video/',
    '#^/(gallery|work)/?$#' => '/portfolio/',
    '#^/(wp-admin|wp-includes|wp-json|wp-login\.php|xmlrpc\.php)(/|$)#' => '/',
];
foreach ($map as $re => $to) {
    if (preg_match($re, $path)) {
        header('Location: ' . $to, true, 301);
        exit;
    }
}

// Directory without trailing slash -> add it.
if (substr($path, -1) !== '/' && strpos($path, '..') === false && is_dir(__DIR__ . $path)) {
    header('Location: ' . $path . '/', true, 301);
    exit;
}
// Directory with trailing slash that reached us (index.html not auto-served) -> serve it.
if (substr($path, -1) === '/' && strpos($path, '..') === false && is_file(__DIR__ . $path . 'index.html')) {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . $path . 'index.html');
    exit;
}

http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
