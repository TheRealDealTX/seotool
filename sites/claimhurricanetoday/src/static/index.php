<?php
// Claim Hurricane Today (claimhurricanetoday.com) - front controller for the static build.
// Real files and directories are served by LiteSpeed directly; everything else comes here.
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = strtok($uri, '?');
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$apex = 'claimhurricanetoday.com';

$secure = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
    || ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https';
if ($host === 'www.' . $apex || ($host === $apex && !$secure)) {
    header('Location: https://' . $apex . $uri, true, 301);
    exit;
}
if (strpos($host, 'hostingersite.com') !== false) {
    header('X-Robots-Tag: noindex, nofollow');   // temporary preview domain
}

if (in_array($path, ['/', '/index.php', '/index.html'], true)) {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}
// Directory without trailing slash -> add it.
if (substr($path, -1) !== '/' && strpos($path, '..') === false && is_dir(__DIR__ . $path)) {
    header('Location: ' . $path . '/', true, 301);
    exit;
}
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
