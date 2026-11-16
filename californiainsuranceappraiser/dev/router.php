<?php
// Local router that mimics the Hostinger host: real files are served directly (a directory's
// index.php is executed), everything else goes to the root index.php front controller.
// Usage: cd public && php -S 127.0.0.1:8099 ../dev/router.php
$root = $_SERVER['DOCUMENT_ROOT'];
$path = rawurldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));
$full = $root . $path;
if ($path !== '/' && is_file($full)) {
    if (substr($full, -4) === '.php') { chdir(dirname($full)); $_SERVER['SCRIPT_FILENAME'] = $full; require $full; return true; }
    return false;
}
if ($path !== '/' && substr($path, -1) === '/' && is_file($full . 'index.php')) {
    $_SERVER['SCRIPT_FILENAME'] = $full . 'index.php'; chdir($full); require $full . 'index.php'; return true;
}
$_SERVER['SCRIPT_FILENAME'] = $root . '/index.php';
require $root . '/index.php';
