<?php
// Pensacola Hurricane (served on destinhurricane.com) - static site front controller. The host serves real
// files directly; anything else lands here.
$path = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$home = 'https://destinhurricane.com';

// Canonical host/scheme on the live domain (the *.hostingersite.com preview
// address is left alone and marked noindex below).
if (substr($host, -strlen('destinhurricane.com')) === 'destinhurricane.com') {
    $insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
    if ($insecure || $host === 'www.destinhurricane.com') {
        header('Location: ' . $home . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
        exit;
    }
}
if (strpos($host, 'hostingersite.com') !== false) {
    header('X-Robots-Tag: noindex, nofollow');
}

if ($path === '/' || $path === '/index.php' || $path === '/index.html') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path) && strpos($path, '..') === false) {
    header('Location: ' . $path . '/', true, 301);
    exit;
}
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
