<?php
// deniedclaimlaw.com front controller. Real files are served directly by the
// web server; "/" and every unknown URL land here (see .htaccess).
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = strtok($uri, '?');
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$apex = 'https://deniedclaimlaw.com';

$https = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
    || ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https';
if ($host === 'www.deniedclaimlaw.com' || ($host === 'deniedclaimlaw.com' && !$https)) {
    header('Location: ' . $apex . $uri, true, 301);
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
if (substr($path, -1) !== '/' && strpos($path, '..') === false && is_dir(__DIR__ . $path)) {
    header('Location: ' . $path . '/', true, 301);
    exit;
}
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
