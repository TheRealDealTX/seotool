<?php
// kotric.com - static site front controller.
// The host serves existing files directly and routes "/" and unknown paths here,
// so the homepage lives in home.html (an index.html would swallow every 404).
$path = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
$home = 'https://kotric.com';
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');

// Canonical scheme and host (TLS terminates upstream, so check X-Forwarded-Proto).
$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
if ($host === 'www.kotric.com' || ($insecure && $host === 'kotric.com')) {
    header('Location: ' . $home . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}

if ($path === '/' || $path === '/index.php') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}

// Old WordPress-era URLs.
$redirects = [
    '/feed/' => '/blog/',
    '/comments/feed/' => '/blog/',
    '/blog/page/2/' => '/blog/',
    '/category/no-sew/' => '/no-sew-fabric-craft-projects/',
    '/no-sew-fabric-projects/' => '/no-sew-fabric-craft-projects/',
    '/41-no-sew-fabric-projects/' => '/no-sew-fabric-craft-projects/',
    '/contact-us/' => '/contact/',
    '/about-us/' => '/about/',
    '/privacy/' => '/privacy-policy/',
    '/terms/' => '/terms-of-use/',
    '/terms-and-conditions/' => '/terms-of-use/',
];
$key = rtrim($path, '/') . '/';
if (isset($redirects[$key])) {
    header('Location: ' . $home . $redirects[$key], true, 301);
    exit;
}
if (preg_match('#^/(wp-admin|wp-includes|wp-json|wp-login\.php|xmlrpc\.php)(/|$)#', $path)) {
    header('Location: ' . $home . '/', true, 301);
    exit;
}
if (preg_match('#^/(page|author|tag)/#', $path) || preg_match('#^/category/[^/]+/page/#', $path)) {
    header('Location: ' . $home . '/blog/', true, 301);
    exit;
}
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path)) {
    header('Location: ' . $home . $path . '/', true, 301);
    exit;
}
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
