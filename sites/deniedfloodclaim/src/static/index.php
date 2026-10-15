<?php
// deniedfloodclaim.com front controller. Real files are served by the web server;
// "/" and every unknown URL land here (see .htaccess).
$uri = $_SERVER['REQUEST_URI'] ?? '/';
$path = strtok($uri, '?');
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$origin = 'https://deniedfloodclaim.com';

$https = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
    || ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https';
if ($host === 'www.deniedfloodclaim.com' || ($host === 'deniedfloodclaim.com' && !$https)) {
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
// Directory without trailing slash -> add it.
if (substr($path, -1) !== '/' && strpos($path, '..') === false && is_file(__DIR__ . $path . '/index.html')) {
    header('Location: ' . $path . '/', true, 301);
    exit;
}
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
