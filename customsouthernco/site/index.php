<?php
// customsouthernco.com - static site front controller.
// The host serves existing files directly and sends / and unknown paths here.
$path = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
$home = 'https://customsouthernco.com';

$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';   // TLS ends upstream
if ($insecure || ($_SERVER['HTTP_HOST'] ?? '') === 'www.customsouthernco.com') {
    header('Location: ' . $home . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}

if ($path === '/' || $path === '/index.php') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}
// Old WordPress-era URLs and short links -> closest new page.
$moved = [
    '/feed/' => '/blog/', '/feed' => '/blog/', '/comments/feed/' => '/blog/',
    '/d05b' => '/', '/u2ur' => '/', '/shop/' => '/', '/about-me/' => '/about/', '/contact-me/' => '/contact/',
    '/blog-2/' => '/blog/', '/home/' => '/',
];
if (isset($moved[$path])) {
    header('Location: ' . $home . $moved[$path], true, 301);
    exit;
}
if (preg_match('#^/category/[^/]+/feed/?$#', $path) || preg_match('#^/[a-z0-9-]+/feed/?$#', $path)) {
    header('Location: ' . $home . preg_replace('#feed/?$#', '', $path), true, 301);
    exit;
}
if (preg_match('#^/(wp-admin|wp-includes|wp-json|wp-content|wp-login\.php|xmlrpc\.php)(/|$)#', $path)) {
    header('Location: ' . $home . '/', true, 301);
    exit;
}
if (preg_match('#^/(tag|author|page)/#', $path) || preg_match('#^/\d{4}/\d{2}/#', $path)) {
    header('Location: ' . $home . '/blog/', true, 301);
    exit;
}
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path)) {
    header('Location: ' . $home . $path . '/', true, 301);
    exit;
}
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
