<?php
// connectedrenter.com - static site front controller.
// The host serves existing files directly and routes "/" and unknown paths here
// (it ignores .htaccess), so the homepage is home.html and everything else 404s properly.
$path = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
$home = 'https://connectedrenter.com';
$host = $_SERVER['HTTP_HOST'] ?? '';

// Canonical scheme and host (only once the real domain is live; preview domains pass through).
$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
if (($host === 'connectedrenter.com' && $insecure) || $host === 'www.connectedrenter.com') {
    header('Location: ' . $home . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}

if ($path === '/' || $path === '/index.php') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}

// Old WordPress / WooCommerce URLs -> nearest static page.
$redirects = [
    '#^/(feed|comments/feed)/?$#' => '/blog/',
    '#^/contact/?$#' => '/contact-us/',
    '#^/(cart|checkout|my-account)/?$#' => '/shop/',
    '#^/product/.*$#' => '/shop/',
    '#^/(category|tag|author)/.*$#' => '/blog/',
    '#^/(wp-admin|wp-includes|wp-json|wp-login\.php|xmlrpc\.php)(/|$)#' => '/',
];
foreach ($redirects as $re => $to) {
    if (preg_match($re, $path)) {
        header('Location: ' . $home . $to, true, 301);
        exit;
    }
}
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path)) {
    header('Location: ' . $home . $path . '/', true, 301);
    exit;
}
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
