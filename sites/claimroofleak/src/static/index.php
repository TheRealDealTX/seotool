<?php
// claimroofleak.com front controller: serves home.html for "/", adds a trailing
// slash to real directories, and returns a real 404 page for everything else.
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?'));
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$apex = 'claimroofleak.com';

$secure = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
    || ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https';
if ($host === 'www.' . $apex || ($host === $apex && !$secure)) {
    header('Location: https://' . $apex . $uri, true, 301);
    exit;
}
if ($host !== $apex && $host !== '') {
    header('X-Robots-Tag: noindex, nofollow');   // temporary/preview hostnames
}

if (in_array($path, ['/', '/index.php', '/index.html', '/home.html'], true)) {
    if ($path !== '/') {
        header('Location: /', true, 301);
        exit;
    }
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
