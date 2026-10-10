<?php
// heathergreenstudios.com front controller. The host serves existing files
// directly and sends / and unknown paths here (see README, "Hosting").
$path = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');

function go($to) { header('Location: ' . $to, true, 301); exit; }

if ($host === 'www.heathergreenstudios.com') {
    go('https://heathergreenstudios.com' . ($_SERVER['REQUEST_URI'] ?? '/'));
}

if ($path === '/' || $path === '/index.php' || $path === '/index.html') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}

// Old Blogger URL shapes from the original studio blog.
if (preg_match('#^/(search|feeds)(/|$)#', $path))            go('/journal/');
if (preg_match('#^/p/.+\.html$#', $path))                     go('/about/');
if (preg_match('#^/\d{4}(/\d{2})?/?$#', $path))               go('/journal/');
if (preg_match('#^/\d{4}/\d{2}/[^/]+\.html$#', $path))        go('/journal/');
if ($path === '/blog' || $path === '/blog/')                  go('/journal/');

if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path)) {
    go($path . '/');
}

http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
