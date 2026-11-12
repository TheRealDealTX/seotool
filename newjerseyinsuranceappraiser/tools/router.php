<?php
// Local dev router that mimics the Hostinger setup: real files are served directly (a directory's
// index.php is executed), everything else goes to the root index.php front controller.
// Usage: php -S 127.0.0.1:8090 -t public tools/router.php
$root = $_SERVER['DOCUMENT_ROOT'];
$path = rawurldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));
$f = $root . $path;
if ($path !== '/' && is_file($f)) {
    if (substr($f, -4) === '.php') { $_SERVER['SCRIPT_FILENAME'] = $f; chdir(dirname($f)); require $f; return true; }
    return false; // static file
}
if (substr($path, -1) === '/' && $path !== '/' && is_file($f . 'index.php')) {
    $_SERVER['SCRIPT_FILENAME'] = $f . 'index.php'; chdir(dirname($f . 'index.php')); require $f . 'index.php'; return true;
}
$_SERVER['SCRIPT_FILENAME'] = $root . '/index.php';
require $root . '/index.php';
return true;
