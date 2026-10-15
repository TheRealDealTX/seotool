<?php
// thepropertylaw.com front controller. Real files and directories are served by
// LiteSpeed directly (see .htaccess); "/" and every unknown URL land here.
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = strtok($uri, '?');
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$apex = 'https://thepropertylaw.com';

$secure = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
    || ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https';
if ($host === 'www.thepropertylaw.com' || ($host === 'thepropertylaw.com' && !$secure)) {
    header('Location: ' . $apex . $uri, true, 301);
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
// "/guide" -> "/guide/" when the directory exists.
if (substr($path, -1) !== '/' && strpos($path, '..') === false && is_dir(__DIR__ . $path)) {
    header('Location: ' . $path . '/', true, 301);
    exit;
}
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
