<?php
// huttoroofs.com - static site front controller. See README, "Hosting note".
$path = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
$home = 'https://huttoroofs.com';

if ($path === '/' || $path === '/index.php') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}
if (preg_match('#^/(feed|comments/feed)/?$#', $path)) {
    header('Location: ' . $home . '/blog/', true, 301);
    exit;
}
if (preg_match('#^/(wp-admin|wp-includes|wp-json|wp-login\.php|xmlrpc\.php)(/|$)#', $path)) {
    header('Location: ' . $home . '/', true, 301);
    exit;
}
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path)) {
    header('Location: ' . $home . $path . '/', true, 301);
    exit;
}
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
