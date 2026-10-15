<?php
// hurricaneflood.com front controller. Real files are served directly by the
// web server; .htaccess routes "/" and every unknown URL here.
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = strtok($uri, '?');
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$origin = 'https://hurricaneflood.com';

$https = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
    || ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https';
if ($host === 'www.hurricaneflood.com' || ($host === 'hurricaneflood.com' && !$https)) {
    header('Location: ' . $origin . $uri, true, 301);
    exit;
}
if (strpos($host, 'hostingersite.com') !== false) {
    header('X-Robots-Tag: noindex, nofollow');
}

if ($path === '/' || $path === '/index.php' || $path === '/index.html') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}
// Directory without trailing slash -> canonical slash URL.
if (substr($path, -1) !== '/' && strpos($path, '..') === false && is_file(__DIR__ . $path . '/index.html')) {
    header('Location: ' . $origin . $path . '/', true, 301);
    exit;
}
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
