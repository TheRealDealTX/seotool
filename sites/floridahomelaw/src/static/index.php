<?php
// Florida Home Law (floridahomelaw.com) front controller. Real files are served
// directly by the web server; everything else is routed here by .htaccess.
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = strtok($uri, '?');
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$apex = 'https://floridahomelaw.com';

$secure = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
    || ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https';
if ($host === 'www.floridahomelaw.com' || ($host === 'floridahomelaw.com' && !$secure)) {
    header('Location: ' . $apex . $uri, true, 301);
    exit;
}
if ($host !== 'floridahomelaw.com' && $host !== '') {
    // Temporary/preview hostnames must never be indexed.
    header('X-Robots-Tag: noindex, nofollow');
}

if ($path === '/' || $path === '/index.php' || $path === '/index.html' || $path === '/home.html') {
    if ($path !== '/') {
        header('Location: ' . $apex . '/', true, 301);
        exit;
    }
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}
// /some-guide -> /some-guide/ when the folder exists
if (substr($path, -1) !== '/' && strpos($path, '..') === false && is_file(__DIR__ . $path . '/index.html')) {
    header('Location: ' . $apex . $path . '/', true, 301);
    exit;
}
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
