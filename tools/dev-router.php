<?php
// Local preview: php -S localhost:8080 -t public tools/dev-router.php
$f = __DIR__ . '/../public' . parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if (is_file($f) && !preg_match('#/(inc|content|pages)/#', $f) && basename($f) !== 'index.php') return false;
$_SERVER['HTTP_X_FORWARDED_PROTO'] = 'https';
$_SERVER['HTTP_HOST'] = 'solarcctvcamera.com';
require __DIR__ . '/../public/index.php';
