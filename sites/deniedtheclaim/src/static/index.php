<?php
// deniedtheclaim.com front controller. Real files are served directly by the
// web server; "/" and every unknown URL land here (see .htaccess).
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = strtok($uri, '?');
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$apex = 'deniedtheclaim.com';

$https = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
    || ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https';
if ($host === 'www.' . $apex || ($host === $apex && !$https)) {
    header('Location: https://' . $apex . $uri, true, 301);
    exit;
}
if ($host !== $apex && $host !== '') {
    header('X-Robots-Tag: noindex, nofollow');   // temporary/preview hostnames
}

if ($path === '/' || $path === '/index.php' || $path === '/index.html') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}
if (strpos($path, '..') === false && substr($path, -1) !== '/' && is_file(__DIR__ . $path . '/index.html')) {
    header('Location: ' . $path . '/', true, 301);
    exit;
}
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
