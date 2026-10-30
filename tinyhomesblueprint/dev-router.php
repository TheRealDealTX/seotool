<?php
// Local preview: php -S localhost:8000 -t site dev-router.php
// Serves real files directly and sends everything else through the front controller,
// like the .htaccess rules do on the server.
$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if ($path !== '/' && is_file(__DIR__ . '/site' . $path)) return false;
$_SERVER['HTTPS'] = 'on';
require __DIR__ . '/site/index.php';
