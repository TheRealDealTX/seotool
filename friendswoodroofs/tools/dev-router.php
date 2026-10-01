<?php
// Local preview only (not deployed): emulates the .htaccess rewrite rules.
//   php -S 127.0.0.1:8080 -t public_html tools/dev-router.php
$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$file = __DIR__ . '/../public_html' . $path;
if ($path !== '/' && is_file($file) && !str_ends_with($file, '.php')) {
    return false; // let the built-in server send the static file
}
require __DIR__ . '/../public_html/index.php';
