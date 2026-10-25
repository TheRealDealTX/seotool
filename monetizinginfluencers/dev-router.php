<?php
// Local preview only (php -S 127.0.0.1:8080 -t public dev-router.php). Mimics the .htaccess rules.
$root = __DIR__ . '/public';
$path = urldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));
if (preg_match('#^/inc/#', $path)) { http_response_code(403); exit('Forbidden'); }
$file = $root . $path;
if (is_file($file) && !str_ends_with($file, '.php')) return false;
if (is_file($file)) { chdir(dirname($file)); require $file; return true; }
if (is_dir($file)) {
    if (substr($path, -1) !== '/') { header('Location: ' . $path . '/', true, 301); exit; }
    if (is_file($file . 'index.php')) { chdir($file); require $file . 'index.php'; return true; }
}
http_response_code(404);
require $root . '/404.php';
