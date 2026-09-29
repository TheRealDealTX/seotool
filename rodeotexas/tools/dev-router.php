<?php
// Local development only:  RT_CONFIG=/path/config.php php -S localhost:8080 -t public_html tools/dev-router.php
// Mimics public_html/.htaccess (static files first, then the front controller / admin).
$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if (preg_match('#^/(includes|pages)(/|$)#', $path)) { http_response_code(403); exit('Forbidden'); }
$file = $_SERVER['DOCUMENT_ROOT'] . $path;
if ($path !== '/' && is_file($file) && !str_ends_with($file, '.php')) { return false; }
if (str_starts_with($path, '/admin/') || $path === '/admin') { require $_SERVER['DOCUMENT_ROOT'] . '/admin/index.php'; return true; }
require $_SERVER['DOCUMENT_ROOT'] . '/index.php';
