<?php
// Local test router for `php -S 127.0.0.1:8099 -t public router.php` that mimics the Hostinger setup:
// real files are served directly (PHP files executed), a directory's index.php is executed,
// everything else falls through to the root index.php front controller.
$path = rawurldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));
$file = __DIR__ . '/public' . $path;
if ($path !== '/' && is_file($file)) {
    if (substr($file, -4) === '.php') { $_SERVER['SCRIPT_FILENAME'] = $file; chdir(dirname($file)); require $file; return true; }
    return false;
}
if (substr($path, -1) === '/' && $path !== '/' && is_file($file . 'index.php')) {
    $_SERVER['SCRIPT_FILENAME'] = $file . 'index.php'; chdir(dirname($file . 'index.php')); require $file . 'index.php'; return true;
}
$_SERVER['SCRIPT_FILENAME'] = __DIR__ . '/public/index.php';
require __DIR__ . '/public/index.php';
