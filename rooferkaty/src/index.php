<?php
// rooferkaty.com - front controller. Serves the homepage for "/", adds
// trailing slashes to folder URLs and returns a real 404 for everything else.
// (Works whether or not the host honors .htaccess.)
$path = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
$home = 'https://rooferkaty.com';
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');

if (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http' || $host === 'www.rooferkaty.com') {
    header('Location: ' . $home . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
if ($path === '/' || $path === '/index.php' || $path === '/index.html') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}
$clean = '/' . trim(str_replace('..', '', $path), '/');
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $clean) && is_file(__DIR__ . $clean . '/index.html')) {
    header('Location: ' . $clean . '/', true, 301);
    exit;
}
if (substr($path, -1) === '/' && is_file(__DIR__ . $clean . '/index.html')) {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . $clean . '/index.html');
    exit;
}
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
